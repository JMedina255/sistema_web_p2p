"""
Módulo de Blindaje y Hardening para Conexiones y Esquemas PostgreSQL (QA-P2P-04)
Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)

Proporciona mecanismos de protección activa contra ejecución en entornos no autorizados
o alteración de esquemas de producción:
1. Validación estricta de entorno (prohíbe 'production', exige marcadores de prueba).
2. Generación de nombres únicos y efímeros de esquemas por ejecución (UUID / timestamp).
3. Registro y control de propiedad de esquemas creados en tiempo de ejecución.
4. Construcción segura de URLs de conexión con 'options=-c search_path=...' mediante urllib.parse.
5. Verificación activa de search_path y current_schema() en cada conexión.
6. Eliminación segura y restringida (prohíbe 'DROP SCHEMA' sobre 'public', esquemas del sistema
   o esquemas que no hayan sido creados explícitamente en la sesión actual).
"""

import os
import re
import urllib.parse
import uuid

from sqlalchemy import Engine, text

# Registro en memoria de esquemas creados exclusivamente durante esta ejecución
_CREATED_SCHEMAS_IN_THIS_RUN: set[str] = set()

# Esquemas del sistema y de producción estrictamente prohibidos
FORBIDDEN_PROTECTED_SCHEMAS = {
    "public",
    "information_schema",
    "pg_catalog",
    "pg_toast",
    "auth",
    "storage",
    "graphql",
    "vault",
    "realtime",
    "extensions",
    "supabase_functions",
    "supabase_migrations",
}

# Patrón obligatorio para esquemas de prueba permitidos
TEST_SCHEMA_PATTERN = re.compile(r"^test_(qa_p2p_\d{2}|sandbox)_[a-z0-9_]+$")


class DatabaseSecurityError(RuntimeError):
    """Excepción de seguridad ante intentos de operar en entornos o esquemas protegidos."""


def validate_test_environment(settings_env: str = "") -> None:
    """
    Verifica que el entorno no sea de producción y que existan marcadores
    explícitos de autorización para ejecución de pruebas.
    """
    app_env = os.environ.get("APP_ENV", "").lower()
    env_name = (settings_env or os.environ.get("ENVIRONMENT", "")).lower()

    if app_env == "production" or env_name == "production":
        raise DatabaseSecurityError(
            "¡BLOQUEO DE SEGURIDAD! Intento de ejecución de pruebas con configuración de producción "
            f"(APP_ENV='{app_env}', ENVIRONMENT='{env_name}'). Abortando inmediatamente."
        )

    # Marcadores de autorización requeridos
    allow_flag = os.environ.get("ALLOW_TEST_SCHEMA_CREATION", "").lower()
    is_authorized = (
        allow_flag in ("true", "1", "yes")
        or app_env in ("test", "testing", "development")
        or env_name in ("test", "testing", "development", "local")
    )

    if not is_authorized:
        raise DatabaseSecurityError(
            "¡ACCESO DENEGADO! No se detectó autorización explícita para crear esquemas de prueba. "
            "Configure ALLOW_TEST_SCHEMA_CREATION=true o APP_ENV=test."
        )


def generate_unique_test_schema(prefix: str = "test_qa_p2p_04") -> str:
    """
    Genera un nombre de esquema único y efímero para la ejecución actual.
    Ejemplo: test_qa_p2p_04_e2e_a1b2c3d4
    """
    token = uuid.uuid4().hex[:8]
    schema_name = f"{prefix}_{token}"
    if not TEST_SCHEMA_PATTERN.match(schema_name):
        raise ValueError(f"El nombre de esquema generado '{schema_name}' no cumple con el patrón permitido.")
    return schema_name


def build_isolated_db_url(base_url: str, schema_name: str) -> str:
    """
    Construye de forma segura la URL de conexión a PostgreSQL agregando
    el parámetro 'options=-c search_path={schema_name}', preservando
    parámetros existentes (como sslmode=require) sin concatenaciones
    inseguras de cadenas.
    """
    if not schema_name or schema_name in FORBIDDEN_PROTECTED_SCHEMAS:
        raise DatabaseSecurityError(f"No se permite construir URL hacia el esquema '{schema_name}'.")

    parsed = urllib.parse.urlsplit(base_url)
    query_params = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))

    schema_option = f"-c search_path={schema_name}"
    existing_options = query_params.get("options", "")
    if existing_options:
        query_params["options"] = f"{existing_options} {schema_option}".strip()
    else:
        query_params["options"] = schema_option

    def _quote_with_equals(s, safe="/", encoding=None, errors=None):
        return urllib.parse.quote(s, safe=safe + "=", encoding=encoding, errors=errors)

    new_query = urllib.parse.urlencode(
        query_params,
        quote_via=_quote_with_equals,
    )

    return urllib.parse.urlunsplit((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        new_query,
        parsed.fragment,
    ))


def verify_connection_search_path(conn, expected_schema: str) -> None:
    """
    Verifica que la conexión activa esté efectivamente aislada en expected_schema
    y que current_schema() no apunte bajo ninguna circunstancia a 'public'.
    """
    curr = conn.execute(text("SELECT current_schema();")).scalar()
    search_path = conn.execute(text("SHOW search_path;")).scalar()

    if curr == "public":
        raise DatabaseSecurityError(
            f"¡VIOLACIÓN DE AISLAMIENTO! current_schema() es 'public'. "
            f"La conexión no está aislada en '{expected_schema}'."
        )

    if curr != expected_schema and expected_schema not in str(search_path):
        # Puede ser None si el esquema aún no fue creado físicamente, pero search_path debe contenerlo
        raise DatabaseSecurityError(
            f"¡VIOLACIÓN DE SEARCH_PATH! search_path='{search_path}' no contiene '{expected_schema}'."
        )


def create_isolated_schema(engine: Engine, schema_name: str) -> str:
    """
    Crea un nuevo esquema temporal vacío en la base de datos y lo registra
    en la lista de esquemas administrados por esta ejecución.
    """
    if schema_name in FORBIDDEN_PROTECTED_SCHEMAS:
        raise DatabaseSecurityError(f"Prohibida la creación del esquema protegido '{schema_name}'.")

    if not TEST_SCHEMA_PATTERN.match(schema_name):
        raise DatabaseSecurityError(f"El esquema '{schema_name}' no cumple el patrón de pruebas permitido.")

    with engine.connect() as conn:
        conn.execute(text(f'CREATE SCHEMA "{schema_name}";'))
        conn.commit()

    _CREATED_SCHEMAS_IN_THIS_RUN.add(schema_name)
    print(f"[SECURITY GUARD] Esquema sandbox único '{schema_name}' creado y registrado con éxito.")
    return schema_name


def safe_teardown_schema(engine: Engine, schema_name: str) -> None:
    """
    Elimina exclusivamente un esquema que haya sido creado por esta ejecución.
    Rechaza eliminar esquemas protegidos, no registrados o preexistentes.
    """
    if schema_name in FORBIDDEN_PROTECTED_SCHEMAS:
        raise DatabaseSecurityError(f"¡INTENTO DE ELIMINACIÓN DE ESQUEMA PROTEGIDO '{schema_name}' RECHAZADO!")

    if schema_name not in _CREATED_SCHEMAS_IN_THIS_RUN:
        raise DatabaseSecurityError(
            f"¡INTENTO DE DROP RECHAZADO! El esquema '{schema_name}' no fue creado por esta ejecución. "
            "Se previene la eliminación accidental de datos preexistentes."
        )

    try:
        engine.dispose()
    except Exception:
        pass

    with engine.connect() as conn:
        conn.execute(text(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE;'))
        conn.commit()

    _CREATED_SCHEMAS_IN_THIS_RUN.discard(schema_name)
    print(f"[SECURITY GUARD] Esquema sandbox verificado '{schema_name}' eliminado limpiamente.")
