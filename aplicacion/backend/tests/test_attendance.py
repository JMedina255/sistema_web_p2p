from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import create_access_token
from app.db.session import Base
from app.main import app
from app.models.attendance import AsistenciaSesion
from app.models.booking import ReservaCupo
from app.models.offer import SesionMentoria
from app.services.attendance_service import (
    clear_attendances_in_memory,
)
from app.services.booking_service import _memory_bookings, clear_bookings_in_memory
from app.services.offer_service import (
    _memory_offers,
    clear_offers_in_memory,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_teardown_attendance():
    clear_offers_in_memory()
    clear_bookings_in_memory()
    clear_attendances_in_memory()
    yield
    clear_offers_in_memory()
    clear_bookings_in_memory()
    clear_attendances_in_memory()


def test_attendance_t36_generate_totp_token_success():
    """T-36: Generación de token criptográfico QR dinámico y TOTP de 6 dígitos con ventana de 30s."""
    mentor = "mentor.asistencia@upt.pe"
    token = create_access_token({"sub": mentor, "roles": ["mentor"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 1101,
            "codigo_sesion": "SES-ATT-1101",
            "mentor_email": mentor,
            "fecha_inicio": now.isoformat(),
            "duracion_minutos": 60,
        }
    )

    res = client.get(
        "/api/v1/sessions/1101/attendance/token",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["session_id"] == 1101
    assert len(data["token"]) == 64
    assert len(data["totp_code"]) == 6
    assert data["expires_in"] == 30
    assert "expires_at" in data


def test_attendance_t36_checkin_success_with_confirmed_reservation():
    """T-36: Check-in exitoso de estudiante mentoreado con reserva CONFIRMADA dentro del horario."""
    mentor = "mentor.asistencia@upt.pe"
    student = "alumno.asiste@upt.pe"
    mentor_token = create_access_token({"sub": mentor, "roles": ["mentor"]})
    student_token = create_access_token({"sub": student, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 1102,
            "codigo_sesion": "SES-ATT-1102",
            "mentor_email": mentor,
            "fecha_inicio": (now - timedelta(minutes=10)).isoformat(),
            "duracion_minutos": 60,
        }
    )
    _memory_bookings.append(
        {
            "id_reserva": 1201,
            "id_sesion": 1102,
            "estudiante_email": student,
            "estado": "CONFIRMADA",
        }
    )

    # 1. Mentor genera token
    token_res = client.get(
        "/api/v1/sessions/1102/attendance/token",
        headers={"Authorization": f"Bearer {mentor_token}"},
    )
    qr_token = token_res.json()["token"]

    # 2. Estudiante realiza check-in con qr_token
    checkin_res = client.post(
        "/api/v1/sessions/1102/attendance/check-in",
        json={"qr_token": qr_token},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert checkin_res.status_code == 200
    data = checkin_res.json()
    assert data["id_sesion"] == 1102
    assert data["estudiante_email"] == student
    assert data["asistio"] is True

    # 3. Comprobar que en la nómina de asistencia figura presente
    roster_res = client.get("/api/v1/sessions/1102/attendance")
    assert roster_res.status_code == 200
    roster = roster_res.json()
    assert len(roster) == 1
    assert roster[0]["estudiante_email"] == student
    assert roster[0]["asistio"] is True


def test_attendance_t36_rejects_checkin_without_confirmed_booking_403():
    """T-36: Rechaza con 403 Forbidden a estudiantes sin reserva confirmada para la sesión."""
    student_sin_reserva = "sin.reserva@upt.pe"
    student_token = create_access_token({"sub": student_sin_reserva, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 1103,
            "codigo_sesion": "SES-ATT-1103",
            "mentor_email": "mentor.titular@upt.pe",
            "fecha_inicio": now.isoformat(),
            "duracion_minutos": 60,
        }
    )

    mentor_token = create_access_token({"sub": "mentor.titular@upt.pe", "roles": ["mentor"]})
    token_res = client.get(
        "/api/v1/sessions/1103/attendance/token",
        headers={"Authorization": f"Bearer {mentor_token}"},
    )
    totp_code = token_res.json()["totp_code"]

    res = client.post(
        "/api/v1/sessions/1103/attendance/check-in",
        json={"numeric_code": totp_code},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 403
    assert "NO_CONFIRMED_BOOKING" in res.json()["detail"]


def test_attendance_t36_rejects_checkin_outside_window():
    """T-36 / RN-12: Rechaza check-in fuera del intervalo [-15m, +30m]."""
    mentor = "mentor.asistencia@upt.pe"
    student = "alumno.asiste@upt.pe"
    mentor_token = create_access_token({"sub": mentor, "roles": ["mentor"]})
    student_token = create_access_token({"sub": student, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    # Sesión programada para dentro de 5 horas (muy temprano para check-in)
    _memory_offers.append(
        {
            "id_sesion": 1104,
            "codigo_sesion": "SES-ATT-1104",
            "mentor_email": mentor,
            "fecha_inicio": (now + timedelta(hours=5)).isoformat(),
            "duracion_minutos": 60,
        }
    )
    _memory_bookings.append(
        {
            "id_reserva": 1204,
            "id_sesion": 1104,
            "estudiante_email": student,
            "estado": "CONFIRMADA",
        }
    )

    # Mentor genera token
    token_res = client.get(
        "/api/v1/sessions/1104/attendance/token",
        headers={"Authorization": f"Bearer {mentor_token}"},
    )
    qr_token = token_res.json()["token"]

    res = client.post(
        "/api/v1/sessions/1104/attendance/check-in",
        json={"qr_token": qr_token},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 400
    assert "CHECKIN_WINDOW_CLOSED" in res.json()["detail"]


def test_attendance_rejects_empty_payload_400():
    """T-36: Rechaza con 400 cuando se envía payload sin qr_token ni numeric_code."""
    student = "alumno.asiste@upt.pe"
    student_token = create_access_token({"sub": student, "roles": ["mentoreado"]})

    res = client.post(
        "/api/v1/sessions/1102/attendance/check-in",
        json={},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 400
    assert "TOKEN_OR_CODE_REQUIRED" in res.json()["detail"]


def test_attendance_rejects_when_no_active_token_400():
    """T-36: Rechaza con 400 cuando el mentor no ha generado el token activo."""
    now = datetime.now(UTC)
    _memory_offers.append(
        {
            "id_sesion": 1199,
            "codigo_sesion": "SES-ATT-1199",
            "mentor_email": "mentor.inactivo@upt.pe",
            "fecha_inicio": now.isoformat(),
            "duracion_minutos": 60,
        }
    )
    _memory_bookings.append(
        {
            "id_reserva": 1299,
            "id_sesion": 1199,
            "estudiante_email": "alumno.sinactivo@upt.pe",
            "estado": "CONFIRMADA",
        }
    )
    student_token = create_access_token({"sub": "alumno.sinactivo@upt.pe", "roles": ["mentoreado"]})

    res = client.post(
        "/api/v1/sessions/1199/attendance/check-in",
        json={"numeric_code": "123456"},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 400
    assert "NO_ACTIVE_ATTENDANCE_TOKEN" in res.json()["detail"]


def test_attendance_token_rejects_fake_admin_email_substring_403():
    """T-36 / RNF02: Rechaza con 403 a un usuario con subcadena 'admin' en su correo sin rol de administrador."""
    fake_admin = "admin_impostor@upt.pe"
    fake_token = create_access_token({"sub": fake_admin, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 1108,
            "codigo_sesion": "SES-ATT-1108",
            "mentor_email": "mentor.legitimo@upt.pe",
            "fecha_inicio": now.isoformat(),
            "duracion_minutos": 60,
        }
    )

    res = client.get(
        "/api/v1/sessions/1108/attendance/token",
        headers={"Authorization": f"Bearer {fake_token}"},
    )
    assert res.status_code == 403
    assert "FORBIDDEN" in res.json()["detail"]


def test_attendance_t36_persistence_in_real_database():
    """T-36: Verificación de persistencia relacional en la tabla asistencias_sesion."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionTest = sessionmaker(bind=engine)
    db = SessionTest()

    try:
        now = datetime.now(UTC)
        student_email = "alumno.real@upt.pe"
        mentor_email = "mentor.real@upt.pe"
        s = SesionMentoria(
            id_sesion=1150,
            codigo_sesion="SES-ATT-DB",
            mentor_email=mentor_email,
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now - timedelta(minutes=5),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Aula 202",
            estado="CONFIRMADA",
        )
        b = ReservaCupo(
            id_sesion=1150,
            codigo_reserva="RES-ATT-DB",
            estudiante_email=student_email,
            estado="CONFIRMADA",
        )
        db.add(s)
        db.add(b)
        db.commit()

        from app.schemas.attendance import AttendanceCheckinPayload
        from app.services.attendance_service import AttendanceService

        token_info = AttendanceService.generate_token(
            db=db,
            session_id=1150,
            caller_email=mentor_email,
            now_utc=now,
        )

        res = AttendanceService.record_checkin(
            db=db,
            session_id=1150,
            payload=AttendanceCheckinPayload(qr_token=token_info.token),
            caller_email=student_email,
            client_ip="192.168.1.100",
            now_utc=now,
        )
        assert res.asistio is True
        assert res.estudiante_email == student_email

        # Comprobar registro en BD
        db_att = (
            db.query(AsistenciaSesion)
            .filter(AsistenciaSesion.id_sesion == 1150, AsistenciaSesion.estudiante_email == student_email)
            .first()
        )
        assert db_att is not None
        assert db_att.asistio is True
        assert db_att.ip_origen == "192.168.1.100"

        # Comprobar mutación de reserva a ASISTIDA
        db.refresh(b)
        assert b.estado == "ASISTIDA"
    finally:
        db.close()
        engine.dispose()

