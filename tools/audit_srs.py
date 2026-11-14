#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit script for Section 6.2.3 in docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md,
docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md, and docs/analisis/NARRATIVAS_SRS_CONSOLIDADAS.md
"""
import re
import sys

def audit_narratives(sec, filepath):
    print(f"=== Auditing {filepath} ===")
    cus_blocks = re.split(r'\n(?=####\s+CUS-\d+)', sec)
    print(f"Total CUS blocks found: {len(cus_blocks)-1}")

    expected_attrs = [
        (r'\*\*Id Caso de Uso\*\*', 'Id Caso de Uso'),
        (r'\*\*Nombre\*\*', 'Nombre'),
        (r'\*\*Tipo\*\*', 'Tipo'),
        (r'\*\*Requisito ID \(RF\)\*\*', 'Requisito ID (RF)'),
        (r'\*\*Versi[oó]n\*\*', 'Versión'),
        (r'\*\*Autor\*\*', 'Autor'),
        (r'\*\*Actores\*\*', 'Actores'),
        (r'\*\*Interacci[oó]n\*\*', 'Interacción'),
        (r'\*\*Descripci[oó]n\*\*', 'Descripción'),
        (r'\*\*Referencias\*\*', 'Referencias'),
        (r'\*\*Anexos\*\*', 'Anexos'),
        (r'\*\*Precondiciones\*\*', 'Precondiciones'),
        (r'\*\*(?:PostCondiciones|Postcondiciones)\*\*', 'PostCondiciones')
    ]

    all_errors = []

    expected_cus_order = [
        'CUS-001', 'CUS-010', # MOD-01
        'CUS-006', 'CUS-008', # MOD-02
        'CUS-005', 'CUS-021', # MOD-03
        'CUS-002', 'CUS-003', # MOD-04
        'CUS-004', 'CUS-024', 'CUS-017', 'CUS-023', 'CUS-007', # MOD-05
        'CUS-012', 'CUS-013', 'CUS-014', # MOD-06
        'CUS-018', 'CUS-019', # MOD-07
        'CUS-009', 'CUS-011', 'CUS-015', 'CUS-016', 'CUS-020', 'CUS-022' # MOD-08
    ]

    found_cus_order = []

    for idx, block in enumerate(cus_blocks[1:], 1):
        header = block.strip().splitlines()[0]
        m_id = re.match(r'####\s+(CUS-\d+)\s+-\s+(.*)', header)
        cid = m_id.group(1) if m_id else f"Block {idx}"
        cname = m_id.group(2) if m_id else "Unknown"
        found_cus_order.append(cid)

        # 1. Attributes
        for pat, attr_name in expected_attrs:
            if not re.search(pat, block):
                all_errors.append((cid, f"Ficha Técnica: Missing attribute '{attr_name}'"))

        # Check Versión 2.0
        if not re.search(r'\|\s*\*\*Versi[oó]n\*\*\s*\|\s*2\.0\s*\|', block):
            all_errors.append((cid, "Ficha Técnica: Versión is not '2.0'"))

        # Check Autor
        if ('Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos' not in block and
            'Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian' not in block):
            all_errors.append((cid, "Ficha Técnica: Autor mismatch"))

        # Check Tipo format
        if not re.search(r'Obligatorio\s*\(\s*[X\s]\s*\)\s*/\s*Opcional\s*\(\s*[X\s]\s*\)', block):
            all_errors.append((cid, "Ficha Técnica: Tipo does not match 'Obligatorio ( X ) / Opcional (   )'"))

        subsections = re.split(r'\n(?=#####\s+)', block)
        normal_flow_sec = None
        alt_flow_secs = []
        exc_flow_secs = []

        for sub in subsections:
            sh = sub.strip().splitlines()[0]
            if 'Flujo Normal de Eventos' in sh:
                normal_flow_sec = sub
            elif 'Flujo alternativo' in sh:
                alt_flow_secs.append(sub)
            elif 'Flujo de excepción' in sh or 'Flujo de excepci' in sh:
                exc_flow_secs.append(sub)

        if not normal_flow_sec:
            all_errors.append((cid, "Missing 'Flujo Normal de Eventos'"))
            continue

        # Check normal flow table
        if '| Usuario | Sistema |' not in normal_flow_sec:
            all_errors.append((cid, "Flujo Normal: Missing '| Usuario | Sistema |' table header"))

        normal_steps = [int(x) for x in re.findall(r'\*\*(\d+)\.\*\*', normal_flow_sec)]
        if not normal_steps:
            all_errors.append((cid, "Flujo Normal: No steps found"))
        else:
            if normal_steps != list(range(1, max(normal_steps)+1)):
                all_errors.append((cid, f"Flujo Normal: Step numbers not sequential: {normal_steps}"))

        # Subfases in normal flow
        subfases = re.findall(r'\*\*Fase\s+\d+:\s+.*?\*\*', normal_flow_sec)
        if len(subfases) < 2:
            all_errors.append((cid, f"Flujo Normal: Less than 2 subfases found ({len(subfases)})"))

        # Jumps in the whole block
        jumps_in_block = re.findall(r'salta a\s+([AE]\d+)', block)

        # Alt flows
        defined_alts = []
        for asub in alt_flow_secs:
            ah = asub.strip().splitlines()[0]
            m_a = re.search(r'Flujo alternativo\s+(A\d+):\s*(.*)', ah)
            if not m_a:
                all_errors.append((cid, f"Alt flow header invalid: {ah}"))
                continue
            aid = m_a.group(1)
            defined_alts.append(aid)

            # Steps
            asteps = re.findall(r'\*\*(' + aid + r'-\d+\.\d+)\*\*', asub)
            if not asteps:
                all_errors.append((cid, f"Alt flow {aid} has no valid numbered steps ({aid}-1.1, etc.)"))

            # Closure
            if not any(k in asub for k in ['retorna al paso', 'finaliza el caso de uso', 'finaliza la interacción', 'finaliza la sesion', 'finaliza la sesión', 'concluye el caso de uso', 'cancela la operación', 'sin generar registros']):
                all_errors.append((cid, f"Alt flow {aid} missing closure clause"))

            # Return step
            ret_m = re.findall(r'retorna al paso\s+(\d+)\s+del Flujo Normal', asub)
            for rs in ret_m:
                if int(rs) not in normal_steps:
                    all_errors.append((cid, f"Alt flow {aid} returns to non-existent step {rs}"))

        # Exc flows
        defined_excs = []
        for esub in exc_flow_secs:
            eh = esub.strip().splitlines()[0]
            m_e = re.search(r'Flujo de excepci[oó]n\s+(E\d+):\s*(.*)', eh)
            if not m_e:
                all_errors.append((cid, f"Exc flow header invalid: {eh}"))
                continue
            eid = m_e.group(1)
            defined_excs.append(eid)

            # Steps
            esteps = re.findall(r'\*\*(' + eid + r'-\d+\.\d+)\*\*', esub)
            if not esteps:
                all_errors.append((cid, f"Exc flow {eid} has no valid numbered steps ({eid}-1.1, etc.)"))

            # Closure
            if not any(k in esub for k in ['retorna al paso', 'finaliza el caso de uso', 'finaliza la interacción', 'finaliza la sesion', 'finaliza la sesión', 'concluye el caso de uso', 'cancela la operación', 'sin generar registros']):
                all_errors.append((cid, f"Exc flow {eid} missing closure clause"))

            # Return step
            ret_m = re.findall(r'retorna al paso\s+(\d+)\s+del Flujo Normal', esub)
            for rs in ret_m:
                if int(rs) not in normal_steps:
                    all_errors.append((cid, f"Exc flow {eid} returns to non-existent step {rs}"))

        # Check orphaned flows (defined but no jump to it)
        for aid in defined_alts:
            if aid not in jumps_in_block:
                all_errors.append((cid, f"Orphaned Alt flow: '{aid}' defined but no 'salta a {aid}' exists!"))
        for eid in defined_excs:
            if eid not in jumps_in_block:
                all_errors.append((cid, f"Orphaned Exc flow: '{eid}' defined but no 'salta a {eid}' exists!"))

        # Check broken jumps (jump to non-existent flow)
        for j in jumps_in_block:
            if j.startswith('A') and j not in defined_alts:
                all_errors.append((cid, f"Broken jump: jumps to '{j}', but '{j}' is not defined in this CUS!"))
            elif j.startswith('E') and j not in defined_excs:
                all_errors.append((cid, f"Broken jump: jumps to '{j}', but '{j}' is not defined in this CUS!"))

        # Check prohibited styling
        color_hex = re.findall(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b', block)
        if color_hex:
            all_errors.append((cid, f"Prohibited CSS hex colors found: {color_hex}"))
        px_matches = re.findall(r'\b\d+px\b', block)
        if px_matches:
            all_errors.append((cid, f"Prohibited px dimensions found: {px_matches}"))
        opacity_matches = re.findall(r'\b\d+%\s*(?:de\s+)?opacidad\b', block, re.IGNORECASE)
        if opacity_matches:
            all_errors.append((cid, f"Prohibited opacity found: {opacity_matches}"))

    # Check CUS order
    if found_cus_order != expected_cus_order:
        all_errors.append(('GLOBAL', f"CUS order mismatch!\nExpected: {expected_cus_order}\nFound:    {found_cus_order}"))

    print(f"Results for {filepath}: {len(all_errors)} errors.")
    for cid, err in all_errors:
        print(f"  [{cid}] {err}")

    return len(all_errors)

def audit_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    m_start = re.search(r'## 6\.2\.3\.?\s+Escenarios de Casos de Uso', text)
    m_next = re.search(r'#+\s+6\.3\.?\s+Modelo L[oó]gico', text)
    if m_start and m_next:
        sec = text[m_start.start():m_next.start()]
    elif m_start and not m_next:
        sec = text[m_start.start():]
    else:
        # Standalone
        sec = text

    return audit_narratives(sec, filepath)

if __name__ == "__main__":
    errs1 = audit_file("docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md")
    errs2 = audit_file("docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md")
    errs3 = audit_file("docs/analisis/NARRATIVAS_SRS_CONSOLIDADAS.md")
    errs4 = audit_file("docs/diseño/NARRATIVAS_FASE_DISEÑO_CONSOLIDADAS.md")
    sys.exit(errs1 + errs2 + errs3 + errs4)
