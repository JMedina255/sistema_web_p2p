"""
Script Reproducible de Aprovisionamiento de Fixtures de Demostración (T-50 / RNF10).
Sistema Web P2P de Mentorías Académicas — EPIS UPT.

Puebla el entorno con cuentas oficiales e institucionales de Google Workspace (@virtual.upt.pe)
y realiza el aprovisionamiento idempotente del ciclo de vida formativo completo.
"""

from datetime import UTC, datetime, timedelta
import hashlib

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from app.db.session import Base, get_engine, get_session
from app.models.attendance import AsistenciaSesion
from app.models.bitacora import BitacoraPedagogica
from app.models.booking import ReservaCupo, SolicitudDemanda
from app.models.certificate import CertificadoHoras
from app.models.consent import ConsentimientoLegal
from app.models.offer import SesionMentoria
from app.models.profile import DisponibilidadHoraria, PerfilAcademico
from app.models.roles import Rol, UsuarioRol
from app.models.survey import EncuestaCalidad


def seed_lifecycle_data(db, now: datetime):
    """
    Aprovisionamiento idempotente del ciclo de vida para tablas nucleares
    que registran 0 filas en Supabase / PostgreSQL.
    """
    print("[DEMO_SEED] 5. Aprovisionando datos del ciclo de vida (reservas, demandas, asistencias, encuestas, certificados)...")

    # A. Solicitudes de demanda académica
    if db.query(SolicitudDemanda).count() == 0:
        demandas = [
            SolicitudDemanda(
                id_demanda=1,
                id_asignatura=1,
                id_tema=1,
                estudiante_email="ra2022073504@virtual.upt.pe",
                observaciones="Requiero asesoría previa para la práctica calificada de límites algebraicos y notables.",
                estado="PENDIENTE",
                created_at=now - timedelta(days=5),
            ),
            SolicitudDemanda(
                id_demanda=2,
                id_asignatura=3,
                id_tema=9,
                estudiante_email="mentoreado@upt.pe",
                observaciones="Refuerzo en recursividad y balanceo de árboles AVL.",
                estado="ATENDIDA",
                created_at=now - timedelta(days=10),
            ),
        ]
        db.add_all(demandas)
        db.commit()
        print("  ✓ Solicitudes de demanda académica sembradas.")

    # B. Reservas de cupo para sesiones concluidas
    if db.query(ReservaCupo).count() == 0:
        reservas = []
        for i in range(1, 23):
            session_id = 9000 + i
            reservas.append(
                ReservaCupo(
                    codigo_reserva=f"RES-2026-II-{session_id:04d}-01",
                    id_sesion=session_id,
                    estudiante_email="ra2022073504@virtual.upt.pe",
                    estado="ASISTIDA",
                    fecha_reserva=now - timedelta(days=32 - i),
                    fecha_ratificacion=now - timedelta(days=31 - i),
                    ticket_hash=hashlib.sha256(f"ticket_{session_id}_ra".encode()).hexdigest(),
                    created_at=now - timedelta(days=32 - i),
                    updated_at=now - timedelta(days=30 - i),
                )
            )
            reservas.append(
                ReservaCupo(
                    codigo_reserva=f"RES-2026-II-{session_id:04d}-02",
                    id_sesion=session_id,
                    estudiante_email="mentoreado@upt.pe",
                    estado="ASISTIDA",
                    fecha_reserva=now - timedelta(days=32 - i),
                    fecha_ratificacion=now - timedelta(days=31 - i),
                    ticket_hash=hashlib.sha256(f"ticket_{session_id}_legacy".encode()).hexdigest(),
                    created_at=now - timedelta(days=32 - i),
                    updated_at=now - timedelta(days=30 - i),
                )
            )
        db.add_all(reservas)
        db.commit()
        print(f"  ✓ {len(reservas)} Reservas de cupo sembradas en estado ASISTIDA.")

    # C. Asistencias a sesiones concluidas
    if db.query(AsistenciaSesion).count() == 0:
        asistencias = []
        for i in range(1, 23):
            session_id = 9000 + i
            past_time = now - timedelta(days=30 - i, hours=4)
            asistencias.append(
                AsistenciaSesion(
                    id_sesion=session_id,
                    estudiante_email="ra2022073504@virtual.upt.pe",
                    asistio=True,
                    fecha_checkin=past_time + timedelta(minutes=5),
                    ip_origen="190.119.180.25",
                    created_at=past_time,
                )
            )
            asistencias.append(
                AsistenciaSesion(
                    id_sesion=session_id,
                    estudiante_email="mentoreado@upt.pe",
                    asistio=True,
                    fecha_checkin=past_time + timedelta(minutes=8),
                    ip_origen="190.119.180.26",
                    created_at=past_time,
                )
            )
        db.add_all(asistencias)
        db.commit()
        print(f"  ✓ {len(asistencias)} Asistencias efectivas sembradas.")

    # D. Encuestas de calidad post-mentoría
    if db.query(EncuestaCalidad).count() == 0:
        encuestas = []
        for i in range(1, 23):
            session_id = 9000 + i
            encuestas.append(
                EncuestaCalidad(
                    id_sesion=session_id,
                    estudiante_email="ra2022073504@virtual.upt.pe",
                    calificacion_general=5,
                    dominio_tema=5,
                    claridad_explicacion=5,
                    puntualidad=5,
                    comentarios=f"Excelente explicación en la sesión formativa #{i}. Muy claros los ejemplos prácticos.",
                    created_at=now - timedelta(days=30 - i, hours=2),
                )
            )
        db.add_all(encuestas)
        db.commit()
        print(f"  ✓ {len(encuestas)} Encuestas de satisfacción y calidad sembradas.")

    # E. Certificado de horas oficial emitido
    if db.query(CertificadoHoras).count() == 0:
        cert = CertificadoHoras(
            id_mentor="jm2022074255@virtual.upt.pe",
            codigo_folio="CERT-2026-II-0001",
            periodo_academico="2026-II",
            horas_acreditadas=22.0,
            hash_firma=hashlib.sha256("CERT-2026-II-0001-VERIFIED-UPT".encode()).hexdigest(),
            estado="EMITIDO",
            created_at=now - timedelta(days=1),
        )
        db.add(cert)
        # Certificado también para alias mentor@upt.pe de compatibilidad
        cert_legacy = CertificadoHoras(
            id_mentor="mentor@upt.pe",
            codigo_folio="CERT-2026-II-0002",
            periodo_academico="2026-II",
            horas_acreditadas=22.0,
            hash_firma=hashlib.sha256("CERT-2026-II-0002-VERIFIED-UPT".encode()).hexdigest(),
            estado="EMITIDO",
            created_at=now - timedelta(days=1),
        )
        db.add(cert_legacy)
        db.commit()
        print("  ✓ Certificados oficiales de acreditación sembrados.")


def seed_demo_environment():
    engine = get_engine()
    if engine is None:
        print("[DEMO_SEED] Base de datos relacional no disponible. Saltando aprovisionamiento físico.")
        return

    Base.metadata.create_all(engine)

    # Asegurar compatibilidad de esquema y restricciones en bases relacionales preexistentes (PostgreSQL/SQLite)
    with engine.begin() as conn:
        try:
            conn.execute(
                text(
                    "ALTER TABLE sesiones_mentoria DROP CONSTRAINT IF EXISTS chk_sesion_estado;"
                )
            )
            conn.execute(
                text(
                    "ALTER TABLE sesiones_mentoria ADD CONSTRAINT chk_sesion_estado "
                    "CHECK (estado IN ('BORRADOR', 'PUBLICADA', 'CONFIRMADA', 'EN_CURSO', "
                    "'COMPLETADA', 'FINALIZADA', 'CANCELADA_QUORUM', 'CANCELADA_MENTOR', "
                    "'CANCELADA_ADMIN', 'RECHAZADA', 'EXPIRADA', 'EN_EVALUACION', 'AUDITADA', 'HORAS_VISADAS'));"
                )
            )
        except Exception:
            pass

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    now = datetime.now(UTC)

    try:
        print("[DEMO_SEED] 1. Aprovisionando roles del sistema...")
        roles_data = {
            "mentoreado": "Estudiante de pregrado con requerimientos de reforzamiento académico.",
            "mentor": "Estudiante avanzado (>= VII ciclo) acreditado para dictar mentorías.",
            "administrador": "Dirección de Escuela EPIS con facultades de auditoría y visado.",
        }
        db_roles = {}
        for r_name, r_desc in roles_data.items():
            r_obj = db.query(Rol).filter(Rol.nombre_rol == r_name).first()
            if not r_obj:
                r_obj = Rol(nombre_rol=r_name, descripcion=r_desc)
                db.add(r_obj)
                db.commit()
                db.refresh(r_obj)
            db_roles[r_name] = r_obj

        print("[DEMO_SEED] 2. Configurando cuentas y roles institucionales (@virtual.upt.pe y @upt.pe)...")
        users = [
            # Cuentas institucionales reales con el nuevo estándar de correo
            ("ra2022073504@virtual.upt.pe", ["mentoreado"]),
            ("jm2022074255@virtual.upt.pe", ["mentor", "mentoreado"]),
            ("admin.epis@upt.pe", ["administrador"]),
            # Cuentas legacy de pruebas para no alterar tests previos
            ("mentoreado@upt.pe", ["mentoreado"]),
            ("mentor@upt.pe", ["mentor", "mentoreado"]),
            ("admin@upt.pe", ["administrador", "mentoreado"]),
        ]
        for email, roles_list in users:
            for r_name in roles_list:
                rol_obj = db_roles[r_name]
                exist = (
                    db.query(UsuarioRol)
                    .filter(UsuarioRol.email == email, UsuarioRol.id_rol == rol_obj.id_rol)
                    .first()
                )
                if not exist:
                    db.add(
                        UsuarioRol(
                            email=email,
                            id_rol=rol_obj.id_rol,
                            fecha_asignacion=now,
                            asignado_por="seed_demo",
                            activo=True,
                        )
                    )
            # Consentimiento legal Ley 29733
            if not db.query(ConsentimientoLegal).filter(ConsentimientoLegal.email == email).first():
                db.add(
                    ConsentimientoLegal(
                        email=email,
                        terms_version="2026-II-v1.0",
                        accepted=True,
                        ip_address="127.0.0.1",
                        user_agent="DemoSeedScript",
                    )
                )
        db.commit()

        print("[DEMO_SEED] 3. Sembrando perfiles formativos y disponibilidades...")
        profiles = [
            {
                "email": "ra2022073504@virtual.upt.pe",
                "codigo_estudiante": "2022073504",
                "nombres": "Renzo Antonio",
                "apellidos": "Antayhua Mamani",
                "ciclo_actual": 3,
                "rol_postulacion": "mentoreado",
                "materias_interes": [1, 3],
                "temas_seleccionados": [1, 2, 9],
                "biografia": "Estudiante de la EPIS-UPT buscando asesoría académica en materias filtro.",
                "modalidad_preferida": "presencial",
            },
            {
                "email": "jm2022074255@virtual.upt.pe",
                "codigo_estudiante": "2022074255",
                "nombres": "Joan Cristian",
                "apellidos": "Medina Quispe",
                "ciclo_actual": 8,
                "rol_postulacion": "mentor",
                "materias_interes": [1, 3],
                "temas_seleccionados": [1, 2, 9, 10],
                "biografia": "Mentor acreditado de VIII ciclo. Especialidad en Estructuras de Datos y Algoritmos.",
                "modalidad_preferida": "presencial",
            },
            {
                "email": "admin.epis@upt.pe",
                "codigo_estudiante": "admin.epis",
                "nombres": "Dirección de Escuela",
                "apellidos": "EPIS UPT",
                "ciclo_actual": 10,
                "rol_postulacion": "administrador",
                "materias_interes": [1, 2, 3],
                "temas_seleccionados": [1, 5, 9],
                "biografia": "Dirección de la Escuela Profesional de Ingeniería de Sistemas.",
                "modalidad_preferida": "presencial",
            },
            {
                "email": "mentoreado@upt.pe",
                "codigo_estudiante": "2024071001",
                "nombres": "Ana Lucía",
                "apellidos": "Pérez Ramos",
                "ciclo_actual": 2,
                "rol_postulacion": "mentoreado",
                "materias_interes": [1, 3],
                "temas_seleccionados": [1, 2, 9],
                "biografia": "Estudiante de II ciclo con interés en nivelación en Cálculo I y Algoritmos.",
                "modalidad_preferida": "presencial",
            },
            {
                "email": "mentor@upt.pe",
                "codigo_estudiante": "2022073504",
                "nombres": "Renzo Antonio",
                "apellidos": "Antayhua Mamani",
                "ciclo_actual": 8,
                "rol_postulacion": "mentor",
                "materias_interes": [1, 3],
                "temas_seleccionados": [1, 2, 9, 10],
                "biografia": "Mentor acreditado de VIII ciclo. Especialidad en Estructuras de Datos y Algoritmos.",
                "modalidad_preferida": "presencial",
            },
            {
                "email": "admin@upt.pe",
                "codigo_estudiante": "admin.epis",
                "nombres": "Dirección de Escuela",
                "apellidos": "EPIS UPT",
                "ciclo_actual": 10,
                "rol_postulacion": "administrador",
                "materias_interes": [1, 2, 3],
                "temas_seleccionados": [1, 5, 9],
                "biografia": "Dirección de la Escuela Profesional de Ingeniería de Sistemas.",
                "modalidad_preferida": "presencial",
            },
        ]
        for p_data in profiles:
            p = db.query(PerfilAcademico).filter(PerfilAcademico.email == p_data["email"]).first()
            if not p:
                db.add(PerfilAcademico(**p_data))
        db.commit()

        # Disponibilidad horaria para mentores
        for mentor_e in ["jm2022074255@virtual.upt.pe", "mentor@upt.pe"]:
            if (
                db.query(DisponibilidadHoraria).filter(DisponibilidadHoraria.email == mentor_e).count()
                == 0
            ):
                slots = [
                    (1, "08:00", "09:00"),
                    (1, "09:00", "10:00"),
                    (3, "14:00", "15:00"),
                    (5, "10:00", "11:00"),
                ]
                for dia, h_ini, h_fin in slots:
                    db.add(
                        DisponibilidadHoraria(
                            email=mentor_e,
                            dia_semana=dia,
                            hora_inicio=h_ini,
                            hora_fin=h_fin,
                        )
                    )
                db.commit()

        print("[DEMO_SEED] 4. Aprovisionando sesiones y 22.0 horas formativas visadas...")
        for i in range(1, 23):
            session_id = 9000 + i
            sesion_exist = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == session_id).first()
            if not sesion_exist:
                past_time = now - timedelta(days=30 - i, hours=4)
                sesion = SesionMentoria(
                    id_sesion=session_id,
                    codigo_sesion=f"SES-DEMO-{session_id}",
                    mentor_email="jm2022074255@virtual.upt.pe",
                    id_asignatura=1,
                    id_tema=1,
                    fecha_inicio=past_time,
                    duracion_minutos=60,  # 1.0 hora
                    modalidad="presencial",
                    aforo_maximo=10,
                    espacio_asignado="Aula 204 - EPIS",
                    estado="HORAS_VISADAS",
                )
                db.add(sesion)
                db.commit()

                # Crear bitácora visada con 1.0 hora
                bitacora = BitacoraPedagogica(
                    id_sesion=session_id,
                    id_mentor="jm2022074255@virtual.upt.pe",
                    temas_cubiertos=[1, 2],
                    observaciones=f"Sesión formativa #{i} completada satisfactoriamente con asistencia plena y desarrollo temático exhaustivo de límites.",
                    nivel_dificultad="Medio",
                    hash_firma=f"hash_demo_visado_{session_id}",
                    horas_declaradas=1.0,
                    visado_administrador=True,
                    created_at=past_time + timedelta(hours=2),
                )
                db.add(bitacora)
                db.commit()

        # Aprovisionamiento del ciclo de vida (asistencias, encuestas, demandas, certificados)
        seed_lifecycle_data(db, now)

        # Sincronización automática de secuencias para prevenir UniqueViolation en claves primarias
        find_seqs_sql = """
        SELECT 
            c.table_name,
            c.column_name,
            pg_get_serial_sequence(c.table_name, c.column_name) AS seq_name
        FROM information_schema.tables t
        JOIN information_schema.columns c 
            ON t.table_name = c.table_name AND t.table_schema = c.table_schema
        WHERE t.table_schema = 'public'
          AND t.table_type = 'BASE TABLE'
          AND pg_get_serial_sequence(c.table_name, c.column_name) IS NOT NULL;
        """
        for table_name, col_name, seq_name in db.execute(text(find_seqs_sql)).fetchall():
            max_val = db.execute(text(f"SELECT COALESCE(MAX({col_name}), 0) FROM {table_name}")).scalar()
            if max_val > 0:
                db.execute(text(f"SELECT setval('{seq_name}', {max_val}, true)"))
        db.commit()

        print("[DEMO_SEED] ¡Entorno de demostración institucional aprovisionado con éxito!")
        print("[DEMO_SEED] Cuentas listas para demostración académica:")
        print("  - Mentoreado Oficial: ra2022073504@virtual.upt.pe (Renzo Antayhua - Código: 2022073504)")
        print("  - Mentor Oficial:     jm2022074255@virtual.upt.pe (Joan Medina - 22.0h visadas)")
        print("  - Admin EPIS:         admin.epis@upt.pe (Dirección de Escuela EPIS-UPT)")

    except Exception as e:
        db.rollback()
        print(f"[DEMO_SEED] Error durante el aprovisionamiento de fixtures: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_environment()
