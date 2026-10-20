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


def test_auth_service_with_real_db_session():
    import pytest
    from fastapi import HTTPException
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from app.db.session import Base
    from app.models.auth import AuthChallenge
    from app.services.auth_service import AuthService

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    email = "dbuser@upt.pe"

    # 1. Solicitar OTP persistido en BD
    req_res = AuthService.request_otp(db, email)
    assert req_res.challengeId.startswith("CHAL-API-")

    chal = db.query(AuthChallenge).filter_by(id_challenge=req_res.challengeId).first()
    assert chal is not None
    assert chal.email == email
    assert chal.consumed is False

    # 2. Cooldown de 60 segundos evaluado en BD
    with pytest.raises(HTTPException) as exc_cooldown:
        AuthService.request_otp(db, email)
    assert exc_cooldown.value.status_code == 429
    assert exc_cooldown.value.detail["code"] == "COOLDOWN_ACTIVE"

    # 3. Verificación con fecha y zona horaria desde BD sin error de tipos
    code = req_res.mockCodeHint
    verify_res = AuthService.verify_otp(db, req_res.challengeId, code)
    assert verify_res.success is True
    assert verify_res.token is not None

    db.refresh(chal)
    assert chal.consumed is True

    # 4. Anti-replay contra BD
    with pytest.raises(HTTPException) as exc_replay:
        AuthService.verify_otp(db, req_res.challengeId, code)
    assert exc_replay.value.status_code == 400
    assert exc_replay.value.detail["code"] == "OTP_ALREADY_USED"

    # 5. Invalidación de desafío anterior al emitir una nueva solicitud tras cooldown
    chal.resend_available_at = datetime.now(UTC) - timedelta(seconds=10)
    chal.consumed = False
    db.commit()

    req_res2 = AuthService.request_otp(db, email)
    db.refresh(chal)
    assert chal.consumed is True  # El anterior fue invalidado automáticamente

    # 6. Reenvío en BD
    chal2 = db.query(AuthChallenge).filter_by(id_challenge=req_res2.challengeId).first()
    chal2.resend_available_at = datetime.now(UTC) - timedelta(seconds=10)
    db.commit()

    resend_res = AuthService.resend_otp(db, req_res2.challengeId)
    assert resend_res.challengeId != req_res2.challengeId
    db.refresh(chal2)
    assert chal2.consumed is True

    db.close()
    engine.dispose()
