# Documento de Evidencia y Catálogo de Pruebas Automatizadas: Sprint 3
## "Publicación de Ofertas, Motor EdRecSys v1.0, Persistencia Relacional y Testbench Algorítmico"

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II)  
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Fecha de Cierre:** 26/10/2026  
**Rama Base de Integración:** `main`  
**Estado:** ✅ **209 de 209 Pruebas Superadas (100% Satisfactorio, 0 Fallos, Cobertura >91%)**

---

## Control de Versiones

A continuación, se presenta la tabla de control de versiones del documento de evidencia de pruebas para el Sprint 3:

### Cuadro 0.1: Control de Versiones — Catálogo de Evidencias de Pruebas (Sprint 3)

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcarcel | Dirección EPIS | 26/10/2026 | Emisión formal del catálogo de evidencias de pruebas automatizadas del Sprint 3: consolidación de 209 pruebas (122 en Pytest Backend y 87 en Vitest Frontend), desglose de las 26 suites, matrices de cobertura por archivo/línea (>91% en ambos subsistemas), auditoría de linteo estático (Ruff/ESLint), reporte de compilación, testbench de evaluación algorítmica y comandos reproducibles de verificación. |

Fuente: Elaboración propia.

El control de versiones acredita la auditabilidad, reproducibilidad técnica y trazabilidad de los artefactos de software generados en estricto cumplimiento del marco de calidad del curso.

---

## 1. Propósito y Estrategia de Pruebas del Sprint 3

El presente documento certifica el cumplimiento del requerimiento no funcional **RNF09 (Mantenibilidad y Calidad de Código)**, que establece un umbral mínimo obligatorio del **70.0% de cobertura de código por pruebas automatizadas** en frontend y backend, así como el requerimiento de latencia algorítmica (**RNF03** $< 50\text{ ms}$) y las reglas de negocio institucionales (**RN-03, RN-04, RN-05, RN-06 y RN-07**).

La estrategia de pruebas consolidada para el Sprint 3 articula cinco niveles de verificación técnica:
1. **Pruebas de Componentes React e Interacción de Usuario (T-14 / Vitest):** Renderizado en DOM virtual (`jsdom`) mediante React Testing Library y Vitest, evaluando:
   - Formulario de publicación con selección dinámica de cursos de I a IV ciclo y temarios silábicos oficiales (`OfferPublishView.test.tsx`).
   - Control de aforo automático e inmutable: 10 cupos presencial y 20 virtual en modo `readOnly` (**RN-05**).
   - Validación reactiva de antelación temporal: alerta roja y bloqueo de envío si $T \le 24\text{ h}$, aviso ámbar si $24 < T < 48\text{ h}$, y distintivo verde si $T \ge 48\text{ h}$ (**RN-04**).
   - Asignación de aulas EPIS (**RN-06**) y generación de enlaces Meet institucionales `@upt.pe` (**RN-07**).
2. **Pruebas Unitarias del Servicio Cliente de Ofertas (`offerService.test.ts`):** Validación exhaustiva de esquemas tipados, duraciones lectivas de 60 y 90 minutos, cálculo de horas de término y simulación de fallbacks locales.
3. **Pruebas de Lógica Algorítmica y Ranking Top-k (T-15 / `test_recommendations.py`):** Evaluación matemática determinista de las funciones de similitud de conjuntos (Jaccard y Dice), solapamiento en grilla horaria semanal 6×11, alineación de modalidades pedagógicas, multiplicadores de materias filtro ($1.0\text{x}$ a $1.3\text{x}$) y exclusión forzada de mérito (**RN-03**).
4. **Pruebas de Integración con Persistencia ORM Relacional (T-16 / `test_offers.py`):** Transaccionalidad ACID en PostgreSQL/Supabase sobre la tabla `sesiones_mentoria`, validación de restricciones `CHECK`, índices B-Tree, borrado restrictivo de claves foráneas y no-suplantación de identidad mediante Bearer JWT.
5. **Banco de Pruebas Algorítmico y Casos Frontera (T-18 / `test_simulation.py`):** Evaluación del motor EdRecSys v1.0 frente a 4 casos frontera (solapamiento horario cero, temas disjuntos, cursos sin ofertas, y postulantes con ciclo $< 7$), prueba de determinismo ante permutaciones aleatorias y benchmark de latencia de cómputo en microsegundos.

---

## 2. Resumen Métrico Consolidado de Cobertura de Código

A continuación, se presentan los resultados consolidados de cobertura obtenidos mediante las herramientas estandarizadas Pytest-Cov (Python 3.14) y V8 Coverage (Vitest 2.1.8).

### Cuadro 2.1: Matriz Consolidada de Cobertura por Capa Arquitectónica (Sprint 3)

| Entorno de Pruebas | Motor de Ejecución | Suites Activas | Pruebas Ejecutadas | Pruebas Aprobadas | Meta RNF09 | Cobertura Lograda | Dictamen Final |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Backend API REST** | Pytest 9.1 + Pytest-Cov | 13 | 122 | 122 (100%) | $\ge 70.0\%$ | **91.83%** | ✅ Superado (+21.83%) |
| **Frontend React SPA**| Vitest 2.1 + V8 Provider | 13 | 87 | 87 (100%) | $\ge 70.0\%$ | **92.52%** | ✅ Superado (+22.52%) |
| **TOTAL CONSOLIDADO** | **Pipeline Dual CI/CD** | **26** | **209** | **209 (100%)** | $\ge 70.0\%$ | **Ambos > 91%** | ✅ **Acreditado con Excelencia** |

Fuente: Reportes automatizados emitidos por `pytest tests/ --cov=app` y `npm run test:coverage`.

> [!NOTE]
> **Metodología de Reporte de Cobertura (Regla 3.2.7):**
> De conformidad con las directrices de documentación de software de la cátedra, las métricas de cobertura de frontend (Vitest v8) y backend (Pytest-Cov) se reportan de forma estrictamente independiente. Ambos subsistemas superan individualmente con amplio margen el umbral normativo del 70.0% estipulado en el **RNF09**.

---

## 3. Desglose Exhaustivo de Suites de Prueba de Backend (122 Pruebas en 13 Suites)

A continuación, se detallan las 122 pruebas automatizadas distribuidas en los 13 archivos de prueba del backend FastAPI.

### 3.1. Pruebas Nuevas del Sprint 3: Ofertas, Recomendador y Simulación (26 Pruebas)
A continuación, se detalla el catálogo de pruebas específicas construidas para las tareas T-15, T-16 y T-18:

### Cuadro 3.1: Catálogo Exhaustivo de Pruebas de Backend — Módulos del Sprint 3 (26 Pruebas Nuevas)

| Archivo de Prueba | Caso de Prueba Evaluado | Tipo de Prueba | Precondición / Fixture | Resultado Esperado |
| :--- | :--- | :---: | :--- | :--- |
| `tests/test_offers.py` | `test_publish_offer_presencial_success` | Integración API | Mentor acreditado ciclo 8, antelación 48h | Retorna HTTP 201 Created con código `SES-XXXX`, aforo 10 y estado `PUBLICADA`. |
| `tests/test_offers.py` | `test_publish_offer_rejects_insufficient_advance_time_rn04`| Regla RN-04 | Antelación de 12 horas ($T \le 24\text{ h}$) | Rechaza con HTTP 400 Bad Request y código `OFFER_ADVANCE_TIME_INVALID`. |
| `tests/test_offers.py` | `test_publish_offer_rejects_unauthorized_spoofing` | Seguridad RNF02| Usuario intenta publicar a nombre de otro mentor | Rechaza con HTTP 403 Forbidden (`FORBIDDEN_OFFER_SPOOFING`). |
| `tests/test_offers.py` | `test_offers_isolation_empty_db_and_exact_boundary`| Frontera / Aislamiento| DB con 0 registros; antelación exacta 24.00h vs 24.03h| Retorna lista vacía sin fugas; rechaza a 24.00h y acepta a 24.03h. |
| `tests/test_recommendations.py`| `test_jaccard_and_dice_mathematical_properties`| Lógica Algorítmica | Conjuntos temáticos idénticos, disjuntos y vacíos | Jaccard y Dice retornan 1.0, 0.0 y 0.0 sin excepción por división entre cero. |
| `tests/test_recommendations.py`| `test_modality_compatibility_scoring` | Lógica Negocio | Presencial-Presencial, Virtual-Virtual, Híbrido | Retorna 1.0 para coincidencia exacta, 0.9 para híbrido y 0.2 para cruce opuesto. |
| `tests/test_recommendations.py`| `test_ineligible_mentor_cycle_below_7_gets_zero_score_rn03`| Regla RN-03 | Candidatos con ciclos 1 a 6 postulando a mentor | Puntaje compuesto 0.0, bandera `institutional_merit_eligible = False`. |
| `tests/test_recommendations.py`| `test_critical_subject_multiplier_boost` | Ponderador Curricular | Coincidencia en *Algoritmos y Estructuras de Datos*| Aplica multiplicador $1.3\text{x}$ incrementando el ranking prioritario. |
| `tests/test_recommendations.py`| `test_top_k_ranking_limit_and_ordering` | Ranking Top-k | Cohorte de 10 mentores, parámetro `top_k = 3` | Retorna exactamente 3 items ordenados estrictamente por puntaje decreciente. |
| `tests/test_recommendations.py`| `test_empty_schedule_neutral_compatibility`| Caso Límite Horario | Mentoreado sin agenda previa configurada ($|H_m|=0$)| Retorna compatibilidad neutral de 0.50 y 0 franjas de coincidencia. |
| `tests/test_recommendations.py`| `test_offer_schedule_90_minutes_partial_and_full_overlap`| Granularidad Horaria| Oferta de 90 min con solapamiento parcial | Computa solapamiento proporcional continuo sin desbordamientos. |
| `tests/test_recommendations.py`| `test_candidate_score_with_corrupt_null_fields_does_not_crash`| Null-Safety | Perfiles con materias o modalidades nulas | Manejo seguro de nulos retornando score 0.0 sin excepciones 500. |
| `tests/test_recommendations.py`| `test_explain_recommendation_nonexistent_mentor_returns_404`| Validación API | Consulta de explicación de mentor no registrado | Retorna HTTP 404 Not Found con mensaje descriptivo. |
| `tests/test_recommendations.py`| `test_explain_recommendation_ineligible_mentor_returns_rejection`| Explicabilidad RN-03| Explicación de mentor con ciclo 5 | Retorna desglose con motivo de exclusión por mérito académico. |
| `tests/test_recommendations.py`| `test_get_candidate_mentors_empty_db_returns_empty_list_no_leak`| Aislamiento Datos | Base de datos vacía sin registros de mentor | Retorna lista vacía `[]` sin reutilización de estado mock. |
| `tests/test_recommendations.py`| `test_recommend_mentors_endpoint_success` | Integración API | Mentoreado registrado solicita `GET /mentors` | Retorna HTTP 200 OK con esquema Pydantic validado. |
| `tests/test_recommendations.py`| `test_recommend_offers_endpoint_success` | Integración API | Mentoreado solicita `GET /offers?id_asignatura=1` | Retorna HTTP 200 OK con sesiones recomendadas. |
| `tests/test_recommendations.py`| `test_explain_recommendation_endpoint_success` | Integración API | Petición `POST /explain` con payload válido | Retorna HTTP 200 OK con desglose multifactorial tipado. |
| `tests/test_recommendations.py`| `test_recommendations_unauthenticated_request_rejected` | Seguridad API | Solicitud sin cabecera Bearer token | Retorna HTTP 401 Unauthorized. |
| `tests/test_recommendations.py`| `test_top_k_parameter_validation_bounds` | Validación Rango | Parámetros `top_k = 0` y `top_k = 25` | Rechaza con HTTP 422 por validación de rango $1 \le k \le 20$. |
| `tests/test_recommendations.py`| `test_deterministic_ordering_tie_breaking` | Determinismo | Dos mentores con puntaje idéntico | Desempata deterministamente por ponderador, ciclo y email. |
| `tests/test_simulation.py` | `test_generate_synthetic_cohorts_validity` | Simulación Datos | Generación de cohorte de 50 estudiantes sintéticos | Perfiles válidos distribuidos en los 10 ciclos EPIS-UPT. |
| `tests/test_simulation.py` | `test_evaluate_edge_cases_all_pass` | Testbench Frontera | Evaluación de los 4 casos frontera críticos | 100% de casos frontera superados satisfactoriamente. |
| `tests/test_simulation.py` | `test_evaluate_deterministic_ordering` | Testbench Robustez | 5 ejecuciones consecutivas barajando candidatos | Ranking Top-k resultante 100% idéntico byte a byte. |
| `tests/test_simulation.py` | `test_run_benchmark_metrics` | Benchmark RNF03 | Evaluación de latencia de 24 pares de candidatos | Tiempo medio por candidato: **35.8 µs**; cohorte total: **0.86 ms** ($< 50\text{ ms}$). |
| `tests/test_simulation.py` | `test_simulation_testbench_endpoint` | Integración API | Petición `GET /simulation/testbench` | Retorna HTTP 200 OK con reporte completo de conformidad. |

Fuente: Elaboración propia a partir de `tests/test_offers.py`, `tests/test_recommendations.py` y `tests/test_simulation.py`.

---

### 3.2. Suites Preexistentes del Backend Preservadas (96 Pruebas)
A continuación, se documenta la certificación de no-regresión en las suites heredadas de los Sprints 1 y 2:

### Cuadro 3.2: Catálogo de Suites de Backend Heredadas y Preservadas (96 Pruebas con 0 Regresiones)

| Archivo de Prueba | N.° Tests | Enfoque Evaluado y Componentes | Resultado Observado |
| :--- | :---: | :--- | :---: |
| `tests/test_auth.py` | 10 | Solicitud OTP, validación `@upt.pe`, cooldown 60s, expiración 5 min, verificación de token. | 10 aprobadas (0 fallos) |
| `tests/test_authorization.py` | 11 | Aislamiento horizontal de perfiles, rechazo de autopromoción a mentor, validación Bearer JWT. | 11 aprobadas (0 fallos) |
| `tests/test_config.py` | 6 | Carga de variables `.env`, normalización de URLs de PostgreSQL y orígenes CORS. | 6 aprobadas (0 fallos) |
| `tests/test_consent.py` | 5 | Consentimiento Ley 29733 (RN-02), aceptación formal, rechazo bloqueante y revocación. | 5 aprobadas (0 fallos) |
| `tests/test_curriculum.py` | 8 | Catálogo curricular, 5 materias filtro, detalle y unidades silábicas (CUS21). | 8 aprobadas (0 fallos) |
| `tests/test_health.py` | 7 | Diagnóstico `/health`, conectividad a BD `/health/db` con `SELECT 1` y fallback. | 7 aprobadas (0 fallos) |
| `tests/test_profiles.py` | 11 | Perfiles formativos, postulación a mentor con mérito RN-03 y matriz semanal 6×11. | 11 aprobadas (0 fallos) |
| `tests/test_roles.py` | 7 | Asignación de rol base mentoreado, promoción administrativa a mentor y revocación. | 7 aprobadas (0 fallos) |
| `tests/test_security.py` | 6 | Firma y verificación HMAC-SHA256, expiración de tokens JWT y enmascaramiento seguro. | 6 aprobadas (0 fallos) |
| `tests/test_session.py` | 10 | Pooler de sesiones SQLAlchemy 2.0, inyección `get_db()`, cierre seguro y transaccionalidad. | 10 aprobadas (0 fallos) |
| **SUBTOTAL HEREDADO** | **96** | **Módulos de Autenticación, Catálogo, Perfiles y Roles (S1 y S2)** | **96 aprobadas (100%)** |

Fuente: Elaboración propia a partir de las ejecuciones en `aplicacion/backend/tests/`.

---

## 4. Desglose Exhaustivo de Suites de Prueba de Frontend (87 Pruebas en 13 Suites)

A continuación, se documenta la batería de pruebas unitarias y de componentes en React 19 ejecutadas con Vitest.

### 4.1. Pruebas Nuevas del Sprint 3: Formulario y Servicio de Ofertas (21 Pruebas)
A continuación, se detalla la matriz de pruebas del frontend para la tarea T-14:

### Cuadro 4.1: Catálogo Exhaustivo de Pruebas de Frontend — Módulo de Ofertas T-14 (21 Pruebas Nuevas)

| Suite de Pruebas | N.° Tests | Enfoque Evaluado y Componentes Bajo Prueba | Cobertura Lograda |
| :--- | :---: | :--- | :---: |
| `src/services/__tests__/offerService.test.ts` | 14 | Validación de payload obligatorio (`validateOfferPayload`); cálculo de horas de antelación (`calculateAdvanceHours`); fijación estricta de aforo 10 presencial / 20 virtual (`STANDARD_CAPACITY`); cálculo de hora de término en 60 y 90 min; publicación presencial con código `SES-XXXX`; publicación virtual con enlace Google Meet; rechazo con antelación $\le 24\text{ h}$; rechazo de duraciones arbitrarias (ej. 45 min); formato de fechas ISO; y persistencia en catálogo local. | **86.46% Líneas** |
| `src/components/__tests__/OfferPublishView.test.tsx`| 7 | Renderizado de formulario con datos del mentor acreditado; carga dinámica silábica al seleccionar materia filtro; actualización reactiva de aforo a 20 al conmutar a Virtual (RN-05); bloqueo con banner rojo ante antelación $\le 24\text{ h}$ (RN-04); habilitación y badge verde con antelación $\ge 48\text{ h}$; flujo completo de publicación interactiva con tarjeta de éxito; y reinicio de estado para nueva publicación. | **97.32% Líneas** |
| **SUBTOTAL OFERTAS T-14** | **21** | **Formulario React, Validaciones RN-04/RN-05 y Adaptador de Servicio** | **91.89% Líneas** |

Fuente: Elaboración propia a partir de `src/services/__tests__/offerService.test.ts` y `src/components/__tests__/OfferPublishView.test.tsx`.

---

### 4.2. Suites Preexistentes del Frontend Preservadas (66 Pruebas)
A continuación, se documentan las suites cliente preexistentes que certifican la no-regresión de la interfaz:

### Cuadro 4.2: Catálogo de Suites de Frontend Heredadas y Preservadas (66 Pruebas con 0 Regresiones)

| Suite de Pruebas | N.° Tests | Enfoque Evaluado y Componentes Bajo Prueba | Cobertura Lograda |
| :--- | :---: | :--- | :---: |
| `src/__tests__/App.test.tsx` | 1 | Navegación entre las 6 pestañas activas (Auth, Consent, Catálogo, Perfil, Ofertas, Servicios). | 99.41% |
| `src/components/__tests__/ConsentModalView.test.tsx`| 4 | Consentimiento informado Ley 29733, checkbox vinculante y bloqueo ante rechazo (RN-02). | 95.05% |
| `src/components/__tests__/CurriculumCatalogView.test.tsx`| 4 | Buscador curricular reactivo por materia, código y temas silábicos oficiales (CUS21). | 94.54% |
| `src/components/__tests__/ProfileAvailabilityView.test.tsx`| 5 | Perfil formativo, alerta reactiva de mérito RN-03 y matriz semanal 6×11 de disponibilidad. | 90.21% |
| `src/components/__tests__/LoginOtpView.test.tsx` | 9 | Flujo OTP en 3 pasos con temporizador, reenvío con cooldown y validación `@upt.pe`. | 94.52% |
| `src/components/__tests__/HealthStatus.test.tsx` | 3 | Monitor de salud FastAPI y Supabase (`SELECT 1`), badge de latencia y reintento. | 100.00% |
| `src/services/__tests__/consentService.test.ts` | 5 | Consulta no registrada, aceptación UTC, rechazo de correos ajenos y revocación. | 73.24% |
| `src/services/__tests__/profileService.test.ts` | 5 | Verificación de mérito RN-03, perfil por defecto y almacenamiento de matriz semanal. | 71.73% |
| `src/services/__tests__/authService.test.ts` | 15 | Adaptador mock de autenticación, expiración 5 min, cooldown 60 s y tokens JWT. | 89.94% |
| `src/services/__tests__/apiAuthAdapter.test.ts` | 9 | Cliente REST real de autenticación, serialización JSON y manejo de errores HTTP 400. | 85.19% |
| `src/services/__tests__/apiClient.test.ts` | 6 | Cliente HTTP base, timeouts, captura de excepciones de red y consulta a `/health/db`. | 84.37% |
| **SUBTOTAL HEREDADO FRONTEND** | **66** | **11 suites de prueba unitarias y de componentes (S1 y S2)** | **91.10% Líneas** |

Fuente: Elaboración propia a partir de las suites en `aplicacion/frontend/src/`.

---

## 5. Reporte Granular de Cobertura de Código

A continuación, se documenta la desagregación de cobertura en ambas capas de código:

### Cuadro 5.1: Cobertura Granular de Backend por Módulo (Pytest-Cov)

| Módulo Backend | Sentencias | Fallos | Cobertura Líneas | Estado RNF09 ($\ge 70\%$) |
| :--- | :---: | :---: | :---: | :---: |
| `app/api/v1/endpoints/offers.py` (T-16) | 17 | 0 | **100%** | ✅ Conforme |
| `app/api/v1/endpoints/recommendations.py` (T-16) | 31 | 0 | **100%** | ✅ Conforme |
| `app/models/offer.py` (SesionMentoria) | 21 | 0 | **100%** | ✅ Conforme |
| `app/schemas/offer.py` (Pydantic v2) | 40 | 0 | **100%** | ✅ Conforme |
| `app/schemas/recommendation.py` | 31 | 0 | **100%** | ✅ Conforme |
| `app/services/simulation_service.py` (T-18) | 77 | 1 | **99%** | ✅ Conforme |
| `app/services/recommendation_service.py` (T-15) | 224 | 15 | **93%** | ✅ Conforme |
| `app/services/offer_service.py` (T-15) | 139 | 21 | **85%** | ✅ Conforme |
| `app/api/v1/endpoints/auth.py` | 15 | 0 | **100%** | ✅ Conforme |
| `app/api/v1/endpoints/consent.py` | 17 | 0 | **100%** | ✅ Conforme |
| `app/api/v1/endpoints/curriculum.py` | 23 | 0 | **100%** | ✅ Conforme |
| `app/api/v1/endpoints/health.py` | 17 | 0 | **100%** | ✅ Conforme |
| `app/api/v1/endpoints/profiles.py` | 48 | 0 | **100%** | ✅ Conforme |
| `app/api/v1/endpoints/roles.py` | 54 | 4 | **93%** | ✅ Conforme |
| `app/services/auth_service.py` | 140 | 21 | **85%** | ✅ Conforme |
| `app/services/consent_service.py` | 50 | 6 | **88%** | ✅ Conforme |
| `app/services/curriculum_service.py` | 53 | 8 | **85%** | ✅ Conforme |
| `app/services/profile_service.py` | 109 | 27 | **75%** | ✅ Conforme |
| `app/services/role_service.py` | 73 | 14 | **81%** | ✅ Conforme |
| **TOTAL CONSOLIDADO (49 archivos)** | **1676** | **137** | **91.83%** | ✅ **Meta Superada (+21.83%)** |

Fuente: Reporte de `pytest tests/ --cov=app --cov-report=term-missing`.

![Backend Pytest Coverage](/docs/diseño/imagenes/sprint-03/05_backend_pytest_coverage_sprint03.png)  
*Figura 5.1: Terminal de ejecución de 122 pruebas de backend con 91.83% de cobertura.*

---

A continuación, se documenta la desagregación de cobertura en el frontend:

### Cuadro 5.2: Cobertura Granular de Frontend por Archivo (Vitest v8)

| Archivo / Componente Frontend | Sentencias (% Stmts) | Ramas (% Branch) | Funciones (% Funcs) | Líneas (% Lines) |
| :--- | :---: | :---: | :---: | :---: |
| `src/App.tsx` | 99.41% | 98.38% | 85.71% | **99.41%** |
| `src/components/OfferPublishView.tsx` (T-14) | 97.32% | 83.65% | 70.58% | **97.32%** |
| `src/components/ConsentModalView.tsx` | 95.05% | 74.54% | 71.42% | **95.05%** |
| `src/components/CurriculumCatalogView.tsx` | 94.54% | 72.54% | 57.14% | **94.54%** |
| `src/components/LoginOtpView.tsx` | 94.52% | 76.13% | 61.11% | **94.52%** |
| `src/components/HealthStatus.tsx` | 100.00% | 75.00% | 100.00% | **100.00%** |
| `src/components/ProfileAvailabilityView.tsx`| 90.21% | 82.24% | 36.36% | **90.21%** |
| `src/services/offerService.ts` (T-14) | 86.46% | 83.33% | 94.44% | **86.46%** |
| `src/services/authService.ts` | 89.94% | 74.19% | 100.00% | **89.94%** |
| `src/services/apiClient.ts` | 84.37% | 69.23% | 100.00% | **84.37%** |
| `src/services/consentService.ts` | 73.24% | 50.00% | 87.50% | **73.24%** |
| `src/services/profileService.ts` | 71.73% | 42.10% | 88.88% | **71.73%** |
| **TOTAL FRONTEND (13 archivos)** | **92.52%** | **77.11%** | **75.52%** | **92.52%** |

Fuente: Reporte de `npm run test:coverage` (Vitest v8).

![Frontend Vitest Coverage](/docs/diseño/imagenes/sprint-03/06_frontend_vitest_coverage_sprint03.png)  
*Figura 5.2: Terminal de ejecución de 87 pruebas de frontend con 92.52% de cobertura.*

---

## 6. Resultados del Banco de Pruebas Algorítmico y Casos Frontera (T-18)

A continuación, se presentan los resultados empíricos obtenidos al someter el motor *EdRecSys v1.0* al testbench de evaluación algorítmica:

### Cuadro 6.1: Resultados del Testbench Algorítmico de EdRecSys v1.0

| Caso Frontera / Dimensión Evaluada | Configuración del Escenario | Comportamiento Esperado | Métrica Empírica Observada | Estado |
| :--- | :--- | :--- | :---: | :---: |
| **Caso 1: Solapamiento horario nulo** | Mentoreado Lun 08-09 y mentor Vie 17-18 ($|H_m \cap H_k|=0$). | $S_{\text{horario}} = 0.0000$. Manejo sin crash clasificado en fondo. | $0\text{ franjas coincidentes}$ | ✅ Superado |
| **Caso 2: Temas silábicos disjuntos** | Mentoreado en Cálculo I y mentor en Base de Datos. | $J(T_m, T_k) = 0.0000$, $D(T_m, T_k) = 0.0000$. Coincidencia nula. | $\text{Jaccard} = 0.0000$ | ✅ Superado |
| **Caso 3: Asignatura sin ofertas activas** | Solicitud para materia sin sesiones registradas en BD. | Retorno seguro de lista vacía (`items: []`) con HTTP 200 (sin error 500). | $\text{items} = 0$ | ✅ Superado |
| **Caso 4: Exclusión de mérito RN-03** | Postulantes con ciclo formativo $< 7$ evaluados como mentores. | Puntaje compuesto forzado a 0.0 y bandera de elegibilidad en `False`. | **0.00% tasa de fuga** | ✅ Superado |
| **Determinismo ante permutaciones** | 5 ejecuciones consecutivas barajando aleatoriamente candidatos. | Orden Top-k resultante idéntico byte a byte en todas las iteraciones. | **100% Determinista** | ✅ Superado |
| **Latencia de cómputo (RNF03)** | Evaluación de 24 pares mentoreado-mentor. | Tiempo medio por candidato $< 50\text{ ms}$. | **35.8 µs / candidato (0.86 ms total)** | ✅ Superado |

Fuente: Elaboración propia a partir de `pytest tests/test_simulation.py -v -s` y `/api/v1/recommendations/simulation/testbench`.

![Algorithmic Testbench](/docs/diseño/imagenes/sprint-03/07_algorithmic_testbench_cases.png)  
*Figura 6.1: Terminal del testbench algorítmico de EdRecSys v1.0 certificando robustez y latencia sub-milisegundo.*

---

## 7. Reporte de Linteo Estático y Calidad de Código

### 7.1. Backend (Ruff 0.9.x)
- **Comando:** `ruff check .`
- **Resultado:** `All checks passed!` (0 infracciones de sintaxis, 0 variables huérfanas, 49 archivos conformes).
- **Comando de Formato:** `ruff format --check .`
- **Resultado:** `61 files already formatted` (100% conforme con las normas de codificación).

### 7.2. Frontend (ESLint 9 + Prettier)
- **Comando:** `npm run lint`
- **Resultado:** `0 errors, 0 warnings` (100% tipado estricto en TypeScript 5.6 y reglas de React Hooks cumplidas).

---

## 8. Comandos Reproducibles para Certificación y Auditoría

Para reproducir fielmente la batería de pruebas en cualquier estación de trabajo:

```powershell
# 1. Auditoría del Backend (122 pruebas, 91.83% cobertura, linteo limpio)
cd aplicacion/backend
ruff check .
ruff format --check .
pytest tests/ --cov=app --cov-report=term-missing

# 2. Ejecución específica del Testbench Algorítmico (T-18)
pytest tests/test_simulation.py -v -s

# 3. Auditoría del Frontend (87 pruebas, 92.52% cobertura, linteo limpio)
cd ../frontend
npm run lint
npm run test:coverage
npm run build
```

---
*Escuela Profesional de Ingeniería de Sistemas — Universidad Privada de Tacna — 26 de Octubre de 2026*
