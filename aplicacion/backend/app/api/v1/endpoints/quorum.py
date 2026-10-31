from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from app.db.session import get_optional_session
from app.schemas.booking import (
    QuorumEvaluationPayload,
    QuorumEvaluationResponse,
)
from app.services.booking_service import BookingService

router = APIRouter()


@router.post(
    "/evaluate",
    response_model=QuorumEvaluationResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluar quórum normativo institucional del 50% a T-24h (RN-08 / RN-09 / CUS23)",
)
def evaluate_session_quorum(
    payload: QuorumEvaluationPayload,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> QuorumEvaluationResponse:
    """
    Evalúa la ratificación de vacantes de una sesión al cumplirse la ventana de corte T-24h.
    Caduca automáticamente las reservas no confirmadas a NO_CONFIRMADA y determina
    si la sesión alcanza el quórum mínimo reglamentario del 50%.
    """
    return BookingService.evaluate_quorum(
        db=db,
        id_sesion=payload.id_sesion,
    )
