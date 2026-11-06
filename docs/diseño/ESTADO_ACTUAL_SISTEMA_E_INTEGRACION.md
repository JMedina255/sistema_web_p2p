# Diagnóstico Exhaustivo del Estado Actual del Sistema y Hoja de Ruta de Integración de Flujos Reales

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I  
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas  
**Semestre Académico:** 2026-II  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Equipo Consultor:** Grupo 03 / C-SharkTeam — Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani  
**Fecha de Corte:** 06/11/2026  
**Ubicación Oficial:** `docs/diseño/ESTADO_ACTUAL_SISTEMA_E_INTEGRACION.md`  

---

## Control de Versiones

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Documento |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcárcel | Dirección EPIS | 06/11/2026 | Diagnóstico integral de la base de código construida entre el Sprint 1 y el Sprint 5. Identificación de componentes reales vs mocks, desacoplamientos de persistencia en Supabase, discordancias de esquemas JWT, evaluación de navegación por roles y plan de integración del flujo real previo al inicio del Sprint 6. |

---

## 1. Resumen Ejecutivo y Motivación

Al cierre formal del **Sprint 5** (02/11/2026), el proyecto *Sistema Web P2P de Mentorías Académicas EPIS-UPT* cuenta con un volumen sustantivo de software construido y validado mediante integración continua (CI en GitHub Actions):
* **452 pruebas automatizadas** superadas con 100% de éxito (265 pruebas en el cliente React 19 / TypeScript mediante Vitest y 187 pruebas en el backend FastAPI / Python 3.14 mediante Pytest).
* Cobertura de código superior al umbral del 70.0% estipulado en **RNF09** (90.00% en backend y 83.25% en frontend).
* Cero incidencias reportadas en linteo estricto (ESLint y Ruff).

No obstante, **el sistema opera actualmente bajo una arquitectura de "islas funcionales" o módulos independientes**. Durante los primeros cinco sprints, cada funcionalidad fue construida y verificada de manera aislada, habilitando adaptadores de simulación (*mocks*) locales en frontend, colecciones volátiles en memoria (*in-memory*) en backend, selectores de pestañas planos en la raíz (`App.tsx`) e identidades de usuario cableadas (*hardcoded*).

Previo a emprender el desarrollo del **Sprint 6** (evaluación desatendida de quórum en $T-24\text{ h}$, contingencia por quórum bajo, registro de bitácoras y marcación de asistencias provisionales), la cátedra y la coordinación técnica del proyecto han solicitado **detener el desarrollo fragmentado y unificar los avances en un flujo de aplicación real, continuo y persistente**.

El presente informe detalla la radiografía técnica del repositorio, clasifica las dependencias operativas reales vs simuladas, explicita las brechas críticas descubiertas en persistencia y autenticación, y establece el plan de acción ejecutable para culminar la integración sistémica.

---

## 2. Estado Actual de Módulos y Funcionalidades (Sprints 1 al 5)

A continuación, se documenta el estado de implementación de cada uno de los módulos canónicos previstos en el SRS (`FD03-EPIS-Informe SRS de Proyecto.md`), SAD (`FD04-EPIS-Informe SAD de Proyecto.md`) y en la planificación oficial (`PLAN_SPRINTS_Y_TAREAS.md`).

### Cuadro 2.1: Matriz de Capacidades Implementadas por Sprint

| Sprint | Módulo / PBI | Requisitos y Reglas | Componentes Frontend | Endpoints y Servicios Backend | Estado Operativo |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **S1** | Base Técnica & Acceso OTP<br>(PB-001, PB-002, PB-004) | RF01, CUS01, RNF01, RNF09, RN-01 | `LoginOtpView.tsx`<br>`HealthStatus.tsx` | `POST /api/v1/auth/request-otp`<br>`POST /api/v1/auth/verify-otp`<br>`GET /api/v1/health` | **Construido**<br>(Opera con mock por defecto en front) |
| **S1/S2** | Catálogo Curricular EPIS<br>(PB-006) | RF05, CUS21, RNF08 | `CurriculumCatalogView.tsx` | `GET /api/v1/curriculum/courses`<br>`GET /api/v1/curriculum/courses/{id}` | **Operativo Real**<br>(Conectado a PostgreSQL) |
| **S2** | Consentimiento Ley 29733<br>(PB-003) | RF02, CUS01, RN-02, RNF02 | `ConsentModalView.tsx` | `GET /api/v1/consent/status`<br>`POST /api/v1/consent/accept`<br>`POST /api/v1/consent/revoke` | **Construido**<br>(Desconectado del Login) |
| **S2** | Gestión de Roles Institucionales<br>(PB-005) | RF03, CUS10, RN-03, RNF02 | *(Sin vista propia en UI)* | `GET /api/v1/roles/users/{email}`<br>`POST /api/v1/roles/promote-mentor`<br>`POST /api/v1/roles/revoke-mentor` | **Backend Listo**<br>(Sin UI para Administrador) |
| **S2** | Perfiles & Disponibilidad Semanal<br>(PB-007) | RF04, CUS15, RN-03 | `ProfileAvailabilityView.tsx` | `GET /api/v1/profiles/me`<br>`PUT /api/v1/profiles/me`<br>`GET /api/v1/profiles/availability`<br>`PUT /api/v1/profiles/availability` | **Construido**<br>(Mock por defecto en front) |
| **S3** | Publicación de Ofertas de Mentoría<br>(PB-009) | RF08, CUS06, RN-04, RN-05, RN-06, RN-07 | `OfferPublishView.tsx` | `POST /api/v1/offers`<br>`GET /api/v1/offers` | **Desacoplado**<br>(Front publica a memoria volátil) |
| **S4** | Motor EdRecSys & Top-k Explicable<br>(PB-010, PB-011) | RF06, CUS02, RN-11, RNF03 | `RecommendationFeedView.tsx` | `GET /api/v1/recommendations/offers`<br>`GET /api/v1/recommendations/mentors`<br>`POST /api/v1/recommendations/explain`<br>`GET /api/v1/recommendations/simulation/testbench` | **Operativo Backend**<br>(API activa por defecto) |
| **S4** | Reserva Transaccional de Plazas<br>(PB-013) | RF12, CUS04, RN-05, RN-08, RNF07 | `BookingModalView.tsx` | `POST /api/v1/bookings/reserve` | **Operativo Backend**<br>(Requiere JWT real) |
| **S5** | Ratificación a T-24h y Desistimiento<br>(PB-014, PB-015) | RF13, RF14, CUS17, CUS24, RN-08, RN-09, RN-10 | `StudentBookingsView.tsx` | `GET /api/v1/bookings/my-reservations`<br>`POST /api/v1/bookings/{id}/confirm`<br>`POST /api/v1/bookings/{id}/cancel` | **Operativo Frontend/Backend**<br>(Aislado en pestaña propia) |

Fuente: Elaboración propia a partir de la inspección del código fuente y especificación de sprints.

El Cuadro 2.1 evidencia que todos los componentes comprometidos hasta el Sprint 5 se encuentran codificados y poseen suites unitarias exhaustivas; sin embargo, no forman una cadena unificada de ejecución para los usuarios finales.

---

## 3. Identificación Precisa: Conexión Real (BD/Backend) vs. Mocks y Memoria

Para determinar por qué la aplicación se comporta como un conjunto de módulos aislados, se realizó una auditoría profunda sobre la configuración de los adaptadores en cliente (`aplicacion/frontend/src/services/`) y los mecanismos de persistencia en servidor (`aplicacion/backend/app/db/` y `aplicacion/backend/app/services/`).

### 3.1. Estado de los Servicios Frontend (React / TypeScript)

A continuación, se detalla la configuración interna de cada servicio cliente y el comportamiento de sus adaptadores:

### Cuadro 3.1: Configuración de Modos en Servicios Frontend

| Servicio Cliente | Archivo Fuente | Modo por Defecto | Persistencia en Modo Mock | Persistencia en Modo API | Brecha Observada |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `authService` | [`authService.ts`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/authService.ts#L432) | `'mock'` | Memoria JavaScript local (`activeChallenge`). **No genera token JWT** en verify. | `fetch('/api/v1/auth/...')`. Guarda token en `sessionStorage` (`p2p_epis_jwt_token`). | Al estar en mock por defecto, el login no expide JWT. Cualquier vista que exija token queda bloqueada. |
| `consentService` | [`consentService.ts`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/consentService.ts#L34-L38) | `'mock'` | Navegador `localStorage` (`p2p_consent_${email}`). | `fetch('/api/v1/consent/...')`. Escribe en BD PostgreSQL (`consentimientos_legales`). | Si el usuario acepta en mock, el backend no registra el consentimiento en base de datos. |
| `profileService` | [`profileService.ts`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/profileService.ts#L30) | `'mock'` | Navegador `localStorage` (`p2p_profile_` y `p2p_availability_`). | `fetch('/api/v1/profiles/...')`. Escribe en tablas `perfiles_academicos` y `disponibilidades_horarias`. | Los perfiles guardados en frontend no alimentan el motor de recomendación backend. |
| `offerService` | [`offerService.ts`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/offerService.ts#L329) | `'mock'` | Array volátil en RAM (`this.offers = []`). Se destruye al recargar F5. | `fetch('/api/v1/offers')`. Escribe en tabla `sesiones_mentoria`. | Una oferta publicada por un mentor en mock jamás llega al catálogo de ofertas del backend. |
| `recommendationService` | [`recommendationService.ts`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/recommendationService.ts#L649) | `'api'` | Array mock de 2 ofertas sintéticas y 1 mentor sintético. | `fetch('/api/v1/recommendations/offers')`. Consume motor EdRecSys real en FastAPI. | Como consulta al backend real, **nunca ve las ofertas publicadas** en el mock de `offerService`. |
| `bookingService` | [`bookingService.ts`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/bookingService.ts#L847-L862) | `'api'` | Colección en memoria mock con simulación temporal. | `fetch('/api/v1/bookings/...')`. Requiere Bearer JWT obligatorio. | Al exigir JWT real, falla si el usuario se autenticó previamente usando el mock de `authService`. |
| `apiClient` | [`apiClient.ts`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/apiClient.ts#L6-L103) | *(Siempre API)* | No posee adaptador mock. | `fetch('/api/v1/health')` y `fetch('/api/v1/curriculum/...')`. | Opera 100% contra el backend real. |

Fuente: Elaboración propia a partir del análisis estático del código fuente en `aplicacion/frontend/src/services/`.

El Cuadro 3.1 revela una **asimetría crítica en los valores por defecto**: mientras `recommendationService` y `bookingService` esperan comunicarse en vivo con el backend (`mode = 'api'`), los servicios de `authService`, `consentService`, `profileService` y `offerService` inician por omisión en `'mock'`. Esto causa que el flujo se fracture de forma inmediata: lo que se hace en Login, Perfiles u Ofertas no impacta en las Recomendaciones ni en las Reservas.

---

### 3.2. Estado de Persistencia en Servidor y Base de Datos Supabase

El backend cuenta con una cadena de conexión válida en [`aplicacion/backend/.env`](file:///d:/sistema_web_p2p/aplicacion/backend/.env):
```env
DATABASE_URL="postgresql://postgres:Sistemap2pEPIS@db.ieaxmtxpcrldbvmqwbyt.supabase.co:5432/postgres"
```
La ejecución de `test_db_connection()` confirma conectividad exitosa con el servidor remoto de PostgreSQL en Supabase:
```text
(True, 'Conexión a PostgreSQL (Supabase) verificada con éxito', 2395.79 ms)
```

No obstante, al inspeccionar el catálogo de tablas del esquema `public` y el registro de versiones de Alembic en la base de datos real mediante script de diagnóstico, se obtienen los siguientes resultados técnicos:

```text
Alembic current version en base de datos: '20261023_002'
Tablas presentes en el esquema public:
- 'auth_challenges'            (3 registros)
- 'consentimientos_legales'    (0 registros)
- 'asignaturas'                (5 registros oficiales de Sprint 1)
- 'temas_conceptuales'         (21 registros oficiales de Sprint 1)
- 'roles'                      (3 roles: mentoreado, mentor, administrador)
- 'usuario_roles'              (0 registros)
- 'perfiles_academicos'        (0 registros)
- 'disponibilidades_horarias'  (0 registros)
- 'alembic_version'            (revisión fijada en '20261023_002')
```

### Cuadro 3.2: Diagnóstico de Migraciones Alembic vs. Tablas Físicas en Supabase

| Migración Alembic | Nombre de Revisión | Tablas Definidas en Código | ¿Existe en Supabase? | Impacto en la Aplicación Real |
| :--- | :--- | :--- | :---: | :--- |
| `001_initial_curriculum_and_auth.py` | `20261019_001` | `asignaturas`, `temas_conceptuales`, `auth_challenges` | **SÍ** ✅ | El catálogo curricular y el registro de códigos OTP persisten en la nube. |
| `002_roles_and_profiles.py` | `20261023_002` | `consentimientos_legales`, `roles`, `usuario_roles`, `perfiles_academicos`, `disponibilidades_horarias` | **SÍ** ✅ | Las estructuras relacionales existen en Supabase, aunque están desprovistas de filas de datos de prueba. |
| `003_mentoring_offers.py` | `20261026_003` | `sesiones_mentoria` | **NO** ❌ | **La tabla NO existe en Supabase**. Cuando `OfferService` intenta insertar en la BD, la sentencia SQL falla y el código cae al bloque `except Exception: db.rollback()` guardando la oferta únicamente en `_memory_offers` de la memoria RAM del servidor. |
| `004_booking_and_reservations.py` | `20261031_004` | `reservas_cupo`, `solicitudes_demanda` | **NO** ❌ | **La tabla NO existe en Supabase**. Toda reserva transaccional `POST /api/v1/bookings/reserve` que llega al backend falla a nivel de base de datos y se conmuta forzosamente a la colección en memoria `_memory_bookings`. |

Fuente: Elaboración propia a partir de consultas en tiempo real a PostgreSQL Supabase y archivos en `aplicacion/backend/app/db/migrations/versions/`.

El Cuadro 3.2 constituye un hallazgo de primer orden: **las migraciones de Alembic se detuvieron en el Sprint 2 (`20261023_002`) y nunca se ejecutaron los scripts 003 y 004 sobre la base de datos de producción/desarrollo en Supabase**. A consecuencia de esto, cualquier intento del backend de persistir ofertas o reservas reales colisiona con errores de tabla inexistente y se refugia en memoria volátil.

---

## 4. Estado de la Experiencia de Usuario (UX) y Navegación

### 4.1. Arquitectura de Navegación Actual en `App.tsx`

La interfaz raíz del cliente React ([`App.tsx`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/App.tsx#L16-L43)) no implementa enrutamiento declarativo (React Router ni rutas protegidas por rol). En su lugar, utiliza un estado local `activeTab` que renderiza una barra horizontal con 8 botones de depuración:

```tsx
// App.tsx (Líneas 265 a 408)
<button onClick={() => setActiveTab('auth')}>🔐 Acceso & OTP (T-02)</button>
<button onClick={() => setActiveTab('consent')}>⚖️ Consentimiento Ley 29733 (T-04)</button>
<button onClick={() => setActiveTab('curriculum')}>📚 Catálogo Curricular (T-10)</button>
<button onClick={() => setActiveTab('profile')}>👤 Perfil & Disponibilidad (T-11)</button>
<button onClick={() => setActiveTab('offers')}>🏷️ Publicar Ofertas (T-14)</button>
<button onClick={() => setActiveTab('recommendations')}>🎯 Recomendaciones & Reservas (T-20 / T-21 / T-23)</button>
<button onClick={() => setActiveTab('bookings')}>📅 Mis Reservas (T-25 / T-27)</button>
<button onClick={() => setActiveTab('services')}>🛰️ Monitor de Servicios (T-01)</button>
```

### 4.2. Recorrido del Usuario según su Rol Hoy en Día

La experiencia de los actores institucionales (estudiante mentoreado, mentor y administrador) se encuentra totalmente desarticulada:

#### A. Experiencia del Estudiante Mentoreado
1. **Acceso:** Ingresa a la pestaña *"🔐 Acceso & OTP"*. Introduce su correo `@upt.pe` y solicita OTP. Si está en modo mock, usa `123456`. Al validar, la pantalla muestra *"¡Acceso Institucional Exitoso!"* y el detalle técnico del token, pero **no redirige al usuario a ninguna parte**. El único botón disponible es *"Probar Otro Acceso / Reiniciar"*.
2. **Consentimiento:** El usuario debe adivinar que debe hacer clic manualmente en la pestaña *"⚖️ Consentimiento Ley 29733"*. La vista se carga con un correo cableado (`2022074255@upt.pe`). Al marcar conformidad y aceptar, muestra un mensaje de éxito, pero no enlaza con la siguiente pantalla formativa.
3. **Perfil:** El usuario hace clic en *"👤 Perfil & Disponibilidad"*. Nuevamente se inicializa con el correo por defecto. Puede elegir ciclo y materias, pero el guardado se realiza en el `localStorage` del navegador sin sincronizarse con el backend.
4. **Recomendaciones:** El estudiante navega a *"🎯 Recomendaciones & Reservas"*. Esta vista se comunica con el backend (`/api/v1/recommendations/offers`). Si el usuario no inició sesión en modo API, al hacer clic en *"Reservar"* en una tarjeta, el componente bloquea la acción mediante un `alert()` de navegador indicando que se requiere sesión `@upt.pe`, y lo regresa a la pestaña de login.
5. **Mis Reservas:** Tras reservar con éxito, el diálogo modal de confirmación cuenta con un botón que conmuta la pestaña a *"📅 Mis Reservas"*. En esta pestaña el estudiante puede consultar sus plazas, ratificar antes de $T-24\text{ h}$ o desistir voluntariamente.

#### B. Experiencia del Mentor Académico
1. **Inexistencia de Portal o Tablero de Mentor:** El sistema no reconoce dinámicamente si el usuario logueado ostenta el rol de mentor. Cualquier estudiante de cualquier ciclo puede pulsar la pestaña *"🏷️ Publicar Ofertas"*.
2. **Publicación Desconectada:** El formulario de ofertas se carga con el nombre de *"Joan Cristian Medina Quispe"* y correo `2022074255@upt.pe` fijados en código. Al hacer clic en *"Publicar Oferta Formativa"*, la oferta se inserta en el array en memoria del mock local de frontend.
3. **Imposibilidad de Supervisión:** No existe ninguna vista o pestaña donde el mentor pueda ver las sesiones que ha publicado, cuántos estudiantes se han inscrito, quiénes han ratificado o si se alcanzó el 50% de quórum (**RN-09**).

#### C. Experiencia del Administrador Institucional
1. **Ausencia Absoluta de Interfaz:** No existe ninguna pestaña, panel o pantalla administrativa en el frontend para el rol `administrador`.
2. Las capacidades construidas en el backend (promoción de mentores con verificación de mérito de ciclo $\ge \text{VII}$ en `POST /api/v1/roles/promote-mentor`, revocación de credenciales en `POST /api/v1/roles/revoke-mentor` y cálculo global de quórum en `POST /api/v1/quorum/evaluate`) solo pueden consumirse mediante Swagger UI (`http://localhost:8000/docs`) o herramientas de consola como `curl`/`pytest`.

---

## 5. Brechas de Integración y Desacoplamientos Críticos

A partir de la trazabilidad entre frontend, backend y persistencia, se han aislado **ocho desacoplamientos arquitectónicos específicos** que impiden el flujo real de la aplicación:

### Brecha 1: Incompatibilidad de Claims en el Token JWT de Backend
En [`auth_service.py`](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/auth_service.py#L282-L289), la emisión del token JWT institucional al verificar el código OTP se realiza con la siguiente estructura de datos:
```python
# auth_service.py (Líneas 282-289)
role = "administrador" if email.startswith("admin") else "estudiante"
jwt_token = create_access_token(
    data={
        "sub": email,
        "email": email,
        "role": role,  # <-- Campo SINGULAR 'role' de tipo string
    }
)
```
Sin embargo, los guardas de seguridad y autorización en todos los demás endpoints del backend ([`bookings.py`](file:///d:/sistema_web_p2p/aplicacion/backend/app/api/v1/endpoints/bookings.py#L31), [`profiles.py`](file:///d:/sistema_web_p2p/aplicacion/backend/app/api/v1/endpoints/profiles.py#L50) y [`roles.py`](file:///d:/sistema_web_p2p/aplicacion/backend/app/api/v1/endpoints/roles.py#L68)) buscan explícitamente una lista de roles bajo la clave en plural `"roles"`:
```python
# bookings.py (Línea 31)
if decoded and "administrador" in decoded.get("roles", []):
    is_admin = True
```
Como el token emitido por el servicio real de autenticación contiene `"role": "estudiante"`, la invocación de `decoded.get("roles", [])` retorna una lista vacía `[]`. Por consiguiente:
* Un administrador logueado en la vida real es rechazado con error 403 en endpoints que requieren rol de administración porque el claim `'roles'` no existe.
* Las pruebas automatizadas no detectaron este fallo porque en [`test_authorization.py`](file:///d:/sistema_web_p2p/aplicacion/backend/tests/test_authorization.py#L14) y [`test_bookings.py`](file:///d:/sistema_web_p2p/aplicacion/backend/tests/test_bookings.py#L245) los tests crean sus propios tokens sintéticos con `create_access_token({"sub": email, "roles": ["mentoreado"]})` en lugar de invocar a `AuthService.verify_otp`.

---

### Brecha 2: Desincronización del Catálogo Curricular entre Front y Back
Existe una discrepancia de nomenclatura y llaves primarias en el catálogo curricular:
* En la base de datos real de Supabase y en [`001_initial_curriculum_and_auth.py`](file:///d:/sistema_web_p2p/aplicacion/backend/app/db/migrations/versions/001_initial_curriculum_and_auth.py#L100-L148):
  * Asignatura 1: `CALC-101` (*Cálculo I*), temas con IDs 1, 2, 3, 4.
  * Asignatura 2: `CALC-201` (*Cálculo II*), temas con IDs 5, 6, 7, 8.
  * Asignatura 3: `ALGO-202` (*Algoritmos y Estructuras de Datos*), temas con IDs 9, 10, 11, 12, 13.
* En el fallback local de [`OfferPublishView.tsx`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/OfferPublishView.tsx#L23-L100):
  * Asignatura 1: `CI-101` (*Cálculo I*), temas con IDs 101, 102, 103.
  * Asignatura 3: `SI-202` (*Algoritmos y Estructuras de Datos*), temas con IDs 301, 302, 303.
* En [`recommendationService.ts`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/services/recommendationService.ts#L510-L530):
  * Asignatura 1: `CI-101`.
  * Asignatura 3: `AED-201`.
Si el mentor publica una oferta usando los códigos locales del frontend (`SI-202`, tema `301`), el backend y el recomendador la rechazan o no pueden vincularla con las asignaturas de la base de datos oficial.

---

### Brecha 3: Omisión de Migraciones de Base de Datos en Supabase
Como se demostró en el Cuadro 3.2, la base de datos remota se encuentra en la revisión `20261023_002`. Las tablas correspondientes a los Sprints 3 y 4:
* `sesiones_mentoria` (definida en `003_mentoring_offers.py`)
* `reservas_cupo` (definida en `004_booking_and_reservations.py`)
* `solicitudes_demanda` (definida en `004_booking_and_reservations.py`)

no han sido desplegadas con `alembic upgrade head`. Mientras estas tablas no existan en Supabase, el backend nunca podrá funcionar de forma persistente real con PostgreSQL.

---

### Brecha 4: Ausencia de Contexto Global de Sesión en el Frontend
En React, el estado de autenticación se encuentra fragmentado:
* `LoginOtpView` maneja su propio estado `verifyResult`. Al finalizar con éxito, guarda el token en `sessionStorage`, pero **no dispara ningún evento, callback ni actualización de contexto hacia `App.tsx`**.
* En `App.tsx`, la función `resolveStudentEmail()` lee el token una única vez cuando el componente se evalúa. Si el usuario se loguea posteriormente, `App.tsx` no se entera del cambio de sesión a menos que el usuario fuerce una recarga completa del navegador.
* No existe un proveedor `<AuthProvider>` que suministre `user`, `token`, `roles`, `hasConsented` y `logout()` a todos los componentes de la aplicación.

---

### Brecha 5: Identidades y Correos Cableados (*Hardcoded*) en Props
Múltiples componentes conservan valores por defecto estáticos correspondientes a los correos de los desarrolladores:
* En [`ConsentModalView.tsx`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/ConsentModalView.tsx#L13): `userEmail = '2022074255@upt.pe'`
* En [`ProfileAvailabilityView.tsx`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/ProfileAvailabilityView.tsx#L36): `userEmail = '2022074255@upt.pe'`
* En [`OfferPublishView.tsx`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/OfferPublishView.tsx#L120-L121): `mentorEmail = '2022074255@upt.pe'`, `mentorName = 'Joan Cristian Medina Quispe'`
* En [`App.tsx`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/App.tsx#L474-L481): Los componentes se renderizan como `<ConsentModalView />`, `<ProfileAvailabilityView />` y `<OfferPublishView />` sin pasarle los datos del usuario logueado en sesión.

---

### Brecha 6: Falta de Conducción Obligatoria del Consentimiento Digital (Ley 29733)
El requerimiento **RF02 / RN-02** estipula que ningún estudiante puede interactuar con el sistema ni reservar cupos si no ha formalizado previamente el consentimiento informado. Actualmente:
* El usuario puede saltarse completamente la pestaña de consentimiento e ir directo a recomendaciones o catálogo.
* El rechazo del consentimiento en `ConsentModalView` emite un mensaje en pantalla, pero no bloquea la navegación general del resto de pestañas de `App.tsx`.

---

### Brecha 7: Inexistencia de Vistas para los Flujos Operativos del Mentor
El mentor actualmente solo cuenta con un formulario de publicación de ofertas. Para poder completar el ciclo formativo y prepararse para el Sprint 6, el mentor carece de:
1. Una vista *"Mis Mentorías Publicadas"* donde pueda consultar sus sesiones activas con fechas, asignaturas, modalidad y recintos.
2. La lista de inscritos por sesión con desglose de cupos ocupados vs disponibles.
3. El estado de quórum en tiempo real (cuántos confirmaron y si se alcanzó el 50% reglamentario).

---

### Brecha 8: Inexistencia del Panel de Supervisión Administrativa
El Administrador Institucional (personal docente o directivo de EPIS) no dispone de ninguna pantalla para:
1. Ver y aprobar la postulación de estudiantes de ciclo $\ge \text{VII}$ al rol de Mentor (**RN-03**).
2. Monitorear las sesiones que no alcanzaron quórum y requieran contingencia.
3. Supervisar la salud del sistema y la base de datos de manera centralizada.

---

## 6. Plan de Acción y Hoja de Ruta de Integración del Flujo Real

Para superar la fragmentación modular y consolidar un flujo integral continuo antes de codificar las reglas del Sprint 6, se establece la siguiente hoja de ruta secuencial estructurada en cuatro fases de trabajo:

```
+-----------------------------------------------------------------------------------+
|                           HOJA DE RUTA DE INTEGRACIÓN                             |
+-----------------------------------------------------------------------------------+
|  FASE 1: Saneamiento de Persistencia y Seguridad Backend                          |
|  - Aplicar migraciones Alembic (003 y 004) a Supabase PostgreSQL.                  |
|  - Corregir emisión de claims JWT ('roles': [...]) en AuthService.verify_otp.     |
|  - Homologar códigos canónicos del catálogo curricular (CALC-101, ALGO-202, etc.).|
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|  FASE 2: Unificación de Servicios Frontend y Modo Operativo Único                 |
|  - Unificar modo operativo a 'api' por defecto en todos los servicios de front.   |
|  - Erradicar correos 'hardcoded' (2022074255@upt.pe) en componentes.              |
|  - Garantizar propagación transparente de token Bearer en apiClient y servicios.  |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|  FASE 3: Arquitectura de Estado Global y Navegación por Roles en React            |
|  - Implementar AuthContext / SessionContext para sesión, roles y consentimiento.  |
|  - Reemplazar barra de 8 pestañas por un Application Shell institucional con:     |
|    * Pantalla de Login OTP como puerta de entrada obligatoria.                    |
|    * Modal bloqueante de Consentimiento Ley 29733 ante primer ingreso (RN-02).    |
|    * Navegación diferenciada según rol activo: Mentoreado, Mentor, Admin.         |
|    * Selector de cambio de rol para usuarios con privilegios múltiples.           |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|  FASE 4: Vistas Complementarias y Preparación de Terreno para Sprint 6            |
|  - Vista de 'Mis Sesiones de Mentor' (gestión de ofertas, nómina y estado quórum).|
|  - Vista de 'Administración Institucional' (gestión de roles RN-03 y monitoreo).  |
|  - Conexión de la ratificación T-24h con la evaluación de quórum de Sprint 6.     |
+-----------------------------------------------------------------------------------+
```

---

### Fase 1: Saneamiento de Persistencia y Seguridad Backend
1. **Despliegue de Esquemas en Supabase:**
   * Ejecutar en el backend la migración pendiente de Alembic:
     ```bash
     cd aplicacion/backend
     alembic upgrade head
     ```
   * Verificar en PostgreSQL la creación efectiva de las tablas `sesiones_mentoria`, `reservas_cupo` y `solicitudes_demanda`.
2. **Corrección de Claims en `AuthService.verify_otp`:**
   * Modificar [`auth_service.py`](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/auth_service.py#L282-L289) para que consulte los roles institucionales del usuario mediante `RoleService.get_user_roles(db, email)` y emita el claim en formato de lista:
     ```python
     user_roles = RoleService.get_user_roles(db, email)
     jwt_token = create_access_token(
         data={
             "sub": email,
             "email": email,
             "roles": user_roles,
         }
     )
     ```
   * Esto habilitará que cualquier token emitido por el login real sea aceptado inmediatamente por los guardas de autorización de reservas, roles y ofertas.
3. **Homologación Curricular:**
   * Alinear las constantes de fallback de frontend en `OfferPublishView.tsx` y `recommendationService.ts` con los códigos canónicos de la base de datos oficial (`CALC-101`, `CALC-201`, `ALGO-202`, `POO-301`, `BDD-401`).

---

### Fase 2: Unificación de Servicios Frontend
1. **Modo Único de Servicio:**
   * Establecer la directiva de configuración para que en desarrollo normal y producción el modo por omisión de `authService`, `consentService`, `profileService`, `offerService`, `recommendationService` y `bookingService` sea `'api'`.
   * Preservar el modo `'mock'` estrictamente cuando la variable `import.meta.env.MODE === 'test'` o cuando el usuario seleccione explícitamente el modo simulación en pruebas unitarias de Vitest.
2. **Erradicación de Valores Cableados (*Hardcoded*):**
   * Eliminar los valores por defecto `userEmail = '2022074255@upt.pe'` y `mentorEmail = '2022074255@upt.pe'`.
   * Exigir que los componentes reciban la identidad obligatoriamente desde el contexto global autenticado.

---

### Fase 3: Estado Global y Shell de Aplicación por Roles
1. **Creación del `AuthContext`:**
   * Crear `src/context/AuthContext.tsx` gestionando los siguientes estados reactivos:
     * `user: { email: string; roles: string[] } | null`
     * `token: string | null`
     * `hasConsented: boolean`
     * `activeRole: 'mentoreado' | 'mentor' | 'administrador'`
     * `login(token: string): void`
     * `logout(): void`
     * `setConsented(status: boolean): void`
     * `switchRole(role: 'mentoreado' | 'mentor' | 'administrador'): void`
2. **Reingeniería de `App.tsx` (Shell Institucional):**
   * Si no hay sesión activa: renderizar únicamente la vista de acceso institucional (`LoginOtpView`).
   * Si hay sesión activa pero `hasConsented === false`: renderizar obligatoriamente el diálogo modal de consentimiento legal (**Ley N° 29733 / RN-02**) impidiendo el acceso a cualquier otra vista hasta que se registre la aceptación.
   * Si hay sesión y consentimiento: renderizar la barra de navegación superior institucional con:
     * Datos del usuario logueado (avatar con iniciales, correo y ciclo).
     * Selector desplegable de rol activo (para alternar entre *Mentoreado* y *Mentor* si posee ambos roles).
     * Enlaces de navegación acordes al rol:
       * **Rol Mentoreado:** *1. Recomendaciones Top-k* | *2. Mis Reservas (Ratificar/Desistir)* | *3. Catálogo Curricular* | *4. Mi Perfil*.
       * **Rol Mentor:** *1. Mis Mentorías Programadas* | *2. Publicar Nueva Oferta* | *3. Mi Disponibilidad*.
       * **Rol Administrador:** *1. Gestión de Roles & Mérito* | *2. Monitoreo de Quórum* | *3. Monitor de Servicios*.
     * Botón de cierre de sesión seguro (*"Cerrar Sesión"*).

---

### Fase 4: Preparación para el Sprint 6 (Quórum y Bitácoras)
1. **Componente de Gestión de Mentor (`MentorSessionsView.tsx`):**
   * Crear la interfaz que consuma `GET /api/v1/offers?mentor_email={email}` y `GET /api/v1/bookings/session/{id_sesion}`.
   * Mostrar el contador de cupos confirmados en relación con el aforo ($n / 10$ o $n / 20$) y la etiqueta reactiva de quórum:
     * Si confirmados $\ge 50\%$: distintivo verde *"Quórum Alcanzado"*.
     * Si confirmados $< 50\%$ a $T-24\text{ h}$: distintivo ámbar *"Quórum Insuficiente"*, habilitando los botones de decisión del mentor (**T-32**): *Confirmar Dictado Excepcional* o *Cancelar Sesión*.
2. **Integración con Bitácoras y Asistencias (T-34 / T-36):**
   * Para sesiones ratificadas que alcancen su fecha de inicio, la interfaz del mentor habilitará la marcación de asistencia individual (`ASISTIDA` vs `INASISTENCIA`) y el formulario de bitácora pedagógica.

---

## 7. El Flujo Real Integrado Resultante (End-to-End)

Con la ejecución del plan de acción propuesto, el sistema funcionará de principio a fin conforme al siguiente recorrido real continuo:

```
[1. Inicio de Sesión]
    Estudiante ingresa '2022073504@upt.pe' en LoginOtpView -> API FastAPI genera OTP en PostgreSQL.
    Estudiante valida su código OTP de 6 dígitos.
    API emite JWT HS256 con claims: sub='2022073504@upt.pe', roles=['mentoreado', 'mentor'].
          │
          ▼
[2. Verificación de Consentimiento - Ley 29733 (RF02 / RN-02)]
    Shell consulta GET /api/v1/consent/status?email=2022073504@upt.pe.
    Si no ha consentido, se despliega obligatoriamente ConsentModalView.
    Al aceptar, se emite POST /api/v1/consent/accept y se habilita la aplicación.
          │
          ▼
[3. Perfil y Selección de Rol (RF03 / RF04 / RN-03)]
    El usuario configura sus asignaturas de interés y su grilla horaria semanal en ProfileAvailabilityView.
    Si su ciclo es >= VII, puede ejercer el rol de Mentor o Mentoreado desde el conmutador de cabecera.
          │
   ┌──────┴──────────────────────────────────────────────────────┐
   ▼                                                             ▼
[FLUX A: Mentor Académico]                          [FLUX B: Estudiante Mentoreado]
Mentor publica oferta en OfferPublishView:          Estudiante entra a RecommendationFeedView:
- Asignatura: CALC-101 (Cálculo I).                 - EdRecSys ejecuta inferencia híbrida Top-k.
- Fecha: En 72 horas (> 24 h antelación RN-04).     - Muestra la oferta publicada por el Mentor.
- Modalidad: Presencial (Aforo estricto: 10 RN-05). - Explica compatibilidad con desglose XAI (RNF03).
API almacena en PostgreSQL (sesiones_mentoria).                   │
   │                                                             ▼
   │                                                Estudiante pulsa "Reservar Cupo" (T-21):
   │                                                - BookingModalView formaliza la inscripción.
   │                                                - Backend adquiere bloqueo pesimista FOR UPDATE.
   │                                                - Reserva guardada como PENDIENTE_CONFIRMACION.
   │                                                             │
   │                                                             ▼
   │                                                Estudiante abre "Mis Reservas" (T-25 / RF13):
   │                                                - Observa la reserva con cuenta regresiva.
   │                                                - Al estar a Delta t > 24 h, pulsa "Confirmar Asistencia".
   │                                                - Estado muta atómicamente a CONFIRMADA (RN-08).
   │                                                             │
   └──────────────────────────────┬──────────────────────────────┘
                                  ▼
[4. Transición Crítica hacia el Sprint 6: Corte T-24h y Quórum (RF15 / RF16 / RN-09)]
    Al alcanzarse la marca de tiempo de 24 horas antes del inicio de la sesión:
    - Se cierra la ventana de confirmaciones y desistimientos (RN-08 / RN-10).
    - El evaluador de quórum (T-29) computa el número de reservas CONFIRMADA sobre el aforo máximo.
    - Si la sesión cuenta con 5 o más alumnos confirmados (>= 50%), la mentoría queda ratificada.
    - Si cuenta con menos del 50%, se activa la alerta de contingencia para la decisión del mentor (T-32 / T-33).
    - Culminada la clase, el mentor registra la asistencia y la bitácora técnica (T-34 / T-36).
```

---

## 8. Conclusiones y Próximos Pasos

1. **La base de código es sólida y robusta a nivel modular:** La existencia de 452 pruebas automatizadas y coberturas superiores al 83% en frontend y 90% en backend demuestran que la lógica de negocio individual está rigurosamente programada y libre de regresiones.
2. **La causa de la fragmentación fue el enfoque de desarrollo por hitos aislados:** El uso de adaptadores mock en el cliente para independizar tareas entre Joan y Renzo, sumado a la falta de ejecución de las migraciones de base de datos de Sprint 3 y 4 en Supabase, creó la ilusión de módulos separados.
3. **El camino hacia la integración real está plenamente trazado:** La ejecución de las cuatro fases descritas en la Hoja de Ruta (despliegue de esquemas relacionales pendientes, corrección del claim JWT, unificación de modos en frontend y shell con `AuthContext`) transformará el conjunto de pruebas aisladas en un sistema web P2P cohesivo, fluido y listo para absorber los requerimientos de quórum y bitácoras del Sprint 6.
