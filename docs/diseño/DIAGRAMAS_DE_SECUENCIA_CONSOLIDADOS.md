# DIAGRAMAS DE SECUENCIA CONSOLIDADOS - FASE DE DISEÑO

**Sistema Web P2P de Mentorías Universitarias - EPIS UPT**
**Versión:** 2.0 (Fase de Diseño / Arquitectura y Construcción)
**Autores:** Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos

---

## 6.3.3. Diagramas de Secuencia del Sistema (Fase de Diseño)

### Presentación de los Diagramas de Secuencia en Fase de Diseño

En la presente **Fase de Diseño de Software**, los diagramas de secuencia formalizan el comportamiento dinámico, la sincronización de procesos y el orden cronológico estricto de los mensajes entre componentes para los **24 casos de uso canónicos** (`CUS-001` a `CUS-024`) del Sistema Web P2P de Mentorías Universitarias de la EPIS-UPT, distribuidos a través de sus **8 módulos arquitectónicos** (`MOD-01` a `MOD-08`).

Cada diagrama desglosa de manera exhaustiva las responsabilidades y mensajes a través de las capas técnicas del sistema:
1. **Actores del Sistema:** Estudiante Mentoreado (`UserRole.mentoreado`), Estudiante Mentor (`UserRole.mentor`), Administrador Institucional (`UserRole.administrador`), Director de Escuela EPIS, Coordinador Académico/Curricular, Comisión de Acreditación ICACIT, y Procesos en Segundo Plano (`SchedulerWorker` / Celery / APScheduler).
2. **Componente de Presentación / Vista React (`.tsx`):** Vistas SPA construidas con React 18, TypeScript y Tailwind CSS (`LoginOtpView.tsx`, `ConsentModalView.tsx`, `AdminDashboardView.tsx`, `OfferPublishView.tsx`, `ProfileAvailabilityView.tsx`, `CurriculumCatalogView.tsx`, `RecommendationFeedView.tsx`, `BookingModalView.tsx`, `StudentBookingsView.tsx`, `MentorSessionsView.tsx`, `SessionAttendanceView.tsx`, `BitacoraFormView.tsx`, `HistorySessionsView.tsx`, `CertificateView.tsx`, `GamificationView.tsx`, `NotificationBell.tsx`, `AnalyticsDashboardView.tsx`, `RetentionDashboardView.tsx`, `AuditLogView.tsx`, `SystemSettingsView.tsx`, `AdminCurriculumView.tsx`).
3. **Servicio y Adaptador Cliente (`.ts`):** Clientes HTTP tipados basados en Axios/Fetch (`authService.ts`, `consentService.ts`, `roleService.ts`, `offerService.ts`, `profileService.ts`, `curriculumService.ts`, `recommendationService.ts`, `bookingService.ts`, `attendanceService.ts`, `bitacoraService.ts`, `historyService.ts`, `certificateService.ts`, `gamificationService.ts`, `notificationService.ts`, `analyticsService.ts`, `auditService.ts`, `configService.ts`).
4. **Controlador y Rutas FastAPI (`.py`):** Endpoints RESTful en `app/api/v1/endpoints/` (`auth.py`, `consent.py`, `roles.py`, `offers.py`, `profiles.py`, `curriculum.py`, `recommendations.py`, `bookings.py`, `quorum.py`, `attendance.py`, `bitacora.py`, `history.py`, `certificates.py`, `gamification.py`, `notifications.py`, `analytics.py`, `audit.py`, `config.py`), con validación de esquemas Pydantic y autorización RBAC vía tokens JWT criptográficos (HS256).
5. **Servicio de Lógica de Negocio Backend (`.py`):** Capa de servicios (`auth_service.py`, `consent_service.py`, `role_service.py`, `offer_service.py`, `profile_service.py`, `curriculum_service.py`, `recommendation_service.py`, `booking_service.py`, `simulation_service.py`, `attendance_service.py`, `bitacora_service.py`, `history_service.py`, `certificate_service.py`, `reputation_service.py`, `notification_service.py`, `analytics_service.py`, `audit_service.py`, `config_service.py`).
6. **Persistencia Relacional PostgreSQL / Repositorio (SQLAlchemy ORM / Cerrojos):** Modelos de datos en Supabase/PostgreSQL con control estricto de concurrencia (`SELECT ... FOR UPDATE`, `SET LOCAL lock_timeout = '5.0s'`, transacciones ACID `db.begin()` / `db.commit()` / `db.rollback()`, políticas RLS e integridad referencial).
7. **Servicios Externos:** Servidor SMTP institucional de la Universidad Privada de Tacna (`EmailService`), generación de documentos PDF oficiales y canales WebSockets / Server-Sent Events (SSE).

### Diagrama 6.15: Diagrama de Secuencia General del Ciclo Transaccional de Mentorías

El diagrama general de secuencia formaliza la visión holística de los flujos temporales y de sincronización entre capas técnicas para el proceso transaccional neurálgico de la plataforma: la orquestación concurrente de Reserva de Cupos (`CUS-004`), Ratificación de Asistencia antes de $T-24	ext{ h}$ (`CUS-024`), y Corte Automatizado de Quórum en $T-24	ext{ h}$ (`CUS-023`) con resolución de contingencia del mentor (`CUS-007`).

```plantuml
@startuml
title Diagrama 6.15: Diagrama de Secuencia General del Ciclo de Reserva, Ratificación y Quórum
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado" as User
participant "Vista React (SPA)
(BookingModal / StudentBookings)" as UI
participant "Adaptador Cliente
(bookingService.ts)" as Client
participant "Controlador FastAPI
(endpoints/bookings.py)" as API
participant "Servicio Backend
(booking_service.py)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB
participant "Planificador Cron
(Celery / SchedulerWorker)" as Cron
participant "Servicio Email
(SMTP UPT)" as Mail
actor "Estudiante Mentor" as Mentor

== 1. Reserva Concurrente de Cupo (CUS-004) ==
User -> UI: Clic en "Reservar Cupo" (idSesion)
activate UI
UI -> Client: reserveSeat(idSesion)
activate Client
Client -> API: POST /api/v1/bookings/reserve {"id_sesion": idSesion} [Bearer JWT]
activate API
API -> Service: reserve_seat(idSesion, user_email)
activate Service
Service -> DB: BEGIN TRANSACTION
activate DB
Service -> DB: SELECT * FROM sesiones_mentoria WHERE id = :idSesion FOR UPDATE OF sesiones_mentoria
DB --> Service: Registro Sesion (aforo, cupos_ocupados)
alt Cupos disponibles > 0 y Elegibilidad Validada
    Service -> DB: INSERT INTO reservas_cupo (id_usuario, id_sesion, estado='PENDIENTE_CONFIRMACION', ticket_hash=SHA256(...))
    Service -> DB: UPDATE sesiones_mentoria SET cupos_ocupados = cupos_ocupados + 1 WHERE id = :idSesion
    Service -> DB: COMMIT
    DB --> Service: Transacción confirmada
    Service --> API: BookingResponseDTO {idReserva, estado: 'PENDIENTE_CONFIRMACION'}
    API --> Client: HTTP 201 Created {idReserva, estado: 'PENDIENTE_CONFIRMACION'}
    Client --> UI: Comprobante provisional
    UI --> User: Muestra confirmación y plazo hasta T-24h
else Conflicto de aforo o estudiante no elegible
    Service -> DB: ROLLBACK
    Service --> API: Lanza HTTPException(409, "Aforo agotado o colisión concurrente")
    API --> Client: HTTP 409 Conflict {"detail": "Aforo agotado"}
    Client --> UI: Captura error 409
    UI --> User: Alerta de denegación de reserva
end
deactivate DB
deactivate Service
deactivate API
deactivate Client
deactivate UI

== 2. Ratificación de Asistencia antes de T-24h (CUS-024) ==
User -> UI: Clic en "Confirmar Asistencia" (idReserva)
activate UI
UI -> Client: confirmBooking(idReserva)
activate Client
Client -> API: POST /api/v1/bookings/{idReserva}/confirm [Bearer JWT]
activate API
API -> Service: confirm_booking(idReserva, user_email)
activate Service
Service -> DB: SELECT * FROM reservas_cupo r JOIN sesiones_mentoria s ON r.id_sesion = s.id WHERE r.id = :idReserva
activate DB
DB --> Service: Datos Reserva y Sesión
deactivate DB
alt Tiempo restante >= 24 horas (now_utc <= s.fecha_inicio - 24h)
    Service -> DB: UPDATE reservas_cupo SET estado = 'CONFIRMADA', fecha_confirmacion = NOW() WHERE id = :idReserva
    activate DB
    Service -> DB: COMMIT
    DB --> Service: Confirmado
    deactivate DB
    Service -> Mail: Despacha ticket digital con código QR de asistencia
    activate Mail
    Mail --> Service: Despacho OK
    deactivate Mail
    Service --> API: BookingConfirmDTO {estado: 'CONFIRMADA', pase_asistencia: 'PASS-8472'}
    API --> Client: HTTP 200 OK {estado: 'CONFIRMADA', pase_asistencia: 'PASS-8472'}
    Client --> UI: Pase digital confirmado
    UI --> User: Despliega ticket digital y acceso formal
else Plazo cerrado (now_utc > s.fecha_inicio - 24h)
    Service --> API: Lanza HTTPException(400, "Ventana de ratificación vencida")
    API --> Client: HTTP 400 Bad Request {"detail": "Ventana de ratificación vencida"}
    Client --> UI: Captura error 400
    UI --> User: Informa revocación reglamentaria
end
deactivate Service
deactivate API
deactivate Client
deactivate UI

== 3. Corte Automatizado y Cómputo de Quórum en T-24h (CUS-023) ==
Cron -> API: Disparo automático de corte de quórum (sesiones a T=24h)
activate API
API -> Service: evaluate_all_active_quorums()
activate Service
Service -> DB: BEGIN TRANSACTION
activate DB
Service -> DB: UPDATE reservas_cupo SET estado = 'NO_CONFIRMADA' WHERE id_sesion = :idSesion AND estado = 'PENDIENTE_CONFIRMACION'
Service -> DB: SELECT COUNT(*) FROM reservas_cupo WHERE id_sesion = :idSesion AND estado = 'CONFIRMADA'
DB --> Service: confirmed_count (ej. 4)
deactivate DB

alt confirmed_count >= 3 (Quórum Reglamentario >= 3 confirmados, RN-05)
    Service -> DB: UPDATE sesiones_mentoria SET estado = 'CONFIRMADA' WHERE id = :idSesion
    activate DB
    Service -> DB: COMMIT
    DB --> Service: Confirmada
    deactivate DB
    Service -> Mail: Notifica realización confirmada al Mentor y a Mentoreados
    activate Mail
    Mail --> Service: Correo enviado
    deactivate Mail
    Service --> API: QuorumBatchSummaryDTO
    API --> Cron: HTTP 200 OK (Quórum alcanzado)
else confirmed_count < 3 (Quórum Insuficiente)
    Service -> DB: UPDATE sesiones_mentoria SET estado = 'QUORUM_INSUFICIENTE' WHERE id = :idSesion
    activate DB
    Service -> DB: COMMIT
    DB --> Service: Estado contingencia
    deactivate DB
    Service -> Mail: Envía alerta urgente de resolución a Mentor (CUS-007)
    activate Mail
    Mail --> Mentor: Notificación de contingencia
    deactivate Mail
    Service --> API: QuorumAlertDTO
    API --> Cron: HTTP 200 OK (Alerta emitida)
    
    Mentor -> UI: Accede a panel de contingencia de sesión
    activate UI
    alt Mentor selecciona "Dictar de Todas Formas"
        Mentor -> UI: Clic "Dictar de Todas Formas"
        UI -> Client: submitQuorumDecision(idSesion, 'PROCEED')
        activate Client
        Client -> API: POST /api/v1/offers/{idSesion}/quorum-decision {"decision": 'PROCEED'}
        API -> Service: process_quorum_decision(idSesion, 'PROCEED')
        Service -> DB: UPDATE sesiones_mentoria SET estado = 'CONFIRMADA'
        activate DB
        Service -> DB: COMMIT
        DB --> Service: Sesión confirmada
        deactivate DB
        Service -> Mail: Confirma dictado a los inscritos
        activate Mail
        Mail --> Service: Mail OK
        deactivate Mail
        Service --> API: QuorumDecisionResponseDTO
        API --> Client: HTTP 200 OK
        Client --> UI: Dictado confirmado
        UI --> Mentor: Notificación de éxito
    else Mentor selecciona "Reprogramar Sesión"
        Mentor -> UI: Clic "Reprogramar Sesión" con nueva fecha (> 24h)
        UI -> Client: submitQuorumDecision(idSesion, 'RESCHEDULE', new_start)
        Client -> API: POST /api/v1/offers/{idSesion}/quorum-decision {"decision": 'RESCHEDULE', ...}
        API -> Service: process_quorum_decision(idSesion, 'RESCHEDULE', new_start)
        Service -> DB: UPDATE sesiones_mentoria SET estado = 'PUBLICADA', fecha_inicio = :new_start
        activate DB
        Service -> DB: COMMIT
        DB --> Service: Reprogramada
        deactivate DB
        Service -> Mail: Notifica reprogramación a los inscritos
        activate Mail
        Mail --> Service: Mail OK
        deactivate Mail
        Service --> API: QuorumDecisionResponseDTO
        API --> Client: HTTP 200 OK
        Client --> UI: Reprogramación confirmada
        UI --> Mentor: Sesión reprogramada
    else Mentor selecciona "Cancelar Sesión"
        Mentor -> UI: Clic "Cancelar sin Penalización" con justificativo
        UI -> Client: submitQuorumDecision(idSesion, 'CANCEL', reason)
        Client -> API: POST /api/v1/offers/{idSesion}/quorum-decision {"decision": 'CANCEL', ...}
        API -> Service: process_quorum_decision(idSesion, 'CANCEL', reason)
        Service -> DB: UPDATE sesiones_mentoria SET estado = 'CANCELADA_QUORUM'
        activate DB
        Service -> DB: UPDATE reservas_cupo SET estado = 'CANCELADA_SISTEMA' WHERE id_sesion = :idSesion
        Service -> DB: COMMIT
        DB --> Service: Cancelada
        deactivate DB
        Service -> Mail: Informa anulación solidaria a confirmados
        activate Mail
        Mail --> Service: Mail OK
        deactivate Mail
        Service --> API: QuorumDecisionResponseDTO
        API --> Client: HTTP 200 OK
        Client --> UI: Cancelación confirmada
        UI --> Mentor: Cancelación registrada
    end
    deactivate Client
    deactivate UI
end
deactivate Service
deactivate API
@enduml
```

Fuente: Elaboración propia a partir del diseño de MOD-05.


---

### MOD-01: Seguridad, Autenticación y Gobernanza

#### Diagrama 6.15.1: Diagrama de Secuencia - CUS-001: Iniciar sesión institucional con 2FA

El diagrama de secuencia para `CUS-001` formaliza la interacción temporal y el intercambio de mensajes entre el usuario universitario, la interfaz de autenticación React, el adaptador de cliente, los controladores FastAPI, el servicio de seguridad y correo institucional, y la base de datos relacional. Modela con precisión exhaustiva las tres fases del Flujo Normal (solicitud de OTP, verificación de código temporal, y formalización de consentimiento bajo la Ley N° 29733 con emisión de JWT de 8 horas), los dos flujos alternativos (consentimiento previo `A001` y reenvío de OTP `A002`) y los seis flujos de excepción (`E001` a `E006`).

```plantuml
@startuml
title Diagrama 6.15.1: Diagrama de Secuencia - CUS-001: Iniciar sesión institucional con 2FA y formalización de consentimiento digital
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Usuario Institucional
(Estudiante / Mentor / Administrador)" as User
participant "Vista React
(LoginOtpView.tsx / ConsentModalView.tsx)" as UI
participant "Adaptador Cliente
(authService.ts / consentService.ts)" as Client
participant "Controlador FastAPI
(endpoints/auth.py / consent.py)" as API
participant "Servicio Backend
(auth_service.py / consent_service.py)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB
participant "Servicio SMTP UPT
(EmailService)" as SMTP

== Fase 1: Validación de identidad institucional y solicitud de OTP ==
User -> UI: 1. Ingresa correo institucional (@upt.pe) y pulsa "Continuar"
activate UI
UI -> Client: requestOtp(email)
activate Client
Client -> API: POST /api/v1/auth/request-otp {"email": email}
activate API

API -> API: Valida sintaxis con Pydantic (EmailStr) y comprueba email.endswith("@upt.pe")

alt [E001] Dominio de correo no termina en @upt.pe
    API --> Client: HTTP 400 Bad Request {"detail": "INVALID_DOMAIN: El acceso está reservado a @upt.pe."}
    Client --> UI: Captura error 400 (INVALID_DOMAIN)
    UI --> User: Despliega etiqueta roja "Acceso denegado: Ingrese correo @upt.pe" y botón [Corregir Correo]
    User -> UI: Clic en [Corregir Correo]
    UI --> User: Limpia cuadro de texto, asigna foco y retorna al paso 1
else Dominio universitario válido
    API -> Service: request_otp(email)
    activate Service
    Service -> DB: SELECT * FROM usuarios WHERE email = :email AND activo = true
    activate DB
    DB --> Service: Registro de usuario (activo)
    deactivate DB
    
    alt [E002] Cuenta institucional inactiva o suspendida (activo = false)
        Service --> API: Lanza HTTPException(403, "ACCOUNT_SUSPENDED")
        API --> Client: HTTP 403 Forbidden {"detail": "ACCOUNT_SUSPENDED: Su cuenta registra suspensión administrativa."}
        Client --> UI: Captura error 403 (ACCOUNT_SUSPENDED)
        UI --> User: Muestra modal rojo con aviso de inhabilitación y botón [Aceptar]
        User -> UI: Clic en [Aceptar]
        UI --> User: Cierra modal, restablece formulario y finaliza interacción
    else Cuenta activa y habilitada
        Service --> API: Correo verificado y habilitado
        API --> Client: HTTP 200 OK {"status": "ELIGIBLE"}
        Client --> UI: Habilita botón de emisión de código
        UI --> User: 2. Habilita botón "Solicitar Código de Acceso"
    end
    deactivate Service
end
deactivate API
deactivate Client
deactivate UI

== Fase 2: Generación criptográfica, despacho SMTP y verificación de código temporal ==
User -> UI: 3. Revisa correo verificado y presiona "Solicitar Código de Acceso"
activate UI
UI -> Client: requestOtp(email)
activate Client
Client -> API: POST /api/v1/auth/request-otp {"email": email}
activate API
API -> Service: generate_and_dispatch_otp(email)
activate Service

Service -> Service: Genera código seguro (secrets.randbelow(900000) + 100000)
Service -> Service: Calcula hash criptográfico SHA-256(otp_code)
Service -> DB: INSERT INTO credenciales_otp (id_usuario, hash_otp, expira_en=NOW()+5m)
activate DB
DB --> Service: Confirmación de persistencia
deactivate DB

Service -> SMTP: send_otp_email(email, otp_plano)
activate SMTP
SMTP --> Service: Despacho SMTP exitoso (HTTP 200 / SMTP OK)
deactivate SMTP

Service --> API: OTP_SENT exitoso
deactivate Service
API --> Client: HTTP 200 OK {"message": "OTP_SENT", "expires_in": 300}
deactivate API
Client --> UI: Notificación de despacho exitoso
deactivate Client
UI --> User: 4. Despliega modal con 6 casillas numéricas, inicia temporizador regresivo de 300s
deactivate UI

opt [A002] Reenvío de código temporal por retraso en buzón (> 60s) o caducidad
    User -> UI: A002-1.1 Clic en "Reenviar código OTP" (tras 60 segundos)
    UI -> Client: requestOtp(email)
    activate Client
    Client -> API: POST /api/v1/auth/request-otp {"email": email}
    activate API
    API -> Service: request_otp(email)
    activate Service
    Service -> DB: UPDATE credenciales_otp SET consumido = true WHERE id_usuario = :uid
    activate DB
    DB --> Service: OK
    deactivate DB
    Service -> Service: Genera nueva clave aleatoria de 6 dígitos
    Service -> SMTP: send_otp_email(email, nuevo_otp)
    activate SMTP
    SMTP --> Service: SMTP OK
    deactivate SMTP
    Service --> API: OTP_SENT
    deactivate Service
    API --> Client: HTTP 200 OK
    deactivate API
    Client --> UI: Confirmación de reenvío
    deactivate Client
    UI --> User: A002-1.3 Reinicia temporizador a 300s y alerta ámbar "Nuevo código remitido" (retorna al paso 4)
end

User -> UI: 5. Copia código de 6 dígitos de su buzón y hace clic en "Verificar e Ingresar"
activate UI
UI -> Client: verifyOtp(email, code)
activate Client
Client -> API: POST /api/v1/auth/verify-otp {"email": email, "otp_code": code}
activate API
API -> Service: verify_otp(email, code)
activate Service

Service -> DB: SELECT * FROM credenciales_otp WHERE email = :email AND consumido = false
activate DB
DB --> Service: Registro OTP persistido
deactivate DB

alt [E003] Código temporal OTP incorrecto
    Service -> DB: UPDATE credenciales_otp SET intentos_fallidos = intentos_fallidos + 1
    activate DB
    DB --> Service: Actualizado
    deactivate DB
    Service --> API: Lanza HTTPException(400, "INVALID_OTP")
    API --> Client: HTTP 400 Bad Request {"detail": "INVALID_OTP: El código no coincide."}
    Client --> UI: Captura error 400
    UI --> User: Alerta roja "Código erróneo. Le quedan X intentos" y botón [Reintentar]
    User -> UI: Clic en [Reintentar]
    UI --> User: Limpia casillas numéricas, enfoca primera casilla y retorna al paso 5
else [E004] Código temporal OTP expirado (NOW() > expira_en)
    Service --> API: Lanza HTTPException(400, "EXPIRED_OTP")
    API --> Client: HTTP 400 Bad Request {"detail": "EXPIRED_OTP: El código ha caducado por límite de 5 min."}
    Client --> UI: Captura error 400
    UI --> User: Alerta ámbar "Código caducado" y botón [Solicitar Nuevo Código]
    User -> UI: Clic en [Solicitar Nuevo Código]
    UI --> User: Restablece casillas, reinicia temporizador y retorna al paso 3
else [E005] Bloqueo temporal por exceso de intentos (intentos_fallidos >= 3)
    Service -> DB: UPDATE usuarios SET bloqueado_hasta = NOW() + INTERVAL '15 MINUTES'
    activate DB
    DB --> Service: Usuario bloqueado
    deactivate DB
    Service --> API: Lanza HTTPException(429, "MAX_ATTEMPTS_EXCEEDED")
    API --> Client: HTTP 429 Too Many Requests {"detail": "MAX_ATTEMPTS_EXCEEDED: Acceso bloqueado por 15 minutos."}
    Client --> UI: Captura error 429
    UI --> User: Bloquea casillas, despliega panel rojo de seguridad y botón [Volver al Inicio]
    User -> UI: Clic en [Volver al Inicio]
    UI --> User: Redirige a vista inicial, restablece formulario y retorna al paso 1
else Código válido y vigente
    Service -> DB: UPDATE credenciales_otp SET consumido = true WHERE id = :id_otp
    activate DB
    DB --> Service: Desafío invalidado
    deactivate DB
    Service --> API: OTP validado exitosamente {"temp_token": temp_token}
    API --> Client: HTTP 200 OK {"temp_token": temp_token}
    Client --> UI: Validación exitosa
    UI --> User: 6. Avanza a comprobación de consentimiento legal
end
deactivate Service
deactivate API
deactivate Client
deactivate UI

== Fase 3: Formalización de consentimiento legal digital y emisión de sesión ==
User -> UI: Solicitud de verificación de consentimiento
activate UI
UI -> Client: getConsentStatus(email)
activate Client
Client -> API: GET /api/v1/consent/status?email={email}
activate API
API -> Service: get_consent_status(email)
activate Service
Service -> DB: SELECT * FROM consentimientos_legales WHERE email = :email AND revocado = false
activate DB
DB --> Service: Registro de consentimiento
deactivate DB

alt [A001] Acceso recurrente con consentimiento formalizado previo (has_consented = true)
    Service -> Service: create_access_token(sub=email, roles=[UserRole], exp=8h)
    Service --> API: TokenJWT_Firmado + Perfil
    API --> Client: HTTP 200 OK {"access_token": token, "token_type": "Bearer", "user": user}
    Client --> UI: Entrega token JWT de sesión
    UI -> UI: localStorage.setItem('auth_token', token)
    UI --> User: A001-1.3 Visualiza carga circular, omite modal de consentimiento y entra al Dashboard (paso 8)
else Primer acceso sin consentimiento legal formalizado
    Service --> API: Requiere consentimiento {"requires_consent": true, "temp_token": temp_token}
    API --> Client: HTTP 200 OK {"requires_consent": true}
    Client --> UI: Señaliza requerimiento de consentimiento
    UI --> User: 7. Renderiza ConsentModalView.tsx con términos bajo Ley N° 29733
    
    alt [E006] Rechazo voluntario del consentimiento informado
        User -> UI: Desmarca casilla o presiona botón "Declinar y Salir"
        UI --> User: Modal ámbar advierte que consentimiento es indispensable, botones [Confirmar Salida] y [Revisar Términos]
        User -> UI: Clic en [Confirmar Salida]
        UI --> User: Destruye sesión provisional, purga formulario y retorna al paso 1
    else Aceptación de términos legales
        User -> UI: Marca casilla "He leído y acepto los términos..." y presiona "Aceptar y Continuar"
        UI -> Client: acceptConsent(user_id, version="2026-II-v1.0")
        activate Client
        Client -> API: POST /api/v1/consent/accept {"version": "2026-II-v1.0"}
        activate API
        API -> Service: register_consent(email, ip, user_agent)
        activate Service
        Service -> DB: INSERT INTO consentimientos_legales (usuario_id, ip, user_agent, version, fecha_registro) VALUES (...)
        activate DB
        DB --> Service: Registro inmutable persistido
        deactivate DB
        
        Service -> Service: create_access_token(sub=email, roles=[UserRole], exp=8h)
        Service --> API: TokenJWT_Firmado + Perfil
        deactivate Service
        API --> Client: HTTP 200 OK {"access_token": token, "token_type": "Bearer", "user": user}
        deactivate API
        Client --> UI: Persistencia exitosa
        deactivate Client
        
        UI -> UI: localStorage.setItem('auth_token', token)
        UI -> UI: Actualiza estado global de autenticación en App.tsx
        UI --> User: 8. Redirige a Dashboard según rol con notificación verde flotante: "¡Sesión institucional iniciada exitosamente!"
    end
end
deactivate Service
deactivate API
deactivate Client
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-001.

---

#### Diagrama 6.15.2: Diagrama de Secuencia - CUS-010: Gestionar asignación de roles de usuario

El diagrama de secuencia para `CUS-010` modela la gestión y administración de roles de usuario por parte de la Dirección de Escuela y administradores institucionales. Desglosa los participantes en capas: Autoridad Administradora, `AdminDashboardView.tsx`, `roleService.ts`, `roles.py`, `role_service.py` y PostgreSQL. Abarca la consulta de nómina paginada, la búsqueda de usuarios (con flujo alternativo `A001`), la verificación de autorización RBAC (`E001`), la tolerancia a fallos de persistencia (`E002`), la prohibición de conjuntos de roles vacíos (`E003`) y la protección de gobernanza contra auto-revocación del rol Administrador (`E004`).

```plantuml
@startuml
title Diagrama 6.15.2: Diagrama de Secuencia - CUS-010: Gestionar asignación y revocación de roles institucionales de usuario
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Autoridad Institucional
(Administrador / Director EPIS)" as Admin
participant "Vista React
(AdminDashboardView.tsx)" as UI
participant "Adaptador Cliente
(roleService.ts / ApiRoleAdapter)" as Client
participant "Controlador FastAPI
(endpoints/roles.py)" as API
participant "Servicio Backend
(role_service.py / RoleService)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Acceso al panel administrativo y consulta de nómina de usuarios ==
Admin -> UI: 1. Accede al panel de control y hace clic en "Gestión de Roles"
activate UI
UI -> Client: listUsers() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/roles/users
activate API

API -> API: require_admin_role(current_user): valida JWT y claim roles conteniendo 'administrador'

alt [E001] Privilegios administrativos insuficientes (rol no administrador)
    API --> Client: HTTP 403 Forbidden {"detail": "FORBIDDEN: Se requieren privilegios de Administrador."}
    Client --> UI: Captura error 403 (FORBIDDEN)
    UI --> Admin: Redirige a vista permitida, despliega aviso rojo "Acceso Restringido" y botón [Entendido]
    Admin -> UI: Clic en [Entendido]
    UI --> Admin: Cierra aviso y retorna al paso 1 en su vista autorizada
else [E002] Error de conexión o timeout en base de datos
    API -> Service: list_users()
    activate Service
    Service -> DB: SELECT u.id, u.email, array_agg(r.nombre) FROM usuarios u...
    activate DB
    DB --> Service: Timeout / Conexión rechazada
    deactivate DB
    Service --> API: Lanza OperationalError
    deactivate Service
    API --> Client: HTTP 503 Service Unavailable {"detail": "SERVICE_UNAVAILABLE: No se pudo conectar a BD."}
    Client --> UI: Captura error 503
    UI --> Admin: Panel ámbar "Servicio no disponible" y botón [Reintentar Carga]
    Admin -> UI: Clic en [Reintentar Carga]
    UI -> Client: listUsers() (retorna al paso 1)
else Token válido y conexión activa
    API -> Service: list_users()
    activate Service
    Service -> DB: SELECT u.id, u.email, u.nombres, u.apellidos, array_agg(r.nombre) AS roles
FROM usuarios u LEFT JOIN roles_usuarios ru ON u.id = ru.id_usuario
LEFT JOIN roles r ON ru.id_rol = r.id GROUP BY u.id
    activate DB
    DB --> Service: Nómina de usuarios con roles asignados
    deactivate DB
    Service --> API: UserRoleListResponseDTO
    deactivate Service
    API --> Client: HTTP 200 OK UserRoleListResponseDTO
    Client --> UI: Nómina de usuarios deserializada
    UI --> Admin: 2. Renderiza tabla interactiva de usuarios con filtros y botones de acción
end
deactivate API
deactivate Client
deactivate UI

== Fase 2: Búsqueda y selección de usuario para modificación ==
Admin -> UI: 3. Ingresa código o correo en "Buscar usuario" y pulsa "Buscar"
activate UI
UI -> Client: searchUsers(query)
activate Client
Client -> API: GET /api/v1/roles/users?query={query}
activate API
API -> Service: search_users(query)
activate Service
Service -> DB: SELECT u.* FROM usuarios u WHERE email ILIKE :q OR codigo ILIKE :q
activate DB
DB --> Service: Resultados coincidentes
deactivate DB
Service --> API: Nómina filtrada
deactivate Service
API --> Client: HTTP 200 OK
deactivate API
Client --> UI: Entrega resultados de búsqueda
deactivate Client

alt [A001] Búsqueda sin coincidencias en el padrón institucional
    UI --> Admin: A001-1.2 Panel informativo "No se encontraron usuarios coincidentes" y botón [Limpiar Búsqueda]
    Admin -> UI: Clic en [Limpiar Búsqueda]
    UI --> Admin: A001-1.4 Restablece buscador, recarga nómina completa y retorna al paso 3
else Usuario localizado
    UI --> Admin: 4. Resalta fila del usuario localizado
    Admin -> UI: Clic en botón "Modificar Roles"
    UI --> Admin: Despliega modal "Asignación de Roles" con checkboxes (Mentoreado, Mentor, Administrador, Coordinador)
end
deactivate UI

== Fase 3: Modificación atómica de roles y registro de auditoría ==
Admin -> UI: 5. Marca o desmarca casillas (ej. asigna 'Mentor') y pulsa "Guardar Asignación"
activate UI
UI -> Client: assignRoles(target_user_id, selected_roles)
activate Client
Client -> API: POST /api/v1/roles/assign {"user_id": target_id, "roles": selected_roles}
activate API

API -> Service: assign_roles(admin_id, target_user_id, selected_roles)
activate Service

alt [E003] Intento de dejar al usuario sin ningún rol asignado (len(selected_roles) == 0)
    Service --> API: Lanza HTTPException(400, "EMPTY_ROLE_SET_PROHIBITED")
    API --> Client: HTTP 400 Bad Request {"detail": "EMPTY_ROLE_SET_PROHIBITED: Todo usuario debe tener al menos un rol."}
    Client --> UI: Captura error 400
    UI --> Admin: Error rojo dentro del modal indicando obligatoriedad de rol, mantiene modal abierto
    Admin -> UI: Marca al menos una casilla de rol válida
    UI --> Admin: Rehabilita botón "Guardar Asignación" y retorna al paso 5
else [E004] Intento de auto-revocación del rol Administrador (target_id == current_user_id)
    Service --> API: Lanza HTTPException(400, "CANNOT_REVOKE_OWN_ADMIN")
    API --> Client: HTTP 400 Bad Request {"detail": "CANNOT_REVOKE_OWN_ADMIN: No puede auto-revocarse el rol Administrador."}
    Client --> UI: Captura error 400
    UI --> Admin: Alerta roja destacada en el modal y botón [Restablecer Selección]
    Admin -> UI: Clic en [Restablecer Selección]
    UI --> Admin: Vuelve a marcar casilla de Administrador y retorna al paso 5
else Asignación válida y conforme a RBAC
    Service -> DB: BEGIN TRANSACTION
    activate DB
    Service -> DB: DELETE FROM roles_usuarios WHERE id_usuario = :target_id
    Service -> DB: INSERT INTO roles_usuarios (id_usuario, id_rol) VALUES (:target_id, :rol_id)...
    Service -> DB: INSERT INTO auditoria_admin (admin_id, target_user_id, accion='ROLE_CHANGE', ip, fecha) VALUES (...)
    Service -> DB: COMMIT
    DB --> Service: Transacción ACID confirmada exitosamente
    deactivate DB
    
    Service --> API: RoleAssignResponseDTO {"success": true, "updated_roles": selected_roles}
    API --> Client: HTTP 200 OK RoleAssignResponseDTO
    Client --> UI: Notificación de actualización confirmada
    
    UI -> UI: Actualiza reactivamente la tabla de usuarios en memoria
    UI -> UI: Cierra cuadro de diálogo modal
    UI --> Admin: 6. Notificación flotante verde de éxito: "Roles actualizados exitosamente para el usuario"
end
deactivate Service
deactivate API
deactivate Client
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-010.


---

### MOD-02: Ofertas de Mentoría y Espacios

#### Diagrama 6.15.3: Diagrama de Secuencia - CUS-006: Publicar oferta de mentoría académica

El diagrama de secuencia para `CUS-006` formaliza la programación y publicación de sesiones de mentoría académica por parte de un mentor acreditado. Modela la interacción entre el Estudiante Mentor, la interfaz React (`OfferPublishView.tsx`), los clientes HTTP (`offerService.ts` / `apiClient.ts`), los endpoints FastAPI (`endpoints/curriculum.py` y `endpoints/offers.py`), los servicios de lógica de negocio (`CurriculumService` y `OfferService`) y PostgreSQL. Abarca la recuperación de temas curriculares silábicos, la verificación criptográfica del token JWT (`RN-01`, `E005`), la validación de mérito académico y rol habilitado (`RN-03`, `E004`), la comprobación de antelación mínima de 24 horas (`RN-04`, `E002`), el aforo reglamentario (exactamente 10 presencial o 20 virtual, `RN-05`, `E003`) y la creación transaccional atómica de la entidad `SesionMentoria` en estado `PUBLICADA`.

```plantuml
@startuml
title Diagrama 6.15.3: Diagrama de Secuencia - CUS-006: Publicar oferta de mentoría académica
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor
(UserRole.mentor)" as Mentor
participant "Vista React
(OfferPublishView.tsx)" as UI
participant "Adaptador Cliente
(offerService.ts / apiClient.ts)" as Client
participant "Controlador FastAPI
(endpoints/offers.py)" as API
participant "Servicio Backend
(offer_service.py / OfferService)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Configuración de la sesión y selección curricular ==
Mentor -> UI: 1. Accede a vista de publicación y selecciona asignatura curricular en "Curso"
activate UI
UI -> Client: fetchCourseDetail(selectedCourseId)
activate Client
Client -> API: GET /api/v1/curriculum/courses/{id}
activate API
API -> Service: get_course_by_id(id)
activate Service
Service -> DB: SELECT * FROM asignaturas WHERE id_asignatura = :id
SELECT * FROM temas_curriculares WHERE id_asignatura = :id
activate DB
DB --> Service: Asignatura y lista de temas silábicos (Topic[])
deactivate DB
Service --> API: CourseDetailResponse
deactivate Service
API --> Client: HTTP 200 OK CourseDetailResponse
deactivate API
Client --> UI: Entrega temas curriculares
deactivate Client
UI --> Mentor: 2. Renderiza temas silábicos, campos de fecha, hora, duración (60|90 min), modalidad y cupos reglamentarios
deactivate UI

== Fase 2: Ingreso de parámetros, validación de reglas de aforo y antelación ==
Mentor -> UI: 3. Selecciona tema, fecha/hora, modalidad, ingresa cupos y pulsa "Verificar y Publicar"
activate UI
UI -> UI: validateOfferPayload(payload) en cliente

alt [E001] Campos obligatorios incompletos o sintaxis inválida
    UI --> Mentor: Resalta campos observados con borde rojo y texto explicativo
    Mentor -> UI: Corrige campos completando los datos requeridos
    UI --> Mentor: Rehabilita botón "Verificar y Publicar" y retorna al paso 3
else Formulario válido en cliente
    UI -> Client: publishOffer(payload: PublishOfferPayload)
    activate Client
    Client -> API: POST /api/v1/offers PublishOfferPayload [Bearer JWT]
    activate API
    API -> API: _extract_caller_and_admin_status(authorization, payload.mentor_email)

    alt [E005] Discrepancia de identidad o suplantación de mentor
        API --> Client: HTTP 403 Forbidden {"detail": "No tiene autorización para publicar ofertas en nombre de otro usuario."}
        Client --> UI: Captura error 403
        UI --> Mentor: Alerta roja de seguridad institucional y retorna al paso 3
    else Identidad de mentor verificada
        API -> Service: publish_offer(db, payload, caller_email, is_admin)
        activate Service

        Service -> Service: validate_mentor_eligibility(db, effective_email)
        Service -> DB: SELECT * FROM usuario_roles ur JOIN roles r ON ur.id_rol = r.id_rol
WHERE ur.email = :email AND ur.activo = true AND r.nombre_rol IN ('mentor', 'administrador')
        activate DB
        DB --> Service: Roles del usuario y perfil académico (ciclo_actual)
        deactivate DB

        alt [E004] Mentor no elegible por ciclo insuficiente o falta de rol (RN-03)
            Service --> API: Lanza HTTPException(403, "Infracción de RN-03: Solo los estudiantes habilitados con rol de mentor (ciclo >= VII)...")
            API --> Client: HTTP 403 Forbidden {"detail": "Infracción de RN-03: Solo los estudiantes habilitados..."}
            Client --> UI: Captura error 403
            UI --> Mentor: Banner rojo informando falta de acreditación académica y retorna al paso 3
        else Mentor acreditado (ciclo >= VII)
            Service -> Service: calculate_advance_hours(payload.fecha_inicio)

            alt [E002] Incumplimiento de antelación mínima de 24 horas (fecha_inicio <= now_utc + 24h)
                Service --> API: Lanza HTTPException(400, "Infracción de RN-04: Toda mentoría debe publicarse con una antelación superior a 24 horas...")
                API --> Client: HTTP 400 Bad Request {"detail": "Infracción de RN-04: Toda mentoría debe publicarse..."}
                Client --> UI: Captura error 400
                UI --> Mentor: Panel rojo "Antelación mínima requerida: 24 horas" y botón [Ajustar Fecha]
                Mentor -> UI: Clic en [Ajustar Fecha], selecciona nueva fecha > 24h
                UI --> Mentor: Retorna al paso 3
            else [E003] Aforo no conforme con la modalidad (aforo != 10 presencial o != 20 virtual)
                Service --> API: Lanza HTTPException(400, "Infracción de RN-05: El aforo reglamentario...")
                API --> Client: HTTP 400 Bad Request {"detail": "Infracción de RN-05: El aforo reglamentario..."}
                Client --> UI: Captura error 400
                UI --> Mentor: Mensaje rojo "Aforo supera límite reglamentario", ajusta vacantes y retorna al paso 3
            else Parámetros de mérito, aforo y antelación válidos
                == Fase 3: Persistencia transaccional de la oferta y confirmación en cliente ==
                Mentor -> UI: 5. Visualiza indicador circular de procesamiento en botón
                
                Service -> DB: sesion_db = SesionMentoria(codigo_sesion=code, mentor_email=..., estado='PUBLICADA', ...)
                Service -> DB: db.add(sesion_db)
db.commit()
db.refresh(sesion_db)
                activate DB
                DB --> Service: Transacción confirmada (id_sesion, codigo_sesion='SES-XXXX')
                deactivate DB
                
                Service --> API: PublishOfferResponse (id_oferta=..., codigo_sesion='SES-XXXX', estado='PUBLICADA')
                API --> Client: HTTP 201 Created PublishOfferResponse
                Client --> UI: Entrega confirmación de publicación
                
                UI -> UI: setPublishedSuccess(response) y onOfferPublished(response)
                UI --> Mentor: 6. Despliega tarjeta verde con código de sesión generado y botón "Ver en Mis Sesiones"
            end
        end
        deactivate Service
    end
    deactivate API
    deactivate Client
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-006.

#### Diagrama 6.15.4: Diagrama de Secuencia - CUS-008: Consultar disponibilidad de espacios y recursos

El diagrama de secuencia para `CUS-008` modela la consulta de disponibilidad de infraestructura física de la EPIS (aulas, laboratorios y salas de estudio) antes de programar sesiones presenciales. Detalla la interacción entre el Mentor, la interfaz de usuario, `offerService.ts`, el endpoint `GET /api/v1/offers/spaces/availability`, `offer_service.py` y las tablas `aulas` y `sesiones_mentoria`. Incorpora la restricción de horario universitario de 08:00 a 20:00 (`RN-07`, `E001`), la tolerancia a fallos de persistencia (`E002`) y la conmutación guiada hacia modalidad virtual (`A001`) ante saturación de espacios físicos.

```plantuml
@startuml
title Diagrama 6.15.4: Diagrama de Secuencia - CUS-008: Consultar disponibilidad de espacios físicos y aulas de la EPIS
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor
(UserRole.mentor)" as Mentor
participant "Vista React
(OfferPublishView.tsx / SpacesModal)" as UI
participant "Adaptador Cliente
(offerService.ts)" as Client
participant "Controlador FastAPI
(endpoints/offers.py)" as API
participant "Servicio Backend
(offer_service.py)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Definición de criterios temporales y despacho de consulta ==
Mentor -> UI: 1. Selecciona fecha y franja horaria (inicio y fin) y pulsa "Consultar Aulas Disponibles"
activate UI
UI -> Client: checkSpaceAvailability(date, startTime, endTime)
activate Client

Client -> API: GET /api/v1/offers/spaces/availability?date={date}&start_time={start_time}&end_time={end_time} [Bearer JWT]
activate API
API -> Service: check_space_availability(date, start_time, end_time)
activate Service

alt [E001] Horario fuera de la jornada institucional (fuera del intervalo 08:00 - 20:00, RN-07)
    Service --> API: Lanza HTTPException(400, "OPERATIONAL_HOURS_VIOLATION")
    API --> Client: HTTP 400 Bad Request {"detail": "OPERATIONAL_HOURS_VIOLATION: Operación sólo entre 08:00 y 20:00 horas."}
    Client --> UI: Captura error 400
    UI --> Mentor: Advertencia roja "Uso de aulas no autorizado fuera de la jornada reglamentaria"
    Mentor -> UI: Modifica franja horaria seleccionando horario entre 08:00 y 20:00
    UI --> Mentor: Actualiza selector y retorna al paso 1
else Rango horario reglamentario válido
    == Fase 2: Verificación de ocupación en base de datos y renderización de resultados ==
    Mentor -> UI: 3. Visualiza indicador circular de carga en color azul institucional
    
    alt [E002] Falla de conexión o timeout con repositorio de infraestructura
        Service -> DB: Conexión y consulta de aulas (timeout)
        activate DB
        DB --> Service: Timeout de conexión en PostgreSQL
        deactivate DB
        Service --> API: Lanza OperationalError
        API --> Client: HTTP 503 Service Unavailable {"detail": "INFRASTRUCTURE_UNAVAILABLE: No se pudo verificar disponibilidad."}
        Client --> UI: Captura error 503
        UI --> Mentor: Alerta roja "Indisponibilidad temporal del servicio" y botón [Reintentar Consulta]
        Mentor -> UI: Clic en [Reintentar Consulta]
        UI -> Client: checkSpaceAvailability(...) (retorna al paso 1)
    else Conexión exitosa y consulta ejecutada
        Service -> DB: SELECT a.id, a.codigo, a.capacidad, a.equipamiento FROM aulas a
WHERE a.activa = true AND a.id NOT IN (
  SELECT aula_id FROM sesiones_mentoria
  WHERE fecha = :fecha AND NOT (hora_fin <= :start OR hora_inicio >= :end)
  AND estado IN ('PUBLICADA', 'CONFIRMADA')
)
        activate DB
        DB --> Service: Lista de aulas disponibles
        deactivate DB
        Service --> API: AvailableSpacesResponseDTO
        API --> Client: HTTP 200 OK AvailableSpacesResponseDTO
        Client --> UI: Entrega catálogo de espacios libres
        
        alt [A001] Aulas físicas agotadas (cero registros libres)
            UI --> Mentor: A001-1.2 Panel ámbar "Todas las aulas físicas ocupadas" y botones [Cambiar a Virtual] / [Modificar Horario]
            Mentor -> UI: A001-1.3 Clic en [Cambiar a Modalidad Virtual]
            UI -> UI: Conmuta modalidad a VIRTUAL, habilita Google Meet y ajusta aforo a 20 (RN-05)
            UI --> Mentor: A001-1.4 Retorna al paso 1 del Flujo Normal
        else Aulas físicas disponibles
            UI --> Mentor: 4. Renderiza cuadrícula interactiva de aulas libres con capacidad y equipamiento
            Mentor -> UI: 5. Selecciona aula física deseada y pulsa "Asignar Aula a la Oferta"
            UI -> UI: Asigna aula_id al formulario de publicación
            UI --> Mentor: 6. Actualiza etiqueta verde con "Aula reservada provisionalmente" y habilita avance
        end
    end
end
deactivate Service
deactivate API
deactivate Client
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-008.


---

### MOD-03: Perfil del Mentor y Plan de Aprendizaje

#### Diagrama 6.15.5: Diagrama de Secuencia - CUS-005: Gestionar perfil académico y disponibilidad horaria

El diagrama de secuencia para `CUS-005` modela la configuración integral del perfil formativo del estudiante mentor y la administración atómica de su matriz semanal de disponibilidad horaria (lunes a sábado, 08:00 a 20:00). Desglosa las interacciones entre el Estudiante Mentor, `ProfileAvailabilityView.tsx`, `profileService.ts`, `profiles.py`, `profile_service.py` y PostgreSQL. Modela la consulta inicial de perfil, la validación sintáctica de biografía y bloques, el reemplazo atómico transaccional (`DELETE` + `INSERT` en bloque bajo `db.begin()`), y los flujos de excepción por matriz horaria vacía (`E001`), validación de texto (`E002`) y colisión de concurrencia (`E003`).

```plantuml
@startuml
title Diagrama 6.15.5: Diagrama de Secuencia - CUS-005: Gestionar perfil formativo y disponibilidad horaria
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor
(UserRole.mentor)" as Mentor
participant "Vista React
(ProfileAvailabilityView.tsx)" as UI
participant "Adaptador Cliente
(profileService.ts / ApiProfileAdapter)" as Client
participant "Controlador FastAPI
(endpoints/profiles.py)" as API
participant "Servicio Backend
(profile_service.py / ProfileService)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta del perfil académico y visualización de la matriz horaria ==
Mentor -> UI: 1. Clic en pestaña "Mi Perfil y Disponibilidad"
activate UI
UI -> Client: getMyProfile() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/profiles/me
activate API
API -> Service: get_profile(user_id)
activate Service
Service -> DB: SELECT p.*, d.* FROM perfiles_academicos p
LEFT JOIN disponibilidad_horaria d ON p.id = d.perfil_id
WHERE p.usuario_id = :uid
activate DB
DB --> Service: Perfil formativo y franjas horarias existentes
deactivate DB
Service --> API: ProfileResponseDTO
deactivate Service
API --> Client: HTTP 200 OK ProfileResponseDTO
deactivate API
Client --> UI: Entrega perfil y franjas horarias
deactivate Client
UI --> Mentor: 2. Renderiza biografía, materias de dominio y matriz semanal interactiva (lun-sáb 08:00-20:00)
deactivate UI

== Fase 2: Edición de datos formativos y selección de bloques de disponibilidad ==
Mentor -> UI: 3. Actualiza biografía, selecciona materias y conmuta bloques horarios (verde = disponible)
activate UI
UI -> UI: Actualiza estado local availabilitySlots

Mentor -> UI: Presiona botón "Guardar Cambios y Disponibilidad"
UI -> UI: Valida biografía (<= 500 caracteres) y slots seleccionados

alt [E001] Matriz de disponibilidad horaria semanal vacía (cero bloques marcados)
    UI --> Mentor: Cuadrícula con borde rojo, advertencia ámbar "Debe marcar al menos 1 hora"
    Mentor -> UI: Hace clic en al menos un bloque horario en la cuadrícula
    UI --> Mentor: Conmuta bloque a verde, rehabilita botón "Guardar Cambios" y retorna al paso 4
else [E002] Biografía excede 500 caracteres o contiene scripts no autorizados
    UI --> Mentor: Resalta biografía en rojo indicando exceso de caracteres
    Mentor -> UI: Ajusta texto al límite reglamentario (<= 500 caracteres)
    UI --> Mentor: Actualiza contador de caracteres y retorna al paso 4
else Datos válidos en cliente
    == Fase 3: Persistencia transaccional de disponibilidad y perfil ==
    Mentor -> UI: 5. Visualiza indicador circular de guardado en botón
    UI -> Client: updateProfile(payload)
    activate Client
    Client -> API: PUT /api/v1/profiles/me ProfileUpdateRequest [Bearer JWT]
    activate API
    API -> Service: update_profile_and_availability(mentor_id, payload)
    activate Service
    
    Service -> DB: BEGIN TRANSACTION
    activate DB
    Service -> DB: UPDATE perfiles_academicos SET biografia = :bio, materias = :m WHERE usuario_id = :uid
    
    alt [E003] Conflicto de concurrencia al actualizar perfil (versión obsoleta)
        DB --> Service: Concurrency Conflict / Row Version Mismatch
        Service -> DB: ROLLBACK
        Service --> API: Lanza HTTPException(409, "CONCURRENCY_CONFLICT")
        API --> Client: HTTP 409 Conflict {"detail": "CONCURRENCY_CONFLICT: Modificado desde otra sesión."}
        Client --> UI: Captura error 409
        UI --> Mentor: Aviso ámbar "El perfil fue actualizado concurrentemente" y botón [Recargar Perfil]
        Mentor -> UI: Clic en [Recargar Perfil]
        UI -> Client: getMyProfile() (retorna al paso 1)
    else Transacción atómica exitosa
        Service -> DB: DELETE FROM disponibilidad_horaria WHERE perfil_id = :pid
        Service -> DB: INSERT INTO disponibilidad_horaria (perfil_id, dia_semana, hora_inicio, hora_fin) VALUES (:pid, :dia, :hi, :hf)...
        Service -> DB: COMMIT
        DB --> Service: Transacción confirmada exitosamente
        deactivate DB
        
        Service --> API: ProfileResponseDTO {"success": true}
        API --> Client: HTTP 200 OK ProfileResponseDTO
        Client --> UI: Perfil actualizado exitosamente
        
        UI -> UI: Actualiza caché local del perfil
        UI --> Mentor: 6. Alerta flotante verde: "Perfil y disponibilidad horaria actualizados exitosamente"
    end
    deactivate Service
    deactivate API
    deactivate Client
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-005.

---

#### Diagrama 6.15.6: Diagrama de Secuencia - CUS-021: Explorar catálogo curricular de asignaturas filtro

El diagrama de secuencia para `CUS-021` modela la navegación por el catálogo curricular oficial de la EPIS-UPT, estructurado jerárquicamente por ciclo académico (I al X), asignaturas y temas silábicos con identificación destacada de materias filtro (`RN-11`). Modela las interacciones entre los estudiantes (mentoreados y mentores), `CurriculumCatalogView.tsx`, `curriculumService.ts`, `curriculum.py`, `curriculum_service.py` y PostgreSQL. Describe la consulta de cursos con manejo de indisponibilidad (`E001`), el filtrado reactivo de materias con flujo alternativo sin coincidencias (`A001`) y la expansión de temarios con derivación directa hacia la reserva o demanda.

```plantuml
@startuml
title Diagrama 6.15.6: Diagrama de Secuencia - CUS-021: Explorar catálogo curricular de asignaturas filtro
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado / Mentor" as User
participant "Vista React
(CurriculumCatalogView.tsx)" as UI
participant "Adaptador Cliente
(curriculumService.ts / ApiCurriculumAdapter)" as Client
participant "Controlador FastAPI
(endpoints/curriculum.py)" as API
participant "Servicio Backend
(curriculum_service.py / CurriculumService)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Navegación por ciclo académico y selección de asignatura ==
User -> UI: 1. Clic en "Catálogo Curricular" del menú principal
activate UI
UI -> Client: getCourses() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/curriculum/courses
activate API
API -> Service: get_courses()
activate Service

alt [E001] Falla de conexión con el repositorio curricular
    Service -> DB: SELECT c.*, count(t.id) FROM cursos c...
    activate DB
    DB --> Service: Timeout / Conexión rechazada
    deactivate DB
    Service --> API: Lanza OperationalError
    API --> Client: HTTP 503 Service Unavailable {"detail": "CURRICULUM_SERVICE_UNAVAILABLE: Repositorio no disponible."}
    Client --> UI: Captura error 503
    UI --> User: Panel de alerta ámbar indicando imposibilidad de cargar malla y botón [Reintentar Carga]
    User -> UI: Clic en [Reintentar Carga]
    UI -> Client: getCourses() (retorna al paso 1)
else Conexión exitosa y consulta de cursos
    Service -> DB: SELECT c.*, count(t.id) as total_temas FROM cursos c
LEFT JOIN temas_curriculares t ON c.id = t.curso_id
WHERE c.activo = true GROUP BY c.id ORDER BY c.ciclo, c.nombre
    activate DB
    DB --> Service: Listado jerárquico de asignaturas (ciclos I al X)
    deactivate DB
    Service --> API: CourseListResponseDTO
    API --> Client: HTTP 200 OK CourseListResponseDTO
    Client --> UI: Entrega catálogo de asignaturas
    UI --> User: 2. Renderiza cursos agrupados por ciclo, destacando asignaturas filtro con insignia azul "Materia Filtro Prioritaria"
end
deactivate Service
deactivate API
deactivate Client
deactivate UI

== Fase 2: Búsqueda y filtrado interactivo de cursos ==
User -> UI: 3. Introduce nombre o código en "Buscar asignatura o tema" y aplica filtro por ciclo
activate UI
UI -> UI: Filtra reactivamente la lista de cursos en estado cliente

alt [A001] Búsqueda curricular sin coincidencias
    UI --> User: A001-1.2 Oculta tarjetas, renderiza panel informativo "No se encontraron coincidencias" y botón [Restablecer Filtros]
    User -> UI: A001-1.3 Clic en [Restablecer Filtros]
    UI -> UI: A001-1.4 Limpia cuadro de búsqueda y restaura vista completa
    UI --> User: Retorna al paso 3 del Flujo Normal
else Cursos coincidentes localizados
    UI --> User: 4. Despliega tarjetas de asignaturas filtradas
end
deactivate UI

== Fase 3: Despliegue de temarios silábicos y vinculación con mentorías ==
User -> UI: 5. Hace clic sobre la tarjeta de un curso específico (ej. Algoritmos)
activate UI
UI -> Client: getCourseTopics(courseId)
activate Client
Client -> API: GET /api/v1/curriculum/courses/{course_id}/topics
activate API
API -> Service: get_topics(course_id)
activate Service
Service -> DB: SELECT * FROM temas_curriculares WHERE curso_id = :cid ORDER BY unidad, semana
activate DB
DB --> Service: Lista de temas silábicos con ofertas activas asociadas
deactivate DB
Service --> API: TopicListResponseDTO
deactivate Service
API --> Client: HTTP 200 OK TopicListResponseDTO
deactivate API
Client --> UI: Entrega temario silábico
deactivate Client

UI -> UI: Expande panel acordeón de temas curriculares
UI --> User: 6. Muestra lista de temas con botones [Ver Ofertas Disponibles] (CUS-004) y [Solicitar Demanda] (CUS-003)
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-021.


---

### MOD-04: Demanda y Recomendaciones Personalizadas

#### Diagrama 6.15.7: Diagrama de Secuencia - CUS-002: Explorar recomendaciones personalizadas Top-k

El diagrama de secuencia para `CUS-002` formaliza la inferencia algorítmica y la entrega de la cartelera personalizada de sesiones de mentoría Top-k. Modela las llamadas entre el Estudiante Mentoreado, el componente cliente `RecommendationFeedView.tsx`, el adaptador `recommendationService.ts`, el endpoint FastAPI en `recommendations.py`, el motor algorítmico `recommendation_service.py` y las tablas de PostgreSQL. Incorpora el fallback heurístico por popularidad ("Cold Start" `A001`), la contingencia ante cartelera desierta (`A002`), el tratamiento de errores de cómputo (`E001`) y la derivación transaccional hacia la reserva de cupo (`CUS-004`).

```plantuml
@startuml
title Diagrama 6.15.7: Diagrama de Secuencia - CUS-002: Explorar recomendaciones personalizadas Top-k
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado
(UserRole.mentoreado)" as User
participant "Vista React
(RecommendationFeedView.tsx)" as UI
participant "Adaptador Cliente
(recommendationService.ts)" as Client
participant "Controlador FastAPI
(endpoints/recommendations.py)" as API
participant "Servicio Backend
(recommendation_service.py)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB
participant "Modal Reserva
(BookingModalView.tsx)" as BookingModal

== Fase 1: Acceso a la cartelera y solicitud de recomendaciones Top-k ==
User -> UI: 1. Accede a la cartelera principal de recomendaciones
activate UI
UI -> Client: getTopKRecommendations(limit=6) [Bearer JWT]
activate Client
Client -> API: GET /api/v1/recommendations/top-k?limit=6
activate API
API -> Service: get_top_k_recommendations(user_id, limit=6)
activate Service

alt [E001] Error interno de cómputo o timeout en base de datos
    Service --> API: Lanza HTTPException(500, "RECOMMENDER_ENGINE_ERROR")
    API --> Client: HTTP 500 Internal Server Error {"detail": "RECOMMENDER_ENGINE_ERROR"}
    Client --> UI: Captura error 500
    UI --> User: Panel de advertencia rojo "Error al procesar recomendaciones" y botón [Reintentar Cartelera]
    User -> UI: Clic en [Reintentar Cartelera]
    UI -> Client: getTopKRecommendations() (retorna al paso 1)
else Motor operativo
    Service -> DB: SELECT * FROM perfiles_academicos WHERE usuario_id = :uid
    activate DB
    DB --> Service: Perfil del estudiante e historial de asignaturas
    deactivate DB
    
    alt [A001] Estudiante nuevo sin historial académico (Cold Start Fallback)
        Service -> DB: SELECT s.* FROM sesiones_mentoria s
JOIN temas_curriculares t ON s.id_tema = t.id
JOIN cursos c ON t.curso_id = c.id
WHERE c.es_filtro = true AND s.estado = 'PUBLICADA' ORDER BY s.aforo_maximo DESC LIMIT 6
        activate DB
        DB --> Service: Sesiones populares en cursos filtro
        deactivate DB
        Service --> API: FallbackRecommendationDTO (populares)
        API --> Client: HTTP 200 OK FallbackRecommendationDTO
        Client --> UI: Entrega recomendaciones por popularidad
        UI --> User: A001-1.3 Tarjetas con distintivo ámbar "Ofertas destacadas para primeros ciclos" y botón [Configurar Mis Materias] (retorna al paso 4)
    else Perfil con historial académico activo
        == Fase 2: Ejecución del algoritmo de emparejamiento y ordenamiento de compatibilidad ==
        User -> UI: 3. Visualiza esqueleto animado de tarjetas (Skeleton Loading)
        
        Service -> DB: SELECT s.*, t.titulo, c.nombre, c.es_filtro FROM sesiones_mentoria s
JOIN temas_curriculares t ON s.id_tema = t.id
JOIN cursos c ON t.curso_id = c.id
WHERE s.estado = 'PUBLICADA' AND s.fecha_inicio > NOW() + INTERVAL '24 HOURS'
AND s.cupos_ocupados < s.aforo_maximo
        activate DB
        DB --> Service: Candidatas a mentoría activas
        deactivate DB
        
        alt [A002] Cartelera vacía por ausencia de sesiones disponibles (0 ofertas)
            Service --> API: EmptyListDTO []
            API --> Client: HTTP 200 OK []
            Client --> UI: Lista vacía
            UI --> User: A002-1.2 Panel informativo "No hay sesiones programadas para tus materias" y botón [Registrar Demanda]
            User -> UI: A002-1.3 Clic en [Registrar Demanda]
            UI -> UI: A002-1.4 Abre modal de demanda académica (CUS-003) y retorna al paso 1
        else Ofertas disponibles
            Service -> Service: Computa Score = 0.5*Similitud + 0.3*FactorFiltro + 0.2*Urgencia
            Service -> Service: Ordena descendentemente y toma las 6 mejores
            Service --> API: TopKRecommendationResponseDTO
            API --> Client: HTTP 200 OK TopKRecommendationResponseDTO
            Client --> UI: Entrega las 6 recomendaciones personalizadas
            
            UI --> User: 4. Renderiza tarjetas con tema, curso, horario, modalidad, cupos y badge azul "X% de afinidad"
            
            == Fase 3: Selección de sesión para reserva de cupo ==
            User -> UI: 5. Revisa tarjetas y hace clic en "Reservar Cupo" en una sesión
            UI -> BookingModal: 6. Abre diálogo modal pasando offer_id y user_id
            activate BookingModal
            BookingModal --> User: Despliega BookingModalView.tsx transfiriendo el flujo a la especificación CUS-004
            deactivate BookingModal
        end
    end
end
deactivate Service
deactivate API
deactivate Client
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-002.

---

#### Diagrama 6.15.8: Diagrama de Secuencia - CUS-003: Registrar solicitud de demanda académica

El diagrama de secuencia para `CUS-003` describe el registro de necesidades pedagógicas no atendidas por parte de los estudiantes mentoreados. Modela la interacción temporal entre el Estudiante Mentoreado, el modal de demanda en `RecommendationFeedView.tsx`, `recommendationService.ts`, el endpoint `POST /api/v1/recommendations/demand`, el servicio `recommendation_service.py` y la tabla `demandas_academicas` en PostgreSQL. Detalla la validación de campos obligatorios (`E001`), la detección y rechazo de solicitudes duplicadas (`E002`), y la persistencia transaccional confirmada con `db.commit()` que actualiza el acumulador de demanda en caché.

```plantuml
@startuml
title Diagrama 6.15.8: Diagrama de Secuencia - CUS-003: Registrar solicitud de demanda académica
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado
(UserRole.mentoreado)" as User
participant "Vista React
(DemandModalView.tsx)" as UI
participant "Adaptador Cliente
(recommendationService.ts)" as Client
participant "Controlador FastAPI
(endpoints/recommendations.py)" as API
participant "Servicio Backend
(recommendation_service.py)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Apertura del formulario de demanda y selección temática ==
User -> UI: 1. Clic en "Registrar Demanda de Tema" en cabecera o catálogo
activate UI
UI -> Client: loadAvailableCoursesAndTopics()
activate Client
Client -> API: GET /api/v1/curriculum/courses-with-topics
activate API
API -> Service: get_courses_with_topics()
activate Service
Service -> DB: SELECT * FROM cursos c JOIN temas_curriculares t ON c.id = t.curso_id
activate DB
DB --> Service: Asignaturas y temarios silábicos
deactivate DB
Service --> API: CoursesWithTopicsDTO
deactivate Service
API --> Client: HTTP 200 OK CoursesWithTopicsDTO
deactivate API
Client --> UI: Pobla selectores del modal
deactivate Client
UI --> User: 2. Abre modal con campos: curso, tema específico, franja preferida (mañana/tarde/noche), modalidad y comentarios
deactivate UI

== Fase 2: Ingreso de preferencias y despacho de solicitud ==
User -> UI: 3. Selecciona asignatura, tema específico, franja horaria preferida y pulsa "Enviar Solicitud"
activate UI
UI -> UI: Valida selección obligatoria de curso y tema

alt [E001] Formulario de demanda incompleto (tema o materia omitida)
    UI --> User: Resalta campos vacíos con borde rojo y texto explicativo
    User -> UI: Selecciona asignatura y tema silábico
    UI --> User: Rehabilita botón "Enviar Solicitud" y retorna al paso 3
else Formulario válido en cliente
    UI -> Client: createDemand(payload)
    activate Client
    Client -> API: POST /api/v1/recommendations/demand DemandCreateRequest [Bearer JWT]
    activate API
    API -> Service: create_demand_request(user_id, payload)
    activate Service
    
    Service -> DB: SELECT id FROM demandas_academicas
WHERE estudiante_id = :uid AND tema_id = :tid AND estado = 'PENDIENTE'
    activate DB
    DB --> Service: Registro existente o nulo
    deactivate DB
    
    alt [E002] Solicitud duplicada de demanda en estado PENDIENTE
        Service --> API: Lanza HTTPException(409, "DUPLICATE_DEMAND")
        API --> Client: HTTP 409 Conflict {"detail": "DUPLICATE_DEMAND: Ya mantienes una solicitud activa para este tema."}
        Client --> UI: Captura error 409
        UI --> User: Alerta ámbar "Ya tienes una solicitud activa registrada" y botón [Entendido]
        User -> UI: Clic en [Entendido]
        UI --> User: Cierra modal sin duplicar registros y retorna al paso 1
    else Demanda no duplicada
        == Fase 3: Registro transaccional e indexación de demanda grupal ==
        User -> UI: 5. Observa animación de registro de solicitud
        
        Service -> DB: BEGIN TRANSACTION
        activate DB
        Service -> DB: INSERT INTO demandas_academicas (estudiante_id, tema_id, franja_horaria, modalidad, comentarios, estado='PENDIENTE')
VALUES (:uid, :tid, :franja, :mod, :com, 'PENDIENTE') RETURNING id
        Service -> DB: UPDATE acumuladores_demanda SET total_solicitudes = total_solicitudes + 1 WHERE tema_id = :tid
        Service -> DB: COMMIT
        DB --> Service: Transacción confirmada (id_demanda)
        deactivate DB
        
        Service --> API: DemandResponseDTO {"id": id_demanda, "estado": "PENDIENTE"}
        API --> Client: HTTP 201 Created DemandResponseDTO
        Client --> UI: Confirmación de registro exitoso
        
        UI -> UI: Cierra modal de demanda
        UI --> User: 6. Notificación flotante verde de éxito: "Tu solicitud ha sido registrada y sumada a la demanda estudiantil de la EPIS"
    end
    deactivate Service
    deactivate API
    deactivate Client
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-003.


---

### MOD-05: Quórum, Confirmación y Cancelaciones

#### Diagrama 6.15.9: Diagrama de Secuencia - CUS-004: Reservar cupo de mentoría académica

El diagrama de secuencia para `CUS-004` formaliza el ciclo transaccional de reserva de cupos con control de aforo y concurrencia crítica bajo PostgreSQL. Modela detalladamente las cuatro fases de interacción entre el Estudiante Mentoreado, la interfaz React (`BookingModalView.tsx`), el adaptador `bookingService.ts`, el endpoint `POST /api/v1/bookings/reserve`, el servicio `booking_service.py` y la base de datos relacional. Incluye la adquisición del cerrojo en memoria `_booking_lock`, el bloqueo pesimista de fila `SELECT ... FOR UPDATE OF sesiones_mentoria` con timeout de 5.0s, y los diez flujos de excepción (`E001` a `E010`).

```plantuml
@startuml
title Diagrama 6.15.9: Diagrama de Secuencia - CUS-004: Reservar cupo de mentoría académica\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado\n(UserRole.mentoreado)" as User
participant "Vista React\n(BookingModalView.tsx / RecommendationFeedView.tsx)" as UI
participant "Adaptador Cliente\n(bookingService.ts / ApiBookingAdapter)" as Client
participant "Controlador FastAPI\n(endpoints/bookings.py)" as API
participant "Servicio Backend\n(booking_service.py / consent_service.py)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Exploración en Cartelera y Apertura del Diálogo Modal ==
User -> UI: 1. Navega por cartelera y pulsa "Reservar Cupo" en sesión en estado PUBLICADA
activate UI
UI -> UI: onSelectOffer: monta BookingModalView.tsx con offer, userEmail

alt [E001] Oferta en cartelera sin vacantes disponibles (available_slots <= 0)
    UI --> User: Inhabilita botón "Confirmar Reserva", aviso ámbar "Aforo completado" y botón [Volver a Cartelera]
    User -> UI: Clic en [Volver a Cartelera]
    UI --> User: Cierra modal y retorna al paso 1
else [E002] Reserva duplicada activa para el mismo estudiante
    UI -> Client: checkActiveBooking(offer.id, userEmail)
    activate Client
    Client -> API: GET /api/v1/bookings/check-duplicate?session_id={session_id}
    activate API
    API -> Service: check_active_booking(session_id, userEmail)
    activate Service
    Service -> DB: SELECT id FROM reservas_cupo WHERE id_sesion = :sid AND estudiante_email = :email AND estado IN ('PENDIENTE_CONFIRMACION', 'CONFIRMADA')
    activate DB
    DB --> Service: Reserva activa existente
    deactivate DB
    Service --> API: ActiveBookingResultDTO {"has_active": true}
    deactivate Service
    API --> Client: HTTP 400 Bad Request {"detail": "ALREADY_BOOKED"}
    deactivate API
    Client --> UI: Captura ALREADY_BOOKED
    deactivate Client
    UI --> User: Notificación roja "Ya posees una reserva activa registrada" y botón [Aceptar]
    User -> UI: Clic en [Aceptar]
    UI --> User: Cierra modal y retorna al paso 1
else Tarjeta con vacantes y sin duplicidad previa
    == Fase 2: Verificación de Precondiciones y Reglas de Negocio en Cliente ==
    User -> UI: 3. Revisa tema, curso, horario, modalidad, cupos restantes y pulsa "Confirmar Reserva"
    UI -> UI: Activa isSubmitting=true, deshabilita controles y muestra spinner azul institucional
    
    alt [E003] Sesión institucional no autenticada o token JWT expirado
        UI -> UI: localStorage.getItem('auth_token') retorna null o expirado
        UI --> User: Redirige a LoginOtpView.tsx con alerta roja "Sesión caducada por inactividad" (transfiere a CUS-001)
    else [E004] Conflicto de rol de mentor (Autoreserva Prohibida: offer.mentor_email === userEmail)
        UI --> User: Inhabilita acción, alerta roja "Un mentor no puede reservar cupos en su propia sesión" y botón [Cerrar]
        User -> UI: Clic en [Cerrar]
        UI --> User: Cierra modal y retorna al paso 1
    else [E005] Ausencia o revocación de consentimiento legal digital Ley N° 29733
        UI -> Client: getConsentStatus(userEmail)
        activate Client
        Client -> API: GET /api/v1/consent/status
        activate API
        API --> Client: HTTP 403 Forbidden {"detail": "CONSENT_REQUIRED"}
        deactivate API
        Client --> UI: Captura CONSENT_REQUIRED
        deactivate Client
        UI --> User: Oculta modal de reserva y monta ConsentModalView.tsx en primer plano
        User -> UI: Acepta términos Ley N° 29733 y pulsa "Aceptar y Continuar"
        UI --> User: Persiste consentimiento y retorna al paso 3
    else Precondiciones en cliente verificadas
        == Fase 3: Transacción Atómica con Bloqueo Pesimista en Base de Datos ==
        User -> UI: 5. Observa progreso de procesamiento seguro en pantalla
        UI -> Client: reserveSeat(offer.id, userEmail)
        activate Client
        Client -> API: POST /api/v1/bookings/reserve {"id_sesion": id, "estudiante_email": email} [Bearer JWT]
        activate API
        API -> Service: reserve_seat(session_id, user_email)
        activate Service
        
        Service -> Service: _booking_lock.acquire(timeout=5.0)
        
        alt [E009] Timeout de concurrencia en adquisición de cerrojo (_booking_lock timeout)
            Service --> API: Lanza HTTPException(503, "DATABASE_BUSY")
            API --> Client: HTTP 503 Service Unavailable {"detail": "DATABASE_BUSY: Servicio sobrecargado."}
            Client --> UI: Captura DATABASE_BUSY
            UI --> User: Aviso ámbar "Servicio con alta concurrencia temporal" y botón [Reintentar Reserva]
            User -> UI: Clic en [Reintentar Reserva]
            UI -> Client: reserveSeat(...) (retorna al paso 4)
        else Cerrojo en memoria adquirido
            Service -> DB: BEGIN TRANSACTION
            activate DB
            Service -> DB: SET LOCAL lock_timeout = '5.0s'
            Service -> DB: SELECT * FROM sesiones_mentoria WHERE id = :sid FOR UPDATE OF sesiones_mentoria
            DB --> Service: Fila bloqueada pesimistamente (aforo_maximo, cupos_ocupados, estado)
            
            alt [E006] Sesión de mentoría inexistente o cancelada concurrentemente
                Service -> DB: ROLLBACK
                Service --> API: Lanza HTTPException(404, "SESSION_NOT_FOUND")
                API --> Client: HTTP 404 Not Found {"detail": "SESSION_NOT_FOUND"}
                Client --> UI: Captura 404
                UI --> User: Modal rojo "La sesión ya no está disponible" y botón [Volver a Cartelera]
                User -> UI: Clic en [Volver a Cartelera]
                UI --> User: Retorna al paso 1
            else [E007] Ventana de antelación menor a 24 horas (now_utc > fecha_inicio - 24h, RN-04)
                Service -> DB: ROLLBACK
                Service --> API: Lanza HTTPException(400, "RESERVATION_WINDOW_CLOSED")
                API --> Client: HTTP 400 Bad Request {"detail": "RESERVATION_WINDOW_CLOSED"}
                Client --> UI: Captura 400
                UI --> User: Mensaje rojo "Plazo de reserva cerrado a T-24h" y botón [Entendido]
                User -> UI: Clic en [Entendido]
                UI --> User: Retorna al paso 1
            else [E008] Aforo agotado en el instante del cerrojo (cupos_ocupados >= aforo_maximo, RN-05)
                Service -> DB: ROLLBACK
                Service --> API: Lanza HTTPException(409, "CAPACITY_EXCEEDED")
                API --> Client: HTTP 409 Conflict {"detail": "CAPACITY_EXCEEDED: Último cupo reservado."}
                Client --> UI: Captura 409
                UI --> User: Alerta ámbar "El último cupo acaba de ser tomado" y botón [Ver Otras Sesiones]
                User -> UI: Clic en [Ver Otras Sesiones]
                UI --> User: Retorna al paso 1
            else Condiciones de reserva válidas y aforo garantizado
                Service -> Service: Genera ticket_hash = SHA256(uid + sid + timestamp)
                Service -> DB: INSERT INTO reservas_cupo (id_usuario, id_sesion, estado='PENDIENTE_CONFIRMACION', ticket_hash)\nVALUES (:uid, :sid, 'PENDIENTE_CONFIRMACION', :th) RETURNING id
                Service -> DB: UPDATE sesiones_mentoria SET cupos_ocupados = cupos_ocupados + 1 WHERE id = :sid
                
                alt [E010] Error inesperado en base de datos al confirmar transacción
                    DB --> Service: Database Write Error
                    Service -> DB: ROLLBACK
                    Service --> API: Lanza HTTPException(500, "TRANSACTION_FAILED")
                    API --> Client: HTTP 500 Internal Server Error {"detail": "TRANSACTION_FAILED"}
                    Client --> UI: Captura error 500
                    UI --> User: Error rojo transaccional y botón [Reintentar]
                    User -> UI: Clic en [Reintentar]
                    UI --> User: Retorna al paso 4
                else Transacción confirmada exitosamente
                    Service -> DB: COMMIT
                    DB --> Service: Transacción ACID confirmada
                    Service -> Service: _booking_lock.release()
                    
                    == Fase 4: Confirmación Provisional y Notificación de Plazo Límite ==
                    Service --> API: BookingCreateResponseDTO {"id": id_reserva, "estado": "PENDIENTE_CONFIRMACION", "deadline": t_minus_24h}
                    API --> Client: HTTP 201 Created BookingCreateResponseDTO
                    Client --> UI: Reserva provisional confirmada
                    
                    UI -> UI: isSubmitting=false, conmuta modal a estado de éxito
                    UI --> User: 6. Modal verde con número de comprobante, plazo hasta T-24h para ratificar asistencia (CUS-024) y botón [Ir a Mis Reservas]
                    User -> UI: 7. Clic en [Ir a Mis Reservas]
                    UI -> UI: Desmonta BookingModalView.tsx
                    UI --> User: Redirige a StudentBookingsView.tsx con la tarjeta en estado "Pendiente de Confirmación"
                end
            end
            deactivate DB
        end
        deactivate Service
        deactivate API
        deactivate Client
    end
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-004.

---

#### Diagrama 6.15.10: Diagrama de Secuencia - CUS-024: Ratificar asistencia a sesión de mentoría

El diagrama de secuencia para `CUS-024` formaliza la confirmación obligatoria de asistencia por parte de los estudiantes con reserva en la ventana reglamentaria entre 48 y 24 horas antes del inicio de la sesión (`[T-48h, T-24h]`, `RN-08`). Modela la interacción entre el Estudiante Mentoreado, el panel `StudentBookingsView.tsx`, `bookingService.ts`, el endpoint `POST /api/v1/bookings/{id}/confirm`, el servicio `booking_service.py` y PostgreSQL. Modela la validación de ventana temporal, la conmutación de estado a `CONFIRMADA`, la emisión del pase digital de asistencia con código alfanumérico y los flujos de excepción por ratificación anticipada (`E001`) o extemporánea (`E002`).

```plantuml
@startuml
title Diagrama 6.15.10: Diagrama de Secuencia - CUS-024: Ratificar asistencia obligatoria a sesión de mentoría a T-24h\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado\n(UserRole.mentoreado)" as User
participant "Vista React\n(StudentBookingsView.tsx)" as UI
participant "Adaptador Cliente\n(bookingService.ts)" as Client
participant "Controlador FastAPI\n(endpoints/bookings.py)" as API
participant "Servicio Backend\n(booking_service.py)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Identificación de reservas pendientes y verificación de ventana temporal ==
User -> UI: 1. Accede a "Mis Reservas" en StudentBookingsView.tsx
activate UI
UI -> Client: getMyBookings() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/bookings/my-bookings
activate API
API -> Service: get_user_bookings(user_email)
activate Service
Service -> DB: SELECT r.*, s.fecha_inicio, s.modalidad FROM reservas_cupo r\nJOIN sesiones_mentoria s ON r.id_sesion = s.id WHERE r.estudiante_email = :email
activate DB
DB --> Service: Lista de reservas del estudiante
deactivate DB
Service --> API: BookingListResponseDTO
deactivate Service
API --> Client: HTTP 200 OK BookingListResponseDTO
deactivate API
Client --> UI: Entrega reservas activas
deactivate Client
UI --> User: 2. Renderiza tarjetas con cuenta regresiva. En reservas dentro de [T-48h, T-24h], despliega botón ámbar "Confirmar Asistencia"

== Fase 2: Despacho de ratificación y validación de reglas de negocio ==
User -> UI: 3. Clic en botón "Confirmar Asistencia" en la tarjeta
UI --> User: 4. Abre modal de confirmación con texto: "¿Se compromete a asistir puntualmente a la sesión?"
User -> UI: Pulsa "Sí, Confirmo mi Asistencia Definitiva"

UI -> Client: confirmBooking(bookingId)
activate Client
Client -> API: POST /api/v1/bookings/{id}/confirm [Bearer JWT]
activate API
API -> Service: confirm_booking(booking_id, user_email)
activate Service

Service -> DB: SELECT r.*, s.fecha_inicio FROM reservas_cupo r\nJOIN sesiones_mentoria s ON r.id_sesion = s.id\nWHERE r.id = :bid AND r.estudiante_email = :email
activate DB
DB --> Service: Datos de reserva y horario de sesión
deactivate DB

alt [E001] Intento de ratificación anticipada fuera de ventana (now_utc < fecha_inicio - 48h)
    Service --> API: Lanza HTTPException(400, "CONFIRMATION_NOT_OPEN")
    API --> Client: HTTP 400 Bad Request {"detail": "CONFIRMATION_NOT_OPEN: La ventana abre 48h antes del inicio."}
    Client --> UI: Captura error 400
    UI --> User: Mensaje azul "La ratificación se habilitará exactamente 48h antes de la sesión" y botón [Entendido]
    User -> UI: Clic en [Entendido]
    UI --> User: Cierra modal y retorna al paso 2
else [E002] Ventana de ratificación vencida a T-24h (now_utc > fecha_inicio - 24h)
    Service --> API: Lanza HTTPException(400, "CONFIRMATION_WINDOW_EXPIRED")
    API --> Client: HTTP 400 Bad Request {"detail": "CONFIRMATION_WINDOW_EXPIRED: Ventana cerró a T-24h."}
    Client --> UI: Captura error 400
    UI --> User: Tarjeta en gris indicando cupo dado de baja por falta de ratificación y botón [Aceptar]
    User -> UI: Clic en [Aceptar]
    UI --> User: Actualiza lista de reservas y retorna al paso 2
else Dentro de la ventana reglamentaria [T-48h, T-24h]
    == Fase 3: Transición atómica de estado y emisión de pase de asistencia ==
    User -> UI: 5. Espera confirmación visual
    Service -> DB: BEGIN TRANSACTION
    activate DB
    Service -> DB: UPDATE reservas_cupo SET estado = 'CONFIRMADA', fecha_confirmacion = NOW() WHERE id = :bid
    Service -> DB: COMMIT
    DB --> Service: Transacción confirmada
    deactivate DB
    
    Service --> API: BookingResponseDTO {"id": booking_id, "estado": "CONFIRMADA", "pass_code": "PASS-8472"}
    API --> Client: HTTP 200 OK BookingResponseDTO
    Client --> UI: Asistencia confirmada
    
    UI -> UI: Conmuta tarjeta a color verde con leyenda "Asistencia Ratificada"
    UI --> User: 6. Despliega código alfanumérico para el pase de lista y emite notificación de éxito
end
deactivate Service
deactivate API
deactivate Client
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-024.

---

#### Diagrama 6.15.11: Diagrama de Secuencia - CUS-017: Desistir voluntariamente de reserva

El diagrama de secuencia para `CUS-017` modela la anulación voluntaria de una reserva de cupo sin penalización académica, condicionada a una antelación mayor a 24 horas (`fecha_inicio > now_utc + 24h`, `RN-04`). Modela las interacciones entre el Estudiante Mentoreado, `StudentBookingsView.tsx`, `bookingService.ts`, el endpoint `POST /api/v1/bookings/{id}/cancel`, `booking_service.py` y PostgreSQL. Modela la adquisición del cerrojo pesimista de fila, la conmutación a estado `CANCELADA_ESTUDIANTE`, la reducción atómica del contador de cupos ocupados y el rechazo de cancelaciones tardías (`E001`).

```plantuml
@startuml
title Diagrama 6.15.11: Diagrama de Secuencia - CUS-017: Desistir voluntariamente de reserva de cupo sin penalidad antes de T-24h\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado\n(UserRole.mentoreado)" as User
participant "Vista React\n(StudentBookingsView.tsx)" as UI
participant "Adaptador Cliente\n(bookingService.ts)" as Client
participant "Controlador FastAPI\n(endpoints/bookings.py)" as API
participant "Servicio Backend\n(booking_service.py)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Solicitud de desistimiento y verificación de plazos ==
User -> UI: 1. Localiza reserva activa en "Mis Reservas" y pulsa "Cancelar Reserva"
activate UI
UI --> User: 2. Abre modal de advertencia indicando que el desistimiento es irrevocable y solicita motivo opcional

alt [E001] Desistimiento tardío con menos de 24 horas de antelación (fecha_inicio <= now_utc + 24h)
    UI -> Client: checkCancellationDeadline(bookingId)
    activate Client
    Client -> API: GET /api/v1/bookings/{id}/cancellation-eligibility
    activate API
    API -> Service: check_cancellation_eligibility(booking_id)
    activate Service
    Service -> DB: SELECT s.fecha_inicio FROM reservas_cupo r JOIN sesiones_mentoria s ON r.id_sesion = s.id WHERE r.id = :bid
    activate DB
    DB --> Service: Horario de sesión (T < 24h)
    deactivate DB
    Service --> API: CancellationEligibilityDTO {"eligible": false, "reason": "LATE_CANCELLATION"}
    deactivate Service
    API --> Client: HTTP 400 Bad Request {"detail": "LATE_CANCELLATION_PROHIBITED: Menos de 24h de antelación."}
    deactivate API
    Client --> UI: Captura error 400
    deactivate Client
    UI --> User: Advertencia roja "No se permite cancelación voluntaria a menos de 24h para no desestabilizar quórum" y botón [Entendido]
    User -> UI: Clic en [Entendido]
    UI --> User: Cierra modal manteniendo la reserva activa y retorna al paso 1
else Antelación superior a 24 horas (cumple RN-04)
    == Fase 2: Confirmación y procesamiento atómico de liberación de cupo ==
    User -> UI: 3. Selecciona motivo opcional y pulsa "Confirmar Cancelación"
    UI -> Client: cancelBooking(bookingId, reason)
    activate Client
    Client -> API: POST /api/v1/bookings/{id}/cancel {"reason": reason} [Bearer JWT]
    activate API
    API -> Service: cancel_booking(booking_id, user_email, reason)
    activate Service
    
    Service -> DB: BEGIN TRANSACTION
    activate DB
    Service -> DB: SELECT * FROM reservas_cupo WHERE id = :bid FOR UPDATE
    Service -> DB: SELECT * FROM sesiones_mentoria WHERE id = :sid FOR UPDATE
    Service -> DB: UPDATE reservas_cupo SET estado = 'CANCELADA_ESTUDIANTE', fecha_cancelacion = NOW(), motivo_cancelacion = :reason WHERE id = :bid
    Service -> DB: UPDATE sesiones_mentoria SET cupos_ocupados = cupos_ocupados - 1 WHERE id = :sid
    Service -> DB: COMMIT
    DB --> Service: Transacción ACID confirmada
    deactivate DB
    
    Service --> API: BookingResponseDTO {"id": booking_id, "estado": "CANCELADA_ESTUDIANTE"}
    deactivate Service
    API --> Client: HTTP 200 OK BookingResponseDTO
    deactivate API
    Client --> UI: Desistimiento confirmado
    deactivate Client
    
    UI --> User: 5. Modal de éxito indicando liberación correcta del cupo sin penalización
    UI -> UI: Cierra modal, conmuta tarjeta a color gris con leyenda "Cancelada por el estudiante"
    UI --> User: 6. Emite evento de actualización que incrementa las vacantes disponibles en la cartelera
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-017.

---

#### Diagrama 6.15.12: Diagrama de Secuencia - CUS-023: Evaluar quórum automático a T-24h

El diagrama de secuencia para `CUS-023` especifica el proceso automatizado y desatendido de evaluación de quórum reglamentario (mínimo 3 estudiantes con asistencia ratificada, `RN-05`) ejecutado exactamente 24 horas antes del inicio de cada sesión de mentoría. Modela la interacción entre el Proceso Demonio (`SchedulerWorker` / Celery / APScheduler), el controlador de quórum en `quorum.py`, `booking_service.py`, `simulation_service.py`, PostgreSQL y el servicio de correo SMTP. Incluye la promoción automática a `CONFIRMADA` si se cumple el quórum, y la transición a `QUORUM_INSUFICIENTE` con disparo de alertas urgentes (`A001`) si no se alcanza el umbral.

```plantuml
@startuml
title Diagrama 6.15.12: Diagrama de Secuencia - CUS-023: Evaluar automáticamente el quórum reglamentario de sesiones de mentoría a T-24h\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

participant "Planificador\n(SchedulerWorker / Celery)" as Cron
actor "Administrador Institucional\n(UserRole.administrador)" as Admin
participant "Vista React\n(AdminDashboardView.tsx / MentorSessionsView.tsx)" as UI
participant "Adaptador Cliente\n(quorumService.ts / apiClient)" as Client
participant "Controlador FastAPI\n(endpoints/quorum.py)" as API
participant "Servicio Backend\n(booking_service.py / simulation_service.py)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB
participant "Servicio SMTP UPT\n(EmailService)" as SMTP
actor "Estudiante Mentor" as Mentor
actor "Estudiante Mentoreado" as Mentoreado

== Fase 1: Disparo de la tarea programada y localización de sesiones a T-24h ==
alt Disparo automatizado por demonio programado
    Cron -> API: 1. Disparo automático de corte de quórum a T-24h
else Disparo administrativo o simulado desde consola
    Admin -> UI: 1. Accede a panel administrativo y pulsa "Evaluar Quórum Masivo"
    activate UI
    UI -> Client: triggerQuorumEvaluation() [Bearer JWT]
    activate Client
    Client -> API: POST /api/v1/quorum/evaluate-all
    deactivate Client
    deactivate UI
end
activate API
API -> Service: evaluate_all_active_quorums()
activate Service

Service -> DB: SELECT * FROM sesiones_mentoria\nWHERE estado = 'PUBLICADA' AND fecha_inicio <= NOW() + INTERVAL '24 HOURS'
activate DB
DB --> Service: Lista de sesiones en ventana T-24h
deactivate DB

== Fase 2: Cuantificación de confirmaciones y verificación de umbral de quórum ==
loop Para cada sesión en ventana T-24h
    Service -> DB: SELECT count(*) FROM reservas_cupo WHERE id_sesion = :sid AND estado = 'CONFIRMADA'
    activate DB
    DB --> Service: confirmed_count (número de estudiantes ratificados)
    deactivate DB
    
    alt [A001] Quórum insuficiente a T-24h (confirmed_count < 3 estudiantes, RN-05)
        Service -> DB: BEGIN TRANSACTION
        activate DB
        Service -> DB: UPDATE sesiones_mentoria SET estado = 'QUORUM_INSUFICIENTE' WHERE id = :sid
        Service -> DB: INSERT INTO auditoria_evaluacion (sesion_id, estado_anterior='PUBLICADA', nuevo_estado='QUORUM_INSUFICIENTE', quorum_logrado=confirmed_count, fecha=NOW())
        Service -> DB: COMMIT
        DB --> Service: Transacción confirmada
        deactivate DB
        
        Service -> SMTP: send_urgent_quorum_alert(mentor_email, session_id, confirmed_count)
        activate SMTP
        SMTP --> Mentor: A001-1.3 Alerta urgente al Mentor: "Tu sesión de mañana no alcanzó quórum de 3 alumnos. Ingrese para decidir."
        deactivate SMTP
        
        Service -> UI: Emite evento WebSocket / SSE hacia panel de control
        UI --> Mentor: Notificación flotante de quórum insuficiente
        Service --> API: A001-1.4 Sesión en QUORUM_INSUFICIENTE (transfiere a CUS-007)
    else Quórum reglamentario alcanzado (confirmed_count >= 3 estudiantes)
        == Fase 3: Confirmación oficial de sesión y notificación de viabilidad ==
        Service -> DB: BEGIN TRANSACTION
        activate DB
        Service -> DB: UPDATE sesiones_mentoria SET estado = 'CONFIRMADA' WHERE id = :sid
        Service -> DB: INSERT INTO auditoria_evaluacion (sesion_id, estado_anterior='PUBLICADA', nuevo_estado='CONFIRMADA', quorum_logrado=confirmed_count, fecha=NOW())
        Service -> DB: COMMIT
        DB --> Service: Transacción confirmada
        deactivate DB
        
        Service -> SMTP: send_session_confirmed_email(mentor_email, session_data)
        activate SMTP
        SMTP --> Mentor: Correo de confirmación oficial de dictado de sesión
        deactivate SMTP
        
        Service -> SMTP: send_confirmation_to_students(enrolled_emails, session_data)
        activate SMTP
        SMTP --> Mentoreado: Correo oficial: "¡Sesión confirmada! Cuenta con quórum reglamentario."
        deactivate SMTP
        
        Service -> UI: Emite evento de sesión confirmada para refrescar cartelera
        UI --> Mentoreado: Actualiza estado a CONFIRMADA en interfaz
        Service --> API: SessionQuorumResultDTO {"session_id": sid, "status": "CONFIRMADA", "confirmed_students": confirmed_count}
    end
end

Service --> API: BatchQuorumEvaluationSummaryDTO
deactivate Service
API --> Cron: HTTP 200 OK (Ciclo completado)
deactivate API
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-023.

---

#### Diagrama 6.15.13: Diagrama de Secuencia - CUS-007: Decisión del mentor ante quórum insuficiente

El diagrama de secuencia para `CUS-007` modela la gestión resolutiva que ejecuta el estudiante mentor cuando una sesión no alcanza el quórum a T-24h (estado `QUORUM_INSUFICIENTE`). Modela las interacciones entre el Mentor, `MentorSessionsView.tsx`, `offerService.ts`, el endpoint `POST /api/v1/offers/{offer_id}/quorum-decision`, `offer_service.py` y PostgreSQL. Abarca las tres alternativas de resolución: dictar de todas formas (`PROCEED`), reprogramar con antelación mayor a 24 horas (`RESCHEDULE`, con validación `E001`), o cancelar definitivamente con justificación obligatoria (`CANCEL`, con validación `E002`), actualizando los estados y notificando a los estudiantes inscritos.

```plantuml
@startuml
title Diagrama 6.15.13: Diagrama de Secuencia - CUS-007: Decisión del mentor ante quórum insuficiente\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor\n(UserRole.mentor)" as Mentor
participant "Vista React\n(MentorSessionsView.tsx)" as UI
participant "Adaptador Cliente\n(offerService.ts)" as Client
participant "Controlador FastAPI\n(endpoints/offers.py)" as API
participant "Servicio Backend\n(offer_service.py)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB
participant "Servicio SMTP UPT\n(EmailService)" as SMTP
actor "Estudiantes Inscritos" as Students

== Fase 1: Acceso a la sesión con quórum insuficiente y visualización de opciones ==
Mentor -> UI: 1. Accede a "Mis Sesiones" y visualiza tarjeta resaltada en ámbar "Quórum Insuficiente"
activate UI
Mentor -> UI: 2. Clic en botón "Gestionar Sesión"
UI --> Mentor: Abre modal con estudiantes ratificados y 3 opciones: [Dictar de Todas Formas], [Reprogramar Sesión], [Cancelar Sesión]

== Fase 2: Elección de la resolución y verificación de parámetros ==
alt Decisión == 'RESCHEDULE' con nueva fecha ingresada
    Mentor -> UI: 3. Selecciona "Reprogramar Sesión" e ingresa nueva fecha y hora
    UI -> UI: Valida en cliente que nueva fecha > now_utc + 24h
    
    alt [E001] Fecha de reprogramación con menos de 24 horas de antelación
        UI --> Mentor: Resalta selector de fecha en rojo, aviso: "La nueva fecha debe ser al menos 24h posterior al momento actual"
        Mentor -> UI: Selecciona fecha y hora reglamentaria (> 24h)
        UI --> Mentor: Rehabilita botón de confirmación y retorna al paso 3
    end
else Decisión == 'CANCEL' con motivo de cancelación
    Mentor -> UI: 3. Selecciona "Cancelar Sesión"
    
    alt [E002] Justificación de cancelación definitiva vacía
        UI --> Mentor: Resalta cuadro de texto obligatorio en rojo con mensaje de error
        Mentor -> UI: Ingresa justificación válida de cancelación
        UI --> Mentor: Rehabilita botón y retorna al paso 3
    end
else Decisión == 'PROCEED' (Dictar de todas formas)
    Mentor -> UI: 3. Selecciona opción "Dictar de Todas Formas"
end

Mentor -> UI: 4. Presiona botón "Confirmar Decisión Resolutiva"
UI -> Client: submitQuorumDecision(offerId, decision, payload)
activate Client
Client -> API: POST /api/v1/offers/{offer_id}/quorum-decision {"decision": d, ...} [Bearer JWT]
activate API
API -> Service: process_quorum_decision(mentor_id, offer_id, decision, payload)
activate Service

== Fase 3: Persistencia de la resolución y notificación a los estudiantes ==
Service -> DB: BEGIN TRANSACTION
activate DB

alt Decisión == 'PROCEED' (Confirmar dictado a pesar del quórum bajo)
    Service -> DB: UPDATE sesiones_mentoria SET estado = 'CONFIRMADA' WHERE id = :oid
    Service -> DB: COMMIT
    Service -> SMTP: notify_students_session_confirmed(enrolled_emails)
    activate SMTP
    SMTP --> Students: Notificación: "Tu sesión de mentoría se dictará según lo programado"
    deactivate SMTP
else Decisión == 'RESCHEDULE' (Reprogramar sesión)
    Service -> DB: UPDATE sesiones_mentoria SET estado = 'PUBLICADA', fecha_inicio = :new_start, fecha_fin = :new_end WHERE id = :oid
    Service -> DB: UPDATE reservas_cupo SET estado = 'PENDIENTE_CONFIRMACION' WHERE id_sesion = :oid
    Service -> DB: COMMIT
    Service -> SMTP: notify_students_session_rescheduled(enrolled_emails, new_start)
    activate SMTP
    SMTP --> Students: Notificación: "La sesión ha sido reprogramada. Por favor confirme su nueva fecha."
    deactivate SMTP
else Decisión == 'CANCEL' (Cancelar definitivamente)
    Service -> DB: UPDATE sesiones_mentoria SET estado = 'CANCELADA_QUORUM', motivo_cancelacion = :reason WHERE id = :oid
    Service -> DB: UPDATE reservas_cupo SET estado = 'CANCELADA_SISTEMA' WHERE id_sesion = :oid
    Service -> DB: COMMIT
    Service -> SMTP: notify_students_session_cancelled(enrolled_emails, reason)
    activate SMTP
    SMTP --> Students: Notificación: "Sesión cancelada por no alcanzar quórum reglamentario."
    deactivate SMTP
end
deactivate DB

Service --> API: QuorumResolutionResponseDTO {"success": true, "new_state": estado}
deactivate Service
API --> Client: HTTP 200 OK QuorumResolutionResponseDTO
deactivate API
Client --> UI: Resolución confirmada
deactivate Client

UI -> UI: Cierra cuadro modal y actualiza estado de tarjeta
UI --> Mentor: 6. Notificación flotante verde: "Decisión registrada exitosamente"
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-007.


---

### MOD-06: Asistencia, Bitácoras y Feedback

#### Diagrama 6.15.14: Diagrama de Secuencia - CUS-012: Registrar asistencia a sesión de mentoría

El diagrama de secuencia para `CUS-012` especifica la captura y validación en tiempo real de la asistencia efectiva mediante códigos QR dinámicos basados en TOTP de 30 segundos. Desglosa los participantes: Estudiante Mentor, Estudiante Mentoreado, `SessionAttendanceView.tsx`, `attendanceService.ts`, `attendance.py`, `attendance_service.py`, WebSockets y PostgreSQL. Modela la rotación criptográfica del token, la verificación de reservas ratificadas y ventana de tolerancia horaria (`-15m` a `+30m`), y los flujos de excepción por caducidad de token (`E001`), ausencia de reserva (`E002`) y fuera de ventana (`E003`).

```plantuml
@startuml
title Diagrama 6.15.14: Diagrama de Secuencia - CUS-012: Registrar asistencia interactiva mediante código QR dinámico
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor
(UserRole.mentor)" as Mentor
actor "Estudiante Mentoreado
(UserRole.mentoreado)" as Mentoreado
participant "Vista React (Mentor / Alumno)
(SessionAttendanceView.tsx)" as UI
participant "Adaptador Cliente
(attendanceService.ts)" as Client
participant "Controlador FastAPI
(endpoints/attendance.py)" as API
participant "Servicio Backend
(attendance_service.py)" as Service
participant "Servicio WebSocket
(FastAPI WS Manager)" as WS
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Apertura de sesión y generación de token dinámico de asistencia ==
Mentor -> UI: 1. Accede a sesión activa y pulsa "Iniciar Pase de Asistencia Digital"
activate UI
UI -> Client: getAttendanceToken(sessionId)
activate Client
Client -> API: GET /api/v1/sessions/{session_id}/attendance/token [Bearer JWT]
activate API
API -> Service: generate_totp_token(session_id)
activate Service
Service -> Service: Genera token TOTP con ciclo de rotación de 30 segundos
Service --> API: AttendanceTokenDTO {"totp_token": token, "expires_in": 30}
deactivate Service
API --> Client: HTTP 200 OK AttendanceTokenDTO
deactivate API
Client --> UI: Entrega token TOTP serializado
deactivate Client
UI --> Mentor: 2. Proyecta código QR dinámico interactivo en pantalla y nómina provisional de alumnos ("Ausente")
deactivate UI

== Fase 2: Escaneo de código QR y validación de reserva y ventana horaria ==
Mentoreado -> UI: 3. Escanea código QR desde móvil o digita código de 6 dígitos y pulsa "Registrar Mi Asistencia"
activate UI
UI -> Client: registerCheckIn(sessionId, qrToken)
activate Client
Client -> API: POST /api/v1/sessions/{session_id}/attendance/check-in {"qr_token": token} [Bearer JWT]
activate API
API -> Service: record_checkin(session_id, mentoreado_id, qr_token)
activate Service

alt [E001] Código QR o token TOTP expirado (> 30 segundos)
    Service --> API: Lanza HTTPException(400, "QR_TOKEN_EXPIRED")
    API --> Client: HTTP 400 Bad Request {"detail": "QR_TOKEN_EXPIRED: Escanee el código QR actualizado."}
    Client --> UI: Captura error 400
    UI --> Mentoreado: Advertencia ámbar "Código expirado, enfoque el código QR actualizado del mentor" y botón [Escanear Nuevo Código]
    Mentoreado -> UI: Clic en [Escanear Nuevo Código]
    UI --> Mentoreado: Captura nuevo token y retorna al paso 3
else Token TOTP vigente
    Service -> DB: SELECT id FROM reservas_cupo WHERE id_sesion = :sid AND id_estudiante = :uid AND estado = 'CONFIRMADA'
    activate DB
    DB --> Service: Reserva confirmada o nulo
    deactivate DB
    
    alt [E002] Estudiante sin reserva previa confirmada en la sesión
        Service --> API: Lanza HTTPException(403, "NO_CONFIRMED_BOOKING")
        API --> Client: HTTP 403 Forbidden {"detail": "NO_CONFIRMED_BOOKING: No registra reserva confirmada."}
        Client --> UI: Captura error 403
        UI --> Mentoreado: Alerta roja "Sólo estudiantes debidamente ratificados a T-24h pueden registrar asistencia" y botón [Entendido]
        Mentoreado -> UI: Clic en [Entendido]
        UI --> Mentoreado: Cierra escáner y finaliza interacción
    else Reserva ratificada verificada
        alt [E003] Check-in fuera del intervalo temporal reglamentario (fuera de [inicio-15m, fin+30m])
            Service --> API: Lanza HTTPException(400, "CHECKIN_WINDOW_CLOSED")
            API --> Client: HTTP 400 Bad Request {"detail": "CHECKIN_WINDOW_CLOSED: Fuera de ventana reglamentaria."}
            Client --> UI: Captura error 400
            UI --> Mentoreado: Mensaje rojo "El pase de asistencia se encuentra cerrado" y botón [Aceptar]
            Mentoreado -> UI: Clic en [Aceptar]
            UI --> Mentoreado: Redirige a vista principal y finaliza caso de uso
        else Dentro del intervalo horario de la sesión
            == Fase 3: Persistencia de asistencia y actualización reactiva en tiempo real ==
            Mentoreado -> UI: 5. Observa progreso en pantalla
            Service -> DB: BEGIN TRANSACTION
            activate DB
            Service -> DB: INSERT INTO asistencias_sesion (sesion_id, estudiante_id, fecha_checkin, asistio, ip_origen)
VALUES (:sid, :uid, NOW(), true, :ip)
ON CONFLICT (sesion_id, estudiante_id) DO UPDATE SET asistio = true, fecha_checkin = NOW()
            Service -> DB: COMMIT
            DB --> Service: Asistencia persistida
            deactivate DB
            
            Service -> WS: broadcast_attendance_event(session_id, {"student_id": uid, "status": "PRESENTE"})
            activate WS
            WS --> UI: Evento WebSocket transmitido al panel del mentor
            deactivate WS
            UI -> UI: Actualiza fila del estudiante a estado "Presente" con distintivo verde en panel del mentor
            
            Service --> API: AttendanceResponseDTO {"success": true, "asistio": true}
            API --> Client: HTTP 200 OK AttendanceResponseDTO
            Client --> UI: Asistencia registrada exitosamente
            UI --> Mentoreado: 6. Notificación verde de éxito: "¡Asistencia registrada exitosamente! Gracias por tu puntualidad."
        end
    end
end
deactivate Service
deactivate API
deactivate Client
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-012.

---

#### Diagrama 6.15.15: Diagrama de Secuencia - CUS-013: Registrar bitácora pedagógica de sesión

El diagrama de secuencia para `CUS-013` modela el registro del reporte formativo post-sesión por parte del estudiante mentor. Modela la interacción entre el Mentor, `BitacoraFormView.tsx`, `bitacoraService.ts`, `bitacora.py`, `bitacora_service.py` y PostgreSQL. Especifica la validación del plazo reglamentario de 48 horas (`RN-12`, `E001`), la exigencia de al menos 50 caracteres pedagógicos (`E002`), el cómputo de la firma digital criptográfica SHA-256 sobre el contenido pedagógico y la promoción de la sesión a estado `BITACORA_REGISTRADA`.

```plantuml
@startuml
title Diagrama 6.15.15: Diagrama de Secuencia - CUS-013: Registrar bitácora pedagógica y reporte formativo
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor
(UserRole.mentor)" as Mentor
participant "Vista React
(BitacoraFormView.tsx)" as UI
participant "Adaptador Cliente
(bitacoraService.ts / ApiBitacoraAdapter)" as Client
participant "Controlador FastAPI
(endpoints/bitacora.py)" as API
participant "Servicio Backend
(bitacora_service.py / BitacoraService)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Apertura de bitácora y verificación de plazo límite a 48h ==
Mentor -> UI: 1. Ingresa a sesión concluida y presiona "Completar Bitácora Pedagógica"
activate UI
UI -> Client: verifySessionDeadline(sessionId)
activate Client
Client -> API: GET /api/v1/sessions/{session_id}/bitacora-eligibility [Bearer JWT]
activate API
API -> Service: check_bitacora_eligibility(session_id)
activate Service
Service -> DB: SELECT fecha_fin, estado FROM sesiones_mentoria WHERE id = :sid
activate DB
DB --> Service: Datos de finalización de sesión
deactivate DB

alt [E001] Plazo límite de 48 horas post-sesión vencido (now_utc > fecha_fin + 48h, RN-12)
    Service --> API: Lanza HTTPException(400, "DEADLINE_EXCEEDED")
    API --> Client: HTTP 400 Bad Request {"detail": "DEADLINE_EXCEEDED: Plazo reglamentario de 48h vencido."}
    Client --> UI: Captura error 400
    UI --> Mentor: Deshabilita formulario, advertencia roja "Bitácora fuera de plazo reglamentario" y botón [Solicitar Desbloqueo]
    Mentor -> UI: Clic en [Solicitar Desbloqueo a Coordinación]
    UI --> Mentor: Abre formulario de prórroga y finaliza interacción
else Dentro del plazo reglamentario de 48 horas
    Service --> API: BitacoraEligibilityDTO {"eligible": true}
    API --> Client: HTTP 200 OK {"eligible": true}
    Client --> UI: Habilita formulario
    UI --> Mentor: 2. Renderiza formulario: temas silábicos cubiertos (checkboxes), dificultad (Bajo/Medio/Alto), observaciones y declaración jurada
end
deactivate Service
deactivate API
deactivate Client
deactivate UI

== Fase 2: Ingreso de evidencias pedagógicas y validación de contenido ==
Mentor -> UI: 3. Marca temas explicados, selecciona asimilación, redacta incidencias pedagógicas y pulsa "Guardar y Firmar Bitácora"
activate UI
UI -> UI: Valida observaciones pedagógicas (longitud >= 50 caracteres)

alt [E002] Descripción pedagógica insuficiente (< 50 caracteres)
    UI --> Mentor: Resalta texto en rojo, muestra contador indicando caracteres faltantes
    Mentor -> UI: Amplía descripción pedagógica hasta superar 50 caracteres
    UI --> Mentor: Actualiza contador y retorna al paso 3
else Contenido sustantivo válido
    UI -> Client: submitBitacora(sessionId, payload)
    activate Client
    Client -> API: POST /api/v1/sessions/{session_id}/bitacora BitacoraCreateRequest [Bearer JWT]
    activate API
    API -> Service: create_bitacora(mentor_id, session_id, payload)
    activate Service
    
    == Fase 3: Persistencia transaccional y certificación de horas ==
    Mentor -> UI: 5. Observa barra de progreso mientras se genera hash criptográfico de integridad
    
    Service -> Service: Calcula hash SHA-256(temas + observaciones + mentor_id + timestamp)
    Service -> DB: BEGIN TRANSACTION
    activate DB
    Service -> DB: INSERT INTO bitacoras_pedagogicas (sesion_id, mentor_id, temas_cubiertos, observaciones, nivel_dificultad, hash_firma, fecha_registro)
VALUES (:sid, :mid, :temas, :obs, :dif, :hash, NOW()) RETURNING id
    Service -> DB: UPDATE sesiones_mentoria SET estado = 'BITACORA_REGISTRADA' WHERE id = :sid
    Service -> DB: COMMIT
    DB --> Service: Transacción confirmada
    deactivate DB
    
    Service --> API: BitacoraResponseDTO {"id": id_bitacora, "hash_firma": hash, "estado": "BITACORA_REGISTRADA"}
    deactivate Service
    API --> Client: HTTP 201 Created BitacoraResponseDTO
    deactivate API
    Client --> UI: Bitácora formalizada
    deactivate Client
    
    UI --> Mentor: 6. Panel verde de confirmación con código de firma digital SHA-256 y redirección al historial de sesiones
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-013.

---

#### Diagrama 6.15.16: Diagrama de Secuencia - CUS-014: Visualizar historial y bitácoras académicas

El diagrama de secuencia para `CUS-014` formaliza la consulta histórica unificada del itinerario de mentorías para estudiantes y mentores. Modela la interacción entre el usuario universitario, `HistorySessionsView.tsx`, `historyService.ts`, `history.py`, `history_service.py` y las tablas de sesiones, bitácoras y asistencias en PostgreSQL. Detalla la renderización de la línea de tiempo interactiva, el filtrado cronológico por ciclo y materia, el tratamiento de usuarios nuevos con historial vacío (`A001`), y la inspección modal de bitácoras pedagógicas con comprobación de firmas criptográficas.

```plantuml
@startuml
title Diagrama 6.15.16: Diagrama de Secuencia - CUS-014: Visualizar historial académico integral y bitácoras pedagógicas
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado / Mentor" as User
participant "Vista React
(HistorySessionsView.tsx)" as UI
participant "Adaptador Cliente
(historyService.ts)" as Client
participant "Controlador FastAPI
(endpoints/history.py)" as API
participant "Servicio Backend
(history_service.py)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta del historial y aplicación de filtros cronológicos ==
User -> UI: 1. Clic en "Mi Historial" en el menú de navegación lateral
activate UI
UI -> Client: getUserHistory() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/history/sessions
activate API
API -> Service: get_user_history(user_id)
activate Service
Service -> DB: SELECT s.*, b.hash_firma, a.asistio FROM sesiones_mentoria s
LEFT JOIN bitacoras_pedagogicas b ON s.id = b.sesion_id
LEFT JOIN asistencias_sesion a ON s.id = a.sesion_id
WHERE s.id_mentor = :uid OR a.estudiante_id = :uid ORDER BY s.fecha_inicio DESC
activate DB
DB --> Service: Historial de sesiones y asistencias
deactivate DB

alt [A001] Historial académico vacío para usuario nuevo (cero registros)
    Service --> API: EmptyHistoryDTO []
    API --> Client: HTTP 200 OK []
    Client --> UI: Lista vacía
    UI --> User: A001-1.2 Panel azul "Aún no registras sesiones en tu historial" y botón [Explorar Cartelera]
    User -> UI: A001-1.3 Clic en [Explorar Cartelera]
    UI --> User: A001-1.4 Redirige a RecommendationFeedView.tsx (retorna a CUS-002)
else Historial con registros consolidados
    Service --> API: UserHistoryResponseDTO
    API --> Client: HTTP 200 OK UserHistoryResponseDTO
    Client --> UI: Entrega historial cronológico
    UI --> User: 2. Renderiza tarjetas de sesiones en línea de tiempo interactiva con distintivos (Concluida, Bitácora Registrada, Visada)
end
deactivate Service
deactivate API
deactivate Client
deactivate UI

== Fase 2: Búsqueda y filtrado por materia o período académico ==
User -> UI: 3. Filtra por semestre o escribe nombre de materia en buscador
activate UI
UI -> UI: 4. Actualiza reactivamente la lista de tarjetas en pantalla
deactivate UI

== Fase 3: Visualización de bitácora pedagógica y comprobante de asistencia ==
User -> UI: 5. Presiona botón "Ver Bitácora Pedagógica" en tarjeta seleccionada
activate UI
UI -> Client: getSessionBitacora(sessionId)
activate Client
Client -> API: GET /api/v1/history/bitacora/{session_id} [Bearer JWT]
activate API
API -> Service: get_bitacora_detail(session_id)
activate Service
Service -> DB: SELECT b.*, u.nombres as mentor_nombre FROM bitacoras_pedagogicas b
JOIN usuarios u ON b.mentor_id = u.id WHERE b.sesion_id = :sid
activate DB
DB --> Service: Detalle pedagógico y firma digital SHA-256
deactivate DB
Service --> API: BitacoraDetailDTO
deactivate Service
API --> Client: HTTP 200 OK BitacoraDetailDTO
deactivate API
Client --> UI: Entrega detalle pedagógico
deactivate Client

UI --> User: 6. Despliega modal con temas cubiertos, nivel de dificultad, observaciones, firma SHA-256 y botón de exportación legible
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-014.


---

### MOD-07: Gamificación e Incentivos

#### Diagrama 6.15.17: Diagrama de Secuencia - CUS-018: Emitir constancia institucional de horas de mentoría

El diagrama de secuencia para `CUS-018` especifica la emisión institucional y descarga de la constancia de horas de mentoría con validación del umbral reglamentario de 20 horas (`RN-14`). Modela las llamadas entre el Estudiante Mentor, `CertificateView.tsx`, `certificateService.ts`, `certificates.py`, `certificate_service.py`, el compilador PDF/QR y PostgreSQL. Incorpora el control de umbral con manejo de horas insuficientes (`E001`), la previsualización modal, la generación del documento oficial foliado con sello SHA-256 y código QR institucional, y la descarga binaria segura en formato PDF.

```plantuml
@startuml
title Diagrama 6.15.17: Diagrama de Secuencia - CUS-018: Emitir constancia oficial de horas de mentoría
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor
(UserRole.mentor)" as Mentor
participant "Vista React
(CertificateView.tsx)" as UI
participant "Adaptador Cliente
(certificateService.ts)" as Client
participant "Controlador FastAPI
(endpoints/certificates.py)" as API
participant "Servicio Backend
(certificate_service.py)" as Service
participant "Compilador PDF / QR
(ReportLab / QREngine)" as PDF
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta de acumulado de horas y verificación de umbral ==
Mentor -> UI: 1. Accede a "Mis Certificados" en CertificateView.tsx
activate UI
UI -> Client: getHoursSummary() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/certificates/summary
activate API
API -> Service: calculate_accredited_hours(mentor_id)
activate Service
Service -> DB: SELECT sum(s.duracion_minutos)/60.0 as horas_totales FROM sesiones_mentoria s
JOIN bitacoras_pedagogicas b ON s.id = b.sesion_id
WHERE s.id_mentor = :mid AND s.estado = 'BITACORA_REGISTRADA'
activate DB
DB --> Service: Total de horas pedagógicas acumuladas
deactivate DB

alt [E001] Horas acreditadas insuficientes para el umbral institucional (horas_totales < 20.0, RN-14)
    Service --> API: Lanza HTTPException(400, "INSUFFICIENT_HOURS")
    API --> Client: HTTP 400 Bad Request {"detail": "INSUFFICIENT_HOURS: Requiere al menos 20 horas (Actual: Xh)."}
    Client --> UI: Captura error 400
    UI --> Mentor: Barra de progreso porcentual (< 100%), botón de emisión inhabilitado, panel ámbar con horas faltantes y botón [Ver Sesiones Pendientes]
    Mentor -> UI: Clic en [Ver Sesiones Pendientes]
    UI --> Mentor: Redirige a vista de sesiones para completar bitácoras y retorna al paso 1
else Umbral alcanzado (horas_totales >= 20.0)
    Service --> API: HoursSummaryDTO {"horas_totales": horas, "eligible": true}
    API --> Client: HTTP 200 OK HoursSummaryDTO
    Client --> UI: Entrega resumen acreditado
    UI --> Mentor: 2. Barra de progreso al 100% en color azul institucional y habilita botón "Emitir Constancia Oficial"
end
deactivate Service
deactivate API
deactivate Client
deactivate UI

== Fase 2: Solicitud de emisión y previsualización de datos ==
Mentor -> UI: 3. Presiona botón "Emitir Constancia Oficial"
activate UI
UI --> Mentor: 4. Despliega modal de previsualización: nombres completos, código universitario, semestre, horas y preview del QR
Mentor -> UI: Verifica sus datos y presiona "Confirmar y Generar PDF Cifrado"

== Fase 3: Generación criptográfica, persistencia y descarga del PDF ==
Mentor -> UI: 5. Observa animación de compilación segura del documento
UI -> Client: generateCertificate(semester="2026-I")
activate Client
Client -> API: POST /api/v1/certificates/generate {"semester": "2026-I"} [Bearer JWT]
activate API
API -> Service: generate_certificate(mentor_id, semester)
activate Service

Service -> Service: Genera serie alfanumérica única (UPT-EPIS-2026-I-0042)
Service -> Service: Calcula hash SHA-256 de los datos curriculares
Service -> PDF: render_certificate_pdf(datos, firma_director, codigo_qr)
activate PDF
PDF --> Service: Documento PDF binario oficial compilado
deactivate PDF

Service -> DB: BEGIN TRANSACTION
activate DB
Service -> DB: INSERT INTO certificados_horas (mentor_id, semestre, total_horas, codigo_serie, hash_integridad, url_archivo, fecha_emision)
VALUES (:mid, :sem, :horas, :serie, :hash, :url, NOW()) RETURNING id
Service -> DB: COMMIT
DB --> Service: Certificado persistido
deactivate DB

Service --> API: CertificateResponseDTO {"id": id_cert, "codigo_serie": serie, "url_descarga": url}
deactivate Service
API --> Client: HTTP 201 Created CertificateResponseDTO
deactivate API
Client --> UI: Emisión confirmada
deactivate Client

UI --> Mentor: 6. Renderiza vista previa oficial y habilita botón de descarga directa en formato PDF

Mentor -> UI: 7. Clic en "Descargar Constancia en PDF"
UI -> Client: downloadCertificate(id_cert)
activate Client
Client -> API: GET /api/v1/certificates/{id}/download [Bearer JWT]
activate API
API -> Service: get_certificate_download(id_cert)
activate Service
Service -> DB: SELECT url_archivo FROM certificados_horas WHERE id = :id_cert
activate DB
DB --> Service: Metadata del archivo persistido
deactivate DB
Service --> API: Archivo binario (application/pdf)
deactivate Service
API --> Client: HTTP 200 OK (Stream PDF)
deactivate API
Client --> UI: Entrega stream de bytes
deactivate Client
UI --> Mentor: 8. Descarga automática del archivo "Constancia_Horas_UPT.pdf"
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-018.

---

#### Diagrama 6.15.18: Diagrama de Secuencia - CUS-019: Gestionar insignias y reputación gamificada

El diagrama de secuencia para `CUS-019` describe el cálculo de la reputación institucional gamificada y la consulta interactiva de insignias de honor alcanzadas por los mentores. Modela la interacción entre el Estudiante Mentor, el Estudiante Mentoreado, `GamificationView.tsx`, `gamificationService.ts`, `gamification.py`, `reputation_service.py` y PostgreSQL. Abarca la consulta de la vitrina virtual de insignias (conquistadas y bloqueadas), la inspección lateral de requisitos de logro y el despliegue del Cuadro de Honor (Leaderboard) con soporte de visualización anónima para privacidad (`A001`).

```plantuml
@startuml
title Diagrama 6.15.18: Diagrama de Secuencia - CUS-019: Gestionar insignias y reputación gamificada
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor / Alumno" as User
participant "Vista React
(GamificationView.tsx)" as UI
participant "Adaptador Cliente
(gamificationService.ts)" as Client
participant "Controlador FastAPI
(endpoints/gamification.py)" as API
participant "Servicio Backend
(reputation_service.py)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta de insignias personales y progreso de nivel ==
User -> UI: 1. Clic en enlace "Insignias y Reputación"
activate UI
UI -> Client: getUserBadges() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/gamification/badges
activate API
API -> Service: get_user_badges(user_id)
activate Service
Service -> DB: SELECT b.*, ub.fecha_obtencion, ub.progreso FROM insignias b
LEFT JOIN insignias_usuarios ub ON b.id = ub.insignia_id AND ub.usuario_id = :uid
activate DB
DB --> Service: Catálogo de insignias y estado de avance
deactivate DB
Service --> API: BadgeListResponseDTO
deactivate Service
API --> Client: HTTP 200 OK BadgeListResponseDTO
deactivate API
Client --> UI: Entrega catálogo de insignias
deactivate Client
UI --> User: 2. Renderiza vitrina virtual: insignias desbloqueadas en color dorado con fecha, y bloqueadas en color gris con barra de porcentaje completado
deactivate UI

== Fase 2: Exploración de criterios de logro y detalle de insignia ==
User -> UI: 3. Hace clic sobre una insignia específica (ej. "Mentor Destacado")
activate UI
UI --> User: 4. Despliega panel lateral interactivo con nombre, descripción pedagógica, icono gráfico y requisitos de desbloqueo (>= 10 sesiones con >= 4.8 estrellas)
deactivate UI

== Fase 3: Visualización del cuadro de honor institucional (Leaderboard) ==
User -> UI: 5. Hace clic en la pestaña "Cuadro de Honor de la Escuela"
activate UI
UI -> Client: getLeaderboard() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/gamification/leaderboard
activate API
API -> Service: calculate_rank()
activate Service
Service -> DB: SELECT u.id, u.nombres, u.apellidos, u.codigo_estudiante, r.score_global, r.modo_anonimo
FROM reputacion_usuarios r JOIN usuarios u ON r.usuario_id = u.id ORDER BY r.score_global DESC LIMIT 10
activate DB
DB --> Service: Top-10 mentores ordenados por reputación RN-13
deactivate DB

alt [A001] Visualización en el cuadro de honor con alias anónimo (modo_anonimo = true)
    Service -> Service: Anonimiza nombres oficiales reemplazándolos por seudónimo (ej. "Mentor EPIS-742")
    Service --> API: LeaderboardResponseDTO (con registros anonimizados)
    API --> Client: HTTP 200 OK
    Client --> UI: Entrega ranking anonimizado
    UI --> User: A001-1.3 Visualiza puntaje con seudónimo garantizando confidencialidad y muestra interruptor de visibilidad
else Perfil público estándar
    Service --> API: LeaderboardResponseDTO (nombres públicos)
    API --> Client: HTTP 200 OK LeaderboardResponseDTO
    Client --> UI: Entrega tabla clasificatoria
    UI --> User: 6. Renderiza tabla clasificatoria destacando los 3 primeros lugares con medallas de honor, e indicando la posición del usuario en el ranking con marco azul institucional
end
deactivate Service
deactivate API
deactivate Client
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-019.


---

### MOD-08: Analítica, Notificaciones y Configuración

#### Diagrama 6.15.19: Diagrama de Secuencia - CUS-009: Notificar eventos críticos y alertas temporales

El diagrama de secuencia para `CUS-009` formaliza el despacho multicanal de notificaciones reactivas (Server-Sent Events y correo electrónico SMTP) ante eventos críticos del ciclo de vida de las mentorías. Modela la interacción entre el Planificador desatendido (`SchedulerWorker`), los usuarios institucionales, el componente `NotificationBell.tsx`, `notificationService.ts`, `notifications.py`, `notification_service.py`, `EmailService` y PostgreSQL. Modela la inicialización del flujo SSE, la persistencia de alertas, la degradación controlada ante fallos del servidor SMTP (`E001`) y la lectura interactiva de notificaciones.

```plantuml
@startuml
title Diagrama 6.15.19: Diagrama de Secuencia - CUS-009: Notificar eventos críticos y alertas de confirmación a T-24h
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

participant "Planificador
(SchedulerWorker / Celery)" as Cron
actor "Usuario Institucional
(Mentor / Alumno)" as User
participant "Vista React
(NotificationBell.tsx)" as UI
participant "Adaptador Cliente
(notificationService.ts)" as Client
participant "Controlador FastAPI
(endpoints/notifications.py)" as API
participant "Servicio Backend
(notification_service.py)" as Service
participant "Servicio SMTP UPT
(EmailService)" as SMTP
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Conexión al canal de notificaciones e inicialización de alertas ==
User -> UI: 1. Inicia sesión en la plataforma y visualiza componente de campana
activate UI
UI -> Client: subscribeNotifications() & getUnread() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/notifications/stream (SSE)
activate API
Client -> API: GET /api/v1/notifications/unread
API -> Service: get_unread(user_id)
activate Service
Service -> DB: SELECT * FROM notificaciones_eventos WHERE usuario_id = :uid AND leida = false ORDER BY fecha_creacion DESC
activate DB
DB --> Service: Nómina de alertas no leídas
deactivate DB
Service --> API: UnreadNotificationsDTO
deactivate Service
API --> Client: HTTP 200 OK UnreadNotificationsDTO
Client --> UI: Actualiza contador de alertas
UI --> User: 2. Renderiza insignia numérica roja sobre la campana con el total de alertas pendientes

== Fase 2: Generación asíncrona de evento crítico y despacho multicanal ==
Cron -> Service: 3. Dispara evento de dominio (ej. evaluación de quórum a T-24h en CUS-023)
activate Service
Service -> Service: dispatch_event(user_id, event_type, message, reference_id)
Service -> DB: INSERT INTO notificaciones_eventos (usuario_id, tipo_evento, mensaje, referencia_id, leida=false, fecha_creacion=NOW())
VALUES (...) RETURNING id
activate DB
DB --> Service: Alerta persistida
deactivate DB

Service -> API: push_sse_event(user_id, notification_data)
API --> Client: SSE Stream Event: "critical_alert" {mensaje, id}
Client --> UI: Recepción reactiva instantánea
UI --> User: Incrementa contador numérico y parpadea en color ámbar

alt [E001] Falla de despacho en servicio SMTP institucional de respaldo
    Service -> SMTP: send_alert_email(email, subject, message)
    activate SMTP
    SMTP --> Service: SMTPException / Conexión rechazada
    deactivate SMTP
    Service -> Service: logger.warning("SMTP dispatch failed, falling back to SSE only")
    Service --> API: Evento despachado (degradación controlada, entrega vía web preservada)
else Despacho SMTP exitoso
    Service -> SMTP: send_alert_email(email, subject, message)
    activate SMTP
    SMTP --> User: Aviso institucional en buzón universitario @upt.pe
    deactivate SMTP
    Service --> API: Multichannel Dispatch OK
end
deactivate Service

== Fase 3: Recepción reactiva en cliente y lectura de notificación ==
User -> UI: 5. Observa actualización en campana y hace clic sobre el icono
UI --> User: 6. Despliega panel flotante con alertas ordenadas cronológicamente (Informativa, Alerta T-24h, Urgente)
User -> UI: Hace clic sobre una alerta específica (ej. "Sesión de mañana confirmada")
UI -> Client: markAsRead(notificationId)
Client -> API: POST /api/v1/notifications/{id}/mark-read [Bearer JWT]
API -> Service: mark_notification_as_read(notificationId, user_id)
activate Service
Service -> DB: UPDATE notificaciones_eventos SET leida = true WHERE id = :id
activate DB
DB --> Service: Confirmación de actualización
deactivate DB
Service --> API: NotificationMarkReadResponseDTO {"success": true}
deactivate Service
API --> Client: HTTP 200 OK
Client --> UI: Notificación leída
UI -> UI: Disminuye contador numérico
UI --> User: Redirige a la vista de la sesión referenciada
deactivate Client
deactivate API
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-009.

---

#### Diagrama 6.15.20: Diagrama de Secuencia - CUS-011: Generar reportes e indicadores analíticos

El diagrama de secuencia para `CUS-011` especifica la agregación analítica de indicadores de mentoría y la exportación de dossiers ejecutivos para la Dirección de Escuela y comités de calidad ICACIT. Modela la interacción entre el Administrador, `AnalyticsDashboardView.tsx`, `analyticsService.ts`, `analytics.py`, `analytics_service.py`, el compilador de hojas de cálculo y PostgreSQL. Describe la consulta de métricas generales, la validación de intervalos temporales con rechazo de fechas inconsistentes (`E001`), y la serialización y descarga del informe binario consolidado (`.xlsx` o `.csv`).

```plantuml
@startuml
title Diagrama 6.15.20: Diagrama de Secuencia - CUS-011: Generar reportes consolidados e indicadores analíticos de gestión
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Administrador / Calidad ICACIT" as Admin
participant "Vista React
(AnalyticsDashboardView.tsx)" as UI
participant "Adaptador Cliente
(analyticsService.ts)" as Client
participant "Controlador FastAPI
(endpoints/analytics.py)" as API
participant "Servicio Backend
(analytics_service.py)" as Service
participant "Generador de Hojas de Cálculo
(Excel / OpenPyXL Engine)" as Excel
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Acceso al panel analítico y configuración de parámetros ==
Admin -> UI: 1. Accede al panel de reportes analíticos
activate UI
UI -> Client: getKpiSummary(semester="2026-I") [Bearer JWT]
activate Client
Client -> API: GET /api/v1/analytics/reports/kpis?semester=2026-I
activate API
API -> Service: calculate_kpis(semester="2026-I")
activate Service
Service -> DB: SELECT count(s.id) as total_sesiones, sum(s.duracion_minutos)/60.0 as total_horas,
       avg(CASE WHEN s.estado = 'CONFIRMADA' THEN 1 ELSE 0 END)*100 as tasa_quorum,
       avg(CASE WHEN a.asistio = true THEN 1 ELSE 0 END)*100 as tasa_asistencia
FROM sesiones_mentoria s LEFT JOIN asistencias_sesion a ON s.id = a.sesion_id WHERE s.semestre = '2026-I'
activate DB
DB --> Service: Métricas agregadas
deactivate DB
Service --> API: KpiSummaryDTO
deactivate Service
API --> Client: HTTP 200 OK KpiSummaryDTO
deactivate API
Client --> UI: Entrega métricas agregadas
deactivate Client
UI --> Admin: 2. Renderiza tarjetas de indicadores clave y gráficos comparativos de barras en color azul institucional

== Fase 2: Ajuste de filtros temporales y selección de formato de exportación ==
Admin -> UI: 3. Ajusta rango de fechas (inicio y fin), elige asignatura filtro y selecciona formato (Excel .xlsx / CSV)
UI -> UI: Valida consistencia de fechas (inicio <= fin y fechas no futuras)

alt [E001] Rango de fechas inconsistente o fechas futuras
    UI --> Admin: Resalta campos de fecha en rojo, alerta ámbar "El rango de fechas seleccionado es inconsistente o futuro"
    Admin -> UI: Modifica fechas seleccionando un período semestral válido
    UI --> Admin: Actualiza selector y retorna al paso 3
else Rango temporal válido
    Admin -> UI: Presiona botón "Exportar Informe Consolidado"
    UI -> Client: exportReport(format="xlsx", startDate, endDate, courseId)
    activate Client
    Client -> API: GET /api/v1/analytics/export?format=xlsx&start_date={start_date}&end_date={end_date}&course_id={course_id} [Bearer JWT]
    activate API
    API -> Service: export_report(format, start_date, end_date, course_id)
    activate Service
    
    == Fase 3: Generación del documento analítico y descarga segura ==
    Admin -> UI: 5. Observa indicador circular de compilación en botón de exportación
    
    Service -> DB: SELECT * FROM sesiones_mentoria s JOIN bitacoras_pedagogicas b ON s.id = b.sesion_id...
    activate DB
    DB --> Service: Registros consolidados
    deactivate DB
    
    Service -> Excel: compile_workbook(resumen_kpi, sesiones, asistencias, materias_criticas)
    activate Excel
    Excel --> Service: StreamBinarioXLSX (Libro con 4 pestañas estructuradas)
    deactivate Excel
    
    Service -> DB: INSERT INTO auditoria_admin (admin_id, accion='EXPORT_REPORT', entidad='analytics', fecha=NOW())
    
    Service --> API: StreamingResponse(content=stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=Reporte_Mentorias_EPIS.xlsx"})
    deactivate Service
    API --> Client: HTTP 200 OK (Stream Binario XLSX)
    deactivate API
    Client --> UI: Flujo binario entregado
    deactivate Client
    
    UI --> Admin: 6. El navegador inicia la descarga automática del archivo "Reporte_Mentorias_EPIS.xlsx"
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-011.

---

#### Diagrama 6.15.21: Diagrama de Secuencia - CUS-015: Consultar métricas de retención y desempeño

El diagrama de secuencia para `CUS-015` formaliza la inferencia estadística del impacto del programa de mentorías en la retención estudiantil y disminución de reprobación en asignaturas filtro, respaldando los criterios de mejora continua de ICACIT. Modela las llamadas entre la Comisión de Calidad, `RetentionDashboardView.tsx`, `analyticsService.ts`, `analytics.py`, `analytics_service.py` y PostgreSQL. Modela la comparación entre grupos de control y participantes, la verificación de tamaño muestral mínimo (`A001`), y la generación y exportación del expediente probatorio en formato PDF oficial.

```plantuml
@startuml
title Diagrama 6.15.21: Diagrama de Secuencia - CUS-015: Consultar métricas de correlación de retención estudiantil y desempeño
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Comisión de Calidad ICACIT / Admin" as Evaluador
participant "Vista React
(RetentionDashboardView.tsx)" as UI
participant "Adaptador Cliente
(analyticsService.ts)" as Client
participant "Controlador FastAPI
(endpoints/analytics.py)" as API
participant "Servicio Backend
(analytics_service.py)" as Service
participant "Compilador PDF ICACIT
(ReportEngine)" as PDF
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Acceso al módulo de impacto y selección de cohorte ==
Evaluador -> UI: 1. Accede a "Impacto y Retención Académica"
activate UI
UI -> Client: getRetentionMetrics() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/analytics/retention/impact
activate API
API -> Service: analyze_retention_correlation()
activate Service
Service -> DB: SELECT count(DISTINCT estudiante_id) as total_alumnos,
       avg(CASE WHEN asistencia_count >= 3 THEN tasa_aprobacion ELSE NULL END) as aprobacion_mentoreados,
       avg(CASE WHEN asistencia_count = 0 THEN tasa_aprobacion ELSE NULL END) as aprobacion_control
FROM cohortes_academicas
activate DB
DB --> Service: Comparativa estadística de cohortes
deactivate DB
Service --> API: RetentionImpactDTO
deactivate Service
API --> Client: HTTP 200 OK RetentionImpactDTO
deactivate API
Client --> UI: Entrega métricas de retención
deactivate Client
UI --> Evaluador: 2. Renderiza gráfico comparativo de barras dobles y estimación de reducción de reprobación en azul institucional

== Fase 2: Segmentación por asignatura filtro y período lectivo ==
Evaluador -> UI: 3. Selecciona asignatura filtro (ej. Estructuras de Datos) y pulsa "Calcular Índice de Impacto"
UI -> Client: getCourseRetentionImpact(courseId)
activate Client
Client -> API: GET /api/v1/analytics/retention/cohorts?course_id={course_id}
activate API
API -> Service: get_course_cohort_stats(course_id)
activate Service
Service -> DB: SELECT count(*) as n_muestra, corr(asistencias, nota_final) as r_pearson
FROM actas_semestrales a JOIN asistencias_sesion s ON a.estudiante_id = s.estudiante_id
WHERE a.curso_id = :cid
activate DB
DB --> Service: Muestra y correlación calculada
deactivate DB

alt [A001] Muestra insuficiente para inferencia estadística (< 10 registros)
    Service --> API: RetentionCohortDTO {"n_muestra": n, "significancia": false, "solo_descriptivo": true}
    API --> Client: HTTP 200 OK
    Client --> UI: Datos descriptivos básicos
    UI --> Evaluador: A001-1.2 Panel ámbar "Muestra preliminar insuficiente (< 10 registros). Se presentan sólo métricas descriptivas"
    UI --> Evaluador: A001-1.4 Ofrece ampliar rango a semestres anteriores y retorna al paso 3
else Tamaño muestral suficiente (>= 10 registros)
    Service --> API: RetentionCohortDTO {"n_muestra": n, "significancia": true, "r_pearson": r}
    API --> Client: HTTP 200 OK RetentionCohortDTO
    Client --> UI: Entrega resultados estadísticos
    UI --> Evaluador: 4. Despliega correlación de Pearson y gráficos de dispersión
end
deactivate Service
deactivate API
deactivate Client

== Fase 3: Visualización de indicadores ICACIT y exportación ==
Evaluador -> UI: 5. Revisa indicadores de logro y presiona "Exportar Evidencia ICACIT"
UI -> Client: exportIcacitEvidence(courseId)
activate Client
Client -> API: POST /api/v1/analytics/retention/export-evidence {"course_id": cid} [Bearer JWT]
activate API
API -> Service: generate_icacit_report(course_id)
activate Service
Service -> PDF: compile_icacit_dossier(datos_retencion, tablas_frecuencia, firmas_integridad)
activate PDF
PDF --> Service: Documento PDF formal de acreditación
deactivate PDF
Service --> API: StreamingResponse(content=pdf_stream, media_type="application/pdf")
deactivate Service
API --> Client: HTTP 200 OK (Stream Binario PDF)
deactivate API
Client --> UI: Flujo PDF entregado
deactivate Client
UI --> Evaluador: 6. Descarga directa del expediente probatorio en formato PDF oficial para acreditación
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-015.

---

#### Diagrama 6.15.22: Diagrama de Secuencia - CUS-016: Auditar trazas de seguridad y consentimiento

El diagrama de secuencia para `CUS-016` modela la auditoría forense inmutable y la verificación de integridad de la cadena criptográfica de logs (Hash Chain) bajo los mandatos de la Ley Nº 29733 y el estándar ISO/IEC 27001. Desglosa los participantes: Oficial de Seguridad, `AuditLogView.tsx`, `auditService.ts`, `audit.py`, `audit_service.py` y PostgreSQL. Especifica la restricción RBAC (`E001`), la verificación de trazas de consentimiento, el cálculo iterativo recursivo `SHA256(prev_hash + data)` con detección de manipulaciones (`E002`), y la acreditación de integridad con 0 alteraciones.

```plantuml
@startuml
title Diagrama 6.15.22: Diagrama de Secuencia - CUS-016: Auditar trazas inmutables de seguridad y consentimientos legales
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Oficial de Seguridad / Delegado DPO
(UserRole.administrador)" as SecOfficer
participant "Vista React
(AuditLogView.tsx)" as UI
participant "Adaptador Cliente
(auditService.ts / ApiAuditAdapter)" as Client
participant "Controlador FastAPI
(endpoints/audit.py)" as API
participant "Servicio Backend
(audit_service.py / AuditService)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta del registro forense de auditoría ==
SecOfficer -> UI: 1. Accede a "Auditoría de Seguridad y Ley 29733"
activate UI
UI -> Client: getAuditLogs(limit=50) [Bearer JWT]
activate Client
Client -> API: GET /api/v1/audit/logs?limit=50
activate API

API -> API: require_security_officer_role(current_user)

alt [E001] Permisos insuficientes para auditoría de seguridad
    API --> Client: HTTP 403 Forbidden {"detail": "FORBIDDEN_AUDIT: Acceso reservado a Oficial de Seguridad."}
    Client --> UI: Captura error 403
    UI --> SecOfficer: Redirige a panel estándar con alerta roja "Acceso Restringido" y botón [Aceptar]
    SecOfficer -> UI: Clic en [Aceptar]
    UI --> SecOfficer: Cierra aviso y retorna al paso 1 en vista autorizada
else Privilegios de seguridad verificados
    API -> Service: get_logs(limit=50)
    activate Service
    Service -> DB: SELECT l.*, u.email FROM log_auditoria_seguridad l
JOIN usuarios u ON l.usuario_id = u.id ORDER BY l.id DESC LIMIT 50
    activate DB
    DB --> Service: Trazas de auditoría forense
    deactivate DB
    Service --> API: AuditLogListResponseDTO
    deactivate Service
    API --> Client: HTTP 200 OK AuditLogListResponseDTO
    Client --> UI: Entrega trazas de seguridad
    UI --> SecOfficer: 2. Renderiza tabla forense con filtros por fecha, evento (AUTH_2FA, ROLE_CHANGE, CONSENT_ACCEPT), IP y hash de bloque
end
deactivate API
deactivate Client

== Fase 2: Filtrado por usuario y verificación de traza legal de consentimiento ==
SecOfficer -> UI: 3. Introduce correo en buscador para auditar historial de consentimiento
UI -> Client: getConsentTraces(email)
activate Client
Client -> API: GET /api/v1/audit/consent-traces?email={email} [Bearer JWT]
activate API
API -> Service: get_consent_traces(email)
activate Service
Service -> DB: SELECT * FROM consentimientos_legales WHERE email = :email ORDER BY fecha_registro ASC
activate DB
DB --> Service: Trazas de formalización (UUID, versión, IP, User-Agent, UTC, revocado)
deactivate DB
Service --> API: ConsentTraceListDTO
deactivate Service
API --> Client: HTTP 200 OK ConsentTraceListDTO
deactivate API
Client --> UI: Entrega expediente digital
deactivate Client
UI --> SecOfficer: 4. Despliega expediente digital del titular conforme a la Ley N° 29733

== Fase 3: Verificación criptográfica de la cadena de auditoría (Hash Chain) ==
SecOfficer -> UI: 5. Presiona botón "Verificar Integridad de Cadena de Logs"
UI -> Client: verifyLogChain()
activate Client
Client -> API: POST /api/v1/audit/verify-chain [Bearer JWT]
activate API
API -> Service: verify_chain_integrity()
activate Service

Service -> DB: SELECT id, hash_bloque, hash_anterior, datos_evento FROM log_auditoria_seguridad ORDER BY id ASC
activate DB
DB --> Service: Todos los registros de auditoría
deactivate DB

Service -> Service: Itera recursivamente recomputando SHA256(hash_anterior + datos_evento)

alt [E002] Inconsistencia detectada en la cadena criptográfica de logs (discrepancia de hash)
    Service --> API: Lanza HTTPException(409, "AUDIT_TAMPERING_DETECTED: Discrepancia en ID {broken_id}")
    API --> Client: HTTP 409 Conflict {"detail": "AUDIT_TAMPERING_DETECTED"}
    Client --> UI: Captura error 409
    UI --> SecOfficer: Alarma roja parpadeante, resalta fila alterada y botón [Descargar Informe Forense]
    SecOfficer -> UI: Clic en [Descargar Informe Forense]
    UI --> SecOfficer: Emite volcado forense para autoridades y finaliza caso de uso
else Cadena 100% íntegra (0 discrepancias)
    Service --> API: VerifyChainResponseDTO {"status": "VALID", "records_verified": count, "tampering_detected": false}
    API --> Client: HTTP 200 OK VerifyChainResponseDTO
    Client --> UI: Integridad ratificada
    UI --> SecOfficer: 6. Despliega insignia destacada verde "Cadena de Auditoría Íntegra y Verificada (0 Alteraciones)" y habilita exportación legal
end
deactivate Service
deactivate API
deactivate Client
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-016.

---

#### Diagrama 6.15.23: Diagrama de Secuencia - CUS-020: Configurar parámetros institucionales y umbrales

El diagrama de secuencia para `CUS-020` describe la calibración dinámica de reglas institucionales y umbrales operacionales sin modificación del código fuente. Modela las llamadas entre el Administrador Institucional, `SystemSettingsView.tsx`, `configService.ts`, `config.py`, `config_service.py` y PostgreSQL. Modela la consulta de parámetros vigentes, la validación de límites operacionales (`E001`), la exigencia de reautenticación para cambios críticos (`E002`), y la persistencia transaccional con purga inmediata de la memoria caché para aplicación en caliente.

```plantuml
@startuml
title Diagrama 6.15.23: Diagrama de Secuencia - CUS-020: Configurar parámetros operativos institucionales y umbrales
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Administrador Institucional
(UserRole.administrador)" as Admin
participant "Vista React
(SystemSettingsView.tsx)" as UI
participant "Adaptador Cliente
(configService.ts)" as Client
participant "Controlador FastAPI
(endpoints/config.py)" as API
participant "Servicio Backend
(config_service.py)" as Service
participant "Caché de Aplicación
(Redis / MemoryCache)" as Cache
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta de parámetros vigentes y despliegue del panel ==
Admin -> UI: 1. Accede a "Configuración del Sistema" en SystemSettingsView.tsx
activate UI
UI -> Client: getParameters() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/config/parameters
activate API
API -> Service: get_parameters()
activate Service
Service -> DB: SELECT clave, valor, descripcion, valor_min, valor_max FROM parametros_institucionales WHERE activo = true
activate DB
DB --> Service: Catálogo de parámetros base
deactivate DB
Service --> API: ParameterListResponseDTO
deactivate Service
API --> Client: HTTP 200 OK ParameterListResponseDTO
deactivate API
Client --> UI: Entrega parámetros institucionales
deactivate Client
UI --> Admin: 2. Renderiza formulario por categorías: 1) Aforos (Presencial 10, Virtual 20), 2) Antelación (24h), 3) Quórum Mínimo (3), 4) Horas Certificación (20h)

== Fase 2: Edición de umbrales y validación de rangos permitidos ==
Admin -> UI: 3. Modifica valores numéricos (ej. ajusta quórum mínimo a 4) y presiona "Guardar Parámetros Institucionales"
UI -> UI: Valida en cliente que valor_min <= valor <= valor_max

alt [E001] Parámetro fuera de los rangos institucionales permitidos
    UI --> Admin: Resalta campo en rojo, alerta de error indicando rango admisible
    Admin -> UI: Corrige valor ingresando número dentro del rango permitido
    UI --> Admin: Rehabilita botón de guardado y retorna al paso 3
else Valores en rangos admisibles
    UI -> Client: updateParameters(payload)
    activate Client
    Client -> API: PUT /api/v1/config/parameters ParameterUpdatePayload [Bearer JWT]
    activate API
    
    alt [E002] Reautenticación de seguridad requerida (cambios críticos sin contraseña secundaria)
        API --> Client: HTTP 401 Unauthorized {"detail": "REAUTH_REQUIRED: Confirmación de credenciales requerida."}
        Client --> UI: Captura error 401
        UI --> Admin: Abre modal de reautenticación solicitando contraseña o código OTP secundario
        Admin -> UI: Ingresa contraseña institucional y presiona "Verificar"
        UI -> Client: reauthenticateAdmin(credentials)
        Client -> API: POST /api/v1/auth/reauth
        API --> Client: HTTP 200 OK {"reauth_token": token}
        Client --> UI: Reautenticación exitosa
        UI --> Admin: Retorna al paso 4 con token de reautenticación
    else Autorización confirmada
        API -> Service: update_parameters(admin_id, payload)
        activate Service
        
        == Fase 3: Persistencia transaccional, purga de caché y aplicación en caliente ==
        Admin -> UI: 5. Observa indicador circular de guardado seguro
        
        Service -> DB: BEGIN TRANSACTION
        activate DB
        Service -> DB: UPDATE parametros_institucionales SET valor = :val, fecha_modificacion = NOW(), modificado_por = :uid WHERE clave = :key
        Service -> DB: INSERT INTO log_auditoria_seguridad (usuario_id, evento='PARAM_UPDATE', detalle=:key, fecha=NOW())
        Service -> DB: COMMIT
        DB --> Service: Transacción confirmada
        deactivate DB
        
        Service -> Cache: purge_system_config_cache()
        activate Cache
        Cache --> Service: Caché invalidada en caliente
        deactivate Cache
        
        Service --> API: ParameterUpdateResponseDTO {"success": true, "updated_keys": keys}
        deactivate Service
        API --> Client: HTTP 200 OK ParameterUpdateResponseDTO
        Client --> UI: Confirmación de actualización
        
        UI --> Admin: 6. Notificación flotante verde de éxito: "Parámetros institucionales actualizados y aplicados en caliente exitosamente"
    end
    deactivate API
    deactivate Client
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-020.

---

#### Diagrama 6.15.24: Diagrama de Secuencia - CUS-022: Gestionar catálogo de temas y materias críticas

El diagrama de secuencia para `CUS-022` formaliza la actualización de la malla curricular y el catálogo silábico de materias críticas por parte de la Dirección de Escuela y administradores. Modela las llamadas entre el Administrador, `AdminCurriculumView.tsx`, `curriculumService.ts`, `curriculum.py`, `curriculum_service.py` y PostgreSQL. Describe la navegación por el árbol curricular, el alta de nuevos temas silábicos con validación de unicidad (`E001`) y rango semestral de semanas 1 a 17 (`E002`), y la confirmación transaccional con actualización reactiva en la interfaz administrativa.

```plantuml
@startuml
title Diagrama 6.15.24: Diagrama de Secuencia - CUS-022: Gestionar catálogo de temas curriculares, asignaturas filtro y malla oficial
Sistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Administrador Institucional
(UserRole.administrador)" as Admin
participant "Vista React
(AdminCurriculumView.tsx)" as UI
participant "Adaptador Cliente
(curriculumService.ts)" as Client
participant "Controlador FastAPI
(endpoints/curriculum.py)" as API
participant "Servicio Backend
(curriculum_service.py)" as Service
database "PostgreSQL DB
(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta del árbol curricular y selección de asignatura ==
Admin -> UI: 1. Accede a "Gestión de Malla y Temarios" en AdminCurriculumView.tsx
activate UI
UI -> Client: getCoursesFullTree() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/curriculum/courses
activate API
API -> Service: get_courses_tree()
activate Service
Service -> DB: SELECT * FROM cursos ORDER BY ciclo, nombre
activate DB
DB --> Service: Malla curricular ordenada por ciclo
deactivate DB
Service --> API: CourseTreeResponseDTO
deactivate Service
API --> Client: HTTP 200 OK CourseTreeResponseDTO
deactivate API
Client --> UI: Entrega árbol curricular
deactivate Client
UI --> Admin: 2. Renderiza vista en árbol con materias clasificadas por ciclo y etiqueta "Materia Filtro" en aquellas con es_filtro=true. Clic en asignatura para ver temas.

== Fase 2: Ingreso de datos del nuevo tema curricular silábico ==
Admin -> UI: 3. Presiona botón "Agregar Nuevo Tema Curricular" en panel de asignatura
UI --> Admin: 4. Abre modal: unidad (1-4), título descriptivo, semana académica (1-17) y descripción conceptual
Admin -> UI: Completa campos y pulsa "Registrar Tema Curricular"
UI -> UI: Valida número de semana en cliente

alt [E002] Número de semana académica fuera de rango semestral (semana < 1 o > 17)
    UI --> Admin: Resalta campo numérico de semana en rojo: "La semana académica debe estar entre 1 y 17"
    Admin -> UI: Ingresa número de semana válido (1 a 17)
    UI --> Admin: Actualiza valor en formulario y retorna al paso 4
else Semana lectiva válida
    UI -> Client: createTopic(courseId, payload)
    activate Client
    Client -> API: POST /api/v1/curriculum/courses/{course_id}/topics TopicCreateRequest [Bearer JWT]
    activate API
    API -> Service: create_topic(course_id, payload)
    activate Service
    
    Service -> DB: SELECT id FROM temas_curriculares WHERE curso_id = :cid AND unidad = :u AND titulo = :t
    activate DB
    DB --> Service: Tema existente o nulo
    deactivate DB
    
    alt [E001] Tema curricular duplicado en la misma unidad didáctica
        Service --> API: Lanza HTTPException(409, "DUPLICATE_TOPIC")
        API --> Client: HTTP 409 Conflict {"detail": "DUPLICATE_TOPIC: Ya existe un tema con ese título en la unidad."}
        Client --> UI: Captura error 409
        UI --> Admin: Resalta título en rojo con mensaje de duplicidad
        Admin -> UI: Modifica título del tema especificando con mayor precisión
        UI --> Admin: Rehabilita botón de guardado en modal y retorna al paso 4
    else Tema nuevo y válido
        == Fase 3: Persistencia transaccional y actualización del catálogo ==
        Admin -> UI: 5. Observa indicador circular de guardado en modal
        
        Service -> DB: BEGIN TRANSACTION
        activate DB
        Service -> DB: INSERT INTO temas_curriculares (curso_id, unidad, semana, titulo, descripcion, activo=true)
VALUES (:cid, :u, :sem, :t, :desc, true) RETURNING id
        Service -> DB: COMMIT
        DB --> Service: Transacción confirmada (id_tema)
        deactivate DB
        
        Service --> API: TopicResponseDTO {"id": id_tema, "titulo": t, "semana": sem}
        API --> Client: HTTP 201 Created TopicResponseDTO
        Client --> UI: Tema curricular creado
        
        UI -> UI: Cierra cuadro de diálogo modal y añade nuevo tema al árbol curricular
        UI --> Admin: 6. Notificación flotante verde de éxito: "Tema curricular registrado y disponible para ofertas y demandas académicas"
    end
    deactivate Service
    deactivate API
    deactivate Client
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-022.


