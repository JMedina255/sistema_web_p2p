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


def test_curriculum_service_with_real_db_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from app.db.session import Base
    from app.models.curriculum import Asignatura, TemaConceptual
    from app.services.curriculum_service import CurriculumService

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    c1 = Asignatura(
        id_asignatura=1,
        codigo_curso="CALC-101",
        nombre_curso="Cálculo I",
        ciclo_plan=1,
        creditos=4,
        es_prioritaria=True,
        factor_ponderacion=1.2,
        estado_activo=True,
    )
    c2 = Asignatura(
        id_asignatura=2,
        codigo_curso="CALC-201",
        nombre_curso="Cálculo II",
        ciclo_plan=2,
        creditos=4,
        es_prioritaria=True,
        factor_ponderacion=1.2,
        estado_activo=True,
    )
    t1 = TemaConceptual(
        id_tema=1,
        id_asignatura=1,
        nombre_tema="Límites",
        descripcion_silabo="Límites y continuidad",
        unidad_silabica=1,
        estado_activo=True,
    )
    db.add_all([c1, c2, t1])
    db.commit()

    # Listado con sesión DB
    courses = CurriculumService.get_courses(db)
    assert len(courses) == 2
    assert isinstance(courses[0], Asignatura)

    # Filtrar por prioridad
    priority = CurriculumService.get_courses(db, only_priority=True)
    assert len(priority) == 2

    # Filtrar por ciclo
    ciclo2 = CurriculumService.get_courses(db, ciclo=2)
    assert len(ciclo2) == 1
    assert ciclo2[0].codigo_curso == "CALC-201"

    # Ciclo sin registros retorna lista vacía (no fallback ciego)
    ciclo5 = CurriculumService.get_courses(db, ciclo=5)
    assert len(ciclo5) == 0

    # Detalle con relación cargada
    detail = CurriculumService.get_course_by_id(db, 1)
    assert detail is not None
    assert len(detail.temas) == 1
    assert detail.temas[0].nombre_tema == "Límites"

    # Detalle no encontrado
    assert CurriculumService.get_course_by_id(db, 999) is None

    # Temas de curso
    topics = CurriculumService.get_course_topics(db, 1)
    assert len(topics) == 1
    assert topics[0].nombre_tema == "Límites"

    db.close()
    engine.dispose()
