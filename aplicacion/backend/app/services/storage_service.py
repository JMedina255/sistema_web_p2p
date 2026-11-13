"""
Servicio de Almacenamiento Híbrido de Archivos (StorageService).
Soporta backend 'local' (por defecto en uploads/) y backend 'supabase'
mediante la API REST de Supabase Storage para persistir constancias PDF oficiales
y recursos académicos docentes de manera desacoplada y configurable.
"""

from __future__ import annotations

import logging
from pathlib import Path

import httpx

from app.core.config import settings

logger = logging.getLogger("app.storage")

_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent


class StorageService:
    """
    Gestor de persistencia física de archivos documentales y binarios:
    - Bucket 'certificados': Constancias oficiales y constancias demo PDF (RN-14 / T-44).
    - Bucket 'recursos_academicos': Archivos adjuntos a sesiones de mentoría (CUS20 / RF24).
    """

    @classmethod
    def _get_local_path(cls, bucket: str, filename: str) -> Path:
        """Calcula la ruta absoluta segura en el sistema de archivos local."""
        clean_bucket = bucket.strip("/\\")
        clean_filename = Path(filename).name  # Prevención estricta de Path Traversal
        base_dir = _BACKEND_ROOT / settings.STORAGE_LOCAL_DIR / clean_bucket
        base_dir.mkdir(parents=True, exist_ok=True)
        return base_dir / clean_filename

    @classmethod
    def save_file(
        cls,
        bucket: str,
        filename: str,
        content: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        """
        Guarda un archivo binario en el backend de almacenamiento configurado (local o supabase).
        Retorna la ruta relativa local o la URL del objeto en Supabase Storage.
        """
        backend = (settings.STORAGE_BACKEND or "local").lower().strip()

        # 1. Estrategia Supabase Storage (REST API)
        if backend == "supabase" and settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY:
            try:
                base_url = settings.SUPABASE_URL.rstrip("/")
                endpoint = f"{base_url}/storage/v1/object/{bucket}/{filename}"
                headers = {
                    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
                    "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                    "x-upsert": "true",
                    "Content-Type": content_type,
                }
                with httpx.Client(timeout=15.0) as client:
                    resp = client.post(endpoint, content=content, headers=headers)
                    if resp.status_code in (200, 201):
                        public_url = f"{base_url}/storage/v1/object/public/{bucket}/{filename}"
                        logger.info("Archivo %s persistido en Supabase Storage (%s)", filename, public_url)
                        return public_url
                    else:
                        logger.warning(
                            "Fallo al subir a Supabase Storage (%s: %s). Aplicando fallback a almacenamiento local.",
                            resp.status_code,
                            resp.text,
                        )
            except Exception as exc:
                logger.error("Excepción en Supabase Storage: %s. Aplicando fallback local.", exc)

        # 2. Estrategia Local (por defecto / fallback seguro)
        local_file = cls._get_local_path(bucket, filename)
        local_file.write_bytes(content)
        rel_path = f"{settings.STORAGE_LOCAL_DIR}/{bucket}/{local_file.name}".replace("\\", "/")
        logger.info("Archivo %s guardado en almacenamiento local (%s)", filename, rel_path)
        return rel_path

    @classmethod
    def get_file(cls, bucket: str, filename: str) -> bytes | None:
        """
        Recupera el contenido binario del archivo desde el backend correspondiente.
        Retorna bytes si existe, o None si no fue encontrado.
        """
        backend = (settings.STORAGE_BACKEND or "local").lower().strip()

        # Intento vía Supabase Storage si aplica
        if backend == "supabase" and settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY:
            try:
                base_url = settings.SUPABASE_URL.rstrip("/")
                endpoint = f"{base_url}/storage/v1/object/authenticated/{bucket}/{filename}"
                headers = {
                    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
                    "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                }
                with httpx.Client(timeout=15.0) as client:
                    resp = client.get(endpoint, headers=headers)
                    if resp.status_code == 200:
                        return resp.content
            except Exception as exc:
                logger.warning("Fallo al descargar de Supabase Storage: %s. Probando almacén local.", exc)

        # Intento vía Almacén Local
        local_file = cls._get_local_path(bucket, filename)
        if local_file.is_file():
            return local_file.read_bytes()

        return None

    @classmethod
    def delete_file(cls, bucket: str, filename: str) -> bool:
        """Elimina un archivo del almacenamiento."""
        backend = (settings.STORAGE_BACKEND or "local").lower().strip()
        deleted = False

        if backend == "supabase" and settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY:
            try:
                base_url = settings.SUPABASE_URL.rstrip("/")
                endpoint = f"{base_url}/storage/v1/object/{bucket}/{filename}"
                headers = {
                    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
                    "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                }
                with httpx.Client(timeout=10.0) as client:
                    resp = client.delete(endpoint, headers=headers)
                    if resp.status_code == 200:
                        deleted = True
            except Exception:
                pass

        local_file = cls._get_local_path(bucket, filename)
        if local_file.is_file():
            local_file.unlink()
            deleted = True

        return deleted

    @classmethod
    def file_exists(cls, bucket: str, filename: str) -> bool:
        """Verifica la existencia del archivo en almacenamiento local o en Supabase Storage."""
        local_file = cls._get_local_path(bucket, filename)
        if local_file.is_file():
            return True

        backend = (settings.STORAGE_BACKEND or "local").lower().strip()
        if backend == "supabase" and settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY:
            try:
                base_url = settings.SUPABASE_URL.rstrip("/")
                endpoint = f"{base_url}/storage/v1/object/authenticated/{bucket}/{filename}"
                headers = {
                    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
                    "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                }
                with httpx.Client(timeout=5.0) as client:
                    resp = client.get(endpoint, headers=headers)
                    if resp.status_code == 200:
                        return True
            except Exception:
                pass

        return False
