# Homologación y Reconciliación Documental Oficial

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT  
**Fase:** Fase 05-B — Cierre Técnico, Preparación de Demo y Consistencia Documental  
**Fecha de Emisión:** 07 de Noviembre de 2026  
**Rama:** `feat/formalizacion-ux-roles`  
**Estado:** Documento Normativo de Reconciliación No Destructiva  

---

## 1. Reconciliación Canónica: CUS08 vs CUS12 / CUS13

### 1.1 Antecedentes de la Divergencia
Durante la auditoría integral de la Fase 04-B se constató una divergencia en la nomenclatura de casos de uso entre los documentos maestros y los entregables del Sprint 06:

1. **SRS Maestro FD03 (Cuadro 5.3 y Cuadro 5.5 - Matriz de Trazabilidad Bidireccional):**
   - **`CUS08`**: *"Registrar bitácora y control de asistencia efectiva"* (asociado formalmente a **RF17**).
   - **`CUS12`**: *"Priorización y emparejamiento institucional"* (asociado a RF11 / Criterios de vulnerabilidad).
   - **`CUS13`**: *"Generación y acreditación de constancias/certificados de mentoría"*.

2. **Entregables y Narrativas de Sprint 06 (`docs/sprints/sprint-06.md` y `docs/sprints/sprint-06/README.md`):**
   - El equipo del Sprint 06 etiquetó el pase de lista digital como **`CUS12`** (*Control de Asistencia Digital TOTP*) y la bitácora pedagógica como **`CUS13`** (*Registro de Bitácora Pedagógica con Sello Criptográfico*).
   - En la sección §6.2.3 del SRS (narrativas detalladas), existía un borrador preliminar que desglosó `CUS-008` (Disponibilidad de espacios), `CUS-012` (Asistencia) y `CUS-013` (Bitácora).

### 1.2 Tabla Oficial de Equivalencia y Resolución No Destructiva
Para salvaguardar la trazabilidad histórica de los commits de los Sprints 01 al 06 sin alterar destructivamente los nombres de archivos ni enlaces cruzados, se formaliza la siguiente equivalencia normativa:

| Requerimiento Funcional | Código SRS Maestro (FD03 Cuadro 5.5) | Alias en Sprint 06 / Tareas | Módulo de Código Implementado | Descripción Funcional Homologada |
| :--- | :--- | :--- | :--- | :--- |
| **RF17** | **CUS08** | **CUS12** (T-34 / T-36) | `app/api/v1/endpoints/attendance.py`<br>`src/services/attendanceService.ts` | Control de asistencia efectiva mediante token dinámico TOTP y código QR. |
| **RF17** | **CUS08** | **CUS13** (T-35 / T-36) | `app/api/v1/endpoints/bitacora.py`<br>`src/services/bitacoraService.ts` | Registro y sellado criptográfico SHA-256 de bitácora pedagógica (< 48h). |
| **RF11** | **CUS12** | *Alcance Sprint 07* | `app/services/recommendation_service.py` | Algoritmo de priorización institucional y vulnerabilidad académica. |
| **RF18** | **CUS13** | *Alcance Sprint 08* | *Pendiente implementación* | Emisión institucional de certificados y acreditación de horas extracurriculares. |

> **Criterio de resolución:** En el código fuente y contratos REST se conservan las referencias combinadas (`CUS08 / CUS12 / CUS13 / RF17`) como alias plenamente válidos, preservando la compatibilidad retroactiva.

---

## 2. Justificación Técnica del Entorno de Ejecución: Python 3.13.5 vs SAD §2.5 (Python 3.11)

### 2.1 Contexto
El Documento de Arquitectura de Software (**SAD FD04, §2.5**) consignó preliminarmente Python 3.11 como versión del runtime del backend. Sin embargo, el entorno local de desarrollo (`.venv`) y los flujos de integración continua en GitHub Actions (`.github/workflows/ci.yml`) ejecutan **Python 3.13.5**.

### 2.2 Fundamentación Técnica y Trazabilidad de Aprobación
Esta divergencia no constituye un defecto de configuración, sino una **desviación técnica deliberada, justificada y formalmente aprobada** desde el Sprint 01:

1. **Registro en Plan Maestro (`docs/sprints/PLAN_SPRINTS_Y_TAREAS.md`, commits `d6bc275` y `8f8a75c`):**
   - Se documentó textualmente:
     > *"Python 3.13 (desviación técnica respecto al plan preliminar de Python 3.11; versión comprobada en el entorno virtual local `.venv`: Python 3.13.5; en CI: 3.13), FastAPI, Uvicorn y pydantic-settings; entorno `.venv` y dependencias reproducibles con versiones fijadas exactamente mediante `==`... Motivo de la desviación: compatibilidad de librerías modernas en el entorno de desarrollo y soporte oficial en GitHub Actions."*
2. **Compatibilidad Verificada:**
   - Todas las dependencias (FastAPI 0.115+, SQLAlchemy 2.0+, Pydantic v2, Pytest 9.1+, Ruff) operan de manera óptima bajo Python 3.13.5.
   - Las 244 pruebas automatizadas de backend aprueban al 100% con 85.22% de cobertura de código.

---

## 3. Matriz de Artefactos Funcionales: 8 HUs vs 16 Especificaciones vs 37 PBIs

### 3.1 Desglose de Niveles de Abstracción
Para auditorías de calidad (SQA) y seguimiento de proyecto, se formaliza la jerarquía de requerimientos del sistema:

1. **Nivel Estratégico (8 Historias de Usuario Originales - HU01 a HU08):**
   - Definidas en la etapa de concepción y requerimientos iniciales del SRS FD03 como las capacidades esenciales del usuario institucional (Estudiante Mentoreado, Mentor, Coordinador EPIS).
2. **Nivel Táctico / Especificación Formal (16 Requerimientos Funcionales - RF01 a RF16/RF17):**
   - Desglose formal del SRS FD03 (Cuadro 5.3) en reglas operativas verificables, tales como autenticación OTP institucional (RF01/RF02), gestión de mérito académico (RF03/RF04), publicación de ofertas con RN-04 (RF08), reservas y control de aforo (RF12/RF13), evaluación de quórum al 50% (RF15), contingencia del mentor (RF16), y bitácora con asistencia efectiva (RF17).
3. **Nivel Operativo / Backlog de Producto (37 PBIs / Tareas Técnicas):**
   - Tareas atómicas de ingeniería (T-01 a T-37) planificadas y desarrolladas incrementalmente en los Sprints 01 al 06 (documentadas en `PLAN_SPRINTS_Y_TAREAS.md`), cubriendo backend, frontend, pruebas automatizadas, bases de datos y seguridad.

### 3.2 Tabla de Correspondencia Integral

| Nivel de Abstracción | Cantidad | Alcance en el Repositorio | Estado al Cierre del Sprint 06 |
| :--- | :--- | :--- | :--- |
| **Historias de Usuario (HUs)** | 8 | HU01 a HU08 | 6 HUs 100% operativas (HU01 a HU06); HU07 y HU08 planificadas para Sprints 07 y 08. |
| **Requerimientos Funcionales (RFs)** | 16 | RF01 a RF17 | 14 RFs implementados y validados con pruebas automatizadas; RF11 y RF18 corresponden a Sprints 07 y 08. |
| **Product Backlog Items (PBIs / Tareas)** | 37 | T-01 a T-37 | 37 tareas completadas y verificadas con 555 pruebas acumuladas (311 frontend + 244 backend). |

---

## 4. Conclusión de la Homologación
Queda formalmente establecido que las diferencias detectadas corresponden a la evolución natural de un desarrollo incremental ágil, no afectan la integridad arquitectural ni funcional de la plataforma, y quedan plenamente reconciliadas sin impacto en los artefactos de software.
