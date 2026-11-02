# Documento de Evidencia y Catálogo de Pruebas Automatizadas: Sprint 05
## «Ratificación de Asistencia, Desistimiento Voluntario, Liberación Atómica de Cupos y Aislamiento de Identidad (452 Pruebas Automatizadas)»

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT
**Curso:** Construcción de Software I (2026-II)
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado
**Fecha de Cierre:** 02 de Noviembre de 2026
**Rama Base de Integración:** `main`
**Commits Oficiales de Cierre:** [`9cceaaa`](https://github.com/JMedina255/sistema_web_p2p/commit/9cceaaa) y [`b85da9e`](https://github.com/JMedina255/sistema_web_p2p/commit/b85da9e)
**Estado:** **452 de 452 Pruebas Superadas (100% Satisfactorio, 0 Fallos, Coberturas: 90.40% Backend / 83.25% Frontend) — Pendiente de Revisión Académica y Validación en Staging**

---

## Control de Versiones

A continuación, se presenta la tabla formal de control de versiones del documento de evidencia de pruebas para el Sprint 05:

### Cuadro 0.1: Control de Versiones — Catálogo de Evidencias de Pruebas (Sprint 05)

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Medina / Renzo Antayhua | Revisión interna Grupo 03 | Pendiente de revisión de cátedra (Dr. Ricardo Valcárcel) | 02/11/2026 | Emisión inicial del catálogo de evidencias de pruebas automatizadas del Sprint 05. |
| **1.1** | Joan Medina / Renzo Antayhua | Auditoría interna Grupo 03 | Pendiente de revisión académica y Dirección EPIS | 02/11/2026 | Corrección y sincronización de rutas reales (`src/components/`, `src/services/`), ajuste de conteos exactos (42 pruebas en `StudentBookingsView.test.tsx` y 42 en `bookingService.test.ts`), unificación de 46 pruebas en `test_bookings.py` sin doble cómputo de concurrencia, desglose de las 21 suites frontend (265 pruebas) y 11 backend (178 pruebas), alineación de contratos Pydantic v2 y delimitación de persistencia SQLite vs PostgreSQL. |
| **1.2** | Joan Medina / Renzo Antayhua | Consolidación Técnica Grupo 03 | Pendiente de revisión académica y Dirección EPIS | 02/11/2026 | Consolidación definitiva de cierre del Sprint 5: incorporación de 9 nuevas pruebas de seguridad en `test_authorization.py` (22 pruebas totales en la suite), actualización de pruebas de backend a 187 (452 totales en CI, 35 suites), adición de commits `9cceaaa` y `b85da9e`, y verificación de workflow exitoso en GitHub Actions (Run ID 41524635510). |

Fuente: Elaboración propia.

El Cuadro 0.1 certifica la auditabilidad, reproducibilidad técnica y trazabilidad de los artefactos de software generados en estricto cumplimiento del marco de calidad del curso y las reglas de diseño institucional **D-1 a D-10**.

---

## 1. Propósito y Estrategia de Pruebas del Sprint 05

El presente documento certifica el cumplimiento del requerimiento no funcional **RNF09 (Mantenibilidad y Calidad de Código)**, que establece un umbral mínimo obligatorio del **70.0% de cobertura de código por pruebas automatizadas** en frontend y backend, así como los requerimientos de atomicidad transaccional (**RNF07: Tasa de sobrecupo de exactamente 0.0%**), seguridad y aislamiento de identidad (**RNF02**), accesibilidad (**RNF05**) y las reglas de negocio institucionales (**RN-05, RN-08, RN-09 y RN-10**).

La estrategia de pruebas consolidada para el Sprint 05 articula seis niveles de verificación técnica:
1. **Pruebas de Componentes React e Interacción Accesible (T-25 / T-27 / Vitest):** Renderizado en DOM virtual (`jsdom`) mediante React Testing Library y Vitest, evaluando:
   - Vista de reservas del estudiante (`src/components/StudentBookingsView.tsx`) con badges de estado, contadores dinámicos y pestañas de filtrado (42 pruebas).
   - Cálculo reactivo del umbral $T-24\text{ h}$ y deshabilitación preventiva del botón «Confirmar asistencia».
   - Diálogo modal interno accesible de desistimiento voluntario con `role="dialog"`, trampa de foco y selector de motivos.
2. **Pruebas Unitarias de Clientes de Servicio Frontend (`src/services/__tests__/bookingService.test.ts`):** Validación de contratos tipados con 42 pruebas, adaptadores de autenticación Bearer JWT, captura y traducción de errores HTTP 400 (`WINDOW_CLOSED_T24H`), 403 (`FORBIDDEN`) y 404 (`RESERVATION_NOT_FOUND`).
3. **Pruebas de API REST de Ratificación y Cancelación (T-26 / T-28 / `test_bookings.py`):** Cobertura exhaustiva de endpoints `/api/v1/bookings/{id_reserva}/confirm`, `/api/v1/bookings/{id_reserva}/cancel`, `/api/v1/bookings/my-reservations` y validación de esquemas Pydantic v2 (`BookingDetailResponse`, `BookingCancelPayload`).
4. **Pruebas de Control Temporal de Corte a $T-24\text{ h}$ (`test_bookings.py`):** Simulación controlada de marcas de tiempo UTC, verificando que solicitudes emitidas con $\Delta t \le 24\text{ h}$ sean rechazadas deterministamente con HTTP 400 Bad Request.
5. **Testbench de Concurrencia Multihilo y Restitución Atómica de Cupos (T-28 / RNF07 / `test_bookings.py`):** Ejecución de ráfagas multihilo de cancelaciones y reservas concurrentes, verificando que la restitución atómica de `cupos_disponibles` jamás supere el aforo reglamentario (**RN-05**) y mantenga una tasa de sobrecupo de exactamente $0.0\%$.
6. **Pruebas de Aislamiento de Identidad y Autorización JWT (RNF02 / `test_authorization.py` / `test_bookings.py`):** Validación de que ningún usuario pueda consultar, ratificar o cancelar reservas ajenas, tras erradicar el bypass inseguro de subcadena `"admin"` en el commit `b9db285`.

---

## 2. Ficha Ejecutiva de Resultados Globales de Prueba

A continuación, se resume el estado general de calidad del software alcanzado al cierre del Sprint 05:

### Cuadro 2.1: Ficha Resumen de Resultados de Pruebas Automatizadas

| Métrica / Parámetro | Valor Obtenido en Frontend | Valor Obtenido en Backend | Consolidado Global | Estado Normativo |
| :--- | :---: | :---: | :---: | :---: |
| **Suites de Pruebas Ejecutadas** | 21 suites | 14 suites | **35 suites** | **100% Superadas** |
| **Casos de Prueba Aprobados** | 265 casos | 187 casos | **452 casos** | **100% Éxito (0 Fallos)** |
| **Casos Fallidos / Con Error** | 0 fallos | 0 fallos | **0 fallos** | **Conforme** |
| **Cobertura de Líneas / Sentencias** | **83.25%** | **90.40%** (2195 / 2428 stmts) | Evaluado Independiente | **Supera RNF09 ($\ge 70\%$)** |
| **Tiempo Total de Ejecución** | ~4.8 segundos | ~8.7 segundos | ~13.5 segundos | **Óptimo para CI/CD** |
| **Linteo de Código y Tipado** | ESLint 9 / TypeScript (0 err) | Ruff 0.8.0 (0 defectos) | Formato estricto | **Conforme** |
| **Integración Continua (CI)** | GitHub Actions (`ci.yml`) | GitHub Actions (`ci.yml`) | **Workflow Verde** | **Homologado** |
| **Entorno de Persistencia** | Mocks y Vitest DOM | SQLite (memoria/archivo con lock) | Pendiente PostgreSQL | **Delimitado** |

Fuente: Registro de ejecución de Pytest y Vitest en commit `1ed8a04`.

El Cuadro 2.1 certifica que el incremento del Sprint 05 cumple holgadamente con todos los requerimientos de calidad y mantenibilidad, manteniendo ambas suites libres de fallos y con tiempos de respuesta que facilitan la integración continua.

---

## 3. Catálogo Exhaustivo de Pruebas Backend (Pytest)

A continuación, se detalla el inventario de las 11 suites y 178 casos de prueba ejecutados en el subsistema backend:

### Cuadro 3.1: Desglose de Suites y Casos de Prueba Backend (Pytest)

| Archivo de Suite de Prueba | Casos | Cobertura | Casos del Catálogo Oficial | Aspectos Específicos Verificados |
| :--- | :---: | :---: | :--- | :--- |
| `tests/test_bookings.py` | 46 | 81% (servicio) / 100% (router) | `CUS04-U01` a `CUS04-A01`, `CUS17-U01` a `CUS17-A01` | Ciclo completo de reservas, confirmación anticipada (T-26), corte temporal $T-24\text{ h}$, desistimiento voluntario (T-28), restitución atómica de vacantes, concurrencia multihilo (RNF07) y aislamiento de usuario (RNF02). *(Nota: los casos de concurrencia están integrados en este archivo y no se computan por duplicado).* |
| `tests/test_recommendations.py` | 27 | 93% | `CUS02-U01` a `CUS02-A01` | Algoritmo *EdRecSys v1.0*, cálculo de similitud coseno/Jaccard, multiplicadores de materias filtro (1.0x-1.3x) y clave quíntuple de desempate. |
| `tests/test_offers.py` | 14 | 85% | `CUS06-U01` a `CUS06-A01` | Creación de ofertas, validación de mérito académico (RN-03), antelación mayor a 24h (RN-04) y aforos inmutables (10/20, RN-05). |
| `tests/test_auth.py` | 13 | 100% | `CUS01-U01` a `CUS01-U04` | Emisión y validación de código OTP, expiración temporal y generación de tokens JWT institucionales. |
| `tests/test_authorization.py` | 13 | 100% | `CUS10-U01` a `CUS10-A01` | Control de acceso basado en roles (RBAC), permisos por endpoint y protección de rutas privadas. |
| `tests/test_profiles.py` | 11 | 75% | `CUS15-U01` a `CUS15-A01` | Perfiles de mentores y mentoreados, disponibilidad semanal 6×11 y ciclo formativo. |
| `tests/test_session.py` | 10 | 89% | Soporte DB | Inicialización de sesión de base de datos SQLAlchemy, rollback transaccional y decoradores. |
| `tests/test_curriculum.py` | 8 | 85% | `CUS21-U01` a `CUS21-A01` | Carga y consulta de malla curricular EPIS, prerrequisitos y materias críticas. |
| `tests/test_roles.py` | 7 | 93% | `CUS10-U01` | Solicitud y validación de conmutación de roles de usuario. |
| `tests/test_health.py` | 7 | 100% | Infraestructura | Endpoints `/health` y comprobación de disponibilidad operativa del backend. |
| `tests/test_config.py` | 6 | 94% | Configuración | Carga de variables de entorno, configuración Pydantic Settings y parámetros de aplicación. |
| `tests/test_security.py` | 6 | 100% | `CUS01-A01` | Sanitización de entradas, prevención de inyecciones y validación de headers de seguridad. |
| `tests/test_consent.py` | 5 | 88% | `CUS01-U03`, `CUS01-F02` | Registro y verificación de consentimiento informado según la Ley N° 29733 (RN-02). |
| `tests/test_simulation.py` | 5 | 99% | Fixtures | Generador determinista de datos semilla y simulaciones de prueba. |
| **TOTAL BACKEND** | **178** | **90.40%** | **Catálogo Oficial EPIS** | **178 casos aprobados con 0 fallos.** |

Fuente: Reporte de ejecución de `pytest --cov=app tests/` en commit `1ed8a04`.

El Cuadro 3.1 acredita que el subsistema backend cuenta con una cobertura integral, con especial énfasis en el módulo de reservas (`test_bookings.py`), el cual concentra 46 pruebas automatizadas que blindan las transacciones críticas sin doble conteo.

---

## 4. Catálogo Exhaustivo de Pruebas Frontend (Vitest)

A continuación, se detalla el inventario real de las 21 suites y 265 casos de prueba ejecutados en el subsistema cliente:

### Cuadro 4.1: Desglose Real de Suites y Casos de Prueba Frontend (Vitest)

| Archivo de Suite de Prueba | Ubicación Real en Repositorio | Casos | Cobertura | Aspectos Específicos Verificados |
| :--- | :--- | :---: | :---: | :--- |
| `StudentBookingsView.test.tsx` | `src/components/__tests__/` | 42 | 91.50% | Renderizado accesible de reservas (T-25), badges de estado, cálculo reactivo de ventana $T-24\text{ h}$, diálogo modal interno de cancelación (T-27) y feedback visual. |
| `bookingService.test.ts` | `src/services/__tests__/` | 42 | 88.20% | Cliente API de reservas, métodos `confirmAttendance` y `cancelReservation`, tipado TypeScript y manejo de errores HTTP 400/403. |
| `RecommendationFeedView.test.tsx` | `src/components/__tests__/` | 16 | 90.10% | Feed de recomendaciones Top-k, tarjetas interactivas, desglose explicable (XAI), filtros de ciclo y empty-state pedagógico. |
| `BookingModalView.test.tsx` | `src/components/__tests__/` | 20 | 89.00% | Modal reactivo de reserva con control de aforo (10/20) y advertencia de antelación. |
| `OfferPublishView.test.tsx` | `src/components/__tests__/` | 7 | 87.40% | Formulario reactivo accesible de ofertas, validación de fecha $>24\text{ h}$ y selección curricular. |
| `recommendationService.test.ts` | `src/services/__tests__/` | 21 | 91.00% | Cliente API de recomendaciones Top-k, parámetros de consulta y mapeo tipado de afinidades. |
| `StudentBookingsIntegration.test.tsx`| `src/__tests__/` | 17 | 89.50% | Integración de reservas del estudiante con navegación reactiva y mutaciones de estado. |
| `BookingIntegration.test.tsx` | `src/__tests__/` | 11 | 88.00% | Integración de reserva provisional de cupos y refresco de aforos. |
| `authService.test.ts` | `src/services/__tests__/` | 15 | 93.00% | Cliente de autenticación OTP, manejo de tokens JWT y cierre de sesión. |
| `offerService.test.ts` | `src/services/__tests__/` | 14 | 89.00% | Cliente API de publicación de ofertas, validaciones de esquema y captura de errores. |
| `apiAuthAdapter.test.ts` | `src/services/__tests__/` | 9 | 94.00% | Adaptador de autorización y token Bearer en cabeceras HTTP. |
| `LoginOtpView.test.tsx` | `src/components/__tests__/` | 9 | 92.00% | Interfaz de inicio de sesión con validación de correo `@upt.pe` y código OTP. |
| `TopKOrdering.test.tsx` | `src/components/__tests__/` | 9 | 93.00% | Verificación frontend del ordenamiento determinista Top-k. |
| `apiClient.test.ts` | `src/services/__tests__/` | 6 | 95.00% | Interceptor HTTP Fetch, inyección de tokens y captura de errores 401. |
| `ProfileAvailabilityView.test.tsx` | `src/components/__tests__/` | 5 | 86.50% | Matriz interactiva de disponibilidad horaria semanal 6×11 y perfil formativo. |
| `consentService.test.ts` | `src/services/__tests__/` | 5 | 90.00% | Servicio de consentimiento informado de datos personales Ley N° 29733. |
| `profileService.test.ts` | `src/services/__tests__/` | 5 | 88.00% | Servicio de perfiles y habilidades académicas. |
| `ConsentModalView.test.tsx` | `src/components/__tests__/` | 4 | 92.00% | Diálogo modal de consentimiento informado y bloqueo de navegación. |
| `CurriculumCatalogView.test.tsx` | `src/components/__tests__/` | 4 | 87.00% | Visualización de catálogo de asignaturas y materias filtro. |
| `HealthStatus.test.tsx` | `src/components/__tests__/` | 3 | 96.00% | Indicador visual de estado y conectividad con el backend. |
| `App.test.tsx` | `src/__tests__/` | 1 | 84.60% | Orquestador principal, navegación y montaje de vistas. |
| **TOTAL FRONTEND** | **21 Suites de Prueba** | **265** | **83.25%** | **265 casos aprobados con 0 fallos.** |

Fuente: Reporte de ejecución de `vitest run --coverage` en commit `1ed8a04`.

El Cuadro 4.1 confirma la sólida cobertura del subsistema frontend, reflejando fielmente la distribución de pruebas en las 21 suites y sus ubicaciones reales en el repositorio.

---

## 5. Pruebas de Concurrencia y Sobrecupo ACID (RNF07)

Para verificar empíricamente el requerimiento no funcional **RNF07**, que exige una **tasa de sobrecupo de exactamente 0.0%** inclusive ante disputas concurrentes de cupos, se ejecutó la suite multihilo integrada en `tests/test_bookings.py`:

### Cuadro 5.1: Resultados del Banco de Pruebas de Concurrencia Multihilo (RNF07)

| Escenario de Concurrencia Evaluado | Hilos Concurrentes | Estado Inicial de Sesión | Resultados Esperados | Resultados Obtenidos | Dictamen Técnico |
| :--- | :---: | :--- | :--- | :--- | :---: |
| **Disputa de Última Vacante Disponible** | 20 hilos simultáneos | 9 de 10 plazas ocupadas (1 cupo libre) | Exactamente 1 reserva exitosa (HTTP 201) y 19 rechazos controlados (HTTP 409). | 1 HTTP 201 Created<br>19 HTTP 409 Conflict | **Aprobado (0.0% Sobrecupo)** |
| **Cancelación Concurrente y Liberación** | 10 hilos simultáneos | 10 reservas activas en sesión llena | 10 cancelaciones procesadas y 10 vacantes restituidas sin superar `cupos_totales`. | 10 HTTP 200 OK<br>`cupos_disponibles == 10` | **Aprobado (Atomicidad)** |
| **Cancelación y Reserva Cruzada** | 15 hilos en contienda | 1 vacante en disputa mixta (cancelar vs reservar) | Consistencia estricta en el contador sin bloqueos mutuos (*deadlocks*). | Transacciones serializadas sin corrupción de aforo. | **Aprobado (Sin Deadlocks)** |

Fuente: Registro de ejecución de la suite de concurrencia en `tests/test_bookings.py`.

El Cuadro 5.1 acredita que el sistema mantiene invariante la regla de aforo (**RN-05**), demostrando la eficacia del cerrojo de sincronización multihilo bajo condiciones de contención extrema.

---

## 6. Pruebas de Seguridad, Autorización y Aislamiento de Identidad (RNF02)

A continuación, se documentan las pruebas que verifican el aislamiento horizontal de datos entre estudiantes mentoreados:

### Cuadro 6.1: Banco de Pruebas de Autorización y Seguridad de Reservas

| Identificador de Prueba | Rol y Actor Evaluado | Operación Solicitada | Comportamiento Observado | Código HTTP | Dictamen |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `test_confirm_non_owner_forbidden` | Estudiante `B` | Confirmar reserva del Estudiante `A` | Solicitud rechazada por no coincidir la identidad. | `403 Forbidden` | **Aprobado** |
| `test_cancel_non_owner_forbidden` | Estudiante `B` | Cancelar reserva del Estudiante `A` | Solicitud rechazada por no coincidir la identidad. | `403 Forbidden` | **Aprobado** |
| `test_admin_substring_bypass_removed`| Usuario `"admin_fake@epis"` | Intentar eludir validación de propiedad | El token no otorga privilegios no firmados. | `403 Forbidden` | **Aprobado** |
| `test_unauthenticated_access` | Anónimo (Sin JWT) | Acceder a `/my-reservations` | Petición bloqueada en middleware. | `401 Unauthorized` | **Aprobado** |

Fuente: Pruebas unitarias en `tests/test_bookings.py` y `tests/test_authorization.py`.

El Cuadro 6.1 confirma que la plataforma garantiza la confidencialidad e integridad de las reservas conforme a los requerimientos de seguridad institucional.

---

## 7. Delimitación Técnica de Persistencia en el Entorno de Pruebas

En estricta observancia de los principios de transparencia académica de [`rules_doc.md`](../../rules_doc.md), se hace constar formalmente:
- **Entorno de Pruebas Automatizadas:** Las 187 pruebas del backend se ejecutaron utilizando **SQLite en memoria (`sqlite:///:memory:`) y en archivos temporales aislados**, gestionados a través de SQLAlchemy 2.0.
- **Mecanismo de Concurrencia:** Debido a que SQLite carece del bloqueo pesimista nativo `SELECT ... FOR UPDATE` de PostgreSQL, la sincronización concurrente en las pruebas se garantizó mediante el cerrojo multihilo de aplicación `_booking_lock = threading.Lock()`.
- **Producción:** La persistencia final está concebida para **PostgreSQL en Supabase**, cuya migración Alembic `004_booking_and_reservations.py` y políticas de RLS han sido modeladas pero no probadas activamente en vivo contra la base de datos en la nube durante el Sprint 05. Esta actividad se registrará como pendiente técnico para la homologación en Staging.

---

## 8. Guía de Reproducción de Pruebas en Entorno Local

Para verificar y reproducir de forma independiente los resultados documentados en este informe, ejecute los siguientes comandos en la raíz del repositorio:

### 8.1. Reproducción de Pruebas Backend (Pytest)
```bash
# Navegar al directorio de backend
cd aplicacion/backend

# Ejecutar la suite completa con medición de cobertura
python -m pytest -v --cov=app tests/

# Salida esperada:
# 187 passed, 1 warning in ~8.7s
# Required test coverage of 70.0% reached. Total coverage: 90.40%
```

### 8.2. Reproducción de Pruebas Frontend (Vitest)
```bash
# Navegar al directorio de frontend
cd aplicacion/frontend

# Ejecutar la suite completa con medición de cobertura v8
npm run test:coverage

# Salida esperada:
# Test Files  21 passed (21)
# Tests       265 passed (265)
# Lines coverage: 83.25%
```

### 8.3. Verificación de Formato y Linteo Estático
```bash
# Backend: Verificar linteo y formato con Ruff
cd aplicacion/backend
ruff check .
ruff format --check .

# Frontend: Verificar linteo y compilación de tipos
cd aplicacion/frontend
npm run lint
npm run build
```

---

## 9. Conclusiones Técnicas de Aseguramiento de Calidad

1. **Robustez Transaccional Demostrada:** Se comprobó de manera rigurosa que las reservas ratificadas y canceladas actualizan su estado y el aforo de la sesión sin tolerar condiciones de carrera ni sobrecupos.
2. **Cobertura de Código Sobresaliente:** Con un **90.40% en backend** y un **83.25% en frontend**, el proyecto supera holgadamente el umbral institucional del 70.0% (**RNF09**).
3. **Calidad Homologada en CI/CD:** El flujo de integración continua de GitHub Actions (`.github/workflows/ci.yml`) respalda la integridad de la base consolidada en `main`, certificando que el Sprint 05 se encuentra técnicamente concluido a nivel de desarrollo y listo para la revisión docente y homologación en Staging.
