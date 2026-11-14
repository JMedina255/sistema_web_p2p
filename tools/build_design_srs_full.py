# -*- coding: utf-8 -*-
"""
Master Builder Script for docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md
Integrates:
- Part A: Portada, Control de Versiones, Secciones 1 a 5 (con 5.6), 6.1, 6.2.1, 6.2.2
- Part B: Sección 6.2.3 (Escenarios de Casos de Uso - 24 CUS canónicos)
- Part C: Sección 6.3 (6.3.1 ECB 24 CUS y 6.3.2 Actividades con Objetos 24 CUS)
- Part D: Sección 6.3.3 (Diagramas de Secuencia del Sistema - 24 CUS bajo Visual Paradigm)
- Part E: Secciones 6.3.4 (Clases Lógicas 24 CUS), 6.3.5 (FSM), 6.3.6 (MER Físico 15 tablas y DDL)
- Part F: Secciones 7 (Conclusiones Sprints 1-8 con 627 tests) y 8 (Bibliografía)
- Diagram Substitution Engine: Sustituye automáticamente los 119 bloques PlantUML
  por figuras renderizadas de alta resolución (PNG) en docs/diseño/diagramas/srs/img/,
  garantizando cumplimiento D-2 y reproducibilidad total para exportación DOCX / Google Docs.
"""

import os
import sys
import re

# Add tools to sys.path
sys.path.insert(0, os.path.dirname(__file__))

from design_sections.generate_part_a import get_part_a
from build_design_srs_narratives import build_full_narratives
from design_sections.generate_part_c import get_part_c
from build_design_sequence_diagrams import build_full_sequence_content
from design_sections.generate_part_e import get_part_e
from design_sections.generate_part_f import get_part_f

from audit_srs import audit_narratives
from audit_sequence_diagrams import audit_sequence_content
from extract_srs_puml import get_filename_for_diag

def build_full_srs():
    print("1. Generando Parte A (Portada, Secciones 1 a 5.6, 6.1, 6.2.1, 6.2.2)...")
    part_a = get_part_a().rstrip()
    
    print("2. Generando Parte B (Sección 6.2.3: 24 Narrativas Canónicas)...")
    part_b = build_full_narratives().strip()
    
    print("3. Generando Parte C (Sección 6.3: 6.3.1 ECB y 6.3.2 Actividades con Objetos)...")
    part_c = get_part_c().strip()
    
    print("4. Generando Parte D (Sección 6.3.3: 24 Diagramas de Secuencia Visual Paradigm)...")
    part_d = build_full_sequence_content().strip()
    
    print("5. Generando Parte E (Secciones 6.3.4 Clases Lógicas, 6.3.5 FSM, 6.3.6 MER Físico)...")
    part_e = get_part_e().strip()
    
    print("6. Generando Parte F (Sección 7 Conclusiones y Sección 8 Bibliografía)...")
    part_f = get_part_f().strip()
    
    full_doc = (
        part_a + "\n\n" +
        part_b + "\n\n---\n\n" +
        part_c + "\n\n---\n\n" +
        part_d + "\n\n---\n\n" +
        part_e + "\n\n---\n\n" +
        part_f + "\n"
    )
    return full_doc

def substitute_diagrams_with_images(text, img_rel_dir="diagramas/srs/img"):
    """
    Sustituye de forma determinista y trazable cada bloque ```plantuml ... ```
    por la referencia a su figura renderizada PNG manteniendo el estándar D-2.
    """
    matches = list(re.finditer(r'```plantuml\s*([\s\S]*?)```', text))
    print(f"Total de bloques PlantUML detectados para sustitución: {len(matches)}")
    
    new_text_parts = []
    last_end = 0
    img_dir_abs = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "diseño", img_rel_dir))
    
    for idx, m in enumerate(matches):
        num = idx + 1
        start = m.start()
        end = m.end()
        
        pre_segment = text[max(0, start-1200):start]
        headings = re.findall(r'(#+\s*(?:Diagrama|Figura)\s*[\d\.]+:[^\n]+)', pre_segment)
        diag_heading = headings[-1].strip('# ') if headings else f"Diagrama {num}"
        diag_id = diag_heading.split(':')[0].strip() if ':' in diag_heading else f"Diagrama {num}"
        diag_name = diag_heading.split(':', 1)[1].strip() if ':' in diag_heading else "Diagrama UML"
        
        puml_name = get_filename_for_diag(num, diag_id, diag_name)
        png_name = puml_name.replace(".puml", ".png")
        
        # Verify image file exists
        png_path = os.path.join(img_dir_abs, png_name)
        if not os.path.exists(png_path) or os.path.getsize(png_path) == 0:
            raise FileNotFoundError(f"Imagen requerida no existe o está vacía: {png_path}")
            
        img_markdown = f"![{diag_heading}]({img_rel_dir}/{png_name})"
        
        new_text_parts.append(text[last_end:start])
        new_text_parts.append(img_markdown)
        last_end = end
        
    new_text_parts.append(text[last_end:])
    converted = "".join(new_text_parts)
    return converted

def main():
    print("=== ENSAMBLADOR INTEGRAL DEL INFORME SRS DE DISEÑO (v3.1 - FIGURAS RENDERIZADAS) ===")
    raw_doc = build_full_srs()
    
    print("\n=== EJECUTANDO AUDITORÍAS SOBRE ESTRUCTURA BASE ===")
    
    # Audit Section 6.2.3
    m_start = re.search(r'## 6\.2\.3\.?\s+Escenarios de Casos de Uso', raw_doc)
    m_next = re.search(r'#+\s+6\.3\.?\s+Modelo L[oó]gico', raw_doc)
    sec_narr = raw_doc[m_start.start():m_next.start()]
    err_narr = audit_narratives(sec_narr, "raw_doc:6.2.3")
    
    # Audit Section 6.3.3
    m_seq_start = re.search(r'## 6\.3\.3\.?\s+Diagramas de Secuencia', raw_doc)
    m_seq_next = re.search(r'## 6\.3\.4\.?\s+Diagrama de Clases', raw_doc)
    sec_seq = raw_doc[m_seq_start.start():m_seq_next.start()]
    err_seq_raw = audit_sequence_content(sec_seq, "raw_doc:6.3.3")
    
    if err_narr > 0 or err_seq_raw > 0:
        print("ERROR: Fallaron las auditorías previas a la sustitución de diagramas.")
        sys.exit(1)
        
    print("\n=== SUSTITUYENDO BLOQUES PLANTUML POR FIGURAS RENDERIZADAS ===")
    full_doc = substitute_diagrams_with_images(raw_doc)
    
    # Strict validation of rendered document
    plantuml_count = len(re.findall(r'```plantuml', full_doc))
    startuml_count = len(re.findall(r'@startuml', full_doc))
    img_count = len(re.findall(r'!\[.*?\]\(diagramas/srs/img/diag_\d+_[^)]+\.png\)', full_doc))
    
    print(f"- Bloques ```plantuml restantes: {plantuml_count}")
    print(f"- Etiquetas @startuml restantes: {startuml_count}")
    print(f"- Figuras renderizadas Markdown insertadas: {img_count}")
    
    if plantuml_count != 0 or startuml_count != 0 or img_count != 119:
        print("ERROR: La validación de figuras falló (deben quedar 0 plantuml y exactamente 119 imágenes).")
        sys.exit(1)
        
    target_path = "docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md"
    print(f"\nEscribiendo documento maestro oficial en {target_path}...")
    with open(target_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(full_doc)
        
    print(f"Documento guardado. Total caracteres: {len(full_doc)}, total líneas: {len(full_doc.splitlines())}")
    
    print("\n=== RE-EJECUTANDO AUDITORÍA SOBRE DOCUMENTO FINAL RENDERIZADO ===")
    sec_seq_final = full_doc[full_doc.find("## 6.3.3"):full_doc.find("## 6.3.4")]
    err_seq_final = audit_sequence_content(sec_seq_final, target_path)
    
    print("\n=== RESUMEN DE CONTROL DE CALIDAD ===")
    print(f"- Errores en Narrativas (6.2.3): {err_narr}")
    print(f"- Errores en Diagramas de Secuencia (6.3.3): {err_seq_final}")
    print(f"- Figuras renderizadas validadas: {img_count}/119")
    
    if err_narr == 0 and err_seq_final == 0:
        print(">>> ÉXITO: 100% DE DIAGRAMAS RENDERIZADOS Y SRS VALIDADO SIN ERRORES <<<")
    else:
        print("ERROR: Se detectaron inconsistencias en la validación final.")
        sys.exit(1)

if __name__ == "__main__":
    main()
