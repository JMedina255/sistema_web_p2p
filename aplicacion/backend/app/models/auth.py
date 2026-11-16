from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AuthChallenge(Base):
    """
    Entidad de Desafío de Autenticación OTP (T-03 / CUS01 / RF01 / RNF01).
    Registra los códigos de verificación temporales vinculados al correo institucional @upt.pe.
    """

    __tablename__ = "auth_challenges"

    id_challenge: Mapped[str] = mapped_column(String(64), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    code_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    code_salt: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    resend_available_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consumed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class AuthRateLimit(Base):
    """
    Entidad de Control de Frecuencia (Rate Limiting) compartido y persistente (H-08).
    Permite controlar límites de tasa atómicos a través de múltiples workers de Uvicorn/PostgreSQL.
    """

    __tablename__ = "auth_rate_limits"

    key: Mapped[str] = mapped_column(String(128), primary_key=True)
    count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    window_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False
    )
