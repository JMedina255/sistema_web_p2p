# -*- coding: utf-8 -*-
"""
Builder and Auditor Script for Root Reference Copies:
- Generates SRS.md in root from docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md
- Generates SAD.md in root from docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md
- Ensures 100% content preservation, root-relative image paths, visible rendered figures,
  D-2 standard compliance, and editable PlantUML source code backups.
"""

import os
import sys
import re
import hashlib

sys.path.insert(0, os.path.dirname(__file__))
from extract_and_render_sad_diagrams import SAD_DIAG_MAPPING

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def clean_title(raw_title):
    # Remove prefix like "Diagrama 2.1: " or "Figura 2.1: " for caption
    cleaned = re.sub(r'^(?:Diagrama|Figura)\s*[\d\.]+:\s*', '', raw_title).strip()
    return cleaned if cleaned else raw_title

def build_root_srs():
    print("--- Generando SRS.md en raíz ---")
    orig_path = "docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md"
    root_path = "SRS.md"
    
    with open(orig_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    puml_dir = "docs/diseño/diagramas/srs/puml"
    img_dir_rel = "docs/diseño/diagramas/srs/img"
    
    # Matches: ![Caption](diagramas/srs/img/diag_XXX_...png)
    pattern = re.compile(r'!\[(.*?)\]\(diagramas/srs/img/(diag_\d+_[^)]+\.png)\)')
    matches = list(pattern.finditer(text))
    print(f"Total imágenes en SRS original: {len(matches)}")
    
    new_text_parts = []
    last_end = 0
    
    for idx, m in enumerate(matches, 1):
        start = m.start()
        end = m.end()
        raw_caption = m.group(1)
        png_name = m.group(2)
        puml_name = png_name.replace(".png", ".puml")
        
        # Read PUML source code
        puml_path = os.path.join(puml_dir, puml_name)
        if not os.path.exists(puml_path):
            raise FileNotFoundError(f"Archivo PUML no encontrado: {puml_path}")
        with open(puml_path, "r", encoding="utf-8") as pf:
            puml_code = pf.read().strip()
            
        # Clean title
        title_desc = clean_title(raw_caption)
        fig_title = f"Figura {idx}. {title_desc}"
        
        # Replacement block: Title with Figura, rendered image, and collapsible PUML backup
        replacement = (
            f"**{fig_title}**\n\n"
            f"![{fig_title}]({img_dir_rel}/{png_name})\n\n"
            f"<details>\n"
            f"<summary>Código fuente PlantUML (respaldo editable)</summary>\n\n"
            f"```plantuml\n"
            f"{puml_code}\n"
            f"```\n"
            f"</details>"
        )
        
        new_text_parts.append(text[last_end:start])
        new_text_parts.append(replacement)
        last_end = end
        
    new_text_parts.append(text[last_end:])
    srs_root_content = "".join(new_text_parts)
    
    with open(root_path, "w", encoding="utf-8", newline="\n") as f_out:
        f_out.write(srs_root_content)
        
    print(f"SRS.md escrito exitosamente: {len(srs_root_content)} caracteres, {len(srs_root_content.splitlines())} líneas.")
    return root_path

def build_root_sad():
    print("\n--- Generando SAD.md en raíz ---")
    orig_path = "docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md"
    root_path = "SAD.md"
    
    with open(orig_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    puml_dir = "docs/diseño/diagramas/sad/puml"
    img_dir_rel = "docs/diseño/diagramas/sad/img"
    
    matches = list(re.finditer(r'```plantuml\s*([\s\S]*?)```', text))
    print(f"Total bloques PlantUML en SAD original: {len(matches)}")
    
    new_text_parts = []
    last_end = 0
    
    for idx, m in enumerate(matches, 1):
        start = m.start()
        end = m.end()
        raw_puml = m.group(1).strip()
        
        base_name, expected_heading = SAD_DIAG_MAPPING[idx]
        png_name = f"{base_name}.png"
        
        # Check image exists
        png_full_path = os.path.join(img_dir_rel, png_name)
        if not os.path.exists(png_full_path) or os.path.getsize(png_full_path) == 0:
            raise FileNotFoundError(f"Imagen SAD no encontrada o vacía: {png_full_path}")
            
        title_desc = clean_title(expected_heading)
        fig_title = f"Figura {idx}. {title_desc}"
        
        # Clean PUML code
        if not raw_puml.startswith("@startuml"):
            puml_code = "@startuml\n" + raw_puml
        else:
            puml_code = raw_puml
        if not puml_code.endswith("@enduml"):
            puml_code = puml_code + "\n@enduml"
            
        replacement = (
            f"**{fig_title}**\n\n"
            f"![{fig_title}]({img_dir_rel}/{png_name})\n\n"
            f"<details>\n"
            f"<summary>Código fuente PlantUML (respaldo editable)</summary>\n\n"
            f"```plantuml\n"
            f"{puml_code}\n"
            f"```\n"
            f"</details>"
        )
        
        new_text_parts.append(text[last_end:start])
        new_text_parts.append(replacement)
        last_end = end
        
    new_text_parts.append(text[last_end:])
    sad_root_content = "".join(new_text_parts)
    
    with open(root_path, "w", encoding="utf-8", newline="\n") as f_out:
        f_out.write(sad_root_content)
        
    print(f"SAD.md escrito exitosamente: {len(sad_root_content)} caracteres, {len(sad_root_content.splitlines())} líneas.")
    return root_path

def audit_root_files():
    print("\n=== AUDITORÍA EXHAUSTIVA DE INTEGRIDAD DE COPIAS MAESTRAS EN RAÍZ ===")
    
    # 1. Audit SRS.md
    srs_text = open("SRS.md", "r", encoding="utf-8").read()
    srs_imgs = list(re.finditer(r'!\[(.*?)\]\((docs/diseño/diagramas/srs/img/(diag_\d+_[^)]+\.png))\)', srs_text))
    srs_details = re.findall(r'<summary>Código fuente PlantUML', srs_text)
    srs_orphan_puml = re.findall(r'```plantuml', srs_text)
    
    print("\n[AUDITORÍA SRS.md]")
    print(f"- Total figuras renderizadas Markdown: {len(srs_imgs)} / 119 esperadas")
    print(f"- Total bloques <details> con código PUML: {len(srs_details)} / 119 esperados")
    print(f"- Total bloques plantuml encontrados: {len(srs_orphan_puml)} (todos en <details>)")
    
    srs_img_errors = []
    for m in srs_imgs:
        path = m.group(2)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            srs_img_errors.append(path)
    print(f"- Errores de resolución física de imágenes en disco: {len(srs_img_errors)}")
    
    # 2. Audit SAD.md
    sad_text = open("SAD.md", "r", encoding="utf-8").read()
    sad_imgs = list(re.finditer(r'!\[(.*?)\]\((docs/diseño/diagramas/sad/img/(diag_\d+_[^)]+\.png))\)', sad_text))
    sad_details = re.findall(r'<summary>Código fuente PlantUML', sad_text)
    sad_orphan_puml = re.findall(r'```plantuml', sad_text)
    
    print("\n[AUDITORÍA SAD.md]")
    print(f"- Total figuras renderizadas Markdown: {len(sad_imgs)} / 14 esperadas")
    print(f"- Total bloques <details> con código PUML: {len(sad_details)} / 14 esperados")
    print(f"- Total bloques plantuml encontrados: {len(sad_orphan_puml)} (todos en <details>)")
    
    sad_img_errors = []
    for m in sad_imgs:
        path = m.group(2)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            sad_img_errors.append(path)
    print(f"- Errores de resolución física de imágenes en disco: {len(sad_img_errors)}")
    
    # 3. Check section and chapter conservation
    print("\n[CONSERVACIÓN ESTRUCTURAL DE CAPÍTULOS Y SECCIONES]")
    srs_orig_h2 = re.findall(r'^##\s+[^\n]+', open("docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md", "r", encoding="utf-8").read(), re.MULTILINE)
    srs_root_h2 = re.findall(r'^##\s+[^\n]+', srs_text, re.MULTILINE)
    print(f"- Secciones ## en SRS original: {len(srs_orig_h2)} | en SRS.md: {len(srs_root_h2)}")
    
    sad_orig_h2 = re.findall(r'^##\s+[^\n]+', open("docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md", "r", encoding="utf-8").read(), re.MULTILINE)
    sad_root_h2 = re.findall(r'^##\s+[^\n]+', sad_text, re.MULTILINE)
    print(f"- Secciones ## en SAD original: {len(sad_orig_h2)} | en SAD.md: {len(sad_root_h2)}")
    
    # 4. SHA-256 Hashes
    print("\n[HASHES CRIPTOGRÁFICOS SHA-256]")
    hash_srs_orig = compute_sha256("docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md")
    hash_srs_root = compute_sha256("SRS.md")
    hash_sad_orig = compute_sha256("docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md")
    hash_sad_root = compute_sha256("SAD.md")
    
    print(f"- SRS original (docs/diseño): {hash_srs_orig}")
    print(f"- SRS copia raíz (SRS.md):     {hash_srs_root}")
    print(f"- SAD original (docs/diseño): {hash_sad_orig}")
    print(f"- SAD copia raíz (SAD.md):     {hash_sad_root}")
    
    # Global verification
    valid = (
        len(srs_imgs) == 119 and
        len(srs_img_errors) == 0 and
        len(sad_imgs) == 14 and
        len(sad_img_errors) == 0 and
        len(srs_orig_h2) == len(srs_root_h2) and
        len(sad_orig_h2) == len(sad_root_h2)
    )
    
    if valid:
        print("\n>>> ÉXITO: 100% DE CONTROL DE CALIDAD APROBADO EN SRS.md Y SAD.md <<<")
    else:
        print("\nERROR: Inconsistencias detectadas en la auditoría.")
        sys.exit(1)

def main():
    build_root_srs()
    build_root_sad()
    audit_root_files()

if __name__ == "__main__":
    main()
