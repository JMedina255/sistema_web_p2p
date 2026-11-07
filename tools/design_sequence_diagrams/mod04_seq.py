# -*- coding: utf-8 -*-
"""
Diagramas de Secuencia - Módulo 04: Demanda y Recomendaciones Personalizadas (Fase de Diseño)
Contiene:
- CUS-002: Explorar recomendaciones personalizadas Top-k
- CUS-003: Registrar solicitud de demanda académica
"""

def get_mod04_seq():
    return """### MOD-04: Demanda y Recomendaciones Personalizadas

#### Diagrama 6.15.7: Diagrama de Secuencia - CUS-002: Explorar recomendaciones personalizadas Top-k

El diagrama de secuencia para `CUS-002` formaliza la inferencia algorítmica y la entrega de la cartelera personalizada de sesiones de mentoría Top-k. Modela las llamadas entre el Estudiante Mentoreado, el componente cliente `RecommendationFeedView.tsx`, el adaptador `recommendationService.ts`, el endpoint FastAPI en `recommendations.py`, el motor algorítmico `recommendation_service.py` y las tablas de PostgreSQL. Incorpora el fallback heurístico por popularidad ("Cold Start" `A001`), la contingencia ante cartelera desierta (`A002`), el tratamiento de errores de cómputo (`E001`) y la derivación transaccional hacia la reserva de cupo (`CUS-004`).

```plantuml
@startuml
title Diagrama 6.15.7: Diagrama de Secuencia - CUS-002: Explorar recomendaciones personalizadas Top-k\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado\n(UserRole.mentoreado)" as User
participant "Vista React\n(RecommendationFeedView.tsx)" as UI
participant "Adaptador Cliente\n(recommendationService.ts)" as Client
participant "Controlador FastAPI\n(endpoints/recommendations.py)" as API
participant "Servicio Backend\n(recommendation_service.py)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB
participant "Modal Reserva\n(BookingModalView.tsx)" as BookingModal

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
        Service -> DB: SELECT s.* FROM sesiones_mentoria s\nJOIN temas_curriculares t ON s.id_tema = t.id\nJOIN cursos c ON t.curso_id = c.id\nWHERE c.es_filtro = true AND s.estado = 'PUBLICADA' ORDER BY s.aforo_maximo DESC LIMIT 6
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
        
        Service -> DB: SELECT s.*, t.titulo, c.nombre, c.es_filtro FROM sesiones_mentoria s\nJOIN temas_curriculares t ON s.id_tema = t.id\nJOIN cursos c ON t.curso_id = c.id\nWHERE s.estado = 'PUBLICADA' AND s.fecha_inicio > NOW() + INTERVAL '24 HOURS'\nAND s.cupos_ocupados < s.aforo_maximo
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
title Diagrama 6.15.8: Diagrama de Secuencia - CUS-003: Registrar solicitud de demanda académica\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado\n(UserRole.mentoreado)" as User
participant "Vista React\n(DemandModalView.tsx)" as UI
participant "Adaptador Cliente\n(recommendationService.ts)" as Client
participant "Controlador FastAPI\n(endpoints/recommendations.py)" as API
participant "Servicio Backend\n(recommendation_service.py)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB

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
    
    Service -> DB: SELECT id FROM demandas_academicas\nWHERE estudiante_id = :uid AND tema_id = :tid AND estado = 'PENDIENTE'
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
        Service -> DB: INSERT INTO demandas_academicas (estudiante_id, tema_id, franja_horaria, modalidad, comentarios, estado='PENDIENTE')\nVALUES (:uid, :tid, :franja, :mod, :com, 'PENDIENTE') RETURNING id
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
"""
