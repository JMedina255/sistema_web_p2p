from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_courses_returns_5_filter_courses():
    response = client.get("/api/v1/curriculum/courses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5

    course_names = [c["nombre_curso"] for c in data]
    assert "Cálculo I" in course_names
    assert "Cálculo II" in course_names
    assert "Algoritmos y Estructuras de Datos" in course_names
    assert "Programación Orientada a Objetos" in course_names
    assert "Base de Datos" in course_names


def test_list_courses_filter_only_priority():
    response = client.get("/api/v1/curriculum/courses?only_priority=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
    for course in data:
        assert course["es_prioritaria"] is True


def test_list_courses_filter_by_ciclo():
    response = client.get("/api/v1/curriculum/courses?ciclo=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    codigos = [c["codigo_curso"] for c in data]
    assert "CALC-201" in codigos
    assert "ALGO-202" in codigos


def test_get_course_detail_success():
    response = client.get("/api/v1/curriculum/courses/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id_asignatura"] == 1
    assert data["nombre_curso"] == "Cálculo I"
    assert "temas" in data
    assert len(data["temas"]) >= 3
    tema_nombres = [t["nombre_tema"] for t in data["temas"]]
    assert any("Límites" in n for n in tema_nombres)


def test_get_course_detail_not_found():
    response = client.get("/api/v1/curriculum/courses/999")
    assert response.status_code == 404
    assert "no encontrada" in response.json()["detail"].lower()


def test_get_course_topics_success():
    response = client.get("/api/v1/curriculum/courses/3/topics")
    assert response.status_code == 200
    topics = response.json()
    assert isinstance(topics, list)
    assert len(topics) >= 4
    topic_names = [t["nombre_tema"] for t in topics]
    assert any("Punteros" in t for t in topic_names)
    assert any("Recursividad" in t for t in topic_names)


def test_get_course_topics_not_found():
    response = client.get("/api/v1/curriculum/courses/999/topics")
    assert response.status_code == 404
