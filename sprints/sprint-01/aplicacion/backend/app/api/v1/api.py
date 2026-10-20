from fastapi import APIRouter

from app.api.v1.endpoints import auth, curriculum, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["Salud & Monitoreo"])
api_router.include_router(curriculum.router, prefix="/curriculum", tags=["Catálogo Curricular"])
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación & OTP"])
