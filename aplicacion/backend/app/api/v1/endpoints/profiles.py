from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
)
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
    explicit_email: str | None = None,
    allow_admin_override: bool = True,
) -> str:
    """
    Función de resolución y validación que delega a get_current_user y valida la titularidad del correo.
    Garantiza que no exista bypass por entorno.
    """
    current_user = get_current_user(authorization)
    if explicit_email and explicit_email.strip():
        clean_target = explicit_email.strip().lower()
        if clean_target != current_user.email:
            if allow_admin_override and current_user.is_admin:
                return clean_target
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Violación de autorización: no tiene permisos para acceder o modificar los datos de otro usuario.",
            )
        return clean_target
    return current_user.email


def _extract_caller_and_admin_status(
    authorization: str | None,
    explicit_email: str | None = None,
) -> tuple[str, bool]:
    """
    Extrae el correo del llamante autenticado y su condición de administrador de forma centralizada.
    """
    current_user = get_current_user(authorization)
    caller_email = _resolve_authenticated_email(
        authorization, explicit_email=explicit_email, allow_admin_override=True
    )
    return caller_email, current_user.is_admin


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
