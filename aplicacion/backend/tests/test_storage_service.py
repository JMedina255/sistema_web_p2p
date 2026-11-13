"""
Pruebas Unitarias para el Servicio de Almacenamiento Híbrido (StorageService).
Valida:
- Guardado y lectura de archivos en backend 'local' con protección contra Path Traversal.
- Detección de existencia y eliminación física de archivos.
- Soporte para backend 'supabase' simulado mediante API REST con httpx.
- Fallback automático a almacenamiento local ante indisponibilidad o error de Supabase.
"""

from unittest.mock import MagicMock, patch

from app.core.config import settings
from app.services.storage_service import StorageService


def test_storage_service_local_save_get_delete(monkeypatch, tmp_path):
    """Verifica el ciclo completo de vida de un archivo en almacenamiento local."""
    monkeypatch.setattr(settings, "STORAGE_BACKEND", "local")
    monkeypatch.setattr(settings, "STORAGE_LOCAL_DIR", "uploads_test_temp")

    bucket = "certificados_test"
    filename = "CERT-2026-TEST-0001.pdf"
    content = b"%PDF-1.4 Official Certificate Content Testing Binary Stream"

    # 1. Guardar archivo
    saved_path = StorageService.save_file(
        bucket=bucket,
        filename=filename,
        content=content,
        content_type="application/pdf",
    )
    assert "uploads_test_temp/certificados_test/CERT-2026-TEST-0001.pdf" in saved_path

    # 2. Verificar existencia
    assert StorageService.file_exists(bucket, filename) is True

    # 3. Leer archivo y verificar fidelidad binaria
    retrieved_bytes = StorageService.get_file(bucket, filename)
    assert retrieved_bytes == content

    # 4. Eliminar archivo
    deleted = StorageService.delete_file(bucket, filename)
    assert deleted is True
    assert StorageService.file_exists(bucket, filename) is False

    # 5. Archivo inexistente retorna None
    assert StorageService.get_file(bucket, "NON_EXISTENT.pdf") is None


def test_storage_service_path_traversal_prevention(monkeypatch):
    """Verifica que nombres de archivo maliciosos con '../' sean saneados por Path(filename).name."""
    monkeypatch.setattr(settings, "STORAGE_BACKEND", "local")
    monkeypatch.setattr(settings, "STORAGE_LOCAL_DIR", "uploads_test_temp")

    bucket = "seguridad"
    malicious_filename = "../../../etc/passwd.pdf"
    content = b"Safe content"

    path = StorageService.save_file(bucket, malicious_filename, content)
    # Debe haber aislado el archivo únicamente a su nombre base
    assert "passwd.pdf" in path
    assert ".." not in path
    StorageService.delete_file(bucket, "passwd.pdf")


def test_storage_service_supabase_mode_success(monkeypatch):
    """Verifica que en backend 'supabase' invoque la API REST con las cabeceras de autorización y service_role."""
    monkeypatch.setattr(settings, "STORAGE_BACKEND", "supabase")
    monkeypatch.setattr(settings, "SUPABASE_URL", "https://xyz.supabase.co")
    monkeypatch.setattr(settings, "SUPABASE_SERVICE_ROLE_KEY", "secret-service-role-key")

    mock_resp_post = MagicMock(status_code=200)
    mock_resp_get = MagicMock(status_code=200, content=b"Supabase binary content")

    with patch("httpx.Client") as mock_client_cls:
        client_instance = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = client_instance
        client_instance.post.return_value = mock_resp_post
        client_instance.get.return_value = mock_resp_get

        # 1. Guardar archivo en Supabase
        url = StorageService.save_file("certificados", "cert.pdf", b"pdf data", "application/pdf")
        assert url == "https://xyz.supabase.co/storage/v1/object/public/certificados/cert.pdf"
        client_instance.post.assert_called_once()
        args, kwargs = client_instance.post.call_args
        assert kwargs["headers"]["Authorization"] == "Bearer secret-service-role-key"

        # 2. Obtener archivo desde Supabase
        data = StorageService.get_file("certificados", "cert.pdf")
        assert data == b"Supabase binary content"
        client_instance.get.assert_called_once()


def test_storage_service_supabase_fallback_to_local_on_error(monkeypatch):
    """Verifica que si Supabase Storage responde con error, el sistema recurra automáticamente al almacenamiento local."""
    monkeypatch.setattr(settings, "STORAGE_BACKEND", "supabase")
    monkeypatch.setattr(settings, "SUPABASE_URL", "https://xyz.supabase.co")
    monkeypatch.setattr(settings, "SUPABASE_SERVICE_ROLE_KEY", "secret-key")
    monkeypatch.setattr(settings, "STORAGE_LOCAL_DIR", "uploads_test_temp")

    mock_resp_error = MagicMock(status_code=500, text="Internal Server Error")

    with patch("httpx.Client") as mock_client_cls:
        client_instance = MagicMock()
        mock_client_cls.return_value.__enter__.return_value = client_instance
        client_instance.post.return_value = mock_resp_error

        # Debe guardar en local como fallback
        path = StorageService.save_file("certificados", "fallback_test.pdf", b"safe bytes")
        assert "uploads_test_temp/certificados/fallback_test.pdf" in path
        assert StorageService.file_exists("certificados", "fallback_test.pdf") is True

        StorageService.delete_file("certificados", "fallback_test.pdf")
