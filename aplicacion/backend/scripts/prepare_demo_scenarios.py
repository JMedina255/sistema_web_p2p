"""
Script seguro, reproducible e idempotente de preparación de escenarios de demostración institucional (DEMO-01 a DEMO-06).
EPIS-UPT - Sistema Web P2P de Mentorías Académicas.

Escenarios cubiertos:
- DEMO-01: Estudiante y mentor listos para autenticación y recomendación
- DEMO-02: Ofertas publicadas con restricciones horarias y aforo válidos (> 24h, RN-04)
- DEMO-03: Sesión con reserva pendiente de confirmación
- DEMO-04: Sesión lista para evaluación de quórum (T-24h)
- DEMO-05: Sesión en curso con código y token de asistencia activo (TOTP QR)
- DEMO-06: Sesión completada con bitácora pedagógica y hash de integridad (SHA-256)
"""

import argparse
import hashlib
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

# Asegurar que aplicacion/backend esté en sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine, text  # noqa: E402
from sqlalchemy.orm import Session, sessionmaker  # noqa: E402

from app.db.session import Base  # noqa: E402
from app.models.attendance import AsistenciaSesion, TokenAsistenciaActivo  # noqa: E402
from app.models.bitacora import BitacoraPedagogica  # noqa: E402
from app.models.booking import ReservaCupo  # noqa: E402
from app.models.consent import ConsentimientoLegal  # noqa: E402
from app.models.curriculum import Asignatura, TemaConceptual  # noqa: E402
from app.models.offer import SesionMentoria  # noqa: E402
from app.models.profile import DisponibilidadHoraria, PerfilAcademico  # noqa: E402
from app.models.roles import Rol, UsuarioRol  # noqa: E402


def prepare_demo_fixtures(db: Session) -> dict:
    """
    Puebla la base de datos de manera idempotente con los seis escenarios de demostración:
    - DEMO-01: Estudiante mentoreado y mentor acreditado listos para login y recomendación.
    - DEMO-02: Oferta futura publicada con antelación > 24h (RN-04) y aforo válido.
    - DEMO-03: Sesión con reserva en estado 'PENDIENTE_CONFIRMACION'.
    - DEMO-04: Sesión en ventana T-24h para evaluación de quórum institucional (RN-09).
    - DEMO-05: Sesión en curso ('CONFIRMADA') con token TOTP activo para check-in por QR.
    - DEMO-06: Sesión concluida con bitácora pedagógica registrada y sellada con hash SHA-256.
    """
    now = datetime.now(UTC)

    # 1. Catálogo Curricular Básico (Idempotente)
    for asig_id, cod, nom, ciclo, cred in [
        (1, "CALC-101", "Cálculo I", 1, 4),
        (2, "CALC-201", "Cálculo II", 2, 4),
        (3, "ALGO-202", "Algoritmos y Estructuras de Datos", 2, 4),
    ]:
        existing_asig = db.query(Asignatura).filter(Asignatura.id_asignatura == asig_id).first()
        if not existing_asig:
            db.add(
                Asignatura(
                    id_asignatura=asig_id,
                    codigo_curso=cod,
                    nombre_curso=nom,
                    ciclo_plan=ciclo,
                    creditos=cred,
                    es_prioritaria=True,
                )
            )
    db.flush()

    for tema_id, asig_id, nom, desc, unidad in [
        (1, 1, "Límites Notables y Asíntotas", "Límites algebraicos, notables y cálculo de asíntotas.", 1),
        (2, 1, "Derivadas y Regla de la Cadena", "Derivadas algebraicas y aplicaciones.", 2),
        (9, 3, "Notación Asintótica y Complejidad", "Big-O, análisis de algoritmos.", 1),
    ]:
        existing_tema = db.query(TemaConceptual).filter(TemaConceptual.id_tema == tema_id).first()
        if not existing_tema:
            db.add(
                TemaConceptual(
                    id_tema=tema_id,
                    id_asignatura=asig_id,
                    nombre_tema=nom,
                    descripcion_silabo=desc,
                    unidad_silabica=unidad,
                    estado_activo=True,
                )
            )
    db.flush()

    # 2. Roles Institucionales (Idempotente)
    roles_data = {
        1: ("mentoreado", "Estudiante mentoreado"),
        2: ("mentor", "Mentor académico con mérito"),
        3: ("administrador", "Administrador de tutoría"),
    }
    for r_id, (r_name, r_desc) in roles_data.items():
        existing_rol = db.query(Rol).filter((Rol.id_rol == r_id) | (Rol.nombre_rol == r_name)).first()
        if not existing_rol:
            db.add(Rol(id_rol=r_id, nombre_rol=r_name, descripcion=r_desc))
    db.flush()

    # 3. Cuentas de Demostración Aisladas
    emails = {
        "student": "estudiante.demo@upt.pe",
        "mentor": "mentor.demo@upt.pe",
        "admin": "admin.demo@upt.pe",
        "peer_student": "companero.demo@upt.pe",
        # Cuentas institucionales estándar para pruebas de presentación
        "student_std": "2022074255@upt.pe",
        "mentor_std": "2022073504@upt.pe",
        "admin_std": "admin.epis@upt.pe",
    }

    # Asignación de Roles Idempotente
    user_roles = [
        (emails["student"], [1]),
        (emails["mentor"], [1, 2]),
        (emails["admin"], [3]),
        (emails["peer_student"], [1]),
        (emails["student_std"], [1]),
        (emails["mentor_std"], [1, 2]),
        (emails["admin_std"], [3]),
    ]
    for em, r_list in user_roles:
        for r_id in r_list:
            existing_ur = (
                db.query(UsuarioRol).filter(UsuarioRol.email == em, UsuarioRol.id_rol == r_id).first()
            )
            if not existing_ur:
                db.add(UsuarioRol(email=em, id_rol=r_id, activo=True, asignado_por="demo_system"))
            else:
                existing_ur.activo = True

    # Consentimientos Informados (Ley N° 29733 / RN-02)
    for em in emails.values():
        existing_c = db.query(ConsentimientoLegal).filter(ConsentimientoLegal.email == em).first()
        if not existing_c:
            db.add(
                ConsentimientoLegal(
                    email=em,
                    terms_version="2026-II-DEMO-v1.0",
                    accepted=True,
                    ip_address="127.0.0.1",
                    user_agent="DemoEnvironmentScaffold",
                )
            )

    # Perfiles Académicos (RN-03 mérito)
    demo_profiles = [
        (
            emails["student"],
            "2024010001",
            "Estudiante",
            "Demostrativo Mentoreado",
            3,
            "mentoreado",
            [1, 3],
            [1, 2, 9],
            "Estudiante de tercer ciclo requiriendo apoyo en límites de Cálculo I.",
            "presencial",
        ),
        (
            emails["mentor"],
            "2022010002",
            "Mentor",
            "Demostrativo Acreditado",
            8,
            "mentor",
            [1, 3],
            [1, 2, 9, 10],
            "Mentor de octavo ciclo con rendimiento sobresaliente.",
            "presencial",
        ),
        (
            emails["admin"],
            "ADM-2026",
            "Coordinador",
            "Tutoría EPIS",
            10,
            "administrador",
            [1, 3],
            [1, 9],
            "Coordinación del programa de mentorías académicas P2P.",
            "presencial",
        ),
        (
            emails["peer_student"],
            "2022010003",
            "Compañero",
            "Demostrativo Elegible",
            7,
            "mentoreado",
            [1, 3],
            [1, 9],
            "Estudiante de séptimo ciclo con mérito académico para promoción a mentor.",
            "presencial",
        ),
        (
            emails["student_std"],
            "2022074255",
            "Joan Cristian",
            "Medina Quispe",
            6,
            "mentoreado",
            [1, 3],
            [1, 2, 9],
            "Estudiante de VI ciclo interesado en nivelación en Cálculo I y Algoritmos.",
            "presencial",
        ),
        (
            emails["mentor_std"],
            "2022073504",
            "Renzo Antonio",
            "Antayhua Mamani",
            7,
            "mentor",
            [1, 3],
            [1, 2, 9, 10],
            "Estudiante de VII ciclo con especialización en Algoritmos y Estructuras de Datos.",
            "presencial",
        ),
        (
            emails["admin_std"],
            "admin.epis",
            "Administrador",
            "EPIS-UPT",
            10,
            "administrador",
            [1, 3],
            [1, 9],
            "Administración del Sistema Web P2P EPIS-UPT.",
            "presencial",
        ),
    ]

    for em, cod, nom, ape, ciclo, rol_post, mats, tems, bio, mod in demo_profiles:
        existing_prof = db.query(PerfilAcademico).filter(PerfilAcademico.email == em).first()
        if not existing_prof:
            db.add(
                PerfilAcademico(
                    email=em,
                    codigo_estudiante=cod,
                    nombres=nom,
                    apellidos=ape,
                    ciclo_actual=ciclo,
                    rol_postulacion=rol_post,
                    materias_interes=mats,
                    temas_seleccionados=tems,
                    biografia=bio,
                    modalidad_preferida=mod,
                )
            )

    # Disponibilidad horaria para los mentores
    for mentor_em in [emails["mentor"], emails["mentor_std"]]:
        slots = [(1, "14:00", "16:00"), (3, "14:00", "16:00"), (5, "10:00", "12:00")]
        for dia, h_ini, h_fin in slots:
            existing_d = (
                db.query(DisponibilidadHoraria)
                .filter(
                    DisponibilidadHoraria.email == mentor_em,
                    DisponibilidadHoraria.dia_semana == dia,
                    DisponibilidadHoraria.hora_inicio == h_ini,
                )
                .first()
            )
            if not existing_d:
                db.add(
                    DisponibilidadHoraria(
                        email=mentor_em,
                        dia_semana=dia,
                        hora_inicio=h_ini,
                        hora_fin=h_fin,
                    )
                )
    db.flush()

    # -------------------------------------------------------------------------
    # ESCENARIOS DE DEMOSTRACIÓN DE SESIONES Y RESERVAS (DEMO-01 a DEMO-06)
    # -------------------------------------------------------------------------
    demo_session_ids = [101, 102, 103, 104, 105]

    # Limpieza idempotente previa de sesiones demo existentes
    db.query(TokenAsistenciaActivo).filter(TokenAsistenciaActivo.id_sesion.in_(demo_session_ids)).delete(
        synchronize_session=False
    )
    db.query(BitacoraPedagogica).filter(BitacoraPedagogica.id_sesion.in_(demo_session_ids)).delete(
        synchronize_session=False
    )
    db.query(AsistenciaSesion).filter(AsistenciaSesion.id_sesion.in_(demo_session_ids)).delete(
        synchronize_session=False
    )
    db.query(ReservaCupo).filter(ReservaCupo.id_sesion.in_(demo_session_ids)).delete(
        synchronize_session=False
    )
    db.query(SesionMentoria).filter(SesionMentoria.id_sesion.in_(demo_session_ids)).delete(
        synchronize_session=False
    )
    db.flush()

    # DEMO-01 / DEMO-02: Oferta futura publicada con antelación > 24h (RN-04)
    t_demo_02 = now + timedelta(days=3)
    sesion_02 = SesionMentoria(
        id_sesion=101,
        codigo_sesion="SES-DEMO-PUB01",
        mentor_email=emails["mentor"],
        id_asignatura=1,
        id_tema=1,
        fecha_inicio=t_demo_02,
        duracion_minutos=60,
        modalidad="presencial",
        aforo_maximo=10,
        espacio_asignado="Aula 201 - Pabellón EPIS",
        estado="PUBLICADA",
    )

    # DEMO-03 / DEMO-04: Sesión en Quórum Insuficiente en T-24h (restan 10h, 2 de 10 ratificados)
    t_demo_03 = now + timedelta(hours=10)
    sesion_03 = SesionMentoria(
        id_sesion=102,
        codigo_sesion="SES-DEMO-Q01",
        mentor_email=emails["mentor"],
        id_asignatura=1,
        id_tema=1,
        fecha_inicio=t_demo_03,
        duracion_minutos=60,
        modalidad="presencial",
        aforo_maximo=10,
        espacio_asignado="Lab 101 - EPIS",
        estado="QUORUM_INSUFICIENTE",
    )

    # DEMO-04 / DEMO-05: Sesión Confirmada en curso para Asistencia QR TOTP
    t_demo_04_start = now - timedelta(minutes=15)
    sesion_04 = SesionMentoria(
        id_sesion=103,
        codigo_sesion="SES-DEMO-ASIS01",
        mentor_email=emails["mentor"],
        id_asignatura=1,
        id_tema=1,
        fecha_inicio=t_demo_04_start,
        duracion_minutos=60,
        modalidad="presencial",
        aforo_maximo=10,
        espacio_asignado="Lab 102 - EPIS",
        estado="CONFIRMADA",
    )

    # DEMO-05 / DEMO-06: Sesión Concluida hace 2 horas para Bitácora (< 48h RN-12)
    t_demo_05_start = now - timedelta(hours=3)
    sesion_05 = SesionMentoria(
        id_sesion=104,
        codigo_sesion="SES-DEMO-BIT01",
        mentor_email=emails["mentor"],
        id_asignatura=1,
        id_tema=1,
        fecha_inicio=t_demo_05_start,
        duracion_minutos=90,
        modalidad="presencial",
        aforo_maximo=10,
        espacio_asignado="Lab 103 - EPIS",
        estado="CONCLUIDA",
    )

    # DEMO-06: Sesión en T-24h para evaluación administrativa de quórum
    t_demo_06_start = now + timedelta(hours=12)
    sesion_06 = SesionMentoria(
        id_sesion=105,
        codigo_sesion="SES-DEMO-ADMIN01",
        mentor_email=emails["mentor"],
        id_asignatura=3,
        id_tema=9,
        fecha_inicio=t_demo_06_start,
        duracion_minutos=60,
        modalidad="presencial",
        aforo_maximo=10,
        espacio_asignado="Aula 301 - Pabellón EPIS",
        estado="PUBLICADA",
    )

    db.add_all([sesion_02, sesion_03, sesion_04, sesion_05, sesion_06])
    db.flush()

    # Reservas asociadas
    # DEMO-01: Reserva del estudiante en la sesión publicada (pendiente de confirmación)
    reserva_01 = ReservaCupo(
        id_reserva=201,
        codigo_reserva="RES-DEMO-001",
        id_sesion=101,
        estudiante_email=emails["student"],
        fecha_reserva=now - timedelta(hours=2),
        estado="PENDIENTE_CONFIRMACION",
    )

    # Reservas en la sesión DEMO-03 (quórum bajo: 2 ratificadas < 50%)
    reserva_q1 = ReservaCupo(
        id_reserva=202,
        codigo_reserva="RES-DEMO-Q01",
        id_sesion=102,
        estudiante_email=emails["student"],
        fecha_reserva=now - timedelta(hours=30),
        fecha_ratificacion=now - timedelta(hours=26),
        estado="CONFIRMADA",
    )
    reserva_q2 = ReservaCupo(
        id_reserva=203,
        codigo_reserva="RES-DEMO-Q02",
        id_sesion=102,
        estudiante_email=emails["peer_student"],
        fecha_reserva=now - timedelta(hours=30),
        fecha_ratificacion=now - timedelta(hours=25),
        estado="CONFIRMADA",
    )

    # Reserva en DEMO-04 (confirmada, lista para checkin)
    reserva_asis = ReservaCupo(
        id_reserva=204,
        codigo_reserva="RES-DEMO-ASIS01",
        id_sesion=103,
        estudiante_email=emails["student"],
        fecha_reserva=now - timedelta(days=2),
        fecha_ratificacion=now - timedelta(days=1),
        estado="CONFIRMADA",
    )

    # Reservas y asistencia en DEMO-05 (concluida con asistencia confirmada)
    reserva_bit = ReservaCupo(
        id_reserva=205,
        codigo_reserva="RES-DEMO-BIT01",
        id_sesion=104,
        estudiante_email=emails["student"],
        fecha_reserva=now - timedelta(days=3),
        fecha_ratificacion=now - timedelta(days=2),
        estado="ASISTIDA",
    )

    db.add_all([reserva_01, reserva_q1, reserva_q2, reserva_asis, reserva_bit])
    db.flush()

    # DEMO-05: Token de asistencia activo (TOTP QR de 6 dígitos)
    token_demo_05 = TokenAsistenciaActivo(
        id_sesion=103,
        token=hashlib.sha256(b"DEMO-TOKEN-ASIS-SESION-103").hexdigest(),
        totp_code="654321",
        expires_at=now + timedelta(minutes=45),
    )
    db.add(token_demo_05)

    # DEMO-06: Asistencia ya registrada en sesión concluida DEMO-05
    asist_bit = AsistenciaSesion(
        id_sesion=104,
        estudiante_email=emails["student"],
        asistio=True,
        fecha_checkin=now - timedelta(hours=2, minutes=45),
        ip_origen="127.0.0.1",
    )
    db.add(asist_bit)

    # DEMO-06: Bitácora Pedagógica con Hash de Integridad SHA-256
    hash_bitacora = hashlib.sha256(
        f"SES-DEMO-BIT01:{emails['mentor']}:1.5:{now.strftime('%Y-%m-%d')}".encode()
    ).hexdigest()
    bitacora_demo = BitacoraPedagogica(
        id_sesion=104,
        id_mentor=emails["mentor"],
        temas_cubiertos=["Límites Notables y Cálculo de Asíntotas"],
        observaciones="Sesión de reforzamiento presencial completada exitosamente con participación activa y resolución de ejercicios.",
        nivel_dificultad="Medio",
        hash_firma=hash_bitacora,
        horas_declaradas=1.5,
        visado_administrador=False,
    )
    db.add(bitacora_demo)
    db.flush()

    # Sincronización automática de secuencias en PostgreSQL
    if db.bind and db.bind.dialect.name == "postgresql":
        find_seqs_sql = """
        SELECT c.table_name, c.column_name, pg_get_serial_sequence(c.table_name, c.column_name) AS seq_name
        FROM information_schema.tables t
        JOIN information_schema.columns c ON t.table_name = c.table_name AND t.table_schema = c.table_schema
        WHERE t.table_schema = 'public' AND t.table_type = 'BASE TABLE'
          AND pg_get_serial_sequence(c.table_name, c.column_name) IS NOT NULL;
        """
        for table_name, col_name, seq_name in db.execute(text(find_seqs_sql)).fetchall():
            max_val = db.execute(text(f"SELECT COALESCE(MAX({col_name}), 0) FROM {table_name}")).scalar()
            if max_val and max_val > 0:
                db.execute(text(f"SELECT setval('{seq_name}', {max_val}, true)"))

    db.commit()

    return {
        "status": "success",
        "scenarios": {
            "DEMO-01": {"user": emails["student"], "reserva_id": 201, "sesion_id": 101},
            "DEMO-02": {"mentor": emails["mentor"], "sesion_id": 101, "aforo": 10, "estado": "PUBLICADA"},
            "DEMO-03": {"sesion_id": 102, "estado": "QUORUM_INSUFICIENTE", "confirmados": 2, "aforo": 10},
            "DEMO-04": {"sesion_id": 103, "estado": "CONFIRMADA", "en_curso": True},
            "DEMO-05": {"sesion_id": 103, "totp_code": "654321", "token_activo": True},
            "DEMO-06": {
                "sesion_id": 104,
                "estado": "CONCLUIDA",
                "bitacora": True,
                "hash_firma": hash_bitacora,
                "admin": emails["admin"],
            },
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Preparación de escenarios reproducibles DEMO-01 a DEMO-06 en base de datos local."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula la preparación de datos en memoria sin persistir.",
    )
    parser.add_argument(
        "--db-url",
        default=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://postgres:demo_p2p_secret_2026@127.0.0.1:5432/p2p_demo_db",
        ),
        help="URL de conexión SQLAlchemy a la base de datos de demostración.",
    )
    parser.add_argument(
        "--sqlite-path",
        default=None,
        help="URL de conexión SQLite alternativa (ej: sqlite:///demo_epis_p2p.db).",
    )
    args = parser.parse_args()

    if args.dry_run:
        target_url = "sqlite:///:memory:"
    elif args.sqlite_path:
        target_url = args.sqlite_path
    else:
        target_url = args.db_url

    # Validación de seguridad: no apuntar a producción remota
    lower_url = target_url.lower()
    if "supabase.co" in lower_url or "aws" in lower_url or "pooler" in lower_url:
        print(
            "[-] ERROR DE SEGURIDAD: No está permitido ejecutar este script contra instancias remotas o de producción.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        f"[*] Inicializando base de datos de demostración en: {target_url.split('@')[-1] if '@' in target_url else target_url}"
    )

    connect_args = {"check_same_thread": False} if "sqlite" in target_url else {}
    engine = create_engine(target_url, connect_args=connect_args)

    if "sqlite" in target_url:
        Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        summary = prepare_demo_fixtures(db)
        print("[+] Escenarios de demostración aprovisionados satisfactoriamente:")
        for sc_name, sc_data in summary["scenarios"].items():
            print(f"    - {sc_name}: {sc_data}")
        if args.dry_run:
            print("[*] Modo --dry-run ejecutado: los datos residieron exclusivamente en memoria.")
    except Exception as exc:
        print(f"[-] Error preparando escenarios de demostración: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
