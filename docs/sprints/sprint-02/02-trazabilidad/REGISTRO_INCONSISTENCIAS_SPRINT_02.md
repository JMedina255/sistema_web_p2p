# Registro Oficial de Inconsistencias, Desviaciones Técnicas y Acciones de Alineación — Sprint 02

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam  
**Integrantes:** Joan Cristian Medina Quispe (2022074255) y Renzo Antonio Antayhua Mamani (2022073504)  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Código de Registro:** `REG-INC-S02-V1.0`  
**Fecha de Emisión:** 26/10/2026  
**Línea Base Documental Auditada:**
- SRS FD03 v2.0 / v2.2 (`docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md`)
- SAD FD04 v2.1 (`docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md`)
- Plan de Sprints v1.2 (`docs/sprints/PLAN_SPRINTS_Y_TAREAS.md`)
- Catálogo de Pruebas (`docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`)
- Código fuente en `aplicacion/` y guion borrador `docs/diseño/GUION_EXPOSICION_SPRINT_02.md`

---

## 1. Principio Metodológico de Precedencia Documental

En concordancia con el principio obligatorio de auditoría («*ningún avance debe presentarse sin respaldo documental y evidencia verificable*»), ante cualquier contradicción entre artefactos se aplica la siguiente jerarquía de fuentes:
$$\text{Requisitos Aprobados (SRS)} \succ \text{Decisiones Arquitectónicas Vigentes (SAD)} \succ \text{Plan Maestro de Sprints} \succ \text{Código Fuente Implementado y Pruebas} \succ \text{Guiones y Materiales Derivados}$$

Todo material de exposición (diapositivas, guiones) es considerado **evidencia derivada** y nunca una nueva fuente de verdad.

---

## 2. Matriz Consolidada de Inconsistencias Detectadas en el Sprint 02

| ID | Dimensión / Sección Auditada | Descripción de la Inconsistencia Detectada | Fuente que Manda | Corrección Propuesta y Aplicada | Justificación Técnica y Metodológica | Archivos Afectados | Estado |
| :---: | :--- | :--- | :---: | :--- | :--- | :--- | :---: |
| **INC-S02-01** | **Pila Tecnológica de Frontend (Vue vs. React)** | El borrador del guion de exposición (`GUION_EXPOSICION_SPRINT_02.md`) hacía referencia sistemática a archivos `.vue` inexistentes (`ConsentModal.vue`, `RoleSelector.vue`, `CurriculumView.vue`, `ProfileScheduleView.vue`). | Código fuente en `aplicacion/frontend/` y SAD FD04 §2.4 | Reemplazar todas las referencias por los componentes reales React 19 + TypeScript: `ConsentModalView.tsx`, `CurriculumCatalogView.tsx`, `ProfileAvailabilityView.tsx`, `consentService.ts`, `profileService.ts`. | El repositorio nunca ha utilizado Vue.js. La arquitectura tecnológica prescriptiva aprobada en SAD FD04 v2.1 y la implementación real en `aplicacion/frontend/` corresponden a React 19, TypeScript 5.6 y Vite con TailwindCSS. | `GUION_EXPOSICION_SPRINT_02.md`, informes preliminares. | **Corregido** ✅ |
| **INC-S02-02** | **Rutas de Endpoints Backend (`app/routers/` vs. API v1)** | El guion citaba rutas de backend en desuso bajo `aplicacion/backend/app/routers/` (`consent.py`, `roles.py`, `curriculum.py`, `profiles.py`). | Estructura real del backend en `aplicacion/backend/app/api/v1/endpoints/` | Actualizar las rutas al esquema modular canónico: `aplicacion/backend/app/api/v1/endpoints/consent.py`, `roles.py`, `curriculum.py`, `profiles.py`, y sus servicios bajo `app/services/`. | La estructura modular del proyecto adoptó el versionamiento explícito `/api/v1/` para permitir evolución de contratos según RNF09 y buenas prácticas REST con FastAPI. | `GUION_EXPOSICION_SPRINT_02.md`, enlaces Markdown. | **Corregido** ✅ |
| **INC-S02-03** | **Intercambio de Requisitos RF04 y RF05** | En secciones del guion, se asignó erróneamente `RF04` a la exploración del catálogo curricular y `RF05` a los perfiles/disponibilidad horaria. | SRS FD03 §5.1, §5.2 y Cuadro 5.1 | Restablecer la numeración canónica: **RF04** es «Configuración de perfil formativo y matriz de disponibilidad horaria», y **RF05** es «Gestión del catálogo de asignaturas críticas y temarios silábicos». | La numeración oficial del SRS FD03 v2.0/v2.2 no admite reordenamientos ad-hoc. Cualquier intercambio genera ambigüedad en la trazabilidad hacia los casos de uso CUS15 y CUS21. | `GUION_EXPOSICION_SPRINT_02.md`, diapositivas, notas. | **Corregido** ✅ |
| **INC-S02-04** | **Confusión de Códigos HTTP (Mérito RN-03 vs. Autorización)** | El guion afirmaba que el incumplimiento del mérito académico (`ciclo_actual < 7`) devolvía `HTTP 403 Forbidden`, confundiéndolo con los controles de autorización y autopromoción. | Código en `role_service.py:58` y SAD FD04 §6.2.2 | Clarificar que el incumplimiento de mérito (RN-03) retorna **HTTP 400 Bad Request** con payload `{"code": "MERIT_RULE_VIOLATION"}`, mientras que **HTTP 403 Forbidden** se reserva para intentos de autopromoción sin privilegios de administrador o acceso cruzado entre cuentas. | Una violación a una regla de negocio sobre datos de entrada no válidos según el estado del estudiante constituye una solicitud malformada para la semántica del negocio (HTTP 400). HTTP 403 responde exclusivamente a fallas de autorización (autenticado pero no autorizado). | `GUION_EXPOSICION_SPRINT_02.md`, contratos OpenAPI, diapositivas. | **Corregido** ✅ |
| **INC-S02-05** | **Autoría del Proyecto y del Guion** | El documento `GUION_EXPOSICION_SPRINT_02.md` consignaba como autores a «Joan Sebastian Medina Lopez, Renzo Gabriel Paredes Rivas», nombres apócrifos no registrados en la cátedra. | Carátula oficial de SRS, SAD, `README.md` e informes G03 | Corregir los autores en todos los encabezados: **Joan Cristian Medina Quispe** (Código: 2022074255) y **Renzo Antonio Antayhua Mamani** (Código: 2022073504). Docente de Cátedra: **Dr. Ricardo Eduardo Valcárcel Alvarado**. | Preservar la integridad académica y la identidad institucional de los miembros del Grupo 03 (C-SharkTeam) en la Universidad Privada de Tacna. | `GUION_EXPOSICION_SPRINT_02.md`. | **Corregido** ✅ |
| **INC-S02-06** | **Declaraciones de Aprobación Institucional no Verificables** | Ciertas versiones mencionaban «Aprobado por Dirección EPIS» y «Certificación oficial de cumplimiento bajo Ley N° 29733». | Directrices de Ética Académica y Criterios del Curso | Sustituir declaraciones de aprobación externa por: «Estado: Entregado para evaluación docente de cátedra (Cierre de Sprint 02)» y «Funcionalidad diseñada e implementada para alinearse técnicamente a los principios de la Ley N° 29733, pendiente de homologación jurídica institucional». | No se debe afirmar aprobación docente o institucional sin constancia documental fehaciente, ni atribuir certificación legal a un incremento técnico de software. | SRS FD03 (versiones 2.1/2.2), SAD FD04, guion, diapositivas. | **Corregido** ✅ |
| **INC-S02-07** | **Discrepancia en Duración y Número de Sprints** | Algunos documentos abreviados (resúmenes ejecutivos preliminares) referían un plan de 5 sprints, mientras que el plan maestro oficial contempla 8 sprints. | `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (v1.2) | Estandarizar la referencia al **Plan Maestro de 8 Sprints** (S1 a S8, 91 horas de esfuerzo total planificado). Aclarar que la referencia a 5 sprints correspondía a una simplificación temática preliminar. | El documento canónico de planificación `PLAN_SPRINTS_Y_TAREAS.md` establece explícitamente 8 hitos con ventanas temporales y capacidad neta de 91 horas-persona distribuidas entre Joan (45 h) y Renzo (46 h). | `SNAPSHOT_INFO.md`, guion, presentación. | **Corregido** ✅ |
| **INC-S02-08** | **Métricas de Pruebas: Corte Sprint 02 vs. Estado de `main`** | En ramas posteriores y `SNAPSHOT_INFO.md` se mencionaban 171 o 209 pruebas. Esto causaba confusión con el corte real del Sprint 02. | Commit de integración `3766a08` / `786dd62` y `EVIDENCIA_PRUEBAS_SPRINT_02.md` | Delimitar taxativamente: Al cierre oficial del Sprint 02 (commit `3766a08` en frontend y consolidación `786dd62` en backend), la suite acumulada certificada es de **150 pruebas automatizadas** (84 backend y 66 frontend), con **90.64%** y **91.10%** de cobertura respectivamente. Las 171/209 pruebas corresponden a la incorporación del Sprint 03. | Evitar atribuir resultados de sprints posteriores a la entrega evaluada del Sprint 02. La evaluación académica exige delimitar el corte exacto del sprint. | Guion de exposición, informe G03, diapositivas. | **Corregido** ✅ |
| **INC-S02-09** | **Enlaces no Portables con Esquema `file:///`** | Múltiples documentos contenían hipervínculos absolutos `file:///c:/Users/Admin/Desktop/...` o `file:///d:/...` que impiden la navegación portable en otros entornos o en GitHub. | Estándar de portabilidad documental Markdown | Sustituir todos los enlaces `file:///` por rutas relativas portables navegables o enlaces permanentes al repositorio en GitHub. | Garantizar que cualquier docente, evaluador o estudiante pueda clonar el repositorio y navegar por la documentación sin enlaces rotos en su máquina local. | `GUION_EXPOSICION_SPRINT_02.md`, `INFORME_GENERAL_SPRINT_02.md`, `G03_EPIS_Informe_Sprint_02.md`. | **Corregido** ✅ |

---

## 3. Registro de Decisiones de Corrección Aplicadas

### Decisión 1: Homologación Terminológica del Frontend
Se revisó integralmente el frontend. El proyecto utiliza:
- React 19.0.0
- TypeScript 5.6.3
- Vite 6.0.5
- Vitest 2.1.8 con `@testing-library/react`
- Tailwind CSS

No existe rastro de Vue.js ni bibliotecas auxiliares como Vuex o Pinia. Se actualizaron todas las explicaciones arquitectónicas para reflejar el patrón de componentes funcionales de React, Hooks personalizados (`useState`, `useEffect`, `useMemo`), y servicios API tipados con Fetch API nativo.

### Decisión 2: Tratamiento Riguroso de la Ley N° 29733
El sistema implementa los controles técnicos necesarios para soportar el principio de consentimiento informado y finalidad:
1. Modal forzado previo al primer ingreso.
2. Persistencia inmutable del estado del consentimiento (`accepted = true/false`).
3. Registro de metadatos de auditoría: dirección IP, agente de usuario, versión del texto legal y marca temporal en UTC.
4. Bloqueo inmediato del acceso a las funcionalidades del sistema si el usuario declina o revoca el consentimiento.

Sin embargo, el equipo deja constancia explícita en todos los documentos de que la plataforma no cuenta con dictamen legal ni certificación emitida por la Autoridad Nacional de Protección de Datos Personales (ANPDS), constituyendo una implementación técnica orientada al cumplimiento normativo en el marco de un proyecto académico universitario.

### Decisión 3: Clarificación de Códigos de Error HTTP
Se formalizó la distinción semántica entre los errores del Sprint 02:
- `HTTP 400 Bad Request`: Disparado por validaciones del negocio, notablemente `code: "MERIT_RULE_VIOLATION"` cuando un estudiante con `ciclo_actual < 7` solicita asignación como mentor, o cuando las franjas horarias violan la restricción `hora_inicio < hora_fin`.
- `HTTP 401 Unauthorized`: Ausencia o expiración del token Bearer JWT.
- `HTTP 403 Forbidden`: Violación de políticas de autorización o aislamiento, como un usuario que intenta autopromoverse a mentor sin rol de administrador institucional, o un usuario que intenta modificar el perfil o disponibilidad de un tercero.
- `HTTP 404 Not Found`: Asignatura, rol o perfil inexistente.
- `HTTP 422 Unprocessable Entity`: Fallo de validación estructural en esquemas Pydantic v2 (tipos incorrectos, cadenas vacías, campos obligatorios omitidos).
