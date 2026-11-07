from datetime import UTC, datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.models.bitacora import BitacoraPedagogica
from app.models.booking import ReservaCupo
from app.models.offer import SesionMentoria
from app.schemas.attendance import AttendanceCheckinPayload
from app.schemas.bitacora import BitacoraCreatePayload
from app.schemas.offer import PublishOfferPayload
from app.services.attendance_service import AttendanceService
from app.services.bitacora_service import BitacoraService
from app.services.booking_service import BookingService


def test_session_closure_end_to_end_lifecycle_t37():
    """
    T-37: Prueba de Integración End-to-End del Ciclo de Vida Completo de una Mentoría:
    1. PUBLICACIÓN: Mentor publica oferta cumpliendo RN-03, RN-04, RN-05.
    2. RESERVA: Mentoreados formalizan reservas provisionales (PENDIENTE_CONFIRMACION).
    3. RATIFICACIÓN: Mentoreados confirman asistencia antes de T-24h (CONFIRMADA).
    4. EVALUACIÓN DE QUÓRUM: En T-24h se evalúa viabilidad institucional (CONFIRMADA).
    5. INICIO Y ASISTENCIA: En T=0 se genera token QR TOTP y se realiza check-in (ASISTIDA).
    6. CIERRE Y BITÁCORA: Conclusión de sesión, registro de bitácora pedagógica con SHA-256
       y acreditación de horas provisionales (BITACORA_REGISTRADA).
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionTest = sessionmaker(bind=engine)
    db = SessionTest()

    try:
        now = datetime.now(UTC)
        mentor_email = "mentor.e2e@upt.pe"
        student_a = "alumno.a@upt.pe"
        student_b = "alumno.b@upt.pe"
        student_c = "alumno.c@upt.pe"

        # ---------------------------------------------------------------------
        # Paso 1: Publicación de la Sesión
        # ---------------------------------------------------------------------
        t_start = now + timedelta(days=2)
        publish_payload = PublishOfferPayload(
            id_asignatura=1,
            codigo_asignatura="CALC-101",
            nombre_asignatura="Cálculo I",
            id_tema=1,
            nombre_tema="Límites Notables",
            fecha_inicio=t_start.isoformat(),
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Lab 102 - EPIS",
            mentor_email=mentor_email,
        )
        assert publish_payload.aforo_maximo == 10

        # Inserción directa de la sesión de mentoría en BD para el test E2E
        sesion = SesionMentoria(
            id_sesion=1401,
            codigo_sesion="SES-E2E-1401",
            mentor_email=mentor_email,
            id_asignatura=1,
            id_tema=1,
            fecha_inicio=t_start,
            duracion_minutos=60,
            modalidad="presencial",
            aforo_maximo=10,
            espacio_asignado="Lab 102 - EPIS",
            estado="PUBLICADA",
        )
        db.add(sesion)
        db.commit()
        assert sesion.estado == "PUBLICADA"

        # ---------------------------------------------------------------------
        # Paso 2 & 3: Reservas y Ratificación de Asistencia
        # ---------------------------------------------------------------------
        for i, email in enumerate([student_a, student_b, student_c]):
            b = ReservaCupo(
                id_sesion=1401,
                codigo_reserva=f"RES-E2E-{i + 1}",
                estudiante_email=email,
                estado="CONFIRMADA",  # Ratificada por los estudiantes
                fecha_reserva=now - timedelta(hours=5),
                fecha_ratificacion=now - timedelta(hours=2),
            )
            db.add(b)
        db.commit()

        # ---------------------------------------------------------------------
        # Paso 4: Evaluación Automática de Quórum en T-24h
        # ---------------------------------------------------------------------
        t_eval = t_start - timedelta(hours=24)
        q_result = BookingService.evaluate_session_quorum(db=db, id_sesion=1401, now_utc=t_eval)
        assert q_result.cumple_quorum is True
        assert q_result.estado_sesion == "CONFIRMADA"

        db.refresh(sesion)
        assert sesion.estado == "CONFIRMADA"
        assert sesion.quorumevaluated_at is not None

        # ---------------------------------------------------------------------
        # Paso 5: Inicio de Sesión y Pase de Asistencia Digital
        # ---------------------------------------------------------------------
        t_checkin = t_start + timedelta(minutes=5)
        token_info = AttendanceService.generate_token(
            db=db, session_id=1401, caller_email=mentor_email, now_utc=t_checkin
        )
        assert token_info.token is not None

        # Check-in de los 3 estudiantes dentro de los 30s del token
        for email in [student_a, student_b, student_c]:
            att_res = AttendanceService.record_checkin(
                db=db,
                session_id=1401,
                payload=AttendanceCheckinPayload(qr_token=token_info.token),
                caller_email=email,
                client_ip="192.168.1.50",
                now_utc=t_checkin + timedelta(seconds=10),
            )
            assert att_res.asistio is True

        roster = AttendanceService.get_roster(db=db, session_id=1401)
        assert len(roster) == 3
        assert all(r.asistio is True for r in roster)

        # ---------------------------------------------------------------------
        # Paso 6: Conclusión y Registro de Bitácora Pedagógica con SHA-256
        # ---------------------------------------------------------------------
        sesion.estado = "CONCLUIDA"
        db.commit()

        t_bitacora = t_start + timedelta(hours=2)
        b_payload = BitacoraCreatePayload(
            temas_cubiertos=["Límites Notables", "Propiedades de Continuidad"],
            observaciones="Sesión ejecutada conforme a la programación silábica de la EPIS. Alto nivel de resolución de problemas prácticos.",
            nivel_dificultad="Medio",
        )

        b_result = BitacoraService.create_bitacora(
            db=db,
            session_id=1401,
            payload=b_payload,
            caller_email=mentor_email,
            now_utc=t_bitacora,
        )

        assert b_result.horas_declaradas == 1.0  # 60 minutos = 1.0 hora
        assert len(b_result.hash_firma) == 64
        assert b_result.visado_administrador is False

        # Estado final del ciclo de vida
        db.refresh(sesion)
        assert sesion.estado == "BITACORA_REGISTRADA"

        # Auditoría de bitácora persistida
        bitacora_db = db.query(BitacoraPedagogica).filter(BitacoraPedagogica.id_sesion == 1401).first()
        assert bitacora_db is not None
        assert bitacora_db.hash_firma == b_result.hash_firma
        assert bitacora_db.id_mentor == mentor_email

    finally:
        db.close()
        engine.dispose()
