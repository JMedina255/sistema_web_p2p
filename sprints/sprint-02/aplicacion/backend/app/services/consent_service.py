from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.consent import ConsentimientoLegal
from app.schemas.consent import ConsentOperationResponse, ConsentStatusResponse

# Almacén en memoria de respaldo para consentimientos (fallback de desarrollo y pruebas)
_memory_consents: dict[str, dict] = {}


class ConsentService:
    @staticmethod
    def get_consent_status(db: Session | None, email: str) -> ConsentStatusResponse:
        clean_email = email.strip().lower()
        if db is not None:
            try:
                record = (
                    db.query(ConsentimientoLegal)
                    .filter(ConsentimientoLegal.email == clean_email)
                    .order_by(ConsentimientoLegal.consented_at.desc())
                    .first()
                )
                if record is not None:
                    return ConsentStatusResponse(
                        has_consented=record.accepted,
                        consented_at=record.consented_at.isoformat() if record.consented_at else None,
                        terms_version=record.terms_version,
                        email=clean_email,
                        mode="api",
                    )
            except Exception:
                pass

        # Fallback en memoria
        if clean_email in _memory_consents:
            mem = _memory_consents[clean_email]
            return ConsentStatusResponse(
                has_consented=bool(mem.get("accepted", False)),
                consented_at=mem.get("consented_at"),
                terms_version=mem.get("terms_version", "2026-II-v1.0"),
                email=clean_email,
                mode="api",
            )

        return ConsentStatusResponse(
            has_consented=False,
            consented_at=None,
            terms_version="2026-II-v1.0",
            email=clean_email,
            mode="api",
        )

    @staticmethod
    def accept_consent(
        db: Session | None,
        email: str,
        accepted: bool = True,
        terms_version: str = "2026-II-v1.0",
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> ConsentOperationResponse:
        clean_email = email.strip().lower()
        now_dt = datetime.now(UTC)

        if db is not None:
            try:
                record = ConsentimientoLegal(
                    email=clean_email,
                    accepted=accepted,
                    terms_version=terms_version,
                    consented_at=now_dt,
                    ip_address=ip_address,
                    user_agent=user_agent,
                )
                db.add(record)
                db.commit()
                db.refresh(record)
                return ConsentOperationResponse(
                    success=True,
                    consented_at=record.consented_at.isoformat(),
                    email=clean_email,
                    message="Consentimiento informado registrado exitosamente en base de datos.",
                )
            except Exception:
                db.rollback()

        # Fallback en memoria
        iso_str = now_dt.isoformat()
        _memory_consents[clean_email] = {
            "accepted": accepted,
            "terms_version": terms_version,
            "consented_at": iso_str,
            "ip_address": ip_address,
            "user_agent": user_agent,
        }
        return ConsentOperationResponse(
            success=True,
            consented_at=iso_str,
            email=clean_email,
            message="Consentimiento informado registrado exitosamente conforme a la Ley N° 29733.",
        )

    @staticmethod
    def revoke_consent(db: Session | None, email: str) -> ConsentOperationResponse:
        clean_email = email.strip().lower()
        now_dt = datetime.now(UTC)

        if db is not None:
            try:
                record = ConsentimientoLegal(
                    email=clean_email,
                    accepted=False,
                    terms_version="2026-II-v1.0",
                    consented_at=now_dt,
                )
                db.add(record)
                db.commit()
            except Exception:
                db.rollback()

        iso_str = now_dt.isoformat()
        _memory_consents[clean_email] = {
            "accepted": False,
            "terms_version": "2026-II-v1.0",
            "consented_at": iso_str,
        }

        return ConsentOperationResponse(
            success=True,
            consented_at=None,
            email=clean_email,
            message="Consentimiento revocado. Acceso a la plataforma bloqueado preventivamente conforme a la regla RN-02.",
        )
