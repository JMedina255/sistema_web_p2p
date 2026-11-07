"""
Módulo de Dependencias Centralizadas de Autenticación y Autorización (RBAC)
==========================================================================
Sistema Web P2P de Mentorías Académicas — EPIS UPT.

Provee dependencias FastAPI reutilizables para:
- Extracción y validación estricta de tokens JWT institucionales (HS256).
- Verificación de roles institucionales (mentoreado, mentor, administrador).
- Verificación de titularidad de recursos (resource ownership) con override administrativo.
- Eliminación de atajos o bypasses de desarrollo en endpoints privados.
"""

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.security import decode_access_token


class AuthenticatedUser(BaseModel):
    """Representación inmutable de la identidad y privilegios del usuario autenticado."""

    email: str
    roles: list[str] = Field(default_factory=list)

    def has_role(self, role: str) -> bool:
        """Determina si el usuario posee un rol institucional específico (case-insensitive)."""
        return role.strip().lower() in [r.strip().lower() for r in self.roles]

    @property
    def is_admin(self) -> bool:
        """Indica si el usuario cuenta con el rol verificado de administrador."""
        return self.has_role("administrador")

    @property
    def is_mentor(self) -> bool:
        """Indica si el usuario cuenta con el rol verificado de mentor."""
        return self.has_role("mentor")

    @property
    def is_mentee(self) -> bool:
        """Indica si el usuario cuenta con el rol de mentoreado."""
        return self.has_role("mentoreado")


def get_current_user(
    authorization: Annotated[
        str | None,
        Header(
            description="Cabecera HTTP de autorización con formato 'Bearer <token_jwt>'"
        ),
    ] = None,
) -> AuthenticatedUser:
    """
    Dependencia FastAPI que autentica obligatoriamente al usuario mediante Bearer JWT.

    Reglas de seguridad:
    1. Si la cabecera está ausente -> HTTP 401 Unauthorized.
    2. Si el formato no inicia con 'Bearer ' -> HTTP 401 Unauthorized.
    3. Si el token es nulo, vacío, simulado ('mock.') o inválido -> HTTP 401 Unauthorized.
    4. Si el token está expirado -> HTTP 401 Unauthorized.
    5. Si el payload carece de 'sub' o 'email' -> HTTP 401 Unauthorized.
    6. No admite atajos ni bypasses por entorno (development / test / production).
    """
    if not authorization:
        if getattr(settings, "APP_ENV", "") == "production":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Se requiere autenticación: en entornos de producción se requiere cabecera Authorization: Bearer <token>.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere autenticación mediante cabecera Authorization: Bearer <token>.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de cabecera Authorization inválido. Se espera Bearer <token>.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorización vacío o ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Rechazo estricto de tokens mock/simulados en la API real (SEC-16)
    if token.startswith("mock.") or token.endswith(".mock") or token == "mock-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación expirado o inválido: los tokens simulados no están autorizados en la API institucional.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación expirado o inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    raw_email = payload.get("sub") or payload.get("email")
    if not raw_email or not isinstance(raw_email, str) or not raw_email.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token no contiene una identidad de usuario válida.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    clean_email = raw_email.strip().lower()

    # Extracción y sanitización de roles
    raw_roles = payload.get("roles")
    if raw_roles is None:
        raw_role = payload.get("role")
        roles_list = [raw_role] if raw_role else ["mentoreado"]
    elif isinstance(raw_roles, list):
        roles_list = raw_roles
    elif isinstance(raw_roles, str):
        roles_list = [raw_roles]
    else:
        roles_list = ["mentoreado"]

    clean_roles = [str(r).strip().lower() for r in roles_list if str(r).strip()]
    if "mentoreado" not in clean_roles:
        clean_roles.insert(0, "mentoreado")

    return AuthenticatedUser(email=clean_email, roles=clean_roles)


def get_optional_current_user(
    authorization: Annotated[
        str | None,
        Header(description="Cabecera HTTP de autorización opcional 'Bearer <token>'"),
    ] = None,
) -> AuthenticatedUser | None:
    """
    Dependencia FastAPI que intenta autenticar al usuario si se provee una cabecera Bearer,
    o retorna None si la petición es de un visitante no autenticado.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization.split(" ", 1)[1].strip()
    if not token or token.startswith("mock."):
        return None

    payload = decode_access_token(token)
    if not payload:
        return None

    raw_email = payload.get("sub") or payload.get("email")
    if not raw_email or not isinstance(raw_email, str) or not raw_email.strip():
        return None

    clean_email = raw_email.strip().lower()
    raw_roles = payload.get("roles")
    if isinstance(raw_roles, list):
        clean_roles = [str(r).strip().lower() for r in raw_roles if str(r).strip()]
    elif isinstance(raw_roles, str):
        clean_roles = [raw_roles.strip().lower()]
    else:
        clean_roles = ["mentoreado"]

    if "mentoreado" not in clean_roles:
        clean_roles.insert(0, "mentoreado")

    return AuthenticatedUser(email=clean_email, roles=clean_roles)


def require_role(*required_roles: str) -> Callable[[AuthenticatedUser], AuthenticatedUser]:
    """
    Factoría de dependencias FastAPI para control de acceso RBAC estricto.
    Verifica que el usuario autenticado posea al menos uno de los roles institucionales exigidos.
    """
    target_roles = [r.strip().lower() for r in required_roles if r.strip()]

    def role_dependency(
        current_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    ) -> AuthenticatedUser:
        user_roles = set(current_user.roles)
        if not any(r in user_roles for r in target_roles):
            roles_formatted = ", ".join(target_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado: se requiere uno de los siguientes roles institucionales: {roles_formatted}.",
            )
        return current_user

    return role_dependency


def check_resource_ownership(
    current_user: AuthenticatedUser,
    owner_email: str,
    allow_admin: bool = True,
    error_message: str = "Violación de autorización: no tiene permisos para acceder o modificar los datos de otro usuario.",
) -> None:
    """
    Verifica que el usuario autenticado sea el titular del recurso que intenta operar.
    Permite acceso a administradores si allow_admin=True.
    Lanza HTTP 403 Forbidden si no tiene autorización.
    """
    caller = current_user.email.strip().lower()
    target = owner_email.strip().lower()

    if caller == target:
        return

    if allow_admin and current_user.is_admin:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=error_message,
    )
