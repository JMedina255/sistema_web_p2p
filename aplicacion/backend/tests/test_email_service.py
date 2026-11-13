"""
Pruebas Unitarias para el Servicio de Correo Institucional (EmailService).
Valida:
- Armado estándar de mensajes MIME (RFC 2822) con versiones plain-text y HTML.
- Fallback seguro a log [EMAIL DEV/MOCK] cuando SMTP_ENABLED=False o credenciales ausentes.
- Despacho real y manejo de excepciones con servidor SMTP mockeado (STARTTLS, login, send).
- Envío asíncrono vía asyncio.to_thread.
- Comportamiento de AuthService en modo producción (mockCodeHint strictly None y bypass '000000' deshabilitado).
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.core.config import settings
from app.services.auth_service import AuthService
from app.services.email_service import EmailService


def test_email_service_mime_message_construction():
    """Verifica que el mensaje MIME contenga los encabezados RFC y partes multipart requeridas."""
    msg = EmailService._create_message(
        to_email="test.student@upt.pe",
        subject="Asunto de Prueba Institucional",
        html_body="<p>Hola Alumno</p>",
        text_body="Hola Alumno",
    )
    assert msg["To"] == "test.student@upt.pe"
    assert "noreply.mentoria.upt@gmail.com" in msg["From"]
    assert msg["Subject"] == "Asunto de Prueba Institucional"
    assert msg.is_multipart()
    parts = msg.get_payload()
    assert len(parts) == 2
    content_types = [p.get_content_type() for p in parts]
    assert "text/plain" in content_types
    assert "text/html" in content_types


def test_email_service_mock_dev_fallback_when_smtp_disabled(monkeypatch, capsys):
    """En desarrollo o con SMTP deshabilitado, registra en consola [EMAIL DEV/MOCK] sin lanzar error."""
    monkeypatch.setattr(settings, "SMTP_ENABLED", False)
    monkeypatch.setattr(settings, "SMTP_USER", None)

    ok_otp = EmailService.send_otp_email("alumno.test@upt.pe", "654321", expires_minutes=5)
    assert ok_otp is True

    captured = capsys.readouterr().out
    assert "[EMAIL DEV/MOCK]" in captured
    assert "alumno.test@upt.pe" in captured
    assert "654321" in captured

    ok_quorum = EmailService.send_quorum_alert_email(
        to_email="mentor.test@upt.pe",
        session_code="SES-101",
        confirmed_students=2,
        required_students=5,
        session_date="2026-11-20T10:00:00Z",
    )
    assert ok_quorum is True

    ok_conf = EmailService.send_session_confirmation_email(
        to_email="alumno.test@upt.pe",
        session_code="SES-101",
        topic_title="Árboles Binarios",
        room_or_link="https://meet.google.com/upt-ci-101",
    )
    assert ok_conf is True


def test_email_service_smtp_sync_success_with_mocked_server(monkeypatch):
    """Verifica que al estar activado SMTP_ENABLED se conecte con TLS, autentique y despache el mensaje."""
    monkeypatch.setattr(settings, "SMTP_ENABLED", True)
    monkeypatch.setattr(settings, "SMTP_HOST", "smtp.gmail.com")
    monkeypatch.setattr(settings, "SMTP_PORT", 587)
    monkeypatch.setattr(settings, "SMTP_USE_TLS", True)
    monkeypatch.setattr(settings, "SMTP_USER", "mentorias.upt@gmail.com")
    monkeypatch.setattr(settings, "SMTP_PASSWORD", "app-password-16ch")

    mock_smtp_instance = MagicMock()
    with patch("smtplib.SMTP", return_value=mock_smtp_instance) as mock_smtp_cls:
        mock_smtp_instance.__enter__.return_value = mock_smtp_instance

        res = EmailService.send_otp_email("destinatario@upt.pe", "123456", expires_minutes=5)

        assert res is True
        mock_smtp_cls.assert_called_once_with("smtp.gmail.com", 587, timeout=15)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with("mentorias.upt@gmail.com", "app-password-16ch")
        mock_smtp_instance.send_message.assert_called_once()


def test_email_service_smtp_sync_handles_exception_gracefully(monkeypatch):
    """Verifica que si el servidor SMTP falla, la excepción se capture, se registre y retorne False sin tumbar el servicio."""
    monkeypatch.setattr(settings, "SMTP_ENABLED", True)
    monkeypatch.setattr(settings, "SMTP_USER", "mentorias.upt@gmail.com")
    monkeypatch.setattr(settings, "SMTP_PASSWORD", "app-password-16ch")

    with patch("smtplib.SMTP", side_effect=ConnectionRefusedError("SMTP server unreachable")):
        res = EmailService.send_otp_email("destinatario@upt.pe", "123456")
        assert res is False


@pytest.mark.anyio
async def test_email_service_async_send(monkeypatch):
    """Verifica el envío asíncrono no bloqueante vía asyncio.to_thread."""
    monkeypatch.setattr(settings, "SMTP_ENABLED", False)

    res = await EmailService.send_email_async(
        to_email="estudiante.async@upt.pe",
        subject="Prueba Asíncrona",
        html_body="<p>Texto</p>",
        text_body="Texto",
    )
    assert res is True


def test_auth_service_production_mode_strict_security(monkeypatch):
    """
    En producción (APP_ENV == 'production'):
    - mockCodeHint debe ser siempre None.
    - El bypass '000000' no debe operar como código expirado artificial, sino validarse normalmente contra el hash.
    """
    monkeypatch.setattr(settings, "APP_ENV", "production")

    # 1. Request OTP en producción
    resp = AuthService.request_otp(None, "estudiante.prod@upt.pe")
    assert resp.mockCodeHint is None
    assert resp.isMock is False
    challenge_id = resp.challengeId

    # 2. Intentar usar bypass '000000' en producción -> No activa OTP_EXPIRED artificialmente
    # Debe fallar con OTP_INVALID si el hash no coincide con '000000'
    with pytest.raises(HTTPException) as exc_info:
        AuthService.verify_otp(None, challenge_id, "000000")
    # En producción no es OTP_EXPIRED (a menos que el código real haya sido '000000', lo cual es 1 en 1,000,000)
    assert exc_info.value.detail["code"] == "OTP_INVALID"
