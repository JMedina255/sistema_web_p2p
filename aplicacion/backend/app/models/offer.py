from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class SesionMentoria(Base):
    """
    Entidad SesionMentoria / OfertaMentoria (T-14 / T-15 / T-16 / RF08 / CUS06).
    Representa una oferta de mentoría académica programada y publicada por un mentor habilitado (RN-03).
    Aplica controles normativos:
    - RN-04: Antelación obligatoria mayor a 24 horas respecto al inicio de la sesión.
    - RN-05: Aforo estándar inmutable: 10 cupos para Presencial, 20 cupos para Virtual.
    - RN-06: Asignación de infraestructura física para modalidad presencial.
    - RN-07: Provisión de enlace institucional para modalidad virtual.
    """

    __tablename__ = "sesiones_mentoria"

    id_sesion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo_sesion: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    mentor_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    id_asignatura: Mapped[int] = mapped_column(
        Integer, ForeignKey("asignaturas.id_asignatura", ondelete="RESTRICT"), nullable=False, index=True
    )
    id_tema: Mapped[int] = mapped_column(
        Integer, ForeignKey("temas_conceptuales.id_tema", ondelete="RESTRICT"), nullable=False, index=True
    )
    fecha_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    duracion_minutos: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("duracion_minutos IN (60, 90)", name="chk_sesion_duracion"),
        default=60,
        nullable=False,
    )
    modalidad: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("modalidad IN ('presencial', 'virtual')", name="chk_sesion_modalidad"),
        nullable=False,
    )
    aforo_maximo: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("aforo_maximo IN (10, 20)", name="chk_sesion_aforo"),
        nullable=False,
    )
    espacio_asignado: Mapped[str] = mapped_column(String(255), nullable=False)
    notas_adicionales: Mapped[str | None] = mapped_column(Text, nullable=True)
    estado: Mapped[str] = mapped_column(
        String(30),
        CheckConstraint(
            "estado IN ('PUBLICADA', 'PENDIENTE_CONFIRMACION', 'CONFIRMADA', 'CANCELADA_SISTEMA', 'CANCELADA_MENTOR', 'FINALIZADA')",
            name="chk_sesion_estado",
        ),
        default="PUBLICADA",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    # Relaciones ORM
    asignatura = relationship("Asignatura", lazy="joined")
    tema = relationship("TemaConceptual", lazy="joined")
