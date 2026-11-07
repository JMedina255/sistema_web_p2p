import hashlib
import secrets
import threading
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.attendance import AsistenciaSesion
from app.models.booking import ReservaCupo
from app.models.offer import SesionMentoria
from app.models.roles import Rol, UsuarioRol
from app.schemas.attendance import (
    AttendanceCheckinPayload,
    AttendanceCheckinResponse,
    AttendanceItemResponse,
    AttendanceTokenResponse,
)
from app.services.booking_service import _booking_lock, _memory_bookings
from app.services.offer_service import _memory_offers

_attendance_lock = threading.RLock()
_memory_attendances: list[dict] = []
_active_attendance_tokens: dict[int, dict] = {}
_attendance_counter = 1


def clear_attendances_in_memory() -> None:
    """Helper para limpiar asistencias en memoria durante pruebas."""
    global _attendance_counter
    with _attendance_lock:
        _memory_attendances.clear()
        _active_attendance_tokens.clear()
        _attendance_counter = 1


class AttendanceService:
    """
    Servicio de Pase de Asistencia Digital con QR Dinámico TOTP (T-34 / T-36 / CUS12 / RF17 / RN-05 / RN-12).
    - Generación de token criptográfico TOTP rotatorio cada 30 segundos.
    - Check-in condicionado a reserva previa CONFIRMADA.
    - Ventana temporal estricta [fecha_inicio - 15m, fecha_fin + 30m].
    - Registro de traza de auditoría (IP y timestamp UTC).
    """

    @classmethod
    def generate_token(
        cls,
        db: Session | None,
        session_id: int,
        caller_email: str | None = None,
        is_admin: bool = False,
        now_utc: datetime | None = None,
    ) -> AttendanceTokenResponse:
        if now_utc is None:
            now_utc = datetime.now(UTC)

        if not caller_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Se requiere autenticación para generar el token de asistencia.",
            )

        # 1. Base de datos
        if db is not None:
            sesion = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == session_id).first()
            if not sesion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: La sesión de mentoría no existe.",
                )

            clean_caller = caller_email.strip().lower()
            clean_mentor = sesion.mentor_email.strip().lower()
            if clean_caller != clean_mentor:
                has_admin_role = is_admin
                if not has_admin_role:
                    try:
                        admin_rol = db.query(Rol).filter(Rol.nombre_rol == "administrador").first()
                        if admin_rol:
                            has_admin = (
                                db.query(UsuarioRol)
                                .filter(
                                    UsuarioRol.email == clean_caller,
                                    UsuarioRol.id_rol == admin_rol.id_rol,
                                    UsuarioRol.activo.is_(True),
                                )
                                .first()
                            )
                            if has_admin:
                                has_admin_role = True
                    except Exception:
                        pass
                if not has_admin_role:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="FORBIDDEN: Solo el mentor titular o un administrador pueden generar el token de asistencia.",
                    )
        else:
            target = next(
                (
                    o
                    for o in _memory_offers
                    if o.get("id_sesion") == session_id or str(o.get("id_sesion")) == str(session_id)
                ),
                None,
            )
            if not target:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: La sesión de mentoría no existe.",
                )
            clean_caller = caller_email.strip().lower()
            clean_mentor = target["mentor_email"].strip().lower()
            if not is_admin and clean_caller != clean_mentor:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="FORBIDDEN: Solo el mentor titular o un administrador pueden generar el token de asistencia.",
                )

        # Generar token y código numérico TOTP de 6 dígitos
        raw_seed = f"{session_id}:{now_utc.timestamp()}:{secrets.token_hex(8)}"
        token = hashlib.sha256(raw_seed.encode("utf-8")).hexdigest()
        totp_code = f"{secrets.randbelow(900000) + 100000}"
        expires_at = now_utc + timedelta(seconds=30)

        with _attendance_lock:
            _active_attendance_tokens[session_id] = {
                "token": token,
                "totp_code": totp_code,
                "expires_at": expires_at,
            }

        return AttendanceTokenResponse(
            session_id=session_id,
            token=token,
            totp_code=totp_code,
            expires_in=30,
            expires_at=expires_at.isoformat(),
        )

    @classmethod
    def record_checkin(
        cls,
        db: Session | None,
        session_id: int,
        payload: AttendanceCheckinPayload,
        caller_email: str | None = None,
        client_ip: str | None = None,
        now_utc: datetime | None = None,
    ) -> AttendanceCheckinResponse:
        if now_utc is None:
            now_utc = datetime.now(UTC)

        student_email = payload.estudiante_email or caller_email
        if not student_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="UNAUTHORIZED: No se pudo determinar la identidad institucional del estudiante mentoreado.",
            )
        student_email = student_email.strip().lower()

        # Validación estricta de código QR o código numérico TOTP
        if not payload.qr_token and not payload.numeric_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="TOKEN_OR_CODE_REQUIRED: Debe proporcionar el código QR dinámico o el código numérico de 6 dígitos de asistencia.",
            )

        with _attendance_lock:
            active_info = _active_attendance_tokens.get(session_id)
            if not active_info:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="NO_ACTIVE_ATTENDANCE_TOKEN: El mentor aún no ha iniciado el pase de asistencia digital para esta sesión.",
                )
            if now_utc > active_info["expires_at"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="QR_TOKEN_EXPIRED: El código de asistencia ha expirado. Por favor, escanee el código QR actualizado proyectado por el mentor.",
                )
            if payload.qr_token and payload.qr_token != active_info["token"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="QR_TOKEN_EXPIRED: Token de asistencia no válido o rotado.",
                )
            if payload.numeric_code and payload.numeric_code != active_info["totp_code"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="QR_TOKEN_EXPIRED: Código numérico de asistencia incorrecto o expirado.",
                )

        # 1. Base de datos
        if db is not None:
            sesion = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == session_id).first()
            if not sesion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: La sesión de mentoría no existe.",
                )

            # Validación de intervalo temporal [fecha_inicio - 15m, fecha_fin + 30m]
            s_start = sesion.fecha_inicio
            if s_start.tzinfo is None:
                s_start = s_start.replace(tzinfo=UTC)
            s_end = s_start + timedelta(minutes=sesion.duracion_minutos)
            window_start = s_start - timedelta(minutes=15)
            window_end = s_end + timedelta(minutes=30)

            if not (window_start <= now_utc <= window_end):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CHECKIN_WINDOW_CLOSED: El pase de asistencia sólo está habilitado durante la realización de la sesión (RN-12).",
                )

            # Comprobar reserva previa en estado CONFIRMADA
            reserva = (
                db.query(ReservaCupo)
                .filter(
                    ReservaCupo.id_sesion == session_id,
                    ReservaCupo.estudiante_email == student_email,
                    ReservaCupo.estado.in_(["CONFIRMADA", "ASISTIDA"]),
                )
                .first()
            )
            if not reserva:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="NO_CONFIRMED_BOOKING: No registra una reserva confirmada para esta sesión de mentoría.",
                )

            # Upsert en asistencias_sesion
            asistencia = (
                db.query(AsistenciaSesion)
                .filter(
                    AsistenciaSesion.id_sesion == session_id,
                    AsistenciaSesion.estudiante_email == student_email,
                )
                .first()
            )
            if asistencia:
                asistencia.asistio = True
                asistencia.fecha_checkin = now_utc
                asistencia.ip_origen = client_ip
            else:
                asistencia = AsistenciaSesion(
                    id_sesion=session_id,
                    estudiante_email=student_email,
                    asistio=True,
                    fecha_checkin=now_utc,
                    ip_origen=client_ip,
                    created_at=now_utc,
                )
                db.add(asistencia)

            reserva.estado = "ASISTIDA"
            db.commit()
            db.refresh(asistencia)

            return AttendanceCheckinResponse(
                id_asistencia=asistencia.id_asistencia,
                id_sesion=session_id,
                estudiante_email=student_email,
                asistio=True,
                fecha_checkin=now_utc.isoformat(),
                mensaje="¡Asistencia registrada exitosamente! Gracias por tu puntualidad.",
            )

        # 2. En memoria
        global _attendance_counter
        target = next(
            (
                o
                for o in _memory_offers
                if o.get("id_sesion") == session_id or str(o.get("id_sesion")) == str(session_id)
            ),
            None,
        )
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="NOT_FOUND: La sesión de mentoría no existe.",
            )

        f_str = target.get("fecha_inicio", "")
        try:
            s_dt = datetime.fromisoformat(f_str.replace("Z", "+00:00"))
            if s_dt.tzinfo is None:
                s_dt = s_dt.replace(tzinfo=UTC)
        except Exception:
            s_dt = now_utc

        dur_min = target.get("duracion_minutos", 60)
        s_end = s_dt + timedelta(minutes=dur_min)
        w_start = s_dt - timedelta(minutes=15)
        w_end = s_end + timedelta(minutes=30)

        if not (w_start <= now_utc <= w_end):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CHECKIN_WINDOW_CLOSED: El pase de asistencia sólo está habilitado durante la realización de la sesión (RN-12).",
            )

        with _booking_lock:
            reserva = next(
                (
                    b
                    for b in _memory_bookings
                    if (b["id_sesion"] == session_id or str(b["id_sesion"]) == str(session_id))
                    and b["estudiante_email"].lower() == student_email
                    and b["estado"] in ["CONFIRMADA", "ASISTIDA"]
                ),
                None,
            )
            if not reserva:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="NO_CONFIRMED_BOOKING: No registra una reserva confirmada para esta sesión de mentoría.",
                )
            reserva["estado"] = "ASISTIDA"

        with _attendance_lock:
            existing = next(
                (
                    a
                    for a in _memory_attendances
                    if a["id_sesion"] == session_id and a["estudiante_email"] == student_email
                ),
                None,
            )
            if existing:
                existing["asistio"] = True
                existing["fecha_checkin"] = now_utc.isoformat()
                a_id = existing["id_asistencia"]
            else:
                a_id = _attendance_counter
                _attendance_counter += 1
                _memory_attendances.append(
                    {
                        "id_asistencia": a_id,
                        "id_sesion": session_id,
                        "estudiante_email": student_email,
                        "asistio": True,
                        "fecha_checkin": now_utc.isoformat(),
                        "ip_origen": client_ip,
                        "created_at": now_utc.isoformat(),
                    }
                )

        return AttendanceCheckinResponse(
            id_asistencia=a_id,
            id_sesion=session_id,
            estudiante_email=student_email,
            asistio=True,
            fecha_checkin=now_utc.isoformat(),
            mensaje="¡Asistencia registrada exitosamente! Gracias por tu puntualidad.",
        )

    @classmethod
    def get_roster(cls, db: Session | None, session_id: int) -> list[AttendanceItemResponse]:
        if db is not None:
            records = (
                db.query(AsistenciaSesion)
                .filter(AsistenciaSesion.id_sesion == session_id)
                .order_by(AsistenciaSesion.estudiante_email.asc())
                .all()
            )
            return [
                AttendanceItemResponse(
                    id_asistencia=r.id_asistencia,
                    id_sesion=r.id_sesion,
                    estudiante_email=r.estudiante_email,
                    asistio=r.asistio,
                    fecha_checkin=r.fecha_checkin.isoformat() if r.fecha_checkin else None,
                )
                for r in records
            ]

        with _attendance_lock:
            items = [a for a in _memory_attendances if a["id_sesion"] == session_id]
            return [
                AttendanceItemResponse(
                    id_asistencia=a["id_asistencia"],
                    id_sesion=a["id_sesion"],
                    estudiante_email=a["estudiante_email"],
                    asistio=a["asistio"],
                    fecha_checkin=a.get("fecha_checkin"),
                )
                for a in items
            ]
