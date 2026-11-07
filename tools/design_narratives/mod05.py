# -*- coding: utf-8 -*-
"""
Modulo 05: Quórum, Confirmación y Cancelaciones (Fase de Diseño)
Contiene: CUS-004, CUS-024, CUS-017, CUS-023, CUS-007
"""

def get_mod05():
    return """### MOD-05: Quórum, Confirmación y Cancelaciones

#### CUS-004 - Reservar cupo de mentoría académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-004** (CUS-004) |
| **Nombre** | Reservar cupo de mentoría académica con control de aforo y concurrencia |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-012 (Reserva de cupos con control de aforo y concurrencia; trazabilidad técnica hacia RF-002, RF-006, RF-013 y RF-014) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`), Administrador Institucional (`UserRole.administrador`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite formalizar una reserva provisional de cupo en estado `PENDIENTE_CONFIRMACION` mediante una petición `POST /api/v1/bookings/reserve` despachada desde el componente cliente `BookingModalView.tsx` hacia el controlador FastAPI `bookings.py`. El backend ejecuta validaciones de seguridad con `decode_access_token` en `app/core/security.py`, comprueba la vigencia del consentimiento legal con `ConsentService.get_consent_status`, adquiere el cerrojo en memoria `_booking_lock` y ejecuta una transacción en PostgreSQL bajo bloqueo pesimista de fila `SELECT ... FOR UPDATE OF sesiones_mentoria` con `SET LOCAL lock_timeout = '5.0s'`. Comprueba que `occupied_seats < sesion.aforo_maximo` (10 presencial / 20 virtual, RN-05) y la antelación mayor a 24 horas (`sesion.fecha_inicio > now_utc + 24h`, RN-04). Genera la entidad ORM `ReservaCupo` con código alfanuméricamente secuencial y hash criptográfico SHA-256 (`ticket_hash`), confirma la transacción con `db.commit()` y retorna el payload serializado `BookingResponse` (HTTP 201 Created). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Ley Nº 29733 de Protección de Datos Personales del Perú y D.S. Nº 003-2013-JUS |
| **Anexos** | `aplicacion/frontend/src/components/BookingModalView.tsx`<br>`aplicacion/frontend/src/components/RecommendationFeedView.tsx`<br>`aplicacion/frontend/src/services/bookingService.ts` (`BookingService`, `ApiBookingAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/reserve`)<br>`aplicacion/backend/app/services/booking_service.py` (`BookingService.reserve_seat`)<br>`aplicacion/backend/app/models/booking.py` (`ReservaCupo`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Token JWT institucional activo en `localStorage` firmado criptográficamente con claim `sub` conteniendo un correo institucional `@upt.pe`.<br>2. Registro de consentimiento persistido en la tabla `consentimientos_legales` con campo `revocado = false`.<br>3. Registro en `sesiones_mentoria` con `estado = 'PUBLICADA'` y `fecha_inicio > NOW() + INTERVAL '24 HOURS'`.<br>4. Recuento transaccional en `reservas_cupo` con estado activo menor a `aforo_maximo` (10 presencial / 20 virtual).<br>5. Inexistencia de tupla activa previa `(id_sesion, estudiante_email)` en la tabla `reservas_cupo`. |
| **PostCondiciones** | 1. Registro insertado en la tabla física `reservas_cupo` con `estado = 'PENDIENTE_CONFIRMACION'` y hash SHA-256 (`ticket_hash`).<br>2. Transacción confirmada en PostgreSQL mediante `db.commit()` con actualización atómica de vacantes.<br>3. Notificación flotante de confirmación desplegada en cliente con código de comprobante y persistencia en la vista `"Mis Reservas"`. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Exploración en Cartelera y Apertura del Diálogo Modal** | |
| **1.** El estudiante mentoreado autenticado navega por `RecommendationFeedView.tsx` y pulsa el botón `"Reservar Cupo"` en la tarjeta correspondiente a una sesión de mentoría en estado `PUBLICADA`. | **2.** En `App.tsx`, el evento `onSelectOffer` actualiza el estado `selectedOfferForBooking`. `BookingModalView.tsx` se renderiza recibiendo las propiedades requeridas (`isOpen={true}`, `offer`, `userEmail`, `onClose`, `onSuccess`). Ejecuta el hook `useEffect` validando `offer.available_slots > 0` y la no expiración de la sesión. (Si la tarjeta quedó desfasada y registra 0 cupos, salta a E001). (Si el mentoreado ya cuenta con una reserva activa para esa misma sesión, salta a E002). |
| **Fase 2: Verificación de Precondiciones y Reglas de Negocio en Cliente** | |
| **3.** En `BookingModalView.tsx`, el usuario revisa el panel de detalles de la sesión: título del tema curricular, nombre de la asignatura, fecha y hora programada, modalidad (Presencial con aula física o Virtual con enlace Google Meet) y aforo restante. Lee la advertencia del compromiso de asistencia y pulsa el botón `"Confirmar Reserva"`. | **4.** El componente activa el estado transicional `isSubmitting = true`, deshabilita los controles del modal y muestra un indicador circular animado en color azul institucional. Lee el token Bearer en `localStorage`. Invoca al método `reserveSeat(offer.id, userEmail)` expuesto por `ApiBookingAdapter` en `bookingService.ts`. (Si el token no existe o expiró, salta a E003). (Si el usuario es el propio mentor titular de la sesión, salta a E004). (Si el usuario no ha suscrito el consentimiento legal digital, salta a E005). |
| **Fase 3: Ejecución de Transacción Atómica con Bloqueo Pesimista en Base de Datos** | |
| **5.** El usuario observa en pantalla el progreso de procesamiento seguro. | **6.** En `bookingService.ts`, se despacha la petición `POST /api/v1/bookings/reserve` con cabecera `Authorization: Bearer <token>` y cuerpo JSON `{"id_sesion": id, "estudiante_email": email}`. El controlador `bookings.py` recibe la petición, valida el esquema Pydantic `BookingCreate` e invoca `booking_service.reserve_seat(db, session_id, current_user.email)`. `booking_service.py` adquiere el cerrojo global en memoria `_booking_lock.acquire(timeout=5.0)`. Inicia la transacción ACID en PostgreSQL con `db.begin()`. Configura el cerrojo de fila con `db.execute(text("SET LOCAL lock_timeout = '5.0s'"))`. Ejecuta la consulta relacional con bloqueo pesimista exclusivo de fila: `SELECT * FROM sesiones_mentoria WHERE id = :id FOR UPDATE OF sesiones_mentoria`. Verifica que la sesión exista, mantenga el estado `PUBLICADA`, no haya sobrepasado la ventana límite de 24 horas (`sesion.fecha_inicio > now_utc + timedelta(hours=24)`, RN-04), y que el recuento de reservas activas sea menor al aforo permitido (`occupied_seats < sesion.aforo_maximo`, 10 en presencial o 20 en virtual, RN-05). Inserta el nuevo registro en `reservas_cupo` con estado `PENDIENTE_CONFIRMACION` y ticket hash criptográfico SHA-256. Confirma atómicamente la transacción mediante `db.commit()` y libera el cerrojo `_booking_lock`. Retorna HTTP 201 Created con el payload `BookingResponse`. (Si la sesión no existe en base de datos, salta a E006). (Si el estado de la sesión cambió concurrentemente a CANCELADA, salta a E007). (Si la fecha de inicio no cumple la antelación de 24 horas, salta a E008). (Si ocurre timeout en la adquisición del cerrojo, salta a E009). (Si otra transacción concurrente ocupó el último cupo disponible en el mismo milisegundo, salta a E010). |
| **Fase 4: Confirmación y Actualización Reactiva de Estados** | |
| **7.** `bookingService.ts` recibe el código HTTP 201 y deserializa la entidad de respuesta. Transfiere el control a `BookingModalView.tsx`, la cual oculta el indicador de carga y conmuta su interfaz al panel de confirmación en color verde, desplegando el código de reserva, un recordatorio de ratificación obligatoria a T-24h y el botón `"Finalizar y Ver Mis Reservas"`. | **8.** El usuario hace clic en el botón `"Finalizar y Ver Mis Reservas"`. `BookingModalView.tsx` ejecuta el callback `onSuccess()`. En `App.tsx`, se invoca `fetchOffers()` para sincronizar las vacantes en cartelera, se actualiza el estado global de reservas del estudiante y se navega a la vista `StudentBookingsView.tsx`, presentando el registro recién formalizado en estado `PENDIENTE_CONFIRMACION`. |

##### Flujos de Excepción

##### Flujo de excepción E001: Oferta en cartelera sin vacantes disponibles
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `BookingModalView.tsx` detecta `offer.available_slots <= 0`. Modifica inmediatamente su estado interno deshabilitando el botón `"Confirmar Reserva"` y mostrando un aviso en color ámbar: *"Lo sentimos, el aforo para esta sesión se ha completado. No es posible generar nuevas reservas"*. Presenta el botón `<button onClick={onClose}>Volver a la Cartelera</button>`. |
| **E001-1.2** Hace clic en el botón "Volver a la Cartelera". | **E001-1.3** Invoca el callback `onClose()`, destruye la instancia modal del árbol del DOM y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Reserva duplicada activa para el mismo estudiante
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 2 del Flujo Normal, el hook `useEffect` en `BookingModalView.tsx` verifica la existencia previa de una reserva activa en el estado local de reservas del usuario. Alternativamente, en el paso 6, `booking_service.py` ejecuta `SELECT id FROM reservas_cupo WHERE id_sesion = :sid AND estudiante_email = :email AND estado IN ('PENDIENTE_CONFIRMACION', 'CONFIRMADA')`. Al hallar una tupla, lanza `HTTPException(status_code=400, detail="ALREADY_BOOKED: Ya posees una reserva activa registrada para esta sesión de mentoría.")`.<br><br>En `bookingService.ts`, captura el error 400 con código `'ALREADY_BOOKED'`. En `BookingModalView.tsx`, renderiza una notificación en color rojo con el mensaje de duplicidad y presenta el botón `<button onClick={onClose}>Aceptar</button>`. |
| **E002-1.2** Hace clic en el botón "Aceptar". | **E002-1.3** Cierra el cuadro modal, retorna el foco a la tarjeta de la sesión y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Sesión institucional no autenticada o token expirado
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 4 del Flujo Normal, `bookingService.ts` ejecuta `localStorage.getItem('auth_token')` y detecta valor nulo, o el backend responde con HTTP 401 Unauthorized por firma JWT vencida (`TokenExpiredError`).<br><br>En `bookingService.ts`, propaga la excepción hacia el contexto global. En `App.tsx`, el interceptor de seguridad purga el token expirado con `localStorage.removeItem('auth_token')`, conmuta el estado global `user` a `null` y monta el componente `LoginOtpView.tsx`, desplegando una alerta en color rojo: *"Su sesión institucional ha caducado por inactividad. Por favor, ingrese nuevamente mediante código OTP."* |
| **E003-1.2** Ingresa su correo institucional y solicita nuevo código de acceso. | **E003-1.3** Transfiere el control al flujo de autenticación y retorna al paso 1 del Flujo Normal de Eventos de CUS-001. |

##### Flujo de excepción E004: Conflicto de rol de mentor (Autoreserva Prohibida)
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 4 del Flujo Normal, `BookingModalView.tsx` compara `offer.mentor_email === userEmail`. Alternativamente, en el paso 6, `booking_service.py` valida `sesion.id_mentor == current_user.id`. Lanza `HTTPException(status_code=400, detail="CANNOT_BOOK_OWN_SESSION: Un mentor no puede reservar cupos en su propia sesión de mentoría.")`.<br><br>En `bookingService.ts`, captura el error con código `'CANNOT_BOOK_OWN_SESSION'`. `BookingModalView.tsx` inhabilita el botón de acción y despliega una advertencia en color rojo. Presenta el botón `<button onClick={onClose}>Cerrar</button>`. |
| **E004-1.2** Hace clic en el botón "Cerrar". | **E004-1.3** Cierra el modal sin realizar peticiones de mutación y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E005: Ausencia o revocación de consentimiento legal digital
| Usuario | Sistema |
|---|---|
| | **E005-1.1** En el paso 4 del Flujo Normal, `booking_service.py` invoca a `ConsentService.get_consent_status(current_user.email)` y obtiene `has_consented = false`. Lanza `HTTPException(status_code=403, detail="CONSENT_REQUIRED: Se requiere la formalización del consentimiento legal digital bajo la Ley Nº 29733 para realizar reservas de cupos.")`.<br><br>En `bookingService.ts`, eleva `new BookingException('CONSENT_REQUIRED', ...)`. En `App.tsx`, captura el error 403, oculta `BookingModalView.tsx` y monta en primer plano `ConsentModalView.tsx`, presentando los términos de tratamiento de datos personales. |
| **E005-1.2** Lee los términos legales, marca la casilla de aceptación y pulsa "Aceptar y Continuar". | **E005-1.3** Despacha `POST /api/v1/consent/accept`, persiste la traza legal, retorna el control al modal de reserva y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E006: Sesión de mentoría inexistente en el catálogo
| Usuario | Sistema |
|---|---|
| | **E006-1.1** En el paso 6 del Flujo Normal, la consulta relacional `SELECT * FROM sesiones_mentoria WHERE id = :id` retorna `None`. `booking_service.py` ejecuta `db.rollback()` y lanza `HTTPException(status_code=404, detail="SESSION_NOT_FOUND: La sesión de mentoría solicitada no existe o fue eliminada del catálogo.")`.<br><br>En `bookingService.ts`, eleva `new BookingException('SESSION_NOT_FOUND', message, 404)`. En `App.tsx`, el bloque `catch` ejecuta `setFeedRefreshKey((prev) => prev + 1)` para purgar la sesión obsoleta y muestra una alerta en color rojo. Presenta el botón `<button onClick={onClose}>Entendido</button>`. |
| **E006-1.2** Hace clic en el botón "Entendido". | **E006-1.3** Cierra el diálogo modal, actualiza la cartelera eliminando la tarjeta huérfana y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E007: Sesión cancelada concurrentemente por el mentor o administración
| Usuario | Sistema |
|---|---|
| | **E007-1.1** En el paso 6 del Flujo Normal, tras adquirir el bloqueo pesimista de fila, `booking_service.py` evalúa `sesion.estado != EstadoSesion.PUBLICADA`. Ejecuta `db.rollback()` y lanza `HTTPException(status_code=400, detail="SESSION_NOT_OPEN: La sesión seleccionada no se encuentra abierta para reservas (Estado actual: CANCELADA).")`.<br><br>En `bookingService.ts`, eleva `new BookingException('SESSION_NOT_OPEN', message, 400)`. En `App.tsx`, el bloque `catch` ejecuta `setFeedRefreshKey((prev) => prev + 1)` para invalidar la oferta obsoleta y muestra una notificación en color rojo. Presenta el botón `<button onClick={onClose}>Actualizar Cartelera</button>`. |
| **E007-1.2** Hace clic en el botón "Actualizar Cartelera". | **E007-1.3** Cierra el modal, remueve la tarjeta obsoleta del DOM mediante `fetchOffers()` y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E008: Ventana de antelación vencida (Regla Institucional RN-04)
| Usuario | Sistema |
|---|---|
| | **E008-1.1** En el paso 6 del Flujo Normal, `booking_service.py` evalúa `sesion.fecha_inicio <= now_utc + timedelta(hours=24)` y lanza `HTTPException(status_code=400, detail="WINDOW_CLOSED_T24H: Las reservas cierran 24 horas antes del inicio de la sesión.")`.<br><br>En `bookingService.ts`, identifica `'WINDOW_CLOSED_T24H'` y eleva `new BookingException('WINDOW_CLOSED_T24H', message, 400)`. `BookingModalView.tsx` renderiza la advertencia en color rojo indicando que las inscripciones cerraron por límite de 24 horas. Presenta el botón `<button onClick={onClose}>Entendido</button>`. |
| **E008-1.2** Hace clic en el botón "Entendido". | **E008-1.3** Cierra el diálogo modal, actualiza la tarjeta mostrando el botón deshabilitado con el texto "Inscripciones Cerradas" y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E009: Timeout de concurrencia en adquisición de cerrojo (Database Busy)
| Usuario | Sistema |
|---|---|
| | **E009-1.1** En el paso 6 del Flujo Normal, `_booking_lock.acquire(timeout=5.0)` retorna `False` o PostgreSQL lanza excepción por timeout de cerrojo. `booking_service.py` lanza `HTTPException(status_code=503, detail="DATABASE_BUSY: El servicio de reservas se encuentra temporalmente sobrecargado. Por favor, reintente en unos momentos.")`.<br><br>En `bookingService.ts`, eleva `new BookingException('DATABASE_BUSY', message, 503)`. En `App.tsx`, el bloque `catch` preserva la intención del usuario sin ejecutar rollback destructivo. `BookingModalView.tsx` rehabilita los botones y muestra un aviso en color ámbar: *"El servicio se encuentra temporalmente con alta concurrencia. No se ha generado ningún cargo. Por favor, pulsa 'Reintentar'"*. Presenta el botón `<button onClick={handleConfirmClick}>Reintentar Reserva</button>`. |
| **E009-1.2** Hace clic en el botón "Reintentar Reserva". | **E009-1.3** Dispara nuevamente la petición `bookingService.reserveSeat` y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E010: Colisión concurrente por aforo agotado en el último milisegundo
| Usuario | Sistema |
|---|---|
| | **E010-1.1** En el paso 6 del Flujo Normal, bajo el cerrojo pesimista `SELECT ... FOR UPDATE OF sesiones_mentoria`, `booking_service.py` evalúa `occupied_seats >= sesion.aforo_maximo`. Ejecuta `db.rollback()` y lanza `HTTPException(status_code=409, detail="CAPACITY_EXCEEDED: Aforo completo. No quedan vacantes disponibles en esta sesión.")`.<br><br>En `bookingService.ts`, eleva `new BookingException('CAPACITY_EXCEEDED', 'Aforo completo o colisión con otra reserva concurrente.', 409)`. En `App.tsx`, el bloque `catch` captura `err.code === 'CAPACITY_EXCEEDED'`, ejecuta `setFeedRefreshKey((prev) => prev + 1)` para sincronizar la cartelera y despliega en `BookingModalView.tsx` un panel en color naranja de alerta indicando que la última vacante fue ocupada simultáneamente por otro usuario. Presenta el botón `<button onClick={handleGoToDemand}>Registrar Demanda de Tema</button>` y el botón `<button onClick={onClose}>Volver a la Cartelera</button>`. |
| **E010-1.2** Hace clic en el botón "Volver a la Cartelera" (o en "Registrar Demanda de Tema"). | **E010-1.3** Cierra `BookingModalView.tsx`, actualiza la tarjeta en la cartelera como "Aforo Completo (0 vacantes)" y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-024 - Ratificar asistencia a sesión de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-024** (CUS-024) |
| **Nombre** | Ratificar asistencia obligatoria a sesión de mentoría académica a T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-013 (Confirmación anticipada de asistencia a mentoría); RN-04 (Ventana de ratificación previa entre T-48h y T-24h), RN-10 (Control de asistencia y quórum institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite a los estudiantes mentoreados con reservas provisionales en estado `PENDIENTE_CONFIRMACION` confirmar obligatoriamente su asistencia definitiva dentro de la ventana de ratificación institucional comprendida entre las 48 horas y las 24 horas previas al inicio de la sesión (`sesion.fecha_inicio - 48h <= now_utc <= sesion.fecha_inicio - 24h`). El usuario accede a la vista `StudentBookingsView.tsx` y acciona el botón de confirmación enlazado a `bookingService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/bookings.py` y `app/services/booking_service.py` procesan la petición `POST /api/v1/bookings/{id}/confirm`, verifican la vigencia temporal de la ventana, conmutan el estado de la entidad `ReservaCupo` a `CONFIRMADA`, generan el identificador criptográfico del pase de lista y emiten una respuesta HTTP 200 OK, contribuyendo al cálculo del quórum mínimo (RN-05). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Reglamento Académico de Asistencia y Quórum EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/StudentBookingsView.tsx`<br>`aplicacion/frontend/src/services/bookingService.ts` (`BookingService.confirmBooking`)<br>`aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/{id}/confirm`)<br>`aplicacion/backend/app/services/booking_service.py` (`BookingService.confirm_booking`)<br>`aplicacion/backend/app/models/booking.py` (`ReservaCupo`, `EstadoReserva`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Usuario con sesión institucional activa y rol `mentoreado` verificado en JWT.<br>2. Reserva en la tabla `reservas_cupo` asociada al estudiante en estado `PENDIENTE_CONFIRMACION`.<br>3. Fecha y hora actual dentro de la ventana temporal de confirmación [T-48h, T-24h]. |
| **PostCondiciones** | 1. Estado de la entidad `ReservaCupo` actualizado atómicamente a `CONFIRMADA` en PostgreSQL.<br>2. Generación del código seguro de verificación de asistencia.<br>3. Actualización reactiva de la tarjeta en la interfaz del estudiante con distintivo verde de confirmación. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de reservas y visualización de ventana de ratificación** | |
| **1.** El estudiante mentoreado accede a `"Mis Reservas"` en `StudentBookingsView.tsx`. | **2.** En `bookingService.ts`, se despacha `GET /api/v1/bookings/my-bookings`. El backend retorna las reservas del estudiante. En `StudentBookingsView.tsx`, para las reservas cuya sesión se encuentra dentro de la ventana de ratificación [T-48h, T-24h], se renderiza un panel de alerta en color ámbar con un temporizador y el botón `"Ratificar Asistencia Obligatoria"`. |
| **Fase 2: Validación de plazos y solicitud de ratificación** | |
| **3.** El estudiante revisa los datos de la sesión y pulsa el botón `"Ratificar Asistencia Obligatoria"`. | **4.** En `StudentBookingsView.tsx`, se abre un cuadro modal de ratificación. El estudiante presiona `"Sí, Confirmo mi Asistencia Definitiva"`. En `bookingService.ts`, se despacha la petición `POST /api/v1/bookings/{booking_id}/confirm`. En `bookings.py`, `booking_service.py` ejecuta `SELECT r.*, s.fecha_inicio FROM reservas_cupo r JOIN sesiones_mentoria s ON r.id_sesion = s.id WHERE r.id = :bid AND r.estudiante_email = :email`. Verifica que `now_utc >= s.fecha_inicio - timedelta(hours=48)` y que `now_utc <= s.fecha_inicio - timedelta(hours=24)`. (Si el estudiante intenta ratificar antes de T-48h, salta a E001). (Si la ventana ya expiró por superar el umbral T-24h, salta a E002). |
| **Fase 3: Transición atómica de estado y emisión de pase de asistencia** | |
| **5.** El estudiante espera la respuesta visual de confirmación. | **6.** En `booking_service.py`, se ejecuta `UPDATE reservas_cupo SET estado = 'CONFIRMADA', fecha_confirmacion = :now WHERE id = :bid`. Confirma la transacción con `db.commit()` y retorna HTTP 200 con el modelo `BookingResponse`. En cliente, `StudentBookingsView.tsx` conmuta el estado de la tarjeta a color verde con la leyenda *"Asistencia Ratificada"*, despliega el código alfanumérico para el pase de lista presencial/virtual y emite una notificación de éxito. |

##### Flujos de Excepción

##### Flujo de excepción E001: Intento de ratificación anticipada fuera de ventana
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `booking_service.py` evalúa `now_utc < sesion.fecha_inicio - timedelta(hours=48)`. Lanza `HTTPException(status_code=400, detail="CONFIRMATION_NOT_OPEN: La ventana de confirmación abre exactamente 48 horas antes del inicio de la sesión.")`.<br><br>En `StudentBookingsView.tsx`, se despliega un mensaje en color azul institucional indicando la fecha y hora exacta en que se habilitará la ratificación obligatoria. |
| **E001-1.2** Hace clic en el botón "Entendido" en la alerta. | **E001-1.3** Cierra el modal de confirmación y retorna al paso 2 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Ventana de ratificación vencida a T-24h
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, `booking_service.py` evalúa `now_utc > sesion.fecha_inicio - timedelta(hours=24)`. Lanza `HTTPException(status_code=400, detail="CONFIRMATION_WINDOW_EXPIRED: La ventana de ratificación cerró 24 horas antes del inicio. La reserva no confirmada fue liberada para dar paso al proceso de quórum.")`.<br><br>En `StudentBookingsView.tsx`, se actualiza la tarjeta a estado inactivo con una insignia en color gris indicando que el cupo fue dado de baja por falta de ratificación en plazo. |
| **E002-1.2** Hace clic en el botón "Aceptar". | **E002-1.3** Actualiza la lista de reservas en cliente y retorna al paso 2 del Flujo Normal de Eventos. |

#### CUS-017 - Desistir voluntariamente de reserva

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-017** (CUS-017) |
| **Nombre** | Desistir voluntariamente de reserva de cupo sin penalidad antes de T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-014 (Desistimiento voluntario y liberación anticipada de cupos); RN-04 (Antelación mínima de 24 horas para cancelaciones sin sanción institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite a los estudiantes mentoreados anular voluntariamente una reserva activa en estado `PENDIENTE_CONFIRMACION` o `CONFIRMADA` sin incurrir en penalizaciones académicas, siempre que la solicitud se despache con una antelación mayor a 24 horas respecto al inicio de la sesión (`fecha_inicio > now_utc + 24h`, RN-04). El componente `StudentBookingsView.tsx` despacha `POST /api/v1/bookings/{id}/cancel` hacia `bookings.py` y `app/services/booking_service.py`. El backend adquiere el cerrojo pesimista de fila, actualiza el estado de la reserva a `CANCELADA_ESTUDIANTE`, decrementa el contador de cupos ocupados de la sesión y confirma la transacción ACID con `db.commit()`, notificando al motor de recomendaciones sobre la vacante liberada. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Reglamento Académico de Asistencia EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/StudentBookingsView.tsx`<br>`aplicacion/frontend/src/services/bookingService.ts` (`BookingService.cancelBooking`)<br>`aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/{id}/cancel`)<br>`aplicacion/backend/app/services/booking_service.py` (`BookingService.cancel_booking`)<br>`aplicacion/backend/app/models/booking.py` (`ReservaCupo`, `EstadoReserva`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Usuario autenticado con token JWT institucional y titularidad sobre la reserva.<br>2. Reserva en estado `PENDIENTE_CONFIRMACION` o `CONFIRMADA`.<br>3. Fecha de inicio de la sesión mayor a la hora actual UTC más 24 horas (`fecha_inicio > now + 24h`). |
| **PostCondiciones** | 1. Estado de `ReservaCupo` actualizado a `CANCELADA_ESTUDIANTE` en PostgreSQL.<br>2. Cupo vacante liberado y disponible nuevamente en la cartelera institucional.<br>3. Despliegue de confirmación en cliente y actualización reactiva de la tarjeta a color neutro. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Solicitud de desistimiento y verificación de plazos** | |
| **1.** El estudiante mentoreado localiza su reserva en `StudentBookingsView.tsx` y hace clic en el botón `"Cancelar Reserva"`. | **2.** En `StudentBookingsView.tsx`, se abre un modal de advertencia indicando que el desistimiento es irrevocable y liberará el cupo para otro compañero. El sistema solicita seleccionar un motivo de cancelación opcional en una lista desplegable. (Si la antelación es inferior a 24 horas respecto al inicio de la sesión, salta a E001). |
| **Fase 2: Confirmación y procesamiento atómico de liberación de cupo** | |
| **3.** El estudiante selecciona el motivo y pulsa el botón `"Confirmar Cancelación"`. | **4.** En `bookingService.ts`, se despacha `POST /api/v1/bookings/{booking_id}/cancel`. En `bookings.py`, `booking_service.py` inicia la transacción con `db.begin()`. Ejecuta bloqueo de fila en `sesiones_mentoria` y `reservas_cupo`. Verifica que `sesion.fecha_inicio > now_utc + timedelta(hours=24)` (RN-04). Actualiza `reservas_cupo.estado = 'CANCELADA_ESTUDIANTE'` y registra `fecha_cancelacion = now_utc`. Ejecuta `db.commit()` y retorna HTTP 200 con `BookingResponse`. |
| **5.** El estudiante visualiza el modal de éxito indicando la liberación correcta del cupo sin penalidad. | **6.** En `StudentBookingsView.tsx`, se cierra el modal, se conmuta el estado de la tarjeta a color gris con la leyenda *"Cancelada por el estudiante"* y se emite un evento de actualización que incrementa las vacantes disponibles en la cartelera. |

##### Flujos de Excepción

##### Flujo de excepción E001: Desistimiento tardío con menos de 24 horas de antelación
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `booking_service.py` comprueba que `sesion.fecha_inicio <= now_utc + timedelta(hours=24)`. Lanza `HTTPException(status_code=400, detail="LATE_CANCELLATION_PROHIBITED: No se permite la cancelación voluntaria con menos de 24 horas de antelación para no desestabilizar el quórum de la sesión.")`.<br><br>En `StudentBookingsView.tsx`, se despliega un panel de advertencia en color rojo indicando que la política institucional prohíbe cancelaciones a menos de 24 horas y que la inasistencia injustificada acarreará una penalización temporal en futuras reservas. |
| **E001-1.2** Hace clic en el botón "Entendido". | **E001-1.3** Cierra el cuadro modal manteniendo la reserva en estado activo y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-023 - Evaluar quórum automático a T-24h

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-023** (CUS-023) |
| **Nombre** | Evaluar automáticamente el quórum reglamentario de sesiones de mentoría a T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-015 (Monitoreo desatendido, emisión de recordatorios y evaluación de quórum); RN-05 (Regla de quórum mínimo de 3 estudiantes confirmados), RN-10 (Automatización de eventos temporales a T-24h) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Proceso Demonio en Segundo Plano (`SchedulerWorker`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite evaluar de forma automatizada y desatendida el cumplimiento del umbral reglamentario de quórum institucional (mínimo 3 estudiantes con asistencia ratificada, RN-05) exactamente 24 horas antes del inicio programado de cada sesión de mentoría. Un proceso en segundo plano programado mediante APScheduler o endpoint administrativo `POST /api/v1/quorum/evaluate-all` en `aplicacion/backend/app/api/v1/endpoints/quorum.py` invoca al método `evaluate_session_quorum` en `app/services/booking_service.py`. El servicio consulta las sesiones en estado `PUBLICADA` con ventana de antelación alcanzada, cuantifica las reservas en estado `CONFIRMADA`; si se alcanza o supera el quórum, promueve automáticamente la sesión a estado `CONFIRMADA`. Si no se alcanza el quórum reglamentario (menos de 3 confirmados), transiciona la sesión a estado `QUORUM_INSUFICIENTE` y despacha alertas urgentes al mentor para la resolución de contingencia (CUS-007). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Reglamento Académico de Quórum y Viabilidad de Sesiones EPIS-UPT |
| **Anexos** | `aplicacion/backend/app/api/v1/endpoints/quorum.py` (`POST /api/v1/quorum/evaluate-all`, `GET /api/v1/quorum/status/{session_id}`)<br>`aplicacion/backend/app/services/booking_service.py` (`BookingService.evaluate_session_quorum`)<br>`aplicacion/backend/app/services/simulation_service.py`<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`, `EstadoSesion`), `app/models/booking.py` (`ReservaCupo`, `EstadoReserva`) |
| **Precondiciones** | 1. Sesión de mentoría en estado `PUBLICADA` en la tabla física `sesiones_mentoria`.<br>2. Fecha y hora actual del servidor en la marca temporal exacta de 24 horas previas al inicio de la sesión (`now_utc >= fecha_inicio - 24h`).<br>3. Proceso planificador o disparador de simulación operativo. |
| **PostCondiciones** | 1. Estado de `SesionMentoria` actualizado en base de datos a `CONFIRMADA` o `QUORUM_INSUFICIENTE`.<br>2. Transacción confirmada en PostgreSQL y generación de registros de auditoría de evaluación.<br>3. Disparo de notificaciones hacia el mentor y los estudiantes inscritos. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Disparo de la tarea programada y localización de sesiones a T-24h** | |
| **1.** El proceso planificador del sistema en segundo plano (`SchedulerWorker`) ejecuta el ciclo de evaluación o el administrador despacha la petición `POST /api/v1/quorum/evaluate-all`. | **2.** En `quorum.py`, el controlador invoca `simulation_service.evaluate_all_active_quorums(db)`. El backend ejecuta `SELECT * FROM sesiones_mentoria WHERE estado = 'PUBLICADA' AND fecha_inicio <= NOW() + INTERVAL '24 HOURS'`. (Si no existen sesiones en la ventana T-24h, el sistema finaliza la ejecución sin mutaciones). |
| **Fase 2: Cuantificación de confirmaciones y verificación de umbral de quórum** | |
| **3.** El sistema procesa cada sesión localizada en un bucle transaccional independiente. | **4.** En `booking_service.py`, para cada sesión se ejecuta `SELECT count(*) FROM reservas_cupo WHERE id_sesion = :sid AND estado = 'CONFIRMADA'`. El servicio evalúa si `confirmed_count >= 3` (RN-05). (Si el recuento es menor a 3 confirmados, salta a A001). |
| **Fase 3: Confirmación oficial de sesión y notificación de viabilidad** | |
| **5.** El sistema constata que la sesión cumple el quórum reglamentario (3 o más estudiantes con asistencia ratificada). | **6.** En `booking_service.py`, se ejecuta `UPDATE sesiones_mentoria SET estado = 'CONFIRMADA' WHERE id = :sid`. Se confirma la transacción con `db.commit()`. Se genera la traza en la bitácora de auditoría y se despacha una notificación por correo electrónico y notificación web al mentor y a los estudiantes inscritos con el texto: *"¡Sesión confirmada! Tu sesión de mentoría cuenta con el quórum reglamentario para su realización"*. Retorna HTTP 200 con el resumen de la evaluación. |

##### Flujos Alternativos

##### Flujo alternativo A001: Quórum insuficiente a T-24h con alerta al mentor
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 4 del Flujo Normal, `booking_service.py` detecta que la sesión tiene menos de 3 estudiantes confirmados (`confirmed_count < 3`). | **A001-1.2** El servicio ejecuta `UPDATE sesiones_mentoria SET estado = 'QUORUM_INSUFICIENTE' WHERE id = :sid` y confirma con `db.commit()`. |
| **A001-1.3** El mentor titular de la sesión recibe una alerta urgente en su panel de control y correo institucional: *"Alerta de Quórum: Tu sesión programada para mañana no alcanzó el quórum mínimo de 3 estudiantes. Por favor, ingresa para decidir si dictarla, reprogramarla o cancelarla"*. | **A001-1.4** El sistema habilita el componente de resolución de contingencia en la interfaz del mentor y concluye el caso de uso y transfiere el flujo a la toma de decisión del mentor (CUS-007). |

#### CUS-007 - Decisión del mentor ante quórum insuficiente

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-007** (CUS-007) |
| **Nombre** | Gestionar sesión de mentoría y decisión resolutiva ante quórum insuficiente |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-016 (Gestión resolutiva de sesiones ante quórum insuficiente); RN-04 (Antelación mínima de reprogramación), RN-10 (Resolución de contingencia ante quórum) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite al estudiante mentor tomar una decisión resolutiva cuando su sesión no alcanza el quórum reglamentario de 3 estudiantes a T-24h (estado `QUORUM_INSUFICIENTE`) a través del componente cliente `MentorSessionsView.tsx` y el servicio `offerService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/offers.py` y `app/services/offer_service.py` procesan la petición `POST /api/v1/offers/{id}/quorum-decision`. El mentor cuenta con tres alternativas reglamentarias: 1) Dictar la sesión de todas formas con los estudiantes confirmados (promoción forzada a `CONFIRMADA`), 2) Reprogramar la sesión para una nueva fecha con antelación mínima de 24 horas, o 3) Cancelar la sesión definitivamente liberando a los inscritos sin penalización alguna. La operación se ejecuta bajo una transacción ACID confirmada con `db.commit()`. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Reglamento Académico de Contingencia de Mentorías EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/MentorSessionsView.tsx`<br>`aplicacion/frontend/src/services/offerService.ts` (`OfferService.resolveQuorum`)<br>`aplicacion/backend/app/api/v1/endpoints/offers.py` (`POST /api/v1/offers/{id}/quorum-decision`)<br>`aplicacion/backend/app/services/offer_service.py` (`OfferService.resolve_quorum_decision`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`, `EstadoSesion`), `app/models/booking.py` (`ReservaCupo`) |
| **Precondiciones** | 1. Mentor titular autenticado con token JWT institucional activo.<br>2. Sesión en la tabla `sesiones_mentoria` en estado estricto `QUORUM_INSUFICIENTE`.<br>3. Decisión despachada antes del inicio programado de la sesión. |
| **PostCondiciones** | 1. Estado de `SesionMentoria` actualizado en base de datos según la decisión elegida (`CONFIRMADA`, `REPROGRAMADA` o `CANCELADA_QUORUM`).<br>2. Actualización en cascada de los estados de reserva de los estudiantes inscritos.<br>3. Despacho automatizado de notificaciones informativas a los estudiantes afectados. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso a la sesión con quórum insuficiente y visualización de opciones** | |
| **1.** El mentor accede a `"Mis Sesiones"` en `MentorSessionsView.tsx` y visualiza la tarjeta de la sesión resaltada en color ámbar con la etiqueta *"Quórum Insuficiente"*. | **2.** El mentor hace clic en el botón `"Gestionar Sesión"`. En `MentorSessionsView.tsx`, se abre una ventana modal desplegando los estudiantes inscritos confirmados y las tres opciones resolutivas: 1) `"Dictar de Todas Formas"`, 2) `"Reprogramar Sesión"`, 3) `"Cancelar Sesión Definitivamente"`. |
| **Fase 2: Elección de la resolución y verificación de parámetros** | |
| **3.** El mentor selecciona la opción `"Dictar de Todas Formas"` (o `"Reprogramar Sesión"` indicando nueva fecha y hora, o `"Cancelar Sesión"` ingresando un justificativo) y presiona el botón `"Confirmar Decisión"`. | **4.** En `offerService.ts`, se despacha la petición `POST /api/v1/offers/{offer_id}/quorum-decision` con payload JSON `{"decision": "PROCEED" | "RESCHEDULE" | "CANCEL", "new_start_time": ..., "reason": ...}`. En `offers.py`, `offer_service.py` inicia la transacción con `db.begin()`. Valida que la sesión se encuentre en estado `QUORUM_INSUFICIENTE`. Si seleccionó reprogramar, valida que la nueva fecha cumpla con la antelación mayor a 24 horas (RN-04). Si seleccionó cancelar, valida que el justificativo no esté vacío. (Si la fecha de reprogramación es inferior a 24 horas, salta a E001). (Si la justificación de cancelación está vacía, salta a E002). |
| **Fase 3: Persistencia de la resolución y notificación a los estudiantes** | |
| **5.** El mentor observa el indicador de procesamiento seguro en el botón de confirmación. | **6.** En `offer_service.py`, si la decisión es `PROCEED`, actualiza `sesiones_mentoria.estado = 'CONFIRMADA'`. Si es `RESCHEDULE`, actualiza fecha y hora, restablece `estado = 'PUBLICADA'` y notifica a los inscritos. Si es `CANCEL`, actualiza `estado = 'CANCELADA_QUORUM'` y libera a los inscritos. Confirma la transacción con `db.commit()` y retorna HTTP 200. En cliente, `MentorSessionsView.tsx` cierra el modal, actualiza el estado de la tarjeta y despliega una notificación flotante en color verde: *"Decisión registrada exitosamente"*. |

##### Flujos de Excepción

##### Flujo de excepción E001: Fecha de reprogramación con menos de 24 horas de antelación
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el mentor selecciona reprogramar pero ingresa una fecha y hora con antelación menor a 24 horas respecto al tiempo actual. `offer_service.py` valida la regla RN-04 y lanza `HTTPException(status_code=400, detail="INSUFFICIENT_RESCHEDULE_ADVANCE: La nueva fecha de la sesión debe programarse con al menos 24 horas de antelación.")`.<br><br>En `MentorSessionsView.tsx`, se resalta el selector de fecha en color rojo con el mensaje de infracción reglamentaria. |
| **E001-1.2** Selecciona una nueva fecha y hora con un margen superior a 24 horas. | **E001-1.3** Rehabilita el botón de confirmación en la interfaz y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Justificación de cancelación definitiva vacía
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, el mentor selecciona cancelar la sesión pero deja en blanco el campo de motivo. `offer_service.py` comprueba que la cadena es nula o vacía y lanza `HTTPException(status_code=422, detail="REASON_REQUIRED: Debe ingresar obligatoriamente un motivo justificado para proceder con la cancelación definitiva.")`.<br><br>En `MentorSessionsView.tsx`, se destaca el área de texto en color rojo solicitando ingresar el motivo para los estudiantes. |
| **E002-1.2** Ingresa una justificación válida en el cuadro de texto. | **E002-1.3** Valida la longitud mínima en cliente y retorna al paso 3 del Flujo Normal de Eventos. |
"""
