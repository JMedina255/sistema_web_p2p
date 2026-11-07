from fastapi import APIRouter, Depends, Header, Request, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.profiles import (
    _extract_caller_and_admin_status,
    _resolve_authenticated_email,
)
from app.db.session import get_optional_session
from app.schemas.attendance import (
    AttendanceCheckinPayload,
    AttendanceCheckinResponse,
    AttendanceItemResponse,
    AttendanceTokenResponse,
)
from app.services.attendance_service import AttendanceService

router = APIRouter()


@router.get(
    "/{id_sesion}/attendance/token",
    response_model=AttendanceTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Generar token QR dinámico TOTP de 30 segundos para asistencia (T-34 / T-36 / CUS12)",
)
def get_attendance_token(
    id_sesion: int,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> AttendanceTokenResponse:
    """
    Genera un token criptográfico dinámico rotatorio cada 30 segundos para la proyección del código QR
    y un código numérico de 6 dígitos por el mentor titular.
    """
    caller_email = None
    is_admin = False
    if authorization:
        caller_email, is_admin = _extract_caller_and_admin_status(authorization)

    return AttendanceService.generate_token(
        db=db,
        session_id=id_sesion,
        caller_email=caller_email,
        is_admin=is_admin,
    )


@router.post(
    "/{id_sesion}/attendance/check-in",
    response_model=AttendanceCheckinResponse,
    status_code=status.HTTP_200_OK,
    summary="Registrar check-in de asistencia de mentoreado con reserva confirmada (T-34 / T-36 / CUS12 / RN-12)",
)
def record_attendance_checkin(
    id_sesion: int,
    payload: AttendanceCheckinPayload,
    request: Request,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> AttendanceCheckinResponse:
    """
    Registra la presencia efectiva del estudiante mentoreado:
    - Valida reserva previa en estado CONFIRMADA.
    - Valida ventana temporal [-15m, +30m].
    - Valida token dinámico TOTP o código numérico.
    - Captura traza de auditoría con IP de origen.
    """
    caller_email = None
    if authorization:
        caller_email = _resolve_authenticated_email(
            authorization, explicit_email=None, allow_admin_override=True
        )

    client_ip = request.client.host if request.client else "127.0.0.1"

    return AttendanceService.record_checkin(
        db=db,
        session_id=id_sesion,
        payload=payload,
        caller_email=caller_email,
        client_ip=client_ip,
    )


@router.get(
    "/{id_sesion}/attendance",
    response_model=list[AttendanceItemResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar nómina de asistencia de la sesión (T-34 / T-36 / CUS12)",
)
def get_session_attendance(
    id_sesion: int,
    db: Session | None = Depends(get_optional_session),
) -> list[AttendanceItemResponse]:
    """
    Retorna la lista de asistencia de los estudiantes inscritos en la sesión de mentoría.
    """
    return AttendanceService.get_roster(
        db=db,
        session_id=id_sesion,
    )
