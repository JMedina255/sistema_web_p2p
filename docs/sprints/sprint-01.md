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

El **Sprint 1** tiene como objetivo fundamental sentar la infraestructura base del sistema web P2P de mentorías académicas, desacoplando estrictamente el frontend SPA y el backend API RESTful (conforme a los requerimientos no funcionales de mantenibilidad **RNF09**), habilitar la verificación de estado operativa (*health check*) e iniciar los mecanismos de acceso y autenticación institucional de prueba (**RF01**, **CUS01**, **RNF01**).

A continuación, se presenta la matriz canónica de asignación y esfuerzo planificado para las actividades del Sprint 1, distinguiendo la distribución técnica entre los integrantes del equipo:

### Cuadro 1.1: Actividades y Compromisos de Desarrollo del Sprint 1

| ID | Actividad | Responsable | Estimación Planificada (h) | Estado Técnico | Hito Asociado |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **T-01** | Configurar entorno React, FastAPI y Supabase. | Joan | 4 | Verificado localmente | H1 / H2 |
| **T-02** | Desarrollar interfaz de acceso y OTP de prueba. | Joan | 2 | Verificado localmente (Mock Dev) | H3 |
| **T-03** | Implementar API de autenticación y OTP de prueba. | Renzo | 4 | Pendiente (Coordinación) | Externo a Joan |
| **T-06** | Configurar integración continua y pruebas iniciales. | Joan | 3 | Verificado en CI remoto (`8f8a75c`) | H4 |
| **T-07** | Implementar políticas RLS iniciales. | Renzo | 3 | Pendiente (Coordinación) | Externo a Joan |
| **T-09** | Crear tablas y datos iniciales del catálogo curricular. | Renzo | 2 | Pendiente (Coordinación) | Externo a Joan |

Fuente: Elaboración propia con base en el documento canónico de planificación `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` y tabla 5.2 de la planificación del Grupo 03.

Como se evidencia en el cuadro anterior, el alcance asignado a Joan se descompone en 9 horas distribuidas en T-01, T-02 y T-06. La totalidad de dichas tareas (**H1** y **H2** para T-01, **H3** para T-02 y **H4** para T-06) han sido completadas y verificadas tanto localmente como en el flujo de GitHub Actions (run [`39331555735`](https://github.com/JMedina255/sistema_web_p2p/actions/runs/39331555735)), aportando evidencia de pruebas y cobertura para el alcance implementado conforme a la meta de **RNF09** ($\ge 70\%$). La tarea T-02 se mantiene con interfaz de acceso simulado mediante adaptador mock en desarrollo. Las actividades T-03, T-07 y T-09 corresponden a Renzo y quedan como dependencias de integración pendientes, por lo que el Sprint 1 continúa en curso y no se declara concluido en su totalidad.

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
- **Dependencias de persistencia:** Fijación estricta de versiones exactas (`==`) en `requirements.txt` (antecedente histórico: durante el planteamiento preliminar de H2 se listaron rangos `>=`, los cuales fueron formalmente sustituidos por versiones exactas en el commit `d6bc275` tras su comprobación en el entorno virtual):
  - `sqlalchemy==2.0.44` (fijada tras comprobación en `.venv`; antecedente de rango: `>=2.0.35`)
  - `psycopg[binary]==3.3.6` (fijada con binarios; antecedente de rango: `>=3.2.0`)
  - `alembic==1.20.0` (fijada tras verificación; antecedente de rango: `>=1.13.0`)
  - Dependencias complementarias exactas: `pydantic==2.12.5`, `pydantic-settings==2.13.1`, `fastapi==0.135.1`, `uvicorn[standard]==0.41.0`, `httpx==0.28.1`, `pytest==9.1.1`, `pytest-cov==7.1.0` y `ruff==0.17.1`.
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

## 4. Registro de Ejecución — Hito 3 (H3: T-02: Interfaz de Acceso y OTP de Prueba)

### 4.1. Alcance Implementado
- **Componente de Acceso Interactivo (`aplicacion/frontend/src/components/LoginOtpView.tsx`):**
  - Flujo de autenticación en dos pasos ordenados conforme a **CUS01** y **RF01**:
    1. **Paso 1 (Identificación Institucional):** Entrada de correo electrónico con validación estricta de terminación `@upt.pe` y formato RFC de usuario. Atajos rápidos de prueba para correos de Joan (`2022074255@upt.pe`), Renzo (`2022073504@upt.pe`) y un correo no institucional (`estudiante@gmail.com`) para pruebas de rechazo.
    2. **Paso 2 (Desafío OTP Temporal):** Entrada numérica de 6 dígitos conservada estrictamente como texto (`string`) para permitir ceros iniciales (p. ej., `012345`). Incluye cálculo de vigencia restante directamente contra la marca temporal `expiresAt` (ventana máxima de 5 minutos conforme a **RNF01**).
    3. **Paso 3 (Confirmación Mínima de Acceso):** Vista informativa que certifica la validación exitosa del código, indicando el correo verificado, la estampa de tiempo y el modo utilizado (`Acceso de prueba — simulación`). No implementa consentimiento informado ni paneles de usuario finales (reservados para T-04 y T-05).
  - **Usabilidad y Accesibilidad:** Etiquetas semánticas vinculadas mediante `htmlFor`, atributos `aria-live="polite"` para alertas, soporte completo de navegación por teclado (`Enter` para avanzar o verificar) y botones con retroalimentación visual de deshabilitación y carga (`disabled` y spinners).
  - **Control de Ciclo de Vida y Cooldown:** Temporizador regresivo de 60 segundos antes de habilitar el botón de reenvío de código, conforme a **CUS01**. Opción explícita de *"Cambiar correo"* que descarta inmediatamente el desafío activo en el cliente y en el servicio.

### 4.2. Modo de Autenticación y Adaptador Mock en Desarrollo
- **Servicio Centralizado (`aplicacion/frontend/src/services/authService.ts`):**
  - **Modo utilizado:** Adaptador MOCK en memoria (`MockAuthAdapter`), activado de manera explícita y exclusiva en entorno de desarrollo local (`import.meta.env.DEV`).
  - **Aviso visual permanente:** Banner superior de alto contraste con el mensaje *"Acceso de prueba — simulación. La API de autenticación real (T-03) está en desarrollo por Renzo. Los códigos no son enviados a correos reales."*
  - **Escenarios reproducibles predecibles:** Código válido predeterminado `123456`; código rotativo tras reenvío `654321`; código de prueba rápida de expiración inmediata `000000`.
  - **Garantías de seguridad:** Cada reenvío o nueva solicitud invalida inmediatamente el código anterior. La verificación exitosa marca el código como consumido impidiendo su reutilización. No emite tokens JWT, no guarda sesiones ficticias en almacenamiento local ni realiza consultas a datos reales de Supabase. El adaptador se desactiva estrictamente fuera de desarrollo arrojando `MOCK_DISABLED` y no opera como fallback silencioso ante caídas de la API real.

### 4.3. Contrato Propuesto de Integración con T-03 (Renzo)
Debido a que la API de backend (T-03) se encuentra en desarrollo por Renzo, el servicio desacoplado formaliza la propuesta de contrato de comunicación mediante interfaces TypeScript:
- `POST /api/v1/auth/otp/request`: Recibe `RequestOtpPayload { email: string }` y retorna `RequestOtpResponse { challengeId: string, email: string, expiresAt: string, cooldownSeconds: number, message: string, isMock: boolean }`.
- `POST /api/v1/auth/otp/verify`: Recibe `VerifyOtpPayload { challengeId: string, otp: string }` y retorna `VerifyOtpResponse { success: boolean, email: string, verifiedAt: string, mode: 'mock' | 'api', message: string }`.
- `POST /api/v1/auth/otp/resend`: Recibe `ResendOtpPayload { challengeId: string }` y retorna `RequestOtpResponse`.
- **Excepciones tipadas (`AuthErrorCode`):** `INVALID_EMAIL`, `NON_UPT_DOMAIN`, `CHALLENGE_NOT_FOUND`, `OTP_EXPIRED`, `OTP_INVALID`, `OTP_ALREADY_USED`, `COOLDOWN_ACTIVE`, `NETWORK_ERROR`, `MOCK_DISABLED`.

*Nota de coordinación:* Este contrato queda registrado como propuesta formal para su homologación con Renzo durante la culminación de T-03.

### 4.4. Comprobaciones Realizadas y Resultados Observados

A continuación, se presenta la matriz detallada de los 11 escenarios de prueba ejecutados sobre el servicio de autenticación y la interfaz de usuario:

### Cuadro 4.1: Matriz de Verificación de Escenarios de Acceso y OTP (Hito 3)

| # | Escenario Evaluado | Datos de Entrada / Condición | Comportamiento Esperado | Resultado Real Observado | Estado |
| :-: | :--- | :--- | :--- | :--- | :---: |
| **01** | Correo institucional permitido | `2022074255@upt.pe` | Emisión exitosa de desafío de 5 min con cooldown de 60s | Genera `challengeId` (`CHAL-DEV-101-...`), `isMock: true` | ✅ Exitoso |
| **02** | Dominio no institucional rechazado | `usuario@gmail.com` | Rechazo inmediato con error de dominio no permitido | Excepción `NON_UPT_DOMAIN`: dominio debe ser `@upt.pe` | ✅ Exitoso |
| **03** | Formato de correo inválido | `@upt.pe` (sin parte local) | Rechazo por formato incorrecto antes del envío | Excepción `INVALID_EMAIL`: formato institucional inválido | ✅ Exitoso |
| **04** | Código OTP incompleto | Desafío activo, OTP: `"123"` | Rechazo por longitud inferior a 6 caracteres numéricos | Excepción `OTP_INVALID`: código debe contener 6 dígitos | ✅ Exitoso |
| **05** | Código OTP incorrecto | Desafío activo, OTP: `"999999"` | Rechazo con retroalimentación de código no coincidente | Excepción `OTP_INVALID`: código OTP incorrecto | ✅ Exitoso |
| **06** | Código OTP vencido | OTP `"000000"` o $t > \text{expiresAt}$ | Rechazo por vencimiento del plazo máximo de 5 min (RNF01) | Excepción `OTP_EXPIRED`: código de verificación ha expirado | ✅ Exitoso |
| **07** | Código OTP válido | Desafío activo, OTP: `"123456"` | Verificación exitosa en modo mock y confirmación | `success: true`, `mode: 'mock'`, marca temporal registrada | ✅ Exitoso |
| **08** | Código OTP ya consumido | Reintento con OTP verificado | Rechazo por consumo previo del código | Excepción `OTP_ALREADY_USED`: código ya utilizado previamente | ✅ Exitoso |
| **09a** | Cooldown de reenvío activo | Reenvío antes de los 60s | Bloqueo temporal informando segundos restantes | Excepción `COOLDOWN_ACTIVE`: espera de cooldown requerida | ✅ Exitoso |
| **09b** | Invalidación por nueva emisión | Verificación con desafío anterior | Desafío previo invalidado al emitir uno nuevo | Excepción `CHALLENGE_NOT_FOUND`: desafío caducado/descartado | ✅ Exitoso |
| **10** | Cambio de correo por usuario | Acción *"Cambiar correo"* | Descarte total del desafío en memoria | Excepción `CHALLENGE_NOT_FOUND` al intentar verificarlo | ✅ Exitoso |
| **11** | Mock fuera de desarrollo | `NODE_ENV=production` | Bloqueo absoluto del adaptador simulado | Excepción `MOCK_DISABLED`: mock deshabilitado fuera de dev | ✅ Exitoso |
| **12** | Calidad de código Frontend | `npm run lint && npm run build` | Compilación limpia de TypeScript y Vite sin advertencias | 38 módulos transformados en 1.39s, 0 errores, 0 warnings | ✅ Exitoso |

Fuente: Elaboración propia a partir de las pruebas automatizadas y ejecución interactiva en desarrollo.

A partir del cuadro anterior, se evidencia que todos los flujos principales, alternativos y de excepción del caso de uso **CUS01** operan de forma consistente en el frontend. El sistema valida rigurosamente el dominio `@upt.pe`, maneja de forma segura los códigos conservándolos como cadenas de texto, respeta las restricciones temporales de vigencia (5 minutos) y cooldown (60 segundos), e inhabilita estrictamente el uso del adaptador de prueba en entornos productivos.

### 4.5. Delimitación de Alcance y Dependencias
Conforme a los lineamientos del Sprint 1 y la asignación técnica de tareas:
- **No se declara RF01 completo ni autenticación institucional implementada:** El envío real de correos electrónicos a través del servidor SMTP institucional de la UPT y los endpoints de verificación en base de datos forman parte de la tarea **T-03**, asignada a Renzo.
- **Sin paneles ni consentimiento informado:** La confirmación posterior a la verificación es una pantalla mínima de diagnóstico. No se incorporan paneles de control, tablas de perfil ni el flujo legal de consentimiento informado (**T-04** y **T-05**), los cuales se construirán en los hitos correspondientes.

---

## 5. Registro de Ejecución — Hito 4 (H4: T-06: Pruebas Iniciales e Integración Continua)

### 5.1. Alcance Implementado
- **Frontend SPA (`aplicacion/frontend/`):**
  - Configuración del entorno de pruebas unitarias y de componentes con **Vitest 2.1.8**, **React Testing Library 16.3.3**, emulación de DOM mediante **jsdom 29.1.1** y motor de cobertura **v8 (@vitest/coverage-v8 2.1.8)**.
  - Implementación de 34 pruebas automatizadas distribuidas en 5 suites:
    1. `src/services/__tests__/authService.test.ts` (15 pruebas): validación de dominio institucional `@upt.pe`, excepciones tipadas `AuthErrorCode`, expiración temporal controlada (5 minutos según **RNF01**) mediante relojes simulados (`vi.useFakeTimers`), cooldown de 60s (**CUS01**), invalidación de desafíos previos, consumo único de OTP y bloqueo estricto en producción (`MOCK_DISABLED`).
    2. `src/components/__tests__/LoginOtpView.test.tsx` (9 pruebas): flujo completo en 2 pasos de la interfaz, manejo de estados de carga, deshabilitación de botones, conservación de ceros iniciales en cadenas de texto, atajos de prueba y temporizadores dinámicos basados en marcas temporales reales.
    3. `src/services/__tests__/apiClient.test.ts` (6 pruebas): consumo de endpoints `health` y `health/db`, manejo de códigos HTTP 200, 404 (fuera de desarrollo) y errores de red.
    4. `src/components/__tests__/HealthStatus.test.tsx` (3 pruebas): renderizado reactivo de estados de carga, éxito y error con diagnóstico guiado y botón de reintento.
    5. `src/__tests__/App.test.tsx` (1 prueba): navegación por pestañas del Sprint 1 (*Acceso OTP* vs *Monitor de Servicios*).
  - Scripts configurados en `package.json`: `npm run test` (sin watch), `npm run test:coverage` (con reporte v8) y `npm run lint`.
- **Backend API (`aplicacion/backend/`):**
  - Incorporación de dependencias fijadas con versiones exactas (`==`): `pytest-cov==7.1.0` y `ruff==0.17.1`.
  - Configuración centralizada de linting, formateo y cobertura en `pyproject.toml`.
  - Implementación de 23 pruebas automatizadas distribuidas en 3 módulos:
    1. `tests/test_health.py` (7 pruebas): operatividad independiente de `GET /api/v1/health` sin base de datos, diagnóstico `GET /api/v1/health/db` restringido a desarrollo (404 en producción), respuesta 503 ante falta de configuración o fallo, y metadatos en raíz.
    2. `tests/test_session.py` (10 pruebas): ciclo de vida de conexión SQLAlchemy, creación diferida (*lazy*), descarte idéntico (`close_engine`), sesión con cierre garantizado, sanitización exhaustiva de errores de base de datos y comprobación técnica `SELECT 1` con conexión sustituida.
    3. `tests/test_config.py` (6 pruebas): parseo robusto de CORS desde cadenas JSON o listas, homologación de dialectos PostgreSQL a `postgresql+psycopg://` y enmascaramiento estricto de secretos (`repr=False`).
- **Aislamiento Estricto del Entorno de Pruebas:**
  - Creación de fixture autouse en `tests/conftest.py` que aísla la carga del `.env` local sin borrarlo ni modificarlo, forzando `DATABASE_URL=None` por defecto y garantizando que ninguna prueba unitaria ejecute llamadas reales a Supabase o requiera credenciales SMTP.
  - Validación de no exposición de secretos ficticios: se comprobó que errores simulados que contienen contraseñas o tokens sensibles son sanitizados sin fugar cadenas confidenciales en la respuesta.
- **Entorno de Ejecución Backend:**
  - Adopción de Python 3.13 en desarrollo local (versión comprobada en consola mediante `.\.venv\Scripts\python.exe --version`: **Python 3.13.5**) y en el pipeline de GitHub Actions (`python-version: "3.13"`).
  - Esto representa una desviación técnica justificada respecto al plan preliminar de Python 3.11, motivada por la optimización de rendimiento del intérprete y plena compatibilidad con las versiones vigentes de `FastAPI 0.135.1`, `SQLAlchemy 2.0.44`, `psycopg 3.3.6` y `Ruff 0.17.1`. Se conserva el antecedente de Python 3.11 en el plan de tareas para fines de auditoría.
- **Verificación de Producción y Bloqueo de Adaptadores Simulados:**
  - Se verificó que durante la compilación de producción (`npm run build`), Vite incrusta estáticamente `import.meta.env.DEV = false`, provocando que el adaptador de prueba en memoria quede completamente bloqueado arrojando `MOCK_DISABLED`, garantizando que el acceso simulado no pueda operar fuera de desarrollo.
- **Flujo de Integración Continua en GitHub Actions (`.github/workflows/ci.yml`):**
  - Disparadores configurados: eventos `push` en `main` y `feat/sprint-01-base-acceso-ci`, y eventos `pull_request` hacia `main`.
  - Permisos mínimos: `permissions: contents: read`.
  - Acciones oficiales vigentes: `actions/checkout@v4`, `actions/setup-node@v4`, `actions/setup-python@v5` y `actions/upload-artifact@v4`.
  - Jobs independientes: `frontend` (npm ci, lint, test:coverage, build y subida de artefacto `frontend-coverage-report`) y `backend` (pip install, ruff check/format, pytest con cobertura y subida de artefacto `backend-coverage-report`).
  - Totalmente desacoplado de secretos externos (sin credenciales de Supabase en el workflow).

### 5.2. Resultados de Pruebas y Cobertura de Código

A continuación, en el Cuadro 5.1 se presenta la matriz consolidada de pruebas automatizadas y cobertura de código alcanzada para el Frontend y el Backend en el Sprint 1:

### Cuadro 5.1: Matriz de Cobertura y Pruebas Automatizadas del Sprint 1 (Hito 4)

| Componente | Framework / Herramienta | Pruebas Ejecutadas | Estado | Cobertura Declaraciones / Líneas (%) | Cobertura Ramas (%) | Cobertura Funciones (%) | Meta RNF09 (≥ 70%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Frontend SPA** | Vitest 2.1.8 + v8 | 34 pasadas (5 suites) | ✅ Exitoso | **97.34%** | **88.02%** | **88.57%** | Superada (+27.34%) |
| **Backend API** | Pytest 9.1.1 + Coverage.py | 23 pasadas (3 módulos) | ✅ Exitoso | **94.52%** | *No medidas* | *No medidas* | Superada (+24.52%) |
| **Total del Proyecto** | Pipeline CI (`ci.yml`) | **57 pruebas pasadas** | ✅ Exitoso | *Medición por componente* | *Medición por componente* | *Medición por componente* | Superada en ambos componentes |

Fuente: Reportes oficiales de cobertura generados por v8 (Vitest) y Coverage.py en el entorno de desarrollo y validados en GitHub Actions (run 39331555735).

Como se desprende del cuadro anterior, las 57 pruebas automatizadas totales (34 en Frontend y 23 en Backend) alcanzaron un resultado 100% satisfactorio. En cuanto a la cobertura de código, el Frontend registra un 97.34% en líneas/declaraciones, 88.02% en ramas y 88.57% en funciones; en tanto que el Backend alcanza un 94.52% en declaraciones (las ramas y funciones del backend se registran formalmente como *No medidas* al no estar habilitada la instrumentación branch/function en `coverage.py`). Ambos componentes superan de manera holgada la meta mínima del 70% estipulada en el requerimiento no funcional **RNF09** (mantenibilidad y calidad de código). Este resultado provee evidencia empírica de pruebas y cobertura para los módulos construidos en el **Sprint 1** (infraestructura base, diagnóstico health check y flujo de acceso OTP con adaptador de desarrollo), sin que deba interpretarse como una garantía definitiva ni una certificación de RNF09 para el sistema en su totalidad, cuya meta requerirá verificación continua en los sprints posteriores.

### 5.3. Evidencias de Persistencia Real de Supabase
Se conserva la comprobación técnica real ejecutada en el Hito 2 (`SELECT 1` contra el proyecto Supabase `p2p-epis-dev`, latencia observada de 2828.53 ms) como evidencia separada de integración manual, garantizando que la suite automatizada opere de forma 100% aislada, determinista y sin dependencia de servicios externos en la nube.

### 5.4. Estado de Verificación Local, Análisis Estático y Remoto en GitHub Actions
- **Análisis Estático (Linting y Formateo):**
  - Frontend: ESLint (`npm run lint`) ejecutado sin errores ni advertencias (0 errores, 0 warnings).
  - Backend: Ruff (`ruff check .` y `ruff format --check .`) ejecutado sin errores ni advertencias (0 errores, 0 warnings).
- **Ejecución de Pruebas y Observaciones de Runtime:**
  - Frontend: 34 pruebas pasadas sin advertencias.
  - Backend: 23 pruebas pasadas con **1 advertencia de ejecución no bloqueante**:
    `StarletteDeprecationWarning: Using 'httpx' with 'starlette.testclient' is deprecated; install 'httpx2' instead.`
    Esta advertencia proviene internamente del import de `TestClient` en `fastapi.testclient` sobre `starlette`. Se cataloga explícitamente como un **pendiente técnico no bloqueante** para el seguimiento de la evolución de dependencias upstream, manteniéndose sin modificaciones las versiones exactas fijadas en `requirements.txt`.
- **Verificación Remota en GitHub Actions:**
  - La rama `feat/sprint-01-base-acceso-ci` fue publicada hacia el repositorio remoto (`https://github.com/JMedina255/sistema_web_p2p`).
  - **Workflow:** [CI - Integración Continua Sprint 1](https://github.com/JMedina255/sistema_web_p2p/actions/runs/39331555735)
  - **Run ID:** `39331555735`
  - **Commit SHA disparador:** `8f8a75c5d0d75d897c0e306be0f870af99034447` (`8f8a75c`)
  - **Resultados por Job:**
    - `Frontend (React + Vite + Vitest)`: `completed` / `success` (duración: 39s).
    - `Backend (FastAPI + Pytest + Ruff)`: `completed` / `success` (duración: 26s).
  - **Conclusión General del Workflow:** **`completed / success`** (flujo de CI verificado exitosamente en la nube).

---

## 6. Comandos Reproducibles para Puesta en Marcha Local

### Backend (FastAPI + PostgreSQL Supabase):
```powershell
# 1. Acceder al directorio e inicializar entorno virtual
cd aplicacion/backend
.\.venv\Scripts\activate

# 2. Instalar dependencias fijadas
pip install -r requirements.txt

# 3. Verificación de formato y estilos con Ruff
ruff check .
ruff format --check .

# 4. Comprobar estado de migraciones con Alembic
alembic current

# 5. Ejecutar suite de pruebas unitarias y cobertura (≥ 70% RNF09)
pytest

# 6. Iniciar servidor FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Endpoint de salud general: `http://localhost:8000/api/v1/health`
- Endpoint de diagnóstico de base de datos (dev): `http://localhost:8000/api/v1/health/db`
- Documentación Swagger: `http://localhost:8000/docs`

### Frontend (React + Vite):
```powershell
# 1. Acceder al directorio
cd aplicacion/frontend

# 2. Instalar dependencias reproducibles
npm ci

# 3. Verificación estricta de tipos y linteo
npm run lint

# 4. Ejecutar pruebas unitarias y de componentes con cobertura (≥ 70% RNF09)
npm run test:coverage

# 5. Compilación de producción
npm run build

# 6. Iniciar servidor de desarrollo
npm run dev
```
- Aplicación cliente: `http://localhost:5173/`
- En la interfaz web, seleccionar la pestaña *"Acceso & OTP de Prueba (T-02)"* para interactuar con los escenarios de acceso institucional `@upt.pe`.

---

## 7. Próximos Pasos y Pendientes

1. **Culminación del alcance de Joan en Sprint 1:** Se completaron satisfactoriamente las tareas asignadas a Joan: **T-01** (entorno base y conexión técnica Supabase), **T-02** (interfaz con acceso simulado mediante adaptador mock en desarrollo) y **T-06** (suite de 57 pruebas automatizadas y flujo de CI verificado en GitHub Actions con evidencia de cobertura).
2. **Sprint 1 en curso y coordinación externa con Renzo:** El Sprint 1 continúa en desarrollo y no se encuentra terminado. Las tareas a cargo de Renzo: API OTP real de autenticación (**T-03**), políticas de seguridad a nivel de fila RLS (**T-07**) y tablas del catálogo curricular (**T-09**) permanecen pendientes de integración.
3. **Pendiente técnico no bloqueante:** Seguimiento a la advertencia upstream `StarletteDeprecationWarning` observada en `fastapi.testclient` durante la ejecución de Pytest, sin alterar dependencias en esta fase.
4. **Sprint 2:** Implementación del flujo de consentimiento legal informado conforme a la Ley N° 29733 (**T-04** y **T-05**).
