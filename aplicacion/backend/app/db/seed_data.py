"""
Script de inicialización y siembra de datos maestros institucionales en PostgreSQL (Supabase).
Sembrado de roles para usuarios institucionales (admin, mentores, estudiantes) y perfiles académicos.
"""

from datetime import UTC, datetime

from app.core.config import settings
from app.db.session import get_engine, get_session
from app.models.consent import ConsentimientoLegal
from app.models.profile import DisponibilidadHoraria, PerfilAcademico
from app.models.roles import Rol, UsuarioRol


def seed_database():
    if settings.APP_ENV == "production":
        print("ADVERTENCIA: seed_database deshabilitado en entorno de producción por razones de seguridad.")
        return

    engine = get_engine()
    if engine is None:
        print("DATABASE_URL no configurada. Saltando siembra.")
        return

    db = next(get_session())
    try:
        # 1. Asegurar roles base
        roles_data = {
            "mentoreado": "Estudiante de pregrado EPIS-UPT con necesidad de reforzamiento académico.",
            "mentor": "Estudiante de ciclo avanzado (>= VII) con mérito académico y capacidad pedagógica.",
            "administrador": "Personal directivo o de coordinación académica con facultades de auditoría y gestión de roles.",
        }
        db_roles = {}
        for role_name, desc in roles_data.items():
            r = db.query(Rol).filter(Rol.nombre_rol == role_name).first()
            if not r:
                r = Rol(nombre_rol=role_name, descripcion=desc)
                db.add(r)
                db.commit()
                db.refresh(r)
            db_roles[role_name] = r

        # 2. Asignar roles a usuarios de prueba
        user_roles_to_seed = [
            ("admin.epis@upt.pe", ["administrador", "mentoreado"]),
            ("2022073504@upt.pe", ["mentor", "mentoreado"]),
            ("2022074255@upt.pe", ["mentoreado"]),
            ("mentor.avanzado@upt.pe", ["mentor", "mentoreado"]),
            ("2023079999@upt.pe", ["mentoreado"]),
        ]

        for email, roles_list in user_roles_to_seed:
            clean_email = email.strip().lower()
            for r_name in roles_list:
                rol_obj = db_roles.get(r_name)
                if not rol_obj:
                    continue
                existing = (
                    db.query(UsuarioRol)
                    .filter(UsuarioRol.email == clean_email, UsuarioRol.id_rol == rol_obj.id_rol)
                    .first()
                )
                if not existing:
                    asig = UsuarioRol(
                        email=clean_email,
                        id_rol=rol_obj.id_rol,
                        fecha_asignacion=datetime.now(UTC),
                        asignado_por="sistema_seed",
                        activo=True,
                    )
                    db.add(asig)
                else:
                    existing.activo = True
        db.commit()

        # 3. Sembrar perfiles académicos de prueba si no existen
        profiles_to_seed = [
            {
                "email": "admin.epis@upt.pe",
                "codigo_estudiante": "admin.epis",
                "nombres": "Administrador",
                "apellidos": "EPIS-UPT",
                "ciclo_actual": 10,
                "rol_postulacion": "administrador",
                "materias_interes": [1, 2, 3],
                "temas_seleccionados": [1, 5, 9],
                "biografia": "Administración del Sistema Web P2P EPIS-UPT.",
                "modalidad_preferida": "presencial",
            },
            {
                "email": "2022073504@upt.pe",
                "codigo_estudiante": "2022073504",
                "nombres": "Renzo Antonio",
                "apellidos": "Antayhua Mamani",
                "ciclo_actual": 7,
                "rol_postulacion": "mentor",
                "materias_interes": [1, 3],
                "temas_seleccionados": [1, 2, 9, 10],
                "biografia": "Estudiante de VII ciclo con especialización en Algoritmos y Estructuras de Datos.",
                "modalidad_preferida": "presencial",
            },
            {
                "email": "2022074255@upt.pe",
                "codigo_estudiante": "2022074255",
                "nombres": "Joan Cristian",
                "apellidos": "Medina Quispe",
                "ciclo_actual": 6,
                "rol_postulacion": "mentoreado",
                "materias_interes": [1, 3],
                "temas_seleccionados": [1, 2],
                "biografia": "Estudiante de VI ciclo interesado en nivelación en Cálculo I y Algoritmos.",
                "modalidad_preferida": "presencial",
            },
            {
                "email": "mentor.avanzado@upt.pe",
                "codigo_estudiante": "mentor.avanzado",
                "nombres": "Mentor",
                "apellidos": "Avanzado EPIS",
                "ciclo_actual": 8,
                "rol_postulacion": "mentor",
                "materias_interes": [1, 2, 3],
                "temas_seleccionados": [1, 5, 9],
                "biografia": "Mentor con alta disponibilidad para asesorías presenciales y virtuales.",
                "modalidad_preferida": "hibrida",
            },
        ]

        for p_data in profiles_to_seed:
            clean_email = p_data["email"].strip().lower()
            prof = db.query(PerfilAcademico).filter(PerfilAcademico.email == clean_email).first()
            if not prof:
                prof = PerfilAcademico(
                    email=clean_email,
                    codigo_estudiante=p_data["codigo_estudiante"],
                    nombres=p_data["nombres"],
                    apellidos=p_data["apellidos"],
                    ciclo_actual=p_data["ciclo_actual"],
                    rol_postulacion=p_data["rol_postulacion"],
                    materias_interes=p_data["materias_interes"],
                    temas_seleccionados=p_data["temas_seleccionados"],
                    biografia=p_data["biografia"],
                    modalidad_preferida=p_data["modalidad_preferida"],
                )
                db.add(prof)

        # 4. Sembrar disponibilidad inicial para el mentor Renzo y mentor.avanzado si no tienen
        renzo_avail = (
            db.query(DisponibilidadHoraria).filter(DisponibilidadHoraria.email == "2022073504@upt.pe").count()
        )
        if renzo_avail == 0:
            default_slots = [
                (1, "14:00", "15:00"),
                (1, "15:00", "16:00"),
                (3, "16:00", "17:00"),
                (3, "17:00", "18:00"),
                (5, "10:00", "11:00"),
            ]
            for dia, h_ini, h_fin in default_slots:
                db.add(
                    DisponibilidadHoraria(
                        email="2022073504@upt.pe",
                        dia_semana=dia,
                        hora_inicio=h_ini,
                        hora_fin=h_fin,
                    )
                )

        # 5. Sembrar consentimiento legal aceptado para usuarios de prueba
        for email in ["admin.epis@upt.pe", "2022073504@upt.pe", "mentor.avanzado@upt.pe"]:
            existing_c = db.query(ConsentimientoLegal).filter(ConsentimientoLegal.email == email).first()
            if not existing_c:
                c = ConsentimientoLegal(
                    email=email,
                    terms_version="2026-II-v1.0",
                    accepted=True,
                    ip_address="127.0.0.1",
                    user_agent="SeedScript",
                )
                db.add(c)

        db.commit()
        print("Siembra completada exitosamente en PostgreSQL.")
    except Exception as e:
        db.rollback()
        print(f"Error durante la siembra: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
