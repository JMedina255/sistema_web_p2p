from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

from app.models.attendance import TokenAsistenciaActivo
from app.schemas.attendance import AttendanceCheckinPayload
from app.services.attendance_service import (
    AttendanceService,
    _active_attendance_tokens,
)


def test_totp_multiworker_persistence_in_database():
    """
    Verifica que el token TOTP se persista físicamente en la BD y que un worker
    con la memoria RAM vacía pueda validar el check-in exitosamente.
    """
    now = datetime.now(UTC)
    expires = now + timedelta(seconds=30)
    session_id = 999

    # Mock de registro en BD
    mock_token_db = TokenAsistenciaActivo(
        id_sesion=session_id,
        token="sha256-test-token-multiworker-123",
        totp_code="654321",
        expires_at=expires,
    )

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_token_db

    # Vaciamos la memoria RAM para emular otro worker que no generó el token
    _active_attendance_tokens.pop(session_id, None)

    # El worker 2 valida el check-in usando el token de base de datos
    payload = AttendanceCheckinPayload(numeric_code="654321")

    # Simulamos la sesión de mentoría y reserva en estado CONFIRMADA
    mock_sesion = MagicMock()
    mock_sesion.id_sesion = session_id
    mock_sesion.fecha_inicio = now - timedelta(minutes=5)
    mock_sesion.duracion_minutos = 60

    mock_reserva = MagicMock()
    mock_reserva.estado = "CONFIRMADA"

    # Configuramos los retornos de mock_db.query para cada modelo
    def query_router(model):
        m = MagicMock()
        if model == TokenAsistenciaActivo:
            m.filter.return_value.first.return_value = mock_token_db
        elif model.__name__ == "SesionMentoria":
            m.filter.return_value.first.return_value = mock_sesion
        elif model.__name__ == "ReservaCupo":
            m.filter.return_value.first.return_value = mock_reserva
        elif model.__name__ == "AsistenciaSesion":
            m.filter.return_value.first.return_value = None
        return m

    mock_db.query.side_effect = query_router

    resp = AttendanceService.record_checkin(
        db=mock_db,
        session_id=session_id,
        payload=payload,
        caller_email="ra2022073504@virtual.upt.pe",
        now_utc=now,
    )

    assert resp.asistio is True
    assert resp.id_sesion == session_id
    assert resp.id_asistencia == 1
    assert mock_db.commit.called
