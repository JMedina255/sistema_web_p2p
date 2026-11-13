"""
Servicio de Correo Electrónico Institucional (EmailService).
Soporta despacho SMTP nativo (por defecto Gmail / Google App Password) con envío asíncrono
mediante asyncio.to_thread, y fallback automático de trazabilidad en consola [EMAIL DEV/MOCK]
para desarrollo local y pruebas automatizadas.
"""

from __future__ import annotations

import asyncio
import email.utils
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from app.core.config import settings

logger = logging.getLogger("app.email")


class EmailService:
    """
    Servicio de mensajería electrónica para notificaciones transaccionales:
    - Códigos OTP de acceso a la plataforma (RNF01 / CUS01).
    - Alertas de contingencia de quórum a T-24h para mentores (RN-09 / RN-10).
    - Confirmaciones de asistencia con enlace de aula virtual / recinto (RN-07).
    """

    @classmethod
    def _create_message(
        cls,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str,
    ) -> MIMEMultipart:
        """Construye un mensaje multipart/alternative estándar RFC 2822."""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        clean_from = settings.SMTP_FROM_EMAIL or settings.SMTP_USER or "noreply.mentoria.upt@gmail.com"
        msg["From"] = email.utils.formataddr((settings.SMTP_FROM_NAME, clean_from))
        msg["To"] = to_email
        msg["Date"] = email.utils.formatdate(localtime=True)
        msg["Message-ID"] = email.utils.make_msgid(domain="upt.pe")

        # Adjuntar versión texto plano y versión enriquecida HTML
        part_text = MIMEText(text_body, "plain", "utf-8")
        part_html = MIMEText(html_body, "html", "utf-8")
        msg.attach(part_text)
        msg.attach(part_html)
        return msg

    @classmethod
    def _send_smtp_sync(
        cls,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str,
    ) -> bool:
        """
        Envía un correo de manera síncrona mediante smtplib.
        Si SMTP_ENABLED es False o SMTP_USER está vacío, realiza fallback a log [EMAIL DEV/MOCK].
        """
        if not to_email or not isinstance(to_email, str) or not to_email.strip():
            logger.warning("Intento de envío de correo cancelado: destinatario vacío o inválido.")
            return False

        clean_to = to_email.strip().lower()

        # Fallback a consola si el servicio SMTP está desactivado o sin credenciales
        if not settings.SMTP_ENABLED or not (settings.SMTP_USER and settings.SMTP_USER.strip()):
            log_line = (
                f"[EMAIL DEV/MOCK] Destinatario: {clean_to} | Asunto: {subject} | Mensaje: {text_body}"
            )
            print(log_line)
            logger.info(log_line)
            return True

        # Despacho real mediante servidor SMTP
        try:
            msg = cls._create_message(
                to_email=clean_to,
                subject=subject,
                html_body=html_body,
                text_body=text_body,
            )
            use_ssl = settings.SMTP_PORT == 465 or not settings.SMTP_USE_TLS
            smtp_cls = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP

            with smtp_cls(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as server:
                server.ehlo()
                if settings.SMTP_USE_TLS and not use_ssl:
                    server.starttls()
                    server.ehlo()
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            logger.info("Correo enviado exitosamente vía SMTP a %s (Asunto: %s)", clean_to, subject)
            return True
        except Exception as exc:
            logger.error(
                "Error al enviar correo SMTP a %s (%s: %s). Se registra en log de contingencia.",
                clean_to,
                exc.__class__.__name__,
                exc,
            )
            return False

    @classmethod
    async def send_email_async(
        cls,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str,
    ) -> bool:
        """Envío asíncrono no bloqueante vía asyncio.to_thread."""
        return await asyncio.to_thread(cls._send_smtp_sync, to_email, subject, html_body, text_body)

    @classmethod
    async def send_otp_email_async(
        cls,
        to_email: str,
        code: str,
        expires_minutes: int = 5,
    ) -> bool:
        """Envío asíncrono de OTP vía asyncio.to_thread."""
        return await asyncio.to_thread(cls.send_otp_email, to_email, code, expires_minutes)

    @classmethod
    async def send_quorum_alert_email_async(
        cls,
        to_email: str,
        session_code: str,
        confirmed_students: int,
        required_students: int,
        session_date: str,
        topic_title: str | None = None,
        **kwargs: Any,
    ) -> bool:
        """Envío asíncrono de alerta de quórum vía asyncio.to_thread."""
        return await asyncio.to_thread(
            cls.send_quorum_alert_email,
            to_email,
            session_code,
            confirmed_students,
            required_students,
            session_date,
            topic_title,
            **kwargs,
        )

    @classmethod
    async def send_session_confirmation_email_async(
        cls,
        to_email: str,
        session_code: str,
        topic_title: str,
        room_or_link: str,
        student_name: str | None = None,
        session_date: str | None = None,
        **kwargs: Any,
    ) -> bool:
        """Envío asíncrono de confirmación de sesión vía asyncio.to_thread."""
        return await asyncio.to_thread(
            cls.send_session_confirmation_email,
            to_email,
            session_code,
            topic_title,
            room_or_link,
            student_name,
            session_date,
            **kwargs,
        )

    # =========================================================================
    # Métodos Transaccionales Específicos
    # =========================================================================

    @classmethod
    def send_otp_email(
        cls,
        to_email: str,
        code: str,
        expires_minutes: int = 5,
    ) -> bool:
        """
        Envía el código numérico OTP de verificación institucional (6 dígitos).
        """
        subject = f"[{code}] Tu código de acceso al Sistema de Mentorías P2P - EPIS UPT"

        text_body = (
            f"Universidad Privada de Tacna - Escuela Profesional de Ingeniería de Sistemas\n\n"
            f"Tu código de verificación institucional para acceder a la plataforma de mentorías es:\n\n"
            f"      {code}\n\n"
            f"Este código tiene una vigencia perentoria de {expires_minutes} minutos según la norma RNF01.\n"
            f"Si no solicitaste este acceso, puedes ignorar este mensaje de seguridad."
        )

        html_body = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Código de Verificación UPT</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; margin: 0; padding: 24px;">
  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
    <div style="background-color: #1c2a59; padding: 20px 24px; text-align: center;">
      <h1 style="color: #ffffff; font-size: 16px; margin: 0; font-weight: 700; letter-spacing: 0.5px;">UNIVERSIDAD PRIVADA DE TACNA</h1>
      <p style="color: #cbd5e1; font-size: 12px; margin: 4px 0 0 0;">Escuela Profesional de Ingeniería de Sistemas</p>
    </div>
    <div style="padding: 28px 24px; text-align: center;">
      <h2 style="color: #1e293b; font-size: 18px; margin: 0 0 12px 0;">Código de Verificación Institucional</h2>
      <p style="color: #475569; font-size: 14px; margin: 0 0 20px 0; line-height: 1.5;">
        Has solicitado acceso al Sistema Web P2P de Mentorías Académicas. Ingresa el siguiente código de 6 dígitos para autenticar tu cuenta:
      </p>
      <div style="display: inline-block; background-color: #f8fafc; border: 2px dashed #3b82f6; border-radius: 8px; padding: 14px 28px; margin: 8px 0 20px 0;">
        <span style="font-size: 32px; font-weight: 800; letter-spacing: 6px; color: #1e3a8a; font-family: monospace;">{code}</span>
      </div>
      <p style="color: #64748b; font-size: 12px; margin: 0; line-height: 1.4;">
        ⏱️ Este código caducará automáticamente en <strong>{expires_minutes} minutos</strong>.<br>
        Por seguridad, no compartas este código con ninguna otra persona.
      </p>
    </div>
    <div style="background-color: #f8fafc; padding: 14px 24px; text-align: center; border-top: 1px solid #e2e8f0;">
      <p style="color: #94a3b8; font-size: 11px; margin: 0;">
        EdRecSys P2P • Sistema de Tutorías y Mentorías entre Pares • EPIS UPT 2026
      </p>
    </div>
  </div>
</body>
</html>"""

        return cls._send_smtp_sync(to_email, subject, html_body, text_body)

    @classmethod
    def send_quorum_alert_email(
        cls,
        to_email: str,
        session_code: str,
        confirmed_students: int,
        required_students: int,
        session_date: str,
        topic_title: str | None = None,
        **kwargs: Any,
    ) -> bool:
        """
        Envía alerta de quórum insuficiente en T-24h al mentor para que proceda a resolver
        (Mantener, Reprogramar o Cancelar la sesión según RN-10).
        """
        subject = f"[Alerta de Quórum] Sesión {session_code} requiere tu decisión - EPIS UPT"

        topic_str = f" ({topic_title})" if topic_title else ""
        text_body = (
            f"Estimado(a) Mentor(a):\n\n"
            f"Se ha cumplido el corte normativo de T-24 horas para la sesión {session_code}{topic_str}.\n"
            f"Fecha de inicio: {session_date}\n\n"
            f"Estado actual de quórum: {confirmed_students} confirmados de {required_students} requeridos.\n"
            f"La sesión se encuentra en estado QUORUM_INSUFICIENTE.\n\n"
            f"Por favor ingresa al portal de mentorías para resolver la contingencia:\n"
            f"- Mantener sesión extraordinaria con los estudiantes ratificados.\n"
            f"- Reprogramar para una nueva fecha con más de 24h de antelación.\n"
            f"- Cancelar la sesión justificando formalmente la razón pedagógica.\n\n"
            f"Dirección de EPIS - Universidad Privada de Tacna"
        )

        html_body = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Alerta de Quórum EPIS</title></head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8fafc; padding: 20px;">
  <div style="max-width: 560px; margin: 0 auto; background: #fff; border-radius: 8px; border: 1px solid #e2e8f0; overflow: hidden;">
    <div style="background-color: #b45309; padding: 16px; text-align: center; color: #fff;">
      <h2 style="margin: 0; font-size: 16px;">⚠️ ALERTA DE QUÓRUM REGISTRO T-24H</h2>
    </div>
    <div style="padding: 24px;">
      <p style="color: #334155;">Estimado(a) Mentor(a):</p>
      <p style="color: #334155;">
        La sesión <strong>{session_code}</strong> programada para el <strong>{session_date}</strong>
        cuenta con <strong>{confirmed_students}</strong> de <strong>{required_students}</strong> inscritos confirmados.
      </p>
      <p style="color: #334155;">
        Conforme a la regla <strong>RN-10</strong>, debes definir en el sistema si deseas:
      </p>
      <ul style="color: #475569; font-size: 14px;">
        <li><strong>Mantener</strong> la sesión con los alumnos confirmados.</li>
        <li><strong>Reprogramar</strong> con nueva fecha &gt; 24h.</li>
        <li><strong>Cancelar</strong> con justificación obligatoria.</li>
      </ul>
    </div>
  </div>
</body>
</html>"""

        return cls._send_smtp_sync(to_email, subject, html_body, text_body)

    @classmethod
    def send_session_confirmation_email(
        cls,
        to_email: str,
        session_code: str,
        topic_title: str,
        room_or_link: str,
        student_name: str | None = None,
        session_date: str | None = None,
        **kwargs: Any,
    ) -> bool:
        """
        Envía confirmación de asistencia al estudiante con el enlace virtual o aula asignada.
        """
        subject = f"[Confirmada] Tu mentoría {session_code}: {topic_title} - EPIS UPT"

        student_greeting = f"Hola {student_name}," if student_name else "Estimado(a) estudiante,"
        date_str = f"Fecha y hora: {session_date}\n" if session_date else ""

        text_body = (
            f"{student_greeting}\n\n"
            f"Tu asistencia para la sesión de mentoría '{topic_title}' ({session_code}) ha sido ratificada con éxito.\n"
            f"{date_str}"
            f"Lugar / Enlace de acceso: {room_or_link}\n\n"
            f"Recuerda conectarte o llegar con 5 minutos de antelación.\n"
            f"¡Muchos éxitos en tu sesión formativa!\n\n"
            f"Dirección de EPIS - Universidad Privada de Tacna"
        )

        html_body = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Mentoría Confirmada</title></head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8fafc; padding: 20px;">
  <div style="max-width: 560px; margin: 0 auto; background: #fff; border-radius: 8px; border: 1px solid #e2e8f0; overflow: hidden;">
    <div style="background-color: #047857; padding: 16px; text-align: center; color: #fff;">
      <h2 style="margin: 0; font-size: 16px;">✅ SESIÓN DE MENTORÍA RATIFICADA</h2>
    </div>
    <div style="padding: 24px;">
      <p style="color: #334155;">{student_greeting}</p>
      <p style="color: #334155;">
        Tu vacante para la sesión <strong>{session_code}</strong> — <em>{topic_title}</em> ha quedado confirmada.
      </p>
      <div style="background: #f1f5f9; padding: 12px; border-radius: 6px; margin: 16px 0;">
        <p style="margin: 0; font-size: 14px; color: #1e293b;">
          📍 <strong>Ubicación / Enlace de Conexión:</strong><br>
          <a href="{room_or_link}" style="color: #2563eb; word-break: break-all;">{room_or_link}</a>
        </p>
      </div>
      <p style="color: #64748b; font-size: 12px; margin: 0;">
        Se registrará la asistencia formativa al inicio de la sesión.
      </p>
    </div>
  </div>
</body>
</html>"""

        return cls._send_smtp_sync(to_email, subject, html_body, text_body)
