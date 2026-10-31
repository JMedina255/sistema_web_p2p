from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import create_access_token
from app.db.session import Base
from app.main import app
from app.models.curriculum import Asignatura, TemaConceptual
from app.models.profile import DisponibilidadHoraria, PerfilAcademico
from app.services.offer_service import clear_offers_in_memory, seed_default_offers_in_memory
from app.services.profile_service import set_profile_in_memory
from app.services.recommendation_service import (
    RecommendationService,
    compute_modality_compatibility,
    dice_similarity,
    jaccard_similarity,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_recommendation_tests():
    clear_offers_in_memory()
    seed_default_offers_in_memory()
    yield
    clear_offers_in_memory()


def test_jaccard_and_dice_similarity_properties():
    # Conjuntos idénticos
    set_a = {1, 2, 3}
    assert jaccard_similarity(set_a, set_a) == 1.0
    assert dice_similarity(set_a, set_a) == 1.0

    # Conjuntos disjuntos
    set_b = {4, 5}
    assert jaccard_similarity(set_a, set_b) == 0.0
    assert dice_similarity(set_a, set_b) == 0.0

    # Conjuntos vacíos
    assert jaccard_similarity(set(), set()) == 0.0
    assert dice_similarity(set(), set()) == 0.0

    # Solapamiento parcial: A={1,2}, B={2,3}. Inter=1, Union=3. J=1/3, D=2/(2+2)=0.5
    set_c = {1, 2}
    set_d = {2, 3}
    assert round(jaccard_similarity(set_c, set_d), 4) == round(1 / 3, 4)
    assert dice_similarity(set_c, set_d) == 0.5


def test_modality_compatibility_rules():
    assert compute_modality_compatibility("presencial", "presencial") == 1.0
    assert compute_modality_compatibility("virtual", "virtual") == 1.0
    assert compute_modality_compatibility("hibrida", "presencial") == 0.9
    assert compute_modality_compatibility("presencial", "hibrida") == 0.9
    assert compute_modality_compatibility("presencial", "virtual") == 0.2


def test_compute_candidate_score_rn03_ineligibility():
    # Mentor con ciclo 6 (< VII) -> debe recibir score 0.0 y no elegible
    score, breakdown = RecommendationService.compute_candidate_score(
        mentee_courses={1},
        mentee_topics={1, 2},
        mentee_slots={(1, "08:00", "09:00")},
        mentee_modality="presencial",
        candidate_courses={1},
        candidate_topics={1, 2},
        candidate_slots={(1, "08:00", "09:00")},
        candidate_modality="presencial",
        candidate_cycle=6,
    )
    assert score == 0.0
    assert not breakdown.institutional_merit_eligible
    assert "no elegible" in breakdown.explanation_text.lower()


def test_compute_candidate_score_critical_course_multiplier():
    # Asignatura Algoritmos (ID 3) tiene factor 1.3x
    score_algo, bd_algo = RecommendationService.compute_candidate_score(
        mentee_courses={3},
        mentee_topics={9, 10},
        mentee_slots={(1, "08:00", "09:00")},
        mentee_modality="presencial",
        candidate_courses={3},
        candidate_topics={9, 10},
        candidate_slots={(1, "08:00", "09:00")},
        candidate_modality="presencial",
        candidate_cycle=8,
    )
    assert bd_algo.course_weight_factor == 1.3
    assert bd_algo.critical_course_applied == "ALGO-202"
    # Base score = 0.40(1.0) + 0.35(1.0) + 0.15(1.0) + 0.10(1.0) = 1.0. Total = 1.0 * 1.3 = 1.3
    assert score_algo == 1.3


def test_get_recommended_mentors_endpoint_top_k():
    mentee_email = "2022074255@upt.pe"
    set_profile_in_memory(
        mentee_email,
        {
            "email": mentee_email,
            "ciclo_actual": 3,
            "materias_interes": [1, 3],
            "temas_seleccionados": [1, 2, 9],
            "modalidad_preferida": "presencial",
        },
    )

    response = client.get(f"/api/v1/recommendations/mentors?mentee_email={mentee_email}&top_k=3")
    assert response.status_code == 200
    data = response.json()
    assert data["mentee_email"] == mentee_email
    assert data["recommendations_count"] <= 3
    items = data["items"]
    assert len(items) > 0

    # Verificar que el ordenamiento sea estrictamente decreciente por score
    scores = [item["score_total"] for item in items]
    assert scores == sorted(scores, reverse=True)

    # Verificar que todos cumplan RN-03
    for m in items:
        assert m["mentor_ciclo"] >= 7
        assert m["breakdown"]["institutional_merit_eligible"] is True


def test_get_recommended_mentors_with_bearer_jwt():
    mentee_email = "2022074255@upt.pe"
    token = create_access_token({"sub": mentee_email, "roles": ["mentoreado"]})

    response = client.get(
        "/api/v1/recommendations/mentors",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mentee_email"] == mentee_email


def test_get_recommended_offers_endpoint():
    mentee_email = "2022074255@upt.pe"

    response = client.get(f"/api/v1/recommendations/offers?mentee_email={mentee_email}&id_asignatura=1")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for offer in data["items"]:
        assert offer["id_asignatura"] == 1
        assert offer["mentor_ciclo"] >= 7
        assert offer["breakdown"]["institutional_merit_eligible"] is True


def test_explain_recommendation_mentor():
    mentee_email = "2022074255@upt.pe"
    mentor_email = "2022073504@upt.pe"

    payload = {
        "mentee_email": mentee_email,
        "mentor_email": mentor_email,
    }

    response = client.post("/api/v1/recommendations/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["target_type"] == "mentor"
    assert data["target_id"] == mentor_email
    assert data["breakdown"]["course_weight_factor"] >= 1.0
    assert len(data["institutional_summary"]) > 10


def test_explain_recommendation_offer():
    mentee_email = "2022074255@upt.pe"

    payload = {
        "mentee_email": mentee_email,
        "id_oferta": "SES-1001",
    }

    response = client.post("/api/v1/recommendations/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["target_type"] == "offer"
    assert "SES-1001" in data["target_id"]


def test_explain_recommendation_not_found():
    payload_offer = {
        "mentee_email": "2022074255@upt.pe",
        "id_oferta": "SES-INEXISTENTE-9999",
    }
    response = client.post("/api/v1/recommendations/explain", json=payload_offer)
    assert response.status_code == 404


def test_recommendation_service_with_real_db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    try:
        # 1. Sembrar cursos
        c1 = Asignatura(
            id_asignatura=1,
            codigo_curso="CALC-101",
            nombre_curso="Cálculo I",
            ciclo_plan=1,
            creditos=4,
            factor_ponderacion=1.2,
        )
        t1 = TemaConceptual(id_tema=1, id_asignatura=1, nombre_tema="Límites", unidad_silabica=1)
        db.add_all([c1, t1])

        # 2. Sembrar mentor elegible (Ciclo 8)
        p_mentor = PerfilAcademico(
            email="mentor.test.db@upt.pe",
            codigo_estudiante="2021001",
            nombres="Carlos",
            apellidos="Test",
            ciclo_actual=8,
            rol_postulacion="mentor",
            materias_interes=[1],
            temas_seleccionados=[1],
            modalidad_preferida="presencial",
        )
        disp_mentor = DisponibilidadHoraria(
            email="mentor.test.db@upt.pe",
            dia_semana=1,
            hora_inicio="08:00",
            hora_fin="09:00",
        )
        # 3. Sembrar mentoreado
        p_mentee = PerfilAcademico(
            email="mentee.test.db@upt.pe",
            codigo_estudiante="2024001",
            nombres="Juan",
            apellidos="Test",
            ciclo_actual=2,
            rol_postulacion="mentoreado",
            materias_interes=[1],
            temas_seleccionados=[1],
            modalidad_preferida="presencial",
        )
        disp_mentee = DisponibilidadHoraria(
            email="mentee.test.db@upt.pe",
            dia_semana=1,
            hora_inicio="08:00",
            hora_fin="09:00",
        )
        db.add_all([p_mentor, disp_mentor, p_mentee, disp_mentee])
        db.commit()

        # Probar recomendación usando la sesión real
        res = RecommendationService.recommend_mentors(
            mentee_email="mentee.test.db@upt.pe",
            top_k=5,
            db=db,
        )
        assert res.recommendations_count >= 1
        top_cand = res.items[0]
        assert top_cand.mentor_email == "mentor.test.db@upt.pe"
        assert top_cand.mentor_ciclo == 8
        assert top_cand.breakdown.schedule_matching_slots_count == 1
    finally:
        db.close()
        engine.dispose()


def test_get_recommended_offers_with_bearer_jwt():
    mentee_email = "2022074255@upt.pe"
    token = create_access_token({"sub": mentee_email, "roles": ["mentoreado"]})

    response = client.get(
        "/api/v1/recommendations/offers",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mentee_email"] == mentee_email
    assert "items" in data


def test_explain_recommendation_with_bearer_jwt():
    mentee_email = "2022074255@upt.pe"
    token = create_access_token({"sub": mentee_email, "roles": ["mentoreado"]})

    payload = {
        "mentee_email": mentee_email,
        "mentor_email": "2022073504@upt.pe",
    }
    response = client.post(
        "/api/v1/recommendations/explain",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mentee_email"] == mentee_email
    assert data["target_type"] == "mentor"


def test_offer_schedule_neutral_when_mentee_has_no_slots():
    from datetime import UTC, datetime

    # Mentoreado sin franjas configuradas: debe recibir 0.50 y 0 franjas de coincidencia
    offer_dt = datetime(2026, 10, 30, 10, 0, tzinfo=UTC)
    score, bd = RecommendationService.compute_candidate_score(
        mentee_courses={1},
        mentee_topics={1},
        mentee_slots=set(),
        mentee_modality="presencial",
        candidate_courses={1},
        candidate_topics={1},
        candidate_slots=set(),
        candidate_modality="presencial",
        candidate_cycle=8,
        offer_time=offer_dt,
        offer_duration_minutes=60,
    )
    assert bd.schedule_compatibility == 0.5
    assert bd.schedule_matching_slots_count == 0
    assert bd.matching_slots == []
    assert "no fijó agenda horaria previa" in bd.explanation_text.lower()


def test_offer_schedule_90_minutes_partial_and_full_overlap():
    from datetime import UTC, datetime

    # Viernes (día 5) de 10:00 a 11:30 (cubre franjas 10:00-11:00 y 11:00-12:00)
    offer_dt = datetime(2026, 10, 30, 10, 0, tzinfo=UTC)

    # 1. Coincidencia completa (el mentoreado tiene ambas horas libres)
    mentee_slots_full = {(5, "10:00", "11:00"), (5, "11:00", "12:00")}
    _, bd_full = RecommendationService.compute_candidate_score(
        mentee_courses={1},
        mentee_topics={1},
        mentee_slots=mentee_slots_full,
        mentee_modality="presencial",
        candidate_courses={1},
        candidate_topics={1},
        candidate_slots=set(),
        candidate_modality="presencial",
        candidate_cycle=8,
        offer_time=offer_dt,
        offer_duration_minutes=90,
    )
    assert bd_full.schedule_compatibility == 1.0
    assert bd_full.schedule_matching_slots_count == 2

    # 2. Coincidencia parcial (el mentoreado solo tiene la primera hora libre)
    mentee_slots_partial = {(5, "10:00", "11:00")}
    _, bd_partial = RecommendationService.compute_candidate_score(
        mentee_courses={1},
        mentee_topics={1},
        mentee_slots=mentee_slots_partial,
        mentee_modality="presencial",
        candidate_courses={1},
        candidate_topics={1},
        candidate_slots=set(),
        candidate_modality="presencial",
        candidate_cycle=8,
        offer_time=offer_dt,
        offer_duration_minutes=90,
    )
    assert bd_partial.schedule_compatibility == 0.5
    assert bd_partial.schedule_matching_slots_count == 1


def test_candidate_score_with_corrupt_null_fields_does_not_crash():
    # Perfil con campos nulos en BD
    score, bd = RecommendationService.compute_candidate_score(
        mentee_courses={1},
        mentee_topics={1},
        mentee_slots=set(),
        mentee_modality=None,
        candidate_courses=None,
        candidate_topics=None,
        candidate_slots=None,
        candidate_modality=None,
        candidate_cycle=8,
    )
    assert score >= 0.0
    assert bd.institutional_merit_eligible is True


def test_explain_recommendation_nonexistent_mentor_returns_404():
    payload = {
        "mentee_email": "2022074255@upt.pe",
        "mentor_email": "mentor.fantasma.inexistente@upt.pe",
    }
    response = client.post("/api/v1/recommendations/explain", json=payload)
    assert response.status_code == 404
    assert "No se encontró el mentor" in response.json()["detail"]


def test_explain_recommendation_ineligible_mentor_returns_rejection_explanation():
    # estudiante.junior@upt.pe existe en mentores semilla pero tiene ciclo 4 (< 7)
    payload = {
        "mentee_email": "2022074255@upt.pe",
        "mentor_email": "estudiante.junior@upt.pe",
    }
    response = client.post("/api/v1/recommendations/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["target_type"] == "mentor"
    assert data["score_total"] == 0.0
    assert data["breakdown"]["institutional_merit_eligible"] is False
    assert "no elegible" in data["breakdown"]["explanation_text"].lower()


def test_get_candidate_mentors_empty_db_returns_empty_list_no_leak():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()
    try:
        # DB conectada pero sin ningún mentor registrado
        mentors = RecommendationService.get_candidate_mentors(db)
        assert len(mentors) == 0
    finally:
        db.close()
        engine.dispose()


# ==============================================================================
# Batería de Pruebas T-17 / T-19: Ordenamiento Determinista y Empates Top-k (ORD-01 a ORD-05)
# ==============================================================================


def test_ord_01_deterministic_tie_breaking_stability():
    """
    ORD-01: Desempate ante puntaje multifactorial idéntico (S_total).
    Aplica desempate determinista por mayor vacante disponible y menor timestamp de inicio.
    Verifica estabilidad idéntica en 10 iteraciones consecutivas.
    """
    from datetime import UTC, datetime, timedelta

    from app.services.booking_service import _memory_bookings, clear_bookings_in_memory
    from app.services.offer_service import _memory_offers

    clear_offers_in_memory()
    clear_bookings_in_memory()

    now = datetime.now(UTC)
    t1 = now + timedelta(days=3)

    # Sesión A: 10 cupos, 0 ocupados -> 10 disponibles, timestamp t1
    # Sesión B: 10 cupos, 5 ocupados -> 5 disponibles, timestamp t1
    # Ambas para la misma asignatura, tema y mentor (mismo puntaje base)
    _memory_offers.extend(
        [
            {
                "id_sesion": 101,
                "codigo_sesion": "SES-101",
                "mentor_email": "2022073504@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites",
                "fecha_inicio": t1.isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Laboratorio 101",
                "mentor_nombre": "Renzo Antonio Antayhua Mamani",
                "estado": "PUBLICADA",
            },
            {
                "id_sesion": 102,
                "codigo_sesion": "SES-102",
                "mentor_email": "2022073504@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites",
                "fecha_inicio": t1.isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Laboratorio 102",
                "mentor_nombre": "Renzo Antonio Antayhua Mamani",
                "estado": "PUBLICADA",
            },
        ]
    )

    # Simular 5 reservas en SES-102 para que tenga menor aforo disponible
    for i in range(5):
        _memory_bookings.append(
            {
                "id_reserva": 200 + i,
                "codigo_reserva": f"RES-{200 + i}",
                "id_sesion": 102,
                "estudiante_email": f"estudiante{i}@upt.pe",
                "estado": "CONFIRMADA",
            }
        )

    # Ejecutar 10 iteraciones y verificar estabilidad exacta del orden
    first_order = None
    for _ in range(10):
        recs = RecommendationService.recommend_offers(
            mentee_email="2022074255@upt.pe",
            top_k=5,
            db=None,
        )
        codes = [item.codigo_sesion for item in recs.items]
        if first_order is None:
            first_order = codes
            # SES-101 debe preceder a SES-102 por tener mayor vacante disponible (10 vs 5)
            assert codes[0] == "SES-101"
            assert codes[1] == "SES-102"
        else:
            assert codes == first_order


def test_ord_02_exclusion_of_sessions_under_24_hours_rn04():
    """
    ORD-02: Exclusión de sesiones con antelación <= 24 h (RN-04).
    Omitir automáticamente del feed toda sesión que haya entrado en la ventana de corte de quórum.
    """
    from datetime import UTC, datetime, timedelta

    from app.services.booking_service import clear_bookings_in_memory
    from app.services.offer_service import _memory_offers

    clear_offers_in_memory()
    clear_bookings_in_memory()

    now = datetime.now(UTC)
    t_vencida = now + timedelta(hours=12)  # Incompatible con RN-04
    t_valida = now + timedelta(hours=48)  # Válida

    _memory_offers.extend(
        [
            {
                "id_sesion": 201,
                "codigo_sesion": "SES-201-VENCIDA",
                "mentor_email": "2022073504@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites",
                "fecha_inicio": t_vencida.isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Aula 101",
                "mentor_nombre": "Renzo Antonio Antayhua Mamani",
                "estado": "PUBLICADA",
            },
            {
                "id_sesion": 202,
                "codigo_sesion": "SES-202-VALIDA",
                "mentor_email": "2022073504@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites",
                "fecha_inicio": t_valida.isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Aula 102",
                "mentor_nombre": "Renzo Antonio Antayhua Mamani",
                "estado": "PUBLICADA",
            },
        ]
    )

    recs = RecommendationService.recommend_offers(
        mentee_email="2022074255@upt.pe",
        top_k=5,
        db=None,
    )
    codes = [item.codigo_sesion for item in recs.items]
    assert "SES-202-VALIDA" in codes
    assert "SES-201-VENCIDA" not in codes
    assert len(recs.items) == 1


def test_ord_03_exclusion_of_sessions_with_zero_available_capacity():
    """
    ORD-03: Exclusión de sesiones con aforo agotado (Aforo_disp = 0).
    No incluir en el Top-k sesiones con 10/10 plazas ocupadas.
    """
    from datetime import UTC, datetime, timedelta

    from app.services.booking_service import _memory_bookings, clear_bookings_in_memory
    from app.services.offer_service import _memory_offers

    clear_offers_in_memory()
    clear_bookings_in_memory()

    now = datetime.now(UTC)
    t = now + timedelta(days=3)

    _memory_offers.append(
        {
            "id_sesion": 301,
            "codigo_sesion": "SES-301-LLENA",
            "mentor_email": "2022073504@upt.pe",
            "id_asignatura": 1,
            "codigo_asignatura": "CALC-101",
            "nombre_asignatura": "Cálculo I",
            "id_tema": 1,
            "nombre_tema": "Límites",
            "fecha_inicio": t.isoformat(),
            "duracion_minutos": 60,
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "espacio_asignado": "Laboratorio 101",
            "mentor_nombre": "Renzo Antonio Antayhua Mamani",
            "estado": "PUBLICADA",
        }
    )

    # Ocupar los 10 cupos
    for i in range(10):
        _memory_bookings.append(
            {
                "id_reserva": 300 + i,
                "codigo_reserva": f"RES-{300 + i}",
                "id_sesion": 301,
                "estudiante_email": f"alumno{i}@upt.pe",
                "estado": "PENDIENTE_CONFIRMACION",
            }
        )

    recs = RecommendationService.recommend_offers(
        mentee_email="2022074255@upt.pe",
        top_k=5,
        db=None,
    )
    assert len(recs.items) == 0


def test_ord_04_top_k_parameterizable_boundary():
    """
    ORD-04: Límite k parametrizable en query string (top_k=1, top_k=2).
    Retornar exactamente min(k, |Ofertas|) respetando el ordenamiento.
    """
    from datetime import UTC, datetime, timedelta

    from app.services.booking_service import clear_bookings_in_memory
    from app.services.offer_service import _memory_offers

    clear_offers_in_memory()
    clear_bookings_in_memory()

    now = datetime.now(UTC)
    for i in range(1, 6):
        _memory_offers.append(
            {
                "id_sesion": 400 + i,
                "codigo_sesion": f"SES-40{i}",
                "mentor_email": "2022073504@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites",
                "fecha_inicio": (now + timedelta(days=2 + i)).isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": f"Aula {i}",
                "mentor_nombre": "Renzo Antonio Antayhua Mamani",
                "estado": "PUBLICADA",
            }
        )

    r1 = client.get("/api/v1/recommendations/offers?top_k=1")
    assert r1.status_code == 200
    assert len(r1.json()["items"]) == 1

    r3 = client.get("/api/v1/recommendations/offers?top_k=3")
    assert r3.status_code == 200
    assert len(r3.json()["items"]) == 3


def test_ord_05_critical_course_multiplier_algo202_priority():
    """
    ORD-05: Aplicación del multiplicador 1.3x en Algoritmos y Estructuras de Datos.
    El score de la sesión sobrepasa a materias estándar aun con menor solapamiento horario.
    """
    # Comparar score de oferta en Algoritmos (ID 3, peso 1.3) vs Materia no crítica (peso 1.0)
    score_algo, bd_algo = RecommendationService.compute_candidate_score(
        mentee_courses=None,
        mentee_topics={9},
        mentee_slots=None,
        mentee_modality="presencial",
        candidate_courses={3},  # Algoritmos
        candidate_topics={9},
        candidate_slots=None,
        candidate_modality="presencial",
        candidate_cycle=8,
        offer_time=datetime.now(UTC) + timedelta(days=3),
    )

    score_standard, bd_standard = RecommendationService.compute_candidate_score(
        mentee_courses=None,
        mentee_topics={9},
        mentee_slots=None,
        mentee_modality="presencial",
        candidate_courses={99},  # Materia estándar sin factor
        candidate_topics={9},
        candidate_slots=None,
        candidate_modality="presencial",
        candidate_cycle=8,
        offer_time=datetime.now(UTC) + timedelta(days=3),
    )

    assert bd_algo.course_weight_factor == 1.3
    assert bd_algo.critical_course_applied == "ALGO-202"
    assert bd_standard.course_weight_factor == 1.0
    assert score_algo > score_standard
    assert round(score_algo, 2) == round(score_standard * 1.3, 2)


def test_ord_01_b_deterministic_tie_breaking_by_fecha_inicio():
    """
    ORD-01b: Desempate determinista por fecha_inicio (menor timestamp).
    Ante puntaje multifactorial y aforo disponible idénticos, la sesión con inicio más cercano precede.
    """
    from datetime import UTC, datetime, timedelta

    from app.services.booking_service import clear_bookings_in_memory
    from app.services.offer_service import _memory_offers

    clear_offers_in_memory()
    clear_bookings_in_memory()

    now = datetime.now(UTC)
    t_early = now + timedelta(days=2, hours=10)
    t_late = now + timedelta(days=5, hours=10)

    _memory_offers.extend(
        [
            {
                "id_sesion": 501,
                "codigo_sesion": "SES-501-LATE",
                "mentor_email": "2022073504@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites",
                "fecha_inicio": t_late.isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Aula 501",
                "mentor_nombre": "Renzo Antonio Antayhua Mamani",
                "estado": "PUBLICADA",
            },
            {
                "id_sesion": 502,
                "codigo_sesion": "SES-502-EARLY",
                "mentor_email": "2022073504@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites",
                "fecha_inicio": t_early.isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Aula 502",
                "mentor_nombre": "Renzo Antonio Antayhua Mamani",
                "estado": "PUBLICADA",
            },
        ]
    )

    recs = RecommendationService.recommend_offers("2022074255@upt.pe", top_k=5, db=None)
    codes = [item.codigo_sesion for item in recs.items]
    assert len(codes) == 2
    # La sesión más temprana debe aparecer primero
    assert codes[0] == "SES-502-EARLY"
    assert codes[1] == "SES-501-LATE"


def test_ord_01_c_deterministic_tie_breaking_by_codigo_sesion():
    """
    ORD-01c: Desempate determinista por codigo_sesion (orden lexicográfico canónico).
    Ante igualdad total en score, factor, aforo disponible y fecha de inicio.
    """
    from datetime import UTC, datetime, timedelta

    from app.services.booking_service import clear_bookings_in_memory
    from app.services.offer_service import _memory_offers

    clear_offers_in_memory()
    clear_bookings_in_memory()

    now = datetime.now(UTC)
    t_exact = now + timedelta(days=3)

    _memory_offers.extend(
        [
            {
                "id_sesion": 602,
                "codigo_sesion": "SES-Z-602",
                "mentor_email": "2022073504@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites",
                "fecha_inicio": t_exact.isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Aula 602",
                "mentor_nombre": "Renzo Antonio Antayhua Mamani",
                "estado": "PUBLICADA",
            },
            {
                "id_sesion": 601,
                "codigo_sesion": "SES-A-601",
                "mentor_email": "2022073504@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites",
                "fecha_inicio": t_exact.isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Aula 601",
                "mentor_nombre": "Renzo Antonio Antayhua Mamani",
                "estado": "PUBLICADA",
            },
        ]
    )

    recs = RecommendationService.recommend_offers("2022074255@upt.pe", top_k=5, db=None)
    codes = [item.codigo_sesion for item in recs.items]
    assert len(codes) == 2
    # SES-A-601 debe preceder lexicográficamente a SES-Z-602
    assert codes[0] == "SES-A-601"
    assert codes[1] == "SES-Z-602"


def test_ord_01_d_permutation_invariance_stability():
    """
    ORD-01d: Invarianza ante permutación del orden de entrada de candidatos en BD/memoria.
    El resultado del ranking es estrictamente determinista independientemente del orden en que se lean.
    """
    import random
    from datetime import UTC, datetime, timedelta

    from app.services.booking_service import clear_bookings_in_memory
    from app.services.offer_service import _memory_offers

    now = datetime.now(UTC)
    base_offers = [
        {
            "id_sesion": 700 + i,
            "codigo_sesion": f"SES-STABLE-{i:02d}",
            "mentor_email": "2022073504@upt.pe",
            "id_asignatura": 1,
            "codigo_asignatura": "CALC-101",
            "nombre_asignatura": "Cálculo I",
            "id_tema": 1,
            "nombre_tema": "Límites",
            "fecha_inicio": (now + timedelta(days=2, hours=i)).isoformat(),
            "duracion_minutos": 60,
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "espacio_asignado": f"Aula {i}",
            "mentor_nombre": "Renzo Antonio Antayhua Mamani",
            "estado": "PUBLICADA",
        }
        for i in range(1, 6)
    ]

    expected_order = None
    for _ in range(5):
        clear_offers_in_memory()
        clear_bookings_in_memory()
        shuffled = list(base_offers)
        random.shuffle(shuffled)
        _memory_offers.extend(shuffled)

        res = RecommendationService.recommend_offers("2022074255@upt.pe", top_k=5, db=None)
        order = [item.codigo_sesion for item in res.items]

        if expected_order is None:
            expected_order = order
        else:
            assert order == expected_order, f"Orden no determinista detectado: {order} != {expected_order}"
