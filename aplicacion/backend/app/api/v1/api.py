from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    consent,
    curriculum,
    health,
    offers,
    profiles,
    recommendations,
    roles,
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
