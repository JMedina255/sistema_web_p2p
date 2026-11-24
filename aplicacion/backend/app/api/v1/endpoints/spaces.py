"""
Endpoints REST para el subsistema de Espacios Físicos, Cronogramas y Parser de Horarios (RF10 / CUS11 / MOD-04).
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.core.dependencies import AuthenticatedUser, require_role
from app.db.session import get_required_session
from app.schemas.spaces import ClassroomListResponse, FreeSlotItem, ScheduleImportResponse
from app.services.offer_service import OfferService
from app.services.schedule_parser_service import (
    ExcepcionFormatoHorarioInvalido,
    ScheduleParserService,
)

router = APIRouter()


@router.post(
    "/import-schedule",
    response_model=ScheduleImportResponse,
    status_code=status.HTTP_200_OK,
    summary="Cargar y procesar cronograma oficial de aulas y laboratorios (RF10 / CUS11)",
    description=(
        "Permite al Administrador subir un archivo estructurado en Excel (.xls, .xlsx) o PDF (.pdf) "
        "con la distribución horaria oficial de la facultad. El componente interno de backend "
        "(Parser de horarios) extrae automáticamente los recintos y franjas libres, actualizando "
        "el catálogo de infraestructura física disponible para prevenir solapamientos presenciales (RN-06)."
    ),
)
async def import_academic_schedule(
    file: UploadFile = File(..., description="Archivo oficial en formato Excel (.xls, .xlsx) o PDF (.pdf)."),
    db: Session | None = Depends(get_required_session),
    current_user: AuthenticatedUser = Depends(require_role("administrador")),
) -> ScheduleImportResponse:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar un archivo con nombre y extensión válidos (.xlsx o .pdf).",
        )

    try:
        content = await file.read()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al leer los datos del archivo transmitido: {str(exc)}",
        ) from exc

    try:
        result = ScheduleParserService.procesar_cronograma_administrador(
            filename=file.filename,
            content=content,
            db=db,
        )
        return ScheduleImportResponse(**result)
    except ExcepcionFormatoHorarioInvalido as exc:
        raise exc
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error inesperado al procesar el cronograma: {str(exc)}",
        ) from exc


@router.get(
    "/free-slots",
    response_model=list[FreeSlotItem],
    summary="Consultar franjas horarias y recintos físicos libres (RF09 / RF10 / RN-06)",
    description="Retorna las franjas horarias libres extraídas del cronograma oficial procesado, con filtros opcionales.",
)
def get_free_physical_slots(
    db: Session | None = Depends(get_required_session),
    dia: str | None = Query(None, description="Filtrar por día de la semana (ej. 'Lunes', 'Martes')."),
    aula: str | None = Query(
        None, description="Filtrar por nombre o código del aula/laboratorio (ej. 'Lab 01')."
    ),
) -> list[FreeSlotItem]:
    slots = ScheduleParserService.get_active_slots(dia=dia, aula=aula, db=db)
    return [FreeSlotItem(**s) for s in slots]


@router.get(
    "/classrooms",
    response_model=ClassroomListResponse,
    summary="Listar recintos físicos disponibles en la facultad (RN-06)",
    description="Retorna la lista de aulas y laboratorios validados a partir del cronograma oficial activo.",
)
def get_available_classrooms(
    fecha_inicio: datetime | None = None,
    duracion_minutos: int = Query(60, ge=60, le=90),
    db: Session | None = Depends(get_required_session),
) -> ClassroomListResponse:
    if duracion_minutos not in (60, 90):
        raise HTTPException(422, "La duración debe ser de 60 o 90 minutos.")
    classrooms = (
        ScheduleParserService.get_classrooms(db=db)
        if fecha_inicio is None
        else OfferService.available_classrooms(db, fecha_inicio, duracion_minutos)
    )
    return ClassroomListResponse(aulas=classrooms, total=len(classrooms))
