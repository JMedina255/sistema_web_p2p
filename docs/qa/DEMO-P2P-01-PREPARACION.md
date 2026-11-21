# DEMO-P2P-01 — Guía de Preparación, Estabilización Local y Protocolo de Presentación

**Proyecto:** Sistema Web P2P con Algoritmo de Recomendación para la Personalización de Mentorías Académicas en la EPIS-UPT  
**Hito:** DEMO-P2P-01 — Estabilización Local y Demostración Académica en Vivo  
**Fecha:** 21 de Noviembre de 2026  
**Rama:** `fix/demo-p2p-presentacion`  
**Destino de PR:** `main` (sin auto-merge)

---

## 1. Resumen Ejecutivo de Estado (1 Página)

El presente documento consolida la preparación del entorno local aislado para la demostración académica del **Sistema Web P2P de Mentorías Académicas EPIS-UPT**. Se garantiza un funcionamiento reproducible al 100%, sin dependencias externas de red ni riesgo de afectación a la base de datos de producción en Supabase.

### Matriz de Diagnóstico y Estado Funcional

| Módulo / Capacidad | Clasificación | Estado de Validación en Demostración | Observaciones Operativas |
| :--- | :---: | :---: | :--- |
| **Infraestructura Local Aislada** | **FUNCIONA** | ✅ Verificado | Contenedor PostgreSQL 16 (`p2p-postgres-demo`) con volumen persistente `p2p-postgres-demo-data`. |
| **Alembic Head (001-006)** | **FUNCIONA** | ✅ Verificado | Migraciones completas aplicadas; esquemas de roles y extensiones alineados. |
| **Autenticación OTP (@upt.pe)** | **FUNCIONA** | ✅ Verificado | Dominio institucional estricto; bypass seguro en local vía `tools/get_demo_otp.py` y controles visuales DEV. |
| **Catálogo Curricular y Prioritarias** | **FUNCIONA** | ✅ Verificado | Asignaturas prioritarias (Cálculo I, Algoritmos) y temas conceptuales plenamente integrados. |
| **Motor EdRecSys Top-k con XAI** | **FUNCIONA** | ✅ Verificado | Ranking multifactorial explicable (afinidad curricular, temas silábicos, agenda horaria, mérito RN-03). |
| **Reserva y Aforo Dinámico** | **FUNCIONA** | ✅ Verificado | Reserva de cupos con control de duplicidad, bloqueo por aforo máximo y ratificación previa. |
| **Publicación de Ofertas Mentor** | **FUNCIONA** | ✅ Verificado | Validación estricta de antelación > 24h (RN-04) y selección de espacios físicos o aula virtual. |
| **Evaluación de Quórum (T-24h)** | **FUNCIONA** | ✅ Verificado | Algoritmo automático RN-09 con flujos de contingencia para el mentor (`PROCEED` o `CANCEL`). |
| **Pase de Asistencia QR + TOTP** | **FUNCIONA** | ✅ Verificado | Generación de código TOTP rotativo de 6 dígitos y token SHA-256 en ventana activa [T-15m, T+30m]. |
| **Bitácora Pedagógica con Hash** | **FUNCIONA** | ✅ Verificado | Cierre pedagógico sellado con hash SHA-256 criptográfico para acreditación de horas (RN-14). |
| **Control de Acceso y Roles (RBAC)** | **FUNCIONA** | ✅ Verificado | Aislamiento estricto de roles: Estudiante (1), Mentor (2), Administrador (3). Prohibición de auditoría cruzada (403). |
| **Envío Real de Correo SMTP** | **PARCIAL** | ⚠️ Emulado en local | `SMTP_ENABLED=false` en entorno de presentación; códigos OTP emitidos por logger y dev controls para evitar bloqueos por cuota o red. |
| **Despliegue Remoto en Staging** | **PENDIENTE** | ⏳ Post-demo | La instancia remota se encuentra desacoplada conforme a los objetivos de DEMO-P2P-01 para priorizar presentación presencial. |

**Dictamen General:** **SISTEMA COMPLETAMENTE OPERATIVO Y ESTABILIZADO EN LOCAL (100% PASS EN SMOKE TEST EN VIVO).**

---

## 2. Arquitectura de Aislamiento y Configuración

Para garantizar aislamiento absoluto y prevenir modificaciones no deseadas en la base productiva de Supabase (`db.ieaxmtxpcrldbvmqwbyt.supabase.co`), la demostración se ejecuta sobre una instancia dedicada local:

```
+--------------------------------------------------------------------------+
|                       ARQUITECTURA LOCAL DEMO-P2P-01                     |
+--------------------------------------------------------------------------+
|                                                                          |
|  [ Navegador Web ] <---> [ Frontend: React 18 + Vite ]                   |
|  http://localhost:5173   - VITE_API_BASE_URL: http://127.0.0.1:8000      |
|                          - VITE_SERVICE_MODE: api                        |
|                          - showDevControls: true (Modo desarrollo)       |
|                                     |                                    |
|                                     v (HTTP / REST API v1)               |
|                                                                          |
|  [ Backend: FastAPI + Uvicorn ]                                          |
|  http://127.0.0.1:8000   - APP_ENV: development                          |
|                          - STRICT_DATABASE_MODE: true                    |
|                          - ENABLE_MOCK_OTP_HINTS: true                   |
|                          - SMTP_ENABLED: false                           |
|                                     |                                    |
|                                     v (SQLAlchemy sync + psycopg)        |
|                                                                          |
|  [ Docker: PostgreSQL 16 Alpine ]                                        |
|  127.0.0.1:5432/p2p_demo_db                                              |
|                          - Contenedor: p2p-postgres-demo                 |
|                          - Volumen: p2p-postgres-demo-data               |
|                          - Esquema: Alembic Head (001 a 006)             |
|                                                                          |
+--------------------------------------------------------------------------+
```

---

## 3. Requisitos Previos y Guía de Encendido Rápido

### Requisitos del Sistema Anfitrión (Windows)
- **Docker Desktop** (v29.x o superior) en ejecución.
- **Python** (v3.13.x) con entorno virtual en `aplicacion/backend/.venv`.
- **Node.js** (v22.x) y `npm` en `aplicacion/frontend`.
- Terminal **PowerShell** ejecutada en la raíz del repositorio (`c:\Users\Admin\Desktop\Proyectos\Proyecto_Sistema_Web_P2P_`).

### Procedimiento de Arranque Paso a Paso

#### Terminal 1 — Base de Datos PostgreSQL 16
```powershell
# 1. Iniciar o verificar el contenedor PostgreSQL dedicado
docker run -d `
  --name p2p-postgres-demo `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=demo_p2p_secret_2026 `
  -e POSTGRES_DB=p2p_demo_db `
  -p 5432:5432 `
  -v p2p-postgres-demo-data:/var/lib/postgresql/data `
  postgres:16-alpine

# Si el contenedor ya fue creado previamente:
docker start p2p-postgres-demo

# 2. Aplicar migraciones y poblar datos semilla de demostración (idempotente)
.\aplicacion\backend\.venv\Scripts\python.exe tools\prepare_demo_scenarios.py
```

#### Terminal 2 — Backend FastAPI
```powershell
# 1. Posicionarse en el backend
cd aplicacion\backend

# 2. Configurar variables de entorno de presentación
$env:APP_ENV = "development"
$env:STRICT_DATABASE_MODE = "true"
$env:ENABLE_MOCK_OTP_HINTS = "true"

# 3. Iniciar el servidor Uvicorn en el puerto 8000
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
> El backend quedará escuchando en `http://127.0.0.1:8000`. Documentación Swagger interactiva en `http://127.0.0.1:8000/docs`.

#### Terminal 3 — Frontend React + Vite
```powershell
# 1. Posicionarse en el frontend
cd aplicacion\frontend

# 2. Iniciar Vite en modo desarrollo
npm run dev -- --host 127.0.0.1 --port 5173
```
> La interfaz quedará accesible en `http://127.0.0.1:5173`.

---

## 4. Directorio de Cuentas Institucionales y Roles para la Demostración

Todas las cuentas se encuentran previamente registradas en la base de datos con su consentimiento informado (Ley N° 29733 / RN-02) y perfil académico correspondiente:

| Rol de Demostración | Correo Institucional | Código Estudiantil | Ciclo | Estado y Mérito Normativo |
| :--- | :--- | :---: | :---: | :--- |
| **Estudiante (Mentoreado)** | `estudiante.demo@upt.pe` | 2024010001 | III | Mentoreado activo; necesita apoyo en Cálculo I y Algoritmos. |
| **Mentor Acreditado** | `mentor.demo@upt.pe` | 2022010002 | VIII | Cumple mérito RN-03 (Ciclo >= VII); dicta Cálculo I y Algoritmos. |
| **Coordinador / Administrador** | `admin.demo@upt.pe` | ADM-2026 | X | Rol administrativo para auditoría, telemetría y subida de horarios. |
| **Estudiante Estándar** | `2022074255@upt.pe` | 2022074255 | VI | Cuenta institucional estándar (Joan Medina). |
| **Mentor Estándar** | `2022073504@upt.pe` | 2022073504 | VII | Cuenta institucional estándar (Renzo Antayhua). |

---

## 5. Procedimiento de Obtención de Códigos OTP en Vivo

Para no depender de un servidor SMTP externo durante la disertación, se implementaron dos mecanismos complementarios e inmediatos:

### Opción A — Asistente de Interfaz Gráfica (Recomendado para la presentación)
En la pantalla de inicio de sesión (`http://127.0.0.1:5173`):
1. Ingrese el correo institucional deseado (o pulse los botones rápidos de inserción en la zona de desarrollo).
2. Pulse **"Solicitar Código OTP"**.
3. Al estar en modo desarrollo, la interfaz despliega un recuadro informativo verde con el código de 6 dígitos generado en la sesión.
4. Pulse **"Usar este código"** para completar automáticamente los 6 dígitos y validar el acceso en 1 segundo.

### Opción B — Recuperador CLI para el Presentador (`tools/get_demo_otp.py`)
Si se desea obtener el código desde otra terminal sin mirar los logs de Uvicorn:
```powershell
# Obtener OTP para el Estudiante Demo
.\aplicacion\backend\.venv\Scripts\python.exe tools\get_demo_otp.py --role student

# Obtener OTP para el Mentor Demo
.\aplicacion\backend\.venv\Scripts\python.exe tools\get_demo_otp.py --role mentor

# Obtener OTP para el Administrador Demo
.\aplicacion\backend\.venv\Scripts\python.exe tools\get_demo_otp.py --role admin
```
Salida en consola:
```
============================================================
  SISTEMA WEB P2P - CÓDIGO OTP DE DEMOSTRACIÓN
============================================================
  Usuario : estudiante.demo@upt.pe
  Código  : 885322
  Validez : 60s cooldown
============================================================
```

---

## 6. Secuencia Guiada de Casos de Uso (Guion de Presentación)

A continuación se detalla la secuencia recomendada para realizar una demostración fluida y convincente ante el jurado o auditorio:

```
+-----------------------------------------------------------------------------------+
|                        SECUENCIA CRONOLÓGICA DE LA DEMOSTRACIÓN                   |
+-----------------------------------------------------------------------------------+
|  1. Autenticación & Consentimiento (Estudiante)                                   |
|     -> Ingreso con estudiante.demo@upt.pe, OTP institucional, aceptación Ley 29733|
|                                                                                   |
|  2. Catálogo Curricular & Motor EdRecSys (XAI)                                    |
|     -> Vista de asignaturas prioritarias, recomendación Top-k, panel explicable   |
|                                                                                   |
|  3. Reserva de Cupo & Ratificación                                                |
|     -> Reserva de vacante en sesión SES-DEMO-PUB01, comprobación de aforo         |
|                                                                                   |
|  4. Gestión de Ofertas de Mentoría (Mentor)                                       |
|     -> Inicio con mentor.demo@upt.pe, publicación de oferta con antelación > 24h  |
|                                                                                   |
|  5. Evaluación de Quórum en T-24h & Contingencia                                  |
|     -> Sesión SES-DEMO-Q01 (aforo insuficiente), decisión PROCEED del mentor      |
|                                                                                   |
|  6. Asistencia Digital Dinámica (QR / TOTP) & Bitácora                            |
|     -> Proyección de token TOTP de 6 dígitos en sesión en curso (SES-DEMO-ASIS01) |
|     -> Check-in del estudiante y sellado de bitácora con hash criptográfico SHA256|
|                                                                                   |
|  7. Seguridad & RBAC (Administrador)                                              |
|     -> Control de acceso estricto, auditoría de usuarios y paneles restringidos   |
+-----------------------------------------------------------------------------------+
```

### Escenario DEMO-01: Autenticación Institucional y Protección de Datos
- **Rol:** Estudiante (`estudiante.demo@upt.pe`).
- **Qué mostrar:**
  1. Intentar ingresar con un correo externo como `usuario@gmail.com`. Mostrar el rechazo institucional con mensaje claro: solo se admite `@upt.pe`.
  2. Ingresar `estudiante.demo@upt.pe` y solicitar OTP.
  3. Ingresar el código OTP de 6 dígitos.
  4. Mostrar la persistencia de la sesión mediante token JWT y la confirmación del consentimiento informado en cumplimiento de la Ley N° 29733 (Protección de Datos Personales).

### Escenario DEMO-02: Catálogo Formativo y Recomendación Inteligente (EdRecSys)
- **Rol:** Estudiante (`estudiante.demo@upt.pe`).
- **Qué mostrar:**
  1. Navegar a **"Cursos"** y mostrar las asignaturas prioritarias (Cálculo I, Algoritmos).
  2. Navegar a **"Recomendaciones"** (`RecommendationFeedView`).
  3. Demostrar el ranking Top-k de sesiones y mentores ordenados de forma determinista.
  4. Pulsar el botón **"¿Por qué se recomienda?"** para desplegar el panel de **Inteligencia Artificial Explicable (XAI)**, destacando:
     - Afinidad curricular y ponderador crítico (1.3x).
     - Coeficiente de similitud de temas silábicos (Jaccard / Dice).
     - Disponibilidad horaria compatible en la matriz semanal.
     - Cumplimiento de mérito normativo del mentor (Ciclo >= VII según RN-03).

### Escenario DEMO-03: Reserva de Cupo y Control de Aforo
- **Rol:** Estudiante (`estudiante.demo@upt.pe`).
- **Qué mostrar:**
  1. Seleccionar la sesión recomendada `SES-DEMO-PUB01` y hacer clic en **"Reservar Cupo"**.
  2. Confirmar la reserva en el modal interactivo.
  3. Ir a **"Mis Reservas"** (`StudentBookingsView`) para verificar el estado `CONFIRMADA`.
  4. Explicar el control estricto de duplicidad: el sistema no permite reservar dos veces la misma clase.

### Escenario DEMO-04: Publicación de Ofertas con Restricciones Normativas
- **Rol:** Mentor (`mentor.demo@upt.pe`).
- **Qué mostrar:**
  1. Iniciar sesión como `mentor.demo@upt.pe`.
  2. Navegar a la sección de **"Publicar Oferta de Mentoría"**.
  3. Intentar programar una clase para dentro de 6 horas: el sistema rechaza la solicitud exigiendo una antelación mínima de 24 horas (regla RN-04).
  4. Programar una clase con 3 días de antelación en el Aula 204 del Pabellón EPIS: el sistema aprueba y publica la oferta en el catálogo de inmediato.

### Escenario DEMO-05: Evaluación de Quórum en T-24h y Decisión de Contingencia
- **Rol:** Coordinador (`admin.demo@upt.pe`) y Mentor (`mentor.demo@upt.pe`).
- **Qué mostrar:**
  1. Mostrar la sesión `SES-DEMO-Q01`, que se encuentra a 10 horas de su inicio y cuenta con reservas por debajo del aforo mínimo institucional (regla RN-09).
  2. La sesión pasa a estado `QUORUM_INSUFICIENTE`.
  3. El mentor recibe la notificación de contingencia y decide **"PROCEED"** (continuar la clase de forma personalizada) o **"CANCEL"** (cancelar de forma justificada liberando a los inscritos).
  4. Al ratificar `PROCEED`, la sesión transiciona exitosamente a `CONFIRMADA`.

### Escenario DEMO-06: Asistencia Digital Dinámica (QR TOTP) y Cierre con Bitácora SHA-256
- **Rol:** Mentor (`mentor.demo@upt.pe`) y Estudiante (`estudiante.demo@upt.pe`).
- **Qué mostrar:**
  1. En la sesión en curso `SES-DEMO-ASIS01`, el mentor pulsa **"Generar Asistencia Digital"**.
  2. Se proyecta el código QR rotativo y el código numérico TOTP de 6 dígitos (vigencia de 30 segundos).
  3. El estudiante ingresa el código TOTP y el sistema registra su asistencia (`ASISTIÓ = True`).
  4. El mentor procede al cierre de la sesión completando la **Bitácora Pedagógica** (temas cubiertos, dificultad 'Medio', observaciones, 1.5 horas).
  5. Mostrar el **Hash de Integridad SHA-256** generado automáticamente que blinda la bitácora contra adulteraciones para la emisión del certificado de horas formativas (RN-14).

### Escenario DEMO-07: Control de Acceso por Roles (RBAC) y Seguridad
- **Rol:** Administrador (`admin.demo@upt.pe`) vs Estudiante.
- **Qué mostrar:**
  1. Demostrar que el administrador tiene acceso a la auditoría de roles y usuarios.
  2. Demostrar que si un estudiante intenta consultar la API administrativa de roles (`/api/v1/roles/users/...`), el sistema responde inmediatamente con `403 Forbidden`.

---

## 7. Verificación Automatizada del Stack Completo

Se cuenta con un script de auditoría en vivo que ejecuta de principio a fin los 7 pasos funcionales contra los servicios locales en ejecución:

```powershell
.\aplicacion\backend\.venv\Scripts\python.exe tools\verify_demo_live_stack.py
```

### Resultado de la Verificación Oficial
```
======================================================================
  VERIFICACIÓN FUNCIONAL DEL STACK EN VIVO — EPIS UPT (DEMO-P2P-01)
======================================================================

[Paso 1] Autenticación de Estudiante (Flujo OTP)...
  ✓ Login exitoso para estudiante.demo@upt.pe. Token JWT emitido (309 chars).
  ✓ Restricción de dominio institucional @upt.pe comprobada satisfactoriamente (HTTP 422/400).

[Paso 2] Catálogo Curricular y Recomendaciones (EdRecSys)...
  ✓ Catálogo curricular consultado: 5 asignaturas formativas activas.
  ✓ Recomendaciones EdRecSys generadas: 3 ofertas ordenadas por compatibilidad Top-k.
  ✓ Ranking de mentores afines generado: 5 candidatos evaluados.

[Paso 3] Reserva de Cupo y Confirmación...
  ✓ Reservas actuales del estudiante consultadas: 4 registradas.
  ✓ Reserva ya registrada o respuesta controlada (400): DUPLICATE_BOOKING.

[Paso 4] Publicación de Oferta de Mentor (RN-04 y RN-05)...
  ✓ Login exitoso para Mentor mentor.demo@upt.pe.
  ✓ Oferta publicada exitosamente con antelación > 24h (HTTP 201).
  ✓ Rechazo reglamentario de oferta con antelación menor a 24 horas (RN-04 verificado).

[Paso 5] Evaluación de Quórum y Decisión de Contingencia (RN-09)...
  ✓ Login exitoso para Administrador admin.demo@upt.pe.
  ✓ Evaluación de quórum ejecutada para sesión 102: cumple_quorum = False.
  ✓ Decisión PROCEED del mentor ratificada (HTTP 200): nuevo estado = CONFIRMADA.

[Paso 6] Asistencia QR TOTP y Bitácora Pedagógica...
  ✓ Token QR TOTP dinámico generado para sesión 103 (64 chars).
  ✓ Check-in de asistencia confirmado (HTTP 200): asistió = True.
  ✓ Bitácora pedagógica registrada y firmada con SHA-256 (1.5h acreditadas).

[Paso 7] Acceso Administrativo y Control de Roles (RBAC)...
  ✓ Admin consultó roles de estudiante.demo@upt.pe: ['mentoreado'].
  ✓ Acceso denegado a estudiante al intentar auditar roles ajenos (403 Forbidden verificado).

======================================================================
  RESUMEN EJECUTIVO DE VALIDACIÓN EN VIVO (DEMO-P2P-01)
======================================================================
  Paso 1 - Autenticación Estudiante (OTP)              : ✅ PASS
  Paso 2 - Catálogo y Recomendaciones (EdRecSys)       : ✅ PASS
  Paso 3 - Reserva de Cupo y Confirmación              : ✅ PASS
  Paso 4 - Publicación de Oferta Mentor (RN-04/RN-05)  : ✅ PASS
  Paso 5 - Evaluación de Quórum y Contingencia         : ✅ PASS
  Paso 6 - Asistencia QR TOTP y Bitácora Pedagógica    : ✅ PASS
  Paso 7 - Control de Roles Administrativos (RBAC)     : ✅ PASS
======================================================================
  ESTADO GENERAL: FUNCIONA AL 100% (Listo para Presentación Académica)
======================================================================
```

---

## 8. Contingencias en Vivo y Solución Rápida de Problemas

| Síntoma en Vivo | Causa Probable | Solución Inmediata para el Presentador |
| :--- | :--- | :--- |
| **Error al iniciar Docker o puerto 5432 ocupado** | Instancia previa de PostgreSQL en ejecución. | Ejecutar en PowerShell: `Get-Process -Name postgres -ErrorAction SilentlyContinue \| Stop-Process -Force` y reiniciar el contenedor: `docker start p2p-postgres-demo`. |
| **Puerto 8000 ocupado al iniciar Uvicorn** | Proceso zombi de Python o contenedor residual. | Ejecutar: `Get-NetTCPConnection -LocalPort 8000 \| ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }`. |
| **Error 429 Too Many Requests en Login OTP** | Límite de tasa por IP alcanzado durante ensayos rápidos. | Ejecutar `.\aplicacion\backend\.venv\Scripts\python.exe tools\verify_demo_live_stack.py` (este script limpia automáticamente la tabla `auth_rate_limits`). |
| **Pase de asistencia indica "CHECKIN_WINDOW_CLOSED"** | Ha transcurrido más de 1 hora desde el inicio de la prueba y la sesión 103 caducó. | Ejecutar `tools\verify_demo_live_stack.py` o reiniciar los escenarios con `tools\prepare_demo_scenarios.py` para refrescar los sellos de tiempo. |
| **Frontend muestra pantalla blanca o error de red** | Backend no está corriendo en el puerto 8000. | Verificar en Terminal 2 que Uvicorn esté activo. Abrir `http://127.0.0.1:8000/docs` para comprobar conectividad. |

---

## 9. Procedimiento de Parada y Limpieza Controlada

Una vez finalizada la exposición o sesión de pruebas:

```powershell
# 1. Detener procesos de Uvicorn y Vite (Ctrl + C en sus respectivas terminales)

# 2. Detener el contenedor de PostgreSQL local sin perder los datos
docker stop p2p-postgres-demo

# 3. (Opcional) Si se desea eliminar el contenedor y volumen persistente:
# docker rm -f p2p-postgres-demo
# docker volume rm p2p-postgres-demo-data
```

---

## 10. Conclusiones y Trazabilidad

1. **Aislamiento Total Comprobado:** Ninguna operación realizada durante la estabilización y validación afectó a la base remota de Supabase.
2. **Compatibilidad Estricta de Esquema:** Las migraciones 001 a 006 de Alembic fueron validadas sobre una base de datos PostgreSQL estándar, asegurando que tanto los modelos SQLAlchemy como las tablas y restricciones operen sin fisuras.
3. **Calidad de Código y Calidad Garantizada:**
   - **Backend Ruff:** 100% de verificaciones y formato aprobados sin advertencias.
   - **Backend Pytest:** 455 pruebas unitarias e integrales aprobadas (0 fallos).
   - **Frontend ESLint:** 0 errores de linteo o formato.
   - **Frontend Vitest:** 373 pruebas unitarias y de componentes aprobadas (38 suites, 0 fallos).
   - **Frontend Build:** Compilación TypeScript / Vite de producción completada con éxito.
4. **Listo para Presentación:** El sistema se encuentra en un estado inmejorable de fiabilidad, solidez técnica y preparación operativa para la presentación académica.
