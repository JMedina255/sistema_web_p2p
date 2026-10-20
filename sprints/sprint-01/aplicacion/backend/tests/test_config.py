from app.core.config import Settings


def test_cors_origins_parsing_from_json_string():
    """Valida el parsing de BACKEND_CORS_ORIGINS desde una cadena JSON."""
    s = Settings(
        BACKEND_CORS_ORIGINS='["http://example.com", "http://upt.pe"]',
        _env_file=None,
    )
    assert s.BACKEND_CORS_ORIGINS == ["http://example.com", "http://upt.pe"]


def test_cors_origins_parsing_from_comma_string():
    """Valida el parsing de BACKEND_CORS_ORIGINS desde valores separados por coma."""
    s = Settings(
        BACKEND_CORS_ORIGINS="http://localhost:3000, http://localhost:5173",
        _env_file=None,
    )
    assert s.BACKEND_CORS_ORIGINS == ["http://localhost:3000", "http://localhost:5173"]


def test_cors_origins_parsing_from_invalid_json():
    """Valida que un JSON inválido recurre al parseo por coma."""
    s = Settings(
        BACKEND_CORS_ORIGINS='["http://broken.com',
        _env_file=None,
    )
    assert s.BACKEND_CORS_ORIGINS == ['["http://broken.com']


def test_cors_origins_parsing_from_list():
    """Valida que una lista directa es preservada."""
    origins = ["http://localhost:8000"]
    s = Settings(BACKEND_CORS_ORIGINS=origins, _env_file=None)
    assert s.BACKEND_CORS_ORIGINS == origins


def test_sync_database_url_dialects():
    """Valida que sync_database_url adapta los dialectos a psycopg 3."""
    # 1. postgres:// -> postgresql+psycopg://
    s1 = Settings(DATABASE_URL="postgres://user:pass@host:5432/db", _env_file=None)
    assert s1.sync_database_url == "postgresql+psycopg://user:pass@host:5432/db"

    # 2. postgresql:// -> postgresql+psycopg://
    s2 = Settings(DATABASE_URL="postgresql://user:pass@host:5432/db", _env_file=None)
    assert s2.sync_database_url == "postgresql+psycopg://user:pass@host:5432/db"

    # 3. postgresql+psycopg:// ya formateado
    s3 = Settings(DATABASE_URL="postgresql+psycopg://user:pass@host:5432/db", _env_file=None)
    assert s3.sync_database_url == "postgresql+psycopg://user:pass@host:5432/db"

    # 4. None -> None
    s4 = Settings(DATABASE_URL=None, _env_file=None)
    assert s4.sync_database_url is None


def test_database_url_repr_masking():
    """Valida que repr=False previene la exposición de contraseñas en logs/prints."""
    secret_pass = "super_classified_pass_123"
    s = Settings(DATABASE_URL=f"postgresql://user:{secret_pass}@host/db", _env_file=None)
    repr_str = repr(s)
    assert secret_pass not in repr_str
