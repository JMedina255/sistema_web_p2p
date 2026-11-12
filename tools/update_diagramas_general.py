# -*- coding: utf-8 -*-
"""
Script to append Sprint 5, 6, 7, and 8 diagrams to docs/diagramas_general.md
"""

ADDITIONAL_DIAGRAMS = r"""

---

## 5. Diagramas de Diseño Técnico — Sprint 5

### 5.1. Secuencia: Ratificación Anticipada de Asistencia y Desistimiento Voluntario (Sprint 5)
```plantuml
@startuml
title Diagrama de Secuencia: Ratificación de Asistencia y Desistimiento Oportuno (T-24h)\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentoreado" as User
participant "Vista React\n(StudentBookingsView.tsx)" as UI
participant "Adaptador Cliente\n(bookingService.ts)" as Client
participant "Controlador FastAPI\n(bookings.py)" as API
participant "Servicio de Negocio\n(booking_service.py)" as Service
database "PostgreSQL\n(reservas_cupos)" as DB

User -> UI : Clic en "Confirmar asistencia"
UI -> Client : confirmAttendance(idReserva)
Client -> API : POST /api/v1/bookings/{id}/confirm\nHeaders: Bearer <JWT>
API -> Service : confirm_attendance(db, id_reserva, user_id)
Service -> DB : SELECT * FROM reservas_cupos WHERE id = :id FOR UPDATE
alt delta_t > 24 horas (Dentro de ventana válida)
    Service -> DB : UPDATE reservas_cupos SET estado = 'CONFIRMADA',\nfecha_ratificacion = NOW() WHERE id = :id
    Service --> API : 200 OK (BookingDetailResponse)
    API --> Client : 200 OK JSON
    Client --> UI : Actualiza estado reactivo a CONFIRMADA
    UI --> User : Notificación verde: Asistencia ratificada
else delta_t <= 24 horas (Ventana cerrada RN-08)
    Service --> API : 400 Bad Request (WINDOW_CLOSED_T24H)
    API --> Client : 400 Bad Request JSON
    Client --> UI : Despliega error pedagógico
    UI --> User : Alerta roja: Ventana de confirmación cerrada
end
@enduml
```

### 5.2. Actividades: Orquestación del Demonio Cron a T-24h y Quórum Mínimo (Sprint 5)
```plantuml
@startuml
title Diagrama de Actividades: Corte Automático a T-24h y Evaluación de Quórum\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

|#F8F9FA|Demonio Cron Backend|
|#E8F8F5|Base de Datos PostgreSQL|
|#FEF9C3|Servicio de Notificaciones|
|#FFF1F2|Estudiante Mentor|

|Demonio Cron Backend|
start
:Inspecciona sesiones con fecha_inicio <= NOW() + 24h\ny estado = 'PROGRAMADA';

|Base de Datos PostgreSQL|
:Identifica reservas en PENDIENTE_CONFIRMACION;
:UPDATE reservas_cupos SET estado = 'NO_CONFIRMADA'\nWHERE estado = 'PENDIENTE_CONFIRMACION';
:Totaliza reservas con estado = 'CONFIRMADA';

|Demonio Cron Backend|
if (¿Confirmados >= aforo_maximo * 0.5?) then (Sí)
  :UPDATE sesiones_mentoria SET estado = 'CONFIRMADA',\nquorum_alcanzado = true;
  |Servicio de Notificaciones|
  :Despacha correo institucional de confirmación;
  stop
else (No)
  :UPDATE sesiones_mentoria SET estado = 'QUORUM_INSUFICIENTE',\nquorum_alcanzado = false;
  |Servicio de Notificaciones|
  :Alerta inmediata al Mentor por correo;
  |Estudiante Mentor|
  :Recibe notificación de quórum deficiente;
  if (¿Mentor decide continuar?) then (Sí)
    :Ratifica sesión extraordinaria (CONFIRMADA);
  else (No)
    :Cancela sesión (CANCELADA_QUORUM);
    |Base de Datos PostgreSQL|
    :Libera aula física o sala virtual;
  endif
  stop
endif
@enduml
```

---

## 6. Diagramas de Diseño Técnico — Sprint 6

### 6.1. Secuencia: Marcación de Asistencia con Pase QR Dinámico TOTP (Sprint 6)
```plantuml
@startuml
title Diagrama de Secuencia: Check-in de Asistencia mediante Pase QR TOTP\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Asistente" as Est
participant "Vista React (QrPassView)" as UIEst
actor "Estudiante Mentor" as Men
participant "Vista React (QrScannerView)" as UIMen
participant "Controlador FastAPI (attendance.py)" as API
participant "Servicio Asistencia (attendance_service.py)" as Service
database "PostgreSQL (asistencias_sesiones)" as DB

Est -> UIEst : Solicita pase QR dinámico
UIEst -> API : GET /api/v1/attendance/qr-pass?sesion_id={id}
API -> Service : generate_totp_pass(user_id, sesion_id)
Service --> API : Token TOTP efímero (HMAC-SHA256, TTL=60s)
API --> UIEst : Token JSON
UIEst -> UIEst : Renderiza código QR dinámico en pantalla

Men -> UIMen : Escanea código QR con la cámara del dispositivo
UIMen -> API : POST /api/v1/attendance/scan-qr\nPayload: {token_totp, sesion_id}
API -> Service : verify_and_checkin(db, token, mentor_id)
Service -> DB : Valida token, horario de sesión y reserva confirmada
alt Token válido y dentro del horario
    Service -> DB : INSERT INTO asistencias_sesiones\n(sesion_id, estudiante_id, estado='ASISTIO', metodo='QR_TOTP')
    Service --> API : 200 OK (CheckinResponse)
    API --> UIMen : 200 OK JSON
    UIMen --> Men : Confirmación visual verde: Asistencia registrada
else Token expirado o reserva ausente
    Service --> API : 403 Forbidden / 400 Bad Request
    API --> UIMen : Error JSON
    UIMen --> Men : Alerta roja de rechazo
end
@enduml
```

### 6.2. Secuencia: Registro de Bitácora Docente con Hash SHA-256 (Sprint 6)
```plantuml
@startuml
title Diagrama de Secuencia: Registro y Firma Criptográfica de Bitácora Pedagógica\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentor" as Men
participant "Vista React (BitacoraRegisterView)" as UI
participant "Controlador FastAPI (bitacora.py)" as API
participant "Servicio Bitácora (bitacora_service.py)" as Service
database "PostgreSQL (bitacoras_pedagogicas)" as DB

Men -> UI : Diligencia contenidos impartidos y observaciones
UI -> API : POST /api/v1/bitacora/sessions/{id}\nPayload: {temas, observaciones, asistencias}
API -> Service : create_bitacora(db, session_id, mentor_id, payload)
Service -> Service : Valida plazo <= 48h desde fin de sesión (RN-12)
alt Dentro de ventana de 48h
    Service -> Service : Calcula hash inmutable SHA-256(session_id + temas + timestamp)
    Service -> DB : INSERT INTO bitacoras_pedagogicas\n(sesion_id, mentor_id, temas, obs, hash_sha256, estado='PENDIENTE')
    Service -> DB : UPDATE sesiones_mentoria SET estado = 'FINALIZADA'
    Service --> API : 201 Created (BitacoraResponse con hash)
    API --> UI : 201 Created JSON
    UI --> Men : Notificación verde con comprobante y hash SHA-256
else Plazo de 48h vencido
    Service --> API : 400 Bad Request (DEADLINE_EXCEEDED_RN12)
    API --> UI : 400 Bad Request JSON
    UI --> Men : Alerta roja: Plazo reglamentario de 48 horas vencido
end
@enduml
```

---

## 7. Diagramas de Diseño Técnico — Sprint 7

### 7.1. Secuencia: Evaluación Gamificada y Desbloqueo de Insignias (Sprint 7)
```plantuml
@startuml
title Diagrama de Secuencia: Recálculo de Reputación y Otorgamiento de Insignias\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentoreado" as Est
participant "Vista React (PostSessionSurveyModal)" as UI
participant "Controlador FastAPI (feedback.py)" as API
participant "Servicio Gamificación (gamification_service.py)" as Service
database "PostgreSQL (perfiles / insignias)" as DB

Est -> UI : Envía calificación (1-5 estrellas) y comentario
UI -> API : POST /api/v1/feedback/sessions/{id}
API -> Service : submit_survey(db, session_id, student_id, rating)
Service -> DB : INSERT INTO evaluaciones_calidad(...)
Service -> DB : Recalcula reputacion = AVG(puntuacion) en perfiles_formativos
Service -> Service : Evalúa reglas de otorgamiento de insignias
alt Cumple regla: >= 10 mentorías y reputación >= 4.8
    Service -> DB : INSERT INTO mentor_insignias (mentor_id, insignia_id='EXCELENCIA_DOCENTE')
    Service --> API : 200 OK con insignia desbloqueada
    API --> UI : 200 OK JSON
    UI --> Est : Encuesta registrada exitosamente
end
@enduml
```

### 7.2. Secuencia: Emisión de Certificados Oficiales PDF con Código QR (Sprint 7)
```plantuml
@startuml
title Diagrama de Secuencia: Emisión Digital de Certificados con ReportLab y QR\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Administrador EPIS" as Admin
participant "Vista React (AdminCertificatesView)" as UI
participant "Controlador FastAPI (certificates.py)" as API
participant "Servicio Certificados (certificate_service.py)" as Service
participant "Motor ReportLab (pdf_generator.py)" as PDF
database "PostgreSQL (certificados_horas)" as DB

Admin -> UI : Solicita emisión de certificado para mentor
UI -> API : POST /api/v1/certificates/generate?mentor_id={id}
API -> Service : generate_certificate(db, mentor_id)
Service -> DB : Suma horas con bitácoras visadas (estado_visado='APROBADO')
alt Horas acumuladas >= 20.0 (RN-14)
    Service -> Service : Asigna folio correlativo único (ej. UPT-EPIS-2026-0042)
    Service -> PDF : Compila documento PDF/A con firmas y código QR institucional
    PDF --> Service : Bytes PDF y hash SHA-256 del documento
    Service -> DB : INSERT INTO certificados_horas\n(mentor_id, folio, horas, hash_documento, url_qr)
    Service --> API : 201 Created (CertificateResponse)
    API --> UI : 201 Created JSON
    UI --> Admin : Notificación verde y vista previa del certificado
else Horas acumuladas < 20.0
    Service --> API : 400 Bad Request (INSUFFICIENT_AUDITED_HOURS_RN14)
    API --> UI : 400 Bad Request JSON
    UI --> Admin : Alerta roja: Mentor no alcanza el umbral mínimo de 20 horas
end
@enduml
```

---

## 8. Diagramas de Diseño Técnico — Sprint 8

### 8.1. Arquitectura de Despliegue Físico Integral (Sprint 8 / Cierre de Construcción)
```plantuml
@startuml
title Diagrama de Despliegue Físico Integral (Arquitectura Cloud en Producción)\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

node "Navegador Web del Cliente\n(Desktop / Mobile)" as ClientNode {
  artifact "React 18 SPA\n(TypeScript / Tailwind CSS / Vite)" as SPA
  artifact "Pase QR Dinámico TOTP\n(jsdom / Canvas)" as QRPass
}

node "Servidor en la Nube (PaaS Render / Docker)" as ServerNode {
  component "FastAPI RESTful API\n(Python 3.11+ / Uvicorn)" as BackendApp
  component "Motor EdRecSys\n(Scikit-learn / Cosine Similarity)" as RecSysApp
  component "Demonio Quorum Cron\n(Background Scheduler)" as CronApp
  component "Compilador ReportLab\n(PDF/A Engine)" as ReportLabApp
}

node "Infraestructura Cloud (Supabase)" as DBNode {
  database "PostgreSQL 15+" as PGDB {
    folder "15 Tablas Relacionales (3FN)" as Tables
    folder "Políticas Row Level Security (RLS)" as RLSPolicies
    folder "Constraints chk_sesion / chk_reserva" as Checks
  }
}

node "Servicios Externos Institucionales" as ExternalNode {
  component "Servidor SMTP UPT\n(Email 2FA / Alertas)" as SMTP
}

SPA --> BackendApp : HTTPS / TLS 1.3 (Puerto 443)\nCabeceras Bearer JWT
BackendApp --> PGDB : Conexión Pool SQLAlchemy 2.0 (ACID)
BackendApp --> SMTP : Protocolo SMTP SSL (Puerto 465)
BackendApp --> RecSysApp : Inferencia en memoria (12.4 ms)
BackendApp --> ReportLabApp : Generación binaria PDF
CronApp --> PGDB : Tareas programadas a T-24h
@enduml
```

### 8.2. Secuencia: Panel de Analítica Institucional y Auditoría de Trazas (Sprint 8)
```plantuml
@startuml
title Diagrama de Secuencia: Tablero de Analítica Institucional y Auditoría de Trazas\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Director EPIS / Coordinador Tutoría" as Admin
participant "Vista React (AdminAnalyticsView)" as UI
participant "Controlador FastAPI (analytics.py)" as API
participant "Servicio Analítica (analytics_service.py)" as Service
database "PostgreSQL (15 Tablas)" as DB

Admin -> UI : Abre pestaña "Analítica Institucional"
UI -> API : GET /api/v1/analytics/dashboard\nHeaders: Bearer <AdminJWT>
API -> Service : get_institutional_kpis(db)
Service -> DB : Ejecuta consultas de agregación (Demanda, Asistencia, Retención ICACIT)
Service --> API : DashboardKpisResponse (KPIs agregados y anonimizados)
API --> UI : 200 OK JSON
UI --> Admin : Renderiza gráficos de barras, tasas de quórum y materias críticas
@enduml
```

---
*Fin del repositorio — Bóveda Centralizada de Diagramas de Diseño Técnico (Sprints 1 al 8).*
"""

def main():
    target = "docs/diagramas_general.md"
    print(f"Actualizando {target}...")
    with open(target, "r", encoding="utf-8") as f:
        text = f.read()

    # Replace end marker
    marker = "---" + "\n" + "*Fin del repositorio — Bóveda Centralizada de Diagramas de Diseño Técnico.*"
    if marker in text:
        new_text = text.replace(marker, ADDITIONAL_DIAGRAMS.strip())
    else:
        new_text = text + "\n" + ADDITIONAL_DIAGRAMS.strip()

    with open(target, "w", encoding="utf-8") as f:
        f.write(new_text)

    print(f"{target} actualizado exitosamente!")

if __name__ == "__main__":
    main()
