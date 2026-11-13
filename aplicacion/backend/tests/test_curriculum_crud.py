import pytest
from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.main import app

client = TestClient(app)


def get_admin_headers() -> dict[str, str]:
    token = create_access_token(data={"sub": "admin.curriculum@upt.pe", "roles": ["administrador"]})
    return {"Authorization": f"Bearer {token}"}


def get_student_headers() -> dict[str, str]:
    token = create_access_token(data={"sub": "estudiante@upt.pe", "roles": ["mentoreado"]})
    return {"Authorization": f"Bearer {token}"}


def test_create_course_as_admin():
    headers = get_admin_headers()
    payload = {
        "codigo_curso": "TEST-101",
        "nombre_curso": "Materia de Prueba Automatizada",
        "ciclo_plan": 3,
        "creditos": 4,
        "es_prioritaria": True,
        "factor_ponderacion": 1.3,
        "estado_activo": True,
    }
    response = client.post("/api/v1/curriculum/courses", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["codigo_curso"] == "TEST-101"
    assert data["nombre_curso"] == "Materia de Prueba Automatizada"


def test_create_course_forbidden_for_non_admin():
    headers = get_student_headers()
    payload = {
        "codigo_curso": "HACK-999",
        "nombre_curso": "Curso No Autorizado",
        "ciclo_plan": 1,
        "creditos": 3,
    }
    response = client.post("/api/v1/curriculum/courses", json=payload, headers=headers)
    assert response.status_code == 403


def test_update_course_as_admin():
    headers = get_admin_headers()
    # Update existing course (id 1)
    payload = {
        "nombre_curso": "Cálculo Diferencial e Integral I",
        "factor_ponderacion": 1.4,
    }
    response = client.put("/api/v1/curriculum/courses/1", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["factor_ponderacion"] == 1.4


def test_create_and_update_and_delete_topic_as_admin():
    headers = get_admin_headers()
    # 1. Create topic for course 1
    t_payload = {
        "nombre_tema": "Sucesiones y Progresiones Aritméticas",
        "descripcion_silabo": "Estudio analítico de progresiones aritméticas y geométricas en R.",
        "unidad_silabica": 1,
        "estado_activo": True,
    }
    res_t = client.post("/api/v1/curriculum/courses/1/topics", json=t_payload, headers=headers)
    assert res_t.status_code == 201
    topic_data = res_t.json()
    topic_id = topic_data["id_tema"]
    assert topic_data["nombre_tema"] == "Sucesiones y Progresiones Aritméticas"

    # 2. Update topic
    up_res = client.put(
        f"/api/v1/curriculum/topics/{topic_id}",
        json={"nombre_tema": "Sucesiones y Progresiones en R"},
        headers=headers,
    )
    assert up_res.status_code == 200
    assert up_res.json()["nombre_tema"] == "Sucesiones y Progresiones en R"

    # 3. Delete topic
    del_res = client.delete(f"/api/v1/curriculum/topics/{topic_id}", headers=headers)
    assert del_res.status_code == 200
    assert del_res.json()["id_tema"] == topic_id


def test_delete_course_as_admin():
    headers = get_admin_headers()
    # Delete / deactivate course 1
    response = client.delete("/api/v1/curriculum/courses/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["id_asignatura"] == 1
