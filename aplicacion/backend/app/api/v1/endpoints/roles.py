from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    AuthenticatedUser,
    check_resource_ownership,
    get_current_user,
)
from app.db.session import get_optional_session
from app.schemas.roles import (
    PromoteMentorRequest,
    RevokeMentorRequest,
    RoleOperationResponse,
    UserRolesResponse,
)
from app.services.role_service import RoleService

router = APIRouter()


@router.get(
    "/users/{email}",
    response_model=UserRolesResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar roles institucionales activos de un usuario",
    description="Retorna el listado de roles vigentes (mentoreado, mentor, administrador) para el correo institucional provisto (T-08 / RF03 / CUS10).",
)
def get_user_roles(
    email: str = Path(..., description="Correo electrónico institucional @upt.pe"),
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session | None = Depends(get_optional_session),
):
    check_resource_ownership(
        current_user=current_user,
        owner_email=email,
        allow_admin=True,
        error_message="Violación de autorización: no tiene permisos para consultar roles de otro usuario.",
    )
    roles = RoleService.get_user_roles(db=db, email=email)
    return UserRolesResponse(email=email, roles=roles, is_active=True)


@router.post(
    "/promote-mentor",
    response_model=RoleOperationResponse,
    status_code=status.HTTP_200_OK,
    summary="Promover estudiante al rol de Mentor con verificación de mérito (RN-03)",
    description="Verifica que el estudiante pertenezca al ciclo VII o superior y asigna el rol de mentor. Deniega la autopromoción no autorizada.",
)
def promote_mentor(
    payload: PromoteMentorRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session | None = Depends(get_optional_session),
):
    # Control estricto de privilegios administrativos
    if not current_user.is_admin:
        if current_user.email == payload.email.strip().lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="La autopromoción al rol de mentor no está permitida. Requiere autorización o asignación por la administración institucional.",
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Violación de autorización: la promoción al rol de mentor requiere privilegios de administrador.",
        )

    assigned_by = payload.assigned_by or current_user.email
    return RoleService.promote_to_mentor(
        db=db,
        email=payload.email,
        assigned_by=assigned_by,
    )


@router.post(
    "/revoke-mentor",
    response_model=RoleOperationResponse,
    status_code=status.HTTP_200_OK,
    summary="Revocar el rol de Mentor de un estudiante",
    description="Desactiva la condición de mentor del estudiante en el sistema institucional.",
)
def revoke_mentor(
    payload: RevokeMentorRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session | None = Depends(get_optional_session),
):
    # Control estricto de privilegios administrativos
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Violación de autorización: la revocación de roles institucionales requiere privilegios de administrador.",
        )

    revoked_by = payload.revoked_by or current_user.email
    return RoleService.revoke_mentor(
        db=db,
        email=payload.email,
        revoked_by=revoked_by,
    )
