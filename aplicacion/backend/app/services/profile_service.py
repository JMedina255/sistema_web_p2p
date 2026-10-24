from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.profile import DisponibilidadHoraria, PerfilAcademico
from app.schemas.profile import (
    AcademicProfileResponse,
    AcademicProfileUpdate,
    AvailabilitySlotSchema,
)

# Almacenes en memoria de respaldo para perfiles y horarios
_memory_profiles: dict[str, dict] = {}
_memory_availability: dict[str, list[dict]] = {}


def get_profile_in_memory(email: str) -> dict | None:
    """Helper para consultar el perfil en memoria por correo institucional."""
    clean_email = email.strip().lower()
    return _memory_profiles.get(clean_email)


def set_profile_in_memory(email: str, data: dict) -> None:
    """Helper para pruebas o inicialización en memoria."""
    clean_email = email.strip().lower()
    _memory_profiles[clean_email] = data


class ProfileService:
    @staticmethod
    def _default_profile(email: str) -> AcademicProfileResponse:
        clean_email = email.strip().lower()
        codigo = clean_email.split("@")[0] if "@" in clean_email else clean_email
        nombres = ""
        apellidos = ""
        ciclo = 3
        rol_pos = "mentoreado"

        if codigo == "2022074255":
            nombres = "Joan Cristian"
            apellidos = "Medina Quispe"
            ciclo = 6
        elif codigo == "2022073504":
            nombres = "Renzo Antonio"
            apellidos = "Antayhua Mamani"
            ciclo = 7
            rol_pos = "mentor"

        return AcademicProfileResponse(
            email=clean_email,
            codigo_estudiante=codigo,
            nombres=nombres,
            apellidos=apellidos,
            ciclo_actual=ciclo,
            rol_postulacion=rol_pos,
            materias_interes=[1, 3],
            temas_seleccionados=[1, 2],
            biografia="Estudiante de la EPIS-UPT buscando asesoría académica en materias filtro.",
            modalidad_preferida="presencial",
            updated_at=datetime.now(UTC).isoformat(),
        )

    @staticmethod
    def get_profile(db: Session | None, email: str) -> AcademicProfileResponse:
        clean_email = email.strip().lower()

        if db is not None:
            try:
                perfil = db.query(PerfilAcademico).filter(PerfilAcademico.email == clean_email).first()
                if perfil is not None:
                    return AcademicProfileResponse(
                        email=perfil.email,
                        codigo_estudiante=perfil.codigo_estudiante,
                        nombres=perfil.nombres,
                        apellidos=perfil.apellidos,
                        ciclo_actual=perfil.ciclo_actual,
                        rol_postulacion=perfil.rol_postulacion,
                        materias_interes=perfil.materias_interes or [],
                        temas_seleccionados=perfil.temas_seleccionados or [],
                        biografia=perfil.biografia,
                        modalidad_preferida=perfil.modalidad_preferida,
                        updated_at=perfil.updated_at.isoformat() if perfil.updated_at else None,
                    )
            except Exception:
                pass

        if clean_email in _memory_profiles:
            p = _memory_profiles[clean_email]
            return AcademicProfileResponse(
                email=clean_email,
                codigo_estudiante=p.get("codigo_estudiante"),
                nombres=p.get("nombres"),
                apellidos=p.get("apellidos"),
                ciclo_actual=p.get("ciclo_actual", 1),
                rol_postulacion=p.get("rol_postulacion", "mentoreado"),
                materias_interes=p.get("materias_interes", []),
                temas_seleccionados=p.get("temas_seleccionados", []),
                biografia=p.get("biografia"),
                modalidad_preferida=p.get("modalidad_preferida", "presencial"),
                updated_at=p.get("updated_at"),
            )

        # Retornar perfil inicial predeterminado
        return ProfileService._default_profile(clean_email)

    @staticmethod
    def update_profile(
        db: Session | None,
        email: str,
        payload: AcademicProfileUpdate,
    ) -> AcademicProfileResponse:
        clean_email = email.strip().lower()

        # Validación estricta de mérito institucional RN-03
        if payload.rol_postulacion == "mentor" and payload.ciclo_actual < 7:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "MERIT_RULE_VIOLATION",
                    "message": "Conforme a la regla institucional RN-03, la postulación al rol de Mentor está reservada para estudiantes de ciclos superiores (VII al X ciclo).",
                },
            )

        now_dt = datetime.now(UTC)
        iso_str = now_dt.isoformat()

        if db is not None:
            try:
                perfil = db.query(PerfilAcademico).filter(PerfilAcademico.email == clean_email).first()
                if not perfil:
                    perfil = PerfilAcademico(
                        email=clean_email,
                        codigo_estudiante=payload.codigo_estudiante or clean_email.split("@")[0],
                        nombres=payload.nombres,
                        apellidos=payload.apellidos,
                        ciclo_actual=payload.ciclo_actual,
                        rol_postulacion=payload.rol_postulacion,
                        materias_interes=payload.materias_interes,
                        temas_seleccionados=payload.temas_seleccionados,
                        biografia=payload.biografia,
                        modalidad_preferida=payload.modalidad_preferida,
                        updated_at=now_dt,
                    )
                    db.add(perfil)
                else:
                    if payload.codigo_estudiante:
                        perfil.codigo_estudiante = payload.codigo_estudiante
                    if payload.nombres is not None:
                        perfil.nombres = payload.nombres
                    if payload.apellidos is not None:
                        perfil.apellidos = payload.apellidos
                    perfil.ciclo_actual = payload.ciclo_actual
                    perfil.rol_postulacion = payload.rol_postulacion
                    perfil.materias_interes = payload.materias_interes
                    perfil.temas_seleccionados = payload.temas_seleccionados
                    perfil.biografia = payload.biografia
                    perfil.modalidad_preferida = payload.modalidad_preferida
                    perfil.updated_at = now_dt

                db.commit()
                db.refresh(perfil)
                return AcademicProfileResponse(
                    email=perfil.email,
                    codigo_estudiante=perfil.codigo_estudiante,
                    nombres=perfil.nombres,
                    apellidos=perfil.apellidos,
                    ciclo_actual=perfil.ciclo_actual,
                    rol_postulacion=perfil.rol_postulacion,
                    materias_interes=perfil.materias_interes or [],
                    temas_seleccionados=perfil.temas_seleccionados or [],
                    biografia=perfil.biografia,
                    modalidad_preferida=perfil.modalidad_preferida,
                    updated_at=perfil.updated_at.isoformat() if perfil.updated_at else iso_str,
                )
            except HTTPException:
                raise
            except Exception:
                db.rollback()

        # Fallback en memoria
        prof_data = {
            "email": clean_email,
            "codigo_estudiante": payload.codigo_estudiante or clean_email.split("@")[0],
            "nombres": payload.nombres,
            "apellidos": payload.apellidos,
            "ciclo_actual": payload.ciclo_actual,
            "rol_postulacion": payload.rol_postulacion,
            "materias_interes": payload.materias_interes,
            "temas_seleccionados": payload.temas_seleccionados,
            "biografia": payload.biografia,
            "modalidad_preferida": payload.modalidad_preferida,
            "updated_at": iso_str,
        }
        _memory_profiles[clean_email] = prof_data

        return AcademicProfileResponse(
            email=clean_email,
            codigo_estudiante=prof_data["codigo_estudiante"],
            nombres=prof_data["nombres"],
            apellidos=prof_data["apellidos"],
            ciclo_actual=prof_data["ciclo_actual"],
            rol_postulacion=prof_data["rol_postulacion"],
            materias_interes=prof_data["materias_interes"],
            temas_seleccionados=prof_data["temas_seleccionados"],
            biografia=prof_data["biografia"],
            modalidad_preferida=prof_data["modalidad_preferida"],
            updated_at=iso_str,
        )

    @staticmethod
    def get_availability(db: Session | None, email: str) -> list[AvailabilitySlotSchema]:
        clean_email = email.strip().lower()

        if db is not None:
            try:
                rows = (
                    db.query(DisponibilidadHoraria)
                    .filter(DisponibilidadHoraria.email == clean_email)
                    .order_by(DisponibilidadHoraria.dia_semana, DisponibilidadHoraria.hora_inicio)
                    .all()
                )
                if rows:
                    return [
                        AvailabilitySlotSchema(
                            dia_semana=r.dia_semana,
                            hora_inicio=r.hora_inicio,
                            hora_fin=r.hora_fin,
                        )
                        for r in rows
                    ]
            except Exception:
                pass

        if clean_email in _memory_availability:
            return [
                AvailabilitySlotSchema(
                    dia_semana=s["dia_semana"],
                    hora_inicio=s["hora_inicio"],
                    hora_fin=s["hora_fin"],
                )
                for s in _memory_availability[clean_email]
            ]

        # Slots predeterminados
        return [
            AvailabilitySlotSchema(dia_semana=1, hora_inicio="14:00", hora_fin="15:00"),
            AvailabilitySlotSchema(dia_semana=1, hora_inicio="15:00", hora_fin="16:00"),
            AvailabilitySlotSchema(dia_semana=3, hora_inicio="14:00", hora_fin="15:00"),
            AvailabilitySlotSchema(dia_semana=3, hora_inicio="15:00", hora_fin="16:00"),
        ]

    @staticmethod
    def update_availability(
        db: Session | None,
        email: str,
        slots: list[AvailabilitySlotSchema],
    ) -> dict:
        clean_email = email.strip().lower()

        if db is not None:
            try:
                # Reemplazo atómico: eliminar slots existentes e insertar nuevos
                db.query(DisponibilidadHoraria).filter(DisponibilidadHoraria.email == clean_email).delete()

                for s in slots:
                    slot_entity = DisponibilidadHoraria(
                        email=clean_email,
                        dia_semana=s.dia_semana,
                        hora_inicio=s.hora_inicio,
                        hora_fin=s.hora_fin,
                        created_at=datetime.now(UTC),
                    )
                    db.add(slot_entity)

                db.commit()
            except Exception:
                db.rollback()

        # En memoria
        _memory_availability[clean_email] = [s.model_dump() for s in slots]

        return {
            "success": True,
            "totalSlots": len(slots),
            "message": f"Disponibilidad horaria guardada ({len(slots)} horas semanales registradas).",
            "slots": slots,
        }
