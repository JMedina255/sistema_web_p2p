# -*- coding: utf-8 -*-
"""
Extract all 119 PlantUML diagrams from docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md
into docs/diseño/diagramas/srs/puml/*.puml and generate README.md
"""

import os
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text).strip('_')
    return text

def get_filename_for_diag(idx, diag_id, diag_name):
    # Mapping based on index (1-based)
    if idx == 1: return "diag_001_sec24_organigrama_consultor.puml"
    if idx == 2: return "diag_002_sec41_actividades_proceso_as_is.puml"
    if idx == 3: return "diag_003_sec42_actividades_proceso_to_be.puml"
    if idx == 4: return "diag_004_sec60_ciclo_vida_metodologia.puml"
    if idx == 5: return "diag_005_sec62_clases_conceptuales_dominio.puml"
    if idx == 6: return "diag_006_sec621_paquetes_arquitecturales.puml"
    if idx == 7: return "diag_007_sec622_casos_uso_general_24cus.puml"
    if 8 <= idx <= 15:
        mod_num = idx - 7
        return f"diag_{idx:03d}_sec622_casos_uso_mod{mod_num:02d}.puml"
    if idx == 16:
        return "diag_016_sec631_ecb_general_consolidado.puml"
    if 17 <= idx <= 40:
        # CUS 001 to 024 mapping in order
        m_cus = re.search(r'CUS-(\d{3})', diag_name)
        cus_tag = f"cus{m_cus.group(1)}" if m_cus else f"item_{idx}"
        return f"diag_{idx:03d}_sec631_ecb_{cus_tag}.puml"
    if idx == 41:
        return "diag_041_sec632_act_general_consolidado.puml"
    if 42 <= idx <= 65:
        m_cus = re.search(r'CUS-(\d{3})', diag_name)
        cus_tag = f"cus{m_cus.group(1)}" if m_cus else f"item_{idx}"
        return f"diag_{idx:03d}_sec632_act_{cus_tag}.puml"
    if idx == 66:
        return "diag_066_sec633_seq_general_integracion.puml"
    if 67 <= idx <= 90:
        m_cus = re.search(r'CUS-(\d{3})', diag_name)
        cus_tag = f"cus{m_cus.group(1)}" if m_cus else f"item_{idx}"
        return f"diag_{idx:03d}_sec633_seq_{cus_tag}.puml"
    if idx == 91:
        return "diag_091_sec634_clases_logico_general.puml"
    if 92 <= idx <= 115:
        m_cus = re.search(r'CUS-(\d{3})', diag_name)
        cus_tag = f"cus{m_cus.group(1)}" if m_cus else f"item_{idx}"
        return f"diag_{idx:03d}_sec634_clases_logico_{cus_tag}.puml"
    if idx == 116:
        return "diag_116_sec635_fsm_sesion_mentoria.puml"
    if idx == 117:
        return "diag_117_sec635_fsm_reserva_cupo.puml"
    if idx == 118:
        return "diag_118_sec635_fsm_bitacora_certificado.puml"
    if idx == 119:
        return "diag_119_sec636_der_fisico_15tablas.puml"
    
    return f"diag_{idx:03d}_{slugify(diag_id)}.puml"

def main():
    doc_path = "docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md"
    with open(doc_path, "r", encoding="utf-8") as f:
        text = f.read()

    puml_dir = "docs/diseño/diagramas/srs/puml"
    img_dir = "docs/diseño/diagramas/srs/img"
    os.makedirs(puml_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    matches = list(re.finditer(r'```plantuml\s*([\s\S]*?)```', text))
    print(f"Total diagramas encontrados: {len(matches)}")

    extracted = []

    for idx, m in enumerate(matches):
        num = idx + 1
        code = m.group(1).strip()
        start = m.start()

        # Find heading
        pre = text[max(0, start-1200):start]
        headings = re.findall(r'(#+\s*(?:Diagrama|Figura)\s*[\d\.]+:[^\n]+)', pre)
        diag_heading = headings[-1].strip('# ') if headings else f"Diagrama {num}"
        
        diag_id = diag_heading.split(':')[0].strip() if ':' in diag_heading else f"Diagrama {num}"
        diag_name = diag_heading.split(':', 1)[1].strip() if ':' in diag_heading else "Diagrama UML"

        # Ensure @startuml and @enduml
        if not code.startswith("@startuml"):
            code = "@startuml\n" + code
        if not code.endswith("@enduml"):
            code = code + "\n@enduml"

        filename = get_filename_for_diag(num, diag_id, diag_name)
        filepath = os.path.join(puml_dir, filename)

        # Build clean file content with metadata header
        header = f"""/'
  Diagrama: {diag_id}: {diag_name}
  Proyecto: Sistema Web P2P de Mentorías Académicas - EPIS UPT
  Estándar: Visual Paradigm / UML 2.5
  Extracción automatizada: Fase D02 (H03)
'/
"""
        full_puml = header + code + "\n"

        with open(filepath, "w", encoding="utf-8", newline="\n") as f_out:
            f_out.write(full_puml)

        extracted.append((num, diag_id, diag_name, filename))

    print(f"Extracción completada: {len(extracted)} archivos .puml generados en {puml_dir}.")

    # Generate README.md
    readme_path = "docs/diseño/diagramas/srs/README.md"
    readme_lines = [
        "# Repositorio de Diagramas Oficiales del Informe SRS v3.1",
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
        "- `puml/`: Contiene los **119 archivos de código fuente PlantUML (`.puml`)** extraídos del informe SRS v3.1.",
        "- `img/`: Contiene las **imágenes renderizadas en formato PNG de alta resolución** listas para incrustación directa en el documento Markdown maestro y su exportación a Microsoft Word (`.docx`) y Google Docs.",
        "",
        "## 2. Convención de Nomenclatura",
        "",
        "Los archivos se nombran conforme al patrón estándar:  ",
        "`diag_{correlativo:03d}_{seccion}_{tipo_o_cus}.puml`",
        "",
        "Ejemplos:",
        "- `diag_001_sec24_organigrama_consultor.puml`: Organigrama funcional del equipo consultor (Diagrama 2.1).",
        "- `diag_002_sec41_actividades_proceso_as_is.puml`: Actividades del proceso actual de asesoría informal (Diagrama 4.1).",
        "- `diag_003_sec42_actividades_proceso_to_be.puml`: Actividades del proceso propuesto P2P (Diagrama 4.2).",
        "- `diag_007_sec622_casos_uso_general_24cus.puml`: Casos de uso general consolidado de los 24 CUS (Diagrama 6.4).",
        "- `diag_016_sec631_ecb_general_consolidado.puml`: Modelo ECB general de análisis (Diagrama 6.13).",
        "- `diag_017_sec631_ecb_cus001.puml` al `diag_040_sec631_ecb_cus022.puml`: Vistas ECB individuales por CUS.",
        "- `diag_041_sec632_act_general_consolidado.puml`: Actividades del dominio general (Diagrama 6.14).",
        "- `diag_042_sec632_act_cus001.puml` al `diag_065_sec632_act_cus022.puml`: Actividades por CUS.",
        "- `diag_066_sec633_seq_general_integracion.puml`: Diagrama de secuencia DSS de integración (Diagrama 6.15).",
        "- `diag_067_sec633_seq_cus001.puml` al `diag_090_sec633_seq_cus022.puml`: Diagramas de secuencia DSS por CUS.",
        "- `diag_091_sec634_clases_logico_general.puml`: Diagrama de clases del modelo lógico general (Diagrama 6.16).",
        "- `diag_092_sec634_clases_logico_cus001.puml` al `diag_115_sec634_clases_logico_cus022.puml`: Clases lógicas por CUS.",
        "- `diag_116_sec635_fsm_sesion_mentoria.puml`: FSM del ciclo de vida de sesión (Diagrama 6.17).",
        "- `diag_117_sec635_fsm_reserva_cupo.puml`: FSM del ciclo de vida de reserva (Diagrama 6.18).",
        "- `diag_118_sec635_fsm_bitacora_certificado.puml`: FSM de bitácoras y constancias (Diagrama 6.19).",
        "- `diag_119_sec636_der_fisico_15tablas.puml`: Diagrama DER físico de las 15 tablas relacionales (Diagrama 6.20).",
        "",
        "## 3. Guía de Renderizado y Automatización",
        "",
        "El renderizado de todos los archivos `.puml` hacia `.png` se realiza mediante el script oficial:",
        "```bash",
        "python tools/render_srs_diagrams.py",
        "```",
        "El script procesa cada archivo de `puml/` y genera su contraparte en `img/` manteniendo el mismo nombre base.",
        "",
        "## 4. Catálogo de Archivos Extraídos (Total: 119)",
        "",
        "| N° | Archivo PUML | Diagrama Oficial | Título |",
        "|:---:|:---|:---:|:---|"
    ]

    for item in extracted:
        readme_lines.append(f"| {item[0]:03d} | `{item[3]}` | **{item[1]}** | {item[2]} |")

    readme_lines.append("")
    readme_lines.append("---")
    readme_lines.append("*Repositorio de diagramas generado en Hito D02.*")

    with open(readme_path, "w", encoding="utf-8", newline="\n") as f_r:
        f_r.write("\n".join(readme_lines) + "\n")

    print(f"README generado en {readme_path}.")

if __name__ == "__main__":
    main()
