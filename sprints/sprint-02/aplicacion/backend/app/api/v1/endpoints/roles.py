from fastapi import APIRouter, Depends, Header, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_access_token
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
    db: Session | None = Depends(get_optional_session),
):
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
    authorization: str | None = Header(None, description="Token JWT de autorización"),
    db: Session | None = Depends(get_optional_session),
):
    assigned_by = payload.assigned_by

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
        # Denegación de autopromoción si el usuario intenta promoverse a sí mismo sin rol de administrador
        if (
            caller_email.strip().lower() == payload.email.strip().lower()
            and "administrador" not in caller_roles
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="La autopromoción al rol de mentor no está permitida. Requiere autorización o asignación por la administración institucional.",
            )
        if not assigned_by:
            assigned_by = caller_email
    elif settings.APP_ENV not in ("development", "test", "testing"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere autenticación mediante cabecera Authorization: Bearer <token>.",
        )

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
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
):
    revoked_by = payload.revoked_by
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
        if (
            "administrador" not in caller_roles
            and caller_email.strip().lower() != payload.email.strip().lower()
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Violación de autorización: no tiene permisos para revocar roles de otro usuario.",
            )
        if not revoked_by:
            revoked_by = caller_email
    elif settings.APP_ENV not in ("development", "test", "testing"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere autenticación mediante cabecera Authorization: Bearer <token>.",
        )

    return RoleService.revoke_mentor(
        db=db,
        email=payload.email,
        revoked_by=revoked_by,
    )
