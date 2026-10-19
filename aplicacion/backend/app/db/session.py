import time

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

Base = declarative_base()

_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None


def get_engine() -> Engine | None:
    """
    Creación diferida (lazy) del motor SQLAlchemy para PostgreSQL.
    Solo inicializa el engine cuando settings.sync_database_url está configurada.
    """
    global _engine, _SessionLocal
    db_url = settings.sync_database_url
    if not db_url:
        return None

    if _engine is None:
        _engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args={
                "connect_timeout": settings.DB_CONNECT_TIMEOUT,
            },
        )
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    return _engine


def get_session():
    """
    Generador de sesiones de base de datos con cierre garantizado de recursos.
    """
    engine = get_engine()
    if engine is None or _SessionLocal is None:
        raise RuntimeError("No se ha configurado la variable DATABASE_URL en el entorno.")
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_optional_session():
    """
    Generador de sesión opcional que retorna None si la base de datos no está configurada.
    """
    try:
        engine = get_engine()
        if engine is not None and _SessionLocal is not None:
            db = _SessionLocal()
            try:
                yield db
            finally:
                db.close()
            return
    except Exception:
        pass
    yield None


def close_engine():
    """
    Libera los recursos del pool de conexiones al apagar el servicio.
    """
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
        _engine = None
        _SessionLocal = None


def sanitize_db_error(error: Exception) -> str:
    """
    Sanitiza los mensajes de error para prevenir la fuga de credenciales,
    contraseñas, tokens o parámetros de conexión hacia los clientes o logs públicos.
    """
    err_str = str(error).lower()
    if "password authentication failed" in err_str:
        return "Error de autenticación con las credenciales de PostgreSQL."
    elif "timeout" in err_str or "timed out" in err_str:
        return "Tiempo de espera agotado al intentar conectar con el servidor de PostgreSQL (timeout)."
    elif "could not translate host name" in err_str or "nodename nor servname provided" in err_str:
        return "No fue posible resolver el nombre de host del servidor de base de datos."
    elif "connection refused" in err_str:
        return "Conexión rechazada por el servidor de base de datos."
    elif "ssl" in err_str and "failed" in err_str:
        return "Fallo en la negociación SSL con el servidor de base de datos."
    return "Error al establecer comunicación con el servidor de base de datos."


def test_db_connection() -> tuple[bool, str | None, float | None]:
    """
    Ejecuta una comprobación técnica SELECT 1 contra el motor PostgreSQL.
    Retorna (is_ok, detail_or_error, latency_ms).
    """
    if not settings.sync_database_url:
        return False, "DATABASE_URL no configurada en el entorno", None

    start_time = time.perf_counter()
    try:
        engine = get_engine()
        if engine is None:
            return False, "No fue posible inicializar el motor de base de datos", None

        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            if result == 1:
                return True, "Conexión a PostgreSQL (Supabase) verificada con éxito", latency_ms
            return False, "La consulta de prueba SELECT 1 no retornó el valor esperado", latency_ms
    except Exception as e:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        sanitized = sanitize_db_error(e)
        return False, sanitized, latency_ms
