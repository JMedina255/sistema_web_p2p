from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import create_access_token
from app.db.session import Base
from app.main import app
from app.models.curriculum import Asignatura, TemaConceptual
from app.models.profile import PerfilAcademico
from app.services.offer_service import clear_offers_in_memory, seed_default_offers_in_memory
from app.services.profile_service import set_profile_in_memory

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_offers():
    clear_offers_in_memory()
    yield
    clear_offers_in_memory()


def test_publish_offer_presencial_success():
    mentor_email = "2022073504@upt.pe"  # Renzo (Ciclo 7 / Mentor)
    token = create_access_token({"sub": mentor_email, "roles": ["mentor"]})

    # Antelación válida > 24 horas (48 horas en el futuro)
    future_date = (datetime.now(UTC) + timedelta(hours=48)).isoformat()

    payload = {
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites y Continuidad",
        "fecha_inicio": future_date,
        "duracion_minutos": 60,
        "modalidad": "presencial",
        "aforo_maximo": 10,
        "espacio_asignado": "Laboratorio de Cómputo 101 - Pabellón G (EPIS)",
        "mentor_email": mentor_email,
        "mentor_nombre": "Renzo Antonio Antayhua Mamani",
        "notas_adicionales": "Traer guía de límites",
    }

    response = client.post(
        "/api/v1/offers",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["estado"] == "PUBLICADA"
    assert data["codigo_sesion"].startswith("SES-")
    assert data["aforo"] == 10
    assert data["offer"]["mentor_email"] == mentor_email


def test_publish_offer_virtual_success():
    mentor_email = "mentor.avanzado@upt.pe"  # Ciclo 9
    token = create_access_token({"sub": mentor_email, "roles": ["mentor"]})

    future_date = (datetime.now(UTC) + timedelta(days=3)).isoformat()

    payload = {
        "id_asignatura": 3,
        "codigo_asignatura": "ALGO-202",
        "nombre_asignatura": "Algoritmos y Estructuras de Datos",
        "id_tema": 9,
        "nombre_tema": "Análisis Asintótico y Notación Big-O",
        "fecha_inicio": future_date,
        "duracion_minutos": 90,
        "modalidad": "virtual",
        "aforo_maximo": 20,
        "espacio_asignado": "https://meet.google.com/upt-epis-algo202",
        "mentor_email": mentor_email,
        "mentor_nombre": "Carlos Alberto Mendoza Dávila",
    }

    response = client.post(
        "/api/v1/offers",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["estado"] == "PUBLICADA"
    assert data["aforo"] == 20


def test_publish_offer_rejects_rn04_antelation_under_24_hours():
    mentor_email = "2022073504@upt.pe"
    token = create_access_token({"sub": mentor_email, "roles": ["mentor"]})

    # Antelación inválida: solo 12 horas en el futuro (< 24 h)
    short_date = (datetime.now(UTC) + timedelta(hours=12)).isoformat()

    payload = {
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites y Continuidad",
        "fecha_inicio": short_date,
        "duracion_minutos": 60,
        "modalidad": "presencial",
        "aforo_maximo": 10,
        "espacio_asignado": "Laboratorio 101",
        "mentor_email": mentor_email,
    }

    response = client.post(
        "/api/v1/offers",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == 400
    assert "Infracción de RN-04" in response.json()["detail"]


def test_publish_offer_rejects_past_datetime():
    mentor_email = "2022073504@upt.pe"
    token = create_access_token({"sub": mentor_email, "roles": ["mentor"]})

    past_date = (datetime.now(UTC) - timedelta(hours=2)).isoformat()

    payload = {
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites",
        "fecha_inicio": past_date,
        "duracion_minutos": 60,
        "modalidad": "presencial",
        "aforo_maximo": 10,
        "espacio_asignado": "Laboratorio 101",
        "mentor_email": mentor_email,
    }

    response = client.post(
        "/api/v1/offers",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == 400
    assert "pasado" in response.json()["detail"].lower()


def test_publish_offer_rejects_capacity_mismatch_rn05():
    mentor_email = "2022073504@upt.pe"
    token = create_access_token({"sub": mentor_email, "roles": ["mentor"]})
    future_date = (datetime.now(UTC) + timedelta(hours=48)).isoformat()

    # Presencial con 25 cupos (debe ser 10)
    payload = {
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites",
        "fecha_inicio": future_date,
        "duracion_minutos": 60,
        "modalidad": "presencial",
        "aforo_maximo": 25,
        "espacio_asignado": "Laboratorio 101",
        "mentor_email": mentor_email,
    }

    response = client.post(
        "/api/v1/offers",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == 422 or response.status_code == 400


def test_publish_offer_rejects_ineligible_mentor_rn03():
    # Estudiante de ciclo 4 (no habilitado como mentor)
    ineligible_email = "estudiante.ciclo4@upt.pe"
    set_profile_in_memory(
        ineligible_email,
        {
            "email": ineligible_email,
            "ciclo_actual": 4,
            "rol_postulacion": "mentoreado",
        },
    )
    token = create_access_token({"sub": ineligible_email, "roles": ["mentoreado"]})
    future_date = (datetime.now(UTC) + timedelta(hours=48)).isoformat()

    payload = {
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites",
        "fecha_inicio": future_date,
        "duracion_minutos": 60,
        "modalidad": "presencial",
        "aforo_maximo": 10,
        "espacio_asignado": "Laboratorio 101",
        "mentor_email": ineligible_email,
    }

    response = client.post(
        "/api/v1/offers",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == 403
    assert "RN-03" in response.json()["detail"]


def test_publish_offer_user_cannot_publish_for_another_forbidden():
    mentor1 = "2022073504@upt.pe"
    mentor2 = "mentor.avanzado@upt.pe"
    token1 = create_access_token({"sub": mentor1, "roles": ["mentor"]})
    future_date = (datetime.now(UTC) + timedelta(hours=48)).isoformat()

    payload = {
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites",
        "fecha_inicio": future_date,
        "duracion_minutos": 60,
        "modalidad": "presencial",
        "aforo_maximo": 10,
        "espacio_asignado": "Laboratorio 101",
        "mentor_email": mentor2,  # Intento de suplantación
    }

    response = client.post(
        "/api/v1/offers",
        headers={"Authorization": f"Bearer {token1}"},
        json=payload,
    )
    assert response.status_code == 403


def test_list_offers_with_filters():
    seed_default_offers_in_memory()

    # 1. Sin filtros
    res_all = client.get("/api/v1/offers")
    assert res_all.status_code == 200
    items = res_all.json()
    assert len(items) >= 3

    # 2. Filtro por mentor
    res_mentor = client.get("/api/v1/offers?mentor_email=2022073504@upt.pe")
    assert res_mentor.status_code == 200
    for item in res_mentor.json():
        assert item["offer"]["mentor_email"] == "2022073504@upt.pe"

    # 3. Filtro por asignatura
    res_asig = client.get("/api/v1/offers?id_asignatura=1")
    assert res_asig.status_code == 200
    for item in res_asig.json():
        assert item["offer"]["id_asignatura"] == 1

    # 4. Filtro por modalidad
    res_mod = client.get("/api/v1/offers?modalidad=virtual")
    assert res_mod.status_code == 200
    for item in res_mod.json():
        assert item["offer"]["modalidad"] == "virtual"


def test_offer_service_with_real_db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    try:
        # Sembrar curso y tema
        asig = Asignatura(
            id_asignatura=1,
            codigo_curso="CALC-101",
            nombre_curso="Cálculo I",
            ciclo_plan=1,
            creditos=4,
            factor_ponderacion=1.2,
        )
        tema = TemaConceptual(
            id_tema=1,
            id_asignatura=1,
            nombre_tema="Límites",
            unidad_silabica=1,
        )
        mentor_profile = PerfilAcademico(
            email="2022073504@upt.pe",
            ciclo_actual=7,
            rol_postulacion="mentor",
        )
        db.add_all([asig, tema, mentor_profile])
        db.commit()

        future_date = (datetime.now(UTC) + timedelta(hours=48)).isoformat()
        from app.schemas.offer import PublishOfferPayload
        from app.services.offer_service import OfferService

        payload = PublishOfferPayload(
            id_asignatura=1,
            codigo_asignatura="CALC-101",
            nombre_asignatura="Cálculo I",
            id_tema=1,
            nombre_tema="Límites",
            fecha_inicio=future_date,
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Lab 101",
            mentor_email="2022073504@upt.pe",
        )

        resp = OfferService.publish_offer(db=db, payload=payload)
        assert resp.codigo_sesion.startswith("SES-")
        assert resp.estado == "PUBLICADA"

        # Verificar consulta en BD
        offers_db = OfferService.get_offers(db=db, id_asignatura=1)
        assert len(offers_db) >= 1
    finally:
        db.close()
        engine.dispose()


def test_publish_offer_rejects_external_email_validation():
    future_date = (datetime.now(UTC) + timedelta(hours=48)).isoformat()
    payload = {
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites",
        "fecha_inicio": future_date,
        "duracion_minutos": 60,
        "modalidad": "presencial",
        "aforo_maximo": 10,
        "espacio_asignado": "Laboratorio 101",
        "mentor_email": "usuario.externo@gmail.com",
    }
    response = client.post("/api/v1/offers", json=payload)
    assert response.status_code == 422


def test_publish_offer_rejects_virtual_capacity_mismatch():
    future_date = (datetime.now(UTC) + timedelta(hours=48)).isoformat()
    payload = {
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites",
        "fecha_inicio": future_date,
        "duracion_minutos": 60,
        "modalidad": "virtual",
        "aforo_maximo": 10,  # Debe ser 20 para virtual
        "espacio_asignado": "https://meet.google.com/test",
        "mentor_email": "2022073504@upt.pe",
    }
    response = client.post("/api/v1/offers", json=payload)
    assert response.status_code == 422


def test_get_offers_empty_db_returns_empty_list_no_leak():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()
    try:
        from app.services.offer_service import OfferService

        # Con sesión de BD activa pero 0 registros en sesiones_mentoria
        offers = OfferService.get_offers(db=db)
        assert len(offers) == 0
    finally:
        db.close()
        engine.dispose()


def test_publish_offer_exact_24_hours_boundary():
    mentor_email = "2022073504@upt.pe"
    token = create_access_token({"sub": mentor_email, "roles": ["mentor"]})

    # Exactamente 24 horas y 0 segundos: debe rechazarse según RN-04 (T > 24 h)
    exact_24h = (datetime.now(UTC) + timedelta(hours=24)).isoformat()
    payload = {
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites",
        "fecha_inicio": exact_24h,
        "duracion_minutos": 60,
        "modalidad": "presencial",
        "aforo_maximo": 10,
        "espacio_asignado": "Laboratorio 101",
        "mentor_email": mentor_email,
    }
    res_exact = client.post(
        "/api/v1/offers",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert res_exact.status_code == 400
    assert "Infracción de RN-04" in res_exact.json()["detail"]

    # 24 horas y 2 minutos (T > 24.0 h): debe aceptarse
    valid_advance = (datetime.now(UTC) + timedelta(hours=24, minutes=2)).isoformat()
    payload["fecha_inicio"] = valid_advance
    res_valid = client.post(
        "/api/v1/offers",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert res_valid.status_code == 201


def test_publish_offer_rejects_invalid_date_format():
    mentor_email = "2022073504@upt.pe"
    token = create_access_token({"sub": mentor_email, "roles": ["mentor"]})

    payload = {
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites",
        "fecha_inicio": "fecha-invalida-no-iso",
        "duracion_minutos": 60,
        "modalidad": "presencial",
        "aforo_maximo": 10,
        "espacio_asignado": "Laboratorio 101",
        "mentor_email": mentor_email,
    }
    res = client.post(
        "/api/v1/offers",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert res.status_code == 400
    assert "inválido" in res.json()["detail"].lower()
