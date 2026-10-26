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
