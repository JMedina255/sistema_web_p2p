from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.main import app
from app.models.consent import ConsentimientoLegal
from app.services.consent_service import ConsentService

client = TestClient(app)


def test_get_consent_status_unconsented():
    email = "2024099999@upt.pe"
    response = client.get(f"/api/v1/consent/status?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert data["has_consented"] is False
    assert data["consented_at"] is None
    assert data["terms_version"] == "2026-II-v1.0"
    assert data["email"] == email


def test_accept_consent_success():
    email = "2022074255@upt.pe"
    payload = {
        "email": email,
        "accepted": True,
        "terms_version": "2026-II-v1.0",
        "ip_address": "190.237.15.42",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }
    response = client.post("/api/v1/consent/accept", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["email"] == email
    assert data["consented_at"] is not None
    assert "conforme a la Ley N° 29733" in data["message"] or "exitosamente" in data["message"]

    # Verificar que el estado cambió a consentido
    status_res = client.get(f"/api/v1/consent/status?email={email}")
    assert status_res.status_code == 200
    assert status_res.json()["has_consented"] is True


def test_accept_consent_rejects_external_email():
    payload = {
        "email": "estudiante@gmail.com",
        "accepted": True,
        "terms_version": "2026-II-v1.0",
    }
    response = client.post("/api/v1/consent/accept", json=payload)
    assert response.status_code == 422
    assert "dominio institucional @upt.pe" in response.text


def test_revoke_consent_blocks_access():
    email = "2022074255@upt.pe"
    # Revocar consentimiento
    response = client.post("/api/v1/consent/revoke", json={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "bloqueado preventivamente" in data["message"]

    # Comprobar que la vigencia del consentimiento queda anulada
    status_res = client.get(f"/api/v1/consent/status?email={email}")
    assert status_res.status_code == 200
    assert status_res.json()["has_consented"] is False


def test_consent_service_with_real_db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    test_email = "2022073504@upt.pe"

    # 1. Estado inicial sin registros
    initial = ConsentService.get_consent_status(db, test_email)
    assert initial.has_consented is False
    assert initial.consented_at is None

    # 2. Aceptar consentimiento
    accepted = ConsentService.accept_consent(
        db=db,
        email=test_email,
        accepted=True,
        terms_version="2026-II-v1.0",
        ip_address="127.0.0.1",
        user_agent="Pytest-TestClient",
    )
    assert accepted.success is True
    assert accepted.consented_at is not None

    # 3. Comprobar lectura en BD
    after_accept = ConsentService.get_consent_status(db, test_email)
    assert after_accept.has_consented is True
    assert after_accept.consented_at is not None

    # Comprobar entidad persistida
    entity = db.query(ConsentimientoLegal).filter(ConsentimientoLegal.email == test_email).first()
    assert entity is not None
    assert entity.accepted is True
    assert entity.ip_address == "127.0.0.1"

    # 4. Revocar consentimiento
    revoked = ConsentService.revoke_consent(db, test_email)
    assert revoked.success is True

    after_revoke = ConsentService.get_consent_status(db, test_email)
    assert after_revoke.has_consented is False

    db.close()
    engine.dispose()
