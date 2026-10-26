from typing import Any

from fastapi import APIRouter, Depends, Header, Query, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.profiles import _resolve_authenticated_email
from app.db.session import get_optional_session
from app.schemas.recommendation import (
    MentorRecommendationItem,
    OfferRecommendationItem,
    RecommendationExplainRequest,
    RecommendationExplainResponse,
    RecommendationListResponse,
)
from app.services.recommendation_service import RecommendationService
from app.services.simulation_service import SimulationService

router = APIRouter()


@router.get(
    "/mentors",
    response_model=RecommendationListResponse[MentorRecommendationItem],
    status_code=status.HTTP_200_OK,
    summary="Recomendar mentores Top-k para un mentoreado (T-15 / T-16 / RF06 / CUS02)",
)
def get_recommended_mentors(
    mentee_email: str | None = Query(None, description="Correo del estudiante mentoreado"),
    top_k: int = Query(5, ge=1, le=20, description="Número de candidatos en el ranking"),
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> RecommendationListResponse[MentorRecommendationItem]:
    """
    Retorna el ranking Top-k de mentores más compatibles según afinidad curricular,
    solapamiento de temas silábicos, disponibilidad horaria (6x11), modalidad y mérito RN-03.
    """
    effective_email = mentee_email
    if authorization:
        effective_email = _resolve_authenticated_email(
            authorization, explicit_email=mentee_email, allow_admin_override=True
        )

    # Fallback si no se proveyó correo explícito ni token
    target_email = effective_email or "2022074255@upt.pe"

    return RecommendationService.recommend_mentors(
        mentee_email=target_email,
        top_k=top_k,
        db=db,
    )


@router.get(
    "/offers",
    response_model=RecommendationListResponse[OfferRecommendationItem],
    status_code=status.HTTP_200_OK,
    summary="Recomendar ofertas de mentoría activas Top-k (T-15 / T-16 / RF06 / CUS02)",
)
def get_recommended_offers(
    mentee_email: str | None = Query(None, description="Correo del estudiante mentoreado"),
    id_asignatura: int | None = Query(None, ge=1, description="Filtrar por asignatura crítica"),
    top_k: int = Query(5, ge=1, le=20, description="Número de ofertas en el ranking"),
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> RecommendationListResponse[OfferRecommendationItem]:
    """
    Retorna el ranking Top-k de sesiones de mentoría programadas en el catálogo activo,
    optimizadas por compatibilidad temporal directa, tema de estudio y aforo RN-05.
    """
    effective_email = mentee_email
    if authorization:
        effective_email = _resolve_authenticated_email(
            authorization, explicit_email=mentee_email, allow_admin_override=True
        )

    target_email = effective_email or "2022074255@upt.pe"

    return RecommendationService.recommend_offers(
        mentee_email=target_email,
        top_k=top_k,
        id_asignatura=id_asignatura,
        db=db,
    )


@router.post(
    "/explain",
    response_model=RecommendationExplainResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener desglose explicable de compatibilidad EdRecSys (T-15 / T-16 / RNF03)",
)
def explain_recommendation(
    payload: RecommendationExplainRequest,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> RecommendationExplainResponse:
    """
    Desglosa matemáticamente y en lenguaje institucional el puntaje de compatibilidad asignado
    a un mentor o a una oferta específica respecto a las necesidades del mentoreado.
    """
    if authorization:
        _resolve_authenticated_email(
            authorization, explicit_email=payload.mentee_email, allow_admin_override=True
        )

    return RecommendationService.explain_score(
        mentee_email=payload.mentee_email,
        mentor_email=payload.mentor_email,
        id_oferta=payload.id_oferta,
        db=db,
    )


@router.get(
    "/simulation/testbench",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Ejecutar banco de pruebas algorítmico y casos frontera (T-18 / RNF03)",
)
def run_simulation_testbench() -> dict[str, Any]:
    """
    Ejecuta el testbench con perfiles sintéticos EPIS-UPT, evaluando ordenamiento determinista,
    latencia por evaluación y los 4 casos frontera algorítmicos.
    """
    return SimulationService.run_benchmark()
