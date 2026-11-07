# -*- coding: utf-8 -*-
"""
Diagramas de Secuencia - Módulo 01: Seguridad, Autenticación y Gobernanza (Fase de Diseño)
Contiene:
- CUS-001: Iniciar sesión institucional con 2FA y formalización de consentimiento digital
- CUS-010: Gestionar asignación y revocación de roles institucionales de usuario
"""

def get_mod01_seq():
    return """### MOD-01: Seguridad, Autenticación y Gobernanza

#### Diagrama 6.15.1: Diagrama de Secuencia - CUS-001: Iniciar sesión institucional con 2FA

El diagrama de secuencia para `CUS-001` formaliza la interacción temporal y el intercambio de mensajes entre el usuario universitario, la interfaz de autenticación React, el adaptador de cliente, los controladores FastAPI, el servicio de seguridad y correo institucional, y la base de datos relacional siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`), manteniéndola actualizada a la espera de las acciones directas del usuario. Modela con precisión exhaustiva las tres fases del Flujo Normal (solicitud de OTP, verificación de código temporal, y formalización de consentimiento bajo la Ley N° 29733 con emisión de JWT de 8 horas), los dos flujos alternativos (consentimiento previo `A001` y reenvío de OTP `A002`) y los seis flujos de excepción (`E001` a `E006`).

```plantuml
@startuml
title Diagrama 6.15.1: Diagrama de Secuencia - CUS-001: Iniciar sesión institucional con 2FA y formalización de consentimiento digital\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Usuario Institucional\\n(Estudiante / Mentor / Administrador)" as User
participant "Vista React\\n(LoginOtpView.tsx / ConsentModalView.tsx)" as UI
participant "Adaptador Cliente\\n(authService.ts / consentService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/auth.py / consent.py)" as API
participant "Servicio Backend\\n(auth_service.py / consent_service.py)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB
participant "Servicio SMTP UPT\\n(EmailService)" as SMTP

== Fase 1: Validación de identidad institucional y solicitud de OTP ==
User -> UI: enter (email: "usuario@upt.pe")
activate UI
User -> UI: click ["Continuar"]
UI -> Client: requestOtp(email)
activate Client
Client -> API: POST /api/v1/auth/otp/request {"email": email}
activate API

API -> API: Valida sintaxis con Pydantic (EmailStr) y comprueba email.endswith("@upt.pe")

alt [E001] Dominio de correo no termina en @upt.pe
    API --> Client: HTTP 400 Bad Request {"detail": "INVALID_DOMAIN: El acceso está reservado a @upt.pe."}
    Client -> UI: displayDomainError(400, "INVALID_DOMAIN: El acceso está reservado a @upt.pe.")
    User -> UI: click ["Corregir Correo"]
    UI -> UI: resetEmailField()
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
        Client -> UI: displayAccountSuspendedModal(403, "Cuenta inhabilitada por suspensión.")
        User -> UI: click ["Aceptar"]
        UI -> UI: resetForm()
    else Cuenta activa y habilitada
        Service --> API: Correo verificado y habilitado
        API --> Client: HTTP 200 OK {"status": "ELIGIBLE"}
        Client -> UI: displayOtpRequestForm(email, eligible=true)
    end
    deactivate Service
end
deactivate API
deactivate Client
deactivate UI

== Fase 2: Generación criptográfica, despacho SMTP y verificación de código temporal ==
User -> UI: click ["Solicitar Código de Acceso"]
activate UI
UI -> Client: requestOtp(email)
activate Client
Client -> API: POST /api/v1/auth/otp/request {"email": email}
activate API
API -> Service: generate_and_dispatch_otp(email)
activate Service

Service -> Service: Genera código seguro (secrets.randbelow(900000) + 100000)
Service -> Service: Calcula hash criptográfico SHA-256(otp_code)
Service -> DB: INSERT INTO credenciales_otp (id_usuario, hash_otp, expira_en=NOW()+5m)
activate DB
DB --> Service: Confirmación de persistencia (challenge_id)
deactivate DB

Service -> SMTP: send_otp_email(email, otp_plano)
activate SMTP
SMTP --> Service: Despacho SMTP exitoso (HTTP 200 / SMTP OK)
deactivate SMTP

Service --> API: OTP_SENT exitoso {"challenge_id": id, "expires_in": 300}
deactivate Service
API --> Client: HTTP 200 OK {"message": "OTP_SENT", "challengeId": id, "expires_in": 300}
deactivate API
Client -> UI: displayOtpModal(challengeId, expiresIn=300)
deactivate Client
deactivate UI

opt [A002] Reenvío de código temporal por retraso en buzón (> 60s) o caducidad
    User -> UI: click ["Reenviar código OTP"]
    activate UI
    UI -> Client: resendOtp(challengeId)
    activate Client
    Client -> API: POST /api/v1/auth/otp/resend {"challengeId": challengeId}
    activate API
    API -> Service: resend_otp(challenge_id)
    activate Service
    Service -> DB: UPDATE credenciales_otp SET consumido = true WHERE id = :challenge_id
    activate DB
    DB --> Service: Desafío previo invalidado
    deactivate DB
    Service -> Service: Genera nueva clave aleatoria de 6 dígitos
    Service -> SMTP: send_otp_email(email, nuevo_otp)
    activate SMTP
    SMTP --> Service: SMTP OK
    deactivate SMTP
    Service --> API: OTP_SENT
    deactivate Service
    API --> Client: HTTP 200 OK {"message": "OTP_SENT"}
    deactivate API
    Client -> UI: displayOtpResentAlert(expiresIn=300)
    deactivate Client
    deactivate UI
end

User -> UI: enter (otpCode: "123456")
activate UI
User -> UI: click ["Verificar e Ingresar"]
UI -> Client: verifyOtp(challengeId, otpCode)
activate Client
Client -> API: POST /api/v1/auth/otp/verify {"challengeId": challengeId, "otp": otpCode}
activate API
API -> Service: verify_otp(challenge_id, otpCode)
activate Service

Service -> DB: SELECT * FROM credenciales_otp WHERE id = :challenge_id AND consumido = false
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
    Client -> UI: displayOtpError(400, "INVALID_OTP: Código erróneo. Le quedan X intentos")
    User -> UI: click ["Reintentar"]
    UI -> UI: clearOtpInputs()
else [E004] Código temporal OTP expirado (NOW() > expira_en)
    Service --> API: Lanza HTTPException(400, "EXPIRED_OTP")
    API --> Client: HTTP 400 Bad Request {"detail": "EXPIRED_OTP: El código ha caducado por límite de 5 min."}
    Client -> UI: displayOtpExpiredAlert(400, "EXPIRED_OTP: Código caducado.")
    User -> UI: click ["Solicitar Nuevo Código"]
    UI -> UI: resetOtpForm()
else [E005] Bloqueo temporal por exceso de intentos (intentos_fallidos >= 3)
    Service -> DB: UPDATE usuarios SET bloqueado_hasta = NOW() + INTERVAL '15 MINUTES'
    activate DB
    DB --> Service: Usuario bloqueado
    deactivate DB
    Service --> API: Lanza HTTPException(429, "MAX_ATTEMPTS_EXCEEDED")
    API --> Client: HTTP 429 Too Many Requests {"detail": "MAX_ATTEMPTS_EXCEEDED: Acceso bloqueado por 15 minutos."}
    Client -> UI: displayBlockedSecurityModal(429, "Acceso bloqueado por 15 minutos.")
    User -> UI: click ["Volver al Inicio"]
    UI -> UI: redirectToInitialLogin()
else Código válido y vigente
    Service -> DB: UPDATE credenciales_otp SET consumido = true WHERE id = :challenge_id
    activate DB
    DB --> Service: Desafío invalidado
    deactivate DB
    Service --> API: OTP validado exitosamente {"temp_token": temp_token}
    deactivate Service
    API --> Client: HTTP 200 OK {"temp_token": temp_token}
    deactivate API
    Client -> UI: displayConsentOrProceed(temp_token)
    deactivate Client
    deactivate UI
end

== Fase 3: Formalización de consentimiento legal digital y emisión de sesión ==
UI -> Client: getConsentStatus(email)
activate UI
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
    Client -> UI: displaySessionDashboard(token, user)
    UI -> UI: localStorage.setItem('auth_token', token)
    UI --> User: displaySuccessSessionNotification
else Primer acceso sin consentimiento legal formalizado
    Service --> API: Requiere consentimiento {"requires_consent": true, "temp_token": temp_token}
    API --> Client: HTTP 200 OK {"requires_consent": true}
    Client -> UI: renderConsentModal(Ley 29733)
    
    alt [E006] Rechazo voluntario del consentimiento informado
        User -> UI: click ["Declinar y Salir"]
        UI -> UI: displayMandatoryConsentWarning()
        User -> UI: click ["Confirmar Salida"]
        UI -> UI: purgeSessionAndReset()
    else Aceptación de términos legales
        User -> UI: selectCheckbox ["He leído y acepto los términos..."]
        User -> UI: click ["Aceptar y Continuar"]
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
        Client -> UI: displaySessionDashboard(token, user)
        deactivate Client
        
        UI -> UI: localStorage.setItem('auth_token', token)
        UI -> UI: Actualiza estado global de autenticación en App.tsx
        UI --> User: displaySuccessSessionNotification
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

El diagrama de secuencia para `CUS-010` modela la gestión y administración de roles de usuario por parte de la Dirección de Escuela y administradores institucionales siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Desglosa los participantes en capas: Autoridad Administradora, `AdminDashboardView.tsx`, `roleService.ts`, `roles.py`, `role_service.py` y PostgreSQL. Abarca la consulta de nómina paginada, la búsqueda de usuarios (con flujo alternativo `A001`), la verificación de autorización RBAC (`E001`), la tolerancia a fallos de persistencia (`E002`), la prohibición de conjuntos de roles vacíos (`E003`) y la protección de gobernanza contra auto-revocación del rol Administrador (`E004`).

```plantuml
@startuml
title Diagrama 6.15.2: Diagrama de Secuencia - CUS-010: Gestionar asignación y revocación de roles institucionales de usuario\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Autoridad Institucional\\n(Administrador / Director EPIS)" as Admin
participant "Vista React\\n(AdminDashboardView.tsx)" as UI
participant "Adaptador Cliente\\n(roleService.ts / ApiRoleAdapter)" as Client
participant "Controlador FastAPI\\n(endpoints/roles.py)" as API
participant "Servicio Backend\\n(role_service.py / RoleService)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Acceso al panel administrativo y consulta de nómina de usuarios ==
Admin -> UI: click ["Gestión de Roles"]
activate UI
UI -> Client: listUsers() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/roles/users
activate API

API -> API: require_admin_role(current_user): valida JWT y claim roles conteniendo 'administrador'

alt [E001] Privilegios administrativos insuficientes (rol no administrador)
    API --> Client: HTTP 403 Forbidden {"detail": "FORBIDDEN: Se requieren privilegios de Administrador."}
    Client -> UI: displayAccessDenied(403, "Acceso Restringido")
    Admin -> UI: click ["Entendido"]
    UI -> UI: redirectToAuthorizedView()
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
    Client -> UI: displayServiceUnavailable(503)
    Admin -> UI: click ["Reintentar Carga"]
    UI -> Client: listUsers()
else Token válido y conexión activa
    API -> Service: list_users()
    activate Service
    Service -> DB: SELECT u.id, u.email, u.nombres, u.apellidos, array_agg(r.nombre) AS roles\\nFROM usuarios u LEFT JOIN roles_usuarios ru ON u.id = ru.id_usuario\\nLEFT JOIN roles r ON ru.id_rol = r.id GROUP BY u.id
    activate DB
    DB --> Service: Nómina de usuarios con roles asignados
    deactivate DB
    Service --> API: UserRoleListResponseDTO
    deactivate Service
    API --> Client: HTTP 200 OK UserRoleListResponseDTO
    Client -> UI: displayUserTable(users)
end
deactivate API
deactivate Client
deactivate UI

== Fase 2: Búsqueda y selección de usuario para modificación ==
Admin -> UI: enter (query: "2020-119001" o "estudiante@upt.pe")
activate UI
Admin -> UI: click ["Buscar"]
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
Client -> UI: displaySearchResults(results)
deactivate Client

alt [A001] Búsqueda sin coincidencias en el padrón institucional
    UI -> UI: displayNoResultsMessage()
    Admin -> UI: click ["Limpiar Búsqueda"]
    UI -> UI: resetSearchAndReload()
else Usuario localizado
    UI -> UI: highlightUserRow(targetUser)
    Admin -> UI: click ["Modificar Roles"]
    UI -> UI: openRoleAssignmentModal(targetUser, currentRoles)
end
deactivate UI

== Fase 3: Modificación atómica de roles y registro de auditoría ==
Admin -> UI: toggleRoles (assign: 'mentor')
activate UI
Admin -> UI: click ["Guardar Asignación"]
UI -> Client: assignRoles(target_user_id, selected_roles)
activate Client
Client -> API: POST /api/v1/roles/assign {"user_id": target_id, "roles": selected_roles}
activate API

API -> Service: assign_roles(admin_id, target_user_id, selected_roles)
activate Service

alt [E003] Intento de dejar al usuario sin ningún rol asignado (len(selected_roles) == 0)
    Service --> API: Lanza HTTPException(400, "EMPTY_ROLE_SET_PROHIBITED")
    API --> Client: HTTP 400 Bad Request {"detail": "EMPTY_ROLE_SET_PROHIBITED: Todo usuario debe tener al menos un rol."}
    Client -> UI: displayEmptyRolesError(400, "Todo usuario debe tener al menos un rol.")
    Admin -> UI: selectRoleCheckbox ('mentoreado')
    UI -> UI: enableSaveButton()
else [E004] Intento de auto-revocación del rol Administrador (target_id == current_user_id)
    Service --> API: Lanza HTTPException(400, "CANNOT_REVOKE_OWN_ADMIN")
    API --> Client: HTTP 400 Bad Request {"detail": "CANNOT_REVOKE_OWN_ADMIN: No puede auto-revocarse el rol Administrador."}
    Client -> UI: displaySelfRevocationError(400, "No puede auto-revocarse el rol Administrador.")
    Admin -> UI: click ["Restablecer Selección"]
    UI -> UI: resetAdminCheckbox()
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
    Client -> UI: displayRoleUpdateSuccess(updated_roles)
    
    UI -> UI: updateTableInMemory()
    UI -> UI: closeAssignmentModal()
    UI --> Admin: displaySuccessNotification
end
deactivate Service
deactivate API
deactivate Client
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-010.
"""
