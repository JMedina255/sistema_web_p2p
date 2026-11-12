from pydantic import BaseModel, Field, field_validator


class SurveyCreatePayload(BaseModel):
    """
    Payload de registro de encuesta de calidad post-mentoría (T-38 / T-39 / CUS05 / RF18 / RN-12 / RN-13).
    """

    calificacion_general: int = Field(
        ...,
        ge=1,
        le=5,
        description="Escala Likert global de satisfacción (1 a 5 estrellas).",
    )
    dominio_tema: int = Field(
        ...,
        ge=1,
        le=5,
        description="Evaluación del dominio conceptual y solvencia del mentor (1 a 5 estrellas).",
    )
    claridad_explicacion: int = Field(
        ...,
        ge=1,
        le=5,
        description="Evaluación de la didáctica y claridad pedagógica (1 a 5 estrellas).",
    )
    puntualidad: int = Field(
        ...,
        ge=1,
        le=5,
        description="Cumplimiento del horario pactado de mentoría (1 a 5 estrellas).",
    )
    comentarios: str | None = Field(
        None,
        description="Retroalimentación cualitativa y sugerencias formativas (mínimo 20 caracteres si se incluye).",
    )

    @field_validator("comentarios")
    @classmethod
    def validate_comentarios_length(cls, v: str | None) -> str | None:
        if v is not None:
            clean = v.strip()
            if clean and len(clean) < 20:
                raise ValueError(
                    "SURVEY_FEEDBACK_TOO_SHORT: Las observaciones cualitativas deben contener al menos 20 caracteres descriptivos."
                )
            return clean if clean else None
        return None


class SurveyResponse(BaseModel):
    """
    Respuesta de encuesta de calidad registrada.
    """

    id_encuesta: int
    id_sesion: int
    estudiante_email: str
    calificacion_general: int
    dominio_tema: int
    claridad_explicacion: int
    puntualidad: int
    comentarios: str | None = None
    created_at: str
    mensaje: str = "Evaluación de calidad post-mentoría registrada con éxito."


class SurveyStatusResponse(BaseModel):
    """
    Estado de elegibilidad y disponibilidad de encuesta de calidad para una sesión.
    """

    id_sesion: int
    eligible: bool
    has_surveyed: bool
    window_open: bool
    deadline: str | None = None
    mensaje: str = "Consulta de elegibilidad completada."
