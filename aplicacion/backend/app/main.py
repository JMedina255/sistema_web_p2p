import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import close_engine, get_session_context
from app.services.booking_service import BookingService

logger = logging.getLogger("app.main")


async def _quorum_scheduler_loop():
    """
    Tarea en segundo plano para evaluación periódica y desatendida del quórum a T-24h (RN-08 / RN-09 / RN-10).
    Se ejecuta de forma autónoma cada SCHEDULER_INTERVAL_MINUTES.
    """
    logger.info(
        "Planificador desatendido de quórum iniciado (intervalo: %s min).",
        settings.SCHEDULER_INTERVAL_MINUTES,
    )
    interval_seconds = max(0.001, float(settings.SCHEDULER_INTERVAL_MINUTES) * 60)
    while True:
        try:
            await asyncio.sleep(interval_seconds)
            logger.info("Ejecutando evaluación automática periódica de quórum (T-24h)...")
            with get_session_context() as db:
                evaluated = BookingService.evaluate_quorum_for_all_active_sessions(db)
                if evaluated:
                    logger.info("Evaluación de quórum procesó %d sesiones activas.", len(evaluated))
        except asyncio.CancelledError:
            logger.info("Planificador desatendido de quórum cancelado limpiamente.")
            break
        except Exception as exc:
            logger.error("Error en ciclo del planificador de quórum: %s", exc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicio diferido (lazy): FastAPI arranca sin bloquearse si DATABASE_URL no está disponible
    scheduler_task = None
    if settings.ENABLE_BACKGROUND_SCHEDULER:
        scheduler_task = asyncio.create_task(_quorum_scheduler_loop())

    yield

    # Cancelación limpia de la tarea en segundo plano al apagar el servicio
    if scheduler_task is not None:
        scheduler_task.cancel()
        try:
            await scheduler_task
        except asyncio.CancelledError:
            pass

    # Cierre de recursos del pool de conexiones al apagar el servicio
    close_engine()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API REST del Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Configuración de CORS para permitir la comunicación con el frontend React
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Enrutador de API v1
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["General"])
async def root():
    return {
        "message": f"Bienvenido a la API REST de {settings.PROJECT_NAME}",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health",
        "environment": settings.APP_ENV,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
