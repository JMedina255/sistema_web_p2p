"""
Pruebas de Validación de Configuración para Entornos de Staging y Producción (REL-P2P-02)
Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)
"""

import pytest
from pydantic import ValidationError

from app.core.config import Settings


class TestStagingProductionConfigValidation:
    """Valida los candados de seguridad en la configuración de Settings para Staging y Producción."""

    def test_development_allows_default_dev_secrets(self):
        s = Settings(
            APP_ENV="development",
            JWT_SECRET_KEY="dev-jwt-secret-key-epis-upt-2026-mentorias-change-in-production",
        )
        assert s.APP_ENV == "development"
        assert s.JWT_SECRET_KEY == "dev-jwt-secret-key-epis-upt-2026-mentorias-change-in-production"
        assert s.STRICT_DATABASE_MODE is False

    def test_staging_rejects_default_dev_jwt_secret(self):
        with pytest.raises(ValidationError) as exc_info:
            Settings(
                APP_ENV="staging",
                JWT_SECRET_KEY="dev-jwt-secret-key-epis-upt-2026-mentorias-change-in-production",
            )
        assert "JWT_SECRET_KEY insegura" in str(exc_info.value)

    def test_staging_rejects_placeholder_jwt_secret(self):
        with pytest.raises(ValidationError) as exc_info:
            Settings(
                APP_ENV="staging",
                JWT_SECRET_KEY="<GENERATE_SECURE_RANDOM_SECRET_MIN_32_CHARS>",
            )
        assert "JWT_SECRET_KEY insegura" in str(exc_info.value)

    def test_staging_rejects_short_jwt_secret(self):
        with pytest.raises(ValidationError) as exc_info:
            Settings(
                APP_ENV="staging",
                JWT_SECRET_KEY="short-secret-key",
            )
        assert "al menos 32 caracteres" in str(exc_info.value)

    def test_staging_rejects_mock_otp_hints(self):
        with pytest.raises(ValidationError) as exc_info:
            Settings(
                APP_ENV="staging",
                JWT_SECRET_KEY="a" * 32,
                ENABLE_MOCK_OTP_HINTS=True,
            )
        assert "ENABLE_MOCK_OTP_HINTS está terminantemente prohibido" in str(exc_info.value)

    def test_staging_rejects_explicit_strict_database_mode_false(self):
        with pytest.raises(ValidationError) as exc_info:
            Settings(
                APP_ENV="staging",
                JWT_SECRET_KEY="a" * 32,
                STRICT_DATABASE_MODE=False,
            )
        assert "STRICT_DATABASE_MODE debe ser True" in str(exc_info.value)

    def test_staging_defaults_strict_database_mode_to_true(self):
        s = Settings(
            APP_ENV="staging",
            JWT_SECRET_KEY="a" * 32,
        )
        assert s.STRICT_DATABASE_MODE is True

    def test_staging_rejects_placeholder_in_database_url(self):
        with pytest.raises(ValidationError) as exc_info:
            Settings(
                APP_ENV="staging",
                JWT_SECRET_KEY="a" * 32,
                DATABASE_URL="postgresql+psycopg://postgres.STAGING_PROJECT_REF:pass@aws-0.pooler.supabase.com/postgres",
            )
        assert "DATABASE_URL contiene marcadores de plantilla" in str(exc_info.value)

    def test_staging_rejects_smtp_enabled_with_placeholder_password(self):
        with pytest.raises(ValidationError) as exc_info:
            Settings(
                APP_ENV="staging",
                JWT_SECRET_KEY="a" * 32,
                SMTP_ENABLED=True,
                SMTP_USER="notificaciones@upt.pe",
                SMTP_PASSWORD="STAGING_APP_PASSWORD",
            )
        assert "SMTP_ENABLED=True en entorno 'staging', pero no se han configurado" in str(exc_info.value)

    def test_staging_accepts_valid_secure_configuration(self):
        s = Settings(
            APP_ENV="staging",
            JWT_SECRET_KEY="secure-high-entropy-jwt-secret-key-for-staging-epis-upt-2026",
            DATABASE_URL="postgresql+psycopg://postgres.abc123def456xyz78901:supersecretpassword@aws-0-us-east-1.pooler.supabase.com:5432/postgres",
            SMTP_ENABLED=False,
            ENABLE_MOCK_OTP_HINTS=False,
        )
        assert s.APP_ENV == "staging"
        assert s.STRICT_DATABASE_MODE is True
        assert s.ENABLE_MOCK_OTP_HINTS is False
