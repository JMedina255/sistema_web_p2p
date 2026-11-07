# -*- coding: utf-8 -*-
"""
Diagramas de Secuencia - Módulo 05: Quórum, Confirmación y Cancelaciones (Fase de Diseño)
Contiene:
- CUS-004: Reservar cupo de mentoría académica con control de aforo y concurrencia
- CUS-024: Ratificar asistencia obligatoria a sesión de mentoría académica a T-24h
- CUS-017: Desistir voluntariamente de reserva de cupo sin penalidad antes de T-24h
- CUS-023: Evaluar automáticamente el quórum reglamentario de sesiones de mentoría a T-24h
- CUS-007: Gestionar sesión de mentoría y decisión resolutiva ante quórum insuficiente
"""

def get_mod05_seq():
    return """### MOD-05: Quórum, Confirmación y Cancelaciones

#### Diagrama 6.15.9: Diagrama de Secuencia - CUS-004: Reservar cupo de mentoría académica

El diagrama de secuencia para `CUS-004` formaliza el ciclo transaccional de reserva de cupos con control de aforo y concurrencia crítica bajo PostgreSQL. Modela detalladamente las cuatro fases de interacción entre el Estudiante Mentoreado, la interfaz React (`BookingModalView.tsx`), el adaptador `bookingService.ts`, el endpoint `POST /api/v1/bookings/reserve`, el servicio `booking_service.py` y la base de datos relacional. Incluye la adquisición del cerrojo en memoria `_booking_lock`, el bloqueo pesimista de fila `SELECT ... FOR UPDATE OF sesiones_mentoria` con timeout de 5.0s, y los diez flujos de excepción (`E001` a `E010`).

```plantuml
@startuml
title Diagrama 6.15.9: Diagrama de Secuencia - CUS-004: Reservar cupo de mentoría académica\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado\\n(UserRole.mentoreado)" as User
participant "Vista React\\n(BookingModalView.tsx / RecommendationFeedView.tsx)" as UI
participant "Adaptador Cliente\\n(bookingService.ts / ApiBookingAdapter)" as Client
participant "Controlador FastAPI\\n(endpoints/bookings.py)" as API
participant "Servicio Backend\\n(booking_service.py / consent_service.py)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

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
                Service -> DB: INSERT INTO reservas_cupo (id_usuario, id_sesion, estado='PENDIENTE_CONFIRMACION', ticket_hash)\\nVALUES (:uid, :sid, 'PENDIENTE_CONFIRMACION', :th) RETURNING id
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
title Diagrama 6.15.10: Diagrama de Secuencia - CUS-024: Ratificar asistencia obligatoria a sesión de mentoría a T-24h\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado\\n(UserRole.mentoreado)" as User
participant "Vista React\\n(StudentBookingsView.tsx)" as UI
participant "Adaptador Cliente\\n(bookingService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/bookings.py)" as API
participant "Servicio Backend\\n(booking_service.py)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Identificación de reservas pendientes y verificación de ventana temporal ==
User -> UI: 1. Accede a "Mis Reservas" en StudentBookingsView.tsx
activate UI
UI -> Client: getMyBookings() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/bookings/my-bookings
activate API
API -> Service: get_user_bookings(user_email)
activate Service
Service -> DB: SELECT r.*, s.fecha_inicio, s.modalidad FROM reservas_cupo r\\nJOIN sesiones_mentoria s ON r.id_sesion = s.id WHERE r.estudiante_email = :email
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

Service -> DB: SELECT r.*, s.fecha_inicio FROM reservas_cupo r\\nJOIN sesiones_mentoria s ON r.id_sesion = s.id\\nWHERE r.id = :bid AND r.estudiante_email = :email
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
title Diagrama 6.15.11: Diagrama de Secuencia - CUS-017: Desistir voluntariamente de reserva de cupo sin penalidad antes de T-24h\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado\\n(UserRole.mentoreado)" as User
participant "Vista React\\n(StudentBookingsView.tsx)" as UI
participant "Adaptador Cliente\\n(bookingService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/bookings.py)" as API
participant "Servicio Backend\\n(booking_service.py)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

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
title Diagrama 6.15.12: Diagrama de Secuencia - CUS-023: Evaluar automáticamente el quórum reglamentario de sesiones de mentoría a T-24h\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

participant "Planificador\\n(SchedulerWorker / Celery)" as Cron
actor "Administrador Institucional\\n(UserRole.administrador)" as Admin
participant "Vista React\\n(AdminDashboardView.tsx / MentorSessionsView.tsx)" as UI
participant "Adaptador Cliente\\n(quorumService.ts / apiClient)" as Client
participant "Controlador FastAPI\\n(endpoints/quorum.py)" as API
participant "Servicio Backend\\n(booking_service.py / simulation_service.py)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB
participant "Servicio SMTP UPT\\n(EmailService)" as SMTP
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

Service -> DB: SELECT * FROM sesiones_mentoria\\nWHERE estado = 'PUBLICADA' AND fecha_inicio <= NOW() + INTERVAL '24 HOURS'
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
title Diagrama 6.15.13: Diagrama de Secuencia - CUS-007: Decisión del mentor ante quórum insuficiente\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor\\n(UserRole.mentor)" as Mentor
participant "Vista React\\n(MentorSessionsView.tsx)" as UI
participant "Adaptador Cliente\\n(offerService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/offers.py)" as API
participant "Servicio Backend\\n(offer_service.py)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB
participant "Servicio SMTP UPT\\n(EmailService)" as SMTP
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
"""
