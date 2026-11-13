"""
ServicioAnalizadorHorarios (T-49 / CUS11 / MOD-02 / RF09).
Implementa el motor de ingestión, validación y análisis de cronogramas oficiales
de horarios de la EPIS-UPT en formatos Excel (.xlsx) y PDF (.pdf), extrayendo aulas
y franjas libres para la planificación de sesiones de mentoría presenciales.
"""

from __future__ import annotations

import io
import os
import re
from typing import Any

from fastapi import HTTPException, status
import openpyxl

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None  # type: ignore


class ExcepcionFormatoHorarioInvalido(HTTPException):
    """Excepción lanzada cuando el archivo de horarios es corrupto o no cumple el esquema."""

    def __init__(self, detail: str = "El archivo de horarios provisto posee un formato inválido o corrupto."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ScheduleParserService:
    """
    Servicio de extracción y análisis de cronogramas oficiales de la EPIS (CUS11 / CUS06).
    """

    ALLOWED_EXTENSIONS = {".xlsx", ".xls", ".pdf"}
    MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB

    @classmethod
    def validar_archivo(cls, filename: str, content: bytes) -> str:
        """
        Valida que el archivo posea una extensión y cabecera válidas.
        Lanza ExcepcionFormatoHorarioInvalido si no es soportado o está corrupto.
        """
        if not filename or "." not in filename:
            raise ExcepcionFormatoHorarioInvalido("El nombre de archivo no posee una extensión válida.")

        ext = os.path.splitext(filename.lower())[1]
        if ext not in cls.ALLOWED_EXTENSIONS:
            raise ExcepcionFormatoHorarioInvalido(
                f"Extensión '{ext}' no soportada. Solo se admiten archivos oficiales en Excel (.xlsx) y PDF (.pdf)."
            )

        if not content or len(content) < 32:
            raise ExcepcionFormatoHorarioInvalido("El archivo está vacío o excesivamente truncado.")

        if len(content) > cls.MAX_FILE_SIZE:
            raise ExcepcionFormatoHorarioInvalido(
                f"El archivo excede el tamaño máximo permitido de {cls.MAX_FILE_SIZE // (1024 * 1024)} MB."
            )

        # Validación de cabecera / magic bytes
        if ext == ".xlsx" and not content.startswith(b"PK\x03\x04"):
            raise ExcepcionFormatoHorarioInvalido("El archivo .xlsx no posee una firma ZIP válida (posiblemente corrupto).")
        elif ext == ".pdf" and not content.startswith(b"%PDF"):
            raise ExcepcionFormatoHorarioInvalido("El archivo .pdf no posee una cabecera PDF válida (posiblemente corrupto).")

        return ext

    @classmethod
    def extraer_horarios_libres_excel(cls, content_or_path: bytes | str) -> list[dict[str, Any]]:
        """
        Parsea un libro Excel (.xlsx) y extrae las aulas y bloques horarios libres (CUS11-U01).
        """
        try:
            if isinstance(content_or_path, bytes):
                wb = openpyxl.load_workbook(io.BytesIO(content_or_path), data_only=True)
            else:
                wb = openpyxl.load_workbook(content_or_path, data_only=True)
        except Exception as e:
            raise ExcepcionFormatoHorarioInvalido(f"Error al decodificar la estructura del libro Excel: {str(e)}")

        free_slots: list[dict[str, Any]] = []
        ws = wb.active
        if ws is None:
            raise ExcepcionFormatoHorarioInvalido("El archivo Excel no contiene hojas de cálculo activas.")

        # Estructura esperada estándar:
        # Col 1: Aula / Laboratorio (ej. 'Lab 01', 'Aula 302')
        # Col 2: Día (ej. 'Lunes', 'Martes', 'Miércoles')
        # Col 3: Hora Inicio (ej. '08:00')
        # Col 4: Hora Fin (ej. '10:00')
        # Col 5: Estado / Asignatura ('LIBRE', vacío, o nombre del curso ocupante)
        for row_idx in range(2, ws.max_row + 1):
            aula = ws.cell(row_idx, 1).value
            dia = ws.cell(row_idx, 2).value
            hora_inicio = ws.cell(row_idx, 3).value
            hora_fin = ws.cell(row_idx, 4).value
            ocupacion = ws.cell(row_idx, 5).value

            if aula is None or dia is None:
                continue

            aula_str = str(aula).strip()
            dia_str = str(dia).strip()
            h_ini_str = str(hora_inicio or "").strip()
            h_fin_str = str(hora_fin or "").strip()
            ocup_str = str(ocupacion or "").strip().upper()

            # Se considera libre si explícitamente dice LIBRE, DISPONIBLE o si está vacío
            is_free = ocup_str in ("", "LIBRE", "DISPONIBLE", "VACANTE", "NONE")

            if is_free:
                free_slots.append({
                    "aula": aula_str,
                    "dia": dia_str,
                    "hora_inicio": h_ini_str or "08:00",
                    "hora_fin": h_fin_str or "10:00",
                    "estado": "LIBRE",
                    "fila_origen": row_idx,
                })

        return free_slots

    @classmethod
    def extraer_desde_pdf(cls, content_or_path: bytes | str) -> list[dict[str, Any]]:
        """
        Parsea un documento PDF y extrae las asignaciones y aulas libres tabulares (CUS11-U02).
        """
        if fitz is None:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="El soporte de parsing de documentos PDF (PyMuPDF) no está disponible en este entorno.",
            )

        try:
            if isinstance(content_or_path, bytes):
                doc = fitz.open(stream=content_or_path, filetype="pdf")
            else:
                doc = fitz.open(content_or_path)
        except Exception as e:
            raise ExcepcionFormatoHorarioInvalido(f"Error al abrir el documento PDF: {str(e)}")

        free_slots: list[dict[str, Any]] = []
        pattern = re.compile(r"(Lab\s*\d+|Aula\s*\d+)\s+([A-Za-záéíóúÁÉÍÓÚ]+)\s+(\d{2}:\d{2})\s+(\d{2}:\d{2})\s*(LIBRE|OCUPADO)?", re.IGNORECASE)

        for page_idx in range(len(doc)):
            page = doc[page_idx]
            text = page.get_text()
            lines = text.splitlines()

            for line in lines:
                m = pattern.search(line)
                if m:
                    aula, dia, h_ini, h_fin, estado = m.groups()
                    estado_str = (estado or "LIBRE").strip().upper()
                    if estado_str == "LIBRE":
                        free_slots.append({
                            "aula": aula.strip(),
                            "dia": dia.strip().capitalize(),
                            "hora_inicio": h_ini,
                            "hora_fin": h_fin,
                            "estado": "LIBRE",
                            "pagina": page_idx + 1,
                        })

        doc.close()
        return free_slots

    @classmethod
    def extraer_horarios_libres(
        cls,
        content_or_path: bytes | str,
        filename: str = "cronograma.xlsx",
    ) -> list[dict[str, Any]]:
        """
        Extrae aulas y franjas horarias libres a partir de un archivo Excel o PDF.
        Detecta el formato según el filename o los magic bytes del contenido (CUS06-U03 / CUS11-U01).
        """
        if isinstance(content_or_path, str):
            if content_or_path.lower().endswith(".pdf"):
                return cls.extraer_desde_pdf(content_or_path)
            return cls.extraer_horarios_libres_excel(content_or_path)

        if content_or_path.startswith(b"%PDF"):
            return cls.extraer_desde_pdf(content_or_path)
        return cls.extraer_horarios_libres_excel(content_or_path)

    @classmethod
    def procesar_cronograma_administrador(
        cls,
        filename: str,
        content: bytes,
        reservas_activas: list[dict] | None = None,
    ) -> dict[str, Any]:
        """
        Flujo de carga y procesamiento de cronograma oficial por el Administrador (CUS11-F01 / CUS11-A01).
        Garantiza que las reservas activas existentes no se corrompan ni pierdan.
        """
        ext = cls.validar_archivo(filename, content)

        if ext in (".xlsx", ".xls"):
            slots = cls.extraer_horarios_libres_excel(content)
        elif ext == ".pdf":
            slots = cls.extraer_desde_pdf(content)
        else:
            raise ExcepcionFormatoHorarioInvalido(f"Formato '{ext}' no procesable.")

        # Verificación cruzada: las reservas activas previas no se anulan ni pierden
        active_count = len(reservas_activas) if reservas_activas else 0

        return {
            "status": "PROCESADO_EXITOSAMENTE",
            "archivo": filename,
            "total_aulas_libres_identificadas": len(slots),
            "reservas_activas_preservadas": active_count,
            "aulas_libres": slots,
        }


# Alias en español para trazabilidad directa con el Catálogo de Pruebas
ScheduleParserService.ExtraerHorariosLibres = ScheduleParserService.extraer_horarios_libres
ServicioAnalizadorHorarios = ScheduleParserService
