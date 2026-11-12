from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_optional_session
from app.schemas.bitacora import (
    BitacoraCreatePayload,
    BitacoraItemResponse,
    BitacoraObservacionResponse,
    BitacoraObservarPayload,
    BitacoraResponse,
    BitacoraVisadoResponse,
)
from app.services.bitacora_service import BitacoraService

router = APIRouter()
admin_router = APIRouter()


@router.post(
    "/{id_sesion}/bitacora",
    response_model=BitacoraResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar bitácora pedagógica y firmar reporte formativo (T-35 / RF17 / CUS13 / RN-12)",
)
def create_session_bitacora(
    id_sesion: int,
    payload: BitacoraCreatePayload,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> BitacoraResponse:
    """
    Registra el reporte pedagógico de la sesión de mentoría con firma criptográfica SHA-256.
    Aplica controles normativos:
    - RN-12: Ventana de 48 horas post-sesión.
    - Observaciones pedagógicas sustantivas (>= 50 caracteres).
    - Cómputo de horas provisionales: duracion_minutos / 60.0.
    """
    user = get_current_user(authorization)
    if not user.is_mentor and not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="FORBIDDEN: Solo el mentor titular o un administrador pueden registrar la bitácora pedagógica.",
        )

    return BitacoraService.create_bitacora(
        db=db,
        session_id=id_sesion,
        payload=payload,
        caller_email=user.email,
        is_admin=user.is_admin,
    )


@router.get(
    "/{id_sesion}/bitacora",
    response_model=BitacoraResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar bitácora pedagógica suscrita de una sesión (T-35 / RF17 / CUS13)",
)
def get_session_bitacora(
    id_sesion: int,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> BitacoraResponse:
    """
    Retorna la bitácora pedagógica registrada y firmada digitalmente para una sesión de mentoría.
    """
    get_current_user(authorization)
    return BitacoraService.get_bitacora(
        db=db,
        session_id=id_sesion,
    )


# --- Endpoints Administrativos de Fiscalización y Visado (T-41 / RF26 / RN-14 / Cuadro 4.2) ---


@admin_router.get(
    "",
    response_model=list[BitacoraItemResponse],
    status_code=status.HTTP_200_OK,
    summary="Bandeja de auditoría administrativa de bitácoras (T-40 / RF26)",
)
def list_bitacoras_admin(
    estado: str | None = Query(None, description="Filtro opcional por estado de sesión o bitácora"),
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> list[BitacoraItemResponse]:
    """
    Lista las bitácoras pedagógicas registradas para fiscalización de horas por la Dirección de Escuela.
    """
    user = get_current_user(authorization)
    return BitacoraService.list_bitacoras(
        db=db,
        estado_filtro=estado,
        caller_email=user.email,
        is_admin=user.is_admin,
    )


@admin_router.post(
    "/{id}/visar",
    response_model=BitacoraVisadoResponse,
    status_code=status.HTTP_200_OK,
    summary="Visar bitácora y convalidar horas acreditadas (T-41 / RF26 / RN-14)",
)
@router.post(
    "/{id}/visar",
    response_model=BitacoraVisadoResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
def visar_bitacora_admin(
    id: int,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> BitacoraVisadoResponse:
    """
    Visa institucionalmente la bitácora pedagógica, conmutando la sesión a HORAS_VISADAS
    y acumulando las horas académicamente acreditadas para certificación (RN-14).
    Exclusivo para rol administrador.
    """
    user = get_current_user(authorization)
    return BitacoraService.visar_bitacora(
        db=db,
        bitacora_id=id,
        caller_email=user.email,
        is_admin=user.is_admin,
    )


@admin_router.post(
    "/{id}/observar",
    response_model=BitacoraObservacionResponse,
    status_code=status.HTTP_200_OK,
    summary="Formular observación técnica sobre bitácora pedagógica (T-41 / RF26)",
)
@router.post(
    "/{id}/observar",
    response_model=BitacoraObservacionResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
def observar_bitacora_admin(
    id: int,
    payload: BitacoraObservarPayload,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> BitacoraObservacionResponse:
    """
    Registra una observación de auditoría sobre la bitácora pedagógica,
    transicionando la sesión a OBSERVADA para su subsanación por el mentor.
    """
    user = get_current_user(authorization)
    return BitacoraService.observar_bitacora(
        db=db,
        bitacora_id=id,
        motivo=payload.motivo,
        caller_email=user.email,
        is_admin=user.is_admin,
    )
