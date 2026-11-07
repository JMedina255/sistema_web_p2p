from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class AsistenciaSesion(Base):
    """
    Entidad AsistenciaSesion (T-34 / T-36 / CUS12 / RF17 / RN-05 / RN-12).
    Registra el pase de lista y presencia efectiva de los estudiantes:
    - Validación de reserva previa en estado CONFIRMADA.
    - Ventana temporal [inicio - 15m, fin + 30m].
    - Token dinámico TOTP de 30 segundos.
    """

    __tablename__ = "asistencias_sesion"
    __table_args__ = (
        UniqueConstraint("id_sesion", "estudiante_email", name="uq_sesion_asistencia_estudiante"),
    )

    id_asistencia: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_sesion: Mapped[int] = mapped_column(
        Integer, ForeignKey("sesiones_mentoria.id_sesion", ondelete="CASCADE"), nullable=False, index=True
    )
    estudiante_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    asistio: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    fecha_checkin: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ip_origen: Mapped[str | None] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    sesion = relationship("SesionMentoria", backref="asistencias", lazy="joined")
