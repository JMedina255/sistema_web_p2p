from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.profiles import _extract_caller_and_admin_status
from app.db.session import get_optional_session
from app.schemas.bitacora import BitacoraCreatePayload, BitacoraResponse
from app.services.bitacora_service import BitacoraService

router = APIRouter()


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
    caller_email = None
    is_admin = False
    if authorization:
        caller_email, is_admin = _extract_caller_and_admin_status(authorization)

    return BitacoraService.create_bitacora(
        db=db,
        session_id=id_sesion,
        payload=payload,
        caller_email=caller_email,
        is_admin=is_admin,
    )


@router.get(
    "/{id_sesion}/bitacora",
    response_model=BitacoraResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar bitácora pedagógica suscrita de una sesión (T-35 / RF17 / CUS13)",
)
def get_session_bitacora(
    id_sesion: int,
    db: Session | None = Depends(get_optional_session),
) -> BitacoraResponse:
    """
    Retorna la bitácora pedagógica registrada y firmada digitalmente para una sesión de mentoría.
    """
    return BitacoraService.get_bitacora(
        db=db,
        session_id=id_sesion,
    )
