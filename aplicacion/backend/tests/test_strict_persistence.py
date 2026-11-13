from unittest.mock import patch
import pytest
from fastapi import HTTPException
from app.core.config import settings
from app.db.session import get_required_session


def test_get_required_session_raises_503_in_strict_mode():
    """Verifica que get_required_session rechace operaciones con HTTP 503 si no hay BD en modo estricto."""
    with patch.object(settings, "STRICT_DATABASE_MODE", True):
        with patch("app.db.session.get_engine", return_value=None):
            gen = get_required_session()
            with pytest.raises(HTTPException) as exc_info:
                next(gen)
            assert exc_info.value.status_code == 503
            assert exc_info.value.detail["code"] == "DATABASE_UNAVAILABLE"


def test_get_required_session_yields_none_in_tolerant_dev_mode():
    """Verifica que en modo desarrollo tolerante emita None sin lanzar excepción."""
    with patch.object(settings, "STRICT_DATABASE_MODE", False), patch.object(settings, "APP_ENV", "development"):
        with patch("app.db.session.get_engine", return_value=None):
            gen = get_required_session()
            val = next(gen)
            assert val is None
