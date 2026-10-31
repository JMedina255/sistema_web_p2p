from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ReservaCupo(Base):
    """
    Entidad ReservaCupo (T-22 / T-24 / CUS04 / RF12 / RN-05 / RNF07).
    Representa una inscripción formal de un estudiante mentoreado a una sesión de mentoría.
    Gobernada por la máquina de estados finitos del Sprint 4:
    - PENDIENTE_CONFIRMACION: Estado inicial de reserva provisional.
    - CONFIRMADA: Ratificada por el estudiante antes de T-24h (RN-08).
    - CANCELADA_USUARIO: Desistimiento voluntario del estudiante (RN-10).
    - NO_CONFIRMADA: Caducada por falta de ratificación a T-24h (RN-08/RN-09).
    - CANCELADA_SISTEMA: Anulada por el mentor o sistema por falta de quórum (RN-09/RN-10).
    - ASISTIDA: Asistencia presencial o virtual constatada por el mentor (RN-12).
    - INASISTENCIA: Inasistencia no justificada registrada al cierre de bitácora (RN-12).
    """

    __tablename__ = "reservas_cupo"
    __table_args__ = (UniqueConstraint("id_sesion", "estudiante_email", name="uq_sesion_estudiante_activa"),)

    id_reserva: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo_reserva: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    id_sesion: Mapped[int] = mapped_column(
        Integer, ForeignKey("sesiones_mentoria.id_sesion", ondelete="CASCADE"), nullable=False, index=True
    )
    estudiante_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    estado: Mapped[str] = mapped_column(
        String(30),
        CheckConstraint(
            "estado IN ('PENDIENTE_CONFIRMACION', 'CONFIRMADA', 'CANCELADA_USUARIO', 'NO_CONFIRMADA', 'CANCELADA_SISTEMA', 'ASISTIDA', 'INASISTENCIA')",
            name="chk_reserva_estado",
        ),
        default="PENDIENTE_CONFIRMACION",
        nullable=False,
        index=True,
    )
    fecha_reserva: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    fecha_ratificacion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    motivo_cancelacion: Mapped[str | None] = mapped_column(Text, nullable=True)
    ticket_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relación ORM con SesionMentoria
    sesion = relationship("SesionMentoria", backref="reservas", lazy="joined")


class SolicitudDemanda(Base):
    """
    Entidad SolicitudDemanda (CUS03 / RF07).
    Registra solicitudes de asesoría temática por demanda cuando un estudiante
    no halla ofertas afines en el catálogo activo (Empty-State pedagógico).
    """

    __tablename__ = "solicitudes_demanda"

    id_demanda: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    estudiante_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    id_asignatura: Mapped[int] = mapped_column(
        Integer, ForeignKey("asignaturas.id_asignatura", ondelete="RESTRICT"), nullable=False, index=True
    )
    id_tema: Mapped[int] = mapped_column(
        Integer, ForeignKey("temas_conceptuales.id_tema", ondelete="RESTRICT"), nullable=False, index=True
    )
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
    estado: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("estado IN ('PENDIENTE', 'ATENDIDA', 'CANCELADA')", name="chk_demanda_estado"),
        default="PENDIENTE",
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    asignatura = relationship("Asignatura", lazy="joined")
    tema = relationship("TemaConceptual", lazy="joined")
