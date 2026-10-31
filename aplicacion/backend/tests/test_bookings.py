import concurrent.futures
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import create_access_token
from app.db.session import Base
from app.main import app
from app.models.booking import ReservaCupo
from app.models.curriculum import Asignatura, TemaConceptual
from app.models.offer import SesionMentoria
from app.schemas.booking import BookingCreatePayload, MentoringDemandPayload
from app.services.booking_service import (
    BookingService,
    _memory_bookings,
    clear_bookings_in_memory,
)
from app.services.offer_service import (
    _memory_offers,
    clear_offers_in_memory,
    seed_default_offers_in_memory,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_teardown_bookings():
    clear_offers_in_memory()
    seed_default_offers_in_memory()
    clear_bookings_in_memory()
    yield
    clear_offers_in_memory()
    clear_bookings_in_memory()


def test_reserve_seat_success_in_memory():
    """Valida la formalización de una reserva provisional exitosa en memoria (201 Created)."""
    payload = {
        "id_sesion": 1,
        "estudiante_email": "2024071111@upt.pe",
    }
    response = client.post("/api/v1/bookings/reserve", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["estado"] == "PENDIENTE_CONFIRMACION"
    assert data["codigo_reserva"].startswith("RES-")
    assert data["id_sesion"] == 1
    assert data["estudiante_email"] == "2024071111@upt.pe"
    assert data["ticket_hash"] is not None
    assert len(data["ticket_hash"]) == 64
    assert "T-24h" in data["mensaje"]


def test_reserve_seat_success_in_real_db():
    """Valida la formalización transaccional de una reserva en base de datos real con claves foráneas."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    try:
        # 1. Sembrar Asignatura y Tema
        asig = Asignatura(
            id_asignatura=1,
            codigo_curso="CALC-101",
            nombre_curso="Cálculo I",
            ciclo_plan=1,
            creditos=4,
            factor_ponderacion=1.2,
        )
        tema = TemaConceptual(id_tema=1, id_asignatura=1, nombre_tema="Límites", unidad_silabica=1)
        db.add_all([asig, tema])

        # 2. Sembrar Sesion de Mentoría
        now = datetime.now(UTC)
        sesion = SesionMentoria(
            id_sesion=10,
            codigo_sesion="SES-10",
            mentor_email="mentor.titular@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now + timedelta(days=3),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Laboratorio 101",
            estado="PUBLICADA",
        )
        db.add(sesion)
        db.commit()

        # 3. Reservar cupo
        payload = BookingCreatePayload(
            id_sesion=10,
            estudiante_email="2024072222@upt.pe",
        )
        res = BookingService.reserve_seat(db=db, payload=payload)
        assert res.id_reserva is not None
        assert res.codigo_reserva.startswith("RES-")
        assert res.estado == "PENDIENTE_CONFIRMACION"
        assert res.id_sesion == 10

        # Verificar persistencia en DB
        persisted = db.query(ReservaCupo).filter(ReservaCupo.id_reserva == res.id_reserva).first()
        assert persisted is not None
        assert persisted.estudiante_email == "2024072222@upt.pe"
        assert persisted.estado == "PENDIENTE_CONFIRMACION"
    finally:
        db.close()
        engine.dispose()


def test_reserve_seat_rejects_nonexistent_session_404():
    """Valida rechazo HTTP 404 ante ID de sesión inexistente."""
    payload = {
        "id_sesion": 99999,
        "estudiante_email": "2024071111@upt.pe",
    }
    response = client.post("/api/v1/bookings/reserve", json=payload)
    assert response.status_code == 404
    assert "SESSION_NOT_FOUND" in response.json()["detail"]


def test_reserve_seat_rejects_session_not_published_400():
    """Valida rechazo HTTP 400 si la sesión no se encuentra en estado PUBLICADA."""
    _memory_offers.append(
        {
            "id_sesion": 50,
            "codigo_sesion": "SES-50",
            "mentor_email": "mentor.titular@upt.pe",
            "id_asignatura": 1,
            "codigo_asignatura": "CALC-101",
            "nombre_asignatura": "Cálculo I",
            "id_tema": 1,
            "nombre_tema": "Límites",
            "fecha_inicio": (datetime.now(UTC) + timedelta(days=3)).isoformat(),
            "duracion_minutos": 60,
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "espacio_asignado": "Aula 101",
            "estado": "CONFIRMADA",  # No PUBLICADA
        }
    )
    payload = {
        "id_sesion": 50,
        "estudiante_email": "2024071111@upt.pe",
    }
    response = client.post("/api/v1/bookings/reserve", json=payload)
    assert response.status_code == 400
    assert "SESSION_NOT_OPEN" in response.json()["detail"]


def test_reserve_seat_rejects_antelation_under_24_hours_rn04():
    """Valida rechazo HTTP 400 por infracción de RN-04 (ventana de corte T-24h)."""
    _memory_offers.append(
        {
            "id_sesion": 60,
            "codigo_sesion": "SES-60",
            "mentor_email": "mentor.titular@upt.pe",
            "id_asignatura": 1,
            "codigo_asignatura": "CALC-101",
            "nombre_asignatura": "Cálculo I",
            "id_tema": 1,
            "nombre_tema": "Límites",
            "fecha_inicio": (datetime.now(UTC) + timedelta(hours=10)).isoformat(),  # < 24 h
            "duracion_minutos": 60,
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "espacio_asignado": "Aula 101",
            "estado": "PUBLICADA",
        }
    )
    payload = {
        "id_sesion": 60,
        "estudiante_email": "2024071111@upt.pe",
    }
    response = client.post("/api/v1/bookings/reserve", json=payload)
    assert response.status_code == 400
    assert "WINDOW_CLOSED_T24H" in response.json()["detail"]


def test_reserve_seat_rejects_mentor_booking_own_session_400():
    """Valida que el mentor titular no pueda autoreservar un cupo en su clase."""
    # SES-1001 tiene como mentor a 2022073504@upt.pe
    payload = {
        "id_sesion": 1,
        "estudiante_email": "2022073504@upt.pe",
    }
    response = client.post("/api/v1/bookings/reserve", json=payload)
    assert response.status_code == 400
    assert "MENTOR_CANNOT_BOOK" in response.json()["detail"]


def test_reserve_seat_rejects_duplicate_active_booking_400():
    """Valida que un estudiante no pueda registrar dos reservas activas sobre la misma sesión."""
    payload = {
        "id_sesion": 1,
        "estudiante_email": "2024073333@upt.pe",
    }
    # Primera reserva -> éxito 201
    r1 = client.post("/api/v1/bookings/reserve", json=payload)
    assert r1.status_code == 201

    # Segunda reserva idéntica -> rechazo 400
    r2 = client.post("/api/v1/bookings/reserve", json=payload)
    assert r2.status_code == 400
    assert "DUPLICATE_BOOKING" in r2.json()["detail"]


def test_reserve_seat_rejects_capacity_exceeded_409():
    """Valida rechazo HTTP 409 cuando se alcanza el aforo reglamentario (RN-05 / RNF07)."""
    # Llenar la sesión 1 (aforo 10) con 10 reservas
    for i in range(10):
        _memory_bookings.append(
            {
                "id_reserva": 700 + i,
                "codigo_reserva": f"RES-{700 + i}",
                "id_sesion": 1,
                "estudiante_email": f"alumno{i}@upt.pe",
                "estado": "CONFIRMADA",
            }
        )

    # Intento de reserva 11
    payload = {
        "id_sesion": 1,
        "estudiante_email": "alumno.excedente@upt.pe",
    }
    response = client.post("/api/v1/bookings/reserve", json=payload)
    assert response.status_code == 409
    assert "CAPACITY_EXCEEDED" in response.json()["detail"]


def test_reserve_seat_with_bearer_jwt_authorization():
    """Valida la autorización por token JWT Bearer al reservar."""
    student_email = "2024075555@upt.pe"
    student_token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})

    # 1. Reserva exitosa con su propio token
    payload = {
        "id_sesion": 1,
        "estudiante_email": student_email,
    }
    r_ok = client.post(
        "/api/v1/bookings/reserve",
        headers={"Authorization": f"Bearer {student_token}"},
        json=payload,
    )
    assert r_ok.status_code == 201

    # 2. Intento de reservar a nombre de otro estudiante con token de mentoreado -> 403
    payload_other = {
        "id_sesion": 1,
        "estudiante_email": "otro.alumno@upt.pe",
    }
    r_forbidden = client.post(
        "/api/v1/bookings/reserve",
        headers={"Authorization": f"Bearer {student_token}"},
        json=payload_other,
    )
    assert r_forbidden.status_code == 403

    # 3. Intento a nombre de otro con token de administrador -> 201
    admin_token = create_access_token({"sub": "admin.epis@upt.pe", "roles": ["administrador"]})
    r_admin = client.post(
        "/api/v1/bookings/reserve",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=payload_other,
    )
    assert r_admin.status_code == 201


def test_get_my_reservations_endpoint():
    """Valida la consulta de nómina de reservas del mentoreado."""
    email = "2024076666@upt.pe"
    token = create_access_token({"sub": email, "roles": ["mentoreado"]})

    # Reservar
    client.post("/api/v1/bookings/reserve", json={"id_sesion": 1, "estudiante_email": email})

    # Consultar
    res = client.get(
        "/api/v1/bookings/my-reservations",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    items = res.json()
    assert len(items) >= 1
    assert items[0]["estudiante_email"] == email
    assert items[0]["estado"] == "PENDIENTE_CONFIRMACION"


def test_get_session_reservations_mentor_access():
    """Valida que el mentor titular pueda inspeccionar los inscritos en su clase."""
    mentor_email = "2022073504@upt.pe"
    mentor_token = create_access_token({"sub": mentor_email, "roles": ["mentor"]})

    # Registrar reserva de un alumno
    client.post("/api/v1/bookings/reserve", json={"id_sesion": 1, "estudiante_email": "2024077777@upt.pe"})

    res = client.get(
        "/api/v1/bookings/session/1",
        headers={"Authorization": f"Bearer {mentor_token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1


def test_create_and_get_demand_requests_cus03():
    """Valida el registro y consulta de solicitudes temáticas por demanda (CUS03 / RF07)."""
    student_email = "2024078888@upt.pe"
    token = create_access_token({"sub": student_email, "roles": ["mentoreado"]})

    payload = {
        "id_asignatura": 3,
        "id_tema": 9,
        "notas": "Requiero reforzamiento intensivo en Notación Big-O",
    }

    # Registrar demanda
    r_post = client.post(
        "/api/v1/bookings/requests",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert r_post.status_code == 201
    d_created = r_post.json()
    assert d_created["id_asignatura"] == 3
    assert d_created["id_tema"] == 9
    assert d_created["estado"] == "PENDIENTE"
    assert d_created["estudiante_email"] == student_email

    # Consultar demandas
    r_get = client.get("/api/v1/bookings/requests?id_asignatura=3")
    assert r_get.status_code == 200
    demands = r_get.json()
    assert len(demands) >= 1
    assert any(d["id_tema"] == 9 for d in demands)


def test_quorum_evaluation_below_50_percent():
    """Valida evaluación de quórum insuficiente (< 50% según RN-09)."""
    # Sesión 1 tiene aforo 10. Sembrar 2 reservas confirmadas (20% < 50%)
    for i in range(2):
        _memory_bookings.append(
            {
                "id_reserva": 800 + i,
                "codigo_reserva": f"RES-{800 + i}",
                "id_sesion": 1,
                "estudiante_email": f"est{i}@upt.pe",
                "estado": "CONFIRMADA",
            }
        )

    res = client.post("/api/v1/quorum/evaluate", json={"id_sesion": 1})
    assert res.status_code == 200
    data = res.json()
    assert data["cumple_quorum"] is False
    assert data["porcentaje_quorum"] == 20.0
    assert data["reservas_confirmadas"] == 2


def test_quorum_evaluation_at_or_above_50_percent():
    """Valida evaluación de quórum reglamentario alcanzado (>= 50% según RN-09)."""
    # Sembrar 5 reservas confirmadas de 10 (50%)
    for i in range(5):
        _memory_bookings.append(
            {
                "id_reserva": 850 + i,
                "codigo_reserva": f"RES-{850 + i}",
                "id_sesion": 1,
                "estudiante_email": f"conf{i}@upt.pe",
                "estado": "CONFIRMADA",
            }
        )

    res = client.post("/api/v1/quorum/evaluate", json={"id_sesion": 1})
    assert res.status_code == 200
    data = res.json()
    assert data["cumple_quorum"] is True
    assert data["porcentaje_quorum"] == 50.0
    assert data["reservas_confirmadas"] == 5


def test_quorum_evaluation_t24h_transitions_unconfirmed_to_no_confirmada():
    """Valida que a T-24h las reservas provisionales no ratificadas caduquen a NO_CONFIRMADA (RN-08)."""
    # Crear sesión con antelación menor a 24 horas (ej. 12 horas)
    now = datetime.now(UTC)
    _memory_offers.append(
        {
            "id_sesion": 90,
            "codigo_sesion": "SES-90",
            "mentor_email": "mentor.titular@upt.pe",
            "id_asignatura": 1,
            "codigo_asignatura": "CALC-101",
            "nombre_asignatura": "Cálculo I",
            "id_tema": 1,
            "nombre_tema": "Límites",
            "fecha_inicio": (now + timedelta(hours=12)).isoformat(),  # Cruzó corte T-24h
            "duracion_minutos": 60,
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "espacio_asignado": "Aula 101",
            "estado": "PUBLICADA",
        }
    )
    _memory_bookings.append(
        {
            "id_reserva": 901,
            "codigo_reserva": "RES-901",
            "id_sesion": 90,
            "estudiante_email": "est.moroso@upt.pe",
            "estado": "PENDIENTE_CONFIRMACION",
        }
    )

    res = client.post("/api/v1/quorum/evaluate", json={"id_sesion": 90})
    assert res.status_code == 200

    # Verificar que mutó a NO_CONFIRMADA
    b_mutada = next(b for b in _memory_bookings if b["id_reserva"] == 901)
    assert b_mutada["estado"] == "NO_CONFIRMADA"
    assert "RN-08" in b_mutada["motivo_cancelacion"]


# ==============================================================================
# Suite de Concurrencia Multihilo (RNF07 / Prevención Absoluta de Sobrecupo)
# ==============================================================================


def test_concurrent_multithreaded_booking_pessimistic_lock_rnf07():
    """
    RNF07 / T-24: Control de Concurrencia Transaccional Multihilo.
    20 hilos simultáneos disputan la ÚLTIMA plaza vacante disponible (9/10 cupos ocupados).
    Criterio de Aceptación:
    - Exactamente 1 solicitud obtiene confirmación exitosa HTTP 201 Created.
    - Exactamente 19 solicitudes reciben HTTP 409 Conflict (CAPACITY_EXCEEDED).
    - El aforo final ocupado es estrictamente 10/10 (Tasa de sobrecupo: exactamente 0.0%).
    """
    clear_offers_in_memory()
    clear_bookings_in_memory()

    now = datetime.now(UTC)
    sesion_id = 1
    aforo_max = 10

    # Crear oferta con 10 plazas
    _memory_offers.append(
        {
            "id_sesion": sesion_id,
            "codigo_sesion": "SES-CONCURRENCY-1",
            "mentor_email": "2022073504@upt.pe",
            "id_asignatura": 1,
            "codigo_asignatura": "CALC-101",
            "nombre_asignatura": "Cálculo I",
            "id_tema": 1,
            "nombre_tema": "Límites",
            "fecha_inicio": (now + timedelta(days=3)).isoformat(),
            "duracion_minutos": 60,
            "modalidad": "presencial",
            "aforo_maximo": aforo_max,
            "espacio_asignado": "Laboratorio 101",
            "mentor_nombre": "Renzo Antonio Antayhua Mamani",
            "estado": "PUBLICADA",
        }
    )

    # Pre-ocupar 9 cupos (queda exactamente 1 vacante)
    for i in range(9):
        _memory_bookings.append(
            {
                "id_reserva": 1000 + i,
                "codigo_reserva": f"RES-{1000 + i}",
                "id_sesion": sesion_id,
                "estudiante_email": f"estudiante_base_{i}@upt.pe",
                "estado": "CONFIRMADA",
            }
        )

    # Preparar 20 peticiones concurrentes de estudiantes distintos
    total_threads = 20
    status_codes = []

    def make_booking_request(thread_idx: int) -> int:
        payload = {
            "id_sesion": sesion_id,
            "estudiante_email": f"concurrente_{thread_idx}@upt.pe",
        }
        res = client.post("/api/v1/bookings/reserve", json=payload)
        return res.status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=total_threads) as executor:
        futures = [executor.submit(make_booking_request, i) for i in range(total_threads)]
        for f in concurrent.futures.as_completed(futures):
            status_codes.append(f.result())

    # Aserciones de verificación formal RNF07
    success_count = status_codes.count(201)
    conflict_count = status_codes.count(409)

    assert success_count == 1, f"Se esperaba exactamente 1 éxito, pero hubo {success_count}"
    assert conflict_count == 19, f"Se esperaban exactamente 19 rechazos HTTP 409, pero hubo {conflict_count}"

    # Validar que el total de ocupados no sobrepasó el aforo máximo de 10
    active_total = sum(
        1
        for b in _memory_bookings
        if b["id_sesion"] == sesion_id and b["estado"] in ["PENDIENTE_CONFIRMACION", "CONFIRMADA"]
    )
    assert active_total == aforo_max, f"Aforo sobrepasado: {active_total} > {aforo_max}"


def test_concurrent_multithreaded_booking_real_db_rnf07():
    """
    RNF07 / T-24: Prueba de Concurrencia Multihilo sobre Base de Datos Real.
    Verifica que el coordinador BookingService mantenga consistencia ACID estricta
    bajo ráfagas concurrentes de hilos sobre persistencia relacional.
    """
    from sqlalchemy.pool import StaticPool

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    try:
        now = datetime.now(UTC)
        asig = Asignatura(
            id_asignatura=1,
            codigo_curso="CALC-101",
            nombre_curso="Cálculo I",
            ciclo_plan=1,
            creditos=4,
            factor_ponderacion=1.2,
        )
        tema = TemaConceptual(id_tema=1, id_asignatura=1, nombre_tema="Límites", unidad_silabica=1)
        db.add_all([asig, tema])

        sesion = SesionMentoria(
            id_sesion=99,
            codigo_sesion="SES-CONC-DB-99",
            mentor_email="mentor.db@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now + timedelta(days=3),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Laboratorio 101",
            estado="PUBLICADA",
        )
        db.add(sesion)
        db.commit()

        # Pre-ocupar 9 cupos
        for i in range(9):
            res_prev = ReservaCupo(
                codigo_reserva=f"RES-DB-{i}",
                id_sesion=99,
                estudiante_email=f"base_db_{i}@upt.pe",
                estado="CONFIRMADA",
                fecha_reserva=now,
            )
            db.add(res_prev)
        db.commit()

        # Lanzar 20 hilos disputando la última plaza sobre la base de datos
        results = []

        def worker(idx: int):
            worker_db = session_factory()
            try:
                p = BookingCreatePayload(id_sesion=99, estudiante_email=f"aspirante_{idx}@upt.pe")
                BookingService.reserve_seat(db=worker_db, payload=p)
                return 201
            except Exception as e:
                if hasattr(e, "status_code"):
                    return e.status_code
                return 500
            finally:
                worker_db.close()

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(worker, i) for i in range(20)]
            for f in concurrent.futures.as_completed(futures):
                results.append(f.result())

        assert results.count(201) == 1
        assert results.count(409) == 19

        final_count = (
            db.query(ReservaCupo)
            .filter(
                ReservaCupo.id_sesion == 99, ReservaCupo.estado.in_(["PENDIENTE_CONFIRMACION", "CONFIRMADA"])
            )
            .count()
        )
        assert final_count == 10
    finally:
        db.close()
        engine.dispose()


def test_db_backed_student_and_session_reservations():
    """Valida consultas filtradas de reservas de estudiante y mentor en base de datos real."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    try:
        now = datetime.now(UTC)
        asig = Asignatura(
            id_asignatura=1,
            codigo_curso="CALC-101",
            nombre_curso="Cálculo I",
            ciclo_plan=1,
            creditos=4,
            factor_ponderacion=1.2,
        )
        tema = TemaConceptual(id_tema=1, id_asignatura=1, nombre_tema="Límites", unidad_silabica=1)
        sesion1 = SesionMentoria(
            id_sesion=1,
            codigo_sesion="SES-01",
            mentor_email="mentor.titular@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now + timedelta(days=3),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Lab 101",
            estado="PUBLICADA",
        )
        sesion2 = SesionMentoria(
            id_sesion=2,
            codigo_sesion="SES-02",
            mentor_email="mentor.titular@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now + timedelta(days=4),
            duracion_minutos=60,
            modalidad="virtual",
            aforo_maximo=20,
            espacio_asignado="https://meet.google.com/test",
            estado="PUBLICADA",
        )
        db.add_all([asig, tema, sesion1, sesion2])
        db.commit()

        # Crear reservas en DB (alumno1 en sesión 1 y 2; alumno2 en sesión 1)
        r1 = ReservaCupo(
            codigo_reserva="RES-101",
            id_sesion=1,
            estudiante_email="alumno1@upt.pe",
            estado="CONFIRMADA",
            fecha_reserva=now,
        )
        r2 = ReservaCupo(
            codigo_reserva="RES-102",
            id_sesion=2,
            estudiante_email="alumno1@upt.pe",
            estado="CANCELADA_USUARIO",
            fecha_reserva=now - timedelta(days=1),
        )
        r3 = ReservaCupo(
            codigo_reserva="RES-103",
            id_sesion=1,
            estudiante_email="alumno2@upt.pe",
            estado="CONFIRMADA",
            fecha_reserva=now,
        )
        db.add_all([r1, r2, r3])
        db.commit()

        # 1. Consultar reservas del estudiante
        all_res = BookingService.get_student_reservations(db, "alumno1@upt.pe")
        assert len(all_res) == 2

        confirmed_only = BookingService.get_student_reservations(db, "alumno1@upt.pe", estado="CONFIRMADA")
        assert len(confirmed_only) == 1
        assert confirmed_only[0].codigo_reserva == "RES-101"

        # 2. Consultar nómina de la sesión por el mentor
        mentor_view = BookingService.get_session_reservations(db, 1, caller_email="mentor.titular@upt.pe")
        assert len(mentor_view) == 2

        # 3. Consultar por admin
        admin_view = BookingService.get_session_reservations(db, 1, caller_email="admin.epis@upt.pe")
        assert len(admin_view) == 2

        # 4. Intento por estudiante no autorizado -> 403
        with pytest.raises(Exception) as exc_info:
            BookingService.get_session_reservations(db, 1, caller_email="alumno1@upt.pe")
        assert exc_info.value.status_code == 403

        # 5. Sesión inexistente -> 404
        with pytest.raises(Exception) as exc_404:
            BookingService.get_session_reservations(db, 9999)
        assert exc_404.value.status_code == 404
    finally:
        db.close()
        engine.dispose()


def test_db_backed_demand_requests_and_filters():
    """Valida registro y filtrado de solicitudes por demanda en base de datos real."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    try:
        asig = Asignatura(
            id_asignatura=3,
            codigo_curso="ALGO-202",
            nombre_curso="Algoritmos y Estructuras de Datos",
            ciclo_plan=3,
            creditos=4,
            factor_ponderacion=1.3,
        )
        tema = TemaConceptual(id_tema=9, id_asignatura=3, nombre_tema="Notación Big-O", unidad_silabica=1)
        db.add_all([asig, tema])
        db.commit()

        p = MentoringDemandPayload(id_asignatura=3, id_tema=9, notas="Demanda DB test")
        res = BookingService.create_demand_request(db, p, "estudiante.demanda@upt.pe")
        assert res.id_demanda is not None
        assert res.nombre_asignatura == "Algoritmos y Estructuras de Datos"
        assert res.nombre_tema == "Notación Big-O"

        # Consultar demandas filtrando por ciclo
        demands_c3 = BookingService.get_demand_requests(db, id_asignatura=3, ciclo=3)
        assert len(demands_c3) == 1

        demands_c5 = BookingService.get_demand_requests(db, id_asignatura=3, ciclo=5)
        assert len(demands_c5) == 0
    finally:
        db.close()
        engine.dispose()


def test_db_backed_quorum_evaluation():
    """Valida la evaluación de quórum (RN-08/RN-09) en base de datos real."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    try:
        now = datetime.now(UTC)
        asig = Asignatura(
            id_asignatura=1,
            codigo_curso="CALC-101",
            nombre_curso="Cálculo I",
            ciclo_plan=1,
            creditos=4,
            factor_ponderacion=1.2,
        )
        tema = TemaConceptual(id_tema=1, id_asignatura=1, nombre_tema="Límites", unidad_silabica=1)
        # Sesión programada en 10 horas (cruzó ventana T-24h)
        sesion = SesionMentoria(
            id_sesion=1,
            codigo_sesion="SES-QUORUM-1",
            mentor_email="mentor@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now + timedelta(hours=10),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Lab 101",
            estado="PUBLICADA",
        )
        db.add_all([asig, tema, sesion])
        db.commit()

        # Sembrar 6 reservas confirmadas y 2 provisionales
        for i in range(6):
            db.add(
                ReservaCupo(
                    codigo_reserva=f"RES-C-{i}",
                    id_sesion=1,
                    estudiante_email=f"conf_{i}@upt.pe",
                    estado="CONFIRMADA",
                    fecha_reserva=now - timedelta(days=1),
                )
            )
        for i in range(2):
            db.add(
                ReservaCupo(
                    codigo_reserva=f"RES-P-{i}",
                    id_sesion=1,
                    estudiante_email=f"prov_{i}@upt.pe",
                    estado="PENDIENTE_CONFIRMACION",
                    fecha_reserva=now - timedelta(days=1),
                )
            )
        db.commit()

        # Evaluar quórum
        q_res = BookingService.evaluate_quorum(db, 1)
        assert q_res.cumple_quorum is True
        assert q_res.porcentaje_quorum == 60.0
        assert q_res.reservas_confirmadas == 6

        # Verificar que las provisionales caducaron a NO_CONFIRMADA
        caducadas = (
            db.query(ReservaCupo)
            .filter(ReservaCupo.id_sesion == 1, ReservaCupo.estado == "NO_CONFIRMADA")
            .count()
        )
        assert caducadas == 2

        # Verificar error si sesión no existe
        with pytest.raises(Exception) as exc_404:
            BookingService.evaluate_quorum(db, 9999)
        assert exc_404.value.status_code == 404
    finally:
        db.close()
        engine.dispose()


def test_reserve_seat_rejects_without_consent_403():
    """Valida rechazo HTTP 403 cuando el estudiante no ha otorgado consentimiento de datos (RN-02)."""
    payload = {
        "id_sesion": 1,
        "estudiante_email": "sin_consentimiento@upt.pe",
    }
    response = client.post("/api/v1/bookings/reserve", json=payload)
    assert response.status_code == 403
    assert "CONSENT_REQUIRED" in response.json()["detail"]


def test_reserve_seat_database_busy_503():
    """Valida rechazo HTTP 503 DATABASE_BUSY cuando el candado de concurrencia no se adquiere en el timeout."""
    import threading

    from app.services.booking_service import _booking_lock

    # Bloquear el lock deliberadamente desde otro hilo
    block_event = threading.Event()
    release_event = threading.Event()

    def lock_holder():
        with _booking_lock:
            block_event.set()
            release_event.wait(timeout=2.0)

    t = threading.Thread(target=lock_holder, daemon=True)
    t.start()
    block_event.wait()

    try:
        payload = {
            "id_sesion": 1,
            "estudiante_email": "estudiante.bloqueado@upt.pe",
        }
        # Intentar reservar con timeout temporalmente reducido para test rápido
        from app.core.config import settings

        orig_timeout = settings.BOOKING_TIMEOUT_SECONDS
        settings.BOOKING_TIMEOUT_SECONDS = 0.05
        try:
            res = client.post("/api/v1/bookings/reserve", json=payload)
            assert res.status_code == 503
            assert "DATABASE_BUSY" in res.json()["detail"]
        finally:
            settings.BOOKING_TIMEOUT_SECONDS = orig_timeout
    finally:
        release_event.set()
        t.join()


def test_get_my_reservations_unauthenticated_rejects_401():
    """Valida que invocar /my-reservations sin autorización devuelva HTTP 401 Unauthorized."""
    res = client.get("/api/v1/bookings/my-reservations")
    assert res.status_code == 401


def test_get_session_reservations_unauthorized_rejects_401_and_403():
    """Valida rechazos de seguridad 401 y 403 en consulta de participantes de sesión."""
    # 1. Sin cabecera -> 401
    r_unauth = client.get("/api/v1/bookings/session/1")
    assert r_unauth.status_code == 401

    # 2. Con token de otro estudiante no mentor -> 403
    other_token = create_access_token({"sub": "estudiante.ajeno@upt.pe", "roles": ["mentoreado"]})
    r_forbidden = client.get(
        "/api/v1/bookings/session/1",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert r_forbidden.status_code == 403


def test_create_demand_request_nonexistent_subject_or_topic_rejects_404():
    """Valida que en BD real registrar demanda para asignatura o tema inexistente rechace con HTTP 404."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    try:
        # Asignatura 99999 inexistente
        p_bad_asig = MentoringDemandPayload(id_asignatura=99999, id_tema=1, notas="Demanda inválida")
        with pytest.raises(Exception) as exc_asig:
            BookingService.create_demand_request(db, p_bad_asig, "alumno@upt.pe")
        assert exc_asig.value.status_code == 404

        # Crear asignatura pero tema 88888 inexistente
        asig = Asignatura(
            id_asignatura=10,
            codigo_curso="CURSO-10",
            nombre_curso="Curso Diez",
            ciclo_plan=2,
            creditos=4,
        )
        db.add(asig)
        db.commit()

        p_bad_tema = MentoringDemandPayload(id_asignatura=10, id_tema=88888, notas="Demanda inválida")
        with pytest.raises(Exception) as exc_tema:
            BookingService.create_demand_request(db, p_bad_tema, "alumno@upt.pe")
        assert exc_tema.value.status_code == 404
    finally:
        db.close()
        engine.dispose()


def test_reserve_seat_real_db_all_validation_guards():
    """Valida todas las reglas de guarda en base de datos real (SESSION_NOT_OPEN, WINDOW_CLOSED, MENTOR_CANNOT_BOOK, DUPLICATE)."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    try:
        now = datetime.now(UTC)
        asig = Asignatura(
            id_asignatura=1,
            codigo_curso="CALC-101",
            nombre_curso="Cálculo I",
            ciclo_plan=1,
            creditos=4,
            factor_ponderacion=1.2,
        )
        tema = TemaConceptual(id_tema=1, id_asignatura=1, nombre_tema="Límites", unidad_silabica=1)
        # 1. Sesión no publicada (CONFIRMADA)
        s_closed = SesionMentoria(
            id_sesion=101,
            codigo_sesion="SES-CLOSED",
            mentor_email="mentor.titular@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now + timedelta(days=3),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Aula 101",
            estado="CONFIRMADA",
        )
        # 2. Sesión con ventana T-24h vencida (< 24 h)
        s_near = SesionMentoria(
            id_sesion=102,
            codigo_sesion="SES-NEAR",
            mentor_email="mentor.titular@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now + timedelta(hours=10),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Aula 102",
            estado="PUBLICADA",
        )
        # 3. Sesión apta
        s_valid = SesionMentoria(
            id_sesion=103,
            codigo_sesion="SES-VALID",
            mentor_email="mentor.titular@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now + timedelta(days=4),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Aula 103",
            estado="PUBLICADA",
        )
        db.add_all([asig, tema, s_closed, s_near, s_valid])
        db.commit()

        # Guarda 1: Sesión no publicada -> 400
        with pytest.raises(Exception) as exc_closed:
            BookingService.reserve_seat(db, BookingCreatePayload(id_sesion=101, estudiante_email="a@upt.pe"))
        assert exc_closed.value.status_code == 400
        assert "SESSION_NOT_OPEN" in str(exc_closed.value.detail)

        # Guarda 2: Ventana cerrada T-24h -> 400
        with pytest.raises(Exception) as exc_near:
            BookingService.reserve_seat(db, BookingCreatePayload(id_sesion=102, estudiante_email="a@upt.pe"))
        assert exc_near.value.status_code == 400
        assert "WINDOW_CLOSED_T24H" in str(exc_near.value.detail)

        # Guarda 3: Mentor autoreservando -> 400
        with pytest.raises(Exception) as exc_mentor:
            BookingService.reserve_seat(
                db, BookingCreatePayload(id_sesion=103, estudiante_email="mentor.titular@upt.pe")
            )
        assert exc_mentor.value.status_code == 400
        assert "MENTOR_CANNOT_BOOK" in str(exc_mentor.value.detail)

        # Guarda 4: Duplicidad de reserva activa -> 400
        p_ok = BookingCreatePayload(id_sesion=103, estudiante_email="postulante@upt.pe")
        r1 = BookingService.reserve_seat(db, p_ok)
        assert r1.id_reserva is not None

        with pytest.raises(Exception) as exc_dup:
            BookingService.reserve_seat(db, p_ok)
        assert exc_dup.value.status_code == 400
        assert "DUPLICATE_BOOKING" in str(exc_dup.value.detail)
    finally:
        db.close()
        engine.dispose()


def test_quorum_evaluation_below_50_percent_in_real_db():
    """Valida que en BD real ante quórum insuficiente (< 50%) la sesión pase a PENDIENTE_CONFIRMACION."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    try:
        now = datetime.now(UTC)
        asig = Asignatura(
            id_asignatura=1,
            codigo_curso="CALC-101",
            nombre_curso="Cálculo I",
            ciclo_plan=1,
            creditos=4,
        )
        tema = TemaConceptual(id_tema=1, id_asignatura=1, nombre_tema="Límites", unidad_silabica=1)
        sesion = SesionMentoria(
            id_sesion=200,
            codigo_sesion="SES-LOW-QUORUM",
            mentor_email="mentor@upt.pe",
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=now + timedelta(hours=10),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Aula 200",
            estado="PUBLICADA",
        )
        db.add_all([asig, tema, sesion])
        db.commit()

        # Sembrar solo 2 reservas confirmadas (20% < 50%)
        for i in range(2):
            db.add(
                ReservaCupo(
                    codigo_reserva=f"RES-LQ-{i}",
                    id_sesion=200,
                    estudiante_email=f"conf_lq_{i}@upt.pe",
                    estado="CONFIRMADA",
                    fecha_reserva=now - timedelta(days=1),
                )
            )
        db.commit()

        q_res = BookingService.evaluate_quorum(db, 200)
        assert q_res.cumple_quorum is False
        assert q_res.porcentaje_quorum == 20.0
        assert q_res.estado_sesion == "PENDIENTE_CONFIRMACION"

        # Verificar en base de datos que la sesión mutó a PENDIENTE_CONFIRMACION
        sesion_db = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == 200).first()
        assert sesion_db.estado == "PENDIENTE_CONFIRMACION"
    finally:
        db.close()
        engine.dispose()


def test_quorum_evaluation_in_memory_state_transitions():
    """Valida las transiciones de estado de sesión (CONFIRMADA / PENDIENTE_CONFIRMACION) en memoria."""
    now = datetime.now(UTC)
    clear_offers_in_memory()
    clear_bookings_in_memory()

    _memory_offers.append(
        {
            "id_sesion": 300,
            "codigo_sesion": "SES-MEM-QUORUM",
            "mentor_email": "mentor.mem@upt.pe",
            "id_asignatura": 1,
            "codigo_asignatura": "CALC-101",
            "nombre_asignatura": "Cálculo I",
            "id_tema": 1,
            "nombre_tema": "Límites",
            "fecha_inicio": (now + timedelta(hours=10)).isoformat(),
            "duracion_minutos": 60,
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "espacio_asignado": "Aula 300",
            "estado": "PUBLICADA",
        }
    )

    # 1. Con 2 confirmadas (20%) -> Quórum insuficiente, pasa a PENDIENTE_CONFIRMACION
    for i in range(2):
        _memory_bookings.append(
            {
                "id_reserva": 301 + i,
                "codigo_reserva": f"RES-MEM-{i}",
                "id_sesion": 300,
                "estudiante_email": f"est_mem_{i}@upt.pe",
                "estado": "CONFIRMADA",
            }
        )
    q_low = BookingService.evaluate_quorum(None, 300)
    assert q_low.cumple_quorum is False
    assert q_low.estado_sesion == "PENDIENTE_CONFIRMACION"

    # 2. Añadir 3 más confirmadas (5/10 = 50%) -> Quórum alcanzado
    target_off = next(o for o in _memory_offers if o["id_sesion"] == 300)
    target_off["estado"] = "PUBLICADA"
    for i in range(2, 5):
        _memory_bookings.append(
            {
                "id_reserva": 301 + i,
                "codigo_reserva": f"RES-MEM-{i}",
                "id_sesion": 300,
                "estudiante_email": f"est_mem_{i}@upt.pe",
                "estado": "CONFIRMADA",
            }
        )
    q_high = BookingService.evaluate_quorum(None, 300)
    assert q_high.cumple_quorum is True
    assert q_high.estado_sesion == "CONFIRMADA"
