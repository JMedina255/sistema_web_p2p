"""
Script seguro y reproducible de preparación de escenarios de demostración institucional (DEMO-01 a DEMO-06).
EPIS-UPT - Sistema Web P2P de Mentorías Académicas.

Restricciones de seguridad y aislamiento:
- Operación sobre base de datos local SQLite desechable o modo memoria.
- NO modifica bases de datos en la nube (Supabase / PostgreSQL institucional).
- NO utiliza credenciales personales ni correos institucionales reales.
- Admite ejecución en modo '--dry-run' para inspección sin escrituras persistentes.
"""

import argparse
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

# Asegurar que el directorio aplicacion/backend esté en sys.path para ejecución directa
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import Session, sessionmaker  # noqa: E402

from app.db.session import Base  # noqa: E402
from app.models.attendance import AsistenciaSesion  # noqa: E402
from app.models.booking import ReservaCupo  # noqa: E402
from app.models.consent import ConsentimientoLegal  # noqa: E402
from app.models.curriculum import Asignatura, TemaConceptual  # noqa: E402
from app.models.offer import SesionMentoria  # noqa: E402
from app.models.profile import DisponibilidadHoraria, PerfilAcademico  # noqa: E402
from app.models.roles import Rol, UsuarioRol  # noqa: E402


def prepare_demo_fixtures(db: Session) -> dict:
    """
    Puebla la base de datos aislada con los seis escenarios mínimos de demostración:
    - DEMO-01: Estudiante mentoreado accede, consulta catálogo y administra su reserva.
    - DEMO-02: Mentor acreditado publica y administra su oferta con fecha futura > 24h.
    - DEMO-03: Sesión en estado 'QUORUM_INSUFICIENTE' para verificar decisión del mentor (PROCEED/RESCHEDULE/CANCEL).
    - DEMO-04: Sesión en estado 'CONFIRMADA' en ventana de ejecución lista para generar QR TOTP y registrar asistencia.
    - DEMO-05: Sesión 'CONCLUIDA' dentro de la ventana de 48h lista para registro de bitácora pedagógica (RN-12).
    - DEMO-06: Administrador institucional acreditado para supervisión, auditoría y evaluación de quórum.
    """
    now = datetime.now(UTC)

    # 1. Catálogo Curricular Básico (Malla EPIS-UPT)
    asig_calc = Asignatura(
        id_asignatura=1,
        codigo_curso="CALC-101",
        nombre_curso="Cálculo I",
        ciclo_plan=1,
        creditos=4,
        es_prioritaria=True,
    )
    asig_algo = Asignatura(
        id_asignatura=2,
        codigo_curso="ALGO-102",
        nombre_curso="Algoritmos y Estructuras de Datos",
        ciclo_plan=2,
        creditos=4,
        es_prioritaria=True,
    )
    db.add_all([asig_calc, asig_algo])
    db.flush()

    tema_lim = TemaConceptual(
        id_tema=1,
        id_asignatura=1,
        nombre_tema="Límites Notables y Asíntotas",
        descripcion_silabo="Límites algebraicos, notables y cálculo de asíntotas.",
        unidad_silabica=1,
        estado_activo=True,
    )
    db.add(tema_lim)
    db.flush()

    # 2. Roles Institucionales
    rol_mentoreado = Rol(id_rol=1, nombre_rol="mentoreado", descripcion="Estudiante mentoreado")
    rol_mentor = Rol(id_rol=2, nombre_rol="mentor", descripcion="Mentor académico con mérito")
    rol_admin = Rol(id_rol=3, nombre_rol="administrador", descripcion="Administrador de tutoría")
    db.add_all([rol_mentoreado, rol_mentor, rol_admin])
    db.flush()

    # 3. Cuentas de Demostración Aisladas
    emails = {
        "student": "estudiante.demo@upt.pe",
        "mentor": "mentor.demo@upt.pe",
        "admin": "admin.demo@upt.pe",
        "peer_student": "companero.demo@upt.pe",
    }

    # Asignación de Roles
    db.add_all(
        [
            UsuarioRol(email=emails["student"], id_rol=1, activo=True, asignado_por="demo_system"),
            UsuarioRol(email=emails["mentor"], id_rol=2, activo=True, asignado_por="demo_system"),
            UsuarioRol(email=emails["mentor"], id_rol=1, activo=True, asignado_por="demo_system"),
            UsuarioRol(email=emails["admin"], id_rol=3, activo=True, asignado_por="demo_system"),
            UsuarioRol(email=emails["peer_student"], id_rol=1, activo=True, asignado_por="demo_system"),
        ]
    )

    # Consentimientos Informados (Ley N° 29733 / RN-02)
    for em in emails.values():
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
    db.add_all(
        [
            PerfilAcademico(
                email=emails["student"],
                codigo_estudiante="2024010001",
                nombres="Estudiante",
                apellidos="Demostrativo Mentoreado",
                ciclo_actual=3,
                rol_postulacion="mentoreado",
                materias_interes=[1, 2],
                temas_seleccionados=[1],
                biografia="Estudiante de tercer ciclo requiriendo apoyo en límites de Cálculo I.",
                modalidad_preferida="presencial",
            ),
            PerfilAcademico(
                email=emails["mentor"],
                codigo_estudiante="2022010002",
                nombres="Mentor",
                apellidos="Demostrativo Acreditado",
                ciclo_actual=8,  # Cumple RN-03 (>= VII ciclo)
                rol_postulacion="mentor",
                materias_interes=[1],
                temas_seleccionados=[1],
                biografia="Mentor de octavo ciclo con rendimiento sobresaliente.",
                modalidad_preferida="presencial",
            ),
            PerfilAcademico(
                email=emails["admin"],
                codigo_estudiante="ADM-2026",
                nombres="Coordinador",
                apellidos="Tutoría EPIS",
                ciclo_actual=10,
                rol_postulacion="administrador",
                materias_interes=[1, 2],
                temas_seleccionados=[1],
                biografia="Coordinación del programa de mentorías académicas P2P.",
                modalidad_preferida="presencial",
            ),
        ]
    )

    # Disponibilidad horaria para el mentor (Lunes y Miércoles 14:00-16:00)
    db.add_all(
        [
            DisponibilidadHoraria(
                email=emails["mentor"],
                dia_semana=1,
                hora_inicio="14:00",
                hora_fin="16:00",
            ),
            DisponibilidadHoraria(
                email=emails["mentor"],
                dia_semana=3,
                hora_inicio="14:00",
                hora_fin="16:00",
            ),
        ]
    )
    db.flush()

    # -------------------------------------------------------------------------
    # ESCENARIOS DE DEMOSTRACIÓN DE SESIONES Y RESERVAS
    # -------------------------------------------------------------------------

    # DEMO-02: Oferta futura publicada con antelación > 24h (RN-04)
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

    # DEMO-03: Sesión en Quórum Insuficiente en T-24h (restan 10h, 2 de 10 ratificados)
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

    # DEMO-04: Sesión Confirmada en ventana de ejecución para Asistencia QR
    t_demo_04_start = now - timedelta(minutes=10)  # Inició hace 10 min
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

    # DEMO-05: Sesión Concluida hace 2 horas para Bitácora (< 48h RN-12)
    t_demo_05_start = now - timedelta(hours=3)
    sesion_05 = SesionMentoria(
        id_sesion=104,
        codigo_sesion="SES-DEMO-BIT01",
        mentor_email=emails["mentor"],
        id_asignatura=1,
        id_tema=1,
        fecha_inicio=t_demo_05_start,
        duracion_minutos=60,
        modalidad="presencial",
        aforo_maximo=10,
        espacio_asignado="Lab 103 - EPIS",
        estado="CONCLUIDA",
    )

    db.add_all([sesion_02, sesion_03, sesion_04, sesion_05])
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
        estado="CONFIRMADA",
    )

    db.add_all([reserva_01, reserva_q1, reserva_q2, reserva_asis, reserva_bit])
    db.flush()

    # Asistencia ya registrada en sesión concluida DEMO-05
    asist_bit = AsistenciaSesion(
        id_sesion=104,
        estudiante_email=emails["student"],
        asistio=True,
        fecha_checkin=now - timedelta(hours=2, minutes=45),
        ip_origen="127.0.0.1",
    )
    db.add(asist_bit)
    db.commit()

    return {
        "status": "success",
        "scenarios": {
            "DEMO-01": {"user": emails["student"], "reserva_id": 201, "sesion_id": 101},
            "DEMO-02": {"mentor": emails["mentor"], "sesion_id": 101, "aforo": 10},
            "DEMO-03": {"sesion_id": 102, "estado": "QUORUM_INSUFICIENTE", "confirmados": 2, "aforo": 10},
            "DEMO-04": {"sesion_id": 103, "estado": "CONFIRMADA", "en_curso": True},
            "DEMO-05": {"sesion_id": 104, "estado": "CONCLUIDA", "horas_desde_fin": 2},
            "DEMO-06": {"admin": emails["admin"], "capacidades": ["quorum_eval", "audit_roles"]},
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Preparación de escenarios reproducibles DEMO-01 a DEMO-06 en base de datos aislada."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula la preparación de datos en memoria sin persistir archivos en disco.",
    )
    parser.add_argument(
        "--sqlite-path",
        default="sqlite:///demo_epis_p2p.db",
        help="URL de conexión SQLite aislada (por defecto 'sqlite:///demo_epis_p2p.db').",
    )
    args = parser.parse_args()

    db_url = "sqlite:///:memory:" if args.dry_run else args.sqlite_path
    print(f"[*] Inicializando base de datos de demostración aislada en: {db_url}")

    engine = create_engine(db_url, connect_args={"check_same_thread": False} if "sqlite" in db_url else {})
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        summary = prepare_demo_fixtures(db)
        print("[+] Escenarios de demostración preparados satisfactoriamente:")
        for sc_name, sc_data in summary["scenarios"].items():
            print(f"    - {sc_name}: {sc_data}")
        if args.dry_run:
            print(
                "[*] Modo --dry-run ejecutado: los datos residieron exclusivamente en memoria y han sido liberados."
            )
        else:
            print(f"[+] Archivo de demostración generado localmente: {args.sqlite_path}")
    except Exception as exc:
        print(f"[-] Error preparando escenarios de demostración: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
