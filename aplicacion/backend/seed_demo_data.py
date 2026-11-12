"""
Script Reproducible de Aprovisionamiento de Fixtures de Demostración (T-50 / RNF10).
Sistema Web P2P de Mentorías Académicas — EPIS UPT.

Puebla el entorno con cuentas oficiales para la demostración académica del MVP:
1. mentoreado@upt.pe: Estudiante de II ciclo con perfil, asignaturas críticas y reservas.
2. mentor@upt.pe: Estudiante de VIII ciclo con 22.0 horas visadas (listo para emitir constancia RN-14).
3. admin@upt.pe: Dirección de Escuela con privilegios para visado y gestión institucional.
"""

from datetime import UTC, datetime, timedelta

from sqlalchemy import text

from app.db.session import Base, get_engine, get_session
from app.models.bitacora import BitacoraPedagogica
from app.models.consent import ConsentimientoLegal
from app.models.offer import SesionMentoria
from app.models.profile import DisponibilidadHoraria, PerfilAcademico
from app.models.roles import Rol, UsuarioRol


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
                    "ALTER TABLE sesiones_mentoria ADD COLUMN IF NOT EXISTS quorumevaluated_at TIMESTAMP WITH TIME ZONE;"
                )
            )
        except Exception:
            pass
        try:
            conn.execute(text("ALTER TABLE sesiones_mentoria DROP CONSTRAINT IF EXISTS chk_sesion_estado;"))
            conn.execute(
                text("""
                ALTER TABLE sesiones_mentoria ADD CONSTRAINT chk_sesion_estado
                CHECK (estado IN (
                    'PUBLICADA', 'PENDIENTE_CONFIRMACION', 'QUORUM_INSUFICIENTE', 'CONFIRMADA',
                    'EN_CURSO', 'CONCLUIDA', 'BITACORA_REGISTRADA', 'HORAS_VISADAS',
                    'OBSERVADA', 'CANCELADA_SISTEMA', 'CANCELADA_MENTOR', 'CANCELADA_QUORUM', 'FINALIZADA'
                ));
            """)
            )
        except Exception:
            pass

    db = next(get_session())
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

        print("[DEMO_SEED] 2. Configurando cuentas y roles institucionales...")
        users = [
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

        # Disponibilidad horaria para el mentor
        if (
            db.query(DisponibilidadHoraria).filter(DisponibilidadHoraria.email == "mentor@upt.pe").count()
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
                        email="mentor@upt.pe",
                        dia_semana=dia,
                        hora_inicio=h_ini,
                        hora_fin=h_fin,
                    )
                )
            db.commit()

        print("[DEMO_SEED] 4. Aprovisionando sesiones y 22.0 horas formativas visadas para mentor@upt.pe...")
        # Crear 22 sesiones pasadas de 1 hora cada una (total = 22.0 h) con bitácoras visadas por Dirección
        for i in range(1, 23):
            session_id = 9000 + i
            sesion_exist = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == session_id).first()
            if not sesion_exist:
                past_time = now - timedelta(days=30 - i, hours=4)
                sesion = SesionMentoria(
                    id_sesion=session_id,
                    codigo_sesion=f"SES-DEMO-{session_id}",
                    mentor_email="mentor@upt.pe",
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
                    id_mentor="mentor@upt.pe",
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

        print("[DEMO_SEED] ¡Entorno de demostración aprovisionado con éxito!")
        print("[DEMO_SEED] Cuentas listas para demostración académica:")
        print("  - Mentoreado: mentoreado@upt.pe (Rol: Mentoreado)")
        print("  - Mentor:     mentor@upt.pe (Rol: Mentor — 22.0h visadas listo para constancia)")
        print("  - Admin:      admin@upt.pe (Rol: Administrador — Visado y auditoría)")

    except Exception as e:
        db.rollback()
        print(f"[DEMO_SEED] Error durante el aprovisionamiento de fixtures: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_environment()
