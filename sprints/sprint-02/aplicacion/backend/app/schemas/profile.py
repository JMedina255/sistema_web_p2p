import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


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


class AvailabilitySlotSchema(BaseModel):
    dia_semana: int = Field(
        ..., ge=1, le=6, description="1: Lunes, 2: Martes, 3: Miércoles, 4: Jueves, 5: Viernes, 6: Sábado"
    )
    hora_inicio: str = Field(..., description="Hora de inicio en formato HH:MM (ej. 08:00)")
    hora_fin: str = Field(..., description="Hora de fin en formato HH:MM (ej. 09:00)")

    @field_validator("hora_inicio", "hora_fin")
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        clean = v.strip()
        if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", clean):
            raise ValueError("El formato de hora debe ser exactamente HH:MM entre 00:00 y 23:59 (ej. 08:00)")
        return clean

    @model_validator(mode="after")
    def validate_time_order(self) -> "AvailabilitySlotSchema":
        if self.hora_inicio >= self.hora_fin:
            raise ValueError(
                f"La hora de inicio ({self.hora_inicio}) debe ser estrictamente anterior a la hora de fin ({self.hora_fin})"
            )
        return self


class AvailabilityUpdatePayload(BaseModel):
    email: str = Field(..., description="Correo institucional oficial")
    slots: list[AvailabilitySlotSchema] = Field(
        default_factory=list, description="Lista de bloques de 1 hora"
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return _validate_upt_email(v)

    @field_validator("slots")
    @classmethod
    def validate_no_overlapping_slots(
        cls, slots: list[AvailabilitySlotSchema]
    ) -> list[AvailabilitySlotSchema]:
        by_day: dict[int, list[AvailabilitySlotSchema]] = {}
        for s in slots:
            by_day.setdefault(s.dia_semana, []).append(s)

        for day, day_slots in by_day.items():
            sorted_slots = sorted(day_slots, key=lambda x: x.hora_inicio)
            for i in range(len(sorted_slots) - 1):
                curr = sorted_slots[i]
                nxt = sorted_slots[i + 1]
                if curr.hora_inicio == nxt.hora_inicio and curr.hora_fin == nxt.hora_fin:
                    raise ValueError(
                        f"Franja horaria duplicada en el día {day}: {curr.hora_inicio} - {curr.hora_fin}"
                    )
                if curr.hora_fin > nxt.hora_inicio:
                    raise ValueError(
                        f"Franjas horarias solapadas en el día {day}: {curr.hora_inicio}-{curr.hora_fin} y {nxt.hora_inicio}-{nxt.hora_fin}"
                    )
        return slots


class AvailabilityResponse(BaseModel):
    email: str
    slots: list[AvailabilitySlotSchema] = Field(default_factory=list)
    total_slots: int = 0


class AvailabilityOperationResponse(BaseModel):
    success: bool
    totalSlots: int
    message: str
    slots: list[AvailabilitySlotSchema] = Field(default_factory=list)


class AcademicProfileResponse(BaseModel):
    email: str
    codigo_estudiante: str | None = None
    nombres: str | None = None
    apellidos: str | None = None
    ciclo_actual: int = Field(..., ge=1, le=10, description="Ciclo formativo cursado (1 a 10)")
    rol_postulacion: Literal["mentoreado", "mentor"] = Field(
        "mentoreado", description="'mentoreado' o 'mentor'"
    )
    materias_interes: list[int] = Field(
        default_factory=list, description="IDs de asignaturas filtro seleccionadas"
    )
    temas_seleccionados: list[int] = Field(
        default_factory=list, description="IDs de temas conceptuales seleccionados"
    )
    biografia: str | None = None
    modalidad_preferida: Literal["presencial", "virtual", "hibrida"] = Field(
        "presencial", description="'presencial', 'virtual' o 'hibrida'"
    )
    updated_at: str | None = None


class AcademicProfileUpdate(BaseModel):
    email: str | None = Field(None, description="Correo institucional (opcional si proviene del token JWT)")
    codigo_estudiante: str | None = None
    nombres: str | None = None
    apellidos: str | None = None
    ciclo_actual: int = Field(..., ge=1, le=10, description="Ciclo formativo cursado (1 a 10)")
    rol_postulacion: Literal["mentoreado", "mentor"] = Field(
        "mentoreado", description="'mentoreado' o 'mentor'"
    )
    materias_interes: list[int] = Field(default_factory=list)
    temas_seleccionados: list[int] = Field(default_factory=list)
    biografia: str | None = None
    modalidad_preferida: Literal["presencial", "virtual", "hibrida"] = Field(
        "presencial", description="'presencial', 'virtual' o 'hibrida'"
    )

    @field_validator("email")
    @classmethod
    def validate_optional_email(cls, v: str | None) -> str | None:
        if v is not None:
            return _validate_upt_email(v)
        return v
