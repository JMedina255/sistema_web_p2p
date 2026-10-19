import pytest

from app.core.config import settings
from app.db import session as db_session


@pytest.fixture(autouse=True)
def isolate_test_environment(monkeypatch):
    """
    Aísla la carga del .env local durante las pruebas automatizadas.
    Garantiza que la suite se ejecute sin credenciales reales ni llamadas externas a Supabase.
    """
    # Liberar cualquier conexión activa previa
    db_session.close_engine()

    # Forzar entorno de desarrollo controlado y DATABASE_URL vacía por defecto
    monkeypatch.setattr(settings, "APP_ENV", "development")
    monkeypatch.setattr(settings, "DATABASE_URL", None)

    yield

    # Liberar recursos y cerrar motores creados durante las pruebas
    db_session.close_engine()
