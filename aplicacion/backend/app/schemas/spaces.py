"""
Esquemas Pydantic para el subsistema de Espacios Físicos, Cronogramas y Parser de Horarios (RF10 / CUS11 / MOD-04).
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class FreeSlotItem(BaseModel):
    """Representa una franja horaria libre identificada en un aula física o laboratorio."""

    aula: str = Field(..., description="Identificador o nombre del aula/laboratorio (ej. 'Lab 01', 'Aula 101').")
    dia: str = Field(..., description="Día de la semana de la franja disponible (ej. 'Lunes', 'Martes').")
    hora_inicio: str = Field(..., description="Hora de inicio en formato HH:mm (ej. '08:00').")
    hora_fin: str = Field(..., description="Hora de fin en formato HH:mm (ej. '10:00').")
    estado: str = Field("LIBRE", description="Estado de ocupación de la franja horaria.")
    fila_origen: int | None = Field(None, description="Fila del archivo Excel de origen si aplica.")
    pagina: int | None = Field(None, description="Página del documento PDF de origen si aplica.")


class ScheduleImportResponse(BaseModel):
    """Respuesta de importación y procesamiento de cronograma oficial de horarios de la EPIS (CUS11)."""

    status: str = Field(..., description="Estado de la operación (ej. 'PROCESADO_EXITOSAMENTE').")
    archivo: str = Field(..., description="Nombre del archivo oficial cargado y procesado.")
    total_aulas_libres_identificadas: int = Field(..., description="Cantidad total de bloques libres detectados.")
    reservas_activas_preservadas: int = Field(0, description="Cantidad de reservas de mentoría preservadas.")
    aulas_libres: list[FreeSlotItem] = Field(..., description="Detalle de franjas horarias y recintos disponibles.")


class ClassroomListResponse(BaseModel):
    """Listado de recintos físicos registrados en la infraestructura de la EPIS."""

    aulas: list[str] = Field(..., description="Nombres oficiales de aulas y laboratorios disponibles.")
    total: int = Field(..., description="Total de recintos disponibles.")
