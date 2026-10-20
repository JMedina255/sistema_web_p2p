import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from app.core.config import settings


def generate_otp_code(length: int = 6) -> str:
    """
    Genera un código OTP numérico de longitud especificada garantizando
    representación textual de exactamente N dígitos (incluyendo ceros a la izquierda).
    """
    # Usamos secrets.randbelow para aleatoriedad criptográficamente segura
    code_int = secrets.randbelow(10**length)
    return str(code_int).zfill(length)


def hash_otp_code(code: str, salt: str = "") -> str:
    """
    Calcula un hash SHA-256 del código OTP con salt para almacenamiento seguro en BD.
    """
    data = f"{salt}:{code}".encode()
    return hashlib.sha256(data).hexdigest()


def verify_otp_hash(code: str, hashed_code: str, salt: str = "") -> bool:
    """
    Verifica si el código ingresado coincide con el hash almacenado usando tiempo constante.
    """
    expected_hash = hash_otp_code(code, salt)
    return secrets.compare_digest(expected_hash, hashed_code)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Crea un token JWT de sesión firmado con JWT_SECRET_KEY y algoritmo HS256.
    """
    to_encode = data.copy()
    now = datetime.now(UTC)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update(
        {
            "iat": int(now.timestamp()),
            "exp": int(expire.timestamp()),
            "iss": "sistema-p2p-epis-upt",
        }
    )
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any] | None:
    """
    Decodifica y valida un token JWT de sesión. Retorna el payload si es válido o None si expiró/es inválido.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            issuer="sistema-p2p-epis-upt",
        )
        return payload
    except (jwt.PyJWTError, Exception):
        return None
