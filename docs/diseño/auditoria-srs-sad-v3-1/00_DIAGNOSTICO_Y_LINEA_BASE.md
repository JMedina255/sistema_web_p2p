# INFORME DE DIAGNÓSTICO Y LÍNEA BASE DOCUMENTAL (H00)
## Auditoría y Refinamiento Documental SRS/SAD v3.1

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT<br>
**Curso:** Construcción de Software I<br>
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas<br>
**Equipo Consultor:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)<br>
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado<br>
**Semestre Académico:** 2026-II<br>
**Fecha de Emisión:** 14 de Noviembre de 2026<br>
**Rama de Trabajo Base:** `main` (integrada mediante PR #11)<br>
**Commit Base Inicial de Auditoría:** `097f90d725e537f411ebadac740905e0c0448f61`<br>
**Commit Base Integrado en Main:** `0542aa2af8d30ecb6afdfa9d4561d0f07a1801b0`

---

## Control de Versiones

A continuación, se presenta el registro histórico de versiones del presente informe de diagnóstico:

### Cuadro 0.1: Registro de Control de Versiones del Entregable H00

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani | Pendiente de revisión (Dr. Ricardo Valcárcel) | Pendiente de aprobación (Dirección EPIS) | 14/11/2026 | Emisión inicial del diagnóstico de línea base, auditoría crítica integral de las versiones v3.0 del SRS y SAD frente al código fuente en rama `main` y formulación del plan de homologación documental H00–H11. |
| **1.1** | Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani | Pendiente de revisión (Dr. Ricardo Valcárcel) | Pendiente de aprobación (Dirección EPIS) | 14/11/2026 | Rectificación H01-R: incorporación formal de HALL-11 (`dummyIdToken`), clarificación metodológica entre discrepancia diagnosticada, decisión aprobada y aplicación en documentos maestros, notas de validación en pruebas (682 históricas) y conversión a rutas relativas portables. |

Fuente: Elaboración propia.

El presente cuadro certifica el registro formal del informe H00 dentro del ciclo de auditoría documental, delimitando la autoría técnica del equipo consultor y consignando formalmente el estado de revisión y aprobación académica ante la cátedra de Construcción de Software I y la Dirección de la EPIS.

---

## 1. Propósito y Alcance del Diagnóstico

El objetivo del presente informe es establecer la **Línea Base Oficial de Auditoría** para la transición documental hacia la versión **v3.1** de la Especificación de Requerimientos de Software ([FD03-EPIS-Informe SRS de Proyecto.md](../FD03-EPIS-Informe%20SRS%20de%20Proyecto.md)) y el Documento de Arquitectura de Software ([FD04-EPIS-Informe SAD de Proyecto.md](../FD04-EPIS-Informe%20SAD%20de%20Proyecto.md)).

La auditoría evalúa exhaustivamente la consistencia, exactitud técnica, completitud y trazabilidad de los documentos de diseño respecto a la implementación real del código fuente en la rama principal (`main`), asegurando que ambos artefactos constituyan documentos de máxima rigurosidad académica para los procesos de acreditación universitaria y sustentación de cátedra.

El alcance comprende:
1. **Contraste de Especificaciones Funcionales:** Evaluación de la matriz de Requerimientos Funcionales (`RF01`–`RF26`), Reglas de Negocio (`RN-01`–`RN-14`) y los 24 Casos de Uso Canónicos (`CUS-001`–`CUS-024`).
2. **Contraste Arquitectónico y Técnico:** Evaluación del modelo relacional físico en PostgreSQL/Supabase (16 tablas físicas), contratos de API REST (FastAPI), servicios en segundo plano, seguridad RBAC/RLS e infraestructura externa.
3. **Control de Calidad Normativo:** Comprobación de las reglas de diseño [reglas_documentacion_diseño.md](../../reglas_documentacion_diseño.md) (Reglas D-1 a D-10) y la plantilla de narrativas [REGLAS_Y_PLANTILLA_NARRATIVAS_SRS.md](../REGLAS_Y_PLANTILLA_NARRATIVAS_SRS.md).

---

## 2. Inventario de Fuentes Documentales y Técnicas Auditadas

A continuación, se detallan las fuentes primarias inspeccionadas durante el proceso de auditoría:

### Cuadro 0.2: Inventario de Fuentes Documentales y Técnicas Inspeccionadas

| Categoría | Ruta del Archivo / Componente | Versión / Estado | Propósito y Relevancia en la Auditoría |
| :--- | :--- | :---: | :--- |
| **Documento Principal** | `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` | v3.0 (607 KB) | Especificación de Requerimientos vigente de la fase de diseño. |
| **Documento Principal** | `docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md` | v3.0 (185 KB) | Documento de Arquitectura de Software vigente de la fase de diseño. |
| **Fuente Histórica** | `docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md` | v2.0 (Histórico) | Línea base analítica preliminar para contraste de evolución. |
| **Fuente Histórica** | `docs/analisis/FD04-EPIS-Informe SAD de Proyecto.md` | v1.1 (Histórico) | SAD inicial de la fase de análisis. |
| **Normativa Técnica** | `reglas_documentacion_diseño.md` | v1.0 | Normas de diseño prescriptivo (Reglas D-1 a D-10). |
| **Normativa Técnica** | `docs/diseño/REGLAS_Y_PLANTILLA_NARRATIVAS_SRS.md` | v2.0 | Estándar institucional de narrativas exhaustivas de casos de uso. |
| **Artefacto de Diseño** | `docs/diseño/NARRATIVAS_FASE_DISEÑO_CONSOLIDADAS.md` | v3.0 (196 KB) | Bóveda consolidada de narrativas de diseño. |
| **Artefacto de Diseño** | `docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md` | v3.0 (142 KB) | Banco de 24 diagramas de secuencia canónicos bajo Visual Paradigm. |
| **Bóveda UML** | `docs/diagramas_general.md` | v3.0 (73 KB) | Bóveda centralizada de diagramas PlantUML sincronizados. |
| **Auditoría Previa** | `docs/INFORME_AUDITORIA_ESTADO_REAL_Y_DEUDA_TECNICA.md` | 12/11/2026 | Auditoría post-Sprint 08 con los 14 hallazgos de severidad. |
| **Planificación** | `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` | Sprints 01–08 | Plan integral de tareas de ingeniería de software. |
| **Código Backend** | `aplicacion/backend/app/api/v1/endpoints/` | 17 módulos | Controladores REST reales implementados en FastAPI. |
| **Código Backend** | `aplicacion/backend/app/models/` | 12 archivos | Modelos ORM relacionales en SQLAlchemy. |
| **Código Backend** | `aplicacion/backend/app/db/migrations/versions/` | 5 migraciones | DDL relacional versionado de PostgreSQL con Alembic. |
| **Código Frontend** | `aplicacion/frontend/src/components/` | 23 vistas | Vistas e interfaces reactivas en React 19 y Tailwind CSS. |
| **Código Frontend** | `aplicacion/frontend/src/services/` | 10 clientes | Clientes HTTP tipados conectados a la API REST. |
| **Integración CI** | `.github/workflows/ci.yml` | Vigente | Pipeline de integración continua de pruebas y linteo. |

Fuente: Elaboración propia.

El análisis de las fuentes demuestra que existe un repositorio activo y altamente cohesionado, con una batería de código real que ha superado la etapa inicial de prototipado y demanda una actualización rigurosa de su documentación rectora para reflejar las capacidades efectivamente desplegadas.

---

## 3. Matriz de Hallazgos Críticos y Diagnóstico Estructurado

A continuación, se exponen los once (11) hallazgos de inconsistencia identificados durante la auditoría técnica documental:

### Cuadro 0.3: Matriz de Hallazgos Críticos de Auditoría Documental

| ID | Categoría | Componentes Afectados | Severidad | Descripción del Hallazgo y Evidencia Técnica | Estado Metodológico en el Flujo Documental |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **HALL-01** | Inconsistencia de Requisitos | SRS 5.3, 5.5 vs. SAD 4.1, 4.3 y Migración 005 | **ALTA** | **Divergencia semántica en RF20:** En el SRS v3.0, `RF20` figura como *"Gestión y descarga de recursos académicos"* (`SessionResourcesView.tsx`, `ResourceService.py`). En el SAD v3.0 y en el código real (Migración `005_closure_and_advanced_modules.py` línea 67, `survey_service.py`, `encuestas_calidad`), `RF20` corresponde a la *"Captura de encuestas de calidad post-mentoría 24h"*. | **Discrepancia diagnosticada; decisión adoptada.** Pendiente de aplicación en Sección 5 del SRS (programada para H02). |
| **HALL-02** | Contradicción de Nomenclatura | Textos narrativos en SRS y SAD vs. Línea Base Canónica | **ALTA** | **Referencias cruzadas obsoletas de CUS-008 y CUS-011:** En la fase de análisis histórica, `CUS08` era *"Bitácora y Asistencia"* y `CUS11` era *"Asistencia QR"*. En la línea base canónica de diseño, `CUS-008` es *"Consultar disponibilidad de espacios y recursos"* (MOD-02) y `CUS-011` es *"Generar reportes e indicadores de analítica académica"* (MOD-08). Existen múltiples párrafos descriptivos en el SRS que aún aluden a `CUS08` como bitácora y a `CUS11` como asistencia QR. | **Discrepancia diagnosticada; decisión adoptada.** Pendiente de depuración textual integral en SRS y SAD (H02, H07). |
| **HALL-03** | Desfase en Persistencia | SAD 10.1, 10.2 vs. Migración 005 y Modelos ORM | **MEDIA-ALTA** | **Diccionario físico incompleto:** El SAD v3.0 titula y describe la sección 10.2 como *"Diccionario DDL Físico de las 15 Tablas Relacionales"*. Sin embargo, la migración `005_closure_and_advanced_modules.py` y `app/models/__init__.py` implementan **16 entidades relacionales**, omitiendo en el diccionario formal la tabla `tokens_asistencia_activos` (soporte multi-worker para TOTP dinámico de asistencia). | **Discrepancia diagnosticada; decisión adoptada.** El SAD conserva 15 tablas físicamente hasta su actualización formal en H08. |
| **HALL-04** | Discrepancia de Entorno | SAD 1.5, Control de Cambios vs. `.github/workflows/ci.yml` | **MEDIA** | **Versión de Python desalineada:** El SAD v3.0 (línea 32) declara *"FastAPI 0.115+ en Python 3.14"*. Python 3.14 no es una versión estable del lenguaje. El workflow de CI (`ci.yml` línea 68) y el entorno de ejecución ejecutan estrictamente **Python 3.13**, configurando una inconsistencia técnica formal. | **Discrepancia diagnosticada; decisión adoptada.** Pendiente de corrección formal en texto del SAD (H07). |
| **HALL-05** | Rutas API Desactualizadas | SRS 5.3, 5.5 vs. Routers en `app/api/v1/endpoints/` | **ALTA** | **Contratos REST desincronizados en SRS:** Las matrices del SRS citan rutas no existentes en la implementación actual, tales como `GET /api/v1/spaces/availability` (la ruta real es `/api/v1/spaces/free-slots` y `/api/v1/spaces/classrooms`), `PUT /api/v1/mentorships/offers/{id}/reschedule` (el router es `/api/v1/offers`) y `GET /api/v1/analytics/dashboard` (actualmente simulado en testbench algorítmico). | **Discrepancia diagnosticada; decisión adoptada.** Pendiente de aplicación en Sección 5 del SRS (H02) y SAD (H08). |
| **HALL-06** | Omisión de Servicios Reales | SAD 2.5, 6.3 vs. Commits `3f6e31d`, `4ca157b` | **MEDIA-ALTA** | **Servicios externos de producción no documentados en SAD:** Tras subsanar los 14 hallazgos de auditoría crítica, se implementó transporte SMTP real para Gmail institucional, persistencia en Supabase Storage (buckets de constancias y guías), Google Identity Services (GIS SDK oficial) y scheduler de quórum, los cuales carecen de fichas formales de arquitectura en el SAD. | **Discrepancia diagnosticada; decisión adoptada.** Pendiente de incorporación en vistas de implementación y despliegue del SAD (H07, H08). |
| **HALL-07** | Métricas de Prueba Desfasadas | SRS 7, SAD 1.5 vs. Historial de Commits | **MEDIA** | **Desfase en la cuantificación de pruebas automatizadas:** El SRS y SAD v3.0 reportan de forma rígida 627 pruebas automatizadas (280 backend, 347 frontend). Las verificaciones post-sprint 08 registraron 658 pruebas y la incorporación de servicios externos elevó la suite a 682 pruebas (cifra histórica reportada en commit `3f6e31d`). Dicha cifra queda consignada como histórica y pendiente de nueva validación en CI debido a fallas de linteo registradas en ejecuciones recientes de `main`. | **Discrepancia diagnosticada; criterio adoptado.** Se registra como cifra histórica sujeta a revalidación formal tras subsanación de linteo. |
| **HALL-08** | Profundidad Dispar en Narrativas | SRS 6.2.3 (24 CUS) vs. Estándar de Narrativas | **ALTA** | **Narrativas con enfoque excesivamente técnico/backend:** Las narrativas vigentes en el SRS v3.0 están orientadas casi exclusivamente a servicios ORM, transacciones y bloqueos pesimistas, careciendo del desglose funcional de interfaz visual exigido (componentes exactos, colores en lenguaje natural, botones entre comillas, subflujos, flujos alternativos detallados y escenarios Given-When-Then). | **Discrepancia diagnosticada; estándar definido en H01.** Casos piloto (`CUS-001`, `CUS-003`) aplicados; 22 CUS restantes programados para H04–H06. |
| **HALL-09** | Confusión Metodológica de Roles | SRS 5.3, 6.2.3 vs. SAD 6.2, 9.1 | **MEDIA-ALTA** | **Inversión de responsabilidades SRS vs. SAD:** El SRS incluye indebidamente nombres de scripts Python (`BitacoraService.py`), componentes TypeScript y sentencias SQL en las descripciones de requerimientos funcionales para el usuario, mientras que el SAD presenta descripciones someras de contratos de interfaz en los módulos más recientes. | **Discrepancia diagnosticada; regla adoptada.** SRS responderá ¿QUÉ? (H02–H06) y SAD responderá ¿CÓMO? (H07–H09). |
| **HALL-10** | Incumplimiento Parcial D-2 | Secciones 6.3.1 y 6.3.2 del SRS | **MEDIA-BAJA** | **Tablas y figuras sin estructura quíntuple:** Se detectaron cuadros y bloques PlantUML que carecen de párrafo de análisis posterior o cuya fuente formal no está explícitamente declarada conforme a la regla D-2. | **Discrepancia diagnosticada.** Corrección progresiva programada en H02 y H10. |
| **HALL-11** | Ruta de Contingencia en Frontend | `LoginOtpView.tsx` (líneas 263–272) vs. Autenticación Real | **MEDIA** | **Generación de `dummyIdToken` en fallback federado:** En el componente de login, la función de contingencia ante ausencia de Google Identity Services genera un token simulado con payload en Base64 (`dummyIdToken = header.${mockPayload}.signature`) con usuario predeterminado (`ra2022073504@virtual.upt.pe`). Constituye un mecanismo de bypass para pruebas/desarrollo que requiere revisión técnica para entornos productivos. | **Hallazgo técnico registrado en H01-R.** Catalogado como deuda técnica de revisión pendiente; se mantiene intacto el código fuente en esta fase documental. |

Fuente: Elaboración propia a partir de la auditoría técnica cruzada sobre el repositorio `sistema_web_p2p`.

El análisis del Cuadro 0.3 pone de manifiesto que, si bien el proyecto cuenta con una base de código funcional y un avance de ingeniería sobresaliente, existen divergencias críticas de trazabilidad entre la documentación de análisis/diseño y la implementación real. Resolver estas discrepancias es imperativo para garantizar la coherencia del software ante evaluaciones institucionales.

---

## 4. Detalle y Evidencia de Hallazgos Principales

### 4.1. HALL-01: Discrepancia Crítica en la Definición de RF20
* **Evidencia en SRS v3.0:** En las tablas 5.3 (Matriz de Requerimientos Funcionales) y 5.5 (Matriz de Trazabilidad), `RF20` se titula *"Gestión y descarga de recursos académicos"* vinculado a `SessionResourcesView.tsx`, `ResourceService.py` y `RecursoAcademico`.
* **Evidencia en SAD v3.0 y Código Fuente:** En la sección 4.1 del SAD, `RF20` se especifica como *"Captura de encuestas de calidad post-mentoría 24h"*. En el backend, la migración `005_closure_and_advanced_modules.py` declara formalmente:
  ```python
  # 3. Tabla encuestas_calidad (T-37 / T-39 / CUS18 / RF20 / RNF07)
  ```
  y los controladores en `app/api/v1/endpoints/survey.py` implementan `SurveyService` sobre la tabla relacional `encuestas_calidad`.
* **Decisión Técnica para v3.1:** Mantener `RF20` formalmente como **Encuestas de Calidad y Retroalimentación Post-Mentoría (MOD-06)** en el SRS, y reasignar la capacidad de gestión de recursos didácticos compartidos como un requerimiento complementario o atributo dentro de `RF08/RF19`, sincronizando de inmediato ambos documentos maestros.

### 4.2. HALL-02: Referencias Cruzadas de CUS-008 y CUS-011
* **Evidencia:** En el historial de análisis (`docs/analisis/`), `CUS08` correspondía a *"Registrar bitácora pedagógica y control de asistencia"* y `CUS11` a *"Registrar asistencia mediante código QR"*. Al migrar a la estructura modular oficial de 8 módulos de la fase de diseño:
  - `CUS-008` fue reasignado a *"Consultar disponibilidad de espacios y recursos"* (`MOD-02`).
  - `CUS-011` fue reasignado a *"Generar reportes e indicadores de analítica académica"* (`MOD-08`).
  - El registro de asistencia pasó canónicamente a `CUS-012` y la bitácora a `CUS-013` (`MOD-06`).
* **Inconsistencia Detectada:** En diversos pasajes explicativos del SRS v3.0 (por ejemplo, en las justificaciones de los diagramas de secuencia 6.15.7 y diagramas de clases 6.16.8), se mantuvieron menciones textuales tales como: *"...para el posterior control de asistencia en la bitácora docente (CUS08)"*, generando severa confusión para el revisor técnico.
* **Decisión Técnica para v3.1:** Depurar y homologar en la totalidad del texto las llamadas a `CUS-008` (Espacios) y `CUS-011` (Reportes Analíticos), referenciando para bitácora y asistencia exclusivamente a `CUS-012` y `CUS-013`.

### 4.3. HALL-03: Omisión de la Tabla `tokens_asistencia_activos` en el SAD
* **Evidencia:** La migración física `005_closure_and_advanced_modules.py` (líneas 116–132) crea la tabla relacional:
  ```sql
  CREATE TABLE tokens_asistencia_activos (
      id_token SERIAL PRIMARY KEY,
      id_sesion INTEGER NOT NULL REFERENCES sesiones_mentoria(id_sesion) ON DELETE CASCADE,
      token VARCHAR(64) NOT NULL,
      totp_code VARCHAR(6) NOT NULL,
      expires_at TIMESTAMPTZ NOT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      CONSTRAINT uq_tokens_asistencia_activos_sesion UNIQUE (id_sesion)
  );
  ```
  Esta tabla es indispensable para soportar el refresco TOTP dinámico de 30 segundos en despliegues con múltiples instancias o workers asíncronos. Sin embargo, el SAD v3.0 mantiene el encabezado *"15 Tablas Relacionales"* y omite la ficha DDL de esta entidad física.
* **Decisión Técnica para v3.1:** Actualizar el SAD a **16 Tablas Relacionales**, incorporando el diagrama entidad-relación y la ficha DDL completa de `tokens_asistencia_activos`.

### 4.4. HALL-04: Versión de Lenguaje Python 3.13 vs. 3.14
* **Evidencia:** En el control de cambios y en la sección 1.5 del SAD v3.0 se indica *"FastAPI 0.115+ en Python 3.14"*. El archivo `.github/workflows/ci.yml` (línea 68) define:
  ```yaml
  - name: Configurar Python
    uses: actions/setup-python@v5
    with:
      python-version: "3.13"
  ```
* **Decisión Técnica para v3.1:** Corregir formalmente la especificación tecnológica a **Python 3.13**, garantizando total veracidad con la configuración de integración continua y el entorno de ejecución. La corrección material en el documento SAD se encuentra programada para el hito H07.

### 4.5. HALL-11: Ruta de Contingencia de Autenticación (`dummyIdToken`) en Frontend
* **Evidencia Técnica:** En `aplicacion/frontend/src/components/LoginOtpView.tsx` (líneas 263–272), ante la eventualidad de fallos o indisponibilidad en la carga del script oficial de Google Identity Services (GIS), la función `handleGoogleFederatedFallback` construye un token simulado con estructura JWT ficticia:
  ```typescript
  const mockPayload = btoa(
    JSON.stringify({
      email: targetEmail,
      given_name: 'Renzo Antonio',
      family_name: 'Antayhua Mamani',
    })
  );
  const dummyIdToken = `header.${mockPayload}.signature`;
  const resp = await authService.loginWithGoogle(dummyIdToken);
  ```
* **Diagnóstico de Auditoría:** Si bien este mecanismo permite sortear bloqueos de red o pruebas locales desconectadas, constituye una vía de acceso de prueba que no debe considerarse mecanismo de producción. Se cataloga como un hallazgo de revisión técnica pendiente. No se efectúa modificación sobre el código funcional en el presente hito documental, dejándose constancia de su necesidad de revisión en la fase de endurecimiento de seguridad.

---

## 5. Plan de Acción y Cronograma de Homologación Documental (H01–H11)

A continuación, se define la hoja de ruta metodológica estructurada para la ejecución de los hitos de auditoría y refinamiento:

### Cuadro 0.4: Cronograma y Hoja de Ruta de los Hitos de Refinamiento Documental

| Hito | Denominación y Alcance Técnico | Entregable Principal | Estado |
| :---: | :--- | :--- | :---: |
| **H00** | **Preparación y Auditoría Inicial:** Creación de rama, inventario documental, detección de inconsistencias y diagnóstico de línea base. | `docs/diseño/auditoria-srs-sad-v3-1/00_DIAGNOSTICO_Y_LINEA_BASE.md` | **Culminado** ✅ (Integrado en `main`) |
| **H01** | **Homologación y Patrón de Narrativas:** Matriz canónica de trazabilidad (MOD→RF→RN→CUS→Código), guía de narrativas detalladas y refinamiento de 2 casos piloto (`CUS-001`, `CUS-003`). | `01_MATRIZ_HOMOLOGACION.md`<br>`02_GUIA_NARRATIVAS_DETALLADAS.md`<br>Actualización SRS v3.0 (`CUS-001`, `CUS-003`) | **Culminado** ✅ (Integrado en `main`) |
| **H01-R** | **Rectificación de Homologación y Evidencias:** Subsanación de inconsistencias de auditoría, diferenciación de estados metodológicos, documentación de `dummyIdToken`, notas de CI y rutas portables. | `03_RECTIFICACIONES_H01.md`<br>Actualización de entregables H00, H01 y scripts de diseño | **En Ejecución** ⏳ |
| **H02** | **Refinamiento Funcional del SRS:** Revisión y actualización integral de capítulos 1 al 5 (Problema, Objetivos, Alcance, Actores, RF01–RF26, RNF01–RNF10, RN-01–RN-14). | Actualización de secciones 1 a 5 del SRS (`generate_part_a.py`) | Autorizado / En curso |
| **H03** | **Calidad y Trazabilidad del SRS:** Matrices de trazabilidad bidireccional, especificación de interfaces externas WCAG 2.1 AA y criterios de aceptación. | Actualización de matrices y sección 5.6 del SRS | Pendiente |
| **H04** | **Narrativas Exhaustivas MOD-01 al MOD-03:** Especificación detallada de casos de uso de seguridad, espacios y catálogo curricular (`CUS-001`, `CUS-010`, `CUS-006`, `CUS-008`, `CUS-005`, `CUS-021`). | Actualización de sección 6.2.3 (MOD 01-03) | Pendiente |
| **H05** | **Narrativas Exhaustivas MOD-04 al MOD-06:** Especificación detallada de recomendador, quórum, asistencias y bitácoras (`CUS-002`, `CUS-003`, `CUS-004`, `CUS-024`, `CUS-017`, `CUS-023`, `CUS-007`, `CUS-012`, `CUS-013`, `CUS-014`). | Actualización de sección 6.2.3 (MOD 04-06) | Pendiente |
| **H06** | **Narrativas Exhaustivas MOD-07 al MOD-08:** Especificación de gamificación, constancias, reportes analíticos y auditoría (`CUS-018`, `CUS-019`, `CUS-009`, `CUS-011`, `CUS-015`, `CUS-016`, `CUS-020`, `CUS-022`). | Actualización de sección 6.2.3 (MOD 07-08) | Pendiente |
| **H07** | **Arquitectura General del SAD:** Modelo 4+1 vistas, componentes C4 Nivel 2, responsabilidades modulares y topología de despliegue. | Actualización de secciones 1 a 5 y 8 del SAD | Pendiente |
| **H08** | **SAD de Contratos y Persistencia:** Catálogo OpenAPI 3.0 actualizado, Diccionario DDL Físico de las 16 tablas y políticas de seguridad RLS. | Actualización de secciones 6 y 10 del SAD | Pendiente |
| **H09** | **SAD de Procesos y Decisiones:** FSM de 13 estados de sesión y 9 de reserva, transaccionalidad ACID pesimista, catálogo de errores y ADR-001 al ADR-016. | Actualización de secciones 7, 11, 12, 13 y 14 del SAD | Pendiente |
| **H10** | **Homologación de Diagramas e Iconografía:** Verificación y sincronización de figuras PlantUML, numeración canónica, fuentes formales y bóveda `diagramas_general.md`. | Sincronización completa de diagramas UML | Pendiente |
| **H11** | **Auditoría Final y Cierre Documental v3.1:** Verificación de trazabilidad al 100%, revisión ortotipográfica y estilística, y emisión del informe final de cierre. | Informe de Cierre y Emisión SRS/SAD v3.1 | Pendiente |

Fuente: Elaboración propia.

El plan presentado en el Cuadro 0.4 garantiza una ejecución disciplinada y modular. Conforme a la instrucción rectora recibida, la fase inmediata en desarrollo comprende los hitos **H01-R** y **H02**, manteniéndose congelada cualquier modificación sobre el SAD hasta los hitos H07–H09.

---

## 6. Conclusión de la Línea Base de Auditoría

El presente informe H00 certifica la existencia de una discrepancia documentada entre las descripciones de requerimientos del SRS v3.0, la arquitectura formalizada en el SAD v3.0 y la implementación efectiva del sistema en la rama `main` al commit `097f90d` y su integración en `0542aa2`.

La resolución de los once hallazgos críticos detectados permitirá elevar la calidad documental del proyecto a un estándar de excelencia académica, dotando a la Universidad Privada de Tacna y a la EPIS de un instrumento técnico fidedigno, auditable y directamente transferible a la práctica profesional de la ingeniería de software.
