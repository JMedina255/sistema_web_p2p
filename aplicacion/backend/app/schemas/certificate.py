from pydantic import BaseModel, ConfigDict, Field


class CertificateMetaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_certificado: int = Field(..., description="Identificador correlativo del certificado emitido")
    id_mentor: str = Field(..., description="Correo institucional del mentor acreditado")
    codigo_folio: str = Field(..., description="Folio institucional único con formato CERT-YYYY-SEM-XXXX")
    periodo_academico: str = Field(..., description="Semestre lectivo de la mentoría (ej. 2026-II)")
    horas_acreditadas: float = Field(
        ..., ge=20.0, description="Total de horas visadas acumuladas (mínimo 20h)"
    )
    hash_firma: str = Field(..., description="Huella criptográfica SHA-256 de autenticidad")
    estado: str = Field(default="EMITIDO_DEMO", description="Estado institucional del documento emitido")
    created_at: str = Field(..., description="Fecha y hora de expedición en formato ISO 8601")
    verification_url: str = Field(..., description="URL institucional pública para validación por código QR")


class HoursSummaryResponse(BaseModel):
    mentor_email: str = Field(..., description="Correo del estudiante mentor consultado")
    horas_visadas: float = Field(..., description="Horas de mentoría con bitácora aprobada por la Escuela")
    horas_pendientes: float = Field(..., description="Horas en revisión provisional pendientes de visado")
    umbral_requerido: float = Field(default=20.0, description="Meta reglamentaria mínima de horas (RN-14)")
    porcentaje_progreso: float = Field(
        ..., ge=0.0, le=100.0, description="Porcentaje de avance hacia el umbral de 20h"
    )
    es_elegible: bool = Field(..., description="Indica si el mentor cumple con las >= 20.0 horas visadas")
    horas_faltantes: float = Field(
        ..., ge=0.0, description="Horas que restan para alcanzar la meta reglamentaria"
    )
    certificado_emitido: CertificateMetaResponse | None = Field(
        default=None, description="Metadatos de constancia si ya fue emitida en el periodo"
    )


class CertificateGenerateRequest(BaseModel):
    periodo_academico: str = Field(default="2026-II", description="Periodo académico para la constancia")
    mentor_email: str | None = Field(
        default=None, description="Correo opcional si es invocado por administrador"
    )


class CertificateVerifyResponse(BaseModel):
    valido: bool = Field(..., description="Indica si la constancia y folio son auténticos y vigentes")
    codigo_folio: str = Field(..., description="Código de folio institucional verificado")
    id_mentor: str = Field(..., description="Correo institucional del mentor titular")
    periodo_academico: str = Field(..., description="Periodo académico acreditado")
    horas_acreditadas: float = Field(..., description="Total de horas formativas acreditadas")
    hash_firma: str = Field(..., description="Huella SHA-256 de integridad institucional")
    estado: str = Field(..., description="Estado de la constancia (EMITIDO_DEMO)")
    fecha_emision: str = Field(..., description="Fecha de expedición registrada")
    institucion: str = Field(
        default="Universidad Privada de Tacna - Escuela Profesional de Ingeniería de Sistemas",
        description="Entidad emisora",
    )
    mensaje: str = Field(..., description="Dictamen oficial de verificación")
