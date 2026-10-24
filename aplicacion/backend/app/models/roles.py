from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Rol(Base):
    """
    Entidad Rol institucional (T-08 / RF03 / CUS10).
    Catálogo de perfiles y permisos en la plataforma: mentoreado, mentor, administrador.
    """

    __tablename__ = "roles"

    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_rol: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

    usuarios: Mapped[list["UsuarioRol"]] = relationship(
        "UsuarioRol", back_populates="rol", cascade="all, delete-orphan"
    )


class UsuarioRol(Base):
    """
    Entidad de asignación UsuarioRol (T-08 / RF03 / CUS10 / RN-03).
    Asocia un correo institucional @upt.pe con uno o más roles del sistema.
    """

    __tablename__ = "usuario_roles"
    __table_args__ = (UniqueConstraint("email", "id_rol", name="uq_usuario_roles_email_rol"),)

    id_usuario_rol: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    id_rol: Mapped[int] = mapped_column(
        Integer, ForeignKey("roles.id_rol", ondelete="CASCADE"), nullable=False
    )
    fecha_asignacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    asignado_por: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    rol: Mapped["Rol"] = relationship("Rol", back_populates="usuarios")
