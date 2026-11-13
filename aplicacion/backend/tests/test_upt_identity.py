import pytest
from app.core.identity import parse_student_email, validate_upt_email


def test_validate_upt_email_valid_domains():
    """Valida correos válidos de estudiantes (@virtual.upt.pe) y directivos/docentes (@upt.pe)."""
    assert validate_upt_email("ra2022073504@virtual.upt.pe") == "ra2022073504@virtual.upt.pe"
    assert validate_upt_email("jm2022074255@virtual.upt.pe") == "jm2022074255@virtual.upt.pe"
    assert validate_upt_email("admin.epis@upt.pe") == "admin.epis@upt.pe"
    assert validate_upt_email("docente@upt.pe") == "docente@upt.pe"
    # Sensibilidad a mayúsculas y espacios
    assert validate_upt_email("  RA2022073504@VIRTUAL.UPT.PE  ") == "ra2022073504@virtual.upt.pe"


def test_validate_upt_email_invalid_domains():
    """Rechaza correos de dominios no autorizados (gmail, hotmail, otros)."""
    with pytest.raises(ValueError, match="El correo electrónico debe pertenecer al dominio institucional"):
        validate_upt_email("estudiante@gmail.com")

    with pytest.raises(ValueError, match="El correo electrónico debe pertenecer al dominio institucional"):
        validate_upt_email("hacker@outlook.com")

    with pytest.raises(ValueError, match="El formato del correo institucional es inválido"):
        validate_upt_email("invalido@@virtual.upt.pe")


def test_parse_student_email_strict_structure():
    """Verifica la extracción determinística de iniciales y código de estudiante."""
    parsed = parse_student_email("ra2022073504@virtual.upt.pe")
    assert parsed["es_estudiante"] is True
    assert parsed["inicial_nombre"] == "R"
    assert parsed["inicial_apellido"] == "A"
    assert parsed["codigo_estudiante"] == "2022073504"
    assert parsed["dominio"] == "virtual.upt.pe"


def test_parse_student_email_administrative_and_fallback():
    """Verifica el comportamiento con cuentas administrativas y casos de respaldo."""
    # Cuenta administrativa
    parsed_admin = parse_student_email("admin.epis@upt.pe")
    assert parsed_admin["es_estudiante"] is False
    assert parsed_admin["codigo_estudiante"] is None
    assert parsed_admin["dominio"] == "upt.pe"

    # Cuenta de estudiante con código legado numérico @upt.pe
    parsed_legacy = parse_student_email("2022074255@upt.pe")
    assert parsed_legacy["es_estudiante"] is True
    assert parsed_legacy["codigo_estudiante"] == "2022074255"

    # Correo no institucional
    parsed_external = parse_student_email("persona@gmail.com")
    assert parsed_external["es_estudiante"] is False
    assert parsed_external["codigo_estudiante"] == None
