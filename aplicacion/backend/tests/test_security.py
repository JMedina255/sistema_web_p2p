from datetime import timedelta

from app.core.config import settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    generate_otp_code,
    hash_otp_code,
    verify_otp_hash,
)


def test_generate_otp_code_length_and_digits():
    code = generate_otp_code(6)
    assert len(code) == 6
    assert code.isdigit()


def test_hash_and_verify_otp_code():
    code = "012345"
    salt = "somesalt123"
    hashed = hash_otp_code(code, salt)
    assert verify_otp_hash(code, hashed, salt) is True
    assert verify_otp_hash("999999", hashed, salt) is False


def test_create_and_decode_access_token():
    payload = {"sub": "2022074255@upt.pe", "email": "2022074255@upt.pe", "role": "estudiante"}
    token = create_access_token(payload)
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "2022074255@upt.pe"
    assert decoded["role"] == "estudiante"
    assert decoded["iss"] == "sistema-p2p-epis-upt"


def test_decode_expired_token_returns_none():
    payload = {"sub": "test@upt.pe"}
    # Token expirado hace 1 hora
    token = create_access_token(payload, expires_delta=timedelta(hours=-1))
    decoded = decode_access_token(token)
    assert decoded is None


def test_decode_invalid_signature_returns_none():
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.invalid_signature"
    assert decode_access_token(invalid_token) is None


def test_jwt_secret_masking_in_settings_repr():
    repr_str = repr(settings)
    assert settings.JWT_SECRET_KEY not in repr_str
