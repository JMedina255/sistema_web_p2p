from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class EncuestaCalidad(Base):
    """
    Entidad EncuestaCalidad (T-38 / T-39 / CUS05 / RF18 / RN-12 / RN-13).
    Registra la evaluación de calidad post-mentoría emitida por los asistentes confirmados:
    - Escala Likert de 1 a 5 estrellas en 4 dimensiones formativas.
    - Retroalimentación cualitativa sustantiva (>= 20 caracteres si se incluye).
    - Restricción estricta de asistencia (RN-12) y ventana perentoria de 24 horas (RN-13).
    - Unicidad por sesión y estudiante evaluador.
    """

    __tablename__ = "encuestas_calidad"
    __table_args__ = (
        UniqueConstraint("id_sesion", "estudiante_email", name="uq_encuesta_sesion_estudiante"),
        CheckConstraint(
            "calificacion_general >= 1 AND calificacion_general <= 5", name="chk_encuesta_calif_gen"
        ),
        CheckConstraint("dominio_tema >= 1 AND dominio_tema <= 5", name="chk_encuesta_dominio"),
        CheckConstraint(
            "claridad_explicacion >= 1 AND claridad_explicacion <= 5", name="chk_encuesta_claridad"
        ),
        CheckConstraint("puntualidad >= 1 AND puntualidad <= 5", name="chk_encuesta_puntualidad"),
    )

    id_encuesta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_sesion: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sesiones_mentoria.id_sesion", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    estudiante_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    calificacion_general: Mapped[int] = mapped_column(Integer, nullable=False)
    dominio_tema: Mapped[int] = mapped_column(Integer, nullable=False)
    claridad_explicacion: Mapped[int] = mapped_column(Integer, nullable=False)
    puntualidad: Mapped[int] = mapped_column(Integer, nullable=False)
    comentarios: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    sesion = relationship("SesionMentoria", backref="encuestas", lazy="joined")
