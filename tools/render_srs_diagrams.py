# -*- coding: utf-8 -*-
"""
Reproducible PlantUML Renderer for SRS Diagrams.
Renders all .puml files in docs/diseño/diagramas/srs/puml/ into docs/diseño/diagramas/srs/img/*.png
"""

import os
import sys
import glob
import subprocess
import urllib.request
import time

PLANTUML_JAR = os.path.abspath("tools/plantuml.jar")
PLANTUML_URL = "https://github.com/plantuml/plantuml/releases/download/v1.2024.7/plantuml-1.2024.7.jar"

PUML_DIR = os.path.abspath("docs/diseño/diagramas/srs/puml")
IMG_DIR = os.path.abspath("docs/diseño/diagramas/srs/img")

def ensure_plantuml_jar():
    if not os.path.exists(PLANTUML_JAR) or os.path.getsize(PLANTUML_JAR) < 1000000:
        print(f"Descargando plantuml.jar desde {PLANTUML_URL}...")
        urllib.request.urlretrieve(PLANTUML_URL, PLANTUML_JAR)
        print(f"Descargado exitosamente ({os.path.getsize(PLANTUML_JAR)} bytes).")
    else:
        print(f"plantuml.jar disponible ({os.path.getsize(PLANTUML_JAR)} bytes).")

def render_diagrams():
    ensure_plantuml_jar()
    os.makedirs(IMG_DIR, exist_ok=True)
    
    puml_files = glob.glob(os.path.join(PUML_DIR, "*.puml"))
    total_puml = len(puml_files)
    print(f"Total de diagramas .puml a procesar: {total_puml}")
    
    if total_puml == 0:
        print("ERROR: No se encontraron archivos .puml en", PUML_DIR)
        sys.exit(1)

    t0 = time.time()
    
    # Run PlantUML in batch mode
    cmd = [
        "java",
        "-DPLANTUML_LIMIT_SIZE=16384",
        "-Djava.awt.headless=true",
        "-jar",
        PLANTUML_JAR,
        "-tpng",
        "-charset", "UTF-8",
        os.path.join(PUML_DIR, "*.puml"),
        "-o",
        IMG_DIR
    ]
    
    print("Ejecutando renderizado por lotes con PlantUML y Graphviz...")
    proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    
    duration = time.time() - t0
    print(f"Proceso concluido en {duration:.2f} segundos.")
    
    if proc.stderr:
        print("Salida de stderr (advertencias/errores):")
        print(proc.stderr[:1000])

    # Verification
    png_files = glob.glob(os.path.join(IMG_DIR, "*.png"))
    total_png = len(png_files)
    
    print("\n=== REPORTE DE CONTROL DE CALIDAD DE RENDERIZADO ===")
    print(f"- Archivos PUML de entrada: {total_puml}")
    print(f"- Archivos PNG generados: {total_png}")
    
    missing = []
    for pf in puml_files:
        base = os.path.splitext(os.path.basename(pf))[0]
        png_path = os.path.join(IMG_DIR, base + ".png")
        if not os.path.exists(png_path) or os.path.getsize(png_path) == 0:
            missing.append(base)

    if missing:
        print(f"ERROR: {len(missing)} diagramas no fueron generados correctamente:")
        for m in missing[:10]:
            print(f"  - {m}")
        sys.exit(1)
    else:
        print(f">>> ÉXITO: 100% de diagramas ({total_png}/{total_puml}) renderizados correctamente en {IMG_DIR} <<<")

if __name__ == "__main__":
    render_diagrams()
