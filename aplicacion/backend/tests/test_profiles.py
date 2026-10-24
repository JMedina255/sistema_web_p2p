from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.main import app
from app.models.profile import DisponibilidadHoraria, PerfilAcademico
from app.schemas.profile import AcademicProfileUpdate, AvailabilitySlotSchema
from app.services.profile_service import ProfileService

client = TestClient(app)


def test_get_profile_default():
    email = "2022074255@upt.pe"
    response = client.get(f"/api/v1/profiles/me?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["codigo_estudiante"] == "2022074255"
    assert data["nombres"] == "Joan Cristian"
    assert data["ciclo_actual"] == 6


def test_update_profile_success():
    email = "2022074255@upt.pe"
    payload = {
        "email": email,
        "codigo_estudiante": "2022074255",
        "nombres": "Joan Cristian",
        "apellidos": "Medina Quispe",
        "ciclo_actual": 6,
        "rol_postulacion": "mentoreado",
        "materias_interes": [1, 2, 3],
        "temas_seleccionados": [1, 5, 8],
        "biografia": "Estudiante de 6to ciclo enfocado en Algoritmos y POO.",
        "modalidad_preferida": "virtual",
    }
    response = client.put("/api/v1/profiles/me", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["modalidad_preferida"] == "virtual"
    assert data["materias_interes"] == [1, 2, 3]
    assert data["updated_at"] is not None


def test_update_profile_rejects_mentor_when_cycle_below_7():
    email = "2022074255@upt.pe"
    payload = {
        "email": email,
        "ciclo_actual": 6,
        "rol_postulacion": "mentor",  # Intento indebido de mentoría con ciclo 6
        "materias_interes": [1],
        "temas_seleccionados": [1],
    }
    response = client.put("/api/v1/profiles/me", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "MERIT_RULE_VIOLATION" in str(data)


def test_update_profile_allows_mentor_when_cycle_gte_7():
    email = "2022073504@upt.pe"
    payload = {
        "email": email,
        "codigo_estudiante": "2022073504",
        "nombres": "Renzo Antonio",
        "apellidos": "Antayhua Mamani",
        "ciclo_actual": 7,
        "rol_postulacion": "mentor",
        "materias_interes": [3, 4],
        "temas_seleccionados": [7, 8],
        "modalidad_preferida": "hibrida",
    }
    response = client.put("/api/v1/profiles/me", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["rol_postulacion"] == "mentor"
    assert data["ciclo_actual"] == 7


def test_get_and_update_availability():
    email = "2022074255@upt.pe"

    # 1. Consulta inicial
    res_get = client.get(f"/api/v1/profiles/availability?email={email}")
    assert res_get.status_code == 200
    data_get = res_get.json()
    assert data_get["email"] == email
    assert "slots" in data_get

    # 2. Reemplazo de bloques semanales
    new_slots = [
        {"dia_semana": 1, "hora_inicio": "08:00", "hora_fin": "09:00"},
        {"dia_semana": 2, "hora_inicio": "10:00", "hora_fin": "11:00"},
        {"dia_semana": 5, "hora_inicio": "16:00", "hora_fin": "17:00"},
    ]
    payload = {"email": email, "slots": new_slots}
    res_put = client.put("/api/v1/profiles/availability", json=payload)
    assert res_put.status_code == 200
    data_put = res_put.json()
    assert data_put["success"] is True
    assert data_put["totalSlots"] == 3

    # 3. Comprobar que los nuevos slots se leen correctamente
    res_get_updated = client.get(f"/api/v1/profiles/availability?email={email}")
    assert res_get_updated.status_code == 200
    assert len(res_get_updated.json()["slots"]) == 3


def test_profile_service_with_real_db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    email = "2020019999@upt.pe"

    # 1. Perfil por defecto
    default_p = ProfileService.get_profile(db, email)
    assert default_p.email == email
    assert default_p.ciclo_actual == 3

    # 2. Actualización exitosa en BD
    up_payload = AcademicProfileUpdate(
        email=email,
        codigo_estudiante="2020019999",
        nombres="Carlos",
        apellidos="Perez",
        ciclo_actual=8,
        rol_postulacion="mentor",
        materias_interes=[1, 5],
        temas_seleccionados=[2, 4],
        biografia="Mentor voluntario de bases de datos",
        modalidad_preferida="hibrida",
    )
    saved = ProfileService.update_profile(db, email, up_payload)
    assert saved.ciclo_actual == 8
    assert saved.rol_postulacion == "mentor"

    # Verificar en BD
    db_entity = db.query(PerfilAcademico).filter(PerfilAcademico.email == email).first()
    assert db_entity is not None
    assert db_entity.biografia == "Mentor voluntario de bases de datos"
    assert db_entity.ciclo_actual == 8

    # 3. Disponibilidad horaria en BD
    slots_input = [
        AvailabilitySlotSchema(dia_semana=1, hora_inicio="09:00", hora_fin="10:00"),
        AvailabilitySlotSchema(dia_semana=3, hora_inicio="11:00", hora_fin="12:00"),
    ]
    res_avail = ProfileService.update_availability(db, email, slots_input)
    assert res_avail["success"] is True
    assert res_avail["totalSlots"] == 2

    # Verificar filas en BD
    db_slots = (
        db.query(DisponibilidadHoraria)
        .filter(DisponibilidadHoraria.email == email)
        .order_by(DisponibilidadHoraria.dia_semana)
        .all()
    )
    assert len(db_slots) == 2
    assert db_slots[0].hora_inicio == "09:00"

    # Consulta por servicio
    queried_slots = ProfileService.get_availability(db, email)
    assert len(queried_slots) == 2
    assert queried_slots[1].dia_semana == 3

    db.close()
    engine.dispose()


def test_profile_cycle_boundary_validations():
    email = "2022074255@upt.pe"

    # Ciclo 0 inválido (< 1)
    res_zero = client.put(
        "/api/v1/profiles/me",
        json={"email": email, "ciclo_actual": 0, "rol_postulacion": "mentoreado"},
    )
    assert res_zero.status_code == 422

    # Ciclo 11 inválido (> 10)
    res_eleven = client.put(
        "/api/v1/profiles/me",
        json={"email": email, "ciclo_actual": 11, "rol_postulacion": "mentoreado"},
    )
    assert res_eleven.status_code == 422

    # Ciclo 1 y 10 válidos (límites superior e inferior)
    res_one = client.put(
        "/api/v1/profiles/me",
        json={"email": email, "ciclo_actual": 1, "rol_postulacion": "mentoreado"},
    )
    assert res_one.status_code == 200
    assert res_one.json()["ciclo_actual"] == 1

    res_ten = client.put(
        "/api/v1/profiles/me",
        json={"email": email, "ciclo_actual": 10, "rol_postulacion": "mentor"},
    )
    assert res_ten.status_code == 200
    assert res_ten.json()["ciclo_actual"] == 10


def test_availability_boundary_and_empty_slots():
    email = "2022074255@upt.pe"

    # Día inválido (0 o 7)
    res_day0 = client.put(
        "/api/v1/profiles/availability",
        json={"email": email, "slots": [{"dia_semana": 0, "hora_inicio": "08:00", "hora_fin": "09:00"}]},
    )
    assert res_day0.status_code == 422

    res_day7 = client.put(
        "/api/v1/profiles/availability",
        json={"email": email, "slots": [{"dia_semana": 7, "hora_inicio": "08:00", "hora_fin": "09:00"}]},
    )
    assert res_day7.status_code == 422

    # Formato de hora inválido
    res_bad_time = client.put(
        "/api/v1/profiles/availability",
        json={"email": email, "slots": [{"dia_semana": 1, "hora_inicio": "8:00", "hora_fin": "9:00"}]},
    )
    assert res_bad_time.status_code == 422

    # Limpiar agenda (array vacío de slots)
    res_empty = client.put(
        "/api/v1/profiles/availability",
        json={"email": email, "slots": []},
    )
    assert res_empty.status_code == 200
    assert res_empty.json()["totalSlots"] == 0


def test_availability_time_order_and_invalid_24h():
    email = "2022074255@upt.pe"

    # 1. hora_inicio >= hora_fin ("14:00" a "13:00")
    res_inverted = client.put(
        "/api/v1/profiles/availability",
        json={"email": email, "slots": [{"dia_semana": 1, "hora_inicio": "14:00", "hora_fin": "13:00"}]},
    )
    assert res_inverted.status_code == 422
    assert "estrictamente anterior" in res_inverted.text

    # 2. hora_inicio == hora_fin ("10:00" a "10:00")
    res_equal = client.put(
        "/api/v1/profiles/availability",
        json={"email": email, "slots": [{"dia_semana": 1, "hora_inicio": "10:00", "hora_fin": "10:00"}]},
    )
    assert res_equal.status_code == 422

    # 3. Horas 24h fuera de rango ("25:00" o "14:99")
    res_bad_hour = client.put(
        "/api/v1/profiles/availability",
        json={"email": email, "slots": [{"dia_semana": 1, "hora_inicio": "25:00", "hora_fin": "09:00"}]},
    )
    assert res_bad_hour.status_code == 422


def test_availability_duplicate_and_overlapping_slots():
    email = "2022074255@upt.pe"

    # 1. Slots duplicados en el mismo día
    res_dup = client.put(
        "/api/v1/profiles/availability",
        json={
            "email": email,
            "slots": [
                {"dia_semana": 2, "hora_inicio": "08:00", "hora_fin": "09:00"},
                {"dia_semana": 2, "hora_inicio": "08:00", "hora_fin": "09:00"},
            ],
        },
    )
    assert res_dup.status_code == 422
    assert "duplicada" in res_dup.text

    # 2. Slots solapados en el mismo día (08:00-10:00 y 09:00-11:00)
    res_overlap = client.put(
        "/api/v1/profiles/availability",
        json={
            "email": email,
            "slots": [
                {"dia_semana": 3, "hora_inicio": "08:00", "hora_fin": "10:00"},
                {"dia_semana": 3, "hora_inicio": "09:00", "hora_fin": "11:00"},
            ],
        },
    )
    assert res_overlap.status_code == 422
    assert "solapadas" in res_overlap.text


def test_profile_invalid_enum_fields_rejected():
    email = "2022074255@upt.pe"

    # rol_postulacion inválido
    res_bad_role = client.put(
        "/api/v1/profiles/me",
        json={"email": email, "ciclo_actual": 5, "rol_postulacion": "invalido"},
    )
    assert res_bad_role.status_code == 422

    # modalidad_preferida inválida
    res_bad_mod = client.put(
        "/api/v1/profiles/me",
        json={"email": email, "ciclo_actual": 5, "modalidad_preferida": "astral"},
    )
    assert res_bad_mod.status_code == 422
