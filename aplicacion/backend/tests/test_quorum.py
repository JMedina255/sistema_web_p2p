from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.main import app
from app.models.booking import ReservaCupo
from app.models.offer import SesionMentoria
from app.services.booking_service import (
    BookingService,
    _memory_bookings,
    clear_bookings_in_memory,
)
from app.services.offer_service import (
    _memory_offers,
    clear_offers_in_memory,
    seed_default_offers_in_memory,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_teardown_quorum():
    clear_offers_in_memory()
    seed_default_offers_in_memory()
    clear_bookings_in_memory()
    yield
    clear_offers_in_memory()
    clear_bookings_in_memory()


def test_quorum_t29_presencial_below_3_mutates_to_insuficiente_in_memory():
    """T-29: Quórum presencial con menos de 3 confirmados transiciona a QUORUM_INSUFICIENTE."""
    now = datetime.now(UTC)
    _memory_offers.append(
        {
            "id_sesion": 501,
            "codigo_sesion": "SES-Q-501",
            "mentor_email": "mentor.q@upt.pe",
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "estado": "PUBLICADA",
            "fecha_inicio": (now + timedelta(hours=12)).isoformat(),
            "quorumevaluated_at": None,
        }
    )
    # Solo 2 reservas confirmadas (menos de 3)
    _memory_bookings.extend(
        [
            {"id_reserva": 1, "id_sesion": 501, "estudiante_email": "est1@upt.pe", "estado": "CONFIRMADA"},
            {"id_reserva": 2, "id_sesion": 501, "estudiante_email": "est2@upt.pe", "estado": "CONFIRMADA"},
            {"id_reserva": 3, "id_sesion": 501, "estudiante_email": "est3@upt.pe", "estado": "PENDIENTE_CONFIRMACION"},
        ]
    )

    res = client.post("/api/v1/quorum/evaluate?mode=sprint6", json={"id_sesion": 501})
    assert res.status_code == 200
    data = res.json()
    assert data["cumple_quorum"] is False
    assert data["estado_sesion"] == "QUORUM_INSUFICIENTE"
    assert data["reservas_confirmadas"] == 2

    # Verificar que la reserva no ratificada mutó a CANCELADA_NO_CONFIRMADA
    unconf = next(b for b in _memory_bookings if b["id_reserva"] == 3)
    assert unconf["estado"] == "CANCELADA_NO_CONFIRMADA"


def test_quorum_t29_presencial_at_least_3_confirms_session_in_memory():
    """T-29: Quórum presencial con 3 o más confirmados transiciona a CONFIRMADA."""
    now = datetime.now(UTC)
    _memory_offers.append(
        {
            "id_sesion": 502,
            "codigo_sesion": "SES-Q-502",
            "mentor_email": "mentor.q@upt.pe",
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "estado": "PUBLICADA",
            "fecha_inicio": (now + timedelta(hours=20)).isoformat(),
            "quorumevaluated_at": None,
        }
    )
    for i in range(3):
        _memory_bookings.append(
            {"id_reserva": 10 + i, "id_sesion": 502, "estudiante_email": f"est{i}@upt.pe", "estado": "CONFIRMADA"}
        )

    res = client.post("/api/v1/quorum/evaluate?mode=sprint6", json={"id_sesion": 502})
    assert res.status_code == 200
    data = res.json()
    assert data["cumple_quorum"] is True
    assert data["estado_sesion"] == "CONFIRMADA"
    assert data["reservas_confirmadas"] == 3


def test_quorum_t30_idempotency_prevents_duplicate_evaluation_in_memory():
    """T-30: Invocaciones repetidas retornan resultado idempotente sin repetir transiciones."""
    now = datetime.now(UTC)
    _memory_offers.append(
        {
            "id_sesion": 503,
            "codigo_sesion": "SES-Q-503",
            "mentor_email": "mentor.q@upt.pe",
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "estado": "PUBLICADA",
            "fecha_inicio": (now + timedelta(hours=5)).isoformat(),
            "quorumevaluated_at": None,
        }
    )
    for i in range(3):
        _memory_bookings.append(
            {"id_reserva": 20 + i, "id_sesion": 503, "estudiante_email": f"est{i}@upt.pe", "estado": "CONFIRMADA"}
        )

    # Primera evaluación
    res1 = client.post("/api/v1/quorum/evaluate?mode=sprint6", json={"id_sesion": 503})
    assert res1.status_code == 200
    assert res1.json()["estado_sesion"] == "CONFIRMADA"

    # Segunda evaluación (idempotente)
    res2 = client.post("/api/v1/quorum/evaluate?mode=sprint6", json={"id_sesion": 503})
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["estado_sesion"] == "CONFIRMADA"
    assert "idempotente" in data2["mensaje"].lower()


def test_quorum_t29_evaluate_all_active_quorums():
    """T-29: POST /api/v1/quorum/evaluate-all procesa todas las sesiones en ventana T-24h."""
    now = datetime.now(UTC)
    clear_offers_in_memory()
    clear_bookings_in_memory()

    # Sesión 1: en ventana (T-10h), quórum alcanzado
    _memory_offers.append(
        {
            "id_sesion": 601,
            "codigo_sesion": "SES-ALL-1",
            "mentor_email": "m1@upt.pe",
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "estado": "PUBLICADA",
            "fecha_inicio": (now + timedelta(hours=10)).isoformat(),
            "quorumevaluated_at": None,
        }
    )
    for i in range(4):
        _memory_bookings.append(
            {"id_reserva": 30 + i, "id_sesion": 601, "estudiante_email": f"e{i}@upt.pe", "estado": "CONFIRMADA"}
        )

    # Sesión 2: fuera de ventana (T-36h), no debe evaluarse
    _memory_offers.append(
        {
            "id_sesion": 602,
            "codigo_sesion": "SES-ALL-2",
            "mentor_email": "m2@upt.pe",
            "modalidad": "virtual",
            "aforo_maximo": 20,
            "estado": "PUBLICADA",
            "fecha_inicio": (now + timedelta(hours=36)).isoformat(),
            "quorumevaluated_at": None,
        }
    )

    res = client.post("/api/v1/quorum/evaluate-all")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["id_sesion"] == 601
    assert data[0]["estado_sesion"] == "CONFIRMADA"

    # Verificar que la sesión 602 sigue intacta en PUBLICADA
    s2 = next(o for o in _memory_offers if o["id_sesion"] == 602)
    assert s2["estado"] == "PUBLICADA"
    assert s2["quorumevaluated_at"] is None


def test_quorum_t29_and_t30_in_real_db_with_row_locking():
    """T-29 & T-30: Verificación con base de datos SQLite/PostgreSQL relacional y campo quorumevaluated_at."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionTest = sessionmaker(bind=engine)
    db = SessionTest()

    try:
        now = datetime.now(UTC)
        s = SesionMentoria(
            id_sesion=701,
            codigo_sesion="SES-DB-701",
            mentor_email="mentor.db@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now + timedelta(hours=15),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Aula 101",
            estado="PUBLICADA",
            quorumevaluated_at=None,
        )
        db.add(s)

        # 1 reserva confirmada y 1 pendiente (quórum insuficiente)
        db.add(ReservaCupo(id_sesion=701, codigo_reserva="R-701-1", estudiante_email="e1@upt.pe", estado="CONFIRMADA"))
        db.add(ReservaCupo(id_sesion=701, codigo_reserva="R-701-2", estudiante_email="e2@upt.pe", estado="PENDIENTE_CONFIRMACION"))
        db.commit()

        # Evaluación 1: pasa a QUORUM_INSUFICIENTE y marca quorumevaluated_at
        res1 = BookingService.evaluate_session_quorum(db=db, id_sesion=701)
        assert res1.cumple_quorum is False
        assert res1.estado_sesion == "QUORUM_INSUFICIENTE"

        db.refresh(s)
        assert s.estado == "QUORUM_INSUFICIENTE"
        assert s.quorumevaluated_at is not None

        # Evaluación 2: idempotencia
        res2 = BookingService.evaluate_session_quorum(db=db, id_sesion=701)
        assert "idempotente" in res2.mensaje.lower()
    finally:
        db.close()
        engine.dispose()
