"""
Módulo de Identidad Institucional de la Universidad Privada de Tacna (UPT).
Gestiona las reglas de dominio (@virtual.upt.pe para alumnos, @upt.pe para docentes/administrativos)
y la extracción determinística de códigos de matrícula y metadatos formativos.
"""

import re
from typing import Any


def validate_upt_email(v: str) -> str:
    """
    Valida que la dirección de correo pertenezca a la Universidad Privada de Tacna:
    - @virtual.upt.pe (Cuentas Google Workspace de estudiantes)
    - @upt.pe (Cuentas institucionales directivas, administrativas y docentes)
    """
    clean_email = v.strip().lower()
    if not (clean_email.endswith("@virtual.upt.pe") or clean_email.endswith("@upt.pe")):
        raise ValueError(
            "El correo electrónico debe pertenecer al dominio institucional @virtual.upt.pe o @upt.pe (CUS01 / RN-01)"
        )

    # Validación sintáctica estándar RFC 5322 para ambos dominios
    email_regex = r"^[a-zA-Z0-9._%+-]+@(virtual\.upt\.pe|upt\.pe)$"
    if not re.match(email_regex, clean_email):
        raise ValueError("El formato del correo institucional es inválido")

    return clean_email


def parse_student_email(email: str) -> dict[str, Any]:
    """
    Analiza un correo institucional para determinar si corresponde a un estudiante
    y extrae determinísticamente sus atributos:
    - Nomenclatura oficial UPT para estudiantes:
      (inicial_nombre)(inicial_apellido_paterno)(codigo_estudiante)@virtual.upt.pe
      Ejemplo: ra2022073504@virtual.upt.pe -> Iniciales: R, A; Código: 2022073504
    """
    clean_email = email.strip().lower()

    if clean_email.endswith("@virtual.upt.pe"):
        student_regex = r"^([a-z])([a-z])(\d{8,10})@virtual\.upt\.pe$"
        match = re.match(student_regex, clean_email)
        if match:
            return {
                "es_estudiante": True,
                "inicial_nombre": match.group(1).upper(),
                "inicial_apellido": match.group(2).upper(),
                "codigo_estudiante": match.group(3),
                "dominio": "virtual.upt.pe",
                "clean_email": clean_email,
            }
        # Caso de cuenta estudiantil sin patrón estricto de dos iniciales
        student_fallback = r"^([a-z0-9._%+-]+)@virtual\.upt\.pe$"
        fallback_match = re.match(student_fallback, clean_email)
        raw_prefix = fallback_match.group(1) if fallback_match else clean_email.split("@")[0]
        digits = "".join(ch for ch in raw_prefix if ch.isdigit())
        return {
            "es_estudiante": True,
            "inicial_nombre": None,
            "inicial_apellido": None,
            "codigo_estudiante": digits if len(digits) >= 8 else raw_prefix,
            "dominio": "virtual.upt.pe",
            "clean_email": clean_email,
        }

    if clean_email.endswith("@upt.pe"):
        # Cuenta directiva, docente o administrativa (ej. admin.epis@upt.pe, 2022074255@upt.pe legado)
        raw_prefix = clean_email.split("@")[0]
        digits = "".join(ch for ch in raw_prefix if ch.isdigit())
        return {
            "es_estudiante": bool(len(digits) >= 8),
            "inicial_nombre": None,
            "inicial_apellido": None,
            "codigo_estudiante": digits if len(digits) >= 8 else None,
            "dominio": "upt.pe",
            "clean_email": clean_email,
        }

    return {
        "es_estudiante": False,
        "inicial_nombre": None,
        "inicial_apellido": None,
        "codigo_estudiante": None,
        "dominio": None,
        "clean_email": clean_email,
    }
