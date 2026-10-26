from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class ConsentimientoLegal(Base):
    """
    Entidad ConsentimientoLegal (T-05 / RF02 / RN-02 / CUS01).
    Registra la conformidad formal y auditada del estudiante para el tratamiento
    de datos personales conforme a la Ley N° 29733 (Perú).
    """

    __tablename__ = "consentimientos_legales"

    id_consentimiento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    terms_version: Mapped[str] = mapped_column(String(50), default="2026-II-v1.0", nullable=False)
    accepted: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    consented_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
