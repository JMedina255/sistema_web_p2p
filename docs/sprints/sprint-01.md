# Bitácora de Ejecución — Sprint 1: Base Técnica y Acceso Inicial

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería (EPIS)  
**Semestre Académico:** 2026-II  
**Equipo:** Grupo 03 — Joan Cristian Medina Quispe (Joan) y Renzo Antonio Antayhua Mamani (Renzo)  
**Rama de trabajo:** `feat/sprint-01-base-acceso-ci`  
**Fecha de corte:** 19/10/2026  

> [!NOTE]
> **Documentación Complementaria de Cierre del Sprint 1:**  
> Para una revisión exhaustiva con capturas de pantalla reales, los 8 diagramas de diseño en PlantUML, catálogo de contratos REST, diccionario físico PostgreSQL y máquinas de estado, consultar el [Informe General Exhaustivo del Sprint 1](../diseño/INFORME_GENERAL_SPRINT_01.md) y el [Catálogo de Evidencias de Pruebas](../diseño/EVIDENCIA_PRUEBAS_SPRINT_01.md).

---

## 1. Visión General y Alcance del Sprint 1

El **Sprint 1** tiene como objetivo fundamental sentar la infraestructura base del sistema web P2P de mentorías académicas, desacoplando estrictamente el frontend SPA y el backend API RESTful (conforme a los requerimientos no funcionales de mantenibilidad **RNF09**), habilitar la verificación de estado operativa (*health check*) e iniciar los mecanismos de acceso y autenticación institucional de prueba (**RF01**, **CUS01**, **RNF01**).

A continuación, se presenta la matriz canónica de asignación y esfuerzo planificado para las actividades del Sprint 1, distinguiendo la distribución técnica entre los integrantes del equipo:

### Cuadro 1.1: Actividades y Compromisos de Desarrollo del Sprint 1

| ID | Actividad | Responsable | Estimación Planificada (h) | Estado Técnico | Hito Asociado |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **T-01** | Configurar entorno React, FastAPI y Supabase. | Joan | 4 | Verificado localmente | H1 / H2 |
| **T-02** | Desarrollar interfaz de acceso y OTP de prueba. | Joan | 2 | Verificado localmente (Mock Dev) | H3 |
| **T-03** | Implementar API de autenticación y OTP de prueba. | Renzo | 4 | Verificado con API real y JWT | H6 |
| **T-06** | Configurar integración continua y pruebas iniciales. | Joan | 3 | Verificado en CI remoto (`8f8a75c`) | H4 |
| **T-07** | Implementar políticas RLS iniciales. | Renzo | 3 | Verificado con script SQL y guía | H7 |
| **T-09** | Crear tablas y datos iniciales del catálogo curricular. | Renzo | 2 | Verificado con Alembic y seed | H5 |

Fuente: Elaboración propia con base en el documento canónico de planificación `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` y tabla 5.2 de la planificación del Grupo 03.

Como se evidencia en el cuadro anterior, el alcance total planificado para el Sprint 1 (18 horas distribuidas equitativamente: 9 horas para Joan en T-01, T-02 y T-06; y 9 horas para Renzo en T-03, T-07 y T-09) ha sido completado y verificado en su integridad. La totalidad de los hitos técnicos (**H1** y **H2** para T-01, **H3** para T-02, **H4** para T-06, **H5** para T-09, **H6** para T-03 y **H7** para T-07) cuentan con artefactos ejecutables, migraciones reproducibles, políticas RLS de seguridad, adaptadores integrados y una suite de 96 pruebas automatizadas que superan holgadamente la meta de mantenibilidad de **RNF09** ($\ge 70\%$).

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

## 6. Registro de Ejecución — Hito 5 (H5: T-09: Catálogo Curricular y Datos Semilla)

### 6.1. Alcance Implementado
- **Modelos ORM de Dominio Curricular (`app/models/curriculum.py`):**
  - Entidad `Asignatura` (tabla `asignaturas`): clave primaria entera autoincremental `id_asignatura`, código único `codigo_curso` (ej. `CALC-101`), denominación `nombre_curso`, ciclo académico `ciclo_plan` (I a IV ciclo), número de créditos lectivos `creditos`, bandera de curso crítico `es_prioritaria`, factor de ponderación para el motor Top-k `factor_ponderacion`, estado activo y marca temporal de auditoría.
  - Entidad `TemaConceptual` (tabla `temas_conceptuales`): clave primaria `id_tema`, clave foránea vinculada `id_asignatura` con eliminación en cascada (`ON DELETE CASCADE`), `nombre_tema`, `descripcion_silabo`, número de unidad silábica `unidad_silabica` y estado activo.
- **Migración Canónica de Base de Datos con Alembic (`app/db/migrations/versions/001_initial_curriculum_and_auth.py`):**
  - Revisión `20261019_001`: crea DDL relacional para `asignaturas`, `temas_conceptuales` y `auth_challenges`.
  - Inserción de datos semilla para las **5 asignaturas formativas filtro** de la carrera de Ingeniería de Sistemas (EPIS-UPT):
    1. *Cálculo I* (`CALC-101`, Ciclo I, 4 créditos, factor 1.2, 4 unidades silábicas).
    2. *Cálculo II* (`CALC-201`, Ciclo II, 4 créditos, factor 1.2, 4 unidades silábicas).
    3. *Algoritmos y Estructuras de Datos* (`ALGO-202`, Ciclo II, 4 créditos, factor 1.3, 5 unidades silábicas).
    4. *Programación Orientada a Objetos* (`POO-301`, Ciclo III, 4 créditos, factor 1.2, 4 unidades silábicas).
    5. *Base de Datos* (`BDD-401`, Ciclo IV, 4 créditos, factor 1.1, 4 unidades silábicas).
- **Capa de Servicios y Endpoints RESTful (`app/api/v1/endpoints/curriculum.py`):**
  - `GET /api/v1/curriculum/courses`: listado general del catálogo curricular con filtros opcionales de prioridad (`only_priority`) y ciclo (`ciclo`).
  - `GET /api/v1/curriculum/courses/{id_asignatura}`: consulta detallada de una asignatura incluyendo su árbol completo de temas silábicos.
  - `GET /api/v1/curriculum/courses/{id_asignatura}/topics`: listado específico de temas y unidades pedagógicas para el agendamiento y recomendación.
  - Esquemas Pydantic tipados `CourseRead`, `CourseDetailRead` y `TopicRead` en `app/schemas/curriculum.py`.
- **Integración con la Interfaz de Usuario React (`aplicacion/frontend`):**
  - Nuevo componente `CurriculumCatalogView.tsx` accesible mediante la pestaña *"📚 Catálogo Curricular (T-09)"* en la barra de navegación superior.
  - Funciones tipadas `fetchCourses()` y `fetchCourseDetail()` en `src/services/apiClient.ts`.
  - Selector de materias por ciclo y visualización interactiva del temario silábico oficial de la UPT.

### 6.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se presenta la matriz de verificación técnica efectuada para el catálogo curricular y sus datos semilla:

### Cuadro 6.1: Matriz de Verificación y Pruebas del Catálogo Curricular (Hito 5)

| Escenario Evaluado | Comando / Prueba Automatizada | Comportamiento Esperado | Resultado Real Observado | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **Generación DDL Alembic** | `alembic upgrade base:head --sql` | Compilación SQL sin errores de sintaxis DDL ni seeds | Genera scripts DDL e INSERTs para las 5 materias filtro | ✅ Exitoso |
| **Catálogo de 5 Materias** | `test_list_courses_returns_5_filter_courses` | Retornar lista con Cálculo I, Cálculo II, Algoritmos, POO y BD | HTTP 200, 5 asignaturas identificadas con nombres oficiales | ✅ Exitoso |
| **Filtro por Prioridad** | `test_list_courses_filter_only_priority` | Filtrar asignaturas con `es_prioritaria=True` | HTTP 200, asignaturas filtro filtradas correctamente | ✅ Exitoso |
| **Filtro por Ciclo** | `test_list_courses_filter_by_ciclo` | Consultar materias de Ciclo II (Cálculo II y Algoritmos) | HTTP 200, retorna exactamente `CALC-201` y `ALGO-202` | ✅ Exitoso |
| **Detalle con Temario** | `test_get_course_detail_success` | Cargar asignatura ID 1 con sus unidades silábicas | HTTP 200, incluye árbol de temas (Límites, Derivadas, etc.) | ✅ Exitoso |
| **Asignatura Inexistente** | `test_get_course_detail_not_found` | Denegar acceso con ID no existente (ej. 999) | HTTP 404 Not Found con mensaje descriptivo | ✅ Exitoso |
| **Temas por Asignatura** | `test_get_course_topics_success` | Listar temas de Algoritmos (ID 3) | HTTP 200, incluye Punteros, Recursividad, Estructuras | ✅ Exitoso |
| **Persistencia ORM en BD** | `test_curriculum_service_with_real_db_session` | Consultar Asignatura y Temas con sesión real SQLAlchemy (selectinload) | Relaciones ORM cargadas, filtros exactos sin fallback forzado | ✅ Exitoso |
| **Interfaz Frontend** | `CurriculumCatalogView.test.tsx` (3 pruebas) | Renderizado reactivo de tarjetas y selección de temas | 3 passed en Vitest, selección de tarjetas y filtros OK | ✅ Exitoso |

Fuente: Elaboración propia a partir de las pruebas automatizadas de Pytest y Vitest ejecutadas localmente.

El cuadro anterior demuestra que el catálogo curricular de asignaturas críticas opera como repositorio único de verdad académica conforme a **RF05** y **CUS21**, garantizando que el futuro motor de recomendación Top-k disponga de la taxonomía jerárquica de temas silábicos oficiales de la EPIS-UPT.

---

## 7. Registro de Ejecución — Hito 6 (H6: T-03: API de Autenticación OTP y Sesión JWT)

### 7.1. Alcance Implementado
- **Criptografía y Gobernanza de Seguridad (`app/core/security.py`):**
  - Generación aleatoria criptográficamente segura de códigos numéricos de 6 dígitos con relleno de ceros a la izquierda mediante `secrets.randbelow()` (conservación estricta de formato `string`).
  - Hashing salado mediante SHA-256 para almacenamiento protegido de códigos en la tabla `auth_challenges`.
  - Emisión de tokens de sesión **JWT (JSON Web Token)** firmados bajo el estándar **HS256** utilizando `JWT_SECRET_KEY` (compatible con el JWT Secret de Supabase), con expiración de 8 horas continuas (480 minutos) conforme a **RNF01** y **SAD-04**, y emisor institucional `sistema-p2p-epis-upt`.
- **Servicio y Endpoints RESTful de Autenticación (`app/api/v1/endpoints/auth.py`):**
  - `POST /api/v1/auth/otp/request`: validación estricta de correo `@upt.pe`, verificación de cooldown de 60 segundos (HTTP 429 ante solicitudes repetitivas conforme a **CUS01**), persistencia de desafío con ventana de vigencia de 5 minutos (**RNF01**), invalidación atómica de desafíos previos del mismo usuario y respuesta normalizada.
  - `POST /api/v1/auth/otp/resend`: invalidación del código previo y emisión de un nuevo desafío respetando la restricción de cooldown.
  - `POST /api/v1/auth/otp/verify`: comprobación de formato de 6 dígitos, validación de caducidad temporal con sincronización UTC, prevención de ataques de repetición (**anti-replay** marcando el código como consumido), y emisión del JWT de sesión de prueba.
- **Adaptador de API Real en Frontend (`ApiAuthAdapter` en `src/services/authService.ts`):**
  - Implementación completa de `ApiAuthAdapter` que consume los endpoints RESTful reales vía `fetch`.
  - Mapeo bidireccional de excepciones tipadas (`AuthException`) ante códigos HTTP 400, 404, 422 y 429.
  - Almacenamiento seguro del token JWT en el almacenamiento de sesión (`sessionStorage`) mediante `authService.saveToken()`.
  - Selector en caliente en la interfaz `LoginOtpView.tsx` que permite alternar fluidamente entre el adaptador mock local (**T-02**) y la API real de backend (**T-03**), mostrando el token emitido en pantalla.

### 7.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se documenta la matriz de pruebas automatizadas ejecutadas para verificar el flujo de autenticación y sesión:

### Cuadro 7.1: Matriz de Verificación de Autenticación y Desafíos OTP (Hito 6)

| # | Escenario Evaluado | Mecanismo de Prueba | Comportamiento Esperado | Resultado Real Observado | Estado |
| :-: | :--- | :--- | :--- | :--- | :---: |
| **01** | Emisión exitosa de OTP | `test_request_otp_success` | Generar desafío con vigencia 5 min y cooldown 60s | HTTP 200, `challengeId` emitido, `isMock: false` | ✅ Exitoso |
| **02** | Rechazo de dominio externo | `test_request_otp_rejects_non_upt_domain` | Rechazar correos que no terminen en `@upt.pe` | HTTP 422, mensaje de restricción institucional | ✅ Exitoso |
| **03** | Rechazo por formato inválido | `test_request_otp_rejects_malformed_email` | Rechazar entradas malformadas antes de persistir | HTTP 422 Unprocessable Entity | ✅ Exitoso |
| **04** | Bloqueo por Cooldown Activo | `test_request_otp_cooldown_rejection` | Rechazar segundo intento en menos de 60 segundos | HTTP 429 Too Many Requests (`COOLDOWN_ACTIVE`) | ✅ Exitoso |
| **05** | Reenvío válido de código | `test_resend_otp_success` | Emitir nuevo desafío e invalidar el anterior | HTTP 200, nuevo `challengeId` generado | ✅ Exitoso |
| **06** | Reenvío de desafío inexistente | `test_resend_otp_not_found` | Rechazar identificadores caducados o corruptos | HTTP 404 Not Found (`CHALLENGE_NOT_FOUND`) | ✅ Exitoso |
| **07** | Código con formato inválido | `test_verify_otp_invalid_format` | Rechazar longitudes distintas a 6 caracteres | HTTP 422 Unprocessable Entity | ✅ Exitoso |
| **08** | Desafío no encontrado en verify | `test_verify_otp_challenge_not_found` | Rechazar códigos de sesiones ya descartadas | HTTP 404 Not Found (`CHALLENGE_NOT_FOUND`) | ✅ Exitoso |
| **09** | Código vencido (> 5 minutos) | `test_verify_otp_expired_code` | Rechazo por vencimiento de vigencia (RNF01) | HTTP 400 Bad Request (`OTP_EXPIRED`) | ✅ Exitoso |
| **10** | Código OTP erróneo | `test_verify_otp_incorrect_code` | Rechazar discrepancias e incrementar intentos | HTTP 400 Bad Request (`OTP_INVALID`) | ✅ Exitoso |
| **11** | Verificación exitosa + JWT | `test_verify_otp_success_and_jwt_token_issued` | Retornar éxito y emitir token firmado HS256 | HTTP 200, JWT decodificable con sub y rol | ✅ Exitoso |
| **12** | Código reutilizado (anti-replay) | `test_verify_otp_already_used` | Bloquear segundo intento con código ya consumido | HTTP 400 Bad Request (`OTP_ALREADY_USED`) | ✅ Exitoso |
| **13** | Pruebas de Adaptador en Frontend | `apiAuthAdapter.test.ts` (9 pruebas) | Integración frontend con mapping de errores y JWT | 9 passed en Vitest, persistencia en sessionStorage | ✅ Exitoso |
| **14** | Persistencia y anti-replay en BD | `test_auth_service_with_real_db_session` | Persistir desafío en BD, evaluar cooldown en BD, verificar sin error de zonas horarias e invalidar desafíos previos | Sesión ORM verificada, anti-replay confirmado y `consumed=true` en BD | ✅ Exitoso |

Fuente: Elaboración propia a partir de las pruebas automatizadas ejecutadas en los suites `test_auth.py` y `apiAuthAdapter.test.ts`.

Como se desprende del análisis del cuadro anterior, la implementación de **T-03** proporciona la capa operativa real de autenticación requerida por **RF01**, **CUS01** y **RNF01**, gestionando adecuadamente los desafíos temporales y protegiendo el sistema contra accesos no autorizados e intentos de reutilización de códigos.

---

## 8. Registro de Ejecución — Hito 7 (H7: T-07: Políticas RLS de Supabase y Guía de Despliegue)

### 8.1. Alcance Implementado
- **Script SQL Canónico de Row Level Security (`aplicacion/backend/scripts/supabase_rls_setup.sql`):**
  - Activación obligatoria de `ROW LEVEL SECURITY` (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY` y `FORCE ROW LEVEL SECURITY`) sobre las tablas `asignaturas`, `temas_conceptuales` y `auth_challenges`.
  - **Políticas para catálogo curricular (`asignaturas` y `temas_conceptuales`):**
    - `p2p_curriculum_asignaturas_select_public`: concede permisos de lectura pública (`SELECT`) a roles `anon` y `authenticated` para materias con `estado_activo = true`.
    - `p2p_curriculum_temas_select_public`: concede permisos de lectura pública sobre unidades temáticas silábicas.
    - `p2p_curriculum_asignaturas_admin_all` y `p2p_curriculum_temas_admin_all`: restringe operaciones de escritura, edición y borrado (`INSERT`, `UPDATE`, `DELETE`) estrictamente a usuarios autenticados cuyo JWT certifique rol `administrador` o `admin`.
  - **Políticas para auditoría y emisión OTP (`auth_challenges`):**
    - `p2p_auth_challenges_insert_upt`: autoriza la inserción de solicitudes únicamente si el correo cumple la condición `email LIKE '%@upt.pe'` y la vigencia temporal `expires_at > now()`.
    - `p2p_auth_challenges_select_active`: permite la lectura condicionada a códigos no consumidos ni vencidos.
    - `p2p_auth_challenges_update_consumed`: limita las actualizaciones exclusivamente al marcado atómico de código consumido (`consumed = true`).
- **Guía Paso a Paso para el Usuario y Despliegue en Supabase (`docs/supabase_setup_guide.md`):**
  - Documento exhaustivo que detalla la obtención de la cadena de conexión mediante el **Session Pooler** (puerto 5432 / IPv4) en Supabase Dashboard.
  - Instrucciones para la sincronización del secreto `JWT_SECRET_KEY` obtenido en Project Settings → API.
  - Procedimiento para ejecutar las migraciones de Alembic (`alembic upgrade head`) y aplicar el script SQL en el **SQL Editor** de Supabase.

### 8.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se detalla la matriz de verificación técnica para las políticas RLS y la seguridad de datos:

### Cuadro 8.1: Matriz de Verificación de Políticas RLS y Aprovisionamiento en Supabase (Hito 7)

| Componente | Artefacto Evaluado | Requisito de Seguridad | Validación Observada | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **Catálogo Curricular** | `asignaturas` | Lectura pública permitida; edición restringida a administradores | Política RLS activa; usuarios anónimos solo pueden leer registros activos | ✅ Exitoso |
| **Temario Silábico** | `temas_conceptuales` | Lectura pública autorizada; modificación bloqueada para roles regulares | Política RLS activa con restricción jerárquica | ✅ Exitoso |
| **Desafíos OTP** | `auth_challenges` | Inserción restringida a dominio `@upt.pe`; lectura bloqueada tras consumo | Políticas de INSERT y SELECT condicionadas activas | ✅ Exitoso |
| **Guía de Despliegue** | `docs/supabase_setup_guide.md` | Documentación paso a paso de configuración para el usuario | Guía completa con parámetros, comandos y matriz de verificación | ✅ Exitoso |
| **Script de Migración SQL** | `supabase_rls_setup.sql` | Sintaxis PostgreSQL estándar ejecutable en SQL Editor | Script verificado sin errores de sintaxis DDL | ✅ Exitoso |

Fuente: Elaboración propia a partir del script de seguridad `supabase_rls_setup.sql` y directrices arquitectónicas del SAD FD04.

El cuadro anterior certifica el cumplimiento del requerimiento no funcional **RNF02** (seguridad y protección de datos) y la tarea **T-07**, asegurando que la base de datos en Supabase imponga las restricciones de acceso en el propio motor PostgreSQL sin depender exclusivamente de filtros en la capa de aplicación.

---

## 9. Matriz Consolidada de Pruebas Automatizadas y Cobertura Final del Sprint 1

A continuación, se presenta la matriz consolidada de pruebas unitarias, de integración y cobertura de código alcanzada para el Frontend y Backend al término del Sprint 1:

### Cuadro 9.1: Matriz de Cobertura y Pruebas Automatizadas Finales del Sprint 1

| Componente | Framework / Herramienta | Pruebas Ejecutadas | Estado | Cobertura Declaraciones / Líneas (%) | Cobertura Ramas (%) | Cobertura Funciones (%) | Meta RNF09 (≥ 70%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Frontend SPA** | Vitest 2.1.8 + v8 | **46 pasadas** (7 suites) | ✅ Exitoso | **93.81%** | **76.92%** | **78.94%** | Superada (+23.81%) |
| **Backend API** | Pytest 9.1.1 + Coverage.py | **50 pasadas** (6 módulos) | ✅ Exitoso | **91.62%** | *No medidas* | *No medidas* | Superada (+21.62%) |
| **Total del Proyecto** | Pipeline de Validación Local | **96 pruebas pasadas** | ✅ Exitoso | *Medición por componente* | *Medición por componente* | *Medición por componente* | Superada ampliamente en ambos |

Fuente: Reportes oficiales generados por v8 (Vitest) y Coverage.py en el entorno de desarrollo del proyecto.

Como se observa en el cuadro anterior, las 96 pruebas automatizadas totales (46 en Frontend y 50 en Backend) alcanzaron un resultado 100% satisfactorio sin registrar fallos. En ambos componentes se superan con holgura los umbrales mínimos del 70% estipulados en el requerimiento no funcional **RNF09**, certificando la calidad del código y la robustez de las interfaces y servicios construidos.

---

## 10. Comandos Reproducibles para Puesta en Marcha Local y Supabase

### Backend (FastAPI + PostgreSQL Supabase):
```powershell
# 1. Acceder al directorio e inicializar entorno virtual
cd aplicacion/backend
.\.venv\Scripts\activate

# 2. Instalar dependencias fijadas (incluye PyJWT)
pip install -r requirements.txt

# 3. Verificación de formato y estilos con Ruff
ruff check .
ruff format --check .

# 4. Aplicar migraciones a la base de datos Supabase
alembic upgrade head

# 5. Ejecutar suite completa de pruebas unitarias con reporte de cobertura
pytest

# 6. Iniciar servidor FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Endpoint de salud general: `http://localhost:8000/api/v1/health`
- Endpoint de salud de base de datos (Supabase dev): `http://localhost:8000/api/v1/health/db`
- Endpoints del catálogo curricular: `http://localhost:8000/api/v1/curriculum/courses`
- Documentación Swagger interactiva: `http://localhost:8000/docs`

### Frontend (React + Vite):
```powershell
# 1. Acceder al directorio
cd aplicacion/frontend

# 2. Instalar dependencias reproducibles
npm ci

# 3. Verificación estricta de tipos y linteo
npm run lint

# 4. Ejecutar suite de pruebas con cobertura
npm run test:coverage

# 5. Compilación de producción
npm run build

# 6. Iniciar servidor de desarrollo
npm run dev
```
- Aplicación cliente: `http://localhost:5173/`
- En la interfaz web se encuentran disponibles tres vistas funcionales:
  1. *"Acceso & OTP de Prueba (T-02 / T-03)"*: permite interactuar con el flujo OTP tanto en modo Mock como contra la API real emitiendo tokens JWT.
  2. *"Catálogo Curricular (T-09)"*: visualiza interactivamente las 5 materias filtro y sus unidades silábicas.
  3. *"Monitor de Servicios & BD (T-01)"*: muestra el estado de salud de la API y latencia del Session Pooler de Supabase.

---

## 11. Conclusiones y Próximos Pasos

1. **Culminación Integral del Sprint 1:** Se concluyeron con éxito las 6 tareas planificadas para el Sprint 1: las asignadas a Joan (**T-01**, **T-02**, **T-06**) y las asignadas a Renzo (**T-03**, **T-07**, **T-09**). El sistema cuenta con infraestructura operativa, catálogo curricular con las 5 materias filtro sembradas, API de autenticación con JWT de sesión, políticas de seguridad RLS documentadas y 96 pruebas automatizadas con cobertura superior al 91% (**RNF09**).
2. **Habilitación para el Sprint 2:** Con la persistencia base y la autenticación operativa, el equipo se encuentra expedito para abordar el **Sprint 2** (Roles, currículo y perfiles), iniciando con el desarrollo del formulario de consentimiento informado digital (**T-04** y **T-05**) en cumplimiento de la Ley N° 29733 de Protección de Datos Personales del Perú.
