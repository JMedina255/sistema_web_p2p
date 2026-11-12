from fastapi import APIRouter

from app.api.v1.endpoints import (
    attendance,
    auth,
    bitacora,
    bookings,
    consent,
    curriculum,
    health,
    offers,
    profiles,
    quorum,
    recommendations,
    roles,
    survey,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["Salud & Monitoreo"])
api_router.include_router(curriculum.router, prefix="/curriculum", tags=["Catálogo Curricular"])
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación & OTP"])
api_router.include_router(consent.router, prefix="/consent", tags=["Consentimiento Ley 29733"])
api_router.include_router(roles.router, prefix="/roles", tags=["Administración de Roles"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["Perfiles & Disponibilidad"])
api_router.include_router(offers.router, prefix="/offers", tags=["Ofertas de Mentoría"])
api_router.include_router(
    recommendations.router, prefix="/recommendations", tags=["Motor de Recomendación EdRecSys"]
)
api_router.include_router(bookings.router, prefix="/bookings", tags=["Reservas de Cupos"])
api_router.include_router(quorum.router, prefix="/quorum", tags=["Evaluación de Quórum"])
api_router.include_router(attendance.router, prefix="/sessions", tags=["Control de Asistencias & TOTP"])
api_router.include_router(bitacora.router, prefix="/sessions", tags=["Bitácoras Pedagógicas"])
api_router.include_router(bitacora.admin_router, prefix="/bitacoras", tags=["Auditoría de Bitácoras"])
api_router.include_router(survey.router, prefix="/sessions", tags=["Encuestas de Calidad"])
