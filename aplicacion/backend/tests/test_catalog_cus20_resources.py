"""
Suite de Pruebas Automatizadas para CUS20 — Compartir y Descargar Recursos Académicos (MOD-06 / RF24).
Trazabilidad directa con el Catálogo Oficial de Pruebas EPIS-UPT:
- CUS20-U01: Validar tipo y tamaño de archivo permitido al subir recurso
- CUS20-U02: Asociar recurso subido a la sesión correspondiente
- CUS20-F01: Flujo de compartir y descargar material pedagógico de una clase
"""

import pytest
from fastapi import HTTPException

from app.services.resource_service import (
    ResourceService,
    ServicioRecursosAcademicos,
    ValidadorCargaRecurso,
)


@pytest.fixture(autouse=True)
def setup_teardown_resources():
    ResourceService.limpiar_almacen_memoria()
    yield
    ResourceService.limpiar_almacen_memoria()


# ==============================================================================
# CUS20-U01: Validar tipo y tamaño de archivo permitido al subir recurso
# ==============================================================================
def test_cus20_u01_validate_file_type_and_size():
    """
    Verifica que ValidadorCargaRecurso acepte tipos permitidos (.pdf, .pptx, .zip, GitHub)
    y rechace binarios ejecutables (.exe, .bat), archivos vacíos o que excedan 25 MB.
    """
    # 1. Enlace de GitHub válido
    val_gh = ValidadorCargaRecurso.validar("https://github.com/epis-upt/algoritmos-2026")
    assert val_gh["valido"] is True
    assert val_gh["tipo"] == "ENLACE_REPOSITORIO"

    # 2. Archivo PDF válido con contenido
    val_pdf = ValidadorCargaRecurso.validar("clase_01_estructuras.pdf", b"%PDF-1.4 mock content...")
    assert val_pdf["valido"] is True
    assert val_pdf["extension"] == ".pdf"

    # 3. Archivo PPTX válido
    val_pptx = ValidadorCargaRecurso.validar("diapositivas_unidad_2.pptx", b"mock binary data...")
    assert val_pptx["valido"] is True
    assert val_pptx["extension"] == ".pptx"

    # 4. Rechazo estricto de archivo ejecutable peligroso (.exe)
    with pytest.raises(HTTPException) as exc_exe:
        ValidadorCargaRecurso.validar("malware_instalador.exe", b"MZ\x90...")
    assert exc_exe.value.status_code == 400
    assert "peligrosa '.exe' rechazada" in str(exc_exe.value.detail)

    # 5. Rechazo estricto de script por lotes (.bat)
    with pytest.raises(HTTPException) as exc_bat:
        ValidadorCargaRecurso.validar("script_ataque.bat", b"@echo off")
    assert exc_bat.value.status_code == 400

    # 6. Rechazo de archivo que excede 25 MB
    contenido_excesivo = b"0" * (26 * 1024 * 1024)
    with pytest.raises(HTTPException) as exc_size:
        ValidadorCargaRecurso.validar("archivo_pesado.zip", contenido_excesivo)
    assert exc_size.value.status_code == 400
    assert "excede el tamaño máximo permitido de 25 MB" in str(exc_size.value.detail)

    # 7. Rechazo de archivo vacío (0 bytes)
    with pytest.raises(HTTPException) as exc_empty:
        ValidadorCargaRecurso.validar("archivo_vacio.pdf", b"")
    assert exc_empty.value.status_code == 400
    assert "vacío" in str(exc_empty.value.detail)


# ==============================================================================
# CUS20-U02: Asociar recurso subido a la sesión correspondiente
# ==============================================================================
def test_cus20_u02_associate_resource_to_mentoring_session():
    """
    Verifica que ServicioRecursosAcademicos.asociar_recurso_a_sesion()
    asocie correctamente el material al identificador de la sesión con metadata íntegra.
    """
    res = ServicioRecursosAcademicos.asociar_recurso_a_sesion(
        id_sesion=101,
        mentor_email="mentor.renzo@upt.pe",
        nombre_recurso="Guia_Ejercicios_POO.pdf",
        content=b"%PDF-1.4 Mock de ejercicios practicos...",
        descripcion="Guía de ejercicios resueltos de programación orientada a objetos.",
    )

    assert res["status"] == "VINCULADO_EXITOSAMENTE"
    assert res["id_sesion"] == 101
    assert res["subido_por"] == "mentor.renzo@upt.pe"
    assert res["nombre_recurso"] == "Guia_Ejercicios_POO.pdf"
    assert res["tamano_bytes"] > 0

    # Rechazo si el id de sesión es inválido
    with pytest.raises(HTTPException) as exc_neg:
        ServicioRecursosAcademicos.asociar_recurso_a_sesion(
            id_sesion=0,
            mentor_email="mentor.renzo@upt.pe",
            nombre_recurso="archivo.pdf",
            content=b"%PDF...",
        )
    assert exc_neg.value.status_code == 400


# ==============================================================================
# CUS20-F01: Flujo de compartir y descargar material pedagógico de una clase
# ==============================================================================
def test_cus20_f01_share_and_download_resource_restricted_to_enrolled():
    """
    Verifica que el mentor y los mentoreados inscritos en la sesión puedan consultar/descargar
    los recursos, mientras que un usuario ajeno reciba HTTP 403 Forbidden.
    """
    id_sesion = 101
    mentor = "mentor.renzo@upt.pe"
    alumno_inscrito = "mentoreado.joan@upt.pe"
    alumno_ajeno = "intruso.externo@upt.pe"

    # 1. El mentor sube diapositivas y enlace a GitHub
    ResourceService.asociar_recurso_a_sesion(
        id_sesion=id_sesion,
        mentor_email=mentor,
        nombre_recurso="Diapositivas_Sesion_05.pptx",
        content=b"PPTX-BINARY-STREAM-DATA",
    )
    ResourceService.asociar_recurso_a_sesion(
        id_sesion=id_sesion,
        mentor_email=mentor,
        nombre_recurso="https://github.com/epis-upt/demo-poo-clase05",
    )

    # 2. El estudiante formalmente inscrito puede consultar los materiales
    recursos_estudiante = ResourceService.obtener_recursos_sesion(
        id_sesion=id_sesion,
        usuario_email=alumno_inscrito,
        correos_inscritos=[alumno_inscrito],
        mentor_email=mentor,
    )
    assert len(recursos_estudiante) == 2
    nombres = [r["nombre_recurso"] for r in recursos_estudiante]
    assert "Diapositivas_Sesion_05.pptx" in nombres
    assert "https://github.com/epis-upt/demo-poo-clase05" in nombres

    # 3. El mentor también puede consultar sus propios materiales subidos
    recursos_mentor = ResourceService.obtener_recursos_sesion(
        id_sesion=id_sesion,
        usuario_email=mentor,
        correos_inscritos=[alumno_inscrito],
        mentor_email=mentor,
    )
    assert len(recursos_mentor) == 2

    # 4. Un estudiante ajeno a la sesión recibe HTTP 403 Forbidden (Aislamiento de Privacidad)
    with pytest.raises(HTTPException) as exc_forb:
        ResourceService.obtener_recursos_sesion(
            id_sesion=id_sesion,
            usuario_email=alumno_ajeno,
            correos_inscritos=[alumno_inscrito],
            mentor_email=mentor,
        )
    assert exc_forb.value.status_code == 403
    assert "solo el mentor y los estudiantes inscritos" in str(exc_forb.value.detail)
