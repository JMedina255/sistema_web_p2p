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


class UserRolesResponse(BaseModel):
    email: str = Field(..., description="Correo institucional oficial")
    roles: list[str] = Field(default_factory=list, description="Lista de nombres de roles activos")
    is_active: bool = Field(True, description="Indica si el usuario mantiene actividad vigente")


class PromoteMentorRequest(BaseModel):
    email: str = Field(..., description="Correo institucional del estudiante a promover al rol Mentor")
    assigned_by: str | None = Field(None, description="Correo o identificador del administrador o sistema")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return _validate_upt_email(v)


class RevokeMentorRequest(BaseModel):
    email: str = Field(
        ..., description="Correo institucional del estudiante al que se le revoca el rol Mentor"
    )
    revoked_by: str | None = Field(None, description="Identificador del solicitante o administrador")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return _validate_upt_email(v)


class RoleOperationResponse(BaseModel):
    success: bool
    email: str
    role: str
    message: str
    roles: list[str]
