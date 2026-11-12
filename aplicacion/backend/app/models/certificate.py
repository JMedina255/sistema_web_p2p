from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, DateTime, Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class CertificadoHoras(Base):
    """
    Entidad CertificadoHoras (T-44 / RF22 / RF23 / CUS18 / RN-14).
    Registra la emisión oficial de constancias de acreditación de horas de mentoría:
    - Umbral mínimo estricto de 20.0 horas visadas (RN-14).
    - Folio institucional correlativo único (ej. CERT-2026-II-0001).
    - Huella criptográfica SHA-256 inmutable de autenticidad.
    - Estado de emisión institucional (EMITIDO_DEMO).
    """

    __tablename__ = "certificados_horas"

    id_certificado: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_mentor: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    codigo_folio: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    periodo_academico: Mapped[str] = mapped_column(String(20), default="2026-II", nullable=False)
    horas_acreditadas: Mapped[float] = mapped_column(Float, nullable=False)
    hash_firma: Mapped[str] = mapped_column(String(64), nullable=False)
    estado: Mapped[str] = mapped_column(String(30), default="EMITIDO_DEMO", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("id_mentor", "periodo_academico", name="uq_mentor_periodo_certificado"),
        CheckConstraint("horas_acreditadas >= 20.0", name="chk_horas_minimas_cert"),
    )
