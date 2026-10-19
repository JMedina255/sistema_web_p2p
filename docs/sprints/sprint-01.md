# Bitácora de Ejecución — Sprint 1: Base Técnica y Acceso Inicial

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería (EPIS)  
**Semestre Académico:** 2026-II  
**Equipo:** Grupo 03 — Joan Cristian Medina Quispe (Joan) y Renzo Antonio Antayhua Mamani (Renzo)  
**Rama de trabajo:** `feat/sprint-01-base-acceso-ci`  
**Fecha de corte:** 19/10/2026  

---

## 1. Visión General y Alcance del Sprint 1

El **Sprint 1** tiene como objetivo fundamental sentar la infraestructura base del sistema web P2P de mentorías académicas, desacoplando estrictamente el frontend SPA y el backend API RESTful (conforme a los requerimientos no funcionales de mantenibilidad **RNF09** e ISO/IEC 25010), habilitar la verificación de estado operativa (*health check*) e iniciar los mecanismos de acceso y autenticación institucional de prueba (**RF01**, **CUS01**, **RNF01**).

A continuación, se presenta la matriz canónica de asignación y esfuerzo planificado para las actividades del Sprint 1, distinguiendo la distribución técnica entre los integrantes del equipo:

### Cuadro 1.1: Actividades y Compromisos de Desarrollo del Sprint 1

| ID | Actividad | Responsable | Estimación Planificada (h) | Estado Técnico | Hito Asociado |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **T-01** | Configurar entorno React, FastAPI y Supabase. | Joan | 4 | Verificado localmente | H1 / H2 |
| **T-02** | Desarrollar interfaz de acceso y OTP de prueba. | Joan | 2 | Pendiente | H3 |
| **T-03** | Implementar API de autenticación y OTP de prueba. | Renzo | 4 | Pendiente (Coordinación) | Externo a Joan |
| **T-06** | Configurar integración continua y pruebas iniciales. | Joan | 3 | Pendiente | H4 |
| **T-07** | Implementar políticas RLS iniciales. | Renzo | 3 | Pendiente (Coordinación) | Externo a Joan |
| **T-09** | Crear tablas y datos iniciales del catálogo curricular. | Renzo | 2 | Pendiente (Coordinación) | Externo a Joan |

Fuente: Elaboración propia con base en el documento canónico de planificación `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` y tabla 5.2 de la planificación del Grupo 03.

Como se evidencia en el cuadro anterior, el alcance asignado a Joan se descompone en 9 horas distribuidas en T-01, T-02 y T-06. La tarea T-01 se subdividió técnicamente en dos hitos operativos (**H1**: estructura base React–FastAPI y comunicación health; **H2**: conexión técnica inicial con Supabase/PostgreSQL) para garantizar incrementos verificables e independientes. Ambos hitos se encuentran formalmente completados y verificados en el entorno de desarrollo local.

---

## 2. Registro de Ejecución — Hito 1 (H1: T-01, Parte 1)

### 2.1. Alcance Implementado
- **Directorio de la aplicación:** Se creó la raíz `aplicacion/`, preservando el directorio `frontend/` en la raíz como maqueta de referencia visual.
- **Backend API (`aplicacion/backend/`):**
  - Estructura canónica según el SAD: `app/api/v1/endpoints`, `app/core`, `app/services`, `app/models`, `app/db`.
  - Configuración centralizada con `pydantic-settings` (`app/core/config.py`), admitiendo variables de entorno y soporte de CORS.
  - Implementación del endpoint autónomo `GET /api/v1/health` en `app/api/v1/endpoints/health.py`, que responde HTTP 200 con `{"status":"ok", "service":"backend", ...}` sin depender de la base de datos.
  - Creación de `.env.example` y `requirements.txt`.
  - Pruebas automatizadas unitarias con `pytest` y `fastapi.testclient.TestClient`.
- **Frontend SPA (`aplicacion/frontend/`):**
  - Aplicación React 19 con TypeScript estricto y empaquetador Vite.
  - Servicio tipado `src/services/apiClient.ts` que consume `GET /api/v1/health` mediante `VITE_API_BASE_URL`.
  - Componente interactivo `HealthStatus.tsx` con estados de carga (`loading`), éxito (`success` con latencia en ms) y error (`error` con diagnóstico guiado y botón de reintento).
  - Interfaz institucional UPT sobria con paleta corporativa Navy (`#1C2A59`) y Dorado (`#B99451`).
- **Control de versiones:** Actualización de `.gitignore` para excluir entornos virtuales `.venv`, cachés de Python y `node_modules`, preservando archivos `.env.example`.

### 2.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se documenta la relación de comandos ejecutados en el entorno de desarrollo y los resultados reales obtenidos:

### Cuadro 2.1: Matriz de Verificación y Comprobaciones Técnicas del Hito 1

| Componente | Comando Reproducible | Propósito de la Prueba | Resultado Observado | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **Backend** | `pytest aplicacion/backend/tests -v` | Validar endpoint `/api/v1/health` y metadatos de `/` | 2 passed in 0.60s | ✅ Exitoso |
| **Frontend** | `npm run build` (en `aplicacion/frontend`) | Compilación TypeScript y bundle Vite | 36 módulos transformados en 1.12s, 0 errores | ✅ Exitoso |
| **Frontend** | `npm run lint` (en `aplicacion/frontend`) | Inspección de reglas ESLint para React/TS | 0 errores, 0 advertencias | ✅ Exitoso |
| **Entorno** | `git status` | Verificación de archivos rastreados y exclusión de artefactos | Limpio de binarios/caché; solo código fuente | ✅ Exitoso |

Fuente: Elaboración propia a partir de las pruebas de consola ejecutadas localmente.

El cuadro previo confirma que la solución cumple cabalmente con los criterios de aceptación del Hito 1: tanto el backend como el frontend compilan, pasan sus pruebas automatizadas y se encuentran preparados para la integración con la capa de persistencia en el Hito 2.

---

## 3. Registro de Ejecución — Hito 2 (H2: T-01, Parte 2)

### 3.1. Alcance Implementado
- **Dependencias de persistencia:** Incorporación y fijación de versiones compatibles en `requirements.txt`:
  - `SQLAlchemy>=2.0.35` (versión instalada: 2.1.5)
  - `psycopg[binary]>=3.2.0` (versión instalada: 3.3.6 con binarios)
  - `alembic>=1.13.0` (versión instalada: 1.20.0)
- **Gestión segura de configuración (`app/core/config.py`):**
  - Carga segura de `DATABASE_URL` desde `aplicacion/backend/.env`.
  - Definición con `Field(default=None, repr=False)` para evitar que la cadena de conexión o contraseñas se impriman en logs, trazas o consolas.
  - Propiedad calculada `sync_database_url` que formatea automáticamente la URL al dialecto `postgresql+psycopg://`.
  - Configuración del timeout de conexión `DB_CONNECT_TIMEOUT = 5` segundos.
- **Conexión diferida y gestión de recursos (`app/db/session.py`):**
  - Creación perezosa (*lazy*) del motor SQLAlchemy en `get_engine()`: FastAPI puede inicializarse aun si no hay base de datos configurada.
  - Implementación de `close_engine()` para liberar conexiones activas en el evento de cierre (`lifespan` en `app/main.py`).
  - Función de sanitización de errores `sanitize_db_error()` para prevenir la exposición de credenciales y rutas internas ante fallos de red o autenticación.
  - Función `test_db_connection()` que ejecuta `SELECT 1` y mide la latencia de respuesta en milisegundos.
- **Preparación de Alembic (`app/db/migrations` y `alembic.ini`):**
  - Inicialización sin creación de tablas de negocio (reservadas para T-09 de Renzo) ni ejecución automática de migraciones al arrancar el servidor.
  - `env.py` configurado para enlazar dinámicamente con `settings.sync_database_url` y `Base.metadata`.
- **Endpoints de diagnóstico y monitoreo (`app/api/v1/endpoints/health.py`):**
  - `GET /api/v1/health`: Preservado 100% independiente de la base de datos (HTTP 200 garantizado si el proceso está activo).
  - `GET /api/v1/health/db`: Disponible únicamente en desarrollo (`APP_ENV=development`). Ejecuta `SELECT 1`, devolviendo HTTP 200 con estado `"connected"` y latencia si es exitoso, HTTP 503 con detalle sanitizado si la conexión falla o falta configuración, y HTTP 404 fuera de desarrollo.
- **Integración con Frontend React (`aplicacion/frontend`):**
  - Métodos `fetchHealth()` y `fetchDbHealth()` en `src/services/apiClient.ts`.
  - Tarjeta de monitoreo en `HealthStatus.tsx` que despliega el estado de conexión del motor PostgreSQL (Supabase - proyecto `p2p-epis-dev`) junto con su latencia en ms.

### 3.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se documentan las pruebas técnicas efectuadas para validar los diferentes escenarios operativos de la capa de persistencia:

### Cuadro 3.1: Matriz de Verificación y Comprobaciones Técnicas del Hito 2

| Escenario Evaluado | Método / Comando de Comprobación | Comportamiento Esperado | Resultado Real Observado | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **Conexión Real Supabase** | `test_db_connection()` contra proyecto `p2p-epis-dev` | Ejecutar `SELECT 1` con Session Pooler y devolver 200 | `Connected: True \| Latency: 2828.53 ms` (HTTP 200) | ✅ Exitoso |
| **Configuración Ausente** | `GET /api/v1/health/db` con `DATABASE_URL=None` | Respuesta controlada HTTP 503 con mensaje sanitizado | `503 error: DATABASE_URL no configurada en el entorno` | ✅ Exitoso |
| **Fallo Controlado de Conexión** | `GET /api/v1/health/db` ante rechazo de conexión | Respuesta HTTP 503 sin fuga de contraseñas ni URLs | `503 error: Conexión rechazada...` (0 trazas de secretos) | ✅ Exitoso |
| **Aislamiento de Health** | `GET /api/v1/health` sin base de datos | HTTP 200 independiente del estado de la base de datos | `200 ok` (FastAPI continúa plenamente operativo) | ✅ Exitoso |
| **Restricción de Entorno** | `GET /api/v1/health/db` con `APP_ENV=production` | Denegar acceso al endpoint de diagnóstico fuera de dev | `HTTP 404 Not Found` | ✅ Exitoso |
| **Alembic Operativo** | `alembic current` contra PostgreSQL | Detectar dialecto PostgresqlImpl sin errores | `Context impl PostgresqlImpl. Will assume transactional DDL.` | ✅ Exitoso |
| **Suite de Pruebas Unitarias** | `pytest aplicacion/backend/tests -v` | Validar los 7 casos de prueba automatizados | `7 passed in 1.08s` | ✅ Exitoso |
| **Frontend Build & Lint** | `npm run lint && npm run build` | Compilar TypeScript y verificar estilos de código | 36 módulos compilados en 1.10s, 0 errores, 0 warnings | ✅ Exitoso |

Fuente: Elaboración propia a partir de las comprobaciones automatizadas y pruebas de consola ejecutadas localmente.

Los resultados verifican que la infraestructura de conexión a Supabase opera conforme a las directrices de seguridad y resiliencia del SAD: no expone credenciales, gestiona tiempos de espera (timeout), desacopla la salud de la API respecto a la persistencia y bloquea accesos no autorizados a rutas de diagnóstico fuera de desarrollo.

---

## 4. Comandos Reproducibles para Puesta en Marcha Local

### Backend (FastAPI + PostgreSQL Supabase):
```bash
# 1. Acceder al directorio e inicializar entorno virtual
cd aplicacion/backend
.\.venv\Scripts\activate

# 2. Instalar dependencias fijadas
pip install -r requirements.txt

# 3. Comprobar estado de migraciones con Alembic
alembic current

# 4. Ejecutar suite de pruebas unitarias
pytest tests/ -v

# 5. Iniciar servidor FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Endpoint de salud general: `http://localhost:8000/api/v1/health`
- Endpoint de diagnóstico de base de datos (dev): `http://localhost:8000/api/v1/health/db`
- Documentación Swagger: `http://localhost:8000/docs`

### Frontend (React + Vite):
```bash
# 1. Acceder al directorio
cd aplicacion/frontend

# 2. Instalar dependencias y validar
npm install
npm run lint
npm run build

# 3. Iniciar servidor de desarrollo
npm run dev
```
- Aplicación cliente: `http://localhost:5173/`

---

## 5. Próximos Pasos y Pendientes

1. **Hito 3 (H3: T-02):** Desarrollar la interfaz institucional de acceso con correo `@upt.pe` y OTP temporal de prueba (5 minutos) en `aplicacion/frontend` conforme a **RF01**, **CUS01** y **RNF01**.
2. **Hito 4 (H4: T-06):** Configurar el flujo de integración continua en `.github/workflows/ci.yml` ejecutando lint, build y pruebas de ambos componentes con cobertura mínima orientada a RNF09.
3. **Coordinación externa con Renzo:** Integración posterior de la API OTP real (**T-03**), políticas de seguridad a nivel de fila RLS (**T-07**) y tablas del catálogo curricular (**T-09**).
