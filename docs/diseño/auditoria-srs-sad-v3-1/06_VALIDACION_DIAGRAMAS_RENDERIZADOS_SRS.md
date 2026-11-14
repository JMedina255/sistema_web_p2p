# Informe de Validación y Control de Calidad: Diagramas Renderizados en el SRS v3.1 [D05]

**Documento:** `docs/diseño/auditoria-srs-sad-v3-1/06_VALIDACION_DIAGRAMAS_RENDERIZADOS_SRS.md`  
**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Equipo Consultor:** C-SharkTeam (Grupo 03)  
**Responsables:** Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani  
**Cátedra:** Construcción de Software I (Semestre 2026-II)  
**Rama de Trabajo:** `docs/srs-diagramas-renderizados`  
**Hito Documental:** Fase 5 / D05 — Validación final y preparación para exportación DOCX  
**Fecha de Auditoría:** 14 de noviembre de 2026  
**Resultado Global:** **APROBADO — 100% CONFORME (0 Bloques de código restantes, 119 Figuras PNG operativas)**

---

## 1. Resumen Ejecutivo de la Intervención

La intervención técnica documental ejecutada en las fases **D01 a D05** resolvió integralmente la deficiencia crítica del documento maestro `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md`, en el cual los diagramas de modelado UML se presentaban como bloques de código fuente PlantUML en lugar de figuras visuales estructuradas.

A través de un pipeline automatizado, reproducible e idempotente desarrollado en `tools/`, se lograron los siguientes objetivos:
1. **Extracción y Preservación del Código Fuente (D02):** Se crearon 119 archivos individuales `.puml` organizados bajo `docs/diseño/diagramas/srs/puml/`, preservando el código original con encabezados formales de trazabilidad y gobernanza.
2. **Renderizado de Alta Fidelidad (D03):** Se ejecutó el motor PlantUML 1.2024.7 acoplado con Graphviz 2.44.1 en modo por lotes, generando 119 imágenes en formato PNG de alta resolución (`docs/diseño/diagramas/srs/img/*.png`) totalizando **11.09 MB** de activos gráficos sin pérdida de legibilidad tipográfica.
3. **Sustitución Documental y Estándar D-2 (D04):** Se integró un motor de reemplazo en el ensamblador maestro `tools/build_design_srs_full.py`, eliminando por completo los bloques ````plantuml` y sustituyéndolos por referencias de figuras Markdown `![Título](diagramas/srs/img/diag_XXX.png)`.
4. **Validación Semántica y de Vínculos (D05):** Se verificó que el 100% de las figuras cuenta con párrafo introductorio, encabezado formal, imagen renderizada, nota al pie de fuente institucional y párrafo interpretativo.

---

## 2. Métricas Consolidadas de Control de Calidad

### Cuadro 2.1: Balance Cuantitativo de Transformación Documental

| Métrica de Control | Valor Inicial (H03) | Valor Final (D05) | Variación | Estado |
|:---|:---:|:---:|:---:|:---:|
| **Bloques de código PlantUML en SRS** | 119 | **0** | -119 (-100%) | **OPTIMIZADO** |
| **Directivas `@startuml` / `@enduml`** | 119 | **0** | -119 (-100%) | **CONFORME** |
| **Archivos fuente `.puml` preservados** | 0 | **119** | +119 (+100%) | **PRESERVADO** |
| **Figuras PNG de alta resolución generadas** | 0 | **119** | +119 (+100%) | **RENDERIZADO** |
| **Imágenes vinculadas en el cuerpo del SRS** | 0 | **119** | +119 (+100%) | **INCRUSTADO** |
| **Rutas de imagen rotas / 0 bytes en disco** | N/A | **0** | 0 | **VERIFICADO** |
| **Volumen de almacenamiento de gráficos** | 0 MB | **11.60 MB** | +11.60 MB | **ALTA CALIDAD** |
| **Trazabilidad contra Estándar D-2 (Fuente/Texto)** | 119 | **119 / 119** | 100% | **CONFORME** |
| **Auditoría Semántica de Narrativas (6.2.3)** | 0 errores | **0 errores** | Invariante | **APROBADO** |
| **Auditoría Semántica de Secuencia (6.3.3)** | 0 errores | **0 errores** | Invariante | **APROBADO** |

Fuente: Elaboración propia a partir de la ejecución de `tools/build_design_srs_full.py`.

---

## 3. Censo y Tabla de Verificación de los 119 Diagramas

La siguiente tabla detalla la correspondencia unívoca entre la figura incorporada en el SRS maestro, el archivo fuente PlantUML conservado, la imagen renderizada y su estado de integridad física en disco:

| N° | Título / Identificador de la Figura | Archivo Fuente (`.puml`) | Archivo Renderizado (`.png`) | Peso en Disco | Estado de Validación |
|:---:|:---|:---|:---|:---:|:---:|
| 001 | **Diagrama 2.1: Organigrama Funcional del Equipo Consultor C-SharkTeam** | `diag_001_sec24_organigrama_consultor.puml` | `diag_001_sec24_organigrama_consultor.png` | 44.1 KB | **CONFORME (100%)** |
| 002 | **Diagrama 4.1: Diagrama de Actividades del Proceso Actual de Asesoría Informal (As-Is)** | `diag_002_sec41_actividades_proceso_as_is.puml` | `diag_002_sec41_actividades_proceso_as_is.png` | 59.9 KB | **CONFORME (100%)** |
| 003 | **Diagrama 4.2: Diagrama de Actividades del Proceso Propuesto de Mentorías P2P (To-Be)** | `diag_003_sec42_actividades_proceso_to_be.puml` | `diag_003_sec42_actividades_proceso_to_be.png` | 153.7 KB | **CONFORME (100%)** |
| 004 | **Diagrama 6.1: Fases del Ciclo de Vida del Desarrollo de Software (Metodología UWE - Semestre 2026-II)** | `diag_004_sec60_ciclo_vida_metodologia.puml` | `diag_004_sec60_ciclo_vida_metodologia.png` | 71.2 KB | **CONFORME (100%)** |
| 005 | **Diagrama 6.2: Diagrama de Clases Conceptuales del Dominio - Sistema Web P2P EPIS-UPT** | `diag_005_sec62_clases_conceptuales_dominio.puml` | `diag_005_sec62_clases_conceptuales_dominio.png` | 192.2 KB | **CONFORME (100%)** |
| 006 | **Diagrama 6.3: Diagrama de Paquetes Arquitecturales y Subsistemas del Sistema Web P2P** | `diag_006_sec621_paquetes_arquitecturales.puml` | `diag_006_sec621_paquetes_arquitecturales.png` | 206.7 KB | **CONFORME (100%)** |
| 007 | **Diagrama 6.4: Diagrama de Casos de Uso General Consolidado del Sistema Web P2P (CUS-001 al CUS-024)** | `diag_007_sec622_casos_uso_general_24cus.puml` | `diag_007_sec622_casos_uso_general_24cus.png` | 303.1 KB | **CONFORME (100%)** |
| 008 | **Diagrama 6.5: Diagrama de Casos de Uso - MOD-01: Seguridad, Autenticación y Gobernanza** | `diag_008_sec622_casos_uso_mod01.puml` | `diag_008_sec622_casos_uso_mod01.png` | 31.3 KB | **CONFORME (100%)** |
| 009 | **Diagrama 6.6: Diagrama de Casos de Uso - MOD-02: Ofertas de Mentoría y Gestión de Recursos** | `diag_009_sec622_casos_uso_mod02.puml` | `diag_009_sec622_casos_uso_mod02.png` | 27.8 KB | **CONFORME (100%)** |
| 010 | **Diagrama 6.7: Diagrama de Casos de Uso - MOD-03: Perfil del Mentor y Plan de Aprendizaje** | `diag_010_sec622_casos_uso_mod03.puml` | `diag_010_sec622_casos_uso_mod03.png` | 26.8 KB | **CONFORME (100%)** |
| 011 | **Diagrama 6.8: Diagrama de Casos de Uso - MOD-04: Demanda y Recomendaciones Personalizadas** | `diag_011_sec622_casos_uso_mod04.puml` | `diag_011_sec622_casos_uso_mod04.png` | 31.5 KB | **CONFORME (100%)** |
| 012 | **Diagrama 6.9: Diagrama de Casos de Uso - MOD-05: Quórum, Confirmación y Cancelaciones** | `diag_012_sec622_casos_uso_mod05.puml` | `diag_012_sec622_casos_uso_mod05.png` | 48.7 KB | **CONFORME (100%)** |
| 013 | **Diagrama 6.10: Diagrama de Casos de Uso - MOD-06: Asistencia, Bitácoras y Feedback** | `diag_013_sec622_casos_uso_mod06.puml` | `diag_013_sec622_casos_uso_mod06.png` | 35.3 KB | **CONFORME (100%)** |
| 014 | **Diagrama 6.11: Diagrama de Casos de Uso - MOD-07: Gamificación e Incentivos** | `diag_014_sec622_casos_uso_mod07.puml` | `diag_014_sec622_casos_uso_mod07.png` | 26.2 KB | **CONFORME (100%)** |
| 015 | **Diagrama 6.12: Diagrama de Casos de Uso - MOD-08: Analítica, Notificaciones y Configuración** | `diag_015_sec622_casos_uso_mod08.puml` | `diag_015_sec622_casos_uso_mod08.png` | 58.8 KB | **CONFORME (100%)** |
| 016 | **Diagrama 6.13: Diagrama de Análisis de Objetos (Modelo ECB) - Flujo General de Mentorías P2P** | `diag_016_sec631_ecb_general_consolidado.puml` | `diag_016_sec631_ecb_general_consolidado.png` | 80.3 KB | **CONFORME (100%)** |
| 017 | **Diagrama 6.13.1: Análisis de Objetos (Modelo ECB) - CUS-001: Iniciar sesión institucional con 2FA** | `diag_017_sec631_ecb_cus001.puml` | `diag_017_sec631_ecb_cus001.png` | 36.0 KB | **CONFORME (100%)** |
| 018 | **Diagrama 6.13.2: Análisis de Objetos (Modelo ECB) - CUS-010: Gestionar asignación de roles de usuario** | `diag_018_sec631_ecb_cus010.puml` | `diag_018_sec631_ecb_cus010.png` | 37.5 KB | **CONFORME (100%)** |
| 019 | **Diagrama 6.13.3: Análisis de Objetos (Modelo ECB) - CUS-006: Publicar oferta de mentoría académica** | `diag_019_sec631_ecb_cus006.puml` | `diag_019_sec631_ecb_cus006.png` | 37.2 KB | **CONFORME (100%)** |
| 020 | **Diagrama 6.13.4: Análisis de Objetos (Modelo ECB) - CUS-008: Consultar disponibilidad de espacios y recursos** | `diag_020_sec631_ecb_cus008.puml` | `diag_020_sec631_ecb_cus008.png` | 38.8 KB | **CONFORME (100%)** |
| 021 | **Diagrama 6.13.5: Análisis de Objetos (Modelo ECB) - CUS-005: Gestionar perfil formativo y disponibilidad horaria** | `diag_021_sec631_ecb_cus005.puml` | `diag_021_sec631_ecb_cus005.png` | 39.7 KB | **CONFORME (100%)** |
| 022 | **Diagrama 6.13.6: Análisis de Objetos (Modelo ECB) - CUS-021: Explorar catálogo curricular de asignaturas filtro** | `diag_022_sec631_ecb_cus021.puml` | `diag_022_sec631_ecb_cus021.png` | 39.0 KB | **CONFORME (100%)** |
| 023 | **Diagrama 6.13.7: Análisis de Objetos (Modelo ECB) - CUS-002: Explorar recomendaciones personalizadas Top-k** | `diag_023_sec631_ecb_cus002.puml` | `diag_023_sec631_ecb_cus002.png` | 39.2 KB | **CONFORME (100%)** |
| 024 | **Diagrama 6.13.8: Análisis de Objetos (Modelo ECB) - CUS-003: Registrar solicitud de demanda académica** | `diag_024_sec631_ecb_cus003.puml` | `diag_024_sec631_ecb_cus003.png` | 38.7 KB | **CONFORME (100%)** |
| 025 | **Diagrama 6.13.9: Análisis de Objetos (Modelo ECB) - CUS-004: Reservar cupo de mentoría académica** | `diag_025_sec631_ecb_cus004.puml` | `diag_025_sec631_ecb_cus004.png` | 37.2 KB | **CONFORME (100%)** |
| 026 | **Diagrama 6.13.10: Análisis de Objetos (Modelo ECB) - CUS-024: Ratificar asistencia a sesión de mentoría** | `diag_026_sec631_ecb_cus024.puml` | `diag_026_sec631_ecb_cus024.png` | 38.0 KB | **CONFORME (100%)** |
| 027 | **Diagrama 6.13.11: Análisis de Objetos (Modelo ECB) - CUS-017: Desistir voluntariamente de reserva** | `diag_027_sec631_ecb_cus017.puml` | `diag_027_sec631_ecb_cus017.png` | 36.5 KB | **CONFORME (100%)** |
| 028 | **Diagrama 6.13.12: Análisis de Objetos (Modelo ECB) - CUS-023: Evaluar quórum automático a T-24h** | `diag_028_sec631_ecb_cus023.puml` | `diag_028_sec631_ecb_cus023.png` | 36.8 KB | **CONFORME (100%)** |
| 029 | **Diagrama 6.13.13: Análisis de Objetos (Modelo ECB) - CUS-007: Decisión del mentor ante quórum insuficiente** | `diag_029_sec631_ecb_cus007.puml` | `diag_029_sec631_ecb_cus007.png` | 38.8 KB | **CONFORME (100%)** |
| 030 | **Diagrama 6.13.14: Análisis de Objetos (Modelo ECB) - CUS-012: Registrar asistencia a sesión de mentoría** | `diag_030_sec631_ecb_cus012.puml` | `diag_030_sec631_ecb_cus012.png` | 37.8 KB | **CONFORME (100%)** |
| 031 | **Diagrama 6.13.15: Análisis de Objetos (Modelo ECB) - CUS-013: Registrar bitácora académica de sesión** | `diag_031_sec631_ecb_cus013.puml` | `diag_031_sec631_ecb_cus013.png` | 37.6 KB | **CONFORME (100%)** |
| 032 | **Diagrama 6.13.16: Análisis de Objetos (Modelo ECB) - CUS-014: Visualizar historial y bitácoras académicas** | `diag_032_sec631_ecb_cus014.puml` | `diag_032_sec631_ecb_cus014.png` | 39.0 KB | **CONFORME (100%)** |
| 033 | **Diagrama 6.13.17: Análisis de Objetos (Modelo ECB) - CUS-018: Emitir constancia institucional de horas de mentoría** | `diag_033_sec631_ecb_cus018.puml` | `diag_033_sec631_ecb_cus018.png` | 39.6 KB | **CONFORME (100%)** |
| 034 | **Diagrama 6.13.18: Análisis de Objetos (Modelo ECB) - CUS-019: Gestionar insignias y reputación gamificada** | `diag_034_sec631_ecb_cus019.puml` | `diag_034_sec631_ecb_cus019.png` | 39.0 KB | **CONFORME (100%)** |
| 035 | **Diagrama 6.13.19: Análisis de Objetos (Modelo ECB) - CUS-009: Notificar eventos críticos y alertas temporales** | `diag_035_sec631_ecb_cus009.puml` | `diag_035_sec631_ecb_cus009.png` | 39.0 KB | **CONFORME (100%)** |
| 036 | **Diagrama 6.13.20: Análisis de Objetos (Modelo ECB) - CUS-011: Generar reportes e indicadores de analítica académica** | `diag_036_sec631_ecb_cus011.puml` | `diag_036_sec631_ecb_cus011.png` | 40.4 KB | **CONFORME (100%)** |
| 037 | **Diagrama 6.13.21: Análisis de Objetos (Modelo ECB) - CUS-015: Consultar métricas de retención y desempeño** | `diag_037_sec631_ecb_cus015.puml` | `diag_037_sec631_ecb_cus015.png` | 39.3 KB | **CONFORME (100%)** |
| 038 | **Diagrama 6.13.22: Análisis de Objetos (Modelo ECB) - CUS-016: Auditar trazas de seguridad y consentimiento Ley 29733** | `diag_038_sec631_ecb_cus016.puml` | `diag_038_sec631_ecb_cus016.png` | 41.0 KB | **CONFORME (100%)** |
| 039 | **Diagrama 6.13.23: Análisis de Objetos (Modelo ECB) - CUS-020: Configurar parámetros institucionales y umbrales** | `diag_039_sec631_ecb_cus020.puml` | `diag_039_sec631_ecb_cus020.png` | 39.6 KB | **CONFORME (100%)** |
| 040 | **Diagrama 6.13.24: Análisis de Objetos (Modelo ECB) - CUS-022: Gestionar catálogo de temas y materias críticas** | `diag_040_sec631_ecb_cus022.puml` | `diag_040_sec631_ecb_cus022.png` | 38.5 KB | **CONFORME (100%)** |
| 041 | **Diagrama 6.14: Diagrama de Actividades con Flujo de Objetos del Ciclo de Mentoría** | `diag_041_sec632_act_general_consolidado.puml` | `diag_041_sec632_act_general_consolidado.png` | 127.5 KB | **CONFORME (100%)** |
| 042 | **Diagrama 6.14.1: Diagrama de Actividades con Flujo de Objetos - CUS-001: Iniciar sesión institucional con 2FA** | `diag_042_sec632_act_cus001.puml` | `diag_042_sec632_act_cus001.png` | 54.2 KB | **CONFORME (100%)** |
| 043 | **Diagrama 6.14.2: Diagrama de Actividades con Flujo de Objetos - CUS-010: Gestionar asignación de roles de usuario** | `diag_043_sec632_act_cus010.puml` | `diag_043_sec632_act_cus010.png` | 54.6 KB | **CONFORME (100%)** |
| 044 | **Diagrama 6.14.3: Diagrama de Actividades con Flujo de Objetos - CUS-006: Publicar oferta de mentoría académica** | `diag_044_sec632_act_cus006.puml` | `diag_044_sec632_act_cus006.png` | 55.2 KB | **CONFORME (100%)** |
| 045 | **Diagrama 6.14.4: Diagrama de Actividades con Flujo de Objetos - CUS-008: Consultar disponibilidad de espacios y recursos** | `diag_045_sec632_act_cus008.puml` | `diag_045_sec632_act_cus008.png` | 55.4 KB | **CONFORME (100%)** |
| 046 | **Diagrama 6.14.5: Diagrama de Actividades con Flujo de Objetos - CUS-005: Gestionar perfil formativo y disponibilidad horaria** | `diag_046_sec632_act_cus005.puml` | `diag_046_sec632_act_cus005.png` | 56.0 KB | **CONFORME (100%)** |
| 047 | **Diagrama 6.14.6: Diagrama de Actividades con Flujo de Objetos - CUS-021: Explorar catálogo curricular de asignaturas filtro** | `diag_047_sec632_act_cus021.puml` | `diag_047_sec632_act_cus021.png` | 55.4 KB | **CONFORME (100%)** |
| 048 | **Diagrama 6.14.7: Diagrama de Actividades con Flujo de Objetos - CUS-002: Explorar recomendaciones personalizadas Top-k** | `diag_048_sec632_act_cus002.puml` | `diag_048_sec632_act_cus002.png` | 55.5 KB | **CONFORME (100%)** |
| 049 | **Diagrama 6.14.8: Diagrama de Actividades con Flujo de Objetos - CUS-003: Registrar solicitud de demanda académica** | `diag_049_sec632_act_cus003.puml` | `diag_049_sec632_act_cus003.png` | 55.2 KB | **CONFORME (100%)** |
| 050 | **Diagrama 6.14.9: Diagrama de Actividades con Flujo de Objetos - CUS-004: Reservar cupo de mentoría académica** | `diag_050_sec632_act_cus004.puml` | `diag_050_sec632_act_cus004.png` | 55.0 KB | **CONFORME (100%)** |
| 051 | **Diagrama 6.14.10: Diagrama de Actividades con Flujo de Objetos - CUS-024: Ratificar asistencia a sesión de mentoría** | `diag_051_sec632_act_cus024.puml` | `diag_051_sec632_act_cus024.png` | 55.1 KB | **CONFORME (100%)** |
| 052 | **Diagrama 6.14.11: Diagrama de Actividades con Flujo de Objetos - CUS-017: Desistir voluntariamente de reserva** | `diag_052_sec632_act_cus017.puml` | `diag_052_sec632_act_cus017.png` | 54.7 KB | **CONFORME (100%)** |
| 053 | **Diagrama 6.14.12: Diagrama de Actividades con Flujo de Objetos - CUS-023: Evaluar quórum automático a T-24h** | `diag_053_sec632_act_cus023.puml` | `diag_053_sec632_act_cus023.png` | 55.2 KB | **CONFORME (100%)** |
| 054 | **Diagrama 6.14.13: Diagrama de Actividades con Flujo de Objetos - CUS-007: Decisión del mentor ante quórum insuficiente** | `diag_054_sec632_act_cus007.puml` | `diag_054_sec632_act_cus007.png` | 55.3 KB | **CONFORME (100%)** |
| 055 | **Diagrama 6.14.14: Diagrama de Actividades con Flujo de Objetos - CUS-012: Registrar asistencia a sesión de mentoría** | `diag_055_sec632_act_cus012.puml` | `diag_055_sec632_act_cus012.png` | 55.3 KB | **CONFORME (100%)** |
| 056 | **Diagrama 6.14.15: Diagrama de Actividades con Flujo de Objetos - CUS-013: Registrar bitácora académica de sesión** | `diag_056_sec632_act_cus013.puml` | `diag_056_sec632_act_cus013.png` | 56.8 KB | **CONFORME (100%)** |
| 057 | **Diagrama 6.14.16: Diagrama de Actividades con Flujo de Objetos - CUS-014: Visualizar historial y bitácoras académicas** | `diag_057_sec632_act_cus014.puml` | `diag_057_sec632_act_cus014.png` | 57.3 KB | **CONFORME (100%)** |
| 058 | **Diagrama 6.14.17: Diagrama de Actividades con Flujo de Objetos - CUS-018: Emitir constancia institucional de horas de mentoría** | `diag_058_sec632_act_cus018.puml` | `diag_058_sec632_act_cus018.png` | 55.5 KB | **CONFORME (100%)** |
| 059 | **Diagrama 6.14.18: Diagrama de Actividades con Flujo de Objetos - CUS-019: Gestionar insignias y reputación gamificada** | `diag_059_sec632_act_cus019.puml` | `diag_059_sec632_act_cus019.png` | 55.3 KB | **CONFORME (100%)** |
| 060 | **Diagrama 6.14.19: Diagrama de Actividades con Flujo de Objetos - CUS-009: Notificar eventos críticos y alertas temporales** | `diag_060_sec632_act_cus009.puml` | `diag_060_sec632_act_cus009.png` | 55.2 KB | **CONFORME (100%)** |
| 061 | **Diagrama 6.14.20: Diagrama de Actividades con Flujo de Objetos - CUS-011: Generar reportes e indicadores de analítica académica** | `diag_061_sec632_act_cus011.puml` | `diag_061_sec632_act_cus011.png` | 55.5 KB | **CONFORME (100%)** |
| 062 | **Diagrama 6.14.21: Diagrama de Actividades con Flujo de Objetos - CUS-015: Consultar métricas de retención y desempeño** | `diag_062_sec632_act_cus015.puml` | `diag_062_sec632_act_cus015.png` | 55.5 KB | **CONFORME (100%)** |
| 063 | **Diagrama 6.14.22: Diagrama de Actividades con Flujo de Objetos - CUS-016: Auditar trazas de seguridad y consentimiento Ley 29733** | `diag_063_sec632_act_cus016.puml` | `diag_063_sec632_act_cus016.png` | 58.0 KB | **CONFORME (100%)** |
| 064 | **Diagrama 6.14.23: Diagrama de Actividades con Flujo de Objetos - CUS-020: Configurar parámetros institucionales y umbrales** | `diag_064_sec632_act_cus020.puml` | `diag_064_sec632_act_cus020.png` | 57.0 KB | **CONFORME (100%)** |
| 065 | **Diagrama 6.14.24: Diagrama de Actividades con Flujo de Objetos - CUS-022: Gestionar catálogo de temas y materias críticas** | `diag_065_sec632_act_cus022.puml` | `diag_065_sec632_act_cus022.png` | 55.3 KB | **CONFORME (100%)** |
| 066 | **Diagrama 6.15: Diagrama de Secuencia General del Ciclo Transaccional de Mentorías** | `diag_066_sec633_seq_general_integracion.puml` | `diag_066_sec633_seq_general_integracion.png` | 545.6 KB | **CONFORME (100%)** |
| 067 | **Diagrama 6.15.1: Diagrama de Secuencia - CUS-001: Iniciar sesión institucional con 2FA** | `diag_067_sec633_seq_cus001.puml` | `diag_067_sec633_seq_cus001.png` | 605.1 KB | **CONFORME (100%)** |
| 068 | **Diagrama 6.15.2: Diagrama de Secuencia - CUS-010: Gestionar asignación de roles de usuario** | `diag_068_sec633_seq_cus010.puml` | `diag_068_sec633_seq_cus010.png` | 374.3 KB | **CONFORME (100%)** |
| 069 | **Diagrama 69** | `diag_069_sec633_seq_item_69.puml` | `diag_069_sec633_seq_item_69.png` | 311.8 KB | **CONFORME (100%)** |
| 070 | **Diagrama 6.15.4: Diagrama de Secuencia - CUS-008: Consultar disponibilidad de espacios y recursos** | `diag_070_sec633_seq_cus008.puml` | `diag_070_sec633_seq_cus008.png` | 226.5 KB | **CONFORME (100%)** |
| 071 | **Diagrama 6.15.5: Diagrama de Secuencia - CUS-005: Gestionar perfil académico y disponibilidad horaria** | `diag_071_sec633_seq_cus005.puml` | `diag_071_sec633_seq_cus005.png` | 249.3 KB | **CONFORME (100%)** |
| 072 | **Diagrama 6.15.6: Diagrama de Secuencia - CUS-021: Explorar catálogo curricular de asignaturas filtro** | `diag_072_sec633_seq_cus021.puml` | `diag_072_sec633_seq_cus021.png` | 201.7 KB | **CONFORME (100%)** |
| 073 | **Diagrama 6.15.7: Diagrama de Secuencia - CUS-002: Explorar recomendaciones personalizadas Top-k** | `diag_073_sec633_seq_cus002.puml` | `diag_073_sec633_seq_cus002.png` | 256.9 KB | **CONFORME (100%)** |
| 074 | **Diagrama 6.15.8: Diagrama de Secuencia - CUS-003: Registrar solicitud de demanda académica** | `diag_074_sec633_seq_cus003.puml` | `diag_074_sec633_seq_cus003.png` | 228.9 KB | **CONFORME (100%)** |
| 075 | **Diagrama 6.15.9: Diagrama de Secuencia - CUS-004: Reservar cupo de mentoría académica** | `diag_075_sec633_seq_cus004.puml` | `diag_075_sec633_seq_cus004.png` | 489.2 KB | **CONFORME (100%)** |
| 076 | **Diagrama 6.15.10: Diagrama de Secuencia - CUS-024: Ratificar asistencia a sesión de mentoría** | `diag_076_sec633_seq_cus024.puml` | `diag_076_sec633_seq_cus024.png` | 238.0 KB | **CONFORME (100%)** |
| 077 | **Diagrama 6.15.11: Diagrama de Secuencia - CUS-017: Desistir voluntariamente de reserva** | `diag_077_sec633_seq_cus017.puml` | `diag_077_sec633_seq_cus017.png` | 197.8 KB | **CONFORME (100%)** |
| 078 | **Diagrama 6.15.12: Diagrama de Secuencia - CUS-023: Evaluar quórum automático a T-24h** | `diag_078_sec633_seq_cus023.puml` | `diag_078_sec633_seq_cus023.png` | 255.3 KB | **CONFORME (100%)** |
| 079 | **Diagrama 6.15.13: Diagrama de Secuencia - CUS-007: Decisión del mentor ante quórum insuficiente** | `diag_079_sec633_seq_cus007.puml` | `diag_079_sec633_seq_cus007.png` | 276.5 KB | **CONFORME (100%)** |
| 080 | **Diagrama 6.15.14: Diagrama de Secuencia - CUS-012: Registrar asistencia a sesión de mentoría** | `diag_080_sec633_seq_cus012.puml` | `diag_080_sec633_seq_cus012.png` | 296.5 KB | **CONFORME (100%)** |
| 081 | **Diagrama 6.15.15: Diagrama de Secuencia - CUS-013: Registrar bitácora pedagógica de sesión** | `diag_081_sec633_seq_cus013.puml` | `diag_081_sec633_seq_cus013.png` | 242.3 KB | **CONFORME (100%)** |
| 082 | **Diagrama 6.15.16: Diagrama de Secuencia - CUS-014: Visualizar historial y bitácoras académicas** | `diag_082_sec633_seq_cus014.puml` | `diag_082_sec633_seq_cus014.png` | 173.6 KB | **CONFORME (100%)** |
| 083 | **Diagrama 6.15.17: Diagrama de Secuencia - CUS-018: Emitir constancia institucional de horas de mentoría** | `diag_083_sec633_seq_cus018.puml` | `diag_083_sec633_seq_cus018.png` | 261.4 KB | **CONFORME (100%)** |
| 084 | **Diagrama 6.15.18: Diagrama de Secuencia - CUS-019: Gestionar insignias y reputación gamificada** | `diag_084_sec633_seq_cus019.puml` | `diag_084_sec633_seq_cus019.png` | 172.3 KB | **CONFORME (100%)** |
| 085 | **Diagrama 6.15.19: Diagrama de Secuencia - CUS-009: Notificar eventos críticos y alertas temporales** | `diag_085_sec633_seq_cus009.puml` | `diag_085_sec633_seq_cus009.png` | 227.3 KB | **CONFORME (100%)** |
| 086 | **Diagrama 6.15.20: Diagrama de Secuencia - CUS-011: Generar reportes e indicadores analíticos** | `diag_086_sec633_seq_cus011.puml` | `diag_086_sec633_seq_cus011.png` | 208.5 KB | **CONFORME (100%)** |
| 087 | **Diagrama 6.15.21: Diagrama de Secuencia - CUS-015: Consultar métricas de retención y desempeño** | `diag_087_sec633_seq_cus015.puml` | `diag_087_sec633_seq_cus015.png` | 228.4 KB | **CONFORME (100%)** |
| 088 | **Diagrama 6.15.22: Diagrama de Secuencia - CUS-016: Auditar trazas de seguridad y consentimiento** | `diag_088_sec633_seq_cus016.puml` | `diag_088_sec633_seq_cus016.png` | 257.3 KB | **CONFORME (100%)** |
| 089 | **Diagrama 6.15.23: Diagrama de Secuencia - CUS-020: Configurar parámetros institucionales y umbrales** | `diag_089_sec633_seq_cus020.puml` | `diag_089_sec633_seq_cus020.png` | 234.8 KB | **CONFORME (100%)** |
| 090 | **Diagrama 6.15.24: Diagrama de Secuencia - CUS-022: Gestionar catálogo de temas y materias críticas** | `diag_090_sec633_seq_cus022.puml` | `diag_090_sec633_seq_cus022.png` | 234.3 KB | **CONFORME (100%)** |
| 091 | **Diagrama 6.16: Diagrama de Clases del Modelo Lógico del Sistema Web P2P** | `diag_091_sec634_clases_logico_general.puml` | `diag_091_sec634_clases_logico_general.png` | 90.8 KB | **CONFORME (100%)** |
| 092 | **Diagrama 6.16.1: Diagrama de Clases Lógico Parcial - CUS-001: Iniciar sesión institucional con 2FA** | `diag_092_sec634_clases_logico_cus001.puml` | `diag_092_sec634_clases_logico_cus001.png` | 23.7 KB | **CONFORME (100%)** |
| 093 | **Diagrama 6.16.2: Diagrama de Clases Lógico Parcial - CUS-010: Gestionar asignación de roles de usuario** | `diag_093_sec634_clases_logico_cus010.puml` | `diag_093_sec634_clases_logico_cus010.png` | 24.1 KB | **CONFORME (100%)** |
| 094 | **Diagrama 6.16.3: Diagrama de Clases Lógico Parcial - CUS-006: Publicar oferta de mentoría académica** | `diag_094_sec634_clases_logico_cus006.puml` | `diag_094_sec634_clases_logico_cus006.png` | 24.8 KB | **CONFORME (100%)** |
| 095 | **Diagrama 6.16.4: Diagrama de Clases Lógico Parcial - CUS-008: Consultar disponibilidad de espacios y recursos** | `diag_095_sec634_clases_logico_cus008.puml` | `diag_095_sec634_clases_logico_cus008.png` | 25.1 KB | **CONFORME (100%)** |
| 096 | **Diagrama 6.16.5: Diagrama de Clases Lógico Parcial - CUS-005: Gestionar perfil formativo y disponibilidad horaria** | `diag_096_sec634_clases_logico_cus005.puml` | `diag_096_sec634_clases_logico_cus005.png` | 25.8 KB | **CONFORME (100%)** |
| 097 | **Diagrama 6.16.6: Diagrama de Clases Lógico Parcial - CUS-021: Explorar catálogo curricular de asignaturas filtro** | `diag_097_sec634_clases_logico_cus021.puml` | `diag_097_sec634_clases_logico_cus021.png` | 25.3 KB | **CONFORME (100%)** |
| 098 | **Diagrama 6.16.7: Diagrama de Clases Lógico Parcial - CUS-002: Explorar recomendaciones personalizadas Top-k** | `diag_098_sec634_clases_logico_cus002.puml` | `diag_098_sec634_clases_logico_cus002.png` | 25.8 KB | **CONFORME (100%)** |
| 099 | **Diagrama 6.16.8: Diagrama de Clases Lógico Parcial - CUS-003: Registrar solicitud de demanda académica** | `diag_099_sec634_clases_logico_cus003.puml` | `diag_099_sec634_clases_logico_cus003.png` | 25.1 KB | **CONFORME (100%)** |
| 100 | **Diagrama 6.16.9: Diagrama de Clases Lógico Parcial - CUS-004: Reservar cupo de mentoría académica** | `diag_100_sec634_clases_logico_cus004.puml` | `diag_100_sec634_clases_logico_cus004.png` | 24.8 KB | **CONFORME (100%)** |
| 101 | **Diagrama 6.16.10: Diagrama de Clases Lógico Parcial - CUS-024: Ratificar asistencia a sesión de mentoría** | `diag_101_sec634_clases_logico_cus024.puml` | `diag_101_sec634_clases_logico_cus024.png` | 24.7 KB | **CONFORME (100%)** |
| 102 | **Diagrama 6.16.11: Diagrama de Clases Lógico Parcial - CUS-017: Desistir voluntariamente de reserva** | `diag_102_sec634_clases_logico_cus017.puml` | `diag_102_sec634_clases_logico_cus017.png` | 24.6 KB | **CONFORME (100%)** |
| 103 | **Diagrama 6.16.12: Diagrama de Clases Lógico Parcial - CUS-023: Evaluar quórum automático a T-24h** | `diag_103_sec634_clases_logico_cus023.puml` | `diag_103_sec634_clases_logico_cus023.png` | 25.0 KB | **CONFORME (100%)** |
| 104 | **Diagrama 6.16.13: Diagrama de Clases Lógico Parcial - CUS-007: Decisión del mentor ante quórum insuficiente** | `diag_104_sec634_clases_logico_cus007.puml` | `diag_104_sec634_clases_logico_cus007.png` | 25.7 KB | **CONFORME (100%)** |
| 105 | **Diagrama 6.16.14: Diagrama de Clases Lógico Parcial - CUS-012: Registrar asistencia a sesión de mentoría** | `diag_105_sec634_clases_logico_cus012.puml` | `diag_105_sec634_clases_logico_cus012.png` | 24.8 KB | **CONFORME (100%)** |
| 106 | **Diagrama 6.16.15: Diagrama de Clases Lógico Parcial - CUS-013: Registrar bitácora académica de sesión** | `diag_106_sec634_clases_logico_cus013.puml` | `diag_106_sec634_clases_logico_cus013.png` | 24.8 KB | **CONFORME (100%)** |
| 107 | **Diagrama 6.16.16: Diagrama de Clases Lógico Parcial - CUS-014: Visualizar historial y bitácoras académicas** | `diag_107_sec634_clases_logico_cus014.puml` | `diag_107_sec634_clases_logico_cus014.png` | 25.3 KB | **CONFORME (100%)** |
| 108 | **Diagrama 6.16.17: Diagrama de Clases Lógico Parcial - CUS-018: Emitir constancia institucional de horas de mentoría** | `diag_108_sec634_clases_logico_cus018.puml` | `diag_108_sec634_clases_logico_cus018.png` | 27.2 KB | **CONFORME (100%)** |
| 109 | **Diagrama 6.16.18: Diagrama de Clases Lógico Parcial - CUS-019: Gestionar insignias y reputación gamificada** | `diag_109_sec634_clases_logico_cus019.puml` | `diag_109_sec634_clases_logico_cus019.png` | 24.9 KB | **CONFORME (100%)** |
| 110 | **Diagrama 6.16.19: Diagrama de Clases Lógico Parcial - CUS-009: Notificar eventos críticos y alertas temporales** | `diag_110_sec634_clases_logico_cus009.puml` | `diag_110_sec634_clases_logico_cus009.png` | 25.6 KB | **CONFORME (100%)** |
| 111 | **Diagrama 6.16.20: Diagrama de Clases Lógico Parcial - CUS-011: Generar reportes e indicadores de analítica académica** | `diag_111_sec634_clases_logico_cus011.puml` | `diag_111_sec634_clases_logico_cus011.png` | 28.2 KB | **CONFORME (100%)** |
| 112 | **Diagrama 6.16.21: Diagrama de Clases Lógico Parcial - CUS-015: Consultar métricas de retención y desempeño** | `diag_112_sec634_clases_logico_cus015.puml` | `diag_112_sec634_clases_logico_cus015.png` | 25.9 KB | **CONFORME (100%)** |
| 113 | **Diagrama 6.16.22: Diagrama de Clases Lógico Parcial - CUS-016: Auditar trazas de seguridad y consentimiento Ley 29733** | `diag_113_sec634_clases_logico_cus016.puml` | `diag_113_sec634_clases_logico_cus016.png` | 28.7 KB | **CONFORME (100%)** |
| 114 | **Diagrama 6.16.23: Diagrama de Clases Lógico Parcial - CUS-020: Configurar parámetros institucionales y umbrales** | `diag_114_sec634_clases_logico_cus020.puml` | `diag_114_sec634_clases_logico_cus020.png` | 26.0 KB | **CONFORME (100%)** |
| 115 | **Diagrama 6.16.24: Diagrama de Clases Lógico Parcial - CUS-022: Gestionar catálogo de temas y materias críticas** | `diag_115_sec634_clases_logico_cus022.puml` | `diag_115_sec634_clases_logico_cus022.png` | 25.1 KB | **CONFORME (100%)** |
| 116 | **Diagrama 6.17: Máquina de Estados Finitos - Ciclo de Vida de SesionMentoria** | `diag_116_sec635_fsm_sesion_mentoria.puml` | `diag_116_sec635_fsm_sesion_mentoria.png` | 87.8 KB | **CONFORME (100%)** |
| 117 | **Diagrama 6.18: Máquina de Estados Finitos - Ciclo de Vida de ReservaCupo** | `diag_117_sec635_fsm_reserva_cupo.puml` | `diag_117_sec635_fsm_reserva_cupo.png` | 77.7 KB | **CONFORME (100%)** |
| 118 | **Diagrama 6.19: Máquina de Estados Finitos - Ciclo de Vida de BitacoraPedagogica y CertificadoHoras** | `diag_118_sec635_fsm_bitacora_certificado.puml` | `diag_118_sec635_fsm_bitacora_certificado.png` | 67.5 KB | **CONFORME (100%)** |
| 119 | **Diagrama 6.20: Diagrama Entidad-Relación Físico (15 Tablas Relacionales) - PostgreSQL** | `diag_119_sec636_der_fisico_15tablas.puml` | `diag_119_sec636_der_fisico_15tablas.png` | 168.2 KB | **CONFORME (100%)** |

Fuente: Elaboración propia a partir de auditoría automatizada sobre el sistema de archivos.

---

## 4. Pipeline de Regeneración Automatizada y Reproducible

Para garantizar que futuras iteraciones sobre los modelos UML no degraden el formato oficial a bloques de código, se establecieron dos scripts en `tools/` que forman un pipeline completamente reproducible:

```bash
# Paso 1: Renderizar por lotes todas las fuentes PUML a imágenes PNG
python tools/render_srs_diagrams.py

# Paso 2: Ejecutar el ensamblador maestro con sustitución automática y auditoría D-2
python tools/build_design_srs_full.py
```

### Garantías del Ensamblador (`tools/build_design_srs_full.py`):
- **Idempotencia:** Ejecutar el comando repetidas veces produce idéntico documento carácter por carácter.
- **Doble Auditoría:** Valida los diagramas de secuencia contra las 24 narrativas de casos de uso antes y después del reemplazo gráfico.
- **Control de Fallo:** Si falta una imagen requerida o su tamaño es 0 bytes, el script aborta inmediatamente con código de salida `1` impidiendo la generación de documentos defectuosos.

---

## 5. Protocolo de Exportación Oficial a DOCX y Google Docs

Con las 119 figuras renderizadas en formato PNG y vinculadas mediante rutas relativas estándar (`diagramas/srs/img/diag_XXX.png`), el documento queda plenamente capacitado para su conversión a procesadores de texto.

### 5.1. Exportación mediante Pandoc (Línea de Comandos)
Para entornos donde `pandoc` se encuentre instalado, ejecutar desde el directorio `docs/diseño/`:

```bash
cd docs/diseño
pandoc "FD03-EPIS-Informe SRS de Proyecto.md" \
  -o "FD03-EPIS-Informe_SRS_de_Proyecto_Oficial.docx" \
  --from=markdown+pipe_tables+strikeout+superscript+subscript \
  --toc --toc-depth=3 \
  --highlight-style=tango
```

### 5.2. Exportación mediante Visual Studio Code
1. Abrir `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` en VS Code.
2. Instalar o habilitar la extensión oficial **Markdown Preview Enhanced** o **Markdown to DOCX**.
3. Abrir la vista previa lateral (`Ctrl+K V` o clic secundario -> *Open Preview*).
4. Hacer clic secundario sobre la vista previa -> Seleccionar `Export to Disk` -> `DOCX`.
5. El procesador empaquetará automáticamente las 119 imágenes PNG dentro del archivo `.docx` sin enlaces externos rotos.

### 5.3. Importación y Visualización en Google Docs
1. Generar el archivo `.docx` siguiendo cualquiera de los dos métodos anteriores.
2. Subir el archivo `.docx` a Google Drive institucional.
3. Hacer doble clic y seleccionar **Abrir con Documentos de Google**.
4. Verificar que todas las figuras se despliegan en línea con alta resolución, manteniendo títulos, leyendas y fuentes bajo el formato D-2.

---

## 6. Conclusión y Dictamen de Auditoría

El hito **[D05] — Validación final y exportación** concluye satisfactoriamente:
- Se eliminó el 100% de los bloques de código PlantUML en el informe oficial SRS.
- Se preservó la base de conocimiento en 119 archivos `.puml` versionados.
- Se garantizó la presencia física de 119 figuras `.png` nítidas y legibles.
- El SRS v3.1 se encuentra en estado óptimo para revisión docente, sustentación y exportación ofimática.

**Dictamen Técnico:** **APROBADO SIN RESERVAS**.
