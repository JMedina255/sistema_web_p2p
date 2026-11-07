# -*- coding: utf-8 -*-
"""
Diagramas de Secuencia - Módulo 07: Gamificación e Incentivos (Fase de Diseño)
Contiene:
- CUS-018: Emitir constancia institucional de horas de mentoría
- CUS-019: Gestionar insignias y reputación gamificada
"""

def get_mod07_seq():
    return """### MOD-07: Gamificación e Incentivos

#### Diagrama 6.15.17: Diagrama de Secuencia - CUS-018: Emitir constancia institucional de horas de mentoría

El diagrama de secuencia para `CUS-018` especifica la emisión institucional y descarga de la constancia de horas de mentoría con validación del umbral reglamentario de 20 horas (`RN-14`) siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Modela las llamadas entre el Estudiante Mentor, `CertificateView.tsx`, `certificateService.ts`, `certificates.py`, `certificate_service.py`, el compilador PDF/QR y PostgreSQL. Incorpora el control de umbral con manejo de horas insuficientes (`E001`), la previsualización modal, la generación del documento oficial foliado con sello SHA-256 y código QR institucional, y la descarga binaria segura en formato PDF.

```plantuml
@startuml
title Diagrama 6.15.17: Diagrama de Secuencia - CUS-018: Emitir constancia oficial de horas de mentoría\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor\\n(UserRole.mentor)" as Mentor
participant "Vista React\\n(CertificateView.tsx)" as UI
participant "Adaptador Cliente\\n(certificateService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/certificates.py)" as API
participant "Servicio Backend\\n(certificate_service.py)" as Service
participant "Compilador PDF / QR\\n(ReportLab / QREngine)" as PDF
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta de acumulado de horas y verificación de umbral ==
Mentor -> UI: click ["Mis Certificados"]
activate UI
UI -> Client: getHoursSummary() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/certificates/summary
activate API
API -> Service: calculate_accredited_hours(mentor_id)
activate Service
Service -> DB: SELECT sum(s.duracion_minutos)/60.0 as horas_totales FROM sesiones_mentoria s\\nJOIN bitacoras_pedagogicas b ON s.id = b.sesion_id\\nWHERE s.id_mentor = :mid AND s.estado = 'BITACORA_REGISTRADA'
activate DB
DB --> Service: Total de horas pedagógicas acumuladas
deactivate DB

alt [E001] Horas acreditadas insuficientes para el umbral institucional (horas_totales < 20.0, RN-14)
    Service --> API: Lanza HTTPException(400, "INSUFFICIENT_HOURS")
    API --> Client: HTTP 400 Bad Request {"detail": "INSUFFICIENT_HOURS: Requiere al menos 20 horas (Actual: Xh)."}
    Client -> UI: displayInsufficientHoursWarning(400)
    Mentor -> UI: click ["Ver Sesiones Pendientes"]
    UI -> UI: redirectToPendingSessions()
else Umbral alcanzado (horas_totales >= 20.0)
    Service --> API: HoursSummaryDTO {"horas_totales": horas, "eligible": true}
    API --> Client: HTTP 200 OK HoursSummaryDTO
    Client -> UI: displayHoursEligible(horas_totales, eligible=true)
end
deactivate Service
deactivate API
deactivate Client
deactivate UI

== Fase 2: Solicitud de emisión y previsualización de datos ==
Mentor -> UI: click ["Emitir Constancia Oficial"]
activate UI
UI -> UI: openCertificatePreviewModal()
Mentor -> UI: click ["Confirmar y Generar PDF Cifrado"]

== Fase 3: Generación criptográfica, persistencia y descarga del PDF ==
UI -> Client: generateCertificate(semester="2026-I")
activate Client
Client -> API: POST /api/v1/certificates/generate {"semester": "2026-I"} [Bearer JWT]
activate API
API -> Service: generate_certificate(mentor_id, semester)
activate Service

Service -> Service: Genera serie alfanumérica única (UPT-EPIS-2026-I-0042)
Service -> Service: Calcula hash SHA-256 de los datos curriculares
Service -> PDF: render_certificate_pdf(datos, firma_director, codigo_qr)
activate PDF
PDF --> Service: Documento PDF binario oficial compilado
deactivate PDF

Service -> DB: BEGIN TRANSACTION
activate DB
Service -> DB: INSERT INTO certificados_horas (mentor_id, semestre, total_horas, codigo_serie, hash_integridad, url_archivo, fecha_emision)\\nVALUES (:mid, :sem, :horas, :serie, :hash, :url, NOW()) RETURNING id
Service -> DB: COMMIT
DB --> Service: Certificado persistido
deactivate DB

Service --> API: CertificateResponseDTO {"id": id_cert, "codigo_serie": serie, "url_descarga": url}
deactivate Service
API --> Client: HTTP 201 Created CertificateResponseDTO
deactivate API
Client -> UI: displayGeneratedCertificatePreview(id_cert, serie, url)
deactivate Client

Mentor -> UI: click ["Descargar Constancia en PDF"]
UI -> Client: downloadCertificate(id_cert)
activate Client
Client -> API: GET /api/v1/certificates/{id}/download [Bearer JWT]
activate API
API -> Service: get_certificate_download(id_cert)
activate Service
Service -> DB: SELECT url_archivo FROM certificados_horas WHERE id = :id_cert
activate DB
DB --> Service: Metadata del archivo persistido
deactivate DB
Service --> API: Archivo binario (application/pdf)
deactivate Service
API --> Client: HTTP 200 OK (Stream PDF)
deactivate API
Client -> UI: triggerBrowserDownload(stream)
deactivate Client
UI --> Mentor: displayDownloadPdfCompleted
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-018.

---

#### Diagrama 6.15.18: Diagrama de Secuencia - CUS-019: Gestionar insignias y reputación gamificada

El diagrama de secuencia para `CUS-019` describe el cálculo de la reputación institucional gamificada y la consulta interactiva de insignias de honor alcanzadas por los mentores siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Modela la interacción entre el Estudiante Mentor, el Estudiante Mentoreado, `GamificationView.tsx`, `gamificationService.ts`, `gamification.py`, `reputation_service.py` y PostgreSQL. Abarca la consulta de la vitrina virtual de insignias (conquistadas y bloqueadas), la inspección lateral de requisitos de logro y el despliegue del Cuadro de Honor (Leaderboard) con soporte de visualización anónima para privacidad (`A001`).

```plantuml
@startuml
title Diagrama 6.15.18: Diagrama de Secuencia - CUS-019: Gestionar insignias y reputación gamificada\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Estudiante Mentor / Alumno" as User
participant "Vista React\\n(GamificationView.tsx)" as UI
participant "Adaptador Cliente\\n(gamificationService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/gamification.py)" as API
participant "Servicio Backend\\n(reputation_service.py)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta de insignias personales y progreso de nivel ==
User -> UI: click ["Insignias y Reputación"]
activate UI
UI -> Client: getUserBadges() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/gamification/badges
activate API
API -> Service: get_user_badges(user_id)
activate Service
Service -> DB: SELECT b.*, ub.fecha_obtencion, ub.progreso FROM insignias b\\nLEFT JOIN insignias_usuarios ub ON b.id = ub.insignia_id AND ub.usuario_id = :uid
activate DB
DB --> Service: Catálogo de insignias y estado de avance
deactivate DB
Service --> API: BadgeListResponseDTO
deactivate Service
API --> Client: HTTP 200 OK BadgeListResponseDTO
deactivate API
Client -> UI: displayBadgesShowcase(badges)
deactivate Client
deactivate UI

== Fase 2: Exploración de criterios de logro y detalle de insignia ==
User -> UI: selectBadgeCard (badgeId="mentor-destacado")
activate UI
UI -> UI: displayBadgeDetailsSidebar(badgeInfo)
deactivate UI

== Fase 3: Visualización del cuadro de honor institucional (Leaderboard) ==
User -> UI: click ["Cuadro de Honor de la Escuela"]
activate UI
UI -> Client: getLeaderboard() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/gamification/leaderboard
activate API
API -> Service: calculate_rank()
activate Service
Service -> DB: SELECT u.id, u.nombres, u.apellidos, u.codigo_estudiante, r.score_global, r.modo_anonimo\\nFROM reputacion_usuarios r JOIN usuarios u ON r.usuario_id = u.id ORDER BY r.score_global DESC LIMIT 10
activate DB
DB --> Service: Top-10 mentores ordenados por reputación RN-13
deactivate DB

alt [A001] Visualización en el cuadro de honor con alias anónimo (modo_anonimo = true)
    Service -> Service: Anonimiza nombres oficiales reemplazándolos por seudónimo (ej. "Mentor EPIS-742")
    Service --> API: LeaderboardResponseDTO (con registros anonimizados)
    API --> Client: HTTP 200 OK
    Client -> UI: displayLeaderboardAnonymous(ranking)
else Perfil público estándar
    Service --> API: LeaderboardResponseDTO (nombres públicos)
    API --> Client: HTTP 200 OK LeaderboardResponseDTO
    Client -> UI: displayLeaderboardTable(ranking)
end
deactivate Service
deactivate API
deactivate Client

UI --> User: displayLeaderboardView
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-019.
"""
