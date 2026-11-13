"""
Pruebas automatizadas de la API REST de Espacios y Parser de Horarios (RF10 / CUS11 / MOD-04).
"""

import io
import openpyxl
import pytest
from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.main import app

client = TestClient(app)


def get_admin_headers() -> dict[str, str]:
    token = create_access_token(data={"sub": "admin.infra@upt.pe", "roles": ["administrador"]})
    return {"Authorization": f"Bearer {token}"}


def get_student_headers() -> dict[str, str]:
    token = create_access_token(data={"sub": "estudiante@upt.pe", "roles": ["mentoreado"]})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_excel_file_bytes() -> bytes:
    """Genera un archivo Excel (.xlsx) válido en memoria con aulas libres y ocupadas."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Aulas_EPIS"
    ws.append(["Aula", "Día", "Hora Inicio", "Hora Fin", "Ocupación"])
    ws.append(["Lab 01", "Lunes", "08:00", "10:00", "LIBRE"])
    ws.append(["Lab 01", "Lunes", "10:00", "12:00", "Programación Web"])
    ws.append(["Lab 03", "Miércoles", "14:00", "16:00", "DISPONIBLE"])
    ws.append(["Aula 204", "Viernes", "16:00", "18:00", ""])
    out = io.BytesIO()
    wb.save(out)
    return out.getvalue()


def test_import_schedule_as_admin_success(sample_excel_file_bytes: bytes):
    """RF10 / CUS11: Administrador sube cronograma en Excel y recibe resumen estructurado."""
    headers = get_admin_headers()
    files = {
        "file": ("cronograma_oficial_epis_2026.xlsx", sample_excel_file_bytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }
    response = client.post("/api/v1/spaces/import-schedule", files=files, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PROCESADO_EXITOSAMENTE"
    assert data["archivo"] == "cronograma_oficial_epis_2026.xlsx"
    assert data["total_aulas_libres_identificadas"] == 3
    aulas = [s["aula"] for s in data["aulas_libres"]]
    assert "Lab 01" in aulas
    assert "Lab 03" in aulas
    assert "Aula 204" in aulas


def test_import_schedule_forbidden_for_non_admin(sample_excel_file_bytes: bytes):
    """RF10 / SEC: Usuario no administrador no puede procesar cronogramas (403 Forbidden)."""
    headers = get_student_headers()
    files = {
        "file": ("cronograma.xlsx", sample_excel_file_bytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }
    response = client.post("/api/v1/spaces/import-schedule", files=files, headers=headers)
    assert response.status_code == 403


def test_import_schedule_unauthorized_without_token(sample_excel_file_bytes: bytes):
    """RF10 / SEC: Petición anónima es rechazada con 401 Unauthorized."""
    files = {
        "file": ("cronograma.xlsx", sample_excel_file_bytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }
    response = client.post("/api/v1/spaces/import-schedule", files=files)
    assert response.status_code == 401


def test_import_schedule_corrupt_file_returns_400():
    """RF10 / CUS11-U03: Archivo corrupto o no soportado retorna 400 Bad Request."""
    headers = get_admin_headers()
    corrupt_bytes = b"Esto no es un archivo excel ni pdf valido, solo texto basura."
    files = {
        "file": ("corrupto.xlsx", corrupt_bytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }
    response = client.post("/api/v1/spaces/import-schedule", files=files, headers=headers)
    assert response.status_code == 400
    assert "firma ZIP" in response.json()["detail"] or "inválido" in response.json()["detail"]


def test_get_free_physical_slots():
    """RF09 / RF10: Consulta franjas libres y permite filtrar por día y aula."""
    response = client.get("/api/v1/spaces/free-slots")
    assert response.status_code == 200
    slots = response.json()
    assert isinstance(slots, list)
    assert len(slots) > 0

    # Filtrar por día
    resp_lunes = client.get("/api/v1/spaces/free-slots?dia=Lunes")
    assert resp_lunes.status_code == 200
    for s in resp_lunes.json():
        assert s["dia"].lower() == "lunes"


def test_get_available_classrooms():
    """RF10: Listado de recintos físicos disponibles para mentorías presenciales."""
    response = client.get("/api/v1/spaces/classrooms")
    assert response.status_code == 200
    data = response.json()
    assert "aulas" in data
    assert data["total"] > 0
    assert isinstance(data["aulas"], list)
