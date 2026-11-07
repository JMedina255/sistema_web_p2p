# -*- coding: utf-8 -*-
"""
Audit script for Design Phase Sequence Diagrams:
Verifies structural integrity, PlantUML syntax, layer breakdown,
no dead/unused lifelines, balanced activations, clean architecture (no API->DB bypass),
OpenAPI route parameter formatting ({param} instead of :param),
and 100% exact traceability against the 24 Design Use Case Narratives.
"""

import os
import sys
import re

EXPECTED_CUS_ORDER = [
    'CUS-001', 'CUS-010', # MOD-01
    'CUS-006', 'CUS-008', # MOD-02
    'CUS-005', 'CUS-021', # MOD-03
    'CUS-002', 'CUS-003', # MOD-04
    'CUS-004', 'CUS-024', 'CUS-017', 'CUS-023', 'CUS-007', # MOD-05
    'CUS-012', 'CUS-013', 'CUS-014', # MOD-06
    'CUS-018', 'CUS-019', # MOD-07
    'CUS-009', 'CUS-011', 'CUS-015', 'CUS-016', 'CUS-020', 'CUS-022' # MOD-08
]

def extract_narrative_metadata(narratives_path):
    """
    Parses NARRATIVAS_FASE_DISEÑO_CONSOLIDADAS.md to extract expected alts, excs, and fases for each CUS.
    """
    if not os.path.exists(narratives_path):
        return {}
    with open(narratives_path, "r", encoding="utf-8") as f:
        text = f.read()

    cus_blocks = re.split(r'\n(?=####\s+CUS-\d+)', text)
    metadata = {}
    for block in cus_blocks[1:]:
        m_id = re.search(r'####\s+(CUS-\d+)', block)
        if not m_id:
            continue
        cid = m_id.group(1)
        alts = re.findall(r'Flujo alternativo\s+([A-Z0-9]+):', block)
        excs = re.findall(r'Flujo de excepci[oó]n\s+([A-Z0-9]+):', block)
        fases = re.findall(r'\*\*Fase\s+(\d+):', block)
        metadata[cid] = {
            "alts": sorted(list(set(alts))),
            "excs": sorted(list(set(excs))),
            "fases": sorted(list(set(fases)))
        }
    return metadata

def audit_sequence_content(content, source_name="Memory", narratives_metadata=None):
    print(f"=== Auditando Diagramas de Secuencia: {source_name} ===")
    errors = []

    # Find all diagram blocks: #### Diagrama 6.15.X: ...
    diag_blocks = re.split(r'\n(?=####\s+Diagrama\s+6\.15\.\d+:)', content)
    found_diagrams = diag_blocks[1:] if len(diag_blocks) > 1 else []

    print(f"Total diagramas encontrados: {len(found_diagrams)}")
    if len(found_diagrams) != 24:
        errors.append(("GLOBAL", f"Se esperaban 24 diagramas de secuencia, pero se encontraron {len(found_diagrams)}"))

    found_cus_list = []

    for idx, block in enumerate(found_diagrams, 1):
        header = block.strip().splitlines()[0]
        m_head = re.match(r'####\s+Diagrama\s+6\.15\.(\d+):\s+Diagrama\s+de\s+Secuencia\s+-\s+(CUS-\d+):\s*(.*)', header)
        if not m_head:
            errors.append((f"Block {idx}", f"Encabezado inválido de diagrama: '{header}'"))
            continue

        diag_num = int(m_head.group(1))
        cid = m_head.group(2)
        cname = m_head.group(3)
        found_cus_list.append(cid)

        # 1. Numbering check
        if diag_num != idx:
            errors.append((cid, f"Numeración desalineada: esperado Diagrama 6.15.{idx}, encontrado 6.15.{diag_num}"))

        # 2. PlantUML block check
        if "```plantuml" not in block or "```" not in block:
            errors.append((cid, "Falta bloque de código ```plantuml ... ```"))
            continue

        puml_match = re.search(r'```plantuml\s*\n(.*?)\n```', block, re.DOTALL)
        if not puml_match:
            errors.append((cid, "No se pudo extraer el bloque PlantUML"))
            continue

        puml = puml_match.group(1)

        # Check @startuml and @enduml
        if "@startuml" not in puml or "@enduml" not in puml:
            errors.append((cid, "PlantUML: Falta @startuml o @enduml"))

        # Check title
        if "title" not in puml:
            errors.append((cid, "PlantUML: Falta instrucción 'title'"))

        # Check autonumber
        if "autonumber" not in puml:
            errors.append((cid, "PlantUML: Falta instrucción 'autonumber'"))

        # Check balanced blocks
        starts = len(re.findall(r'^\s*(?:alt|opt|loop|group)\b', puml, re.MULTILINE))
        ends = len(re.findall(r'^\s*end\b', puml, re.MULTILINE))
        if starts != ends:
            errors.append((cid, f"PlantUML: Bloques desbalanceados (starts={starts}, ends={ends})"))

        # 3. Check layer participants breakdown
        has_actor = bool(re.search(r'^\s*actor\s+', puml, re.MULTILINE))
        has_ui = bool(re.search(r'participant\s+.*?(?:\.tsx|Vista React|UI)', puml, re.IGNORECASE))
        has_client = bool(re.search(r'participant\s+.*?(?:Service\.ts|Adapter|Client|Adaptador)', puml, re.IGNORECASE))
        has_api = bool(re.search(r'participant\s+.*?(?:endpoints/|API|Controlador|FastAPI)', puml, re.IGNORECASE))
        has_service = bool(re.search(r'participant\s+.*?(?:_service\.py|Backend|Servicio Backend)', puml, re.IGNORECASE))
        has_db = bool(re.search(r'(?:database|participant)\s+.*?(?:PostgreSQL|DB|Supabase)', puml, re.IGNORECASE))

        if not has_actor:
            errors.append((cid, "Capas: Falta declaración de 'actor' institucional"))
        if not has_ui:
            errors.append((cid, "Capas: Falta declaración de componente React / Vista (.tsx)"))
        if not has_client:
            errors.append((cid, "Capas: Falta declaración de adaptador cliente (.ts)"))
        if not has_api:
            errors.append((cid, "Capas: Falta declaración de controlador FastAPI (.py)"))
        if not has_service:
            errors.append((cid, "Capas: Falta declaración de servicio de negocio backend (.py)"))
        if not has_db:
            errors.append((cid, "Capas: Falta declaración de persistencia PostgreSQL / DB"))

        # 4. Check for UNUSED lifelines (no dead actor or participant lifelines)
        lifeline_aliases = re.findall(r'^\s*(?:actor|participant|database)\s+.*?\s+as\s+([A-Za-z0-9_]+)', puml, re.MULTILINE)
        for alias in lifeline_aliases:
            usage_pat = re.compile(rf'(?:^\s*{alias}\s*[-=]>|[-=]>\s*{alias}\s*:|activate\s+{alias}\b|deactivate\s+{alias}\b)', re.MULTILINE)
            if not usage_pat.search(puml):
                errors.append((cid, f"Línea de vida muerta/inutilizada: '{alias}' está declarada pero nunca envía ni recibe mensajes"))

        # 5. Check activation/deactivation balance
        counts = {}
        for line_no, line in enumerate(puml.splitlines(), 1):
            line_str = line.strip()
            m_act = re.match(r'^activate\s+([A-Za-z0-9_]+)', line_str)
            m_deact = re.match(r'^deactivate\s+([A-Za-z0-9_]+)', line_str)
            if m_act:
                alias = m_act.group(1)
                counts[alias] = counts.get(alias, 0) + 1
            elif m_deact:
                alias = m_deact.group(1)
                if counts.get(alias, 0) <= 0:
                    errors.append((cid, f"Línea {line_no}: 'deactivate {alias}' ejecutado sin activación previa activa"))
                counts[alias] = counts.get(alias, 0) - 1
        for alias, count in counts.items():
            if count != 0:
                errors.append((cid, f"Desbalance de activación en '{alias}': balance neto = {count}"))

        # 6. Check Clean Architecture: No direct API -> DB or UI -> DB bypasses
        bypasses = re.findall(r'^\s*(?:API|UI|Client)\s*->\s*DB\b.*', puml, re.MULTILINE)
        if bypasses:
            for b in bypasses:
                errors.append((cid, f"Violación de Arquitectura Limpia: salto directo a base de datos '{b.strip()}'"))

        # 7. Check OpenAPI route parameter syntax (no Express-style :param)
        colon_params = re.findall(r'(?:GET|POST|PUT|DELETE|PATCH)\s+[^ \n]*:[a-zA-Z_]+[^ \n]*', puml)
        if colon_params:
            for cp in colon_params:
                errors.append((cid, f"Sintaxis de endpoint inválida: se usó ':param' en '{cp}', use '{{param}}'"))

        # 8. Check Traceability against Narratives
        if narratives_metadata and cid in narratives_metadata:
            meta = narratives_metadata[cid]
            # Check fases
            for f in meta["fases"]:
                if f"Fase {f}:" not in puml:
                    errors.append((cid, f"Trazabilidad: Falta Fase {f} en el diagrama de secuencia"))
            # Check alts
            for a in meta["alts"]:
                if a not in puml:
                    errors.append((cid, f"Trazabilidad: Falta flujo alternativo {a} en el diagrama de secuencia"))
            # Check excs
            for e in meta["excs"]:
                if e not in puml:
                    errors.append((cid, f"Trazabilidad: Falta flujo de excepción {e} en el diagrama de secuencia"))

    # Check order
    if found_cus_list != EXPECTED_CUS_ORDER:
        errors.append(("GLOBAL", f"Orden de CUS desalineado!\nEsperado: {EXPECTED_CUS_ORDER}\nEncontrado: {found_cus_list}"))

    print(f"Resultado auditoría {source_name}: {len(errors)} errores detectados.")
    for cid, err in errors:
        print(f"  [{cid}] {err}")

    return len(errors)

if __name__ == "__main__":
    meta = extract_narrative_metadata("docs/diseño/NARRATIVAS_FASE_DISEÑO_CONSOLIDADAS.md")
    
    # Audit standalone file if exists
    standalone = "docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md"
    errs = 0
    if os.path.exists(standalone):
        with open(standalone, "r", encoding="utf-8") as f:
            content = f.read()
        errs += audit_sequence_content(content, standalone, meta)
    else:
        print(f"Archivo {standalone} no existe aún para auditar.")

    sys.exit(errs)
