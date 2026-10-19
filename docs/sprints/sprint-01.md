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
| **T-01** | Configurar entorno React, FastAPI y Supabase. | Joan | 4 | En curso (H1 verificado) | H1 / H2 |
| **T-02** | Desarrollar interfaz de acceso y OTP de prueba. | Joan | 2 | Pendiente | H3 |
| **T-03** | Implementar API de autenticación y OTP de prueba. | Renzo | 4 | Pendiente (Coordinación) | Externo a Joan |
| **T-06** | Configurar integración continua y pruebas iniciales. | Joan | 3 | Pendiente | H4 |
| **T-07** | Implementar políticas RLS iniciales. | Renzo | 3 | Pendiente (Coordinación) | Externo a Joan |
| **T-09** | Crear tablas y datos iniciales del catálogo curricular. | Renzo | 2 | Pendiente (Coordinación) | Externo a Joan |

Fuente: Elaboración propia con base en el documento canónico de planificación `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` y tabla 5.2 de la planificación del Grupo 03.

Como se evidencia en el cuadro anterior, el alcance asignado a Joan se descompone en 9 horas distribuidas en T-01, T-02 y T-06. La tarea T-01 se subdivide técnicamente en dos hitos operativos (**H1**: estructura base React–FastAPI y comunicación health; **H2**: conexión técnica inicial con Supabase/PostgreSQL) para garantizar incrementos verificables e independientes.

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

## 3. Comandos Reproducibles para Puesta en Marcha Local

### Backend (FastAPI):
```bash
# 1. Crear e inicializar entorno virtual
cd aplicacion/backend
python -m venv .venv
.\.venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar pruebas unitarias
pytest tests/ -v

# 4. Iniciar servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
La documentación interactiva OpenAPI queda disponible en `http://localhost:8000/docs`.

### Frontend (React + Vite):
```bash
# 1. Instalar dependencias
cd aplicacion/frontend
npm install

# 2. Validar linter y construcción
npm run lint
npm run build

# 3. Iniciar servidor de desarrollo
npm run dev
```
La aplicación queda accesible en `http://localhost:5173/`.

---

## 4. Próximos Pasos y Pendientes

1. **Hito 2 (H2: T-01, Parte 2):** Configurar la cadena de conexión a PostgreSQL/Supabase mediante `psycopg 3` y SQLAlchemy, preparar el entorno de migraciones con Alembic e implementar el endpoint de verificación técnica `GET /api/v1/health/db`.
2. **Hito 3 (H3: T-02):** Implementar la interfaz institucional de acceso con correo `@upt.pe` y OTP temporal de prueba (5 minutos) en `aplicacion/frontend`.
3. **Hito 4 (H4: T-06):** Configurar el flujo de integración continua en `.github/workflows/ci.yml` con cobertura de pruebas.
