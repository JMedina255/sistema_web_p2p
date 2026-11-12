import html
import threading
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.attendance import AsistenciaSesion
from app.models.offer import SesionMentoria
from app.models.survey import EncuestaCalidad
from app.schemas.survey import SurveyCreatePayload, SurveyResponse, SurveyStatusResponse
from app.services.attendance_service import _memory_attendances
from app.services.booking_service import _memory_bookings
from app.services.offer_service import _memory_offers

_survey_lock = threading.RLock()
_memory_surveys: list[dict] = []
_survey_counter = 1


def clear_surveys_in_memory() -> None:
    """Helper para limpiar encuestas en memoria durante pruebas."""
    global _survey_counter
    with _survey_lock:
        _memory_surveys.clear()
        _survey_counter = 1


class SurveyService:
    """
    Servicio de Encuestas de Calidad y Satisfacción Post-Mentoría (T-38 / T-39 / CUS05 / RF18 / RN-12 / RN-13).
    - RN-12: Validación estricta de asistencia efectiva (asistio = True).
    - RN-13: Ventana temporal de 24 horas posteriores al fin de la sesión.
    - Prevención de duplicados (UNIQUE por sesión y estudiante).
    - Escala Likert de 1 a 5 estrellas en 4 dimensiones.
    - Retroalimentación cualitativa sustantiva (>= 20 caracteres si se incluye).
    """

    @classmethod
    def create_survey(
        cls,
        db: Session | None,
        session_id: int,
        payload: SurveyCreatePayload,
        caller_email: str | None = None,
        now_utc: datetime | None = None,
    ) -> SurveyResponse:
        if now_utc is None:
            now_utc = datetime.now(UTC)

        if not caller_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Se requiere autenticación para evaluar la mentoría.",
            )

        clean_caller = caller_email.strip().lower()

        # Validación sustantiva de comentarios si están presentes
        if payload.comentarios:
            clean_com = payload.comentarios.strip()
            if clean_com and len(clean_com) < 20:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="SURVEY_FEEDBACK_TOO_SHORT: Las observaciones cualitativas deben contener al menos 20 caracteres descriptivos.",
                )

        # 1. Base de datos
        if db is not None:
            sesion = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == session_id).first()
            if not sesion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: La sesión de mentoría no existe.",
                )

            if sesion.estado.startswith("CANCELADA"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"INVALID_SESSION_STATE: No se puede emitir una evaluación de calidad para una sesión cancelada ({sesion.estado}).",
                )

            # Comprobación de asistencia efectiva (RN-12)
            asistencia = (
                db.query(AsistenciaSesion)
                .filter(
                    AsistenciaSesion.id_sesion == session_id,
                    AsistenciaSesion.estudiante_email == clean_caller,
                )
                .first()
            )
            if not asistencia or not asistencia.asistio:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="SURVEY_NOT_ELIGIBLE: Solo los estudiantes cuya asistencia efectiva fue validada por el mentor pueden evaluar la sesión",
                )

            # Prevención de duplicados
            existing = (
                db.query(EncuestaCalidad)
                .filter(
                    EncuestaCalidad.id_sesion == session_id,
                    EncuestaCalidad.estudiante_email == clean_caller,
                )
                .first()
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="DUPLICATE_SURVEY_SUBMISSION: Ya has registrado tu evaluación para esta sesión de mentoría.",
                )

            # Ventana perentoria de 24 horas posteriores al cierre (RN-13)
            s_start = sesion.fecha_inicio
            if s_start.tzinfo is None:
                s_start = s_start.replace(tzinfo=UTC)
            s_end = s_start + timedelta(minutes=sesion.duracion_minutos)
            deadline = s_end + timedelta(hours=24)

            if now_utc < s_end:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="SURVEY_WINDOW_NOT_OPEN: La encuesta de calidad post-mentoría solo está disponible una vez concluida la sesión (RN-13).",
                )

            if now_utc > deadline:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="SURVEY_WINDOW_EXPIRED: La ventana perentoria de 24 horas para remitir la evaluación de calidad ha expirado",
                )

            sanitized_com = (
                html.escape(payload.comentarios.strip()) if payload.comentarios else None
            )

            encuesta = EncuestaCalidad(
                id_sesion=session_id,
                estudiante_email=clean_caller,
                calificacion_general=payload.calificacion_general,
                dominio_tema=payload.dominio_tema,
                claridad_explicacion=payload.claridad_explicacion,
                puntualidad=payload.puntualidad,
                comentarios=sanitized_com,
                created_at=now_utc,
            )
            db.add(encuesta)
            db.commit()
            db.refresh(encuesta)

            return SurveyResponse(
                id_encuesta=encuesta.id_encuesta,
                id_sesion=session_id,
                estudiante_email=encuesta.estudiante_email,
                calificacion_general=encuesta.calificacion_general,
                dominio_tema=encuesta.dominio_tema,
                claridad_explicacion=encuesta.claridad_explicacion,
                puntualidad=encuesta.puntualidad,
                comentarios=encuesta.comentarios,
                created_at=encuesta.created_at.isoformat(),
                mensaje="Evaluación de calidad post-mentoría registrada con éxito.",
            )

        # 2. En memoria
        global _survey_counter
        with _survey_lock:
            target = None
            for off in _memory_offers:
                if off.get("id_sesion") == session_id or str(off.get("id_sesion")) == str(session_id):
                    target = off
                    break

            if not target:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: La sesión de mentoría no existe.",
                )

            if str(target.get("estado", "")).startswith("CANCELADA"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"INVALID_SESSION_STATE: No se puede emitir una evaluación de calidad para una sesión cancelada ({target.get('estado')}).",
                )

            # Comprobación de inasistencia explícita y asistencia efectiva (RN-12)
            is_absent = any(
                a.get("id_sesion") == session_id
                and a.get("estudiante_email", "").strip().lower() == clean_caller
                and a.get("asistio") is False
                for a in _memory_attendances
            )
            has_attendance = any(
                a.get("id_sesion") == session_id
                and a.get("estudiante_email", "").strip().lower() == clean_caller
                and a.get("asistio") is True
                for a in _memory_attendances
            )
            has_booking_attended = any(
                b.get("id_sesion") == session_id
                and b.get("estudiante_email", "").strip().lower() == clean_caller
                and (b.get("asistio") is True or b.get("estado") == "ASISTIDA" or b.get("asistencia_confirmada") is True)
                for b in _memory_bookings
            )

            if is_absent or not (has_attendance or has_booking_attended):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="SURVEY_NOT_ELIGIBLE: Solo los estudiantes cuya asistencia efectiva fue validada por el mentor pueden evaluar la sesión",
                )

            # Prevención de duplicados
            if any(
                s.get("id_sesion") == session_id
                and s.get("estudiante_email", "").strip().lower() == clean_caller
                for s in _memory_surveys
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="DUPLICATE_SURVEY_SUBMISSION: Ya has registrado tu evaluación para esta sesión de mentoría.",
                )

            # Ventana perentoria de 24 horas posteriores al cierre (RN-13)
            f_str = target.get("fecha_inicio", "")
            try:
                s_dt = datetime.fromisoformat(f_str.replace("Z", "+00:00"))
                if s_dt.tzinfo is None:
                    s_dt = s_dt.replace(tzinfo=UTC)
            except Exception:
                s_dt = now_utc - timedelta(hours=1)

            dur_min = target.get("duracion_minutos", 60)
            s_end = s_dt + timedelta(minutes=dur_min)
            deadline = s_end + timedelta(hours=24)

            if now_utc < s_end:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="SURVEY_WINDOW_NOT_OPEN: La encuesta de calidad post-mentoría solo está disponible una vez concluida la sesión (RN-13).",
                )

            if now_utc > deadline:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="SURVEY_WINDOW_EXPIRED: La ventana perentoria de 24 horas para remitir la evaluación de calidad ha expirado",
                )

            sanitized_com = (
                html.escape(payload.comentarios.strip()) if payload.comentarios else None
            )

            s_id = _survey_counter
            _survey_counter += 1

            survey_dict = {
                "id_encuesta": s_id,
                "id_sesion": session_id,
                "estudiante_email": clean_caller,
                "calificacion_general": payload.calificacion_general,
                "dominio_tema": payload.dominio_tema,
                "claridad_explicacion": payload.claridad_explicacion,
                "puntualidad": payload.puntualidad,
                "comentarios": sanitized_com,
                "created_at": now_utc.isoformat(),
            }
            _memory_surveys.append(survey_dict)

            return SurveyResponse(
                id_encuesta=s_id,
                id_sesion=session_id,
                estudiante_email=clean_caller,
                calificacion_general=payload.calificacion_general,
                dominio_tema=payload.dominio_tema,
                claridad_explicacion=payload.claridad_explicacion,
                puntualidad=payload.puntualidad,
                comentarios=sanitized_com,
                created_at=now_utc.isoformat(),
                mensaje="Evaluación de calidad post-mentoría registrada con éxito.",
            )

    @classmethod
    def get_survey_status(
        cls,
        db: Session | None,
        session_id: int,
        caller_email: str | None = None,
        now_utc: datetime | None = None,
    ) -> SurveyStatusResponse:
        if now_utc is None:
            now_utc = datetime.now(UTC)

        clean_caller = caller_email.strip().lower() if caller_email else ""

        if db is not None:
            sesion = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == session_id).first()
            if not sesion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: La sesión de mentoría no existe.",
                )

            s_start = sesion.fecha_inicio
            if s_start.tzinfo is None:
                s_start = s_start.replace(tzinfo=UTC)
            s_end = s_start + timedelta(minutes=sesion.duracion_minutos)
            deadline = s_end + timedelta(hours=24)
            is_cancelled = sesion.estado.startswith("CANCELADA")
            window_open = (not is_cancelled) and (s_end <= now_utc <= deadline)

            has_surveyed = False
            eligible = False
            if clean_caller:
                existing = (
                    db.query(EncuestaCalidad)
                    .filter(
                        EncuestaCalidad.id_sesion == session_id,
                        EncuestaCalidad.estudiante_email == clean_caller,
                    )
                    .first()
                )
                has_surveyed = existing is not None

                asistencia = (
                    db.query(AsistenciaSesion)
                    .filter(
                        AsistenciaSesion.id_sesion == session_id,
                        AsistenciaSesion.estudiante_email == clean_caller,
                    )
                    .first()
                )
                eligible = bool(asistencia and asistencia.asistio and not is_cancelled)

            return SurveyStatusResponse(
                id_sesion=session_id,
                eligible=eligible,
                has_surveyed=has_surveyed,
                window_open=window_open,
                deadline=deadline.isoformat(),
                mensaje="Consulta de elegibilidad completada.",
            )

        with _survey_lock:
            target = None
            for off in _memory_offers:
                if off.get("id_sesion") == session_id or str(off.get("id_sesion")) == str(session_id):
                    target = off
                    break

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
                s_dt = now_utc - timedelta(hours=1)

            dur_min = target.get("duracion_minutos", 60)
            s_end = s_dt + timedelta(minutes=dur_min)
            deadline = s_end + timedelta(hours=24)
            is_cancelled = str(target.get("estado", "")).startswith("CANCELADA")
            window_open = (not is_cancelled) and (s_end <= now_utc <= deadline)

            has_surveyed = any(
                s.get("id_sesion") == session_id
                and s.get("estudiante_email", "").strip().lower() == clean_caller
                for s in _memory_surveys
            )
            is_absent = any(
                a.get("id_sesion") == session_id
                and a.get("estudiante_email", "").strip().lower() == clean_caller
                and a.get("asistio") is False
                for a in _memory_attendances
            )
            has_attendance = any(
                a.get("id_sesion") == session_id
                and a.get("estudiante_email", "").strip().lower() == clean_caller
                and a.get("asistio") is True
                for a in _memory_attendances
            )
            has_booking_attended = any(
                b.get("id_sesion") == session_id
                and b.get("estudiante_email", "").strip().lower() == clean_caller
                and (b.get("asistio") is True or b.get("estado") == "ASISTIDA" or b.get("asistencia_confirmada") is True)
                for b in _memory_bookings
            )
            eligible = (not is_cancelled) and (not is_absent) and (has_attendance or has_booking_attended)

            return SurveyStatusResponse(
                id_sesion=session_id,
                eligible=eligible,
                has_surveyed=has_surveyed,
                window_open=window_open,
                deadline=deadline.isoformat(),
                mensaje="Consulta de elegibilidad completada.",
            )
