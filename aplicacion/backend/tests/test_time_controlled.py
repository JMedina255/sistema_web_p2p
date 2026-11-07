from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from app.schemas.attendance import AttendanceCheckinPayload
from app.schemas.bitacora import BitacoraCreatePayload
from app.services.attendance_service import (
    AttendanceService,
    clear_attendances_in_memory,
)
from app.services.bitacora_service import (
    BitacoraService,
    clear_bitacoras_in_memory,
)
from app.services.booking_service import (
    BookingService,
    _memory_bookings,
    clear_bookings_in_memory,
)
from app.services.offer_service import (
    _memory_offers,
    clear_offers_in_memory,
)


def test_time_controlled_temporal_milestones_t31():
    """
    T-31: Batería con Reloj Controlado simulando la progresión temporal de una sesión:
    - T-48h: Apertura ordinaria de reservas.
    - T-24h: Corte perentorio y disparo de evaluación de quórum.
    - T=0: Inicio de sesión y apertura de check-in de asistencia.
    - T+48h: Cierre de ventana perentoria para registro de bitácora pedagógica.
    """
    clear_offers_in_memory()
    clear_bookings_in_memory()
    clear_attendances_in_memory()
    clear_bitacoras_in_memory()

    # Fijamos el punto cero de la sesión T_session
    t_session = datetime(2026, 11, 20, 10, 0, 0, tzinfo=UTC)
    mentor_email = "mentor.tiempo@upt.pe"
    student_confirmed = "estudiante.confirmado@upt.pe"
    student_pending = "estudiante.pendiente@upt.pe"

    _memory_offers.append(
        {
            "id_sesion": 1301,
            "codigo_sesion": "SES-TIME-1301",
            "mentor_email": mentor_email,
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "duracion_minutos": 60,
            "fecha_inicio": t_session.isoformat(),
            "estado": "PUBLICADA",
            "quorumevaluated_at": None,
        }
    )

    _memory_bookings.extend(
        [
            {
                "id_reserva": 1,
                "id_sesion": 1301,
                "estudiante_email": student_confirmed,
                "estado": "CONFIRMADA",
            },
            {
                "id_reserva": 2,
                "id_sesion": 1301,
                "estudiante_email": "est2@upt.pe",
                "estado": "CONFIRMADA",
            },
            {
                "id_reserva": 3,
                "id_sesion": 1301,
                "estudiante_email": "est3@upt.pe",
                "estado": "CONFIRMADA",
            },
            {
                "id_reserva": 4,
                "id_sesion": 1301,
                "estudiante_email": student_pending,
                "estado": "PENDIENTE_CONFIRMACION",
            },
        ]
    )

    # =========================================================================
    # Hito 1: T - 48h (Dos días antes del inicio)
    # =========================================================================
    t_minus_48h = t_session - timedelta(hours=48)
    with patch("datetime.datetime") as mock_dt:
        mock_dt.now.return_value = t_minus_48h
        # En T-48h, la sesión está en fase de convocatoria. No se evalúa quórum todavía.
        active = BookingService.evaluate_all_active_quorums(db=None, now_utc=t_minus_48h)
        assert len(active) == 0
        target = next(o for o in _memory_offers if o["id_sesion"] == 1301)
        assert target["estado"] == "PUBLICADA"

    # =========================================================================
    # Hito 2: T - 24h (Exactamente 24 horas antes)
    # =========================================================================
    t_minus_24h = t_session - timedelta(hours=24)
    # En T-24h se dispara el motor de quórum
    res_q = BookingService.evaluate_session_quorum(db=None, id_sesion=1301, now_utc=t_minus_24h)
    assert res_q.cumple_quorum is True
    assert res_q.estado_sesion == "CONFIRMADA"

    # La reserva no ratificada pasa a CANCELADA_NO_CONFIRMADA
    res_pend = next(b for b in _memory_bookings if b["id_reserva"] == 4)
    assert res_pend["estado"] == "CANCELADA_NO_CONFIRMADA"

    # =========================================================================
    # Hito 3: T = 0 (Hora de inicio de la mentoría)
    # =========================================================================
    t_zero = t_session + timedelta(minutes=5)
    # Mentor genera token en T=0
    token_resp = AttendanceService.generate_token(
        db=None, session_id=1301, caller_email=mentor_email, now_utc=t_zero
    )
    assert token_resp.token is not None

    # Estudiante confirmado registra check-in exitosamente
    att_resp = AttendanceService.record_checkin(
        db=None,
        session_id=1301,
        payload=AttendanceCheckinPayload(qr_token=token_resp.token),
        caller_email=student_confirmed,
        now_utc=t_zero,
    )
    assert att_resp.asistio is True

    # =========================================================================
    # Hito 4: T + 40h (Dentro del límite de 48h de bitácora)
    # =========================================================================
    t_plus_40h = t_session + timedelta(hours=40)
    target["estado"] = "CONCLUIDA"

    bit_payload = BitacoraCreatePayload(
        temas_cubiertos=["Programación Dinámica", "Memorización"],
        observaciones="Excelente asimilación conceptual por parte del grupo, resolviendo el problema de la mochila.",
        nivel_dificultad="Alto",
    )
    bit_resp = BitacoraService.create_bitacora(
        db=None,
        session_id=1301,
        payload=bit_payload,
        caller_email=mentor_email,
        now_utc=t_plus_40h,
    )
    assert bit_resp.horas_declaradas == 1.0
    assert len(bit_resp.hash_firma) == 64
    assert target["estado"] == "BITACORA_REGISTRADA"

    # =========================================================================
    # Hito 5: T + 50h (Expiración del plazo perentorio RN-12)
    # =========================================================================
    t_plus_50h = t_session + timedelta(hours=50)
    import pytest
    from fastapi import HTTPException

    # Intentar registrar una segunda sesión después de las 48h reglamentarias
    _memory_offers.append(
        {
            "id_sesion": 1302,
            "codigo_sesion": "SES-TIME-1302",
            "mentor_email": mentor_email,
            "modalidad": "presencial",
            "aforo_maximo": 10,
            "duracion_minutos": 60,
            "fecha_inicio": t_session.isoformat(),
            "estado": "CONCLUIDA",
        }
    )
    with pytest.raises(HTTPException) as exc_info:
        BitacoraService.create_bitacora(
            db=None,
            session_id=1302,
            payload=bit_payload,
            caller_email=mentor_email,
            now_utc=t_plus_50h,
        )
    assert exc_info.value.status_code == 400
    assert "DEADLINE_EXCEEDED" in exc_info.value.detail
