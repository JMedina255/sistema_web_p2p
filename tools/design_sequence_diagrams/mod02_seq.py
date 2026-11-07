# -*- coding: utf-8 -*-
"""
Diagramas de Secuencia - Módulo 02: Ofertas de Mentoría y Espacios (Fase de Diseño)
Contiene:
- CUS-006: Publicar oferta de mentoría individual o grupal
- CUS-008: Consultar disponibilidad de espacios físicos y recursos
"""

def get_mod02_seq():
    return """### MOD-02: Ofertas de Mentoría y Espacios

#### Diagrama 6.15.3: Diagrama de Secuencia - CUS-006: Publicar oferta de mentoría académica

El diagrama de secuencia para `CUS-006` formaliza la programación y publicación de sesiones de mentoría académica por parte de un mentor acreditado. Modela la interacción entre el Estudiante Mentor, la interfaz React, el cliente HTTP `offerService.ts`, el endpoint en `offers.py`, el servicio de lógica de negocio `offer_service.py` y PostgreSQL. Abarca la recuperación de temas curriculares, la validación estricta de antelación mínima de 24 horas (`RN-04`, `E002`), el aforo reglamentario (máximo 10 presencial, 20 virtual, `RN-05`, `E003`), la detección de conflictos de horario (`E004`), la verificación de enlaces Google Meet (`E005`) y la creación transaccional atómica en estado `PUBLICADA`.

```plantuml
@startuml
title Diagrama 6.15.3: Diagrama de Secuencia - CUS-006: Publicar oferta de mentoría académica\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor\n(UserRole.mentor)" as Mentor
participant "Vista React\n(OfferPublishView.tsx)" as UI
participant "Adaptador Cliente\n(offerService.ts / ApiOfferAdapter)" as Client
participant "Controlador FastAPI\n(endpoints/offers.py)" as API
participant "Servicio Backend\n(offer_service.py / OfferService)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Configuración de la sesión y selección curricular ==
Mentor -> UI: 1. Accede a vista de publicación y selecciona asignatura curricular en "Curso"
activate UI
UI -> Client: loadCourseTopics(courseId)
activate Client
Client -> API: GET /api/v1/curriculum/courses/{course_id}/topics
activate API
API -> Service: get_course_topics(course_id)
activate Service
Service -> DB: SELECT * FROM temas_curriculares WHERE curso_id = :cid
activate DB
DB --> Service: Lista de temas silábicos
deactivate DB
Service --> API: TopicListDTO
deactivate Service
API --> Client: HTTP 200 OK TopicListDTO
deactivate API
Client --> UI: Entrega temas curriculares
deactivate Client
UI --> Mentor: 2. Renderiza temas silábicos, campos de fecha, hora, duración (60-120 min), modalidad y cupos
deactivate UI

== Fase 2: Ingreso de parámetros, validación de reglas de aforo y antelación ==
Mentor -> UI: 3. Selecciona tema, fecha/hora, modalidad, ingresa cupos y pulsa "Verificar y Publicar"
activate UI
UI -> UI: Valida sintaxis de campos en formulario cliente

alt [E001] Campos obligatorios incompletos o inválidos
    UI --> Mentor: Resalta campos observados con borde rojo y texto explicativo
    Mentor -> UI: Corrige campos completando los datos requeridos
    UI --> Mentor: Rehabilita botón "Verificar y Publicar" y retorna al paso 3
else Formulario válido en cliente
    UI -> Client: publishOffer(payload)
    activate Client
    Client -> API: POST /api/v1/offers/publish OfferCreateRequest [Bearer JWT]
    activate API
    API -> Service: publish_offer(mentor_id, payload)
    activate Service
    
    alt [E002] Incumplimiento de antelación mínima de 24 horas (fecha_inicio < now_utc + 24h)
        Service --> API: Lanza HTTPException(400, "INSUFFICIENT_ADVANCE_TIME")
        API --> Client: HTTP 400 Bad Request {"detail": "INSUFFICIENT_ADVANCE_TIME: Mínimo 24 horas de antelación."}
        Client --> UI: Captura error 400
        UI --> Mentor: Panel rojo "Antelación mínima requerida: 24 horas" y botón [Ajustar Fecha]
        Mentor -> UI: Clic en [Ajustar Fecha], selecciona nueva fecha > 24h
        UI --> Mentor: Retorna al paso 3
    else [E003] Aforo sobrepasa límites institucionales (presencial > 10 o virtual > 20)
        Service --> API: Lanza HTTPException(400, "CAPACITY_EXCEEDED")
        API --> Client: HTTP 400 Bad Request {"detail": "CAPACITY_EXCEEDED: Máximo 10 presencial y 20 virtual."}
        Client --> UI: Captura error 400
        UI --> Mentor: Mensaje rojo "Aforo supera límite reglamentario", ajusta vacantes y retorna al paso 3
    else Parámetros de aforo y antelación válidos
        == Fase 3: Verificación de concurrencia de horarios y persistencia transaccional ==
        Mentor -> UI: 5. Visualiza indicador circular de procesamiento en botón
        
        Service -> DB: SELECT count(*) FROM sesiones_mentoria\nWHERE id_mentor = :mid AND estado IN ('PUBLICADA', 'CONFIRMADA')\nAND NOT (fecha_fin <= :inicio OR fecha_inicio >= :fin)
        activate DB
        DB --> Service: Resultado de solapamiento de horarios
        deactivate DB
        
        alt [E004] Conflicto de horario del mentor o traslape en aula física
            Service --> API: Lanza HTTPException(409, "SCHEDULE_CONFLICT")
            API --> Client: HTTP 409 Conflict {"detail": "SCHEDULE_CONFLICT: Traslape con otra sesión o aula ocupada."}
            Client --> UI: Captura error 409
            UI --> Mentor: Alerta ámbar "Existe conflicto de horario o aula ocupada" y botón [Cambiar Horario o Aula]
            Mentor -> UI: Clic en [Cambiar Horario o Aula]
            UI --> Mentor: Habilita selectores y retorna al paso 3
        else [E005] Enlace de videoconferencia virtual no pertenece a Google Meet institucional
            Service --> API: Lanza HTTPException(400, "INVALID_MEETING_URL")
            API --> Client: HTTP 400 Bad Request {"detail": "INVALID_MEETING_URL: Debe pertenecer a meet.google.com."}
            Client --> UI: Captura error 400
            UI --> Mentor: Resalta enlace en rojo solicitando URL de meet.google.com válida y retorna al paso 3
        else Ausencia de traslapes y enlace validado
            Service -> DB: BEGIN TRANSACTION
            activate DB
            Service -> DB: INSERT INTO sesiones_mentoria (id_mentor, id_tema, modalidad, aforo_maximo, fecha_inicio, fecha_fin, estado='PUBLICADA')\nVALUES (...) RETURNING id
            Service -> DB: COMMIT
            DB --> Service: Transacción confirmada (id_sesion)
            deactivate DB
            
            Service --> API: OfferResponseDTO {"id": id_sesion, "estado": "PUBLICADA"}
            API --> Client: HTTP 201 Created OfferResponseDTO
            Client --> UI: Oferta creada exitosamente
            
            UI -> UI: Limpia formulario y actualiza caché
            UI --> Mentor: 6. Despliega tarjeta verde con código de sesión generado y botón "Ver en Cartelera"
        end
    end
    deactivate Service
    deactivate API
    deactivate Client
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-006.

---

#### Diagrama 6.15.4: Diagrama de Secuencia - CUS-008: Consultar disponibilidad de espacios y recursos

El diagrama de secuencia para `CUS-008` modela la consulta de disponibilidad de infraestructura física de la EPIS (aulas, laboratorios y salas de estudio) antes de programar sesiones presenciales. Detalla la interacción entre el Mentor, la interfaz de usuario, `offerService.ts`, el endpoint `GET /api/v1/offers/spaces/availability`, `offer_service.py` y las tablas `aulas` y `sesiones_mentoria`. Incorpora la restricción de horario universitario de 08:00 a 20:00 (`RN-07`, `E001`), la tolerancia a fallos de persistencia (`E002`) y la conmutación guiada hacia modalidad virtual (`A001`) ante saturación de espacios físicos.

```plantuml
@startuml
title Diagrama 6.15.4: Diagrama de Secuencia - CUS-008: Consultar disponibilidad de espacios físicos y aulas de la EPIS\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor\n(UserRole.mentor)" as Mentor
participant "Vista React\n(OfferPublishView.tsx / SpacesModal)" as UI
participant "Adaptador Cliente\n(offerService.ts)" as Client
participant "Controlador FastAPI\n(endpoints/offers.py)" as API
participant "Servicio Backend\n(offer_service.py)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB

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
        Service -> DB: SELECT a.id, a.codigo, a.capacidad, a.equipamiento FROM aulas a\nWHERE a.activa = true AND a.id NOT IN (\n  SELECT aula_id FROM sesiones_mentoria\n  WHERE fecha = :fecha AND NOT (hora_fin <= :start OR hora_inicio >= :end)\n  AND estado IN ('PUBLICADA', 'CONFIRMADA')\n)
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
"""
