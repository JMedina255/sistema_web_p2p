from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.roles import Rol, UsuarioRol
from app.schemas.roles import RoleOperationResponse

# Almacén en memoria de respaldo para roles de usuario
_memory_user_roles: dict[str, set[str]] = {}


class RoleService:
    @staticmethod
    def get_user_roles(db: Session | None, email: str) -> list[str]:
        clean_email = email.strip().lower()

        if db is not None:
            try:
                roles = (
                    db.query(Rol.nombre_rol)
                    .join(UsuarioRol, UsuarioRol.id_rol == Rol.id_rol)
                    .filter(UsuarioRol.email == clean_email, UsuarioRol.activo.is_(True))
                    .all()
                )
                role_names = [r[0] for r in roles]
                if "mentoreado" not in role_names:
                    role_names.insert(0, "mentoreado")
                return role_names
            except Exception:
                pass

        if clean_email in _memory_user_roles:
            active_roles = list(_memory_user_roles[clean_email])
            if "mentoreado" not in active_roles:
                active_roles.insert(0, "mentoreado")
            return active_roles

        # Rol institucional por defecto para todo estudiante
        return ["mentoreado"]

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
            _memory_user_roles[clean_email] = {"mentoreado"}
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

        if clean_email in _memory_user_roles:
            _memory_user_roles[clean_email].discard("mentor")

        current_roles = RoleService.get_user_roles(db, clean_email)
        return RoleOperationResponse(
            success=True,
            email=clean_email,
            role="mentor",
            message="Rol de Mentor revocado exitosamente.",
            roles=current_roles,
        )
