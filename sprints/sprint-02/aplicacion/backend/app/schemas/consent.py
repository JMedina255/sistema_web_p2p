import re

from pydantic import BaseModel, Field, field_validator


def _validate_upt_email(v: str) -> str:
    clean_email = v.strip().lower()
    if not clean_email.endswith("@upt.pe"):
        raise ValueError(
            "El correo electrónico debe pertenecer al dominio institucional @upt.pe (CUS01 / RN-01)"
        )
    email_regex = r"^[a-zA-Z0-9._%+-]+@upt\.pe$"
    if not re.match(email_regex, clean_email):
        raise ValueError("El formato del correo institucional es inválido")
    return clean_email


class ConsentStatusResponse(BaseModel):
    has_consented: bool = Field(..., description="Indica si el usuario ha otorgado consentimiento vigente")
    consented_at: str | None = Field(None, description="Estampa temporal UTC en formato ISO 8601")
    terms_version: str = Field("2026-II-v1.0", description="Versión de los términos y condiciones")
    email: str = Field(..., description="Correo institucional consultado")
    mode: str = Field("api", description="Modo de ejecución: api o mock")


class ConsentAcceptRequest(BaseModel):
    email: str = Field(..., description="Correo institucional oficial @upt.pe")
    accepted: bool = Field(True, description="Conformidad expresa (true)")
    terms_version: str = Field("2026-II-v1.0", description="Versión de términos aceptada")
    ip_address: str | None = Field(None, description="Dirección IP de origen para fines de auditoría")
    user_agent: str | None = Field(None, description="User Agent del navegador del usuario")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return _validate_upt_email(v)


class ConsentRevokeRequest(BaseModel):
    email: str = Field(..., description="Correo institucional oficial @upt.pe a revocar")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return _validate_upt_email(v)


class ConsentOperationResponse(BaseModel):
    success: bool
    consented_at: str | None = None
    email: str
    message: str
