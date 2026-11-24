from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class VersionCronograma(Base):
    __tablename__ = "versiones_cronograma"

    id: Mapped[int] = mapped_column(primary_key=True)
    archivo: Mapped[str] = mapped_column(String(255))
    franjas: Mapped[list[dict[str, Any]]] = mapped_column(JSON)
    creado: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class CronogramaActivo(Base):
    __tablename__ = "cronograma_activo"
    __table_args__ = (CheckConstraint("id = 1", name="chk_cronograma_unico"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    id_version: Mapped[int | None] = mapped_column(ForeignKey("versiones_cronograma.id"))
    version: Mapped[VersionCronograma | None] = relationship()
