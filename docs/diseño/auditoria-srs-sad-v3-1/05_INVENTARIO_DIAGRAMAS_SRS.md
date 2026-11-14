# Inventario Integral de Diagramas PlantUML del SRS v3.1 [D01]

**Documento:** `docs/diseño/auditoria-srs-sad-v3-1/05_INVENTARIO_DIAGRAMAS_SRS.md`  
**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Equipo Consultor:** C-SharkTeam (Grupo 03)  
**Responsables:** Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani  
**Cátedra:** Construcción de Software I (Semestre 2026-II)  
**Rama de Trabajo:** `docs/srs-diagramas-renderizados`  
**Commit Base de `main`:** `b5408f2303fd8e0eb54803294d7385a51166d47d`  
**Fecha de Auditoría:** 14 de noviembre de 2026  
**Estado:** Diagnóstico e Inventario Concluido (Fase 1 / Hito D01)

---

## 1. Resumen Ejecutivo y Diagnóstico de Situación Actual

En el marco de la auditoría y refinamiento documental para la presentación final y exportación oficial a formato DOCX / Google Docs del **Informe de Especificación de Requisitos de Software (SRS v3.1)**, se realizó la inspección exhaustiva de los artefactos documentales maestros y scripts generadores.

### Diagnóstico Principal:
- Se identificaron exactamente **119 bloques de código fuente PlantUML** (` ```plantuml ... ``` ` con directivas `@startuml ... @enduml`) insertados directamente como texto plano en el cuerpo del documento maestro `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md`.
- Esta condición provoca que en visores Markdown estándar, convertidores Pandoc o al exportar a Microsoft Word (.docx), los diagramas se muestren como bloques crudos de código de programación en lugar de figuras gráficas y diagramas visuales renderizados.
- **Meta Operativa del Plan D01–D05:** Extraer la totalidad de las 119 fuentes PlantUML a archivos independientes estructurados `.puml`, renderizarlos a imágenes de alta definición PNG (óptimas para incrustación DOCX sin pérdida de legibilidad) y sustituir los bloques de código por figuras formales bajo el estándar académico D-2 de la facultad.

## 2. Métricas y Distribución General de Diagramas

A continuación, se presentan los consolidados cuantitativos por tipo de modelo UML y por ubicación seccional:

### Cuadro 2.1: Distribución de los 119 Diagramas por Tipo de Modelo UML

| Categoría / Tipo de Diagrama UML | Cantidad de Diagramas | Porcentaje | Propósito en el Documento SRS |
|:---|:---:|:---:|:---|
| **Ciclo de Vida / Fases de Proceso** | **106** | 89.1% | Especificación y formalización visual del comportamiento y estructura. |
| **Casos de Uso (General / Modular)** | **6** | 5.0% | Especificación y formalización visual del comportamiento y estructura. |
| **Actividades de Negocio (As-Is / To-Be)** | **2** | 1.7% | Especificación y formalización visual del comportamiento y estructura. |
| **Clases Conceptuales del Dominio** | **2** | 1.7% | Especificación y formalización visual del comportamiento y estructura. |
| **Organigrama Estructural** | **1** | 0.8% | Especificación y formalización visual del comportamiento y estructura. |
| **Paquetes Arquitecturales y Subsistemas** | **1** | 0.8% | Especificación y formalización visual del comportamiento y estructura. |
| **UML General** | **1** | 0.8% | Especificación y formalización visual del comportamiento y estructura. |
| **Total Consolidado** | **119** | **100.0%** | **119 diagramas identificados en el SRS v3.1.** |

Fuente: Elaboración propia a partir del escaneo del documento maestro `FD03-EPIS-Informe SRS de Proyecto.md`.

### Cuadro 2.2: Distribución de Diagramas por Sección del SRS y Archivo Generador

| Sección del SRS | Denominación Temática | Cantidad | Script Generador en `tools/` |
|:---|:---|:---:|:---|
| **6.0 Metodología** | Vistas y modelos de requisitos y diseño | **106** | Generador modular específico |
| **6.2.2 Casos de Uso** | Vistas y modelos de requisitos y diseño | **6** | Generador modular específico |
| **6.2 Modelo Conceptual** | Vistas y modelos de requisitos y diseño | **2** | Generador modular específico |
| **2.4 Organigrama** | Vistas y modelos de requisitos y diseño | **1** | Generador modular específico |
| **4.1 Proceso As-Is** | Vistas y modelos de requisitos y diseño | **1** | Generador modular específico |
| **4.2 Proceso To-Be** | Vistas y modelos de requisitos y diseño | **1** | Generador modular específico |
| **6.2.1 Paquetes** | Vistas y modelos de requisitos y diseño | **1** | Generador modular específico |
| **Sec. 2 / 4 / 6** | Vistas y modelos de requisitos y diseño | **1** | Generador modular específico |
| **Gran Total** | Cobertura integral del documento | **119** | **Pipeline `tools/build_design_srs_full.py`** |

Fuente: Elaboración propia.

## 3. Inventario Completo y Detallado de los 119 Diagramas PlantUML

A continuación, se detalla el censo individual de la totalidad de diagramas que conforman el informe SRS:

### Cuadro 3.1: Censo Exhaustivo de Diagramas PlantUML del SRS v3.1 (1 al 119)

| N° | Identificador | Título Oficial del Diagrama | Sección SRS | Tipo UML | CUS / Módulo | Archivo Fuente | Estado Actual |
|:---:|:---:|:---|:---:|:---|:---:|:---|:---:|
| 001 | **Diagrama 2.1** | Organigrama Funcional del Equipo Consultor C-SharkTeam | 2.4 Organigrama | Organigrama Estructural | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 002 | **Diagrama 4.1** | Diagrama de Actividades del Proceso Actual de Asesoría Informal (As-Is) | 4.1 Proceso As-Is | Actividades de Negocio (As-Is / To-Be) | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 003 | **Diagrama 4.2** | Diagrama de Actividades del Proceso Propuesto de Mentorías P2P (To-Be) | 4.2 Proceso To-Be | Actividades de Negocio (As-Is / To-Be) | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 004 | **Diagrama 6.1** | Fases del Ciclo de Vida del Desarrollo de Software (Metodología UWE - Semestre 2026-II) | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 005 | **Diagrama 6.2** | Diagrama de Clases Conceptuales del Dominio - Sistema Web P2P EPIS-UPT | 6.2 Modelo Conceptual | Clases Conceptuales del Dominio | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 006 | **Diagrama 6.3** | Diagrama de Paquetes Arquitecturales y Subsistemas del Sistema Web P2P | 6.2.1 Paquetes | Paquetes Arquitecturales y Subsistemas | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 007 | **Diagrama 6.4** | Diagrama de Casos de Uso General Consolidado del Sistema Web P2P (CUS-001 al CUS-024) | 6.2.2 Casos de Uso | Casos de Uso (General / Modular) | CUS-001 | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 008 | **Diagrama 6.5** | Diagrama de Casos de Uso - MOD-01: Seguridad, Autenticación y Gobernanza | 6.2.2 Casos de Uso | Casos de Uso (General / Modular) | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 009 | **Diagrama 6.6** | Diagrama de Casos de Uso - MOD-02: Ofertas de Mentoría y Gestión de Recursos | 6.2.2 Casos de Uso | Casos de Uso (General / Modular) | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 010 | **Diagrama 6.7** | Diagrama de Casos de Uso - MOD-03: Perfil del Mentor y Plan de Aprendizaje | 6.2.2 Casos de Uso | Casos de Uso (General / Modular) | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 011 | **Diagrama 6.8** | Diagrama de Casos de Uso - MOD-04: Demanda y Recomendaciones Personalizadas | 6.2.2 Casos de Uso | Casos de Uso (General / Modular) | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 012 | **Diagrama 6.9** | Diagrama de Casos de Uso - MOD-05: Quórum, Confirmación y Cancelaciones | 6.2.2 Casos de Uso | Casos de Uso (General / Modular) | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 013 | **Diagrama 6.10** | Diagrama de Casos de Uso - MOD-06: Asistencia, Bitácoras y Feedback | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 014 | **Diagrama 6.11** | Diagrama de Casos de Uso - MOD-07: Gamificación e Incentivos | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 015 | **Diagrama 6.12** | Diagrama de Casos de Uso - MOD-08: Analítica, Notificaciones y Configuración | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | Transversal / General | `tools/design_sections/generate_part_a.py` | Solo código PlantUML (crudo en Markdown) |
| 016 | **Diagrama 6.13** | Diagrama de Análisis de Objetos (Modelo ECB) - Flujo General de Mentorías P2P | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | Transversal / General | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 017 | **Diagrama 6.13.1** | Análisis de Objetos (Modelo ECB) - CUS-001: Iniciar sesión institucional con 2FA | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-001 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 018 | **Diagrama 6.13.2** | Análisis de Objetos (Modelo ECB) - CUS-010: Gestionar asignación de roles de usuario | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-010 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 019 | **Diagrama 6.13.3** | Análisis de Objetos (Modelo ECB) - CUS-006: Publicar oferta de mentoría académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-006 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 020 | **Diagrama 6.13.4** | Análisis de Objetos (Modelo ECB) - CUS-008: Consultar disponibilidad de espacios y recursos | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-008 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 021 | **Diagrama 6.13.5** | Análisis de Objetos (Modelo ECB) - CUS-005: Gestionar perfil formativo y disponibilidad horaria | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-005 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 022 | **Diagrama 6.13.6** | Análisis de Objetos (Modelo ECB) - CUS-021: Explorar catálogo curricular de asignaturas filtro | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-021 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 023 | **Diagrama 6.13.7** | Análisis de Objetos (Modelo ECB) - CUS-002: Explorar recomendaciones personalizadas Top-k | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-002 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 024 | **Diagrama 6.13.8** | Análisis de Objetos (Modelo ECB) - CUS-003: Registrar solicitud de demanda académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-003 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 025 | **Diagrama 6.13.9** | Análisis de Objetos (Modelo ECB) - CUS-004: Reservar cupo de mentoría académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-004 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 026 | **Diagrama 6.13.10** | Análisis de Objetos (Modelo ECB) - CUS-024: Ratificar asistencia a sesión de mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-024 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 027 | **Diagrama 6.13.11** | Análisis de Objetos (Modelo ECB) - CUS-017: Desistir voluntariamente de reserva | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-017 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 028 | **Diagrama 6.13.12** | Análisis de Objetos (Modelo ECB) - CUS-023: Evaluar quórum automático a T-24h | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-023 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 029 | **Diagrama 6.13.13** | Análisis de Objetos (Modelo ECB) - CUS-007: Decisión del mentor ante quórum insuficiente | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-007 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 030 | **Diagrama 6.13.14** | Análisis de Objetos (Modelo ECB) - CUS-012: Registrar asistencia a sesión de mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-012 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 031 | **Diagrama 6.13.15** | Análisis de Objetos (Modelo ECB) - CUS-013: Registrar bitácora académica de sesión | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-013 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 032 | **Diagrama 6.13.16** | Análisis de Objetos (Modelo ECB) - CUS-014: Visualizar historial y bitácoras académicas | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-014 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 033 | **Diagrama 6.13.17** | Análisis de Objetos (Modelo ECB) - CUS-018: Emitir constancia institucional de horas de mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-018 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 034 | **Diagrama 6.13.18** | Análisis de Objetos (Modelo ECB) - CUS-019: Gestionar insignias y reputación gamificada | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-019 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 035 | **Diagrama 6.13.19** | Análisis de Objetos (Modelo ECB) - CUS-009: Notificar eventos críticos y alertas temporales | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-009 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 036 | **Diagrama 6.13.20** | Análisis de Objetos (Modelo ECB) - CUS-011: Generar reportes e indicadores de analítica académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-011 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 037 | **Diagrama 6.13.21** | Análisis de Objetos (Modelo ECB) - CUS-015: Consultar métricas de retención y desempeño | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-015 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 038 | **Diagrama 6.13.22** | Análisis de Objetos (Modelo ECB) - CUS-016: Auditar trazas de seguridad y consentimiento Ley 29733 | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-016 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 039 | **Diagrama 6.13.23** | Análisis de Objetos (Modelo ECB) - CUS-020: Configurar parámetros institucionales y umbrales | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-020 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 040 | **Diagrama 6.13.24** | Análisis de Objetos (Modelo ECB) - CUS-022: Gestionar catálogo de temas y materias críticas | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-022 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 041 | **Diagrama 6.14** | Diagrama de Actividades con Flujo de Objetos del Ciclo de Mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | Transversal / General | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 042 | **Diagrama 6.14.1** | Diagrama de Actividades con Flujo de Objetos - CUS-001: Iniciar sesión institucional con 2FA | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-001 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 043 | **Diagrama 6.14.2** | Diagrama de Actividades con Flujo de Objetos - CUS-010: Gestionar asignación de roles de usuario | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-010 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 044 | **Diagrama 6.14.3** | Diagrama de Actividades con Flujo de Objetos - CUS-006: Publicar oferta de mentoría académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-006 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 045 | **Diagrama 6.14.4** | Diagrama de Actividades con Flujo de Objetos - CUS-008: Consultar disponibilidad de espacios y recursos | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-008 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 046 | **Diagrama 6.14.5** | Diagrama de Actividades con Flujo de Objetos - CUS-005: Gestionar perfil formativo y disponibilidad horaria | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-005 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 047 | **Diagrama 6.14.6** | Diagrama de Actividades con Flujo de Objetos - CUS-021: Explorar catálogo curricular de asignaturas filtro | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-021 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 048 | **Diagrama 6.14.7** | Diagrama de Actividades con Flujo de Objetos - CUS-002: Explorar recomendaciones personalizadas Top-k | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-002 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 049 | **Diagrama 6.14.8** | Diagrama de Actividades con Flujo de Objetos - CUS-003: Registrar solicitud de demanda académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-003 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 050 | **Diagrama 6.14.9** | Diagrama de Actividades con Flujo de Objetos - CUS-004: Reservar cupo de mentoría académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-004 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 051 | **Diagrama 6.14.10** | Diagrama de Actividades con Flujo de Objetos - CUS-024: Ratificar asistencia a sesión de mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-024 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 052 | **Diagrama 6.14.11** | Diagrama de Actividades con Flujo de Objetos - CUS-017: Desistir voluntariamente de reserva | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-017 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 053 | **Diagrama 6.14.12** | Diagrama de Actividades con Flujo de Objetos - CUS-023: Evaluar quórum automático a T-24h | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-023 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 054 | **Diagrama 6.14.13** | Diagrama de Actividades con Flujo de Objetos - CUS-007: Decisión del mentor ante quórum insuficiente | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-007 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 055 | **Diagrama 6.14.14** | Diagrama de Actividades con Flujo de Objetos - CUS-012: Registrar asistencia a sesión de mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-012 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 056 | **Diagrama 6.14.15** | Diagrama de Actividades con Flujo de Objetos - CUS-013: Registrar bitácora académica de sesión | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-013 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 057 | **Diagrama 6.14.16** | Diagrama de Actividades con Flujo de Objetos - CUS-014: Visualizar historial y bitácoras académicas | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-014 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 058 | **Diagrama 6.14.17** | Diagrama de Actividades con Flujo de Objetos - CUS-018: Emitir constancia institucional de horas de mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-018 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 059 | **Diagrama 6.14.18** | Diagrama de Actividades con Flujo de Objetos - CUS-019: Gestionar insignias y reputación gamificada | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-019 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 060 | **Diagrama 6.14.19** | Diagrama de Actividades con Flujo de Objetos - CUS-009: Notificar eventos críticos y alertas temporales | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-009 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 061 | **Diagrama 6.14.20** | Diagrama de Actividades con Flujo de Objetos - CUS-011: Generar reportes e indicadores de analítica académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-011 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 062 | **Diagrama 6.14.21** | Diagrama de Actividades con Flujo de Objetos - CUS-015: Consultar métricas de retención y desempeño | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-015 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 063 | **Diagrama 6.14.22** | Diagrama de Actividades con Flujo de Objetos - CUS-016: Auditar trazas de seguridad y consentimiento Ley 29733 | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-016 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 064 | **Diagrama 6.14.23** | Diagrama de Actividades con Flujo de Objetos - CUS-020: Configurar parámetros institucionales y umbrales | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-020 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 065 | **Diagrama 6.14.24** | Diagrama de Actividades con Flujo de Objetos - CUS-022: Gestionar catálogo de temas y materias críticas | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-022 | `tools/design_sections/generate_part_c.py` | Solo código PlantUML (crudo en Markdown) |
| 066 | **Diagrama 6.15** | Diagrama de Secuencia General del Ciclo Transaccional de Mentorías | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | Transversal / General | `tools/build_design_sequence_diagrams.py` | Solo código PlantUML (crudo en Markdown) |
| 067 | **Diagrama 6.15.1** | Diagrama de Secuencia - CUS-001: Iniciar sesión institucional con 2FA | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-001 | `tools/design_sequence_diagrams/mod01_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 068 | **Diagrama 6.15.2** | Diagrama de Secuencia - CUS-010: Gestionar asignación de roles de usuario | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-010 | `tools/design_sequence_diagrams/mod01_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 069 | **Diagrama 69** | Diagrama 6.15.3: Diagrama de Secuencia - CUS-006: Publicar oferta de mentoría académica - Sistema Web P2P - EPIS UPT | Sec. 2 / 4 / 6 | UML General | CUS-006 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 070 | **Diagrama 6.15.4** | Diagrama de Secuencia - CUS-008: Consultar disponibilidad de espacios y recursos | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-008 | `tools/design_sequence_diagrams/mod02_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 071 | **Diagrama 6.15.5** | Diagrama de Secuencia - CUS-005: Gestionar perfil académico y disponibilidad horaria | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-005 | `tools/design_sequence_diagrams/mod03_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 072 | **Diagrama 6.15.6** | Diagrama de Secuencia - CUS-021: Explorar catálogo curricular de asignaturas filtro | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-021 | `tools/design_sequence_diagrams/mod03_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 073 | **Diagrama 6.15.7** | Diagrama de Secuencia - CUS-002: Explorar recomendaciones personalizadas Top-k | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-002 | `tools/design_sequence_diagrams/mod04_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 074 | **Diagrama 6.15.8** | Diagrama de Secuencia - CUS-003: Registrar solicitud de demanda académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-003 | `tools/design_sequence_diagrams/mod04_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 075 | **Diagrama 6.15.9** | Diagrama de Secuencia - CUS-004: Reservar cupo de mentoría académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-004 | `tools/design_sequence_diagrams/mod05_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 076 | **Diagrama 6.15.10** | Diagrama de Secuencia - CUS-024: Ratificar asistencia a sesión de mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-024 | `tools/design_sequence_diagrams/mod05_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 077 | **Diagrama 6.15.11** | Diagrama de Secuencia - CUS-017: Desistir voluntariamente de reserva | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-017 | `tools/design_sequence_diagrams/mod05_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 078 | **Diagrama 6.15.12** | Diagrama de Secuencia - CUS-023: Evaluar quórum automático a T-24h | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-023 | `tools/design_sequence_diagrams/mod05_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 079 | **Diagrama 6.15.13** | Diagrama de Secuencia - CUS-007: Decisión del mentor ante quórum insuficiente | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-007 | `tools/design_sequence_diagrams/mod05_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 080 | **Diagrama 6.15.14** | Diagrama de Secuencia - CUS-012: Registrar asistencia a sesión de mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-012 | `tools/design_sequence_diagrams/mod06_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 081 | **Diagrama 6.15.15** | Diagrama de Secuencia - CUS-013: Registrar bitácora pedagógica de sesión | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-013 | `tools/design_sequence_diagrams/mod06_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 082 | **Diagrama 6.15.16** | Diagrama de Secuencia - CUS-014: Visualizar historial y bitácoras académicas | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-014 | `tools/design_sequence_diagrams/mod06_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 083 | **Diagrama 6.15.17** | Diagrama de Secuencia - CUS-018: Emitir constancia institucional de horas de mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-018 | `tools/design_sequence_diagrams/mod07_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 084 | **Diagrama 6.15.18** | Diagrama de Secuencia - CUS-019: Gestionar insignias y reputación gamificada | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-019 | `tools/design_sequence_diagrams/mod07_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 085 | **Diagrama 6.15.19** | Diagrama de Secuencia - CUS-009: Notificar eventos críticos y alertas temporales | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-009 | `tools/design_sequence_diagrams/mod08_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 086 | **Diagrama 6.15.20** | Diagrama de Secuencia - CUS-011: Generar reportes e indicadores analíticos | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-011 | `tools/design_sequence_diagrams/mod08_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 087 | **Diagrama 6.15.21** | Diagrama de Secuencia - CUS-015: Consultar métricas de retención y desempeño | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-015 | `tools/design_sequence_diagrams/mod08_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 088 | **Diagrama 6.15.22** | Diagrama de Secuencia - CUS-016: Auditar trazas de seguridad y consentimiento | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-016 | `tools/design_sequence_diagrams/mod08_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 089 | **Diagrama 6.15.23** | Diagrama de Secuencia - CUS-020: Configurar parámetros institucionales y umbrales | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-020 | `tools/design_sequence_diagrams/mod08_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 090 | **Diagrama 6.15.24** | Diagrama de Secuencia - CUS-022: Gestionar catálogo de temas y materias críticas | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-022 | `tools/design_sequence_diagrams/mod08_seq.py` | Solo código PlantUML (crudo en Markdown) |
| 091 | **Diagrama 6.16** | Diagrama de Clases del Modelo Lógico del Sistema Web P2P | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | Transversal / General | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 092 | **Diagrama 6.16.1** | Diagrama de Clases Lógico Parcial - CUS-001: Iniciar sesión institucional con 2FA | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-001 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 093 | **Diagrama 6.16.2** | Diagrama de Clases Lógico Parcial - CUS-010: Gestionar asignación de roles de usuario | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-010 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 094 | **Diagrama 6.16.3** | Diagrama de Clases Lógico Parcial - CUS-006: Publicar oferta de mentoría académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-006 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 095 | **Diagrama 6.16.4** | Diagrama de Clases Lógico Parcial - CUS-008: Consultar disponibilidad de espacios y recursos | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-008 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 096 | **Diagrama 6.16.5** | Diagrama de Clases Lógico Parcial - CUS-005: Gestionar perfil formativo y disponibilidad horaria | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-005 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 097 | **Diagrama 6.16.6** | Diagrama de Clases Lógico Parcial - CUS-021: Explorar catálogo curricular de asignaturas filtro | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-021 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 098 | **Diagrama 6.16.7** | Diagrama de Clases Lógico Parcial - CUS-002: Explorar recomendaciones personalizadas Top-k | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-002 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 099 | **Diagrama 6.16.8** | Diagrama de Clases Lógico Parcial - CUS-003: Registrar solicitud de demanda académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-003 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 100 | **Diagrama 6.16.9** | Diagrama de Clases Lógico Parcial - CUS-004: Reservar cupo de mentoría académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-004 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 101 | **Diagrama 6.16.10** | Diagrama de Clases Lógico Parcial - CUS-024: Ratificar asistencia a sesión de mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-024 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 102 | **Diagrama 6.16.11** | Diagrama de Clases Lógico Parcial - CUS-017: Desistir voluntariamente de reserva | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-017 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 103 | **Diagrama 6.16.12** | Diagrama de Clases Lógico Parcial - CUS-023: Evaluar quórum automático a T-24h | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-023 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 104 | **Diagrama 6.16.13** | Diagrama de Clases Lógico Parcial - CUS-007: Decisión del mentor ante quórum insuficiente | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-007 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 105 | **Diagrama 6.16.14** | Diagrama de Clases Lógico Parcial - CUS-012: Registrar asistencia a sesión de mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-012 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 106 | **Diagrama 6.16.15** | Diagrama de Clases Lógico Parcial - CUS-013: Registrar bitácora académica de sesión | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-013 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 107 | **Diagrama 6.16.16** | Diagrama de Clases Lógico Parcial - CUS-014: Visualizar historial y bitácoras académicas | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-014 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 108 | **Diagrama 6.16.17** | Diagrama de Clases Lógico Parcial - CUS-018: Emitir constancia institucional de horas de mentoría | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-018 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 109 | **Diagrama 6.16.18** | Diagrama de Clases Lógico Parcial - CUS-019: Gestionar insignias y reputación gamificada | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-019 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 110 | **Diagrama 6.16.19** | Diagrama de Clases Lógico Parcial - CUS-009: Notificar eventos críticos y alertas temporales | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-009 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 111 | **Diagrama 6.16.20** | Diagrama de Clases Lógico Parcial - CUS-011: Generar reportes e indicadores de analítica académica | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-011 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 112 | **Diagrama 6.16.21** | Diagrama de Clases Lógico Parcial - CUS-015: Consultar métricas de retención y desempeño | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-015 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 113 | **Diagrama 6.16.22** | Diagrama de Clases Lógico Parcial - CUS-016: Auditar trazas de seguridad y consentimiento Ley 29733 | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-016 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 114 | **Diagrama 6.16.23** | Diagrama de Clases Lógico Parcial - CUS-020: Configurar parámetros institucionales y umbrales | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-020 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 115 | **Diagrama 6.16.24** | Diagrama de Clases Lógico Parcial - CUS-022: Gestionar catálogo de temas y materias críticas | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | CUS-022 | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 116 | **Diagrama 6.17** | Máquina de Estados Finitos - Ciclo de Vida de SesionMentoria | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | Transversal / General | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 117 | **Diagrama 6.18** | Máquina de Estados Finitos - Ciclo de Vida de ReservaCupo | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | Transversal / General | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 118 | **Diagrama 6.19** | Máquina de Estados Finitos - Ciclo de Vida de BitacoraPedagogica y CertificadoHoras | 6.0 Metodología | Ciclo de Vida / Fases de Proceso | Transversal / General | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |
| 119 | **Diagrama 6.20** | Diagrama Entidad-Relación Físico (15 Tablas Relacionales) - PostgreSQL | 6.2 Modelo Conceptual | Clases Conceptuales del Dominio | Transversal / General | `tools/design_sections/generate_part_e.py` | Solo código PlantUML (crudo en Markdown) |

Fuente: Elaboración propia mediante análisis estático automatizado de la línea base documental.

## 4. Análisis de la Infraestructura de Generación Documental

El documento maestro `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` no se edita directamente de forma manual, sino que se compila de manera determinista e idempotente mediante el ensamblador `tools/build_design_srs_full.py` a partir de seis componentes maestros:

1. **`tools/design_sections/generate_part_a.py` (15 diagramas):** Genera la Portada, Control de Versiones, Secciones 1 a 5 (con las 26 fichas de requisitos funcionales), Sección 6.1 (Perfiles RBAC), 6.2 (Clases Conceptuales), 6.2.1 (Paquetes) y 6.2.2 (Casos de Uso general y modulares).
2. **`tools/build_design_srs_narratives.py` (0 diagramas):** Genera la Sección 6.2.3 con los 24 escenarios narrativos detallados de casos de uso (CUS-001 al CUS-024).
3. **`tools/design_sections/generate_part_c.py` (50 diagramas):** Genera la Sección 6.3.1 (25 diagramas ECB: 1 general + 24 por CUS) y la Sección 6.3.2 (25 diagramas de actividades con objetos: 1 general + 24 por CUS).
4. **`tools/build_design_sequence_diagrams.py` (25 diagramas):** Ensambla a partir de `tools/design_sequence_diagrams/mod01_seq.py` a `mod08_seq.py` los 25 diagramas de secuencia DSS bajo estándar Visual Paradigm (1 general de integración + 24 individuales).
5. **`tools/design_sections/generate_part_e.py` (29 diagramas):** Genera la Sección 6.3.4 (25 diagramas de clases lógicas: 1 general + 24 individuales), Sección 6.3.5 (3 máquinas de estados finitos FSM) y Sección 6.3.6 (1 diagrama entidad-relación físico de 15 tablas).
6. **`tools/design_sections/generate_part_f.py` (0 diagramas):** Genera la Sección 7 (Conclusiones con métricas empíricas de S1–S8) y Sección 8 (Referencias bibliográficas).

## 5. Estrategia de Convención de Nombres y Estructura para Fases D02–D05

Para asegurar la portabilidad y trazabilidad absoluta, se define la siguiente arquitectura de almacenamiento de diagramas:

- **Directorio de fuentes PlantUML:** `docs/diseño/diagramas/srs/puml/`
- **Directorio de imágenes renderizadas:** `docs/diseño/diagramas/srs/img/`

### Convención de Nomenclatura Estandarizada:

- `diag_001_sec2_organigrama.puml` $\rightarrow$ `diag_001_sec2_organigrama.png`
- `diag_002_sec4_proceso_as_is.puml` $\rightarrow$ `diag_002_sec4_proceso_as_is.png`
- `diag_003_sec4_proceso_to_be.puml` $\rightarrow$ `diag_003_sec4_proceso_to_be.png`
- `diag_004_sec6_fases_metodologia.puml` $\rightarrow$ `diag_004_sec6_fases_metodologia.png`
- `diag_005_sec6_clases_conceptuales.puml` $\rightarrow$ `diag_005_sec6_clases_conceptuales.png`
- `diag_006_sec6_paquetes_arquitectura.puml` $\rightarrow$ `diag_006_sec6_paquetes_arquitectura.png`
- `diag_007_sec6_cus_general.puml` $\rightarrow$ `diag_007_sec6_cus_general.png`
- `diag_008_sec6_cus_mod01.puml` a `diag_015_sec6_cus_mod08.puml`
- `diag_016_sec6_ecb_general.puml` y `diag_017_sec6_ecb_cus001.puml` a `diag_040_sec6_ecb_cus022.puml`
- `diag_041_sec6_act_general.puml` y `diag_042_sec6_act_cus001.puml` a `diag_065_sec6_act_cus022.puml`
- `diag_066_sec6_seq_general.puml` y `diag_067_sec6_seq_cus001.puml` a `diag_090_sec6_seq_cus022.puml`
- `diag_091_sec6_logico_general.puml` y `diag_092_sec6_logico_cus001.puml` a `diag_115_sec6_logico_cus022.puml`
- `diag_116_sec6_fsm_sesion.puml`, `diag_117_sec6_fsm_reserva.puml`, `diag_118_sec6_fsm_bitacora_cert.puml`
- `diag_119_sec6_der_fisico_15tablas.puml` $\rightarrow$ `diag_119_sec6_der_fisico_15tablas.png`

## 6. Dictamen de Fase 1 [D01]

El diagnóstico concluye exitosamente con el inventario del 100% de diagramas PlantUML (119 diagramas atómicos). Queda expedito el repositorio para la ejecución de la **Fase 2 [D02]: Extracción y organización modular de fuentes PlantUML**.

---
*Fin del informe de inventario D01.*
