# AUD-P2P-01 — Diagnóstico Integral del Sistema Web P2P EPIS UPT

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Repositorio Oficial:** `https://github.com/JMedina255/sistema_web_p2p.git`  
**Rama Base:** `main` (commit sincronizado: `4400a14`)  
**Rama de Auditoría:** `fix/auditoria-integral-qa-20261121`  
**Fecha de Evaluación:** 21 de noviembre de 2026  
**Auditor:** QA & Security Engineering Agent  

---

## 1. Estado del Repositorio y Sincronización Inicial

Al iniciar la sesión de auditoría, se evaluó la correspondencia entre el espacio de trabajo local y el repositorio remoto oficial:

1. **Estado inicial del árbol local:**
   - Rama activa: `main`
   - Hash local inicial: `6089ad5` (*Merge pull request #17 from JMedina255/fix/qa-auth-remediation*)
   - Estado de modificaciones: Árbol de trabajo completamente limpio (`nothing to commit, working tree clean`).
2. **Sincronización remota:**
   - Se ejecutó `git fetch origin --prune`.
   - Se detectó que el remoto `origin/main` se encontraba 2 commits por delante:
     - `63f5deb`: `fix(ci): subsanar linteo ruff en backend y error de tipos/eslint en frontend (PRE-LAB-01)`
     - `4400a14`: `Merge pull request #18 from JMedina255/fix/pre-lab-ci-validation`
3. **Actualización Fast-Forward:**
   - Se aplicó `git pull --ff-only origin main` actualizando el puntero local a `4400a14ef3b805179ce581b94d5aeb87d328ae61`.
   - Verificación de hash: `4400a14` idéntico en local y remoto.
4. **Aislamiento en Rama de Trabajo:**
   - Se creó y activó la rama de trabajo `fix/auditoria-integral-qa-20261121` derivada directamente de `4400a14`.

---

## 2. Inspección Arquitectónica y Organización de Código

### 2.1. Estructura General del Repositorio
* **Backend:** `aplicacion/backend/`
  - Framework: FastAPI 0.115+ con Python 3.13.
  - ORM y Migraciones: SQLAlchemy 2.0+ y Alembic 1.14+.
  - Capas: `api/v1/endpoints` (controladores), `services` (lógica de negocio y transacciones), `models` (entidades relacionales), `schemas` (validación Pydantic v2), `db` (sesiones, pooling, migraciones).
* **Frontend:** `aplicacion/frontend/`
  - SPA: React 19 + TypeScript 5.6+ empaquetada con Vite 8.3+.
  - Capas: `components` (vistas institucionales por rol), `services` (fachada dual mock/api), `context` (autenticación y sesión de usuario), `navigation` (rutas y RBAC).
* **Directorio Residual Detectado:**
  - En la raíz del repositorio coexiste una carpeta `frontend/` que únicamente alberga subdirectorios ignorados (`dist/` y `node_modules/`). No contiene archivos versionados en Git, pero representa una ambigüedad potencial para nuevos desarrolladores frente a la ruta canónica `aplicacion/frontend/`.
* **Alineación con SRS y SAD:**
  - Los módulos reflejan con fidelidad los 23 Casos de Uso del Catálogo Oficial (`CUS01` a `CUS23`) y los Requisitos Funcionales (`RF01` a `RF26`).

### 2.2. Configuración y Seguridad de Entorno
* **Gestión de Secretos:**
  - En `aplicacion/backend/app/core/config.py`, los campos sensibles (`DATABASE_URL`, `JWT_SECRET_KEY`, `SMTP_PASSWORD`, `SUPABASE_SERVICE_ROLE_KEY`) tienen la directiva `repr=False` de Pydantic, impidiendo su exposición en impresiones de consola o volcados de logs.
* **CORS:**
  - Configurado para los orígenes autorizados locales: `http://localhost:5173`, `http://127.0.0.1:5173` y `http://localhost:3000`.
* **Modo Estricto de Persistencia (`STRICT_DATABASE_MODE`):**
  - Configurado en `Settings`. En entorno de producción (`APP_ENV=production`), se auto-ajusta a `True`, forzando que cualquier transacción relacional aborte con `HTTP 503 DATABASE_UNAVAILABLE` ante caídas de la base de datos, erradicando la degradación silenciosa a memoria RAM.

---

## 3. Estado de la Base de Datos y Supabase

### 3.1. Migraciones Alembic
La cadena de revisiones de Alembic en `aplicacion/backend/app/db/migrations/versions/` es estrictamente secuencial y lineal:
1. `001_initial_curriculum_and_auth.py` (`20261019_001`)
2. `002_roles_and_profiles.py` (`20261023_002`)
3. `003_mentoring_offers.py` (`20261026_003`)
4. `004_booking_and_reservations.py` (`20261031_004`)
5. `005_closure_and_advanced_modules.py` (`20261113_005`)
6. `006_auth_rate_limits.py` (`20261116_006`)

### 3.2. Inspección del Entorno Supabase Remoto (Solo Lectura)
* Conexión técnica verificada: `SELECT 1` exitoso (latencia promedio: ~2686 ms).
* Versión activa en `alembic_version`: `20261113_005`.
* Total de tablas activas: 17 tablas institucionales.
* Estado de la migración `006_auth_rate_limits`: **Pendiente de aplicación en Supabase**. La tabla `auth_rate_limits` no existe en la base remota. La migración está completamente implementada y probada localmente, reservada para su ejecución en la ventana de mantenimiento autorizada.

---

## 4. Línea Base de Pruebas y Calidad de Código

### 4.1. Backend (Python / FastAPI)
* **Linter y Formato (Ruff 0.17+):**
  - `ruff check .` → **100% PASS** (Cero errores de linteo en 134 archivos).
  - `ruff format --check .` → **100% PASS** (Todos los archivos correctamente formateados).
* **Suite de Pruebas Automatizadas (Pytest 9.1+):**
  - Total ejecutadas: 377 pruebas.
  - Aprobadas: **376 PASS** (99.7%).
  - Omitidas justificadas: **1 SKIP** (`test_auth_rate_limit_postgresql_atomic_concurrency` requiere PostgreSQL multi-worker nativo con schema temporal; se ejecuta en entornos dedicados).
  - Fallidas: **0 FAIL**.
  - Cobertura de código: **83.66%** (Supera holgadamente el umbral normativo del 70.0% establecido en `pyproject.toml`).
  - Herramienta de Diagnóstico (`run_auth_diagnostics.py`): **16/16 PASS** (100% en los 16 escenarios de autenticación, OTP, JWT y seguridad).
  - Verificación Expo/Demo (`test_expo_ready.py`): **100% PASS** (Cursos, demandas, reservas y certificados operativos con HTTP 200).

### 4.2. Frontend (React / TypeScript / Vite)
* **Linter (ESLint):**
  - `npm run lint` → **0 errores / 0 advertencias**.
* **Compilación TypeScript (tsc -b && vite build):**
  - Compilación exitosa en 2.63s sin errores de tipado. Chunks generados en `dist/`.
* **Suite de Pruebas Automatizadas (Vitest 2.1+):**
  - Total inicial: 37 suites, 366 pruebas.
  - Estado inicial: **365 PASS / 1 FAIL**.
  - Fallo detectado: En `src/services/__tests__/bookingService.test.ts` (línea 862), la prueba `ejecuta confirmAttendance y cancelReservation mediante la fachada en modo mock` fallaba con `WINDOW_CLOSED_T24H`.
  - Causa del fallo: Fixture con fecha fija `fecha_inicio: '2026-11-20T10:00:00Z'` que al ejecutarse el 21/11/2026 quedaba en el pasado (diferencia `<= 24h`), disparando legítimamente la validación de ventana temporal RN-10.
  - Remediación aplicada: Se desacopló la fixture empleando tiempo dinámico relativo al reloj simulado (`new Date(mockNow + 72 * 3600 * 1000).toISOString()`).
  - Estado post-remediación: **37/37 suites PASS, 366/366 pruebas PASS (100%)**.
  - Cobertura de código Frontend: **82.44% Stmts / 75.82% Branch / 82.44% Lines**.

---

## 5. Resumen de Defectos y Riesgos Identificados

| ID | Módulo | Severidad | Descripción Sintética | Estado |
| :--- | :--- | :---: | :--- | :---: |
| **P2P-BUG-001** | Frontend / Reservas | **P1 (Alta)** | Fragilidad temporal en prueba unitaria de `bookingService.test.ts` por fecha estática vencida | **RESUELTO** |
| **P2P-BUG-002** | Repositorio / Estructura | **P2 (Media)** | Directorio residual `frontend/` en raíz con carpetas ignoradas `dist/` y `node_modules/` | **DOCUMENTADO** |
| **P2P-BUG-003** | Base de Datos / Supabase | **P2 (Media)** | Migración Alembic 006 pendiente de aplicación en base de producción Supabase | **DOCUMENTADO** |
| **P2P-BUG-004** | Backend / Dependencias | **P3 (Baja)** | Advertencias de deprecación externa (`fitz` → `pymupdf`, `starlette.testclient` → `httpx2`) | **DOCUMENTADO** |

---

## 6. Limitaciones de Verificación de la Sesión
1. **Entorno SMTP:** El envío real de correos electrónicos a buzones `@upt.pe` y `@virtual.upt.pe` está configurado con `SMTP_ENABLED=false` en desarrollo para evitar envíos no autorizados; el flujo completo de 5 momentos requiere validación manual con credenciales autorizadas en producción.
2. **Migración en Supabase:** Por directriz estricta de seguridad y control de cambios, no se aplicaron migraciones destructivas ni DDL sobre la base remota de producción sin ventana de mantenimiento programada.
