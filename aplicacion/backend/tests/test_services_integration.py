"""
Pruebas de Integración y Casos de Borde para Servicios Externos (Punto 1 / T-42 / T-44 / T-50).
Valida:
- Emisión de constancias oficiales limpias (estado 'EMITIDO' sin marca de agua DEMO) cuando ENABLE_DEMO_WATERMARK=False.
- Persistencia del archivo PDF generado en StorageService y recuperación binaria.
- Vinculación de recursos académicos en ResourceService con persistencia física en StorageService.
- Ciclo de vida y cancelación limpia de la corrutina _quorum_scheduler_loop en app.main.
"""

import asyncio
import io
from unittest.mock import MagicMock

import PyPDF2
import pytest

from app.core.config import settings
from app.main import _quorum_scheduler_loop
from app.services.bitacora_service import _bitacora_lock, _memory_bitacoras
from app.services.booking_service import BookingService
from app.services.certificate_service import (
    CertificateService,
    clear_certificates_in_memory,
)
from app.services.resource_service import ResourceService
from app.services.storage_service import StorageService


@pytest.fixture(autouse=True)
def clean_state():
    clear_certificates_in_memory()
    with _bitacora_lock:
        _memory_bitacoras.clear()
    ResourceService.limpiar_almacen_memoria()
    yield
    clear_certificates_in_memory()
    with _bitacora_lock:
        _memory_bitacoras.clear()
    ResourceService.limpiar_almacen_memoria()


def test_certificate_official_emission_without_watermark_when_watermark_disabled(monkeypatch):
    """
    Cuando ENABLE_DEMO_WATERMARK es False:
    - El PDF compilado no contiene la marca de agua 'DEMO - FINES ACADÉMICOS'.
    - El estado registrado en la constancia es 'EMITIDO'.
    - El PDF binario se persiste físicamente mediante StorageService.
    """
    monkeypatch.setattr(settings, "ENABLE_DEMO_WATERMARK", False)
    monkeypatch.setattr(settings, "STORAGE_LOCAL_DIR", "uploads_test_clean")

    mentor_email = "mentor.titular@upt.pe"

    # Simular 22 horas visadas en bitácoras (supera el umbral de 20h RN-14)
    with _bitacora_lock:
        _memory_bitacoras.append(
            {
                "id_bitacora": 1,
                "id_sesion": 101,
                "id_mentor": mentor_email,
                "horas_declaradas": 22.0,
                "visado_administrador": True,
            }
        )

    cert_dict, pdf_bytes = CertificateService.issue_certificate(
        db=None,
        mentor_email=mentor_email,
        periodo_academico="2026-II",
        caller_email=mentor_email,
    )

    # 1. Estado oficial EMITIDO
    assert cert_dict["estado"] == "EMITIDO"
    folio = cert_dict["codigo_folio"]

    # 2. Persistencia en StorageService
    assert StorageService.file_exists(settings.SUPABASE_BUCKET_CERTIFICATES, f"{folio}.pdf") is True
    retrieved_bytes, filename = CertificateService.get_certificate_pdf(None, cert_dict["id_certificado"])
    assert retrieved_bytes == pdf_bytes
    assert folio in filename

    # 3. Inspeccionar texto del PDF compilado mediante PyPDF2 / pypdf
    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    full_text = "".join(page.extract_text() or "" for page in reader.pages)
    assert "DEMO - FINES ACADÉMICOS" not in full_text
    assert "UNIVERSIDAD PRIVADA DE TACNA" in full_text
    assert "EMITIDO" in full_text

    # Limpiar archivo temporal
    StorageService.delete_file(settings.SUPABASE_BUCKET_CERTIFICATES, f"{folio}.pdf")


def test_certificate_demo_emission_with_watermark_when_watermark_enabled(monkeypatch):
    """
    Cuando ENABLE_DEMO_WATERMARK es True:
    - El PDF compilado contiene la marca de agua 'DEMO - FINES ACADÉMICOS'.
    - El estado registrado en la constancia es 'EMITIDO_DEMO'.
    """
    monkeypatch.setattr(settings, "ENABLE_DEMO_WATERMARK", True)
    monkeypatch.setattr(settings, "STORAGE_LOCAL_DIR", "uploads_test_clean")

    mentor_email = "mentor.demo@upt.pe"

    with _bitacora_lock:
        _memory_bitacoras.append(
            {
                "id_bitacora": 2,
                "id_sesion": 102,
                "id_mentor": mentor_email,
                "horas_declaradas": 20.0,
                "visado_administrador": True,
            }
        )

    cert_dict, pdf_bytes = CertificateService.issue_certificate(
        db=None,
        mentor_email=mentor_email,
        periodo_academico="2026-II",
        caller_email=mentor_email,
    )

    assert cert_dict["estado"] == "EMITIDO_DEMO"
    folio = cert_dict["codigo_folio"]

    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    full_text = "".join(page.extract_text() or "" for page in reader.pages)
    assert "DEMO - FINES ACADÉMICOS" in full_text

    StorageService.delete_file(settings.SUPABASE_BUCKET_CERTIFICATES, f"{folio}.pdf")


def test_resource_service_physical_storage_persistence(monkeypatch):
    """
    Verifica que al asociar un recurso documental con bytes:
    - Se persista en disco mediante StorageService en lugar de mantener bytes en memoria RAM.
    """
    monkeypatch.setattr(settings, "STORAGE_LOCAL_DIR", "uploads_test_clean")

    content = b"PDF-ACADEMIC-RESOURCES-CONTENT-BYTES-STREAM"
    result = ResourceService.asociar_recurso_a_sesion(
        id_sesion=99,
        mentor_email="mentor.rec@upt.pe",
        nombre_recurso="Guia_Semana_08.pdf",
        content=content,
        descripcion="Material oficial de práctica",
    )

    assert result["status"] == "VINCULADO_EXITOSAMENTE"
    assert result["tamano_bytes"] == len(content)

    # Verificar que el archivo existe en el bucket de recursos
    safe_name = "sesion_99_Guia_Semana_08.pdf"
    assert StorageService.file_exists(settings.SUPABASE_BUCKET_RESOURCES, safe_name) is True

    stored = StorageService.get_file(settings.SUPABASE_BUCKET_RESOURCES, safe_name)
    assert stored == content

    StorageService.delete_file(settings.SUPABASE_BUCKET_RESOURCES, safe_name)


@pytest.mark.anyio
async def test_quorum_scheduler_loop_lifecycle(monkeypatch):
    """
    Verifica que la corrutina en segundo plano _quorum_scheduler_loop:
    - Ejecute BookingService.evaluate_quorum_for_all_active_sessions.
    - Se cancele limpiamente al recibir CancelledError.
    """
    monkeypatch.setattr(settings, "SCHEDULER_INTERVAL_MINUTES", 0.0001)  # Intervalo ínfimo para la prueba

    mock_eval = MagicMock(return_value=[])
    monkeypatch.setattr(BookingService, "evaluate_quorum_for_all_active_sessions", mock_eval)

    # Lanzar la tarea y esperar un ciclo breve
    task = asyncio.create_task(_quorum_scheduler_loop())
    await asyncio.sleep(0.05)

    # Cancelar la tarea
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    assert task.done() is True
    assert mock_eval.called


def test_booking_confirmation_triggers_email_notification(monkeypatch):
    """
    Verifica que al ratificar la asistencia a una reserva (confirm_attendance):
    - Se invoque EmailService.send_session_confirmation_email con los detalles de recinto y sesión.
    """
    from datetime import UTC, datetime, timedelta

    from app.services.booking_service import _booking_lock, _memory_bookings
    from app.services.email_service import EmailService

    mock_send = MagicMock(return_value=True)
    monkeypatch.setattr(EmailService, "send_session_confirmation_email", mock_send)

    now = datetime.now(UTC)
    with _booking_lock:
        _memory_bookings.append(
            {
                "id_reserva": 8888,
                "codigo_reserva": "RES-8888",
                "id_sesion": 55,
                "codigo_sesion": "SES-55",
                "estudiante_email": "estudiante.test@upt.pe",
                "estado": "PENDIENTE_CONFIRMACION",
                "fecha_reserva": (now - timedelta(hours=2)).isoformat(),
                "fecha_ratificacion": None,
                "motivo_cancelacion": None,
                "ticket_hash": "hash8888",
                "fecha_inicio": (now + timedelta(hours=48)).isoformat(),
                "nombre_asignatura": "Algoritmos",
                "nombre_tema": "Grafos",
                "duracion_minutos": 90,
                "modalidad": "virtual",
                "espacio_asignado": "https://meet.google.com/upt-ses55-abcd",
                "mentor_email": "mentor.test@upt.pe",
            }
        )

    res = BookingService.confirm_attendance(
        db=None,
        id_reserva=8888,
        caller_email="estudiante.test@upt.pe",
    )
    assert res.estado == "CONFIRMADA"
    mock_send.assert_called_once()
    _, kwargs = mock_send.call_args
    assert kwargs["to_email"] == "estudiante.test@upt.pe"
    assert kwargs["session_code"] == "SES-55"
    assert "https://meet.google.com/upt-ses55-abcd" in kwargs["room_or_link"]


def test_quorum_failure_at_t24_triggers_email_alert(monkeypatch):
    """
    Verifica que cuando BookingService evalúa una sesión en T-24h y no alcanza el quórum:
    - Se invoque EmailService.send_quorum_alert_email alertando al mentor.
    """
    from datetime import UTC, datetime, timedelta

    from app.services.booking_service import _booking_lock
    from app.services.email_service import EmailService
    from app.services.offer_service import _memory_offers

    mock_alert = MagicMock(return_value=True)
    monkeypatch.setattr(EmailService, "send_quorum_alert_email", mock_alert)

    now = datetime.now(UTC)
    session_start = now + timedelta(hours=20)  # Dentro de la ventana perentoria T-24h

    with _booking_lock:
        _memory_offers.append(
            {
                "id_sesion": 7777,
                "codigo_sesion": "SES-7777",
                "id_asignatura": 1,
                "nombre_asignatura": "Cálculo I",
                "nombre_tema": "Límites",
                "fecha_inicio": session_start.isoformat(),
                "duracion_minutos": 60,
                "modalidad": "virtual",
                "aforo_maximo": 20,
                "espacio_asignado": "https://meet.google.com/upt-ses7777-1234",
                "mentor_email": "mentor.titular@upt.pe",
                "mentor_nombre": "Prof. Test",
                "estado": "PUBLICADA",
                "quorumevaluated_at": None,
            }
        )

    res = BookingService.evaluate_session_quorum(db=None, id_sesion=7777, now_utc=now)
    assert res.estado_sesion == "QUORUM_INSUFICIENTE"
    mock_alert.assert_called_once()
    _, kwargs = mock_alert.call_args
    assert kwargs["to_email"] == "mentor.titular@upt.pe"
    assert kwargs["session_code"] == "SES-7777"
    assert kwargs["confirmed_students"] == 0


@pytest.mark.anyio
async def test_email_service_async_transactional_methods(monkeypatch):
    """
    Verifica que los métodos asíncronos send_otp_email_async, send_quorum_alert_email_async
    y send_session_confirmation_email_async ejecuten sin bloqueo mediante asyncio.to_thread.
    """
    from app.services.email_service import EmailService

    monkeypatch.setattr(settings, "SMTP_ENABLED", False)

    ok1 = await EmailService.send_otp_email_async("test.async@upt.pe", "999888")
    assert ok1 is True

    ok2 = await EmailService.send_quorum_alert_email_async(
        to_email="mentor.async@upt.pe",
        session_code="SES-99",
        confirmed_students=1,
        required_students=5,
        session_date="2026-11-20T10:00:00Z",
    )
    assert ok2 is True

    ok3 = await EmailService.send_session_confirmation_email_async(
        to_email="student.async@upt.pe",
        session_code="SES-99",
        topic_title="Grafos",
        room_or_link="https://meet.google.com/upt-ses99-demo",
    )
    assert ok3 is True


def test_virtual_room_service_query_params_and_safeguards():
    """
    Verifica que VirtualRoomService reconozca enlaces con parámetros de consulta
    y maneje de manera segura entradas nulas en generate_google_meet_url.
    """
    from app.services.virtual_room_service import VirtualRoomService

    # URL con query parameters
    assert (
        VirtualRoomService.is_valid_meeting_url(
            "https://meet.google.com/abc-defg-hij?authuser=1&hs=179"
        )
        is True
    )

    # Invocación con None no debe lanzar TypeError
    meet_url = VirtualRoomService.generate_google_meet_url(None)
    assert meet_url.startswith("https://meet.google.com/upt-epis-")

