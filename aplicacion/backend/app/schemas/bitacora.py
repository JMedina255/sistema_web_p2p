from typing import Literal

from pydantic import BaseModel, Field, field_validator


class BitacoraCreatePayload(BaseModel):
    """
    Payload de registro de bitácora pedagógica post-sesión (T-35 / RF17 / CUS13 / RN-12).
    """

    temas_cubiertos: list[str] = Field(
        ..., min_length=1, description="Listado de títulos de temas silábicos impartidos."
    )
    observaciones: str = Field(
        ...,
        min_length=50,
        description="Observaciones pedagógicas sustantivas y desarrollo de la sesión (mínimo 50 caracteres).",
    )
    nivel_dificultad: Literal["Bajo", "Medio", "Alto"] = Field(
        "Medio", description="Nivel de dificultad percibido en el aprendizaje del grupo."
    )

    @field_validator("observaciones")
    @classmethod
    def validate_observaciones_substantive(cls, v: str) -> str:
        clean = v.strip()
        if len(clean) < 50:
            raise ValueError(
                "Infracción de RN-12: Las observaciones pedagógicas deben contener al menos 50 caracteres sustantivos."
            )
        return clean


class BitacoraResponse(BaseModel):
    """
    Respuesta estructurada de bitácora pedagógica suscrita con firma criptográfica.
    """

    id_bitacora: int
    id_sesion: int
    id_mentor: str
    temas_cubiertos: list[str]
    observaciones: str
    nivel_dificultad: str
    hash_firma: str
    horas_declaradas: float
    visado_administrador: bool
    created_at: str
    mensaje: str = "Bitácora pedagógica registrada y sellada criptográficamente con éxito."


class BitacoraObservarPayload(BaseModel):
    """
    Payload de observación técnica de bitácora por Administrador (T-41 / RF26 / CUS22).
    """

    motivo: str = Field(
        ...,
        description="Justificación técnica obligatoria de la observación de auditoría (mínimo 15 caracteres).",
    )

    @field_validator("motivo")
    @classmethod
    def validate_motivo_min_length(cls, v: str) -> str:
        clean = v.strip()
        if len(clean) < 15:
            raise ValueError(
                "OBSERVATION_REASON_REQUIRED: Debe ingresar obligatoriamente una justificación para la observación técnica."
            )
        return clean


class BitacoraVisadoResponse(BaseModel):
    """
    Respuesta de visado y acreditación formal de horas por la autoridad universitaria (RN-14).
    """

    id_bitacora: int
    id_sesion: int
    id_mentor: str
    horas_declaradas: float
    visado_administrador: bool
    estado_sesion: str
    auditor_email: str
    visado_at: str
    mensaje: str = "Bitácora pedagógica visada institucionalmente con éxito. Horas formativas acreditadas para certificación."


class BitacoraObservacionResponse(BaseModel):
    """
    Respuesta tras formular observación sobre la bitácora pedagógica.
    """

    id_bitacora: int
    id_sesion: int
    id_mentor: str
    estado_sesion: str
    motivo_observacion: str
    auditor_email: str
    observado_at: str
    mensaje: str = "Bitácora observada para corrección técnica por el Administrador."


class BitacoraItemResponse(BaseModel):
    """
    Item para la bandeja administrativa de auditoría de bitácoras (T-40 / RF26).
    """

    id_bitacora: int
    id_sesion: int
    codigo_sesion: str | None = None
    id_mentor: str
    temas_cubiertos: list[str]
    observaciones: str
    nivel_dificultad: str
    hash_firma: str
    horas_declaradas: float
    visado_administrador: bool
    estado_sesion: str
    fecha_inicio: str | None = None
    created_at: str
