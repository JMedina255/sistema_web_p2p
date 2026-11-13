import jwt
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_google_login_valid_virtual_upt_student():
    """Valida que un estudiante @virtual.upt.pe autentique vía Google y se extraiga su código y nombre."""
    mock_payload = {
        "email": "ra2022073504@virtual.upt.pe",
        "email_verified": True,
        "given_name": "Renzo Antonio",
        "family_name": "Antayhua Mamani",
        "picture": "https://lh3.googleusercontent.com/test-avatar",
        "sub": "google-uid-12345",
    }
    # Generamos un ID token simulado
    dummy_token = jwt.encode(mock_payload, "dummy-secret-test", algorithm="HS256")

    response = client.post("/api/v1/auth/google", json={"id_token": dummy_token})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["email"] == "ra2022073504@virtual.upt.pe"
    assert data["codigo_estudiante"] == "2022073504"
    assert data["nombres"] == "Renzo Antonio"
    assert data["apellidos"] == "Antayhua Mamani"
    assert "mentoreado" in data["roles"]
    assert data["access_token"] is not None
    assert data["refresh_token"] is not None


def test_google_login_rejects_non_upt_domain():
    """Valida que correos externos de Google (ej. @gmail.com) sean rechazados con 403."""
    mock_payload = {
        "email": "estudiante.externo@gmail.com",
        "email_verified": True,
        "given_name": "Juan",
        "family_name": "Pérez",
    }
    dummy_token = jwt.encode(mock_payload, "dummy-secret-test", algorithm="HS256")

    response = client.post("/api/v1/auth/google", json={"id_token": dummy_token})
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "NON_UPT_DOMAIN"


def test_google_login_rejects_empty_token():
    """Valida que tokens vacíos sean rechazados con 400."""
    response = client.post("/api/v1/auth/google", json={"id_token": "   "})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "INVALID_TOKEN"
