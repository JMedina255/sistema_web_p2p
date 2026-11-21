# AUD-P2P-01 — Inventario de Incidencias, Clasificación y Priorización

**Proyecto:** Sistema Web P2P de Mentorías Académicas EPIS UPT  
**Fecha:** 21 de noviembre de 2026  
**Rama de Intervención:** `fix/auditoria-integral-qa-20261121`  

---

## 1. Criterios de Clasificación y Priorización

| Prioridad | Definición | Acción Requerida |
| :--- | :--- | :--- |
| **P0 — Bloqueante** | Vulnerabilidad crítica, pérdida de datos o flujo esencial completamente inoperativo | Remediación inmediata e incondicional |
| **P1 — Alta** | Funcionalidad principal incorrecta, fallo de autorización o error reproducible importante | Remediación prioritaria en la sesión actual |
| **P2 — Media** | Defecto funcional parcial, validación incorrecta, inconsistencia de interfaz o riesgo operativo | Planificación y corrección controlada |
| **P3 — Baja** | Mejora menor, deuda técnica no crítica o advertencia cosmética/informativa | Registro para iteraciones posteriores |

---

## 2. Inventario Detallado de Incidencias

### P2P-BUG-001 — Fragilidad Temporal en Batería de Pruebas de Desistimiento de Reservas (Frontend)
* **Identificador:** `P2P-BUG-001`
* **Módulo Afectado:** Frontend — Servicio de Reservas (`bookingService.ts` / `bookingService.test.ts`).
* **Requisito / Caso de Uso Relacionado:** `RF14` / `CUS17` / `RN-08` / `RN-10` (Desistimiento voluntario de reservas con corte perentorio a T-24h).
* **Prioridad:** **P1 — Alta** (Causa fallo en la suite de pruebas automatizadas y rompería el pipeline de CI en ejecuciones posteriores al 20/11/2026).
* **Descripción Precisa:**
  En la prueba unitaria `bookingService (T-23 / Sprint 05 Fase 1) > 4. Fachada bookingService (Modos mock y api) > ejecuta confirmAttendance y cancelReservation mediante la fachada en modo mock`, se invocaba `bookingService.seedBooking(...)` inyectando una reserva con `fecha_inicio: '2026-11-20T10:00:00Z'` sin fijar un reloj simulado (`bookingService.setCurrentTime(...)`). Al ejecutarse en tiempo real el 21/11/2026, la diferencia `diffMs = startTime - now` resultaba negativa (`-15 horas`), cayendo en la condición `diffMs <= 24 * 3600 * 1000` y arrojando la excepción `BookingException: WINDOW_CLOSED_T24H`.
* **Pasos para Reproducir:**
  1. Ubicarse en `aplicacion/frontend`.
  2. Ejecutar `npx vitest run src/services/__tests__/bookingService.test.ts`.
  3. Observar el fallo en la aserción de `cancelReservation(888)`.
* **Resultado Esperado:** La prueba debe verificar la transición de estado a `CANCELADA_USUARIO` empleando una fecha de sesión válida en el futuro respecto a la hora de prueba.
* **Resultado Obtenido (Inicial):**
  ```
  BookingException: WINDOW_CLOSED_T24H: El desistimiento voluntario debe realizarse con más de 24 horas de anticipación al inicio de la sesión (RN-08 / RN-10).
  at MockBookingAdapter.cancelReservation (src/services/bookingService.ts:982:15)
  at Object.cancelReservation (src/services/bookingService.ts:1159:34)
  at src/services/__tests__/bookingService.test.ts:862:46
  ```
* **Causa Raíz:** Uso de timestamp estático absoluto `2026-11-20T10:00:00Z` en datos de prueba (fixture "bomba de tiempo"), susceptible al avance del calendario real sin fijar el reloj simulado o calcular el delta relativo.
* **Archivos Implicados:** `aplicacion/frontend/src/services/__tests__/bookingService.test.ts`.
* **Propuesta de Corrección:** Calcular la fecha de inicio dinámicamente como `new Date(mockNow + 72 * 3600 * 1000).toISOString()` para garantizar que la sesión semillada siempre esté a +72 horas del reloj del adaptador, emulando la conducta determinista de `reserveSeat()`.
* **Prueba de Regresión:** Reejecución de `bookingService.test.ts` y de la suite completa de 37 archivos en Vitest.
* **Estado Actual:** **RESUELTO** (Commit: `8be2a28`).

---

### P2P-BUG-002 — Coexistencia de Directorio Residual `frontend/` en Raíz del Proyecto
* **Identificador:** `P2P-BUG-002`
* **Módulo Afectado:** Arquitectura y Estructura del Repositorio.
* **Requisito / Caso de Uso Relacionado:** RNF09 (Mantenibilidad y Estructura Canónica del Proyecto).
* **Prioridad:** **P2 — Media**.
* **Descripción Precisa:**
  En la raíz del proyecto existe la carpeta `frontend/` que contiene subdirectorios locales ignorados (`dist/` y `node_modules/`), remanentes de una etapa previa a la consolidación en `aplicacion/frontend/`. Si bien `.gitignore` incluye `frontend/dist/` y `frontend/node_modules/` y no existen archivos rastreados en Git, induce a confusión para desarrolladores que ejecuten comandos `npm` desde la raíz.
* **Pasos para Reproducir:**
  1. Ejecutar `Get-ChildItem frontend` en la terminal.
  2. Verificar la presencia de `dist/` y `node_modules/`.
* **Resultado Esperado:** Estructura unificada exclusivamente bajo `aplicacion/frontend/`.
* **Resultado Obtenido:** Coexistencia de carpeta raíz residual.
* **Causa Raíz:** Migración histórica de carpetas sin remoción de artefactos no rastreados en el entorno de desarrollo local.
* **Archivos Implicados:** `frontend/` (directorio no rastreado).
* **Propuesta de Corrección:** Conservar la exclusión en `.gitignore` y documentar formalmente la ruta canónica en `AUD-P2P-01-DIAGNOSTICO.md`. No requiere borrado destructivo riesgoso.
* **Estado Actual:** **DOCUMENTADO / RIESGO MITIGADO**.

---

### P2P-BUG-003 — Desalineación de Migración 006 en Supabase de Producción
* **Identificador:** `P2P-BUG-003`
* **Módulo Afectado:** Base de Datos / Persistencia de Autenticación.
* **Requisito / Caso de Uso Relacionado:** RNF01, RNF02, RNF07 / Migración Alembic `006_auth_rate_limits.py`.
* **Prioridad:** **P2 — Media** (Riesgo operativo condicionado a despliegue).
* **Descripción Precisa:**
  La migración Alembic `006_auth_rate_limits.py` (`20261116_006`) define la tabla `auth_rate_limits`, políticas RLS y triggers de unicidad. La base de producción en Supabase se encuentra actualmente en la versión `20261113_005` y no cuenta con dicha tabla. Si se desplegase el backend en modo de persistencia estricta (`STRICT_DATABASE_MODE=true` o `APP_ENV=production`) sin haber ejecutado `alembic upgrade head`, los endpoints de autenticación que evalúan el rate limit en base de datos arrojarían `HTTP 503 DATABASE_UNAVAILABLE`.
* **Pasos para Reproducir:**
  1. Conectar a Supabase en modo solo lectura.
  2. Consultar `SELECT version_num FROM alembic_version`.
  3. Comprobar que el valor es `20261113_005`.
* **Resultado Esperado:** Base de datos sincronizada con `20261116_006` antes de habilitar el backend en producción estricta.
* **Resultado Obtenido:** Migración preparada en código pero pendiente de aplicación en base remota.
* **Causa Raíz:** Política de control de cambios: las migraciones remotas en producción no se aplican en turnos automatizados no programados.
* **Archivos Implicados:** `aplicacion/backend/app/db/migrations/versions/006_auth_rate_limits.py`.
* **Propuesta de Corrección:** Ejecutar `alembic upgrade head` en la ventana de mantenimiento autorizada, previa creación de respaldo, conforme al protocolo documentado en `INFORME_ESTABILIZACION_QA_AUTH_02B.md`.
* **Estado Actual:** **DOCUMENTADO / PENDIENTE DE VENTANA DE MANTENIMIENTO**.

---

### P2P-BUG-004 — Advertencias de Deprecación Externa en Suites de Pruebas Backend
* **Identificador:** `P2P-BUG-004`
* **Módulo Afectado:** Backend — Configuración de Pruebas y Librerías de Terceros.
* **Requisito / Caso de Uso Relacionado:** RNF09 (Mantenibilidad).
* **Prioridad:** **P3 — Baja**.
* **Descripción Precisa:**
  Durante la ejecución de Pytest se registran 18 advertencias de deprecación provenientes de dependencias externas:
  - `StarletteDeprecationWarning`: Uso de `httpx` con `starlette.testclient` deprecado en favor de `httpx2`.
  - `FutureWarning`: El módulo `fitz` está deprecado y sugiere `import pymupdf`.
  - `ResourceWarning`: Conexión de SQLite no cerrada explícitamente en tests de inspección de AST.
* **Pasos para Reproducir:**
  1. Ejecutar `pytest -rW` en `aplicacion/backend`.
  2. Observar la sección de warnings al final de la suite.
* **Resultado Esperado:** 0 advertencias de deprecación.
* **Resultado Obtenido:** 18 warnings informativos.
* **Causa Raíz:** Evolución de versiones de dependencias (`PyMuPDF` 1.24+, `Starlette` 0.40+).
* **Archivos Implicados:** `aplicacion/backend/app/services/certificate_service.py`, `pyproject.toml`.
* **Propuesta de Corrección:** Reemplazar `import fitz` por `import pymupdf` y añadir filtros de warning en `pyproject.toml` para Starlette en la siguiente iteración de deuda técnica.
* **Estado Actual:** **DOCUMENTADO / DEUDA TÉCNICA CONTROLADA**.
