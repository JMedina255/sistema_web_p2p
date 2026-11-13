"""
Suite de Pruebas Automatizadas para CUS11 — Cargar Cronograma de Horarios Oficiales (MOD-02 / RF09).
Trazabilidad directa con el Catálogo Oficial de Pruebas EPIS-UPT:
- CUS11-U01: Parsear horario Excel y extraer aulas libres
- CUS11-U02: Parsear horario en PDF y extraer estructura tabular
- CUS11-U03: Rechazar archivo con formato inválido o corrupto
- CUS11-F01: Flujo de carga de cronograma oficial por el Administrador
- CUS11-F02: Manejo de error al cargar archivo con formato inválido
- CUS11-A01: Aceptación: exactitud del parser y tiempos de procesamiento
"""

import io
import time
import pytest
from fastapi import HTTPException
import openpyxl

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

from app.services.schedule_parser_service import (
    ExcepcionFormatoHorarioInvalido,
    ScheduleParserService,
    ServicioAnalizadorHorarios,
)


@pytest.fixture
def sample_excel_schedule_bytes() -> bytes:
    """Genera un archivo Excel (.xlsx) válido en memoria con datos representativos de aulas EPIS."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cronograma_EPIS"
    # Encabezados
    ws.append(["Aula", "Día", "Hora Inicio", "Hora Fin", "Ocupación"])
    # Filas de prueba: 3 libres y 2 ocupadas
    ws.append(["Lab 01", "Lunes", "08:00", "10:00", "LIBRE"])
    ws.append(["Lab 01", "Lunes", "10:00", "12:00", "Base de Datos I (Dr. Valcárcel)"])
    ws.append(["Lab 02", "Martes", "14:00", "16:00", "DISPONIBLE"])
    ws.append(["Aula 301", "Miércoles", "09:00", "11:00", "Inteligencia Artificial"])
    ws.append(["Aula 302", "Jueves", "16:00", "18:00", ""])  # Vacío cuenta como libre

    out = io.BytesIO()
    wb.save(out)
    return out.getvalue()


@pytest.fixture
def sample_pdf_schedule_bytes() -> bytes | None:
    """Genera un archivo PDF válido en memoria con texto estructurado de aulas EPIS."""
    if fitz is None:
        return None
    doc = fitz.open()
    page = doc.new_page()
    text = (
        "CRONOGRAMA OFICIAL DE AULAS EPIS-UPT 2026-II\n"
        "Lab 01 Lunes 08:00 10:00 LIBRE\n"
        "Lab 01 Lunes 10:00 12:00 OCUPADO\n"
        "Aula 301 Martes 14:00 16:00 LIBRE\n"
    )
    page.insert_text((50, 72), text, fontsize=11)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


# ==============================================================================
# CUS11-U01: Parsear horario Excel y extraer aulas libres
# ==============================================================================
def test_cus11_u01_parse_excel_and_extract_free_classrooms(sample_excel_schedule_bytes: bytes):
    """
    Verifica que ServicioAnalizadorHorarios.extraer_horarios_libres_excel()
    identifique correctamente las 3 aulas/bloques libres del archivo.
    """
    slots = ServicioAnalizadorHorarios.extraer_horarios_libres_excel(sample_excel_schedule_bytes)

    assert len(slots) == 3
    aulas_libres = [s["aula"] for s in slots]
    assert "Lab 01" in aulas_libres
    assert "Lab 02" in aulas_libres
    assert "Aula 302" in aulas_libres

    # Validar estructura de campos
    slot1 = slots[0]
    assert slot1["dia"] == "Lunes"
    assert slot1["hora_inicio"] == "08:00"
    assert slot1["hora_fin"] == "10:00"
    assert slot1["estado"] == "LIBRE"


# ==============================================================================
# CUS11-U02: Parsear horario en PDF y extraer estructura tabular
# ==============================================================================
def test_cus11_u02_parse_pdf_and_extract_tabular_structure(sample_pdf_schedule_bytes: bytes | None):
    """
    Verifica que ServicioAnalizadorHorarios.extraer_desde_pdf()
    extraiga correctamente aulas, días y horas libres desde documento PDF.
    """
    if sample_pdf_schedule_bytes is None:
        pytest.skip("PyMuPDF (fitz) no disponible para test PDF.")

    slots = ServicioAnalizadorHorarios.extraer_desde_pdf(sample_pdf_schedule_bytes)
    assert len(slots) >= 2
    aulas = [s["aula"] for s in slots]
    assert "Lab 01" in aulas
    assert "Aula 301" in aulas


# ==============================================================================
# CUS11-U03: Rechazar archivo con formato inválido o corrupto
# ==============================================================================
def test_cus11_u03_reject_corrupt_or_invalid_file_format():
    """
    Verifica que el parser detecte archivos corruptos, vacíos o con extensiones
    no soportadas y lance ExcepcionFormatoHorarioInvalido con HTTP 400.
    """
    # 1. Extensión no soportada
    with pytest.raises(ExcepcionFormatoHorarioInvalido) as exc1:
        ScheduleParserService.validar_archivo("horarios.txt", b"contenido plano...")
    assert "Extensión '.txt' no soportada" in str(exc1.value.detail)

    # 2. Archivo corrupto (extensión .xlsx pero sin cabecera ZIP PK\x03\x04)
    with pytest.raises(ExcepcionFormatoHorarioInvalido) as exc2:
        ScheduleParserService.validar_archivo("horarios_falso.xlsx", b"ESTO NO ES UN ARCHIVO ZIP VALIDO...")
    assert "firma ZIP válida" in str(exc2.value.detail)

    # 3. Archivo excesivamente truncado
    with pytest.raises(ExcepcionFormatoHorarioInvalido) as exc3:
        ScheduleParserService.validar_archivo("vacio.xlsx", b"abc")
    assert "vacío o excesivamente truncado" in str(exc3.value.detail)


# ==============================================================================
# CUS11-F01: Flujo de carga de cronograma oficial por el Administrador
# ==============================================================================
def test_cus11_f01_admin_upload_official_schedule_flow(sample_excel_schedule_bytes: bytes):
    """
    Verifica el flujo completo de subida y procesamiento de cronograma por el Administrador,
    garantizando la preservación de reservas activas existentes.
    """
    reservas_mock = [{"id_reserva": 1, "id_sesion": 101, "estado": "CONFIRMADA"}]

    res = ScheduleParserService.procesar_cronograma_administrador(
        filename="Cronograma_Oficial_2026_II.xlsx",
        content=sample_excel_schedule_bytes,
        reservas_activas=reservas_mock,
    )

    assert res["status"] == "PROCESADO_EXITOSAMENTE"
    assert res["archivo"] == "Cronograma_Oficial_2026_II.xlsx"
    assert res["total_aulas_libres_identificadas"] == 3
    assert res["reservas_activas_preservadas"] == 1


# ==============================================================================
# CUS11-F02: Manejo de error al cargar archivo con formato inválido
# ==============================================================================
def test_cus11_f02_handle_error_uploading_invalid_or_corrupt_file():
    """
    Verifica que el flujo de administración capture el error ante archivo inválido
    y no altere el estado del sistema.
    """
    corrupt_bytes = b"CORRUPTED_STREAM_00000000000000000000000000000000"

    with pytest.raises(ExcepcionFormatoHorarioInvalido):
        ScheduleParserService.procesar_cronograma_administrador(
            filename="horario_corrupto.xlsx",
            content=corrupt_bytes,
        )


# ==============================================================================
# CUS11-A01: Aceptación: exactitud del parser y tiempos de procesamiento (RNF03)
# ==============================================================================
def test_cus11_a01_parser_accuracy_and_performance_benchmark_500_rows():
    """
    Criterios de Aceptación:
    (1) Identifica correctamente el 100% de aulas libres en un archivo de 500 filas.
    (2) Tiempo de procesamiento <= 3.0 s (benchmark de rendimiento RNF03).
    (3) Las reservas activas no se corrompen ni pierden.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Aula", "Día", "Hora Inicio", "Hora Fin", "Ocupación"])

    # Generar 500 filas sintéticas: 250 libres y 250 ocupadas
    total_filas = 500
    esperadas_libres = 250
    for i in range(1, total_filas + 1):
        aula = f"Aula {(i % 20) + 101}"
        dia = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"][i % 6]
        h_ini = f"{8 + (i % 8):02d}:00"
        h_fin = f"{10 + (i % 8):02d}:00"
        ocupacion = "LIBRE" if (i % 2 == 0) else f"Asignatura_{i}"
        ws.append([aula, dia, h_ini, h_fin, ocupacion])

    out = io.BytesIO()
    wb.save(out)
    excel_content = out.getvalue()

    reservas_vigentes = [{"id": r} for r in range(10)]

    t_inicio = time.perf_counter()
    res = ScheduleParserService.procesar_cronograma_administrador(
        filename="Cronograma_500_Filas_EPIS.xlsx",
        content=excel_content,
        reservas_activas=reservas_vigentes,
    )
    t_delta = time.perf_counter() - t_inicio

    # Validación estricta de criterios de aceptación
    assert res["total_aulas_libres_identificadas"] == esperadas_libres
    assert res["reservas_activas_preservadas"] == 10
    assert t_delta < 3.0, f"El tiempo de procesamiento ({t_delta:.3f} s) superó el umbral reglamentario de 3.0 s."
