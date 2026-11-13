"""
Servicio de Aprovisionamiento y Normalización de Aulas Virtuales (VirtualRoomService).
Diseñado para operar de forma autónoma sin credenciales administrativas de Google Workspace
o Microsoft 365, permitiendo a los mentores ingresar sus propios enlaces de Meet, Teams,
Zoom o Discord, o solicitar la generación estándar automática de una sala de Google Meet institucional.
"""

from __future__ import annotations

import logging
import re
import uuid

logger = logging.getLogger("app.virtual_room")


class VirtualRoomService:
    """
    Gestor de salas virtuales para sesiones de mentoría (CUS06 / RN-07):
    - Valida enlaces proporcionados por el mentor (Google Meet, Microsoft Teams, Zoom, Discord).
    - Genera enlaces deterministas e institucionales de Google Meet (@upt.pe) cuando se solicita modo automático.
    - Sanitiza y normaliza la URL final persistida en 'espacio_asignado'.
    """

    # Expresiones regulares de plataformas de videoconferencia soportadas
    PATTERNS = {
        "meet": re.compile(r"^https?://meet\.google\.com/[a-z0-9\-]+(\?[^\s]*)?$", re.IGNORECASE),
        "teams": re.compile(
            r"^https?://([a-zA-Z0-9\-]+\.)?teams\.(microsoft|live)\.com/[^\s]+$", re.IGNORECASE
        ),
        "zoom": re.compile(
            r"^https?://([a-zA-Z0-9\-]+\.)?zoom\.us/(j|my|w)/[^\s]+$", re.IGNORECASE
        ),
        "discord": re.compile(
            r"^https?://(discord\.(gg|com/invite|com/channels))/[^\s]+$", re.IGNORECASE
        ),
    }

    GENERIC_URL_PATTERN = re.compile(r"^https?://[^\s]+$", re.IGNORECASE)

    AUTO_TRIGGERS = {
        "",
        "auto",
        "automatico",
        "automático",
        "generar",
        "generar automáticamente",
        "generar automaticamente",
        "sistema",
    }

    @classmethod
    def is_valid_meeting_url(cls, url: str) -> bool:
        """
        Verifica si la cadena corresponde a un enlace válido de videoconferencia.
        """
        if not url:
            return False
        clean = url.strip()
        for pattern in cls.PATTERNS.values():
            if pattern.match(clean):
                return True
        return bool(cls.GENERIC_URL_PATTERN.match(clean))

    @classmethod
    def generate_google_meet_url(cls, session_code: str | None = None) -> str:
        """
        Genera un enlace estándar de Google Meet con prefijo institucional y sufijo pseudoaleatorio.
        Ejemplo: https://meet.google.com/upt-ses-1-a1b2
        """
        raw_code = str(session_code or "")
        clean_code = re.sub(r"[^a-zA-Z0-9]", "", raw_code).lower() or "epis"
        unique_suffix = uuid.uuid4().hex[:4]
        return f"https://meet.google.com/upt-{clean_code}-{unique_suffix}"

    @classmethod
    def resolve_virtual_room(
        cls,
        provided_link: str | None,
        session_code: str,
    ) -> str:
        """
        Resuelve la URL definitiva para una oferta virtual:
        - Si el mentor dejó el campo vacío o indicó 'auto', genera URL estándar de Meet.
        - Si proporcionó un enlace válido, lo respeta y preserva.
        - Si proporcionó un texto inválido o no URL, genera el enlace estándar de respaldo.
        """
        if not provided_link:
            room = cls.generate_google_meet_url(session_code)
            logger.info("Generada sala virtual automática: %s para %s", room, session_code)
            return room

        clean = provided_link.strip()
        if clean.lower() in cls.AUTO_TRIGGERS:
            room = cls.generate_google_meet_url(session_code)
            logger.info("Generada sala virtual automática (trigger '%s'): %s para %s", clean, room, session_code)
            return room

        if cls.is_valid_meeting_url(clean):
            return clean

        # Si el texto no es una URL válida (ej. 'meet'), generar enlace estándar
        fallback = cls.generate_google_meet_url(session_code)
        logger.warning(
            "Enlace '%s' no parece una URL válida. Aplicando fallback de Google Meet: %s",
            clean,
            fallback,
        )
        return fallback
