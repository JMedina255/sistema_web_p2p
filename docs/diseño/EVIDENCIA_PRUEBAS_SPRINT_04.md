# Documento de Evidencia y Catálogo de Pruebas Automatizadas: Sprint 4
## "Recomendación Top-k, Feed de Mentorías, Reserva Transaccional Concurrente (ACID RNF07) y Evaluación de Quórum T-24h"

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II)  
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Fecha de Cierre:** 31/10/2026  
**Rama Base de Integración:** `main`  
**Estado:** ✅ **245 de 245 Pruebas Superadas (100% Satisfactorio, 0 Fallos, Coberturas: 91.22% Backend / 92.56% Frontend)**

---

## Control de Versiones

A continuación, se presenta la tabla de control de versiones del documento de evidencia de pruebas para el Sprint 4:

### Cuadro 0.1: Control de Versiones — Catálogo de Evidencias de Pruebas (Sprint 4)

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcarcel | Dirección EPIS | 31/10/2026 | Emisión formal del catálogo de evidencias de pruebas automatizadas del Sprint 4: consolidación de 245 pruebas automatizadas (158 en Pytest Backend y 87 en Vitest Frontend), desglose de las 27 suites, matrices de cobertura por archivo/línea (91.22% backend / 92.56% frontend), auditoría de linteo estático (Ruff/ESLint), testbench multihilo ACID con bloqueo pesimista `SELECT ... FOR UPDATE` (RNF07, 0.00% sobrecupo), benchmark de latencia algorítmica y comandos reproducibles de verificación. |

Fuente: Elaboración propia.

El control de versiones acredita la auditabilidad, reproducibilidad técnica y trazabilidad de los artefactos de software generados en estricto cumplimiento del marco de calidad del curso y las reglas de diseño institucional **D-1 a D-10**.

---

## 1. Propósito y Estrategia de Pruebas del Sprint 4

El presente documento certifica el cumplimiento del requerimiento no funcional **RNF09 (Mantenibilidad y Calidad de Código)**, que establece un umbral mínimo obligatorio del **70.0% de cobertura de código por pruebas automatizadas** en frontend y backend, así como los requerimientos de atomicidad transaccional (**RNF07: Tasa de sobrecupo de exactamente 0.0%**), latencia algorítmica (**RNF03** $< 50\text{ ms}$) y las reglas de negocio institucionales (**RN-04, RN-05, RN-08, RN-09 y RN-11**).

La estrategia de pruebas consolidada para el Sprint 4 articula seis niveles de verificación técnica:
1. **Pruebas de Componentes React e Interacción de Usuario (T-18 / T-20 / T-21 / T-23 / Vitest):** Renderizado en DOM virtual (`jsdom`) mediante React Testing Library y Vitest, evaluando:
   - Feed interactivo de recomendaciones Top-k con tarjetas de desglose explicable (XAI), compatibilidad temática (Jaccard), horaria (6×11), modalidad y multiplicadores curriculares (`OfferPublishView.test.tsx`, `App.test.tsx`).
   - Modal reactivo de reserva con bloqueo de no-autoreserva, aforos inmutables (10 presencial / 20 virtual, **RN-05**) y advertencia reglamentaria de corte a $T-24\text{ h}$ (**RN-08**).
   - Formulario de consentimiento informado según la Ley N° 29733 (**RN-02** / `ConsentModalView.test.tsx`).
   - Gestión de perfiles y disponibilidad horaria 6×11 (`ProfileAvailabilityView.test.tsx`).
2. **Pruebas Unitarias de Clientes de Servicio Frontend (`offerService.test.ts`, `authService.test.ts`, `apiClient.test.ts`):** Validación exhaustiva de contratos tipados, adaptadores de autenticación Bearer JWT, captura y traducción de errores HTTP 400, 403, 404 y 409 (`CAPACITY_EXCEEDED`).
3. **Pruebas de Ranking Top-k y Ponderadores Curriculares (T-17 / `test_recommendations.py`):** Evaluación matemática determinista de la función de afinidad multifactorial ($S_{\text{total}}$), multiplicadores de materias filtro EPIS ($1.0\text{x}$ a $1.3\text{x}$), desempate determinista quíntuple y exclusión estricta de postulantes de ciclo $< 7$ (**RN-03**).
4. **Pruebas de API REST de Reservas y Solicitudes por Demanda (T-22 / `test_bookings.py`):** Cobertura exhaustiva de endpoints `/api/v1/bookings/reserve`, `/api/v1/bookings/my-reservations`, `/api/v1/bookings/session/{id}/reservations`, `/api/v1/bookings/demands` y validación de esquemas Pydantic v2.
5. **Pruebas de Evaluación de Quórum a $T-24\text{ h}$ (`test_bookings.py` / `test_quorum.py`):** Cómputo del 50% de quórum reglamentario (**RN-09**), transición de reservas no confirmadas a `NO_CONFIRMADA` (**RN-08**) y transición de sesiones a `CONFIRMADA` o `CANCELADA_FALTA_QUORUM`.
6. **Testbench de Concurrencia Multihilo ACID con Bloqueo Pesimista (T-24 / RNF07 / `test_bookings.py`):** Ejecución simultánea de 20 hilos en contención extrema disputando la última vacante disponible (9/10 ocupadas) sobre base de datos relacional y SQLite file-backed, verificando exactamente 1 éxito (HTTP 201 Created), 19 rechazos controlados (HTTP 409 Conflict) y 0.00% de sobrecupo.

---

## 2. Resumen Métrico Consolidado de Cobertura de Código

A continuación, se presentan los resultados consolidados de cobertura obtenidos mediante las herramientas estandarizadas Pytest-Cov (Python 3.14/3.13) y V8 Coverage (Vitest 2.1.8).

### Cuadro 2.1: Matriz Consolidada de Cobertura por Capa Arquitectónica (Sprint 4)

| Entorno de Pruebas | Motor de Ejecución | Suites Activas | Pruebas Ejecutadas | Pruebas Aprobadas | Meta RNF09 | Cobertura Lograda | Dictamen Final |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Backend API REST** | Pytest 9.1 + Pytest-Cov | 14 | 158 | 158 (100%) | $\ge 70.0\%$ | **91.22%** | ✅ Superado (+21.22%) |
| **Frontend React SPA**| Vitest 2.1 + V8 Provider | 13 | 87 | 87 (100%) | $\ge 70.0\%$ | **92.56%** | ✅ Superado (+22.56%) |
| **TOTAL CONSOLIDADO** | **Pipeline Dual CI/CD** | **27** | **245** | **245 (100%)** | $\ge 70.0\%$ | **Ambos > 91%** | ✅ **Acreditado con Excelencia** |

Fuente: Reportes automatizados emitidos por `pytest tests/ --cov=app` y `npx vitest run --coverage`.

> [!NOTE]
> **Metodología de Reporte de Cobertura (Regla 3.2.7):**
> De conformidad con las directrices de documentación de software de la cátedra, las métricas de cobertura de frontend (Vitest v8) y backend (Pytest-Cov) se reportan de forma estrictamente independiente. Ambos subsistemas superan individualmente con amplio margen el umbral normativo del 70.0% estipulado en el **RNF09**.

---

## 3. Desglose Exhaustivo de Suites de Prueba de Backend (158 Pruebas en 14 Suites)

A continuación, se detallan las 158 pruebas automatizadas distribuidas en los 14 archivos de prueba del backend FastAPI.

### 3.1. Pruebas Nuevas del Sprint 4: Reservas, Concurrencia ACID y Quórum (36 Pruebas)

A continuación, se detalla el catálogo de pruebas específicas construidas para las tareas T-17, T-19, T-22 y T-24 del Sprint 4:

### Cuadro 3.1: Catálogo Exhaustivo de Pruebas de Backend — Módulos del Sprint 4 (36 Pruebas Nuevas y Ampliadas)

| Archivo de Prueba | Caso de Prueba Evaluado | Tipo de Prueba | Precondición / Fixture | Resultado Esperado |
| :--- | :--- | :---: | :--- | :--- |
| `tests/test_bookings.py` | `test_reserve_seat_success_in_memory` | Transaccional | Sesión con vacantes libres en memoria | Retorna HTTP 201 Created con código `RES-XXXX`, ticket hash SHA-256 y estado `PENDIENTE_CONFIRMACION`. |
| `tests/test_bookings.py` | `test_reserve_seat_success_in_real_db` | Integración ORM | Sesión en SQLite/PostgreSQL relacional | Inserta fila en tabla `reservas_cupo`, actualiza aforo y confirma transacción ACID. |
| `tests/test_bookings.py` | `test_reserve_seat_rejects_nonexistent_session_404` | Validación API | Petición con `id_sesion` inexistente (99999) | Rechaza con HTTP 404 Not Found y mensaje `SESSION_NOT_FOUND`. |
| `tests/test_bookings.py` | `test_reserve_seat_rejects_session_not_published_400` | Regla de Estado | Sesión en estado `CANCELADA` o `FINALIZADA` | Rechaza con HTTP 400 Bad Request (`SESSION_NOT_AVAILABLE`). |
| `tests/test_bookings.py` | `test_reserve_seat_rejects_antelation_under_24_hours_rn04`| Regla RN-04 | Inicio en menos de 24 horas respecto a `now()` | Rechaza con HTTP 400 Bad Request (`CUTOFF_TIME_EXCEEDED`). |
| `tests/test_bookings.py` | `test_reserve_seat_rejects_mentor_booking_own_session_400`| Integridad Negocio | Mentor intenta reservar cupo en su propia clase | Rechaza con HTTP 400 Bad Request (`MENTOR_CANNOT_BOOK_OWN_SESSION`). |
| `tests/test_bookings.py` | `test_reserve_seat_rejects_duplicate_active_booking_400` | Unicidad CUS04 | Estudiante ya posee reserva `PENDIENTE` o `CONFIRMADA` | Rechaza con HTTP 400 Bad Request (`DUPLICATE_BOOKING`). |
| `tests/test_bookings.py` | `test_reserve_seat_rejects_capacity_exceeded_409` | Control Aforo | Sesión con 10/10 plazas cubiertas (RN-05) | Rechaza con HTTP 409 Conflict (`CAPACITY_EXCEEDED`). |
| `tests/test_bookings.py` | `test_reserve_seat_with_bearer_jwt_authorization` | Seguridad RNF02 | Petición con cabecera `Authorization: Bearer <token>` | Procesa reserva validando identidad del token sin suplantación. |
| `tests/test_bookings.py` | `test_get_my_reservations_endpoint` | Consulta API | Estudiante autenticado consulta `/my-reservations` | Retorna lista tipada de reservas con desglose de asignatura, fecha y código. |
| `tests/test_bookings.py` | `test_get_session_reservations_mentor_access` | Autorización RBAC | Mentor de la clase solicita nómina de inscritos | Retorna HTTP 200 OK con detalle de asistentes. |
| `tests/test_bookings.py` | `test_create_and_get_demand_requests_cus03` | Flujo CUS03 | Registro de necesidad formativa por demanda | Retorna HTTP 201 Created y persiste en `solicitudes_demanda`. |
| `tests/test_bookings.py` | `test_quorum_evaluation_below_50_percent` | Regla RN-09 | Sesión a T-24h con 3/10 ratificados (30% < 50%) | Retorna dictamen `CANCELADA_FALTA_QUORUM`, ratio 0.30 y mensaje explicativo. |
| `tests/test_bookings.py` | `test_quorum_evaluation_at_or_above_50_percent` | Regla RN-09 | Sesión a T-24h con 6/10 ratificados (60% >= 50%) | Retorna dictamen `CONFIRMADA`, ratio 0.60 y ratificación de espacio físico. |
| `tests/test_bookings.py` | `test_quorum_evaluation_t24h_transitions_unconfirmed_to_no_confirmada`| Regla RN-08 | Reservas `PENDIENTE_CONFIRMACION` al llegar a T-24h | Transicionan automáticamente a `NO_CONFIRMADA` liberando sus plazas. |
| `tests/test_bookings.py` | `test_concurrent_multithreaded_booking_pessimistic_lock_rnf07` | Concurrencia RNF07| 20 hilos disputando la última plaza en memoria | Exactamente 1 éxito (201), 19 conflictos (409). Sobrecupo = 0.00%. |
| `tests/test_bookings.py` | `test_concurrent_multithreaded_booking_real_db_rnf07` | Concurrencia ACID | 20 hilos simultáneos sobre base de datos relacional | 1 HTTP 201, 19 HTTP 409. 10/10 plazas finales. 0 colisiones en C/SQLite. |
| `tests/test_bookings.py` | `test_db_backed_student_and_session_reservations` | Integración ORM | Consultas filtradas por estado en base de datos real | Filtra correctamente por `CONFIRMADA`, `PENDIENTE` y `CANCELADA`. |
| `tests/test_bookings.py` | `test_db_backed_demand_requests_and_filters` | Integración ORM | Inserción y consulta de demandas en tabla relacional | Persistencia conforme en `solicitudes_demanda` con filtros por tema. |
| `tests/test_bookings.py` | `test_db_backed_quorum_evaluation` | Integración ORM | Corte de quórum sobre sesiones y reservas relacionales | Transición atómica de estados y actualización de registros en BD. |
| `tests/test_bookings.py` | `test_reserve_seat_rejects_without_consent_403` | Legalidad RN-02 | Usuario sin consentimiento o con prefijo `sin_consentimiento`| Rechaza con HTTP 403 Forbidden (`CONSENT_REQUIRED`). |
| `tests/test_bookings.py` | `test_reserve_seat_database_busy_503` | Resiliencia | Simulación de candado transaccional ocupado con timeout | Retorna HTTP 503 Service Unavailable (`DATABASE_BUSY`). |
| `tests/test_bookings.py` | `test_get_my_reservations_unauthenticated_rejects_401`| Seguridad API | Solicitud a `/my-reservations` sin cabeceras | Rechaza con HTTP 401 Unauthorized. |
| `tests/test_bookings.py` | `test_get_session_reservations_unauthorized_rejects_401_and_403`| Seguridad RBAC | Usuario ajeno a la sesión intenta ver inscritos | Rechaza con HTTP 403 Forbidden. |
| `tests/test_bookings.py` | `test_create_demand_request_nonexistent_subject_or_topic_rejects_404`| Integridad Referencial| Demanda con asignatura o tema inexistente | Rechaza con HTTP 404 Not Found. |
| `tests/test_bookings.py` | `test_reserve_seat_real_db_all_validation_guards` | Frontera / Guardas | Evaluación secuencial de todas las guardas transaccionales| Cobertura de caminos alternativos en motor relacional. |
| `tests/test_bookings.py` | `test_quorum_evaluation_below_50_percent_in_real_db` | Integración ORM | Evaluación de quórum insuficiente sobre tablas reales | Asienta `CANCELADA_FALTA_QUORUM` en base de datos. |
| `tests/test_bookings.py` | `test_quorum_evaluation_in_memory_state_transitions`| Máquina Estados | Transiciones de estado completas en memoria | Cobertura de todas las ramas del Cuadro 4.1. |
| `tests/test_recommendations.py`| `test_top_k_ranking_limit_and_ordering` | Ranking Top-k | Cohorte de mentores, parámetro `top_k = 3` | Retorna exactamente 3 items ordenados por score decreciente. |
| `tests/test_recommendations.py`| `test_critical_subject_multiplier_boost` | Ponderador Curricular | Coincidencia en *Algoritmos y Estructuras de Datos*| Aplica multiplicador $1.3\text{x}$ incrementando el ranking prioritario. |
| `tests/test_recommendations.py`| `test_deterministic_ordering_tie_breaking` | Determinismo | Dos candidatos con score idéntico | Desempata deterministamente por ponderador, ciclo y email. |
| `tests/test_recommendations.py`| `test_ineligible_mentor_cycle_below_7_gets_zero_score_rn03`| Regla RN-03 | Candidatos con ciclos 1 a 6 postulando a mentor | Puntaje compuesto 0.0, bandera `institutional_merit_eligible = False`. |
| `tests/test_recommendations.py`| `test_top_k_parameter_validation_bounds` | Validación Rango | Parámetros `top_k = 0` y `top_k = 25` | Rechaza con HTTP 422 por validación de rango $1 \le k \le 20$. |
| `tests/test_auth.py` | `test_auth_service_with_real_db_session` | Persistencia Auth | Sesión relacional de base de datos para verificación | Valida ciclo de vida de credenciales OTP en base de datos física. |
| `tests/test_auth.py` | `test_verify_otp_already_used` | Anti-Replay | Intento de reutilización de código OTP consumido | Rechaza con error de código expirado o ya utilizado. |
| `tests/test_auth.py` | `test_verify_otp_success_and_jwt_token_issued` | Emisión JWT | Verificación de código OTP conforme | Emite token JWT firmado con claims válidos del dominio `@upt.pe`. |

Fuente: Elaboración propia a partir de las suites de prueba de backend.

El Cuadro 3.1 certifica que las 36 pruebas nuevas y ampliadas del backend blindan los componentes neurálgicos del Sprint 4: la API transaccional de reservas con bloqueo pesimista `SELECT ... FOR UPDATE` (RNF07), la prevención de sobrecupo absoluto (tasa 0.0%), la evaluación de quórum a $T-24\text{ h}$ (RN-08 / RN-09), y el ranking Top-k de recomendaciones con multiplicadores curriculares y desempate determinista.

---

### 3.2. Suites Preexistentes del Backend Preservadas (122 Pruebas en 13 Suites)

A continuación, se documenta la certificación de no-regresión en las suites heredadas de los Sprints 1, 2 y 3:

### Cuadro 3.2: Catálogo de Suites de Backend Heredadas y Preservadas (122 Pruebas con 0 Regresiones)

| Archivo de Prueba | N.° Tests | Enfoque Evaluado y Componentes | Resultado Observado |
| :--- | :---: | :--- | :---: |
| `tests/test_auth.py` | 10 | Solicitud OTP, validación `@upt.pe`, cooldown 60s, expiración 5 min, verificación de token. | 10 aprobadas (0 fallos) |
| `tests/test_authorization.py` | 11 | Aislamiento horizontal de perfiles, rechazo de autopromoción a mentor, validación Bearer JWT. | 11 aprobadas (0 fallos) |
| `tests/test_offers.py` | 14 | Publicación de ofertas presencial/virtual, antelación RN-04, aforo RN-05, anti-suplantación. | 14 aprobadas (0 fallos) |
| `tests/test_recommendations.py`| 22 | Similitud Jaccard/Dice, compatibilidad horaria 6×11, modalidad, explicabilidad XAI. | 22 aprobadas (0 fallos) |
| `tests/test_simulation.py` | 5 | Testbench algorítmico, evaluación de 4 casos frontera, prueba de determinismo y benchmark RNF03. | 5 aprobadas (0 fallos) |
| `tests/test_curriculum.py` | 8 | Catálogo de materias de I a IV ciclo, temarios silábicos, factores de ponderación (CUS21). | 8 aprobadas (0 fallos) |
| `tests/test_profiles.py` | 11 | Registro de perfil formativo, disponibilidad horaria 6×11, actualización y aislamiento. | 11 aprobadas (0 fallos) |
| `tests/test_consent.py` | 5 | Consentimiento Ley N° 29733 (RN-02), registro de aceptación, revocación y auditoría. | 5 aprobadas (0 fallos) |
| `tests/test_roles.py` | 7 | Gestión de roles (estudiante, mentor, admin), promoción y restricciones de acceso. | 7 aprobadas (0 fallos) |
| `tests/test_health.py` | 7 | Monitor de salud `/health`, conectividad con PostgreSQL/Supabase y fallback local. | 7 aprobadas (0 fallos) |
| `tests/test_session.py` | 10 | Ciclo de vida de sesiones de base de datos SQLAlchemy, pool de conexiones y rollbacks. | 10 aprobadas (0 fallos) |
| `tests/test_security.py` | 6 | Funciones criptográficas, hashing SHA-256 de OTP, firma y verificación de tokens JWT. | 6 aprobadas (0 fallos) |
| `tests/test_config.py` | 6 | Carga de variables de entorno, configuración de CORS, modos dev/test/prod y fallbacks. | 6 aprobadas (0 fallos) |
| **TOTAL PRESERVADO** | **122** | **Conjunto consolidado de suites preexistentes (Sprints 1, 2 y 3)** | **122 aprobadas (0 fallos)** |

Fuente: Elaboración propia a partir de las suites de prueba de backend.

El Cuadro 3.2 acredita formalmente que las 122 pruebas preexistentes mantienen una tasa de éxito del **100% (cero regresiones)**, garantizando la estabilidad operativa del sistema tras la incorporación de la lógica de reservas y concurrencia del Sprint 4.

---

## 4. Desglose Exhaustivo de Suites de Prueba de Frontend (87 Pruebas en 13 Suites)

A continuación, se detalla el conjunto consolidado de pruebas automatizadas del frontend React SPA ejecutadas con Vitest y V8 Coverage.

### Cuadro 4.1: Catálogo Consolidado de Suites de Prueba de Frontend (87 Pruebas en 13 Suites)

| Archivo de Prueba | N.° Tests | Componente o Servicio Evaluado | Cobertura Líneas | Estado |
| :--- | :---: | :--- | :---: | :---: |
| `src/__tests__/App.test.tsx` | 1 | Navegación entre pestañas (Acceso, Consentimiento, Catálogo, Perfil, Ofertas, Feed). | 99.41% | ✅ Aprobado |
| `src/components/__tests__/OfferPublishView.test.tsx` | 7 | Publicación de ofertas, aforo inmutable RN-05, antelación RN-04, aulas EPIS y Meet. | 97.32% | ✅ Aprobado |
| `src/components/__tests__/ConsentModalView.test.tsx` | 4 | Modal de consentimiento Ley 29733 (RN-02), bloqueo de botón y aceptación voluntaria. | 95.05% | ✅ Aprobado |
| `src/components/__tests__/LoginOtpView.test.tsx` | 9 | Flujo OTP completo, validación de dominio `@upt.pe`, cooldown de 60s y manejo de errores. | 94.75% | ✅ Aprobado |
| `src/components/__tests__/CurriculumCatalogView.test.tsx`| 4 | Catálogo de materias de I a IV ciclo, filtros silábicos y manejo resiliente de errores. | 94.54% | ✅ Aprobado |
| `src/components/__tests__/ProfileAvailabilityView.test.tsx`| 5 | Perfil formativo, validación de mérito RN-03 (ciclo $\ge 7$), grilla horaria 6×11 interactiva. | 90.21% | ✅ Aprobado |
| `src/components/__tests__/HealthStatus.test.tsx` | 3 | Indicadores de salud de API y base de datos, reintentos reactivos y estados de carga. | 100.0% | ✅ Aprobado |
| `src/services/__tests__/offerService.test.ts` | 14 | Cliente tipado de ofertas, cálculo de antelación temporal, duraciones de 60/90 min y mocks. | 86.46% | ✅ Aprobado |
| `src/services/__tests__/authService.test.ts` | 15 | Cliente de autenticación, solicitud/verificación de OTP, almacenamiento de JWT y sesión. | 89.94% | ✅ Aprobado |
| `src/services/__tests__/apiClient.test.ts` | 6 | Cliente HTTP base, interceptor de cabeceras Bearer, manejo de offline y timeout. | 84.37% | ✅ Aprobado |
| `src/services/__tests__/consentService.test.ts` | 5 | Servicio cliente de consentimiento, persistencia local y sincronización con API. | 73.24% | ✅ Aprobado |
| `src/services/__tests__/profileService.test.ts` | 5 | Servicio cliente de perfiles y agenda horaria 6×11, serialización y validación. | 71.73% | ✅ Aprobado |
| `src/services/__tests__/apiAuthAdapter.test.ts` | 9 | Adaptador de compatibilidad de autenticación, decodificación de claims y roles. | 91.67% | ✅ Aprobado |
| **TOTAL FRONTEND** | **87** | **13 suites de prueba automatizadas en DOM virtual (JSDOM)** | **92.56%** | ✅ **Acreditado** |

Fuente: Reporte oficial emitido por `npx vitest run --coverage`.

El Cuadro 4.1 confirma que las 13 suites de prueba del frontend alcanzan una cobertura consolidada de **92.56%** en líneas y sentencias, superando ampliamente el umbral del 70.0% estipulado en el **RNF09**.

---

## 5. Auditoría de Linteo Estático y Calidad de Código (Ruff y ESLint)

En cumplimiento de las directrices de calidad y mantenibilidad del software, se ejecutaron las herramientas de análisis estático en ambos subsistemas:

### 5.1. Backend Python: Ruff Linter y Formatter
- **Comandos Ejecutados:** `ruff check .` y `ruff format --check .` en `aplicacion/backend/`.
- **Archivos Auditados:** 69 archivos de código fuente Python (módulos de endpoints, servicios, modelos, esquemas y pruebas).
- **Resultado:**
  ```text
  All checks passed!
  69 files already formatted
  ```
- **Defectos Detectados:** **0 errores, 0 advertencias**. Código 100% conforme a las reglas PEP 8, flake8, isort y convenciones modernas de Python 3.13/3.14.

### 5.2. Frontend React / TypeScript: ESLint 9
- **Comando Ejecutado:** `npm run lint` en `aplicacion/frontend/`.
- **Resultado:** **0 errores, 0 advertencias**. Tipado estricto verificado sin supresiones inseguras (`any`).

---

## 6. Reporte de Compilación y Análisis de Dependencias

- **Compilador TypeScript:** `tsc -b` ejecutado exitosamente sin discrepancias de tipado entre contratos REST y modelos React.
- **Empaquetador Vite:** `npm run build` genera el bundle de producción de forma limpia en el directorio `dist/`:
  - `dist/index.html`: 0.72 kB
  - `dist/assets/index-[hash].css`: 18.42 kB (gzip: 4.18 kB)
  - `dist/assets/index-[hash].js`: 214.36 kB (gzip: 68.91 kB)
  - Tiempo de compilación: **682 ms**.

---

## 7. Banco de Pruebas Algorítmico, Determinismo y Benchmark de Concurrencia RNF07

### 7.1. Benchmark de Latencia Algorítmica EdRecSys v1.0 (RNF03)
En cumplimiento del requerimiento **RNF03** (latencia de recomendación $< 50\text{ ms}$):
- **Tamaño de Cohorte Evaluada:** 24 pares de candidatos sintéticos distribuidos en los 10 ciclos de la EPIS-UPT.
- **Tiempo Medio por Candidato:** **35.8 µs** ($0.0358\text{ ms}$).
- **Tiempo Total de Cómputo de la Cohorte:** **0.86 ms** ($< 50\text{ ms}$).
- **Margen de Cumplimiento:** **98.28% por debajo del umbral límite permitido**.

### 7.2. Test de Determinismo y Estabilidad ante Empates
- **Procedimiento:** 5 ejecuciones consecutivas del algoritmo barajando aleatoriamente el orden de ingreso de los candidatos.
- **Resultado:** El ranking Top-k resultante fue **100% idéntico byte a byte** en las 5 repeticiones, acreditando la eficacia del sistema quíntuple de desempate determinista ($S_{\text{total}} \to W_{\text{curso}} \to S_{\text{tema}} \to Ciclo \to Email$).

### 7.3. Testbench de Concurrencia Multihilo ACID (RNF07)
- **Escenario de Prueba:** 20 hilos concurrentes compitiendo simultáneamente por la última vacante disponible en una sesión con 9/10 cupos previamente cubiertos.
- **Mecanismo de Exclusión:** Candado pesimista de fila `SELECT ... FOR UPDATE` sobre la tabla relacional `sesiones_mentoria` y coordinador `_booking_lock` a nivel de proceso.
- **Resultados Observados:**
  - **Peticiones Exitosas:** Exactamente **1** (HTTP 201 Created con código `RES-DB-XXXX` y ticket hash criptográfico).
  - **Peticiones Rechazadas por Sobrecupo:** Exactamente **19** (HTTP 409 Conflict con código `CAPACITY_EXCEEDED`).
  - **Aforo Final Asentado en Base de Datos:** Exactamente **10 / 10 plazas** (0 sobrecupo, 0 colisiones en memoria, 0 excepciones no controladas).
  - **Tasa de Sobrecupo Efectiva:** **0.00%** (cumplimiento pleno de **RNF07**).

---

## 8. Instrucciones Reproducibles de Ejecución de Pruebas y Validación Local

Para reproducir y auditar la totalidad de las 245 pruebas automatizadas del proyecto, ejecute las siguientes instrucciones desde la raíz del repositorio:

### 8.1. Ejecución de Pruebas de Backend
```bash
# Navegar al directorio del backend
cd aplicacion/backend

# Ejecutar la suite completa con medición de cobertura y linteo
pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=70
ruff check .
ruff format --check .
```

### 8.2. Ejecución de Pruebas de Frontend
```bash
# Navegar al directorio del frontend
cd aplicacion/frontend

# Ejecutar la suite completa con motor Vitest y proveedor V8
npx vitest run --coverage
npm run lint
npm run build
```

---

## 9. Declaración de Homologación de Cierre y Dictamen Técnico

Los integrantes del equipo consultor **Grupo 03 / C-SharkTeam** certifican que:
1. Las 245 pruebas automatizadas documentadas en el presente catálogo se encuentran plenamente operativas y verificadas en la rama `main`.
2. Las coberturas alcanzadas (**91.22% en Backend** y **92.56% en Frontend**) superan con amplio margen el estándar institucional del 70.0% estipulado en el requerimiento **RNF09**.
3. El coordinador transaccional de reservas garantiza una tasa de sobrecupo de exactamente **0.00%** bajo contención multihilo estricta (**RNF07**), eliminando cualquier riesgo de colisión o inconsistencia relacional.
4. Las reglas institucionales de la EPIS-UPT (**RN-04, RN-05, RN-08, RN-09 y RN-11**) se encuentran formalmente codificadas, testeadas e integradas de forma prescriptiva en ambos subsistemas.

| Joan Cristian Medina Quispe | Renzo Antonio Antayhua Mamani |
| :---: | :---: |
| **Código: 2022074255** | **Código: 2022073504** |
| Rol: Arquitectura Base, Frontend & CI/CD | Rol: Backend, Persistencia ORM & Concurrencia ACID |
| Firma Digital Homologada ✅ | Firma Digital Homologada ✅ |

---
*Fin del Catálogo de Evidencias de Pruebas Automatizadas — Sprint 4.*
