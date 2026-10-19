from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from app.core.security import decode_access_token
from app.main import app
from app.services.auth_service import _memory_challenges

client = TestClient(app)


def setup_function():
    _memory_challenges.clear()


def test_request_otp_success():
    response = client.post("/api/v1/auth/otp/request", json={"email": "2022074255@upt.pe"})
    assert response.status_code == 200
    data = response.json()
    assert "challengeId" in data
    assert data["email"] == "2022074255@upt.pe"
    assert data["cooldownSeconds"] == 60
    assert data["isMock"] is False
    assert data["mockCodeHint"] is not None


def test_request_otp_rejects_non_upt_domain():
    response = client.post("/api/v1/auth/otp/request", json={"email": "estudiante@gmail.com"})
    assert response.status_code == 422
    err_text = response.text.lower()
    assert "upt.pe" in err_text


def test_request_otp_rejects_malformed_email():
    response = client.post("/api/v1/auth/otp/request", json={"email": "@upt.pe"})
    assert response.status_code == 422


def test_request_otp_cooldown_rejection():
    # Primer request exitoso
    res1 = client.post("/api/v1/auth/otp/request", json={"email": "cooldown@upt.pe"})
    assert res1.status_code == 200

    # Segundo request inmediato -> 429 COOLDOWN_ACTIVE
    res2 = client.post("/api/v1/auth/otp/request", json={"email": "cooldown@upt.pe"})
    assert res2.status_code == 429
    assert "COOLDOWN_ACTIVE" in res2.text


def test_resend_otp_success():
    res1 = client.post("/api/v1/auth/otp/request", json={"email": "resend@upt.pe"})
    assert res1.status_code == 200
    challenge_id = res1.json()["challengeId"]

    # Simular que el cooldown ya transcurrió modificando resend_available_at
    if challenge_id in _memory_challenges:
        _memory_challenges[challenge_id]["resend_available_at"] = datetime.now(UTC) - timedelta(seconds=5)

    res2 = client.post("/api/v1/auth/otp/resend", json={"challengeId": challenge_id})
    assert res2.status_code == 200
    data = res2.json()
    assert "challengeId" in data


def test_resend_otp_not_found():
    response = client.post("/api/v1/auth/otp/resend", json={"challengeId": "NONEXISTENT_CHALLENGE"})
    assert response.status_code == 404
    assert "CHALLENGE_NOT_FOUND" in response.text


def test_verify_otp_invalid_format():
    response = client.post(
        "/api/v1/auth/otp/verify",
        json={"challengeId": "CHAL-TEST", "otp": "123"},
    )
    assert response.status_code == 422


def test_verify_otp_challenge_not_found():
    response = client.post(
        "/api/v1/auth/otp/verify",
        json={"challengeId": "NONEXISTENT", "otp": "123456"},
    )
    assert response.status_code == 404
    assert "CHALLENGE_NOT_FOUND" in response.text


def test_verify_otp_expired_code():
    res1 = client.post("/api/v1/auth/otp/request", json={"email": "expired@upt.pe"})
    challenge_id = res1.json()["challengeId"]

    # Caso rápido "000000" para expiración
    response = client.post(
        "/api/v1/auth/otp/verify",
        json={"challengeId": challenge_id, "otp": "000000"},
    )
    assert response.status_code == 400
    assert "OTP_EXPIRED" in response.text


def test_verify_otp_incorrect_code():
    res1 = client.post("/api/v1/auth/otp/request", json={"email": "wrong@upt.pe"})
    challenge_id = res1.json()["challengeId"]

    response = client.post(
        "/api/v1/auth/otp/verify",
        json={"challengeId": challenge_id, "otp": "999999"},
    )
    assert response.status_code == 400
    assert "OTP_INVALID" in response.text


def test_verify_otp_success_and_jwt_token_issued():
    res1 = client.post("/api/v1/auth/otp/request", json={"email": "2022073504@upt.pe"})
    assert res1.status_code == 200
    data1 = res1.json()
    challenge_id = data1["challengeId"]
    code = data1["mockCodeHint"]

    # Verificación exitosa
    res2 = client.post(
        "/api/v1/auth/otp/verify",
        json={"challengeId": challenge_id, "otp": code},
    )
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["success"] is True
    assert data2["email"] == "2022073504@upt.pe"
    assert data2["mode"] == "api"
    assert "token" in data2
    assert data2["token"] is not None

    # Validar el token JWT emitido
    decoded = decode_access_token(data2["token"])
    assert decoded is not None
    assert decoded["sub"] == "2022073504@upt.pe"
    assert decoded["iss"] == "sistema-p2p-epis-upt"


def test_verify_otp_already_used():
    res1 = client.post("/api/v1/auth/otp/request", json={"email": "used@upt.pe"})
    challenge_id = res1.json()["challengeId"]
    code = res1.json()["mockCodeHint"]

    # Primera verificación exitosa
    res2 = client.post(
        "/api/v1/auth/otp/verify",
        json={"challengeId": challenge_id, "otp": code},
    )
    assert res2.status_code == 200

    # Segunda verificación con el mismo código -> OTP_ALREADY_USED
    res3 = client.post(
        "/api/v1/auth/otp/verify",
        json={"challengeId": challenge_id, "otp": code},
    )
    assert res3.status_code == 400
    assert "OTP_ALREADY_USED" in res3.text
