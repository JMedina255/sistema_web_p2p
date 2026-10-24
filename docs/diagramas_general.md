# Bóveda Centralizada de Diagramas de Diseño Técnico (PlantUML)

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II)  
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)  
**Normativa de Diseño:** `reglas_documentacion_diseño.md` (Regla D-5: Sincronización continua de diagramas)  
**Estado:** Sincronizado y Homologado tras el Cierre del Sprint 2

---

## 1. Diagramas de Diseño Técnico — Sprint 1

### 1.1. Arquitectura y Despliegue Físico de Componentes (Sprint 1)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam linetype ortho

skinparam node {
    BackgroundColor #F8FAFC
    BorderColor #1E293B
    FontColor #0F172A
}
skinparam component {
    BackgroundColor #FFFFFF
    BorderColor #3B82F6
    FontColor #1E293B
}
skinparam database {
    BackgroundColor #FEF3C7
    BorderColor #D97706
    FontColor #78350F
}

title Diagrama de Arquitectura y Despliegue Físico — Sprint 1 (EPIS-UPT)

node "Navegador Web del Estudiante / Mentor" as ClientNode {
    component "SPA React 19 + TypeScript\n(Vite Dev Server :5173)" as ReactApp {
        portin "HTTP Interface" as WebPort
    }
}

node "Servidor de Aplicación (Host Local / Contenedor)" as BackendNode {
    component "FastAPI REST Server\n(Uvicorn ASGI :8000)" as FastApiApp {
        portin "CORS Router\n/api/v1/*" as ApiPort
        component "AuthService\n(OTP / JWT HS256)" as AuthSvc
        component "CurriculumService\n(5 Asignaturas Filtro)" as CurricSvc
        component "SQLAlchemy 2.0 Engine\n(Lazy Pooler / Sanitizer)" as SqlEngine
    }
}

node "Nube Supabase (AWS us-east-1)" as CloudNode {
    database "PostgreSQL 16\n(p2p-epis-dev)" as SupabaseDb {
        component "Políticas RLS\n(Row Level Security)" as RlsEngine
        component "Tablas:\nasignaturas\ntemas_conceptuales\nauth_challenges" as DbTables
    }
}

node "Servicios Externos de Integración" as ExternalNode {
    component "GitHub Actions Runner\n(Ubuntu Latest • CI Pipeline)" as CiServer
}

ReactApp --> ApiPort : JSON / HTTPS (REST API)\nFetch con Credentials
SqlEngine --> SupabaseDb : psycopg3 TCP 5432\nSession Pooler (Transaccional)
CiServer ..> BackendNode : Ejecuta Pytest (50 tests)\nValida Cobertura 91.62%
CiServer ..> ReactApp : Ejecuta Vitest (46 tests)\nValida Lint y Build

@enduml
```

### 1.2. Diagrama de Paquetes y Capas de Software Desacopladas (Sprint 1)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
skinparam packageStyle rectangle

package "aplicacion/frontend/src" as FrontendPkg #F8FAFC {
    package "components" as UIComponents #FFFFFF {
        class LoginOtpView <<Component>>
        class CurriculumCatalogView <<Component>>
        class HealthStatus <<Component>>
    }
    package "services" as FrontServices #FFFFFF {
        interface IAuthService <<Interface>>
        class ApiAuthAdapter <<Adapter>>
        class MockAuthAdapter <<Adapter>>
        class apiClient <<Utility>>
    }
    package "data" as FrontData #FFFFFF {
        class types <<TypeScript Types>>
    }

    LoginOtpView --> IAuthService : consume
    CurriculumCatalogView --> apiClient : consume
    HealthStatus --> apiClient : consume
    ApiAuthAdapter ..|> IAuthService : implementa
    MockAuthAdapter ..|> IAuthService : implementa
    ApiAuthAdapter --> apiClient : usa
}

package "aplicacion/backend/app" as BackendPkg #F0FDF4 {
    package "api/v1/endpoints" as EndpointsPkg #FFFFFF {
        class auth <<Router>>
        class curriculum <<Router>>
        class health <<Router>>
    }
    package "services" as BackServices #FFFFFF {
        class AuthService <<Business Service>>
        class CurriculumService <<Business Service>>
    }
    package "schemas" as SchemasPkg #FFFFFF {
        class OtpRequest <<Pydantic>>
        class OtpVerify <<Pydantic>>
        class CourseResponse <<Pydantic>>
    }
    package "models" as ModelsPkg #FFFFFF {
        class AsignaturaFiltro <<SQLAlchemy Model>>
        class TemaConceptual <<SQLAlchemy Model>>
        class AuthChallenge <<SQLAlchemy Model>>
    }
    package "db" as DbPkg #FFFFFF {
        class session <<Engine / Session Maker>>
        class AlembicMigrations <<001_initial>>
    }
    package "core" as CorePkg #FFFFFF {
        class Settings <<Pydantic BaseSettings>>
        class security <<JWT / Hash Functions>>
    }

    auth --> AuthService
    auth --> SchemasPkg
    curriculum --> CurriculumService
    curriculum --> SchemasPkg
    AuthService --> ModelsPkg
    AuthService --> security
    AuthService --> DbPkg
    CurriculumService --> ModelsPkg
    CurriculumService --> DbPkg
    session --> CorePkg
}

apiClient ..> EndpointsPkg : Peticiones HTTP JSON
@enduml
```

### 1.3. Diagrama Entidad-Relación Físico de Base de Datos (Sprint 1)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
skinparam roundCorner 4
skinparam classFontSize 11

entity "asignaturas" as asignaturas #FFFFFF {
    * id_asignatura : INTEGER <<PK, Sequence>>
    --
    * codigo_curso : VARCHAR(15) <<UNIQUE, Index>>
    * nombre_curso : VARCHAR(100) <<NOT NULL>>
    * ciclo_formativo : INTEGER <<NOT NULL, CHECK(1..4)>>
    * es_prioritaria : BOOLEAN <<NOT NULL, DEFAULT TRUE>>
    * created_at : TIMESTAMPTZ <<NOT NULL, DEFAULT now()>>
}

entity "temas_conceptuales" as temas #FFFFFF {
    * id_tema : INTEGER <<PK, Sequence>>
    --
    * id_asignatura : INTEGER <<FK, NOT NULL, Index>>
    * nombre_tema : VARCHAR(120) <<NOT NULL>>
    * descripcion_silabo : TEXT <<NOT NULL>>
    embedding_vector : TEXT <<NULLABLE>>
    * created_at : TIMESTAMPTZ <<NOT NULL, DEFAULT now()>>
}

entity "auth_challenges" as auth_challenges #FFFFFF {
    * challenge_id : UUID <<PK, gen_random_uuid()>>
    --
    * email : VARCHAR(255) <<NOT NULL, Index>>
    * otp_code : VARCHAR(6) <<NOT NULL>>
    * expires_at : TIMESTAMPTZ <<NOT NULL>>
    * consumed : BOOLEAN <<NOT NULL, DEFAULT FALSE>>
    * created_at : TIMESTAMPTZ <<NOT NULL, DEFAULT now()>>
}

asignaturas ||--|{ temas : "1 asignatura contiene 1..* temas (ON DELETE CASCADE)"
@enduml
```

### 1.4. Secuencia Técnica: Monitoreo de Salud y Conexión de Base de Datos
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
autonumber

actor "Estudiante / Auditor" as User
participant "HealthStatus.tsx\n(React UI)" as UI
participant "apiClient.ts\n(Fetch Client)" as Client
participant "health.py\n(FastAPI Router)" as Router
participant "session.py\n(DB Session Pool)" as DbSession
database "PostgreSQL 16\n(Supabase)" as Postgres

User -> UI : Abre pestaña "Servicios / Monitor"
activate UI
UI -> Client : fetchDbHealth()
activate Client
Client -> Router : GET /api/v1/health/db
activate Router

alt Modo Desarrollo (ENVIRONMENT = 'development')
    Router -> DbSession : test_db_connection()
    activate DbSession
    DbSession -> Postgres : SELECT 1 (Heartbeat Query)
    activate Postgres

    alt Conexión Exitosa
        Postgres --> DbSession : 1 (Query Result OK)
        DbSession --> Router : True, latency_ms = 45.2
        Router --> Client : HTTP 200 OK\n{"status": "healthy", "database": "connected", "latency_ms": 45.2}
        Client --> UI : DbHealthStatus Object
        UI --> User : Muestra indicador verde "Base de datos conectada (45 ms)"
    else Excepción / Timeout en Conexión
        Postgres --> DbSession : Error de socket / timeout
        DbSession -> DbSession : sanitize_db_error()\n(Oculta contraseñas e IP)
        DbSession --> Router : False, sanitized_error
        Router --> Client : HTTP 503 Service Unavailable\n{"status": "unhealthy", "error": "Database unavailable"}
        Client --> UI : Objeto de error sanitizado
        UI --> User : Muestra indicador rojo "Error de base de datos"
    end
    deactivate Postgres
    deactivate DbSession
else Modo Producción
    Router --> Client : HTTP 404 Not Found (Oculta endpoint de diagnóstico)
    deactivate Router
end
deactivate Client
deactivate UI
@enduml
```

### 1.5. Secuencia Técnica: Solicitud de Desafío OTP Institucional
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
autonumber

actor "Estudiante UPT" as Student
participant "LoginOtpView.tsx\n(Paso 1)" as UI
participant "authService.ts\n(ApiAuthAdapter)" as AuthAdapter
participant "api/v1/endpoints/auth.py\n(FastAPI)" as AuthRouter
participant "AuthService\n(Backend Service)" as Svc
database "auth_challenges\n(PostgreSQL / Memoria)" as Db

Student -> UI : Ingresa "estudiante@upt.pe" y pulsa "Solicitar Código"
activate UI
UI -> UI : Valida regex /^[a-zA-Z0-9._%+-]+@upt\.pe$/

alt Correo No Institucional (distinto de @upt.pe)
    UI --> Student : Error en pantalla: "Debe ser correo institucional @upt.pe"
else Correo Válido @upt.pe
    UI -> AuthAdapter : requestOtp("estudiante@upt.pe")
    activate AuthAdapter
    AuthAdapter -> AuthRouter : POST /api/v1/auth/otp/request\n{"email": "estudiante@upt.pe"}
    activate AuthRouter
    AuthRouter -> Svc : request_otp(email="estudiante@upt.pe")
    activate Svc

    Svc -> Db : Consulta último desafío del email
    activate Db
    Db --> Svc : Desafío previo (created_at)

    alt Cooldown Activo (now - created_at < 60 segundos)
        Svc --> AuthRouter : HTTPException(400, "COOLDOWN_ACTIVE")
        AuthRouter --> AuthAdapter : HTTP 400 Bad Request
        AuthAdapter --> UI : Error: "Espere 60 segundos antes de solicitar otro código"
        UI --> Student : Bloquea botón y activa temporizador de cooldown
    else Cooldown Vencido o Primera Solicitud
        Svc -> Db : Invalida desafíos previos (consumed = True) [RN-01]
        Svc -> Svc : Genera OTP aleatorio de 6 dígitos (ej. "849201")
        Svc -> Svc : Calcula expires_at = now(UTC) + 5 minutos
        Svc -> Db : INSERT INTO auth_challenges (challenge_id, email, otp_code, expires_at)
        Db --> Svc : Registro confirmado
        deactivate Db

        Svc -> Svc : Imprime código en consola (dev) / Despacha email
        Svc --> AuthRouter : OtpResponse(challenge_id, expires_at, cooldown_seconds=60)
        AuthRouter --> AuthAdapter : HTTP 200 OK (JSON)
        AuthAdapter --> UI : Challenge Metadata
        UI --> Student : Transición a Paso 2 (Muestra campo de 6 dígitos + timer 5:00)
    end
    deactivate Svc
    deactivate AuthRouter
    deactivate AuthAdapter
end
deactivate UI
@enduml
```

### 1.6. Secuencia Técnica: Verificación OTP y Emisión de Sesión JWT
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
autonumber

actor "Estudiante UPT" as Student
participant "LoginOtpView.tsx\n(Paso 2)" as UI
participant "authService.ts\n(ApiAuthAdapter)" as AuthAdapter
participant "auth.py\n(FastAPI Router)" as Router
participant "AuthService\n(Backend Service)" as Svc
database "auth_challenges\n(PostgreSQL)" as Db
participant "security.py\n(PyJWT Core)" as Security

Student -> UI : Digita "849201" y pulsa "Verificar e Iniciar Sesión"
activate UI
UI -> AuthAdapter : verifyOtp(challengeId, "849201")
activate AuthAdapter
AuthAdapter -> Router : POST /api/v1/auth/otp/verify\n{"challenge_id": "...", "otp_code": "849201"}
activate Router
Router -> Svc : verify_otp(challenge_id, otp_code)
activate Svc

Svc -> Db : SELECT FROM auth_challenges WHERE challenge_id = ...
activate Db
Db --> Svc : Registro de desafío
deactivate Db

alt Desafío No Encontrado
    Svc --> Router : HTTPException(404, "CHALLENGE_NOT_FOUND")
    Router --> AuthAdapter : HTTP 404 Not Found
    AuthAdapter --> UI : Error: "Desafío de autenticación no encontrado"
else Desafío Ya Consumido (consumed == True)
    Svc --> Router : HTTPException(400, "OTP_ALREADY_USED")
    Router --> AuthAdapter : HTTP 400 Bad Request
    AuthAdapter --> UI : Error: "Este código ya ha sido utilizado"
else Desafío Expirado (datetime.now(UTC) > expires_at)
    Svc --> Router : HTTPException(400, "OTP_EXPIRED")
    Router --> AuthAdapter : HTTP 400 Bad Request
    AuthAdapter --> UI : Error: "El código ha expirado. Solicite uno nuevo."
else Código Incorrecto (otp_code != "849201")
    Svc --> Router : HTTPException(400, "OTP_INVALID")
    Router --> AuthAdapter : HTTP 400 Bad Request
    AuthAdapter --> UI : Error: "Código incorrecto. Verifique e intente nuevamente."
else Código Válido y Vigente
    Svc -> Db : UPDATE auth_challenges SET consumed = True WHERE challenge_id = ...
    Svc -> Security : create_access_token(data={"sub": email}, expires_delta=480m)
    activate Security
    Security -> Security : Firma JWT HS256 con JWT_SECRET_KEY
    Security --> Svc : access_token (String JWT)
    deactivate Security

    Svc --> Router : TokenResponse(access_token, token_type="bearer", expires_in=28800)
    Router --> Client : HTTP 200 OK (JSON)
    AuthAdapter --> UI : VerifyOtpResponse (Token + Email)
    UI --> Student : Transición a Paso 3 (Sesión Iniciada con éxito)
end
deactivate Svc
deactivate Router
deactivate AuthAdapter
deactivate UI
@enduml
```

### 1.7. Secuencia Técnica: Consulta y Filtrado del Catálogo Curricular
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
autonumber

actor "Estudiante / Mentor" as User
participant "CurriculumCatalogView.tsx\n(React UI)" as UI
participant "apiClient.ts\n(Fetch Client)" as Client
participant "curriculum.py\n(FastAPI Router)" as Router
participant "CurriculumService\n(Backend Service)" as Svc
database "asignaturas / temas\n(PostgreSQL)" as Db

User -> UI : Ingresa a pestaña "Catálogo Curricular"
activate UI
UI -> Client : fetchCourses(ciclo=None, onlyPriority=True)
activate Client
Client -> Router : GET /api/v1/curriculum/courses?only_priority=true
activate Router
Router -> Svc : get_courses(db, ciclo=None, only_priority=True)
activate Svc

Svc -> Db : SELECT a FROM asignaturas a\nWHERE a.es_prioritaria = True\nORDER BY a.ciclo_formativo, a.codigo_curso
activate Db
Db --> Svc : Lista de 5 entidades AsignaturaFiltro
deactivate Db

Svc --> Router : Lista de CourseResponse (Pydantic)
Router --> Client : HTTP 200 OK (JSON Array con 5 asignaturas)
deactivate Router
Client --> UI : CourseSummary[]
UI -> UI : Selecciona automáticamente la primera materia (Cálculo I)
UI -> Client : fetchCourseTopics(id_asignatura=1)
Client -> Router : GET /api/v1/curriculum/courses/1/topics
activate Router
Router -> Svc : get_course_topics(db, course_id=1)
activate Svc
Svc -> Db : SELECT t FROM temas_conceptuales t\nWHERE t.id_asignatura = 1
activate Db
Db --> Svc : Lista de temas de Cálculo I
deactivate Db
Svc --> Router : Lista de TopicResponse
Router --> Client : HTTP 200 OK (JSON)
deactivate Router
Client --> UI : TopicSummary[]
UI --> User : Renderiza tarjetas de las 5 materias y el temario silábico
deactivate Client
deactivate UI
@enduml
```

### 1.8. Máquina de Estados del Desafío OTP (Sprint 1)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
skinparam roundCorner 8

state "GENERADO / ACTIVO\n[consumed == False && now < expires_at]" as Activo #DCFCE7
state "CONSUMIDO / VERIFICADO\n[consumed == True]" as Consumido #DBEAFE
state "EXPIRADO\n[consumed == False && now >= expires_at]" as Expirado #FEE2E2
state "INVALIDADO POR NUEVA SOLICITUD\n[consumed == True (Reemplazado)]" as Invalidado #FEF3C7

[*] --> Activo : Estudiante solicita OTP tras cooldown (>= 60s)
Activo --> Consumido : Verificación exitosa del código de 6 dígitos
Activo --> Expirado : Transcurren 300 segundos (5 minutos)
Activo --> Invalidado : Estudiante solicita nuevo código tras cooldown

Consumido --> [*] : Emite JWT de sesión de 8 horas
Expirado --> [*] : Requiere nueva solicitud
Invalidado --> [*] : Descartado permanentemente
@enduml
```

---

## 2. Diagramas de Diseño Técnico — Sprint 2

### 2.1. Arquitectura de Despliegue Físico y Comunicación Multi-Capa (Sprint 2)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam linetype ortho

skinparam node {
    BackgroundColor #F8FAFC
    BorderColor #1E293B
    FontColor #0F172A
}
skinparam component {
    BackgroundColor #FFFFFF
    BorderColor #3B82F6
    FontColor #1E293B
}
skinparam database {
    BackgroundColor #FEF3C7
    BorderColor #D97706
    FontColor #78350F
}

title Diagrama de Arquitectura y Despliegue Físico — Sprint 2 (EPIS-UPT)

node "Navegador Web del Estudiante / Administrador" as ClientNode {
    component "SPA React 19 + TypeScript\n(Vite Dev Server :5173)" as ReactApp {
        portin "Web Interface" as WebPort
        component "ConsentModalView.tsx\n(T-04 Ley 29733)" as UIModal
        component "CurriculumCatalogView.tsx\n(T-10 Buscador Avanzado)" as UICatalog
        component "ProfileAvailabilityView.tsx\n(T-11 Perfil & Grilla 6x11)" as UIProfile
    }
}

node "Servidor de Aplicación (Host Local / Contenedor)" as BackendNode {
    component "FastAPI REST Server\n(Uvicorn ASGI :8000)" as FastApiApp {
        portin "CORS Router\n/api/v1/*" as ApiPort
        component "ConsentService\n(T-05 Auditoría UTC / IP)" as ConsentSvc
        component "RoleService\n(T-08 Mérito Académico RN-03)" as RoleSvc
        component "ProfileService\n(T-12 Reemplazo Atómico Agenda)" as ProfileSvc
        component "CurriculumService\n(T-10 Búsqueda Silábica)" as CurricSvc
        component "AuthMiddleware / Security\n(T-13 Bearer JWT HS256)" as SecModule
        component "SQLAlchemy 2.0 Engine\n(Session Pooler Transaccional)" as SqlEngine
    }
}

node "Nube Supabase (PostgreSQL 16 en AWS us-east-1)" as CloudNode {
    database "PostgreSQL 16 (p2p-epis-dev)\nAlembic Migration: 002_roles_and_profiles" as SupabaseDb {
        component "Políticas RLS Activas\n(relrowsecurity = True)" as RlsEngine
        component "Tablas del Sprint 2:\n• consentimientos_legales\n• roles\n• usuario_roles\n• perfiles_academicos\n• disponibilidades_horarias" as DbSprint2
        component "Tablas Base Sprint 1:\n• asignaturas\n• temas_conceptuales\n• auth_challenges" as DbSprint1
    }
}

node "Pipeline de Integración Continua" as ExternalNode {
    component "GitHub Actions Runner\n(Ubuntu Latest • CI Pipeline)" as CiServer
}

ReactApp --> ApiPort : Peticiones HTTPS / JSON con Cabecera Authorization: Bearer JWT
ApiPort --> SecModule : Resuelve identidad (_resolve_authenticated_email)
SecModule --> ConsentSvc : Valida estado legal (RN-02)
SecModule --> RoleSvc : Valida privilegios y mérito (RN-03)
SecModule --> ProfileSvc : Gestiona perfiles y franjas horarias
SqlEngine --> SupabaseDb : Conexión psycopg3 TCP 5432 (Pooler Transaccional)
CiServer ..> BackendNode : Ejecuta Pytest (84 tests, 90.64% cov, Ruff 0 errores)
CiServer ..> ReactApp : Ejecuta Vitest (66 tests, 91.10% cov, ESLint 0 errores)

@enduml
```

### 2.2. Diagrama de Paquetes y Capas de Software Desacopladas (Sprint 2)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
skinparam packageStyle rectangle

package "aplicacion/frontend/src" as FrontendPkg #F8FAFC {
    package "components" as UIComponents #FFFFFF {
        class ConsentModalView <<Component (T-04)>>
        class CurriculumCatalogView <<Component (T-10)>>
        class ProfileAvailabilityView <<Component (T-11)>>
        class LoginOtpView <<Component (T-02)>>
        class HealthStatus <<Component (T-01)>>
    }
    package "services" as FrontServices #FFFFFF {
        class consentService <<Service / Mock Adapter>>
        class profileService <<Service / Mock Adapter>>
        class authService <<Service Adapter>>
        class apiClient <<HTTP Client>>
    }
    package "types" as FrontTypes #FFFFFF {
        class ConsentStatus <<TypeScript Interface>>
        class AcademicProfile <<TypeScript Interface>>
        class AvailabilitySlot <<TypeScript Interface>>
    }

    ConsentModalView --> consentService : consume
    ProfileAvailabilityView --> profileService : consume
    CurriculumCatalogView --> apiClient : consume
    consentService --> apiClient : usa
    profileService --> apiClient : usa
}

package "aplicacion/backend/app" as BackendPkg #F0FDF4 {
    package "api/v1/endpoints" as EndpointsPkg #FFFFFF {
        class consent <<Router (T-05)>>
        class roles <<Router (T-08)>>
        class profiles <<Router (T-12)>>
        class curriculum <<Router (T-10)>>
        class auth <<Router (T-03)>>
    }
    package "services" as BackServices #FFFFFF {
        class ConsentService <<Business Service>>
        class RoleService <<Business Service>>
        class ProfileService <<Business Service>>
        class CurriculumService <<Business Service>>
    }
    package "schemas" as SchemasPkg #FFFFFF {
        class ConsentAcceptRequest <<Pydantic>>
        class RolePromoteRequest <<Pydantic>>
        class ProfileUpdateRequest <<Pydantic>>
        class AvailabilityUpdateRequest <<Pydantic>>
    }
    package "models" as ModelsPkg #FFFFFF {
        class ConsentimientoLegal <<SQLAlchemy Model>>
        class Rol <<SQLAlchemy Model>>
        class UsuarioRol <<SQLAlchemy Model>>
        class PerfilAcademico <<SQLAlchemy Model>>
        class DisponibilidadHoraria <<SQLAlchemy Model>>
    }
    package "db" as DbPkg #FFFFFF {
        class session <<Engine / get_db()>>
        class Migration002 <<002_roles_and_profiles>>
    }

    consent --> ConsentService
    roles --> RoleService
    profiles --> ProfileService
    ConsentService --> ModelsPkg
    RoleService --> ModelsPkg
    ProfileService --> ModelsPkg
    ConsentService --> DbPkg
    RoleService --> DbPkg
    ProfileService --> DbPkg
}

apiClient ..> EndpointsPkg : JSON / HTTPS REST Calls
@enduml
```

### 2.3. Diagrama Entidad-Relación Físico de Base de Datos (Sprint 2)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
skinparam roundCorner 4
skinparam classFontSize 10

entity "roles" as roles #FFFFFF {
    * id_rol : INTEGER <<PK, Sequence>>
    --
    * nombre_rol : VARCHAR(50) <<UNIQUE, Index>>
    descripcion : TEXT <<NULLABLE>>
}

entity "usuario_roles" as usuario_roles #FFFFFF {
    * id_usuario_rol : INTEGER <<PK, Sequence>>
    --
    * email : VARCHAR(255) <<NOT NULL, Index>>
    * id_rol : INTEGER <<FK, NOT NULL, Index>>
    * fecha_asignacion : TIMESTAMPTZ <<NOT NULL, DEFAULT now()>>
    asignado_por : VARCHAR(255) <<NULLABLE>>
    * activo : BOOLEAN <<NOT NULL, DEFAULT TRUE>>
    --
    CONSTRAINT: uq_usuario_roles_email_rol UNIQUE(email, id_rol)
}

entity "consentimientos_legales" as consentimientos #FFFFFF {
    * id_consentimiento : INTEGER <<PK, Sequence>>
    --
    * email : VARCHAR(255) <<NOT NULL, Index>>
    * terms_version : VARCHAR(50) <<NOT NULL, DEFAULT '2026-II-v1.0'>>
    * accepted : BOOLEAN <<NOT NULL>>
    consented_at : TIMESTAMPTZ <<NULLABLE>>
    ip_address : VARCHAR(45) <<NULLABLE>>
    user_agent : TEXT <<NULLABLE>>
    * created_at : TIMESTAMPTZ <<NOT NULL, DEFAULT now()>>
}

entity "perfiles_academicos" as perfiles #FFFFFF {
    * id_perfil : INTEGER <<PK, Sequence>>
    --
    * email : VARCHAR(255) <<UNIQUE, Index>>
    codigo_estudiante : VARCHAR(20) <<NULLABLE>>
    nombres : VARCHAR(100) <<NULLABLE>>
    apellidos : VARCHAR(100) <<NULLABLE>>
    * ciclo_actual : INTEGER <<NOT NULL, DEFAULT 1, CHECK(1..10)>>
    * rol_postulacion : VARCHAR(30) <<NOT NULL, DEFAULT 'mentoreado'>>
    materias_interes : JSONB / TEXT <<NULLABLE>>
    temas_seleccionados : JSONB / TEXT <<NULLABLE>>
    biografia : TEXT <<NULLABLE>>
    * modalidad_preferida : VARCHAR(30) <<NOT NULL, DEFAULT 'presencial'>>
    * updated_at : TIMESTAMPTZ <<NOT NULL, DEFAULT now()>>
}

entity "disponibilidades_horarias" as disponibilidades #FFFFFF {
    * id_disponibilidad : INTEGER <<PK, Sequence>>
    --
    * email : VARCHAR(255) <<NOT NULL, Index>>
    * dia_semana : INTEGER <<NOT NULL, CHECK(1..6)>>
    * hora_inicio : VARCHAR(10) <<NOT NULL>>
    * hora_fin : VARCHAR(10) <<NOT NULL>>
    * created_at : TIMESTAMPTZ <<NOT NULL, DEFAULT now()>>
}

entity "asignaturas" as asignaturas #FFFFFF {
    * id_asignatura : INTEGER <<PK, Sequence>>
    --
    * codigo_curso : VARCHAR(15) <<UNIQUE, Index>>
    * nombre_curso : VARCHAR(100) <<NOT NULL>>
    * ciclo_formativo : INTEGER <<NOT NULL, CHECK(1..4)>>
    * es_prioritaria : BOOLEAN <<NOT NULL, DEFAULT TRUE>>
}

roles ||--o{ usuario_roles : "1 rol asignado a 0..* usuarios (ON DELETE CASCADE)"
perfiles ||--o{ disponibilidades : "1 perfil posee 0..* franjas horarias semanales"

@enduml
```

### 2.4. Diagrama de Casos de Uso del Sprint 2
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
skinparam roundCorner 8

skinparam actor {
    BackgroundColor #F1F5F9
    BorderColor #1E293B
}
skinparam usecase {
    BackgroundColor #FFFFFF
    BorderColor #3B82F6
    ArrowColor #1E293B
}

title Diagrama de Casos de Uso del Sprint 2 — Roles, Currículo y Perfiles

actor "Estudiante Universitario\n(@upt.pe)" as Estudiante
actor "Estudiante Postulante\na Mentor (Ciclo >= VII)" as Postulante
actor "Administrador / Dirección\nEPIS-UPT" as Admin

rectangle "Límites del Sistema Web P2P (Sprint 2)" {
    usecase "CUS01: Emitir Consentimiento Digital\nInformado (Ley N° 29733)" as CUS01_Consent
    usecase "CUS01-R: Revocar Consentimiento\n(Bloqueo RN-02)" as CUS01_Revoke
    usecase "CUS21: Explorar Catálogo Curricular\ny Temarios en Tiempo Real" as CUS21_Catalog
    usecase "CUS15: Configurar Perfil Formativo\ny Modalidad Preferida" as CUS15_Profile
    usecase "CUS15-A: Configurar Matriz Horaria\nSemanal (Grilla 6x11)" as CUS15_Avail
    usecase "CUS10: Postular a Rol Mentor\n(Validación de Mérito RN-03)" as CUS10_Promote
    usecase "CUS10-A: Administrar y Revocar\nPrivilegios de Mentoría" as CUS10_Admin
}

Estudiante --> CUS01_Consent
Estudiante --> CUS01_Revoke
Estudiante --> CUS21_Catalog
Estudiante --> CUS15_Profile
Estudiante --> CUS15_Avail

Postulante --|> Estudiante
Postulante --> CUS10_Promote : Exige ciclo >= 7

Admin --> CUS10_Admin

CUS01_Consent ..> CUS15_Profile : <<precondición obligatoria (RN-02)>>
CUS10_Promote ..> CUS15_Profile : <<requiere perfil formativo>>
CUS15_Avail ..> CUS15_Profile : <<sección vinculada>>
@enduml
```

### 2.5. Secuencia Técnica: Registro y Validación de Consentimiento Informado (T-04 / T-05)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
autonumber

actor "Estudiante UPT" as Student
participant "ConsentModalView.tsx\n(React UI)" as UI
participant "consentService.ts\n(Client Service)" as ClientSvc
participant "consent.py\n(FastAPI Router)" as Router
participant "ConsentService\n(Backend Service)" as Svc
database "consentimientos_legales\n(PostgreSQL)" as Db

Student -> UI : Ingresa al sistema tras autenticación OTP
activate UI
UI -> ClientSvc : getConsentStatus("estudiante@upt.pe")
activate ClientSvc
ClientSvc -> Router : GET /api/v1/consent/status?email=estudiante@upt.pe
activate Router
Router -> Svc : get_status(email)
activate Svc
Svc -> Db : SELECT FROM consentimientos_legales WHERE email = ...
activate Db
Db --> Svc : Registro (accepted=False / Sin registro)
deactivate Db
Svc --> Router : ConsentStatusResponse(has_consented=False, terms_version="2026-II-v1.0")
Router --> ClientSvc : HTTP 200 OK (JSON)
deactivate Router
ClientSvc --> UI : ConsentStatus
UI --> Student : Despliega modal de términos Ley N° 29733 con botón Aceptar deshabilitado

alt Escenario A: Estudiante Acepta Términos
    Student -> UI : Marca checkbox "He leído y acepto los términos..."
    UI -> UI : Habilita botón "Aceptar y Continuar"
    Student -> UI : Pulsa "Aceptar y Continuar"
    UI -> ClientSvc : acceptConsent("estudiante@upt.pe")
    ClientSvc -> Router : POST /api/v1/consent/accept\n{"email": "estudiante@upt.pe", "terms_version": "2026-II-v1.0"}
    activate Router
    Router -> Svc : accept_consent(email, terms_version, ip, user_agent)
    Svc -> Db : INSERT INTO consentimientos_legales (email, terms_version, accepted, consented_at, ip_address, user_agent)\nVALUES (email, '2026-II-v1.0', True, now() at time zone 'utc', '127.0.0.1', 'Mozilla/...')
    activate Db
    Db --> Svc : Confirmación de fila insertada
    deactivate Db
    Svc --> Router : ConsentOperationResponse(success=True, has_consented=True, consented_at=UTC)
    Router --> ClientSvc : HTTP 200 OK (JSON)
    ClientSvc --> UI : Éxito
    UI --> Student : Cierra modal y desbloquea navegación en el sistema
else Escenario B: Estudiante Rechaza Términos (Regla RN-02)
    Student -> UI : Pulsa "Rechazar y Salir"
    UI -> ClientSvc : revokeConsent("estudiante@upt.pe")
    ClientSvc -> Router : POST /api/v1/consent/revoke\n{"email": "estudiante@upt.pe"}
    activate Router
    Router -> Svc : revoke_consent(email)
    Svc -> Db : UPDATE consentimientos_legales SET accepted = False WHERE email = ...
    activate Db
    Db --> Svc : Actualización confirmada
    deactivate Db
    Svc --> Router : ConsentOperationResponse(success=True, has_consented=False)
    Router --> ClientSvc : HTTP 200 OK
    ClientSvc --> UI : Consentimiento Revocado
    UI --> Student : Bloqueo preventivo RN-02: Alerta roja informativa y denegación de navegación
end
deactivate Svc
deactivate Router
deactivate ClientSvc
deactivate UI
@enduml
```

### 2.6. Secuencia Técnica: Asignación de Roles y Verificación de Mérito Académico (T-08 / RN-03)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
autonumber

actor "Estudiante / Administrador" as Caller
participant "roles.py\n(FastAPI Router)" as Router
participant "RoleService\n(Backend Service)" as Svc
participant "perfiles_academicos\n(PostgreSQL)" as ProfileDb
participant "roles / usuario_roles\n(PostgreSQL)" as RoleDb

Caller -> Router : POST /api/v1/roles/promote-mentor\n{"email": "postulante@upt.pe", "promoted_by": "admin@upt.pe"}\nAuthorization: Bearer <AdminJWT>
activate Router

Router -> Router : _resolve_authenticated_email(token)\nVerifica rol administrador de Caller

alt Intento de Autopromoción No Autorizada (Caller == postulante y no admin)
    Router --> Caller : HTTP 403 Forbidden\n{"detail": {"code": "SELF_PROMOTION_FORBIDDEN", "message": "No puede autopromoverse a mentor sin supervisión administrativa"}}
else Invocación Autorizada
    Router -> Svc : promote_to_mentor(email="postulante@upt.pe", promoted_by="admin@upt.pe")
    activate Svc
    Svc -> ProfileDb : SELECT ciclo_actual FROM perfiles_academicos WHERE email = 'postulante@upt.pe'
    activate ProfileDb
    ProfileDb --> Svc : ciclo_actual (Integer)
    deactivate ProfileDb

    alt Violación de Mérito Académico: ciclo_actual < 7 (Regla RN-03)
        Svc --> Router : HTTPException(400, detail={"code": "MERIT_RULE_VIOLATION", "message": "El estudiante debe cursar el séptimo ciclo o superior (ciclo_actual >= 7)"})
        Router --> Caller : HTTP 400 Bad Request\n{"code": "MERIT_RULE_VIOLATION", ...}
    else Mérito Cumplido: ciclo_actual >= 7
        Svc -> RoleDb : INSERT INTO usuario_roles (email, id_rol, asignado_por, activo)\nVALUES ('postulante@upt.pe', 2, 'admin@upt.pe', True)\nON CONFLICT (email, id_rol) DO UPDATE SET activo = True
        activate RoleDb
        RoleDb --> Svc : Confirmación de asignación
        deactivate RoleDb
        Svc --> Router : UserRolesResponse(email='postulante@upt.pe', roles=['mentoreado', 'mentor'])
        Router --> Caller : HTTP 200 OK (JSON con rol mentor activado)
    end
    deactivate Svc
end
deactivate Router
@enduml
```

### 2.7. Secuencia Técnica: Configuración de Perfil Formativo y Reemplazo Atómico de Matriz Horaria (T-11 / T-12)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
autonumber

actor "Estudiante UPT" as Student
participant "ProfileAvailabilityView.tsx\n(React UI)" as UI
participant "profileService.ts\n(Client Service)" as ClientSvc
participant "profiles.py\n(FastAPI Router)" as Router
participant "ProfileService\n(Backend Service)" as Svc
database "disponibilidades_horarias\n(PostgreSQL)" as AvailDb

Student -> UI : Modifica franjas horarias en la grilla 6x11 y pulsa "Guardar Perfil y Disponibilidad"
activate UI
UI -> ClientSvc : saveAvailability("estudiante@upt.pe", slots)
activate ClientSvc
ClientSvc -> Router : PUT /api/v1/profiles/availability\n{"email": "estudiante@upt.pe", "slots": [{"dia_semana": 1, "hora_inicio": "08:00", "hora_fin": "10:00"}, ...]}\nAuthorization: Bearer <Token>
activate Router

Router -> Router : _resolve_authenticated_email(token)\nVerifica que token.email == request.email
Router -> Svc : update_availability(email, slots)
activate Svc

note over Svc, AvailDb
  <b>Transacción ACID Atómica (session.begin()):</b>
  Garantiza que la agenda no quede en estado parcial corrupto ante fallas.
end note

Svc -> AvailDb : DELETE FROM disponibilidades_horarias WHERE email = 'estudiante@upt.pe'
activate AvailDb
AvailDb --> Svc : N franjas previas eliminadas

loop Para cada slot en slots
    Svc -> Svc : Valida formato HH:MM, dia_semana (1..6) y hora_inicio < hora_fin
    Svc -> AvailDb : INSERT INTO disponibilidades_horarias (email, dia_semana, hora_inicio, hora_fin)\nVALUES ('estudiante@upt.pe', slot.dia, slot.inicio, slot.fin)
end

Svc -> AvailDb : COMMIT
AvailDb --> Svc : Transacción confirmada exitosamente
deactivate AvailDb

Svc --> Router : AvailabilityResponse(email='estudiante@upt.pe', total_slots=slots.count, slots=[...])
Router --> ClientSvc : HTTP 200 OK (JSON)
deactivate Svc
deactivate Router
ClientSvc --> UI : Éxito de guardado
UI --> Student : Muestra badge verde "Perfil y disponibilidad guardados correctamente"
deactivate ClientSvc
deactivate UI
@enduml
```

### 2.8. Secuencia Técnica: Aislamiento Criptográfico y Seguridad Multi-Usuario RLS (T-13 / RNF02)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
autonumber

actor "Estudiante Malicioso (usuarioA@upt.pe)" as Attacker
participant "profiles.py\n(FastAPI Router)" as Router
participant "ProfileService\n(Backend Service)" as Svc
database "perfiles_academicos\n(Supabase PostgreSQL)" as Postgres

Attacker -> Router : GET /api/v1/profiles/me?email=usuarioB@upt.pe\nAuthorization: Bearer <JWT_usuarioA>
activate Router

Router -> Router : _resolve_authenticated_email(token)\nExtrae token_email = "usuarioA@upt.pe"

alt Discrepancia de Sujeto (token_email != target_email Y no es admin)
    Router --> Attacker : HTTP 403 Forbidden\n{"detail": {"code": "FORBIDDEN_CROSS_ACCESS", "message": "No tiene autorización para consultar o modificar el perfil de otro usuario"}}
else Identidad Coincidente o Rol Administrador
    Router -> Svc : get_profile(target_email)
    activate Svc
    Svc -> Postgres : SELECT * FROM perfiles_academicos WHERE email = target_email
    activate Postgres
    note right of Postgres
      <b>Evaluación de Política RLS:</b>
      USING (email = (auth.jwt() ->> 'email') OR auth.role() = 'service_role')
    end note
    Postgres --> Svc : Fila del perfil legítimo
    deactivate Postgres
    Svc --> Router : ProfileResponse
    deactivate Svc
    Router --> Attacker : HTTP 200 OK
end
deactivate Router
@enduml
```

### 2.9. Máquinas de Estado del Ciclo de Vida del Consentimiento Legal y del Rol de Usuario
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
skinparam roundCorner 8

state "Máquina de Estados: Consentimiento Legal (Ley 29733)" as SM_Consent {
    state "PENDIENTE / NO_REGISTRADO\n[has_consented == False]" as C_Pendiente #FEF3C7
    state "OTORGADO / ACTIVO\n[has_consented == True && accepted == True]" as C_Otorgado #DCFCE7
    state "REVOCADO / BLOQUEADO\n[has_consented == False && accepted == False]" as C_Revocado #FEE2E2

    [*] --> C_Pendiente : Estudiante inicia sesión por primera vez
    C_Pendiente --> C_Otorgado : Estudiante marca checkbox y pulsa 'Aceptar'\n[POST /api/v1/consent/accept]
    C_Otorgado --> C_Revocado : Estudiante ejerce derecho de revocación\n[POST /api/v1/consent/revoke]
    C_Revocado --> C_Otorgado : Estudiante renueva conformidad expresa\n[POST /api/v1/consent/accept]
    
    C_Revocado --> [*] : Bloqueo preventivo RN-02 activo
}

state "Máquina de Estados: Jerarquía de Roles y Mérito (RN-03)" as SM_Roles {
    state "MENTOREADO_BASE\n[rol == 'mentoreado']" as R_Mentoreado #DBEAFE
    state "POSTULANTE_A_MENTOR\n[rol_postulacion == 'mentor']" as R_Postulante #FEF3C7
    state "MENTOR_ACREDITADO\n[rol == 'mentor' && activo == True]" as R_Mentor #DCFCE7
    state "MENTOR_REVOCADO\n[rol == 'mentor' && activo == False]" as R_Revocado #FEE2E2

    [*] --> R_Mentoreado : Registro automático al verificar OTP
    R_Mentoreado --> R_Postulante : Estudiante declara intención en perfil
    R_Postulante --> R_Mentor : Promoción administrativa validada\n[ciclo_actual >= 7 (RN-03)]
    R_Mentor --> R_Revocado : Revocación administrativa de tutoría\n[POST /api/v1/roles/revoke-mentor]
    R_Revocado --> R_Mentor : Readmisión supervisada por Dirección EPIS
}

@enduml
```

---
*Fin del repositorio — Bóveda Centralizada de Diagramas de Diseño Técnico.*
