from typing import Dict, Any
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/health", response_model=Dict[str, Any], summary="Verificación de estado del servicio backend")
async def check_health() -> Dict[str, Any]:
    """
    Comprobación de operatividad del backend FastAPI (Hito 1 - T-01).
    Devuelve HTTP 200 y status ok de manera autónoma, independiente de la base de datos.
    """
    return {
        "status": "ok",
        "service": "backend",
        "project": settings.PROJECT_NAME,
        "environment": settings.APP_ENV,
    }
