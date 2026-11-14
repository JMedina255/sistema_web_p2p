# -*- coding: utf-8 -*-
"""
Extracts and renders all 14 architectural PlantUML diagrams from
docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md
into docs/diseño/diagramas/sad/puml/*.puml and docs/diseño/diagramas/sad/img/*.png
"""

import os
import sys
import re
import subprocess
import time

SAD_DOC_PATH = "docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md"
PLANTUML_JAR = os.path.abspath("tools/plantuml.jar")
SAD_PUML_DIR = os.path.abspath("docs/diseño/diagramas/sad/puml")
SAD_IMG_DIR = os.path.abspath("docs/diseño/diagramas/sad/img")

SAD_DIAG_MAPPING = {
    1: ("diag_001_sec02_kruchten_escenarios", "Diagrama 2.1: Vista de Escenarios Arquitectónicos Nucleares (+1 de Kruchten)"),
    2: ("diag_002_sec02_vista_logica_ecb", "Diagrama 2.2: Vista Lógica en Capas y Subsistemas ECB"),
    3: ("diag_003_sec02_vista_procesos_concurrencia", "Diagrama 2.3: Vista de Procesos, Concurrencia y Sincronización Transaccional"),
    4: ("diag_004_sec02_vista_desarrollo_paquetes", "Diagrama 2.4: Vista de Desarrollo y Organización de Paquetes de Software"),
    5: ("diag_005_sec02_vista_fisica_despliegue", "Diagrama 2.5: Vista Física y Topología de Despliegue en Red"),
    6: ("diag_006_sec05_casos_uso_8modulos", "Diagrama 5.1: Casos de Uso Canónicos Oficiales agrupados por los 8 Módulos (CUS-001 al CUS-024)"),
    7: ("diag_007_sec06_limites_contexto_sistema", "Diagrama 6.1: Límites del Sistema Web P2P y Sistemas Externos"),
    8: ("diag_008_sec07_actividades_proceso_as_is", "Diagrama 7.1: Diagrama de Actividades del Proceso As-Is de Mentorías Informales"),
    9: ("diag_009_sec07_actividades_proceso_to_be", "Diagrama 7.2: Diagrama de Actividades del Proceso Propuesto (To-Be) de Mentorías P2P"),
    10: ("diag_010_sec08_c4_contenedores_software", "Diagrama 8.1: Diagrama de Contenedores de Software (C4 Nivel 2 / Metodología UWE)"),
    11: ("diag_011_sec09_componentes_backend", "Diagrama 9.1: Componentes de Software y Módulos Canónicos del Backend"),
    12: ("diag_012_sec10_der_fisico_15tablas", "Diagrama 10.1: Diagrama Entidad-Relación Físico (15 Tablas Relacionales en PostgreSQL / Supabase)"),
    13: ("diag_013_sec11_fsm_sesion_mentoria", "Diagrama 11.4: Máquina de Estados Finitos de la Sesión de Mentoría (13 Estados Canónicos)"),
    14: ("diag_014_sec11_fsm_reserva_cupo", "Diagrama 11.5: Máquina de Estados Finitos de la Reserva de Cupo (9 Estados Canónicos)"),
}

def extract_and_render_sad():
    print("=== EXTRACCIÓN Y RENDERIZADO DE DIAGRAMAS SAD ===")
    os.makedirs(SAD_PUML_DIR, exist_ok=True)
    os.makedirs(SAD_IMG_DIR, exist_ok=True)
    
    with open(SAD_DOC_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    matches = list(re.finditer(r'```plantuml\s*([\s\S]*?)```', content))
    print(f"Total diagramas encontrados en SAD: {len(matches)}")
    
    if len(matches) != 14:
        print(f"ADVERTENCIA: Se esperaban 14 diagramas en SAD, pero se encontraron {len(matches)}")
        
    extracted = []
    
    for idx, m in enumerate(matches, 1):
        code = m.group(1).strip()
        base_name, expected_heading = SAD_DIAG_MAPPING[idx]
        puml_filename = base_name + ".puml"
        puml_filepath = os.path.join(SAD_PUML_DIR, puml_filename)
        
        # Ensure startuml and enduml
        if not code.startswith("@startuml"):
            code = "@startuml\n" + code
        if not code.endswith("@enduml"):
            code = code + "\n@enduml"
            
        header = f"""/'
  Diagrama SAD: {expected_heading}
  Proyecto: Sistema Web P2P de Mentorías Académicas - EPIS UPT
  Estándar: Kruchten 4+1 / UML 2.5 / C4 Nivel 2
  Extracción automatizada: Documento SAD Oficial
'/
"""
        full_puml = header + code + "\n"
        with open(puml_filepath, "w", encoding="utf-8", newline="\n") as f_out:
            f_out.write(full_puml)
            
        extracted.append((idx, base_name, expected_heading, puml_filename))
        print(f"[{idx:02d}] Extraído: {puml_filename}")
        
    # Render with PlantUML
    print("\nEjecutando renderizado por lotes de los diagramas SAD con PlantUML y Graphviz...")
    t0 = time.time()
    cmd = [
        "java",
        "-DPLANTUML_LIMIT_SIZE=16384",
        "-Djava.awt.headless=true",
        "-jar",
        PLANTUML_JAR,
        "-tpng",
        "-charset", "UTF-8",
        os.path.join(SAD_PUML_DIR, "*.puml"),
        "-o",
        SAD_IMG_DIR
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    duration = time.time() - t0
    print(f"Renderizado SAD concluido en {duration:.2f} segundos.")
    
    # Check generated PNGs
    errors = []
    for idx, base_name, heading, puml_fn in extracted:
        png_fn = base_name + ".png"
        png_path = os.path.join(SAD_IMG_DIR, png_fn)
        if not os.path.exists(png_path) or os.path.getsize(png_path) == 0:
            errors.append(f"Falta o está vacía la imagen: {png_fn}")
        else:
            sz = os.path.getsize(png_path)
            print(f"[{idx:02d}] OK: {png_fn} ({sz/1024:.1f} KB)")
            
    if errors:
        print("\nERRORES DETECTADOS:")
        for err in errors:
            print("  -", err)
        sys.exit(1)
        
    print(f"\n>>> ÉXITO: 14/14 diagramas del SAD extraídos y renderizados correctamente en {SAD_IMG_DIR} <<<")
    
    # Generate README in docs/diseño/diagramas/sad/
    readme_path = os.path.join(os.path.dirname(SAD_PUML_DIR), "README.md")
    readme_lines = [
        "# Repositorio de Diagramas Oficiales del Documento SAD v3.1",
        "",
        "**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  ",
        "**Equipo Consultor:** C-SharkTeam (Grupo 03)  ",
        "**Autores:** Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani  ",
        "**Cátedra:** Construcción de Software I (Semestre 2026-II)  ",
        "**Fecha:** 14 de noviembre de 2026  ",
        "",
        "---",
        "",
        "## 1. Estructura del Directorio",
        "",
        "- `puml/`: Contiene los **14 archivos de código fuente PlantUML (`.puml`)** correspondientes a las vistas arquitectónicas del SAD.",
        "- `img/`: Contiene las **imágenes renderizadas en formato PNG de alta resolución** listas para incrustación directa en el documento Markdown maestro y su exportación a Microsoft Word (`.docx`) y Google Docs.",
        "",
        "## 2. Catálogo de los 14 Diagramas Arquitectónicos del SAD",
        "",
        "| N° | Identificador / Vista Arquitectónica | Archivo PUML | Archivo Renderizado |",
        "|:---:|:---|:---|:---|",
    ]
    for idx, base_name, heading, puml_fn in extracted:
        readme_lines.append(f"| {idx:02d} | **{heading}** | `{puml_fn}` | `{base_name}.png` |")
        
    readme_lines.append("")
    readme_lines.append("Fuente: Elaboración propia a partir del documento oficial SAD.")
    with open(readme_path, "w", encoding="utf-8", newline="\n") as f_readme:
        f_readme.write("\n".join(readme_lines) + "\n")
    print(f"Catálogo generado en {readme_path}")

if __name__ == "__main__":
    extract_and_render_sad()
