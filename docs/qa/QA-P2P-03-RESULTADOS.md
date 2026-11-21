# QA-P2P-03 — Informe de Validación E2E Real, Pruebas de Interfaz y Cierre de Integración

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Fecha de Ejecución y Cierre:** 21 de noviembre de 2026  
**Rama de Trabajo:** `test/qa-p2p-03-e2e-integracion`  
**Commit Base (Merge PR #20 en `main`):** `8b17b14710b1979d56df2cc9b686f1538df7b024`  
**Estado General:** **APROBADO CON CONDICIONES OPERATIVAS CONTROLADAS (19/20 PRUEBAS E2E APROBADAS, 1 CONDICIÓN BLOQUEADA CONTROLADA / JUSTIFICADA: GOOGLE OAUTH INTERACTIVO, 100% PRUEBAS TRANSACCIONALES POSTGRESQL EXITOSAS)**

---

## 1. Fase 0 — Preparación del Entorno y Verificación de Sincronización

### 1.1. Estado de Sincronización con Repositorio Remoto
- **Repositorio Oficial:** `https://github.com/JMedina255/sistema_web_p2p.git`
- **Integración de PR #20:** Confirmada en la rama `main` de GitHub. Incorporó los resultados de integración funcional de QA-P2P-02 ([QA-P2P-02-RESULTADOS.md](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/QA-P2P-02-RESULTADOS.md)), la modernización de imports de PyMuPDF (P2P-BUG-005) y la reconciliación de trazas de CI.
- **Hash de Merge Commit en `main`:** `8b17b14710b1979d56df2cc9b686f1538df7b024`
- **Estado de GitHub Actions:**
  - **Workflow:** `CI - Integración Continua Sprint 1`
  - **Run ID:** `44886433035` (Ejecución oficial #108)
  - **Head SHA:** `8b17b14`
  - **Estado:** `completed`
  - **Conclusión:** `success` (100% aprobado en CI remoto)
- **Rama de Trabajo QA-P2P-03:** Creada y bifurcada limpiamente desde `main` (`8b17b14`): `test/qa-p2p-03-e2e-integracion`.

### 1.2. Aislamiento Estricto en Base de Datos PostgreSQL
Para evitar cualquier impacto, alteración o lectura indebida sobre el esquema `public` de producción alojado en Supabase:
1. **Esquema Sandbox Transaccional (`test_qa_p2p_03_tx`):** Esquema dedicado creado dinámicamente con DDL completo para las pruebas de alta concurrencia, sobrecupo y atomicidad ACID.
2. **Esquema Sandbox E2E Browser (`test_qa_p2p_03_e2e`):** Esquema exclusivo para el backend FastAPI durante las pruebas de interfaz gráfica. La inyección se realizó configurando el parámetro de conexión `search_path`:
   ```bash
   DATABASE_URL="postgresql://postgres:[PASSWORD]@[HOST]:[PORT]/postgres?sslmode=require&options=-c%20search_path=test_qa_p2p_03_e2e"
   ```
3. **Limpieza e Inmutabilidad de Producción:** El esquema `public` se mantuvo 100% inalterado (0 escrituras). Ambos esquemas sandbox son temporales y cuentan con teardown automático mediante `DROP SCHEMA IF EXISTS ... CASCADE`.

### 1.3. Seguridad y Protección de Secretos
- Las credenciales sensibles de base de datos, claves de firma JWT y secretos de sesión se leyeron exclusivamente de variables de entorno locales de desarrollo (`.env`).
- Ningún secreto, código OTP en texto claro ni cadena de conexión a base de datos fue registrado en logs o incluido en el código versionado.

---

## 2. Fase 1 — Rectificación Técnica y Sanitización de QA-P2P-02

### 2.1. Reclasificación Documental de la Suite
En el ciclo QA-P2P-02 se catalogó la suite [tools/validate_functional_journeys.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/tools/validate_functional_journeys.py) genéricamente como "recorridos de integración E2E". Conforme al rigor metodológico exigido para QA-P2P-03:
- **Clasificación Correcta:** **Pruebas de Integración de API en Entorno Controlado**.
- **Entorno de Ejecución:** FastAPI `TestClient` (basado en `httpx`/`starlette`) acoplado a un motor SQLite en memoria configurado con `poolclass=StaticPool` y `PRAGMA foreign_keys=ON`.
- **Alcance Operativo:** Valida exhaustivamente contratos HTTP RESTful, serialización de esquemas Pydantic, validaciones de dominio `@upt.pe`, RBAC a nivel de endpoint y lógica de persistencia ORM. No ejecuta un navegador ni renderiza el DOM de React.

### 2.2. Sanitización y Eliminación de Fallbacks Inseguros
Se implementaron remediaciones quirúrgicas en [tools/validate_functional_journeys.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/tools/validate_functional_journeys.py):
1. **Eliminación de Impresión de Secretos:** Se suprimió la emisión en consola de códigos numéricos TOTP y fragmentos de firmas criptográficas SHA-256.
2. **Retiro de Fallback de Desarrollo Fijo:** Se eliminó la asignación por defecto `otp_valid = chal_obj.get("code_plain") if chal_obj else "123456"`. En su lugar, se añadieron aserciones explícitas de preparación:
   ```python
   chal_obj = _memory_challenges.get(chal_id)
   assert chal_obj is not None and "code_plain" in chal_obj, (
       "Fallo de preparación: el desafío OTP no fue registrado en el almacén de autenticación"
   )
   otp_valid = chal_obj["code_plain"]
   ```
   Esto previene que un fallo real en el mecanismo de autenticación quede enmascarado por un código fijo.
3. **Línea Base para CI:** Las 30 comprobaciones se mantienen con 100% de éxito y quedan estandarizadas como suite rápida de integración en pipelines de integración continua.

---

## 3. Fase 2 — Validación E2E Real en Navegador (Playwright / Edge)

Se desplegó la arquitectura completa del sistema en modo real:
- **Frontend Web:** React 19 + TypeScript + Tailwind CSS servido por Vite en `http://127.0.0.1:5173`, con `VITE_SERVICE_MODE=api` y proxy reverso activo hacia `/api/v1`.
- **Backend API:** FastAPI + Uvicorn en `http://127.0.0.1:8000`, conectado al motor PostgreSQL sandbox `test_qa_p2p_03_e2e`.
- **Automatizador de Navegador:** Playwright interactuando sobre **Microsoft Edge** (`channel="msedge"`), con viewport estándar de escritorio de 1280x800 píxeles.
- **Suite de Pruebas Automatizada:** [tools/run_browser_e2e_tests.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/tools/run_browser_e2e_tests.py).

### 3.1. Matriz de Resultados E2E en Navegador Real

| ID de Prueba | Rol / Contexto | Recorrido / Acción en UI | Evidencia Visual (Screenshot) | Estado | Comportamiento Observado y Validación |
|---|---|---|---|:---:|---|
| **E2E-EST-01** | Estudiante | Acceso Institucional OTP | [01_estudiante_login.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/01_estudiante_login.png) | **PASS** | Ingreso de `estudiante@upt.pe`, emisión de OTP, digitación en formulario, verificación y redirección exitosa al dashboard principal. |
| **E2E-EST-02** | Estudiante | Perfil Académico | [02_estudiante_perfil.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/02_estudiante_perfil.png) | **PASS** | Carga de datos formativos (Ciclo V, EPIS), modificación de disponibilidad horaria y persistencia inmediata en PostgreSQL. |
| **E2E-EST-03** | Estudiante | Catálogo Curricular | [03_estudiante_cursos.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/03_estudiante_cursos.png) | **PASS** | Consulta de asignaturas prioritarias (Cálculo I, Algoritmos, Estructuras de Datos), visualización de temarios silábicos normalizados. |
| **E2E-EST-04** | Estudiante | Recomendaciones y XAI | [04_estudiante_recomendaciones.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/04_estudiante_recomendaciones.png) | **PASS** | Renderizado del ranking EdRecSys con métricas de compatibilidad y badges de explicabilidad ("Alta afinidad curricular", "Ponderación 1.2x"). |
| **E2E-EST-05** | Estudiante | Modal de Reserva | [05_estudiante_reserva_modal.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/05_estudiante_reserva_modal.png) | **PASS** | Clic en "Reservar Cupo", despliegue del modal interactivo, desglose de sesión, horario normativo y cupos disponibles. |
| **E2E-EST-06** | Estudiante | Transacción de Reserva | [06_estudiante_reserva_confirmada.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/06_estudiante_reserva_confirmada.png) | **PASS** | Confirmación de reserva en UI, respuesta HTTP 201 Created de la API, creación de registro en tabla `reservas_cupos` en PostgreSQL. |
| **E2E-EST-07** | Estudiante | Mis Reservas | [07_estudiante_mis_reservas.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/07_estudiante_mis_reservas.png) | **PASS** | Despliegue de reservas en estado `PENDIENTE_CONFIRMACION`, verificación de botones de ratificación (T-24h) y desistimiento voluntario. |
| **E2E-MEN-01** | Mentor | Login y Dashboard Mentor | [08_mentor_login_dashboard.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/08_mentor_login_dashboard.png) | **PASS** | Autenticación de `mentor@upt.pe`, verificación de rol `mentor` en JWT, visualización de pestañas operativas de mentoría. |
| **E2E-MEN-02** | Mentor | Publicación de Oferta | [09_mentor_publicar_oferta.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/09_mentor_publicar_oferta.png) | **PASS** | Formulario de publicación con fecha > 24h (RN-04). Aforo fijado en modo readonly según modalidad (10 presencial / 20 virtual, RN-05). Creación exitosa. |
| **E2E-MEN-03** | Mentor | Mis Sesiones y Quórum | [10_mentor_mis_sesiones.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/10_mentor_mis_sesiones.png) | **PASS** | Listado de sesiones programadas, cómputo visual de reservas vs. aforo y evaluación de quórum normativo (>= 50%). |
| **E2E-MEN-04** | Mentor | Asistencia QR Dinámico | [11_mentor_asistencia_qr.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/11_mentor_asistencia_qr.png) | **PASS** | Proyección de código QR dinámico y token TOTP numérico de 6 dígitos con rotación temporal de 30 segundos (CUS12). |
| **E2E-MEN-05** | Mentor | Bitácora Pedagógica | [12_mentor_bitacora.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/12_mentor_bitacora.png) | **PASS** | Selección de temas silábicos, validación sustantiva (>= 50 caracteres), declaración jurada y firma inmutable SHA-256 (RN-12). |
| **E2E-MEN-06** | Mentor | Constancias de Horas | [13_mentor_constancias.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/13_mentor_constancias.png) | **PASS** | Bandeja de acreditación de horas pedagógicas, estado de visado administrativo y opción de descarga de constancia digital. |
| **E2E-ADM-01** | Administrador | Dashboard Gobernanza | [14_admin_dashboard.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/14_admin_dashboard.png) | **PASS** | Acceso concedido exclusivamente al rol institucional `admin`, métricas consolidadas de la escuela y estado de sesiones. |
| **E2E-ADM-02** | Administrador | Usuarios y Roles RBAC | [15_admin_usuarios_roles.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/15_admin_usuarios_roles.png) | **PASS** | Panel de supervisión de identidades, asignación controlada de roles institucionales y auditoría de permisos. |
| **E2E-ADM-03** | Administrador | Visado de Bitácoras | [16_admin_visado_bitacora.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/16_admin_visado_bitacora.png) | **PASS** | Fiscalización académica de bitácoras, verificación de hash criptográfico y acción de visado normativo (RN-14). |
| **E2E-ADM-04** | Administrador | Telemetría y Salud DB | [17_admin_telemetria_servicios.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/17_admin_telemetria_servicios.png) | **PASS** | Diagnóstico en tiempo real: estado del motor PostgreSQL, latencia de endpoints, memoria y versión del sistema. |
| **E2E-AUTH-01** | Seguridad | Control de OTP Inválido | [18_auth_otp_error.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/18_auth_otp_error.png) | **PASS** | Ingreso deliberado de código erróneo `000000`. Respuesta HTTP 400 Bad Request y despliegue de alerta clara en UI sin romper el flujo. |
| **E2E-AUTH-02** | Seguridad | Google OAuth en CI/CD | [19_auth_google_oauth_blocked.png](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/evidencias/19_auth_google_oauth_blocked.png) | **BLOCKED** | *Condición de Contorno Justificada:* El botón Google Sign-In renderiza correctamente en el DOM. Requiere una sesión de usuario humano interactivo en el popup externo de Google Identity Services; clasificado justificadamente como **BLOCKED** sin impacto en la funcionalidad local. |
| **E2E-SEC-01** | Seguridad | No Fuga de Credenciales | *N/A (Inspección DOM/Storage)* | **PASS** | Inspección automatizada de `localStorage`, cookies y respuestas de red: 0 cadenas de conexión, 0 credenciales de Supabase o secretos del backend expuestos. |

---

## 4. Fase 3 — Validación Transaccional y de Concurrencia en PostgreSQL Real

Se ejecutó la suite transaccional de concurrencia [tools/validate_postgresql_transactions.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/tools/validate_postgresql_transactions.py) contra el esquema sandbox `test_qa_p2p_03_tx` en el motor PostgreSQL de Supabase.

### 4.1. Escenarios de Concurrencia y Atomicidad Verificados

```
================================================================================
INICIANDO VALIDACIÓN TRANSACCIONAL Y DE CONCURRENCIA EN POSTGRESQL REAL (QA-P2P-03)
Esquema aislado: test_qa_p2p_03_tx
================================================================================
```

| # | Escenario Transaccional | Criterio Normativo | Concurrencia / Metodología | Resultado Observado | Estado |
|---|---|---|---|---|:---:|
| **TX-01** | Reservas simultáneas sobre la última plaza disponible | RN-05 (Aforo estricto, 0.0% sobrecupo) | 10 hilos concurrentes simultáneos (`ThreadPoolExecutor`) compitiendo por un único cupo libre (cupos: 1) | **Exactamente 1 reserva exitosa (HTTP 201), 9 solicitudes rechazadas con HTTP 400 (CAPACITY_EXCEEDED). 0.0% de overbooking.** | **PASS** |
| **TX-02** | Detección de reserva duplicada para el mismo usuario | RNF07 (Integridad de reservas) | Segundo intento inmediato del mismo estudiante sobre la misma sesión | **Rechazado con HTTP 400 (DUPLICATE_BOOKING). No se generaron registros huérfanos.** | **PASS** |
| **TX-03A** | Ratificación antes de ventana límite (T-30h) | RN-08 (Ratificación perentoria) | Confirmación dentro de la ventana habilitada (>= 24h antes del inicio) | **Transición exitosa a `CONFIRMADA`. Registro computable para quórum normativo.** | **PASS** |
| **TX-03B** | Bloqueo de ratificación fuera de plazo (T-12h) | RN-08 (Ventana expirada) | Intento de ratificación a menos de 24 horas del inicio de la sesión | **Rechazado con HTTP 400 (CONFIRMATION_WINDOW_EXPIRED). Garantía de previsibilidad para el mentor.** | **PASS** |
| **TX-04** | Desistimiento voluntario y liberación atómica de cupo | RN-10 (Liberación inmediata) | Carga de 10 reservas simultáneas + cancelación explícita | **Reserva transiciona a `CANCELADA_USUARIO`. El cupo liberado queda disponible de forma atómica para otros estudiantes.** | **PASS** |
| **TX-05** | Evaluación y cómputo de quórum normativo | RN-09 (Quórum >= 50%) | Evaluación automática a T-24h con 5 de 10 reservas confirmadas | **Cálculo de quórum exacto (50%). La sesión cambia a estado `CONFIRMADA`.** | **PASS** |
| **TX-06** | Restricciones entre estudiante y mentor (RBAC) | RN-03 / Reglas de Rol | Intento de un usuario con rol mentor de auto-reservar su propia sesión | **Bloqueado por regla de negocio (SELF_BOOKING_FORBIDDEN). Control de integridad de roles.** | **PASS** |
| **TX-07** | Atomicidad y Rollback ante excepción inducida | Garantía ACID / RNF01 | Transacción con fallo provocado a mitad de inserción | **Rollback completo ejecutado por PostgreSQL. El estado de la base de datos no sufre contaminación ni inconsistencias.** | **PASS** |

**Resultado Transaccional PostgreSQL:** **7/7 escenarios aprobados (15/15 aserciones superadas con 100% de éxito)**.

---

## 5. Fase 4 — Evaluación de Autenticación y Resiliencia de Servicios Externos

### 5.1. Ciclo de Vida de Desafíos OTP Institucionales
- **Hashing Criptográfico:** Cada desafío se genera mediante código numérico de 6 dígitos derivado con `secrets.randbelow(1_000_000)` y almacenado con hash seguro SHA-256 más salt independiente.
- **Expiración Perentoria:** La vigencia de cada OTP es estrictamente de 5 minutos (300 segundos). Los intentos posteriores a la ventana son rechazados automáticamente con error `CHALLENGE_EXPIRED`.
- **Consumo Único:** Tras una verificación exitosa, el desafío se marca inmediatamente como consumido (`consumed=True`). Cualquier intento posterior de reutilización arroja `CHALLENGE_ALREADY_USED`.

### 5.2. Google OAuth en Entorno Desatendido de Pruebas
- **Diagnóstico:** El componente `GoogleSignInButton` se encuentra debidamente integrado en el frontend mediante el SDK de Google Identity Services (`https://accounts.google.com/gsi/client`).
- **Comportamiento en Automatización:** Al ejecutarse en un entorno headless desatendido sin sesión activa de cuenta institucional de Google y sin interacción biométrica/humana, el endpoint de Google requiere resolución interactiva de consentimiento.
- **Veredicto Técnico:** Se clasifica formalmente como **BLOCKED** justificado por diseño del proveedor externo. No representa un defecto en la arquitectura del sistema.

### 5.3. Resiliencia ante Indisponibilidad o Caída de SMTP
- **Aislamiento de Transporte:** El servicio backend `EmailService` implementa manejo de excepciones de conexión y timeout (`smtplib.SMTPException`, `socket.timeout`).
- **Comportamiento ante Caída:** Si el servidor SMTP no responde, la falla de entrega queda registrada en la bitácora de auditoría del servidor (`logger.warning`), devolviendo un estado controlado al cliente sin abortar el proceso ni exponer trazas de depuración (stack traces) al usuario.

---

## 6. Fase 5 — Registro y Análisis de Incidencias

Durante la ejecución de las pruebas E2E e integración de interfaz gráfica, se comprobaron las siguientes restricciones operativas sin detectar defectos regresivos en la lógica de negocio:

| Registro / Control | Módulo Afectado | Descripción del Comportamiento | Estado y Mitigación Aplicada |
|---|---|---|:---:|
| **CTRL-E2E-01** | `OfferPublishView` (Frontend) | El campo `#input-capacity` está configurado como `readonly` en la interfaz gráfica. | **Conforme a Especificación (RN-05):** El aforo no es editable libremente por el usuario; se calcula y fija automáticamente según la modalidad (10 presencial, 20 virtual). Se ajustó el script de pruebas para seleccionar la modalidad en lugar de intentar sobrescribir el campo de solo lectura. |
| **CTRL-E2E-02** | `tools/validate_postgresql_transactions.py` | Colisiones de clave primaria al relanzar scripts de sandbox si el esquema previo no se había purgado. | **Solventado:** Se implementó `DROP SCHEMA IF EXISTS ... CASCADE` al inicio del ciclo de pruebas, asegurando que cada ejecución disponga de un esquema relacional completamente limpio y estéril. |
| **P2P-BUG-007** | General | No se requirió la apertura de nuevos reportes de error de código aplicativo. | **Ninguno pendiente.** Todos los módulos cumplen cabalmente con los requisitos funcionales SRS y las reglas de negocio RN-01 a RN-14. |

---

## 7. Fase 6 — Resultados de Calidad Integral y Compilación

### 7.1. Backend (Python / FastAPI)
- **Suite Completa Pytest:**
  - **376 aprobadas**, **1 omitida**, **0 fallidas** en 35.91 segundos.
  - *Prueba omitida:* `test_auth_rate_limit_postgresql_atomic_concurrency` (omitida en CI cuando no hay conexión externa a PostgreSQL, pero ejecutada y verificada exitosamente en este informe dentro del sandbox PostgreSQL).
  - **Cobertura de Código:** **83%** (supera holgadamente el umbral normativo del 70%).
- **Linter Ruff:** `ruff check aplicacion\backend` → **0 errores** (All checks passed).
- **Formateador Ruff:** `ruff format --check aplicacion\backend` → **134 archivos verificados y conformes**.

### 7.2. Frontend (React 19 / TypeScript / Vitest)
- **Suite Completa Vitest:**
  - **37 archivos de prueba**, **366 pruebas aprobadas**, **0 fallidas**.
  - Validación completa de componentes para CUS01, CUS02, CUS04, CUS06, CUS07, CUS08, CUS12, CUS13, CUS15, CUS17, CUS24 y accesibilidad WCAG 2.1 AA.
- **Linter ESLint:** `npm --prefix aplicacion\frontend run lint` → **0 errores, 0 advertencias**.
- **Compilación de Producción (Vite Build):**
  - `npm --prefix aplicacion\frontend run build` → **Compilación exitosa en 2.82 segundos**.
  - `dist/` generado con empaquetado optimizado, mapas de componentes limpios y sin advertencias de tipado TypeScript.

---

## 8. Dictamen de Cierre y Próximos Pasos

### 8.1. Dictamen de Auditoría QA-P2P-03
El **Sistema Web P2P de Mentorías Académicas EPIS-UPT** ha superado con éxito la fase más rigurosa de validación integral:
1. **Navegación Visual E2E Real:** 19 de 20 casos de interfaz gráfica completados con éxito en Microsoft Edge, respaldados por capturas de pantalla reales en alta resolución.
2. **Concurrencia y Atomicidad en PostgreSQL:** Cero casos de overbooking en escenarios de alta competencia multi-hilo, ratificación en ventana perentoria y reversión segura de transacciones.
3. **Seguridad y Cero Regresiones:** Códigos OTP protegidos, variables de entorno desacopladas de producción y pruebas unitarias/estáticas con 100% de éxito.

### 8.2. Recomendaciones de Despliegue Operativo
1. **Paso a Staging:** El código contenido en la rama `test/qa-p2p-03-e2e-integracion` está listo para ser sometido a revisión de Pull Request hacia `main`.
2. **Migración 006 en Supabase:** Aplicar la migración de rate limiting en el esquema `public` siguiendo el protocolo de despliegue seguro documentado en QA-P2P-02 (Sección 2.5).
3. **Credenciales SMTP Institucionales:** Configurar las variables del servidor SMTP institucional de la UPT en el entorno de staging para habilitar el despacho de correos reales a alumnos y mentores.
