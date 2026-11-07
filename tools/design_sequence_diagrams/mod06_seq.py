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

El diagrama de secuencia para `CUS-012` especifica la captura y validación en tiempo real de la asistencia efectiva mediante códigos QR dinámicos basados en TOTP de 30 segundos. Desglosa los participantes: Estudiante Mentor, Estudiante Mentoreado, `SessionAttendanceView.tsx`, `attendanceService.ts`, `attendance.py`, `attendance_service.py`, WebSockets y PostgreSQL. Modela la rotación criptográfica del token, la verificación de reservas ratificadas y ventana de tolerancia horaria (`-15m` a `+30m`), y los flujos de excepción por caducidad de token (`E001`), ausencia de reserva (`E002`) y fuera de ventana (`E003`).

```plantuml
@startuml
title Diagrama 6.15.14: Diagrama de Secuencia - CUS-012: Registrar asistencia interactiva mediante código QR dinámico\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor\n(UserRole.mentor)" as Mentor
actor "Estudiante Mentoreado\n(UserRole.mentoreado)" as Mentoreado
participant "Vista React (Mentor / Alumno)\n(SessionAttendanceView.tsx)" as UI
participant "Adaptador Cliente\n(attendanceService.ts)" as Client
participant "Controlador FastAPI\n(endpoints/attendance.py)" as API
participant "Servicio Backend\n(attendance_service.py)" as Service
participant "Servicio WebSocket\n(FastAPI WS Manager)" as WS
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB

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
            Service -> DB: INSERT INTO asistencias_sesion (sesion_id, estudiante_id, fecha_checkin, asistio, ip_origen)\nVALUES (:sid, :uid, NOW(), true, :ip)\nON CONFLICT (sesion_id, estudiante_id) DO UPDATE SET asistio = true, fecha_checkin = NOW()
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
title Diagrama 6.15.15: Diagrama de Secuencia - CUS-013: Registrar bitácora pedagógica y reporte formativo\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor\n(UserRole.mentor)" as Mentor
participant "Vista React\n(BitacoraFormView.tsx)" as UI
participant "Adaptador Cliente\n(bitacoraService.ts / ApiBitacoraAdapter)" as Client
participant "Controlador FastAPI\n(endpoints/bitacora.py)" as API
participant "Servicio Backend\n(bitacora_service.py / BitacoraService)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB

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
    Service -> DB: INSERT INTO bitacoras_pedagogicas (sesion_id, mentor_id, temas_cubiertos, observaciones, nivel_dificultad, hash_firma, fecha_registro)\nVALUES (:sid, :mid, :temas, :obs, :dif, :hash, NOW()) RETURNING id
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
title Diagrama 6.15.16: Diagrama de Secuencia - CUS-014: Visualizar historial académico integral y bitácoras pedagógicas\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentoreado / Mentor" as User
participant "Vista React\n(HistorySessionsView.tsx)" as UI
participant "Adaptador Cliente\n(historyService.ts)" as Client
participant "Controlador FastAPI\n(endpoints/history.py)" as API
participant "Servicio Backend\n(history_service.py)" as Service
database "PostgreSQL DB\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta del historial y aplicación de filtros cronológicos ==
User -> UI: 1. Clic en "Mi Historial" en el menú de navegación lateral
activate UI
UI -> Client: getUserHistory() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/history/sessions
activate API
API -> Service: get_user_history(user_id)
activate Service
Service -> DB: SELECT s.*, b.hash_firma, a.asistio FROM sesiones_mentoria s\nLEFT JOIN bitacoras_pedagogicas b ON s.id = b.sesion_id\nLEFT JOIN asistencias_sesion a ON s.id = a.sesion_id\nWHERE s.id_mentor = :uid OR a.estudiante_id = :uid ORDER BY s.fecha_inicio DESC
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
Service -> DB: SELECT b.*, u.nombres as mentor_nombre FROM bitacoras_pedagogicas b\nJOIN usuarios u ON b.mentor_id = u.id WHERE b.sesion_id = :sid
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
"""
