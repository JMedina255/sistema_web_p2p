"""
Wrapper de conveniencia para aprovisionamiento de escenarios DEMO-01 a DEMO-06.
Sistema Web P2P de Mentorías Académicas — EPIS UPT.
"""

import sys
from pathlib import Path

# Añadir aplicacion/backend al sys.path
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / "aplicacion" / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from scripts.prepare_demo_scenarios import main

if __name__ == "__main__":
    main()
