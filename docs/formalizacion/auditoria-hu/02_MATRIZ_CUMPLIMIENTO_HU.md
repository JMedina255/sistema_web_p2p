# 02 — Matriz Maestra de Cumplimiento de Historias de Usuario y Criterios de Aceptación

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT  
**Etapa:** Auditoría Integral de Cumplimiento Funcional (Fase 04-B)  
**Fecha de Auditoría:** 7 de noviembre de 2026  
**Rama:** `feat/formalizacion-ux-roles`  
**Commit Auditado:** `4cbf504`  
**Estado:** Documento Oficial de Auditoría SQA  

---

## 1. Convenciones y Estados de Cumplimiento

Para garantizar una evaluación objetiva, reproducible y basada en evidencia empírica, cada historia de usuario y criterio de aceptación se clasifica bajo la siguiente taxonomía estricta:

| Estado | Definición Operativa |
|---|---|
| **COMPLETA** | Todos los criterios de aceptación verificados con evidencia empírica en código frontend, servicios, endpoints FastAPI, persistencia, autorización y pruebas automatizadas passing. |
| **PARCIAL** | La funcionalidad opera de forma demostrable, pero presenta dependencias de adaptadores mock en partes del flujo, validaciones pendientes o limitaciones documentadas. |
| **NO IMPLEMENTADA** | No existe código funcional ni interfaces que soporten el requerimiento en el repositorio. |
| **BLOQUEADA** | Existe una dependencia técnica o error de compilación que impide su verificación o despliegue en producción. |
| **NO VERIFICABLE** | No existe evidencia documental ni suites de prueba suficientes para dictaminar su cumplimiento objetivo. |
| **FUERA DE ALCANCE** | Corresponde planificadamente a los Sprints 07, 08 o al backlog posterior (no comprometido en Sprints 01 a 06). |

---

## 2. Matriz Detallada Criterio por Criterio (Sprints 01 al 06)

A continuación se audita cada historia de usuario comprometida hasta el Sprint 06 a través de sus 9 dimensiones de ingeniería:

```
[1] Interfaz React | [2] Servicios Frontend | [3] Endpoints FastAPI | [4] Servicios de Dominio Backend | [5] Modelos y Persistencia | [6] Autorización y Ownership | [7] Pruebas Automatizadas | [8] Evidencias Documentales | [9] Comportamiento Funcional
```

---

### HU-01 (PB-002 / RF01 / CUS01): Autenticación Institucional 2FA con OTP
- **Criterio CA-01.1: Validación de dominio institucional `@upt.pe`**
  - *UI React:* `LoginOtpView.tsx` (valida regex y despliega mensaje de advertencia si no termina en `@upt.pe`).
  - *Servicios Frontend:* `authService.ts`, `apiAuthAdapter.ts` (`requestOtp(email)`).
  - *FastAPI:* `POST /api/v1/auth/otp/request` en `app/api/v1/endpoints/auth.py`.
  - *Servicio Backend:* `app/services/auth_service.py` (`AuthService.request_otp()`).
  - *Persistencia:* Tabla `otp_challenges` (PostgreSQL/SQLite) con hash SHA-256 del código.
  - *Autorización:* Endpoint público; rate limiting por IP/email.
  - *Pruebas:* Backend: `test_auth.py::test_request_otp_rejects_non_upt_domain`, `test_request_otp_rejects_malformed_email`. Frontend: `authService.test.ts` (15 tests).
  - *Evidencias:* SRS §5.3 (RF01), SAD §2.3 (Diagrama de Secuencia 1), Catálogo Excel `CUS01-U01`.
  - *Comportamiento:* Rechaza correos personales (`@gmail.com`) con HTTP 400.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-01.2: Generación, expiración (5 min) y cooldown (60s) de OTP**
  - *UI React:* Contador regresivo interactivo de 60 segundos en `LoginOtpView.tsx` antes de habilitar "Reenviar código".
  - *Servicios Frontend:* `authService.ts` gestiona timestamp de cooldown.
  - *FastAPI:* `POST /api/v1/auth/otp/resend` con validación de cooldown.
  - *Servicio Backend:* `AuthService.request_otp()` calcula `expira_en = now + 5 min`.
  - *Persistencia:* `otp_challenges.expira_en`, `otp_challenges.usado`.
  - *Autorización:* Pública.
  - *Pruebas:* Backend: `test_auth.py::test_request_otp_cooldown_rejection`, `test_verify_otp_expired_code`. Frontend: `LoginOtpView.test.tsx` (9 tests).
  - *Evidencias:* Catálogo Excel `CUS01-U02`.
  - *Comportamiento:* Bloquea reenvíos antes de 60s y rechaza códigos vencidos.
  - *Limitación/Mock:* El despacho SMTP real no está conectado a un servidor de correos institucional; imprime el código OTP en la consola del servidor o usa `123456` en local.
  - *Estado del Criterio:* **COMPLETO (Con despacho SMTP simulado)**.

- **Criterio CA-01.3: Verificación de código y emisión de JWT HS256**
  - *UI React:* Input de 6 dígitos con foco automático, recepción del token y almacenamiento en memoria/sessionStorage.
  - *Servicios Frontend:* `AuthContext.tsx` (`login()`, `initUserFromToken()`).
  - *FastAPI:* `POST /api/v1/auth/otp/verify`.
  - *Servicio Backend:* `AuthService.verify_otp()` -> `create_access_token()`.
  - *Persistencia:* `otp_challenges.usado = True` (previene reutilización).
  - *Autorización:* Token firmado con HS256, expiración a 60 minutos, claims `sub`, `roles`, `iss`.
  - *Pruebas:* Backend: `test_auth.py::test_verify_otp_success_and_jwt_token_issued`, `test_sec_02_malformed_or_tampered_jwt_signature_rejected_401`. Frontend: `LoginOtpView.test.tsx`.
  - *Evidencias:* SAD §6.1, Catálogo Excel `CUS01-U04`.
  - *Comportamiento:* Invalida el desafío OTP tras su uso y emite credencial JWT criptográfica.
  - *Estado del Criterio:* **COMPLETO**.

- **Dictamen HU-01:** **COMPLETA (Despacho de correo simulado en entorno local)**.

---

### HU-02 (PB-001 / PB-004 / RNF09): Entorno Base, Persistencia y Monitoreo de Salud
- **Criterio CA-02.1: Diagnóstico de API y CORS local**
  - *UI React:* `HealthStatus.tsx` consulta estado de FastAPI en montaje.
  - *Servicios Frontend:* `apiClient.ts` (`fetchDbHealth()`).
  - *FastAPI:* `GET /api/v1/health` en `app/api/v1/endpoints/health.py`.
  - *Servicio Backend:* Retorna `{"status": "ok", "app": "Sistema Web P2P EPIS-UPT"}`.
  - *Persistencia:* Independiente de BD.
  - *Pruebas:* Backend: `test_health.py::test_health_check_endpoint`. Frontend: `HealthStatus.test.tsx` (3 tests).
  - *Evidencias:* `docs/sprints/sprint-01.md`.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-02.2: Diagnóstico de conectividad a Base de Datos**
  - *UI React:* Renderiza indicador de salud de base de datos (PostgreSQL/Supabase) en banner o vista técnica.
  - *FastAPI:* `GET /api/v1/health/db`.
  - *Servicio Backend:* Ejecuta `SELECT 1` mediante SQLAlchemy y sanitiza credenciales en excepciones.
  - *Pruebas:* `test_session.py::test_test_db_connection_success`, `test_test_db_connection_exception_sanitizes_secret`.
  - *Evidencias:* `docs/supabase_setup_guide.md`.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-02.3: Integración Continua (CI)**
  - *Pipeline:* `.github/workflows/ci.yml` ejecuta linter, pruebas de frontend (Vitest) y backend (Pytest).
  - *Evidencias:* GitHub Actions Run ID `39331555735`.
  - *Estado del Criterio:* **COMPLETO**.

- **Dictamen HU-02:** **COMPLETA**.

---

### HU-03 (PB-003 / RF02 / RN-02 / CUS01): Consentimiento Digital (Ley N° 29733)
- **Criterio CA-03.1: Modal forzado en primer login y persistencia legal**
  - *UI React:* `ConsentModalView.tsx` intercepta al usuario si `consentStatus.has_consented === false`. Cláusulas legales de Ley N° 29733 desplegadas.
  - *Servicios Frontend:* `consentService.ts` (`getConsentStatus()`, `acceptConsent()`).
  - *FastAPI:* `GET /api/v1/consent/status`, `POST /api/v1/consent/accept`.
  - *Servicio Backend:* `app/services/consent_service.py` (`ConsentService.record_consent()`).
  - *Persistencia:* Tabla `consentimientos_legales` (`id_consentimiento`, `usuario_email`, `accepted=True`, `ip_origen`, `fecha_registro`).
  - *Autorización:* Requiere token JWT válido; asigna al `sub` autenticado.
  - *Pruebas:* Backend: `test_consent.py` (7 tests), `test_security_rbac.py::test_sec_18`. Frontend: `ConsentModalView.test.tsx` (4 tests).
  - *Evidencias:* SRS §5.3 (RF02), §5.4 (RN-02), Catálogo Excel `CUS01-U03`, `CUS01-F01`.
  - *Comportamiento:* Cierra modal y permite navegación normal tras aceptación.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-03.2: Rechazo, revocación y bloqueo normativo (RN-02)**
  - *UI React:* Botón "Rechazar y Salir" en modal o configuración; despliega banner rojo de bloqueo.
  - *FastAPI:* `POST /api/v1/consent/revoke`.
  - *Servicio Backend:* `ConsentService.record_consent(accepted=False)`.
  - *Persistencia:* Actualiza estado en `consentimientos_legales`.
  - *Autorización:* Ownership verificado.
  - *Pruebas:* Backend: `test_consent.py::test_revoke_consent_success`, `test_sec_18_unconsented_user_blocked_from_reservations_rn02`.
  - *Comportamiento:* Si un usuario sin consentimiento intenta reservar vacantes, recibe HTTP 403 `CONSENT_REQUIRED`.
  - *Estado del Criterio:* **COMPLETO**.

- **Dictamen HU-03:** **COMPLETA**.

---

### HU-04 (PB-005 / RF03 / RN-03 / CUS10): Gestión de Roles y Verificación de Mérito
- **Criterio CA-04.1: Asignación de rol mentor con mérito académico (ciclo >= VII)**
  - *UI React:* `AdminDashboardView.tsx` permite buscar estudiante y pulsar "Promover a Mentor".
  - *Servicios Frontend:* `roleService.ts` (`promoteToMentor()`).
  - *FastAPI:* `POST /api/v1/roles/promote-mentor`.
  - *Servicio Backend:* `RoleService.promote_to_mentor()`. Valida `ciclo_actual >= 7` en `perfiles_academicos`.
  - *Persistencia:* Tupla en tabla `usuario_roles` (`id_rol=2`, `activo=True`, `asignado_por`).
  - *Autorización:* Exige claim `administrador` verificado en token JWT.
  - *Pruebas:* Backend: `test_roles.py` (6 tests), `test_security_rbac.py::test_sec_04`. Frontend: `AdminDashboardView.test.tsx` (4 tests).
  - *Evidencias:* SRS §5.3 (RF03), §5.4 (RN-03), SAD §2.2.
  - *Comportamiento:* Asigna rol y actualiza privilegios inmediatamente.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-04.2: Rechazo determinista por mérito insuficiente (ciclo < VII)**
  - *UI React:* Muestra alerta de infracción de regla RN-03.
  - *FastAPI:* `POST /api/v1/roles/promote-mentor` responde HTTP 400.
  - *Servicio Backend:* Detecta `ciclo_actual < 7` y aborta con código `MERIT_RULE_VIOLATION`.
  - *Persistencia:* No modifica `usuario_roles`.
  - *Pruebas:* Backend: `test_roles.py::test_promote_mentor_rejects_student_below_seventh_cycle`.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-04.3: Denegación de autopromoción y control de acceso administrativo**
  - *FastAPI:* Protegido por `require_role("administrador")`.
  - *Pruebas:* `test_security_rbac.py::test_sec_04_mentee_attempts_to_promote_another_student_forbidden_403`, `test_sec_05`.
  - *Estado del Criterio:* **COMPLETO**.

- **Limitación Identificada:**
  - En modo memoria/desarrollo, `RoleService` inicializa un diccionario estático con 3 cuentas semilla (`admin.epis@upt.pe`, `mentor.avanzado@upt.pe`, `2022073504@upt.pe`). La interfaz de administración carece de un paginador general de alumnos matriculados y depende de la búsqueda individual por correo.
- **Dictamen HU-04:** **COMPLETA (Con scaffold de semillas en modo memoria)**.

---

### HU-05 (PB-006 / RF05 / CUS21): Exploración del Catálogo Curricular
- **Criterio CA-05.1: Búsqueda reactiva de materias y temas silábicos en tiempo real**
  - *UI React:* `CurriculumCatalogView.tsx` incluye buscador por texto y filtro por ciclo (I al IV).
  - *Servicios Frontend:* `curriculumService.ts` (`getCourses()`).
  - *FastAPI:* `GET /api/v1/curriculum/courses`.
  - *Servicio Backend:* `CurriculumService.get_catalog()`.
  - *Persistencia:* Tablas `asignaturas`, `unidades_silabicas`, `temas_silabicos` pobladas con datos oficiales de la EPIS.
  - *Autorización:* Endpoint público para usuarios autenticados y visitantes.
  - *Pruebas:* Backend: `test_curriculum.py` (7 tests). Frontend: `CurriculumCatalogView.test.tsx` (4 tests).
  - *Evidencias:* SRS §5.3 (RF05), §6.2.3 (CUS21), Catálogo Excel `CUS21-U01..A01`.
  - *Comportamiento:* Filtra instantáneamente y resalta temas coincidentes.
  - *Estado del Criterio:* **COMPLETO**.

- **Dictamen HU-05:** **COMPLETA**.

---

### HU-06 (PB-007 / RF04 / RN-03 / CUS15): Perfiles Formativos y Matriz Semanal 6x11
- **Criterio CA-06.1: Reemplazo atómico transaccional de disponibilidad horaria**
  - *UI React:* `ProfileAvailabilityView.tsx` con grilla interactiva de 6 días (Lunes a Sábado) x 11 bloques (08:00 a 20:00).
  - *Servicios Frontend:* `profileService.ts` (`updateMyProfile()`, `updateMyAvailability()`).
  - *FastAPI:* `PUT /api/v1/profiles/me`, `POST /api/v1/profiles/{email}/availability`.
  - *Servicio Backend:* `ProfileService.update_availability()` ejecuta transacción `DELETE FROM disponibilidades_horarias WHERE ...` seguido de inserción en lote.
  - *Persistencia:* Tablas `perfiles_academicos` y `disponibilidades_horarias`.
  - *Autorización:* Ownership verificado; un alumno no puede alterar la agenda de otro (`HTTP 403`).
  - *Pruebas:* Backend: `test_profiles.py` (11 tests), `test_security_rbac.py::test_sec_07`. Frontend: `ProfileAvailabilityView.test.tsx` (5 tests).
  - *Evidencias:* SRS §5.3 (RF04), §6.2.3 (CUS15), SAD §2.2 (Diagrama 7).
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-06.2: Alerta preventiva de mérito RN-03 en formulario**
  - *UI React:* Al seleccionar rol Mentor con ciclo < VII, renderiza alerta roja pedagógica.
  - *Pruebas:* Frontend: `ProfileAvailabilityView.test.tsx::2. Muestra advertencia de la regla RN-03 al seleccionar Mentor con ciclo menor a VII`.
  - *Estado del Criterio:* **COMPLETO**.

- **Dictamen HU-06:** **COMPLETA**.

---

### HU-07 (PB-008 / RNF01 / RNF02): Aislamiento Multiusuario y Control RLS
- **Criterio CA-07.1: Prevención de acceso cruzado entre cuentas (*Cross-Access*)**
  - *Implementación:* Dependencia `check_resource_ownership(current_user, target_email)` en FastAPI.
  - *Pruebas:* `test_authorization.py` (11 tests de aislamiento), `test_security_rbac.py::test_sec_06, test_sec_07, test_sec_08`.
  - *Comportamiento:* Retorna HTTP 403 ante cualquier intento de consulta o edición ajena sin rol admin.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-07.2: Políticas Row Level Security en Base de Datos**
  - *Implementación:* Script SQL `aplicacion/backend/scripts/supabase_rls_sprint02.sql` define políticas `auth.jwt() ->> 'email' = usuario_email`.
  - *Evidencias:* SAD §10.1 (DDL RLS).
  - *Estado del Criterio:* **COMPLETO**.

- **Dictamen HU-07:** **COMPLETA**.

---

### HU-08 (PB-004 / PB-031 / RNF09): Interfaces OpenAPI y Cobertura de Pruebas
- **Criterio CA-08.1: Contratos Pydantic y TypeScript tipados**
  - *Backend:* Esquemas en `app/schemas/` fuertemente tipados con Pydantic v2.
  - *Frontend:* Tipos e interfaces en `src/services/` y `src/types/`.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-08.2: Cobertura de pruebas automatizadas >= 70%**
  - *Backend:* 237 pruebas pasando, **85.13% de cobertura** (supera el 70%).
  - *Frontend:* 311 pruebas pasando, **>85% de cobertura de componentes**.
  - *Estado del Criterio:* **COMPLETO**.

- **Dictamen HU-08:** **COMPLETA**.

---

### HU-09 (PB-009 / RF08 / RN-04 / RN-05 / CUS06): Publicación de Ofertas de Mentoría
- **Criterio CA-09.1: Validación de antelación obligatoria > 24 horas (RN-04)**
  - *UI React:* `OfferPublishView.tsx` valida fecha seleccionada y bloquea el botón si antelación <= 24h.
  - *Servicios Frontend:* `offerService.ts` (`validateOffer()`, `publishOffer()`).
  - *FastAPI:* `POST /api/v1/offers/`.
  - *Servicio Backend:* `app/services/offer_service.py` (`OfferService.publish_offer()`) rechaza con HTTP 400 y código `ADVANCE_NOTICE_VIOLATION`.
  - *Pruebas:* Backend: `test_offers.py` (14 tests). Frontend: `OfferPublishView.test.tsx` (7 tests).
  - *Evidencias:* SRS §5.3 (RF08), §5.4 (RN-04), `docs/diseño/TRAZABILIDAD_PUBLICACION_OFERTAS.md`.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-09.2: Asignación inmutable de aforo según modalidad (RN-05)**
  - *UI React:* Modalidad "Presencial" fija aforo en 10; modalidad "Virtual" fija aforo en 20. Deshabilita edición manual de aforo.
  - *Servicio Backend:* Valida coherencia de aforo según modalidad.
  - *Persistencia:* Tabla `sesiones_mentoria` (`aforo_maximo`, `modalidad`).
  - *Pruebas:* Backend: `test_offers.py::test_publish_offer_capacity_rules`. Frontend: `OfferPublishView.test.tsx::3. Al cambiar a modalidad Virtual, actualiza reactivamente el aforo a 20 estudiantes`.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-09.3: Autorización exclusiva para mentores verificados**
  - *FastAPI:* `require_role(["mentor", "administrador"])`.
  - *Pruebas:* Backend: `test_security_rbac.py::test_sec_15`.
  - *Estado del Criterio:* **COMPLETO**.

- **Limitaciones Identificadas:**
  - El aprovisionamiento de infraestructura física (aulas asignadas dinámicamente) y virtual (enlaces Meet/Discord automáticos) no está integrado con APIs de Google o Discord; requiere que el mentor escriba el texto del aula o URL (corresponde a PB-033/PB-034 en backlog posterior).
  - En la interfaz del mentor, el listado de sesiones utiliza almacenamiento local (`localStorage`) en modo desconectado.
- **Dictamen HU-09:** **PARCIAL (Funcionalidad central de publicación completa; aprovisionamiento de aulas/enlaces manual)**.

---

### HU-10 (PB-010 / PB-011 / RF06 / RN-11 / CUS02): Inferencia Top-k y Feed
- **Criterio CA-10.1: Similitud coseno y ponderación de asignaturas filtro**
  - *UI React:* `RecommendationFeedView.tsx` renderiza tarjetas ordenadas de mayor a menor afinidad con desglose de puntaje.
  - *Servicios Frontend:* `recommendationService.ts` (`getOfferRecommendations()`).
  - *FastAPI:* `GET /api/v1/recommendations/offers`.
  - *Servicio Backend:* `app/services/recommendation_service.py` (`RecommendationService.rank_offers()`).
  - *Pruebas:* Backend: `test_recommendations.py` (22 tests). Frontend: `recommendationService.test.ts` (21 tests).
  - *Evidencias:* SRS §5.3 (RF06), §6.2.3 (CUS02).
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-10.2: Desempate determinista e invarianza (ORD-01 a ORD-05)**
  - *Implementación:* Regla de desempate en backend y frontend: ante similitud idéntica, prioriza mayor aforo disponible y menor fecha.
  - *Pruebas:* Frontend: `TopKOrdering.test.tsx` (9 tests de desempate determinista e invarianza ante permutación).
  - *Estado del Criterio:* **COMPLETO**.

- **Dictamen HU-10:** **COMPLETA**.

---

### HU-11 (PB-013 / RF12 / RN-05 / CUS04): Reserva Transaccional de Vacantes
- **Criterio CA-11.1: Creación de reserva en estado `PENDIENTE_CONFIRMACION`**
  - *UI React:* `BookingModalView.tsx` muestra detalles, cupos disponibles y botón "Confirmar Reserva".
  - *Servicios Frontend:* `bookingService.ts` (`reserveSeat()`).
  - *FastAPI:* `POST /api/v1/bookings/reserve`.
  - *Servicio Backend:* `app/services/booking_service.py` (`BookingService.reserve_seat()`).
  - *Persistencia:* Tabla `reservas_sesion` (`estado = 'PENDIENTE_CONFIRMACION'`, `codigo_reserva`).
  - *Pruebas:* Backend: `test_bookings.py` (52 tests). Frontend: `BookingModalView.test.tsx` (20 tests).
  - *Evidencias:* SRS §5.3 (RF12), §6.2.3 (CUS04).
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-11.2: Control transaccional de aforo y concurrencia**
  - *Implementación:* Bloqueo pesimista `SELECT ... FOR UPDATE` en PostgreSQL (o lock threading en SQLite/memoria) para prevenir condiciones de carrera. Solicitud concurrente sobre última vacante retorna HTTP 409 `CAPACITY_EXCEEDED`.
  - *Pruebas:* Backend: `test_bookings.py::test_concurrent_last_seat_reservation_prevention`.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-11.3: Prevención de duplicidad y validación de consentimiento (RN-02)**
  - *Implementación:* Verifica reserva preexistente activa y consulta `ConsentService.get_consent_status()`.
  - *Pruebas:* Backend: `test_security_rbac.py::test_sec_18`.
  - *Estado del Criterio:* **COMPLETO**.

- **Dictamen HU-11:** **COMPLETA**.

---

### HU-12 (PB-014 / RF13 / RN-08 / RN-09 / CUS24): Ratificación de Asistencia en T-24h
- **Criterio CA-12.1: Ratificación permitida con antelación > 24 horas**
  - *UI React:* Bandeja de reservas del estudiante (`MyBookingsView.tsx` o modal de reserva) con botón "Ratificar Asistencia".
  - *Servicios Frontend:* `bookingService.ts` (`confirmAttendance()`).
  - *FastAPI:* `POST /api/v1/bookings/{id}/confirm`.
  - *Servicio Backend:* `BookingService.confirm_attendance()`.
  - *Persistencia:* Actualiza `reservas_sesion.estado = 'CONFIRMADA'`, `fecha_ratificacion`.
  - *Autorización:* Titular de la cuenta o administrador verificado.
  - *Pruebas:* Backend: `test_bookings.py::test_confirm_attendance_success_before_cutoff`. Frontend: `bookingService.test.ts`.
  - *Evidencias:* SRS §5.3 (RF13), `docs/sprints/sprint-05/02-trazabilidad/MAPA_FUENTES_SPRINT_05.md`.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-12.2: Bloqueo de confirmación fuera de plazo (`delta <= 24h`)**
  - *FastAPI:* Retorna HTTP 400 con código canónico `WINDOW_CLOSED_T24H`.
  - *Pruebas:* Backend: `test_bookings.py::test_confirm_attendance_rejected_within_24h`.
  - *Estado del Criterio:* **COMPLETO**.

- **Dictamen HU-12:** **COMPLETA**.

---

### HU-13 (PB-015 / RF14 / RN-08 / RN-10 / CUS17): Desistimiento Voluntario y Liberación
- **Criterio CA-13.1: Desistimiento voluntario antes del corte y liberación de vacante**
  - *UI React:* Diálogo modal de desistimiento en bandeja de reservas.
  - *Servicios Frontend:* `bookingService.ts` (`cancelReservation()`).
  - *FastAPI:* `POST /api/v1/bookings/{id}/cancel`.
  - *Servicio Backend:* `BookingService.cancel_reservation()`.
  - *Persistencia:* Actualiza `reservas_sesion.estado = 'CANCELADA_USUARIO'` e incrementa plazas disponibles.
  - *Pruebas:* Backend: `test_bookings.py::test_cancel_reservation_releases_capacity`. Frontend: `bookingService.test.ts`.
  - *Evidencias:* SRS §5.3 (RF14).
  - *Estado del Criterio:* **COMPLETO**.

- **Dictamen HU-13:** **COMPLETA**.

---

### HU-14 (PB-017 / RF15 / RN-08 / RN-09 / CUS23): Evaluación de Quórum en T-24h
- **Criterio CA-14.1: Cálculo de 50% de quórum y transición de estados**
  - *FastAPI:* `POST /api/v1/quorum/evaluate-all`.
  - *Servicio Backend:* `app/services/booking_service.py` (`BookingService.evaluate_and_close_session_quorum()`).
  - *Persistencia:* Transiciona `sesiones_mentoria.estado` a `CONFIRMADA` (si >= 50% ratificados) o a `QUORUM_INSUFICIENTE` (si < 50%).
  - *Autorización:* Restringido a administradores institucionales o proceso desatendido del sistema.
  - *Pruebas:* Backend: `test_quorum.py` (7 tests).
  - *Evidencias:* SRS §5.3 (RF15), `docs/sprints/sprint-06.md`.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-14.2: Idempotencia y control de ejecuciones repetidas**
  - *Implementación:* Filtra sesiones que ya no estén en estado evaluable (`PUBLICADA`).
  - *Pruebas:* Backend: `test_quorum.py::test_quorum_evaluation_idempotency`.
  - *Estado del Criterio:* **COMPLETO**.

- **Limitaciones Identificadas:**
  - El trigger de evaluación se ejecuta mediante endpoint manual/administrativo o reloj simulado; el cron desatendido de producción para PostgreSQL (ej. pg_cron o Cloud Scheduler) no está aprovisionado en local.
- **Dictamen HU-14:** **PARCIAL (Lógica de quórum e idempotencia completa; automatización cron en producción pendiente)**.

---

### HU-15 (PB-018 / RF16 / RN-04 / RN-10 / CUS07): Gestión Resolutiva por el Mentor
- **Criterio CA-15.1: Modal de contingencia con opciones PROCEED, RESCHEDULE, CANCEL**
  - *UI React:* `MentorSessionsView.tsx` despliega modal de contingencia para sesiones en `QUORUM_INSUFICIENTE`.
  - *Servicios Frontend:* `offerService.ts` (`resolveQuorum()`).
  - *FastAPI:* `POST /api/v1/offers/{id_sesion}/quorum-decision`.
  - *Servicio Backend:* `OfferService.resolve_quorum_decision()`.
  - *Persistencia:*
    - `PROCEED`: estado pasa a `CONFIRMADA`.
    - `RESCHEDULE`: estado vuelve a `PUBLICADA` con nueva fecha > 24h.
    - `CANCEL`: estado pasa a `CANCELADA_QUORUM` y cancela reservas asociadas.
  - *Autorización:* Exclusivo del mentor titular de la sesión (`check_resource_ownership`).
  - *Pruebas:* Backend: `test_offers.py::test_resolve_quorum_proceed, test_reschedule, test_cancel`. Frontend: `MentorSessionsView.test.tsx` (5 tests en Vitest).
  - *Evidencias:* SRS §5.3 (RF16), §6.2.3 (CUS07), `docs/sprints/sprint-06.md`.
  - *Estado del Criterio:* **COMPLETO a nivel funcional**.

- **Problema Crítico de Compilación TypeScript:**
  - En `src/components/__tests__/MentorSessionsView.test.tsx`, líneas 79, 143 y 186, los objetos de respuesta mockeados contienen la propiedad `motivo_cancelacion`, la cual no existe en `QuorumDecisionResponse`. Aunque Vitest ejecuta la prueba exitosamente, `npm run build` falla al invocar `tsc -b`.
- **Dictamen HU-15:** **BLOQUEADA PARA BUILD DE PRODUCCIÓN (Funcionalidad 100% implementada; requiere corrección sintáctica en el mock de pruebas)**.

---

### HU-16 (PB-019 / RF17 / RN-05 / RN-12 / CUS08): Asistencia Digital QR y Bitácoras
- **Criterio CA-16.1: Generación y proyección de código QR dinámico TOTP**
  - *UI React:* `SessionAttendanceView.tsx` genera QR dinámico y admite ingreso manual de 6 dígitos.
  - *Servicios Frontend:* `attendanceService.ts` (`generateAttendanceToken()`, `checkinAttendance()`).
  - *FastAPI:* `POST /api/v1/attendance/token`, `POST /api/v1/attendance/checkin`.
  - *Servicio Backend:* `app/services/attendance_service.py` (`AttendanceService.generate_session_token()`).
  - *Persistencia:* Token con caducidad en tabla `asistencias_sesion`.
  - *Autorización:* Mentor titular emite token; mentoreado con reserva confirmada marca asistencia.
  - *Pruebas:* Backend: `test_attendance.py` (8 tests). Frontend: `SessionAttendanceView.test.tsx` (5 tests).
  - *Evidencias:* SRS §5.3 (RF17), §6.2.3 (CUS08), `docs/sprints/sprint-06.md`.
  - *Estado del Criterio:* **COMPLETO**.

- **Criterio CA-16.2: Registro de bitácora pedagógica antes de 48 horas (RN-12)**
  - *UI React:* `BitacoraFormView.tsx` bloquea el formulario con alerta roja si transcurrieron > 48 horas.
  - *Servicios Frontend:* `bitacoraService.ts` (`createBitacora()`).
  - *FastAPI:* `POST /api/v1/sessions/{id}/bitacora`.
  - *Servicio Backend:* `app/services/bitacora_service.py` (`BitacoraService.create_bitacora()`). Valida `delta <= 48h` y observaciones >= 50 caracteres.
  - *Persistencia:* Tabla `bitacoras_sesion` (`id_bitacora`, `id_sesion`, `temas_cubiertos`, `observaciones`, `nivel_dificultad`, `estado = 'PENDIENTE_REVISION'`).
  - *Autorización:* Exclusivo del mentor titular (`check_resource_ownership`).
  - *Pruebas:* Backend: `test_bitacora.py` (8 tests), `test_security_rbac.py::test_sec_10`. Frontend: `BitacoraFormView.test.tsx` (5 tests).
  - *Evidencias:* SRS §5.3 (RF17), §5.4 (RN-12), `docs/sprints/sprint-06.md`.
  - *Estado del Criterio:* **COMPLETO**.

- **Dictamen HU-16:** **COMPLETA**.

---

## 3. Resumen Consolidado del Estado de Cumplimiento (Sprints 01 al 06)

| ID Historia | PBI Asociado | Sprint | Requerimiento / Regla | Estado SQA | Observaciones y Brechas Principales |
|---|---|:---:|---|:---:|---|
| **HU-01** | PB-002 | S1 | RF01 / RN-01 / CUS01 | **COMPLETA** | Flujo 2FA funcional; entrega SMTP simulada en local. |
| **HU-02** | PB-001, PB-004 | S1 | RNF09 / RNF06 | **COMPLETA** | Arquitectura desacoplada, health endpoints y CI operativos. |
| **HU-03** | PB-003 | S2 | RF02 / RN-02 / CUS01 | **COMPLETA** | Modal forzado, persistencia legal y bloqueo RN-02 verificados. |
| **HU-04** | PB-005 | S2 | RF03 / RN-03 / CUS10 | **COMPLETA** | Mérito validado (ciclo >= VII); semillas en memoria para desarrollo. |
| **HU-05** | PB-006 | S2 | RF05 / CUS21 | **COMPLETA** | Catálogo oficial con temarios silábicos y búsqueda reactiva. |
| **HU-06** | PB-007 | S2 | RF04 / RN-03 / CUS15 | **COMPLETA** | Perfil formativo y grilla semanal 6x11 con reemplazo atómico. |
| **HU-07** | PB-008 | S2 | RNF01, RNF02 | **COMPLETA** | Aislamiento verificado; prevención total de cruce de datos. |
| **HU-08** | PB-004, PB-031 | S2 | RNF09 | **COMPLETA** | Contratos OpenAPI fuertemente tipados; cobertura backend 85.13%. |
| **HU-09** | PB-009 | S3 | RF08 / RN-04, 05 / CUS06 | **PARCIAL** | Antelación >24h y aforo inmutable listos; aprovisionamiento de aulas/enlaces manual. |
| **HU-10** | PB-010, PB-011 | S4 | RF06 / RN-11 / CUS02 | **COMPLETA** | Motor Top-k, similitud coseno y desempate determinista probados. |
| **HU-11** | PB-013 | S4 | RF12 / RN-05 / CUS04 | **COMPLETA** | Reserva transaccional con prevención de sobreaforo concurrente. |
| **HU-12** | PB-014 | S5 | RF13 / RN-08, 09 / CUS24 | **COMPLETA** | Ratificación en ventana >24h y bloqueo T-24h verificados. |
| **HU-13** | PB-015 | S5 | RF14 / RN-08, 10 / CUS17 | **COMPLETA** | Desistimiento voluntario y restitución atómica de cupos. |
| **HU-14** | PB-017 | S6 | RF15 / RN-08, 09 / CUS23 | **PARCIAL** | Evaluación de quórum e idempotencia listos; cron desatendido manual en local. |
| **HU-15** | PB-018 | S6 | RF16 / RN-04, 10 / CUS07 | **BLOQUEADA** | Lógica completa, pero falla `npm run build` por TS2353 en mock de test. |
| **HU-16** | PB-019 | S6 | RF17 / RN-05, 12 / CUS08 | **COMPLETA** | Pase de lista QR/TOTP y bitácoras pedagógicas con límite 48h. |

---

## 4. Estadísticas de Cumplimiento

### A. Alcance Comprometido en Sprints 01 al 06 (16 Historias / 19 PBIs):
- **COMPLETAS:** **13 historias (81.25%)**
- **PARCIALES:** **2 historias (12.50%)** (HU-09 por integración de aulas externas, HU-14 por cron desatendido de producción)
- **BLOQUEADAS:** **1 historia (6.25%)** (HU-15 por error TypeScript TS2353 en `npm run build`)
- **NO IMPLEMENTADAS:** **0 historias (0.0%)**

### B. Product Backlog Total del Proyecto (37 PBIs):
- **Implementados y Verificados (S1 a S6):** **19 PBIs (51.35%)**
- **Planificados para Sprints Futuros (S7 y S8):** **5 PBIs (13.51%)** (PB-020, PB-023, PB-024, PB-027, PB-037)
- **Backlog Posterior / Mejoras Fuera de Alcance:** **13 PBIs (35.14%)** (PB-012, PB-016, PB-021, PB-022, PB-025, PB-026, PB-028, PB-029, PB-030, PB-032, PB-033, PB-034, PB-035)
