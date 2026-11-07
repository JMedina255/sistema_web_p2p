from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, CheckConstraint, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class BitacoraPedagogica(Base):
    """
    Entidad BitacoraPedagogica (T-35 / T-36 / CUS13 / RF17 / RN-12).
    Registra el reporte pedagógico de cierre y acreditación provisional de horas:
    - RN-12: Ventana perentoria de 48 horas tras el fin de la sesión.
    - Observaciones pedagógicas sustantivas (mínimo 50 caracteres).
    - Sellado criptográfico con hash SHA-256.
    - Acreditación de horas calculadas: duracion_minutos / 60.0.
    """

    __tablename__ = "bitacoras_pedagogicas"

    id_bitacora: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_sesion: Mapped[int] = mapped_column(
        Integer, ForeignKey("sesiones_mentoria.id_sesion", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    id_mentor: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    temas_cubiertos: Mapped[list[Any]] = mapped_column(JSON, default=list, nullable=False)
    observaciones: Mapped[str] = mapped_column(Text, nullable=False)
    nivel_dificultad: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("nivel_dificultad IN ('Bajo', 'Medio', 'Alto')", name="chk_bitacora_dificultad"),
        default="Medio",
        nullable=False,
    )
    hash_firma: Mapped[str] = mapped_column(String(64), nullable=False)
    horas_declaradas: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    visado_administrador: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    sesion = relationship("SesionMentoria", backref="bitacora", lazy="joined")
