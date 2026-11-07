from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
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
