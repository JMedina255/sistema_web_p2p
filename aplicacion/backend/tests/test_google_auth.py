from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)


def test_google_login_valid_virtual_upt_student():
    """Valida que un estudiante @virtual.upt.pe autentique legítimamente con token verificado por Google."""
    mock_payload = {
        "email": "ra2022073504@virtual.upt.pe",
        "email_verified": True,
        "aud": settings.GOOGLE_CLIENT_ID,
        "iss": "https://accounts.google.com",
        "exp": 9999999999,
        "given_name": "Renzo Antonio",
        "family_name": "Antayhua Mamani",
        "picture": "https://lh3.googleusercontent.com/test-avatar",
        "sub": "google-uid-12345",
    }

    with patch("google.oauth2.id_token.verify_oauth2_token", return_value=mock_payload):
        response = client.post("/api/v1/auth/google", json={"id_token": "valid.google.jwt"})
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


def test_google_login_rejects_invalid_signature():
    """Valida que tokens con firma inválida sean estrictamente rechazados con 401."""
    with patch("google.oauth2.id_token.verify_oauth2_token", side_effect=ValueError("Invalid token signature")):
        response = client.post("/api/v1/auth/google", json={"id_token": "tampered.jwt.signature"})
        assert response.status_code == 401
        assert response.json()["detail"]["code"] == "GOOGLE_AUTH_FAILED"


def test_google_login_rejects_wrong_audience():
    """Valida que tokens con aud errónea (emitidos para otro cliente) sean rechazados con 401."""
    mock_payload = {
        "email": "ra2022073504@virtual.upt.pe",
        "email_verified": True,
        "aud": "wrong-client-id.apps.googleusercontent.com",
        "iss": "https://accounts.google.com",
        "exp": 9999999999,
        "sub": "123",
    }
    with patch("google.oauth2.id_token.verify_oauth2_token", return_value=mock_payload):
        response = client.post("/api/v1/auth/google", json={"id_token": "wrong.aud.token"})
        assert response.status_code == 401
        assert response.json()["detail"]["code"] == "INVALID_AUDIENCE"


def test_google_login_rejects_expired_token():
    """Valida que tokens expirados sean rechazados con 401."""
    mock_payload = {
        "email": "ra2022073504@virtual.upt.pe",
        "email_verified": True,
        "aud": settings.GOOGLE_CLIENT_ID,
        "iss": "https://accounts.google.com",
        "exp": 1000000000,  # Pasado
        "sub": "123",
    }
    with patch("google.oauth2.id_token.verify_oauth2_token", return_value=mock_payload):
        response = client.post("/api/v1/auth/google", json={"id_token": "expired.google.token"})
        assert response.status_code == 401
        assert response.json()["detail"]["code"] == "TOKEN_EXPIRED"


def test_google_login_rejects_unauthorized_issuer():
    """Valida que emisores no oficiales de Google sean rechazados con 401."""
    mock_payload = {
        "email": "ra2022073504@virtual.upt.pe",
        "email_verified": True,
        "aud": settings.GOOGLE_CLIENT_ID,
        "iss": "https://malicious-issuer.com",
        "exp": 9999999999,
        "sub": "123",
    }
    with patch("google.oauth2.id_token.verify_oauth2_token", return_value=mock_payload):
        response = client.post("/api/v1/auth/google", json={"id_token": "fake.issuer.token"})
        assert response.status_code == 401
        assert response.json()["detail"]["code"] == "INVALID_ISSUER"


def test_google_login_rejects_unverified_email():
    """Valida que cuentas de Google sin correo verificado sean rechazadas con 401."""
    mock_payload = {
        "email": "ra2022073504@virtual.upt.pe",
        "email_verified": False,
        "aud": settings.GOOGLE_CLIENT_ID,
        "iss": "https://accounts.google.com",
        "exp": 9999999999,
        "sub": "123",
    }
    with patch("google.oauth2.id_token.verify_oauth2_token", return_value=mock_payload):
        response = client.post("/api/v1/auth/google", json={"id_token": "unverified.email.token"})
        assert response.status_code == 401
        assert response.json()["detail"]["code"] == "UNVERIFIED_EMAIL"


def test_google_login_rejects_non_upt_domain():
    """Valida que correos externos de Google (ej. @gmail.com) sean rechazados con 403."""
    mock_payload = {
        "email": "estudiante.externo@gmail.com",
        "email_verified": True,
        "aud": settings.GOOGLE_CLIENT_ID,
        "iss": "https://accounts.google.com",
        "exp": 9999999999,
        "given_name": "Juan",
        "family_name": "Pérez",
        "sub": "123",
    }
    with patch("google.oauth2.id_token.verify_oauth2_token", return_value=mock_payload):
        response = client.post("/api/v1/auth/google", json={"id_token": "external.domain.token"})
        assert response.status_code == 403
        assert response.json()["detail"]["code"] == "NON_UPT_DOMAIN"


def test_google_login_rejects_empty_token():
    """Valida que tokens vacíos sean rechazados con 400."""
    response = client.post("/api/v1/auth/google", json={"id_token": "   "})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "INVALID_TOKEN"
