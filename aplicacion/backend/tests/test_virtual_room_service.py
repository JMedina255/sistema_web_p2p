"""
Pruebas Unitarias para el Servicio de Aprovisionamiento de Aulas Virtuales (VirtualRoomService).
Valida:
- Reconocimiento y validación estricta de URLs de plataformas soportadas (Google Meet, MS Teams, Zoom, Discord).
- Rechazo y normalización de entradas vacías o marcadores 'auto'.
- Generación de enlaces Google Meet estandarizados con formato 'https://meet.google.com/upt-xxx-yyyy'.
- Integración en OfferService.publish_offer para aprovisionamiento desatendido sin APIs institucionales.
"""

from app.schemas.offer import PublishOfferPayload
from app.services.offer_service import OfferService
from app.services.virtual_room_service import VirtualRoomService


def test_virtual_room_service_url_validation():
    """Valida que reconozca enlaces reales de plataformas de teleconferencia."""
    # Google Meet
    assert VirtualRoomService.is_valid_meeting_url("https://meet.google.com/abc-defg-hij") is True
    assert VirtualRoomService.is_valid_meeting_url("http://meet.google.com/upt-algo-1234") is True

    # MS Teams
    assert (
        VirtualRoomService.is_valid_meeting_url(
            "https://teams.microsoft.com/l/meetup-join/19%3ameeting_xyz%40thread.v2/0?context=demo"
        )
        is True
    )

    # Zoom
    assert VirtualRoomService.is_valid_meeting_url("https://zoom.us/j/123456789") is True
    assert VirtualRoomService.is_valid_meeting_url("https://us04web.zoom.us/my/profe.epis") is True

    # Discord
    assert VirtualRoomService.is_valid_meeting_url("https://discord.gg/epis-upt-room") is True
    assert VirtualRoomService.is_valid_meeting_url("https://discord.com/channels/123/456") is True

    # Enlaces no válidos / vacíos
    assert VirtualRoomService.is_valid_meeting_url("") is False
    assert VirtualRoomService.is_valid_meeting_url("   ") is False


def test_virtual_room_service_generate_meet_url():
    """Verifica que la generación de URL Meet cumpla el estándar institucional."""
    url = VirtualRoomService.generate_google_meet_url("SES-42")
    assert url.startswith("https://meet.google.com/upt-ses42-")
    # Sufijo hex de 4 caracteres
    suffix = url.split("-")[-1]
    assert len(suffix) == 4


def test_virtual_room_service_resolve_virtual_room_behaviors():
    """Verifica la resolución según enlace provisto, disparador automático o fallback."""
    # 1. Sin enlace provisto -> Genera automáticamente Meet
    r1 = VirtualRoomService.resolve_virtual_room(None, "SES-10")
    assert r1.startswith("https://meet.google.com/upt-ses10-")

    # 2. Trigger 'auto' o 'generar' -> Genera automáticamente Meet
    r2 = VirtualRoomService.resolve_virtual_room("auto", "SES-20")
    assert r2.startswith("https://meet.google.com/upt-ses20-")
    r2_bis = VirtualRoomService.resolve_virtual_room("generar automáticamente", "SES-21")
    assert r2_bis.startswith("https://meet.google.com/upt-ses21-")

    # 3. Enlace propio válido del mentor (ej. Zoom) -> Se preserva íntegro
    custom_zoom = "https://zoom.us/j/9876543210"
    r3 = VirtualRoomService.resolve_virtual_room(custom_zoom, "SES-30")
    assert r3 == custom_zoom

    # 4. Enlace propio de Google Meet -> Se preserva íntegro
    custom_meet = "https://meet.google.com/xyz-uvwx-rst"
    r4 = VirtualRoomService.resolve_virtual_room(custom_meet, "SES-40")
    assert r4 == custom_meet

    # 5. Texto inválido no URL -> Aplica fallback a enlace Meet estándar
    r5 = VirtualRoomService.resolve_virtual_room("sala 101 sin internet", "SES-50")
    assert r5.startswith("https://meet.google.com/upt-ses50-")


def test_offer_service_virtual_room_auto_provisioning():
    """
    Verifica que al publicar una oferta en modalidad 'virtual':
    - Si espacio_asignado está vacío o es 'auto', OfferService genera y persiste la sala virtual en espacio_asignado.
    """
    from datetime import UTC, datetime, timedelta

    start_dt = (datetime.now(UTC) + timedelta(hours=48)).isoformat()

    payload = PublishOfferPayload(
        id_asignatura=1,
        codigo_asignatura="CI-101",
        nombre_asignatura="Cálculo I",
        id_tema=1,
        nombre_tema="Límites",
        fecha_inicio=start_dt,
        duracion_minutos=60,
        modalidad="virtual",
        aforo_maximo=20,
        espacio_asignado="auto",
        mentor_email="mentor.virtual@upt.pe",
        mentor_nombre="Mentor Virtual Test",
    )

    res = OfferService.publish_offer(
        db=None,
        payload=payload,
        caller_email="mentor.virtual@upt.pe",
    )

    assert res.estado == "PUBLICADA"
    assert res.espacio_asignado.startswith("https://meet.google.com/upt-ses")
    assert res.offer.espacio_asignado.startswith("https://meet.google.com/upt-ses")
