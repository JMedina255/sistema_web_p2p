from app.services.attendance_service import AttendanceService
from app.services.auth_service import AuthService
from app.services.bitacora_service import BitacoraService
from app.services.booking_service import BookingService
from app.services.catalog_support_service import (
    ExcepcionAulaNoDisponible,
    ServicioAprovisionamientoDiscord,
    ServicioAprovisionamientoMeet,
    ServicioAuditoria,
    ServicioInsignia,
    ServicioNotificacion,
    ServicioRecordatorio,
    ServicioReputacion,
    ServicioReservaAula,
    ServicioResolucionReclamo,
    ServicioSolicitudDemanda,
    TareaProgramadaQuorum,
)
from app.services.certificate_service import CertificateService
from app.services.consent_service import ConsentService
from app.services.curriculum_service import CurriculumService
from app.services.email_service import EmailService
from app.services.offer_service import OfferService
from app.services.profile_service import ProfileService
from app.services.recommendation_service import RecommendationService
from app.services.resource_service import ResourceService, ServicioRecursosAcademicos
from app.services.role_service import RoleService
from app.services.schedule_parser_service import ScheduleParserService, ServicioAnalizadorHorarios
from app.services.simulation_service import SimulationService
from app.services.storage_service import StorageService
from app.services.survey_service import SurveyService
from app.services.virtual_room_service import VirtualRoomService

__all__ = [
    "CurriculumService",
    "AuthService",
    "EmailService",
    "ConsentService",
    "RoleService",
    "ProfileService",
    "OfferService",
    "VirtualRoomService",
    "RecommendationService",
    "SimulationService",
    "BookingService",
    "AttendanceService",
    "BitacoraService",
    "CertificateService",
    "StorageService",
    "SurveyService",
    "ScheduleParserService",
    "ServicioAnalizadorHorarios",
    "ResourceService",
    "ServicioRecursosAcademicos",
    "ServicioSolicitudDemanda",
    "ServicioNotificacion",
    "ServicioReputacion",
    "ServicioInsignia",
    "ServicioAuditoria",
    "ServicioResolucionReclamo",
    "TareaProgramadaQuorum",
    "ServicioRecordatorio",
    "ExcepcionAulaNoDisponible",
    "ServicioReservaAula",
    "ServicioAprovisionamientoMeet",
    "ServicioAprovisionamientoDiscord",
]
