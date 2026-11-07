import hashlib
import threading
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.bitacora import BitacoraPedagogica
from app.models.offer import SesionMentoria
from app.models.roles import Rol, UsuarioRol
from app.schemas.bitacora import BitacoraCreatePayload, BitacoraResponse
from app.services.offer_service import _memory_offers

_bitacora_lock = threading.RLock()
_memory_bitacoras: list[dict] = []
_bitacora_counter = 1


def clear_bitacoras_in_memory() -> None:
    """Helper para limpiar bitácoras en memoria durante pruebas."""
    global _bitacora_counter
    with _bitacora_lock:
        _memory_bitacoras.clear()
        _bitacora_counter = 1


class BitacoraService:
    """
    Servicio de Registro y Certificación de Bitácoras Pedagógicas (T-35 / RF17 / CUS13 / RN-12).
    - RN-12: Ventana perentoria de 48 horas tras el fin de la sesión.
    - Observaciones pedagógicas sustantivas (>= 50 caracteres).
    - Sellado criptográfico de integridad inmutable con hash SHA-256.
    - Acreditación de horas calculadas: duracion_minutos / 60.0.
    - Transición atómica de la sesión a BITACORA_REGISTRADA.
    """

    @classmethod
    def create_bitacora(
        cls,
        db: Session | None,
        session_id: int,
        payload: BitacoraCreatePayload,
        caller_email: str | None = None,
        is_admin: bool = False,
        now_utc: datetime | None = None,
    ) -> BitacoraResponse:
        if now_utc is None:
            now_utc = datetime.now(UTC)

        # 1. Base de datos
        if db is not None:
            sesion = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == session_id).first()
            if not sesion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: La sesión de mentoría no existe.",
                )

            # Control de titularidad del mentor
            if not caller_email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Se requiere autenticación para registrar la bitácora pedagógica.",
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
                        detail="FORBIDDEN: Solo el mentor titular o un administrador pueden registrar la bitácora pedagógica.",
                    )

            # Validación de ventana temporal de 48 horas (RN-12)
            s_start = sesion.fecha_inicio
            if s_start.tzinfo is None:
                s_start = s_start.replace(tzinfo=UTC)
            s_end = s_start + timedelta(minutes=sesion.duracion_minutos)
            deadline = s_end + timedelta(hours=48)

            if now_utc > deadline:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="DEADLINE_EXCEEDED: El plazo reglamentario de 48 horas para registrar la bitácora ha vencido (RN-12).",
                )

            # Validación sustantiva de observaciones (>= 50 caracteres)
            clean_obs = payload.observaciones.strip()
            if len(clean_obs) < 50:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="VALIDATION_ERROR: Las observaciones pedagógicas deben contener una descripción sustantiva de al menos 50 caracteres.",
                )

            # Generación de firma criptográfica SHA-256
            raw_signature = (
                f"{session_id}:{sesion.mentor_email}:{sorted(payload.temas_cubiertos)}:{now_utc.isoformat()}"
            )
            hash_firma = hashlib.sha256(raw_signature.encode("utf-8")).hexdigest()
            horas = round(sesion.duracion_minutos / 60.0, 2)

            existing_bitacora = (
                db.query(BitacoraPedagogica).filter(BitacoraPedagogica.id_sesion == session_id).first()
            )
            if existing_bitacora:
                existing_bitacora.temas_cubiertos = payload.temas_cubiertos
                existing_bitacora.observaciones = clean_obs
                existing_bitacora.nivel_dificultad = payload.nivel_dificultad
                existing_bitacora.hash_firma = hash_firma
                existing_bitacora.horas_declaradas = horas
                b_entity = existing_bitacora
            else:
                b_entity = BitacoraPedagogica(
                    id_sesion=session_id,
                    id_mentor=sesion.mentor_email,
                    temas_cubiertos=payload.temas_cubiertos,
                    observaciones=clean_obs,
                    nivel_dificultad=payload.nivel_dificultad,
                    hash_firma=hash_firma,
                    horas_declaradas=horas,
                    visado_administrador=False,
                    created_at=now_utc,
                )
                db.add(b_entity)

            sesion.estado = "BITACORA_REGISTRADA"
            db.commit()
            db.refresh(b_entity)

            return BitacoraResponse(
                id_bitacora=b_entity.id_bitacora,
                id_sesion=session_id,
                id_mentor=b_entity.id_mentor,
                temas_cubiertos=b_entity.temas_cubiertos,
                observaciones=b_entity.observaciones,
                nivel_dificultad=b_entity.nivel_dificultad,
                hash_firma=b_entity.hash_firma,
                horas_declaradas=b_entity.horas_declaradas,
                visado_administrador=b_entity.visado_administrador,
                created_at=b_entity.created_at.isoformat(),
                mensaje="Bitácora pedagógica registrada y sellada criptográficamente con éxito.",
            )

        # 2. En memoria
        global _bitacora_counter
        with _bitacora_lock:
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

            if not caller_email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Se requiere autenticación para registrar la bitácora pedagógica.",
                )

            clean_caller = caller_email.strip().lower()
            clean_mentor = target["mentor_email"].strip().lower()
            if not is_admin and clean_caller != clean_mentor:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="FORBIDDEN: Solo el mentor titular o un administrador pueden registrar la bitácora pedagógica.",
                )

            f_str = target.get("fecha_inicio", "")
            try:
                s_dt = datetime.fromisoformat(f_str.replace("Z", "+00:00"))
                if s_dt.tzinfo is None:
                    s_dt = s_dt.replace(tzinfo=UTC)
            except Exception:
                s_dt = now_utc - timedelta(hours=2)

            dur_min = target.get("duracion_minutos", 60)
            s_end = s_dt + timedelta(minutes=dur_min)
            deadline = s_end + timedelta(hours=48)

            if now_utc > deadline:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="DEADLINE_EXCEEDED: El plazo reglamentario de 48 horas para registrar la bitácora ha vencido (RN-12).",
                )

            clean_obs = payload.observaciones.strip()
            if len(clean_obs) < 50:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="VALIDATION_ERROR: Las observaciones pedagógicas deben contener una descripción sustantiva de al menos 50 caracteres.",
                )

            raw_sig = f"{session_id}:{target['mentor_email']}:{sorted(payload.temas_cubiertos)}:{now_utc.isoformat()}"
            hash_firma = hashlib.sha256(raw_sig.encode("utf-8")).hexdigest()
            horas = round(dur_min / 60.0, 2)

            existing = next((b for b in _memory_bitacoras if b["id_sesion"] == session_id), None)
            if existing:
                existing["temas_cubiertos"] = payload.temas_cubiertos
                existing["observaciones"] = clean_obs
                existing["nivel_dificultad"] = payload.nivel_dificultad
                existing["hash_firma"] = hash_firma
                existing["horas_declaradas"] = horas
                b_id = existing["id_bitacora"]
            else:
                b_id = _bitacora_counter
                _bitacora_counter += 1
                _memory_bitacoras.append(
                    {
                        "id_bitacora": b_id,
                        "id_sesion": session_id,
                        "id_mentor": target["mentor_email"],
                        "temas_cubiertos": payload.temas_cubiertos,
                        "observaciones": clean_obs,
                        "nivel_dificultad": payload.nivel_dificultad,
                        "hash_firma": hash_firma,
                        "horas_declaradas": horas,
                        "visado_administrador": False,
                        "created_at": now_utc.isoformat(),
                    }
                )

            target["estado"] = "BITACORA_REGISTRADA"

            return BitacoraResponse(
                id_bitacora=b_id,
                id_sesion=session_id,
                id_mentor=target["mentor_email"],
                temas_cubiertos=payload.temas_cubiertos,
                observaciones=clean_obs,
                nivel_dificultad=payload.nivel_dificultad,
                hash_firma=hash_firma,
                horas_declaradas=horas,
                visado_administrador=False,
                created_at=now_utc.isoformat(),
                mensaje="Bitácora pedagógica registrada y sellada criptográficamente con éxito.",
            )

    @classmethod
    def get_bitacora(cls, db: Session | None, session_id: int) -> BitacoraResponse:
        if db is not None:
            b = db.query(BitacoraPedagogica).filter(BitacoraPedagogica.id_sesion == session_id).first()
            if not b:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: No existe bitácora registrada para esta sesión.",
                )
            return BitacoraResponse(
                id_bitacora=b.id_bitacora,
                id_sesion=b.id_sesion,
                id_mentor=b.id_mentor,
                temas_cubiertos=b.temas_cubiertos,
                observaciones=b.observaciones,
                nivel_dificultad=b.nivel_dificultad,
                hash_firma=b.hash_firma,
                horas_declaradas=b.horas_declaradas,
                visado_administrador=b.visado_administrador,
                created_at=b.created_at.isoformat(),
            )

        with _bitacora_lock:
            existing = next((b for b in _memory_bitacoras if b["id_sesion"] == session_id), None)
            if not existing:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: No existe bitácora registrada para esta sesión.",
                )
            return BitacoraResponse(**existing)
