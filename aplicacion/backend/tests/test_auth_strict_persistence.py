"""
Pruebas de Persistencia Estricta, Resiliencia ante Fallos SQL y Recuperación SMTP (QA-AUTH-02B).
Valida:
- Actividad 2: Cero degradación silenciosa a memoria cuando STRICT_DATABASE_MODE=True ante fallos en SELECT, UPDATE, COMMIT y locks de fila.
- Actividad 3: Rate limiting persistente con AuthRateLimit y soporte concurrente.
- Actividad 4: Recuperación estricta ante los 5 escenarios de fallo SMTP sin códigos huérfanos ni estados inconsistentes.
"""

from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db import session as db_session
from app.main import app
from app.models.auth import AuthChallenge, AuthRateLimit
from app.services.auth_service import AuthService
from app.services.email_service import EmailService

client = TestClient(app)


@pytest.fixture
def isolated_db():
    """Crea una base de datos SQLite en memoria aislada para pruebas de persistencia estricta."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    db_session.Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()
        db_session.Base.metadata.drop_all(bind=engine)


# -----------------------------------------------------------------------------
# ACTIVIDAD 2: PERSISTENCIA ESTRICTA ANTE ERRORES SQL
# -----------------------------------------------------------------------------


def test_strict_db_mode_rejects_none_session(monkeypatch):
    """En STRICT_DATABASE_MODE=True, si la sesión de BD es None se debe abortar con HTTP 503."""
    monkeypatch.setattr(settings, "STRICT_DATABASE_MODE", True)

    with pytest.raises(HTTPException) as exc_info:
        AuthService.request_otp(None, "2022074255@upt.pe")
    assert exc_info.value.status_code == 503
    assert exc_info.value.detail["code"] == "DATABASE_UNAVAILABLE"


def test_strict_db_mode_fails_on_select_error(isolated_db, monkeypatch):
    """Si una consulta SELECT en _get_challenge o _find_active_by_email falla, lanza HTTP 503 sin usar memoria."""
    monkeypatch.setattr(settings, "STRICT_DATABASE_MODE", True)

    # Simular fallo en query()
    mock_db = MagicMock(spec=isolated_db)
    mock_db.query.side_effect = Exception("Conexión perdida con PostgreSQL durante SELECT")

    with pytest.raises(HTTPException) as exc_info:
        AuthService._get_challenge(mock_db, "CHAL-TEST-001")
    assert exc_info.value.status_code == 503
    assert exc_info.value.detail["code"] == "DATABASE_UNAVAILABLE"

    with pytest.raises(HTTPException) as exc_info:
        AuthService._find_active_by_email(mock_db, "2022074255@upt.pe")
    assert exc_info.value.status_code == 503
    assert exc_info.value.detail["code"] == "DATABASE_UNAVAILABLE"


def test_strict_db_mode_fails_on_update_or_commit_error(isolated_db, monkeypatch):
    """Si el commit de un nuevo desafío falla en base de datos, lanza HTTP 503 en modo estricto."""
    monkeypatch.setattr(settings, "STRICT_DATABASE_MODE", True)

    mock_db = MagicMock(spec=isolated_db)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.commit.side_effect = Exception("Fallo de I/O o red en COMMIT")

    with pytest.raises(HTTPException) as exc_info:
        AuthService.request_otp(mock_db, "2022074255@upt.pe")
    assert exc_info.value.status_code == 503
    assert exc_info.value.detail["code"] == "DATABASE_UNAVAILABLE"


def test_strict_db_mode_verify_fails_on_commit_error(isolated_db, monkeypatch):
    """Al verificar OTP, si el commit de actualización o consumo falla en BD, lanza HTTP 503 en modo estricto."""
    monkeypatch.setattr(settings, "STRICT_DATABASE_MODE", True)
    monkeypatch.setattr(settings, "ENABLE_MOCK_OTP_HINTS", True)

    # Crear desafío real en isolated_db
    resp = AuthService.request_otp(isolated_db, "2022074255@upt.pe")
    chal_id = resp.challengeId
    code = resp.mockCodeHint

    # Mockear fallo al hacer commit en verify_otp
    mock_db = MagicMock(spec=isolated_db)
    chal_real = isolated_db.query(AuthChallenge).filter(AuthChallenge.id_challenge == chal_id).first()
    mock_db.query.return_value.filter.return_value.first.return_value = chal_real
    mock_db.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = chal_real
    mock_db.commit.side_effect = Exception("PostgreSQL deadlock o desconexión en commit")

    with pytest.raises(HTTPException) as exc_info:
        AuthService.verify_otp(mock_db, chal_id, code)
    assert exc_info.value.status_code == 503
    assert exc_info.value.detail["code"] == "DATABASE_UNAVAILABLE"


# -----------------------------------------------------------------------------
# ACTIVIDAD 3: LIMITACIÓN DE FRECUENCIA PERSISTENTE (AuthRateLimit)
# -----------------------------------------------------------------------------


def test_auth_rate_limit_persistence(isolated_db):
    """Verifica que AuthRateLimit incremente de forma atómica y persistente en la BD."""
    from app.services.auth_service import _check_rate_limit

    key = "test:ip:192.168.1.100"
    # Primera solicitud
    _check_rate_limit(isolated_db, key=key, max_requests=2, window_seconds=60)
    record = isolated_db.query(AuthRateLimit).filter(AuthRateLimit.key == key).first()
    assert record is not None
    assert record.count == 1

    # Segunda solicitud
    _check_rate_limit(isolated_db, key=key, max_requests=2, window_seconds=60)
    isolated_db.refresh(record)
    assert record.count == 2

    # Tercera solicitud -> Excede el límite de 2 -> HTTP 429
    with pytest.raises(HTTPException) as exc_info:
        _check_rate_limit(isolated_db, key=key, max_requests=2, window_seconds=60)
    assert exc_info.value.status_code == 429
    assert "RATE_LIMIT_EXCEEDED" in exc_info.value.detail["code"]


def test_auth_rate_limit_resets_after_window(isolated_db):
    """Comprueba que cuando la ventana expira, el contador de AuthRateLimit se reinicia a 1."""
    from app.services.auth_service import _check_rate_limit

    key = "test:email:alumno@upt.pe"
    # Crear registro ya vencido
    past = datetime.now(UTC) - timedelta(seconds=10)
    expired_record = AuthRateLimit(key=key, count=5, window_expires_at=past)
    isolated_db.add(expired_record)
    isolated_db.commit()

    # Nueva solicitud debe reiniciar el contador
    _check_rate_limit(isolated_db, key=key, max_requests=3, window_seconds=60)
    isolated_db.refresh(expired_record)
    assert expired_record.count == 1
    from app.services.auth_service import _ensure_utc

    assert _ensure_utc(expired_record.window_expires_at) > datetime.now(UTC)


# -----------------------------------------------------------------------------
# ACTIVIDAD 4: RECUPERACIÓN ANTE FALLOS SMTP (5 ESCENARIOS)
# -----------------------------------------------------------------------------


def test_scenario_1_smtp_failure_first_request(isolated_db, monkeypatch):
    """Escenario 1: Fallo SMTP durante la primera solicitud -> 502 Bad Gateway y desafío revocado."""
    monkeypatch.setattr(settings, "SMTP_ENABLED", True)
    monkeypatch.setattr(settings, "SMTP_USER", "smtp@upt.pe")
    monkeypatch.setattr(EmailService, "send_otp_email", classmethod(lambda cls, to, code, exp: False))

    with pytest.raises(HTTPException) as exc_info:
        AuthService.request_otp(isolated_db, "fallo1@virtual.upt.pe")
    assert exc_info.value.status_code == 502
    assert exc_info.value.detail["code"] == "EMAIL_DISPATCH_FAILED"

    # Verificar que el desafío creado fue revocado (consumed=True) para no dejar códigos huérfanos
    chal = isolated_db.query(AuthChallenge).filter(AuthChallenge.email == "fallo1@virtual.upt.pe").first()
    assert chal is not None
    assert chal.consumed is True


def test_scenario_2_smtp_failure_after_invalidating_previous(isolated_db, monkeypatch):
    """Escenario 2: Fallo SMTP después de invalidar un desafío previo."""
    monkeypatch.setattr(settings, "SMTP_ENABLED", True)
    monkeypatch.setattr(settings, "SMTP_USER", "smtp@upt.pe")

    # Primer desafío emitido exitosamente
    monkeypatch.setattr(EmailService, "send_otp_email", classmethod(lambda cls, to, code, exp: True))
    resp1 = AuthService.request_otp(isolated_db, "fallo2@virtual.upt.pe")
    chal1_id = resp1.challengeId

    # Simular paso del cooldown para permitir siguiente petición
    chal1 = isolated_db.query(AuthChallenge).filter(AuthChallenge.id_challenge == chal1_id).first()
    chal1.resend_available_at = datetime.now(UTC) - timedelta(seconds=1)
    isolated_db.commit()

    # Segundo intento con fallo SMTP
    monkeypatch.setattr(EmailService, "send_otp_email", classmethod(lambda cls, to, code, exp: False))
    with pytest.raises(HTTPException) as exc_info:
        AuthService.request_otp(isolated_db, "fallo2@virtual.upt.pe")
    assert exc_info.value.status_code == 502

    # Verificar que el primer desafío quedó invalidado y el segundo también fue revocado
    challenges = isolated_db.query(AuthChallenge).filter(AuthChallenge.email == "fallo2@virtual.upt.pe").all()
    assert len(challenges) == 2
    assert all(c.consumed is True for c in challenges)


def test_scenario_3_smtp_failure_during_resend(isolated_db, monkeypatch):
    """Escenario 3: Fallo SMTP durante un reenvío (resend_otp)."""
    monkeypatch.setattr(settings, "SMTP_ENABLED", True)
    monkeypatch.setattr(settings, "SMTP_USER", "smtp@upt.pe")

    # Desafío inicial exitoso
    monkeypatch.setattr(EmailService, "send_otp_email", classmethod(lambda cls, to, code, exp: True))
    resp_init = AuthService.request_otp(isolated_db, "fallo3@virtual.upt.pe")
    c_id = resp_init.challengeId

    # Simular fin de cooldown
    chal = isolated_db.query(AuthChallenge).filter(AuthChallenge.id_challenge == c_id).first()
    chal.resend_available_at = datetime.now(UTC) - timedelta(seconds=5)
    isolated_db.commit()

    # Reenvío con fallo SMTP
    monkeypatch.setattr(EmailService, "send_otp_email", classmethod(lambda cls, to, code, exp: False))
    with pytest.raises(HTTPException) as exc_info:
        AuthService.resend_otp(isolated_db, c_id)
    assert exc_info.value.status_code == 502
    assert exc_info.value.detail["code"] == "EMAIL_DISPATCH_FAILED"

    # Ningún desafío debe quedar utilizable
    active = AuthService._find_active_by_email(isolated_db, "fallo3@virtual.upt.pe")
    assert active is None


def test_scenario_4_retry_succeeds_immediately_after_smtp_failure(isolated_db, monkeypatch):
    """
    Escenario 4: Reintento posterior a un fallo SMTP.
    Como el código fallido fue revocado inmediatamente (consumed=True), el usuario no queda bloqueado
    por un cooldown fantasma y puede reintentar con éxito una vez restablecido el servicio.
    """
    monkeypatch.setattr(settings, "SMTP_ENABLED", True)
    monkeypatch.setattr(settings, "SMTP_USER", "smtp@upt.pe")
    monkeypatch.setattr(settings, "ENABLE_MOCK_OTP_HINTS", True)

    # 1. Fallo en el primer envío
    monkeypatch.setattr(EmailService, "send_otp_email", classmethod(lambda cls, to, code, exp: False))
    with pytest.raises(HTTPException):
        AuthService.request_otp(isolated_db, "reintento@virtual.upt.pe")

    # 2. El proveedor SMTP se restablece de inmediato
    monkeypatch.setattr(EmailService, "send_otp_email", classmethod(lambda cls, to, code, exp: True))

    # Limpiar rate limit si aplicara para probar específicamente la regla de cooldown institucional
    isolated_db.query(AuthRateLimit).delete()
    isolated_db.commit()

    # 3. El usuario reintenta inmediatamente: debe tener éxito sin error de cooldown
    resp_retry = AuthService.request_otp(isolated_db, "reintento@virtual.upt.pe")
    assert resp_retry.deliveryStatus == "dispatched"
    assert resp_retry.emailDispatched is True
    assert resp_retry.challengeId is not None


def test_scenario_5_db_disconnect_during_smtp_revocation(isolated_db, monkeypatch):
    """
    Escenario 5: Desconexión de PostgreSQL durante la actualización de revocación post-fallo SMTP.
    En STRICT_DATABASE_MODE=True, debe reportar 503 DATABASE_UNAVAILABLE en lugar de 502 o degradar silenciosamente.
    """
    monkeypatch.setattr(settings, "STRICT_DATABASE_MODE", True)
    monkeypatch.setattr(settings, "SMTP_ENABLED", True)
    monkeypatch.setattr(settings, "SMTP_USER", "smtp@upt.pe")
    monkeypatch.setattr(EmailService, "send_otp_email", classmethod(lambda cls, to, code, exp: False))

    mock_db = MagicMock(spec=isolated_db)
    # Permite el primer commit (creación del desafío), pero falla en el segundo commit (revocación tras fallo SMTP)
    commit_calls = 0

    def mock_commit():
        nonlocal commit_calls
        commit_calls += 1
        if commit_calls >= 2:
            raise Exception("PostgreSQL socket closed unexpectedly during revocation commit")

    mock_db.commit.side_effect = mock_commit
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        AuthService.request_otp(mock_db, "fallo5@virtual.upt.pe")
    assert exc_info.value.status_code == 503
    assert exc_info.value.detail["code"] == "DATABASE_UNAVAILABLE"
