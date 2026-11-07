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

El diagrama de secuencia para `CUS-006` formaliza la programación y publicación de sesiones de mentoría académica por parte de un mentor acreditado siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`interface : UI`), reflejando que la interfaz se actualiza y permanece a la espera de las acciones directas del estudiante mentor. Modela la interacción entre el Estudiante Mentor, la interfaz React (`OfferPublishView.tsx`), los clientes HTTP (`offerService.ts` / `apiClient.ts`), los endpoints FastAPI (`endpoints/curriculum.py` y `endpoints/offers.py`), los servicios de lógica de negocio (`CurriculumService` y `OfferService`) y PostgreSQL. Abarca la recuperación de temas curriculares silábicos, la verificación criptográfica del token JWT (`RN-01`, `E005`), la validación de mérito académico y rol habilitado (`RN-03`, `E004`), la comprobación de antelación mínima de 24 horas (`RN-04`, `E002`), el aforo reglamentario (exactamente 10 presencial o 20 virtual, `RN-05`, `E003`) y la creación transaccional atómica de la entidad `SesionMentoria` en estado `PUBLICADA`.

```plantuml
@startuml
title Diagrama 6.15.3: Diagrama de Secuencia - CUS-006: Publicar oferta de mentoría académica\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor\\n(UserRole.mentor)" as Mentor
participant "interface : UI\\n(OfferPublishView.tsx)" as UI
participant "clientAdapter : Client\\n(offerService.ts / apiClient.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/offers.py)" as API
participant "Servicio Backend\\n(offer_service.py / OfferService)" as Service
database "postgresDB : Database\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Configuración de la sesión y selección curricular ==
Mentor -> UI: selectCourse(selectedCourseId)
activate UI
UI -> Client: fetchCourseDetail(selectedCourseId)
activate Client
Client -> API: GET /api/v1/curriculum/courses/{id}
activate API
API -> Service: get_course_by_id(id)
activate Service
Service -> DB: SELECT * FROM asignaturas WHERE id_asignatura = :id\\nSELECT * FROM temas_curriculares WHERE id_asignatura = :id
activate DB
DB --> Service: Asignatura y lista de temas silábicos (Topic[])
deactivate DB
Service --> API: CourseDetailResponse
deactivate Service
API --> Client: HTTP 200 OK CourseDetailResponse
deactivate API
Client -> UI: displayTopicsAndForm(temas, defaultCapacity, suggestedSpace)
deactivate Client
deactivate UI

== Fase 2: Ingreso de parámetros, validación de reglas de aforo y antelación ==
Mentor -> UI: enter (topicId, startDateTime, duration, modality, assignedSpace)
activate UI
Mentor -> UI: click ["Verificar y Publicar"]
UI -> UI: validateOfferPayload(payload)

alt [E001] Campos obligatorios incompletos o sintaxis inválida
    UI -> UI: displayValidationErrors(fieldErrors)
    Mentor -> UI: enterMissingFields(payload)
    Mentor -> UI: click ["Verificar y Publicar"]
else Formulario válido en cliente
    UI -> Client: publishOffer(payload: PublishOfferPayload)
    activate Client
    Client -> API: POST /api/v1/offers PublishOfferPayload [Bearer JWT]
    activate API
    API -> API: _extract_caller_and_admin_status(authorization, payload.mentor_email)

    alt [E005] Discrepancia de identidad o suplantación de mentor
        API --> Client: HTTP 403 Forbidden {"detail": "No tiene autorización para publicar ofertas en nombre de otro usuario."}
        Client -> UI: displaySecurityError(403, "No tiene autorización para publicar ofertas en nombre de otro usuario.")
    else Identidad de mentor verificada
        API -> Service: publish_offer(db, payload, caller_email, is_admin)
        activate Service

        Service -> Service: validate_mentor_eligibility(db, effective_email)
        Service -> DB: SELECT * FROM usuario_roles ur JOIN roles r ON ur.id_rol = r.id_rol\\nWHERE ur.email = :email AND ur.activo = true AND r.nombre_rol IN ('mentor', 'administrador')
        activate DB
        DB --> Service: Roles del usuario y perfil académico (ciclo_actual)
        deactivate DB

        alt [E004] Mentor no elegible por ciclo insuficiente o falta de rol (RN-03)
            Service --> API: Lanza HTTPException(403, "Infracción de RN-03: Solo los estudiantes habilitados con rol de mentor (ciclo >= VII)...")
            API --> Client: HTTP 403 Forbidden {"detail": "Infracción de RN-03: Solo los estudiantes habilitados..."}
            Client -> UI: displayEligibilityError(403, "Infracción de RN-03: Solo los estudiantes habilitados con rol de mentor...")
        else Mentor acreditado (ciclo >= VII)
            Service -> Service: calculate_advance_hours(payload.fecha_inicio)

            alt [E002] Incumplimiento de antelación mínima de 24 horas (fecha_inicio <= now_utc + 24h)
                Service --> API: Lanza HTTPException(400, "Infracción de RN-04: Toda mentoría debe publicarse con una antelación superior a 24 horas...")
                API --> Client: HTTP 400 Bad Request {"detail": "Infracción de RN-04: Toda mentoría debe publicarse..."}
                Client -> UI: displayAdvanceTimeError(400, "Infracción de RN-04: Toda mentoría debe publicarse con antelación > 24h")
            else [E003] Aforo no conforme con la modalidad (aforo != 10 presencial o != 20 virtual)
                Service --> API: Lanza HTTPException(400, "Infracción de RN-05: El aforo reglamentario...")
                API --> Client: HTTP 400 Bad Request {"detail": "Infracción de RN-05: El aforo reglamentario..."}
                Client -> UI: displayCapacityError(400, "Infracción de RN-05: El aforo reglamentario...")
            else Parámetros de mérito, aforo y antelación válidos
                == Fase 3: Persistencia transaccional de la oferta y confirmación en cliente ==
                Service -> DB: sesion_db = SesionMentoria(codigo_sesion=code, mentor_email=..., estado='PUBLICADA', ...)
                Service -> DB: db.add(sesion_db)\\ndb.commit()\\ndb.refresh(sesion_db)
                activate DB
                DB --> Service: Transacción confirmada (id_sesion, codigo_sesion='SES-XXXX')
                deactivate DB
                
                Service --> API: PublishOfferResponse (id_oferta=..., codigo_sesion='SES-XXXX', estado='PUBLICADA')
                API --> Client: HTTP 201 Created PublishOfferResponse
                Client -> UI: showSuccessScreen(codigo_sesion='SES-XXXX', estado='PUBLICADA')
                UI --> Mentor: displayPublishedConfirmation
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

---

#### Diagrama 6.15.4: Diagrama de Secuencia - CUS-008: Consultar disponibilidad de espacios y recursos

El diagrama de secuencia para `CUS-008` modela la consulta de disponibilidad de infraestructura física de la EPIS (aulas, laboratorios y salas de estudio) antes de programar sesiones presenciales siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Detalla la interacción entre el Mentor, la interfaz de usuario, `offerService.ts`, el endpoint `GET /api/v1/offers/spaces/availability`, `offer_service.py` y las tablas `aulas` y `sesiones_mentoria`. Incorpora la restricción de horario universitario de 08:00 a 20:00 (`RN-07`, `E001`), la tolerancia a fallos de persistencia (`E002`) y la conmutación guiada hacia modalidad virtual (`A001`) ante saturación de espacios físicos.

```plantuml
@startuml
title Diagrama 6.15.4: Diagrama de Secuencia - CUS-008: Consultar disponibilidad de espacios físicos y aulas de la EPIS\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor\\n(UserRole.mentor)" as Mentor
participant "Vista React\\n(OfferPublishView.tsx / SpacesModal)" as UI
participant "Adaptador Cliente\\n(offerService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/offers.py)" as API
participant "Servicio Backend\\n(offer_service.py)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Definición de criterios temporales y despacho de consulta ==
Mentor -> UI: enter (date, startTime, endTime)
activate UI
Mentor -> UI: click ["Consultar Aulas Disponibles"]
UI -> Client: checkSpaceAvailability(date, startTime, endTime)
activate Client

Client -> API: GET /api/v1/offers/spaces/availability?date={date}&start_time={start_time}&end_time={end_time} [Bearer JWT]
activate API
API -> Service: check_space_availability(date, start_time, end_time)
activate Service

alt [E001] Horario fuera de la jornada institucional (fuera del intervalo 08:00 - 20:00, RN-07)
    Service --> API: Lanza HTTPException(400, "OPERATIONAL_HOURS_VIOLATION")
    API --> Client: HTTP 400 Bad Request {"detail": "OPERATIONAL_HOURS_VIOLATION: Operación sólo entre 08:00 y 20:00 horas."}
    Client -> UI: displayOperationalHoursError(400, "OPERATIONAL_HOURS_VIOLATION")
    Mentor -> UI: enter (correctedStartTime, correctedEndTime)
    Mentor -> UI: click ["Consultar Aulas Disponibles"]
else Rango horario reglamentario válido
    == Fase 2: Verificación de ocupación en base de datos y renderización de resultados ==
    alt [E002] Falla de conexión o timeout con repositorio de infraestructura
        Service -> DB: Conexión y consulta de aulas (timeout)
        activate DB
        DB --> Service: Timeout de conexión en PostgreSQL
        deactivate DB
        Service --> API: Lanza OperationalError
        API --> Client: HTTP 503 Service Unavailable {"detail": "INFRASTRUCTURE_UNAVAILABLE: No se pudo verificar disponibilidad."}
        Client -> UI: displayInfrastructureUnavailable(503)
        Mentor -> UI: click ["Reintentar Consulta"]
        UI -> Client: checkSpaceAvailability(date, startTime, endTime)
    else Conexión exitosa y consulta ejecutada
        Service -> DB: SELECT a.id, a.codigo, a.capacidad, a.equipamiento FROM aulas a\\nWHERE a.activa = true AND a.id NOT IN (\\n  SELECT aula_id FROM sesiones_mentoria\\n  WHERE fecha = :fecha AND NOT (hora_fin <= :start OR hora_inicio >= :end)\\n  AND estado IN ('PUBLICADA', 'CONFIRMADA')\\n)
        activate DB
        DB --> Service: Lista de aulas disponibles
        deactivate DB
        Service --> API: AvailableSpacesResponseDTO
        API --> Client: HTTP 200 OK AvailableSpacesResponseDTO
        Client -> UI: displayAvailableSpaces(availableSpaces)
        
        alt [A001] Aulas físicas agotadas (cero registros libres)
            UI -> UI: displayNoSpacesAlert()
            Mentor -> UI: click ["Cambiar a Modalidad Virtual"]
            UI -> UI: setModalityVirtual(capacity=20, meet=true)
        else Aulas físicas disponibles
            Mentor -> UI: selectSpace (selectedSpaceId)
            Mentor -> UI: click ["Asignar Aula a la Oferta"]
            UI -> UI: assignSpaceToForm(selectedSpaceId)
            UI --> Mentor: displaySpaceAssignedConfirmation
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
