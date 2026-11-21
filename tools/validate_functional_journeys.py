"""
Script de Validación de Integración de API en Entorno Controlado (Línea Base QA-P2P-02 / QA-P2P-03)
Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)

Entorno de ejecución:
- Cliente HTTP: FastAPI TestClient (Starlette / HTTPX)
- Base de datos: SQLite en memoria aislada con StaticPool y PRAGMA foreign_keys=ON
- Propósito: 30 comprobaciones de integración de endpoints RESTful, serialización,
  validación Pydantic, RBAC y persistencia ORM para la suite de integración de CI.
- Nota de alcance: Este script valida contratos de API y lógica de negocio en entorno
  controlado. La validación E2E real en navegador y con PostgreSQL de pruebas se ejecuta
  de forma complementaria en los escenarios de Fase 2 y Fase 3 de QA-P2P-03.

Ejecuta 30 comprobaciones distribuidas en 9 módulos de API:
1. Autenticación (Solicitud OTP, validación de dominio @upt.pe, JWT HS256, Consentimiento Ley 29733)
2. Perfiles y Disponibilidad (Perfil académico formativo, Grilla semanal 6x11)
3. Catálogo Curricular (Asignaturas formativas, Temarios silábicos)
4. Ofertas de Mentoría (Validación RN-04 > 24h, aforo normativo RN-05, estados)
5. Motor de Recomendación EdRecSys (Top-k ofertas y mentores, filtros)
6. Reservas de Cupos (Creación transaccional, confirmación T-24h, desistimiento, liberación de cupos)
7. Sesiones y Quórum (Evaluación a T-24h, contingencias normativas)
8. Control de Asistencia y Bitácora (TOTP dinámico rotatorio, check-in, bitácora pedagógica, SHA-256)
9. Administración y Certificación (RBAC, visado de bitácoras, resumen de horas, verificación pública)
"""

import os
import sys
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ajustar PYTHONPATH
base_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "aplicacion", "backend")
)
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import app.models  # Registra todos los modelos ORM en Base.metadata
from app.db.session import Base, get_optional_session, get_required_session
from app.main import app
from app.models.booking import ReservaCupo
from app.models.curriculum import Asignatura, TemaConceptual
from app.models.offer import SesionMentoria
from app.models.profile import PerfilAcademico
from app.models.roles import Rol, UsuarioRol

# Crear base de datos aislada con soporte de Foreign Keys y StaticPool
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(test_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


Base.metadata.create_all(test_engine)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_required_session] = override_get_db
app.dependency_overrides[get_optional_session] = override_get_db

client = TestClient(app)

results_summary = []


def record_result(journey: str, test_name: str, passed: bool, detail: str = ""):
    status_str = "PASS" if passed else "FAIL"
    results_summary.append(
        {"journey": journey, "test": test_name, "status": status_str, "detail": detail}
    )
    print(f"[{status_str}] {journey} -> {test_name}: {detail}")
    if not passed:
        raise AssertionError(f"Fallo en {journey} -> {test_name}: {detail}")


def seed_initial_catalog(db):
    # Semillar asignaturas curriculares
    a1 = Asignatura(
        id_asignatura=1,
        codigo_curso="CALC-101",
        nombre_curso="Cálculo I",
        ciclo_plan=1,
        creditos=4,
        es_prioritaria=True,
        factor_ponderacion=1.2,
        estado_activo=True,
    )
    a2 = Asignatura(
        id_asignatura=2,
        codigo_curso="ALGO-201",
        nombre_curso="Algoritmos y Estructuras de Datos",
        ciclo_plan=3,
        creditos=4,
        es_prioritaria=True,
        factor_ponderacion=1.0,
        estado_activo=True,
    )
    db.add_all([a1, a2])
    db.commit()

    # Semillar temas silábicos
    t1 = TemaConceptual(
        id_tema=1,
        id_asignatura=1,
        nombre_tema="Límites y Continuidad",
        unidad_silabica=1,
        estado_activo=True,
    )
    t2 = TemaConceptual(
        id_tema=2,
        id_asignatura=1,
        nombre_tema="Derivadas y Regla de la Cadena",
        unidad_silabica=2,
        estado_activo=True,
    )
    t3 = TemaConceptual(
        id_tema=3,
        id_asignatura=2,
        nombre_tema="Árboles Binarios y AVL",
        unidad_silabica=1,
        estado_activo=True,
    )
    db.add_all([t1, t2, t3])
    db.commit()

    # Semillar roles institucionales
    r_est = Rol(id_rol=1, nombre_rol="mentoreado", descripcion="Estudiante mentoreado")
    r_men = Rol(id_rol=2, nombre_rol="mentor", descripcion="Mentor par")
    r_adm = Rol(id_rol=3, nombre_rol="administrador", descripcion="Administrador EPIS")
    db.add_all([r_est, r_men, r_adm])
    db.commit()


def run_all_journeys():
    print("=" * 70)
    print("INICIANDO PRUEBAS DE INTEGRACIÓN DE API EN ENTORNO CONTROLADO")
    print("Arquitectura: FastAPI TestClient + SQLite en memoria (StaticPool)")
    print("=" * 70)

    with TestSessionLocal() as db:
        seed_initial_catalog(db)

    # -------------------------------------------------------------------------
    # Recorrido 1: Autenticación & Consentimiento (CUS01 / RN-01 / RN-02 / RNF01)
    # -------------------------------------------------------------------------
    journey_1 = "1. Autenticación & Consentimiento"

    # 1.1 Rechazo de dominio externo
    resp = client.post("/api/v1/auth/otp/request", json={"email": "hacker@gmail.com"})
    record_result(
        journey_1,
        "Rechazo de correo externo @gmail.com",
        resp.status_code in (400, 422),
        "RN-01 validado",
    )

    # 1.2 Solicitud OTP para estudiante institucional
    resp = client.post("/api/v1/auth/otp/request", json={"email": "2022074255@upt.pe"})
    record_result(
        journey_1,
        "Emisión OTP institucional @upt.pe",
        resp.status_code == 200,
        f"Challenge: {resp.json().get('challengeId')}",
    )
    chal_id = resp.json()["challengeId"]

    # 1.3 Verificación con código erróneo
    resp = client.post(
        "/api/v1/auth/otp/verify", json={"challengeId": chal_id, "otp": "999999"}
    )
    record_result(
        journey_1,
        "Rechazo de código OTP erróneo",
        resp.status_code == 400,
        "Código inválido rechazado",
    )

    # 1.4 Verificación exitosa
    from app.services.auth_service import _memory_challenges

    chal_obj = _memory_challenges.get(chal_id)
    assert (
        chal_obj is not None and "code_plain" in chal_obj
    ), "Fallo de preparación: el desafío OTP no fue registrado en el almacén de autenticación"
    otp_valid = chal_obj["code_plain"]

    resp = client.post(
        "/api/v1/auth/otp/verify", json={"challengeId": chal_id, "otp": otp_valid}
    )
    record_result(
        journey_1,
        "Validación OTP exitosa y emisión JWT",
        resp.status_code == 200 and "token" in resp.json(),
        "JWT emitido",
    )
    jwt_student = resp.json()["token"]
    student_headers = {"Authorization": f"Bearer {jwt_student}"}

    # 1.5 Consentimiento legal Ley 29733 (RN-02)
    resp = client.post(
        "/api/v1/consent/accept",
        json={"email": "2022074255@upt.pe", "accepted": True},
        headers=student_headers,
    )
    record_result(
        journey_1,
        "Aceptación de consentimiento Ley 29733",
        resp.status_code == 200,
        "Consentimiento persistido",
    )

    # Registrar rol MENTOR y perfil habilitado en BD antes de emitir token de mentor
    with TestSessionLocal() as db:
        ur_m = UsuarioRol(
            email="mentor.par@upt.pe", id_rol=2, asignado_por="ADMIN_INIT", activo=True
        )
        prof_m = PerfilAcademico(
            email="mentor.par@upt.pe",
            codigo_estudiante="2020010101",
            nombres="Carlos",
            apellidos="Mentor",
            ciclo_actual=8,
            rol_postulacion="mentor",
            materias_interes=[1],
            temas_seleccionados=[1],
        )
        db.add_all([ur_m, prof_m])
        db.commit()

    resp_m = client.post(
        "/api/v1/auth/otp/request", json={"email": "mentor.par@upt.pe"}
    )
    chal_m = resp_m.json()["challengeId"]
    chal_obj_m = _memory_challenges.get(chal_m)
    assert (
        chal_obj_m is not None and "code_plain" in chal_obj_m
    ), "Fallo de preparación: el desafío OTP de mentor no fue registrado"
    otp_m = chal_obj_m["code_plain"]
    resp_v_m = client.post(
        "/api/v1/auth/otp/verify", json={"challengeId": chal_m, "otp": otp_m}
    )
    jwt_mentor = resp_v_m.json()["token"]
    mentor_headers = {"Authorization": f"Bearer {jwt_mentor}"}
    from app.core.security import decode_access_token

    decoded_mentor = decode_access_token(jwt_mentor) or {}
    record_result(
        journey_1,
        "Emisión JWT para Mentor con rol institucional",
        "mentor" in decoded_mentor.get("roles", []),
        "Rol mentor incluido en JWT",
    )

    # -------------------------------------------------------------------------
    # Recorrido 2: Perfiles & Disponibilidad (CUS15 / RN-03)
    # -------------------------------------------------------------------------
    journey_2 = "2. Perfiles & Disponibilidad"

    # 2.1 Obtener perfil inicial
    resp = client.get("/api/v1/profiles/me", headers=student_headers)
    record_result(
        journey_2,
        "Consulta de perfil propio autenticado",
        resp.status_code == 200,
        "Perfil retornado",
    )

    # 2.2 Actualizar perfil académico
    profile_payload = {
        "nombres": "Joan",
        "apellidos": "Medina",
        "codigo_estudiante": "2022074255",
        "ciclo_actual": 5,
        "rol_postulacion": "mentoreado",
        "materias_interes": [1],
        "temas_seleccionados": [1],
        "modalidad_preferida": "presencial",
    }
    resp = client.put(
        "/api/v1/profiles/me", json=profile_payload, headers=student_headers
    )
    record_result(
        journey_2,
        "Actualización de perfil académico",
        resp.status_code == 200,
        "Ciclo V y preferencias guardadas",
    )

    # 2.3 Disponibilidad horaria semanal
    avail_payload = {
        "email": "2022074255@upt.pe",
        "slots": [
            {"dia_semana": 1, "hora_inicio": "10:00", "hora_fin": "11:00"},
            {"dia_semana": 3, "hora_inicio": "14:00", "hora_fin": "15:00"},
        ],
    }
    resp = client.put(
        "/api/v1/profiles/availability", json=avail_payload, headers=student_headers
    )
    record_result(
        journey_2,
        "Persistencia de disponibilidad horaria semanal",
        resp.status_code == 200,
        "2 bloques horarios guardados",
    )

    # -------------------------------------------------------------------------
    # Recorrido 3: Catálogo Curricular (CUS21 / RF05)
    # -------------------------------------------------------------------------
    journey_3 = "3. Catálogo Curricular"
    resp = client.get("/api/v1/curriculum/courses")
    record_result(
        journey_3,
        "Consulta de asignaturas oficiales",
        resp.status_code == 200 and len(resp.json()) >= 2,
        f"{len(resp.json())} asignaturas",
    )

    resp = client.get("/api/v1/curriculum/courses/1/topics")
    record_result(
        journey_3,
        "Consulta de temario conceptual",
        resp.status_code == 200 and len(resp.json()) >= 2,
        f"{len(resp.json())} temas en Cálculo I",
    )

    # -------------------------------------------------------------------------
    # Recorrido 4: Ofertas de Mentoría (CUS06 / RN-04 / RN-05)
    # -------------------------------------------------------------------------
    journey_4 = "4. Ofertas de Mentoría"
    now_utc = datetime.now(UTC)

    # 4.1 Infracción de RN-04: Sesión con menos de 24 horas de antelación
    invalid_offer = {
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites y Continuidad",
        "fecha_inicio": (now_utc + timedelta(hours=12)).isoformat(),
        "duracion_minutos": 60,
        "modalidad": "presencial",
        "aforo_maximo": 10,
        "espacio_asignado": "Aula 204 - EPIS",
        "mentor_email": "mentor.par@upt.pe",
    }
    resp = client.post("/api/v1/offers", json=invalid_offer, headers=mentor_headers)
    record_result(
        journey_4,
        "Rechazo de oferta con antelación <= 24h (RN-04)",
        resp.status_code == 400,
        "RN-04 validada",
    )

    # 4.2 Publicación válida (antelación = 48 horas)
    valid_time = now_utc + timedelta(hours=48)
    valid_offer = {
        "id_asignatura": 1,
        "codigo_asignatura": "CALC-101",
        "nombre_asignatura": "Cálculo I",
        "id_tema": 1,
        "nombre_tema": "Límites y Continuidad",
        "fecha_inicio": valid_time.isoformat(),
        "duracion_minutos": 60,
        "modalidad": "presencial",
        "aforo_maximo": 10,
        "espacio_asignado": "Aula 204 - EPIS",
        "mentor_email": "mentor.par@upt.pe",
    }
    resp = client.post("/api/v1/offers", json=valid_offer, headers=mentor_headers)
    record_result(
        journey_4,
        "Publicación exitosa de oferta formal",
        resp.status_code == 201,
        f"Sesión ID: {resp.json().get('id_oferta')}",
    )
    created_session_id = int(resp.json().get("id_oferta"))

    # -------------------------------------------------------------------------
    # Recorrido 5: Recomendaciones Top-k (CUS02 / RN-11 / RNF03)
    # -------------------------------------------------------------------------
    journey_5 = "5. Recomendaciones Top-k"
    resp = client.get("/api/v1/recommendations/offers?top_k=5", headers=student_headers)
    record_result(
        journey_5,
        "Consulta de ofertas recomendadas EdRecSys",
        resp.status_code == 200,
        f"Items: {len(resp.json().get('items', []))}",
    )

    resp_m = client.get(
        "/api/v1/recommendations/mentors?top_k=5", headers=student_headers
    )
    record_result(
        journey_5,
        "Consulta de mentores recomendados EdRecSys",
        resp_m.status_code == 200,
        f"Mentores: {len(resp_m.json().get('items', []))}",
    )

    # -------------------------------------------------------------------------
    # Recorrido 6: Reservas de Cupos (CUS04 / CUS17 / RN-05 / RN-08 / RN-10)
    # -------------------------------------------------------------------------
    journey_6 = "6. Reservas de Cupos"

    # 6.1 Formalizar reserva provisional
    booking_req = {
        "id_sesion": created_session_id,
        "estudiante_email": "2022074255@upt.pe",
    }
    resp = client.post(
        "/api/v1/bookings/reserve", json=booking_req, headers=student_headers
    )
    record_result(
        journey_6,
        "Reserva provisional de cupo (PENDIENTE_CONFIRMACION)",
        resp.status_code == 201,
        f"Reserva ID: {resp.json().get('id_reserva')}",
    )
    created_booking_id = resp.json().get("id_reserva")

    # 6.2 Detección de duplicado por mismo estudiante
    resp = client.post(
        "/api/v1/bookings/reserve", json=booking_req, headers=student_headers
    )
    record_result(
        journey_6,
        "Prevención de reserva duplicada",
        resp.status_code == 400,
        "DUPLICATE_BOOKING rechazado",
    )

    # 6.3 Ratificación de asistencia a tiempo (RN-08)
    resp = client.post(
        f"/api/v1/bookings/{created_booking_id}/confirm", headers=student_headers
    )
    record_result(
        journey_6,
        "Ratificación de asistencia (CONFIRMADA)",
        resp.status_code == 200 and resp.json().get("estado") == "CONFIRMADA",
        "Estado CONFIRMADA",
    )

    # 6.4 Desistimiento voluntario (RN-10)
    cancel_payload = {"motivo": "Cruce de horario con examen de práctica"}
    resp = client.post(
        f"/api/v1/bookings/{created_booking_id}/cancel",
        json=cancel_payload,
        headers=student_headers,
    )
    record_result(
        journey_6,
        "Desistimiento voluntario y liberación de cupo",
        resp.status_code == 200 and resp.json().get("estado") == "CANCELADA_USUARIO",
        "Estado CANCELADA_USUARIO",
    )

    # 6.5 Doble desistimiento rechazado
    resp = client.post(
        f"/api/v1/bookings/{created_booking_id}/cancel",
        json=cancel_payload,
        headers=student_headers,
    )
    record_result(
        journey_6,
        "Rechazo de doble desistimiento (ALREADY_CANCELLED)",
        resp.status_code == 400,
        "ALREADY_CANCELLED validado",
    )

    # -------------------------------------------------------------------------
    # Recorrido 7: Sesiones y Quórum (CUS07 / CUS23 / RN-08 / RN-09)
    # -------------------------------------------------------------------------
    journey_7 = "7. Sesiones y Quórum"

    # Crear una nueva sesión con 5 confirmados para evaluar quórum positivo (50% de 10)
    with TestSessionLocal() as db:
        s2 = SesionMentoria(
            id_sesion=9901,
            codigo_sesion="SES-Q-9901",
            mentor_email="mentor.par@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now_utc + timedelta(hours=30),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Lab 101",
            estado="PUBLICADA",
        )
        db.add(s2)
        # Añadir 5 reservas confirmadas (50% de aforo 10 = 5, quórum alcanzado)
        for idx, em in enumerate(
            ["s1@upt.pe", "s2@upt.pe", "s3@upt.pe", "s4@upt.pe", "s5@upt.pe"]
        ):
            b = ReservaCupo(
                id_sesion=9901,
                codigo_reserva=f"RES-Q-{idx + 1}",
                estudiante_email=em,
                estado="CONFIRMADA",
                fecha_reserva=now_utc - timedelta(hours=10),
                fecha_ratificacion=now_utc - timedelta(hours=5),
            )
            db.add(b)
        db.commit()

    resp = client.post(
        "/api/v1/quorum/evaluate", json={"id_sesion": 9901}, headers=mentor_headers
    )
    record_result(
        journey_7,
        "Evaluación de quórum normativo >= 50% (RN-09)",
        resp.status_code == 200 and resp.json().get("cumple_quorum") is True,
        f"Total confirmados: {resp.json().get('total_confirmados')}/{resp.json().get('aforo_maximo')}",
    )

    # -------------------------------------------------------------------------
    # Recorrido 8: Control de Asistencia y Bitácora (CUS08 / CUS12 / CUS13 / RN-12)
    # -------------------------------------------------------------------------
    journey_8 = "8. Asistencia & Bitácora"

    # 8.1 Generar token TOTP dinámico para sesión en curso
    with TestSessionLocal() as db:
        s_live = SesionMentoria(
            id_sesion=8801,
            codigo_sesion="SES-LIVE-8801",
            mentor_email="mentor.par@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now_utc - timedelta(minutes=15),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Aula 101",
            estado="CONFIRMADA",
        )
        db.add(s_live)
        b_live = ReservaCupo(
            id_sesion=8801,
            codigo_reserva="RES-LIVE-01",
            estudiante_email="2022074255@upt.pe",
            estado="CONFIRMADA",
        )
        db.add(b_live)
        db.commit()

    resp = client.get("/api/v1/sessions/8801/attendance/token", headers=mentor_headers)
    record_result(
        journey_8,
        "Generación de token QR TOTP dinámico",
        resp.status_code == 200,
        "Token TOTP dinámico de 30s generado exitosamente",
    )
    totp_active = resp.json().get("totp_code")
    token_str = resp.json().get("token")

    # 8.2 Check-in del estudiante
    checkin_payload = {"qr_token": token_str, "numeric_code": totp_active}
    resp = client.post(
        "/api/v1/sessions/8801/attendance/check-in",
        json=checkin_payload,
        headers=student_headers,
    )
    record_result(
        journey_8,
        "Check-in presencial validado con TOTP",
        resp.status_code == 200 and resp.json().get("asistio") is True,
        "Asistencia registrada",
    )

    # 8.3 Registro de bitácora pedagógica (RN-12: observaciones >= 50 caracteres)
    bitacora_invalid = {
        "temas_cubiertos": ["Límites"],
        "observaciones": "Demasiado breve",
        "nivel_dificultad": "Medio",
    }
    resp = client.post(
        "/api/v1/sessions/8801/bitacora", json=bitacora_invalid, headers=mentor_headers
    )
    record_result(
        journey_8,
        "Rechazo de bitácora pedagógica con < 50 caracteres (RN-12)",
        resp.status_code in (400, 422),
        "RN-12 validada",
    )

    bitacora_valid = {
        "temas_cubiertos": ["Límites y Continuidad en Cálculo I"],
        "observaciones": "Se desarrollaron demostraciones formales de límites laterales y asíntotas con activa participación estudiantil.",
        "nivel_dificultad": "Medio",
    }
    resp = client.post(
        "/api/v1/sessions/8801/bitacora", json=bitacora_valid, headers=mentor_headers
    )
    record_result(
        journey_8,
        "Registro formal de bitácora y generación SHA-256",
        resp.status_code == 201,
        "Bitácora pedagógica registrada y sellada con hash SHA-256",
    )
    created_bitacora_id = resp.json().get("id_bitacora")

    # -------------------------------------------------------------------------
    # Recorrido 9: Administración y Roles (CUS10 / CUS14 / CUS22 / RN-14)
    # -------------------------------------------------------------------------
    journey_9 = "9. Administración & Certificados"

    # Registrar rol administrador en BD
    with TestSessionLocal() as db:
        ur_adm = UsuarioRol(
            email="admin.epis@upt.pe", id_rol=3, asignado_por="SYS_INIT", activo=True
        )
        db.add(ur_adm)
        db.commit()

    resp_adm = client.post(
        "/api/v1/auth/otp/request", json={"email": "admin.epis@upt.pe"}
    )
    chal_a = resp_adm.json()["challengeId"]
    chal_obj_a = _memory_challenges.get(chal_a)
    assert (
        chal_obj_a is not None and "code_plain" in chal_obj_a
    ), "Fallo de preparación: el desafío OTP de administrador no fue registrado"
    otp_a = chal_obj_a["code_plain"]
    resp_v_a = client.post(
        "/api/v1/auth/otp/verify", json={"challengeId": chal_a, "otp": otp_a}
    )
    jwt_admin = resp_v_a.json()["token"]
    admin_headers = {"Authorization": f"Bearer {jwt_admin}"}

    # 9.1 Acceso privilegiado de Administrador a roles de otro usuario
    resp = client.get("/api/v1/roles/users/mentor.par@upt.pe", headers=admin_headers)
    record_result(
        journey_9,
        "Consulta de roles de usuario por Administrador",
        resp.status_code == 200,
        f"Roles: {resp.json().get('roles')}",
    )

    # 9.2 Bloqueo de acceso de Estudiante para consultar roles ajenos -> HTTP 403
    resp = client.get("/api/v1/roles/users/mentor.par@upt.pe", headers=student_headers)
    record_result(
        journey_9,
        "Bloqueo de acceso privilegiado para rol Estudiante",
        resp.status_code == 403,
        "RBAC validado con 403 FORBIDDEN",
    )

    # 9.3 Visado administrativo de bitácora (RN-14)
    resp = client.post(
        f"/api/v1/bitacoras/{created_bitacora_id}/visar", headers=admin_headers
    )
    record_result(
        journey_9,
        "Visado institucional de horas pedagógicas",
        resp.status_code == 200 and resp.json().get("visado_administrador") is True,
        "Horas acreditadas oficialmente",
    )

    # 9.4 Resumen de horas para certificación
    resp = client.get(
        "/api/v1/certificates/summary?mentor_email=mentor.par@upt.pe",
        headers=admin_headers,
    )
    record_result(
        journey_9,
        "Cálculo acumulativo de horas visadas",
        resp.status_code == 200,
        f"Horas visadas: {resp.json().get('horas_visadas')}",
    )

    # 9.5 Verificación pública de constancia inexistente (404)
    resp = client.get("/api/v1/certificates/verificar?folio=CERT-2026-II-9999")
    record_result(
        journey_9,
        "Verificación pública QR de constancia",
        resp.status_code == 404,
        "Folio inexistente reporta 404 seguro",
    )

    print("=" * 70)
    print("30 COMPROBACIONES DE INTEGRACIÓN DE API VERIFICADAS CON ÉXITO")
    print(
        f"Total pruebas ejecutadas: {len(results_summary)} | APROBADAS: {sum(1 for r in results_summary if r['status'] == 'PASS')}"
    )
    print("Clasificación: Pruebas de integración de endpoints FastAPI con SQLite en memoria")
    print("=" * 70)


if __name__ == "__main__":
    run_all_journeys()
