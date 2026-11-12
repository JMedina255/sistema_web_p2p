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
    res_get = client.get(
        "/api/v1/sessions/951/bitacora",
        headers={"Authorization": f"Bearer {token}"},
    )
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


def test_bitacora_t41_visar_success_by_admin():
    """T-41 / RN-14: Visado exitoso de horas formativas por autoridad universitaria con rol administrador."""
    admin_email = "admin.epis@upt.pe"
    admin_token = create_access_token({"sub": admin_email, "roles": ["administrador"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 971,
            "codigo_sesion": "SES-BIT-971",
            "mentor_email": "mentor@upt.pe",
            "estado": "BITACORA_REGISTRADA",
            "fecha_inicio": (now - timedelta(hours=3)).isoformat(),
            "duracion_minutos": 120,
        }
    )

    from app.services.bitacora_service import _memory_bitacoras

    _memory_bitacoras.append(
        {
            "id_bitacora": 71,
            "id_sesion": 971,
            "id_mentor": "mentor@upt.pe",
            "temas_cubiertos": ["Recursión de cola y árboles"],
            "observaciones": "Se cubrió satisfactoriamente toda la sesión con 10 asistentes activos.",
            "nivel_dificultad": "Medio",
            "hash_firma": "sha256-mock-hash-71",
            "horas_declaradas": 2.0,
            "visado_administrador": False,
            "created_at": now.isoformat(),
        }
    )

    res = client.post(
        "/api/v1/bitacoras/71/visar",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["visado_administrador"] is True
    assert data["estado_sesion"] == "HORAS_VISADAS"
    assert data["horas_declaradas"] == 2.0
    assert data["auditor_email"] == admin_email

    # Verificar mutación de oferta
    target = next(o for o in _memory_offers if o["id_sesion"] == 971)
    assert target["estado"] == "HORAS_VISADAS"


def test_bitacora_t41_visar_rejects_non_admin_403():
    """T-41 / RNF02: Rechaza intento de visado de horas por usuarios sin rol institucional de administrador."""
    mentor_token = create_access_token({"sub": "mentor@upt.pe", "roles": ["mentor"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 972,
            "mentor_email": "mentor@upt.pe",
            "estado": "BITACORA_REGISTRADA",
            "duracion_minutos": 60,
        }
    )

    from app.services.bitacora_service import _memory_bitacoras

    _memory_bitacoras.append(
        {
            "id_bitacora": 72,
            "id_sesion": 972,
            "id_mentor": "mentor@upt.pe",
            "temas_cubiertos": ["Grafos"],
            "observaciones": "Sesión completada con desarrollo de algoritmos de Dijkstra.",
            "nivel_dificultad": "Alto",
            "hash_firma": "sha256-mock-hash-72",
            "horas_declaradas": 1.0,
            "visado_administrador": False,
            "created_at": now.isoformat(),
        }
    )

    res = client.post(
        "/api/v1/bitacoras/72/visar",
        headers={"Authorization": f"Bearer {mentor_token}"},
    )
    assert res.status_code == 403
    assert "ADMIN_ROLE_REQUIRED" in res.json()["detail"]


def test_bitacora_t41_observar_success_with_justification():
    """T-41 / RF26: Formulación de observación técnica debidamente justificada (>= 15 chars) por Administrador."""
    admin_token = create_access_token({"sub": "admin.epis@upt.pe", "roles": ["administrador"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 973,
            "mentor_email": "mentor@upt.pe",
            "estado": "BITACORA_REGISTRADA",
            "duracion_minutos": 60,
        }
    )

    from app.services.bitacora_service import _memory_bitacoras

    _memory_bitacoras.append(
        {
            "id_bitacora": 73,
            "id_sesion": 973,
            "id_mentor": "mentor@upt.pe",
            "temas_cubiertos": ["Programación dinámica"],
            "observaciones": "Se desarrollaron ejercicios de la mochila y subsecuencia común.",
            "nivel_dificultad": "Medio",
            "hash_firma": "sha256-mock-hash-73",
            "horas_declaradas": 1.0,
            "visado_administrador": False,
            "created_at": now.isoformat(),
        }
    )

    payload = {"motivo": "Discrepancia detectada en lista de temas silábicos cubiertos vs tiempo reportado."}

    res = client.post(
        "/api/v1/bitacoras/73/observar",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["estado_sesion"] == "OBSERVADA"
    assert "Discrepancia detectada" in data["motivo_observacion"]

    # Verificar mutación de estado en oferta
    target = next(o for o in _memory_offers if o["id_sesion"] == 973)
    assert target["estado"] == "OBSERVADA"


def test_bitacora_t41_observar_rejects_short_justification_422():
    """T-41 / RF26: Rechaza observación si no contiene justificación sustantiva de al menos 15 caracteres."""
    admin_token = create_access_token({"sub": "admin.epis@upt.pe", "roles": ["administrador"]})

    payload = {"motivo": "Muy breve"}  # < 15 caracteres

    res = client.post(
        "/api/v1/bitacoras/73/observar",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 422
    assert "OBSERVATION_REASON_REQUIRED" in str(res.json())


def test_bitacora_t41_observar_rejects_non_admin_403():
    """T-41 / RNF02: Rechaza formulación de observación técnica por usuarios no administradores."""
    student_token = create_access_token({"sub": "2022074255@upt.pe", "roles": ["mentoreado"]})

    payload = {"motivo": "Observación emitida indebidamente por estudiante."}

    res = client.post(
        "/api/v1/bitacoras/73/observar",
        json=payload,
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 403
    assert "ADMIN_ROLE_REQUIRED" in res.json()["detail"]


def test_bitacora_t40_list_inbox_with_filters():
    """T-40: Consulta de bandeja administrativa de bitácoras con soporte de filtros."""
    admin_token = create_access_token({"sub": "admin.epis@upt.pe", "roles": ["administrador"]})
    now = datetime.now(UTC)

    from app.services.bitacora_service import _memory_bitacoras

    _memory_offers.extend(
        [
            {"id_sesion": 981, "codigo_sesion": "SES-981", "estado": "BITACORA_REGISTRADA"},
            {"id_sesion": 982, "codigo_sesion": "SES-982", "estado": "HORAS_VISADAS"},
            {"id_sesion": 983, "codigo_sesion": "SES-983", "estado": "OBSERVADA"},
        ]
    )

    _memory_bitacoras.extend(
        [
            {
                "id_bitacora": 81,
                "id_sesion": 981,
                "id_mentor": "mentor1@upt.pe",
                "temas_cubiertos": ["Tema 1"],
                "observaciones": "Observaciones de al menos 50 caracteres para la bitacora 81...",
                "nivel_dificultad": "Medio",
                "hash_firma": "hash81",
                "horas_declaradas": 1.5,
                "visado_administrador": False,
                "created_at": now.isoformat(),
            },
            {
                "id_bitacora": 82,
                "id_sesion": 982,
                "id_mentor": "mentor2@upt.pe",
                "temas_cubiertos": ["Tema 2"],
                "observaciones": "Observaciones de al menos 50 caracteres para la bitacora 82...",
                "nivel_dificultad": "Bajo",
                "hash_firma": "hash82",
                "horas_declaradas": 2.0,
                "visado_administrador": True,
                "created_at": now.isoformat(),
            },
            {
                "id_bitacora": 83,
                "id_sesion": 983,
                "id_mentor": "mentor3@upt.pe",
                "temas_cubiertos": ["Tema 3"],
                "observaciones": "Observaciones de al menos 50 caracteres para la bitacora 83...",
                "nivel_dificultad": "Alto",
                "hash_firma": "hash83",
                "horas_declaradas": 1.0,
                "visado_administrador": False,
                "created_at": now.isoformat(),
            },
        ]
    )

    res_all = client.get(
        "/api/v1/bitacoras?estado=TODAS",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res_all.status_code == 200
    assert len(res_all.json()) == 3

    res_pendientes = client.get(
        "/api/v1/bitacoras?estado=PENDIENTES",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res_pendientes.status_code == 200
    assert len(res_pendientes.json()) == 1
    assert res_pendientes.json()[0]["id_bitacora"] == 81

    res_visadas = client.get(
        "/api/v1/bitacoras?estado=VISADAS",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res_visadas.status_code == 200
    assert len(res_visadas.json()) == 1
    assert res_visadas.json()[0]["id_bitacora"] == 82


def test_bitacora_t41_visado_and_observacion_persistence_real_database():
    """T-41: Verificación de visado y observación de bitácora en base de datos SQLAlchemy real."""
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    now = datetime.now(UTC)
    admin_email = "admin.real@upt.pe"

    try:
        sesion = SesionMentoria(
            id_sesion=990,
            codigo_sesion="SES-DB-990",
            mentor_email="mentor.real@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now - timedelta(hours=3),
            duracion_minutos=90,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Lab 101",
            estado="BITACORA_REGISTRADA",
        )
        b_entity = BitacoraPedagogica(
            id_bitacora=90,
            id_sesion=990,
            id_mentor="mentor.real@upt.pe",
            temas_cubiertos=["Árboles B+"],
            observaciones="Desarrollo completo con ejercicios prácticos sobre indexación en BD.",
            nivel_dificultad="Alto",
            hash_firma="hash990",
            horas_declaradas=1.5,
            visado_administrador=False,
            created_at=now,
        )
        db.add(sesion)
        db.add(b_entity)
        db.commit()

        # 1. Visar bitácora
        visado_resp = BitacoraService.visar_bitacora(
            db=db,
            bitacora_id=90,
            caller_email=admin_email,
            is_admin=True,
            now_utc=now,
        )
        assert visado_resp.visado_administrador is True
        assert visado_resp.horas_declaradas == 1.5
        assert sesion.estado == "HORAS_VISADAS"

        # 2. Observar bitácora
        obs_resp = BitacoraService.observar_bitacora(
            db=db,
            bitacora_id=90,
            motivo="Observación técnica de auditoría: requiere adjuntar lista detallada de asistencia.",
            caller_email=admin_email,
            is_admin=True,
            now_utc=now,
        )
        assert obs_resp.estado_sesion == "OBSERVADA"
        assert b_entity.visado_administrador is False
        assert sesion.estado == "OBSERVADA"

    finally:
        db.close()
        engine.dispose()


def test_bitacora_t41_visar_rejects_cancelled_session_400():
    """T-41 / RN-14: Rechaza visar bitácora si la sesión asociada se encuentra cancelada."""
    admin_token = create_access_token({"sub": "admin.epis@upt.pe", "roles": ["administrador"]})
    now = datetime.now(UTC)

    from app.services.bitacora_service import _memory_bitacoras

    _memory_offers.append(
        {
            "id_sesion": 991,
            "mentor_email": "mentor@upt.pe",
            "estado": "CANCELADA_MENTOR",
            "duracion_minutos": 60,
        }
    )
    _memory_bitacoras.append(
        {
            "id_bitacora": 91,
            "id_sesion": 991,
            "id_mentor": "mentor@upt.pe",
            "temas_cubiertos": ["Algoritmos Voraces"],
            "observaciones": "Observaciones docentes con mas de 50 caracteres...",
            "nivel_dificultad": "Medio",
            "hash_firma": "hash91",
            "horas_declaradas": 1.0,
            "visado_administrador": False,
            "created_at": now.isoformat(),
        }
    )

    res = client.post(
        "/api/v1/bitacoras/91/visar",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 400
    assert "INVALID_SESSION_STATE" in res.json()["detail"]


def test_bitacora_t41_observar_rejects_cancelled_session_400():
    """T-41 / RF26: Rechaza formular observación técnica sobre una sesión cancelada."""
    admin_token = create_access_token({"sub": "admin.epis@upt.pe", "roles": ["administrador"]})
    now = datetime.now(UTC)

    from app.services.bitacora_service import _memory_bitacoras

    _memory_offers.append(
        {
            "id_sesion": 992,
            "mentor_email": "mentor@upt.pe",
            "estado": "CANCELADA_QUORUM",
            "duracion_minutos": 60,
        }
    )
    _memory_bitacoras.append(
        {
            "id_bitacora": 92,
            "id_sesion": 992,
            "id_mentor": "mentor@upt.pe",
            "temas_cubiertos": ["Programación"],
            "observaciones": "Observaciones docentes con mas de 50 caracteres...",
            "nivel_dificultad": "Medio",
            "hash_firma": "hash92",
            "horas_declaradas": 1.0,
            "visado_administrador": False,
            "created_at": now.isoformat(),
        }
    )

    payload = {"motivo": "Justificación válida de al menos 15 caracteres para la observación."}
    res = client.post(
        "/api/v1/bitacoras/92/observar",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 400
    assert "INVALID_SESSION_STATE" in res.json()["detail"]


def test_bitacora_t40_list_inbox_rejects_non_admin_403():
    """T-40 / RNF02: Rechaza consulta de la bandeja administrativa de bitácoras a usuarios no administradores."""
    student_token = create_access_token({"sub": "estudiante@upt.pe", "roles": ["mentoreado"]})

    res = client.get(
        "/api/v1/bitacoras",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 403
    assert "ADMIN_ROLE_REQUIRED" in res.json()["detail"]


def test_bitacora_t35_create_rejects_cancelled_session_400():
    """T-35: Rechaza registro de bitácora para una sesión que fue cancelada."""
    mentor = "mentor@upt.pe"
    mentor_token = create_access_token({"sub": mentor, "roles": ["mentor"]})
    now = datetime.now(UTC)

    _memory_offers.append(
        {
            "id_sesion": 993,
            "mentor_email": mentor,
            "estado": "CANCELADA_MENTOR",
            "fecha_inicio": (now - timedelta(hours=2)).isoformat(),
            "duracion_minutos": 60,
        }
    )

    payload = {
        "temas_cubiertos": ["Backtracking y Grafos"],
        "observaciones": "Intento de registro de bitacora para una sesion previamente cancelada.",
        "nivel_dificultad": "Medio",
    }

    res = client.post(
        "/api/v1/sessions/993/bitacora",
        json=payload,
        headers={"Authorization": f"Bearer {mentor_token}"},
    )
    assert res.status_code == 400
    assert "INVALID_SESSION_STATE" in res.json()["detail"]
