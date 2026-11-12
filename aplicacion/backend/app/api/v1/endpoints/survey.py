from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_optional_session
from app.schemas.survey import SurveyCreatePayload, SurveyResponse, SurveyStatusResponse
from app.services.survey_service import SurveyService

router = APIRouter()


@router.post(
    "/{id}/survey",
    response_model=SurveyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar evaluación de calidad post-mentoría (T-38 / T-39 / CUS05 / RF18 / RN-12 / RN-13)",
)
def submit_session_survey(
    id: int,
    payload: SurveyCreatePayload,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> SurveyResponse:
    """
    Registra la evaluación de calidad de la sesión de mentoría remitida por un estudiante con asistencia confirmada.
    Aplica controles normativos:
    - RN-12: Validación estricta de asistencia efectiva (asistio = True).
    - RN-13: Límite perentorio de 24 horas tras la culminación de la sesión.
    - Prevención de re-evaluaciones duplicadas por estudiante.
    - Retroalimentación cualitativa sustantiva (>= 20 caracteres si se incluye).
    """
    user = get_current_user(authorization)
    return SurveyService.create_survey(
        db=db,
        session_id=id,
        payload=payload,
        caller_email=user.email,
    )


@router.get(
    "/{id}/survey",
    response_model=SurveyStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar elegibilidad y ventana de encuesta post-mentoría",
)
def get_session_survey_status(
    id: int,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> SurveyStatusResponse:
    """
    Verifica si el usuario autenticado está habilitado para responder la encuesta
    de satisfacción y si la ventana temporal de 24h permanece abierta.
    """
    user = get_current_user(authorization)
    return SurveyService.get_survey_status(
        db=db,
        session_id=id,
        caller_email=user.email,
    )
