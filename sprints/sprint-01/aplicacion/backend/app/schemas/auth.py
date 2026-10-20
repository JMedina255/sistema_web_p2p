import re

from pydantic import BaseModel, Field, field_validator


class RequestOtpPayload(BaseModel):
    email: str = Field(..., description="Correo electrónico institucional oficial @upt.pe")

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        clean_email = v.strip().lower()
        if not clean_email.endswith("@upt.pe"):
            raise ValueError(
                "El correo electrónico debe pertenecer al dominio institucional @upt.pe (CUS01 / RN-01)"
            )
        email_regex = r"^[a-zA-Z0-9._%+-]+@upt\.pe$"
        if not re.match(email_regex, clean_email):
            raise ValueError("El formato del correo institucional es inválido")
        return clean_email


class RequestOtpResponse(BaseModel):
    challengeId: str
    email: str
    expiresAt: str
    cooldownSeconds: int
    message: str
    isMock: bool = False
    mockCodeHint: str | None = None


class ResendOtpPayload(BaseModel):
    challengeId: str = Field(..., description="Identificador del desafío OTP activo")


class VerifyOtpPayload(BaseModel):
    challengeId: str = Field(..., description="Identificador del desafío OTP a validar")
    otp: str = Field(..., description="Código numérico de exactamente 6 dígitos")

    @field_validator("otp")
    @classmethod
    def validate_otp_format(cls, v: str) -> str:
        clean_otp = v.strip()
        if not re.match(r"^\d{6}$", clean_otp):
            raise ValueError("El código OTP debe contener exactamente 6 dígitos numéricos (CUS01 / RNF01)")
        return clean_otp


class VerifyOtpResponse(BaseModel):
    success: bool
    email: str
    verifiedAt: str
    mode: str = "api"
    message: str
    token: str | None = None
    tokenType: str = "bearer"
