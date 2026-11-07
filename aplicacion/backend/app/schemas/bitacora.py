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
