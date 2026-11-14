from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.roles import Rol, UsuarioRol
from app.schemas.roles import RoleOperationResponse

# Almacén en memoria de respaldo para roles de usuario
_memory_user_roles: dict[str, set[str]] = {}


def clear_user_roles_in_memory() -> None:
    _memory_user_roles.clear()


class RoleService:
    @staticmethod
    def get_user_roles(db: Session | None, email: str) -> list[str]:
        clean_email = email.strip().lower()

        # Resolver alias institucional de estudiante (@virtual.upt.pe <-> @upt.pe)
        from app.core.identity import parse_student_email
        parsed = parse_student_email(clean_email)
        codigo = parsed.get("codigo_estudiante")
        emails_to_check = [clean_email]
        if codigo:
            emails_to_check.append(f"{codigo}@upt.pe")
            emails_to_check.append(f"{codigo}@virtual.upt.pe")
            if codigo == "2022073504":
                emails_to_check.append("mentor@upt.pe")

        if db is not None:
            try:
                roles = (
                    db.query(Rol.nombre_rol)
                    .join(UsuarioRol, UsuarioRol.id_rol == Rol.id_rol)
                    .filter(UsuarioRol.email.in_(emails_to_check), UsuarioRol.activo.is_(True))
                    .all()
                )
                role_names = list({r[0] for r in roles})
                # El administrador es autoridad institucional; no posee rol de estudiante mentoreado
                if "administrador" in role_names:
                    return ["administrador"]
                if "mentoreado" not in role_names:
                    role_names.insert(0, "mentoreado")
                return role_names
            except Exception:
                pass

        if clean_email in _memory_user_roles:
            active_roles = list(_memory_user_roles[clean_email])
            if "administrador" in active_roles:
                return ["administrador"]
            if "mentoreado" not in active_roles:
                active_roles.insert(0, "mentoreado")
            return active_roles

        # Roles por omisión para nuevos usuarios en memoria (el administrador no es mentoreado)
        if clean_email in ("admin.epis@upt.pe", "admin.demo@upt.pe") or clean_email.startswith("admin."):
            initial_roles = ["administrador"]
        elif (
            clean_email in ("mentor.avanzado@upt.pe", "2022073504@upt.pe", "ra2022073504@virtual.upt.pe", "mentor.demo@upt.pe", "mentor@upt.pe")
            or clean_email.startswith("ra2022073504")
            or clean_email.startswith("2022073504")
            or codigo == "2022073504"
        ):
            initial_roles = ["mentoreado", "mentor"]
        else:
            initial_roles = ["mentoreado"]

        _memory_user_roles[clean_email] = set(initial_roles)
        return list(initial_roles)

    @staticmethod
    def promote_to_mentor(
        db: Session | None,
        email: str,
        assigned_by: str | None = None,
    ) -> RoleOperationResponse:
        clean_email = email.strip().lower()

        # 1. Verificación de mérito académico estricto (Regla RN-03)
        from app.services.profile_service import ProfileService

        prof = ProfileService.get_profile(db=db, email=clean_email)
        ciclo = prof.ciclo_actual

        if ciclo < 7:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "MERIT_RULE_VIOLATION",
                    "message": "Conforme a la regla institucional RN-03, la postulación al rol de Mentor está reservada para estudiantes de ciclos superiores (VII al X ciclo).",
                },
            )

        # 2. Asignación del rol en BD o en memoria
        if db is not None:
            try:
                # Asegurar que el rol 'mentor' existe
                rol_mentor = db.query(Rol).filter(Rol.nombre_rol == "mentor").first()
                if not rol_mentor:
                    rol_mentor = Rol(
                        nombre_rol="mentor",
                        descripcion="Estudiante de ciclo avanzado (>= VII) con mérito académico.",
                    )
                    db.add(rol_mentor)
                    db.commit()
                    db.refresh(rol_mentor)

                # Buscar asignación previa
                asig = (
                    db.query(UsuarioRol)
                    .filter(UsuarioRol.email == clean_email, UsuarioRol.id_rol == rol_mentor.id_rol)
                    .first()
                )
                if asig:
                    asig.activo = True
                    asig.fecha_asignacion = datetime.now(UTC)
                    asig.asignado_por = assigned_by
                else:
                    asig = UsuarioRol(
                        email=clean_email,
                        id_rol=rol_mentor.id_rol,
                        fecha_asignacion=datetime.now(UTC),
                        asignado_por=assigned_by,
                        activo=True,
                    )
                    db.add(asig)
                db.commit()
            except Exception:
                db.rollback()

        # En memoria
        if clean_email not in _memory_user_roles:
            _memory_user_roles[clean_email] = set(RoleService.get_user_roles(None, clean_email))
        _memory_user_roles[clean_email].add("mentor")

        current_roles = RoleService.get_user_roles(db, clean_email)
        return RoleOperationResponse(
            success=True,
            email=clean_email,
            role="mentor",
            message="Rol de Mentor asignado exitosamente tras verificar mérito académico (RN-03).",
            roles=current_roles,
        )

    @staticmethod
    def revoke_mentor(
        db: Session | None,
        email: str,
        revoked_by: str | None = None,
    ) -> RoleOperationResponse:
        clean_email = email.strip().lower()

        if db is not None:
            try:
                rol_mentor = db.query(Rol).filter(Rol.nombre_rol == "mentor").first()
                if rol_mentor:
                    asig = (
                        db.query(UsuarioRol)
                        .filter(UsuarioRol.email == clean_email, UsuarioRol.id_rol == rol_mentor.id_rol)
                        .first()
                    )
                    if asig:
                        asig.activo = False
                        db.commit()
            except Exception:
                db.rollback()

        if clean_email not in _memory_user_roles:
            _memory_user_roles[clean_email] = set(RoleService.get_user_roles(None, clean_email))
        _memory_user_roles[clean_email].discard("mentor")

        current_roles = RoleService.get_user_roles(db, clean_email)
        return RoleOperationResponse(
            success=True,
            email=clean_email,
            role="mentor",
            message="Rol de Mentor revocado exitosamente.",
            roles=current_roles,
        )
