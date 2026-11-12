from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import create_access_token
from app.db.session import Base
from app.main import app
from app.models.attendance import AsistenciaSesion
from app.models.offer import SesionMentoria
from app.models.survey import EncuestaCalidad
from app.services.attendance_service import (
    _memory_attendances,
    clear_attendances_in_memory,
)
from app.services.booking_service import (
    clear_bookings_in_memory,
)
from app.services.offer_service import (
    _memory_offers,
    clear_offers_in_memory,
)
from app.services.survey_service import (
    SurveyService,
    clear_surveys_in_memory,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_teardown_survey():
    clear_offers_in_memory()
    clear_bookings_in_memory()
    clear_attendances_in_memory()
    clear_surveys_in_memory()
    yield
    clear_offers_in_memory()
    clear_bookings_in_memory()
    clear_attendances_in_memory()
    clear_surveys_in_memory()


def test_survey_t39_success_within_24h_in_memory():
    """T-39 / RN-12 / RN-13: Envío exitoso de encuesta de calidad por estudiante asistente dentro de 24h."""
    student_email = "2022074255@upt.pe"
    token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    # Sesión concluida hace 3 horas (dentro de la ventana de 24h)
    _memory_offers.append(
        {
            "id_sesion": 1401,
            "codigo_sesion": "SES-SURV-1401",
            "mentor_email": "mentor.sistemas@upt.pe",
            "estado": "FINALIZADA",
            "fecha_inicio": (now - timedelta(hours=4)).isoformat(),
            "duracion_minutos": 60,
        }
    )

    # Asistencia efectiva confirmada (RN-12)
    _memory_attendances.append(
        {
            "id_asistencia": 1,
            "id_sesion": 1401,
            "estudiante_email": student_email,
            "asistio": True,
            "fecha_checkin": (now - timedelta(hours=4)).isoformat(),
        }
    )

    payload = {
        "calificacion_general": 5,
        "dominio_tema": 5,
        "claridad_explicacion": 4,
        "puntualidad": 5,
        "comentarios": "Excelente explicación de punteros dobles y gestión de memoria dinámica en C++.",
    }

    res = client.post(
        "/api/v1/sessions/1401/survey",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["id_sesion"] == 1401
    assert data["estudiante_email"] == student_email
    assert data["calificacion_general"] == 5
    assert data["dominio_tema"] == 5
    assert data["claridad_explicacion"] == 4
    assert data["puntualidad"] == 5
    assert "Excelente explicación" in data["comentarios"]


def test_survey_t39_rejects_ineligible_student_rn12():
    """T-39 / RN-12: Rechaza evaluación de estudiantes sin asistencia confirmada (HTTP 403 SURVEY_NOT_ELIGIBLE)."""
    student_email = "2022074255@upt.pe"
    token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 1402,
            "codigo_sesion": "SES-SURV-1402",
            "mentor_email": "mentor.sistemas@upt.pe",
            "estado": "FINALIZADA",
            "fecha_inicio": (now - timedelta(hours=2)).isoformat(),
            "duracion_minutos": 60,
        }
    )

    # Estudiante marcado como inasistente (asistio = False)
    _memory_attendances.append(
        {
            "id_asistencia": 2,
            "id_sesion": 1402,
            "estudiante_email": student_email,
            "asistio": False,
        }
    )

    payload = {
        "calificacion_general": 4,
        "dominio_tema": 4,
        "claridad_explicacion": 4,
        "puntualidad": 4,
        "comentarios": "Buenas explicaciones pero no pude asistir presencialmente.",
    }

    res = client.post(
        "/api/v1/sessions/1402/survey",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert "SURVEY_NOT_ELIGIBLE" in res.json()["detail"]


def test_survey_t39_rejects_expired_window_rn13():
    """T-39 / RN-13: Rechaza envío posterior a 24 horas del cierre de la mentoría (HTTP 400 SURVEY_WINDOW_EXPIRED)."""
    student_email = "2022074255@upt.pe"
    token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    # Sesión concluida hace 26 horas (> 24 horas vencida)
    _memory_offers.append(
        {
            "id_sesion": 1403,
            "codigo_sesion": "SES-SURV-1403",
            "mentor_email": "mentor.sistemas@upt.pe",
            "estado": "FINALIZADA",
            "fecha_inicio": (now - timedelta(hours=28)).isoformat(),
            "duracion_minutos": 60,
        }
    )

    _memory_attendances.append(
        {
            "id_asistencia": 3,
            "id_sesion": 1403,
            "estudiante_email": student_email,
            "asistio": True,
        }
    )

    payload = {
        "calificacion_general": 5,
        "dominio_tema": 5,
        "claridad_explicacion": 5,
        "puntualidad": 5,
        "comentarios": "Sesión muy clara y didáctica, resolvió todas las dudas teóricas.",
    }

    res = client.post(
        "/api/v1/sessions/1403/survey",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400
    assert "SURVEY_WINDOW_EXPIRED" in res.json()["detail"]


def test_survey_t39_rejects_duplicate_submission():
    """T-39: Rechaza re-evaluaciones redundantes por el mismo estudiante (HTTP 409 DUPLICATE_SURVEY_SUBMISSION)."""
    student_email = "2022074255@upt.pe"
    token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 1404,
            "codigo_sesion": "SES-SURV-1404",
            "mentor_email": "mentor.sistemas@upt.pe",
            "estado": "FINALIZADA",
            "fecha_inicio": (now - timedelta(hours=2)).isoformat(),
            "duracion_minutos": 60,
        }
    )

    _memory_attendances.append(
        {
            "id_asistencia": 4,
            "id_sesion": 1404,
            "estudiante_email": student_email,
            "asistio": True,
        }
    )

    payload = {
        "calificacion_general": 5,
        "dominio_tema": 5,
        "claridad_explicacion": 5,
        "puntualidad": 5,
        "comentarios": "Excelente sesión de resolución de problemas de algoritmos.",
    }

    # Primer envío exitoso
    res1 = client.post(
        "/api/v1/sessions/1404/survey",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res1.status_code == 201

    # Segundo envío duplicado rechazado
    res2 = client.post(
        "/api/v1/sessions/1404/survey",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res2.status_code == 409
    assert "DUPLICATE_SURVEY_SUBMISSION" in res2.json()["detail"]


def test_survey_t39_rejects_feedback_under_20_chars():
    """T-39: Rechaza comentarios de retroalimentación con menos de 20 caracteres (HTTP 422)."""
    student_email = "2022074255@upt.pe"
    token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 1405,
            "codigo_sesion": "SES-SURV-1405",
            "mentor_email": "mentor.sistemas@upt.pe",
            "estado": "FINALIZADA",
            "fecha_inicio": (now - timedelta(hours=1)).isoformat(),
            "duracion_minutos": 60,
        }
    )

    _memory_attendances.append(
        {
            "id_asistencia": 5,
            "id_sesion": 1405,
            "estudiante_email": student_email,
            "asistio": True,
        }
    )

    payload = {
        "calificacion_general": 5,
        "dominio_tema": 5,
        "claridad_explicacion": 5,
        "puntualidad": 5,
        "comentarios": "Muy bueno",  # < 20 caracteres
    }

    res = client.post(
        "/api/v1/sessions/1405/survey",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 422
    assert "SURVEY_FEEDBACK_TOO_SHORT" in str(res.json())


def test_survey_status_endpoint():
    """T-39: Consulta de estado de elegibilidad y disponibilidad de la encuesta."""
    student_email = "2022074255@upt.pe"
    token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 1406,
            "codigo_sesion": "SES-SURV-1406",
            "mentor_email": "mentor.sistemas@upt.pe",
            "estado": "FINALIZADA",
            "fecha_inicio": (now - timedelta(hours=2)).isoformat(),
            "duracion_minutos": 60,
        }
    )

    _memory_attendances.append(
        {
            "id_asistencia": 6,
            "id_sesion": 1406,
            "estudiante_email": student_email,
            "asistio": True,
        }
    )

    res = client.get(
        "/api/v1/sessions/1406/survey",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["eligible"] is True
    assert data["has_surveyed"] is False
    assert data["window_open"] is True


def test_survey_persistence_in_real_database():
    """T-39 / RN-12 / RN-13: Persistencia relacional de encuesta en base de datos SQLAlchemy."""
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    now = datetime.now(UTC)
    student_email = "2022074255@upt.pe"

    try:
        sesion = SesionMentoria(
            id_sesion=1407,
            codigo_sesion="SES-DB-1407",
            mentor_email="mentor.real@upt.pe",
            id_asignatura=1,
            id_tema=1,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Lab 101",
            estado="FINALIZADA",
            fecha_inicio=now - timedelta(hours=3),
            duracion_minutos=60,
        )
        asistencia = AsistenciaSesion(
            id_sesion=1407,
            estudiante_email=student_email,
            asistio=True,
            fecha_checkin=now - timedelta(hours=3),
        )
        db.add(sesion)
        db.add(asistencia)
        db.commit()

        from app.schemas.survey import SurveyCreatePayload

        payload = SurveyCreatePayload(
            calificacion_general=5,
            dominio_tema=5,
            claridad_explicacion=4,
            puntualidad=5,
            comentarios="Explicación sumamente clara de estructuras de datos y árboles AVL.",
        )

        resp = SurveyService.create_survey(
            db=db,
            session_id=1407,
            payload=payload,
            caller_email=student_email,
            now_utc=now,
        )
        assert resp.id_encuesta > 0
        assert resp.id_sesion == 1407

        # Verificar consulta en BD
        saved = db.query(EncuestaCalidad).filter(EncuestaCalidad.id_sesion == 1407).first()
        assert saved is not None
        assert saved.estudiante_email == student_email
        assert saved.calificacion_general == 5

        # Verificar rechazo por duplicado en BD
        with pytest.raises(Exception) as exc_dup:
            SurveyService.create_survey(
                db=db,
                session_id=1407,
                payload=payload,
                caller_email=student_email,
                now_utc=now,
            )
        assert "DUPLICATE_SURVEY_SUBMISSION" in str(exc_dup.value)

    finally:
        db.close()


def test_survey_t39_rejects_before_session_concluded_400():
    """T-39 / RN-13: Rechaza envío de encuesta antes de la conclusión formal de la sesión."""
    student_email = "2022074255@upt.pe"
    token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    # Sesión inicia en 1 hora (no concluida)
    _memory_offers.append(
        {
            "id_sesion": 1408,
            "codigo_sesion": "SES-SURV-1408",
            "mentor_email": "mentor.sistemas@upt.pe",
            "estado": "CONFIRMADA",
            "fecha_inicio": (now + timedelta(hours=1)).isoformat(),
            "duracion_minutos": 60,
        }
    )
    _memory_attendances.append(
        {
            "id_asistencia": 8,
            "id_sesion": 1408,
            "estudiante_email": student_email,
            "asistio": True,
        }
    )

    payload = {
        "calificacion_general": 5,
        "dominio_tema": 5,
        "claridad_explicacion": 5,
        "puntualidad": 5,
        "comentarios": "Excelente explicación y desarrollo pedagógico completo.",
    }

    res = client.post(
        "/api/v1/sessions/1408/survey",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400
    assert "SURVEY_WINDOW_NOT_OPEN" in res.json()["detail"]


def test_survey_t39_rejects_cancelled_session_400():
    """T-39: Rechaza evaluar una sesión cancelada."""
    student_email = "2022074255@upt.pe"
    token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 1409,
            "codigo_sesion": "SES-SURV-1409",
            "mentor_email": "mentor.sistemas@upt.pe",
            "estado": "CANCELADA_MENTOR",
            "fecha_inicio": (now - timedelta(hours=3)).isoformat(),
            "duracion_minutos": 60,
        }
    )
    _memory_attendances.append(
        {
            "id_asistencia": 9,
            "id_sesion": 1409,
            "estudiante_email": student_email,
            "asistio": True,
        }
    )

    payload = {
        "calificacion_general": 5,
        "dominio_tema": 5,
        "claridad_explicacion": 5,
        "puntualidad": 5,
        "comentarios": "Comentarios de retroalimentación cualitativa sustantiva...",
    }

    res = client.post(
        "/api/v1/sessions/1409/survey",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400
    assert "INVALID_SESSION_STATE" in res.json()["detail"]


def test_survey_t39_sanitizes_xss_in_comments():
    """T-39: Sanitiza posibles ataques XSS en comentarios de la encuesta."""
    student_email = "2022074255@upt.pe"
    token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 1410,
            "codigo_sesion": "SES-SURV-1410",
            "mentor_email": "mentor.sistemas@upt.pe",
            "estado": "FINALIZADA",
            "fecha_inicio": (now - timedelta(hours=3)).isoformat(),
            "duracion_minutos": 60,
        }
    )
    _memory_attendances.append(
        {
            "id_asistencia": 10,
            "id_sesion": 1410,
            "estudiante_email": student_email,
            "asistio": True,
        }
    )

    payload = {
        "calificacion_general": 5,
        "dominio_tema": 5,
        "claridad_explicacion": 5,
        "puntualidad": 5,
        "comentarios": "<script>alert('xss')</script> Buen docente.",
    }

    res = client.post(
        "/api/v1/sessions/1410/survey",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201
    assert "<script>" not in res.json()["comentarios"]
    assert "&lt;script&gt;" in res.json()["comentarios"]
