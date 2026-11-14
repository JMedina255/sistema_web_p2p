"""
Script de Aprovisionamiento Integral para Demostración Académica (Expo / Sustentación).
Configura datos consistentes y escenarios de prueba para los 3 perfiles principales:
  1. Mentor:      mentor.avanzado@upt.pe
  2. Mentoreado:  ra2022073504@virtual.upt.pe
  3. Admin:       admin.epis@upt.pe

Cubre todos los requerimientos funcionales (RF01 al RF26), respetando ventanas temporales
(T-24h, T+24h, T+48h), umbral de quórum (50%), asistencia TOTP y certificación (>= 20h).
"""

import hashlib
from datetime import UTC, datetime, timedelta
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from app.db.session import get_engine
from app.models.auth import AuthChallenge
from app.models.bitacora import BitacoraPedagogica
from app.models.booking import ReservaCupo, SolicitudDemanda
from app.models.certificate import CertificadoHoras
from app.models.consent import ConsentimientoLegal
from app.models.curriculum import Asignatura, TemaConceptual
from app.models.offer import SesionMentoria
from app.models.profile import DisponibilidadHoraria, PerfilAcademico
from app.models.roles import Rol, UsuarioRol
from app.models.survey import EncuestaCalidad


def generate_ticket_hash(codigo_reserva: str, id_sesion: int, estudiante_email: str, fecha_iso: str) -> str:
    raw = f"{codigo_reserva}:{id_sesion}:{estudiante_email}:{fecha_iso}:UPT_P2P_SECRET"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def seed_expo_dataset():
    engine = get_engine()
    if engine is None:
        print("[EXPO_SEED] Error: Motor de base de datos no disponible.")
        return

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    now = datetime.now(UTC)

    try:
        print("==================================================================")
        print("  INICIANDO APROVISIONAMIENTO PARA DEMOSTRACIÓN ACADÉMICA (EXPO)  ")
        print("==================================================================")

        # ------------------------------------------------------------------
        # 1. Configuración de Roles y Usuarios de la Expo
        # ------------------------------------------------------------------
        print("\n[1/7] Configurando roles institucionales...")
        db_roles = {}
        for r_name in ["mentoreado", "mentor", "administrador"]:
            r_obj = db.query(Rol).filter(Rol.nombre_rol == r_name).first()
            if not r_obj:
                r_obj = Rol(nombre_rol=r_name, descripcion=f"Rol de {r_name}")
                db.add(r_obj)
                db.commit()
                db.refresh(r_obj)
            db_roles[r_name] = r_obj

        # Asignar roles explícitos en usuario_roles
        user_roles_map = {
            "mentor.avanzado@upt.pe": ["mentor", "mentoreado"],
            "ra2022073504@virtual.upt.pe": ["mentoreado", "mentor"],
            "admin.epis@upt.pe": ["administrador"],
            "mentoreado@upt.pe": ["mentoreado"],
            "2022073504@upt.pe": ["mentor", "mentoreado"],
            "mentor@upt.pe": ["mentor", "mentoreado"],
        }

        for email, roles_list in user_roles_map.items():
            for r_name in roles_list:
                r_obj = db_roles[r_name]
                ur = db.query(UsuarioRol).filter(UsuarioRol.email == email, UsuarioRol.id_rol == r_obj.id_rol).first()
                if not ur:
                    ur = UsuarioRol(email=email, id_rol=r_obj.id_rol, activo=True, fecha_asignacion=now, asignado_por="expo_seed")
                    db.add(ur)
                else:
                    ur.activo = True

            # Consentimiento legal obligatorio Ley 29733 (RF02)
            c = db.query(ConsentimientoLegal).filter(ConsentimientoLegal.email == email).first()
            if not c:
                c = ConsentimientoLegal(
                    email=email,
                    terms_version="2026-II-v1.0",
                    accepted=True,
                    ip_address="127.0.0.1",
                    user_agent="ExpoSeedScript",
                )
                db.add(c)
            else:
                c.accepted = True

        db.commit()

        # ------------------------------------------------------------------
        # 2. Configuración de Perfiles Académicos (RF04)
        # ------------------------------------------------------------------
        print("\n[2/7] Aprovisionando perfiles académicos y disponibilidades...")
        profiles_to_seed = [
            {
                "email": "mentor.avanzado@upt.pe",
                "codigo_estudiante": "mentor.avanzado",
                "nombres": "Carlos Alberto",
                "apellidos": "Mendoza Dávila",
                "ciclo_actual": 9,
                "rol_postulacion": "mentor",
                "materias_interes": [1, 2, 3, 4, 5, 6],
                "temas_seleccionados": [1, 2, 5, 9, 10, 14, 15, 22, 23],
                "biografia": "Mentor Acreditado de IX ciclo EPIS-UPT. Especialista en Algoritmos, Cálculo y POO.",
                "modalidad_preferida": "presencial",
            },
            {
                "email": "ra2022073504@virtual.upt.pe",
                "codigo_estudiante": "2022073504",
                "nombres": "Renzo Antonio",
                "apellidos": "Antayhua Mamani",
                "ciclo_actual": 4,
                "rol_postulacion": "mentoreado",
                "materias_interes": [1, 3, 4],
                "temas_seleccionados": [1, 2, 9, 14],
                "biografia": "Estudiante de IV ciclo en preparación para asignaturas críticas y proyectos.",
                "modalidad_preferida": "presencial",
            },
            {
                "email": "admin.epis@upt.pe",
                "codigo_estudiante": "admin.epis",
                "nombres": "Dirección de Escuela",
                "apellidos": "EPIS-UPT",
                "ciclo_actual": 10,
                "rol_postulacion": "administrador",
                "materias_interes": [1, 2, 3, 4, 5, 6],
                "temas_seleccionados": [1, 2, 9],
                "biografia": "Dirección y Coordinación de Tutorías y Mentorías Académicas EPIS-UPT.",
                "modalidad_preferida": "presencial",
            },
        ]

        for p_data in profiles_to_seed:
            p_obj = db.query(PerfilAcademico).filter(PerfilAcademico.email == p_data["email"]).first()
            if not p_obj:
                p_obj = PerfilAcademico(**p_data)
                db.add(p_obj)
            else:
                for k, v in p_data.items():
                    setattr(p_obj, k, v)

        # Disponibilidad horaria para matching en EdRecSys (Lunes a Viernes)
        for email in ["mentor.avanzado@upt.pe", "ra2022073504@virtual.upt.pe"]:
            db.query(DisponibilidadHoraria).filter(DisponibilidadHoraria.email == email).delete()
            for dia in range(1, 6):  # Lun a Vie
                for h_ini, h_fin in [("08:00", "10:00"), ("10:00", "12:00"), ("14:00", "16:00"), ("16:00", "18:00")]:
                    db.add(DisponibilidadHoraria(email=email, dia_semana=dia, hora_inicio=h_ini, hora_fin=h_fin))

        db.commit()

        # ------------------------------------------------------------------
        # 3. Solicitud Temática por Demanda (RF07)
        # ------------------------------------------------------------------
        print("\n[3/7] Aprovisionando Banco de Solicitudes por Demanda (RF07)...")
        # Limpiar solicitudes demo previas para este mentoreado
        db.query(SolicitudDemanda).filter(SolicitudDemanda.estudiante_email == "ra2022073504@virtual.upt.pe").delete()
        solicitud_demo = SolicitudDemanda(
            estudiante_email="ra2022073504@virtual.upt.pe",
            id_asignatura=3,  # Algoritmos y Estructuras de Datos
            id_tema=10,       # Recursividad y Relaciones de Recurrencia
            observaciones="Requiero asesoría pedagógica urgente para la resolución de árboles de recursión y el teorema maestro.",
            estado="PENDIENTE",
            created_at=now - timedelta(hours=5),
        )
        db.add(solicitud_demo)
        db.commit()

        # ------------------------------------------------------------------
        # 4. Sesiones Estratégicas para Demostración en Vivo
        # ------------------------------------------------------------------
        print("\n[4/7] Creando sesiones y reservas para los casos de prueba de la Expo...")

        # A) Sesión Recomendada Top-k para Mentoreado (RF06 / RF08 / RF12)
        # Programada para dentro de 4 días a las 10:00 AM (ventana abierta > 48h)
        s_recom = db.query(SesionMentoria).filter(SesionMentoria.codigo_sesion == "SES-EXPO-01-RECOM").first()
        if not s_recom:
            s_recom = SesionMentoria(
                codigo_sesion="SES-EXPO-01-RECOM",
                mentor_email="mentor.avanzado@upt.pe",
                id_asignatura=1,  # Cálculo I
                id_tema=1,        # Límites y Continuidad
                fecha_inicio=now + timedelta(days=4, hours=2),
                duracion_minutos=60,
                modalidad="virtual",
                aforo_maximo=20,
                espacio_asignado="https://meet.google.com/upt-cal-1001",
                notas_adicionales="Sesión de nivelación teórica y resolución de límites algebraicos y trigonométricos.",
                estado="PUBLICADA",
            )
            db.add(s_recom)
            db.commit()
            db.refresh(s_recom)

        # B) Sesión en Alerta de Quórum Insuficiente para Demostrar Decisión del Mentor (RF15 / RF16)
        # Inicio dentro de 18 horas (< 24h), confirmados < 50%
        s_quorum = db.query(SesionMentoria).filter(SesionMentoria.codigo_sesion == "SES-EXPO-02-QUORUM").first()
        if not s_quorum:
            s_quorum = SesionMentoria(
                codigo_sesion="SES-EXPO-02-QUORUM",
                mentor_email="mentor.avanzado@upt.pe",
                id_asignatura=3,  # Algoritmos
                id_tema=9,        # Notación Big-O
                fecha_inicio=now + timedelta(hours=18),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Lab 01",
                notas_adicionales="Práctica guiada en laboratorio sobre análisis asintótico de algoritmos de ordenamiento.",
                estado="QUORUM_INSUFICIENTE",
                quorumevaluated_at=now - timedelta(hours=6),
            )
            db.add(s_quorum)
            db.commit()
            db.refresh(s_quorum)
            # Solo 1 alumno confirmado de 10 plazas (10% < 50%)
            r_q1 = ReservaCupo(
                codigo_reserva="RES-EXPO-Q01",
                id_sesion=s_quorum.id_sesion,
                estudiante_email="mentoreado@upt.pe",
                estado="CONFIRMADA",
                fecha_reserva=now - timedelta(days=2),
                fecha_ratificacion=now - timedelta(days=1),
                ticket_hash=generate_ticket_hash("RES-EXPO-Q01", s_quorum.id_sesion, "mentoreado@upt.pe", (now - timedelta(days=1)).isoformat()),
            )
            db.add(r_q1)
            db.commit()

        # C) Sesión EN VIVO para Control de Asistencia y Proyección QR/TOTP (RF17)
        # Inicio hace 15 minutos, termina en 45 minutos (está en curso)
        s_live = db.query(SesionMentoria).filter(SesionMentoria.codigo_sesion == "SES-EXPO-03-LIVE").first()
        if not s_live:
            s_live = SesionMentoria(
                codigo_sesion="SES-EXPO-03-LIVE",
                mentor_email="mentor.avanzado@upt.pe",
                id_asignatura=4,  # POO
                id_tema=14,       # Clases y Objetos
                fecha_inicio=now - timedelta(minutes=15),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Lab 02",
                notas_adicionales="Implementación orientada a objetos con herencia y polimorfismo en C++.",
                estado="CONFIRMADA",
            )
            db.add(s_live)
            db.commit()
            db.refresh(s_live)
            # Renzo tiene cupo confirmado para hacer check-in en vivo
            r_live = ReservaCupo(
                codigo_reserva="RES-EXPO-LIVE-RENZO",
                id_sesion=s_live.id_sesion,
                estudiante_email="ra2022073504@virtual.upt.pe",
                estado="CONFIRMADA",
                fecha_reserva=now - timedelta(days=2),
                fecha_ratificacion=now - timedelta(days=1),
                ticket_hash=generate_ticket_hash("RES-EXPO-LIVE-RENZO", s_live.id_sesion, "ra2022073504@virtual.upt.pe", (now - timedelta(days=1)).isoformat()),
            )
            db.add(r_live)
            db.commit()

        # D) Sesión Concluida Lista para Llenar Bitácora Pedagógica (RF17 / RN-12)
        # Culminó hace 1 hora (dentro de las 48 h reglamentarias de RN-12)
        s_bitacora = db.query(SesionMentoria).filter(SesionMentoria.codigo_sesion == "SES-EXPO-04-BITACORA").first()
        if not s_bitacora:
            s_bitacora = SesionMentoria(
                codigo_sesion="SES-EXPO-04-BITACORA",
                mentor_email="mentor.avanzado@upt.pe",
                id_asignatura=1,  # Cálculo I
                id_tema=2,        # Derivadas
                fecha_inicio=now - timedelta(hours=2),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Aula 101",
                notas_adicionales="Ejercicios prácticos de derivación implícita y regla de la cadena.",
                estado="CONFIRMADA",  # Pendiente de llenado de bitácora
            )
            db.add(s_bitacora)
            db.commit()
            db.refresh(s_bitacora)
            r_bit = ReservaCupo(
                codigo_reserva="RES-EXPO-BIT-RENZO",
                id_sesion=s_bitacora.id_sesion,
                estudiante_email="ra2022073504@virtual.upt.pe",
                estado="CONFIRMADA",
                fecha_reserva=now - timedelta(days=2),
                fecha_ratificacion=now - timedelta(days=1),
                ticket_hash=generate_ticket_hash("RES-EXPO-BIT-RENZO", s_bitacora.id_sesion, "ra2022073504@virtual.upt.pe", (now - timedelta(days=1)).isoformat()),
            )
            db.add(r_bit)
            db.commit()

        # E) Sesión Concluida para que el Mentoreado Realice Encuesta de Calidad (RF18)
        # Terminó hace 3 horas (dentro de las 24 h de RN-13), asistencia ASISTIDA, encuesta no respondida
        s_survey = db.query(SesionMentoria).filter(SesionMentoria.codigo_sesion == "SES-EXPO-05-SURVEY").first()
        if not s_survey:
            s_survey = SesionMentoria(
                codigo_sesion="SES-EXPO-05-SURVEY",
                mentor_email="mentor.avanzado@upt.pe",
                id_asignatura=3,  # Algoritmos
                id_tema=10,       # Recursividad
                fecha_inicio=now - timedelta(hours=4),
                duracion_minutos=60,
                modalidad="virtual",
                aforo_maximo=20,
                espacio_asignado="https://meet.google.com/upt-rec-5005",
                notas_adicionales="Estrategias recursivas de divide y vencerás.",
                estado="FINALIZADA",
            )
            db.add(s_survey)
            db.commit()
            db.refresh(s_survey)

            # Bitácora ya cerrada por el mentor
            b_surv = BitacoraPedagogica(
                id_sesion=s_survey.id_sesion,
                id_mentor="mentor.avanzado@upt.pe",
                temas_cubiertos=[9, 10],
                observaciones="Sesión formativa concluida exitosamente con participación activa de los estudiantes inscritos.",
                nivel_dificultad="Medio",
                hash_firma=f"hash_expo_survey_{s_survey.id_sesion}",
                horas_declaradas=1.0,
                visado_administrador=False,
                created_at=now - timedelta(hours=2, minutes=30),
            )
            db.add(b_surv)

            # Reserva de Renzo con estado ASISTIDA para habilitar el botón de encuesta (RF18 / RN-13)
            r_surv = ReservaCupo(
                codigo_reserva="RES-EXPO-SURV-RENZO",
                id_sesion=s_survey.id_sesion,
                estudiante_email="ra2022073504@virtual.upt.pe",
                estado="ASISTIDA",
                fecha_reserva=now - timedelta(days=2),
                fecha_ratificacion=now - timedelta(days=1),
                ticket_hash=generate_ticket_hash("RES-EXPO-SURV-RENZO", s_survey.id_sesion, "ra2022073504@virtual.upt.pe", (now - timedelta(days=1)).isoformat()),
            )
            db.add(r_surv)
            db.commit()

        # F) Bitácora Pedagógica Pendiente de Visado por el Administrador (RF26)
        s_audit = db.query(SesionMentoria).filter(SesionMentoria.codigo_sesion == "SES-EXPO-06-AUDIT").first()
        if not s_audit:
            s_audit = SesionMentoria(
                codigo_sesion="SES-EXPO-06-AUDIT",
                mentor_email="mentor.avanzado@upt.pe",
                id_asignatura=2,  # Cálculo II
                id_tema=5,        # Métodos de Integración
                fecha_inicio=now - timedelta(days=1, hours=4),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Aula 202",
                notas_adicionales="Resolución integral de integrales por sustitución trigonométrica.",
                estado="FINALIZADA",
            )
            db.add(s_audit)
            db.commit()
            db.refresh(s_audit)

            b_audit = BitacoraPedagogica(
                id_sesion=s_audit.id_sesion,
                id_mentor="mentor.avanzado@upt.pe",
                temas_cubiertos=[5, 6],
                observaciones="Desarrollo completo de integración por fracciones parciales y sustitución con asistencia plena.",
                nivel_dificultad="Alto",
                hash_firma=f"hash_expo_audit_{s_audit.id_sesion}",
                horas_declaradas=1.0,
                visado_administrador=False,  # En estado REGISTRADA para que el admin la vise u observe
                created_at=now - timedelta(days=1, hours=2),
            )
            db.add(b_audit)
            db.commit()

        # G) Reserva Futura Pendiente de Ratificación para el Mentoreado (RF13 / RF14)
        # Inicio en 3 días (ventana abierta > 24h para probar Confirmar o Desistir)
        s_future = db.query(SesionMentoria).filter(SesionMentoria.codigo_sesion == "SES-EXPO-07-FUTURE").first()
        if not s_future:
            s_future = SesionMentoria(
                codigo_sesion="SES-EXPO-07-FUTURE",
                mentor_email="mentor.avanzado@upt.pe",
                id_asignatura=5,  # Base de Datos
                id_tema=18,       # Modelo ER
                fecha_inicio=now + timedelta(days=3, hours=4),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Lab 03",
                notas_adicionales="Transformación de diagramas ER a esquema relacional normalizado.",
                estado="PUBLICADA",
            )
            db.add(s_future)
            db.commit()
            db.refresh(s_future)

            r_fut = ReservaCupo(
                codigo_reserva="RES-EXPO-FUT-RENZO",
                id_sesion=s_future.id_sesion,
                estudiante_email="ra2022073504@virtual.upt.pe",
                estado="PENDIENTE_CONFIRMACION",  # Permite al alumno pulsar Confirmar Asistencia o Desistir
                fecha_reserva=now - timedelta(hours=3),
                ticket_hash=generate_ticket_hash("RES-EXPO-FUT-RENZO", s_future.id_sesion, "ra2022073504@virtual.upt.pe", (now - timedelta(hours=3)).isoformat()),
            )
            db.add(r_fut)
            db.commit()

        # ------------------------------------------------------------------
        # 5. Acumulación Histórica de 22 Horas para Certificación Oficial (RF22 / RF23)
        # ------------------------------------------------------------------
        print("\n[5/7] Generando histórico de 22 sesiones visadas para certificar a mentor.avanzado@upt.pe (>= 20h)...")
        # Generar 22 sesiones en el pasado con bitácoras visadas (duración 60 min = 1.0 h c/u)
        for i in range(1, 23):
            s_code = f"SES-EXPO-HIST-{i:02d}"
            s_hist = db.query(SesionMentoria).filter(SesionMentoria.codigo_sesion == s_code).first()
            p_date = now - timedelta(days=10 + i, hours=i % 4)
            if not s_hist:
                s_hist = SesionMentoria(
                    codigo_sesion=s_code,
                    mentor_email="mentor.avanzado@upt.pe",
                    id_asignatura=1 if i % 2 == 0 else 3,
                    id_tema=1 if i % 2 == 0 else 9,
                    fecha_inicio=p_date,
                    duracion_minutos=60,
                    modalidad="presencial" if i % 2 == 0 else "virtual",
                    aforo_maximo=10 if i % 2 == 0 else 20,
                    espacio_asignado="Lab 01" if i % 2 == 0 else "https://meet.google.com/upt-hist",
                    notas_adicionales=f"Sesión formativa correlativa #{i} del semestre 2026-II.",
                    estado="FINALIZADA",
                )
                db.add(s_hist)
                db.commit()
                db.refresh(s_hist)

            # Bitácora visada por el administrador
            b_hist = db.query(BitacoraPedagogica).filter(BitacoraPedagogica.id_sesion == s_hist.id_sesion).first()
            if not b_hist:
                b_hist = BitacoraPedagogica(
                    id_sesion=s_hist.id_sesion,
                    id_mentor="mentor.avanzado@upt.pe",
                    temas_cubiertos=[1, 2] if i % 2 == 0 else [9, 10],
                    observaciones=f"Sesión formativa #{i} concluida con desarrollo exhaustivo y conformidad de asistencia.",
                    nivel_dificultad="Medio",
                    hash_firma=f"hash_visado_hist_{s_hist.id_sesion}",
                    horas_declaradas=1.0,
                    visado_administrador=True,  # 1.0 hora convalidada por sesión
                    created_at=p_date + timedelta(hours=2),
                )
                db.add(b_hist)

            # Reserva de asistencia
            r_hist = db.query(ReservaCupo).filter(ReservaCupo.codigo_reserva == f"RES-EXPO-HIST-{i:02d}").first()
            if not r_hist:
                r_hist = ReservaCupo(
                    codigo_reserva=f"RES-EXPO-HIST-{i:02d}",
                    id_sesion=s_hist.id_sesion,
                    estudiante_email="ra2022073504@virtual.upt.pe",
                    estado="ASISTIDA",
                    fecha_reserva=p_date - timedelta(days=2),
                    fecha_ratificacion=p_date - timedelta(days=1),
                    ticket_hash=generate_ticket_hash(f"RES-EXPO-HIST-{i:02d}", s_hist.id_sesion, "ra2022073504@virtual.upt.pe", p_date.isoformat()),
                )
                db.add(r_hist)

            # Encuesta de satisfacción para alimentar la reputación a 5 estrellas
            e_hist = db.query(EncuestaCalidad).filter(EncuestaCalidad.id_sesion == s_hist.id_sesion).first()
            if not e_hist:
                e_hist = EncuestaCalidad(
                    id_sesion=s_hist.id_sesion,
                    estudiante_email="ra2022073504@virtual.upt.pe",
                    calificacion_general=5,
                    dominio_tema=5,
                    claridad_explicacion=5,
                    puntualidad=5,
                    comentarios="Excelente dominio pedagógico y claridad conceptual del mentor.",
                    created_at=p_date + timedelta(hours=4),
                )
                db.add(e_hist)

        db.commit()

        # ------------------------------------------------------------------
        # 6. Certificado Oficial Emitido para Descarga en PDF (RF22 / RF23)
        # ------------------------------------------------------------------
        print("\n[6/7] Aprovisionando certificado oficial en PDF para mentor.avanzado@upt.pe...")
        cert_exist = db.query(CertificadoHoras).filter(
            CertificadoHoras.id_mentor == "mentor.avanzado@upt.pe",
            CertificadoHoras.periodo_academico == "2026-II"
        ).first()

        if not cert_exist:
            cert_hash = hashlib.sha256("CERT-UPT-EXPO-MA01:mentor.avanzado@upt.pe:22.0:2026-II".encode("utf-8")).hexdigest()
            cert_obj = CertificadoHoras(
                id_mentor="mentor.avanzado@upt.pe",
                codigo_folio="UPT-EPIS-2026-II-0012",
                periodo_academico="2026-II",
                horas_acreditadas=22.0,
                hash_firma=cert_hash,
                estado="EMITIDO_DEMO",
                created_at=now - timedelta(days=2),
            )
            db.add(cert_obj)
            db.commit()

        # ------------------------------------------------------------------
        # 7. Sincronización Automática de Secuencias de PostgreSQL
        # ------------------------------------------------------------------
        print("\n[7/7] Sincronizando secuencias de PostgreSQL a sus valores máximos...")
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

        print("\n==================================================================")
        print("  ¡APROVISIONAMIENTO DE DATOS PARA LA EXPO COMPLETADO CON ÉXITO! ")
        print("==================================================================")
        print("Cuentas preparadas para demostración interactiva:")
        print("  1. Mentor:     mentor.avanzado@upt.pe       (22h visadas, cert oficial, sesiones en vivo y quórum)")
        print("  2. Mentoreado: ra2022073504@virtual.upt.pe  (Top-k match, reservas activas, encuesta pendiente)")
        print("  3. Admin:      admin.epis@upt.pe            (Auditoría de bitácoras, roles, horarios y certificados)")

    except Exception as exc:
        db.rollback()
        print(f"[EXPO_SEED] Error crítico durante el aprovisionamiento: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_expo_dataset()
