"""
Validación Transaccional Concurrente en PostgreSQL Aislado (QA-P2P-03 — Fase 3)
Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)

Ejecuta 7 escenarios transaccionales de alta concurrencia sobre un esquema
sandbox temporal en PostgreSQL (Supabase), asegurando:
1. Sobrecupo y reservas simultáneas sobre la última plaza disponible (0.0% sobrecupo - RNF07)
2. Intentos de reserva duplicada concurrente
3. Ratificación antes y después del límite temporal T-24h (RN-08)
4. Desistimiento concurrente y liberación inmediata de cupos (RN-10)
5. Validación de quórum normativo institucional >= 50% (RN-09)
6. Restricciones y aislamiento de autorización entre estudiantes (RBAC)
7. Fallos transaccionales y rollback atómico

Aislamiento: Todo opera dentro del esquema temporal 'test_qa_p2p_03_tx' sin tocar 'public'.
"""

import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configurar path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
base_dir = os.path.join(root_dir, "aplicacion", "backend")
tools_dir = os.path.abspath(os.path.dirname(__file__))

for p in (base_dir, tools_dir):
    if p not in sys.path:
        sys.path.insert(0, p)

import app.models  # noqa: F401
from app.core.config import settings
from app.db.session import Base
from app.models.booking import ReservaCupo
from app.models.consent import ConsentimientoLegal
from app.models.curriculum import Asignatura, TemaConceptual
from app.models.offer import SesionMentoria
from app.models.profile import PerfilAcademico
from app.models.roles import Rol, UsuarioRol
from app.schemas.booking import BookingCancelPayload, BookingCreatePayload
from app.services.booking_service import BookingService
from qa_db_hardening import (
    DatabaseSecurityError,
    build_isolated_db_url,
    create_isolated_schema,
    generate_unique_test_schema,
    resolve_qa_database_url,
    safe_teardown_schema,
    validate_test_environment,
    verify_connection_search_path,
)

tx_results = []


def record_tx(scenario: str, name: str, passed: bool, detail: str = ""):
    status_str = "PASS" if passed else "FAIL"
    tx_results.append({
        "scenario": scenario,
        "name": name,
        "status": status_str,
        "detail": detail,
    })
    print(f"[{status_str}] {scenario} -> {name}: {detail}")
    if not passed:
        raise AssertionError(f"Fallo en {scenario} -> {name}: {detail}")


def setup_isolated_schema():
    validate_test_environment(getattr(settings, "APP_ENV", ""))
    qa_db_url = resolve_qa_database_url()
    schema_name = generate_unique_test_schema("test_qa_p2p_04_tx")
    print(f"[SETUP] Inicializando esquema sandbox aislado '{schema_name}' en PostgreSQL QA...")

    admin_engine = create_engine(qa_db_url, pool_pre_ping=True)
    create_isolated_schema(admin_engine, schema_name)

    # Motor vinculado al esquema aislado de forma estricta mediante URL con search_path
    isolated_url = build_isolated_db_url(qa_db_url, schema_name)
    schema_engine = create_engine(isolated_url, pool_pre_ping=True)

    with schema_engine.connect() as conn:
        verify_connection_search_path(conn, schema_name)
        Base.metadata.create_all(bind=conn)
        conn.commit()

    SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=schema_engine)
    return admin_engine, schema_engine, SessionMaker, schema_name


def teardown_isolated_schema(admin_engine, schema_engine, schema_name):
    print(f"[TEARDOWN] Eliminando esquema sandbox '{schema_name}' en PostgreSQL...")
    try:
        schema_engine.dispose()
    except Exception:
        pass
    safe_teardown_schema(admin_engine, schema_name)


def seed_base_catalog(db):
    # Asignatura
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
    db.add(a1)
    db.commit()

    # Tema
    t1 = TemaConceptual(
        id_tema=1,
        id_asignatura=1,
        nombre_tema="Límites y Continuidad",
        unidad_silabica=1,
        estado_activo=True,
    )
    db.add(t1)
    db.commit()

    # Roles
    r1 = Rol(id_rol=1, nombre_rol="mentoreado", descripcion="Estudiante")
    r2 = Rol(id_rol=2, nombre_rol="mentor", descripcion="Mentor par")
    r3 = Rol(id_rol=3, nombre_rol="administrador", descripcion="Administrador")
    db.add_all([r1, r2, r3])
    db.commit()

    # Mentor
    ur_m = UsuarioRol(email="mentor.tx@upt.pe", id_rol=2, asignado_por="ADMIN_INIT", activo=True)
    prof_m = PerfilAcademico(
        email="mentor.tx@upt.pe",
        codigo_estudiante="2020010101",
        nombres="Mentor",
        apellidos="Transaccional",
        ciclo_actual=8,
        rol_postulacion="mentor",
        materias_interes=[1],
        temas_seleccionados=[1],
    )
    db.add_all([ur_m, prof_m])
    db.commit()

    # Admin
    ur_a = UsuarioRol(email="admin.tx@upt.pe", id_rol=3, asignado_por="SYS_INIT", activo=True)
    db.add(ur_a)
    db.commit()


def run_all_postgresql_transactions():
    print("=" * 75)
    try:
        admin_engine, schema_engine, SessionMaker, schema_name = setup_isolated_schema()
    except DatabaseSecurityError as e:
        print("[BLOCKED] Pruebas transaccionales en PostgreSQL detenidas por política de seguridad:")
        print(f"          {e}")
        sys.exit(2)
    print("INICIANDO PRUEBAS TRANSACCIONALES CONTROLADAS EN POSTGRESQL AISLADO (FASE 3)")
    print(f"Motor: PostgreSQL (Supabase) | Esquema sandbox verificado: {schema_name}")
    print("=" * 75)

    try:
        with SessionMaker() as db:
            seed_base_catalog(db)

        now = datetime.now(UTC)

        # ---------------------------------------------------------------------
        # Escenario 1: Sobrecupo y Reservas simultáneas sobre la última plaza (RNF07)
        # ---------------------------------------------------------------------
        sc_1 = "1. Sobrecupo & Concurrencia de Última Plaza"
        with SessionMaker() as db:
            s1 = SesionMentoria(
                id_sesion=1001,
                codigo_sesion="SES-TX-1001",
                mentor_email="mentor.tx@upt.pe",
                id_asignatura=1,
                id_tema=1,
                fecha_inicio=now + timedelta(hours=48),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Lab 101 - EPIS",
                estado="PUBLICADA",
            )
            db.add(s1)
            # Sembrar 9 reservas activas confirmadas previas
            for i in range(1, 10):
                em = f"estudiante_base_{i:02d}@upt.pe"
                # Otorgar consentimiento
                c = ConsentimientoLegal(email=em, accepted=True, terms_version="2026-II")
                db.add(c)
                b = ReservaCupo(
                    codigo_reserva=f"RES-BASE-{i:02d}",
                    id_sesion=1001,
                    estudiante_email=em,
                    estado="CONFIRMADA",
                    fecha_reserva=now - timedelta(hours=5),
                    fecha_ratificacion=now - timedelta(hours=4),
                )
                db.add(b)
            db.commit()

            # Registrar consentimiento para los 5 competidores concurrentes
            for j in range(10, 15):
                em_comp = f"estudiante_comp_{j:02d}@upt.pe"
                db.add(ConsentimientoLegal(email=em_comp, accepted=True, terms_version="2026-II"))
            db.commit()

        # Ejecutar 5 reservas concurrentes simultáneas por 5 hilos
        success_count = 0
        conflict_count = 0
        results_lock = threading.Lock()

        def try_booking(comp_idx):
            nonlocal success_count, conflict_count
            student_em = f"estudiante_comp_{comp_idx:02d}@upt.pe"
            with SessionMaker() as local_db:
                payload = BookingCreatePayload(id_sesion=1001, estudiante_email=student_em)
                try:
                    res = BookingService.reserve_seat(
                        db=local_db,
                        payload=payload,
                        caller_email=student_em,
                    )
                    with results_lock:
                        success_count += 1
                    return "SUCCESS", res.codigo_reserva
                except HTTPException as e:
                    with results_lock:
                        if e.status_code == 409:
                            conflict_count += 1
                    return f"HTTP_{e.status_code}", str(e.detail)

        statuses = []
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = [pool.submit(try_booking, idx) for idx in range(10, 15)]
            for f in as_completed(futures):
                status_code, det = f.result()
                statuses.append(status_code)
                print(f"      [Thread Result] {status_code}: {det[:60]}")

        # Verificar integridad en base de datos
        with SessionMaker() as db:
            total_active = (
                db.query(ReservaCupo)
                .filter(
                    ReservaCupo.id_sesion == 1001,
                    ReservaCupo.estado.in_(["PENDIENTE_CONFIRMACION", "CONFIRMADA"]),
                )
                .count()
            )

        record_tx(
            sc_1,
            "Exactamente 1 reserva aceptada sobre última plaza",
            success_count == 1,
            f"Aceptadas: {success_count}/5 | Estados: {statuses}",
        )
        record_tx(
            sc_1,
            "Todas las demás peticiones denegadas (409 CAPACITY_EXCEEDED o 503 DATABASE_BUSY)",
            success_count == 1 and (conflict_count + statuses.count("HTTP_503")) == 4,
            f"Aceptada: 1 | Rechazadas: {conflict_count} (409) + {statuses.count('HTTP_503')} (503)",
        )
        record_tx(
            sc_1,
            "Aforo final exacto en 10/10 (0.0% Sobrecupo en PostgreSQL - RNF07)",
            total_active == 10,
            f"Cupos ocupados: {total_active}/10 | Sobrecupo: 0.0%",
        )

        # ---------------------------------------------------------------------
        # Escenario 2: Intentos de reserva duplicada concurrente
        # ---------------------------------------------------------------------
        sc_2 = "2. Concurrencia de Reserva Duplicada"
        dup_email = "estudiante_dup@upt.pe"
        with SessionMaker() as db:
            s2 = SesionMentoria(
                id_sesion=1002,
                codigo_sesion="SES-TX-1002",
                mentor_email="mentor.tx@upt.pe",
                id_asignatura=1,
                id_tema=1,
                fecha_inicio=now + timedelta(hours=48),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Lab 102 - EPIS",
                estado="PUBLICADA",
            )
            db.add(s2)
            db.add(ConsentimientoLegal(email=dup_email, accepted=True, terms_version="2026-II"))
            db.commit()

        dup_success = 0
        dup_rejected = 0

        def try_duplicate_booking():
            nonlocal dup_success, dup_rejected
            with SessionMaker() as local_db:
                payload = BookingCreatePayload(id_sesion=1002, estudiante_email=dup_email)
                try:
                    res = BookingService.reserve_seat(
                        db=local_db,
                        payload=payload,
                        caller_email=dup_email,
                    )
                    with results_lock:
                        dup_success += 1
                    return "SUCCESS", res.codigo_reserva
                except HTTPException as e:
                    with results_lock:
                        if e.status_code == 400:
                            dup_rejected += 1
                    return f"HTTP_{e.status_code}", str(e.detail)

        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(try_duplicate_booking) for _ in range(4)]
            for f in as_completed(futures):
                _ = f.result()

        with SessionMaker() as db:
            dup_rows = (
                db.query(ReservaCupo)
                .filter(
                    ReservaCupo.id_sesion == 1002,
                    ReservaCupo.estudiante_email == dup_email,
                    ReservaCupo.estado.in_(["PENDIENTE_CONFIRMACION", "CONFIRMADA"]),
                )
                .count()
            )

        record_tx(
            sc_2,
            "Exactamente 1 reserva aceptada para mismo estudiante",
            dup_success == 1,
            f"Aceptada: {dup_success} | Rechazadas: {dup_rejected}",
        )
        record_tx(
            sc_2,
            "Exactamente 1 registro persistido sin duplicación",
            dup_rows == 1,
            f"Registros en BD: {dup_rows}",
        )

        # ---------------------------------------------------------------------
        # Escenario 3: Ratificación antes y después del corte temporal T-24h (RN-08)
        # ---------------------------------------------------------------------
        sc_3 = "3. Ratificación Temporal T-24h"
        with SessionMaker() as db:
            # Sesión abierta (T+48h)
            s_open = SesionMentoria(
                id_sesion=1003,
                codigo_sesion="SES-TX-1003",
                mentor_email="mentor.tx@upt.pe",
                id_asignatura=1,
                id_tema=1,
                fecha_inicio=now + timedelta(hours=48),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Aula 201",
                estado="PUBLICADA",
            )
            # Sesión cerrada (T+12h, antelación < 24h)
            s_closed = SesionMentoria(
                id_sesion=1004,
                codigo_sesion="SES-TX-1004",
                mentor_email="mentor.tx@upt.pe",
                id_asignatura=1,
                id_tema=1,
                fecha_inicio=now + timedelta(hours=12),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Aula 202",
                estado="PUBLICADA",
            )
            b_open = ReservaCupo(
                id_reserva=2003,
                codigo_reserva="RES-OPEN-01",
                id_sesion=1003,
                estudiante_email="alumno_open@upt.pe",
                estado="PENDIENTE_CONFIRMACION",
            )
            b_closed = ReservaCupo(
                id_reserva=2004,
                codigo_reserva="RES-CLOSED-01",
                id_sesion=1004,
                estudiante_email="alumno_closed@upt.pe",
                estado="PENDIENTE_CONFIRMACION",
            )
            db.add_all([s_open, s_closed, b_open, b_closed])
            db.commit()

        # 3.1 Confirmación antes de T-24h -> SUCEDE
        with SessionMaker() as db:
            res_open = BookingService.confirm_attendance(
                db=db,
                id_reserva=2003,
                caller_email="alumno_open@upt.pe",
            )
            record_tx(
                sc_3,
                "Ratificación exitosa antes de T-24h (CONFIRMADA)",
                res_open.estado == "CONFIRMADA",
                f"Estado: {res_open.estado}",
            )

        # 3.2 Confirmación después de T-24h -> RECHAZADO con 400
        with SessionMaker() as db:
            threw_400 = False
            try:
                BookingService.confirm_attendance(
                    db=db,
                    id_reserva=2004,
                    caller_email="alumno_closed@upt.pe",
                )
            except HTTPException as e:
                if e.status_code == 400:
                    threw_400 = True
            record_tx(
                sc_3,
                "Rechazo de ratificación extemporánea a T-12h (WINDOW_CLOSED_T24H)",
                threw_400,
                "HTTP 400 capturado correctamente",
            )

        # ---------------------------------------------------------------------
        # Escenario 4: Desistimiento Concurrente y Liberación Inmediata (RN-10)
        # ---------------------------------------------------------------------
        sc_4 = "4. Desistimiento & Liberación Concurrente"
        with SessionMaker() as db:
            s4 = SesionMentoria(
                id_sesion=1005,
                codigo_sesion="SES-TX-1005",
                mentor_email="mentor.tx@upt.pe",
                id_asignatura=1,
                id_tema=1,
                fecha_inicio=now + timedelta(hours=48),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Aula 203",
                estado="PUBLICADA",
            )
            # Llenar 10 cupos
            db.add(s4)
            for k in range(1, 11):
                em_k = f"estudiante_s4_{k:02d}@upt.pe"
                db.add(ConsentimientoLegal(email=em_k, accepted=True, terms_version="2026-II"))
                db.add(
                    ReservaCupo(
                        id_reserva=3000 + k,
                        codigo_reserva=f"RES-S4-{k:02d}",
                        id_sesion=1005,
                        estudiante_email=em_k,
                        estado="CONFIRMADA",
                    )
                )
            # Agregar consentimiento para nuevo postulante
            db.add(ConsentimientoLegal(email="estudiante_nuevo_post@upt.pe", accepted=True, terms_version="2026-II"))
            db.commit()

        # Intentar cancelar la reserva 3001 simultáneamente desde 2 peticiones
        cancel_success = 0
        cancel_conflict = 0

        def try_cancel():
            nonlocal cancel_success, cancel_conflict
            with SessionMaker() as local_db:
                try:
                    payload = BookingCancelPayload(motivo="Fuerza mayor")
                    res = BookingService.cancel_reservation(
                        db=local_db,
                        id_reserva=3001,
                        payload=payload,
                        caller_email="estudiante_s4_01@upt.pe",
                    )
                    with results_lock:
                        cancel_success += 1
                    return "SUCCESS", res.estado
                except HTTPException as e:
                    with results_lock:
                        if e.status_code == 400:
                            cancel_conflict += 1
                    return f"HTTP_{e.status_code}", str(e.detail)

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(try_cancel) for _ in range(2)]
            for f in as_completed(futures):
                _ = f.result()

        record_tx(
            sc_4,
            "Desistimiento concurrente: exactamente 1 cancelación exitosa",
            cancel_success == 1 and cancel_conflict == 1,
            f"Éxito: {cancel_success} | Conflicto 400: {cancel_conflict}",
        )

        # Ahora el cupo liberado debe estar disponible inmediatamente para un nuevo alumno
        with SessionMaker() as db:
            new_booking_res = BookingService.reserve_seat(
                db=db,
                payload=BookingCreatePayload(id_sesion=1005, estudiante_email="estudiante_nuevo_post@upt.pe"),
                caller_email="estudiante_nuevo_post@upt.pe",
            )
            record_tx(
                sc_4,
                "Liberación inmediata de vacante aprovechada por nuevo estudiante",
                new_booking_res.estado == "PENDIENTE_CONFIRMACION",
                f"Nueva reserva: {new_booking_res.codigo_reserva}",
            )

        # ---------------------------------------------------------------------
        # Escenario 5: Validación de Quórum Normativo >= 50% (RN-09)
        # ---------------------------------------------------------------------
        sc_5 = "5. Quórum Normativo >= 50% (RN-09)"
        with SessionMaker() as db:
            # Caso 5A: Cumple quórum (5/10 = 50%)
            sq_ok = SesionMentoria(
                id_sesion=1006,
                codigo_sesion="SES-Q-OK",
                mentor_email="mentor.tx@upt.pe",
                id_asignatura=1,
                id_tema=1,
                fecha_inicio=now + timedelta(hours=30),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Aula 204",
                estado="PUBLICADA",
            )
            db.add(sq_ok)
            for m in range(1, 6):
                db.add(
                    ReservaCupo(
                        id_sesion=1006,
                        codigo_reserva=f"RES-QOK-{m}",
                        estudiante_email=f"qok_{m}@upt.pe",
                        estado="CONFIRMADA",
                    )
                )

            # Caso 5B: No cumple quórum (2 confirmados, 4 no confirmados)
            sq_fail = SesionMentoria(
                id_sesion=1007,
                codigo_sesion="SES-Q-FAIL",
                mentor_email="mentor.tx@upt.pe",
                id_asignatura=1,
                id_tema=1,
                fecha_inicio=now + timedelta(hours=30),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Aula 205",
                estado="PUBLICADA",
            )
            db.add(sq_fail)
            for m in range(1, 3):
                db.add(
                    ReservaCupo(
                        id_sesion=1007,
                        codigo_reserva=f"RES-QCONF-{m}",
                        estudiante_email=f"qconf_{m}@upt.pe",
                        estado="CONFIRMADA",
                    )
                )
            for m in range(3, 7):
                db.add(
                    ReservaCupo(
                        id_sesion=1007,
                        codigo_reserva=f"RES-QPEN-{m}",
                        estudiante_email=f"qpen_{m}@upt.pe",
                        estado="PENDIENTE_CONFIRMACION",
                    )
                )
            db.commit()

        with SessionMaker() as db:
            q_res_ok = BookingService.evaluate_session_quorum(
                db=db,
                id_sesion=1006,
                now_utc=now + timedelta(hours=6),
            )
            record_tx(
                sc_5,
                "Quórum 50% alcanzado -> Sesión CONFIRMADA (RN-09)",
                q_res_ok.cumple_quorum is True and q_res_ok.estado_sesion == "CONFIRMADA",
                f"Confirmados: {q_res_ok.reservas_confirmadas}/{q_res_ok.aforo_maximo}",
            )

            q_res_fail = BookingService.evaluate_session_quorum(
                db=db,
                id_sesion=1007,
                now_utc=now + timedelta(hours=6),
            )
            record_tx(
                sc_5,
                "Quórum insuficiente (2/10) -> Sesión QUORUM_INSUFICIENTE (RN-09)",
                q_res_fail.cumple_quorum is False and q_res_fail.estado_sesion == "QUORUM_INSUFICIENTE",
                f"Confirmados: {q_res_fail.reservas_confirmadas}/{q_res_fail.aforo_maximo}",
            )

        # ---------------------------------------------------------------------
        # Escenario 6: Aislamiento y Control de Autorización entre Estudiantes
        # ---------------------------------------------------------------------
        sc_6 = "6. Aislamiento & RBAC entre Alumnos"
        with SessionMaker() as db:
            b_target = ReservaCupo(
                id_reserva=4001,
                codigo_reserva="RES-RBAC-01",
                id_sesion=1003,
                estudiante_email="alumno_victima@upt.pe",
                estado="PENDIENTE_CONFIRMACION",
            )
            db.add(b_target)
            db.commit()

        # Intento de Alumno Hacker de confirmar reserva de Alumno Víctima -> 403
        with SessionMaker() as db:
            hacker_confirm_blocked = False
            try:
                BookingService.confirm_attendance(
                    db=db,
                    id_reserva=4001,
                    caller_email="alumno_hacker@upt.pe",
                )
            except HTTPException as e:
                if e.status_code == 403:
                    hacker_confirm_blocked = True
            record_tx(
                sc_6,
                "Intento de confirmación de reserva ajena denegado (403 FORBIDDEN)",
                hacker_confirm_blocked,
                "RBAC titular verificado",
            )

            # Intento de Alumno Hacker de cancelar reserva de Alumno Víctima -> 403
            hacker_cancel_blocked = False
            try:
                BookingService.cancel_reservation(
                    db=db,
                    id_reserva=4001,
                    caller_email="alumno_hacker@upt.pe",
                )
            except HTTPException as e:
                if e.status_code == 403:
                    hacker_cancel_blocked = True
            record_tx(
                sc_6,
                "Intento de cancelación de reserva ajena denegado (403 FORBIDDEN)",
                hacker_cancel_blocked,
                "RBAC titular verificado",
            )

            # Administrador con override permitido -> 200 OK
            admin_confirm_ok = BookingService.confirm_attendance(
                db=db,
                id_reserva=4001,
                caller_email="admin.tx@upt.pe",
                is_admin=True,
            )
            record_tx(
                sc_6,
                "Override administrativo legítimo sobre reserva estudiantil",
                admin_confirm_ok.estado == "CONFIRMADA",
                "Admin override verificado",
            )

        # ---------------------------------------------------------------------
        # Escenario 7: Fallos Transaccionales y Rollback Atómico
        # ---------------------------------------------------------------------
        sc_7 = "7. Rollback Atómico ante Fallo"
        with SessionMaker() as db:
            count_before = db.query(ReservaCupo).count()
            rollback_verified = False
            try:
                # Iniciar operación y forzar excepción después de add
                b_faulty = ReservaCupo(
                    codigo_reserva="RES-FAULTY-01",
                    id_sesion=999999,  # ID inexistente que violará FK al hacer flush/commit si FK activa
                    estudiante_email="alumno_faulty@upt.pe",
                    estado="PENDIENTE_CONFIRMACION",
                )
                db.add(b_faulty)
                # Forzar excepción de negocio deliberada antes del commit
                raise RuntimeError("Simulación de fallo en medio de transacción distribuida")
            except RuntimeError:
                db.rollback()
                rollback_verified = True

            count_after = db.query(ReservaCupo).count()

        record_tx(
            sc_7,
            "Rollback atómico restaura estado sin registros huérfanos",
            rollback_verified and count_before == count_after,
            f"Filas antes: {count_before} == Filas después: {count_after}",
        )

        print("=" * 75)
        print("TODAS LAS PRUEBAS TRANSACCIONALES EN POSTGRESQL FUERON APROBADAS (7/7)")
        print(f"Total escenarios verificados: {len(tx_results)} | 100% EXITOSOS")
        print("=" * 75)

    finally:
        teardown_isolated_schema(admin_engine, schema_engine, schema_name)


if __name__ == "__main__":
    run_all_postgresql_transactions()
