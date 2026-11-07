from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import create_access_token
from app.db.session import Base
from app.main import app
from app.models.booking import ReservaCupo
from app.models.offer import SesionMentoria
from app.services.booking_service import _memory_bookings, clear_bookings_in_memory
from app.services.offer_service import (
    _memory_offers,
    clear_offers_in_memory,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_teardown_contingency():
    clear_offers_in_memory()
    clear_bookings_in_memory()
    yield
    clear_offers_in_memory()
    clear_bookings_in_memory()


def test_quorum_decision_proceed_success_in_memory():
    """T-33: Decisión PROCEED confirma dictado con aforo reducido."""
    mentor = "mentor.titular@upt.pe"
    token = create_access_token({"sub": mentor, "roles": ["mentor"]})

    _memory_offers.append(
        {
            "id_sesion": 801,
            "codigo_sesion": "SES-DEC-801",
            "mentor_email": mentor,
            "estado": "QUORUM_INSUFICIENTE",
            "fecha_inicio": (datetime.now(UTC) + timedelta(hours=10)).isoformat(),
        }
    )

    res = client.post(
        "/api/v1/offers/801/quorum-decision",
        json={"decision": "PROCEED"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["decision"] == "PROCEED"
    assert data["estado_nuevo"] == "CONFIRMADA"

    target = next(o for o in _memory_offers if o["id_sesion"] == 801)
    assert target["estado"] == "CONFIRMADA"


def test_quorum_decision_reschedule_success_in_memory():
    """T-33: Decisión RESCHEDULE con >24h reprograma y restablece a PUBLICADA."""
    mentor = "mentor.titular@upt.pe"
    token = create_access_token({"sub": mentor, "roles": ["mentor"]})
    now = datetime.now(UTC)
    new_start = (now + timedelta(days=3)).isoformat()

    _memory_offers.append(
        {
            "id_sesion": 802,
            "codigo_sesion": "SES-DEC-802",
            "mentor_email": mentor,
            "estado": "QUORUM_INSUFICIENTE",
            "fecha_inicio": (now + timedelta(hours=10)).isoformat(),
            "quorumevaluated_at": now.isoformat(),
        }
    )

    res = client.post(
        "/api/v1/offers/802/quorum-decision",
        json={"decision": "RESCHEDULE", "new_start_time": new_start},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["decision"] == "RESCHEDULE"
    assert data["estado_nuevo"] == "PUBLICADA"

    target = next(o for o in _memory_offers if o["id_sesion"] == 802)
    assert target["estado"] == "PUBLICADA"
    assert target["quorumevaluated_at"] is None


def test_quorum_decision_reschedule_rejects_advance_under_24h_rn04():
    """T-33 / RN-04: Rechaza reprogramación si la nueva fecha no cumple antelación mínima de 24h."""
    mentor = "mentor.titular@upt.pe"
    token = create_access_token({"sub": mentor, "roles": ["mentor"]})
    now = datetime.now(UTC)
    invalid_start = (now + timedelta(hours=12)).isoformat()

    _memory_offers.append(
        {
            "id_sesion": 803,
            "codigo_sesion": "SES-DEC-803",
            "mentor_email": mentor,
            "estado": "QUORUM_INSUFICIENTE",
            "fecha_inicio": (now + timedelta(hours=5)).isoformat(),
        }
    )

    res = client.post(
        "/api/v1/offers/803/quorum-decision",
        json={"decision": "RESCHEDULE", "new_start_time": invalid_start},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400
    assert "INSUFFICIENT_RESCHEDULE_ADVANCE" in res.json()["detail"]


def test_quorum_decision_cancel_requires_reason_and_cancels_bookings():
    """T-33: Decisión CANCEL exige motivo justificado y muta reservas a CANCELADA_SISTEMA_QUORUM."""
    mentor = "mentor.titular@upt.pe"
    token = create_access_token({"sub": mentor, "roles": ["mentor"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 804,
            "codigo_sesion": "SES-DEC-804",
            "mentor_email": mentor,
            "estado": "QUORUM_INSUFICIENTE",
            "fecha_inicio": (now + timedelta(hours=10)).isoformat(),
        }
    )
    _memory_bookings.append(
        {
            "id_reserva": 901,
            "id_sesion": 804,
            "estudiante_email": "alumno@upt.pe",
            "estado": "CONFIRMADA",
        }
    )

    # 1. Sin motivo -> 422
    res_err = client.post(
        "/api/v1/offers/804/quorum-decision",
        json={"decision": "CANCEL", "reason": "   "},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res_err.status_code == 422
    assert "REASON_REQUIRED" in res_err.json()["detail"]

    # 2. Con motivo justificado -> 200
    reason_text = "Cruce con examen parcial de la materia y bajo aforo confirmado"
    res_ok = client.post(
        "/api/v1/offers/804/quorum-decision",
        json={"decision": "CANCEL", "reason": reason_text},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res_ok.status_code == 200
    data = res_ok.json()
    assert data["estado_nuevo"] == "CANCELADA_QUORUM"

    # Verificar reservas liberadas
    booking = next(b for b in _memory_bookings if b["id_reserva"] == 901)
    assert booking["estado"] == "CANCELADA_SISTEMA_QUORUM"
    assert reason_text in booking["motivo_cancelacion"]


def test_quorum_decision_rejects_unauthorized_user_403():
    """T-33 / RNF02: Usuario distinto al mentor titular o administrador es rechazado con 403."""
    impostor = "otro.estudiante@upt.pe"
    token = create_access_token({"sub": impostor, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 805,
            "codigo_sesion": "SES-DEC-805",
            "mentor_email": "mentor.titular@upt.pe",
            "estado": "QUORUM_INSUFICIENTE",
            "fecha_inicio": (now + timedelta(hours=8)).isoformat(),
        }
    )

    res = client.post(
        "/api/v1/offers/805/quorum-decision",
        json={"decision": "PROCEED"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert "FORBIDDEN" in res.json()["detail"]


def test_quorum_decision_rejects_fake_admin_email_substring_403():
    """T-33 / RNF02: Correo que contiene 'admin' sin rol 'administrador' es rechazado con 403."""
    fake_admin = "admin_impostor@upt.pe"
    token = create_access_token({"sub": fake_admin, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 806,
            "codigo_sesion": "SES-DEC-806",
            "mentor_email": "mentor.titular@upt.pe",
            "estado": "QUORUM_INSUFICIENTE",
            "fecha_inicio": (now + timedelta(hours=8)).isoformat(),
        }
    )

    res = client.post(
        "/api/v1/offers/806/quorum-decision",
        json={"decision": "PROCEED"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert "FORBIDDEN" in res.json()["detail"]


def test_quorum_decision_in_real_database():
    """T-33: Transacciones atómicas de contingencia en base de datos real con rollback/commit."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionTest = sessionmaker(bind=engine)
    db = SessionTest()

    try:
        now = datetime.now(UTC)
        mentor_email = "mentor.real@upt.pe"
        s = SesionMentoria(
            id_sesion=850,
            codigo_sesion="SES-REAL-850",
            mentor_email=mentor_email,
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now + timedelta(hours=10),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Lab 201",
            estado="QUORUM_INSUFICIENTE",
        )
        b = ReservaCupo(
            id_sesion=850,
            codigo_reserva="RES-REAL-850",
            estudiante_email="alumno.real@upt.pe",
            estado="CONFIRMADA",
        )
        db.add(s)
        db.add(b)
        db.commit()

        from app.schemas.offer import QuorumDecisionPayload
        from app.services.offer_service import OfferService

        res = OfferService.resolve_quorum_decision(
            db=db,
            id_sesion=850,
            payload=QuorumDecisionPayload(decision="PROCEED"),
            caller_email=mentor_email,
        )
        assert res.estado_nuevo == "CONFIRMADA"

        db.refresh(s)
        assert s.estado == "CONFIRMADA"
    finally:
        db.close()
        engine.dispose()
