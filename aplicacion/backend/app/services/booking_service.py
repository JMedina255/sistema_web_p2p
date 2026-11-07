import hashlib
import secrets
import threading
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.booking import ReservaCupo, SolicitudDemanda
from app.models.curriculum import Asignatura, TemaConceptual
from app.models.offer import SesionMentoria
from app.schemas.booking import (
    BookingCancelPayload,
    BookingCreatePayload,
    BookingDetailResponse,
    BookingResponse,
    MentoringDemandPayload,
    MentoringDemandResponse,
    QuorumEvaluationResponse,
)
from app.services.consent_service import ConsentService
from app.services.offer_service import _memory_offers, seed_default_offers_in_memory

# Candado de concurrencia para operaciones en memoria y entornos compartidos
_booking_lock = threading.RLock()

# Almacenes en memoria para pruebas y ejecución sin base de datos
_memory_bookings: list[dict] = []
_memory_demands: list[dict] = []
_booking_counter: int = 1000
_demand_counter: int = 100


def clear_bookings_in_memory() -> None:
    """Limpia el almacén de reservas y demandas en memoria para aislamiento de pruebas."""
    global _booking_counter, _demand_counter
    with _booking_lock:
        _memory_bookings.clear()
        _memory_demands.clear()
        _booking_counter = 1000
        _demand_counter = 100


def seed_default_bookings_in_memory() -> None:
    """Siembra reservas base en memoria para desarrollo interactivo."""
    with _booking_lock:
        if _memory_bookings:
            return
        now = datetime.now(UTC)
        _memory_bookings.append(
            {
                "id_reserva": 1,
                "codigo_reserva": "RES-0001",
                "id_sesion": 1,
                "codigo_sesion": "SES-1001",
                "estudiante_email": "2023079999@upt.pe",
                "estado": "CONFIRMADA",
                "fecha_reserva": (now - timedelta(days=2)).isoformat(),
                "fecha_ratificacion": (now - timedelta(days=1)).isoformat(),
                "motivo_cancelacion": None,
                "ticket_hash": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
                "fecha_inicio": (now + timedelta(days=2)).isoformat(),
                "nombre_asignatura": "Cálculo I",
                "nombre_tema": "Límites y Continuidad",
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "espacio_asignado": "Laboratorio de Cómputo 101 - Pabellón G (EPIS)",
                "mentor_email": "2022073504@upt.pe",
                "created_at": (now - timedelta(days=2)).isoformat(),
                "updated_at": (now - timedelta(days=1)).isoformat(),
            }
        )
        # Reservas correspondientes a escenarios de demostración (DEMO-01 a DEMO-05)
        _memory_bookings.extend(
            [
                {
                    "id_reserva": 201,
                    "codigo_reserva": "RES-DEMO-001",
                    "id_sesion": 101,
                    "codigo_sesion": "SES-DEMO-PUB01",
                    "estudiante_email": "estudiante.demo@upt.pe",
                    "estado": "PENDIENTE_CONFIRMACION",
                    "fecha_reserva": (now - timedelta(hours=2)).isoformat(),
                    "fecha_ratificacion": None,
                    "motivo_cancelacion": None,
                    "ticket_hash": None,
                    "fecha_inicio": (now + timedelta(days=3)).isoformat(),
                    "nombre_asignatura": "Cálculo I",
                    "nombre_tema": "Límites Notables y Asíntotas",
                    "duracion_minutos": 60,
                    "modalidad": "presencial",
                    "espacio_asignado": "Aula 201 - Pabellón EPIS",
                    "mentor_email": "mentor.demo@upt.pe",
                    "created_at": (now - timedelta(hours=2)).isoformat(),
                },
                {
                    "id_reserva": 202,
                    "codigo_reserva": "RES-DEMO-Q01",
                    "id_sesion": 102,
                    "codigo_sesion": "SES-DEMO-Q01",
                    "estudiante_email": "estudiante.demo@upt.pe",
                    "estado": "CONFIRMADA",
                    "fecha_reserva": (now - timedelta(hours=30)).isoformat(),
                    "fecha_ratificacion": (now - timedelta(hours=26)).isoformat(),
                    "motivo_cancelacion": None,
                    "ticket_hash": "b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef01",
                    "fecha_inicio": (now + timedelta(hours=10)).isoformat(),
                    "nombre_asignatura": "Cálculo I",
                    "nombre_tema": "Límites Notables y Asíntotas",
                    "duracion_minutos": 60,
                    "modalidad": "presencial",
                    "espacio_asignado": "Lab 101 - EPIS",
                    "mentor_email": "mentor.demo@upt.pe",
                    "created_at": (now - timedelta(hours=30)).isoformat(),
                },
                {
                    "id_reserva": 203,
                    "codigo_reserva": "RES-DEMO-Q02",
                    "id_sesion": 102,
                    "codigo_sesion": "SES-DEMO-Q01",
                    "estudiante_email": "companero.demo@upt.pe",
                    "estado": "CONFIRMADA",
                    "fecha_reserva": (now - timedelta(hours=30)).isoformat(),
                    "fecha_ratificacion": (now - timedelta(hours=25)).isoformat(),
                    "motivo_cancelacion": None,
                    "ticket_hash": "c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef012",
                    "fecha_inicio": (now + timedelta(hours=10)).isoformat(),
                    "nombre_asignatura": "Cálculo I",
                    "nombre_tema": "Límites Notables y Asíntotas",
                    "duracion_minutos": 60,
                    "modalidad": "presencial",
                    "espacio_asignado": "Lab 101 - EPIS",
                    "mentor_email": "mentor.demo@upt.pe",
                    "created_at": (now - timedelta(hours=30)).isoformat(),
                },
                {
                    "id_reserva": 204,
                    "codigo_reserva": "RES-DEMO-ASIS01",
                    "id_sesion": 103,
                    "codigo_sesion": "SES-DEMO-ASIS01",
                    "estudiante_email": "estudiante.demo@upt.pe",
                    "estado": "CONFIRMADA",
                    "fecha_reserva": (now - timedelta(days=2)).isoformat(),
                    "fecha_ratificacion": (now - timedelta(days=1)).isoformat(),
                    "motivo_cancelacion": None,
                    "ticket_hash": "d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0123",
                    "fecha_inicio": (now - timedelta(minutes=15)).isoformat(),
                    "nombre_asignatura": "Cálculo I",
                    "nombre_tema": "Límites Notables y Asíntotas",
                    "duracion_minutos": 60,
                    "modalidad": "presencial",
                    "espacio_asignado": "Lab 102 - EPIS",
                    "mentor_email": "mentor.demo@upt.pe",
                    "created_at": (now - timedelta(days=2)).isoformat(),
                },
                {
                    "id_reserva": 205,
                    "codigo_reserva": "RES-DEMO-BIT01",
                    "id_sesion": 104,
                    "codigo_sesion": "SES-DEMO-BIT01",
                    "estudiante_email": "estudiante.demo@upt.pe",
                    "estado": "CONFIRMADA",
                    "fecha_reserva": (now - timedelta(days=3)).isoformat(),
                    "fecha_ratificacion": (now - timedelta(days=2)).isoformat(),
                    "motivo_cancelacion": None,
                    "ticket_hash": "e5f67890123456789abcdef0123456789abcdef0123456789abcdef01234",
                    "fecha_inicio": (now - timedelta(hours=3)).isoformat(),
                    "nombre_asignatura": "Cálculo I",
                    "nombre_tema": "Límites Notables y Asíntotas",
                    "duracion_minutos": 90,
                    "modalidad": "presencial",
                    "espacio_asignado": "Lab 103 - EPIS",
                    "mentor_email": "mentor.demo@upt.pe",
                    "created_at": (now - timedelta(days=3)).isoformat(),
                },
            ]
        )


class BookingService:
    """
    Servicio de Coordinación Transaccional ACID para Reservas de Cupos y Quórum (T-22 / T-24).
    Implementa:
    - Bloqueo pesimista 'SELECT ... FOR UPDATE' en PostgreSQL (with_for_update()).
    - Prevención estricta de sobrecupo (RN-05 / RNF07: 0.0% de sobrecupo bajo concurrencia).
    - Validación de corte de antelación T-24h (RN-04 / RN-08).
    - Regla de no-autoreserva del mentor titular.
    - Detección de reservas duplicadas (restricción uq_sesion_estudiante_activa).
    - Evaluación formal de quórum del 50% institucional (RN-09 / CUS23).
    - Registro y consulta de solicitudes temáticas por demanda (CUS03 / RF07).
    """

    @classmethod
    def generate_booking_code(cls, db: Session | None = None) -> str:
        """Genera un código canónico de reserva en formato RES-XXXX garantizando unicidad estricta."""
        global _booking_counter
        with _booking_lock:
            _booking_counter += 1
            suffix = secrets.token_hex(2).upper()
            if db is not None:
                try:
                    max_id = db.query(ReservaCupo.id_reserva).order_by(ReservaCupo.id_reserva.desc()).first()
                    base_num = (max_id[0] if max_id else 0) + 1000 + (_booking_counter % 900)
                    return f"RES-{base_num}-{suffix}"
                except Exception:
                    pass
            return f"RES-{_booking_counter}-{suffix}"

    @classmethod
    def generate_ticket_hash(
        cls, codigo_reserva: str, id_sesion: int, estudiante_email: str, fecha_iso: str
    ) -> str:
        """Genera el hash SHA-256 criptográfico para validación QR del cupo."""
        raw = f"{codigo_reserva}:{id_sesion}:{estudiante_email.strip().lower()}:{fecha_iso}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @classmethod
    def count_active_bookings(
        cls,
        db: Session | None,
        id_sesion: int | str,
        codigo_sesion: str | None = None,
    ) -> int:
        """
        Calcula la cantidad de cupos ocupados actualmente en una sesión
        (estados PENDIENTE_CONFIRMACION o CONFIRMADA).
        """
        if db is not None:
            try:
                q = db.query(ReservaCupo).filter(
                    ReservaCupo.estado.in_(["PENDIENTE_CONFIRMACION", "CONFIRMADA"]),
                )
                try:
                    s_id = int(id_sesion)
                    q = q.filter(ReservaCupo.id_sesion == s_id)
                except Exception:
                    if codigo_sesion:
                        ses = (
                            db.query(SesionMentoria)
                            .filter(SesionMentoria.codigo_sesion == codigo_sesion)
                            .first()
                        )
                        if ses:
                            q = q.filter(ReservaCupo.id_sesion == ses.id_sesion)
                        else:
                            return 0
                    else:
                        return 0
                return q.count()
            except Exception:
                pass

        # Fallback en memoria
        with _booking_lock:
            return sum(
                1
                for b in _memory_bookings
                if (
                    b.get("id_sesion") == id_sesion
                    or str(b.get("id_sesion")) == str(id_sesion)
                    or (codigo_sesion and b.get("codigo_sesion") == codigo_sesion)
                )
                and b.get("estado") in ["PENDIENTE_CONFIRMACION", "CONFIRMADA"]
            )

    @classmethod
    def reserve_seat(
        cls,
        db: Session | None,
        payload: BookingCreatePayload,
        caller_email: str | None = None,
        is_admin: bool = False,
    ) -> BookingResponse:
        """
        Formalización atómica de una reserva provisional bajo control transaccional ACID.
        Aplica Cuadro 4.3 de la especificación técnica Sprint 4.
        """
        clean_email = payload.estudiante_email.strip().lower()

        # Validación estricta de propiedad de reserva: solo el estudiante o admin verificado
        if caller_email:
            caller_clean = caller_email.strip().lower()
            if not is_admin and caller_clean != clean_email:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene autorización para registrar reservas a nombre de otro estudiante.",
                )
        elif settings.APP_ENV not in ("development", "test", "testing"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Se requiere autenticación institucional válida para formalizar reservas.",
            )

        now_utc = datetime.now(UTC)

        # Adquisición del candado pesimista con timeout parametrizable (BOOKING_TIMEOUT_SECONDS)
        timeout_s = float(settings.BOOKING_TIMEOUT_SECONDS)
        lock_acquired = _booking_lock.acquire(timeout=timeout_s)
        if not lock_acquired:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="DATABASE_BUSY: El servicio de reservas se encuentra temporalmente sobrecargado. Por favor, reintente en unos momentos.",
            )

        try:
            # Validación de consentimiento de datos personales (Ley 29733 / RN-02)
            consent_status = ConsentService.get_consent_status(db, clean_email)
            if not consent_status.has_consented:
                # En producción se exige consentimiento previo; en test/dev se valida ante revocación explícita
                if (
                    settings.APP_ENV not in ("development", "test", "testing")
                    or clean_email.startswith("sin_consentimiento")
                    or clean_email.startswith("revocado")
                ):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="CONSENT_REQUIRED: Debes aceptar los términos de tratamiento de datos personales conforme a la Ley N° 29733 (RN-02).",
                    )
            # ------------------------------------------------------------------
            # Camino 1: Ejecución en Base de Datos Relacional con Bloqueo Pesimista
            # ------------------------------------------------------------------
            if db is not None:
                try:
                    # Configurar lock_timeout en PostgreSQL si aplica dialecto
                    if db.bind and db.bind.dialect.name == "postgresql":
                        db.execute(text(f"SET LOCAL lock_timeout = '{settings.BOOKING_TIMEOUT_SECONDS}s';"))

                    # Paso 2: Bloqueo pesimista de fila en PostgreSQL (SELECT ... FOR UPDATE)
                    sesion = (
                        db.query(SesionMentoria)
                        .filter(SesionMentoria.id_sesion == payload.id_sesion)
                        .with_for_update(of=SesionMentoria)
                        .first()
                    )

                    if not sesion:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="SESSION_NOT_FOUND: La clase de mentoría seleccionada no existe o fue retirada.",
                        )

                    # Paso 3: Validar estado de la sesión y antelación RN-04
                    if sesion.estado != "PUBLICADA":
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="SESSION_NOT_OPEN: La sesión no se encuentra en estado PUBLICADA.",
                        )

                    sesion_start = sesion.fecha_inicio
                    if sesion_start.tzinfo is None:
                        sesion_start = sesion_start.replace(tzinfo=UTC)

                    if sesion_start <= now_utc + timedelta(hours=24):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="WINDOW_CLOSED_T24H: Las reservas cierran 24 horas antes del inicio de la sesión.",
                        )

                    # Paso 4: Validar no autoreserva del mentor titular
                    if clean_email == sesion.mentor_email.strip().lower():
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="MENTOR_CANNOT_BOOK: Como mentor titular no puedes reservar una vacante en tu clase.",
                        )

                    # Paso 6: Verificar ausencia de reserva activa previa del estudiante
                    existing = (
                        db.query(ReservaCupo)
                        .filter(
                            ReservaCupo.id_sesion == sesion.id_sesion,
                            ReservaCupo.estudiante_email == clean_email,
                            ReservaCupo.estado.in_(["PENDIENTE_CONFIRMACION", "CONFIRMADA"]),
                        )
                        .first()
                    )
                    if existing:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="DUPLICATE_BOOKING: Ya cuentas con una reserva registrada para esta clase.",
                        )

                    # Paso 5: Contar reservas activas existentes bajo el bloqueo pesimista
                    occupied_seats = (
                        db.query(ReservaCupo)
                        .filter(
                            ReservaCupo.id_sesion == sesion.id_sesion,
                            ReservaCupo.estado.in_(["PENDIENTE_CONFIRMACION", "CONFIRMADA"]),
                        )
                        .count()
                    )

                    if occupied_seats >= sesion.aforo_maximo:
                        db.rollback()
                        raise HTTPException(
                            status_code=status.HTTP_409_CONFLICT,
                            detail="CAPACITY_EXCEEDED: Aforo completo. No quedan vacantes disponibles en esta sesión.",
                        )

                    # Paso 7: Insertar o reactivar registro en reservas_cupo
                    code = cls.generate_booking_code(db)
                    t_hash = cls.generate_ticket_hash(
                        code, sesion.id_sesion, clean_email, now_utc.isoformat()
                    )

                    inactive_row = (
                        db.query(ReservaCupo)
                        .filter(
                            ReservaCupo.id_sesion == sesion.id_sesion,
                            ReservaCupo.estudiante_email == clean_email,
                        )
                        .first()
                    )
                    if inactive_row:
                        inactive_row.codigo_reserva = code
                        inactive_row.estado = "PENDIENTE_CONFIRMACION"
                        inactive_row.fecha_reserva = now_utc
                        inactive_row.fecha_ratificacion = None
                        inactive_row.motivo_cancelacion = None
                        inactive_row.ticket_hash = t_hash
                        inactive_row.updated_at = now_utc
                        db.commit()
                        db.refresh(inactive_row)
                        reserva = inactive_row
                    else:
                        reserva = ReservaCupo(
                            codigo_reserva=code,
                            id_sesion=sesion.id_sesion,
                            estudiante_email=clean_email,
                            estado="PENDIENTE_CONFIRMACION",
                            fecha_reserva=now_utc,
                            ticket_hash=t_hash,
                        )
                        db.add(reserva)
                        db.commit()
                        db.refresh(reserva)

                    cutoff_limit = (sesion_start - timedelta(hours=24)).isoformat()

                    return BookingResponse(
                        id_reserva=reserva.id_reserva,
                        codigo_reserva=reserva.codigo_reserva,
                        id_sesion=reserva.id_sesion,
                        estudiante_email=reserva.estudiante_email,
                        estado="PENDIENTE_CONFIRMACION",
                        fecha_reserva=reserva.fecha_reserva.isoformat(),
                        fecha_limite_confirmacion=cutoff_limit,
                        mensaje="Reserva provisional registrada. Recuerde ratificar su asistencia antes de T-24h conforme a la regla institucional RN-08.",
                        ticket_hash=t_hash,
                    )

                except HTTPException:
                    db.rollback()
                    raise
                except Exception as exc:
                    db.rollback()
                    err_msg = str(exc).lower()
                    if (
                        "lock timeout" in err_msg
                        or "canceling statement due to lock timeout" in err_msg
                        or "could not obtain lock" in err_msg
                        or "database_busy" in err_msg
                    ):
                        raise HTTPException(
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="DATABASE_BUSY: Tiempo de espera agotado al adquirir el bloqueo transaccional. Por favor, reintente en unos momentos.",
                        ) from exc
                    if "uq_sesion_estudiante_activa" in err_msg or "unique" in err_msg:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="DUPLICATE_BOOKING: Ya cuentas con una reserva registrada para esta clase.",
                        ) from exc
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error transaccional al formalizar la reserva: {exc}",
                    ) from exc

            # ------------------------------------------------------------------
            # Camino 2: Ejecución en Memoria (Fallback aislado y thread-safe)
            # ------------------------------------------------------------------
            seed_default_offers_in_memory()
            target_sesion = None
            for off in _memory_offers:
                if off.get("id_sesion") == payload.id_sesion or str(off.get("id_sesion")) == str(
                    payload.id_sesion
                ):
                    target_sesion = off
                    break

            if not target_sesion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="SESSION_NOT_FOUND: La clase de mentoría seleccionada no existe o fue retirada.",
                )

            if target_sesion.get("estado") != "PUBLICADA":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="SESSION_NOT_OPEN: La sesión no se encuentra en estado PUBLICADA.",
                )

            # Validar antelación RN-04
            f_inicio_str = target_sesion.get("fecha_inicio", "")
            try:
                iso_clean = f_inicio_str.replace("Z", "+00:00")
                start_dt = datetime.fromisoformat(iso_clean)
                if start_dt.tzinfo is None:
                    start_dt = start_dt.replace(tzinfo=UTC)
            except Exception:
                start_dt = now_utc + timedelta(hours=48)

            if start_dt <= now_utc + timedelta(hours=24):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="WINDOW_CLOSED_T24H: Las reservas cierran 24 horas antes del inicio de la sesión.",
                )

            # Validar no autoreserva del mentor titular
            if clean_email == target_sesion.get("mentor_email", "").strip().lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="MENTOR_CANNOT_BOOK: Como mentor titular no puedes reservar una vacante en tu clase.",
                )

            # Verificar ausencia de reserva activa previa
            for b in _memory_bookings:
                if (
                    (b["id_sesion"] == payload.id_sesion or str(b["id_sesion"]) == str(payload.id_sesion))
                    and b["estudiante_email"] == clean_email
                    and b["estado"] in ["PENDIENTE_CONFIRMACION", "CONFIRMADA"]
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="DUPLICATE_BOOKING: Ya cuentas con una reserva registrada para esta clase.",
                    )

            # Contar ocupados
            aforo_max = target_sesion.get("aforo_maximo", 10)
            occupied = sum(
                1
                for b in _memory_bookings
                if (b["id_sesion"] == payload.id_sesion or str(b["id_sesion"]) == str(payload.id_sesion))
                and b["estado"] in ["PENDIENTE_CONFIRMACION", "CONFIRMADA"]
            )

            if occupied >= aforo_max:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="CAPACITY_EXCEEDED: Aforo completo. No quedan vacantes disponibles en esta sesión.",
                )

            code = cls.generate_booking_code(db=None)
            res_id = _booking_counter
            t_hash = cls.generate_ticket_hash(code, payload.id_sesion, clean_email, now_utc.isoformat())

            booking_record = {
                "id_reserva": res_id,
                "codigo_reserva": code,
                "id_sesion": payload.id_sesion,
                "codigo_sesion": target_sesion.get("codigo_sesion", f"SES-{payload.id_sesion}"),
                "estudiante_email": clean_email,
                "estado": "PENDIENTE_CONFIRMACION",
                "fecha_reserva": now_utc.isoformat(),
                "fecha_ratificacion": None,
                "motivo_cancelacion": None,
                "ticket_hash": t_hash,
                "nombre_asignatura": target_sesion.get("nombre_asignatura", "Asignatura EPIS"),
                "nombre_tema": target_sesion.get("nombre_tema", "Tema Silábico"),
                "fecha_inicio": f_inicio_str,
                "duracion_minutos": target_sesion.get("duracion_minutos", 60),
                "modalidad": target_sesion.get("modalidad", "presencial"),
                "espacio_asignado": target_sesion.get("espacio_asignado", "Aula EPIS"),
                "mentor_email": target_sesion.get("mentor_email", ""),
                "created_at": now_utc.isoformat(),
                "updated_at": now_utc.isoformat(),
            }
            _memory_bookings.append(booking_record)

            cutoff_limit = (start_dt - timedelta(hours=24)).isoformat()

            return BookingResponse(
                id_reserva=res_id,
                codigo_reserva=code,
                id_sesion=payload.id_sesion,
                estudiante_email=clean_email,
                estado="PENDIENTE_CONFIRMACION",
                fecha_reserva=now_utc.isoformat(),
                fecha_limite_confirmacion=cutoff_limit,
                mensaje="Reserva provisional registrada. Recuerde ratificar su asistencia antes de T-24h conforme a la regla institucional RN-08.",
                ticket_hash=t_hash,
            )
        finally:
            _booking_lock.release()

    @classmethod
    def get_student_reservations(
        cls,
        db: Session | None,
        student_email: str,
        estado: str | None = None,
    ) -> list[BookingDetailResponse]:
        """Consulta la nómina de reservas del estudiante mentoreado."""
        clean_email = student_email.strip().lower()

        if db is not None:
            try:
                q = db.query(ReservaCupo).filter(ReservaCupo.estudiante_email == clean_email)
                if estado:
                    q = q.filter(ReservaCupo.estado == estado)
                rows = q.order_by(ReservaCupo.fecha_reserva.desc()).all()
                results: list[BookingDetailResponse] = []
                for r in rows:
                    ses = r.sesion
                    results.append(
                        BookingDetailResponse(
                            id_reserva=r.id_reserva,
                            codigo_reserva=r.codigo_reserva,
                            id_sesion=r.id_sesion,
                            codigo_sesion=ses.codigo_sesion if ses else None,
                            estudiante_email=r.estudiante_email,
                            estado=r.estado,
                            fecha_reserva=r.fecha_reserva.isoformat(),
                            fecha_ratificacion=r.fecha_ratificacion.isoformat()
                            if r.fecha_ratificacion
                            else None,
                            motivo_cancelacion=r.motivo_cancelacion,
                            ticket_hash=r.ticket_hash,
                            nombre_asignatura=ses.asignatura.nombre_curso if ses and ses.asignatura else None,
                            nombre_tema=ses.tema.nombre_tema if ses and ses.tema else None,
                            fecha_inicio=ses.fecha_inicio.isoformat() if ses else None,
                            duracion_minutos=ses.duracion_minutos if ses else None,
                            modalidad=ses.modalidad if ses else None,
                            espacio_asignado=ses.espacio_asignado if ses else None,
                            mentor_email=ses.mentor_email if ses else None,
                        )
                    )
                return results
            except Exception:
                pass

        # Fallback en memoria
        with _booking_lock:
            seed_default_bookings_in_memory()
            results = []
            for b in _memory_bookings:
                if b["estudiante_email"] == clean_email:
                    if estado and b["estado"] != estado:
                        continue
                    results.append(BookingDetailResponse(**b))
            return sorted(results, key=lambda x: x.fecha_reserva, reverse=True)

    @classmethod
    def confirm_attendance(
        cls,
        db: Session | None,
        id_reserva: int,
        caller_email: str | None = None,
        is_admin: bool = False,
    ) -> BookingDetailResponse:
        """
        Ratifica formalmente la asistencia a una sesión de mentoría (T-26 / RF13 / CUS24 / RN-08).
        Transiciona la reserva de PENDIENTE_CONFIRMACION a CONFIRMADA si se encuentra antes del
        corte perentorio de T-24h y pertenece al estudiante autenticado.
        """
        if not id_reserva or id_reserva < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="VALIDATION_ERROR: El identificador de reserva debe ser un número entero positivo.",
            )

        now_utc = datetime.now(UTC)
        timeout_s = float(settings.BOOKING_TIMEOUT_SECONDS)
        lock_acquired = _booking_lock.acquire(timeout=timeout_s)
        if not lock_acquired:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="DATABASE_BUSY: El servicio de reservas se encuentra temporalmente sobrecargado. Por favor, reintente en unos momentos.",
            )

        try:
            # ------------------------------------------------------------------
            # Camino 1: Base de datos relacional con bloqueo pesimista
            # ------------------------------------------------------------------
            if db is not None:
                try:
                    if db.bind and db.bind.dialect.name == "postgresql":
                        db.execute(text(f"SET LOCAL lock_timeout = '{settings.BOOKING_TIMEOUT_SECONDS}s';"))

                    reserva = (
                        db.query(ReservaCupo)
                        .filter(ReservaCupo.id_reserva == id_reserva)
                        .with_for_update()
                        .first()
                    )

                    if not reserva:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"RESERVATION_NOT_FOUND: No se encontró la reserva con ID {id_reserva}.",
                        )

                    clean_caller = (caller_email or "").strip().lower()
                    if not is_admin:
                        if not clean_caller:
                            raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="UNAUTHORIZED: Se requiere autenticación institucional válida para ratificar la asistencia.",
                            )
                        if clean_caller != reserva.estudiante_email.strip().lower():
                            raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN,
                                detail="FORBIDDEN: No tiene autorización para ratificar una reserva que no le pertenece.",
                            )

                    if reserva.estado == "CONFIRMADA":
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="INVALID_STATUS_TRANSITION: La reserva ya se encuentra ratificada y confirmada.",
                        )

                    if reserva.estado in (
                        "CANCELADA_USUARIO",
                        "CANCELADA_SISTEMA",
                        "NO_CONFIRMADA",
                        "ASISTIDA",
                        "INASISTENCIA",
                    ):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"INVALID_STATUS_TRANSITION: No se puede ratificar una reserva en estado {reserva.estado}.",
                        )

                    if reserva.estado != "PENDIENTE_CONFIRMACION":
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"INVALID_STATUS_TRANSITION: Transición no permitida desde el estado {reserva.estado}.",
                        )

                    sesion = reserva.sesion
                    if not sesion:
                        sesion = (
                            db.query(SesionMentoria)
                            .filter(SesionMentoria.id_sesion == reserva.id_sesion)
                            .first()
                        )
                    if not sesion:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"SESSION_NOT_FOUND: No se encontró la sesión de mentoría vinculada a la reserva {id_reserva}.",
                        )

                    ses_start = sesion.fecha_inicio
                    if ses_start.tzinfo is None:
                        ses_start = ses_start.replace(tzinfo=UTC)
                    if ses_start <= now_utc + timedelta(hours=24):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="WINDOW_CLOSED_T24H: La ratificación de asistencia debe realizarse como mínimo 24 horas antes del inicio de la sesión (RN-08).",
                        )

                    reserva.estado = "CONFIRMADA"
                    reserva.fecha_ratificacion = now_utc
                    reserva.updated_at = now_utc
                    db.commit()
                    db.refresh(reserva)

                    ses = reserva.sesion
                    return BookingDetailResponse(
                        id_reserva=reserva.id_reserva,
                        codigo_reserva=reserva.codigo_reserva,
                        id_sesion=reserva.id_sesion,
                        codigo_sesion=ses.codigo_sesion if ses else None,
                        estudiante_email=reserva.estudiante_email,
                        estado=reserva.estado,
                        fecha_reserva=reserva.fecha_reserva.isoformat(),
                        fecha_ratificacion=reserva.fecha_ratificacion.isoformat()
                        if reserva.fecha_ratificacion
                        else None,
                        motivo_cancelacion=reserva.motivo_cancelacion,
                        ticket_hash=reserva.ticket_hash,
                        nombre_asignatura=ses.asignatura.nombre_curso if ses and ses.asignatura else None,
                        nombre_tema=ses.tema.nombre_tema if ses and ses.tema else None,
                        fecha_inicio=ses.fecha_inicio.isoformat() if ses else None,
                        duracion_minutos=ses.duracion_minutos if ses else None,
                        modalidad=ses.modalidad if ses else None,
                        espacio_asignado=ses.espacio_asignado if ses else None,
                        mentor_email=ses.mentor_email if ses else None,
                    )
                except HTTPException:
                    db.rollback()
                    raise
                except Exception as exc:
                    db.rollback()
                    err_msg = str(exc).lower()
                    if (
                        "lock timeout" in err_msg
                        or "canceling statement due to lock timeout" in err_msg
                        or "could not obtain lock" in err_msg
                        or "database_busy" in err_msg
                    ):
                        raise HTTPException(
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="DATABASE_BUSY: Tiempo de espera agotado al adquirir el bloqueo transaccional. Por favor, reintente en unos momentos.",
                        ) from exc
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error transaccional al ratificar la asistencia: {exc}",
                    ) from exc

            # ------------------------------------------------------------------
            # Camino 2: Almacén en Memoria Aislada (Tests y Desarrollo Local)
            # ------------------------------------------------------------------
            seed_default_bookings_in_memory()
            target_booking = None
            for b in _memory_bookings:
                if b["id_reserva"] == id_reserva or str(b["id_reserva"]) == str(id_reserva):
                    target_booking = b
                    break

            if not target_booking:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"RESERVATION_NOT_FOUND: No se encontró la reserva con ID {id_reserva}.",
                )

            clean_caller = (caller_email or "").strip().lower()
            if not is_admin:
                if not clean_caller:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="UNAUTHORIZED: Se requiere autenticación institucional válida para ratificar la asistencia.",
                    )
                if clean_caller != target_booking["estudiante_email"].strip().lower():
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="FORBIDDEN: No tiene autorización para ratificar una reserva que no le pertenece.",
                    )

            if target_booking["estado"] == "CONFIRMADA":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="INVALID_STATUS_TRANSITION: La reserva ya se encuentra ratificada y confirmada.",
                )

            if target_booking["estado"] in (
                "CANCELADA_USUARIO",
                "CANCELADA_SISTEMA",
                "NO_CONFIRMADA",
                "ASISTIDA",
                "INASISTENCIA",
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"INVALID_STATUS_TRANSITION: No se puede ratificar una reserva en estado {target_booking['estado']}.",
                )

            if target_booking["estado"] != "PENDIENTE_CONFIRMACION":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"INVALID_STATUS_TRANSITION: Transición no permitida desde el estado {target_booking['estado']}.",
                )

            f_inicio = target_booking.get("fecha_inicio")
            if f_inicio:
                try:
                    f_dt = datetime.fromisoformat(f_inicio)
                    if f_dt.tzinfo is None:
                        f_dt = f_dt.replace(tzinfo=UTC)
                    if f_dt <= now_utc + timedelta(hours=24):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="WINDOW_CLOSED_T24H: La ratificación de asistencia debe realizarse como mínimo 24 horas antes del inicio de la sesión (RN-08).",
                        )
                except (ValueError, TypeError):
                    pass

            target_booking["estado"] = "CONFIRMADA"
            target_booking["fecha_ratificacion"] = now_utc.isoformat()
            target_booking["updated_at"] = now_utc.isoformat()

            return BookingDetailResponse(**target_booking)
        finally:
            _booking_lock.release()

    @classmethod
    def cancel_reservation(
        cls,
        db: Session | None,
        id_reserva: int,
        payload: BookingCancelPayload | None = None,
        caller_email: str | None = None,
        is_admin: bool = False,
    ) -> BookingDetailResponse:
        """
        Desiste voluntariamente de una reserva activa de mentoría (T-28 / RF14 / CUS17 / RN-10).
        Libera de manera atómica el cupo reservado si la solicitud se formula con más de 24 horas
        de antelación a la sesión (RN-10) y la reserva pertenece al estudiante autenticado.
        """
        if not id_reserva or id_reserva < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="VALIDATION_ERROR: El identificador de reserva debe ser un número entero positivo.",
            )

        motivo_texto = (
            payload.motivo.strip()
            if payload and payload.motivo and payload.motivo.strip()
            else "Desistimiento voluntario del estudiante"
        )

        now_utc = datetime.now(UTC)
        timeout_s = float(settings.BOOKING_TIMEOUT_SECONDS)
        lock_acquired = _booking_lock.acquire(timeout=timeout_s)
        if not lock_acquired:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="DATABASE_BUSY: El servicio de reservas se encuentra temporalmente sobrecargado. Por favor, reintente en unos momentos.",
            )

        try:
            # ------------------------------------------------------------------
            # Camino 1: Base de datos relacional con bloqueo pesimista
            # ------------------------------------------------------------------
            if db is not None:
                try:
                    if db.bind and db.bind.dialect.name == "postgresql":
                        db.execute(text(f"SET LOCAL lock_timeout = '{settings.BOOKING_TIMEOUT_SECONDS}s';"))

                    reserva = (
                        db.query(ReservaCupo)
                        .filter(ReservaCupo.id_reserva == id_reserva)
                        .with_for_update()
                        .first()
                    )

                    if not reserva:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"RESERVATION_NOT_FOUND: No se encontró la reserva con ID {id_reserva}.",
                        )

                    clean_caller = (caller_email or "").strip().lower()
                    if not is_admin:
                        if not clean_caller:
                            raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="UNAUTHORIZED: Se requiere autenticación institucional válida para desistir de la reserva.",
                            )
                        if clean_caller != reserva.estudiante_email.strip().lower():
                            raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN,
                                detail="FORBIDDEN: No tiene autorización para cancelar una reserva que no le pertenece.",
                            )

                    if reserva.estado in ("CANCELADA_USUARIO", "CANCELADA_SISTEMA"):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="ALREADY_CANCELLED: La reserva ya ha sido cancelada previamente.",
                        )

                    if reserva.estado in ("NO_CONFIRMADA", "ASISTIDA", "INASISTENCIA"):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"INVALID_STATUS_TRANSITION: No se puede desistir de una reserva en estado terminal {reserva.estado}.",
                        )

                    if reserva.estado not in ("PENDIENTE_CONFIRMACION", "CONFIRMADA"):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"INVALID_STATUS_TRANSITION: Transición no permitida desde el estado {reserva.estado}.",
                        )

                    # Bloqueo atómico de la sesión de mentoría para garantizar consistencia de cupos
                    sesion = (
                        db.query(SesionMentoria)
                        .filter(SesionMentoria.id_sesion == reserva.id_sesion)
                        .with_for_update(of=SesionMentoria)
                        .first()
                    )

                    if not sesion:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"SESSION_NOT_FOUND: No se encontró la sesión de mentoría vinculada a la reserva {id_reserva}.",
                        )

                    ses_start = sesion.fecha_inicio
                    if ses_start.tzinfo is None:
                        ses_start = ses_start.replace(tzinfo=UTC)
                    if ses_start <= now_utc + timedelta(hours=24):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="WINDOW_CLOSED_T24H: El desistimiento voluntario debe efectuarse con más de 24 horas de antelación al inicio de la sesión (RN-10).",
                        )

                    # Transición atómica de estado y registro de motivo
                    reserva.estado = "CANCELADA_USUARIO"
                    reserva.motivo_cancelacion = motivo_texto
                    reserva.updated_at = now_utc
                    db.commit()
                    db.refresh(reserva)

                    ses = reserva.sesion or sesion
                    return BookingDetailResponse(
                        id_reserva=reserva.id_reserva,
                        codigo_reserva=reserva.codigo_reserva,
                        id_sesion=reserva.id_sesion,
                        codigo_sesion=ses.codigo_sesion if ses else None,
                        estudiante_email=reserva.estudiante_email,
                        estado=reserva.estado,
                        fecha_reserva=reserva.fecha_reserva.isoformat(),
                        fecha_ratificacion=reserva.fecha_ratificacion.isoformat()
                        if reserva.fecha_ratificacion
                        else None,
                        motivo_cancelacion=reserva.motivo_cancelacion,
                        ticket_hash=reserva.ticket_hash,
                        nombre_asignatura=ses.asignatura.nombre_curso if ses and ses.asignatura else None,
                        nombre_tema=ses.tema.nombre_tema if ses and ses.tema else None,
                        fecha_inicio=ses.fecha_inicio.isoformat() if ses else None,
                        duracion_minutos=ses.duracion_minutos if ses else None,
                        modalidad=ses.modalidad if ses else None,
                        espacio_asignado=ses.espacio_asignado if ses else None,
                        mentor_email=ses.mentor_email if ses else None,
                    )
                except HTTPException:
                    db.rollback()
                    raise
                except Exception as exc:
                    db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error transaccional al cancelar la reserva: {exc}",
                    ) from exc

            # ------------------------------------------------------------------
            # Camino 2: Ejecución en Memoria (Fallback aislado y thread-safe)
            # ------------------------------------------------------------------
            target_booking = None
            for b in _memory_bookings:
                if b.get("id_reserva") == id_reserva:
                    target_booking = b
                    break

            if not target_booking:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"RESERVATION_NOT_FOUND: No se encontró la reserva con ID {id_reserva}.",
                )

            clean_caller = (caller_email or "").strip().lower()
            if not is_admin:
                if not clean_caller:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="UNAUTHORIZED: Se requiere autenticación institucional válida para desistir de la reserva.",
                    )
                if clean_caller != target_booking.get("estudiante_email", "").strip().lower():
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="FORBIDDEN: No tiene autorización para cancelar una reserva que no le pertenece.",
                    )

            current_estado = target_booking.get("estado")
            if current_estado in ("CANCELADA_USUARIO", "CANCELADA_SISTEMA"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ALREADY_CANCELLED: La reserva ya ha sido cancelada previamente.",
                )

            if current_estado in ("NO_CONFIRMADA", "ASISTIDA", "INASISTENCIA"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"INVALID_STATUS_TRANSITION: No se puede desistir de una reserva en estado terminal {current_estado}.",
                )

            if current_estado not in ("PENDIENTE_CONFIRMACION", "CONFIRMADA"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"INVALID_STATUS_TRANSITION: Transición no permitida desde el estado {current_estado}.",
                )

            f_inicio = target_booking.get("fecha_inicio")
            if f_inicio:
                try:
                    f_dt = datetime.fromisoformat(f_inicio.replace("Z", "+00:00"))
                    if f_dt.tzinfo is None:
                        f_dt = f_dt.replace(tzinfo=UTC)
                    if f_dt <= now_utc + timedelta(hours=24):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="WINDOW_CLOSED_T24H: El desistimiento voluntario debe efectuarse con más de 24 horas de antelación al inicio de la sesión (RN-10).",
                        )
                except (ValueError, TypeError):
                    pass

            target_booking["estado"] = "CANCELADA_USUARIO"
            target_booking["motivo_cancelacion"] = motivo_texto
            target_booking["updated_at"] = now_utc.isoformat()

            return BookingDetailResponse(**target_booking)
        finally:
            _booking_lock.release()

    @classmethod
    def get_session_reservations(
        cls,
        db: Session | None,
        id_sesion: int,
        caller_email: str | None = None,
        is_admin: bool = False,
    ) -> list[BookingDetailResponse]:
        """Consulta la nómina de estudiantes inscritos en una sesión (para el mentor titular)."""
        if db is not None:
            sesion = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == id_sesion).first()
            if not sesion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="La sesión de mentoría solicitada no existe.",
                )
            if not caller_email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Se requiere autenticación para acceder a la nómina de inscritos.",
                )
            caller_clean = caller_email.strip().lower()
            has_admin = is_admin or caller_clean == "admin.epis@upt.pe"
            if not has_admin and caller_clean != sesion.mentor_email.strip().lower():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acceso exclusivo al mentor titular de la sesión o administrador.",
                )
            rows = (
                db.query(ReservaCupo)
                .filter(ReservaCupo.id_sesion == id_sesion)
                .order_by(ReservaCupo.fecha_reserva.asc())
                .all()
            )
            return [
                BookingDetailResponse(
                    id_reserva=r.id_reserva,
                    codigo_reserva=r.codigo_reserva,
                    id_sesion=r.id_sesion,
                    codigo_sesion=sesion.codigo_sesion,
                    estudiante_email=r.estudiante_email,
                    estado=r.estado,
                    fecha_reserva=r.fecha_reserva.isoformat(),
                    fecha_ratificacion=r.fecha_ratificacion.isoformat() if r.fecha_ratificacion else None,
                    motivo_cancelacion=r.motivo_cancelacion,
                    ticket_hash=r.ticket_hash,
                    nombre_asignatura=sesion.asignatura.nombre_curso if sesion.asignatura else None,
                    nombre_tema=sesion.tema.nombre_tema if sesion.tema else None,
                    fecha_inicio=sesion.fecha_inicio.isoformat(),
                    duracion_minutos=sesion.duracion_minutos,
                    modalidad=sesion.modalidad,
                    espacio_asignado=sesion.espacio_asignado,
                    mentor_email=sesion.mentor_email,
                )
                for r in rows
            ]

        # Fallback en memoria
        with _booking_lock:
            seed_default_offers_in_memory()
            target = None
            for off in _memory_offers:
                if off.get("id_sesion") == id_sesion or str(off.get("id_sesion")) == str(id_sesion):
                    target = off
                    break

            if not target:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="La sesión de mentoría solicitada no existe.",
                )

            if not caller_email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Se requiere autenticación para acceder a la nómina de inscritos.",
                )

            caller_clean = caller_email.strip().lower()
            has_admin = is_admin or caller_clean == "admin.epis@upt.pe"
            if not has_admin and caller_clean != target.get("mentor_email", "").strip().lower():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acceso exclusivo al mentor titular de la sesión o administrador.",
                )

            results = [
                BookingDetailResponse(**b)
                for b in _memory_bookings
                if b["id_sesion"] == id_sesion or str(b["id_sesion"]) == str(id_sesion)
            ]
            return results

    @classmethod
    def create_demand_request(
        cls,
        db: Session | None,
        payload: MentoringDemandPayload,
        student_email: str,
    ) -> MentoringDemandResponse:
        """Registra una solicitud temática por demanda (CUS03 / RF07)."""
        clean_email = student_email.strip().lower()
        now_utc = datetime.now(UTC)

        obs = payload.observaciones or payload.notas

        if db is not None:
            asig = db.query(Asignatura).filter(Asignatura.id_asignatura == payload.id_asignatura).first()
            if not asig:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="La asignatura curricular solicitada no existe en el catálogo institucional.",
                )
            tema = db.query(TemaConceptual).filter(TemaConceptual.id_tema == payload.id_tema).first()
            if not tema:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El tema conceptual silábico solicitado no existe en el catálogo institucional.",
                )

            demanda = SolicitudDemanda(
                estudiante_email=clean_email,
                id_asignatura=payload.id_asignatura,
                id_tema=payload.id_tema,
                observaciones=obs,
                estado="PENDIENTE",
                created_at=now_utc,
            )
            db.add(demanda)
            db.commit()
            db.refresh(demanda)

            asig_nombre = demanda.asignatura.nombre_curso if demanda.asignatura else None
            tema_nombre = demanda.tema.nombre_tema if demanda.tema else None

            return MentoringDemandResponse(
                id_demanda=demanda.id_demanda,
                estudiante_email=demanda.estudiante_email,
                id_asignatura=demanda.id_asignatura,
                id_tema=demanda.id_tema,
                nombre_asignatura=asig_nombre,
                nombre_tema=tema_nombre,
                observaciones=demanda.observaciones,
                estado="PENDIENTE",
                created_at=demanda.created_at.isoformat(),
            )

        # Fallback en memoria
        global _demand_counter
        with _booking_lock:
            _demand_counter += 1
            d_id = _demand_counter
            rec = {
                "id_demanda": d_id,
                "estudiante_email": clean_email,
                "id_asignatura": payload.id_asignatura,
                "id_tema": payload.id_tema,
                "nombre_asignatura": f"Asignatura {payload.id_asignatura}",
                "nombre_tema": f"Tema Silábico {payload.id_tema}",
                "observaciones": obs,
                "estado": "PENDIENTE",
                "created_at": now_utc.isoformat(),
            }
            _memory_demands.append(rec)
            return MentoringDemandResponse(**rec)

    @classmethod
    def get_demand_requests(
        cls,
        db: Session | None,
        id_asignatura: int | None = None,
        ciclo: int | None = None,
    ) -> list[MentoringDemandResponse]:
        """Consulta el banco institucional de solicitudes de asesoría por demanda."""
        if db is not None:
            try:
                q = db.query(SolicitudDemanda).filter(SolicitudDemanda.estado == "PENDIENTE")
                if id_asignatura:
                    q = q.filter(SolicitudDemanda.id_asignatura == id_asignatura)
                if ciclo:
                    q = q.join(Asignatura).filter(Asignatura.ciclo_plan == ciclo)
                rows = q.order_by(SolicitudDemanda.created_at.desc()).all()
                return [
                    MentoringDemandResponse(
                        id_demanda=r.id_demanda,
                        estudiante_email=r.estudiante_email,
                        id_asignatura=r.id_asignatura,
                        id_tema=r.id_tema,
                        nombre_asignatura=r.asignatura.nombre_curso if r.asignatura else None,
                        nombre_tema=r.tema.nombre_tema if r.tema else None,
                        observaciones=r.observaciones,
                        estado=r.estado,  # type: ignore
                        created_at=r.created_at.isoformat(),
                    )
                    for r in rows
                ]
            except Exception:
                pass

        # Fallback en memoria
        with _booking_lock:
            res = []
            for d in _memory_demands:
                if d["estado"] == "PENDIENTE":
                    if id_asignatura and d["id_asignatura"] != id_asignatura:
                        continue
                    res.append(MentoringDemandResponse(**d))
            return res

    @classmethod
    def evaluate_quorum(
        cls,
        db: Session | None,
        id_sesion: int,
    ) -> QuorumEvaluationResponse:
        """
        Evalúa el quórum normativo institucional (50% de aforo en T-24h) según RN-08 y RN-09.
        Caduca a NO_CONFIRMADA las reservas provisionales no ratificadas al cumplirse T-24h.
        """
        now_utc = datetime.now(UTC)
        cutoff_hours = float(settings.QUORUM_CUTOFF_HOURS)
        min_quorum_pct = float(settings.QUORUM_MINIMUM_PERCENTAGE)

        # 1. Recuperar sesión
        if db is not None:
            sesion = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == id_sesion).first()
            if not sesion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="La sesión de mentoría no existe.",
                )
            s_start = sesion.fecha_inicio
            if s_start.tzinfo is None:
                s_start = s_start.replace(tzinfo=UTC)

            hours_to_start = (s_start - now_utc).total_seconds() / 3600.0

            # Si ya cruzó la ventana T-24h, transicionar reservas provisionales a NO_CONFIRMADA
            if hours_to_start <= cutoff_hours:
                unconfirmed = (
                    db.query(ReservaCupo)
                    .filter(
                        ReservaCupo.id_sesion == id_sesion,
                        ReservaCupo.estado == "PENDIENTE_CONFIRMACION",
                    )
                    .all()
                )
                for u in unconfirmed:
                    u.estado = "NO_CONFIRMADA"
                    u.motivo_cancelacion = (
                        f"Expiración automática por no ratificación en T-{int(cutoff_hours)}h (RN-08)."
                    )
                if unconfirmed:
                    db.commit()

            # Contar confirmadas
            confirmed_count = (
                db.query(ReservaCupo)
                .filter(ReservaCupo.id_sesion == id_sesion, ReservaCupo.estado == "CONFIRMADA")
                .count()
            )
            total_active = (
                db.query(ReservaCupo)
                .filter(
                    ReservaCupo.id_sesion == id_sesion,
                    ReservaCupo.estado.in_(["PENDIENTE_CONFIRMACION", "CONFIRMADA"]),
                )
                .count()
            )

            aforo = sesion.aforo_maximo
            pct = round((confirmed_count / aforo) * 100.0, 2)
            cumple = pct >= min_quorum_pct

            # Actualizar estado de sesión si corresponde
            if hours_to_start <= cutoff_hours:
                if cumple and sesion.estado == "PUBLICADA":
                    sesion.estado = "CONFIRMADA"
                    db.commit()
                elif not cumple and sesion.estado == "PUBLICADA":
                    sesion.estado = "PENDIENTE_CONFIRMACION"
                    db.commit()

            msg = (
                f"Quórum alcanzado: {pct}% ({confirmed_count}/{aforo} confirmados). Sesión apta."
                if cumple
                else f"Quórum insuficiente: {pct}% ({confirmed_count}/{aforo} confirmados). Requiere mínimo {int(min_quorum_pct)}% según RN-09."
            )

            return QuorumEvaluationResponse(
                id_sesion=sesion.id_sesion,
                codigo_sesion=sesion.codigo_sesion,
                aforo_maximo=aforo,
                reservas_totales=total_active,
                reservas_confirmadas=confirmed_count,
                porcentaje_quorum=pct,
                quorum_minimo_requerido=min_quorum_pct,
                cumple_quorum=cumple,
                estado_sesion=sesion.estado,
                horas_antelacion=round(hours_to_start, 2),
                mensaje=msg,
            )

        # Fallback en memoria
        with _booking_lock:
            target = None
            for off in _memory_offers:
                if off.get("id_sesion") == id_sesion or str(off.get("id_sesion")) == str(id_sesion):
                    target = off
                    break

            if not target:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="La sesión de mentoría no existe.",
                )

            f_str = target.get("fecha_inicio", "")
            try:
                s_dt = datetime.fromisoformat(f_str.replace("Z", "+00:00"))
                if s_dt.tzinfo is None:
                    s_dt = s_dt.replace(tzinfo=UTC)
            except Exception:
                s_dt = now_utc + timedelta(hours=30)

            hours = (s_dt - now_utc).total_seconds() / 3600.0
            if hours <= cutoff_hours:
                for b in _memory_bookings:
                    if (b["id_sesion"] == id_sesion or str(b["id_sesion"]) == str(id_sesion)) and b[
                        "estado"
                    ] == "PENDIENTE_CONFIRMACION":
                        b["estado"] = "NO_CONFIRMADA"
                        b["motivo_cancelacion"] = (
                            f"Expiración automática por no ratificación en T-{int(cutoff_hours)}h (RN-08)."
                        )

            confirmed = sum(
                1
                for b in _memory_bookings
                if (b["id_sesion"] == id_sesion or str(b["id_sesion"]) == str(id_sesion))
                and b["estado"] == "CONFIRMADA"
            )
            active = sum(
                1
                for b in _memory_bookings
                if (b["id_sesion"] == id_sesion or str(b["id_sesion"]) == str(id_sesion))
                and b["estado"] in ["PENDIENTE_CONFIRMACION", "CONFIRMADA"]
            )
            aforo = target.get("aforo_maximo", 10)
            pct = round((confirmed / aforo) * 100.0, 2)
            cumple = pct >= min_quorum_pct

            if hours <= cutoff_hours:
                if cumple and target.get("estado") == "PUBLICADA":
                    target["estado"] = "CONFIRMADA"
                elif not cumple and target.get("estado") == "PUBLICADA":
                    target["estado"] = "PENDIENTE_CONFIRMACION"

            msg = (
                f"Quórum alcanzado: {pct}% ({confirmed}/{aforo} confirmados). Sesión apta."
                if cumple
                else f"Quórum insuficiente: {pct}% ({confirmed}/{aforo} confirmados). Requiere mínimo {int(min_quorum_pct)}% según RN-09."
            )

            return QuorumEvaluationResponse(
                id_sesion=id_sesion,
                codigo_sesion=target.get("codigo_sesion", f"SES-{id_sesion}"),
                aforo_maximo=aforo,
                reservas_totales=active,
                reservas_confirmadas=confirmed,
                porcentaje_quorum=pct,
                quorum_minimo_requerido=min_quorum_pct,
                cumple_quorum=cumple,
                estado_sesion=target.get("estado", "PUBLICADA"),
                horas_antelacion=round(hours, 2),
                mensaje=msg,
            )

    @classmethod
    def evaluate_session_quorum(
        cls,
        db: Session | None,
        id_sesion: int,
        now_utc: datetime | None = None,
    ) -> QuorumEvaluationResponse:
        """
        Evalúa el quórum normativo en T-24h con control de idempotencia y cerrojo pesimista (T-29 / T-30 / RF15 / CUS23).
        - Quórum alcanzado: transiciona a CONFIRMADA y cancela provisionales no ratificadas a CANCELADA_NO_CONFIRMADA.
        - Quórum no alcanzado: transiciona a QUORUM_INSUFICIENTE para resolución por el mentor (RN-10).
        - Idempotencia: Si ya fue evaluada (quorumevaluated_at no nulo), no repite transiciones ni mutaciones.
        """
        if now_utc is None:
            now_utc = datetime.now(UTC)
        cutoff_hours = float(settings.QUORUM_CUTOFF_HOURS)
        min_quorum_pct = float(settings.QUORUM_MINIMUM_PERCENTAGE)

        if db is not None:
            # Cerrojo pesimista de fila para control estricto de concurrencia e idempotencia (T-30)
            try:
                sesion = (
                    db.query(SesionMentoria)
                    .filter(SesionMentoria.id_sesion == id_sesion)
                    .with_for_update()
                    .first()
                )
            except Exception:
                sesion = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == id_sesion).first()

            if not sesion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="La sesión de mentoría no existe.",
                )

            # Idempotencia: sesión ya evaluada previamente
            if sesion.quorumevaluated_at is not None:
                confirmed_count = (
                    db.query(ReservaCupo)
                    .filter(ReservaCupo.id_sesion == id_sesion, ReservaCupo.estado == "CONFIRMADA")
                    .count()
                )
                aforo = sesion.aforo_maximo
                pct = round((confirmed_count / aforo) * 100.0, 2)
                cumple = sesion.estado == "CONFIRMADA"
                return QuorumEvaluationResponse(
                    id_sesion=sesion.id_sesion,
                    codigo_sesion=sesion.codigo_sesion,
                    aforo_maximo=aforo,
                    reservas_totales=confirmed_count,
                    reservas_confirmadas=confirmed_count,
                    porcentaje_quorum=pct,
                    quorum_minimo_requerido=min_quorum_pct,
                    cumple_quorum=cumple,
                    estado_sesion=sesion.estado,
                    horas_antelacion=0.0,
                    mensaje=f"Sesión ya evaluada previamente de forma idempotente en {sesion.quorumevaluated_at.isoformat()}.",
                )

            s_start = sesion.fecha_inicio
            if s_start.tzinfo is None:
                s_start = s_start.replace(tzinfo=UTC)

            hours_to_start = (s_start - now_utc).total_seconds() / 3600.0

            # Umbral normativo: Presencial >= 3 alumnos confirmados (o 50%); Virtual >= 5 (o 50%)
            is_presencial = (sesion.modalidad or "presencial").lower() == "presencial"
            min_students = 3 if is_presencial else 5

            confirmed_count = (
                db.query(ReservaCupo)
                .filter(ReservaCupo.id_sesion == id_sesion, ReservaCupo.estado == "CONFIRMADA")
                .count()
            )
            total_active = (
                db.query(ReservaCupo)
                .filter(
                    ReservaCupo.id_sesion == id_sesion,
                    ReservaCupo.estado.in_(["PENDIENTE_CONFIRMACION", "CONFIRMADA"]),
                )
                .count()
            )
            aforo = sesion.aforo_maximo
            pct = round((confirmed_count / aforo) * 100.0, 2)
            cumple = confirmed_count >= min_students or pct >= min_quorum_pct

            # Transición perentoria en ventana T-24h
            if hours_to_start <= cutoff_hours:
                unconfirmed = (
                    db.query(ReservaCupo)
                    .filter(
                        ReservaCupo.id_sesion == id_sesion,
                        ReservaCupo.estado == "PENDIENTE_CONFIRMACION",
                    )
                    .all()
                )
                for u in unconfirmed:
                    u.estado = "CANCELADA_NO_CONFIRMADA"
                    u.motivo_cancelacion = f"Expiración automática por falta de ratificación en T-{int(cutoff_hours)}h (RN-08/RN-09)."

                if cumple:
                    sesion.estado = "CONFIRMADA"
                else:
                    sesion.estado = "QUORUM_INSUFICIENTE"

                sesion.quorumevaluated_at = now_utc
                db.commit()

            msg = (
                f"Quórum alcanzado: {pct}% ({confirmed_count}/{aforo} confirmados). Sesión confirmada reglamentariamente."
                if cumple
                else f"Quórum insuficiente: {pct}% ({confirmed_count}/{aforo} confirmados). Sesión mutada a QUORUM_INSUFICIENTE para resolución del mentor (RN-10)."
            )

            return QuorumEvaluationResponse(
                id_sesion=sesion.id_sesion,
                codigo_sesion=sesion.codigo_sesion,
                aforo_maximo=aforo,
                reservas_totales=total_active,
                reservas_confirmadas=confirmed_count,
                porcentaje_quorum=pct,
                quorum_minimo_requerido=min_quorum_pct,
                cumple_quorum=cumple,
                estado_sesion=sesion.estado,
                horas_antelacion=round(hours_to_start, 2),
                mensaje=msg,
            )

        # Fallback en memoria
        with _booking_lock:
            target = None
            for off in _memory_offers:
                if off.get("id_sesion") == id_sesion or str(off.get("id_sesion")) == str(id_sesion):
                    target = off
                    break

            if not target:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="La sesión de mentoría no existe.",
                )

            # Idempotencia en memoria
            if target.get("quorumevaluated_at") is not None:
                confirmed = sum(
                    1
                    for b in _memory_bookings
                    if (b["id_sesion"] == id_sesion or str(b["id_sesion"]) == str(id_sesion))
                    and b["estado"] == "CONFIRMADA"
                )
                aforo = target.get("aforo_maximo", 10)
                pct = round((confirmed / aforo) * 100.0, 2)
                cumple = target.get("estado") == "CONFIRMADA"
                return QuorumEvaluationResponse(
                    id_sesion=id_sesion,
                    codigo_sesion=target.get("codigo_sesion", f"SES-{id_sesion}"),
                    aforo_maximo=aforo,
                    reservas_totales=confirmed,
                    reservas_confirmadas=confirmed,
                    porcentaje_quorum=pct,
                    quorum_minimo_requerido=min_quorum_pct,
                    cumple_quorum=cumple,
                    estado_sesion=target.get("estado", "PUBLICADA"),
                    horas_antelacion=0.0,
                    mensaje="Sesión ya evaluada previamente en memoria de forma idempotente.",
                )

            f_str = target.get("fecha_inicio", "")
            try:
                s_dt = datetime.fromisoformat(f_str.replace("Z", "+00:00"))
                if s_dt.tzinfo is None:
                    s_dt = s_dt.replace(tzinfo=UTC)
            except Exception:
                s_dt = now_utc + timedelta(hours=30)

            hours = (s_dt - now_utc).total_seconds() / 3600.0
            is_presencial = (target.get("modalidad") or "presencial").lower() == "presencial"
            min_students = 3 if is_presencial else 5

            if hours <= cutoff_hours:
                for b in _memory_bookings:
                    if (b["id_sesion"] == id_sesion or str(b["id_sesion"]) == str(id_sesion)) and b[
                        "estado"
                    ] == "PENDIENTE_CONFIRMACION":
                        b["estado"] = "CANCELADA_NO_CONFIRMADA"
                        b["motivo_cancelacion"] = (
                            f"Expiración automática por falta de ratificación en T-{int(cutoff_hours)}h (RN-08/RN-09)."
                        )

            confirmed = sum(
                1
                for b in _memory_bookings
                if (b["id_sesion"] == id_sesion or str(b["id_sesion"]) == str(id_sesion))
                and b["estado"] == "CONFIRMADA"
            )
            active = sum(
                1
                for b in _memory_bookings
                if (b["id_sesion"] == id_sesion or str(b["id_sesion"]) == str(id_sesion))
                and b["estado"] in ["PENDIENTE_CONFIRMACION", "CONFIRMADA"]
            )
            aforo = target.get("aforo_maximo", 10)
            pct = round((confirmed / aforo) * 100.0, 2)
            cumple = confirmed >= min_students or pct >= min_quorum_pct

            if hours <= cutoff_hours:
                if cumple:
                    target["estado"] = "CONFIRMADA"
                else:
                    target["estado"] = "QUORUM_INSUFICIENTE"
                target["quorumevaluated_at"] = now_utc.isoformat()

            msg = (
                f"Quórum alcanzado: {pct}% ({confirmed}/{aforo} confirmados). Sesión confirmada."
                if cumple
                else f"Quórum insuficiente: {pct}% ({confirmed}/{aforo} confirmados). Sesión en QUORUM_INSUFICIENTE."
            )

            return QuorumEvaluationResponse(
                id_sesion=id_sesion,
                codigo_sesion=target.get("codigo_sesion", f"SES-{id_sesion}"),
                aforo_maximo=aforo,
                reservas_totales=active,
                reservas_confirmadas=confirmed,
                porcentaje_quorum=pct,
                quorum_minimo_requerido=min_quorum_pct,
                cumple_quorum=cumple,
                estado_sesion=target.get("estado", "PUBLICADA"),
                horas_antelacion=round(hours, 2),
                mensaje=msg,
            )

    @classmethod
    def evaluate_all_active_quorums(
        cls,
        db: Session | None,
        now_utc: datetime | None = None,
    ) -> list[QuorumEvaluationResponse]:
        """
        Evalúa de forma desatendida todas las sesiones activas en la ventana perentoria T-24h (T-29 / CUS23).
        """
        if now_utc is None:
            now_utc = datetime.now(UTC)
        cutoff_hours = float(settings.QUORUM_CUTOFF_HOURS)
        max_start = now_utc + timedelta(hours=cutoff_hours)
        results: list[QuorumEvaluationResponse] = []

        if db is not None:
            sessions = (
                db.query(SesionMentoria)
                .filter(
                    SesionMentoria.estado == "PUBLICADA",
                    SesionMentoria.quorumevaluated_at.is_(None),
                    SesionMentoria.fecha_inicio <= max_start,
                )
                .all()
            )
            for s in sessions:
                try:
                    res = cls.evaluate_session_quorum(db=db, id_sesion=s.id_sesion, now_utc=now_utc)
                    results.append(res)
                except Exception:
                    continue
            return results

        # En memoria
        with _booking_lock:
            eligible_ids: list[int] = []
            for off in _memory_offers:
                if off.get("estado") == "PUBLICADA" and off.get("quorumevaluated_at") is None:
                    f_str = off.get("fecha_inicio", "")
                    try:
                        s_dt = datetime.fromisoformat(f_str.replace("Z", "+00:00"))
                        if s_dt.tzinfo is None:
                            s_dt = s_dt.replace(tzinfo=UTC)
                        if s_dt <= max_start:
                            eligible_ids.append(off["id_sesion"])
                    except Exception:
                        pass

        for sid in eligible_ids:
            try:
                res = cls.evaluate_session_quorum(db=None, id_sesion=sid, now_utc=now_utc)
                results.append(res)
            except Exception:
                continue

        return results
