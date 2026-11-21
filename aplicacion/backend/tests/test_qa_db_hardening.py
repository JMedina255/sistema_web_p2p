"""
Pruebas de Seguridad y Hardening de Base de Datos (QA-P2P-04R & REL-P2P-01)
Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)

Valida exhaustivamente los mecanismos de protección activa:
1. Comprobación estrictamente independiente de variables (APP_ENV, ENVIRONMENT, NODE_ENV, STAGE, settings_env).
2. Rechazo de anulación por variables locales cuando se detecta producción.
3. Validación de URLs: solo hosts autorizados explícitamente (sin excepciones por substrings 'qa' o 'test').
4. Prevención de colisión de destinos: rechazo si QA_DATABASE_URL apunta a la misma BD que DATABASE_URL.
5. Exigencia de coincidencia exacta de current_schema() en verify_connection_search_path().
6. Bloqueo de adopción de esquemas preexistentes en create_isolated_schema().
7. Restricción estricta de safe_teardown_schema() a esquemas registrados en la corrida.
8. Limpieza garantizada y recuperación ante fallos en provision_fn con isolated_test_schema().
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
    extract_supabase_project_ref,
    generate_unique_test_schema,
    isolated_test_schema,
    resolve_qa_database_url,
    safe_teardown_schema,
    validate_qa_not_same_as_production,
    validate_qa_target_url,
    validate_test_environment,
    verify_connection_search_path,
    verify_database_identity_and_role,
)


class TestEnvironmentProtection:
    """Verifica el blindaje estricto e independiente ante banderas de entorno."""

    @pytest.mark.parametrize("var_name", ["APP_ENV", "ENVIRONMENT", "NODE_ENV", "STAGE"])
    @pytest.mark.parametrize("prod_val", ["production", "prod", "Production", "PROD", "prod-cluster", "live"])
    def test_production_environment_variables_strictly_aborts(self, var_name, prod_val, monkeypatch):
        monkeypatch.setenv(var_name, prod_val)
        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_test_environment()
        assert "BLOQUEO DE SEGURIDAD" in str(exc_info.value)
        assert var_name in str(exc_info.value)

    def test_each_variable_checked_independently_no_shadowing(self, monkeypatch):
        """Verifica que ENVIRONMENT en os.environ no sea silenciado si settings_env se provee."""
        # Caso 1: os.environ[ENVIRONMENT] es prod, settings_env es development -> RECHAZADO
        monkeypatch.setenv("ENVIRONMENT", "production")
        monkeypatch.delenv("APP_ENV", raising=False)
        monkeypatch.delenv("NODE_ENV", raising=False)
        monkeypatch.delenv("STAGE", raising=False)
        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_test_environment("development")
        assert "ENVIRONMENT='production'" in str(exc_info.value)

        # Caso 2: os.environ[ENVIRONMENT] es test, settings_env es production -> RECHAZADO
        monkeypatch.setenv("ENVIRONMENT", "test")
        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_test_environment("production")
        assert "SETTINGS_ENV='production'" in str(exc_info.value)

        # Caso 3: NODE_ENV es production, APP_ENV es test -> RECHAZADO
        monkeypatch.setenv("APP_ENV", "test")
        monkeypatch.setenv("NODE_ENV", "production")
        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_test_environment()
        assert "NODE_ENV='production'" in str(exc_info.value)

        # Caso 4: STAGE es production, APP_ENV es test -> RECHAZADO
        monkeypatch.setenv("NODE_ENV", "test")
        monkeypatch.setenv("STAGE", "production")
        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_test_environment()
        assert "STAGE='production'" in str(exc_info.value)

    def test_local_dev_cannot_override_production(self, monkeypatch):
        """Una variable local de desarrollo o flag de prueba NO debe anular la presencia de producción."""
        monkeypatch.setenv("APP_ENV", "production")
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("ALLOW_TEST_SCHEMA_CREATION", "true")
        monkeypatch.setenv("NODE_ENV", "development")

        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_test_environment("development")
        assert "BLOQUEO DE SEGURIDAD" in str(exc_info.value)

    def test_unauthorized_environment_value_rejected(self, monkeypatch):
        """Valores no reconocidos para variables de prueba son rechazados de forma independiente."""
        monkeypatch.delenv("APP_ENV", raising=False)
        monkeypatch.delenv("NODE_ENV", raising=False)
        monkeypatch.delenv("STAGE", raising=False)
        monkeypatch.setenv("ENVIRONMENT", "unauthorized_custom_env")

        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_test_environment()
        assert "VALOR NO AUTORIZADO" in str(exc_info.value)

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
    """Verifica que solo se permitan hosts de pruebas explícitamente autorizados (sin excepciones heurísticas)."""

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
        "heuristic_host",
        [
            "qa-postgres.otherdomain.com",
            "test-database.corp.net",
            "my-database-qa.internal",
            "local-server.local",
            "staging-qa-box.org",
        ],
    )
    def test_heuristic_substring_hosts_strictly_rejected_without_explicit_whitelist(self, heuristic_host):
        """Elimina excepciones basadas únicamente en contener 'qa' o 'test'."""
        url = f"postgresql+psycopg://user:pass@{heuristic_host}:5432/postgres"
        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_qa_target_url(url)
        assert "DESTINO NO AUTORIZADO" in str(exc_info.value)

    @pytest.mark.parametrize(
        "good_host",
        [
            "localhost",
            "127.0.0.1",
            "::1",
        ],
    )
    def test_allowed_qa_hosts_accepted(self, good_host):
        host_repr = f"[{good_host}]" if ":" in good_host else good_host
        url = f"postgresql+psycopg://user:pass@{host_repr}:5432/postgres"
        validate_qa_target_url(url)

    def test_primary_supabase_host_rejected_by_default(self, monkeypatch):
        # El host principal de Supabase ya no está en la lista blanca por defecto
        monkeypatch.delenv("ALLOWED_QA_HOSTS", raising=False)
        url = "postgresql+psycopg://user:pass@db.ieaxmtxpcrldbvmqwbyt.supabase.co:5432/postgres"
        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_qa_target_url(url)
        assert "DESTINO NO AUTORIZADO" in str(exc_info.value)

    def test_custom_allowed_qa_hosts_via_env(self, monkeypatch):
        monkeypatch.setenv(
            "ALLOWED_QA_HOSTS", "custom-qa.internal,staging-db.test,db.ieaxmtxpcrldbvmqwbyt.supabase.co"
        )
        url = "postgresql+psycopg://user:pass@custom-qa.internal:5432/postgres"
        validate_qa_target_url(url)
        # Con la variable de entorno, ahora sí es aceptado
        supabase_url = "postgresql+psycopg://user:pass@db.ieaxmtxpcrldbvmqwbyt.supabase.co:5432/postgres"
        validate_qa_target_url(supabase_url)


class TestDestinationCollisionProtection:
    """Verifica que QA_DATABASE_URL no resuelva al mismo destino que DATABASE_URL."""

    def test_extract_supabase_project_ref_direct_and_pooler(self):
        direct_url = "postgresql+psycopg://postgres:secret@db.ieaxmtxpcrldbvmqwbyt.supabase.co:5432/postgres"
        assert extract_supabase_project_ref(direct_url) == "ieaxmtxpcrldbvmqwbyt"

        pooler_url = "postgresql+psycopg://postgres.ieaxmtxpcrldbvmqwbyt:secret@aws-0-us-east-1.pooler.supabase.com:5432/postgres"
        assert extract_supabase_project_ref(pooler_url) == "ieaxmtxpcrldbvmqwbyt"

        non_supabase = "postgresql+psycopg://user:pass@127.0.0.1:5432/qa_postgres"
        assert extract_supabase_project_ref(non_supabase) is None

    def test_qa_same_destination_as_production_rejected(self, monkeypatch):
        same_url = "postgresql+psycopg://postgres:secret@127.0.0.1:5432/postgres"
        monkeypatch.setenv("DATABASE_URL", same_url)
        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_qa_not_same_as_production(same_url, same_url)
        assert "COLISIÓN DE DESTINOS DETECTADA" in str(exc_info.value)

    def test_qa_supabase_project_collision_across_direct_and_pooler_rejected(self, monkeypatch):
        prod_direct = "postgresql+psycopg://postgres:secret@db.ieaxmtxpcrldbvmqwbyt.supabase.co:5432/postgres"
        qa_pooler = "postgresql+psycopg://postgres.ieaxmtxpcrldbvmqwbyt:secret@aws-0-us-east-1.pooler.supabase.com:5432/postgres"
        monkeypatch.setenv("DATABASE_URL", prod_direct)

        with pytest.raises(DatabaseSecurityError) as exc_info:
            validate_qa_not_same_as_production(qa_pooler, prod_direct)
        assert "COLISIÓN DE PROYECTO SUPABASE DETECTADA" in str(exc_info.value)

    def test_qa_distinct_supabase_projects_accepted(self, monkeypatch):
        prod_url = "postgresql+psycopg://postgres:secret@db.ieaxmtxpcrldbvmqwbyt.supabase.co:5432/postgres"
        staging_url = "postgresql+psycopg://postgres.stgprojectref1234567:secret@aws-0-us-east-1.pooler.supabase.com:5432/postgres"
        monkeypatch.setenv("DATABASE_URL", prod_url)
        validate_qa_not_same_as_production(staging_url, prod_url)

    def test_qa_different_destination_accepted(self, monkeypatch):
        prod_url = "postgresql+psycopg://postgres:secret@db.ieaxmtxpcrldbvmqwbyt.supabase.co:5432/postgres"
        qa_url = "postgresql+psycopg://qa_user:secret@127.0.0.1:5432/qa_postgres"
        monkeypatch.setenv("DATABASE_URL", prod_url)
        validate_qa_not_same_as_production(qa_url, prod_url)


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
        monkeypatch.delenv("DATABASE_URL", raising=False)
        with patch("app.core.config.settings") as mock_settings:
            mock_settings.DATABASE_URL = None
            url = resolve_qa_database_url(check_distinct_destination=False)
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
        mock_conn.execute.return_value.fetchone.return_value = (
            "prod_epis_upt",
            "qa_user",
            "qa_user",
            False,
            False,
        )
        with pytest.raises(DatabaseSecurityError) as exc_info:
            verify_database_identity_and_role(mock_engine)
        assert "DESTINO PROHIBIDO" in str(exc_info.value)

        # current_database() legítimo con rol de mínimos privilegios -> PERMITIDO
        mock_conn.execute.return_value.fetchone.return_value = (
            "postgres",
            "qa_role",
            "qa_role",
            False,
            False,
        )
        ident = verify_database_identity_and_role(mock_engine)
        assert ident["database"] == "postgres"
        assert ident["current_user"] == "qa_role"
        assert ident["is_superuser"] is False
        assert ident["can_create_role"] is False

    def test_database_identity_rejects_superuser_role(self, monkeypatch):
        monkeypatch.delenv("ALLOW_SUPERUSER_QA_ROLE", raising=False)
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        # Rol con rolsuper=True -> RECHAZADO por no cumplir least-privilege
        mock_conn.execute.return_value.fetchone.return_value = (
            "postgres",
            "postgres_admin",
            "postgres_admin",
            True,
            False,
        )
        with pytest.raises(DatabaseSecurityError) as exc_info:
            verify_database_identity_and_role(mock_engine)
        assert "PRIVILEGIOS EXCESIVOS RECHAZADOS" in str(exc_info.value)
        assert "rolsuper=True" in str(exc_info.value)

    def test_database_identity_rejects_createrole_privilege(self, monkeypatch):
        monkeypatch.delenv("ALLOW_SUPERUSER_QA_ROLE", raising=False)
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        # Rol con rolcreaterole=True -> RECHAZADO
        mock_conn.execute.return_value.fetchone.return_value = (
            "postgres",
            "qa_elevated_role",
            "qa_elevated_role",
            False,
            True,
        )
        with pytest.raises(DatabaseSecurityError) as exc_info:
            verify_database_identity_and_role(mock_engine)
        assert "PRIVILEGIOS EXCESIVOS RECHAZADOS" in str(exc_info.value)
        assert "rolcreaterole=True" in str(exc_info.value)

    def test_database_identity_allows_superuser_when_explicitly_authorized(self, monkeypatch):
        monkeypatch.setenv("ALLOW_SUPERUSER_QA_ROLE", "true")
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_conn.execute.return_value.fetchone.return_value = (
            "postgres",
            "postgres",
            "postgres",
            True,
            True,
        )
        ident = verify_database_identity_and_role(mock_engine)
        assert ident["current_user"] == "postgres"
        assert ident["is_superuser"] is True


class TestSchemaLifecycleAndGuards:
    """Verifica la generación, creación, aislamiento, teardown y recuperación de esquemas."""

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

        mock_conn.execute.return_value.fetchone.return_value = (
            "postgres",
            "qa_user",
            "qa_user",
            False,
            False,
        )
        mock_conn.execute.return_value.scalar.return_value = 1  # Ya existe

        with pytest.raises(DatabaseSecurityError) as exc_info:
            create_isolated_schema(mock_engine, "test_qa_p2p_04_exists")
        assert "ya existe previamente en la base de datos" in str(exc_info.value)

    def test_create_isolated_schema_success_registers_in_memory(self):
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_conn.execute.return_value.fetchone.return_value = (
            "postgres",
            "qa_user",
            "qa_user",
            False,
            False,
        )
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

    def test_isolated_test_schema_cleans_up_on_failure_during_provisioning(self):
        """Verifica que si provision_fn falla, el esquema se destruye de forma garantizada."""
        mock_engine = MagicMock()
        mock_engine.url = "postgresql+psycopg://user:pass@127.0.0.1:5432/qa_postgres"
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_conn.execute.return_value.fetchone.return_value = (
            "postgres",
            "qa_user",
            "qa_user",
            False,
            False,
        )
        mock_conn.execute.return_value.scalar.return_value = None  # No existe al crear, 1 al teardown

        def failing_provision(schema_name, isolated_url):
            raise RuntimeError("Fallo deliberado al crear tablas / fixtures DDL")

        yielded = False
        with pytest.raises(RuntimeError) as exc_info:
            with isolated_test_schema(mock_engine, provision_fn=failing_provision):
                yielded = True

        assert not yielded, "El bloque no debió ejecutarse si provision_fn falló"
        assert "Fallo deliberado al crear tablas" in str(exc_info.value)
        # Debe haberse limpiado el registro en memoria
        assert len(_CREATED_SCHEMAS_IN_THIS_RUN) == 0

    def test_isolated_test_schema_context_manager_cleans_up_on_test_failure(self):
        mock_engine = MagicMock()
        mock_engine.url = "postgresql+psycopg://user:pass@127.0.0.1:5432/qa_postgres"
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_conn.execute.return_value.fetchone.return_value = (
            "postgres",
            "qa_user",
            "qa_user",
            False,
            False,
        )
        mock_conn.execute.return_value.scalar.return_value = None

        yielded_schema = None
        with pytest.raises(ZeroDivisionError):
            with isolated_test_schema(mock_engine) as s:
                yielded_schema = s
                assert yielded_schema in _CREATED_SCHEMAS_IN_THIS_RUN
                _ = 1 / 0

        assert yielded_schema not in _CREATED_SCHEMAS_IN_THIS_RUN

    def test_isolated_test_schema_raises_when_teardown_fails(self):
        mock_engine = MagicMock()
        mock_engine.url = "postgresql+psycopg://user:pass@127.0.0.1:5432/qa_postgres"
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_conn.execute.return_value.fetchone.return_value = (
            "postgres",
            "qa_user",
            "qa_user",
            False,
            False,
        )
        # Permite creación (scalar -> None)
        mock_conn.execute.return_value.scalar.return_value = None

        with patch("qa_db_hardening.safe_teardown_schema") as mock_teardown:
            mock_teardown.side_effect = RuntimeError("Error forzado en DROP SCHEMA")

            with pytest.raises(DatabaseSecurityError) as exc_info:
                with isolated_test_schema(mock_engine) as s:
                    assert s in _CREATED_SCHEMAS_IN_THIS_RUN

            assert "FALLO CRÍTICO DE TEARDOWN" in str(exc_info.value)
