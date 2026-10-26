from typing import Literal

from fastapi import APIRouter, Depends, Header, Query, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.profiles import _resolve_authenticated_email
from app.db.session import get_optional_session
from app.schemas.offer import PublishOfferPayload, PublishOfferResponse
from app.services.offer_service import OfferService

router = APIRouter()


@router.post(
    "",
    response_model=PublishOfferResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Publicar oferta de mentoría académica (T-14 / T-15 / RF08 / CUS06)",
)
def publish_offer(
    payload: PublishOfferPayload,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> PublishOfferResponse:
    """
    Publica una oferta de mentoría académica conforme a las reglas del sistema:
    - RN-03: Solo mentores autorizados (ciclo >= VII).
    - RN-04: Antelación obligatoria mayor a 24 horas respecto al inicio de la sesión.
    - RN-05: Aforo estándar estricto (10 presencial, 20 virtual).
    """
    caller_email = None
    if authorization:
        caller_email = _resolve_authenticated_email(
            authorization, explicit_email=payload.mentor_email, allow_admin_override=True
        )

    return OfferService.publish_offer(db=db, payload=payload, caller_email=caller_email)


@router.get(
    "",
    response_model=list[PublishOfferResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar catálogo de ofertas de mentoría activas (T-15 / RF08 / CUS06)",
)
def list_offers(
    mentor_email: str | None = Query(None, description="Filtrar por correo del mentor"),
    id_asignatura: int | None = Query(None, ge=1, description="Filtrar por asignatura crítica"),
    modalidad: Literal["presencial", "virtual"] | None = Query(None, description="Filtrar por modalidad"),
    estado: str | None = Query(None, description="Filtrar por estado de la sesión"),
    db: Session | None = Depends(get_optional_session),
) -> list[PublishOfferResponse]:
    """
    Retorna el listado de ofertas de mentoría disponibles para consulta y recomendación.
    """
    return OfferService.get_offers(
        db=db,
        mentor_email=mentor_email,
        id_asignatura=id_asignatura,
        modalidad=modalidad,
        estado=estado,
    )
