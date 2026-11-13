import hashlib
import threading
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.bitacora import BitacoraPedagogica
from app.models.curriculum import TemaConceptual
from app.models.offer import SesionMentoria
from app.models.roles import Rol, UsuarioRol
from app.schemas.bitacora import (
    BitacoraCreatePayload,
    BitacoraItemResponse,
    BitacoraObservacionResponse,
    BitacoraResponse,
    BitacoraVisadoResponse,
)
from app.services.offer_service import _memory_offers

_bitacora_lock = threading.RLock()
_memory_bitacoras: list[dict] = []
_bitacora_counter = 1


def _format_temas_cubiertos(
    raw_temas: list[Any] | None, topic_map: dict[int, str] | None = None
) -> list[str]:
    """
    Normaliza y formatea la lista de temas cubiertos.
    Si se suministraron IDs numéricos de temas silábicos, los resuelve a sus títulos descriptivos.
    """
    if not raw_temas:
        return []
    resolved: list[str] = []
    for item in raw_temas:
        if item is None:
            continue
        if topic_map:
            if isinstance(item, int) and item in topic_map:
                resolved.append(topic_map[item])
                continue
            if isinstance(item, str) and item.isdigit() and int(item) in topic_map:
                resolved.append(topic_map[int(item)])
                continue
        resolved.append(str(item))
    return resolved


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
            if sesion.estado.startswith("CANCELADA"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"INVALID_SESSION_STATE: No se puede registrar la bitácora de una sesión cancelada ({sesion.estado}).",
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

            if str(target.get("estado", "")).startswith("CANCELADA"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"INVALID_SESSION_STATE: No se puede registrar la bitácora de una sesión cancelada ({target.get('estado')}).",
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
            topic_map: dict[int, str] = {}
            try:
                topics = db.query(TemaConceptual).all()
                topic_map = {t.id_tema: t.nombre_tema for t in topics}
            except Exception:
                pass

            return BitacoraResponse(
                id_bitacora=b.id_bitacora,
                id_sesion=b.id_sesion,
                id_mentor=b.id_mentor,
                temas_cubiertos=_format_temas_cubiertos(b.temas_cubiertos, topic_map),
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
            item_data = dict(existing)
            item_data["temas_cubiertos"] = _format_temas_cubiertos(item_data.get("temas_cubiertos"))
            return BitacoraResponse(**item_data)

    @classmethod
    def visar_bitacora(
        cls,
        db: Session | None,
        bitacora_id: int,
        caller_email: str | None = None,
        is_admin: bool = False,
        now_utc: datetime | None = None,
    ) -> BitacoraVisadoResponse:
        """
        Visa y aprueba administrativamente una bitácora pedagógica (T-41 / RF26 / CUS22 / RN-14).
        - Exclusivo para rol administrador (RNF02).
        - Conmuta visado_administrador = True y sesion.estado = 'HORAS_VISADAS'.
        - Convalida horas declaradas como acreditadas.
        """
        if now_utc is None:
            now_utc = datetime.now(UTC)

        clean_caller = (caller_email or "").strip().lower()
        has_admin = is_admin

        if not has_admin and db is not None and clean_caller:
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
                        is not None
                    )
            except Exception:
                pass

        if not has_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ADMIN_ROLE_REQUIRED: Se requieren privilegios de Administrador de Escuela para auditar bitácoras.",
            )

        # 1. Base de datos
        if db is not None:
            b = (
                db.query(BitacoraPedagogica)
                .filter(
                    (BitacoraPedagogica.id_bitacora == bitacora_id)
                    | (BitacoraPedagogica.id_sesion == bitacora_id)
                )
                .first()
            )
            if not b:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: La bitácora pedagógica no existe.",
                )

            sesion = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == b.id_sesion).first()
            if sesion:
                if sesion.estado.startswith("CANCELADA"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"INVALID_SESSION_STATE: No se puede visar una bitácora de una sesión cancelada ({sesion.estado}).",
                    )
                if sesion.estado not in ("BITACORA_REGISTRADA", "HORAS_VISADAS", "OBSERVADA", "CONCLUIDA"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"INVALID_SESSION_STATE: Solo se pueden visar bitácoras de sesiones concluidas con bitácora registrada (estado actual: {sesion.estado}).",
                    )
                sesion.estado = "HORAS_VISADAS"
            b.visado_administrador = True

            db.commit()
            db.refresh(b)

            return BitacoraVisadoResponse(
                id_bitacora=b.id_bitacora,
                id_sesion=b.id_sesion,
                id_mentor=b.id_mentor,
                horas_declaradas=b.horas_declaradas,
                visado_administrador=True,
                estado_sesion=sesion.estado if sesion else "HORAS_VISADAS",
                auditor_email=clean_caller or "admin.epis@upt.pe",
                visado_at=now_utc.isoformat(),
                mensaje=f"Bitácora pedagógica visada institucionalmente con éxito. {b.horas_declaradas} horas formativas acreditadas para certificación.",
            )

        # 2. En memoria
        with _bitacora_lock:
            target_b = next(
                (
                    b
                    for b in _memory_bitacoras
                    if b["id_bitacora"] == bitacora_id
                    or str(b["id_bitacora"]) == str(bitacora_id)
                    or b["id_sesion"] == bitacora_id
                    or str(b["id_sesion"]) == str(bitacora_id)
                ),
                None,
            )
            if not target_b:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: La bitácora pedagógica no existe.",
                )

            s_id = target_b["id_sesion"]
            target_sesion = next(
                (
                    off
                    for off in _memory_offers
                    if off.get("id_sesion") == s_id or str(off.get("id_sesion")) == str(s_id)
                ),
                None,
            )
            if target_sesion:
                curr_estado = target_sesion.get("estado", "")
                if curr_estado.startswith("CANCELADA"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"INVALID_SESSION_STATE: No se puede visar una bitácora de una sesión cancelada ({curr_estado}).",
                    )
                if curr_estado not in ("BITACORA_REGISTRADA", "HORAS_VISADAS", "OBSERVADA", "CONCLUIDA"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"INVALID_SESSION_STATE: Solo se pueden visar bitácoras de sesiones concluidas con bitácora registrada (estado actual: {curr_estado}).",
                    )
                target_sesion["estado"] = "HORAS_VISADAS"
            target_b["visado_administrador"] = True

            return BitacoraVisadoResponse(
                id_bitacora=target_b["id_bitacora"],
                id_sesion=target_b["id_sesion"],
                id_mentor=target_b["id_mentor"],
                horas_declaradas=target_b["horas_declaradas"],
                visado_administrador=True,
                estado_sesion="HORAS_VISADAS",
                auditor_email=clean_caller or "admin.epis@upt.pe",
                visado_at=now_utc.isoformat(),
                mensaje=f"Bitácora pedagógica visada institucionalmente con éxito. {target_b['horas_declaradas']} horas formativas acreditadas para certificación.",
            )

    @classmethod
    def observar_bitacora(
        cls,
        db: Session | None,
        bitacora_id: int,
        motivo: str,
        caller_email: str | None = None,
        is_admin: bool = False,
        now_utc: datetime | None = None,
    ) -> BitacoraObservacionResponse:
        """
        Formula una observación de auditoría sobre la bitácora pedagógica (T-41 / RF26 / CUS22 / CUS25).
        - Exclusivo para rol administrador.
        - Requiere motivo sustantivo (>= 15 caracteres).
        - Transiciona el estado a 'OBSERVADA' y visado_administrador = False.
        """
        if now_utc is None:
            now_utc = datetime.now(UTC)

        clean_caller = (caller_email or "").strip().lower()
        has_admin = is_admin

        if not has_admin and db is not None and clean_caller:
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
                        is not None
                    )
            except Exception:
                pass

        if not has_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ADMIN_ROLE_REQUIRED: Se requieren privilegios de Administrador de Escuela para auditar bitácoras.",
            )

        clean_motivo = (motivo or "").strip()
        if len(clean_motivo) < 15:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="OBSERVATION_REASON_REQUIRED: Debe ingresar obligatoriamente una justificación para la observación técnica.",
            )

        # 1. Base de datos
        if db is not None:
            b = (
                db.query(BitacoraPedagogica)
                .filter(
                    (BitacoraPedagogica.id_bitacora == bitacora_id)
                    | (BitacoraPedagogica.id_sesion == bitacora_id)
                )
                .first()
            )
            if not b:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: La bitácora pedagógica no existe.",
                )

            sesion = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == b.id_sesion).first()
            if sesion:
                if sesion.estado.startswith("CANCELADA"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"INVALID_SESSION_STATE: No se puede observar una bitácora de una sesión cancelada ({sesion.estado}).",
                    )
                if sesion.estado not in ("BITACORA_REGISTRADA", "HORAS_VISADAS", "OBSERVADA", "CONCLUIDA"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"INVALID_SESSION_STATE: No se puede observar una bitácora de una sesión en estado {sesion.estado}.",
                    )
                sesion.estado = "OBSERVADA"
            b.visado_administrador = False

            db.commit()
            db.refresh(b)

            return BitacoraObservacionResponse(
                id_bitacora=b.id_bitacora,
                id_sesion=b.id_sesion,
                id_mentor=b.id_mentor,
                estado_sesion=sesion.estado if sesion else "OBSERVADA",
                motivo_observacion=clean_motivo,
                auditor_email=clean_caller or "admin.epis@upt.pe",
                observado_at=now_utc.isoformat(),
                mensaje="Bitácora observada para corrección técnica por el Administrador.",
            )

        # 2. En memoria
        with _bitacora_lock:
            target_b = next(
                (
                    b
                    for b in _memory_bitacoras
                    if b["id_bitacora"] == bitacora_id
                    or str(b["id_bitacora"]) == str(bitacora_id)
                    or b["id_sesion"] == bitacora_id
                    or str(b["id_sesion"]) == str(bitacora_id)
                ),
                None,
            )
            if not target_b:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: La bitácora pedagógica no existe.",
                )

            s_id = target_b["id_sesion"]
            target_sesion = next(
                (
                    off
                    for off in _memory_offers
                    if off.get("id_sesion") == s_id or str(off.get("id_sesion")) == str(s_id)
                ),
                None,
            )
            if target_sesion:
                curr_estado = target_sesion.get("estado", "")
                if curr_estado.startswith("CANCELADA"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"INVALID_SESSION_STATE: No se puede observar una bitácora de una sesión cancelada ({curr_estado}).",
                    )
                if curr_estado not in ("BITACORA_REGISTRADA", "HORAS_VISADAS", "OBSERVADA", "CONCLUIDA"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"INVALID_SESSION_STATE: No se puede observar una bitácora de una sesión en estado {curr_estado}.",
                    )
                target_sesion["estado"] = "OBSERVADA"
            target_b["visado_administrador"] = False

            return BitacoraObservacionResponse(
                id_bitacora=target_b["id_bitacora"],
                id_sesion=target_b["id_sesion"],
                id_mentor=target_b["id_mentor"],
                estado_sesion="OBSERVADA",
                motivo_observacion=clean_motivo,
                auditor_email=clean_caller or "admin.epis@upt.pe",
                observado_at=now_utc.isoformat(),
                mensaje="Bitácora observada para corrección técnica por el Administrador.",
            )

    @classmethod
    def list_bitacoras(
        cls,
        db: Session | None,
        estado_filtro: str | None = None,
        caller_email: str | None = None,
        is_admin: bool = False,
    ) -> list[BitacoraItemResponse]:
        """
        Retorna la lista de bitácoras registradas para la bandeja de auditoría administrativa (T-40).
        """
        clean_caller = (caller_email or "").strip().lower()
        has_admin = is_admin

        if not has_admin and db is not None and clean_caller:
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
                        is not None
                    )
            except Exception:
                pass

        if not has_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ADMIN_ROLE_REQUIRED: Se requieren privilegios de Administrador de Escuela para auditar bitácoras.",
            )

        clean_filtro = estado_filtro.strip().upper() if estado_filtro else None

        if db is not None:
            bitacoras = db.query(BitacoraPedagogica).all()
            topic_map: dict[int, str] = {}
            try:
                topics = db.query(TemaConceptual).all()
                topic_map = {t.id_tema: t.nombre_tema for t in topics}
            except Exception:
                pass

            results: list[BitacoraItemResponse] = []
            for b in bitacoras:
                sesion = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == b.id_sesion).first()
                estado = (
                    sesion.estado
                    if sesion
                    else ("HORAS_VISADAS" if b.visado_administrador else "BITACORA_REGISTRADA")
                )

                if clean_filtro and clean_filtro != "TODAS":
                    if clean_filtro == "PENDIENTES" and (
                        b.visado_administrador or estado != "BITACORA_REGISTRADA"
                    ):
                        continue
                    elif clean_filtro == "VISADAS" and (
                        not b.visado_administrador and estado != "HORAS_VISADAS"
                    ):
                        continue
                    elif clean_filtro not in ("PENDIENTES", "VISADAS") and estado != clean_filtro:
                        continue

                results.append(
                    BitacoraItemResponse(
                        id_bitacora=b.id_bitacora,
                        id_sesion=b.id_sesion,
                        codigo_sesion=sesion.codigo_sesion if sesion else f"SES-{b.id_sesion}",
                        id_mentor=b.id_mentor,
                        temas_cubiertos=_format_temas_cubiertos(b.temas_cubiertos, topic_map),
                        observaciones=b.observaciones,
                        nivel_dificultad=b.nivel_dificultad,
                        hash_firma=b.hash_firma,
                        horas_declaradas=b.horas_declaradas,
                        visado_administrador=b.visado_administrador,
                        estado_sesion=estado,
                        fecha_inicio=sesion.fecha_inicio.isoformat()
                        if sesion and sesion.fecha_inicio
                        else None,
                        created_at=b.created_at.isoformat(),
                    )
                )
            return results

        with _bitacora_lock:
            results = []
            for b in _memory_bitacoras:
                s_id = b["id_sesion"]
                target_sesion = next(
                    (
                        off
                        for off in _memory_offers
                        if off.get("id_sesion") == s_id or str(off.get("id_sesion")) == str(s_id)
                    ),
                    None,
                )
                estado = (
                    target_sesion.get("estado", "BITACORA_REGISTRADA")
                    if target_sesion
                    else ("HORAS_VISADAS" if b.get("visado_administrador") else "BITACORA_REGISTRADA")
                )

                if clean_filtro and clean_filtro != "TODAS":
                    if clean_filtro == "PENDIENTES" and (
                        b.get("visado_administrador") or estado != "BITACORA_REGISTRADA"
                    ):
                        continue
                    elif clean_filtro == "VISADAS" and (
                        not b.get("visado_administrador") and estado != "HORAS_VISADAS"
                    ):
                        continue
                    elif clean_filtro not in ("PENDIENTES", "VISADAS") and estado != clean_filtro:
                        continue

                results.append(
                    BitacoraItemResponse(
                        id_bitacora=b["id_bitacora"],
                        id_sesion=b["id_sesion"],
                        codigo_sesion=target_sesion.get("codigo_sesion", f"SES-{b['id_sesion']}")
                        if target_sesion
                        else f"SES-{b['id_sesion']}",
                        id_mentor=b["id_mentor"],
                        temas_cubiertos=_format_temas_cubiertos(b.get("temas_cubiertos")),
                        observaciones=b["observaciones"],
                        nivel_dificultad=b["nivel_dificultad"],
                        hash_firma=b["hash_firma"],
                        horas_declaradas=b["horas_declaradas"],
                        visado_administrador=b.get("visado_administrador", False),
                        estado_sesion=estado,
                        fecha_inicio=target_sesion.get("fecha_inicio") if target_sesion else None,
                        created_at=b.get("created_at", datetime.now(UTC).isoformat()),
                    )
                )
            return results
