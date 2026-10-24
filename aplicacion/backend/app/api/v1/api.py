from fastapi import APIRouter

from app.api.v1.endpoints import auth, consent, curriculum, health, profiles, roles

api_router = APIRouter()
api_router.include_router(health.router, tags=["Salud & Monitoreo"])
api_router.include_router(curriculum.router, prefix="/curriculum", tags=["Catálogo Curricular"])
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación & OTP"])
api_router.include_router(consent.router, prefix="/consent", tags=["Consentimiento Ley 29733"])
api_router.include_router(roles.router, prefix="/roles", tags=["Administración de Roles"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["Perfiles & Disponibilidad"])
