# -*- coding: utf-8 -*-
"""
Modulo 08: Analítica, Notificaciones y Configuración (Fase de Diseño)
Contiene: CUS-009, CUS-011, CUS-015, CUS-016, CUS-020, CUS-022
"""

def get_mod08():
    return """### MOD-08: Analítica, Notificaciones y Configuración

#### CUS-009 - Notificar eventos críticos y alertas temporales

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-009** (CUS-009) |
| **Nombre** | Notificar eventos críticos y alertas de confirmación a T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-015 (Monitoreo desatendido, emisión de recordatorios y alertas); RN-04 (Antelación de 24 horas), RN-10 (Control de asistencia y quórum institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Proceso Planificador (`SchedulerWorker`), Estudiante Mentor, Estudiante Mentoreado, Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite transmitir notificaciones asíncronas y alertas en tiempo real a los usuarios institucionales ante eventos críticos del ciclo de vida de las sesiones de mentoría (tales como recordatorios de ratificación de asistencia a T-24h, confirmación oficial de quórum, reprogramación o cancelación contingente). El frontend gestiona las alertas reactivas a través del componente `NotificationBell.tsx` y el servicio `notificationService.ts`, conectándose al canal de Server-Sent Events (SSE) `/api/v1/notifications/stream`. El backend `aplicacion/backend/app/api/v1/endpoints/notifications.py` y `app/services/notification_service.py` procesan eventos generados por tareas programadas de Celery/APScheduler, persisten la entidad `NotificacionEvento` (`app/models/notification.py`) en PostgreSQL y despachan simultáneamente correos electrónicos de respaldo vía SMTP universitario (`EmailService`), garantizando la notificación oportuna a mentores y estudiantes. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Estándar W3C Server-Sent Events y Protocolo SMTP RFC 5321 |
| **Anexos** | `aplicacion/frontend/src/components/NotificationBell.tsx`<br>`aplicacion/frontend/src/services/notificationService.ts` (`NotificationService`, `ApiNotificationAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/notifications.py` (`GET /api/v1/notifications/unread`, `POST /api/v1/notifications/{id}/mark-read`, `GET /api/v1/notifications/stream`)<br>`aplicacion/backend/app/services/notification_service.py` (`NotificationService.dispatch_event`, `NotificationService.get_unread`)<br>`aplicacion/backend/app/models/notification.py` (`NotificacionEvento`), `app/models/auth.py` (`Usuario`) |
| **Precondiciones** | 1. Usuario institucional autenticado con token JWT activo en la plataforma.<br>2. Evento de dominio generado en backend (e.g. evaluación de quórum, reserva formalizada, cancelación).<br>3. Servicio SMTP institucional o canal SSE operativo en el servidor. |
| **PostCondiciones** | 1. Registro insertado en la tabla física `notificaciones_eventos` con `leida = false` y marca temporal UTC.<br>2. Transmisión reactiva del mensaje a la campana de notificaciones de la interfaz cliente.<br>3. Despacho de correo electrónico de respaldo al buzón universitario del destinatario. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Conexión al canal de notificaciones e inicialización de alertas** | |
| **1.** El usuario inicia sesión en la plataforma y visualiza el componente de campana en la cabecera `NotificationBell.tsx`. | **2.** En `notificationService.ts`, se establece una conexión persistente SSE con `GET /api/v1/notifications/stream` y se despacha `GET /api/v1/notifications/unread`. En `notifications.py`, `NotificationService` consulta `SELECT * FROM notificaciones_eventos WHERE usuario_id = :uid AND leida = false ORDER BY fecha_creacion DESC`. Retorna HTTP 200 con la nómina de alertas pendientes. En `NotificationBell.tsx`, se renderiza una insignia numérica en color rojo sobre la campana indicando las notificaciones no leídas. |
| **Fase 2: Generación asíncrona de evento crítico y despacho multicanal** | |
| **3.** Un proceso del sistema en segundo plano (e.g. evaluación de quórum a T-24h en CUS-023) detecta la necesidad de alertar al usuario. | **4.** En `notification_service.py`, se invoca `dispatch_event(user_id, event_type, message, reference_id)`. Se ejecuta `INSERT INTO notificaciones_eventos (...) VALUES (...)` y se emite el evento al flujo SSE. Simultáneamente, se invoca a `EmailService.send_alert_email()` para despachar el aviso a su correo `@upt.pe`. (Si el servidor SMTP sufre timeout o indisponibilidad de red, salta a E001). |
| **Fase 3: Recepción reactiva en cliente y lectura de notificación** | |
| **5.** El usuario observa la actualización instantánea del contador en la campana y hace clic sobre el icono `NotificationBell.tsx`. | **6.** En `NotificationBell.tsx`, se abre un panel flotante desplegando las alertas ordenadas cronológicamente con distintivos de criticidad (Informativa, Alerta T-24h, Urgente). El usuario hace clic sobre una alerta específica (e.g. *"Tu sesión de mañana ha sido confirmada"*). En `notificationService.ts`, se despacha `POST /api/v1/notifications/{id}/mark-read`. El backend actualiza `leida = true` en base de datos. El sistema disminuye el contador y redirige al usuario a la vista de la sesión referenciada. |

##### Flujos de Excepción

##### Flujo de excepción E001: Falla de despacho en el servicio SMTP de respaldo
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, la pasarela de correo SMTP universitario no responde o rechaza la conexión. `EmailService` captura la excepción `SMTPException`, registra una advertencia en la bitácora de auditoría del servidor (`logger.warning("SMTP dispatch failed, falling back to SSE only")`) y preserva la entrega mediante el canal web en tiempo real sin abortar la transacción de base de datos.<br><br>En `NotificationBell.tsx`, el usuario recibe la notificación instantánea en pantalla de forma normal, manteniendo la continuidad operativa. |
| **E001-1.2** Hace clic en la campana de notificaciones y lee el mensaje directamente en la aplicación. | **E001-1.3** Marca la notificación como leída y retorna al paso 6 del Flujo Normal de Eventos. |

#### CUS-011 - Generar reportes e indicadores de analítica académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-011** (CUS-011) |
| **Nombre** | Generar reportes consolidados e indicadores analíticos de gestión de mentorías |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-025 (Tablero analítico y métricas de rendimiento académico) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional (`UserRole.administrador`), Director de Escuela EPIS, Comité de Calidad ICACIT |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a las autoridades académicas y evaluadores de acreditación generar informes estadísticos agregados sobre la cobertura, demanda y efectividad del programa de mentorías entre pares mediante el componente cliente `AnalyticsDashboardView.tsx` y el servicio `analyticsService.ts`. El backend en `aplicacion/backend/app/api/v1/endpoints/analytics.py` y `app/services/analytics_service.py` procesa las peticiones `GET /api/v1/analytics/reports/kpis` y `GET /api/v1/analytics/export`. El servicio ejecuta consultas analíticas relacionales en PostgreSQL agrupando métricas por asignatura filtro, ciclo y modalidad (horas dictadas, porcentaje de asistencia efectiva, quórum promedio alcanzado y tasa de demanda no atendida). Permite descargar el consolidado en formato de hoja de cálculo estructurada (`.xlsx` o `.csv`) con metadatos de auditoría institucional. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Criterio 4 ICACIT: Evaluación y Mejora Continua |
| **Anexos** | `aplicacion/frontend/src/components/AnalyticsDashboardView.tsx`<br>`aplicacion/frontend/src/services/analyticsService.ts` (`AnalyticsService`, `ApiAnalyticsAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/analytics.py` (`GET /api/v1/analytics/reports/kpis`, `GET /api/v1/analytics/export`)<br>`aplicacion/backend/app/services/analytics_service.py` (`AnalyticsService.calculate_kpis`, `AnalyticsService.export_report`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`), `app/models/attendance.py` (`AsistenciaSesion`), `app/models/curriculum.py` (`Curso`) |
| **Precondiciones** | 1. Usuario autenticado con rol `UserRole.administrador` o directivo verificado en JWT.<br>2. Datos de sesiones, asistencias y demandas registradas en el semestre académico consultado.<br>3. Parámetros de rango de fechas válidos dentro del calendario lectivo. |
| **PostCondiciones** | 1. Conjunto estructurado de KPIs retornado en JSON y renderizado en gráficos analíticos.<br>2. Flujo binario de hoja de cálculo generado y descargado en el navegador del usuario.<br>3. Registro de auditoría administrativa persistido en el sistema. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al panel analítico y configuración de parámetros** | |
| **1.** El administrador accede al panel de reportes en `AnalyticsDashboardView.tsx`. | **2.** En `analyticsService.ts`, se despacha `GET /api/v1/analytics/reports/kpis?semester=2026-I`. En `analytics.py`, `AnalyticsService.calculate_kpis` ejecuta consultas agregadas: total de sesiones ejecutadas, horas pedagógicas acumuladas, tasa global de asistencia efectiva y distribución porcentual por modalidad (Presencial vs Virtual). Retorna HTTP 200 con el resumen estadístico. En `AnalyticsDashboardView.tsx`, se renderizan tarjetas de indicadores clave y gráficos de barras comparativos en color azul institucional. |
| **Fase 2: Ajuste de filtros temporales y selección de formato de exportación** | |
| **3.** El usuario ajusta el rango de fechas en los selectores de inicio y fin, elige una asignatura filtro específica y selecciona el formato de salida (`Excel .xlsx` o `CSV`). | **4.** En `AnalyticsDashboardView.tsx`, se validan las fechas seleccionadas verificando que la fecha de inicio no sea posterior a la fecha de fin ni exceda la fecha actual. El usuario presiona el botón `"Exportar Informe Consolidado"`. (Si el rango de fechas es inconsistente o futuro, salta a E001). |
| **Fase 3: Generación del documento analítico y descarga segura** | |
| **5.** El usuario observa el indicador circular de compilación del reporte en el botón de exportación. | **6.** En `analyticsService.ts`, se despacha `GET /api/v1/analytics/export?format=xlsx&start_date=...&end_date=...`. En `analytics.py`, `AnalyticsService.export_report` compila el libro de cálculo estructurado con pestañas de: 1) Resumen Ejecutivo de KPIs, 2) Detalle de Sesiones Impartidas, 3) Registro Consolidado de Asistencias, y 4) Análisis de Materias Críticas. Retorna la respuesta binaria con cabecera `Content-Disposition: attachment; filename="Reporte_Mentorias_EPIS.xlsx"`. El navegador del usuario inicia la descarga automática del archivo y el sistema registra la traza de auditoría. |

##### Flujos de Excepción

##### Flujo de excepción E001: Rango de fechas inconsistente o futuro
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el validador en cliente o `analytics.py` comprueba que la fecha inicial es mayor a la final o que se ingresaron fechas futuras no transcurridas. Lanza `HTTPException(status_code=400, detail="INVALID_DATE_RANGE: El rango de fechas seleccionado es inconsistente o corresponde a períodos futuros.")`.<br><br>En `AnalyticsDashboardView.tsx`, se resaltan los campos de fecha en color rojo y se muestra una notificación de advertencia en color ámbar. |
| **E001-1.2** Modifica las fechas seleccionando un período semestral válido. | **E001-1.3** Actualiza los valores en la interfaz y retorna al paso 3 del Flujo Normal de Eventos. |

#### CUS-015 - Consultar métricas de retención y desempeño

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-015** (CUS-015) |
| **Nombre** | Consultar métricas de correlación de retención estudiantil y desempeño académico |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-025 (Tablero analítico y métricas de rendimiento académico); Criterios ICACIT de retención y graduación oportuna |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional, Comisión de Acreditación ICACIT, Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a los comités de calidad educativa evaluar el impacto del programa de mentorías en la retención estudiantil y en la reducción del índice de reprobación en materias filtro a través del componente cliente `RetentionDashboardView.tsx` y el servicio `analyticsService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/analytics.py` procesa las peticiones `GET /api/v1/analytics/retention/cohorts` y `GET /api/v1/analytics/retention/impact`. El servicio analiza estadísticamente las cohortes estudiantiles, calculando la correlación entre la participación recurrente en mentorías (asistencia >= 3 sesiones) y la tasa de aprobación de las asignaturas críticas (Cálculo, Física, Algoritmos, Estructuras de Datos). Presenta comparativas entre grupos de control (estudiantes no asistentes) y grupos participantes para respaldar las auditorías ICACIT. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Modelo de Calidad y Acreditación de Programas de Ingeniería ICACIT |
| **Anexos** | `aplicacion/frontend/src/components/RetentionDashboardView.tsx`<br>`aplicacion/frontend/src/services/analyticsService.ts` (`AnalyticsService.getRetentionMetrics`)<br>`aplicacion/backend/app/api/v1/endpoints/analytics.py` (`GET /api/v1/analytics/retention/cohorts`, `GET /api/v1/analytics/retention/impact`)<br>`aplicacion/backend/app/services/analytics_service.py` (`AnalyticsService.analyze_retention_correlation`)<br>`aplicacion/backend/app/models/attendance.py` (`AsistenciaSesion`), `app/models/curriculum.py` (`Curso`), `app/models/profile.py` (`PerfilAcademico`) |
| **Precondiciones** | 1. Usuario con credenciales administrativas o de evaluador de calidad.<br>2. Registros de calificaciones o actas académicas consolidadas de asignaturas filtro en el semestre.<br>3. Mínimo de registros estadísticos requeridos para inferencia de correlación. |
| **PostCondiciones** | 1. Métricas de retención, tasa de deserción relativa e impacto en aprobación retornadas en JSON.<br>2. Consulta de lectura analítica sin modificación de registros académicos oficiales.<br>3. Visualización de gráficos de dispersión y comparativas de cohortes en la interfaz. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al módulo de impacto y selección de cohorte** | |
| **1.** El evaluador de calidad accede a `"Impacto y Retención Académica"` en `RetentionDashboardView.tsx`. | **2.** En `analyticsService.ts`, se despacha `GET /api/v1/analytics/retention/impact`. En `analytics.py`, `AnalyticsService.analyze_retention_correlation` ejecuta la consulta de comparación: calcula el porcentaje de aprobación de estudiantes que recibieron mentoría versus el grupo de estudiantes que no participó en el programa. Retorna HTTP 200. En `RetentionDashboardView.tsx`, se renderiza un gráfico comparativo de barras dobles y un panel con la estimación de reducción del riesgo de reprobación en color azul institucional. |
| **Fase 2: Segmentación por asignatura filtro y período lectivo** | |
| **3.** El usuario selecciona una asignatura filtro específica (e.g. Estructuras de Datos) en la lista desplegable de materias y presiona `"Calcular Índice de Impacto"`. | **4.** En `RetentionDashboardView.tsx`, se envía la consulta parametrizada. En `analytics.py`, se evalúa el tamaño muestral de la asignatura. Si el número de estudiantes evaluados es suficiente (al menos 10 registros), se calcula el coeficiente de correlación y la significancia estadística. (Si la muestra disponible es menor a 10 registros estadísticos, salta a A001). |
| **Fase 3: Visualización de indicadores ICACIT y exportación** | |
| **5.** El usuario revisa los indicadores de logro académico y presiona el botón `"Exportar Evidencia ICACIT"`. | **6.** El sistema genera un resumen analítico con la tasa de retención estudiantil, la tabla de frecuencias de asistencia y las firmas de integridad del informe, descargando el archivo en formato PDF oficial para su incorporación en el expediente de acreditación. |

##### Flujos Alternativos

##### Flujo alternativo A001: Muestra insuficiente para análisis estadístico
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 4 del Flujo Normal, el servicio detecta que la asignatura seleccionada cuenta con menos de 10 estudiantes participantes en el semestre analizado. | **A001-1.2** En `RetentionDashboardView.tsx`, se despliega un panel en color ámbar: *"Muestra preliminar insuficiente para inferencia estadística significativa (< 10 registros). Se presentan únicamente métricas descriptivas básicas"*. |
| **A001-1.3** El evaluador visualiza las frecuencias absolutas sin la estimación de correlación inferencial. | **A001-1.4** El sistema ofrece la opción de ampliar el rango temporal a semestres anteriores y retorna al paso 3 del Flujo Normal de Eventos. |

#### CUS-016 - Auditar trazas de seguridad y consentimiento Ley 29733

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-016** (CUS-016) |
| **Nombre** | Auditar trazas inmutables de seguridad y consentimientos legales digitales |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-026 (Auditoría administrativa de bitácoras, accesos y seguridad); RN-02 (Registro inmutable de consentimiento legal digital Ley Nº 29733) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Oficial de Seguridad de la Información (`UserRole.administrador`), Delegado de Protección de Datos |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a los oficiales de seguridad y autoridades universitarias inspeccionar las trazas de auditoría inmutables del sistema y verificar el estricto cumplimiento de la Ley Nº 29733 (Protección de Datos Personales del Perú) mediante el componente `AuditLogView.tsx` y el servicio `auditService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/audit.py` y `app/services/audit_service.py` exponen los endpoints `GET /api/v1/audit/logs`, `GET /api/v1/audit/consent-traces` y `POST /api/v1/audit/verify-chain`. El sistema verifica la integridad criptográfica de la cadena de bloques o hashes encadenados de auditoría (donde cada registro contiene el SHA-256 del registro anterior), garantizando la no alteración de eventos críticos (inicios de sesión 2FA, modificaciones de roles, aceptaciones y revocaciones de consentimiento legal con direcciones IP y marcas temporales UTC). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Ley Nº 29733 de Protección de Datos Personales y Estándar ISO/IEC 27001 |
| **Anexos** | `aplicacion/frontend/src/components/AuditLogView.tsx`<br>`aplicacion/frontend/src/services/auditService.ts` (`AuditService`, `ApiAuditAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/audit.py` (`GET /api/v1/audit/logs`, `GET /api/v1/audit/consent-traces`, `POST /api/v1/audit/verify-chain`)<br>`aplicacion/backend/app/services/audit_service.py` (`AuditService.get_logs`, `AuditService.verify_chain_integrity`)<br>`aplicacion/backend/app/models/consent.py` (`ConsentimientoLegal`), `app/models/auth.py` (`LogAuditoriaSeguridad`) |
| **Precondiciones** | 1. Usuario autenticado portando token JWT institucional con privilegios de Oficial de Seguridad o Administrador.<br>2. Registros de auditoría y trazas de consentimiento persistidos en la base de datos PostgreSQL.<br>3. Claves criptográficas institucionales de verificación activas en el servidor. |
| **PostCondiciones** | 1. Verificación de integridad de la cadena de hashes ejecutada sin detectar corrupciones.<br>2. Consulta forense de sólo lectura generada con registros paginados e inmutables.<br>3. Exportación de expediente de trazabilidad bajo la Ley Nº 29733 con firma digital de auditoría. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del registro forense de auditoría** | |
| **1.** El oficial de seguridad accede al módulo `"Auditoría de Seguridad y Ley 29733"` en `AuditLogView.tsx`. | **2.** En `auditService.ts`, se despacha `GET /api/v1/audit/logs?limit=50`. En `audit.py`, se valida el token con `require_security_officer_role`. `AuditService` ejecuta `SELECT l.*, u.email FROM log_auditoria_seguridad l JOIN usuarios u ON l.usuario_id = u.id ORDER BY l.id DESC LIMIT 50`. Retorna HTTP 200 con la nómina paginada. En `AuditLogView.tsx`, se renderiza una tabla con filtros por fecha, tipo de evento (`AUTH_2FA`, `ROLE_CHANGE`, `CONSENT_ACCEPT`, `CONSENT_REVOKE`), IP de origen y hash de bloque. (Si el usuario no cuenta con privilegios de seguridad, salta a E001). |
| **Fase 2: Filtrado por usuario y verificación de traza legal de consentimiento** | |
| **3.** El oficial introduce el correo institucional de un estudiante o docente en el buscador para auditar su historial de consentimiento digital. | **4.** En `auditService.ts`, se despacha `GET /api/v1/audit/consent-traces?email=...`. El backend retorna la secuencia completa de formalización: UUID, versión de términos aceptada, IP de origen, User-Agent, fecha UTC y estado de revocación. `AuditLogView.tsx` despliega el expediente digital del titular de los datos. |
| **Fase 3: Verificación criptográfica de la cadena de auditoría (Hash Chain)** | |
| **5.** El oficial presiona el botón `"Verificar Integridad de Cadena de Logs"`. | **6.** En `auditService.ts`, se despacha `POST /api/v1/audit/verify-chain`. En `audit_service.py`, se itera secuencialmente por la tabla de auditoría recomputando recursivamente `SHA256(registro_anterior_hash + registro_actual_data)` y comparándolo con el valor almacenado en `hash_bloque`. Al comprobar que todas las firmas coinciden, retorna HTTP 200 `{"status": "VALID", "records_verified": count, "tampering_detected": false}`. En `AuditLogView.tsx`, se despliega una insignia destacada en color verde con la leyenda *"Cadena de Auditoría Íntegra y Verificada (0 Alteraciones)"* y se habilita el botón de exportación de expediente legal. (Si el sistema detecta una inconsistencia en la cadena de hashes, salta a E002). |

##### Flujos de Excepción

##### Flujo de excepción E001: Permisos insuficientes para auditoría de seguridad
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, el interceptor de seguridad en `audit.py` comprueba que el token JWT carece de rol de Oficial de Seguridad o Administrador Institucional. Lanza `HTTPException(status_code=403, detail="FORBIDDEN_AUDIT: Acceso restringido. Se requieren credenciales de Oficial de Seguridad para auditar registros forenses.")`.<br><br>En `App.tsx`, se captura el error 403 y se redirige al panel estándar del usuario desplegando una alerta en color rojo. |
| **E001-1.2** Hace clic en el botón "Aceptar" en la alerta de restricción. | **E001-1.3** Cierra el aviso y retorna al paso 1 del Flujo Normal de Eventos en su vista autorizada. |

##### Flujo de excepción E002: Inconsistencia detectada en la cadena criptográfica de logs
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 6 del Flujo Normal, `AuditService.verify_chain_integrity` detecta una discrepancia entre el hash recalculado y el hash almacenado en un bloque específico (evidencia de manipulación o corrupción de datos). Lanza `HTTPException(status_code=409, detail="AUDIT_TAMPERING_DETECTED: ¡Alerta Crítica! Se detectó una inconsistencia en la cadena de hashes en el registro ID {broken_id}.")`.<br><br>En `AuditLogView.tsx`, la interfaz conmuta inmediatamente a un estado de alarma en color rojo parpadeante, resalta la fila alterada y genera una entrada prioritaria en el sistema de seguridad institucional. |
| **E002-1.2** Presiona el botón "Descargar Informe Forense de Incidencia". | **E002-1.3** Emite el volcado forense de la discrepancia para su remisión a las autoridades universitarias y finaliza el caso de uso registrando el incidente de seguridad institucional. |

#### CUS-020 - Configurar parámetros institucionales y umbrales

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-020** (CUS-020) |
| **Nombre** | Configurar parámetros operativos institucionales y umbrales de gobernanza |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-024 (Priorización institucional y realce algorítmico); RN-04 (Umbral temporal T-24h), RN-05 (Aforos máximos 10 y 20), RN-10 (Quórum mínimo de 3 estudiantes), RN-14 (Horas de acreditación) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional (`UserRole.administrador`), Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a las autoridades de la EPIS-UPT parametrizar y calibrar las reglas de negocio globales y umbrales operacionales del sistema sin requerir modificaciones en el código fuente a través del componente cliente `SystemSettingsView.tsx` y el servicio `configService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/config.py` y `app/services/config_service.py` procesan las peticiones `GET /api/v1/config/parameters` y `PUT /api/v1/config/parameters`. El administrador puede ajustar los aforos máximos presenciales y virtuales (RN-05), la ventana de antelación obligatoria para reservas y cancelaciones (RN-04), el quórum mínimo para confirmación automática de sesiones (RN-10) y el umbral de horas acumuladas para emisión de constancias (RN-14). Los parámetros se persisten en la tabla `parametros_institucionales` (`app/models/config.py`), invalidan la caché global de la aplicación y registran una traza auditada de modificación. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Reglamento General de Mentorías Universitarias EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/SystemSettingsView.tsx`<br>`aplicacion/frontend/src/services/configService.ts` (`ConfigService`, `ApiConfigAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/config.py` (`GET /api/v1/config/parameters`, `PUT /api/v1/config/parameters`)<br>`aplicacion/backend/app/services/config_service.py` (`ConfigService.get_parameters`, `ConfigService.update_parameters`)<br>`aplicacion/backend/app/models/config.py` (`ParametroInstitucional`), `app/models/auth.py` (`LogAuditoriaSeguridad`) |
| **Precondiciones** | 1. Administrador institucional autenticado con token JWT portando claim `administrador`.<br>2. Catálogo de parámetros base inicializado en la tabla `parametros_institucionales`.<br>3. Autenticación de doble factor reconfirmada para modificaciones críticas de configuración. |
| **PostCondiciones** | 1. Registro actualizado en la tabla física `parametros_institucionales` en PostgreSQL.<br>2. Invalidación atómica de la caché en memoria del servidor de aplicaciones.<br>3. Despliegue de confirmación en cliente y aplicación inmediata de los nuevos umbrales operacionales. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de parámetros vigentes y despliegue del panel** | |
| **1.** El administrador accede a `"Configuración del Sistema"` en `SystemSettingsView.tsx`. | **2.** En `configService.ts`, se despacha `GET /api/v1/config/parameters`. En `config.py`, se valida el rol administrativo. `ConfigService.get_parameters` ejecuta `SELECT clave, valor, descripcion, tipo_dato, valor_min, valor_max FROM parametros_institucionales WHERE activo = true`. Retorna HTTP 200 con el diccionario de parámetros. En `SystemSettingsView.tsx`, se renderiza un formulario organizado por categorías: 1) Aforos Institucionales (Presencial máx 10, Virtual máx 20), 2) Ventana de Antelación (24 horas), 3) Quórum Mínimo (3 confirmados), y 4) Horas de Certificación (20 horas). |
| **Fase 2: Edición de umbrales y validación de rangos permitidos** | |
| **3.** El administrador modifica uno o más valores numéricos (e.g. ajusta el quórum mínimo a 4 estudiantes para períodos de alta demanda) y presiona el botón `"Guardar Parámetros Institucionales"`. | **4.** En `SystemSettingsView.tsx`, se ejecutan validaciones en cliente comprobando que los nuevos valores se encuentren dentro de los rangos operacionales permitidos (`valor_min <= valor <= valor_max`). En `configService.ts`, se despacha `PUT /api/v1/config/parameters` con el payload `ParameterUpdatePayload`. En `config.py`, el controlador valida el esquema y delega a `config_service.py`. (Si un parámetro numérico excede los límites institucionales de seguridad, salta a E001). (Si la sesión requiere reautenticación administrativa para cambios críticos, salta a E002). |
| **Fase 3: Persistencia transaccional, purga de caché y aplicación en caliente** | |
| **5.** El administrador observa el indicador circular de guardado seguro. | **6.** En `config_service.py`, se inicia una transacción ACID. Se ejecutan las sentencias `UPDATE parametros_institucionales SET valor = :val, fecha_modificacion = NOW(), modificado_por = :uid WHERE clave = :key`. Se inserta el evento en `log_auditoria_seguridad`. Se confirma la transacción con `db.commit()`. El servicio purga la caché interna del servidor para forzar la recarga de los nuevos umbrales en todos los módulos dependientes (ofertas, reservas y quórum). Retorna HTTP 200 con los parámetros actualizados. En cliente, `SystemSettingsView.tsx` despliega una notificación flotante en color verde de éxito: *"Parámetros institucionales actualizados y aplicados en caliente exitosamente"*. |

##### Flujos de Excepción

##### Flujo de excepción E001: Parámetro fuera de los rangos institucionales permitidos
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `config_service.py` comprueba que el valor propuesto supera los límites de seguridad institucional (e.g. se intenta fijar un aforo presencial mayor a 30 cupos excediendo la capacidad de los laboratorios). Lanza `HTTPException(status_code=422, detail="PARAMETER_OUT_OF_BOUNDS: El valor ingresado para '{param_key}' excede los límites operacionales autorizados por la Dirección de Escuela.")`.<br><br>En `SystemSettingsView.tsx`, se resalta el campo observado en color rojo y se muestra el rango admisible. |
| **E001-1.2** Corrige el valor ingresando un número dentro del rango permitido. | **E001-1.3** Rehabilita el botón de guardado y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Reautenticación de seguridad requerida
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, al modificar parámetros de gobernanza crítica, el sistema exige reconfirmación de clave o token OTP. Si el administrador no suministra la clave secundaria, `config.py` lanza `HTTPException(status_code=401, detail="REAUTH_REQUIRED: Se requiere confirmación de credenciales para modificar parámetros de gobernanza crítica.")`.<br><br>En `SystemSettingsView.tsx`, se abre una ventana modal solicitando la confirmación de identidad institucional. |
| **E002-1.2** Ingresa su contraseña institucional o código OTP de confirmación y presiona "Verificar". | **E002-1.3** Valida las credenciales secundarias y retorna al paso 4 del Flujo Normal de Eventos. |

#### CUS-022 - Gestionar catálogo de temas y materias críticas

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-022** (CUS-022) |
| **Nombre** | Gestionar catálogo de temas curriculares, asignaturas filtro y malla oficial |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-005 (Gestión del catálogo de asignaturas y temarios), RF-026 (Auditoría administrativa de bitácoras y materias); RN-11 (Asignaturas filtro prioritarias) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional (`UserRole.administrador`), Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a la Dirección de Escuela y a los administradores actualizar la malla curricular de la EPIS-UPT, gestionar las asignaturas designadas como materias filtro (`es_filtro = true`) y dar de alta, modificar o desactivar temas silábicos de aprendizaje a través del componente cliente `AdminCurriculumView.tsx` y el servicio `curriculumService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/curriculum.py` y `app/services/curriculum_service.py` procesan las peticiones `POST /api/v1/curriculum/courses`, `PUT /api/v1/curriculum/courses/{id}`, `POST /api/v1/curriculum/courses/{id}/topics` y `DELETE /api/v1/curriculum/topics/{id}`. El servicio valida que los temas ingresados correspondan a las unidades didácticas del semestre lectivo vigente (semanas 1 a 17), previene duplicidades conceptuales mediante comprobaciones de unicidad en `temas_curriculares` (`app/models/curriculum.py`) y asegura la consistencia referencial con las ofertas de mentoría y solicitudes de demanda en curso. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-02: Gestión Curricular y Perfiles Académicos)<br>Plan de Estudios y Sílabos Oficiales de Ingeniería de Sistemas UPT |
| **Anexos** | `aplicacion/frontend/src/components/AdminCurriculumView.tsx`<br>`aplicacion/frontend/src/services/curriculumService.ts` (`CurriculumService.manageCurriculum`)<br>`aplicacion/backend/app/api/v1/endpoints/curriculum.py` (`POST /api/v1/curriculum/courses`, `POST /api/v1/curriculum/courses/{id}/topics`)<br>`aplicacion/backend/app/services/curriculum_service.py` (`CurriculumService.create_course`, `CurriculumService.manage_topics`)<br>`aplicacion/backend/app/models/curriculum.py` (`Carrera`, `Curso`, `TemaCurricular`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Usuario con credenciales de Administrador Institucional o Director de Escuela.<br>2. Plan de estudios registrado en la tabla `carreras` en la base de datos.<br>3. Número de semana lectiva comprendido entre las semanas 1 y 17 del calendario académico. |
| **PostCondiciones** | 1. Entidad `Curso` o `TemaCurricular` insertada o actualizada en la tabla física de PostgreSQL.<br>2. Transacción ACID confirmada con `db.commit()` e indexación para el motor de búsqueda.<br>3. Actualización reactiva del árbol curricular en la interfaz administrativa. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del árbol curricular y selección de asignatura** | |
| **1.** El administrador accede a `"Gestión de Malla y Temarios"` en `AdminCurriculumView.tsx`. | **2.** En `curriculumService.ts`, se despacha `GET /api/v1/curriculum/courses`. En `curriculum.py`, `curriculum_service.py` recupera la estructura completa de asignaturas ordenadas por ciclo. En `AdminCurriculumView.tsx`, se renderiza una vista en árbol con las materias clasificadas por ciclo y la etiqueta *"Materia Filtro"* en aquellas con `es_filtro = true`. El administrador hace clic sobre una asignatura específica para desplegar sus temas silábicos. |
| **Fase 2: Ingreso de datos del nuevo tema curricular silábico** | |
| **3.** El administrador presiona el botón `"Agregar Nuevo Tema Curricular"` en el panel de la asignatura. | **4.** En `AdminCurriculumView.tsx`, se abre una ventana modal con los campos: número de unidad didáctica (1 a 4), título descriptivo del tema, semana académica programada (semanas 1 a 17) y descripción conceptual. El administrador completa los campos y pulsa el botón `"Registrar Tema Curricular"`. (Si el título del tema ya existe en esa misma unidad, salta a E001). (Si el número de semana está fuera del calendario lectivo de 1 a 17, salta a E002). |
| **Fase 3: Persistencia transaccional y actualización del catálogo** | |
| **5.** El administrador observa el indicador circular de guardado en el botón del modal. | **6.** En `curriculumService.ts`, se despacha `POST /api/v1/curriculum/courses/{id}/topics` con el payload `TopicCreateRequest`. En `curriculum.py`, `curriculum_service.py` inicia la transacción con `db.begin()`. Valida que el curso exista y que no exista una tupla idéntica `(curso_id, unidad, titulo)`. Inserta en `temas_curriculares`, ejecuta `db.commit()` y retorna HTTP 201 Created. En cliente, `AdminCurriculumView.tsx` cierra el modal, añade el nuevo tema al árbol curricular en pantalla y despliega una notificación flotante en color verde de éxito: *"Tema curricular registrado y disponible para ofertas y demandas académicas"*. |

##### Flujos de Excepción

##### Flujo de excepción E001: Tema curricular duplicado en la misma unidad
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `curriculum_service.py` detecta que ya existe un tema con el mismo título para la misma unidad didáctica del curso. Lanza `HTTPException(status_code=409, detail="DUPLICATE_TOPIC: Ya existe un tema curricular registrado con ese título para la unidad seleccionada.")`.<br><br>En `AdminCurriculumView.tsx`, se resalta el cuadro de texto del título en color rojo con el mensaje de duplicidad. |
| **E001-1.2** Modifica el título del tema especificando con mayor precisión el contenido temático. | **E001-1.3** Rehabilita el botón de guardado en el modal y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Número de semana lectiva fuera de rango semestral
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, Pydantic en `curriculum.py` comprueba que el campo `semana` es menor a 1 o mayor a 17 (duración máxima del semestre lectivo universitario). Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: El número de semana académica debe estar comprendido estrictamente entre 1 y 17.")`.<br><br>En `AdminCurriculumView.tsx`, se resalta el campo numérico de semana en color rojo. |
| **E002-1.2** Ingresa un número de semana válido dentro del intervalo 1 a 17. | **E002-1.3** Actualiza el valor en el estado del formulario y retorna al paso 4 del Flujo Normal de Eventos. |
"""
