from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_optional_session, get_required_session
from app.schemas.certificate import (
    CertificateGenerateRequest,
    CertificateMetaResponse,
    CertificateVerifyResponse,
    HoursSummaryResponse,
)
from app.services.certificate_service import CertificateService

router = APIRouter()


@router.get(
    "/summary",
    response_model=HoursSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar resumen de horas formativas y progreso de certificación (T-43 / RF22 / RN-14)",
)
def get_certificate_hours_summary(
    mentor_email: str | None = Query(None, description="Correo del estudiante mentor a consultar"),
    periodo_academico: str = Query("2026-II", description="Periodo académico de evaluación"),
    authorization: Annotated[str | None, Header()] = None,
    db: Session | None = Depends(get_optional_session),
) -> HoursSummaryResponse:
    """
    Retorna el estado de acreditación de horas del estudiante mentor:
    - Total de horas visadas con bitácora aprobada por Dirección.
    - Horas provisionales en revisión.
    - Avance porcentual hacia las 20.0 horas reglamentarias (RN-14).
    - Metadatos de constancia emitida si ya cuenta con una en el semestre.
    """
    target_email = mentor_email

    if authorization:
        user = get_current_user(authorization)
        if mentor_email and mentor_email.strip().lower() != user.email.strip().lower():
            if not user.is_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="FORBIDDEN: Solo el mentor titular o un administrador pueden consultar el resumen de horas.",
                )
            target_email = mentor_email
        else:
            target_email = user.email
    elif not target_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere autenticación o especificar el correo del mentor.",
        )

    return CertificateService.get_hours_summary(
        db=db,
        mentor_email=target_email,
        periodo_academico=periodo_academico,
    )


@router.post(
    "/generate",
    response_model=CertificateMetaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Emitir constancia oficial de mentoría DEMO con QR y hash SHA-256 (T-42 / T-44 / RF22 / RN-14)",
)
def generate_mentor_certificate(
    payload: CertificateGenerateRequest | None = None,
    authorization: Annotated[str | None, Header()] = None,
    db: Session | None = Depends(get_required_session),
) -> CertificateMetaResponse:
    """
    Compila y emite la constancia oficial de mentoría académica en formato PDF:
    - Valida obligatoriamente que el mentor acumule >= 20.0 horas visadas (RN-14).
    - Asigna folio correlativo único institucional: CERT-YYYY-SEM-XXXX.
    - Estampa marca de agua diagonal obligatoria 'DEMO - FINES ACADÉMICOS'.
    - Inserta código QR de validación institucional y huella SHA-256.
    - Registra la expedición en la tabla relacional 'certificados_horas'.
    """
    user = get_current_user(authorization)

    target_email = user.email
    periodo = payload.periodo_academico if payload and payload.periodo_academico else "2026-II"

    if (
        payload
        and payload.mentor_email
        and payload.mentor_email.strip().lower() != user.email.strip().lower()
    ):
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="FORBIDDEN: Solo un administrador puede emitir constancias para otro mentor.",
            )
        target_email = payload.mentor_email

    cert_dict, _ = CertificateService.generate_certificate(
        db=db,
        mentor_email=target_email,
        periodo_academico=periodo,
        caller_email=user.email,
        is_admin=user.is_admin,
    )

    return CertificateMetaResponse(**cert_dict)


@router.get(
    "/verificar",
    response_model=CertificateVerifyResponse,
    status_code=status.HTTP_200_OK,
    summary="Verificar autenticidad institucional de constancia por folio o código QR (CUS09 / RF23)",
)
def verify_certificate_by_folio(
    folio: str = Query(..., description="Código de folio institucional a verificar (ej. CERT-2026-II-0001)"),
    db: Session | None = Depends(get_optional_session),
) -> CertificateVerifyResponse:
    """
    Endpoint público de consulta para validar constancias oficiales emitidas por la EPIS-UPT.
    """
    return CertificateService.verify_certificate_by_folio(db=db, folio=folio)


@router.get(
    "/{id_certificado}/download",
    status_code=status.HTTP_200_OK,
    summary="Descargar binario PDF de la constancia oficial emitida (T-42 / RF23 / CUS18)",
)
def download_certificate_pdf(
    id_certificado: int,
    db: Session | None = Depends(get_optional_session),
) -> Response:
    """
    Entrega el stream binario de la constancia en formato application/pdf con cabeceras de descarga.
    """
    pdf_bytes, filename = CertificateService.get_certificate_pdf(db=db, certificate_id=id_certificado)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": "application/pdf",
        },
    )


@router.get(
    "/{id_certificado}",
    response_model=CertificateMetaResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar metadatos de una constancia emitida por su ID (T-44 / RF23)",
)
def get_certificate_details(
    id_certificado: int,
    db: Session | None = Depends(get_optional_session),
) -> CertificateMetaResponse:
    """Recupera los metadatos institucionales de una constancia por su identificador."""
    cert_data = CertificateService.get_certificate_by_id(db=db, certificate_id=id_certificado)
    return CertificateMetaResponse(**cert_data)
