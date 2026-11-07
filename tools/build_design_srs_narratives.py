# -*- coding: utf-8 -*-
"""
Script to build, audit, and inject the Design Phase Use Case Narratives (Section 6.2.3)
into:
- docs/diseño/NARRATIVAS_FASE_DISEÑO_CONSOLIDADAS.md
- docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md
"""

import os
import sys
import re

# Add tools to sys.path
sys.path.insert(0, os.path.dirname(__file__))

from design_narratives.mod01 import get_mod01
from design_narratives.mod02 import get_mod02
from design_narratives.mod03 import get_mod03
from design_narratives.mod04 import get_mod04
from design_narratives.mod05 import get_mod05
from design_narratives.mod06 import get_mod06
from design_narratives.mod07 import get_mod07
from design_narratives.mod08 import get_mod08
from audit_srs import audit_narratives

def get_section_header():
    return """## 6.2.3. Escenarios de Casos de Uso (Fase de Diseño)

### Presentación de los Escenarios de Casos de Uso en Fase de Diseño

En la presente **Fase de Diseño de Software**, los escenarios de casos de uso traducen los requerimientos funcionales del sistema en especificaciones de comportamiento detalladas a nivel de arquitectura y código ejecutable. Cada especificación proporciona trazabilidad completa hacia los componentes de frontend (React 18 con TypeScript y Tailwind CSS), servicios y adaptadores HTTP (`apiClient`), controladores y rutas de FastAPI, esquemas de validación Pydantic, servicios de lógica de negocio, entidades del modelo relacional ORM en SQLAlchemy y transacciones ACID en PostgreSQL bajo control estricto de concurrencia y cerrojos pesimistas.

La estructura de cada caso de uso conserva con rigurosidad la plantilla canónica institucional:
1. **Ficha Técnica Estructurada (13 atributos):** Identificador unívoco (`Id Caso de Uso`), `Nombre`, `Tipo`, `Requisito ID (RF)`, `Versión` (2.0), `Autor`, `Actores` con roles de sistema (`UserRole`), `Interacción`, `Descripción` técnica exhaustiva, `Referencias` normativas y arquitectónicas, `Anexos` de código fuente, `Precondiciones` y `PostCondiciones`.
2. **Flujo Normal de Eventos:** Distribuido en columnas estrictas (**`Usuario`** | **`Sistema`**), subdividido en fases secuenciales de interacción con pasos numerados correlativamente y llamadas explícitas de desvío `(Si [condición], salta a E00X / A00X)`.
3. **Flujos Alternativos (`A00X`) y de Excepción (`E00X`):** Encabezados de bloque específicos, columnas **`Usuario`** | **`Sistema`**, pasos jerárquicos (`E00X-1.1`, `E00X-1.2`) y cláusula formal de retorno al paso correspondiente del Flujo Normal o cierre explícito del caso de uso.
4. **Trazabilidad de Código y Diseño:** Especificación exacta de endpoints RESTful, verbos HTTP, códigos de estado (`200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`, `503 Service Unavailable`), tipos de excepciones y directivas de control de concurrencia (`SELECT ... FOR UPDATE`, locks transaccionales y mecanismos de desempate).

A continuación, se presentan los 24 casos de uso canónicos estructurados en los 8 módulos arquitectónicos del sistema:

---

"""

def build_full_narratives():
    header = get_section_header()
    mods = [
        get_mod01(),
        get_mod02(),
        get_mod03(),
        get_mod04(),
        get_mod05(),
        get_mod06(),
        get_mod07(),
        get_mod08(),
    ]
    return header + "\n\n---\n\n".join(mods) + "\n\n"

def main():
    print("=== Generando Narrativas de Casos de Uso (Fase de Diseño) ===")
    content = build_full_narratives()
    
    # 1. Audit generated content in-memory
    print("Ejecutando auditoría estructural preliminar...")
    errors = audit_narratives(content, "Memoria (Fase de Diseño)")
    if errors > 0:
        print(f"ERROR: Se detectaron {errors} errores en la auditoría preliminar. Abortando escritura.")
        sys.exit(1)
    print("Auditoría preliminar exitosa: 0 errores detectados.")

    # 2. Write standalone consolidated file
    standalone_path = "docs/diseño/NARRATIVAS_FASE_DISEÑO_CONSOLIDADAS.md"
    print(f"Escribiendo {standalone_path}...")
    with open(standalone_path, "w", encoding="utf-8") as f:
        f.write("# NARRATIVAS DE CASOS DE USO CONSOLIDADAS - FASE DE DISEÑO\n\n")
        f.write("**Sistema Web P2P de Mentorías Universitarias - EPIS UPT**\n")
        f.write("**Versión:** 2.0 (Fase de Diseño / Arquitectura y Construcción)\n")
        f.write("**Autores:** Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos\n\n---\n\n")
        f.write(content)

    # 3. Inject into docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md
    target_srs = "docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md"
    print(f"Inyectando sección 6.2.3 en {target_srs}...")
    with open(target_srs, "r", encoding="utf-8") as f:
        srs_text = f.read()

    m_start = re.search(r'## 6\.2\.3\.?\s+Escenarios de Casos de Uso', srs_text)
    m_next = re.search(r'#+\s+6\.3\.?\s+Modelo L[oó]gico', srs_text)

    if not m_start or not m_next:
        print("ERROR: No se pudieron localizar los delimitadores de la sección 6.2.3 en el SRS.")
        sys.exit(1)

    prefix = srs_text[:m_start.start()]
    suffix = srs_text[m_next.start():]
    new_srs_text = prefix + content + "---\n\n" + suffix

    with open(target_srs, "w", encoding="utf-8") as f:
        f.write(new_srs_text)

    print("Inyección completada.")

    # 4. Final Audit
    print("Ejecutando auditoría final sobre los archivos generados...")
    err1 = audit_narratives(content, standalone_path)
    
    # Audit target srs section
    m_start2 = re.search(r'## 6\.2\.3\.?\s+Escenarios de Casos de Uso', new_srs_text)
    m_next2 = re.search(r'#+\s+6\.3\.?\s+Modelo L[oó]gico', new_srs_text)
    srs_sec = new_srs_text[m_start2.start():m_next2.start()]
    err2 = audit_narratives(srs_sec, target_srs)

    total_errs = err1 + err2
    if total_errs == 0:
        print("=== PROCESO COMPLETADO EXITOSAMENTE CON 0 ERRORES ===")
    else:
        print(f"=== PROCESO CONCLUIDO CON {total_errs} ERRORES ===")
        sys.exit(1)

if __name__ == "__main__":
    main()
