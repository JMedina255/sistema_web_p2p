from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.db.session import test_db_connection

router = APIRouter()


@router.get("/health", response_model=Dict[str, Any], summary="Verificación básica de operatividad del backend")
async def check_health() -> Dict[str, Any]:
    """
    Comprobación de operatividad del backend FastAPI.
    Independiente de la base de datos; devuelve HTTP 200 siempre que el proceso esté activo.
    """
    return {
        "status": "ok",
        "service": "backend",
        "project": settings.PROJECT_NAME,
        "environment": settings.APP_ENV,
    }


@router.get("/health/db", summary="Verificación de conectividad a PostgreSQL / Supabase (Solo en desarrollo)")
async def check_db_health():
    """
    Comprobación técnica de conexión a la base de datos PostgreSQL (Supabase) mediante SELECT 1.
    Disponible únicamente en entorno de desarrollo ('development').
    Devuelve HTTP 200 si la conexión es exitosa, o HTTP 503 con detalle sanitizado si falla o no está configurada.
    """
    if settings.APP_ENV != "development":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint de diagnóstico de base de datos no disponible fuera del entorno de desarrollo.",
        )

    is_ok, detail, latency_ms = test_db_connection()

    if is_ok:
        return {
            "status": "ok",
            "database": "connected",
            "detail": detail,
            "latency_ms": latency_ms,
            "environment": settings.APP_ENV,
        }
    else:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "database": "unavailable",
                "detail": detail,
                "latency_ms": latency_ms,
                "environment": settings.APP_ENV,
            },
        )
