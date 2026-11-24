import json
import os
from math import ceil
from pathlib import Path

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
_ENV_PATH = _BACKEND_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(_ENV_PATH, ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_ENV: str = "development"
    PROJECT_NAME: str = "Sistema Web P2P - EPIS UPT"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    # Cadena de conexión privada a PostgreSQL / Supabase
    # repr=False previene que el valor sea expuesto en logs o representaciones de texto
    DATABASE_URL: str | None = Field(default=None, repr=False)
    QA_DATABASE_URL: str | None = Field(
        default=None,
        repr=False,
        description="Cadena de conexión privada exclusiva para pruebas de QA e integración (independiente de producción)",
    )
    DB_CONNECT_TIMEOUT: int = Field(default=5, description="Timeout en segundos para conexión con la BD")

    # Configuración de Seguridad y JWT (T-03 / RNF01 / RNF02)
    JWT_SECRET_KEY: str = Field(
        default="dev-jwt-secret-key-epis-upt-2026-mentorias-change-in-production",
        repr=False,
        description="Clave secreta para firma de tokens JWT (usar el JWT Secret de Supabase en producción)",
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 horas continuas según RNF01
    OTP_EXPIRE_MINUTES: int = 5  # Ventana de 5 minutos según RNF01
    OTP_COOLDOWN_SECONDS: int = 60  # Cooldown de 60 segundos según CUS01
    MAX_OTP_ATTEMPTS: int = Field(
        default=5,
        description="Número máximo de intentos fallidos permitidos antes del bloqueo definitivo del desafío OTP",
    )
    OTP_RATE_LIMIT_PER_MINUTE: int = Field(
        default=5,
        description="Límite normativo de solicitudes de emisión OTP por minuto por destinatario e IP",
    )
    ENABLE_MOCK_OTP_HINTS: bool = Field(
        default=False,
        description="Expone mockCodeHint exclusivamente en entornos de pruebas automatizadas aisladas",
    )

    # Variables de entorno para Reservas, Concurrencia y Quórum (Sprint 4 / Cuadro 4.9 / Regla D-9)
    BOOKING_TIMEOUT_SECONDS: int = Field(
        default=5,
        description="Tiempo límite en segundos para adquisición del candado pesimista FOR UPDATE antes de abortar.",
    )
    QUORUM_MINIMUM_PERCENTAGE: int = Field(
        default=50,
        ge=0,
        le=100,
        description="Porcentaje mínimo normativo de alumnos confirmados respecto al aforo para declarar sesión confirmada (RN-09).",
    )
    QUORUM_CUTOFF_HOURS: int = Field(
        default=24,
        description="Horas de antelación obligatoria para el cierre de confirmaciones y cálculo desatendido de quórum (RN-08).",
    )
    ENABLE_CONCURRENCY_STRESS_TEST: bool = Field(
        default=False,
        description="Habilita endpoints de prueba de simulación multihilo para auditoría de concurrencia y validación de RNF07.",
    )

    # Configuración de Correo Electrónico (SMTP orientada por defecto a Gmail / Google)
    SMTP_ENABLED: bool = Field(
        default=False,
        description="Activa el envío real de correos mediante servidor SMTP",
    )
    SMTP_HOST: str = Field(
        default="smtp.gmail.com",
        description="Servidor SMTP (por defecto smtp.gmail.com para cuentas de Google)",
    )
    SMTP_PORT: int = Field(
        default=587,
        description="Puerto SMTP (587 para STARTTLS, 465 para SSL)",
    )
    SMTP_USE_TLS: bool = Field(
        default=True,
        description="Usar cifrado STARTTLS",
    )
    SMTP_USER: str | None = Field(
        default=None,
        description="Usuario o correo de la cuenta de Google (ej. mentorias.upt@gmail.com)",
    )
    SMTP_PASSWORD: str | None = Field(
        default=None,
        repr=False,
        description="Contraseña de aplicación (Google App Password de 16 caracteres)",
    )
    SMTP_FROM_EMAIL: str = Field(
        default="noreply.mentoria.upt@gmail.com",
        description="Dirección remitente visible",
    )
    SMTP_FROM_NAME: str = Field(
        default="Sistema de Mentorías EPIS-UPT",
        description="Nombre del remitente",
    )

    # Configuración de Almacenamiento Híbrido (Storage)
    STORAGE_BACKEND: str = Field(
        default="local",
        description="Proveedor de almacenamiento: 'local' o 'supabase'",
    )
    STORAGE_LOCAL_DIR: str = Field(
        default="uploads",
        description="Directorio local para almacenamiento de archivos",
    )
    SUPABASE_URL: str | None = Field(
        default=None,
        description="URL base del proyecto de Supabase (ej. https://xyz.supabase.co)",
    )
    SUPABASE_SERVICE_ROLE_KEY: str | None = Field(
        default=None,
        repr=False,
        description="Clave de servicio de Supabase con permisos para Storage",
    )
    SUPABASE_BUCKET_CERTIFICATES: str = Field(
        default="certificados",
        description="Bucket para constancias PDF",
    )
    SUPABASE_BUCKET_RESOURCES: str = Field(
        default="recursos",
        description="Bucket o carpeta para recursos académicos adjuntos",
    )
    ENABLE_DEMO_WATERMARK: bool = Field(
        default=False,
        description="Estampar marca de agua 'DEMO' en PDFs generados. Por defecto False (emisión oficial limpia sin marcas de agua).",
    )

    # Planificador Desatendido en Segundo Plano (Scheduler)
    ENABLE_BACKGROUND_SCHEDULER: bool = Field(
        default=True,
        description="Activa el evaluador automático de quórum en segundo plano",
    )
    SCHEDULER_INTERVAL_MINUTES: int = Field(
        default=15,
        description="Intervalo en minutos para revisión periódica de quórum a T-24h",
    )

    # Autenticación Federada Google Identity
    GOOGLE_CLIENT_ID: str = Field(
        default="542248584798-ev9m68d5ial7g4bghqiatd1r3b5rduls.apps.googleusercontent.com",
        description="Google OAuth Client ID para autenticación institucional con @virtual.upt.pe",
    )

    # Modo de Persistencia Estricto (Prevención de degradación silenciosa a RAM)
    STRICT_DATABASE_MODE: bool = Field(
        default=False,
        description="En modo estricto, rechaza transacciones con HTTP 503 si PostgreSQL no está disponible",
    )

    def quorum_minimum_students(self, capacity: int) -> int:
        return ceil(capacity * self.QUORUM_MINIMUM_PERCENTAGE / 100)

    @model_validator(mode="after")
    def adjust_production_defaults(self):
        # En producción o staging, forzar persistencia estricta para erradicar degradación a RAM
        if self.APP_ENV in ("production", "staging"):
            if "STRICT_DATABASE_MODE" not in self.model_fields_set:
                self.STRICT_DATABASE_MODE = True
            elif not self.STRICT_DATABASE_MODE:
                raise ValueError(
                    f"STRICT_DATABASE_MODE debe ser True en entorno '{self.APP_ENV}' "
                    "para impedir la degradación silenciosa a almacenamiento volátil en RAM."
                )

            if self.ENABLE_MOCK_OTP_HINTS:
                raise ValueError(
                    f"ENABLE_MOCK_OTP_HINTS está terminantemente prohibido en entorno '{self.APP_ENV}' "
                    "(RNF01 / RNF02). Los desafíos OTP no deben exponer pistas de código fuera de pruebas unitarias aisladas."
                )

            # Validación de clave JWT en entornos controlados
            known_insecure_keys = {
                "dev-jwt-secret-key-epis-upt-2026-mentorias-change-in-production",
                "staging-jwt-secret-key-epis-upt-2026-mentorias-staging-env-only",
            }
            if (
                self.JWT_SECRET_KEY in known_insecure_keys
                or "<GENERATE_" in self.JWT_SECRET_KEY
                or "change-in-production" in self.JWT_SECRET_KEY.lower()
                or len(self.JWT_SECRET_KEY) < 32
            ):
                raise ValueError(
                    f"JWT_SECRET_KEY insegura o con valor de plantilla detectada en entorno '{self.APP_ENV}'. "
                    "Debe configurarse una clave criptográfica de alta entropía de al menos 32 caracteres."
                )

            # Validación de marcadores de plantilla en DATABASE_URL
            if self.DATABASE_URL:
                db_str = str(self.DATABASE_URL)
                if "<GENERATE_" in db_str or "STAGING_PROJECT_REF" in db_str:
                    raise ValueError(
                        f"DATABASE_URL contiene marcadores de plantilla no sustituidos en entorno '{self.APP_ENV}'. "
                        "Configure la cadena de conexión real de la instancia dedicada."
                    )

            # Validación de credenciales SMTP si el servicio está habilitado
            if self.SMTP_ENABLED:
                if (
                    not self.SMTP_USER
                    or not self.SMTP_PASSWORD
                    or "<GENERATE_" in (self.SMTP_PASSWORD or "")
                    or "STAGING_APP_PASSWORD" in (self.SMTP_PASSWORD or "")
                ):
                    raise ValueError(
                        f"SMTP_ENABLED=True en entorno '{self.APP_ENV}', pero no se han configurado "
                        "credenciales válidas de correo (SMTP_USER / SMTP_PASSWORD). "
                        "Mantenga SMTP_ENABLED=False mientras no existan buzones ni credenciales de prueba autorizadas."
                    )

            if self.APP_ENV == "production" and "ENABLE_DEMO_WATERMARK" not in self.model_fields_set:
                self.ENABLE_DEMO_WATERMARK = False

        return self

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            v_str = v.strip()
            if v_str.startswith("[") and v_str.endswith("]"):
                try:
                    return json.loads(v_str)
                except Exception:
                    pass
            return [i.strip() for i in v_str.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return [str(v)]

    @property
    def sync_database_url(self) -> str | None:
        """
        Retorna la URL formateada para el dialecto psycopg 3 (postgresql+psycopg://).
        """
        if not self.DATABASE_URL:
            return None
        url = self.DATABASE_URL.strip()
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+psycopg://", 1)
        elif url.startswith("postgresql://") and not url.startswith("postgresql+"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url

    @property
    def sync_qa_database_url(self) -> str | None:
        """
        Retorna la URL de QA formateada para el dialecto psycopg 3 (postgresql+psycopg://).
        Si no se define QA_DATABASE_URL, retorna None.
        """
        raw_url = self.QA_DATABASE_URL or os.environ.get("QA_DATABASE_URL")
        if not raw_url:
            return None
        url = raw_url.strip()
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+psycopg://", 1)
        elif url.startswith("postgresql://") and not url.startswith("postgresql+"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url


settings = Settings()
