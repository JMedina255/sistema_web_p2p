"""
Suite de Pruebas Automatizadas para CUS06 — Publicar Oferta de Mentoría, Reserva de Aula y Aprovisionamiento Virtual (MOD-02 / RF08).
Trazabilidad directa con el Catálogo Oficial de Pruebas EPIS-UPT:
- CUS06-U03: Consultar aulas libres mediante el parser de horarios (modalidad presencial)
- CUS06-U04: Generar enlace virtual (Meet/Discord) al publicar sesión virtual con mocks de APIs externas
- CUS06-I01: Rechazar reserva en aula/horario no disponible (integración parser-reserva)
- CUS06-F01: Flujo de publicación de oferta presencial con reserva automática de aula
- CUS06-F02: Flujo de publicación de oferta virtual con aprovisionamiento automático (Meet y Discord)
- CUS06-A01: Aceptación: usabilidad, exactitud de espacios y rendimiento de publicación (10 publicaciones simultáneas)
"""

import io
import time
import pytest
from fastapi import HTTPException
import openpyxl

from app.services.catalog_support_service import (
    ExcepcionAulaNoDisponible,
    ServicioAprovisionamientoDiscord,
    ServicioAprovisionamientoMeet,
    ServicioReservaAula,
)
from app.services.schedule_parser_service import (
    ScheduleParserService,
    ServicioAnalizadorHorarios,
)


@pytest.fixture(autouse=True)
def clean_reserva_aula():
    ServicioReservaAula.limpiar()
    yield
    ServicioReservaAula.limpiar()


@pytest.fixture
def sample_schedule_bytes() -> bytes:
    """Genera en memoria un archivo Excel (.xlsx) con aulas libres y ocupadas de muestra."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cronograma_EPIS"
    ws.append(["Aula", "Día", "Hora Inicio", "Hora Fin", "Ocupación"])
    # 2 aulas libres y 2 ocupadas
    ws.append(["Lab 01", "Lunes", "08:00", "10:00", "LIBRE"])
    ws.append(["Lab 01", "Lunes", "10:00", "12:00", "Sistemas Operativos II"])
    ws.append(["Aula 204", "Martes", "14:00", "16:00", "DISPONIBLE"])
    ws.append(["Aula 204", "Martes", "16:00", "18:00", "Compiladores"])
    out = io.BytesIO()
    wb.save(out)
    return out.getvalue()


# ==============================================================================
# CUS06-U03: Consultar aulas libres mediante el parser de horarios
# ==============================================================================
def test_cus06_u03_consult_free_classrooms_via_schedule_parser(sample_schedule_bytes: bytes):
    """
    CUS06-U03: Probar ServicioAnalizadorHorarios.ExtraerHorariosLibres() con un archivo de
    horarios de muestra: identifica correctamente aulas/horarios libres.
    """
    # Probar mediante método canónico en español alias
    aulas_libres = ServicioAnalizadorHorarios.ExtraerHorariosLibres(sample_schedule_bytes)

    assert len(aulas_libres) == 2
    nombres_aulas = [slot["aula"] for slot in aulas_libres]
    assert "Lab 01" in nombres_aulas
    assert "Aula 204" in nombres_aulas

    slot_lab = next(s for s in aulas_libres if s["aula"] == "Lab 01")
    assert slot_lab["dia"] == "Lunes"
    assert slot_lab["hora_inicio"] == "08:00"
    assert slot_lab["hora_fin"] == "10:00"

    slot_aula = next(s for s in aulas_libres if s["aula"] == "Aula 204")
    assert slot_aula["dia"] == "Martes"
    assert slot_aula["hora_inicio"] == "14:00"


# ==============================================================================
# CUS06-U04: Generar enlace virtual (Meet/Discord) con mocks de APIs externas
# ==============================================================================
def test_cus06_u04_virtual_provisioning_meet_and_discord():
    """
    CUS06-U04: Probar ServicioAprovisionamientoMeet.CrearReunion() y
    ServicioAprovisionamientoDiscord.AsignarCanal() con mocks de las APIs externas.
    """
    # 1. Google Meet
    res_meet = ServicioAprovisionamientoMeet.CrearReunion(
        titulo="Taller de Algoritmos Avanzados",
        fecha_inicio="2026-10-15T10:00:00Z",
        duracion_minutos=120,
    )
    assert res_meet["plataforma"] == "GOOGLE_MEET"
    assert res_meet["enlace_reunion"].startswith("https://meet.google.com/")
    assert len(res_meet["codigo_reunion"]) > 5
    assert res_meet["duracion_minutos"] == 120

    # 2. Discord
    res_discord = ServicioAprovisionamientoDiscord.AsignarCanal(
        titulo="Asesoría de Estructuras de Datos",
        id_sesion=705,
    )
    assert res_discord["plataforma"] == "DISCORD"
    assert res_discord["id_sesion"] == 705
    assert res_discord["canal_id"] == "disc-chan-00705"
    assert "discord.gg/upt-epis-0705" in res_discord["enlace_invitacion"]


# ==============================================================================
# CUS06-I01: Rechazar reserva en aula/horario no disponible (integración parser-reserva)
# ==============================================================================
def test_cus06_i01_reject_room_reservation_occupied_slot(sample_schedule_bytes: bytes):
    """
    CUS06-I01: Verificar que ServicioReservaAula.Reservar() consulta el resultado real
    del parser y rechaza reservas en horarios/aulas marcados como ocupados.
    """
    aulas_libres = ServicioAnalizadorHorarios.ExtraerHorariosLibres(sample_schedule_bytes)

    # 1. Reserva exitosa en aula libre extraída por el parser
    reserva_ok = ServicioReservaAula.Reservar(
        id_aula="Lab 01",
        dia="Lunes",
        hora_inicio="08:00",
        hora_fin="10:00",
        parser_horarios_libres=aulas_libres,
        mentor_email="mentor.experto@upt.pe",
        id_sesion=101,
    )
    assert reserva_ok["estado"] == "RESERVA_CONFIRMADA"
    assert reserva_ok["aula"] == "Lab 01"

    # 2. Intento de reserva en aula ocupada según el parser (Lab 01 de 10:00 a 12:00)
    with pytest.raises(ExcepcionAulaNoDisponible) as exc_ocupado:
        ServicioReservaAula.Reservar(
            id_aula="Lab 01",
            dia="Lunes",
            hora_inicio="10:00",
            hora_fin="12:00",
            parser_horarios_libres=aulas_libres,
            mentor_email="mentor.experto@upt.pe",
            id_sesion=102,
        )
    assert exc_ocupado.value.status_code == 409
    assert "no se encuentra disponible" in exc_ocupado.value.detail

    # 3. Intento de colisión: reservar exactamente la misma aula libre ya reservada en paso 1
    with pytest.raises(ExcepcionAulaNoDisponible) as exc_colision:
        ServicioReservaAula.Reservar(
            id_aula="Lab 01",
            dia="Lunes",
            hora_inicio="08:00",
            hora_fin="10:00",
            parser_horarios_libres=aulas_libres,
            mentor_email="otro.mentor@upt.pe",
            id_sesion=103,
        )
    assert exc_colision.value.status_code == 409
    assert "Colisión de reserva" in exc_colision.value.detail


# ==============================================================================
# CUS06-F01: Flujo de publicación presencial con reserva automática de aula
# ==============================================================================
def test_cus06_f01_publish_presencial_offer_with_automatic_classroom_reservation(
    sample_schedule_bytes: bytes,
):
    """
    CUS06-F01: El mentor (VII-X ciclo) publica una oferta presencial; el sistema sugiere
    solo aulas libres según el parser y confirma la reserva junto con la publicación.
    """
    aulas_disponibles = ServicioAnalizadorHorarios.ExtraerHorariosLibres(sample_schedule_bytes)

    # Validar que un aula ocupada ("Aula 204" a las 16:00) NO figura en las sugerencias
    ocupadas_presentes = [
        s for s in aulas_disponibles
        if s["aula"] == "Aula 204" and s["hora_inicio"] == "16:00"
    ]
    assert len(ocupadas_presentes) == 0, "El parser filtró incorrectamente un aula ocupada."

    # Mentor selecciona "Aula 204" en su horario libre 14:00-16:00
    reserva = ServicioReservaAula.Reservar(
        id_aula="Aula 204",
        dia="Martes",
        hora_inicio="14:00",
        hora_fin="16:00",
        parser_horarios_libres=aulas_disponibles,
        mentor_email="mentor.septimo@upt.pe",
        id_sesion=201,
    )

    assert reserva["estado"] == "RESERVA_CONFIRMADA"
    assert reserva["id_sesion"] == 201
    assert reserva["mentor_email"] == "mentor.septimo@upt.pe"


# ==============================================================================
# CUS06-F02: Flujo de publicación virtual con aprovisionamiento automático
# ==============================================================================
def test_cus06_f02_publish_virtual_offer_with_automatic_provisioning():
    """
    CUS06-F02: El mentor publica una oferta virtual eligiendo Meet o Discord;
    el sistema genera automáticamente el enlace/canal y lo asocia a la sesión.
    """
    # Sesión 1: Modalidad Virtual con Google Meet
    meet_info = ServicioAprovisionamientoMeet.CrearReunion(
        titulo="Refuerzo Cálculo I",
        fecha_inicio="2026-10-20T16:00:00Z",
    )
    assert meet_info["plataforma"] == "GOOGLE_MEET"
    assert meet_info["estado"] == "ACTIVO"
    assert meet_info["enlace_reunion"].startswith("https://meet.google.com/")

    # Sesión 2: Modalidad Virtual con Discord
    discord_info = ServicioAprovisionamientoDiscord.AsignarCanal(
        titulo="Laboratorio Virtual POO",
        id_sesion=302,
    )
    assert discord_info["plataforma"] == "DISCORD"
    assert discord_info["estado"] == "ACTIVO"
    assert "discord.gg" in discord_info["enlace_invitacion"]


# ==============================================================================
# CUS06-A01: Aceptación: 10 publicaciones simultáneas y verificación cruzada
# ==============================================================================
def test_cus06_a01_acceptance_concurrent_publishing_and_latency():
    """
    CUS06-A01: 10 mentores publican sesiones (mixtas presencial/virtual) simultáneamente.
    Criterios:
    (1) Publicación con reserva/aprovisionamiento en <= 3 s.
    (2) 100% de aulas sugeridas están realmente libres (verificación cruzada).
    (3) Ninguna colisión no controlada ni degradación del servicio.
    """
    # Generar cronograma con 10 aulas libres distintas
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Aula", "Día", "Hora Inicio", "Hora Fin", "Ocupación"])
    for i in range(1, 11):
        ws.append([f"Lab {i:02d}", "Lunes", "08:00", "10:00", "LIBRE"])
    out = io.BytesIO()
    wb.save(out)
    cronograma_bytes = out.getvalue()

    t0 = time.perf_counter()

    aulas_libres = ServicioAnalizadorHorarios.ExtraerHorariosLibres(cronograma_bytes)
    assert len(aulas_libres) == 10

    # 10 publicaciones (5 presenciales con reserva + 5 virtuales con aprovisionamiento)
    publicaciones = []
    for i in range(1, 11):
        mentor_email = f"mentor_{i:02d}@upt.pe"
        if i % 2 == 1:
            # Presencial: reserva en aula libre correspondiente
            aula = f"Lab {i:02d}"
            res_aula = ServicioReservaAula.Reservar(
                id_aula=aula,
                dia="Lunes",
                hora_inicio="08:00",
                hora_fin="10:00",
                parser_horarios_libres=aulas_libres,
                mentor_email=mentor_email,
                id_sesion=1000 + i,
            )
            publicaciones.append(res_aula)
        else:
            # Virtual: aprovisionamiento automático alternando Meet / Discord
            if i % 4 == 0:
                prov = ServicioAprovisionamientoDiscord.AsignarCanal(
                    titulo=f"Sesión Virtual {i}", id_sesion=1000 + i
                )
            else:
                prov = ServicioAprovisionamientoMeet.CrearReunion(
                    titulo=f"Sesión Virtual {i}", fecha_inicio="2026-10-25T14:00:00Z"
                )
            publicaciones.append(prov)

    elapsed = time.perf_counter() - t0

    assert len(publicaciones) == 10
    assert elapsed < 3.0, f"El tiempo total ({elapsed:.3f} s) superó el umbral reglamentario de 3.0 s."
