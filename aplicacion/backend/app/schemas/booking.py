from typing import Literal

from pydantic import BaseModel, Field, field_validator


class BookingCreatePayload(BaseModel):
    """
    Payload para la formalización atómica de reserva de cupo (CUS04 / RF12 / RN-05).
    """

    id_sesion: int = Field(..., ge=1, description="Identificador unívoco de la sesión de mentoría.")
    estudiante_email: str = Field(..., description="Correo institucional @upt.pe del estudiante mentoreado.")

    @field_validator("estudiante_email")
    @classmethod
    def validate_upt_email(cls, v: str) -> str:
        clean = v.strip().lower()
        if not clean.endswith("@upt.pe"):
            raise ValueError("El correo del estudiante debe pertenecer al dominio institucional @upt.pe.")
        return clean


class BookingResponse(BaseModel):
    """
    Respuesta canónica de confirmación de reserva provisional (HTTP 201 Created).
    """

    id_reserva: int
    codigo_reserva: str
    id_sesion: int
    estudiante_email: str
    estado: Literal[
        "PENDIENTE_CONFIRMACION",
        "CONFIRMADA",
        "CANCELADA_USUARIO",
        "NO_CONFIRMADA",
        "CANCELADA_SISTEMA",
        "ASISTIDA",
        "INASISTENCIA",
    ] = "PENDIENTE_CONFIRMACION"
    fecha_reserva: str
    fecha_limite_confirmacion: str | None = None
    mensaje: str
    ticket_hash: str | None = None


class BookingDetailResponse(BaseModel):
    """
    Detalle ampliado de una reserva de cupo con metadatos de la sesión y mentoría.
    """

    id_reserva: int
    codigo_reserva: str
    id_sesion: int
    codigo_sesion: str | None = None
    estudiante_email: str
    estado: str
    fecha_reserva: str
    fecha_ratificacion: str | None = None
    motivo_cancelacion: str | None = None
    ticket_hash: str | None = None
    nombre_asignatura: str | None = None
    nombre_tema: str | None = None
    fecha_inicio: str | None = None
    duracion_minutos: int | None = None
    modalidad: str | None = None
    espacio_asignado: str | None = None
    mentor_email: str | None = None


class MentoringDemandPayload(BaseModel):
    """
    Registro de solicitud temática por demanda (CUS03 / RF07).
    """

    id_asignatura: int = Field(..., ge=1, description="Identificador de la asignatura curricular.")
    id_tema: int = Field(..., ge=1, description="Identificador del tema conceptual silábico.")
    notas: str | None = Field(
        None, max_length=500, description="Observaciones o temas específicos requeridos."
    )
    observaciones: str | None = Field(None, max_length=500, description="Alias para notas pedagógicas.")


class MentoringDemandResponse(BaseModel):
    """
    Respuesta canónica de registro de solicitud de mentoría por demanda.
    """

    id_demanda: int
    estudiante_email: str
    id_asignatura: int
    id_tema: int
    nombre_asignatura: str | None = None
    nombre_tema: str | None = None
    observaciones: str | None = None
    estado: Literal["PENDIENTE", "ATENDIDA", "CANCELADA"] = "PENDIENTE"
    created_at: str


class QuorumEvaluationPayload(BaseModel):
    """
    Payload para evaluar el quórum normativo institucional del 50% a T-24h (RN-08 / RN-09 / CUS23).
    """

    id_sesion: int = Field(..., ge=1, description="Identificador de la sesión a evaluar.")


class QuorumEvaluationResponse(BaseModel):
    """
    Respuesta detallada de evaluación de quórum normativo institucional.
    """

    id_sesion: int
    codigo_sesion: str
    aforo_maximo: int
    reservas_totales: int
    reservas_confirmadas: int
    porcentaje_quorum: float
    quorum_minimo_requerido: float = 50.0
    cumple_quorum: bool
    estado_sesion: str
    horas_antelacion: float
    mensaje: str
