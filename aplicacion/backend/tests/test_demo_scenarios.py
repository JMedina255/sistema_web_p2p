from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import create_access_token
from app.db.session import Base
from app.main import app
from app.services.attendance_service import (
    clear_attendances_in_memory,
)
from app.services.bitacora_service import (
    clear_bitacoras_in_memory,
)
from app.services.booking_service import (
    _memory_bookings,
    clear_bookings_in_memory,
)
from app.services.offer_service import (
    _memory_offers,
    clear_offers_in_memory,
)
from scripts.prepare_demo_scenarios import prepare_demo_fixtures

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_teardown_demo():
    clear_offers_in_memory()
    clear_bookings_in_memory()
    clear_attendances_in_memory()
    clear_bitacoras_in_memory()
    yield
    clear_offers_in_memory()
    clear_bookings_in_memory()
    clear_attendances_in_memory()
    clear_bitacoras_in_memory()


def test_prepare_demo_fixtures_sqlite_in_memory():
    """Verifica que el script de preparación genere los 6 escenarios en una base de datos SQLite aislada."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionTest = sessionmaker(bind=engine)
    db = SessionTest()

    try:
        summary = prepare_demo_fixtures(db)
        assert summary["status"] == "success"
        scenarios = summary["scenarios"]
        assert "DEMO-01" in scenarios
        assert "DEMO-02" in scenarios
        assert "DEMO-03" in scenarios
        assert "DEMO-04" in scenarios
        assert "DEMO-05" in scenarios
        assert "DEMO-06" in scenarios
    finally:
        db.close()


def test_demo_01_mentee_access_catalog_and_active_booking():
    """DEMO-01: Acceso de mentoreado, consulta de ofertas y estado de reserva activa."""
    student_email = "estudiante.demo@upt.pe"
    student_token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})
    headers = {"Authorization": f"Bearer {student_token}"}
    now = datetime.now(UTC)

    # Sesión publicada disponible
    _memory_offers.append(
        {
            "id_sesion": 101,
            "codigo_sesion": "SES-DEMO-PUB01",
            "mentor_email": "mentor.demo@upt.pe",
            "id_asignatura": 1,
            "id_tema": 1,
            "fecha_inicio": (now + timedelta(days=3)).isoformat(),
            "duracion_minutos": 60,
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "espacio_asignado": "Aula 201 - EPIS",
            "estado": "PUBLICADA",
        }
    )

    # Reserva activa del estudiante
    _memory_bookings.append(
        {
            "id_reserva": 201,
            "codigo_reserva": "RES-DEMO-001",
            "id_sesion": 101,
            "estudiante_email": student_email,
            "estado": "PENDIENTE_CONFIRMACION",
            "fecha_reserva": now.isoformat(),
            "created_at": now.isoformat(),
        }
    )

    # 1. Consulta del catálogo de ofertas
    res_offers = client.get("/api/v1/offers", headers=headers)
    assert res_offers.status_code == 200
    offers = res_offers.json()
    assert any(o["codigo_sesion"] == "SES-DEMO-PUB01" for o in offers)

    # 2. Consulta de reservas activas del mentoreado
    res_bookings = client.get("/api/v1/bookings/my-reservations", headers=headers)
    assert res_bookings.status_code == 200
    bookings = res_bookings.json()
    assert len(bookings) == 1
    assert bookings[0]["codigo_reserva"] == "RES-DEMO-001"
    assert bookings[0]["estado"] == "PENDIENTE_CONFIRMACION"


def test_demo_02_mentor_publish_and_query_future_offer():
    """DEMO-02: Publicación y consulta de oferta por mentor con antelación > 24h (RN-04)."""
    mentor_email = "mentor.demo@upt.pe"
    mentor_token = create_access_token({"sub": mentor_email, "roles": ["mentor"]})
    headers = {"Authorization": f"Bearer {mentor_token}"}
    now = datetime.now(UTC)

    # 1. Mentor habilitado publica oferta con fecha futura > 24h
    payload = {
        "mentor_email": mentor_email,
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites Notables y Asíntotas",
        "fecha_inicio": (now + timedelta(days=2)).isoformat(),
        "duracion_minutos": 60,
        "modalidad": "presencial",
        "aforo_maximo": 10,
        "espacio_asignado": "Aula 302 - Pabellón EPIS",
        "notas_adicionales": "Revisión de ejercicios de límites notables.",
    }
    res_pub = client.post("/api/v1/offers", json=payload, headers=headers)
    assert res_pub.status_code == 201
    created_offer = res_pub.json()
    assert created_offer["offer"]["mentor_email"] == mentor_email
    assert created_offer["estado"] == "PUBLICADA"
    assert created_offer["aforo"] == 10

    # 2. Mentor consulta sus ofertas registradas
    res_list = client.get(f"/api/v1/offers?mentor_email={mentor_email}", headers=headers)
    assert res_list.status_code == 200
    mentor_offers = res_list.json()
    assert len(mentor_offers) >= 1
    assert any(o["codigo_sesion"] == created_offer["codigo_sesion"] for o in mentor_offers)


def test_demo_03_quorum_insufficient_mentor_decisions():
    """DEMO-03: Sesión en QUORUM_INSUFICIENTE donde el mentor decide (PROCEED, RESCHEDULE, CANCEL)."""
    mentor_email = "mentor.demo@upt.pe"
    mentor_token = create_access_token({"sub": mentor_email, "roles": ["mentor"]})
    headers = {"Authorization": f"Bearer {mentor_token}"}
    now = datetime.now(UTC)

    # Configurar sesión en QUORUM_INSUFICIENTE
    _memory_offers.append(
        {
            "id_sesion": 102,
            "codigo_sesion": "SES-DEMO-Q01",
            "mentor_email": mentor_email,
            "id_asignatura": 1,
            "id_tema": 1,
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "estado": "QUORUM_INSUFICIENTE",
            "fecha_inicio": (now + timedelta(hours=10)).isoformat(),
        }
    )

    # Decisión PROCEED: confirma dictado con aforo reducido
    res_proceed = client.post(
        "/api/v1/offers/102/quorum-decision",
        json={"decision": "PROCEED"},
        headers=headers,
    )
    assert res_proceed.status_code == 200
    data_proceed = res_proceed.json()
    assert data_proceed["decision"] == "PROCEED"
    assert data_proceed["estado_nuevo"] == "CONFIRMADA"

    # Reset a QUORUM_INSUFICIENTE para probar CANCEL
    target = next(o for o in _memory_offers if o["id_sesion"] == 102)
    target["estado"] = "QUORUM_INSUFICIENTE"

    res_cancel = client.post(
        "/api/v1/offers/102/quorum-decision",
        json={
            "decision": "CANCEL",
            "reason": "Aforo mínimo no cubierto y choque con evaluación departamental.",
        },
        headers=headers,
    )
    assert res_cancel.status_code == 200
    data_cancel = res_cancel.json()
    assert data_cancel["decision"] == "CANCEL"
    assert data_cancel["estado_nuevo"] == "CANCELADA_QUORUM"


def test_demo_04_session_attendance_qr_totp_and_checkin():
    """DEMO-04: Sesión confirmada en curso que genera token QR TOTP y confirma asistencia."""
    mentor_email = "mentor.demo@upt.pe"
    student_email = "estudiante.demo@upt.pe"
    mentor_token = create_access_token({"sub": mentor_email, "roles": ["mentor"]})
    student_token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    # Sesión en curso
    _memory_offers.append(
        {
            "id_sesion": 103,
            "codigo_sesion": "SES-DEMO-ASIS01",
            "mentor_email": mentor_email,
            "estado": "CONFIRMADA",
            "fecha_inicio": (now - timedelta(minutes=15)).isoformat(),
            "duracion_minutos": 60,
        }
    )
    # Reserva confirmada del estudiante
    _memory_bookings.append(
        {
            "id_reserva": 204,
            "codigo_reserva": "RES-DEMO-ASIS01",
            "id_sesion": 103,
            "estudiante_email": student_email,
            "estado": "CONFIRMADA",
        }
    )

    # 1. Mentor genera token dinámico TOTP / QR
    token_res = client.get(
        "/api/v1/sessions/103/attendance/token",
        headers={"Authorization": f"Bearer {mentor_token}"},
    )
    assert token_res.status_code == 200
    token_data = token_res.json()
    assert token_data["session_id"] == 103
    assert len(token_data["token"]) == 64
    assert len(token_data["totp_code"]) == 6
    assert token_data["expires_in"] == 30

    # 2. Mentoreado realiza check-in con el token QR generado
    checkin_res = client.post(
        "/api/v1/sessions/103/attendance/check-in",
        json={"qr_token": token_data["token"]},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert checkin_res.status_code == 200
    checkin_data = checkin_res.json()
    assert checkin_data["id_sesion"] == 103
    assert checkin_data["estudiante_email"] == student_email
    assert checkin_data["asistio"] is True


def test_demo_05_concluded_session_bitacora_validation_and_registration():
    """DEMO-05: Sesión concluida (<48h) acepta bitácora pedagógica >= 50 chars y rechaza < 50 chars."""
    mentor_email = "mentor.demo@upt.pe"
    mentor_token = create_access_token({"sub": mentor_email, "roles": ["mentor"]})
    headers = {"Authorization": f"Bearer {mentor_token}"}
    now = datetime.now(UTC)

    # Sesión concluida hace 2 horas
    _memory_offers.append(
        {
            "id_sesion": 104,
            "codigo_sesion": "SES-DEMO-BIT01",
            "mentor_email": mentor_email,
            "estado": "CONCLUIDA",
            "fecha_inicio": (now - timedelta(hours=3)).isoformat(),
            "duracion_minutos": 90,
        }
    )

    # 1. Rechazo de observaciones breves (< 50 caracteres según RN-12)
    invalid_payload = {
        "temas_cubiertos": ["Límites"],
        "observaciones": "Sesión completada correctamente sin novedades.",  # 46 chars
        "nivel_dificultad": "Medio",
    }
    res_invalid = client.post("/api/v1/sessions/104/bitacora", json=invalid_payload, headers=headers)
    assert res_invalid.status_code == 422

    # 2. Registro exitoso con observaciones sustantivas (>= 50 caracteres)
    valid_payload = {
        "temas_cubiertos": ["Definición de límites notables", "Resolución de indeterminaciones 0/0"],
        "observaciones": "Se desarrollaron con éxito los ejercicios prácticos de límites trigonométricos con alta participación del grupo.",
        "nivel_dificultad": "Medio",
    }
    res_valid = client.post("/api/v1/sessions/104/bitacora", json=valid_payload, headers=headers)
    assert res_valid.status_code == 201
    bit_data = res_valid.json()
    assert bit_data["id_sesion"] == 104
    assert bit_data["id_mentor"] == mentor_email
    assert len(bit_data["hash_firma"]) == 64
    assert bit_data["horas_declaradas"] == 1.5  # 90 min / 60

    # 3. Consulta de bitácora registrada
    res_get = client.get("/api/v1/sessions/104/bitacora", headers=headers)
    assert res_get.status_code == 200
    assert res_get.json()["hash_firma"] == bit_data["hash_firma"]


def test_demo_06_admin_quorum_evaluation_and_role_management():
    """DEMO-06: Administrador evalúa quórum institucional (RN-09) y gestiona roles institucionales."""
    admin_email = "admin.demo@upt.pe"
    student_email = "estudiante.demo@upt.pe"
    admin_token = create_access_token({"sub": admin_email, "roles": ["administrador"]})
    student_token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    # Sesión a evaluar quórum en T-24h
    _memory_offers.append(
        {
            "id_sesion": 105,
            "codigo_sesion": "SES-DEMO-ADMIN01",
            "mentor_email": "mentor.demo@upt.pe",
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "estado": "PUBLICADA",
            "fecha_inicio": (now + timedelta(hours=12)).isoformat(),
        }
    )

    # 1. Admin evalúa quórum individual y desatendido exitosamente
    res_quorum = client.post(
        "/api/v1/quorum/evaluate",
        json={"id_sesion": 105},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res_quorum.status_code == 200
    data_quorum = res_quorum.json()
    assert data_quorum["id_sesion"] == 105
    assert data_quorum["cumple_quorum"] is False  # 0 reservas confirmadas < 3 mínimo

    res_all = client.post(
        "/api/v1/quorum/evaluate-all",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res_all.status_code == 200

    # 2. Mentoreado no autorizado intenta evaluar quórum masivo -> 403 Forbidden
    res_forbidden = client.post(
        "/api/v1/quorum/evaluate-all",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res_forbidden.status_code == 403

    # 3. Mentoreado intenta auditar roles de otro usuario -> 403 Forbidden
    res_roles_forbidden = client.get(
        "/api/v1/roles/users/mentor.demo@upt.pe",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res_roles_forbidden.status_code == 403

    # 4. Admin consulta roles de cualquier usuario institucional -> 200 OK
    res_roles_admin = client.get(
        f"/api/v1/roles/users/{student_email}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res_roles_admin.status_code == 200
    assert res_roles_admin.json()["email"] == student_email
