import io
from datetime import UTC, datetime, timedelta

import PyPDF2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.models.bitacora import BitacoraPedagogica
from app.models.booking import ReservaCupo
from app.models.offer import SesionMentoria
from app.models.roles import Rol, UsuarioRol
from app.schemas.attendance import AttendanceCheckinPayload
from app.schemas.bitacora import BitacoraCreatePayload
from app.services.attendance_service import AttendanceService
from app.services.bitacora_service import BitacoraService
from app.services.booking_service import BookingService
from app.services.certificate_service import CertificateService


def test_full_mentoring_cycle_and_certificate_issuance_t48():
    """
    T-48: Suite de Integración End-to-End del Ciclo Integral del MVP (Sprint 08):
    1. PUBLICACIÓN: Mentor publica oferta de mentoría académica.
    2. RESERVAS: Mentoreados formalizan reservas provisionales.
    3. RATIFICACIÓN T-24h: Estudiantes ratifican asistencia confirmada.
    4. EVALUACIÓN DE QUÓRUM: Sistema evalúa viabilidad automática en T-24h.
    5. CONTROL DE ASISTENCIA: Mentor proyecta QR dinámico TOTP y alumnos registran check-in.
    6. CIERRE Y BITÁCORA: Mentor registra bitácora pedagógica con hash SHA-256.
    7. AUDITORÍA Y VISADO ADMINISTRATIVO: Dirección de Escuela visa la bitácora (HORAS_VISADAS).
    8. EVALUACIÓN DE UMBRAL RN-14: Validación acumulativa de horas visadas (>= 20h).
    9. EMISIÓN DE CONSTANCIA DEMO: Generación de PDF con folio único, marca de agua y código QR.
    10. DESCARGA Y VERIFICACIÓN FORENSE: Descarga binaria y validación de autenticidad SHA-256.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionTest = sessionmaker(bind=engine)
    db = SessionTest()

    try:
        now = datetime.now(UTC)
        mentor_email = "mentor.integral@upt.pe"
        admin_email = "admin.epis@upt.pe"
        students = ["alumno.1@upt.pe", "alumno.2@upt.pe", "alumno.3@upt.pe"]

        # ---------------------------------------------------------------------
        # 1. Configurar roles institucionales
        # ---------------------------------------------------------------------
        r_admin = Rol(id_rol=1, nombre_rol="administrador", descripcion="Admin")
        r_mentor = Rol(id_rol=2, nombre_rol="mentor", descripcion="Mentor")
        db.add_all([r_admin, r_mentor])
        db.commit()

        db.add(UsuarioRol(email=admin_email, id_rol=1, activo=True, asignado_por="seed"))
        db.add(UsuarioRol(email=mentor_email, id_rol=2, activo=True, asignado_por="seed"))
        db.commit()

        # ---------------------------------------------------------------------
        # 2. Publicación de Sesión de Mentoría
        # ---------------------------------------------------------------------
        t_start = now + timedelta(days=2)
        sesion = SesionMentoria(
            id_sesion=7701,
            codigo_sesion="SES-E2E-7701",
            mentor_email=mentor_email,
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=t_start,
            duracion_minutos=60,  # 1.0 hora
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Aula Magna EPIS",
            estado="PUBLICADA",
        )
        db.add(sesion)
        db.commit()
        assert sesion.estado == "PUBLICADA"

        # ---------------------------------------------------------------------
        # 3. Reservas y Ratificación en T-24h
        # ---------------------------------------------------------------------
        for i, s_email in enumerate(students):
            db.add(
                ReservaCupo(
                    id_sesion=7701,
                    codigo_reserva=f"RES-E2E-{i + 1}",
                    estudiante_email=s_email,
                    estado="CONFIRMADA",
                    fecha_reserva=now - timedelta(hours=6),
                    fecha_ratificacion=now - timedelta(hours=3),
                )
            )
        db.commit()

        # ---------------------------------------------------------------------
        # 4. Evaluación de Quórum
        # ---------------------------------------------------------------------
        q_res = BookingService.evaluate_session_quorum(
            db=db, id_sesion=7701, now_utc=t_start - timedelta(hours=24)
        )
        assert q_res.cumple_quorum is True
        assert q_res.estado_sesion == "CONFIRMADA"

        # ---------------------------------------------------------------------
        # 5. Control de Asistencia con Token QR TOTP
        # ---------------------------------------------------------------------
        t_live = t_start + timedelta(minutes=5)
        tok = AttendanceService.generate_token(
            db=db, session_id=7701, caller_email=mentor_email, now_utc=t_live
        )
        for s_email in students:
            att = AttendanceService.record_checkin(
                db=db,
                session_id=7701,
                payload=AttendanceCheckinPayload(qr_token=tok.token),
                caller_email=s_email,
                client_ip="127.0.0.1",
                now_utc=t_live + timedelta(seconds=5),
            )
            assert att.asistio is True

        # ---------------------------------------------------------------------
        # 6. Conclusión y Registro de Bitácora Pedagógica con SHA-256
        # ---------------------------------------------------------------------
        sesion.estado = "CONCLUIDA"
        db.commit()

        b_res = BitacoraService.create_bitacora(
            db=db,
            session_id=7701,
            payload=BitacoraCreatePayload(
                temas_cubiertos=["Derivadas Parciales", "Optimización"],
                observaciones="Sesión formativa de cierre ejecutada con participación activa y resolución integral de ejercicios.",
                nivel_dificultad="Alto",
            ),
            caller_email=mentor_email,
            now_utc=t_start + timedelta(hours=3),
        )
        assert b_res.horas_declaradas == 1.0
        assert b_res.visado_administrador is False

        # ---------------------------------------------------------------------
        # 7. Auditoría y Visado de Dirección de Escuela
        # ---------------------------------------------------------------------
        v_res = BitacoraService.visar_bitacora(
            db=db,
            bitacora_id=b_res.id_bitacora,
            caller_email=admin_email,
            is_admin=True,
        )
        assert v_res.visado_administrador is True
        assert v_res.estado_sesion == "HORAS_VISADAS"

        # ---------------------------------------------------------------------
        # 8. Evaluación de Umbral RN-14 (Comprobación de 1.0h -> Faltan 19.0h)
        # ---------------------------------------------------------------------
        s_initial = CertificateService.get_hours_summary(db=db, mentor_email=mentor_email)
        assert s_initial.horas_visadas == 1.0
        assert s_initial.es_elegible is False
        assert s_initial.horas_faltantes == 19.0

        # Simular 19 sesiones pasadas adicionales visadas de 1.0h cada una (+19.0h = 20.0h total)
        for j in range(1, 20):
            past_s_id = 8000 + j
            db.add(
                SesionMentoria(
                    id_sesion=past_s_id,
                    codigo_sesion=f"SES-HIST-{past_s_id}",
                    mentor_email=mentor_email,
                    id_asignatura=1,
                    id_tema=1,
                    fecha_inicio=now - timedelta(days=30 - j),
                    duracion_minutos=60,
                    modalidad="presencial",
                    aforo_maximo=10,
                    espacio_asignado="Lab 102",
                    estado="HORAS_VISADAS",
                )
            )
            db.add(
                BitacoraPedagogica(
                    id_sesion=past_s_id,
                    id_mentor=mentor_email,
                    temas_cubiertos=["Límites"],
                    observaciones="Sesión histórica aprobada y acreditada por la cátedra para el estudiante mentor.",
                    nivel_dificultad="Medio",
                    hash_firma=f"hash_hist_{j}",
                    horas_declaradas=1.0,
                    visado_administrador=True,
                )
            )
        db.commit()

        # Resumen al alcanzar el umbral de 20.0h
        s_ready = CertificateService.get_hours_summary(db=db, mentor_email=mentor_email)
        assert s_ready.horas_visadas == 20.0
        assert s_ready.es_elegible is True
        assert s_ready.porcentaje_progreso == 100.0
        assert s_ready.horas_faltantes == 0.0

        # ---------------------------------------------------------------------
        # 9. Emisión de Constancia Oficial DEMO con Marca de Agua y Folio
        # ---------------------------------------------------------------------
        cert_data, pdf_bytes = CertificateService.generate_certificate(
            db=db,
            mentor_email=mentor_email,
            periodo_academico="2026-II",
            caller_email=mentor_email,
        )
        assert cert_data["id_certificado"] > 0
        assert cert_data["codigo_folio"].startswith("CERT-2026-II-")
        assert cert_data["horas_acreditadas"] == 20.0
        assert cert_data["estado"] == "EMITIDO_DEMO"
        assert len(cert_data["hash_firma"]) == 64

        # ---------------------------------------------------------------------
        # 10. Descarga del PDF e Inspección Forense de Seguridad
        # ---------------------------------------------------------------------
        pdf_out, filename = CertificateService.get_certificate_pdf(
            db=db, certificate_id=cert_data["id_certificado"]
        )
        assert len(pdf_out) > 2000
        assert filename.endswith(".pdf")
        assert cert_data["codigo_folio"] in filename

        reader = PyPDF2.PdfReader(io.BytesIO(pdf_out))
        extracted_text = reader.pages[0].extract_text()
        assert "DEMO - FINES ACADÉMICOS" in extracted_text
        assert cert_data["codigo_folio"] in extracted_text
        assert "20.0 HORAS FORMATIVAS" in extracted_text
        assert "FIRMA CRIPTOGRÁFICA SHA-256:" in extracted_text

        # ---------------------------------------------------------------------
        # 11. Validación Institucional por Folio (QR Code)
        # ---------------------------------------------------------------------
        v_check = CertificateService.verify_certificate_by_folio(db=db, folio=cert_data["codigo_folio"])
        assert v_check.valido is True
        assert v_check.codigo_folio == cert_data["codigo_folio"]
        assert v_check.id_mentor == mentor_email
        assert v_check.horas_acreditadas == 20.0

    finally:
        db.close()
        engine.dispose()
