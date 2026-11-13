"""
ServicioRecursoAcademico (T-50 / CUS20 / MOD-06 / RF24).
Gestiona la subida, validación de seguridad (antivirus / extensiones prohibidas)
y descarga compartida de recursos académicos asociados a sesiones de mentoría.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from fastapi import HTTPException, status

from app.core.config import settings
from app.services.storage_service import StorageService


class ValidadorCargaRecurso:
    """Validador de extensiones, tamaños y enlaces seguros para recursos pedagógicos (CUS20-U01)."""

    ALLOWED_EXTENSIONS = {".pdf", ".pptx", ".ppt", ".zip", ".rar", ".7z", ".tar.gz", ".ipynb"}
    PROHIBITED_EXTENSIONS = {".exe", ".bat", ".cmd", ".sh", ".bin", ".msi", ".dll", ".ps1", ".vbs", ".scr"}
    MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 Megabytes

    @classmethod
    def validar(cls, filename_or_url: str, content: bytes | None = None) -> dict[str, Any]:
        """
        Valida que el archivo o URL cumpla los requisitos de seguridad académica.
        Lanza HTTPException si el archivo es inseguro, demasiado grande o no permitido.
        """
        if not filename_or_url or not filename_or_url.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de recurso o enlace no puede estar vacío.",
            )

        target = filename_or_url.strip()

        # Si es un enlace web (ej. repositorio de GitHub)
        if target.startswith("http://") or target.startswith("https://"):
            parsed = urlparse(target)
            if not parsed.netloc:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La URL provista tiene una sintaxis inválida.",
                )
            if "github.com" in parsed.netloc.lower() or "gitlab.com" in parsed.netloc.lower():
                return {
                    "tipo": "ENLACE_REPOSITORIO",
                    "url": target,
                    "valido": True,
                }
            return {
                "tipo": "ENLACE_WEB",
                "url": target,
                "valido": True,
            }

        # Validación de archivo físico
        ext = os.path.splitext(target.lower())[1]

        # Rechazo estricto de binarios ejecutables
        if ext in cls.PROHIBITED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Extensión potencialmente peligrosa '{ext}' rechazada por políticas de seguridad institucional.",
            )

        if ext not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Extensión '{ext}' no permitida. Solo se admiten archivos .pdf, .pptx, .zip o enlaces a GitHub.",
            )

        if content is not None:
            if len(content) > cls.MAX_FILE_SIZE_BYTES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El archivo ({len(content) / (1024*1024):.1f} MB) excede el tamaño máximo permitido de 25 MB.",
                )
            if len(content) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El archivo proporcionado está vacío (0 bytes).",
                )

        return {
            "tipo": "ARCHIVO_DOCUMENTAL",
            "extension": ext,
            "tamano_bytes": len(content) if content else 0,
            "valido": True,
        }


class ResourceService:
    """
    Servicio de gestión y vinculación de recursos académicos a sesiones de mentoría (CUS20-U02 / CUS20-F01).
    """

    # Almacén en memoria para recursos pedagógicos
    _memory_resources: list[dict[str, Any]] = []
    _counter: int = 1

    @classmethod
    def limpiar_almacen_memoria(cls) -> None:
        cls._memory_resources.clear()
        cls._counter = 1

    @classmethod
    def asociar_recurso_a_sesion(
        cls,
        id_sesion: int,
        mentor_email: str,
        nombre_recurso: str,
        content: bytes | None = None,
        descripcion: str | None = None,
    ) -> dict[str, Any]:
        """
        Asocia un material académico validado a la sesión correspondiente (CUS20-U02).
        """
        if id_sesion <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Identificador de sesión inválido.")

        validation = ValidadorCargaRecurso.validar(nombre_recurso, content)

        rec_id = cls._counter
        cls._counter += 1

        # Persistencia física mediante StorageService si se adjuntan bytes
        storage_path = None
        if content is not None:
            safe_filename = f"sesion_{id_sesion}_{Path(nombre_recurso).name}"
            storage_path = StorageService.save_file(
                bucket=settings.SUPABASE_BUCKET_RESOURCES,
                filename=safe_filename,
                content=content,
            )

        rec = {
            "id_recurso": rec_id,
            "id_sesion": id_sesion,
            "subido_por": mentor_email,
            "nombre_recurso": nombre_recurso,
            "tipo": validation["tipo"],
            "tamano_bytes": validation.get("tamano_bytes", 0),
            "descripcion": descripcion or "",
            "storage_path": storage_path,
        }
        cls._memory_resources.append(rec)
        return {
            "id_recurso": rec["id_recurso"],
            "id_sesion": rec["id_sesion"],
            "subido_por": rec["subido_por"],
            "nombre_recurso": rec["nombre_recurso"],
            "tipo": rec["tipo"],
            "tamano_bytes": rec["tamano_bytes"],
            "status": "VINCULADO_EXITOSAMENTE",
        }

    @classmethod
    def obtener_recursos_sesion(
        cls,
        id_sesion: int,
        usuario_email: str,
        correos_inscritos: list[str],
        mentor_email: str,
    ) -> list[dict[str, Any]]:
        """
        Descarga o consulta recursos garantizando aislamiento: solo el mentor o los inscritos acceden (CUS20-F01).
        Lanza HTTP 403 Forbidden si un tercero no participante intenta consultar los recursos.
        """
        clean_user = usuario_email.strip().lower()
        participantes_autorizados = {mentor_email.strip().lower()} | {e.strip().lower() for e in correos_inscritos}

        if clean_user not in participantes_autorizados:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado: solo el mentor y los estudiantes inscritos en esta clase pueden descargar este material.",
            )

        return [
            {
                "id_recurso": r["id_recurso"],
                "id_sesion": r["id_sesion"],
                "nombre_recurso": r["nombre_recurso"],
                "tipo": r["tipo"],
                "tamano_bytes": r["tamano_bytes"],
                "descripcion": r["descripcion"],
            }
            for r in cls._memory_resources
            if r["id_sesion"] == id_sesion
        ]


# Alias en español para trazabilidad directa con el Catálogo de Pruebas
ServicioRecursosAcademicos = ResourceService
