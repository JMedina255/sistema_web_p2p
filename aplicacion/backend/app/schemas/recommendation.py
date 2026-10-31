from typing import Literal

from pydantic import BaseModel, Field


class ScoreBreakdown(BaseModel):
    """
    Desglose explicable de los factores multifactoriales del algoritmo EdRecSys.
    """

    curricular_affinity: float = Field(
        ..., ge=0.0, le=1.0, description="Proporción de asignaturas comunes de interés (0.0 a 1.0)."
    )
    course_weight_factor: float = Field(
        ..., ge=1.0, le=1.3, description="Factor ponderador de asignatura crítica / filtro (1.0x a 1.3x)."
    )
    critical_course_applied: str | None = Field(
        None, description="Código de la asignatura crítica que aportó la máxima ponderación."
    )
    topic_overlap_jaccard: float = Field(
        ..., ge=0.0, le=1.0, description="Coeficiente de similitud de Jaccard sobre temas silábicos."
    )
    topic_overlap_dice: float = Field(
        ..., ge=0.0, le=1.0, description="Coeficiente de coincidencia de Dice sobre temas silábicos."
    )
    schedule_compatibility: float = Field(
        ..., ge=0.0, le=1.0, description="Compatibilidad de agenda horaria semanal (0.0 a 1.0)."
    )
    schedule_matching_slots_count: int = Field(
        ..., ge=0, description="Cantidad de franjas horarias de 1 hora en intersección común."
    )
    matching_slots: list[str] = Field(
        default_factory=list,
        description="Listado legible de franjas horarias comunes (ej. 'Lun 10:00-11:00').",
    )
    modality_compatibility: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Compatibilidad de modalidad formativa (presencial / virtual / híbrida).",
    )
    institutional_merit_eligible: bool = Field(
        ..., description="Cumplimiento de la regla de mérito RN-03 (ciclo >= VII)."
    )
    explanation_text: str = Field(
        ..., description="Resumen cualitativo explicable en lenguaje natural para el estudiante."
    )


class MentorRecommendationItem(BaseModel):
    """
    Item recomendado de Mentor Académico ordenado por afinidad Top-k.
    """

    mentor_email: str
    mentor_codigo: str | None = None
    mentor_nombres: str
    mentor_apellidos: str
    mentor_ciclo: int = Field(..., ge=7, le=10, description="Ciclo académico (VII a X según RN-03).")
    materias_ofrecidas: list[int] = Field(default_factory=list)
    materias_nombres: list[str] = Field(default_factory=list)
    temas_ofrecidos: list[int] = Field(default_factory=list)
    modalidad_preferida: str
    score_total: float = Field(..., description="Puntaje compuesto ponderado (EdRecSys Score).")
    breakdown: ScoreBreakdown


class OfferRecommendationItem(BaseModel):
    """
    Item recomendado de Oferta / Sesión de mentoría programada en catálogo activo.
    """

    id_oferta: str
    codigo_sesion: str
    id_asignatura: int
    codigo_asignatura: str
    nombre_asignatura: str
    id_tema: int
    nombre_tema: str
    fecha_inicio: str
    duracion_minutos: int
    modalidad: str
    aforo_maximo: int
    aforo_disponible: int = Field(
        default=10, description="Plazas disponibles para reserva (aforo_maximo - cupos ocupados)."
    )
    espacio_asignado: str
    mentor_email: str
    mentor_nombre: str | None = None
    mentor_ciclo: int = Field(..., ge=7, le=10)
    score_total: float
    breakdown: ScoreBreakdown


class RecommendationListResponse[T](BaseModel):
    """
    Contenedor estándar de respuestas de recomendación Top-k.
    """

    mentee_email: str
    total_candidates_evaluated: int
    top_k: int
    recommendations_count: int
    algorithm: Literal["EdRecSys-v1.0-HybridMultifactorial"] = "EdRecSys-v1.0-HybridMultifactorial"
    items: list[T]


class RecommendationExplainRequest(BaseModel):
    """
    Solicitud de desglose explicable para un mentor o sesión específica.
    """

    mentee_email: str = Field(..., description="Correo del mentoreado.")
    mentor_email: str | None = Field(None, description="Correo del mentor candidato a evaluar.")
    id_oferta: str | None = Field(None, description="Código o identificador de oferta candidata a evaluar.")


class RecommendationExplainResponse(BaseModel):
    """
    Respuesta detallada con explicabilidad completa del algoritmo EdRecSys.
    """

    target_type: Literal["mentor", "offer"]
    target_id: str
    mentee_email: str
    score_total: float
    breakdown: ScoreBreakdown
    institutional_summary: str
