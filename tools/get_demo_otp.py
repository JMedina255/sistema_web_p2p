"""
Herramienta de soporte para el presentador (DEMO-P2P-01):
Permite consultar o emitir un código OTP para cuentas de demostración local.
EPIS-UPT - Sistema Web P2P de Mentorías Académicas.
"""

import argparse
import sys
from pathlib import Path

# Añadir aplicacion/backend al sys.path
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / "aplicacion" / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from app.db.session import get_session
from app.services.auth_service import AuthService

ACCOUNTS = {
    "student": "estudiante.demo@upt.pe",
    "mentor": "mentor.demo@upt.pe",
    "admin": "admin.demo@upt.pe",
    "student_std": "2022074255@upt.pe",
    "mentor_std": "2022073504@upt.pe",
    "admin_std": "admin.epis@upt.pe",
}


def main():
    parser = argparse.ArgumentParser(description="Recuperador de Códigos OTP para Presentación Académica Local.")
    parser.add_argument(
        "--email",
        "-e",
        default="estudiante.demo@upt.pe",
        help="Correo institucional a autenticar (ej: estudiante.demo@upt.pe o 2022074255@upt.pe)",
    )
    parser.add_argument(
        "--role",
        "-r",
        choices=["student", "mentor", "admin", "student_std", "mentor_std", "admin_std"],
        help="Alias de rol rápido para seleccionar la cuenta",
    )
    args = parser.parse_args()

    target_email = ACCOUNTS[args.role] if args.role else args.email

    try:
        settings.ENABLE_MOCK_OTP_HINTS = True
        db = next(get_session())
        resp = AuthService.request_otp(db=db, email=target_email)
        code = resp.mockCodeHint or "Consulte los logs del backend"

        print("=" * 60)
        print("  SISTEMA WEB P2P - CÓDIGO OTP DE DEMOSTRACIÓN")
        print("=" * 60)
        print(f"  Usuario : {target_email}")
        print(f"  Código  : {code}")
        print(f"  Validez : {resp.cooldownSeconds}s cooldown")
        print("=" * 60)
    except Exception as exc:
        print(f"[-] Error generando OTP para {target_email}: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
