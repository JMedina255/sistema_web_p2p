"""
Pruebas de Seguridad y Hardening de Base de Datos (QA-P2P-04R)
Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)

Valida exhaustivamente los mecanismos de protección activa:
1. Prohibición estricta ante variables de producción (APP_ENV, ENVIRONMENT, NODE_ENV, STAGE).
2. Rechazo de anulación por variables locales cuando se detecta producción.
3. Validación de URLs permitidas y denegadas para QA_DATABASE_URL.
4. Exigencia de coincidencia exacta de current_schema() en verify_connection_search_path().
5. Bloqueo de adopción de esquemas preexistentes en create_isolated_schema().
6. Restricción estricta de safe_teardown_schema() a esquemas registrados en la corrida.
7. Manejo seguro de ciclo de vida con isolated_test_schema().
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Asegurar path de tools
root_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
tools_dir = os.path.join(root_project_dir, "tools")
if tools_dir not in sys.path:
    sys.path.insert(0, tools_dir)

from qa_db_hardening import (  # noqa: E402
    _CREATED_SCHEMAS_IN_THIS_RUN,
    FORBIDDEN_PROTECTED_SCHEMAS,
    DatabaseSecurityError,
    build_isolated_db_url,
    create_isolated_schema,
    generate_unique_test_schema,
    isolated_test_schema,
    resolve_qa_database_url,
    safe_teardown_schema,
    validate_qa_target_url,
    validate_test_environment,
    verify_connection_search_path,
    verify_database_identity_and_role,
)


class TestEnvironmentProtection:
    """Verifica el blindaje estricto ante banderas de entorno de producción."""

    @pytest.mark.parametrize("var_name", ["APP_ENV", "ENVIRONMENT", "NODE_ENV", "STAGE"])
    @pytest.mark.parametrize("prod_val", ["production", "prod", "Production", "PROD", "prod-cluster"])
    def test_production_environment_variables_strictly_aborts(self, var_name, prod_val, monkeypatch):
        monkeypatch.setenv(var_name, prod_val)
        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_test_environment()
        assert "BLOQUEO DE SEGURIDAD" in str(exc_info.value)
        assert var_name in str(exc_info.value)

    def test_local_dev_cannot_override_production(self, monkeypatch):
        """Una variable local de desarrollo o flag de prueba NO debe anular la presencia de producción."""
        monkeypatch.setenv("APP_ENV", "production")
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("ALLOW_TEST_SCHEMA_CREATION", "true")
        monkeypatch.setenv("NODE_ENV", "development")

        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_test_environment("development")
        assert "BLOQUEO DE SEGURIDAD" in str(exc_info.value)

    def test_unauthorized_environment_aborts(self, monkeypatch):
        """Si no hay marcadores explícitos de test/dev, el acceso es denegado por defecto."""
        monkeypatch.setenv("APP_ENV", "random_untrusted")
        monkeypatch.setenv("ENVIRONMENT", "unknown")
        monkeypatch.setenv("NODE_ENV", "")
        monkeypatch.setenv("STAGE", "")
        monkeypatch.delenv("ALLOW_TEST_SCHEMA_CREATION", raising=False)

        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_test_environment()
        assert "ACCESO DENEGADO" in str(exc_info.value)

    @pytest.mark.parametrize(
        "flag,val",
        [
            ("ALLOW_TEST_SCHEMA_CREATION", "true"),
            ("APP_ENV", "test"),
            ("APP_ENV", "development"),
            ("ENVIRONMENT", "test"),
            ("STAGE", "staging-qa"),
        ],
    )
    def test_authorized_environment_passes(self, flag, val, monkeypatch):
        # Limpiar variables productivas
        for k in ["APP_ENV", "ENVIRONMENT", "NODE_ENV", "STAGE", "ALLOW_TEST_SCHEMA_CREATION"]:
            monkeypatch.delenv(k, raising=False)
        monkeypatch.setenv(flag, val)
        # No debe lanzar excepción
        validate_test_environment()


class TestTargetUrlValidation:
    """Verifica que solo se permitan hosts de pruebas explícitamente autorizados."""

    def test_invalid_or_empty_urls_rejected(self):
        with pytest.raises(DatabaseSecurityError):
            validate_qa_target_url("")
        with pytest.raises(DatabaseSecurityError):
            validate_qa_target_url(None)
        with pytest.raises(DatabaseSecurityError):
            validate_qa_target_url("not_a_valid_url")

    @pytest.mark.parametrize(
        "bad_host",
        [
            "db.production.supabase.co",
            "live-db.upt.pe",
            "prod-postgres.upt.pe",
            "main-cluster.internal",
        ],
    )
    def test_production_host_markers_rejected(self, bad_host):
        url = f"postgresql+psycopg://user:pass@{bad_host}:5432/postgres"
        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_qa_target_url(url)
        assert "identificadores de producción" in str(exc_info.value)

    def test_unrecognized_host_rejected_by_default(self):
        url = "postgresql+psycopg://user:pass@random-unauthorized-server.com:5432/db"
        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_qa_target_url(url)
        assert "DESTINO NO AUTORIZADO" in str(exc_info.value)

    @pytest.mark.parametrize(
        "good_host",
        [
            "localhost",
            "127.0.0.1",
            "::1",
            "db.ieaxmtxpcrldbvmqwbyt.supabase.co",
            "my-test-db.local",
            "qa-postgres-instance",
        ],
    )
    def test_allowed_qa_hosts_accepted(self, good_host):
        host_repr = f"[{good_host}]" if ":" in good_host else good_host
        url = f"postgresql+psycopg://user:pass@{host_repr}:5432/postgres"
        validate_qa_target_url(url)

    def test_custom_allowed_qa_hosts_via_env(self, monkeypatch):
        monkeypatch.setenv("ALLOWED_QA_HOSTS", "custom-qa.internal,staging-db.test")
        url = "postgresql+psycopg://user:pass@custom-qa.internal:5432/postgres"
        validate_qa_target_url(url)


class TestResolveQaDatabaseUrl:
    """Verifica la resolución exclusiva de QA_DATABASE_URL."""

    def test_missing_qa_database_url_raises(self, monkeypatch):
        monkeypatch.delenv("QA_DATABASE_URL", raising=False)
        with patch("app.core.config.settings") as mock_settings:
            mock_settings.sync_qa_database_url = None
            with pytest.raises(DatabaseSecurityError) as exc_info:
                resolve_qa_database_url()
            assert "QA_DATABASE_URL_NOT_CONFIGURED" in str(exc_info.value)

    def test_valid_qa_database_url_resolved_and_normalized(self, monkeypatch):
        monkeypatch.setenv("QA_DATABASE_URL", "postgres://qa_user:pass@127.0.0.1:5432/qa_db")
        url = resolve_qa_database_url()
        assert url.startswith("postgresql+psycopg://qa_user:pass@127.0.0.1:5432/qa_db")


class TestSearchPathAndIdentityVerification:
    """Verifica la comprobación estricta de current_schema() e identidad de base de datos."""

    def test_verify_search_path_strictly_requires_exact_match(self):
        mock_conn = MagicMock()

        # Caso 1: current_schema() es 'public' -> RECHAZADO
        mock_conn.execute.return_value.scalar.side_effect = ["public", "test_schema, public"]
        with pytest.raises(DatabaseSecurityError) as exc_info:
            verify_connection_search_path(mock_conn, "test_schema")
        assert "current_schema() es 'public'" in str(exc_info.value)

        # Caso 2: current_schema() no coincide aunque search_path contenga el esquema -> RECHAZADO
        mock_conn.execute.return_value.scalar.side_effect = ["other_schema", "test_schema, other_schema"]
        with pytest.raises(DatabaseSecurityError) as exc_info:
            verify_connection_search_path(mock_conn, "test_schema")
        assert "coincidencia exacta" in str(exc_info.value)

        # Caso 3: current_schema() coincide exactamente -> PERMITIDO
        mock_conn.execute.return_value.scalar.side_effect = ["test_schema", "test_schema"]
        verify_connection_search_path(mock_conn, "test_schema")

    def test_verify_database_identity_rejects_production_dbname(self):
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        # current_database() con nombre prod -> RECHAZADO
        mock_conn.execute.return_value.fetchone.return_value = ("prod_epis_upt", "qa_user", "qa_user")
        with pytest.raises(DatabaseSecurityError) as exc_info:
            verify_database_identity_and_role(mock_engine)
        assert "DESTINO PROHIBIDO" in str(exc_info.value)

        # current_database() legítimo -> PERMITIDO
        mock_conn.execute.return_value.fetchone.return_value = ("postgres", "qa_role", "qa_role")
        ident = verify_database_identity_and_role(mock_engine)
        assert ident["database"] == "postgres"
        assert ident["current_user"] == "qa_role"


class TestSchemaLifecycleAndGuards:
    """Verifica la generación, creación, aislamiento y teardown seguro de esquemas."""

    def setup_method(self):
        _CREATED_SCHEMAS_IN_THIS_RUN.clear()

    def test_schema_name_generation_and_pattern(self):
        schema1 = generate_unique_test_schema("test_qa_p2p_04")
        schema2 = generate_unique_test_schema("test_qa_p2p_04")
        assert schema1.startswith("test_qa_p2p_04_")
        assert schema2.startswith("test_qa_p2p_04_")
        assert schema1 != schema2

    def test_build_isolated_db_url_guards(self):
        base_url = "postgresql+psycopg://user:pass@127.0.0.1:5432/postgres?sslmode=require"

        # Prohíbe esquemas protegidos
        for p in FORBIDDEN_PROTECTED_SCHEMAS:
            with pytest.raises(DatabaseSecurityError):
                build_isolated_db_url(base_url, p)

        # Construcción segura agregando options
        iso_url = build_isolated_db_url(base_url, "test_qa_p2p_04_a1b2c3d4")
        assert "options=-c%20search_path=test_qa_p2p_04_a1b2c3d4" in iso_url
        assert "sslmode=require" in iso_url

    def test_create_isolated_schema_blocks_preexisting_schemas(self):
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        # Simular identidad segura
        mock_conn.execute.return_value.fetchone.return_value = ("postgres", "qa_user", "qa_user")

        # Simular que el esquema ya existe en information_schema.schemata
        mock_conn.execute.return_value.scalar.return_value = 1

        with pytest.raises(DatabaseSecurityError) as exc_info:
            create_isolated_schema(mock_engine, "test_qa_p2p_04_exists")
        assert "ya existe previamente en la base de datos" in str(exc_info.value)

    def test_create_isolated_schema_success_registers_in_memory(self):
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_conn.execute.return_value.fetchone.return_value = ("postgres", "qa_user", "qa_user")
        mock_conn.execute.return_value.scalar.return_value = None  # No existe

        schema_name = "test_qa_p2p_04_new_1234"
        created = create_isolated_schema(mock_engine, schema_name)
        assert created == schema_name
        assert schema_name in _CREATED_SCHEMAS_IN_THIS_RUN

    def test_safe_teardown_rejects_unregistered_or_protected_schemas(self):
        mock_engine = MagicMock()

        # Rechazo de protegido
        with pytest.raises(DatabaseSecurityError):
            safe_teardown_schema(mock_engine, "public")

        # Rechazo de esquema no creado por esta corrida
        with pytest.raises(DatabaseSecurityError) as exc_info:
            safe_teardown_schema(mock_engine, "test_qa_p2p_04_unregistered")
        assert "no fue creado por esta ejecución" in str(exc_info.value)

    def test_safe_teardown_success_drops_and_unregisters(self):
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value.scalar.return_value = 1  # Existe

        schema_name = "test_qa_p2p_04_registered"
        _CREATED_SCHEMAS_IN_THIS_RUN.add(schema_name)

        safe_teardown_schema(mock_engine, schema_name)
        assert schema_name not in _CREATED_SCHEMAS_IN_THIS_RUN

    def test_isolated_test_schema_context_manager_cleans_up_on_failure(self):
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_conn.execute.return_value.fetchone.return_value = ("postgres", "qa_user", "qa_user")
        mock_conn.execute.return_value.scalar.return_value = None  # Para create: no existe

        yielded_schema = None
        with pytest.raises(ZeroDivisionError):
            with isolated_test_schema(mock_engine) as s:
                yielded_schema = s
                assert yielded_schema in _CREATED_SCHEMAS_IN_THIS_RUN
                # Provocar excepción deliberada en bloque
                _ = 1 / 0

        # Al salir por la excepción, el teardown debe haber desregistrado el esquema
        assert yielded_schema not in _CREATED_SCHEMAS_IN_THIS_RUN
