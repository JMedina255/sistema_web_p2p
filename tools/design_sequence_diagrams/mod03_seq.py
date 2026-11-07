# -*- coding: utf-8 -*-
"""
Diagramas de Secuencia - Módulo 03: Perfil del Mentor y Plan de Aprendizaje (Fase de Diseño)
Contiene:
- CUS-005: Gestionar perfil formativo y disponibilidad horaria
- CUS-021: Explorar catálogo curricular de asignaturas filtro
"""

def get_mod03_seq():
    return """### MOD-03: Perfil del Mentor y Plan de Aprendizaje

#### Diagrama 6.15.5: Diagrama de Secuencia - CUS-005: Gestionar perfil académico y disponibilidad horaria

El diagrama de secuencia para `CUS-005` modela la configuración integral del perfil formativo del estudiante mentor y la administración atómica de su matriz semanal de disponibilidad horaria (lunes a sábado, 08:00 a 20:00). Desglosa las interacciones entre el Estudiante Mentor, `ProfileAvailabilityView.tsx`, `profileService.ts`, `profiles.py`, `profile_service.py` y PostgreSQL. Modela la consulta inicial de perfil, la validación sintáctica de biografía y bloques, el reemplazo atómico transaccional (`DELETE` + `INSERT` en bloque bajo `db.begin()`), y los flujos de excepción por matriz horaria vacía (`E001`), validación de texto (`E002`) y colisión de concurrencia (`E003`).

```plantuml
@startuml
title Diagrama 6.15.5: Diagrama de Secuencia - CUS-005: Gestionar perfil formativo y disponibilidad horaria\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor\n(UserRole.mentor)" as Mentor
participant "Vista React\n(ProfileAvailabilityView.tsx)" as UI
participant "Adaptador Cliente\n(profileService.ts / ApiProfileAdapter)" as Client
participant "Controlador FastAPI\n(endpoints/profiles.py)" as API
participant "Servicio Backend\n(profile_service.py / ProfileService)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta del perfil académico y visualización de la matriz horaria ==
Mentor -> UI: 1. Clic en pestaña "Mi Perfil y Disponibilidad"
activate UI
UI -> Client: getMyProfile() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/profiles/me
activate API
API -> Service: get_profile(user_id)
activate Service
Service -> DB: SELECT p.*, d.* FROM perfiles_academicos p\nLEFT JOIN disponibilidad_horaria d ON p.id = d.perfil_id\nWHERE p.usuario_id = :uid
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
title Diagrama 6.15.6: Diagrama de Secuencia - CUS-021: Explorar catálogo curricular de asignaturas filtro\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado / Mentor" as User
participant "Vista React\n(CurriculumCatalogView.tsx)" as UI
participant "Adaptador Cliente\n(curriculumService.ts / ApiCurriculumAdapter)" as Client
participant "Controlador FastAPI\n(endpoints/curriculum.py)" as API
participant "Servicio Backend\n(curriculum_service.py / CurriculumService)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB

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
    Service -> DB: SELECT c.*, count(t.id) as total_temas FROM cursos c\nLEFT JOIN temas_curriculares t ON c.id = t.curso_id\nWHERE c.activo = true GROUP BY c.id ORDER BY c.ciclo, c.nombre
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
"""
