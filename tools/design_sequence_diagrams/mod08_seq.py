# -*- coding: utf-8 -*-
"""
Diagramas de Secuencia - Módulo 08: Analítica, Notificaciones y Configuración (Fase de Diseño)
Contiene:
- CUS-009: Notificar eventos críticos y alertas temporales
- CUS-011: Generar reportes e indicadores de analítica académica
- CUS-015: Consultar métricas de retención y desempeño
- CUS-016: Auditar trazas de seguridad y consentimiento Ley 29733
- CUS-020: Configurar parámetros institucionales y umbrales
- CUS-022: Gestionar catálogo de temas y materias críticas
"""

def get_mod08_seq():
    return """### MOD-08: Analítica, Notificaciones y Configuración

#### Diagrama 6.15.19: Diagrama de Secuencia - CUS-009: Notificar eventos críticos y alertas temporales

El diagrama de secuencia para `CUS-009` formaliza el despacho multicanal de notificaciones reactivas (Server-Sent Events y correo electrónico SMTP) ante eventos críticos del ciclo de vida de las mentorías siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Modela la interacción entre el Planificador desatendido (`SchedulerWorker`), los usuarios institucionales, el componente `NotificationBell.tsx`, `notificationService.ts`, `notifications.py`, `notification_service.py`, `EmailService` y PostgreSQL. Modela la inicialización del flujo SSE, la persistencia de alertas, la degradación controlada ante fallos del servidor SMTP (`E001`) y la lectura interactiva de notificaciones.

```plantuml
@startuml
title Diagrama 6.15.19: Diagrama de Secuencia - CUS-009: Notificar eventos críticos y alertas de confirmación a T-24h\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

participant "Planificador\\n(SchedulerWorker / Celery)" as Cron
actor "Usuario Institucional\\n(Mentor / Alumno)" as User
participant "Vista React\\n(NotificationBell.tsx)" as UI
participant "Adaptador Cliente\\n(notificationService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/notifications.py)" as API
participant "Servicio Backend\\n(notification_service.py)" as Service
participant "Servicio SMTP UPT\\n(EmailService)" as SMTP
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Conexión al canal de notificaciones e inicialización de alertas ==
User -> UI: click ["Campana de Notificaciones"]
activate UI
UI -> Client: subscribeNotifications() & getUnread() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/notifications/stream (SSE)
activate API
Client -> API: GET /api/v1/notifications/unread
API -> Service: get_unread(user_id)
activate Service
Service -> DB: SELECT * FROM notificaciones_eventos WHERE usuario_id = :uid AND leida = false ORDER BY fecha_creacion DESC
activate DB
DB --> Service: Nómina de alertas no leídas
deactivate DB
Service --> API: UnreadNotificationsDTO
deactivate Service
API --> Client: HTTP 200 OK UnreadNotificationsDTO
Client -> UI: displayUnreadBadge(unreadCount)

== Fase 2: Generación asíncrona de evento crítico y despacho multicanal ==
Cron -> Service: dispatch_critical_event(user_id, event_type, message, reference_id)
activate Service
Service -> DB: INSERT INTO notificaciones_eventos (usuario_id, tipo_evento, mensaje, referencia_id, leida=false, fecha_creacion=NOW())\\nVALUES (...) RETURNING id
activate DB
DB --> Service: Alerta persistida
deactivate DB

Service -> API: push_sse_event(user_id, notification_data)
API --> Client: SSE Stream Event: "critical_alert" {mensaje, id}
Client -> UI: updateNotificationBadge(unreadCount + 1)

alt [E001] Falla de despacho en servicio SMTP institucional de respaldo
    Service -> SMTP: send_alert_email(email, subject, message)
    activate SMTP
    SMTP --> Service: SMTPException / Conexión rechazada
    deactivate SMTP
    Service -> Service: logger.warning("SMTP dispatch failed, falling back to SSE only")
    Service --> API: Evento despachado (degradación controlada, entrega vía web preservada)
else Despacho SMTP exitoso
    Service -> SMTP: send_alert_email(email, subject, message)
    activate SMTP
    SMTP --> User: Aviso institucional en buzón universitario @upt.pe
    deactivate SMTP
    Service --> API: Multichannel Dispatch OK
end
deactivate Service

== Fase 3: Recepción reactiva en cliente y lectura de notificación ==
User -> UI: clickIcon ["Campana"]
UI -> UI: openNotificationPanel()
User -> UI: selectNotificationItem(notificationId)
UI -> Client: markAsRead(notificationId)
Client -> API: POST /api/v1/notifications/{id}/mark-read [Bearer JWT]
API -> Service: mark_notification_as_read(notificationId, user_id)
activate Service
Service -> DB: UPDATE notificaciones_eventos SET leida = true WHERE id = :id
activate DB
DB --> Service: Confirmación de actualización
deactivate DB
Service --> API: NotificationMarkReadResponseDTO {"success": true}
deactivate Service
API --> Client: HTTP 200 OK
Client -> UI: decreaseUnreadCounter()
UI -> UI: decrementNotificationCounter()
UI --> User: displayReferencedSessionView
deactivate Client
deactivate API
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-009.

---

#### Diagrama 6.15.20: Diagrama de Secuencia - CUS-011: Generar reportes e indicadores analíticos

El diagrama de secuencia para `CUS-011` especifica la agregación analítica de indicadores de mentoría y la exportación de dossiers ejecutivos para la Dirección de Escuela y comités de calidad ICACIT siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Modela la interacción entre el Administrador, `AnalyticsDashboardView.tsx`, `analyticsService.ts`, `analytics.py`, `analytics_service.py`, el compilador de hojas de cálculo y PostgreSQL. Describe la consulta de métricas generales, la validación de intervalos temporales con rechazo de fechas inconsistentes (`E001`), y la serialización y descarga del informe binario consolidado (`.xlsx` o `.csv`).

```plantuml
@startuml
title Diagrama 6.15.20: Diagrama de Secuencia - CUS-011: Generar reportes consolidados e indicadores analíticos de gestión\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Administrador / Calidad ICACIT" as Admin
participant "Vista React\\n(AnalyticsDashboardView.tsx)" as UI
participant "Adaptador Cliente\\n(analyticsService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/analytics.py)" as API
participant "Servicio Backend\\n(analytics_service.py)" as Service
participant "Generador de Hojas de Cálculo\\n(Excel / OpenPyXL Engine)" as Excel
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Acceso al panel analítico y configuración de parámetros ==
Admin -> UI: click ["Reportes y Analítica"]
activate UI
UI -> Client: getKpiSummary(semester="2026-I") [Bearer JWT]
activate Client
Client -> API: GET /api/v1/analytics/reports/kpis?semester=2026-I
activate API
API -> Service: calculate_kpis(semester="2026-I")
activate Service
Service -> DB: SELECT count(s.id) as total_sesiones, sum(s.duracion_minutos)/60.0 as total_horas,\\n       avg(CASE WHEN s.estado = 'CONFIRMADA' THEN 1 ELSE 0 END)*100 as tasa_quorum,\\n       avg(CASE WHEN a.asistio = true THEN 1 ELSE 0 END)*100 as tasa_asistencia\\nFROM sesiones_mentoria s LEFT JOIN asistencias_sesion a ON s.id = a.sesion_id WHERE s.semestre = '2026-I'
activate DB
DB --> Service: Métricas agregadas
deactivate DB
Service --> API: KpiSummaryDTO
deactivate Service
API --> Client: HTTP 200 OK KpiSummaryDTO
deactivate API
Client -> UI: displayKpiCardsAndCharts(kpis)
deactivate Client

== Fase 2: Ajuste de filtros temporales y selección de formato de exportación ==
Admin -> UI: enter (startDate, endDate, courseId, format="xlsx")
UI -> UI: validateDateConsistency(startDate, endDate)

alt [E001] Rango de fechas inconsistente o fechas futuras
    UI -> UI: displayDateRangeError()
    Admin -> UI: enter (validStartDate, validEndDate)
    UI -> UI: updateDateSelector()
else Rango temporal válido
    Admin -> UI: click ["Exportar Informe Consolidado"]
    UI -> Client: exportReport(format="xlsx", startDate, endDate, courseId)
    activate Client
    Client -> API: GET /api/v1/analytics/export?format=xlsx&start_date={start_date}&end_date={end_date}&course_id={course_id} [Bearer JWT]
    activate API
    API -> Service: export_report(format, start_date, end_date, course_id)
    activate Service
    
    == Fase 3: Generación del documento analítico y descarga segura ==
    Service -> DB: SELECT * FROM sesiones_mentoria s JOIN bitacoras_pedagogicas b ON s.id = b.sesion_id...
    activate DB
    DB --> Service: Registros consolidados
    deactivate DB
    
    Service -> Excel: compile_workbook(resumen_kpi, sesiones, asistencias, materias_criticas)
    activate Excel
    Excel --> Service: StreamBinarioXLSX (Libro con 4 pestañas estructuradas)
    deactivate Excel
    
    Service -> DB: INSERT INTO auditoria_admin (admin_id, accion='EXPORT_REPORT', entidad='analytics', fecha=NOW())
    
    Service --> API: StreamingResponse(content=stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    deactivate Service
    API --> Client: HTTP 200 OK (Stream Binario XLSX)
    deactivate API
    Client -> UI: triggerExcelDownload()
    deactivate Client
    
    UI --> Admin: displayExcelDownloadedConfirmation
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-011.

---

#### Diagrama 6.15.21: Diagrama de Secuencia - CUS-015: Consultar métricas de retención y desempeño

El diagrama de secuencia para `CUS-015` formaliza la inferencia estadística del impacto del programa de mentorías en la retención estudiantil y disminución de reprobación en asignaturas filtro, respaldando los criterios de mejora continua de ICACIT siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Modela las llamadas entre la Comisión de Calidad, `RetentionDashboardView.tsx`, `analyticsService.ts`, `analytics.py`, `analytics_service.py` y PostgreSQL. Modela la comparación entre grupos de control y participantes, la verificación de tamaño muestral mínimo (`A001`), y la generación y exportación del expediente probatorio en formato PDF oficial.

```plantuml
@startuml
title Diagrama 6.15.21: Diagrama de Secuencia - CUS-015: Consultar métricas de correlación de retención estudiantil y desempeño\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Comisión de Calidad ICACIT / Admin" as Evaluador
participant "Vista React\\n(RetentionDashboardView.tsx)" as UI
participant "Adaptador Cliente\\n(analyticsService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/analytics.py)" as API
participant "Servicio Backend\\n(analytics_service.py)" as Service
participant "Compilador PDF ICACIT\\n(ReportEngine)" as PDF
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Acceso al módulo de impacto y selección de cohorte ==
Evaluador -> UI: click ["Impacto y Retención Académica"]
activate UI
UI -> Client: getRetentionMetrics() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/analytics/retention/impact
activate API
API -> Service: analyze_retention_correlation()
activate Service
Service -> DB: SELECT count(DISTINCT estudiante_id) as total_alumnos,\\n       avg(CASE WHEN asistencia_count >= 3 THEN tasa_aprobacion ELSE NULL END) as aprobacion_mentoreados,\\n       avg(CASE WHEN asistencia_count = 0 THEN tasa_aprobacion ELSE NULL END) as aprobacion_control\\nFROM cohortes_academicas
activate DB
DB --> Service: Comparativa estadística de cohortes
deactivate DB
Service --> API: RetentionImpactDTO
deactivate Service
API --> Client: HTTP 200 OK RetentionImpactDTO
deactivate API
Client -> UI: displayRetentionChart(metrics)
deactivate Client

== Fase 2: Segmentación por asignatura filtro y período lectivo ==
Evaluador -> UI: selectCourseFilter (courseId="algoritmos-epis")
Evaluador -> UI: click ["Calcular Índice de Impacto"]
UI -> Client: getCourseRetentionImpact(courseId)
activate Client
Client -> API: GET /api/v1/analytics/retention/cohorts?course_id={course_id}
activate API
API -> Service: get_course_cohort_stats(course_id)
activate Service
Service -> DB: SELECT count(*) as n_muestra, corr(asistencias, nota_final) as r_pearson\\nFROM actas_semestrales a JOIN asistencias_sesion s ON a.estudiante_id = s.estudiante_id\\nWHERE a.curso_id = :cid
activate DB
DB --> Service: Muestra y correlación calculada
deactivate DB

alt [A001] Muestra insuficiente para inferencia estadística (< 10 registros)
    Service --> API: RetentionCohortDTO {"n_muestra": n, "significancia": false, "solo_descriptivo": true}
    API --> Client: HTTP 200 OK
    Client -> UI: displayInsufficientSampleAlert()
    Evaluador -> UI: click ["Ampliar Rango a Semestres Anteriores"]
    UI -> UI: offerExpandedRange()
else Tamaño muestral suficiente (>= 10 registros)
    Service --> API: RetentionCohortDTO {"n_muestra": n, "significancia": true, "r_pearson": r}
    API --> Client: HTTP 200 OK RetentionCohortDTO
    Client -> UI: displayCorrelationResults(stats)
end
deactivate Service
deactivate API
deactivate Client

== Fase 3: Visualización de indicadores ICACIT y exportación ==
Evaluador -> UI: click ["Exportar Evidencia ICACIT"]
UI -> Client: exportIcacitEvidence(courseId)
activate Client
Client -> API: POST /api/v1/analytics/retention/export-evidence {"course_id": cid} [Bearer JWT]
activate API
API -> Service: generate_icacit_report(course_id)
activate Service
Service -> PDF: compile_icacit_dossier(datos_retencion, tablas_frecuencia, firmas_integridad)
activate PDF
PDF --> Service: Documento PDF formal de acreditación
deactivate PDF
Service --> API: StreamingResponse(content=pdf_stream, media_type="application/pdf")
deactivate Service
API --> Client: HTTP 200 OK (Stream Binario PDF)
deactivate API
Client -> UI: triggerPdfDownload()
deactivate Client
UI --> Evaluador: displayIcacitDossierDownloadedConfirmation
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-015.

---

#### Diagrama 6.15.22: Diagrama de Secuencia - CUS-016: Auditar trazas de seguridad y consentimiento

El diagrama de secuencia para `CUS-016` modela la auditoría forense inmutable y la verificación de integridad de la cadena criptográfica de logs (Hash Chain) bajo los mandatos de la Ley Nº 29733 y el estándar ISO/IEC 27001 siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Desglosa los participantes: Oficial de Seguridad, `AuditLogView.tsx`, `auditService.ts`, `audit.py`, `audit_service.py` y PostgreSQL. Especifica la restricción RBAC (`E001`), la verificación de trazas de consentimiento, el cálculo iterativo recursivo `SHA256(prev_hash + data)` con detección de manipulaciones (`E002`), y la acreditación de integridad con 0 alteraciones.

```plantuml
@startuml
title Diagrama 6.15.22: Diagrama de Secuencia - CUS-016: Auditar trazas inmutables de seguridad y consentimientos legales\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Oficial de Seguridad / Delegado DPO\\n(UserRole.administrador)" as SecOfficer
participant "Vista React\\n(AuditLogView.tsx)" as UI
participant "Adaptador Cliente\\n(auditService.ts / ApiAuditAdapter)" as Client
participant "Controlador FastAPI\\n(endpoints/audit.py)" as API
participant "Servicio Backend\\n(audit_service.py / AuditService)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta del registro forense de auditoría ==
SecOfficer -> UI: click ["Auditoría de Seguridad y Ley 29733"]
activate UI
UI -> Client: getAuditLogs(limit=50) [Bearer JWT]
activate Client
Client -> API: GET /api/v1/audit/logs?limit=50
activate API

API -> API: require_security_officer_role(current_user)

alt [E001] Permisos insuficientes para auditoría de seguridad
    API --> Client: HTTP 403 Forbidden {"detail": "FORBIDDEN_AUDIT: Acceso reservado a Oficial de Seguridad."}
    Client -> UI: displayAccessDeniedModal(403)
    SecOfficer -> UI: click ["Aceptar"]
    UI -> UI: redirectToAuthorizedDashboard()
else Privilegios de seguridad verificados
    API -> Service: get_logs(limit=50)
    activate Service
    Service -> DB: SELECT l.*, u.email FROM log_auditoria_seguridad l\\nJOIN usuarios u ON l.usuario_id = u.id ORDER BY l.id DESC LIMIT 50
    activate DB
    DB --> Service: Trazas de auditoría forense
    deactivate DB
    Service --> API: AuditLogListResponseDTO
    deactivate Service
    API --> Client: HTTP 200 OK AuditLogListResponseDTO
    Client -> UI: displayAuditLogTable(logs)
end
deactivate API
deactivate Client

== Fase 2: Filtrado por usuario y verificación de traza legal de consentimiento ==
SecOfficer -> UI: enter (email: "usuario@upt.pe")
SecOfficer -> UI: click ["Buscar Consentimiento"]
UI -> Client: getConsentTraces(email)
activate Client
Client -> API: GET /api/v1/audit/consent-traces?email={email} [Bearer JWT]
activate API
API -> Service: get_consent_traces(email)
activate Service
Service -> DB: SELECT * FROM consentimientos_legales WHERE email = :email ORDER BY fecha_registro ASC
activate DB
DB --> Service: Trazas de formalización (UUID, versión, IP, User-Agent, UTC, revocado)
deactivate DB
Service --> API: ConsentTraceListDTO
deactivate Service
API --> Client: HTTP 200 OK ConsentTraceListDTO
deactivate API
Client -> UI: displayConsentTraceModal(traces)
deactivate Client

== Fase 3: Verificación criptográfica de la cadena de auditoría (Hash Chain) ==
SecOfficer -> UI: click ["Verificar Integridad de Cadena de Logs"]
UI -> Client: verifyLogChain()
activate Client
Client -> API: POST /api/v1/audit/verify-chain [Bearer JWT]
activate API
API -> Service: verify_chain_integrity()
activate Service

Service -> DB: SELECT id, hash_bloque, hash_anterior, datos_evento FROM log_auditoria_seguridad ORDER BY id ASC
activate DB
DB --> Service: Todos los registros de auditoría
deactivate DB

Service -> Service: Itera recursivamente recomputando SHA256(hash_anterior + datos_evento)

alt [E002] Inconsistencia detectada en la cadena criptográfica de logs (discrepancia de hash)
    Service --> API: Lanza HTTPException(409, "AUDIT_TAMPERING_DETECTED: Discrepancia en ID {broken_id}")
    API --> Client: HTTP 409 Conflict {"detail": "AUDIT_TAMPERING_DETECTED"}
    Client -> UI: displayTamperingAlert(409, broken_id)
    SecOfficer -> UI: click ["Descargar Informe Forense"]
    UI -> UI: exportForensicDump()
else Cadena 100% íntegra (0 discrepancias)
    Service --> API: VerifyChainResponseDTO {"status": "VALID", "records_verified": count, "tampering_detected": false}
    API --> Client: HTTP 200 OK VerifyChainResponseDTO
    Client -> UI: displayIntegrityVerifiedBadge()
    UI --> SecOfficer: displayChainIntegrityConfirmation
end
deactivate Service
deactivate API
deactivate Client
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-016.

---

#### Diagrama 6.15.23: Diagrama de Secuencia - CUS-020: Configurar parámetros institucionales y umbrales

El diagrama de secuencia para `CUS-020` describe la calibración dinámica de reglas institucionales y umbrales operacionales sin modificación del código fuente siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Modela las llamadas entre el Administrador Institucional, `SystemSettingsView.tsx`, `configService.ts`, `config.py`, `config_service.py` y PostgreSQL. Modela la consulta de parámetros vigentes, la validación de límites operacionales (`E001`), la exigencia de reautenticación para cambios críticos (`E002`), y la persistencia transaccional con purga inmediata de la memoria caché para aplicación en caliente.

```plantuml
@startuml
title Diagrama 6.15.23: Diagrama de Secuencia - CUS-020: Configurar parámetros operativos institucionales y umbrales\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Administrador Institucional\\n(UserRole.administrador)" as Admin
participant "Vista React\\n(SystemSettingsView.tsx)" as UI
participant "Adaptador Cliente\\n(configService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/config.py)" as API
participant "Servicio Backend\\n(config_service.py)" as Service
participant "Caché de Aplicación\\n(Redis / MemoryCache)" as Cache
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta de parámetros vigentes y despliegue del panel ==
Admin -> UI: click ["Configuración del Sistema"]
activate UI
UI -> Client: getParameters() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/config/parameters
activate API
API -> Service: get_parameters()
activate Service
Service -> DB: SELECT clave, valor, descripcion, valor_min, valor_max FROM parametros_institucionales WHERE activo = true
activate DB
DB --> Service: Catálogo de parámetros base
deactivate DB
Service --> API: ParameterListResponseDTO
deactivate Service
API --> Client: HTTP 200 OK ParameterListResponseDTO
deactivate API
Client -> UI: displayParametersForm(parameters)
deactivate Client

== Fase 2: Edición de umbrales y validación de rangos permitidos ==
Admin -> UI: enter (quorumMinimo=4, aforoPresencial=10)
Admin -> UI: click ["Guardar Parámetros Institucionales"]
UI -> UI: validateValueRanges(parameters)

alt [E001] Parámetro fuera de los rangos institucionales permitidos
    UI -> UI: displayOutOfRangeError()
    Admin -> UI: enter (correctedParameterValue)
    UI -> UI: enableSaveButton()
else Valores en rangos admisibles
    UI -> Client: updateParameters(payload)
    activate Client
    Client -> API: PUT /api/v1/config/parameters ParameterUpdatePayload [Bearer JWT]
    activate API
    
    alt [E002] Reautenticación de seguridad requerida (cambios críticos sin contraseña secundaria)
        API --> Client: HTTP 401 Unauthorized {"detail": "REAUTH_REQUIRED: Confirmación de credenciales requerida."}
        Client -> UI: displayReauthModal()
        Admin -> UI: enter (adminSecondaryPassword)
        Admin -> UI: click ["Verificar"]
        UI -> Client: reauthenticateAdmin(credentials)
        Client -> API: POST /api/v1/auth/reauth
        API --> Client: HTTP 200 OK {"reauth_token": token}
        Client -> UI: setReauthToken(token)
    else Autorización confirmada
        API -> Service: update_parameters(admin_id, payload)
        activate Service
        
        == Fase 3: Persistencia transaccional, purga de caché y aplicación en caliente ==
        Service -> DB: BEGIN TRANSACTION
        activate DB
        Service -> DB: UPDATE parametros_institucionales SET valor = :val, fecha_modificacion = NOW(), modificado_por = :uid WHERE clave = :key
        Service -> DB: INSERT INTO log_auditoria_seguridad (usuario_id, evento='PARAM_UPDATE', detalle=:key, fecha=NOW())
        Service -> DB: COMMIT
        DB --> Service: Transacción confirmada
        deactivate DB
        
        Service -> Cache: purge_system_config_cache()
        activate Cache
        Cache --> Service: Caché invalidada en caliente
        deactivate Cache
        
        Service --> API: ParameterUpdateResponseDTO {"success": true, "updated_keys": keys}
        deactivate Service
        API --> Client: HTTP 200 OK ParameterUpdateResponseDTO
        Client -> UI: displayParametersUpdatedSuccess(updated_keys)
        UI --> Admin: displayParametersUpdatedConfirmation
    end
    deactivate API
    deactivate Client
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-020.

---

#### Diagrama 6.15.24: Diagrama de Secuencia - CUS-022: Gestionar catálogo de temas y materias críticas

El diagrama de secuencia para `CUS-022` formaliza la actualización de la malla curricular y el catálogo silábico de materias críticas por parte de la Dirección de Escuela y administradores siguiendo el estándar de modelado de secuencia (Visual Paradigm). Todas las respuestas del sistema concluyen en la capa de vista (`Vista React`). Modela las llamadas entre el Administrador, `AdminCurriculumView.tsx`, `curriculumService.ts`, `curriculum.py`, `curriculum_service.py` y PostgreSQL. Describe la navegación por el árbol curricular, el alta de nuevos temas silábicos con validación de unicidad (`E001`) y rango semestral de semanas 1 a 17 (`E002`), y la confirmación transaccional con actualización reactiva en la interfaz administrativa.

```plantuml
@startuml
title Diagrama 6.15.24: Diagrama de Secuencia - CUS-022: Gestionar catálogo de temas curriculares, asignaturas filtro y malla oficial\\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11
skinparam sequenceBoxBorderColor #1E3A8A
skinparam sequenceBoxBackgroundColor #F0F4F8

actor "Administrador Institucional\\n(UserRole.administrador)" as Admin
participant "Vista React\\n(AdminCurriculumView.tsx)" as UI
participant "Adaptador Cliente\\n(curriculumService.ts)" as Client
participant "Controlador FastAPI\\n(endpoints/curriculum.py)" as API
participant "Servicio Backend\\n(curriculum_service.py)" as Service
database "PostgreSQL DB\\n(SQLAlchemy / Supabase)" as DB

== Fase 1: Consulta del árbol curricular y selección de asignatura ==
Admin -> UI: click ["Gestión de Malla y Temarios"]
activate UI
UI -> Client: getCoursesFullTree() [Bearer JWT]
activate Client
Client -> API: GET /api/v1/curriculum/courses
activate API
API -> Service: get_courses_tree()
activate Service
Service -> DB: SELECT * FROM cursos ORDER BY ciclo, nombre
activate DB
DB --> Service: Malla curricular ordenada por ciclo
deactivate DB
Service --> API: CourseTreeResponseDTO
deactivate Service
API --> Client: HTTP 200 OK CourseTreeResponseDTO
deactivate API
Client -> UI: displayCourseTree(coursesTree)
deactivate Client

== Fase 2: Ingreso de datos del nuevo tema curricular silábico ==
Admin -> UI: clickCourse ["Ver Asignatura"]
Admin -> UI: click ["Agregar Nuevo Tema Curricular"]
UI -> UI: openNewTopicModal()
Admin -> UI: enter (unidad=2, titulo="Grafos y Dijkstra", semana=7, descripcion="Teoría y algoritmos")
Admin -> UI: click ["Registrar Tema Curricular"]
UI -> UI: validateWeekNumber(semana)

alt [E002] Número de semana académica fuera de rango semestral (semana < 1 o > 17)
    UI -> UI: displayWeekOutOfRangeError()
    Admin -> UI: enter (validWeekNumber)
    UI -> UI: updateFormWeek()
else Semana lectiva válida
    UI -> Client: createTopic(courseId, payload)
    activate Client
    Client -> API: POST /api/v1/curriculum/courses/{course_id}/topics TopicCreateRequest [Bearer JWT]
    activate API
    API -> Service: create_topic(course_id, payload)
    activate Service
    
    Service -> DB: SELECT id FROM temas_curriculares WHERE curso_id = :cid AND unidad = :u AND titulo = :t
    activate DB
    DB --> Service: Tema existente o nulo
    deactivate DB
    
    alt [E001] Tema curricular duplicado en la misma unidad didáctica
        Service --> API: Lanza HTTPException(409, "DUPLICATE_TOPIC")
        API --> Client: HTTP 409 Conflict {"detail": "DUPLICATE_TOPIC: Ya existe un tema con ese título en la unidad."}
        Client -> UI: displayDuplicateTopicError(409)
        Admin -> UI: enter (adjustedTitle)
        UI -> UI: enableSaveButton()
    else Tema nuevo y válido
        == Fase 3: Persistencia transaccional y actualización del catálogo ==
        Service -> DB: BEGIN TRANSACTION
        activate DB
        Service -> DB: INSERT INTO temas_curriculares (curso_id, unidad, semana, titulo, descripcion, activo=true)\\nVALUES (:cid, :u, :sem, :t, :desc, true) RETURNING id
        Service -> DB: COMMIT
        DB --> Service: Transacción confirmada (id_tema)
        deactivate DB
        
        Service --> API: TopicResponseDTO {"id": id_tema, "titulo": t, "semana": sem}
        API --> Client: HTTP 201 Created TopicResponseDTO
        Client -> UI: displayTopicCreatedSuccess(id_tema)
        
        UI -> UI: closeNewTopicModal()
        UI -> UI: appendTopicToTree(id_tema)
        UI --> Admin: displayTopicRegisteredConfirmation
    end
    deactivate Service
    deactivate API
    deactivate Client
end
deactivate UI
@enduml
```

Fuente: Elaboración propia a partir de las especificaciones de diseño de CUS-022.
"""
