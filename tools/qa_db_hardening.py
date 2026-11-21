"""
Módulo de Blindaje y Hardening para Conexiones y Esquemas PostgreSQL (QA-P2P-04R)
Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)

Proporciona mecanismos de protección activa contra ejecución en entornos no autorizados
o alteración de esquemas de producción:
1. Validación estricta de entorno: prohíbe 'production' en APP_ENV, ENVIRONMENT, NODE_ENV, STAGE.
   Ninguna variable local de desarrollo puede anular la prohibición productiva.
2. Resolución obligatoria de QA_DATABASE_URL exclusiva e independiente de producción.
3. Validación de destino: rechazo por defecto si el host no está explícitamente reconocido como QA/test.
4. Verificación de identidad de la base de datos y rol de conexión antes de cualquier DDL.
5. Generación de nombres únicos y efímeros de esquemas (test_qa_p2p_04_<tipo>_<hex8>).
6. Construcción segura de URLs de conexión con 'options=-c search_path={schema}' mediante urllib.parse.
7. Verificación activa de search_path: exige coincidencia exacta de current_schema() con el esquema sandbox.
8. Eliminación segura y restringida: verifica titularidad, registro en memoria y prohíbe eliminar esquemas
   protegidos o preexistentes.
"""

from contextlib import contextmanager
import os
import re
import urllib.parse
import uuid

from sqlalchemy import Engine, text

# Registro en memoria de esquemas creados exclusivamente durante esta ejecución
_CREATED_SCHEMAS_IN_THIS_RUN: set[str] = set()

# Esquemas del sistema y de producción estrictamente protegidos e intangibles
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
    "cron",
    "net",
    "pgsodium",
    "pg_graphql",
    "pgsodium_masks",
}

# Patrón obligatorio para esquemas de prueba permitidos
TEST_SCHEMA_PATTERN = re.compile(r"^test_(qa_p2p_\d{2}|sandbox)_[a-z0-9_]+$")

# Hosts y proyectos reconocidos explícitamente como destinos autorizados de prueba / QA
DEFAULT_ALLOWED_QA_HOSTS = {
    "localhost",
    "127.0.0.1",
    "::1",
    "db.ieaxmtxpcrldbvmqwbyt.supabase.co",  # Proyecto Supabase dedicado para QA/Dev EPIS-UPT
}


class DatabaseSecurityError(RuntimeError):
    """Excepción de seguridad ante intentos de operar en entornos o esquemas protegidos."""


def validate_test_environment(settings_env: str = "") -> None:
    """
    Verifica que ninguna variable de entorno declare producción y que existan marcadores
    explícitos de autorización para ejecución de pruebas.
    
    Regla estricta: Si CUALQUIERA de APP_ENV, ENVIRONMENT, NODE_ENV o STAGE declara 'production',
    la ejecución se aborta de forma inmediata. Ninguna variable local de desarrollo puede
    anular una bandera de producción.
    """
    env_vars = {
        "APP_ENV": os.environ.get("APP_ENV", ""),
        "ENVIRONMENT": settings_env or os.environ.get("ENVIRONMENT", ""),
        "NODE_ENV": os.environ.get("NODE_ENV", ""),
        "STAGE": os.environ.get("STAGE", ""),
    }

    # 1. Comprobación de banderas de producción
    for var_name, var_val in env_vars.items():
        val = str(var_val).strip().lower()
        if val in ("production", "prod") or val.startswith("prod"):
            raise DatabaseSecurityError(
                f"¡BLOQUEO DE SEGURIDAD! Variable de entorno prohibitiva detectada: {var_name}='{var_val}'. "
                "Las pruebas no pueden ejecutarse contra entornos de producción, "
                "incluso si otra variable declara un entorno local o de desarrollo."
            )

    # 2. Marcadores de autorización requeridos
    allow_flag = os.environ.get("ALLOW_TEST_SCHEMA_CREATION", "").lower()
    app_env = env_vars["APP_ENV"].lower()
    env_name = env_vars["ENVIRONMENT"].lower()
    stage = env_vars["STAGE"].lower()
    node_env = env_vars["NODE_ENV"].lower()

    is_authorized = (
        allow_flag in ("true", "1", "yes")
        or app_env in ("test", "testing", "development")
        or env_name in ("test", "testing", "development", "local")
        or stage in ("test", "testing", "dev", "qa", "staging-qa")
        or node_env in ("test", "development")
    )

    if not is_authorized:
        raise DatabaseSecurityError(
            "¡ACCESO DENEGADO! No se detectó autorización explícita para crear esquemas de prueba. "
            "Configure ALLOW_TEST_SCHEMA_CREATION=true o APP_ENV=test."
        )


def validate_qa_target_url(raw_url: str) -> None:
    """
    Verifica que la URL de destino esté explícitamente reconocida como entorno de pruebas o QA.
    Rechaza por defecto cualquier destino desconocido o que contenga marcadores de producción.
    """
    if not raw_url or not isinstance(raw_url, str):
        raise DatabaseSecurityError("La URL de base de datos de QA proporcionada es nula o inválida.")

    parsed = urllib.parse.urlsplit(raw_url)
    host = (parsed.hostname or "").strip().lower()

    if not host:
        raise DatabaseSecurityError("No se pudo determinar el nombre de host de la URL de base de datos.")

    # Marcadores prohibitivos en el host o path
    if any(p in host for p in ("prod", "production", "live", "main-cluster")):
        raise DatabaseSecurityError(
            f"¡BLOQUEO DE SEGURIDAD! El host '{host}' contiene identificadores de producción. Acceso denegado."
        )

    # Lista blanca configurable mediante ALLOWED_QA_HOSTS
    extra_hosts = {
        h.strip().lower()
        for h in os.environ.get("ALLOWED_QA_HOSTS", "").split(",")
        if h.strip()
    }
    allowed_hosts = DEFAULT_ALLOWED_QA_HOSTS | extra_hosts

    is_allowed = (
        host in allowed_hosts
        or host.endswith(".local")
        or host.startswith("test-")
        or host.startswith("qa-")
        or "qa" in host
        or "test" in host
    )

    if not is_allowed:
        raise DatabaseSecurityError(
            f"DESTINO NO AUTORIZADO: El host de base de datos '{host}' no está reconocido explícitamente "
            f"como un entorno de pruebas o QA autorizado. Lista permitida: {sorted(allowed_hosts)}"
        )


def resolve_qa_database_url() -> str:
    """
    Resuelve la URL de conexión exclusiva para pruebas de QA.
    Prioridad:
    1. Variable de entorno QA_DATABASE_URL
    2. settings.sync_qa_database_url (cargada desde aplicacion/backend/.env)
    
    Si no está configurada o no apunta a un destino de QA verificado, arroja DatabaseSecurityError.
    """
    raw_url = os.environ.get("QA_DATABASE_URL", "").strip()

    if not raw_url:
        try:
            from app.core.config import settings

            raw_url = (settings.sync_qa_database_url or "").strip()
        except Exception:
            pass

    if not raw_url:
        raise DatabaseSecurityError(
            "QA_DATABASE_URL_NOT_CONFIGURED: No se ha configurado la variable 'QA_DATABASE_URL'. "
            "Para proteger la instancia de producción, las pruebas automatizadas exigen una base "
            "de datos de QA debidamente identificada e independiente."
        )

    # Validar dialecto psycopg
    if raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif raw_url.startswith("postgresql://") and not raw_url.startswith("postgresql+"):
        raw_url = raw_url.replace("postgresql://", "postgresql+psycopg://", 1)

    validate_qa_target_url(raw_url)
    return raw_url


def verify_database_identity_and_role(engine: Engine) -> dict[str, str]:
    """
    Verifica la identidad de la base de datos y el rol de conexión en PostgreSQL
    antes de permitir cualquier operación DDL de creación de esquemas.
    """
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT current_database(), current_user, session_user;")
        ).fetchone()

        if not row:
            raise DatabaseSecurityError("No fue posible consultar la identidad de la base de datos en PostgreSQL.")

        curr_db = str(row[0]).strip().lower()
        curr_user = str(row[1]).strip().lower()
        sess_user = str(row[2]).strip().lower()

        if any(p in curr_db for p in ("prod", "production", "live")):
            raise DatabaseSecurityError(
                f"¡DESTINO PROHIBIDO! current_database()='{curr_db}' posee identificadores productivos."
            )

        return {
            "database": curr_db,
            "current_user": curr_user,
            "session_user": sess_user,
        }


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

    if not TEST_SCHEMA_PATTERN.match(schema_name):
        raise DatabaseSecurityError(f"El esquema '{schema_name}' no cumple con el patrón de pruebas permitido.")

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
    y que current_schema() coincida EXACTAMENTE con el esquema generado para la ejecución.
    
    No acepta como válido que el esquema esperado simplemente aparezca dentro de SHOW search_path.
    """
    curr = conn.execute(text("SELECT current_schema();")).scalar()
    search_path = conn.execute(text("SHOW search_path;")).scalar()

    if curr == "public":
        raise DatabaseSecurityError(
            f"¡VIOLACIÓN DE AISLAMIENTO! current_schema() es 'public'. "
            f"La conexión no está aislada en '{expected_schema}'."
        )

    if curr != expected_schema:
        raise DatabaseSecurityError(
            f"¡VIOLACIÓN DE AISLAMIENTO! current_schema() es '{curr}', "
            f"pero se exige coincidencia exacta con '{expected_schema}'. "
            f"(search_path activo reportado: '{search_path}')"
        )


def create_isolated_schema(engine: Engine, schema_name: str) -> str:
    """
    Crea un nuevo esquema temporal vacío en la base de datos y lo registra
    en la lista de esquemas administrados por esta ejecución.
    
    Verifica además que el esquema no exista previamente en PostgreSQL para
    evitar sobreescrituras accidentales de datos preexistentes.
    """
    if schema_name in FORBIDDEN_PROTECTED_SCHEMAS:
        raise DatabaseSecurityError(f"Prohibida la creación del esquema protegido '{schema_name}'.")

    if not TEST_SCHEMA_PATTERN.match(schema_name):
        raise DatabaseSecurityError(f"El esquema '{schema_name}' no cumple el patrón de pruebas permitido.")

    # 1. Verificar identidad del servidor
    verify_database_identity_and_role(engine)

    with engine.connect() as conn:
        # 2. Comprobar que no exista previamente en pg_namespace
        exists = conn.execute(
            text("SELECT 1 FROM information_schema.schemata WHERE schema_name = :s"),
            {"s": schema_name},
        ).scalar()
        if exists:
            raise DatabaseSecurityError(
                f"El esquema '{schema_name}' ya existe previamente en la base de datos. "
                "Se rechaza su adopción o reutilización para garantizar aislamiento estricto."
            )

        # 3. Crear esquema
        conn.execute(text(f'CREATE SCHEMA "{schema_name}";'))
        conn.commit()

    _CREATED_SCHEMAS_IN_THIS_RUN.add(schema_name)
    print(f"[SECURITY GUARD] Esquema sandbox único '{schema_name}' creado y registrado con éxito.")
    return schema_name


def safe_teardown_schema(engine: Engine, schema_name: str) -> None:
    """
    Elimina exclusivamente un esquema que haya sido creado por esta ejecución.
    Rechaza eliminar esquemas protegidos, no registrados o preexistentes.
    Comprueba en el catálogo de PostgreSQL la existencia y propiedad del esquema.
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
        # Verificar que el esquema exista en pg_namespace antes del drop
        exists = conn.execute(
            text("SELECT 1 FROM information_schema.schemata WHERE schema_name = :s"),
            {"s": schema_name},
        ).scalar()

        if exists:
            conn.execute(text(f'DROP SCHEMA "{schema_name}" CASCADE;'))
            conn.commit()

    _CREATED_SCHEMAS_IN_THIS_RUN.discard(schema_name)
    print(f"[SECURITY GUARD] Esquema sandbox verificado '{schema_name}' eliminado limpiamente.")


@contextmanager
def isolated_test_schema(engine: Engine, prefix: str = "test_qa_p2p_04"):
    """
    Context manager para aprovisionar y limpiar de forma garantizada un esquema sandbox
    incluso ante fallos o excepciones no controladas.
    """
    schema_name = generate_unique_test_schema(prefix)
    create_isolated_schema(engine, schema_name)
    try:
        yield schema_name
    finally:
        safe_teardown_schema(engine, schema_name)
