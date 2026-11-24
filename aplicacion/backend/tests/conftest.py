import pytest

from app.core.config import settings
from app.db import session as db_session
from app.services.auth_service import (
    _email_request_timestamps,
    _ip_request_timestamps,
    _ip_verify_timestamps,
    _memory_challenges,
)
from app.services.schedule_parser_service import ScheduleParserService


class BlockedSMTPConnectionError(RuntimeError):
    """Excepción lanzada cuando una prueba intenta realizar conexiones SMTP salientes no autorizadas."""


class GuardedSMTP:
    def __init__(self, *args, **kwargs):
        raise BlockedSMTPConnectionError(
            "Conexión SMTP real bloqueada por el entorno de aislamiento de pruebas (QA-AUTH-02B Actividad 1)."
        )


@pytest.fixture(autouse=True)
def isolate_test_environment(monkeypatch):
    """
    Aísla la carga del entorno local durante las pruebas automatizadas.
    Garantiza que la suite se ejecute sin credenciales reales, sin despacho SMTP saliente
    y sin llamadas externas o modificaciones a la base Supabase remota del proyecto.
    """
    # 1. Liberar cualquier conexión activa previa a la base de datos
    db_session.close_engine()

    # 2. Forzar entorno de desarrollo controlado, sin acceso a Supabase ni SMTP real
    monkeypatch.setattr(settings, "APP_ENV", "development")
    monkeypatch.setattr(settings, "DATABASE_URL", None)
    monkeypatch.setattr(settings, "STRICT_DATABASE_MODE", False)
    monkeypatch.setattr(settings, "SMTP_ENABLED", False)
    monkeypatch.setattr(settings, "SMTP_USER", "")
    monkeypatch.setattr(settings, "SMTP_PASSWORD", "")
    monkeypatch.setattr(settings, "SMTP_FROM_EMAIL", "test-auth-noreply@upt.pe")
    monkeypatch.setattr(settings, "ENABLE_MOCK_OTP_HINTS", False)
    monkeypatch.setattr(
        ScheduleParserService, "_active_free_slots", list(ScheduleParserService._default_slots)
    )
    monkeypatch.setattr(ScheduleParserService, "_last_imported_filename", "cronograma_oficial_base_2026.xlsx")

    # 3. Bloqueo estricto a nivel de socket/biblioteca smtplib para impedir envíos externos
    monkeypatch.setattr("smtplib.SMTP", GuardedSMTP)
    monkeypatch.setattr("smtplib.SMTP_SSL", GuardedSMTP)

    # 4. Limpiar estructuras en memoria antes de la ejecución de cada prueba
    _memory_challenges.clear()
    _ip_request_timestamps.clear()
    _email_request_timestamps.clear()
    _ip_verify_timestamps.clear()

    yield

    # 5. Limpieza posterior a cada prueba
    _memory_challenges.clear()
    _ip_request_timestamps.clear()
    _email_request_timestamps.clear()
    _ip_verify_timestamps.clear()
    db_session.close_engine()
