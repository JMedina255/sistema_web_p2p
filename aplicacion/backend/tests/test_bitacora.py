from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import create_access_token
from app.db.session import Base
from app.main import app
from app.models.bitacora import BitacoraPedagogica
from app.models.offer import SesionMentoria
from app.services.bitacora_service import (
    BitacoraService,
    clear_bitacoras_in_memory,
)
from app.services.offer_service import (
    _memory_offers,
    clear_offers_in_memory,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_teardown_bitacora():
    clear_offers_in_memory()
    clear_bitacoras_in_memory()
    yield
    clear_offers_in_memory()
    clear_bitacoras_in_memory()


def test_bitacora_t35_success_within_48h_in_memory():
    """T-35: Registro exitoso de bitácora pedagógica con SHA-256 y acreditación de horas."""
    mentor = "mentor.academico@upt.pe"
    token = create_access_token({"sub": mentor, "roles": ["mentor"]})
    now = datetime.now(UTC)

    # Sesión concluida hace 2 horas (bien dentro de la ventana de 48h)
    _memory_offers.append(
        {
            "id_sesion": 951,
            "codigo_sesion": "SES-BIT-951",
            "mentor_email": mentor,
            "estado": "CONCLUIDA",
            "fecha_inicio": (now - timedelta(hours=3)).isoformat(),
            "duracion_minutos": 90,
        }
    )

    payload = {
        "temas_cubiertos": ["Definición formal de límites", "Asíntotas verticales y horizontales"],
        "observaciones": "La sesión se desarrolló con activa participación estudiantil, resolviendo dudas conceptuales críticas del sílabo oficial.",
        "nivel_dificultad": "Medio",
    }

    res = client.post(
        "/api/v1/sessions/951/bitacora",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["id_sesion"] == 951
    assert data["id_mentor"] == mentor
    assert len(data["hash_firma"]) == 64
    assert data["horas_declaradas"] == 1.5  # 90 / 60.0
    assert data["nivel_dificultad"] == "Medio"

    # Verificar mutación de estado a BITACORA_REGISTRADA
    target = next(o for o in _memory_offers if o["id_sesion"] == 951)
    assert target["estado"] == "BITACORA_REGISTRADA"

    # Consultar endpoint GET
    res_get = client.get("/api/v1/sessions/951/bitacora")
    assert res_get.status_code == 200
    assert res_get.json()["hash_firma"] == data["hash_firma"]


def test_bitacora_t35_rejects_exceeded_deadline_rn12():
    """T-35 / RN-12: Rechaza registro extemporáneo cuando transcurren más de 48h tras el fin de sesión."""
    mentor = "mentor.academico@upt.pe"
    token = create_access_token({"sub": mentor, "roles": ["mentor"]})
    now = datetime.now(UTC)

    # Sesión concluida hace 50 horas (ventana de 48h vencida)
    _memory_offers.append(
        {
            "id_sesion": 952,
            "codigo_sesion": "SES-BIT-952",
            "mentor_email": mentor,
            "estado": "CONCLUIDA",
            "fecha_inicio": (now - timedelta(hours=52)).isoformat(),
            "duracion_minutos": 60,
        }
    )

    payload = {
        "temas_cubiertos": ["Recursividad y Árboles"],
        "observaciones": "Sesión realizada pero reportada fuera de plazo reglamentario debido a problemas de conectividad.",
        "nivel_dificultad": "Alto",
    }

    res = client.post(
        "/api/v1/sessions/952/bitacora",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400
    assert "DEADLINE_EXCEEDED" in res.json()["detail"]


def test_bitacora_t35_rejects_observations_under_50_chars():
    """T-35: Rechaza observaciones pedagógicas insuficientes (< 50 caracteres)."""
    mentor = "mentor.academico@upt.pe"
    token = create_access_token({"sub": mentor, "roles": ["mentor"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 953,
            "codigo_sesion": "SES-BIT-953",
            "mentor_email": mentor,
            "estado": "CONCLUIDA",
            "fecha_inicio": (now - timedelta(hours=2)).isoformat(),
            "duracion_minutos": 60,
        }
    )

    payload = {
        "temas_cubiertos": ["Programación Orientada a Objetos"],
        "observaciones": "Clase corta y rápida.",  # 21 caracteres (< 50)
        "nivel_dificultad": "Bajo",
    }

    res = client.post(
        "/api/v1/sessions/953/bitacora",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 422


def test_bitacora_t35_rejects_non_mentor_user_403():
    """T-35: Rechaza con 403 Forbidden a usuarios que no son el mentor titular de la sesión."""
    otro_usuario = "alumno.ajeno@upt.pe"
    token = create_access_token({"sub": otro_usuario, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 954,
            "codigo_sesion": "SES-BIT-954",
            "mentor_email": "mentor.titular@upt.pe",
            "estado": "CONCLUIDA",
            "fecha_inicio": (now - timedelta(hours=2)).isoformat(),
            "duracion_minutos": 60,
        }
    )

    payload = {
        "temas_cubiertos": ["Estructuras Lineales"],
        "observaciones": "Intento no autorizado de suplantación de bitácora pedagógica por un usuario ajeno.",
        "nivel_dificultad": "Medio",
    }

    res = client.post(
        "/api/v1/sessions/954/bitacora",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert "FORBIDDEN" in res.json()["detail"]


def test_bitacora_rejects_fake_admin_email_substring_403():
    """T-35 / RNF02: Correo que contiene 'admin' sin rol 'administrador' es rechazado con 403."""
    fake_admin = "admin_estudiante@upt.pe"
    token = create_access_token({"sub": fake_admin, "roles": ["mentoreado"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 955,
            "codigo_sesion": "SES-BIT-955",
            "mentor_email": "mentor.titular@upt.pe",
            "estado": "CONCLUIDA",
            "fecha_inicio": (now - timedelta(hours=2)).isoformat(),
            "duracion_minutos": 60,
        }
    )

    payload = {
        "temas_cubiertos": ["Estructuras Lineales"],
        "observaciones": "Intento no autorizado de suplantación de bitácora pedagógica por un usuario con subcadena admin.",
        "nivel_dificultad": "Medio",
    }

    res = client.post(
        "/api/v1/sessions/955/bitacora",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403
    assert "FORBIDDEN" in res.json()["detail"]



def test_bitacora_t35_persistence_in_real_database():
    """T-35: Verificación en base de datos real con cálculo de horas proporcionales y firma SHA-256."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionTest = sessionmaker(bind=engine)
    db = SessionTest()

    try:
        now = datetime.now(UTC)
        mentor_email = "mentor.persistencia@upt.pe"
        sesion = SesionMentoria(
            id_sesion=960,
            codigo_sesion="SES-DB-960",
            mentor_email=mentor_email,
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now - timedelta(hours=4),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Lab 101",
            estado="CONCLUIDA",
        )
        db.add(sesion)
        db.commit()

        from app.schemas.bitacora import BitacoraCreatePayload

        b_payload = BitacoraCreatePayload(
            temas_cubiertos=["Derivadas de funciones implícitas", "Regla de la Cadena"],
            observaciones="Desarrollo completo de la guía práctica con alta comprensión del estudiantado.",
            nivel_dificultad="Medio",
        )

        res = BitacoraService.create_bitacora(
            db=db,
            session_id=960,
            payload=b_payload,
            caller_email=mentor_email,
        )
        assert res.horas_declaradas == 1.0
        assert len(res.hash_firma) == 64

        # Comprobar en base de datos
        db_b = db.query(BitacoraPedagogica).filter(BitacoraPedagogica.id_sesion == 960).first()
        assert db_b is not None
        assert db_b.hash_firma == res.hash_firma
        assert db_b.visado_administrador is False

        db.refresh(sesion)
        assert sesion.estado == "BITACORA_REGISTRADA"
    finally:
        db.close()
        engine.dispose()
