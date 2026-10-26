from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_access_token
from app.db.session import get_optional_session
from app.schemas.profile import (
    AcademicProfileResponse,
    AcademicProfileUpdate,
    AvailabilityOperationResponse,
    AvailabilityResponse,
    AvailabilityUpdatePayload,
)
from app.services.profile_service import ProfileService

router = APIRouter()


def _resolve_authenticated_email(
    authorization: str | None,
    explicit_email: str | None,
    allow_admin_override: bool = True,
) -> str:
    """
    Resuelve y autoriza la identidad del estudiante a partir del token JWT Bearer,
    con fallback al correo explícito en entorno de desarrollo o pruebas.
    Garantiza el aislamiento de acceso entre usuarios (T-13 / RNF02).
    """
    if authorization:
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Formato de cabecera Authorization inválido. Se espera Bearer <token>.",
            )
        token = authorization.split(" ", 1)[1].strip()
        decoded = decode_access_token(token)
        if not decoded:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autenticación expirado o inválido.",
            )

        caller_email = decoded.get("sub") or decoded.get("email")
        if not caller_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El token no contiene una identidad de usuario válida.",
            )

        caller_roles = decoded.get("roles", [])
        if explicit_email and explicit_email.strip().lower() != caller_email.strip().lower():
            if allow_admin_override and "administrador" in caller_roles:
                return explicit_email.strip().lower()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Violación de autorización: no tiene permisos para acceder o modificar los datos de otro usuario.",
            )

        return caller_email.strip().lower()

    if explicit_email and explicit_email.strip():
        if settings.APP_ENV in ("development", "test", "testing"):
            return explicit_email.strip().lower()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="En entornos de producción se requiere cabecera Authorization: Bearer <token>.",
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Se requiere autenticación mediante cabecera Authorization: Bearer <token> o parámetro email.",
    )


@router.get(
    "/me",
    response_model=AcademicProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar perfil formativo académico del estudiante",
    description="Retorna el perfil formativo con materias filtro de interés, ciclo y modalidad preferida (T-12 / RF04 / CUS15).",
)
def get_profile(
    email: str | None = Query(None, description="Correo institucional (opcional si se provee Bearer token)"),
    authorization: str | None = Header(None, description="Cabecera Authorization: Bearer <token>"),
    db: Session | None = Depends(get_optional_session),
):
    target_email = _resolve_authenticated_email(authorization, email)
    return ProfileService.get_profile(db=db, email=target_email)


@router.put(
    "/me",
    response_model=AcademicProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar perfil formativo académico y postulación",
    description="Actualiza el perfil del estudiante verificando la regla de mérito RN-03 si postula al rol de Mentor.",
)
def update_profile(
    payload: AcademicProfileUpdate,
    authorization: str | None = Header(None, description="Cabecera Authorization: Bearer <token>"),
    db: Session | None = Depends(get_optional_session),
):
    target_email = _resolve_authenticated_email(authorization, payload.email)
    return ProfileService.update_profile(db=db, email=target_email, payload=payload)


@router.get(
    "/availability",
    response_model=AvailabilityResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar matriz semanal de disponibilidad horaria",
    description="Retorna las franjas horarias seleccionadas por el estudiante entre Lunes y Sábado.",
)
def get_availability(
    email: str | None = Query(None, description="Correo institucional"),
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
):
    target_email = _resolve_authenticated_email(authorization, email)
    slots = ProfileService.get_availability(db=db, email=target_email)
    return AvailabilityResponse(email=target_email, slots=slots, total_slots=len(slots))


@router.put(
    "/availability",
    response_model=AvailabilityOperationResponse,
    status_code=status.HTTP_200_OK,
    summary="Reemplazar atómicamente la matriz semanal de disponibilidad horaria",
    description="Actualiza de forma completa la agenda de bloques horarios semanales del estudiante.",
)
def update_availability(
    payload: AvailabilityUpdatePayload,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
):
    target_email = _resolve_authenticated_email(authorization, payload.email)
    result = ProfileService.update_availability(db=db, email=target_email, slots=payload.slots)
    return AvailabilityOperationResponse(**result)
