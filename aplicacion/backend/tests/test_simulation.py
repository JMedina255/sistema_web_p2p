from fastapi.testclient import TestClient

from app.main import app
from app.services.simulation_service import SimulationService

client = TestClient(app)


def test_generate_synthetic_cohorts_validity():
    mentees, mentors = SimulationService.generate_synthetic_cohorts()
    assert len(mentees) >= 4
    assert len(mentors) >= 5

    # Validar que los mentoreados sean de ciclos tempranos (I a IV)
    for m in mentees:
        assert 1 <= m["ciclo_actual"] <= 4
        assert len(m["materias_interes"]) > 0
        assert len(m["temas_seleccionados"]) > 0

    # Validar que la cohorte de mentores incluya casos elegibles e inelegibles
    eligible_count = sum(1 for m in mentors if m["ciclo_actual"] >= 7)
    ineligible_count = sum(1 for m in mentors if m["ciclo_actual"] < 7)
    assert eligible_count >= 3
    assert ineligible_count >= 2


def test_evaluate_edge_cases_all_pass():
    edge_results = SimulationService.evaluate_edge_cases()
    assert "case_1_no_schedule_overlap" in edge_results
    assert "case_2_disjoint_topics" in edge_results
    assert "case_3_course_without_offers" in edge_results
    assert "case_4_ineligible_mentors_rn03" in edge_results

    # 1. Caso 1: Sin solapamiento
    c1 = edge_results["case_1_no_schedule_overlap"]
    assert c1["status"] == "PASSED"
    assert c1["schedule_matching_slots_count"] == 0
    assert c1["handled_gracefully"] is True

    # 2. Caso 2: Temas disjuntos
    c2 = edge_results["case_2_disjoint_topics"]
    assert c2["status"] == "PASSED"
    assert c2["jaccard"] == 0.0
    assert c2["handled_gracefully"] is True

    # 3. Caso 3: Asignatura sin oferta
    c3 = edge_results["case_3_course_without_offers"]
    assert c3["status"] == "PASSED"
    assert c3["recommendations_count"] == 0
    assert c3["handled_gracefully"] is True

    # 4. Caso 4: Mentores con ciclo < 7
    c4 = edge_results["case_4_ineligible_mentors_rn03"]
    assert c4["status"] == "PASSED"
    assert c4["leak_rate"] == 0.0
    assert c4["cycles_filtered_strictly"] == 6
    assert c4["handled_gracefully"] is True


def test_evaluate_deterministic_ordering():
    det_result = SimulationService.evaluate_deterministic_ordering(runs=5)
    assert det_result["is_deterministic"] is True
    assert det_result["total_runs"] == 5
    assert len(det_result["stable_top_k"]) > 0


def test_run_benchmark_metrics():
    bench = SimulationService.run_benchmark()
    assert bench["testbench_status"] == "SUCCESS"
    assert bench["evaluations_count"] > 0
    assert bench["total_elapsed_ms"] >= 0
    assert bench["determinism_verified"] is True
    assert bench["rn03_filter_leak_rate"] == 0.0


def test_simulation_testbench_endpoint():
    response = client.get("/api/v1/recommendations/simulation/testbench")
    assert response.status_code == 200
    data = response.json()
    assert data["testbench_status"] == "SUCCESS"
    assert data["determinism_verified"] is True
    assert "edge_cases" in data
