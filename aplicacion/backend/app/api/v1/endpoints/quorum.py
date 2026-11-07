from fastapi import APIRouter, Depends, Header, Query, status
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
    mode: str | None = Query(None, description="Modo de evaluación ('sprint6' o estándar)"),
    db: Session | None = Depends(get_optional_session),
) -> QuorumEvaluationResponse:
    """
    Evalúa la ratificación de vacantes de una sesión al cumplirse la ventana de corte T-24h.
    Caduca automáticamente las reservas no confirmadas y determina si la sesión alcanza el quórum reglamentario.
    """
    if mode == "sprint6":
        return BookingService.evaluate_session_quorum(
            db=db,
            id_sesion=payload.id_sesion,
        )
    return BookingService.evaluate_quorum(
        db=db,
        id_sesion=payload.id_sesion,
    )


@router.post(
    "/evaluate-all",
    response_model=list[QuorumEvaluationResponse],
    status_code=status.HTTP_200_OK,
    summary="Evaluar quórum desatendido para todas las sesiones en T-24h (T-29 / T-30 / RF15 / CUS23)",
)
def evaluate_all_active_quorums(
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> list[QuorumEvaluationResponse]:
    """
    Motor desatendido de evaluación de quórum a T-24h con control de idempotencia y cerrojo pesimista.
    Identifica sesiones en estado PUBLICADA en la ventana de corte, evalúa cumplimiento de quórum (3 presencial / 5 virtual),
    transiciona a CONFIRMADA o QUORUM_INSUFICIENTE e inhabilita reevaluaciones redundantes.
    """
    return BookingService.evaluate_all_active_quorums(db=db)
