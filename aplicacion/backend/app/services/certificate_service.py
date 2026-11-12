import hashlib
import io
import threading
from datetime import UTC, datetime
from typing import Any

import qrcode
from fastapi import HTTPException, status
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.bitacora import BitacoraPedagogica
from app.models.certificate import CertificadoHoras
from app.models.profile import PerfilAcademico
from app.schemas.certificate import (
    CertificateMetaResponse,
    CertificateVerifyResponse,
    HoursSummaryResponse,
)
from app.services.bitacora_service import _bitacora_lock, _memory_bitacoras

_certificate_lock = threading.RLock()
_memory_certificates: list[dict[str, Any]] = []
_certificate_counter = 1


def clear_certificates_in_memory() -> None:
    """Helper para limpiar el almacén en memoria durante las pruebas unitarias."""
    global _certificate_counter
    with _certificate_lock:
        _memory_certificates.clear()
        _certificate_counter = 1


class CertificateService:
    """
    Motor de Generación y Persistencia de Constancias Oficiales de Mentoría DEMO (T-42 / T-44 / RF22 / RF23 / RN-14).
    - Valida umbral mínimo estricto de 20.0 horas visadas por Dirección (RN-14).
    - Emite folio correlativo institucional único: CERT-YYYY-SEM-XXXX.
    - Estampa marca de agua diagonal obligatoria: "DEMO - FINES ACADÉMICOS".
    - Inserta código QR vectorial de verificación institucional en alta resolución.
    - Sella criptográficamente el documento con hash SHA-256 inmutable.
    """

    DEFAULT_PERIOD = "2026-II"
    REQUIRED_HOURS_THRESHOLD = 20.0
    INSTITUTION_NAME = "Universidad Privada de Tacna"
    FACULTY_NAME = "Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas"

    @classmethod
    def _build_verification_url(cls, folio: str) -> str:
        return f"https://epis.upt.edu.pe/p2p/certificados/verificar?folio={folio}"

    @classmethod
    def get_hours_summary(
        cls,
        db: Session | None,
        mentor_email: str,
        periodo_academico: str = DEFAULT_PERIOD,
    ) -> HoursSummaryResponse:
        """
        Calcula el acumulado de horas de mentoría visadas y en revisión para un mentor,
        verificando la elegibilidad para solicitar la constancia institucional (RN-14).
        """
        clean_mentor = mentor_email.strip().lower()
        horas_visadas = 0.0
        horas_pendientes = 0.0

        # 1. Consulta en Base de Datos PostgreSQL / SQLite
        if db is not None:
            bitacoras_db = (
                db.query(BitacoraPedagogica).filter(BitacoraPedagogica.id_mentor.ilike(clean_mentor)).all()
            )
            for b in bitacoras_db:
                if b.visado_administrador:
                    horas_visadas += float(b.horas_declaradas)
                else:
                    horas_pendientes += float(b.horas_declaradas)

        # 2. Acumulación complementaria desde memoria si aplica
        with _bitacora_lock:
            for mb in _memory_bitacoras:
                if mb.get("id_mentor", "").strip().lower() == clean_mentor:
                    # Evitar duplicar si ya fue sumado desde la BD
                    if db is not None and any(
                        b.id_sesion == mb.get("id_sesion") for b in (bitacoras_db or [])
                    ):
                        continue
                    if mb.get("visado_administrador", False):
                        horas_visadas += float(mb.get("horas_declaradas", 0.0))
                    else:
                        horas_pendientes += float(mb.get("horas_declaradas", 0.0))

        horas_visadas = round(horas_visadas, 2)
        horas_pendientes = round(horas_pendientes, 2)
        progreso = min(100.0, round((horas_visadas / cls.REQUIRED_HOURS_THRESHOLD) * 100.0, 1))
        es_elegible = horas_visadas >= cls.REQUIRED_HOURS_THRESHOLD
        horas_faltantes = max(0.0, round(cls.REQUIRED_HOURS_THRESHOLD - horas_visadas, 2))

        # 3. Verificar si ya cuenta con constancia emitida en el periodo
        cert_emitido: CertificateMetaResponse | None = None
        if db is not None:
            c_db = (
                db.query(CertificadoHoras)
                .filter(
                    CertificadoHoras.id_mentor.ilike(clean_mentor),
                    CertificadoHoras.periodo_academico == periodo_academico,
                )
                .first()
            )
            if c_db:
                cert_emitido = CertificateMetaResponse(
                    id_certificado=c_db.id_certificado,
                    id_mentor=c_db.id_mentor,
                    codigo_folio=c_db.codigo_folio,
                    periodo_academico=c_db.periodo_academico,
                    horas_acreditadas=c_db.horas_acreditadas,
                    hash_firma=c_db.hash_firma,
                    estado=c_db.estado,
                    created_at=c_db.created_at.isoformat(),
                    verification_url=cls._build_verification_url(c_db.codigo_folio),
                )

        if cert_emitido is None:
            with _certificate_lock:
                for mc in _memory_certificates:
                    if (
                        mc.get("id_mentor", "").strip().lower() == clean_mentor
                        and mc.get("periodo_academico") == periodo_academico
                    ):
                        cert_emitido = CertificateMetaResponse(**mc)
                        break

        return HoursSummaryResponse(
            mentor_email=clean_mentor,
            horas_visadas=horas_visadas,
            horas_pendientes=horas_pendientes,
            umbral_requerido=cls.REQUIRED_HOURS_THRESHOLD,
            porcentaje_progreso=progreso,
            es_elegible=es_elegible,
            horas_faltantes=horas_faltantes,
            certificado_emitido=cert_emitido,
        )

    @classmethod
    def compile_pdf(
        cls,
        mentor_name: str,
        mentor_email: str,
        codigo_folio: str,
        periodo_academico: str,
        horas_acreditadas: float,
        hash_firma: str,
        fecha_emision: datetime,
    ) -> bytes:
        """
        Compila el documento oficial en formato PDF vectorial incorporando:
        - Membrete de la EPIS - Universidad Privada de Tacna.
        - Folio correlativo oficial.
        - Marca de agua diagonal "DEMO - FINES ACADÉMICOS".
        - Código QR vectorial de validación institucional.
        - Huella criptográfica SHA-256 al pie.
        """
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        page_width, page_height = letter

        # ---------------------------------------------------------------------
        # 1. Marca de agua diagonal "DEMO - FINES ACADÉMICOS" (Capa de fondo)
        # ---------------------------------------------------------------------
        c.saveState()
        c.setFont("Helvetica-Bold", 42)
        c.setFillColor(colors.Color(0.82, 0.82, 0.82, alpha=0.35))
        c.translate(page_width / 2.0, page_height / 2.0)
        c.rotate(45)
        c.drawCentredString(0, 0, "DEMO - FINES ACADÉMICOS")
        c.drawCentredString(0, -70, "USO EXCLUSIVO CÁTEDRA CS-I")
        c.restoreState()

        # ---------------------------------------------------------------------
        # 2. Marco perimetral institucional y orla decorativa
        # ---------------------------------------------------------------------
        c.setStrokeColor(colors.HexColor("#1C2A59"))
        c.setLineWidth(2.5)
        c.rect(36, 36, page_width - 72, page_height - 72)
        c.setStrokeColor(colors.HexColor("#C59B27"))  # Dorado institucional UPT
        c.setLineWidth(0.8)
        c.rect(40, 40, page_width - 80, page_height - 80)

        # ---------------------------------------------------------------------
        # 3. Encabezado y membrete oficial
        # ---------------------------------------------------------------------
        c.setFillColor(colors.HexColor("#1C2A59"))
        c.setFont("Helvetica-Bold", 17)
        c.drawCentredString(page_width / 2.0, page_height - 75, "UNIVERSIDAD PRIVADA DE TACNA")

        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor("#334155"))
        c.drawCentredString(page_width / 2.0, page_height - 92, cls.FACULTY_NAME)

        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawCentredString(
            page_width / 2.0,
            page_height - 106,
            "Programa Institucional de Mentorías Académicas entre Pares (EdRecSys P2P)",
        )

        c.setStrokeColor(colors.HexColor("#CBD5E1"))
        c.setLineWidth(1)
        c.line(60, page_height - 116, page_width - 60, page_height - 116)

        # ---------------------------------------------------------------------
        # 4. Folio correlativo y título principal
        # ---------------------------------------------------------------------
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor("#1C2A59"))
        c.drawRightString(page_width - 60, page_height - 134, f"FOLIO: {codigo_folio}")

        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(colors.HexColor("#1C2A59"))
        c.drawCentredString(page_width / 2.0, page_height - 170, "CONSTANCIA OFICIAL DE MENTORÍA")

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor("#C59B27"))
        c.drawCentredString(
            page_width / 2.0,
            page_height - 188,
            f"ACREDITACIÓN DE HORAS FORMATIVAS — PERIODO {periodo_academico}",
        )

        # ---------------------------------------------------------------------
        # 5. Cuerpo de certificación pedagógica
        # ---------------------------------------------------------------------
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor("#1E293B"))

        p1 = (
            "La Dirección de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de "
            "Tacna hace constar mediante el presente documento que el/la estudiante mentor(a):"
        )
        c.drawCentredString(page_width / 2.0, page_height - 230, p1)

        # Destacar al mentor titular
        c.setFont("Helvetica-Bold", 15)
        c.setFillColor(colors.HexColor("#1C2A59"))
        display_mentor = mentor_name if mentor_name and mentor_name != mentor_email else mentor_email
        c.drawCentredString(page_width / 2.0, page_height - 260, display_mentor.upper())

        c.setFont("Helvetica", 10)
        c.setFillColor(colors.HexColor("#475569"))
        c.drawCentredString(
            page_width / 2.0, page_height - 276, f"Identificador Institucional: {mentor_email}"
        )

        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor("#1E293B"))
        c.drawCentredString(
            page_width / 2.0,
            page_height - 310,
            "Ha cumplido con excelencia académica y compromiso formativo la labor de acompañamiento pedagógico,",
        )
        c.drawCentredString(
            page_width / 2.0,
            page_height - 326,
            "acumulando un volumen total de horas presenciales y virtuales visadas por la Escuela de:",
        )

        # Cuadro destacado con el total de horas
        c.setFillColor(colors.HexColor("#F1F5F9"))
        c.setStrokeColor(colors.HexColor("#CBD5E1"))
        c.roundRect((page_width / 2.0) - 160, page_height - 395, 320, 52, 6, fill=1, stroke=1)

        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(colors.HexColor("#1C2A59"))
        c.drawCentredString(page_width / 2.0, page_height - 370, f"{horas_acreditadas:.1f} HORAS FORMATIVAS")

        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawCentredString(
            page_width / 2.0,
            page_height - 387,
            "Horas debidamente auditadas con visado de Dirección de Escuela (Regla RN-14)",
        )

        # ---------------------------------------------------------------------
        # 6. Tabla resumida de especificaciones
        # ---------------------------------------------------------------------
        y_spec = page_height - 435
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.HexColor("#334155"))
        c.drawString(70, y_spec, "Período Lectivo:")
        c.setFont("Helvetica", 9)
        c.drawString(160, y_spec, periodo_academico)

        c.setFont("Helvetica-Bold", 9)
        c.drawString(330, y_spec, "Estado Oficial:")
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.HexColor("#0284C7"))
        c.drawString(420, y_spec, "EMITIDO_DEMO (Acreditado)")

        y_spec -= 18
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.HexColor("#334155"))
        c.drawString(70, y_spec, "Fecha de Emisión:")
        c.setFont("Helvetica", 9)
        c.drawString(160, y_spec, fecha_emision.strftime("%d/%m/%Y %H:%M:%S UTC"))

        c.setFont("Helvetica-Bold", 9)
        c.drawString(330, y_spec, "Umbral Reglamentario:")
        c.setFont("Helvetica", 9)
        c.drawString(450, y_spec, f">= {cls.REQUIRED_HOURS_THRESHOLD:.1f} h (Superado)")

        # ---------------------------------------------------------------------
        # 7. Código QR Vectorial de Validación Institucional (Esquina Inferior Izquierda)
        # ---------------------------------------------------------------------
        verification_url = cls._build_verification_url(codigo_folio)
        qr = qrcode.QRCode(box_size=4, border=1)
        qr.add_data(verification_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        qr_buf = io.BytesIO()
        qr_img.save(qr_buf, format="PNG")
        qr_buf.seek(0)

        c.drawImage(ImageReader(qr_buf), 65, 75, width=90, height=90)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#1C2A59"))
        c.drawString(65, 65, "Escanear para verificar autenticidad")
        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawString(65, 55, "epis.upt.edu.pe/p2p/certificados")

        # ---------------------------------------------------------------------
        # 8. Firmas de Cátedra y Dirección de Escuela (Esquina Inferior Derecha)
        # ---------------------------------------------------------------------
        x_sig1 = page_width - 200
        c.setStrokeColor(colors.HexColor("#94A3B8"))
        c.setLineWidth(1)
        c.line(x_sig1 - 30, 115, x_sig1 + 140, 115)

        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(colors.HexColor("#1C2A59"))
        c.drawCentredString(x_sig1 + 55, 102, "Dr. Ricardo E. Valcárcel Alvarado")
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#475569"))
        c.drawCentredString(x_sig1 + 55, 90, "Docente de Cátedra — Construcción de Software I")
        c.drawCentredString(x_sig1 + 55, 80, "Dirección EPIS — Facultad de Ingeniería UPT")

        # ---------------------------------------------------------------------
        # 9. Sello Criptográfico SHA-256 de Integridad (Pie de página inmutable)
        # ---------------------------------------------------------------------
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.setLineWidth(0.5)
        c.line(60, 48, page_width - 60, 48)

        c.setFont("Courier-Bold", 6.5)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawCentredString(
            page_width / 2.0,
            41,
            f"FIRMA CRIPTOGRÁFICA SHA-256: {hash_firma}",
        )

        c.showPage()
        c.save()
        buf.seek(0)
        return buf.getvalue()

    @classmethod
    def generate_certificate(
        cls,
        db: Session | None,
        mentor_email: str,
        periodo_academico: str = DEFAULT_PERIOD,
        caller_email: str | None = None,
        is_admin: bool = False,
        now_utc: datetime | None = None,
    ) -> tuple[dict[str, Any], bytes]:
        """
        Emite formalmente la constancia de acreditación en formato PDF y registra en persistencia (T-42 / T-44).
        - Verifica titularidad del mentor o permisos de administrador.
        - Exige umbral mínimo de 20.0 horas visadas (RN-14).
        - Impide doble emisión en el mismo semestre (409 Conflict).
        """
        if now_utc is None:
            now_utc = datetime.now(UTC)

        clean_mentor = mentor_email.strip().lower()
        clean_caller = (caller_email or "").strip().lower()

        # 1. Control de autorización
        if clean_caller and not is_admin and clean_caller != clean_mentor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="FORBIDDEN: Solo el mentor titular o un administrador pueden emitir esta constancia.",
            )

        # 2. Resumen de horas y validación de regla RN-14
        summary = cls.get_hours_summary(db, clean_mentor, periodo_academico)
        if not summary.es_elegible:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"INSUFFICIENT_ACCREDITED_HOURS: No cumples con el umbral mínimo de {cls.REQUIRED_HOURS_THRESHOLD:.1f} "
                    f"horas visadas para emitir la constancia (acumulas {summary.horas_visadas:.1f} h, faltan {summary.horas_faltantes:.1f} h)."
                ),
            )

        # 3. Control de no duplicidad de constancias por período
        if summary.certificado_emitido is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="DUPLICATE_CERTIFICATE_ISSUANCE: Ya se encuentra emitida tu constancia institucional para este período académico.",
            )

        # 4. Generación de folio correlativo único y persistencia con cerrojo
        with _certificate_lock:
            # Re-verificar no duplicidad dentro del candado crítico para prevenir carreras de hilos
            if db is not None:
                c_db_dup = (
                    db.query(CertificadoHoras)
                    .filter(
                        CertificadoHoras.id_mentor.ilike(clean_mentor),
                        CertificadoHoras.periodo_academico == periodo_academico,
                    )
                    .first()
                )
                if c_db_dup:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="DUPLICATE_CERTIFICATE_ISSUANCE: Ya se encuentra emitida tu constancia institucional para este período académico.",
                    )

            for mc in _memory_certificates:
                if (
                    mc.get("id_mentor", "").strip().lower() == clean_mentor
                    and mc.get("periodo_academico") == periodo_academico
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="DUPLICATE_CERTIFICATE_ISSUANCE: Ya se encuentra emitida tu constancia institucional para este período académico.",
                    )

            # Contar certificados existentes en DB y memoria para el periodo
            total_existing = 0
            if db is not None:
                try:
                    total_existing = (
                        db.query(CertificadoHoras)
                        .filter(CertificadoHoras.periodo_academico == periodo_academico)
                        .count()
                    )
                except Exception:
                    total_existing = 0

            mem_count = sum(
                1 for c in _memory_certificates if c.get("periodo_academico") == periodo_academico
            )
            next_correlative = max(total_existing, mem_count) + 1

            # Garantizar que el folio no colisione con folios preexistentes
            while True:
                codigo_folio = f"CERT-{periodo_academico}-{next_correlative:04d}"
                folio_in_mem = any(c.get("codigo_folio") == codigo_folio for c in _memory_certificates)
                folio_in_db = False
                if db is not None:
                    try:
                        folio_in_db = (
                            db.query(CertificadoHoras)
                            .filter(CertificadoHoras.codigo_folio == codigo_folio)
                            .first()
                            is not None
                        )
                    except Exception:
                        folio_in_db = False
                if not folio_in_mem and not folio_in_db:
                    break
                next_correlative += 1

            # 5. Cálculo de firma criptográfica SHA-256
            raw_canonical = f"{clean_mentor}:{summary.horas_visadas:.2f}:{codigo_folio}:{now_utc.isoformat()}"
            hash_firma = hashlib.sha256(raw_canonical.encode("utf-8")).hexdigest()

            # 6. Obtener nombres del mentor si existen en perfiles
            mentor_display_name = clean_mentor
            if db is not None:
                try:
                    p = db.query(PerfilAcademico).filter(PerfilAcademico.email.ilike(clean_mentor)).first()
                    if p and p.nombres:
                        mentor_display_name = f"{p.nombres} {p.apellidos or ''}".strip()
                except Exception:
                    pass

            # 7. Compilar PDF oficial
            pdf_bytes = cls.compile_pdf(
                mentor_name=mentor_display_name,
                mentor_email=clean_mentor,
                codigo_folio=codigo_folio,
                periodo_academico=periodo_academico,
                horas_acreditadas=summary.horas_visadas,
                hash_firma=hash_firma,
                fecha_emision=now_utc,
            )

            # 8. Persistencia relacional en base de datos con manejo atómico de IntegrityError
            global _certificate_counter
            cert_id = _certificate_counter
            _certificate_counter += 1

            if db is not None:
                try:
                    cert_orm = CertificadoHoras(
                        id_mentor=clean_mentor,
                        codigo_folio=codigo_folio,
                        periodo_academico=periodo_academico,
                        horas_acreditadas=summary.horas_visadas,
                        hash_firma=hash_firma,
                        estado="EMITIDO_DEMO",
                        created_at=now_utc,
                    )
                    db.add(cert_orm)
                    db.commit()
                    db.refresh(cert_orm)
                    cert_id = cert_orm.id_certificado
                except IntegrityError as err:
                    db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="DUPLICATE_CERTIFICATE_ISSUANCE: Ya se encuentra emitida tu constancia institucional para este período académico.",
                    ) from err

            # Almacenar en memoria
            cert_dict = {
                "id_certificado": cert_id,
                "id_mentor": clean_mentor,
                "codigo_folio": codigo_folio,
                "periodo_academico": periodo_academico,
                "horas_acreditadas": summary.horas_visadas,
                "hash_firma": hash_firma,
                "estado": "EMITIDO_DEMO",
                "created_at": now_utc.isoformat(),
                "verification_url": cls._build_verification_url(codigo_folio),
                "pdf_bytes": pdf_bytes,
                "mentor_name": mentor_display_name,
            }
            _memory_certificates.append(cert_dict)

            return cert_dict, pdf_bytes

    @classmethod
    def get_certificate_by_id(cls, db: Session | None, certificate_id: int) -> dict[str, Any]:
        """Recupera los metadatos de un certificado por ID."""
        if db is not None:
            c = db.query(CertificadoHoras).filter(CertificadoHoras.id_certificado == certificate_id).first()
            if c:
                return {
                    "id_certificado": c.id_certificado,
                    "id_mentor": c.id_mentor,
                    "codigo_folio": c.codigo_folio,
                    "periodo_academico": c.periodo_academico,
                    "horas_acreditadas": c.horas_acreditadas,
                    "hash_firma": c.hash_firma,
                    "estado": c.estado,
                    "created_at": c.created_at.isoformat(),
                    "verification_url": cls._build_verification_url(c.codigo_folio),
                }

        with _certificate_lock:
            for mc in _memory_certificates:
                if mc.get("id_certificado") == certificate_id:
                    return {
                        "id_certificado": mc["id_certificado"],
                        "id_mentor": mc["id_mentor"],
                        "codigo_folio": mc["codigo_folio"],
                        "periodo_academico": mc["periodo_academico"],
                        "horas_acreditadas": mc["horas_acreditadas"],
                        "hash_firma": mc["hash_firma"],
                        "estado": mc["estado"],
                        "created_at": mc["created_at"],
                        "verification_url": mc["verification_url"],
                    }

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CERTIFICATE_NOT_FOUND: La constancia solicitada no fue encontrada en el repositorio institucional.",
        )

    @classmethod
    def get_certificate_pdf(cls, db: Session | None, certificate_id: int) -> tuple[bytes, str]:
        """
        Recupera o recompila el binario PDF de la constancia garantizando coincidencia estricta de hash.
        """
        # 1. Buscar en memoria primero (si ya está compilado el binario)
        with _certificate_lock:
            for mc in _memory_certificates:
                if mc.get("id_certificado") == certificate_id and "pdf_bytes" in mc:
                    folio = mc["codigo_folio"]
                    filename = f"Constancia_Mentoria_EPIS_2026_II_{folio}.pdf"
                    return mc["pdf_bytes"], filename

        # 2. Si solo está en base de datos, recompilarlo con datos idénticos
        if db is not None:
            c = db.query(CertificadoHoras).filter(CertificadoHoras.id_certificado == certificate_id).first()
            if c:
                mentor_name = c.id_mentor
                try:
                    p = db.query(PerfilAcademico).filter(PerfilAcademico.email.ilike(c.id_mentor)).first()
                    if p and p.nombres:
                        mentor_name = f"{p.nombres} {p.apellidos or ''}".strip()
                except Exception:
                    pass

                pdf_bytes = cls.compile_pdf(
                    mentor_name=mentor_name,
                    mentor_email=c.id_mentor,
                    codigo_folio=c.codigo_folio,
                    periodo_academico=c.periodo_academico,
                    horas_acreditadas=c.horas_acreditadas,
                    hash_firma=c.hash_firma,
                    fecha_emision=c.created_at,
                )
                filename = f"Constancia_Mentoria_EPIS_2026_II_{c.codigo_folio}.pdf"
                return pdf_bytes, filename

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CERTIFICATE_NOT_FOUND: La constancia solicitada no fue encontrada en el repositorio institucional.",
        )

    @classmethod
    def verify_certificate_by_folio(cls, db: Session | None, folio: str) -> CertificateVerifyResponse:
        """
        Endpoint público institucional de auditoría y verificación por código QR (CUS09 / RF23).
        """
        clean_folio = folio.strip().upper()

        # 1. Base de datos
        if db is not None:
            c = db.query(CertificadoHoras).filter(CertificadoHoras.codigo_folio == clean_folio).first()
            if c:
                return CertificateVerifyResponse(
                    valido=True,
                    codigo_folio=c.codigo_folio,
                    id_mentor=c.id_mentor,
                    periodo_academico=c.periodo_academico,
                    horas_acreditadas=c.horas_acreditadas,
                    hash_firma=c.hash_firma,
                    estado=c.estado,
                    fecha_emision=c.created_at.isoformat(),
                    mensaje="Constancia de mentoría auténtica, vigente y acreditada por la EPIS-UPT.",
                )

        # 2. Almacén en memoria
        with _certificate_lock:
            for mc in _memory_certificates:
                if mc.get("codigo_folio", "").strip().upper() == clean_folio:
                    return CertificateVerifyResponse(
                        valido=True,
                        codigo_folio=mc["codigo_folio"],
                        id_mentor=mc["id_mentor"],
                        periodo_academico=mc["periodo_academico"],
                        horas_acreditadas=mc["horas_acreditadas"],
                        hash_firma=mc["hash_firma"],
                        estado=mc["estado"],
                        fecha_emision=mc["created_at"],
                        mensaje="Constancia de mentoría auténtica, vigente y acreditada por la EPIS-UPT.",
                    )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CERTIFICATE_NOT_FOUND: El folio '{clean_folio}' no corresponde a ninguna constancia válida emitida.",
        )
