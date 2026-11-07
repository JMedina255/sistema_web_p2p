# -*- coding: utf-8 -*-
"""
Diagramas de Secuencia - Módulo 06: Asistencia, Bitácoras y Feedback (Fase de Diseño)
Contiene:
- CUS-012: Registrar asistencia interactiva mediante código QR dinámico
- CUS-013: Registrar bitácora pedagógica de sesión
- CUS-014: Visualizar historial y bitácoras académicas
"""

def get_mod06_seq():
    return """### MOD-06: Asistencia, Bitácoras y Feedback

#### Diagrama 6.15.14: Diagrama de Secuencia - CUS-012: Registrar asistencia a sesión de mentoría

El diagrama de secuencia para `CUS-012` especifica la captura y validación en tiempo real de la asistencia efectiva mediante códigos QR dinámicos basados en TOTP de 30 segundos siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Desglosa los participantes: Estudiante Mentor, Estudiante Mentoreado, `SessionAttendanceView.tsx`, `attendanceService.ts`, `attendance.py`, `attendance_service.py`, WebSockets y PostgreSQL. Modela la rotación criptográfica del token, la verificación de reservas ratificadas y ventana de tolerancia horaria (`-15m` a `+30m`), y los flujos de excepción por caducidad de token (`E001`), ausencia de reserva (`E002`) y fuera de ventana (`E003`).

```plantuml
@startuml
title Diagrama 6.15.14: Diagrama de Secuencia - CUS-012: Registrar asistencia interactiva mediante código QR dinámico\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor\\n(UserRole.mentor)" as Mentor
actor "Estudiante Mentoreado\\n(UserRole.mentoreado)" as Mentoreado
participant "Vista React (Mentor / Alumno)\\n(SessionAttendanceView.tsx)" as UI
participant "Adaptador Cliente\\n(attendanceService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/attendance.py)" as API
participant "Servicio Backend\\n(attendance_service.py)" as Service
participant "Servicio WebSocket\\n(FastAPI WS Manager)" as WS
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Apertura de sesión y generación de token dinámico de asistencia ==
Mentor -> UI: click ["Iniciar Pase de Asistencia Digital"]
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
Client -> UI: displayQrCodeAndRoster(totp_token, expires_in=30)
deactivate Client
deactivate UI

== Fase 2: Escaneo de código QR y validación de reserva y ventana horaria ==
Mentoreado -> UI: scanQrCode (qrToken: "TOTP-928192")
activate UI
Mentoreado -> UI: click ["Registrar Mi Asistencia"]
UI -> Client: registerCheckIn(sessionId, qrToken)
activate Client
Client -> API: POST /api/v1/sessions/{session_id}/attendance/check-in {"qr_token": token} [Bearer JWT]
activate API
API -> Service: record_checkin(session_id, mentoreado_id, qr_token)
activate Service

alt [E001] Código QR o token TOTP expirado (> 30 segundos)
    Service --> API: Lanza HTTPException(400, "QR_TOKEN_EXPIRED")
    API --> Client: HTTP 400 Bad Request {"detail": "QR_TOKEN_EXPIRED: Escanee el código QR actualizado."}
    Client -> UI: displayQrExpiredWarning(400)
    Mentoreado -> UI: click ["Escanear Nuevo Código"]
    UI -> UI: captureNewToken()
else Token TOTP vigente
    Service -> DB: SELECT id FROM reservas_cupo WHERE id_sesion = :sid AND id_estudiante = :uid AND estado = 'CONFIRMADA'
    activate DB
    DB --> Service: Reserva confirmada o nulo
    deactivate DB
    
    alt [E002] Estudiante sin reserva previa confirmada en la sesión
        Service --> API: Lanza HTTPException(403, "NO_CONFIRMED_BOOKING")
        API --> Client: HTTP 403 Forbidden {"detail": "NO_CONFIRMED_BOOKING: No registra reserva confirmada."}
        Client -> UI: displayNoConfirmedBookingAlert(403)
        Mentoreado -> UI: click ["Entendido"]
        UI -> UI: closeScanner()
    else Reserva ratificada verificada
        alt [E003] Check-in fuera del intervalo temporal reglamentario (fuera de [inicio-15m, fin+30m])
            Service --> API: Lanza HTTPException(400, "CHECKIN_WINDOW_CLOSED")
            API --> Client: HTTP 400 Bad Request {"detail": "CHECKIN_WINDOW_CLOSED: Fuera de ventana reglamentaria."}
            Client -> UI: displayCheckinWindowClosed(400)
            Mentoreado -> UI: click ["Aceptar"]
            UI -> UI: redirectToHome()
        else Dentro del intervalo horario de la sesión
            == Fase 3: Persistencia de asistencia y actualización reactiva en tiempo real ==
            Service -> DB: BEGIN TRANSACTION
            activate DB
            Service -> DB: INSERT INTO asistencias_sesion (sesion_id, estudiante_id, fecha_checkin, asistio, ip_origen)\\nVALUES (:sid, :uid, NOW(), true, :ip)\\nON CONFLICT (sesion_id, estudiante_id) DO UPDATE SET asistio = true, fecha_checkin = NOW()
            Service -> DB: COMMIT
            DB --> Service: Asistencia persistida
            deactivate DB
            
            Service -> WS: broadcast_attendance_event(session_id, {"student_id": uid, "status": "PRESENTE"})
            activate WS
            WS --> UI: pushWsAttendanceUpdate(student_id, "PRESENTE")
            deactivate WS
            UI -> UI: updateAttendanceRoster(student_id, "PRESENTE")
            
            Service --> API: AttendanceResponseDTO {"success": true, "asistio": true}
            API --> Client: HTTP 200 OK AttendanceResponseDTO
            Client -> UI: displayCheckinSuccessNotification()
            UI --> Mentoreado: displayCheckinConfirmation
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

El diagrama de secuencia para `CUS-013` modela el registro del reporte formativo post-sesión por parte del estudiante mentor siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Modela la interacción entre el Mentor, `BitacoraFormView.tsx`, `bitacoraService.ts`, `bitacora.py`, `bitacora_service.py` y PostgreSQL. Especifica la validación del plazo reglamentario de 48 horas (`RN-12`, `E001`), la exigencia de al menos 50 caracteres pedagógicos (`E002`), el cómputo de la firma digital criptográfica SHA-256 sobre el contenido pedagógico y la promoción de la sesión a estado `BITACORA_REGISTRADA`.

```plantuml
@startuml
title Diagrama 6.15.15: Diagrama de Secuencia - CUS-013: Registrar bitácora pedagógica y reporte formativo\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor\\n(UserRole.mentor)" as Mentor
participant "Vista React\\n(BitacoraFormView.tsx)" as UI
participant "Adaptador Cliente\\n(bitacoraService.ts / ApiBitacoraAdapter)" as Client
participant "Controlador FastAPI\\n(endpoints/bitacora.py)" as API
participant "Servicio Backend\\n(bitacora_service.py / BitacoraService)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Apertura de bitácora y verificación de plazo límite a 48h ==
Mentor -> UI: click ["Completar Bitácora Pedagógica"]
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
    Client -> UI: displayDeadlineExceededError(400)
    Mentor -> UI: click ["Solicitar Desbloqueo a Coordinación"]
    UI -> UI: openExtensionForm()
else Dentro del plazo reglamentario de 48 horas
    Service --> API: BitacoraEligibilityDTO {"eligible": true}
    API --> Client: HTTP 200 OK {"eligible": true}
    Client -> UI: displayBitacoraForm(eligible=true)
end
deactivate Service
deactivate API
deactivate Client
deactivate UI

== Fase 2: Ingreso de evidencias pedagógicas y validación de contenido ==
Mentor -> UI: selectTopicsCheckboxes (coveredTopics)
activate UI
Mentor -> UI: selectDifficulty (difficultyLevel="Medio")
Mentor -> UI: enter (observacionesPedagogicas)
Mentor -> UI: click ["Guardar y Firmar Bitácora"]
UI -> UI: validatePedagogicalObservations(observacionesPedagogicas)

alt [E002] Descripción pedagógica insuficiente (< 50 caracteres)
    UI -> UI: displayLengthError(required=50)
    Mentor -> UI: enter (expandedObservations >= 50 chars)
    Mentor -> UI: click ["Guardar y Firmar Bitácora"]
else Contenido sustantivo válido
    UI -> Client: submitBitacora(sessionId, payload)
    activate Client
    Client -> API: POST /api/v1/sessions/{session_id}/bitacora BitacoraCreateRequest [Bearer JWT]
    activate API
    API -> Service: create_bitacora(mentor_id, session_id, payload)
    activate Service
    
    == Fase 3: Persistencia transaccional y certificación de horas ==
    Service -> Service: Calcula hash SHA-256(temas + observaciones + mentor_id + timestamp)
    Service -> DB: BEGIN TRANSACTION
    activate DB
    Service -> DB: INSERT INTO bitacoras_pedagogicas (sesion_id, mentor_id, temas_cubiertos, observaciones, nivel_dificultad, hash_firma, fecha_registro)\\nVALUES (:sid, :mid, :temas, :obs, :dif, :hash, NOW()) RETURNING id
    Service -> DB: UPDATE sesiones_mentoria SET estado = 'BITACORA_REGISTRADA' WHERE id = :sid
    Service -> DB: COMMIT
    DB --> Service: Transacción confirmada
    deactivate DB
    
    Service --> API: BitacoraResponseDTO {"id": id_bitacora, "hash_firma": hash, "estado": "BITACORA_REGISTRADA"}
    deactivate Service
    API --> Client: HTTP 201 Created BitacoraResponseDTO
    deactivate API
    Client -> UI: displayBitacoraSuccess(id_bitacora, hash)
    deactivate Client
    
    UI -> UI: redirectToSessionHistory()
    UI --> Mentor: displayBitacoraCreatedConfirmation
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-013.

---

#### Diagrama 6.15.16: Diagrama de Secuencia - CUS-014: Visualizar historial y bitácoras académicas

El diagrama de secuencia para `CUS-014` formaliza la consulta histórica unificada del itinerario de mentorías para estudiantes y mentores siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Modela la interacción entre el usuario universitario, `HistorySessionsView.tsx`, `historyService.ts`, `history.py`, `history_service.py` y las tablas de sesiones, bitácoras y asistencias en PostgreSQL. Detalla la renderización de la línea de tiempo interactiva, el filtrado cronológico por ciclo y materia, el tratamiento de usuarios nuevos con historial vacío (`A001`), y la inspección modal de bitácoras pedagógicas con comprobación de firmas criptográficas.

```plantuml
@startuml
title Diagrama 6.15.16: Diagrama de Secuencia - CUS-014: Visualizar historial académico integral y bitácoras pedagógicas\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado / Mentor" as User
participant "Vista React\\n(HistorySessionsView.tsx)" as UI
participant "Adaptador Cliente\\n(historyService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/history.py)" as API
participant "Servicio Backend\\n(history_service.py)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta del historial y aplicación de filtros cronológicos ==
User -> UI: click ["Mi Historial"]
activate UI
UI -> Client: getUserHistory() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/history/sessions
activate API
API -> Service: get_user_history(user_id)
activate Service
Service -> DB: SELECT s.*, b.hash_firma, a.asistio FROM sesiones_mentoria s\\nLEFT JOIN bitacoras_pedagogicas b ON s.id = b.sesion_id\\nLEFT JOIN asistencias_sesion a ON s.id = a.sesion_id\\nWHERE s.id_mentor = :uid OR a.estudiante_id = :uid ORDER BY s.fecha_inicio DESC
activate DB
DB --> Service: Historial de sesiones y asistencias
deactivate DB

alt [A001] Historial académico vacío para usuario nuevo (cero registros)
    Service --> API: EmptyHistoryDTO []
    API --> Client: HTTP 200 OK []
    Client -> UI: displayEmptyHistoryAlert()
    User -> UI: click ["Explorar Cartelera"]
    UI -> UI: redirectToRecommendations()
else Historial con registros consolidados
    Service --> API: UserHistoryResponseDTO
    API --> Client: HTTP 200 OK UserHistoryResponseDTO
    Client -> UI: displayHistoryTimeline(history)
end
deactivate Service
deactivate API
deactivate Client
deactivate UI

== Fase 2: Búsqueda y filtrado por materia o período académico ==
User -> UI: enter (searchQuery: "Algoritmos", semester="2026-I")
activate UI
UI -> UI: filterHistoryInState(searchQuery, semester)
deactivate UI

== Fase 3: Visualización de bitácora pedagógica y comprobante de asistencia ==
User -> UI: clickCardButton ["Ver Bitácora Pedagógica"]
activate UI
UI -> Client: getSessionBitacora(sessionId)
activate Client
Client -> API: GET /api/v1/history/bitacora/{session_id} [Bearer JWT]
activate API
API -> Service: get_bitacora_detail(session_id)
activate Service
Service -> DB: SELECT b.*, u.nombres as mentor_nombre FROM bitacoras_pedagogicas b\\nJOIN usuarios u ON b.mentor_id = u.id WHERE b.sesion_id = :sid
activate DB
DB --> Service: Detalle pedagógico y firma digital SHA-256
deactivate DB
Service --> API: BitacoraDetailDTO
deactivate Service
API --> Client: HTTP 200 OK BitacoraDetailDTO
deactivate API
Client -> UI: displayBitacoraDetailModal(bitacoraDetail)
deactivate Client

UI --> User: displayBitacoraDetailModal
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-014.
"""
