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

El diagrama de secuencia para `CUS-001` formaliza la interacción temporal y el intercambio de mensajes entre el usuario universitario, la interfaz de autenticación React, el adaptador de cliente, los controladores FastAPI, el servicio de seguridad y correo institucional, y la base de datos relacional. Modela con precisión exhaustiva las tres fases del Flujo Normal (solicitud de OTP, verificación de código temporal, y formalización de consentimiento bajo la Ley N° 29733 con emisión de JWT de 8 horas), los dos flujos alternativos (consentimiento previo `A001` y reenvío de OTP `A002`) y los seis flujos de excepción (`E001` a `E006`).

```plantuml
@startuml
title Diagrama 6.15.1: Diagrama de Secuencia - CUS-001: Iniciar sesión institucional con 2FA y formalización de consentimiento digital\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Usuario Institucional\n(Estudiante / Mentor / Administrador)" as User
participant "Vista React\n(LoginOtpView.tsx / ConsentModalView.tsx)" as UI
participant "Adaptador Cliente\n(authService.ts / consentService.ts)" as Client
participant "Controlador FastAPI\n(endpoints/auth.py / consent.py)" as API
participant "Servicio Backend\n(auth_service.py / consent_service.py)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB
participant "Servicio SMTP UPT\n(EmailService)" as SMTP

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
title Diagrama 6.15.2: Diagrama de Secuencia - CUS-010: Gestionar asignación y revocación de roles institucionales de usuario\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Autoridad Institucional\n(Administrador / Director EPIS)" as Admin
participant "Vista React\n(AdminDashboardView.tsx)" as UI
participant "Adaptador Cliente\n(roleService.ts / ApiRoleAdapter)" as Client
participant "Controlador FastAPI\n(endpoints/roles.py)" as API
participant "Servicio Backend\n(role_service.py / RoleService)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB

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
    Service -> DB: SELECT u.id, u.email, u.nombres, u.apellidos, array_agg(r.nombre) AS roles\nFROM usuarios u LEFT JOIN roles_usuarios ru ON u.id = ru.id_usuario\nLEFT JOIN roles r ON ru.id_rol = r.id GROUP BY u.id
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
"""
