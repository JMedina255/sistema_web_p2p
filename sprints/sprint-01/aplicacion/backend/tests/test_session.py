from unittest.mock import MagicMock, patch

import pytest

from app.core.config import settings
from app.db import session as db_session


def test_get_engine_returns_none_when_unconfigured():
    """Valida que get_engine() devuelve None si no hay URL configurada."""
    db_session.close_engine()
    assert db_session.get_engine() is None


def test_get_engine_initializes_and_caches(monkeypatch):
    """Valida que get_engine() crea e inicializa el motor con SQLite en memoria y lo reutiliza."""
    monkeypatch.setattr(settings, "DATABASE_URL", "sqlite:///:memory:")
    db_session.close_engine()

    engine1 = db_session.get_engine()
    assert engine1 is not None
    engine2 = db_session.get_engine()
    assert engine1 is engine2

    db_session.close_engine()
    assert db_session._engine is None


def test_get_session_raises_runtime_error_when_unconfigured():
    """Valida que get_session() lanza RuntimeError si la base de datos no está configurada."""
    db_session.close_engine()
    gen = db_session.get_session()
    with pytest.raises(RuntimeError, match="No se ha configurado la variable DATABASE_URL"):
        next(gen)


def test_get_session_yields_and_closes_session(monkeypatch):
    """Valida que get_session() provee una sesión activa y la cierra al finalizar."""
    monkeypatch.setattr(settings, "DATABASE_URL", "sqlite:///:memory:")
    db_session.close_engine()

    gen = db_session.get_session()
    session = next(gen)
    assert session is not None

    with pytest.raises(StopIteration):
        next(gen)


def test_close_engine_is_idempotent():
    """Valida que close_engine() puede ser ejecutado múltiples veces sin fallar."""
    db_session.close_engine()
    db_session.close_engine()
    assert db_session._engine is None
    assert db_session._SessionLocal is None


def test_sanitize_db_error_protects_secrets():
    """Valida que sanitize_db_error no expone contraseñas ficticias ni tokens sensibles."""
    fake_secret = "super_secret_supabase_token_999!"

    # 1. Error de autenticación con contraseña
    err_auth = Exception(f"password authentication failed for user postgres with password: {fake_secret}")
    sanitized_auth = db_session.sanitize_db_error(err_auth)
    assert fake_secret not in sanitized_auth
    assert "credenciales de PostgreSQL" in sanitized_auth

    # 2. Timeout
    err_timeout = Exception(
        f"Connection timed out after 5000ms url=postgresql://user:{fake_secret}@db.supabase.co"
    )
    sanitized_timeout = db_session.sanitize_db_error(err_timeout)
    assert fake_secret not in sanitized_timeout
    assert "timeout" in sanitized_timeout.lower()

    # 3. DNS / Hostname
    err_dns = Exception(f"could not translate host name db.supabase.co for secret={fake_secret}")
    sanitized_dns = db_session.sanitize_db_error(err_dns)
    assert fake_secret not in sanitized_dns
    assert "nombre de host" in sanitized_dns.lower()

    # 4. Connection refused
    err_refused = Exception("connection refused by 127.0.0.1:5432")
    sanitized_refused = db_session.sanitize_db_error(err_refused)
    assert "rechazada" in sanitized_refused.lower()

    # 5. SSL
    err_ssl = Exception("SSL connection failed during handshake")
    sanitized_ssl = db_session.sanitize_db_error(err_ssl)
    assert "ssl" in sanitized_ssl.lower()

    # 6. Desconocido genérico
    err_unknown = Exception(f"Some obscure database failure token={fake_secret}")
    sanitized_unknown = db_session.sanitize_db_error(err_unknown)
    assert fake_secret not in sanitized_unknown
    assert "comunicación con el servidor de base de datos" in sanitized_unknown


def test_test_db_connection_unconfigured():
    """Valida que test_db_connection retorna False si falta DATABASE_URL."""
    ok, detail, latency = db_session.test_db_connection()
    assert ok is False
    assert "no configurada" in detail.lower()
    assert latency is None


def test_test_db_connection_success(monkeypatch):
    """Valida test_db_connection exitoso con conexión sustituida satisfactoria (SELECT 1 == 1)."""
    monkeypatch.setattr(settings, "DATABASE_URL", "postgresql+psycopg://user:pass@localhost:5432/db")
    db_session.close_engine()

    mock_conn = MagicMock()
    mock_conn.execute.return_value.scalar.return_value = 1

    mock_engine = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    with patch.object(db_session, "get_engine", return_value=mock_engine):
        ok, detail, latency = db_session.test_db_connection()
        assert ok is True
        assert "verificada con éxito" in detail
        assert latency is not None
        assert latency >= 0


def test_test_db_connection_unexpected_scalar(monkeypatch):
    """Valida el manejo cuando SELECT 1 no devuelve 1."""
    monkeypatch.setattr(settings, "DATABASE_URL", "sqlite:///:memory:")
    db_session.close_engine()

    mock_conn = MagicMock()
    mock_conn.execute.return_value.scalar.return_value = 0

    mock_engine = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    with patch.object(db_session, "get_engine", return_value=mock_engine):
        ok, detail, latency = db_session.test_db_connection()
        assert ok is False
        assert "no retornó el valor esperado" in detail


def test_test_db_connection_exception_sanitizes_secret(monkeypatch):
    """Valida que excepciones durante SELECT 1 son capturadas y sanitizadas."""
    monkeypatch.setattr(settings, "DATABASE_URL", "sqlite:///:memory:")
    db_session.close_engine()

    fake_secret = "secret_db_pass_xyz123"
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = Exception(f"password authentication failed {fake_secret}")

    with patch.object(db_session, "get_engine", return_value=mock_engine):
        ok, detail, latency = db_session.test_db_connection()
        assert ok is False
        assert fake_secret not in detail
        assert "credenciales de PostgreSQL" in detail
        assert latency is not None
