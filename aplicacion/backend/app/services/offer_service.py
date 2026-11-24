from datetime import UTC, datetime, time, timedelta
from typing import Literal
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.booking import ReservaCupo, SolicitudDemanda
from app.models.offer import SesionMentoria
from app.models.profile import PerfilAcademico
from app.models.roles import Rol, UsuarioRol
from app.schemas.offer import (
    PublishOfferPayload,
    PublishOfferResponse,
    QuorumDecisionPayload,
    QuorumDecisionResponse,
)
from app.services.schedule_parser_service import ScheduleParserService
from app.services.virtual_room_service import VirtualRoomService

# Almacén en memoria de respaldo para ofertas
_memory_offers: list[dict] = []
_session_counter = 1001
_DEMAND_UNAVAILABLE = (
    "La solicitud ya no está pendiente o no corresponde a la asignatura y al tema seleccionados."
)


def get_offers_in_memory() -> list[dict]:
    """Helper para consultar ofertas en memoria."""
    return list(_memory_offers)


def clear_offers_in_memory() -> None:
    """Helper para limpiar almacén de ofertas en pruebas."""
    global _session_counter
    _memory_offers.clear()
    _session_counter = 1001


def seed_default_offers_in_memory() -> None:
    """Pobla ofertas semilla representativas de la EPIS-UPT para pruebas y recomendador."""
    if _memory_offers:
        return
    # Oferta 1: Cálculo I por Renzo (Ciclo VII) - Presencial
    now = datetime.now(UTC)

    f1 = (now + timedelta(days=3, hours=2)).replace(minute=0, second=0, microsecond=0)
    f2 = (now + timedelta(days=4, hours=4)).replace(minute=0, second=0, microsecond=0)
    f3 = (now + timedelta(days=5, hours=1)).replace(minute=0, second=0, microsecond=0)

    _memory_offers.extend(
        [
            {
                "id_sesion": 1,
                "codigo_sesion": "SES-1001",
                "mentor_email": "2022073504@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites y Continuidad",
                "fecha_inicio": f1.isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Laboratorio de Cómputo 101 - Pabellón G (EPIS)",
                "mentor_nombre": "Renzo Antonio Antayhua Mamani",
                "notas_adicionales": "Traer guía de ejercicios silábicos de límites.",
                "estado": "PUBLICADA",
                "created_at": now.isoformat(),
            },
            {
                "id_sesion": 2,
                "codigo_sesion": "SES-1002",
                "mentor_email": "2022073504@upt.pe",
                "id_asignatura": 3,
                "codigo_asignatura": "ALGO-202",
                "nombre_asignatura": "Algoritmos y Estructuras de Datos",
                "id_tema": 9,
                "nombre_tema": "Análisis Asintótico y Notación Big-O",
                "fecha_inicio": f2.isoformat(),
                "duracion_minutos": 90,
                "modalidad": "virtual",
                "aforo_maximo": 20,
                "espacio_asignado": "https://meet.google.com/upt-epis-algo202",
                "mentor_nombre": "Renzo Antonio Antayhua Mamani",
                "notas_adicionales": "Sesión práctica con profiling de algoritmos en C++.",
                "estado": "PUBLICADA",
                "created_at": now.isoformat(),
            },
            {
                "id_sesion": 3,
                "codigo_sesion": "SES-1003",
                "mentor_email": "mentor.avanzado@upt.pe",
                "id_asignatura": 5,
                "codigo_asignatura": "BDD-401",
                "nombre_asignatura": "Base de Datos",
                "id_tema": 18,
                "nombre_tema": "Modelado Conceptual Entidad-Relación",
                "fecha_inicio": f3.isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Aula Magna 104 - Pabellón Central (EPIS)",
                "mentor_nombre": "Carlos Alberto Mendoza Dávila",
                "notas_adicionales": "Casos prácticos de normalización y modelado entidad-relación.",
                "estado": "PUBLICADA",
                "created_at": now.isoformat(),
            },
            # Escenarios de Demostración Oficiales (DEMO-01 a DEMO-05)
            {
                "id_sesion": 101,
                "codigo_sesion": "SES-DEMO-PUB01",
                "mentor_email": "mentor.demo@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites Notables y Asíntotas",
                "fecha_inicio": (now + timedelta(days=3)).isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Aula 201 - Pabellón EPIS",
                "mentor_nombre": "Mentor Demostrativo Acreditado",
                "notas_adicionales": "Sesión modelo de demostración institucional de límites de Cálculo I.",
                "estado": "PUBLICADA",
                "created_at": now.isoformat(),
            },
            {
                "id_sesion": 102,
                "codigo_sesion": "SES-DEMO-Q01",
                "mentor_email": "mentor.demo@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites Notables y Asíntotas",
                "fecha_inicio": (now + timedelta(hours=10)).isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Lab 101 - EPIS",
                "mentor_nombre": "Mentor Demostrativo Acreditado",
                "notas_adicionales": "Sesión modelo en contingencia por quórum insuficiente a T-24h.",
                "estado": "QUORUM_INSUFICIENTE",
                "created_at": now.isoformat(),
            },
            {
                "id_sesion": 103,
                "codigo_sesion": "SES-DEMO-ASIS01",
                "mentor_email": "mentor.demo@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites Notables y Asíntotas",
                "fecha_inicio": (now - timedelta(minutes=15)).isoformat(),
                "duracion_minutos": 60,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Lab 102 - EPIS",
                "mentor_nombre": "Mentor Demostrativo Acreditado",
                "notas_adicionales": "Sesión modelo en curso lista para pase de lista con QR TOTP.",
                "estado": "CONFIRMADA",
                "created_at": now.isoformat(),
            },
            {
                "id_sesion": 104,
                "codigo_sesion": "SES-DEMO-BIT01",
                "mentor_email": "mentor.demo@upt.pe",
                "id_asignatura": 1,
                "codigo_asignatura": "CALC-101",
                "nombre_asignatura": "Cálculo I",
                "id_tema": 1,
                "nombre_tema": "Límites Notables y Asíntotas",
                "fecha_inicio": (now - timedelta(hours=3)).isoformat(),
                "duracion_minutos": 90,
                "modalidad": "presencial",
                "aforo_maximo": 10,
                "espacio_asignado": "Lab 103 - EPIS",
                "mentor_nombre": "Mentor Demostrativo Acreditado",
                "notas_adicionales": "Sesión modelo concluida (< 48h) lista para suscripción de bitácora pedagógica.",
                "estado": "CONCLUIDA",
                "created_at": now.isoformat(),
            },
        ]
    )


class OfferService:
    @staticmethod
    def calculate_advance_hours(start_datetime_str: str, reference_now: datetime | None = None) -> float:
        """
        Calcula las horas de antelación entre la fecha programada y la referencia actual (UTC).
        """
        ref = reference_now or datetime.now(UTC)
        try:
            # Reemplazar Z por +00:00 para parsing estándar ISO
            iso_str = start_datetime_str.replace("Z", "+00:00")
            dt = datetime.fromisoformat(iso_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=UTC)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de fecha_inicio inválido. Se espera ISO 8601 (ej. YYYY-MM-DDTHH:MM:SSZ).",
            ) from None

        diff = dt - ref
        return diff.total_seconds() / 3600.0

    @staticmethod
    def validate_mentor_eligibility(db: Session | None, email: str) -> None:
        """
        Verifica el cumplimiento de la regla de mérito institucional RN-03:
        Solo estudiantes con rol 'mentor' y ciclo >= VII son elegibles para publicar ofertas.
        """
        clean_email = email.strip().lower()

        # 1. Verificación en base de datos si la sesión está activa
        if db is not None:
            try:
                # Comprobar rol de mentor o admin en usuario_roles
                rol_mentor = (
                    db.query(UsuarioRol)
                    .join(Rol, UsuarioRol.id_rol == Rol.id_rol)
                    .filter(
                        UsuarioRol.email == clean_email,
                        UsuarioRol.activo.is_(True),
                        Rol.nombre_rol.in_(["mentor", "administrador"]),
                    )
                    .first()
                )
                perfil = db.query(PerfilAcademico).filter(PerfilAcademico.email == clean_email).first()
                if rol_mentor or (perfil and perfil.ciclo_actual >= 7):
                    return
                # Si el usuario existe en BD pero no cumple mérito ni rol, rechazamos
                if (
                    perfil is not None
                    or db.query(UsuarioRol).filter(UsuarioRol.email == clean_email).first() is not None
                ):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Infracción de RN-03: Solo los estudiantes habilitados con rol de mentor (ciclo >= VII) pueden publicar ofertas de mentoría.",
                    )
            except HTTPException:
                raise
            except Exception:
                pass  # Fallback a verificación en servicios

        # 2. Verificación mediante servicios de perfil y rol (memoria o catálogo institucional)
        from app.services.profile_service import ProfileService
        from app.services.role_service import RoleService

        roles = RoleService.get_user_roles(db=None, email=clean_email)
        if "mentor" in roles or "administrador" in roles:
            return

        prof = ProfileService.get_profile(db=None, email=clean_email)
        if prof and prof.ciclo_actual >= 7:
            return

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Infracción de RN-03: Solo los estudiantes habilitados con rol de mentor (ciclo >= VII) pueden publicar ofertas de mentoría.",
        )

    @classmethod
    def available_classrooms(
        cls,
        db: Session | None,
        start: datetime,
        duration: int,
        lock: bool = False,
        exclude_session: int | None = None,
    ) -> list[str]:
        start = (start if start.tzinfo else start.replace(tzinfo=UTC)).astimezone(UTC)
        end = start + timedelta(minutes=duration)
        lima = ZoneInfo("America/Lima")
        local_start, local_end = start.astimezone(lima), end.astimezone(lima)
        if local_start.date() != local_end.date():
            return []
        weekday = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo")[
            local_start.weekday()
        ]
        slots = ScheduleParserService.get_active_slots(dia=weekday, db=db, lock=lock)
        intervals = {}
        for slot in slots:
            try:
                begin, finish = time.fromisoformat(slot["hora_inicio"]), time.fromisoformat(slot["hora_fin"])
            except ValueError:
                continue
            intervals.setdefault(slot["aula"], []).append((begin, finish))

        rooms = set()
        for room, spans in intervals.items():
            covered = local_start.time()
            for begin, finish in sorted(spans):
                if begin <= covered < finish:
                    covered = finish
            if covered >= local_end.time():
                rooms.add(room)

        occupied_states = (
            "PUBLICADA",
            "PENDIENTE_CONFIRMACION",
            "QUORUM_INSUFICIENTE",
            "CONFIRMADA",
            "EN_CURSO",
        )
        if db is not None:
            # Sessions last at most 90 minutes. Touching endpoints do not overlap.
            query = db.query(
                SesionMentoria.espacio_asignado, SesionMentoria.fecha_inicio, SesionMentoria.duracion_minutos
            ).filter(
                SesionMentoria.modalidad == "presencial",
                SesionMentoria.estado.in_(occupied_states),
                SesionMentoria.fecha_inicio > start - timedelta(minutes=90),
                SesionMentoria.fecha_inicio < end,
            )
            if exclude_session is not None:
                query = query.filter(SesionMentoria.id_sesion != exclude_session)
            existing = query.all()
        else:
            existing = [
                (s["espacio_asignado"], datetime.fromisoformat(s["fecha_inicio"]), s["duracion_minutos"])
                for s in _memory_offers
                if s.get("modalidad") == "presencial"
                and s.get("estado") in occupied_states
                and s.get("id_sesion") != exclude_session
            ]
        busy = set()
        for room, when, length in existing:
            when = when if when.tzinfo else when.replace(tzinfo=UTC)
            if when < end and when + timedelta(minutes=length) > start:
                busy.add(room.strip().casefold())
        return sorted(room for room in rooms if room.casefold() not in busy)

    @classmethod
    def require_available_room(
        cls, db: Session | None, room: str, start: datetime, duration: int, exclude_session: int | None = None
    ) -> None:
        if room not in cls.available_classrooms(
            db, start, duration, lock=True, exclude_session=exclude_session
        ):
            raise HTTPException(
                409, "El aula no está disponible durante toda la sesión en el cronograma vigente."
            )

    @classmethod
    def publish_offer(
        cls,
        db: Session | None,
        payload: PublishOfferPayload,
        caller_email: str | None = None,
        is_admin: bool = False,
    ) -> PublishOfferResponse:
        """
        Publica una oferta de mentoría académica aplicando RN-03, RN-04 y RN-05.
        """
        global _session_counter
        # 1. Resolver y validar identidad
        effective_email = payload.mentor_email.strip().lower()
        if caller_email is not None and caller_email.strip().lower() != effective_email and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene autorización para publicar ofertas en nombre de otro usuario.",
            )

        # 2. Validar mérito académico RN-03
        cls.validate_mentor_eligibility(db, effective_email)

        # 3. Validar antelación obligatoria RN-04 (> 24 horas)
        advance_hours = cls.calculate_advance_hours(payload.fecha_inicio)
        if advance_hours < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha y hora de inicio de la mentoría no puede encontrarse en el pasado.",
            )
        if advance_hours <= 24.0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Infracción de RN-04: Toda mentoría debe publicarse con una antelación superior a 24 horas respecto al inicio de la sesión para garantizar la confirmación de quórum.",
            )

        # 4. Validar y forzar aforo reglamentario RN-05
        expected_capacity = 10 if payload.modalidad == "presencial" else 20
        if payload.aforo_maximo != expected_capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Infracción de RN-05: El aforo reglamentario para la modalidad {payload.modalidad} debe ser exactamente {expected_capacity} estudiantes.",
            )

        # 5. Persistencia en Base de Datos o Almacén en Memoria
        now = datetime.now(UTC)
        assigned_space = (payload.espacio_asignado or "Aula EPIS").strip()
        iso_str = payload.fecha_inicio.replace("Z", "+00:00")
        start_dt = datetime.fromisoformat(iso_str)
        if start_dt.tzinfo is None:
            start_dt = start_dt.replace(tzinfo=UTC)

        start_dt = start_dt.astimezone(UTC)
        if payload.modalidad == "presencial":
            cls.require_available_room(db, assigned_space, start_dt, payload.duracion_minutos)

        if db is not None:
            sesion_db = SesionMentoria(
                # The temporary value is never committed. The primary key supplies the public folio.
                codigo_sesion=uuid4().hex[:20],
                mentor_email=effective_email,
                id_asignatura=payload.id_asignatura,
                id_tema=payload.id_tema,
                fecha_inicio=start_dt,
                duracion_minutos=payload.duracion_minutos,
                modalidad=payload.modalidad,
                aforo_maximo=expected_capacity,
                espacio_asignado=assigned_space,
                notas_adicionales=payload.notas_adicionales,
                estado="PUBLICADA",
            )
            try:
                if payload.id_demanda is not None:
                    claimed = db.execute(
                        update(SolicitudDemanda)
                        .where(
                            SolicitudDemanda.id_demanda == payload.id_demanda,
                            SolicitudDemanda.id_asignatura == payload.id_asignatura,
                            SolicitudDemanda.id_tema == payload.id_tema,
                            SolicitudDemanda.estado == "PENDIENTE",
                        )
                        .values(estado="ATENDIDA")
                        .returning(SolicitudDemanda.id_demanda)
                    ).scalar_one_or_none()
                    if claimed is None:
                        raise HTTPException(409, _DEMAND_UNAVAILABLE)
                db.add(sesion_db)
                db.flush()
                id_oferta_str = str(sesion_db.id_sesion)
                code = f"SES-P{id_oferta_str}"
                sesion_db.codigo_sesion = code
                if payload.modalidad == "virtual":
                    assigned_space = VirtualRoomService.resolve_virtual_room(payload.espacio_asignado, code)
                    sesion_db.espacio_asignado = assigned_space
                db.commit()
            except HTTPException:
                db.rollback()
                raise
            except SQLAlchemyError as exc:
                db.rollback()
                raise HTTPException(503, "No se pudo guardar la oferta de mentoría.") from exc
        else:
            from app.services.booking_service import _booking_lock, _memory_demands

            with _booking_lock:
                demand = None
                if payload.id_demanda is not None:
                    demand = next(
                        (
                            d
                            for d in _memory_demands
                            if d["id_demanda"] == payload.id_demanda
                            and d["estado"] == "PENDIENTE"
                            and d["id_asignatura"] == payload.id_asignatura
                            and d["id_tema"] == payload.id_tema
                        ),
                        None,
                    )
                    if demand is None:
                        raise HTTPException(409, _DEMAND_UNAVAILABLE)
                code = id_oferta_str = f"SES-{_session_counter}"
                _session_counter += 1
                if payload.modalidad == "virtual":
                    assigned_space = VirtualRoomService.resolve_virtual_room(payload.espacio_asignado, code)
                offer_dict = {
                    "id_sesion": _session_counter - 1,
                    "codigo_sesion": code,
                    "mentor_email": effective_email,
                    "id_asignatura": payload.id_asignatura,
                    "codigo_asignatura": payload.codigo_asignatura,
                    "nombre_asignatura": payload.nombre_asignatura,
                    "id_tema": payload.id_tema,
                    "nombre_tema": payload.nombre_tema,
                    "fecha_inicio": payload.fecha_inicio,
                    "duracion_minutos": payload.duracion_minutos,
                    "modalidad": payload.modalidad,
                    "aforo_maximo": expected_capacity,
                    "espacio_asignado": assigned_space,
                    "mentor_nombre": payload.mentor_nombre,
                    "notas_adicionales": payload.notas_adicionales,
                    "estado": "PUBLICADA",
                    "created_at": now.isoformat(),
                }
                _memory_offers.append(offer_dict)
                if demand is not None:
                    demand["estado"] = "ATENDIDA"

        payload.espacio_asignado = assigned_space
        return PublishOfferResponse(
            id_oferta=id_oferta_str,
            codigo_sesion=code,
            estado="PUBLICADA",
            mensaje=f"¡Oferta de mentoría publicada con éxito en el catálogo EPIS! Código de sesión: {code}",
            fecha_publicacion=now.isoformat(),
            aforo=expected_capacity,
            espacio_asignado=assigned_space,
            modo="api",
            offer=payload,
        )

    @classmethod
    def get_offers(
        cls,
        db: Session | None,
        mentor_email: str | None = None,
        id_asignatura: int | None = None,
        modalidad: Literal["presencial", "virtual"] | None = None,
        estado: str | tuple[str, ...] | None = None,
    ) -> list[PublishOfferResponse]:
        """
        Consulta las ofertas de mentoría activas filtradas por mentor, asignatura, modalidad o estado.
        """
        seed_default_offers_in_memory()
        results: list[PublishOfferResponse] = []

        # 1. Consulta en BD si está disponible
        if db is not None:
            try:
                query = db.query(SesionMentoria)
                if mentor_email:
                    clean_m = mentor_email.strip().lower()
                    from app.core.identity import parse_student_email

                    parsed = parse_student_email(clean_m)
                    codigo = parsed.get("codigo_estudiante")
                    mentor_aliases = [clean_m]
                    if codigo == "2022073504" or clean_m in (
                        "ra2022073504@virtual.upt.pe",
                        "2022073504@upt.pe",
                        "mentor@upt.pe",
                    ):
                        mentor_aliases.extend(
                            ["ra2022073504@virtual.upt.pe", "2022073504@upt.pe", "mentor@upt.pe"]
                        )
                    elif codigo:
                        mentor_aliases.extend([f"{codigo}@upt.pe", f"{codigo}@virtual.upt.pe"])
                    query = query.filter(SesionMentoria.mentor_email.in_(list(set(mentor_aliases))))
                if id_asignatura:
                    query = query.filter(SesionMentoria.id_asignatura == id_asignatura)
                if modalidad:
                    query = query.filter(SesionMentoria.modalidad == modalidad)
                if estado:
                    query = query.filter(
                        SesionMentoria.estado.in_((estado,) if isinstance(estado, str) else estado)
                    )
                elif not mentor_email:
                    query = query.filter(SesionMentoria.estado == "PUBLICADA")

                rows = query.order_by(SesionMentoria.fecha_inicio.asc()).all()
                for s in rows:
                    # Obtener nombres de asignatura y tema
                    asig_nombre = s.asignatura.nombre_curso if s.asignatura else "Asignatura EPIS"
                    asig_codigo = s.asignatura.codigo_curso if s.asignatura else "CURSO"
                    tema_nombre = s.tema.nombre_tema if s.tema else "Tema silábico"

                    results.append(
                        PublishOfferResponse(
                            id_oferta=str(s.id_sesion),
                            codigo_sesion=s.codigo_sesion,
                            estado=s.estado,  # type: ignore
                            mensaje="Oferta recuperada desde la base de datos institucional.",
                            fecha_publicacion=s.created_at.isoformat(),
                            aforo=s.aforo_maximo,
                            espacio_asignado=s.espacio_asignado,
                            modo="api",
                            offer=PublishOfferPayload(
                                id_asignatura=s.id_asignatura,
                                codigo_asignatura=asig_codigo,
                                nombre_asignatura=asig_nombre,
                                id_tema=s.id_tema,
                                nombre_tema=tema_nombre,
                                fecha_inicio=s.fecha_inicio.isoformat(),
                                duracion_minutos=s.duracion_minutos,  # type: ignore
                                modalidad=s.modalidad,  # type: ignore
                                aforo_maximo=s.aforo_maximo,
                                espacio_asignado=s.espacio_asignado,
                                mentor_email=s.mentor_email,
                                notas_adicionales=s.notas_adicionales,
                            ),
                        )
                    )
                return results
            except SQLAlchemyError as exc:
                db.rollback()
                raise HTTPException(503, "No se pudieron consultar las ofertas.") from exc

        # 2. Consulta en almacén en memoria
        filtered = _memory_offers
        if mentor_email:
            clean = mentor_email.strip().lower()
            filtered = [o for o in filtered if o["mentor_email"].lower() == clean]
        if id_asignatura:
            filtered = [o for o in filtered if o["id_asignatura"] == id_asignatura]
        if modalidad:
            filtered = [o for o in filtered if o["modalidad"] == modalidad]
        if estado:
            states = (estado,) if isinstance(estado, str) else estado
            filtered = [o for o in filtered if o["estado"] in states]
        elif not mentor_email:
            filtered = [o for o in filtered if o["estado"] == "PUBLICADA"]

        for o in filtered:
            results.append(
                PublishOfferResponse(
                    id_oferta=str(o.get("id_sesion", o["codigo_sesion"])),
                    codigo_sesion=o["codigo_sesion"],
                    estado=o["estado"],
                    mensaje="Oferta recuperada desde el catálogo activo de mentorías.",
                    fecha_publicacion=o.get("created_at", datetime.now(UTC).isoformat()),
                    aforo=o["aforo_maximo"],
                    espacio_asignado=o["espacio_asignado"],
                    modo="api",
                    offer=PublishOfferPayload(
                        id_asignatura=o["id_asignatura"],
                        codigo_asignatura=o.get("codigo_asignatura", "CURSO"),
                        nombre_asignatura=o.get("nombre_asignatura", "Asignatura"),
                        id_tema=o["id_tema"],
                        nombre_tema=o.get("nombre_tema", "Tema"),
                        fecha_inicio=o["fecha_inicio"],
                        duracion_minutos=o["duracion_minutos"],
                        modalidad=o["modalidad"],
                        aforo_maximo=o["aforo_maximo"],
                        espacio_asignado=o["espacio_asignado"],
                        mentor_email=o["mentor_email"],
                        mentor_nombre=o.get("mentor_nombre"),
                        notas_adicionales=o.get("notas_adicionales"),
                    ),
                )
            )

        return results

    @classmethod
    def _require_open_contingency(cls, state: str, start: str, now: datetime) -> None:
        if state != "QUORUM_INSUFICIENTE" or cls.calculate_advance_hours(start, now) <= 0:
            raise HTTPException(
                status_code=400,
                detail=f"INVALID_SESSION_STATE: No hay contingencia abierta para la sesión ({state}).",
            )

    @classmethod
    def resolve_quorum_decision(
        cls,
        db: Session | None,
        id_sesion: int,
        payload: QuorumDecisionPayload,
        caller_email: str | None = None,
        is_admin: bool = False,
    ) -> QuorumDecisionResponse:
        """
        Gestiona la decisión resolutiva del mentor ante quórum insuficiente (T-33 / RF16 / CUS07 / RN-04 / RN-10).
        Opciones:
        - PROCEED: Confirma el dictado de la sesión con aforo reducido (estado -> CONFIRMADA).
        - RESCHEDULE: Reprograma fecha/hora con antelación > 24h (estado -> PUBLICADA).
        - CANCEL: Cancela definitivamente con justificativo obligatorio (estado -> CANCELADA_QUORUM) y libera reservas.
        """
        now_utc = datetime.now(UTC)

        # 1. Base de datos relacional
        if db is not None:
            sesion = db.query(SesionMentoria).filter(SesionMentoria.id_sesion == id_sesion).first()
            if not sesion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="NOT_FOUND: La sesión de mentoría especificada no existe.",
                )

            # Control de titularidad y autorización (RNF02)
            if not caller_email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Se requiere autenticación para resolver la contingencia de quórum.",
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
                        detail="FORBIDDEN: Solo el mentor titular o un administrador pueden resolver la contingencia de quórum.",
                    )

            cls._require_open_contingency(sesion.estado, sesion.fecha_inicio.isoformat(), now_utc)

            if payload.decision == "PROCEED":
                sesion.estado = "CONFIRMADA"
                db.commit()
                return QuorumDecisionResponse(
                    id_sesion=sesion.id_sesion,
                    codigo_sesion=sesion.codigo_sesion,
                    decision="PROCEED",
                    estado_nuevo="CONFIRMADA",
                    mensaje="El mentor ha resuelto dictar la mentoría con aforo reducido. Sesión confirmada exitosamente.",
                )

            elif payload.decision == "RESCHEDULE":
                if not payload.new_start_time:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="NEW_START_TIME_REQUIRED: Debe proporcionar la nueva fecha y hora para reprogramar la sesión.",
                    )
                try:
                    raw_dt = datetime.fromisoformat(payload.new_start_time.replace("Z", "+00:00"))
                    if raw_dt.tzinfo is None:
                        raw_dt = raw_dt.replace(tzinfo=UTC)
                except Exception:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="INVALID_DATETIME: Formato de nueva fecha y hora inválido (utilice ISO 8601).",
                    ) from None

                if (raw_dt - now_utc).total_seconds() / 3600.0 <= 24.0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="INSUFFICIENT_RESCHEDULE_ADVANCE: La nueva fecha de la sesión debe programarse con al menos 24 horas de antelación respecto al momento actual (RN-04).",
                    )

                if sesion.modalidad == "presencial":
                    cls.require_available_room(
                        db, sesion.espacio_asignado, raw_dt, sesion.duracion_minutos, id_sesion
                    )
                sesion.fecha_inicio = raw_dt.astimezone(UTC)
                sesion.estado = "PUBLICADA"
                sesion.quorumevaluated_at = None
                db.commit()

                return QuorumDecisionResponse(
                    id_sesion=sesion.id_sesion,
                    codigo_sesion=sesion.codigo_sesion,
                    decision="RESCHEDULE",
                    estado_nuevo="PUBLICADA",
                    mensaje=f"Sesión reprogramada exitosamente para {raw_dt.isoformat()}. Se ha restablecido en cartelera pública.",
                    nueva_fecha_inicio=raw_dt.isoformat(),
                )

            elif payload.decision == "CANCEL":
                if not payload.reason or not payload.reason.strip():
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="REASON_REQUIRED: Debe ingresar obligatoriamente un motivo justificado para proceder con la cancelación definitiva.",
                    )

                sesion.estado = "CANCELADA_QUORUM"
                # Cancelar reservas de estudiantes sin penalización
                bookings = (
                    db.query(ReservaCupo)
                    .filter(
                        ReservaCupo.id_sesion == id_sesion,
                        ReservaCupo.estado.in_(["PENDIENTE_CONFIRMACION", "CONFIRMADA"]),
                    )
                    .all()
                )
                for b in bookings:
                    b.estado = "CANCELADA_SISTEMA_QUORUM"
                    b.motivo_cancelacion = f"Cancelación por quórum insuficiente: {payload.reason.strip()}"

                db.commit()

                return QuorumDecisionResponse(
                    id_sesion=sesion.id_sesion,
                    codigo_sesion=sesion.codigo_sesion,
                    decision="CANCEL",
                    estado_nuevo="CANCELADA_QUORUM",
                    mensaje=f"Sesión cancelada definitivamente por el mentor. Motivo registrado: '{payload.reason.strip()}'.",
                )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="INVALID_DECISION: La decisión debe ser 'PROCEED', 'RESCHEDULE' o 'CANCEL'.",
            )

        # 2. Fallback en memoria
        target = None
        for off in _memory_offers:
            if off.get("id_sesion") == id_sesion or str(off.get("id_sesion")) == str(id_sesion):
                target = off
                break

        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="NOT_FOUND: La sesión de mentoría especificada no existe.",
            )

        if not caller_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Se requiere autenticación para resolver la contingencia de quórum.",
            )

        clean_caller = caller_email.strip().lower()
        clean_mentor = target["mentor_email"].strip().lower()
        if not is_admin and clean_caller != clean_mentor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="FORBIDDEN: Solo el mentor titular o un administrador pueden resolver la contingencia de quórum.",
            )

        cls._require_open_contingency(target["estado"], target["fecha_inicio"], now_utc)

        if payload.decision == "PROCEED":
            target["estado"] = "CONFIRMADA"
            return QuorumDecisionResponse(
                id_sesion=id_sesion,
                codigo_sesion=target.get("codigo_sesion", f"SES-{id_sesion}"),
                decision="PROCEED",
                estado_nuevo="CONFIRMADA",
                mensaje="El mentor ha resuelto dictar la mentoría con aforo reducido. Sesión confirmada exitosamente.",
            )

        elif payload.decision == "RESCHEDULE":
            if not payload.new_start_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="NEW_START_TIME_REQUIRED: Debe proporcionar la nueva fecha y hora para reprogramar la sesión.",
                )
            try:
                raw_dt = datetime.fromisoformat(payload.new_start_time.replace("Z", "+00:00"))
                if raw_dt.tzinfo is None:
                    raw_dt = raw_dt.replace(tzinfo=UTC)
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="INVALID_DATETIME: Formato de nueva fecha y hora inválido (utilice ISO 8601).",
                ) from None

            if (raw_dt - now_utc).total_seconds() / 3600.0 <= 24.0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="INSUFFICIENT_RESCHEDULE_ADVANCE: La nueva fecha de la sesión debe programarse con al menos 24 horas de antelación respecto al momento actual (RN-04).",
                )

            if target.get("modalidad") == "presencial":
                cls.require_available_room(
                    None, target["espacio_asignado"], raw_dt, target["duracion_minutos"], id_sesion
                )
            target["fecha_inicio"] = raw_dt.isoformat()
            target["estado"] = "PUBLICADA"
            target["quorumevaluated_at"] = None

            return QuorumDecisionResponse(
                id_sesion=id_sesion,
                codigo_sesion=target.get("codigo_sesion", f"SES-{id_sesion}"),
                decision="RESCHEDULE",
                estado_nuevo="PUBLICADA",
                mensaje=f"Sesión reprogramada exitosamente para {raw_dt.isoformat()}. Se ha restablecido en cartelera pública.",
                nueva_fecha_inicio=raw_dt.isoformat(),
            )

        elif payload.decision == "CANCEL":
            if not payload.reason or not payload.reason.strip():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="REASON_REQUIRED: Debe ingresar obligatoriamente un motivo justificado para proceder con la cancelación definitiva.",
                )

            target["estado"] = "CANCELADA_QUORUM"
            from app.services.booking_service import _booking_lock, _memory_bookings

            with _booking_lock:
                for b in _memory_bookings:
                    if (b["id_sesion"] == id_sesion or str(b["id_sesion"]) == str(id_sesion)) and b[
                        "estado"
                    ] in ["PENDIENTE_CONFIRMACION", "CONFIRMADA"]:
                        b["estado"] = "CANCELADA_SISTEMA_QUORUM"
                        b["motivo_cancelacion"] = (
                            f"Cancelación por quórum insuficiente: {payload.reason.strip()}"
                        )

            return QuorumDecisionResponse(
                id_sesion=id_sesion,
                codigo_sesion=target.get("codigo_sesion", f"SES-{id_sesion}"),
                decision="CANCEL",
                estado_nuevo="CANCELADA_QUORUM",
                mensaje=f"Sesión cancelada definitivamente por el mentor. Motivo registrado: '{payload.reason.strip()}'.",
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="INVALID_DECISION: La decisión debe ser 'PROCEED', 'RESCHEDULE' o 'CANCEL'.",
        )
