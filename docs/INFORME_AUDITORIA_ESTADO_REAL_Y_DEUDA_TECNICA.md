# INFORME DE AUDITORÍA CRÍTICA INTEGRAL: REVISIÓN TOTAL DE CÓDIGO
## Estado Real de Mocks, Emulaciones, Integraciones Externas y Persistencia en Supabase

**Sistema Web P2P de Mentorías Universitarias - EPIS UPT**  
**Fecha de Auditoría:** 12 de Noviembre de 2026  
**Entorno Evaluado:** Rama `main` (Post-Sprint 08 / Cobertura de 658 Pruebas Automatizadas)  
**Alcance Técnico:** Backend FastAPI (`aplicacion/backend/`) y Frontend React 19 / TypeScript (`aplicacion/frontend/`)  
**Base de Datos Objetivo:** PostgreSQL 16 alojado en Supabase (`ieaxmtxpcrldbvmqwbyt.supabase.co`)  

---

## 1. Resumen Ejecutivo y Diagnóstico Global

El presente informe consolida los hallazgos de la auditoría técnica integral realizada sobre la totalidad del código fuente del **Sistema Web P2P de Mentorías Universitarias de la EPIS-UPT**.

### Diagnóstico General:
Aunque el sistema exhibe un diseño conceptual robusto, alineado con los 8 módulos canónicos (`MOD-01` a `MOD-08`), 24 casos de uso (`CUS-001` a `CUS-024`) y **658 pruebas automatizadas pasando al 100%** (311 en backend con 86% de cobertura y 347 en frontend), **la plataforma se encuentra actualmente en un estado híbrido de demostración/desarrollo**. No está en condiciones operativas de producción debido a dependencias faltantes en empaquetado, servicios externos 100% simulados (como el servidor SMTP para códigos OTP), desfase en las migraciones de base de datos y adaptadores en el frontend bloqueados inmutablemente en modo `mock`.

---

## 2. Servicios Externos y Proveedores Reales (100% Simulados / Modo Demo)

### 2.1. Servidor SMTP para Autenticación OTP y Notificaciones Institucionales
* **Estado Actual:** **Inexistente.** No existen librerías de transporte de correo instaladas (`fastapi-mail`, `aiosmtplib`, `smtplib`) ni configuración de servidor SMTP institucional (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`) en `aplicacion/backend/app/core/config.py`.
* **Mecanismo Actual en Código:**
  - En [auth_service.py#L140-L153](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/auth_service.py#L140-L153), el backend genera criptográficamente el código OTP de 6 dígitos, pero **únicamente lo imprime en la consola del servidor**:
    ```python
    print(f"[AUTH DEV] >>> CÓDIGO OTP EMITIDO PARA {req.email}: {challenge.code} <<<")
    ```
  - Si la variable `APP_ENV == "development"`, el código generado se retorna adjunto en la respuesta JSON dentro de la propiedad `mockCodeHint` para que la UI lo consuma automáticamente.
* **Bypass de Prueba en Código Duro:**
  - En [auth_service.py#L226](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/auth_service.py#L226), el código `"000000"` está cableado para forzar de inmediato el error `HTTP 400 OTP_EXPIRED`.
* **Impacto en Producción:**
  - Al cambiar `APP_ENV=production`, la propiedad `mockCodeHint` se suprime por seguridad y, al no existir un relay SMTP real conectado con `@upt.pe`, **ningún estudiante o docente recibe el código en su buzón universitario**, imposibilitando el acceso formal al sistema.

---

### 2.2. Aprovisionamiento de Aulas Virtuales (Google Meet y Discord)
* **Estado Actual:** **100% sintético / Desconectado de APIs de terceros.**
* **Generación en Frontend:**
  - En [offerService.ts#L469-L473](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/offerService.ts#L469-L473), el navegador genera el enlace de la reunión mediante números pseudoaleatorios locales:
    ```typescript
    generateVirtualLink(subjectCode: string): string {
      const codePrefix = (subjectCode || 'ASESORIA').toUpperCase().replace(/[^A-Z0-9]/g, '');
      const randomHex = Math.random().toString(36).substring(2, 7);
      return `https://meet.google.com/upt-${codePrefix}-${randomHex}`;
    }
    ```
    Dicha cadena de texto arbitraria se envía en el campo `espacio_asignado` del payload hacia el backend.
* **Generación en Backend:**
  - En [catalog_support_service.py#L218-L272](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/catalog_support_service.py#L218-L272), `ServicioAprovisionamientoMeet` calcula un hash MD5 local (`f"https://meet.google.com/upt-{hash_str[:4]}-{hash_str[4:7]}"`) y `ServicioAprovisionamientoDiscord` genera una invitación simulada (`f"https://discord.gg/upt-epis-{id_sesion:04d}"`).
  - **Ninguno de estos servicios está conectado** al controlador oficial de publicación de ofertas en [endpoints/offers.py](file:///d:/sistema_web_p2p/aplicacion/backend/app/api/v1/endpoints/offers.py).

---

### 2.3. Almacenamiento de Constancias y Recursos Pedagógicos (Storage Buckets)
* **Estado Actual:** **Inexistente.** No existe integración con buckets de Supabase Storage ni AWS S3 (`boto3`).
* **Constancias de Horas de Mentoría (PDF):**
  - En [certificate_service.py#L150-L200](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/certificate_service.py#L150-L200), la generación de constancias compila el documento vectorial directamente en memoria RAM (`io.BytesIO()`) mediante ReportLab.
  - En [L180-L181](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/certificate_service.py#L180-L181), el backend estampa de forma inmutable una marca de agua diagonal:
    ```python
    canv.drawString(100, 200, "DEMO - FINES ACADÉMICOS — USO EXCLUSIVO CÁTEDRA CS-I")
    ```
  - En [L524](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/certificate_service.py#L524), el estado de emisión registrado en base de datos es `"EMITIDO_DEMO"`.
* **Recursos Académicos (.pdf, .zip, .pptx):**
  - En [resource_service.py#L98-L137](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/resource_service.py#L98-L137), los archivos subidos se almacenan como arrays de bytes dentro de la lista de Python `_memory_resources: list[dict[str, Any]] = []`. Si el proceso de Uvicorn se reinicia, todos los archivos subidos desaparecen de forma irreversible.

---

### 2.4. Evaluador Desatendido de Quórum a T-24h (Scheduler Cron)
* **Estado Actual:** **Simulado.**
* En [catalog_support_service.py#L675-L689](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/catalog_support_service.py#L675-L689), el método `verificar_registro_scheduler()` retorna un diccionario simulado:
  ```python
  return {"scheduler": "CeleryBeat / BackgroundScheduler", "job_id": "cron_quorum_t24h", "status": "REGISTERED"}
  ```
* En el ciclo de vida de la aplicación ([main.py#L11-L17](file:///d:/sistema_web_p2p/aplicacion/backend/app/main.py#L11-L17)), el evento `lifespan` de FastAPI **no inicia ningún daemon ni hilo planificador en segundo plano**. La evaluación de quórum a $T-24\text{ h}$ depende de una invocación manual vía HTTP (`POST /api/v1/quorum/evaluate-all`).

---

## 3. Estado de la Conexión y Persistencia en Supabase / PostgreSQL

Se ejecutaron pruebas empíricas directas contra la base de datos de producción de Supabase:

### 3.1. Estado de Conectividad y Tablas Físicas
* **Conexión:** Operativa (latencia: 2.24 segundos).
* **Catálogo de Tablas en Supabase:** 16 tablas detectadas.
* **Censo de Registros Reales en la Nube:**
  - `asistencias_sesion`: **0 filas**
  - `certificados_horas`: **0 filas**
  - `encuestas_calidad`: **0 filas**
  - `reservas_cupo`: **0 filas**
  - `solicitudes_demanda`: **0 filas**
  - `sesiones_mentoria`: 23 filas (datos semilla)
  - `bitacoras_pedagogicas`: 22 filas (datos semilla)
  - `auth_challenges`: 17 filas
  - `perfiles_academicos`: 9 filas
  - `alembic_version`: 1 fila (versión `'20261031_004'`)

---

### 3.2. Desfase Estructural en Migraciones de Alembic
* El árbol de migraciones oficiales en [app/db/migrations/versions/](file:///d:/sistema_web_p2p/aplicacion/backend/app/db/migrations/versions/) culmina en `004_booking_and_reservations.py`.
* **Las tablas `asistencias_sesion`, `bitacoras_pedagogicas`, `encuestas_calidad` y `certificados_horas` no están versionadas en Alembic.**
* Dichas tablas existen en Supabase únicamente porque se ejecutó un script auxiliar ([seed_demo_data.py#L29-L54](file:///d:/sistema_web_p2p/aplicacion/backend/seed_demo_data.py#L29-L54)) que ejecutó `Base.metadata.create_all(engine)` e inyectó sentencias DDL manuales (`ALTER TABLE sesiones_mentoria ADD COLUMN IF NOT EXISTS quorumevaluated_at...`).
* **Riesgo:** Si un entorno nuevo o contenedor Docker ejecuta `alembic upgrade head`, esas cuatro tablas no se crearán y las restricciones de chequeo (`chk_sesion_estado`) rechazarán los estados finales del ciclo de vida de la sesión.

---

### 3.3. Degradación Silenciosa a Memoria (`get_optional_session`)
* En [app/db/session.py#L53-L73](file:///d:/sistema_web_p2p/aplicacion/backend/app/db/session.py#L53-L73), si PostgreSQL falla o la conexión es inestable, `get_optional_session` captura la excepción silenciosamente y entrega `yield None`.
* En lugar de responder con un error formal `HTTP 503 Service Unavailable`, la mayoría de los controladores verifican `if db is None:` y **conmutan automáticamente a listas globales en memoria RAM** (`_memory_offers`, `_memory_bookings`, etc.), provocando pérdida de datos silenciosa.

---

### 3.4. Tokens TOTP de Asistencia en Memoria del Proceso
* En [attendance_service.py#L24, L128-L132](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/attendance_service.py#L24), el token rotatorio dinámico de 30 segundos reside en `_active_attendance_tokens: dict[int, dict] = {}`.
* Si Uvicorn se despliega con múltiples procesos worker (`uvicorn -w 4`) o en balanceo de carga en la nube, el check-in del estudiante fallará aleatoriamente al atenderse la solicitud en un worker distinto al que generó el token.

---

## 4. Componentes y Adaptadores en Modo Demo / Mockup en el Frontend

### 4.1. Bloqueo Rígido e Inmutable a Modo `'mock'` en Servicios Clave
* A diferencia de `bookingService` o `authService` (que exponen el método `setMode('api' | 'mock')`), los siguientes servicios se inicializan como constantes inmutables fijas en modo `'mock'` en desarrollo:
  - [attendanceService.ts#L164-L170](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/attendanceService.ts#L164-L170)
  - [bitacoraService.ts#L344-L350](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/bitacoraService.ts#L344-L350)
  - [surveyService.ts#L157-L163](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/surveyService.ts#L157-L163)
* **Impacto:** En entorno de desarrollo local, estos tres servicios **nunca se comunican con la API de FastAPI** a menos que se fuerce la variable de compilación `VITE_SERVICE_MODE=api` en un archivo `.env`.

---

### 4.2. Backdoor por Query Parameter en la Pantalla de Login
* En [LoginOtpView.tsx#L13-L16](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/LoginOtpView.tsx#L13-L16), existe una trampa de URL activa:
  ```typescript
  const [mockHint] = useState<string>(() => {
    const params = new URLSearchParams(window.location.search);
    return params.get('step') === 'otp' ? '849201' : '';
  });
  ```
  Al ingresar con `?step=otp`, se auto-inyecta un desafío mock con código visible `'849201'` y correo `estudiante@upt.pe`, eludiendo el flujo real de autenticación.

---

### 4.3. Catálogo Curricular Estático como Fallback Silencioso
* En [OfferPublishView.tsx#L24-L105](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/OfferPublishView.tsx#L24-L105), están declaradas en código duro las constantes `FALLBACK_COURSES` y `FALLBACK_TOPICS`.
* Si el endpoint `GET /api/v1/curriculum/courses` falla ([L166](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/OfferPublishView.tsx#L166)), la interfaz sustituye silenciosamente la información por la lista estática sin emitir advertencia al usuario.

---

### 4.4. Motor de Recomendaciones Ejecutado Localmente en Cliente
* En [recommendationService.ts#L481-L645](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/recommendationService.ts#L481-L645), el adaptador mock contiene arreglos estáticos de ofertas y mentores y ejecuta el algoritmo de ponderación Jaccard puramente en JavaScript en el navegador, sin consultar al motor EdRecSys del backend.

---

### 4.5. Simulación de Cámara en Control de Asistencia
* En [SessionAttendanceView.tsx#L126-L144](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/SessionAttendanceView.tsx#L126-L144), el botón "📷 Escaneo de Cámara" ejecuta `handleSimulateQrScan()`, el cual no invoca la API `navigator.mediaDevices` de la cámara web: simplemente copia de forma artificial el token que se está proyectando en pantalla en ese momento.

---

### 4.6. Módulo Huérfano de Solicitudes por Demanda (CUS03 / RF07)
* El backend expone operativamente los endpoints `POST /api/v1/bookings/requests` y `GET /api/v1/bookings/requests` ([bookings.py#L173-L219](file:///d:/sistema_web_p2p/aplicacion/backend/app/api/v1/endpoints/bookings.py#L173-L219)).
* En el frontend, [bookingService.ts](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/bookingService.ts) no tiene métodos cliente para consumirlos, y en [App.tsx](file:///d:/sistema_web_p2p/aplicacion/frontend/src/App.tsx) el botón de registro de demanda no abre ninguna ventana modal funcional.

---

## 5. Dependencias Faltantes en `requirements.txt` (Bloqueante de Empaquetado)

El archivo [aplicacion/backend/requirements.txt](file:///d:/sistema_web_p2p/aplicacion/backend/requirements.txt) contiene únicamente 12 paquetes base. No incluye dependencias que se importan de forma incondicional en los módulos de producción:

1. **`openpyxl`**: Requerido incondicionalmente en [schedule_parser_service.py#L16](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/schedule_parser_service.py#L16).
2. **`reportlab`**: Requerido para la compilación de certificados en [certificate_service.py#L9-L12](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/certificate_service.py#L9-L12).
3. **`qrcode`**: Requerido para la incrustación del código QR de verificación en [certificate_service.py#L7](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/certificate_service.py#L7).
4. **`PyPDF2`**: Requerido para la inspección y unión de documentos en [test_certificates.py#L4](file:///d:/sistema_web_p2p/aplicacion/backend/tests/test_certificates.py#L4).

> [!WARNING]
> Cualquier despliegue en un contenedor Docker limpio o servidor de integración continua ejecutando `pip install -r requirements.txt` fallará de inmediato al arrancar Uvicorn con `ModuleNotFoundError: No module named 'openpyxl'`.

---

## 6. Matriz Priorizada de Hallazgos por Severidad

| Severidad | Código | Componente / Archivo | Deficiencia / Modo Demo | Ubicación Exacta |
| :---: | :---: | :--- | :--- | :--- |
| 🔴 **CRÍTICA** | **DEP-01** | Backend: `requirements.txt` | Faltan 4 dependencias obligatorias (`openpyxl`, `reportlab`, `qrcode`, `PyPDF2`). Impide arrancar en entornos limpios. | [requirements.txt#L1-L12](file:///d:/sistema_web_p2p/aplicacion/backend/requirements.txt#L1-L12) |
| 🔴 **CRÍTICA** | **SEC-01** | Backend: `auth_service.py` | Servidor SMTP inexistente. Códigos OTP impresos en consola y bypass con `"000000"`. Nadie recibe correos en producción. | [auth_service.py#L140-L153](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/auth_service.py#L140-L153) |
| 🔴 **CRÍTICA** | **DB-01** | Backend: Migraciones Alembic | Migraciones detenidas en la versión 004. Tablas de asistencia, bitácoras, encuestas y certificados no están en Alembic. | [versions/004...](file:///d:/sistema_web_p2p/aplicacion/backend/app/db/migrations/versions/) |
| 🔴 **CRÍTICA** | **STATE-01** | Backend: `attendance_service.py` | Tokens TOTP residen en RAM del proceso Python. Falla en balanceo de carga o con múltiples workers de Uvicorn. | [attendance_service.py#L24](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/attendance_service.py#L24) |
| 🟠 **ALTA** | **UI-LOCK** | Frontend: Servicios de Asistencia, Bitácora y Encuesta | Forzados permanentemente a modo `'mock'` en desarrollo sin función `setMode()` ni toggles en la UI. | [attendanceService.ts#L164](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/attendanceService.ts#L164) |
| 🟠 **ALTA** | **ARCH-01** | Backend: `db/session.py` | `get_optional_session` oculta caídas de base de datos y conmuta silenciosamente a variables en memoria RAM. | [session.py#L53-L73](file:///d:/sistema_web_p2p/aplicacion/backend/app/db/session.py#L53-L73) |
| 🟡 **MEDIA** | **EXT-01** | Full-Stack: Google Meet y Discord | Enlaces virtuales generados mediante `Math.random()` en cliente y hashes MD5 en backend; sin integración con APIs reales. | [offerService.ts#L469](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/offerService.ts#L469) |
| 🟡 **MEDIA** | **STO-01** | Backend: Constancias y Recursos | Sin almacenamiento en Supabase Storage ni AWS S3. Constancias en RAM y recursos docentes en listas de memoria. | [resource_service.py#L98](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/resource_service.py#L98) |
| 🟡 **MEDIA** | **PDF-01** | Backend: `certificate_service.py` | Marca de agua diagonal forzada `"DEMO - FINES ACADÉMICOS"` y estado `"EMITIDO_DEMO"` en base de datos. | [certificate_service.py#L180](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/certificate_service.py#L180) |
| 🟡 **MEDIA** | **API-01** | Frontend: Solicitudes por Demanda | Endpoints de demanda académica existen en backend pero el frontend no tiene los métodos ni la vista modal conectada. | [RecommendationFeedView.tsx#L696](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/RecommendationFeedView.tsx#L696) |
| 🟡 **MEDIA** | **CRON-01** | Backend: Scheduler de Quórum | No hay motor Celery/APScheduler en segundo plano. Requiere trigger manual por HTTP. | [catalog_support_service.py#L675](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/catalog_support_service.py#L675) |
| 🟢 **MENOR** | **UI-01** | Frontend: `LoginOtpView.tsx` | Backdoor por parámetro de URL (`?step=otp`) que pre-inicializa un desafío mock con código visible `'849201'`. | [LoginOtpView.tsx#L13-L16](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/LoginOtpView.tsx#L13-L16) |
| 🟢 **MENOR** | **UI-02** | Frontend: `OfferPublishView.tsx` | Constantes `FALLBACK_COURSES` y `FALLBACK_TOPICS` hardcodeadas que ocultan fallos de red en la carga curricular. | [OfferPublishView.tsx#L24-L105](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/OfferPublishView.tsx#L24-L105) |
| 🟢 **MENOR** | **DATA-01** | Backend: Datos Hardcodeados | Nombres de estudiantes ("Joan Medina", "Renzo Antayhua") y asignación de roles cableados en código de servicios. | [profile_service.py#L40-L59](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/profile_service.py#L40-L59) |

---

## 7. Plan de Acción y Hoja de Ruta para Pase a Producción

1. **Fase 1: Estabilización de Dependencias y Migraciones (Inmediata)**
   * Actualizar [requirements.txt](file:///d:/sistema_web_p2p/aplicacion/backend/requirements.txt) agregando: `openpyxl>=3.1.5`, `reportlab>=4.2.5`, `qrcode>=8.0`, `PyPDF2>=3.0.0` y `fastapi-mail>=1.4.1` (o `aiosmtplib`).
   * Generar la migración oficial de Alembic `005_closure_tables.py` que registre formalmente `asistencias_sesion`, `bitacoras_pedagogicas`, `encuestas_calidad`, `certificados_horas` y actualice el constraint de estados de `sesiones_mentoria`.
2. **Fase 2: Infraestructura Real de Correo Electrónico (SMTP)**
   * Configurar variables `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` y `SMTP_FROM_EMAIL` en `Settings`.
   * Sustituir el `print()` en consola por el despacho de plantillas HTML institucionales a buzones `@upt.pe`.
   * Suprimir el código de bypass `"000000"` y retirar la propiedad `mockCodeHint` en respuestas JSON.
3. **Fase 3: Persistencia Robusta y Erradicación de Fallbacks a Memoria**
   * Reemplazar `Depends(get_optional_session)` por `Depends(get_session)` obligatorio en todas las operaciones transaccionales. Si la base de datos no está disponible, responder `HTTP 503 Service Unavailable`.
   * Migrar los tokens TOTP de asistencia a una tabla de base de datos con TTL o a una instancia compartida de Redis.
4. **Fase 4: Almacenamiento en Nube y Aulas Virtuales**
   * Activar e integrar Supabase Storage mediante su API REST o SDK para almacenar los archivos PDF de constancias y los recursos académicos adjuntos.
   * Modificar [certificate_service.py](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/certificate_service.py) para que la marca de agua `"DEMO"` y el estado `"EMITIDO_DEMO"` dependan de una bandera de configuración de entorno.
5. **Fase 5: Sincronización Total del Frontend**
   * Dotar a `attendanceService`, `bitacoraService` y `surveyService` de selectores de modo dinámicos (`setMode`) y priorizar la API real en desarrollo.
   * Conectar la ventana modal de "Registrar Solicitud por Demanda" en `App.tsx` implementando los métodos correspondientes en `bookingService.ts`.
