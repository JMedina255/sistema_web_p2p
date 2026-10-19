from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)


def test_health_check_returns_ok():
    """Valida que /api/v1/health devuelve HTTP 200 y status ok."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "backend"
    assert "environment" in data


def test_health_check_remains_operational_without_db():
    """Valida que /api/v1/health no depende de la base de datos."""
    with patch.object(settings, "DATABASE_URL", None):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_health_db_returns_404_outside_development():
    """Valida que /api/v1/health/db no está expuesto fuera de desarrollo."""
    with patch.object(settings, "APP_ENV", "production"):
        response = client.get("/api/v1/health/db")
        assert response.status_code == 404


def test_health_db_returns_503_when_unconfigured():
    """Valida que /api/v1/health/db devuelve 503 controlado si falta DATABASE_URL."""
    with patch.object(settings, "DATABASE_URL", None):
        response = client.get("/api/v1/health/db")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "error"
        assert data["database"] == "unavailable"
        assert "no configurada" in data["detail"].lower()


def test_health_db_returns_503_sanitized_on_failure():
    """Valida que los errores de conexión se sanitizan sin exponer secretos."""
    with patch("app.api.v1.endpoints.health.test_db_connection", return_value=(False, "Conexión rechazada por el servidor de base de datos.", 12.5)):
        response = client.get("/api/v1/health/db")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "error"
        assert data["database"] == "unavailable"
        assert "rechazada" in data["detail"].lower()
        # Verificar que no hay trazas de contraseñas ni URLs
        assert "password" not in str(data).lower()
        assert "postgres://" not in str(data)


def test_health_db_returns_200_when_connected():
    """Valida que /api/v1/health/db devuelve 200 cuando SELECT 1 es exitoso."""
    with patch("app.api.v1.endpoints.health.test_db_connection", return_value=(True, "Conexión a PostgreSQL (Supabase) verificada con éxito", 45.2)):
        response = client.get("/api/v1/health/db")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["database"] == "connected"
        assert data["latency_ms"] == 45.2


def test_root_returns_metadata():
    """Valida metadatos en la ruta raíz."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "docs" in data
    assert "health" in data
