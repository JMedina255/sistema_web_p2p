"""Run against a local PostgreSQL server with P2P_TEST_POSTGRES_URL."""
import os
from uuid import uuid4

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from psycopg import sql
from sqlalchemy.engine import make_url

from app.core.config import settings


@pytest.fixture
def local_database(monkeypatch):
    url = os.getenv("P2P_TEST_POSTGRES_URL")
    if not url:
        pytest.skip("P2P_TEST_POSTGRES_URL is not set")
    address = make_url(url)
    assert address.host in {"localhost", "127.0.0.1", "::1"}
    name = "p2p_test_" + uuid4().hex
    with psycopg.connect(url, autocommit=True) as admin:
        admin.execute(sql.SQL("CREATE DATABASE {} TEMPLATE template0").format(sql.Identifier(name)))
        try:
            target = address.set(database=name).render_as_string(hide_password=False)
            monkeypatch.setattr(settings, "DATABASE_URL", target)
            yield target
        finally:
            admin.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(name)))


def seed_session(db):
    db.execute("INSERT INTO asignaturas(codigo_curso,nombre_curso,ciclo_plan,creditos) VALUES ('QA','Curso QA',1,4)")
    db.execute("INSERT INTO temas_conceptuales(id_asignatura,nombre_tema) VALUES (1,'Tema QA')")
    return db.execute("""INSERT INTO sesiones_mentoria(codigo_sesion,mentor_email,id_asignatura,id_tema,fecha_inicio,
        duracion_minutos,modalidad,aforo_maximo,espacio_asignado,estado)
        VALUES ('QA-MIG','mentor@upt.pe',1,1,now(),90,'virtual',20,'virtual','HORAS_VISADAS') RETURNING id_sesion""").fetchone()[0]


def test_closure_migration_preserves_legacy_data(local_database):
    config = Config("alembic.ini")
    command.upgrade(config, "20261113_005")
    with psycopg.connect(local_database) as db:
        sid = seed_session(db)
        db.execute("""INSERT INTO bitacoras_pedagogicas(id_sesion,mentor_email,resumen_temas,logros_alcanzados,hash_integridad)
            VALUES (%s,'mentor@upt.pe','Límites','Resolvieron ejercicios','firma-original')""", (sid,))
        db.execute("""INSERT INTO encuestas_calidad(id_sesion,estudiante_email,puntuacion_general,
            claridad_explicacion,dominio_tema,puntualidad_compromiso,comentario)
            VALUES (%s,'estudiante@upt.pe',4,3,5,4,'Comentario original')""", (sid,))
        db.execute("""INSERT INTO certificados_horas
            (codigo_certificado, mentor_email,total_horas,sesiones_concluidas,promedio_calidad,hash_seguridad)
            VALUES ('CERT-2025-I-0001','mentor@upt.pe',22,11,5,'firma'),
                   ('CERT-2025-I-0002','mentor@upt.pe',24,12,5,'firma2')""")
    command.upgrade(config, "head")
    with psycopg.connect(local_database) as db:
        assert db.execute("""SELECT codigo_folio,id_mentor,periodo_academico,horas_acreditadas,hash_firma,revision_historica
            FROM certificados_horas ORDER BY id_certificado""").fetchall() == [
                ("CERT-2025-I-0001", "mentor@upt.pe", "2025-I", 22, "firma", 1),
                ("CERT-2025-I-0002", "mentor@upt.pe", "2025-I", 24, "firma2", 0)]
        assert db.execute("""SELECT temas_cubiertos,observaciones,horas_declaradas,visado_administrador,hash_firma
            FROM bitacoras_pedagogicas""").fetchone() == (["Límites"], "Resolvieron ejercicios", 1.5, True, "firma-original")
        assert db.execute("""SELECT puntualidad,calificacion_general,comentarios FROM encuestas_calidad""").fetchone() == (
            4, 4, "Comentario original")


def test_concurrent_room_publication_postgres(local_database):
    from concurrent.futures import ThreadPoolExecutor
    from datetime import UTC, datetime, timedelta
    from threading import Barrier

    from fastapi import HTTPException
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    from app.schemas.offer import PublishOfferPayload
    from app.services.offer_service import OfferService

    command.upgrade(Config("alembic.ini"), "head")
    with psycopg.connect(local_database) as db:
        seed_session(db)
    engine = create_engine(make_url(local_database).set(drivername="postgresql+psycopg"))
    now = datetime.now(UTC)
    start = (now + timedelta(days=14 - now.weekday())).replace(hour=15, minute=0, second=0, microsecond=0)
    payload = PublishOfferPayload(mentor_email="2022073504@upt.pe", id_asignatura=1, codigo_asignatura="QA",
        nombre_asignatura="Curso QA", id_tema=1, nombre_tema="Tema QA", fecha_inicio=start.isoformat(),
        modalidad="presencial", duracion_minutos=60, aforo_maximo=10, espacio_asignado="Aula 101")
    ready = Barrier(2, timeout=10)

    def publish():
        with Session(engine) as db:
            ready.wait()
            try:
                OfferService.publish_offer(db, payload.model_copy())
                return 201
            except HTTPException as exc:
                return exc.status_code

    try:
        with ThreadPoolExecutor(max_workers=2) as workers:
            results = [workers.submit(publish) for _ in range(2)]
            assert sorted(result.result(timeout=20) for result in results) == [201, 409]
        with psycopg.connect(local_database) as db:
            assert db.execute("SELECT count(*) FROM sesiones_mentoria WHERE espacio_asignado='Aula 101'").fetchone() == (1,)
    finally:
        engine.dispose()


def test_upgrade_already_aligned_schema(local_database):
    from sqlalchemy import create_engine

    from app.db.session import Base

    engine = create_engine(make_url(local_database).set(drivername="postgresql+psycopg"))
    try:
        Base.metadata.create_all(engine)
        config = Config("alembic.ini")
        command.stamp(config, "20261113_005")
        command.upgrade(config, "head")
        with psycopg.connect(local_database) as db:
            assert db.execute("SELECT id FROM cronograma_activo").fetchall() == [(1,)]
            db.execute("SELECT id_mentor, horas_declaradas FROM bitacoras_pedagogicas")
    finally:
        engine.dispose()


def test_expo_booking_survey_and_roster(local_database, monkeypatch):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    import seed_expo_showcase as expo
    from app.models.attendance import AsistenciaSesion
    from app.models.booking import ReservaCupo
    from app.models.offer import SesionMentoria
    from app.schemas.survey import SurveyCreatePayload
    from app.services.attendance_service import AttendanceService
    from app.services.booking_service import BookingService
    from app.services.survey_service import SurveyService

    command.upgrade(Config("alembic.ini"), "head")
    engine = create_engine(make_url(local_database).set(drivername="postgresql+psycopg"))
    monkeypatch.setattr(expo, "get_engine", lambda: engine)
    try:
        expo.seed_expo_dataset()
        email = "ra2022073504@virtual.upt.pe"
        with Session(engine) as db:
            def reservation():
                return next(row for row in BookingService.get_student_reservations(db, email)
                            if row.codigo_reserva == "RES-EXPO-SURV-RENZO")

            booking = reservation()
            assert booking.asistio and booking.survey_eligible and not booking.has_surveyed
            attendance = db.query(AsistenciaSesion).filter_by(id_sesion=booking.id_sesion, estudiante_email=email)
            attendance.delete()
            db.commit()
            assert not reservation().survey_eligible
            expo.seed_expo_dataset()
            assert reservation().survey_eligible and attendance.count() == 1
            from concurrent.futures import ThreadPoolExecutor
            from threading import Barrier
            from fastapi import HTTPException

            ready = Barrier(2, timeout=10)
            payload = SurveyCreatePayload(calificacion_general=5, dominio_tema=4, claridad_explicacion=5, puntualidad=5)

            def submit():
                with Session(engine) as worker:
                    ready.wait()
                    try:
                        SurveyService.create_survey(worker, booking.id_sesion, payload, email)
                        return 201
                    except HTTPException as exc:
                        return exc.status_code

            with ThreadPoolExecutor(max_workers=2) as pool:
                requests = [pool.submit(submit) for _ in range(2)]
                assert sorted(req.result(timeout=15) for req in requests) == [201, 409]
            assert reservation().has_surveyed
            attendance.one().asistio = False
            db.commit()
            expo.seed_expo_dataset()
            assert reservation().asistio is False

            live = db.query(SesionMentoria).filter_by(codigo_sesion="SES-EXPO-03-LIVE").one()
            confirmed = db.query(ReservaCupo).filter_by(id_sesion=live.id_sesion, estado="CONFIRMADA").all()
            roster = AttendanceService.get_roster(db, live.id_sesion)
            assert len(roster) == len(confirmed) >= 2 and all(r.pendiente for r in roster)
            db.add(AsistenciaSesion(id_sesion=live.id_sesion, estudiante_email=email, asistio=True,
                                    fecha_checkin=live.fecha_inicio))
            db.commit()
            roster = AttendanceService.get_roster(db, live.id_sesion)
            assert [r.estudiante_email for r in roster if r.asistio and not r.pendiente] == [email]
            assert len(roster) == len(confirmed)
    finally:
        engine.dispose()


def test_concurrent_directed_publication_consumes_demand_once(local_database):
    from concurrent.futures import ThreadPoolExecutor
    from datetime import UTC, datetime, timedelta
    from threading import Barrier

    from fastapi.testclient import TestClient

    from app.core.security import create_access_token
    from app.db.session import close_engine
    from app.main import app

    command.upgrade(Config("alembic.ini"), "head")
    with psycopg.connect(local_database) as db:
        seed_session(db)
        demand_id = db.execute("""
            INSERT INTO solicitudes_demanda(estudiante_email,id_asignatura,id_tema,estado,created_at)
            VALUES ('estudiante@upt.pe',1,1,'PENDIENTE',now()) RETURNING id_demanda
        """).fetchone()[0]

    mentor = "2022073504@upt.pe"
    token = create_access_token({"sub": mentor, "roles": ["mentor"]})
    offer = {
        "id_demanda": demand_id, "id_asignatura": 1, "codigo_asignatura": "QA", "nombre_asignatura": "Curso QA",
        "id_tema": 1, "nombre_tema": "Tema QA", "modalidad": "virtual", "aforo_maximo": 20,
        "mentor_email": mentor, "fecha_inicio": (datetime.now(UTC) + timedelta(days=3)).isoformat(),
    }
    client = TestClient(app)
    ready = Barrier(2, timeout=10)

    def publish():
        ready.wait()
        return client.post("/api/v1/offers", headers={"Authorization": f"Bearer {token}"}, json=offer)

    try:
        assert [row["id_demanda"] for row in client.get("/api/v1/bookings/requests").json()] == [demand_id]
        with ThreadPoolExecutor(max_workers=2) as pool:
            responses = [pool.submit(publish) for _ in range(2)]
            assert sorted(response.result(timeout=15).status_code for response in responses) == [201, 409]
        assert client.get("/api/v1/bookings/requests").json() == []
        with psycopg.connect(local_database) as db:
            assert db.execute("SELECT estado FROM solicitudes_demanda").fetchone() == ("ATENDIDA",)
            assert db.execute("SELECT count(*) FROM sesiones_mentoria WHERE mentor_email = %s", (mentor,)).fetchone() == (1,)
    finally:
        close_engine()
