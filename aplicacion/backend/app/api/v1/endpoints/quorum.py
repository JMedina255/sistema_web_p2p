from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import AuthenticatedUser, get_current_user, require_role
from app.db.session import get_required_session
from app.schemas.booking import (
    QuorumEvaluationPayload,
    QuorumEvaluationResponse,
)
from app.schemas.offer import QuorumOverviewItem
from app.services.booking_service import BookingService

router = APIRouter()


@router.get("/overview", response_model=list[QuorumOverviewItem])
def quorum_overview(
    user: AuthenticatedUser = Depends(require_role("administrador")),
    db: Session | None = Depends(get_required_session),
) -> list[QuorumOverviewItem]:
    return BookingService.get_quorum_overview(db)


@router.post(
    "/evaluate",
    response_model=QuorumEvaluationResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluar quórum según el porcentaje configurado a T-24h (RN-08 / RN-09 / CUS23)",
)
def evaluate_session_quorum(
    payload: QuorumEvaluationPayload,
    authorization: str | None = Header(None),
    mode: str | None = Query(None, description="Modo de evaluación ('sprint6' o estándar)"),
    db: Session | None = Depends(get_required_session),
) -> QuorumEvaluationResponse:
    """
    Evalúa la ratificación de vacantes de una sesión al cumplirse la ventana de corte T-24h.
    Caduca automáticamente las reservas no confirmadas y determina si la sesión alcanza el quórum reglamentario.
    """
    get_current_user(authorization)
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
    db: Session | None = Depends(get_required_session),
) -> list[QuorumEvaluationResponse]:
    """
    Motor desatendido de evaluación de quórum a T-24h con control de idempotencia y cerrojo pesimista.
    Identifica sesiones en estado PUBLICADA en la ventana de corte, evalúa cumplimiento de quórum (porcentaje configurado del aforo),
    transiciona a CONFIRMADA o QUORUM_INSUFICIENTE e inhabilita reevaluaciones redundantes.
    """
    user = get_current_user(authorization)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Violación de autorización: la evaluación masiva de quórum requiere privilegios de administrador.",
        )

    return BookingService.evaluate_all_active_quorums(db=db)
