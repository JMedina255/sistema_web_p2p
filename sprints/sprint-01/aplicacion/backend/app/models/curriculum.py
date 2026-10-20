from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Asignatura(Base):
    """
    Entidad AsignaturaFiltro (CUS21 / RF05 / MOD-02).
    Representa una asignatura crítica o formativa de la malla curricular de la EPIS-UPT.
    """

    __tablename__ = "asignaturas"

    id_asignatura: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo_curso: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    nombre_curso: Mapped[str] = mapped_column(String(150), nullable=False)
    ciclo_plan: Mapped[int] = mapped_column(Integer, nullable=False)
    creditos: Mapped[int] = mapped_column(Integer, nullable=False)
    es_prioritaria: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    factor_ponderacion: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    estado_activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    temas: Mapped[list["TemaConceptual"]] = relationship(
        "TemaConceptual",
        back_populates="asignatura",
        cascade="all, delete-orphan",
        order_by="TemaConceptual.unidad_silabica, TemaConceptual.id_tema",
    )


class TemaConceptual(Base):
    """
    Entidad TemaConceptual (CUS21 / RF05 / MOD-02).
    Representa una unidad silábica o concepto pedagógico específico dentro de una asignatura formativa.
    """

    __tablename__ = "temas_conceptuales"

    id_tema: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_asignatura: Mapped[int] = mapped_column(
        Integer, ForeignKey("asignaturas.id_asignatura", ondelete="CASCADE"), nullable=False, index=True
    )
    nombre_tema: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion_silabo: Mapped[str | None] = mapped_column(Text, nullable=True)
    unidad_silabica: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    estado_activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    asignatura: Mapped["Asignatura"] = relationship("Asignatura", back_populates="temas")
