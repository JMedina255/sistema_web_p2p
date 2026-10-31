# Mapa Maestro de Fuentes, Trazabilidad y Fundamentación Técnica — Presentación Sprint 03

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre Académico 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe & Renzo Antonio Antayhua Mamani)  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Documento Técnico:** `docs/sprints/sprint-03/02-trazabilidad/MAPA_FUENTES_PRESENTACION_SPRINT_03.md`  
**Estado:** Documento Perfeccionado — Versión 2.0 (Fase 1.5 de Auditoría, Trazabilidad y Aprobación de Contenido)  

---

## A. Información de Auditoría

* **Repositorio de Referencia:** `https://github.com/JMedina255/sistema_web_p2p`
* **Rama Evaluada:** `main`
* **SHA del Commit de Referencia (Línea Base Congelada):** [`7df0a88345a06254940eab8f2d7d8b7f4d33d1e0`](https://github.com/JMedina255/sistema_web_p2p/tree/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0) (Commit corto: `7df0a88`)
* **Fecha de Revisión y Auditoría:** 31 de octubre de 2026
* **Directorios y Archivos Examinados:**
  1. `docs/analisis/`: Especificación original de requisitos (SRS FD03 v2.0), arquitectura (SAD FD04 v1.1) y Catálogo Oficial de Pruebas en Excel (`Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`).
  2. `docs/diseño/`: Requisitos refinados (SRS FD03 v2.1), arquitectura prescriptiva (SAD FD04 v2.0), Informe Académico Canónico G03 (`G03_EPIS_Informe_Sprint_03.md`), Informe Técnico Maestro (`INFORME_GENERAL_SPRINT_03.md`), Evidencia de Pruebas (`EVIDENCIA_PRUEBAS_SPRINT_03.md`), Trazabilidad de Ofertas (`TRAZABILIDAD_PUBLICACION_OFERTAS.md`) y acervo gráfico en `imagenes/sprint-03/`.
  3. `docs/sprints/`: Plan maestro de sprints y tareas (`PLAN_SPRINTS_Y_TAREAS.md`) y bitácora de ejecución (`sprint-03.md`).
  4. `aplicacion/backend/`: Modelos ORM, esquemas Pydantic v2, servicios de dominio (`OfferService`, `RecommendationService`, `SimulationService`), endpoints REST, migración Alembic `003_mentoring_offers.py` y 122 pruebas en Pytest.
  5. `aplicacion/frontend/`: Componente reactivo accesible `OfferPublishView.tsx`, cliente de servicio `offerService.ts`, orquestador `App.tsx` y 87 pruebas en Vitest.
* **Criterios Metodológicos para Determinar Fuentes Autoritativas:**
  * **Precedencia Documental Formal:** Rige el orden canónico $\text{SRS (FD03)} \succ \text{SAD (FD04)} \succ \text{Plan de Sprints} \succ \text{Código y Pruebas} \succ \text{Materiales de Exposición}$.
  * **Inmutabilidad de Línea Base:** Se preservan con rigurosidad las nomenclaturas canónicas (`RF06`, `RF08`, `CUS02`, `CUS06`, `RN-03`, `RN-04`, `RN-05`, `RN-06`, `RN-07`, `RN-11`).
  * **Trazabilidad Verificable:** Cada afirmación, número de línea y celda ha sido contrastado contra los archivos físicos del repositorio sin tolerar ubicaciones aproximadas o simuladas.
  * **Separación de Madurez Técnica:** Se distingue formalmente el comportamiento persistido con transacciones ACID en PostgreSQL de los adaptadores de prueba en memoria (*mocks*) y datos curriculares semilla.

---

## B. Índice Maestro de Fuentes Auditadas

A continuación, se listan todas las fuentes documentales, técnicas, analíticas y de código empleadas para respaldar la exposición del Sprint 03:

### Cuadro B.1: Catálogo Exhaustivo de Fuentes Autoritativas

| N.° | Nombre de Fuente | Tipo de Artefacto | Ruta Relativa en Repositorio | Sección / Apartado | Rango Líneas / Celdas | Enlace Directo a GitHub (SHA `7df0a88`) |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **F-01** | Catálogo Oficial de Pruebas | Matriz Excel de Análisis | `docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` | Hoja: `Catálogo de Pruebas` | A14:O21 (CUS02), A41:O48 (CUS06) | [Ver en Repo](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx) |
| **F-02** | SRS Canónico (Diseño v2.1) | Requerimientos de Software | `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` | Tablas RF06/08, RNs, Narrativas CUS02 y CUS06 | L512-515, L547-557, L1610-1648, L1742-1784 | [L1610-L1784](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1610-L1784) |
| **F-03** | SAD Prescriptivo (Diseño v2.0) | Arquitectura de Software | `docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md` | Vistas 4+1, Contenedor C4, DDL y Casos de Uso | L110-111, L180-194, L648-650, L798-804, L1165 | [L110-L1165](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md#L110-L1165) |
| **F-04** | Informe Académico Canónico G03 | Informe Formal de Sprint | `docs/diseño/G03_EPIS_Informe_Sprint_03.md` | 11 Secciones, Formulación EdRecSys, Contratos REST | L1-576 (L280-345 matemática, L350-380 API) | [L1-L576](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L1-L576) |
| **F-05** | Informe General Técnico S3 | Reporte Maestro Exhaustivo | `docs/diseño/INFORME_GENERAL_SPRINT_03.md` | Ficha técnica, código, DDL, pruebas y evidencias | L1-1050 | [L1-L1050](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/INFORME_GENERAL_SPRINT_03.md#L1-L1050) |
| **F-06** | Evidencia de Pruebas S3 | Catálogo de Pruebas S3 | `docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_03.md` | Matrices de suites, coberturas y comandos | L1-420 | [L1-L420](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/EVIDENCIA_PRUEBAS_SPRINT_03.md#L1-L420) |
| **F-07** | Trazabilidad Ofertas (INF-TRZ-01) | Documento de Trazabilidad | `docs/diseño/TRAZABILIDAD_PUBLICACION_OFERTAS.md` | Secuencia técnica PlantUML y flujo CUS06 | L1-559 (L72-128 PlantUML) | [L72-L128](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/TRAZABILIDAD_PUBLICACION_OFERTAS.md#L72-L128) |
| **F-08** | Bitácora de Sprint 3 | Registro de Ejecución | `docs/sprints/sprint-03.md` | Tareas T-14, T-15, T-16, T-18, Métricas consolidadas | L1-391 | [L1-L391](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L1-L391) |
| **F-09** | Plan Maestro de Sprints | Planificación Scrum | `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` | Product Backlog PB-009, PB-010 y Tabla 5.4 | L49, L77-78, L152-167, L174-184 | [L152-L184](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/PLAN_SPRINTS_Y_TAREAS.md#L152-L184) |
| **F-10** | Modelo ORM SesionMentoria | Código Backend (Persistencia) | `aplicacion/backend/app/models/offer.py` | Clase `SesionMentoria`, restricciones y claves | L9-65 | [L9-L65](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/models/offer.py#L9-L65) |
| **F-11** | Esquemas Pydantic v2 Ofertas | Código Backend (Contratos) | `aplicacion/backend/app/schemas/offer.py` | `PublishOfferPayload`, validadores RN-04/05 | L6-79 | [L6-L79](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/schemas/offer.py#L6-L79) |
| **F-12** | Esquemas Recomendador | Código Backend (Contratos) | `aplicacion/backend/app/schemas/recommendation.py`| `ScoreBreakdown`, `OfferRecommendationItem` | L6-125 | [L6-L125](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/schemas/recommendation.py#L6-L125) |
| **F-13** | Servicio de Ofertas Backend | Código Backend (Lógica) | `aplicacion/backend/app/services/offer_service.py` | `OfferService`, validación RN-03, RN-04, RN-05 | L105-409 (L128-181 RN-03) | [L105-L409](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/offer_service.py#L105-L409) |
| **F-14** | Servicio EdRecSys v1.0 | Código Backend (Algoritmo) | `aplicacion/backend/app/services/recommendation_service.py` | Similitud Jaccard, grilla 6x11, ranking Top-k | L128-156, L159-716 | [L128-L716](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L128-L716) |
| **F-15** | Servicio de Simulación y Testbench | Código Backend (Testbench) | `aplicacion/backend/app/services/simulation_service.py` | Cohortes sintéticas, 4 casos frontera, benchmark | L9-411 | [L9-L411](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/simulation_service.py#L9-L411) |
| **F-16** | Endpoints REST de Ofertas | Código Backend (API) | `aplicacion/backend/app/api/v1/endpoints/offers.py` | `POST /api/v1/offers`, `GET /api/v1/offers` | L20-62 | [L20-L62](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/api/v1/endpoints/offers.py#L20-L62) |
| **F-17** | Endpoints Recomendador | Código Backend (API) | `aplicacion/backend/app/api/v1/endpoints/recommendations.py`| `/mentors`, `/offers`, `/explain`, `/testbench` | L27-125 | [L27-L125](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/api/v1/endpoints/recommendations.py#L27-L125) |
| **F-18** | Migración Alembic 003 | Código Backend (BD DDL) | `aplicacion/backend/app/db/migrations/versions/003_mentoring_offers.py` | Creación de tabla `sesiones_mentoria`, índices | L25-77 | [L25-L77](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/db/migrations/versions/003_mentoring_offers.py#L25-L77) |
| **F-19** | Pruebas Backend de Ofertas | Código Backend (Tests) | `aplicacion/backend/tests/test_offers.py` | 14 pruebas de límites, permisos, aforos, BD | L26-449 | [L26-L449](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_offers.py#L26-L449) |
| **F-20** | Pruebas Backend Recomendador | Código Backend (Tests) | `aplicacion/backend/tests/test_recommendations.py` | 19 pruebas matemáticas, Top-k, null-safety | L31-424 | [L31-L424](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_recommendations.py#L31-L424) |
| **F-21** | Pruebas Backend Simulación | Código Backend (Tests) | `aplicacion/backend/tests/test_simulation.py` | 5 pruebas de casos frontera, determinismo | L9-82 | [L9-L82](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_simulation.py#L9-L82) |
| **F-22** | Vista de Publicación React | Código Frontend (UI) | `aplicacion/frontend/src/components/OfferPublishView.tsx` | Formulario reactivo, aforos inmutables, avisos | L119-1186 | [L119-L1186](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/OfferPublishView.tsx#L119-L1186) |
| **F-23** | Servicio de Ofertas Frontend | Código Frontend (Lógica) | `aplicacion/frontend/src/services/offerService.ts` | Validaciones RN-04/05, mock y cliente API | L22-61, L80-180, L335-387 | [L80-L387](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/services/offerService.ts#L80-L387) |
| **F-24** | Orquestador SPA Principal | Código Frontend (UI) | `aplicacion/frontend/src/App.tsx` | Pestaña `🏷️ Publicar Ofertas`, integración | L15-60, L220-260, L340-365 | [L220-L365](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/App.tsx#L220-L365) |
| **F-25** | Pruebas de Vista de Ofertas | Código Frontend (Tests) | `aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx` | 7 pruebas interactivas en React Testing Library | L82-259 | [L82-L259](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx#L82-L259) |
| **F-26** | Pruebas de Servicio Ofertas | Código Frontend (Tests) | `aplicacion/frontend/src/services/__tests__/offerService.test.ts` | 14 pruebas de cálculo temporal, aforos y mock | L12-277 | [L12-L277](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/services/__tests__/offerService.test.ts#L12-L277) |
| **F-27** | Acervo de Capturas y Diagramas | Recursos Visuales | `docs/diseño/imagenes/sprint-03/` | 7 capturas de pantalla PNG y 1 diagrama vectorial | Archivos físicos >100KB | [Ver Directorio](https://github.com/JMedina255/sistema_web_p2p/tree/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/imagenes/sprint-03) |

---

## C. Auditoría y Profundización en Discrepancias Técnicas

### 1. Planificación Original frente al Trabajo Ejecutado y Colisión de IDs (T-18)
* **Planificación Original (`docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` L49, L158-163):**
  * El Sprint 3 contemplaba formalmente 5 horas-persona de esfuerzo:
    * `T-14`: Desarrollar formulario de publicación de ofertas (Joan, 2 h).
    * `T-15`: Implementar API básica de gestión de ofertas (Renzo, 2 h).
    * `T-16`: Crear estructura de datos y relaciones de ofertas (Renzo, 1 h).
* **Ejecución Real Documentada (`docs/sprints/sprint-03.md` L33-44):**
  * El sprint consumió 11 horas-persona (Joan 2 h, Renzo 9 h) debido a una **ampliación sustancial del alcance técnico**:
    1. Se adelantó el desarrollo integral del motor inteligente de recomendación *EdRecSys v1.0* (`T-15` ampliada a 4 h).
    2. Se formalizó la entidad relacional `sesiones_mentoria`, su migración Alembic 003 y endpoints REST tipados Pydantic v2 (`T-16` ampliada a 3 h).
    3. Se implementó un banco de evaluación algorítmica con 4 casos frontera, prueba de determinismo y benchmark de latencia denominado `T-18` (Renzo, 2 h).
* **Colisión Crítica de Identificadores de Tarea (`T-18`):**
  * En `PLAN_SPRINTS_Y_TAREAS.md` (L180), el identificador `T-18` fue originalmente asignado a Joan para el **Sprint 4**: *«Integrar perfiles y ofertas con API Top-k (Joan, 2 h)»*.
  * En los informes de cierre del Sprint 3 (`G03_EPIS_Informe_Sprint_03.md` y `sprint-03.md`), el identificador `T-18` fue reutilizado por Renzo para el *«Servicio de simulación y testbench algorítmico»*.
  * **Dictamen de Auditoría:** No debe declararse que el incremento ejecutó el 100% de la planificación sin explicar esta desviación. Se produjo una ampliación de alcance de +6 horas (+120% respecto a las 5 h base) y existe una colisión de nomenclatura en `T-18` que debe transparentarse en la Diapositiva 02.

---

### 2. Conformidad de Requisitos: RF06 y Regla RN-11 frente a EdRecSys v1.0

A continuación, se contrasta la especificación canónica del SRS frente a la lógica implementada en `recommendation_service.py`:

### Cuadro C.1: Matriz de Conformidad Técnica — RF06 y RN-11

| Comportamiento Requerido por SRS (FD03) | Comportamiento Implementado (`recommendation_service.py`) | Estado de Conformidad Técnica |
| :--- | :--- | :---: |
| **Similitud Temática Silábica:** El SRS exige similitud coseno sobre espacios vectoriales de competencias (`RF06` L512, `RN-11` L559). | Calcula coeficientes discretos de **Jaccard** $J(T_m, T_k)$ ([L128-L135](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L128-L135)) y **Dice** $D(T_m, T_k)$ ([L138-L143](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L138-L143)) sobre los conjuntos de IDs de temas conceptuales. Ponderación: 40% del puntaje base. | **Parcialmente Conforme (Desviación Matemática Justificada):** Jaccard es equivalente y óptimo para conjuntos finitos silábicos sin embeddings continuos, reduciendo latencia. |
| **Compatibilidad Horaria:** El SRS exige evaluar coincidencia semanal de horarios (`RF06`). | Evalúa solapamiento sobre la matriz semanal 6×11 (66 franjas) $S_{\text{horario}} = \frac{\|H_m \cap H_k\|}{\|H_m\|}$ ([L218-L255](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L218-L255)). Ponderación: 35% del puntaje base. | **Conforme ✅** |
| **Modalidad Pedagógica:** El SRS contempla modalidades presencial y virtual (`RF08`). | Matriz de compatibilidad: 1.0 (idéntica), 0.9 (híbrida), 0.2 (opuesta presencial/virtual) ([L146-L156](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L146-L156)). Ponderación: 15% del puntaje base. | **Conforme ✅** |
| **Filtrado por Reputación y Carga Activa:** El SRS exige reordenar mediante filtrado colaborativo ponderado por reputación histórica y carga activa (`RF06` L512, `RN-11` L559). | No implementado en Sprint 3: Las encuestas de reputación pertenecen al Sprint 7 (`RF18`) y las bitácoras al Sprint 6 (`RF17`). El recomendador utiliza afinidad curricular base (10%) y mérito formativo (`ciclo_actual`). | **Pendiente por Dependencia Temporal ⏳** (Planificado para S4 y S8). |
| **Multiplicadores de Materias Filtro:** El SRS no define multiplicadores fijos en RN-11; la regla RN-11 establece prioridad cualitativa institucional y la especificación de CUS12 / RF24 define una bonificación algorítmica $\alpha$. | Aplica una constante fija `CRITICAL_COURSE_WEIGHTS` ([L18-L24](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L18-L24)): Algoritmos 1.3x, Cálculo I/II y POO 1.2x, BD 1.1x. | **Discrepancia de Atribución Normativa:** Los multiplicadores son una heurística de dominio de la EPIS, no un mandato textual de RN-11. |
| **Criterios de Desempate:** RN-11 exige desempatar por: 1) mayor reputación, 2) menor carga activa, y 3) prioridad institucional (`RN-11` L559). | Desempata mediante la tupla multiclave determinista: `(-total_score, -multiplier, -ciclo_actual, -matching_slots, email)` ([L464-L470](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L464-L470)). | **Parcialmente Conforme (Proxy Provisional):** Ante la falta de encuestas históricas en S3, utiliza ciclo académico y coincidencia de agenda como proxies deterministas. |

---

### 3. Validación del Rol de Mentor en `OfferService.validate_mentor_eligibility()`
* **Regla RN-03 del SRS (FD03 L547):** *«Solo podrán postular y ser admitidos como mentores aquellos estudiantes de la EPIS que pertenezcan a los ciclos académicos VII, VIII, IX o X... y cuenten con rol habilitado por la coordinación.»* Exige **conjunción simultánea** ($\text{rol} = \text{'mentor'} \land \text{ciclo} \ge 7$).
* **Implementación Real en `offer_service.py` ([L135-L181](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/offer_service.py#L135-L181)):**
  ```python
  # Líneas 149-151: Verificación en Base de Datos
  perfil = db.query(PerfilAcademico).filter(PerfilAcademico.email == clean_email).first()
  if rol_mentor or (perfil and perfil.ciclo_actual >= 7):
      return  # <-- DISYUNCIÓN (OR): Acepta tener rol O tener ciclo >= 7

  # Líneas 164-167: Verificación en Memoria
  if ciclo >= 7 or rol in ["mentor", "administrador"]:
      return  # <-- DISYUNCIÓN (OR)

  # Líneas 174-176: Whitelist cableada (Bypass)
  if codigo in ["2022073504", "mentor.avanzado", "admin.epis"]:
      return  # <-- Acceso directo por código institucional de desarrollo
  ```
* **Dictamen de Auditoría:** La implementación en código relaja la conjunción estricta de RN-03 al aplicar una **disyunción (`OR`)**: un alumno de ciclo VII sin rol registrado puede publicar, o un usuario con rol de mentor y ciclo inferior a VII sería admitido. Asimismo, existe un bypass para correos de prueba. Esto debe ser aclarado técnicamente en la Diapositiva 08 como una flexibilización controlada para entornos de desarrollo.

---

### 4. Persistencia, Modos de Ejecución e Integración Real vs Mock
* **Modo Predeterminado en Frontend (`offerService.ts` L329):**
  * `let currentServiceMode: 'mock' | 'api' = 'mock';` $\rightarrow$ La interfaz cliente opera **por defecto en modo simulación (Mock)**, persistiendo las ofertas en la clave `p2p_offers_mock_sprint03` del `localStorage`.
* **Comportamiento del Adaptador API (`ApiOfferAdapter` L280-310):**
  * La llamada `fetch(url, { method: 'POST', ... })` en el frontend **NO envía la cabecera `Authorization: Bearer <token>`**. El payload se envía sin credenciales JWT.
* **Protección Efectiva en Backend (`endpoints/offers.py` L20-37):**
  * El endpoint declara `authorization: str | None = Header(None)`. La autenticación **NO es obligatoria a nivel de gateway**: si el cliente omite el token, `caller_email` es `None` y el backend no valida si el emisor suplanta a otro usuario; únicamente valida que el correo en el cuerpo cumpla la elegibilidad de RN-03.
* **Tratamiento de Errores al Persistir en PostgreSQL (`offer_service.py` L260-263):**
  * Si la base de datos Supabase falla, se interrumpe la conexión o se viola una restricción relacional, el bloque `except Exception:` ejecuta `db.rollback()` y silencia el error mediante `pass`, almacenando la oferta en la lista en memoria `_offers_in_memory` y emitiendo HTTP 201 Created sin advertir al cliente de la degradación.
* **Infraestructura Física y Virtual (Aulas y Google Meet):**
  * Las aulas sugeridas provienen de una lista estática en `offerService.ts` (`SUGGESTED_CLASSROOMS`, L88-97: *Lab Cómputo 101, Lab Redes 202, Aula Magna 104*). No hay invocación al parser PDF de horarios (`RF10` / `PB-032`).
  * Los enlaces de Google Meet se generan por interpolación sintética de texto (`https://meet.google.com/upt-[codigo]-[hash]`). No hay integración OAuth viva con Google Workspace API (`PB-034`).

---

### 5. Reconciliación Integral del Inventario de Pruebas y Coberturas
* **Línea Base Heredada y Pruebas de Regresión (Cierre de Sprint 02):**
  * **150 pruebas automatizadas** (84 en Pytest Backend y 66 en Vitest Frontend), acreditadas en commit `3766a08`.
  * **Comportamiento de Regresión:** Las 150 pruebas preexistentes se ejecutan íntegramente en el pipeline de CI/CD con **100% de tasa de éxito**, certificando que los nuevos módulos de ofertas y recomendación de Sprint 03 no introdujeron ninguna rotura ni regresión en autenticación OTP, consentimiento de privacidad, perfiles de usuario ni disponibilidad horaria.
* **Pruebas Efectivamente Añadidas durante el Sprint 03:**
  * **Frontend (21 pruebas nuevas en 2 archivos reales):**
    * `OfferPublishView.test.tsx`: 7 pruebas interactivas de interfaz y aforos ([L82-L247](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx#L82-L247)).
    * `offerService.test.ts`: 14 pruebas unitarias de antelación temporal y cálculo ([L22-L260](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/services/__tests__/offerService.test.ts#L22-L260)).
  * **Backend (38 pruebas nuevas en 3 archivos reales):**
    * `test_offers.py`: 14 pruebas de límites temporales, permisos y persistencia ([L26-L435](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_offers.py#L26-L435)).
    * `test_recommendations.py`: 19 pruebas de formulación matemática y Top-k ([L31-L425](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_recommendations.py#L31-L425)).
    * `test_simulation.py`: 5 pruebas de casos frontera y determinismo algorítmico ([L9-L82](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_simulation.py#L9-L82)).
  * **Total de Pruebas Nuevas:** $21 + 38 = \mathbf{59\text{ pruebas nuevas}}$.
* **Descarte de Archivos Inexistentes en Commit `7df0a88`:**
  * Se auditó formalmente el árbol de archivos en el commit congelado `7df0a88` y se ratifica que **NO EXISTEN** las rutas `RecommendationsView.test.tsx` (frontend) ni `test_recommendation_benchmark.py` (backend). La cobertura interactiva de recomendación en cliente se probó vía contratos en `offerService.test.ts`, y las pruebas de testbench algorítmico y benchmarking de latencia residen íntegramente en `test_simulation.py`.
* **Cronología de Git y Reconciliación Documental de la Cifra Histórica de «47 Pruebas»:**
  * **Comprobación de Commits (`git show` / `git diff`):**
    * En el commit `741256b` (snapshot Sprint 02) ya se encontraban desarrolladas las **21 pruebas de frontend** (`OfferPublishView.test.tsx` [7] y `offerService.test.ts` [14]).
    * En el commit `094c9fb` (*«feat(sprint-03): culminar backend, motor EdRecSys v1.0, testbench...»*) se incorporaron íntegramente las tres suites de backend con sus **38 pruebas** (`test_offers.py` [14], `test_recommendations.py` [19] y `test_simulation.py` [5]).
    * En el commit `fea566c` (*«docs(sprint-03): estandarizar contratos REST...»*) **no se agregaron funciones de prueba nuevas**; únicamente se agregaron cláusulas `engine.dispose()` para limpieza de conexiones y se actualizaron diagramas e informes de diseño.
    * En el commit `7df0a88` no hubo modificaciones sobre pruebas de código.
  * **Naturaleza de la Cifra «47 Pruebas»:** La mención de 47 pruebas en reportes preliminares como `INFORME_GENERAL_SPRINT_03.md` responde a una **cifra documental preliminar** de redacción durante la fase intermedia de pruebas, no a una carencia física de funciones de prueba en el repositorio.
  * **Inventario Real Verificado y Ejecutado:** En la revisión técnica exhaustiva en `7df0a88`, se ejecutan y superan **209 pruebas consolidadas** (122 backend con Pytest y 87 frontend con Vitest), de las cuales **150 corresponden a la suite de regresión** de los Sprints 1 y 2 (100% aprobadas) y **59 corresponden al incremento estricto del Sprint 03** (21 frontend y 38 backend).
* **Métricas de Cobertura Backend Documentadas vs Verificadas:**
  * **91.83%:** Cifra histórica registrada en informes preliminares sobre una corrida inicial de 1,676 sentencias.
  * **92.14% / 92.15%:** Métrica efectivamente comprobada en ejecución automatizada sobre 1,746 sentencias (137 miss) en la versión consolidada `7df0a88`.

---

## D. Reorganización Pedagógica de las 14 Diapositivas (Secuencia SRS / SAD)

A continuación, se define la estructura narrativa y técnica definitiva para la presentación oficial:

```
Secuencia Pedagógica Reorganizada (14 Diapositivas)

[Marco de Trabajo y Planificación]
  ├─ D-01: Portada Institucional y Datos de Auditoría
  └─ D-02: Objetivo del Sprint, Backlog y Comparación de Alcance (Plan vs Real)

[Ingeniería de Requisitos y Análisis: Publicación de Ofertas]
  ├─ D-03: RF08: Publicación de Ofertas — Definición y Criterios del SRS
  ├─ D-04: CUS06: Narrativa Canónica, Actores, Flujo, Alternativas y Excepciones
  └─ D-05: Diagramas de CUS06: Actividades del SRS y Secuencia Técnica del SAD

[Construcción y Verificación de Ofertas: UI y Servidor]
  ├─ D-06: Evidencia Frontend (T-14): Formulario Reactivo y Selección Curricular
  ├─ D-07: Reglas RN-04 y RN-05: Antelación (>24h) y Aforo Inmutable (10/20)
  └─ D-08: Backend de Ofertas (T-16): API REST, Modelo SesionMentoria y Modos Real/Mock

[Ingeniería de Requisitos y Diseño: Motor de Recomendación]
  ├─ D-09: RF06: Especificación del Motor de Recomendación Top-k en el SRS
  ├─ D-10: CUS02: Narrativa Canónica, Flujo de Demanda y Diagrama Conceptual
  └─ D-11: Motor EdRecSys v1.0 (T-15): Algoritmo, Formulación Matemática y Top-k

[Verificación, Calidad y Cierre]
  ├─ D-12: Demostración Funcional: Recorrido Reproducible e Integración Real/Mock
  ├─ D-13: Catálogo Oficial de Pruebas: Homologación Excel CUS06 y CUS02
  └─ D-14: Calidad Consolidada: 209 Pruebas, Cobertura >92%, Testbench y Cierre DoD
```

---

## E. Contenido Aprobable de las 14 Diapositivas

### Diapositiva 01: Portada Institucional y Datos de Auditoría
* **Título:** Sistema Web P2P de Mentorías Académicas — EPIS UPT (Sprint 03)
* **Objetivo:** Presentar formalmente el incremento del Sprint 03, contextualizando la institución, autores y commit auditado.
* **Contenido Visible:**
  * Universidad Privada de Tacna — Facultad de Ingeniería — EPIS.
  * Construcción de Software I — Semestre Académico 2026-II.
  * Docente de Cátedra: Dr. Ricardo Eduardo Valcárcel Alvarado.
  * Equipo Grupo 03: Joan Cristian Medina Quispe & Renzo Antonio Antayhua Mamani.
  * Línea Base Congelada: Commit [`7df0a88`](https://github.com/JMedina255/sistema_web_p2p/commit/7df0a88) (26/10/2026).
* **Explicación del Expositor:** Presentación conjunta (Joan y Renzo). Introducir la plataforma como solución a la reprobación estudiantil y delimitar que la exposición se sustenta en la línea base congelada del commit `7df0a88`.
* **Fuentes SRS/SAD:** `G03_EPIS_Informe_Sprint_03.md` ([L5-L17](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L5-L17)); `README.md` ([L1-L13](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/README.md#L1-L13)).
* **Código Correspondiente:** Metadatos de repositorio Git.
* **Recurso Visual:** Logotipos oficiales EPIS-UPT y plantilla institucional 16:9.
* **Pruebas Relacionadas:** N/A (Auditoría de Control de Versiones).
* **Limitaciones:** Ninguna.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 02: Objetivo del Sprint, Backlog y Comparación de Alcance
* **Título:** Visión del Sprint 03: Alcance Planificado frente a Ejecutado
* **Objetivo:** Demostrar el avance del Product Backlog, justificando la ampliación de esfuerzo y la colisión de IDs en T-18.
* **Contenido Visible:**
  * PBI Comprometido: `PB-009` (Publicar ofertas) + Adelanto de `PB-010` (Motor Top-k).
  * Planificación Base: 5 horas-persona (T-14: 2h, T-15: 2h, T-16: 1h).
  * Ejecución Real: 11 horas-persona (+120% esfuerzo) por incorporación de EdRecSys v1.0 y Testbench.
  * Aclaración Metodológica: T-18 de simulación (Renzo, S3) vs T-18 de integración UI (Joan, S4).
* **Explicación del Expositor:** Presenta Renzo. Explicar que para garantizar la viabilidad de las ofertas se adelantó la construcción del motor algorítmico, detallando el balance de horas.
* **Fuentes SRS/SAD:** `PLAN_SPRINTS_Y_TAREAS.md` ([L49](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/PLAN_SPRINTS_Y_TAREAS.md#L49), [L152-L184](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/PLAN_SPRINTS_Y_TAREAS.md#L152-L184)); `sprint-03.md` ([L33-L44](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L33-L44)).
* **Código Correspondiente:** N/A (Gestión de Proyecto Scrum).
* **Recurso Visual:** Cuadro comparativo de tareas planificadas vs horas reales ejecutadas.
* **Pruebas Relacionadas:** N/A.
* **Limitaciones:** Registrar formalmente la colisión del código T-18 entre S3 y S4.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 03: RF08: Publicación de Ofertas — Definición y Criterios del SRS
* **Título:** Requisito Funcional RF08: Publicación de Ofertas de Mentoría
* **Objetivo:** Exponer la especificación contractual del requerimiento central de ofertas según el estándar IEEE 830 del SRS.
* **Contenido Visible:**
  * Definición SRS: Mentor habilitado programa asesoría grupal en materias aprobadas.
  * Parámetros Obligatorios: Asignatura, unidad temática silábica, fecha/hora, modalidad pedagógica.
  * Reglas Vinculadas: Mérito `RN-03` ($\text{ciclo} \ge 7$), Antelación obligatoria `RN-04` ($>24\text{ h}$), Aforo `RN-05` (10/20).
  * Dependencia: Requisito `RF09` para asignación de espacios físicos (aulas EPIS) o virtuales (Meet).
* **Explicación del Expositor:** Presenta Joan. Analizar cómo el SRS concibe la oferta como el evento disparador que abastece el catálogo del sistema.
* **Fuentes SRS/SAD:** `FD03-EPIS-Informe SRS de Proyecto.md` ([L514-L515](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L514-L515), [L547-L553](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L547-L553)).
* **Código Correspondiente:** `schemas/offer.py` (`PublishOfferPayload`, [L6-L53](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/schemas/offer.py#L6-L53)).
* **Recurso Visual:** Ficha formal del requerimiento RF08 extraída del SRS.
* **Pruebas Relacionadas:** `test_offers.py` ([L26-L91](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_offers.py#L26-L91)).
* **Limitaciones:** El aprovisionamiento automatizado RF09 opera con catálogo estático y enlaces sintéticos.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 04: CUS06: Narrativa Canónica, Actores, Flujo, Alternativas y Excepciones
* **Título:** Caso de Uso Canónico CUS06: Publicar Oferta de Mentoría
* **Objetivo:** Desglosar la narrativa oficial de 4 tablas normada en la Regla 6 de documentación del proyecto.
* **Contenido Visible:**
  * Actor Principal: Mentor Académico (Ciclos VII al X).
  * Flujo Principal: Selección curricular $\rightarrow$ Validación temporal $\rightarrow$ Aforo automático $\rightarrow$ Asignación de espacio $\rightarrow$ Código `SES-XXXX`.
  * Flujos Alternativos: FA01 (Atención de demanda de CUS03), FA02 (Aula alternativa ante ocupación).
  * Excepciones: E01 (Infracción de antelación RN-04), E02 (Cruce de horario), E03 (Fallo en teleconferencia).
* **Explicación del Expositor:** Presenta Joan. Repasar los 6 pasos del flujo principal y detallar cómo las excepciones E01 y E02 están blindadas por software.
* **Fuentes SRS/SAD:** `FD03-EPIS-Informe SRS de Proyecto.md` ([L1742-L1784](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1742-L1784)).
* **Código Correspondiente:** `OfferPublishView.tsx` ([L266-L300](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/OfferPublishView.tsx#L266-L300)); `offer_service.py` ([L184-L297](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/offer_service.py#L184-L297)).
* **Recurso Visual:** Estructura canónica de 4 tablas de la narrativa CUS06.
* **Pruebas Relacionadas:** Catálogo Excel Fila 41-48 (`CUS06-U01` a `CUS06-A01`).
* **Limitaciones:** FA01 requiere la existencia previa de demandas en base de datos.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 05: Diagramas de CUS06: Flujo de Actividades y Secuencia Técnica del SAD
* **Título:** Modelado Visual de CUS06: Actividades y Secuencia Técnica Multicapa
* **Objetivo:** Exponer la dinámica de ejecución técnica entre las capas de presentación, API, dominio y persistencia.
* **Contenido Visible:**
  * Diagrama de Secuencia SAD (15 pasos): `OfferPublishView` $\rightarrow$ `offerService` $\rightarrow$ `Router` $\rightarrow$ `OfferService` $\rightarrow$ `PostgreSQL`.
  * Verificación en dos niveles: validación reactiva en cliente y transacción ACID con rollback en servidor.
  * Emisión de identificador unívoco institucional `SES-XXXX` y retorno HTTP 201 Created.
* **Explicación del Expositor:** Presenta Renzo. Demostrar cómo se orquestan las llamadas asíncronas y el control de excepciones entre frontend y backend.
* **Fuentes SRS/SAD:** `FD04-EPIS-Informe SAD de Proyecto.md` ([L798-L804](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md#L798-L804)); `TRAZABILIDAD_PUBLICACION_OFERTAS.md` ([L72-L128](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/TRAZABILIDAD_PUBLICACION_OFERTAS.md#L72-L128)).
* **Código Correspondiente:** Integración `apiClient.ts` con `endpoints/offers.py`.
* **Recurso Visual:** Diagrama vectorial oficial `08_secuencia_tecnica_publicacion_ofertas.png` / `.svg`.
* **Pruebas Relacionadas:** `OfferPublishView.test.tsx` ([L183-L232](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx#L183-L232)).
* **Limitaciones:** El diagrama SAD incluye Bearer JWT, el cual está pendiente de adjuntarse en el cliente HTTP del frontend.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 06: Evidencia Frontend (T-14): Formulario Reactivo y Selección Curricular
* **Título:** Capa de Cliente: Formulario Reactivo y Navegación Curricular (T-14)
* **Objetivo:** Demostrar la experiencia de usuario desarrollada por Joan bajo estándares de accesibilidad institucional.
* **Contenido Visible:**
  * Selector curricular dinámico: consulta de 5 asignaturas críticas (`Cálculo I/II, Algoritmos, POO, BD`).
  * Carga bajo demanda de unidades silábicas oficiales (`fetchCourseDetail`).
  * Prevención de duplicados con bandera `isSubmitting` y modo dual visible (Mock/API).
  * Cumplimiento estricto de colores institucionales EPIS (`#1C2A59` y `#B99451`).
* **Explicación del Expositor:** Presenta Joan. Mostrar la captura de pantalla real del sistema operando localmente, evidenciando los estados de carga y confirmación.
* **Fuentes SRS/SAD:** `G03_EPIS_Informe_Sprint_03.md` ([L50-L79](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L50-L79)).
* **Código Correspondiente:** `OfferPublishView.tsx` ([L119-L200](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/OfferPublishView.tsx#L119-L200), [L370-L460](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/OfferPublishView.tsx#L370-L460)).
* **Recurso Visual:** Captura auténtica `01_offer_publish_form.png`.
* **Pruebas Relacionadas:** `OfferPublishView.test.tsx` ([L82-L98](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx#L82-L98)).
* **Limitaciones:** Opera por defecto con adaptador Mock para garantizar la interacción fluida sin requerir backend encendido.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 07: Reglas RN-04 y RN-05: Antelación (>24h) y Aforo Inmutable (10/20)
* **Título:** Reglas de Negocio en Acción: Validación RN-04 y Aforo Inmutable RN-05
* **Objetivo:** Probar el cumplimiento riguroso de las reglas de antelación temporal y control de cupos normativos.
* **Contenido Visible:**
  * Regla RN-04: Bloqueo perentorio con alerta roja si $T \le 24\text{ h}$; distintivo verde si $T \ge 48\text{ h}$.
  * Justificación de RN-04: Protege la ventana de confirmación previa y corte de quórum a $T-24\text{ h}$ (RN-08/RN-09).
  * Regla RN-05: Input de aforo estrictamente `readOnly`: exactamente 10 para Presencial y 20 para Virtual.
* **Explicación del Expositor:** Presenta Joan. Explicar que la antelación mayor a 24 horas es un candado indispensable para evitar que se publiquen ofertas que nazcan con el quórum vencido.
* **Fuentes SRS/SAD:** `FD03-EPIS-Informe SRS de Proyecto.md` ([L550-L551](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L550-L551), [L1763](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1763), [L1779](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1779)).
* **Código Correspondiente:** `offerService.ts` ([L80-L86](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/services/offerService.ts#L80-L86), [L107-L117](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/services/offerService.ts#L107-L117)); `OfferPublishView.tsx` ([L480-L530](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/OfferPublishView.tsx#L480-L530)).
* **Recurso Visual:** Capturas auténticas `02_advance_time_validation_rn04.png` y `03_capacity_control_rn05.png`.
* **Pruebas Relacionadas:** `offerService.test.ts` ([L71-L183](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/services/__tests__/offerService.test.ts#L71-L183)); `test_offers.py` ([L94-L121](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_offers.py#L94-L121), [L153-L178](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_offers.py#L153-L178)).
* **Limitaciones:** Ninguna. Ambas reglas se validan de forma isomórfica en cliente y servidor.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 08: Backend de Ofertas (T-16): API REST, Modelo SesionMentoria y Modos Real/Mock
* **Título:** Persistencia Relacional y Arquitectura Backend de Ofertas (T-16)
* **Objetivo:** Sustentar el diseño físico en PostgreSQL, los endpoints REST y la política de degradación controlada.
* **Contenido Visible:**
  * Entidad `sesiones_mentoria`: clave primaria `id_sesion`, `codigo_sesion` canónico, foráneas a asignaturas y temas.
  * Restricciones `CHECK`: aforo en (10, 20), modalidad en ('presencial', 'virtual'), duración en (60, 90).
  * Migración Alembic `003_mentoring_offers.py`: 5 índices B-Tree para optimización de consultas.
  * Análisis de Integración: Fallback en memoria ante contingencias de red y validación de mérito `RN-03`.
* **Explicación del Expositor:** Presenta Renzo. Detallar el esquema relacional, los índices creados y transparentar que `validate_mentor_eligibility()` implementa una disyunción para facilitar pruebas.
* **Fuentes SRS/SAD:** `INFORME_GENERAL_SPRINT_03.md` ([L220-L275](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/INFORME_GENERAL_SPRINT_03.md#L220-L275)); `sprint-03.md` ([L212-L259](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L212-L259)).
* **Código Correspondiente:** `models/offer.py` ([L9-L65](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/models/offer.py#L9-L65)); `offer_service.py` ([L135-L181](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/offer_service.py#L135-L181), [L240-L265](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/offer_service.py#L240-L265)).
* **Recurso Visual:** Especificación DDL física de la tabla `sesiones_mentoria` y diagrama de entidades.
* **Pruebas Relacionadas:** `test_offers.py` (`test_offer_service_with_real_db_session`, [L274-L331](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_offers.py#L274-L331)).
* **Limitaciones:** En caso de caída de Supabase, la API almacena en memoria volátil de forma transparente.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 09: RF06: Especificación del Motor de Recomendación Top-k en el SRS
* **Título:** Requisito Funcional RF06: Recomendación Personalizada Top-k
* **Objetivo:** Exponer la especificación teórica del algoritmo de recomendación según el modelo analítico del SRS.
* **Contenido Visible:**
  * Definición SRS: Emparejamiento por afinidad conceptual, disponibilidad horaria compartida y balance de carga.
  * Meta Cualitativa: Conectar a alumnos vulnerables (Ciclos I al IV) con mentores de excelencia (Ciclos VII al X).
  * Parámetros de Inferencia: Necesidades silábicas, agenda semanal de 66 franjas, modalidad y asignaturas críticas.
  * Latencia Exigida por RNF03: Cálculo y entrega de la lista Top-k en menos de 50 ms.
* **Explicación del Expositor:** Presenta Renzo. Contrastar la necesidad pedagógica institucional con la formulación analítica de emparejamiento.
* **Fuentes SRS/SAD:** `FD03-EPIS-Informe SRS de Proyecto.md` ([L512](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L512), [L586](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L586)); `FD04` ([L648](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md#L648)).
* **Código Correspondiente:** `schemas/recommendation.py` (`RecommendationListResponse`, [L92-L102](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/schemas/recommendation.py#L92-L102)).
* **Recurso Visual:** Diagrama conceptual C4 de recomendación del SAD.
* **Pruebas Relacionadas:** `test_recommendations.py` ([L98-L126](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_recommendations.py#L98-L126)).
* **Limitaciones:** El filtrado por reputación histórica y carga activa está planificado para sprints posteriores.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 10: CUS02: Narrativa Canónica, Flujo de Demanda y Diagrama Conceptual
* **Título:** Caso de Uso Canónico CUS02: Consultar Recomendaciones Top-k
* **Objetivo:** Explicar el flujo del mentoreado al explorar el feed de recomendaciones personalizadas.
* **Contenido Visible:**
  * Actor Principal: Estudiante Mentoreado (Ciclos I a IV). Actor Secundario: EdRecSys v1.0.
  * Flujo Principal: Acceso al panel $\rightarrow$ Extracción de perfil y matriz semanal $\rightarrow$ Inferencia $\rightarrow$ Tarjetas Top-5 con % de afinidad.
  * Flujos Alternativos: FA01 (Filtro por materia crítica), FA02 (Sin coincidencia $\rightarrow$ Sugiere solicitud por demanda CUS03).
  * Excepciones: E01 (Matriz horaria no configurada $\rightarrow$ Redirige a CUS15), E02 (Latencia excesiva $\rightarrow$ Fallback).
* **Explicación del Expositor:** Presenta Renzo. Destacar la articulación entre CUS02 y CUS03 cuando no existe oferta compatible.
* **Fuentes SRS/SAD:** `FD03-EPIS-Informe SRS de Proyecto.md` ([L1610-L1648](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1610-L1648)); `FD04` ([L180-L194](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md#L180-L194)).
* **Código Correspondiente:** `endpoints/recommendations.py` (`get_recommended_offers`, [L59-L83](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/api/v1/endpoints/recommendations.py#L59-L83)).
* **Recurso Visual:** Diagrama de Casos de Uso del subsistema MOD-03 en el SAD.
* **Pruebas Relacionadas:** Catálogo Excel Fila 14-21 (`CUS02-U01` a `CUS02-A01`).
* **Limitaciones:** En S3 el consumo se verifica a nivel de API REST; la interfaz visual del feed se acopla en S4.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 11: Motor EdRecSys v1.0 (T-15): Algoritmo, Formulación Matemática y Top-k
* **Título:** Motor EdRecSys v1.0: Formulación Matemática y Desempate Determinista
* **Objetivo:** Sustentar el núcleo matemático del algoritmo, demostrando su transparencia y reproducibilidad.
* **Contenido Visible:**
  * Ecuación Compuesta: $S_{\text{base}} = 0.40 \cdot S_{\text{tema}} + 0.35 \cdot S_{\text{horario}} + 0.15 \cdot S_{\text{modalidad}} + 0.10 \cdot S_{\text{afinidad}}$.
  * Similitud Temática: Jaccard $J = \frac{|T_m \cap T_k|}{|T_m \cup T_k|}$ y Dice $D = \frac{2|T_m \cap T_k|}{|T_m| + |T_k|}$.
  * Ponderador Curricular Filtro: Algoritmos ($1.3\text{x}$), Cálculo I/II y POO ($1.2\text{x}$), BD ($1.1\text{x}$).
  * Tupla de Desempate: `(-total_score, -multiplier, -ciclo_actual, -matching_slots, email)`.
  * Explicabilidad: Endpoint `/recommendations/explain` con desglose auditable de puntajes.
* **Explicación del Expositor:** Presenta Renzo. Explicar cómo el algoritmo evita cajas negras y permite auditar por qué un mentor o sesión ocupa el primer lugar.
* **Fuentes SRS/SAD:** `G03_EPIS_Informe_Sprint_03.md` ([L280-L345](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L280-L345)); `sprint-03.md` ([L142-L180](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L142-L180)).
* **Código Correspondiente:** `recommendation_service.py` ([L128-L156](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L128-L156), [L177-L335](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L177-L335), [L464-L470](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L464-L470)).
* **Recurso Visual:** Fórmulas matemáticas en KaTeX y diagrama de desglose de explicabilidad.
* **Pruebas Relacionadas:** `test_recommendations.py` ([L31-L95](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_recommendations.py#L31-L95), [L155-L185](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_recommendations.py#L155-L185)).
* **Limitaciones:** La ponderación de materias críticas es un ajuste empírico de dominio, no una regla cuantitativa de RN-11.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 12: Demostración Funcional: Recorrido Reproducible e Integración Real/Mock
* **Título:** Demostración Funcional: Guía de Reproducción y Verificación
* **Objetivo:** Explicar el recorrido demostrativo para evaluar la aplicación en vivo distinguiendo componentes reales y mocks.
* **Contenido Visible:**
  * Paso 1: Ingreso a `🏷️ Publicar Ofertas` en React SPA (`http://localhost:5173`).
  * Paso 2: Selección de asignatura filtro (*Algoritmos y Estructuras de Datos*) y tema silábico oficial.
  * Paso 3: Comprobación reactiva de RN-04: forzar fecha a $T < 24\text{ h}$ (bloqueo rojo); corregir a $T > 48\text{ h}$ (badge verde).
  * Paso 4: Alternancia de modalidad y verificación de aforo inmutable RN-05 (10 presencial / 20 virtual).
  * Paso 5: Publicación y confirmación inmediata con código `SES-XXXX`.
  * Paso 6: Verificación en backend vía Swagger UI (`/docs`) y ejecución de `/testbench`.
* **Explicación del Expositor:** Presenta Joan (con apoyo de Renzo en API). Guiar al evaluador a través de los pasos concretos de la demostración.
* **Fuentes SRS/SAD:** `README.md` ([L204-L263](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/README.md#L204-L263)); `sprint-03.md` ([L48-L80](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L48-L80)).
* **Código Correspondiente:** `App.tsx` ([L340-L365](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/App.tsx#L340-L365)); `OfferPublishView.tsx`.
* **Recurso Visual:** Capturas `01_offer_publish_form.png` y `04_swagger_api_docs_sprint03.png`.
* **Pruebas Relacionadas:** `App.test.tsx` ([L5-L50](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/__tests__/App.test.tsx#L5-L50)).
* **Limitaciones:** En la interfaz SPA el envío utiliza el adaptador mock con bandera visible para independencia de despliegue.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 13: Catálogo Oficial de Pruebas: Homologación Excel CUS06 y CUS02
* **Título:** Homologación con el Catálogo de Pruebas Institucional (Excel)
* **Objetivo:** Acreditar que el desarrollo satisface formalmente los casos de prueba definidos en la fase de análisis.
* **Contenido Visible:**
  * Casos CUS06: `CUS06-U01` (campos obligatorios), `CUS06-U02` (aforos RN-05), `CUS06-F01` (flujo presencial), `CUS06-F02` (antelación RN-04).
  * Casos CUS02: `CUS02-U01..U04` (similitud matemática y desempate), `CUS02-U05` (endpoint `/recommend`), `CUS02-A01` (rendimiento RNF03).
  * Resultado Empírico: 100% de los casos implementados superados con aserciones automatizadas en Pytest y Vitest.
* **Explicación del Expositor:** Presenta Joan (CUS06) y Renzo (CUS02). Demostrar la trazabilidad directa entre las celdas del Excel y los métodos de prueba en código.
* **Fuentes SRS/SAD:** `Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` (A14:O21, A41:O48); `sprint-03.md` ([L82-L100](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L82-L100), [L183-L200](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L183-L200)).
* **Código Correspondiente:** Suites `test_offers.py`, `test_recommendations.py`, `OfferPublishView.test.tsx` y `offerService.test.ts`.
* **Recurso Visual:** Matriz de trazabilidad Excel Cuadro 3.1 y Cuadro 5.1 del informe de sprint.
* **Pruebas Relacionadas:** 59 pruebas automatizadas del incremento de Sprint 3.
* **Limitaciones:** Casos `CUS06-U03` (parser horarios) y `CUS06-U04` (OAuth Meet) están pendientes de integración con servicios externos reales.
* **Estado de Preparación:** Lista ✅.

---

### Diapositiva 14: Calidad Consolidada: 209 Pruebas, Cobertura >92%, Testbench y Cierre DoD
* **Título:** Aseguramiento de Calidad, Testbench Algorítmico y Cierre del DoD
* **Objetivo:** Respaldar con métricas objetivas la madurez del software y formalizar la transición hacia el Sprint 04.
* **Contenido Visible:**
  * Batería Automatizada: 209 pruebas aprobadas (122 backend / 87 frontend) en 26 suites sin fallos.
  * Clasificación Rigurosa: 150 pruebas de regresión verificadas (Línea Base S1-S2) + 59 pruebas nuevas del Sprint 03.
  * Desglose Real S3: 21 en Frontend (`OfferPublishView.test.tsx`: 7, `offerService.test.ts`: 14) y 38 en Backend (`test_offers.py`: 14, `test_recommendations.py`: 19, `test_simulation.py`: 5).
  * Aclaración de Rutas: En `7df0a88` no existen `RecommendationsView.test.tsx` ni `test_recommendation_benchmark.py` (el testbench reside en `test_simulation.py`).
  * Cobertura Independiente (RNF09): 92.52% en Frontend (Vitest) y 92.14% en Backend (Pytest).
  * Linteo y Formato: 0 errores ESLint 9, 0 defectos Ruff 0.9, 62 archivos formateados conformes.
  * Testbench T-18: 4 casos frontera superados, 100% determinismo y latencia media de $35.8\text{ µs}$ ($0.86\text{ ms}$ total).
  * Cierre DoD y Entrada a Sprint 04: Catálogo y motor listos para las reservas transaccionales ACID (`RF12` / `CUS04`).
* **Explicación del Expositor:** Presentación conjunta (Joan y Renzo). Concluir con la certificación de calidad y declarar el Sprint 03 formalmente culminado y aprobado.
* **Fuentes SRS/SAD:** `G03_EPIS_Informe_Sprint_03.md` ([L109-L125](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L109-L125), [L363-L389](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L363-L389)).
* **Código Correspondiente:** Las 5 suites reales: `test_offers.py` (L26-L435), `test_recommendations.py` (L31-L425), `test_simulation.py` (L9-L82), `OfferPublishView.test.tsx` (L82-L247) y `offerService.test.ts` (L22-L260); reportes `coverage.xml`.
* **Recurso Visual:** Capturas `05_backend_pytest_coverage_sprint03.png`, `06_frontend_vitest_coverage_sprint03.png` y `07_algorithmic_testbench_cases.png`.
* **Pruebas Relacionadas:** 209 pruebas en ejecución simultánea.
* **Limitaciones:** La cobertura backend documentada preliminarmente (91.83% sobre 1,676 sentencias) se perfeccionó a 92.14% (92.15% en terminal sobre 1,746 sentencias) en la corrida consolidada de auditoría.
* **Estado de Preparación:** Lista ✅.

---

## F. Catálogo de Recursos Visuales Auditados

### Cuadro F.1: Inventario Oficial de Capturas y Diagramas del Sprint 03

| N.° | Archivo Gráfico | Ruta Física en Repositorio | Tamaño (Bytes) | Funcionalidad o Pantalla que Acredita | Componente Responsable | Requerimiento / Regla | Nivel de Madurez |
| :---: | :--- | :--- | :---: | :--- | :--- | :---: | :---: |
| **V-01** | `01_offer_publish_form.png` | `docs/diseño/imagenes/sprint-03/01_offer_publish_form.png` | 161,192 | Formulario accesible de publicación con carga reactiva de temas silábicos del catálogo oficial EPIS. | `OfferPublishView.tsx` | RF08, CUS06, RF05 | **Real (UI Integrada)** con fallback a catálogo semilla |
| **V-02** | `02_advance_time_validation_rn04.png` | `docs/diseño/imagenes/sprint-03/02_advance_time_validation_rn04.png` | 117,877 | Validación reactiva de antelación temporal: banner rojo de bloqueo ($T \le 24\text{ h}$) y badge verde ($T \ge 48\text{ h}$). | `OfferPublishView.tsx` y `offerService.ts` | RN-04, RF08 | **Real (Validación Activa)** en cliente y servidor |
| **V-03** | `03_capacity_control_rn05.png` | `docs/diseño/imagenes/sprint-03/03_capacity_control_rn05.png` | 136,431 | Control inmutable de aforo: alternancia reactiva a 10 cupos en presencial y 20 en virtual en campo `readOnly`. | `OfferPublishView.tsx` | RN-05, RF08 | **Real (Norma Inmutable)** |
| **V-04** | `04_swagger_api_docs_sprint03.png` | `docs/diseño/imagenes/sprint-03/04_swagger_api_docs_sprint03.png` | 166,411 | Documentación OpenAPI/Swagger en `/docs` con endpoints `/api/v1/offers` y `/api/v1/recommendations/*`. | `main.py`, routers de FastAPI | RNF08, RF06, RF08 | **Real (API Operativa)** |
| **V-05** | `05_backend_pytest_coverage_sprint03.png` | `docs/diseño/imagenes/sprint-03/05_backend_pytest_coverage_sprint03.png` | 128,489 | Reporte de terminal de `pytest --cov=app`: 122 pruebas aprobadas y 92.14% de cobertura de código. | `tests/` backend | RNF09 | **Real (Acreditación CI)** |
| **V-06** | `06_frontend_vitest_coverage_sprint03.png` | `docs/diseño/imagenes/sprint-03/06_frontend_vitest_coverage_sprint03.png` | 131,214 | Reporte de terminal de `vitest --coverage`: 87 pruebas aprobadas y 92.52% de cobertura de código. | `src/**/__tests__/` | RNF09 | **Real (Acreditación CI)** |
| **V-07** | `07_algorithmic_testbench_cases.png` | `docs/diseño/imagenes/sprint-03/07_algorithmic_testbench_cases.png` | 122,200 | Salida JSON del testbench en navegador (`/testbench`): 4 casos frontera conformes y latencia de $35.8\text{ µs}$. | `SimulationService` | RF06, RNF03, PB-027 | **Real (Testbench Activo)** |
| **V-08** | `08_secuencia_tecnica_publicacion_ofertas.png` / `.svg` | `docs/diseño/imagenes/sprint-03/08_secuencia_tecnica_publicacion_ofertas.png` | 69,818 (PNG) / 24,687 (SVG) | Diagrama de secuencia técnica multicapa entre React, FastAPI, Dominio y PostgreSQL (PlantUML canónico). | PlantUML en `TRAZABILIDAD_PUBLICACION_OFERTAS.md` | SAD Escenarios 2.3 | **Diseño Verificado** frente al código implementado |

---

## G. Registro Consolidado de Inconsistencias y Advertencias para el Expositor

### Cuadro G.1: Registro de Inconsistencias Técnicas y Mitigaciones en Exposición

| N.° | Hallazgo / Discrepancia Identificada | Fuente de Origen | Código / Estado Real Comprobable | Clasificación Técnica | Recomendación Obligatoria al Expositor |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **INC-01** | **Rutas relativas ficticias en documento de trazabilidad:** La tabla 3 de `TRAZABILIDAD_PUBLICACION_OFERTAS.md` cita `src/features/offers/OfferPublishView.tsx` y `offerValidation.ts`. | `TRAZABILIDAD_PUBLICACION_OFERTAS.md` L139-140 | En el repositorio físico residen en `aplicacion/frontend/src/components/OfferPublishView.tsx` y `aplicacion/frontend/src/services/offerService.ts`. | **Discrepancia Documental** | Citar exclusivamente las rutas físicas reales de `src/components/` y `src/services/` durante la defensa técnica. |
| **INC-02** | **Nombres de autores erróneos en `INF-TRZ-01`:** El encabezado coloca "Joan Manuel Medina Medina" y "Renzo Anthony Valles Ramos". | `TRAZABILIDAD_PUBLICACION_OFERTAS.md` L7 | Los integrantes oficiales son Joan Cristian Medina Quispe (2022074255) y Renzo Antonio Antayhua Mamani (2022073504). | **Discrepancia de Metadatos** | Aclarar que fue una errata tipográfica en plantilla auxiliar; los informes canónicos contienen los nombres correctos. |
| **INC-03** | **Alcance diferido de parser de aulas y Google Workspace OAuth:** El catálogo cita `ServicioAnalizadorHorarios` y aprovisionamiento dinámico de Meet. | Excel Fila 43-44; SRS `RF09` | El parser PDF (`PB-032`) y la API OAuth de Meet (`PB-034`) son "Posterior" en Scrum. Se opera con catálogo curado de laboratorios y enlaces deterministas `@upt.pe`. | **Parcialmente Conforme (Alcance Planificado)** | Transparentar con total claridad que la integración desatendida OAuth es una ampliación posterior del Product Backlog. |
| **INC-04** | **Motor EdRecSys en Python puro (sin NumPy ni Scikit-learn):** El SRS y SAD sugerían dependencias externas de Machine Learning. | `FD03` L512; `FD04` L1165 | Se implementó en Python 3.13 puro con estructuras nativas, logrando latencia de $35.8\text{ µs}$ y eliminando dependencias pesadas. | **Optimización Conforme** | Presentar como un logro de ingeniería de eficiencia y portabilidad en el contenedor de backend. |
| **INC-05** | **Colisión de identificador T-18:** T-18 estaba asignada a Joan en S4 (Integración UI), pero se usó para Renzo en S3 (Testbench). | `PLAN_SPRINTS_Y_TAREAS.md` L180 vs `sprint-03.md` L40 | Colisión de nomenclaturas por adelanto de actividades algorítmicas en S3. | **Discrepancia Metodológica** | Explicar en Diapositiva 02 que T-18 en S3 representó una tarea no programada de testbench algorítmico. |
| **INC-06** | **Disyunción en validación de mérito RN-03:** El SRS exige rol mentor Y ciclo $\ge 7$. El código evalúa `rol_mentor OR (ciclo >= 7)`. | `offer_service.py` L150, L166 | La comprobación en código utiliza un operador `OR` y contiene bypass para cuentas semilla. | **Desviación de Implementación** | Explicar en Diapositiva 08 como una flexibilización controlada para viabilizar pruebas locales sin poblar roles completos. |
| **INC-07** | **Modo mock por defecto y ausencia de Bearer token en cliente de ofertas:** `offerService.ts` opera en mock por defecto y su cliente API no adjunta JWT. | `offerService.ts` L284-289, L329; `endpoints/offers.py` L34 | La API de ofertas permite llamadas anónimas si el email es válido; el frontend opera en mock de forma predeterminada. | **Aislamiento de Entorno** | Explicar en Diapositiva 12 que la SPA desacopla la UI mediante adaptador mock para demostraciones locales independientes. |

---

## H. Referencias Directas a GitHub Ancladas al Commit `7df0a88`

### 1. Documentación Canónica y de Diseño
* **SRS FD03 (Diseño v2.1) — Requerimientos RF06/RF08 y Reglas RN-03..RN-11:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L512-L557`
* **SRS FD03 (Diseño v2.1) — Narrativa Canónica CUS02:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1610-L1648`
* **SRS FD03 (Diseño v2.1) — Narrativa Canónica CUS06:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1742-L1784`
* **SAD FD04 (Diseño v2.0) — Módulos MOD-03 y MOD-04:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md#L110-L111`
* **SAD FD04 (Diseño v2.0) — Diagrama de Casos de Uso CUS02 y CUS06:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md#L798-L838`
* **Informe Académico Canónico G03 (Sprint 03) — Formulación Matemática EdRecSys:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L280-L345`
* **Informe Académico Canónico G03 (Sprint 03) — Contratos REST:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L350-L380`
* **Trazabilidad de Ofertas — Código PlantUML de Secuencia Técnica:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/TRAZABILIDAD_PUBLICACION_OFERTAS.md#L72-L128`
* **Plan Maestro de Sprints y Tareas — Asignación Sprint 03:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/PLAN_SPRINTS_Y_TAREAS.md#L152-L184`

### 2. Código Fuente Backend (FastAPI / SQLAlchemy / Alembic)
* **Modelo ORM `SesionMentoria`:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/models/offer.py#L9-L65`
* **Esquemas Pydantic `PublishOfferPayload` y `PublishOfferResponse`:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/schemas/offer.py#L6-L79`
* **Esquemas Pydantic `ScoreBreakdown` y `OfferRecommendationItem`:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/schemas/recommendation.py#L6-L125`
* **Servicio `OfferService` (Validaciones RN-03, RN-04, RN-05 e inserción):**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/offer_service.py#L105-L409`
* **Servicio `RecommendationService` (Motor EdRecSys v1.0 y Top-k):**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L128-L716`
* **Servicio `SimulationService` (Cohortes sintéticas y 4 casos frontera):**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/simulation_service.py#L9-L411`
* **Endpoints REST de Ofertas (`POST` y `GET /api/v1/offers`):**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/api/v1/endpoints/offers.py#L20-L62`
* **Endpoints REST de Recomendaciones (`/mentors`, `/offers`, `/explain`, `/testbench`):**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/api/v1/endpoints/recommendations.py#L27-L125`
* **Migración Alembic `003_mentoring_offers.py`:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/db/migrations/versions/003_mentoring_offers.py#L25-L77`

### 3. Código Fuente Frontend (React 19 / TypeScript / Vitest)
* **Componente React `OfferPublishView.tsx`:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/OfferPublishView.tsx#L119-L1186`
* **Servicio de Cliente `offerService.ts`:**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/services/offerService.ts#L80-L387`
* **Orquestador Principal `App.tsx` (Pestaña Ofertas):**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/App.tsx#L220-L365`

### 4. Pruebas Automatizadas (Pytest y Vitest)
* **Suite Backend de Ofertas (`test_offers.py` — 14 pruebas):**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_offers.py#L26-L449`
* **Suite Backend de Recomendaciones (`test_recommendations.py` — 19 pruebas):**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_recommendations.py#L31-L424`
* **Suite Backend de Simulación (`test_simulation.py` — 5 pruebas):**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_simulation.py#L9-L82`
* **Suite Frontend de Vista de Ofertas (`OfferPublishView.test.tsx` — 7 pruebas):**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx#L82-L259`
* **Suite Frontend de Servicio de Ofertas (`offerService.test.ts` — 14 pruebas):**  
  `https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/services/__tests__/offerService.test.ts#L12-L277`

---

## I. Checklist Final de Validación de Diapositivas

| Diapositiva | Título de la Diapositiva | Fuente Documental | Código Fuente | Recurso Gráfico | Pruebas Automatizadas | Dictamen de Auditoría |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **D-01** | Portada Institucional y Datos de Auditoría | ✅ Completa | ✅ Completa | ✅ Completa | N/A (Auditoría Git) | **Aprobada para Generación** |
| **D-02** | Objetivo del Sprint, Backlog y Comparación | ✅ Completa | ✅ Completa | ✅ Completa | N/A (Gestión Scrum) | **Aprobada para Generación** |
| **D-03** | RF08: Criterios y Especificación del SRS | ✅ Completa | ✅ Completa | ✅ Completa | ✅ Completa | **Aprobada para Generación** |
| **D-04** | CUS06: Narrativa Formal y Excepciones | ✅ Completa | ✅ Completa | ✅ Completa | ✅ Completa | **Aprobada para Generación** |
| **D-05** | Diagramas de CUS06: Actividades y Secuencia | ✅ Completa | ✅ Completa | ✅ Completa | ✅ Completa | **Aprobada para Generación** |
| **D-06** | Evidencia Frontend (T-14): Formulario y Temas | ✅ Completa | ✅ Completa | ✅ Completa | ✅ Completa | **Aprobada para Generación** |
| **D-07** | Reglas RN-04 y RN-05: Antelación y Aforos | ✅ Completa | ✅ Completa | ✅ Completa | ✅ Completa | **Aprobada para Generación** |
| **D-08** | Backend de Ofertas (T-16): DDL y Modos Real/Mock| ✅ Completa | ✅ Completa | ✅ Completa | ✅ Completa | **Aprobada para Generación** |
| **D-09** | RF06: Especificación del Recomendador SRS | ✅ Completa | ✅ Completa | ✅ Completa | ✅ Completa | **Aprobada para Generación** |
| **D-10** | CUS02: Narrativa Canónica y Flujo Demanda | ✅ Completa | ✅ Completa | ✅ Completa | ✅ Completa | **Aprobada para Generación** |
| **D-11** | EdRecSys v1.0 (T-15): Algoritmo y Top-k | ✅ Completa | ✅ Completa | ✅ Completa | ✅ Completa | **Aprobada para Generación** |
| **D-12** | Demostración Funcional: Recorrido y Mocks | ✅ Completa | ✅ Completa | ✅ Completa | ✅ Completa | **Aprobada para Generación** |
| **D-13** | Catálogo de Pruebas: Homologación Excel | ✅ Completa | ✅ Completa | ✅ Completa | ✅ Completa | **Aprobada para Generación** |
| **D-14** | Calidad Consolidada: 209 Tests y Cierre DoD | ✅ Completa | ✅ Completa | ✅ Completa | ✅ Completa | **Aprobada para Generación** |

---
*Escuela Profesional de Ingeniería de Sistemas — Universidad Privada de Tacna — Octubre 2026*
