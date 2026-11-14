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

def main():
    print("=== ENSAMBLADOR INTEGRAL DEL INFORME SRS DE DISEÑO (v3.0) ===")
    full_doc = build_full_srs()
    
    target_path = "docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md"
    print(f"Escribiendo documento completo en {target_path}...")
    with open(target_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(full_doc)
        
    print(f"Documento guardado. Total caracteres: {len(full_doc)}, total líneas: {len(full_doc.splitlines())}")
    
    print("\n=== EJECUTANDO AUDITORÍAS FORMALES ===")
    
    # Audit Section 6.2.3
    m_start = re.search(r'## 6\.2\.3\.?\s+Escenarios de Casos de Uso', full_doc)
    m_next = re.search(r'#+\s+6\.3\.?\s+Modelo L[oó]gico', full_doc)
    sec_narr = full_doc[m_start.start():m_next.start()]
    err_narr = audit_narratives(sec_narr, target_path)
    
    # Audit Section 6.3.3
    m_seq_start = re.search(r'## 6\.3\.3\.?\s+Diagramas de Secuencia', full_doc)
    m_seq_next = re.search(r'## 6\.3\.4\.?\s+Diagrama de Clases', full_doc)
    sec_seq = full_doc[m_seq_start.start():m_seq_next.start()]
    err_seq = audit_sequence_content(sec_seq, target_path)
    
    print("\n=== RESUMEN DE CONTROL DE CALIDAD ===")
    print(f"- Errores en Narrativas (6.2.3): {err_narr}")
    print(f"- Errores en Diagramas de Secuencia (6.3.3): {err_seq}")
    
    if err_narr == 0 and err_seq == 0:
        print(">>> DOCUMENTO SRS v3.0 VALIDADO Y APROBADO EXITOSAMENTE AL 100% <<<")
    else:
        print("ERROR: Se detectaron inconsistencias en la validación.")
        sys.exit(1)

if __name__ == "__main__":
    main()
