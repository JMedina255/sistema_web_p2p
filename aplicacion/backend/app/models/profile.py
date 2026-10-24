from datetime import UTC, datetime

from sqlalchemy import JSON, CheckConstraint, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class PerfilAcademico(Base):
    """
    Entidad PerfilAcademico (T-12 / RF04 / CUS15 / RNF04).
    Almacena los datos formativos, ciclo, rol de postulación, asignaturas críticas de interés
    y modalidad pedagógica preferida del estudiante.
    """

    __tablename__ = "perfiles_academicos"

    id_perfil: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    codigo_estudiante: Mapped[str | None] = mapped_column(String(20), nullable=True)
    nombres: Mapped[str | None] = mapped_column(String(100), nullable=True)
    apellidos: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ciclo_actual: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("ciclo_actual >= 1 AND ciclo_actual <= 10", name="chk_ciclo_actual"),
        default=1,
        nullable=False,
    )
    rol_postulacion: Mapped[str] = mapped_column(String(20), default="mentoreado", nullable=False)
    materias_interes: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    temas_seleccionados: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    biografia: Mapped[str | None] = mapped_column(Text, nullable=True)
    modalidad_preferida: Mapped[str] = mapped_column(String(20), default="presencial", nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class DisponibilidadHoraria(Base):
    """
    Entidad DisponibilidadHoraria (T-12 / RF04 / CUS15).
    Registra los bloques horarios de 1 hora disponibles en la semana (Lunes a Sábado).
    """

    __tablename__ = "disponibilidades_horarias"

    id_disponibilidad: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    dia_semana: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("dia_semana >= 1 AND dia_semana <= 6", name="chk_dia_semana"),
        nullable=False,
    )
    hora_inicio: Mapped[str] = mapped_column(String(10), nullable=False)
    hora_fin: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
