# -*- coding: utf-8 -*-
"""
Modulo 06: Asistencia, Bitácoras y Feedback (Fase de Diseño)
Contiene: CUS-012, CUS-013, CUS-014
"""

def get_mod06():
    return """### MOD-06: Asistencia, Bitácoras y Feedback

#### CUS-012 - Registrar asistencia a sesión de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-012** (CUS-012) |
| **Nombre** | Registrar asistencia interactiva a sesión de mentoría mediante código QR dinámico |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-017 (Registro de bitácora pedagógica y control de asistencia); RN-05 (Aforo y presencia efectiva), RN-12 (Trazabilidad de asistencia y ventana temporal de check-in) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 |
| **Descripción** | Permite registrar la presencia efectiva de los estudiantes durante la ejecución de una sesión de mentoría a través del componente cliente `SessionAttendanceView.tsx` y el servicio `attendanceService.ts`. El mentor proyecta o comparte un código QR dinámico cifrado basado en TOTP que rota cada 30 segundos. El estudiante mentoreado escanea el código o digita el pase numérico de 6 dígitos despachando `POST /api/v1/sessions/{id}/attendance/check-in` hacia el backend en `aplicacion/backend/app/api/v1/endpoints/attendance.py`. El servicio `AttendanceService` valida que la solicitud se produzca dentro de la ventana de la sesión (desde 15 minutos antes del inicio hasta 30 minutos tras el fin), comprueba que el estudiante posea una reserva en estado `CONFIRMADA` y persiste el registro en la tabla `asistencias_sesion` (`app/models/attendance.py`) con timestamp UTC y geolocalización o IP institucional, transmitiendo el evento en tiempo real vía WebSockets al panel del mentor. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-06: Trazabilidad, Bitácoras y Evaluación)<br>Reglamento Académico de Control de Asistencia y Acreditación EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/SessionAttendanceView.tsx`<br>`aplicacion/frontend/src/services/attendanceService.ts` (`AttendanceService`, `ApiAttendanceAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/attendance.py` (`POST /api/v1/sessions/{id}/attendance/check-in`, `GET /api/v1/sessions/{id}/attendance`)<br>`aplicacion/backend/app/services/attendance_service.py` (`AttendanceService.record_checkin`, `AttendanceService.get_roster`)<br>`aplicacion/backend/app/models/attendance.py` (`AsistenciaSesion`), `app/models/booking.py` (`ReservaCupo`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Sesión de mentoría en estado `CONFIRMADA` o `EN_CURSO` en la base de datos.<br>2. Estudiante mentoreado con reserva en estado `CONFIRMADA` en la tabla `reservas_cupo`.<br>3. Petición ejecutada dentro de la ventana temporal de validez de la sesión [inicio - 15m, fin + 30m]. |
| **PostCondiciones** | 1. Registro insertado o actualizado en la tabla física `asistencias_sesion` con `asistio = true`.<br>2. Transmisión del evento de presencia en tiempo real al panel del mentor.<br>3. Despliegue del comprobante de asistencia en la interfaz del mentoreado y habilitación de encuesta de calidad post-mentoría. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura de sesión y generación de token dinámico de asistencia** | |
| **1.** El mentor accede a la sesión activa en `SessionAttendanceView.tsx` y pulsa el botón `"Iniciar Pase de Asistencia Digital"`. | **2.** En `attendanceService.ts`, se despacha `GET /api/v1/sessions/{id}/attendance/token`. El backend genera un token criptográfico TOTP con ventana de rotación de 30 segundos y lo serializa en un código QR interactivo proyectado en la pantalla del mentor junto con la nómina de estudiantes con reserva confirmada en estado provisional *"Ausente"*. |
| **Fase 2: Escaneo de código QR y validación de reserva y ventana horaria** | |
| **3.** El mentoreado presente en la sesión escanea el código QR desde su dispositivo móvil o ingresa el código numérico de 6 dígitos en su aplicación y pulsa `"Registrar Mi Asistencia"`. | **4.** En `attendanceService.ts`, se despacha `POST /api/v1/sessions/{id}/attendance/check-in` con payload `{"session_id": id, "qr_token": token}`. En `attendance.py`, `AttendanceService.record_checkin` valida: 1) que el token TOTP no haya expirado, 2) que el estudiante mantenga una reserva en estado `CONFIRMADA`, 3) que la hora actual esté dentro del intervalo de la sesión (`fecha_inicio - 15m <= now_utc <= fecha_fin + 30m`). (Si el token TOTP o código numérico ha expirado, salta a E001). (Si el estudiante no cuenta con reserva confirmada en la sesión, salta a E002). (Si el check-in se intenta fuera del intervalo temporal permitido, salta a E003). |
| **Fase 3: Persistencia de asistencia y actualización reactiva en tiempo real** | |
| **5.** El estudiante y el mentor observan la actualización instantánea en pantalla. | **6.** En `attendance_service.py`, se ejecuta `INSERT INTO asistencias_sesion (sesion_id, estudiante_id, fecha_checkin, asistio, ip_origen) VALUES (...) ON CONFLICT (sesion_id, estudiante_id) DO UPDATE SET asistio = true, fecha_checkin = NOW()`. Se confirma la transacción con `db.commit()`. El servidor emite un evento WebSocket hacia el panel del mentor, actualizando la fila del estudiante a estado *"Presente"* con un distintivo en color verde. En el dispositivo del mentoreado, se muestra una notificación de éxito: *"¡Asistencia registrada exitosamente! Gracias por tu puntualidad."* |

##### Flujos de Excepción

##### Flujo de excepción E001: Código QR o token TOTP expirado
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `AttendanceService` comprueba que el token TOTP superó su ciclo de vida de 30 segundos. Lanza `HTTPException(status_code=400, detail="QR_TOKEN_EXPIRED: El código de asistencia ha expirado. Por favor, escanee el código QR actualizado proyectado por el mentor.")`.<br><br>En el cliente del estudiante, se despliega una advertencia en color ámbar solicitando enfocar el nuevo código dinámico. Presenta el botón `<button onClick={handleRetryScan}>Escanear Nuevo Código</button>`. |
| **E001-1.2** Hace clic en el botón "Escanear Nuevo Código" y enfoca la pantalla del mentor. | **E001-1.3** Captura el nuevo token TOTP y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Estudiante sin reserva previa confirmada
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, la consulta relacional detecta que el estudiante no posee una tupla en `reservas_cupo` con `estado = 'CONFIRMADA'`. Lanza `HTTPException(status_code=403, detail="NO_CONFIRMED_BOOKING: No registra una reserva confirmada para esta sesión de mentoría.")`.<br><br>En la interfaz del estudiante, se muestra una alerta en color rojo indicando que solo los estudiantes debidamente inscritos y ratificados a T-24h pueden registrar su asistencia. |
| **E002-1.2** Hace clic en el botón "Entendido" en la alerta de restricción. | **E002-1.3** Cierra el escáner y finaliza la interacción sin registrar presencia. |

##### Flujo de excepción E003: Check-in fuera del intervalo temporal reglamentario
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 4 del Flujo Normal, el servicio comprueba que la hora actual del servidor se ubica fuera del intervalo de tolerancia reglamentaria (más de 15 minutos antes del inicio o más de 30 minutos después de concluida la sesión). Lanza `HTTPException(status_code=400, detail="CHECKIN_WINDOW_CLOSED: El pase de asistencia sólo está habilitado durante la realización de la sesión.")`.<br><br>En la interfaz del estudiante, se despliega un mensaje en color rojo indicando que el registro de asistencia se encuentra cerrado. |
| **E003-1.2** Hace clic en el botón "Aceptar". | **E003-1.3** Redirige a la vista principal y finaliza el caso de uso sin generar registros en la base de datos. |

#### CUS-013 - Registrar bitácora académica de sesión

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-013** (CUS-013) |
| **Nombre** | Registrar bitácora pedagógica y reporte formativo de sesión de mentoría |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-017 (Registro de bitácora pedagógica y control de asistencia); RN-12 (Plazo máximo de 48 horas post-sesión para registro de bitácora) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Coordinador Académico |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 |
| **Descripción** | Permite al estudiante mentor consignar el reporte pedagógico de la sesión de mentoría recién concluida a través del formulario `BitacoraFormView.tsx` y el servicio `bitacoraService.ts`. El mentor detalla los temas específicos del sílabo abordados, el nivel de asimilación conceptual de los participantes, las dificultades pedagógicas observadas y las observaciones institucionales. La petición se despacha mediante `POST /api/v1/sessions/{id}/bitacora` hacia el backend en `aplicacion/backend/app/api/v1/endpoints/bitacora.py`. El servicio `BitacoraService` valida que la sesión se encuentre en estado `CONCLUIDA`, que el plazo transcurrido desde el fin de la sesión no exceda las 48 horas reglamentarias (RN-12) y que el texto pedagógico supere los 50 caracteres mínimos. Persiste la entidad `BitacoraPedagogica` (`app/models/bitacora.py`) vinculada a la sesión y actualiza el estado a `BITACORA_REGISTRADA` para su posterior visado administrativo. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-06: Trazabilidad, Bitácoras y Evaluación)<br>Reglamento Académico de Mentorías y Certificación de Horas EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/BitacoraFormView.tsx`<br>`aplicacion/frontend/src/services/bitacoraService.ts` (`BitacoraService`, `ApiBitacoraAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/bitacora.py` (`POST /api/v1/sessions/{id}/bitacora`, `GET /api/v1/sessions/{id}/bitacora`)<br>`aplicacion/backend/app/services/bitacora_service.py` (`BitacoraService.create_bitacora`)<br>`aplicacion/backend/app/models/bitacora.py` (`BitacoraPedagogica`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Mentor titular con sesión institucional autenticada.<br>2. Sesión de mentoría en estado `CONCLUIDA` en la base de datos.<br>3. Plazo posterior a la finalización de la sesión menor o igual a 48 horas (`now_utc <= fecha_fin + 48h`). |
| **PostCondiciones** | 1. Registro insertado en la tabla `bitacoras_pedagogicas` con código de firma digital SHA-256.<br>2. Estado de `SesionMentoria` actualizado a `BITACORA_REGISTRADA` en PostgreSQL.<br>3. Despliegue de confirmación en cliente y habilitación de las horas para acreditación institucional. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura de bitácora y verificación de plazo límite** | |
| **1.** El mentor ingresa a la sesión concluida en `BitacoraFormView.tsx` y presiona el botón `"Completar Bitácora Pedagógica"`. | **2.** En `bitacoraService.ts`, se invoca la verificación de estado de la sesión. El backend comprueba que la sesión finalizó y que `now_utc <= fecha_fin + timedelta(hours=48)` (RN-12). En `BitacoraFormView.tsx`, se renderiza el formulario pedagógico: lista de temas silábicos cubiertos con casillas de verificación, selector de nivel de dificultad (Bajo, Medio, Alto), cuadro de texto para observaciones pedagógicas y declaración jurada de veracidad. (Si han transcurrido más de 48 horas desde el cierre de la sesión, salta a E001). |
| **Fase 2: Ingreso de evidencias pedagógicas y validación de contenido** | |
| **3.** El mentor marca los temas curriculares explicados, selecciona el nivel de asimilación, redacta las incidencias pedagógicas y presiona el botón `"Guardar y Firmar Bitácora"`. | **4.** En `BitacoraFormView.tsx`, se valida que las observaciones pedagógicas posean una extensión mínima de 50 caracteres y no contengan scripts. En `bitacoraService.ts`, se despacha `POST /api/v1/sessions/{id}/bitacora` con el payload `BitacoraCreateRequest`. En `bitacora.py`, `BitacoraService.create_bitacora` valida la firma del mentor y el esquema de datos. (Si la descripción pedagógica no alcanza el mínimo de 50 caracteres, salta a E002). |
| **Fase 3: Persistencia transaccional y certificación de horas** | |
| **5.** El mentor observa la barra de progreso mientras se genera el hash de integridad de la bitácora. | **6.** En `bitacora_service.py`, se calcula el hash criptográfico SHA-256 sobre el contenido pedagógico y se ejecuta `INSERT INTO bitacoras_pedagogicas (sesion_id, mentor_id, temas_cubiertos, observaciones, nivel_dificultad, hash_firma, fecha_registro) VALUES (...)`. Se actualiza `sesiones_mentoria.estado = 'BITACORA_REGISTRADA'`. Se confirma la transacción con `db.commit()` y se retorna HTTP 201 Created. En cliente, `BitacoraFormView.tsx` muestra un panel de confirmación en color verde con el código de firma digital y redirige al historial de sesiones. |

##### Flujos de Excepción

##### Flujo de excepción E001: Plazo límite de 48 horas vencido
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `bitacora_service.py` evalúa `now_utc > sesion.fecha_fin + timedelta(hours=48)`. Lanza `HTTPException(status_code=400, detail="DEADLINE_EXCEEDED: El plazo reglamentario de 48 horas para registrar la bitácora ha vencido.")`.<br><br>En `BitacoraFormView.tsx`, se deshabilita la edición del formulario y se muestra una advertencia en color rojo indicando que la bitácora quedó fuera de plazo reglamentario y requiere solicitud de desbloqueo administrativo ante la Dirección de Escuela. |
| **E001-1.2** Hace clic en el botón "Solicitar Desbloqueo a Coordinación". | **E001-1.3** Abre un formulario de solicitud de prórroga y finaliza la interacción sin registrar la bitácora ordinaria. |

##### Flujo de excepción E002: Descripción pedagógica insuficiente o vacía
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, el validador Pydantic en `bitacora.py` comprueba que el campo de observaciones tiene menos de 50 caracteres. Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: Las observaciones pedagógicas deben contener una descripción sustantiva de al menos 50 caracteres.")`.<br><br>En `BitacoraFormView.tsx`, se resalta el cuadro de texto en color rojo y se muestra un contador de caracteres indicando los faltantes. |
| **E002-1.2** Amplía la descripción pedagógica detallando el desarrollo de la sesión hasta superar los 50 caracteres. | **E002-1.3** Actualiza el contador de caracteres en la interfaz y retorna al paso 3 del Flujo Normal de Eventos. |

#### CUS-014 - Visualizar historial y bitácoras académicas

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-014** (CUS-014) |
| **Nombre** | Visualizar historial académico integral de sesiones y bitácoras pedagógicas |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-019 (Consulta de historial cronológico individual de sesiones y asistencias) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor, Estudiante Mentoreado, Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 05 - Sprint 06 |
| **Descripción** | Permite a los usuarios consultar su trayectoria histórica dentro del programa de mentorías académicas a través del componente cliente `HistorySessionsView.tsx` y el servicio `historyService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/history.py` y `app/services/history_service.py` procesan las peticiones `GET /api/v1/history/sessions` y `GET /api/v1/history/bitacora/{session_id}`. Para los mentoreados, el sistema presenta la relación cronológica de sesiones a las que asistió con sus comprobantes y temas repasados. Para los mentores, despliega las sesiones impartidas, las bitácoras pedagógicas suscritas con su hash de firma digital y el estado de validación de horas ante la Dirección de Escuela. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-06: Trazabilidad, Bitácoras y Evaluación)<br>Reglamento Académico de Seguimiento Estudiantil EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/HistorySessionsView.tsx`<br>`aplicacion/frontend/src/services/historyService.ts` (`HistoryService`, `ApiHistoryAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/history.py` (`GET /api/v1/history/sessions`, `GET /api/v1/history/bitacora/{session_id}`)<br>`aplicacion/backend/app/services/history_service.py` (`HistoryService.get_user_history`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`), `app/models/bitacora.py` (`BitacoraPedagogica`), `app/models/attendance.py` (`AsistenciaSesion`) |
| **Precondiciones** | 1. Usuario institucional autenticado con token JWT activo en la plataforma.<br>2. Registros históricos persistidos en las tablas de sesiones, bitácoras o asistencias. |
| **PostCondiciones** | 1. Respuesta JSON paginada con el historial cronológico y metadatos pedagógicos retornada al cliente.<br>2. Operación idempotente de lectura sin alteraciones destructivas en la base de datos.<br>3. Renderizado de la línea de tiempo interactiva con opciones de filtrado por ciclo y asignatura. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del historial y aplicación de filtros cronológicos** | |
| **1.** El usuario hace clic en `"Mi Historial"` en el menú lateral de navegación de `HistorySessionsView.tsx`. | **2.** En `historyService.ts`, se despacha `GET /api/v1/history/sessions` enviando el token institucional. En `history.py`, `HistoryService.get_user_history` recupera las sesiones en que el usuario participó (como mentor o mentoreado) ordenadas de forma cronológica descendente. Retorna HTTP 200 con la nómina histórica. `HistorySessionsView.tsx` renderiza las tarjetas de sesiones en una línea de tiempo interactiva con distintivos por estado (`Concluida`, `Bitácora Registrada`, `Visada`). (Si el usuario es nuevo y no registra historial de sesiones, salta a A001). |
| **Fase 2: Búsqueda y filtrado por materia o período académico** | |
| **3.** El usuario filtra por semestre académico o escribe el nombre de una materia en el cuadro de búsqueda. | **4.** En `HistorySessionsView.tsx`, se actualiza reactivamente la lista de tarjetas en pantalla. El usuario hace clic sobre una sesión concluida para consultar el detalle pedagógico. |
| **Fase 3: Visualización de bitácora pedagógica y comprobante de asistencia** | |
| **5.** El usuario presiona el botón `"Ver Bitácora Pedagógica"` en la tarjeta seleccionada. | **6.** En `historyService.ts`, se despacha `GET /api/v1/history/bitacora/{session_id}`. El backend valida los permisos de lectura y retorna el registro de `BitacoraPedagogica` incluyendo los temas abordados, el nivel de dificultad, las observaciones y la firma digital SHA-256. `HistorySessionsView.tsx` despliega una ventana modal con el desglose formal de la bitácora y el botón de exportación en formato legible. |

##### Flujos Alternativos

##### Flujo alternativo A001: Historial académico vacío para usuario nuevo
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 2 del Flujo Normal, la consulta histórica retorna cero registros para el usuario. | **A001-1.2** En `HistorySessionsView.tsx`, se despliega un panel amigable en color azul institucional con el mensaje: *"Aún no registras sesiones de mentoría en tu historial. Comienza explorando la cartelera de recomendaciones para inscribirte en un tema"*. Presenta el botón `<button onClick={handleGoToBillboard}>Explorar Cartelera</button>`. |
| **A001-1.3** El usuario hace clic en el botón "Explorar Cartelera". | **A001-1.4** El sistema redirige al componente `RecommendationFeedView.tsx` y retorna al paso 1 del Flujo Normal de Eventos de CUS-002. |
"""
