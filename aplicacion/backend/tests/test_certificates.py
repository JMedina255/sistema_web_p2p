import io
from datetime import UTC, datetime, timedelta

import PyPDF2
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import Base
from app.main import app
from app.models.bitacora import BitacoraPedagogica
from app.models.certificate import CertificadoHoras
from app.models.offer import SesionMentoria
from app.services.bitacora_service import _memory_bitacoras, clear_bitacoras_in_memory
from app.services.certificate_service import (
    CertificateService,
    clear_certificates_in_memory,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup():
    clear_certificates_in_memory()
    clear_bitacoras_in_memory()
    yield
    clear_certificates_in_memory()
    clear_bitacoras_in_memory()


def get_auth_header(email: str, roles: list[str]) -> dict[str, str]:
    token = create_access_token(data={"sub": email, "email": email, "roles": roles})
    return {"Authorization": f"Bearer {token}"}


def test_hours_summary_zero_and_partial_hours():
    mentor_email = "mentor.test@upt.pe"
    summary = CertificateService.get_hours_summary(db=None, mentor_email=mentor_email)
    assert summary.horas_visadas == 0.0
    assert summary.horas_pendientes == 0.0
    assert summary.umbral_requerido == 20.0
    assert summary.porcentaje_progreso == 0.0
    assert summary.es_elegible is False
    assert summary.horas_faltantes == 20.0
    assert summary.certificado_emitido is None

    # Simular 14.0 horas visadas y 4.0 pendientes en memoria
    _memory_bitacoras.append(
        {
            "id_bitacora": 101,
            "id_sesion": 501,
            "id_mentor": mentor_email,
            "horas_declaradas": 14.0,
            "visado_administrador": True,
        }
    )
    _memory_bitacoras.append(
        {
            "id_bitacora": 102,
            "id_sesion": 502,
            "id_mentor": mentor_email,
            "horas_declaradas": 4.0,
            "visado_administrador": False,
        }
    )

    summary2 = CertificateService.get_hours_summary(db=None, mentor_email=mentor_email)
    assert summary2.horas_visadas == 14.0
    assert summary2.horas_pendientes == 4.0
    assert summary2.porcentaje_progreso == 70.0
    assert summary2.es_elegible is False
    assert summary2.horas_faltantes == 6.0


def test_generate_certificate_rejected_if_insufficient_hours_400():
    mentor_email = "mentor.insuficiente@upt.pe"
    headers = get_auth_header(mentor_email, ["mentor"])

    # Simular solo 16.0 horas visadas (falta para el umbral de 20.0h según RN-14)
    _memory_bitacoras.append(
        {
            "id_bitacora": 201,
            "id_sesion": 601,
            "id_mentor": mentor_email,
            "horas_declaradas": 16.0,
            "visado_administrador": True,
        }
    )

    response = client.post(
        "/api/v1/certificates/generate",
        json={"periodo_academico": "2026-II"},
        headers=headers,
    )
    assert response.status_code == 400
    data = response.json()
    assert "INSUFFICIENT_ACCREDITED_HOURS" in data["detail"]
    assert "20.0" in data["detail"]


def test_generate_certificate_success_with_twenty_or_more_hours_201():
    mentor_email = "mentor.cumplido@upt.pe"
    headers = get_auth_header(mentor_email, ["mentor"])

    # Simular 22.0 horas visadas
    _memory_bitacoras.append(
        {
            "id_bitacora": 301,
            "id_sesion": 701,
            "id_mentor": mentor_email,
            "horas_declaradas": 22.0,
            "visado_administrador": True,
        }
    )

    response = client.post(
        "/api/v1/certificates/generate",
        json={"periodo_academico": "2026-II"},
        headers=headers,
    )
    assert response.status_code == 201
    cert = response.json()

    assert cert["id_mentor"] == mentor_email
    assert cert["periodo_academico"] == "2026-II"
    assert cert["horas_acreditadas"] == 22.0
    expected_estado = "EMITIDO_DEMO" if settings.ENABLE_DEMO_WATERMARK else "EMITIDO"
    assert cert["estado"] == expected_estado
    assert cert["codigo_folio"].startswith("CERT-2026-II-")
    assert len(cert["hash_firma"]) == 64
    assert f"folio={cert['codigo_folio']}" in cert["verification_url"]

    # Verificar que el resumen ahora reporte elegible y certificado_emitido
    sum_resp = client.get(
        f"/api/v1/certificates/summary?mentor_email={mentor_email}",
        headers=headers,
    )
    assert sum_resp.status_code == 200
    sum_data = sum_resp.json()
    assert sum_data["es_elegible"] is True
    assert sum_data["horas_visadas"] == 22.0
    assert sum_data["certificado_emitido"] is not None
    assert sum_data["certificado_emitido"]["codigo_folio"] == cert["codigo_folio"]


def test_generate_certificate_duplicate_rejected_409():
    mentor_email = "mentor.duplicado@upt.pe"
    headers = get_auth_header(mentor_email, ["mentor"])

    _memory_bitacoras.append(
        {
            "id_bitacora": 401,
            "id_sesion": 801,
            "id_mentor": mentor_email,
            "horas_declaradas": 24.0,
            "visado_administrador": True,
        }
    )

    # Primera emisión: exitosa
    r1 = client.post(
        "/api/v1/certificates/generate",
        json={"periodo_academico": "2026-II"},
        headers=headers,
    )
    assert r1.status_code == 201

    # Segunda emisión en el mismo semestre: conflicto 409
    r2 = client.post(
        "/api/v1/certificates/generate",
        json={"periodo_academico": "2026-II"},
        headers=headers,
    )
    assert r2.status_code == 409
    assert "DUPLICATE_CERTIFICATE_ISSUANCE" in r2.json()["detail"]


def test_download_certificate_pdf_binary_and_watermark_200(monkeypatch):
    monkeypatch.setattr(settings, "ENABLE_DEMO_WATERMARK", True)
    mentor_email = "mentor.pdf@upt.pe"
    headers = get_auth_header(mentor_email, ["mentor"])

    _memory_bitacoras.append(
        {
            "id_bitacora": 501,
            "id_sesion": 901,
            "id_mentor": mentor_email,
            "horas_declaradas": 20.0,
            "visado_administrador": True,
        }
    )

    gen_resp = client.post(
        "/api/v1/certificates/generate",
        json={"periodo_academico": "2026-II"},
        headers=headers,
    )
    assert gen_resp.status_code == 201
    cert_id = gen_resp.json()["id_certificado"]
    folio = gen_resp.json()["codigo_folio"]

    # Descargar binario PDF
    dl_resp = client.get(f"/api/v1/certificates/{cert_id}/download")
    assert dl_resp.status_code == 200
    assert dl_resp.headers["content-type"] == "application/pdf"
    assert f"Constancia_Mentoria_EPIS_2026_II_{folio}.pdf" in dl_resp.headers["content-disposition"]

    pdf_bytes = dl_resp.content
    assert pdf_bytes.startswith(b"%PDF-")

    # Extraer texto del PDF y validar marca de agua y folio
    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    page_text = reader.pages[0].extract_text()

    assert "DEMO - FINES ACADÉMICOS" in page_text
    assert folio in page_text
    assert "UNIVERSIDAD PRIVADA DE TACNA" in page_text
    assert "20.0 HORAS FORMATIVAS" in page_text
    assert "FIRMA CRIPTOGRÁFICA SHA-256:" in page_text


def test_verify_certificate_endpoint_public_200_and_404():
    mentor_email = "mentor.qr@upt.pe"
    headers = get_auth_header(mentor_email, ["mentor"])

    _memory_bitacoras.append(
        {
            "id_bitacora": 601,
            "id_sesion": 1001,
            "id_mentor": mentor_email,
            "horas_declaradas": 21.0,
            "visado_administrador": True,
        }
    )

    gen_resp = client.post(
        "/api/v1/certificates/generate",
        json={"periodo_academico": "2026-II"},
        headers=headers,
    )
    assert gen_resp.status_code == 201
    folio = gen_resp.json()["codigo_folio"]

    # 1. Consulta pública de validación de folio existente
    v_resp = client.get(f"/api/v1/certificates/verificar?folio={folio}")
    assert v_resp.status_code == 200
    v_data = v_resp.json()
    assert v_data["valido"] is True
    assert v_data["codigo_folio"] == folio
    assert v_data["id_mentor"] == mentor_email
    assert v_data["horas_acreditadas"] == 21.0
    expected_estado = "EMITIDO_DEMO" if settings.ENABLE_DEMO_WATERMARK else "EMITIDO"
    assert v_data["estado"] == expected_estado

    # 2. Folio inexistente -> 404
    bad_resp = client.get("/api/v1/certificates/verificar?folio=CERT-2026-II-9999")
    assert bad_resp.status_code == 404
    assert "CERTIFICATE_NOT_FOUND" in bad_resp.json()["detail"]


def test_certificates_rbac_and_admin_override():
    mentor_email = "mentor.regular@upt.pe"
    other_email = "otro.estudiante@upt.pe"
    admin_email = "admin.epis@upt.pe"

    mentor_headers = get_auth_header(mentor_email, ["mentor"])
    other_headers = get_auth_header(other_email, ["mentoreado"])
    admin_headers = get_auth_header(admin_email, ["administrador"])

    _memory_bitacoras.append(
        {
            "id_bitacora": 701,
            "id_sesion": 1101,
            "id_mentor": mentor_email,
            "horas_declaradas": 20.0,
            "visado_administrador": True,
        }
    )

    # Mentor titular consulta su propio resumen -> 200 OK
    r_mentor = client.get(
        "/api/v1/certificates/summary",
        headers=mentor_headers,
    )
    assert r_mentor.status_code == 200
    assert r_mentor.json()["horas_visadas"] == 20.0

    # Estudiante ajeno intenta consultar resumen del mentor -> 403 Forbidden
    r_forbidden = client.get(
        f"/api/v1/certificates/summary?mentor_email={mentor_email}",
        headers=other_headers,
    )
    assert r_forbidden.status_code == 403

    # Administrador consulta resumen de otro mentor -> 200 OK
    r_admin = client.get(
        f"/api/v1/certificates/summary?mentor_email={mentor_email}",
        headers=admin_headers,
    )
    assert r_admin.status_code == 200
    assert r_admin.json()["horas_visadas"] == 20.0

    # Usuario sin autenticación intenta emitir -> 401 Unauthorized
    r_unauth = client.post("/api/v1/certificates/generate")
    assert r_unauth.status_code == 401


def test_certificate_persistence_in_real_database():
    """Valida persistencia relacional y restricciones de integridad en BD SQLite/PostgreSQL."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionTest = sessionmaker(bind=engine)
    db = SessionTest()

    try:
        mentor = "mentor.db@upt.pe"
        now = datetime.now(UTC)

        # Crear 20 bitácoras visadas de 1 hora cada una (total = 20.0 h)
        for i in range(1, 21):
            s = SesionMentoria(
                id_sesion=2000 + i,
                codigo_sesion=f"SES-DB-{i}",
                mentor_email=mentor,
                id_asignatura=1,
                id_tema=1,
                fecha_inicio=now - timedelta(days=25 - i),
                duracion_minutos=60,
                modalidad="presencial",
                aforo_maximo=10,
                espacio_asignado="Lab 1",
                estado="HORAS_VISADAS",
            )
            db.add(s)
            db.commit()

            b = BitacoraPedagogica(
                id_sesion=2000 + i,
                id_mentor=mentor,
                temas_cubiertos=[1],
                observaciones="Sesión completada y auditada con excelencia pedagógica para acreditar horas formativas.",
                nivel_dificultad="Medio",
                hash_firma=f"hash_db_{i}",
                horas_declaradas=1.0,
                visado_administrador=True,
            )
            db.add(b)
        db.commit()

        # Comprobar resumen de horas en base de datos
        summary = CertificateService.get_hours_summary(db=db, mentor_email=mentor)
        assert summary.horas_visadas == 20.0
        assert summary.es_elegible is True

        # Emitir certificado persistiendo en la entidad CertificadoHoras
        cert_data, pdf_bytes = CertificateService.generate_certificate(
            db=db,
            mentor_email=mentor,
            periodo_academico="2026-II",
        )
        assert cert_data["id_certificado"] > 0
        assert cert_data["horas_acreditadas"] == 20.0
        assert len(pdf_bytes) > 1000

        # Verificar persistencia relacional
        cert_in_db = db.query(CertificadoHoras).filter(CertificadoHoras.id_mentor == mentor).first()
        assert cert_in_db is not None
        assert cert_in_db.codigo_folio == cert_data["codigo_folio"]
        assert cert_in_db.horas_acreditadas == 20.0

        # Verificar descarga y lectura desde BD
        pdf_out, fn = CertificateService.get_certificate_pdf(db=db, certificate_id=cert_in_db.id_certificado)
        assert len(pdf_out) > 1000
        assert cert_data["codigo_folio"] in fn

    finally:
        db.close()


def test_hours_boundary_19_99_rejected_and_20_00_accepted():
    """Valida casos de borde estrictos de la regla RN-14 (19.99h vs 20.00h sin fugas por redondeo)."""
    mentor_boundary = "mentor.boundary@upt.pe"
    headers = get_auth_header(mentor_boundary, ["mentor"])

    # Caso 1: 19.99 horas -> Rechazo estricto con HTTP 400
    _memory_bitacoras.append(
        {
            "id_bitacora": 901,
            "id_sesion": 1901,
            "id_mentor": mentor_boundary,
            "horas_declaradas": 19.99,
            "visado_administrador": True,
        }
    )

    s1 = CertificateService.get_hours_summary(db=None, mentor_email=mentor_boundary)
    assert s1.horas_visadas == 19.99
    assert s1.es_elegible is False
    assert s1.horas_faltantes == 0.01

    r_fail = client.post(
        "/api/v1/certificates/generate",
        json={"periodo_academico": "2026-II"},
        headers=headers,
    )
    assert r_fail.status_code == 400
    assert "INSUFFICIENT_ACCREDITED_HOURS" in r_fail.json()["detail"]

    # Caso 2: Se agrega 0.01h para alcanzar exactamente 20.00h -> Aprobación con HTTP 201
    _memory_bitacoras.append(
        {
            "id_bitacora": 902,
            "id_sesion": 1902,
            "id_mentor": mentor_boundary,
            "horas_declaradas": 0.01,
            "visado_administrador": True,
        }
    )

    s2 = CertificateService.get_hours_summary(db=None, mentor_email=mentor_boundary)
    assert s2.horas_visadas == 20.00
    assert s2.es_elegible is True
    assert s2.horas_faltantes == 0.0

    r_ok = client.post(
        "/api/v1/certificates/generate",
        json={"periodo_academico": "2026-II"},
        headers=headers,
    )
    assert r_ok.status_code == 201
    assert r_ok.json()["horas_acreditadas"] == 20.0


def test_concurrent_duplicate_generation_strictly_returns_409():
    """Valida que solicitudes concurrentes de emisión retornen exactamente un 201 y un 409 Conflict."""
    import concurrent.futures

    mentor_concurrent = "mentor.concurrent@upt.pe"
    headers = get_auth_header(mentor_concurrent, ["mentor"])

    _memory_bitacoras.append(
        {
            "id_bitacora": 950,
            "id_sesion": 1950,
            "id_mentor": mentor_concurrent,
            "horas_declaradas": 21.0,
            "visado_administrador": True,
        }
    )

    def send_request():
        return client.post(
            "/api/v1/certificates/generate",
            json={"periodo_academico": "2026-II"},
            headers=headers,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(send_request) for _ in range(4)]
        results = [f.result() for f in futures]

    status_codes = [r.status_code for r in results]
    assert status_codes.count(201) == 1
    assert status_codes.count(409) == 3


def test_pdf_contains_embedded_qr_image_stream():
    """Valida la incrustación física del stream de imagen QR en el documento PDF oficial."""
    mentor_email = "mentor.imgcheck@upt.pe"
    now = datetime.now(UTC)

    pdf_bytes = CertificateService.compile_pdf(
        mentor_name="Ingeniero Mentor",
        mentor_email=mentor_email,
        codigo_folio="CERT-2026-II-0042",
        periodo_academico="2026-II",
        horas_acreditadas=20.0,
        hash_firma="b" * 64,
        fecha_emision=now,
    )

    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    page = reader.pages[0]
    resources = page.get("/Resources", {})
    xobjects = resources.get("/XObject", {})
    if hasattr(xobjects, "get_object"):
        xobjects = xobjects.get_object()

    image_found = False
    for name in xobjects.keys():
        obj = xobjects[name].get_object()
        if obj.get("/Subtype") == "/Image":
            image_found = True
            assert obj.get("/Width") >= 100
            assert obj.get("/Height") >= 100
            assert obj.get("/ColorSpace") == "/DeviceRGB"

    assert image_found is True
