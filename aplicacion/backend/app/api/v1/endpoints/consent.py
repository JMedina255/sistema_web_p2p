from fastapi import APIRouter, Depends, Header, Query, Request, status
from sqlalchemy.orm import Session

from app.core.dependencies import check_resource_ownership, get_optional_current_user
from app.db.session import get_optional_session
from app.schemas.consent import (
    ConsentAcceptRequest,
    ConsentOperationResponse,
    ConsentRevokeRequest,
    ConsentStatusResponse,
)
from app.services.consent_service import ConsentService

router = APIRouter()


@router.get(
    "/status",
    response_model=ConsentStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar estado de consentimiento informado (Ley N° 29733)",
    description="Retorna si el usuario registra consentimiento vigente, versión aceptada y estampa temporal UTC (T-05 / RF02 / RN-02).",
)
def get_consent_status(
    email: str = Query(..., description="Correo institucional oficial @upt.pe"),
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
):
    user = get_optional_current_user(authorization)
    if user:
        check_resource_ownership(user, email, allow_admin=True)
    return ConsentService.get_consent_status(db=db, email=email)


@router.post(
    "/accept",
    response_model=ConsentOperationResponse,
    status_code=status.HTTP_200_OK,
    summary="Registrar aceptación de consentimiento informado digital",
    description="Almacena la conformidad formal del estudiante para el tratamiento de datos personales y emparejamiento Top-k con auditoría de IP y User Agent.",
)
def accept_consent(
    payload: ConsentAcceptRequest,
    request: Request,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
):
    user = get_optional_current_user(authorization)
    if user:
        check_resource_ownership(user, payload.email, allow_admin=True)
    ip_addr = payload.ip_address or (request.client.host if request.client else None)
    ua = payload.user_agent or request.headers.get("user-agent")
    return ConsentService.accept_consent(
        db=db,
        email=payload.email,
        accepted=payload.accepted,
        terms_version=payload.terms_version,
        ip_address=ip_addr,
        user_agent=ua,
    )


@router.post(
    "/revoke",
    response_model=ConsentOperationResponse,
    status_code=status.HTTP_200_OK,
    summary="Revocar consentimiento informado digital (Efecto bloqueante RN-02)",
    description="Revoca la autorización de tratamiento de datos personales, provocando el bloqueo preventivo del acceso a los servicios de la plataforma.",
)
def revoke_consent(
    payload: ConsentRevokeRequest,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
):
    user = get_optional_current_user(authorization)
    if user:
        check_resource_ownership(user, payload.email, allow_admin=True)
    return ConsentService.revoke_consent(db=db, email=payload.email)
