from typing import Literal

from pydantic import BaseModel, Field, field_validator


class PublishOfferPayload(BaseModel):
    id_asignatura: int = Field(..., gt=0, description="Identificador de la asignatura curricular crítica.")
    codigo_asignatura: str = Field(
        ..., min_length=2, max_length=20, description="Código de curso (ej. CALC-101)."
    )
    nombre_asignatura: str = Field(
        ..., min_length=2, max_length=150, description="Nombre oficial de la asignatura."
    )
    id_tema: int = Field(..., gt=0, description="Identificador del tema silábico conceptual.")
    nombre_tema: str = Field(
        ..., min_length=2, max_length=150, description="Nombre de la unidad o tema del sílabo."
    )
    fecha_inicio: str = Field(..., description="Fecha y hora de inicio de la sesión en formato ISO 8601.")
    duracion_minutos: Literal[60, 90] = Field(60, description="Duración en minutos (60 o 90 lectivos).")
    modalidad: Literal["presencial", "virtual"] = Field(..., description="Modalidad formativa.")
    aforo_maximo: int = Field(..., description="Aforo estándar (10 presencial, 20 virtual según RN-05).")
    espacio_asignado: str = Field(
        ..., min_length=3, max_length=255, description="Aula física o enlace virtual."
    )
    mentor_email: str = Field(
        ..., min_length=5, max_length=255, description="Correo institucional del mentor."
    )
    mentor_nombre: str | None = Field(None, max_length=200, description="Nombre del mentor.")
    notas_adicionales: str | None = Field(
        None, max_length=1000, description="Instrucciones o requerimientos previos."
    )

    @field_validator("mentor_email")
    @classmethod
    def validate_upt_email(cls, v: str) -> str:
        clean = v.strip().lower()
        if not clean.endswith("@upt.pe"):
            raise ValueError("El correo del mentor debe pertenecer al dominio institucional @upt.pe.")
        return clean

    @field_validator("aforo_maximo")
    @classmethod
    def validate_capacity_by_modality(cls, v: int, info) -> int:
        modality = info.data.get("modalidad")
        if modality == "presencial" and v != 10:
            raise ValueError(
                "Infracción de RN-05: El aforo para la modalidad presencial debe ser exactamente 10."
            )
        if modality == "virtual" and v != 20:
            raise ValueError(
                "Infracción de RN-05: El aforo para la modalidad virtual debe ser exactamente 20."
            )
        return v


class PublishOfferResponse(BaseModel):
    id_oferta: str
    codigo_sesion: str
    estado: Literal[
        "PUBLICADA",
        "PENDIENTE_CONFIRMACION",
        "CONFIRMADA",
        "CANCELADA_SISTEMA",
        "CANCELADA_MENTOR",
        "FINALIZADA",
    ] = "PUBLICADA"
    mensaje: str
    fecha_publicacion: str
    aforo: int
    espacio_asignado: str
    modo: Literal["api", "mock"] = "api"
    offer: PublishOfferPayload


class OfferFilterParams(BaseModel):
    mentor_email: str | None = None
    id_asignatura: int | None = None
    modalidad: Literal["presencial", "virtual"] | None = None
    estado: str | None = None
