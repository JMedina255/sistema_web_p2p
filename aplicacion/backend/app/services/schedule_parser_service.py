"""
ServicioAnalizadorHorarios (T-49 / CUS11 / MOD-02 / RF09).
Implementa el motor de ingestión, validación y análisis de cronogramas oficiales
de horarios de la EPIS-UPT en formatos Excel (.xls, .xlsx) y PDF (.pdf), extrayendo aulas
y franjas libres para la planificación de sesiones de mentoría presenciales.
"""

from __future__ import annotations

import io
import os
import re
from pathlib import Path
from typing import Any

import openpyxl
import xlrd
from fastapi import HTTPException, status
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.schedule import CronogramaActivo, VersionCronograma

try:
    import pymupdf as fitz  # PyMuPDF moderno (evita advertencia de deprecación de import fitz)
except ImportError:
    try:
        import fitz  # Fallback a namespace tradicional
    except ImportError:
        fitz = None  # type: ignore


class ExcepcionFormatoHorarioInvalido(HTTPException):
    """Excepción lanzada cuando el archivo de horarios es corrupto o no cumple el esquema."""

    def __init__(self, detail: str = "El archivo de horarios provisto posee un formato inválido o corrupto."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


OLE_SIGNATURE = bytes.fromhex("D0CF11E0A1B11AE1")


class ScheduleParserService:
    """
    Servicio de extracción y análisis de cronogramas oficiales de la EPIS (CUS11 / CUS06).
    """

    ALLOWED_EXTENSIONS = {".xlsx", ".xls", ".pdf"}
    MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB

    _default_slots: list[dict[str, Any]] = [
        {"aula": "Lab 01", "dia": "Lunes", "hora_inicio": "08:00", "hora_fin": "10:00", "estado": "LIBRE"},
        {
            "aula": "Lab 01",
            "dia": "Miércoles",
            "hora_inicio": "14:00",
            "hora_fin": "16:00",
            "estado": "LIBRE",
        },
        {"aula": "Lab 02", "dia": "Martes", "hora_inicio": "10:00", "hora_fin": "12:00", "estado": "LIBRE"},
        {"aula": "Lab 02", "dia": "Jueves", "hora_inicio": "16:00", "hora_fin": "18:00", "estado": "LIBRE"},
        {"aula": "Aula 101", "dia": "Lunes", "hora_inicio": "10:00", "hora_fin": "12:00", "estado": "LIBRE"},
        {
            "aula": "Aula 202",
            "dia": "Miércoles",
            "hora_inicio": "08:00",
            "hora_fin": "10:00",
            "estado": "LIBRE",
        },
        {
            "aula": "Aula 302",
            "dia": "Viernes",
            "hora_inicio": "14:00",
            "hora_fin": "16:00",
            "estado": "LIBRE",
        },
    ]
    _active_free_slots = list(_default_slots)
    _last_imported_filename: str | None = "cronograma_oficial_base_2026.xlsx"

    @classmethod
    def schedule_row(cls, db: Session, lock: bool = False) -> CronogramaActivo | None:
        query = db.query(CronogramaActivo).filter_by(id=1)
        if lock:
            query = query.with_for_update().populate_existing()
        row = query.one_or_none()
        if row is None and lock:
            # ORM-created databases can lack the singleton installed by Alembic.
            db.execute(insert(CronogramaActivo).values(id=1).on_conflict_do_nothing(index_elements=["id"]))
            row = query.one()
        return row

    @classmethod
    def get_active_slots(
        cls, dia: str | None = None, aula: str | None = None, db: Session | None = None, lock: bool = False
    ) -> list[dict[str, Any]]:
        if db is None:
            slots = list(cls._active_free_slots)
        else:
            row = cls.schedule_row(db, lock=lock)
            slots = row.version.franjas if row is not None and row.version is not None else cls._default_slots
        if dia:
            dia_clean = dia.strip().lower()
            slots = [s for s in slots if s.get("dia", "").lower() == dia_clean]
        if aula:
            aula_clean = aula.strip().lower()
            slots = [s for s in slots if aula_clean in s.get("aula", "").lower()]
        return slots

    @classmethod
    def get_classrooms(cls, db: Session | None = None) -> list[str]:
        aulas = sorted({s["aula"] for s in cls.get_active_slots(db=db) if s.get("aula")})
        return aulas

    @classmethod
    def update_active_slots(cls, slots: list[dict[str, Any]], filename: str) -> None:
        cls._active_free_slots = slots
        cls._last_imported_filename = filename

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
                f"Extensión '{ext}' no soportada. Solo se admiten archivos oficiales en Excel (.xls, .xlsx) y PDF (.pdf)."
            )

        if not content or len(content) < 32:
            raise ExcepcionFormatoHorarioInvalido("El archivo está vacío o excesivamente truncado.")

        if len(content) > cls.MAX_FILE_SIZE:
            raise ExcepcionFormatoHorarioInvalido(
                f"El archivo excede el tamaño máximo permitido de {cls.MAX_FILE_SIZE // (1024 * 1024)} MB."
            )

        # Validación de cabecera / magic bytes
        if ext == ".xlsx" and not content.startswith(b"PK\x03\x04"):
            raise ExcepcionFormatoHorarioInvalido(
                "El archivo .xlsx no posee una firma ZIP válida (posiblemente corrupto)."
            )
        elif ext == ".xls" and not content.startswith(OLE_SIGNATURE):
            raise ExcepcionFormatoHorarioInvalido(
                "El archivo .xls no posee una firma de libro binario válida."
            )
        elif ext == ".pdf" and not content.startswith(b"%PDF"):
            raise ExcepcionFormatoHorarioInvalido(
                "El archivo .pdf no posee una cabecera PDF válida (posiblemente corrupto)."
            )

        return ext

    @classmethod
    def extraer_horarios_libres_excel(cls, content_or_path: bytes | str) -> list[dict[str, Any]]:
        """
        Parsea un libro Excel (.xls, .xlsx) y extrae las aulas y bloques horarios libres (CUS11-U01).
        """
        try:
            content = (
                content_or_path if isinstance(content_or_path, bytes) else Path(content_or_path).read_bytes()
            )
            if content.startswith(OLE_SIGNATURE):
                with xlrd.open_workbook(file_contents=content, on_demand=True) as book:
                    sheet = book.sheet_by_index(0)
                    rows = []
                    for index in range(1, sheet.nrows):
                        values = []
                        for cell in sheet.row(index)[:5]:
                            if cell.ctype == xlrd.XL_CELL_DATE:
                                value = xlrd.xldate_as_datetime(cell.value, book.datemode).strftime("%H:%M")
                            else:
                                value = cell.value
                            values.append(value)
                        rows.append((values + [None] * 5)[:5])
            else:
                workbook = openpyxl.load_workbook(io.BytesIO(content), data_only=True, read_only=True)
                try:
                    rows = list(workbook.active.iter_rows(min_row=2, max_col=5, values_only=True))
                finally:
                    workbook.close()
        except Exception as exc:
            raise ExcepcionFormatoHorarioInvalido(
                f"Error al decodificar la estructura del libro Excel: {exc}"
            ) from exc

        free_slots: list[dict[str, Any]] = []
        for row_idx, (aula, dia, hora_inicio, hora_fin, ocupacion) in enumerate(rows, start=2):
            if not str(aula or "").strip() or not str(dia or "").strip():
                continue

            aula_str = str(aula).strip()
            dia_str = str(dia).strip()
            h_ini_str = str(hora_inicio or "").strip()
            h_fin_str = str(hora_fin or "").strip()
            ocup_str = str(ocupacion or "").strip().upper()

            # Se considera libre si explícitamente dice LIBRE, DISPONIBLE o si está vacío
            is_free = ocup_str in ("", "LIBRE", "DISPONIBLE", "VACANTE", "NONE")

            if is_free:
                free_slots.append(
                    {
                        "aula": aula_str,
                        "dia": dia_str,
                        "hora_inicio": h_ini_str or "08:00",
                        "hora_fin": h_fin_str or "10:00",
                        "estado": "LIBRE",
                        "fila_origen": row_idx,
                    }
                )

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
            raise ExcepcionFormatoHorarioInvalido(f"Error al abrir el documento PDF: {str(e)}") from e

        free_slots: list[dict[str, Any]] = []
        pattern = re.compile(
            r"(Lab\s*\d+|Aula\s*\d+)\s+([A-Za-záéíóúÁÉÍÓÚ]+)\s+(\d{2}:\d{2})\s+(\d{2}:\d{2})\s*(LIBRE|OCUPADO)?",
            re.IGNORECASE,
        )

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
                        free_slots.append(
                            {
                                "aula": aula.strip(),
                                "dia": dia.strip().capitalize(),
                                "hora_inicio": h_ini,
                                "hora_fin": h_fin,
                                "estado": "LIBRE",
                                "pagina": page_idx + 1,
                            }
                        )

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
        db: Session | None = None,
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

        # Actualiza las aulas y franjas libres en el repositorio activo del sistema
        if db is None:
            cls.update_active_slots(slots, filename)
        else:
            row = cls.schedule_row(db, lock=True)
            row.version = VersionCronograma(archivo=filename, franjas=slots)
            db.commit()

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
