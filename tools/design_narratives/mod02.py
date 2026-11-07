# -*- coding: utf-8 -*-
"""
Modulo 02: Ofertas de Mentoría y Gestión de Recursos (Fase de Diseño)
Contiene: CUS-006, CUS-008
"""

def get_mod02():
    return """### MOD-02: Ofertas de Mentoría y Gestión de Recursos

#### CUS-006 - Publicar oferta de mentoría académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-006** (CUS-006) |
| **Nombre** | Publicar oferta de mentoría académica con validación de antelación y aforo |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-008 (Publicación y parametrización de ofertas de mentoría), RF-009 (Aprovisionamiento automatizado de infraestructura); RN-04 (Ventana de antelación mínima de 24 horas a T-24h), RN-05 (Aforo máximo de 10 presencial y 20 virtual), RN-06 (Prevención de colisión horaria de espacios) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los estudiantes mentores formalizar la apertura de una sesión de mentoría a través del componente cliente `OfferPublishView.tsx` y el servicio `offerService.ts`, despachando una petición `POST /api/v1/offers/publish` hacia el controlador `aplicacion/backend/app/api/v1/endpoints/offers.py`. El backend valida el token JWT institucional extrayendo el claim del mentor, y ejecuta en `app/services/offer_service.py` (`OfferService.publish_offer`) las validaciones de negocio institucionales: antelación mínima de 24 horas respecto a la fecha y hora actual en UTC (`fecha_inicio > now_utc + 24h`, RN-04), límites de capacidad según modalidad (máximo 10 cupos en presencial y 20 en virtual, RN-05), verificación de ausencia de traslape con otras sesiones activas del mentor, y validación del aula física o enlace institucional de videoconferencia. Persiste la entidad ORM `SesionMentoria` (`app/models/offer.py`) en estado `PUBLICADA`, emite una confirmación con HTTP 201 Created y sincroniza la cartelera institucional. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-04: Planificación, Espacios y Agendamiento)<br>Reglamento Académico de Mentorías EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/OfferPublishView.tsx`<br>`aplicacion/frontend/src/services/offerService.ts` (`OfferService`, `ApiOfferAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/offers.py` (`POST /api/v1/offers/publish`)<br>`aplicacion/backend/app/services/offer_service.py` (`OfferService.publish_offer`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`, `EstadoSesion`, `ModalidadSesion`), `app/models/curriculum.py` (`TemaCurricular`) |
| **Precondiciones** | 1. Usuario autenticado con token JWT institucional activo conteniendo el rol `UserRole.mentor`.<br>2. Perfil de mentor registrado en `perfiles_academicos` con materias y temas habilitados.<br>3. Fecha y hora de inicio fijadas con al menos 24 horas de antelación respecto a la hora UTC actual. |
| **PostCondiciones** | 1. Registro insertado en la tabla `sesiones_mentoria` con `estado = 'PUBLICADA'` y aforo parametrizado.<br>2. Transacción confirmada en PostgreSQL y emisión de evento de invalidación de caché para el motor de recomendación.<br>3. Despliegue de comprobante de publicación en cliente con código identificador de sesión. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Configuración de la sesión y selección curricular** | |
| **1.** El estudiante mentor accede a la vista de publicación en `OfferPublishView.tsx` y selecciona la asignatura curricular en la lista desplegable `"Curso"`. | **2.** En `offerService.ts`, se invoca la carga de temas disponibles. `OfferPublishView.tsx` renderiza los temas silábicos correspondientes, los campos de fecha de inicio, hora de inicio, duración en minutos (60 a 120), modalidad (`Presencial` o `Virtual`), aula asignada o enlace de videoconferencia (`meet.google.com`), y número de cupos máximos. |
| **Fase 2: Ingreso de parámetros, validación de reglas de aforo y antelación** | |
| **3.** El mentor completa la selección de tema, especifica la fecha y hora programada, selecciona la modalidad, ingresa el número de vacantes deseadas y hace clic en el botón `"Verificar y Publicar"`. | **4.** En `OfferPublishView.tsx`, se ejecutan validaciones previas de formulario. En `offerService.ts`, se despacha `POST /api/v1/offers/publish` con el payload `OfferCreateRequest`. En `offers.py`, el controlador recibe la petición y delega a `offer_service.py`. El servicio valida: 1) que todos los campos requeridos estén completos, 2) que `fecha_inicio >= now_utc + timedelta(hours=24)` (RN-04), 3) que `aforo_maximo <= 10` si la modalidad es `PRESENCIAL` o `aforo_maximo <= 20` si es `VIRTUAL` (RN-05). (Si faltan campos obligatorios o la sintaxis es inválida, salta a E001). (Si la fecha es inferior a 24 horas de antelación, salta a E002). (Si el aforo sobrepasa los límites institucionales de 10 o 20 cupos, salta a E003). |
| **Fase 3: Verificación de concurrencia de horarios y persistencia transaccional** | |
| **5.** El mentor espera la confirmación visual en el botón que presenta un indicador circular de procesamiento. | **6.** En `offer_service.py`, se ejecuta una consulta transaccional `SELECT count(*) FROM sesiones_mentoria WHERE id_mentor = :mid AND estado IN ('PUBLICADA', 'CONFIRMADA') AND NOT (fecha_fin <= :inicio OR fecha_inicio >= :fin)`. Si se seleccionó aula presencial, se verifica que no esté ocupada por otra sesión en ese intervalo. Si es virtual, se valida que el enlace pertenezca al dominio universitario. El backend ejecuta `INSERT INTO sesiones_mentoria (...) VALUES (...)`, confirma la transacción con `db.commit()` y retorna HTTP 201 Created con el payload `OfferResponse`. En `OfferPublishView.tsx`, se limpia el formulario, se despliega una tarjeta de confirmación en color verde con el código generado de sesión y el botón `"Ver en Cartelera"`. (Si existe traslape de horario para el mentor o en el aula solicitada, salta a E004). (Si el enlace de videoconferencia es inválido, salta a E005). |

##### Flujos de Excepción

##### Flujo de excepción E001: Campos obligatorios incompletos o inválidos
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el validador Pydantic `OfferCreateRequest` en `offers.py` detecta omisión de campos requeridos (e.g. tema curricular o modalidad ausente). Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: Todos los campos de la sesión son obligatorios.")`.<br><br>En `OfferPublishView.tsx`, se capturan los errores de validación y se resaltan los campos observados con un borde en color rojo y texto explicativo. |
| **E001-1.2** Corrige los campos observados completando los datos requeridos. | **E001-1.3** Rehabilita el botón `"Verificar y Publicar"` y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Incumplimiento de antelación mínima de 24 horas
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, `offer_service.py` evalúa `fecha_inicio < now_utc + timedelta(hours=24)` (violación de RN-04). Lanza `HTTPException(status_code=400, detail="INSUFFICIENT_ADVANCE_TIME: Las ofertas de mentoría deben programarse con un mínimo de 24 horas de antelación.")`.<br><br>En `OfferPublishView.tsx`, se despliega un panel de advertencia en color rojo destacando que no se permite publicar sesiones con menos de 24 horas de margen para garantizar la convocatoria de estudiantes. Presenta el botón `<button onClick={handleAdjustDate}>Ajustar Fecha</button>`. |
| **E002-1.2** Hace clic en el botón "Ajustar Fecha". | **E002-1.3** Asigna el foco al selector de fecha y hora, sugiriendo una fecha válida posterior a 24 horas, y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Aforo sobrepasa los límites institucionales
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 4 del Flujo Normal, `offer_service.py` detecta que el valor de aforo ingresado excede el límite máximo institucional establecido en RN-05 (aforo > 10 para modalidad presencial o aforo > 20 para virtual). Lanza `HTTPException(status_code=400, detail="CAPACITY_EXCEEDED: El aforo máximo permitido es de 10 estudiantes en modalidad presencial y 20 en modalidad virtual.")`.<br><br>En `OfferPublishView.tsx`, se despliega un mensaje de error en color rojo junto al campo de vacantes indicando el límite reglamentario. |
| **E003-1.2** Ajusta el número de vacantes al rango permitido (1 a 10 en presencial o 1 a 20 en virtual). | **E003-1.3** Actualiza el valor en el estado del componente y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E004: Conflicto de horario o traslape de espacio físico
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 6 del Flujo Normal, la consulta de solapamiento en `offer_service.py` detecta que el mentor ya tiene una sesión programada en ese bloque horario, o que el aula física seleccionada se encuentra reservada. Lanza `HTTPException(status_code=409, detail="SCHEDULE_CONFLICT: Existe un traslape de horario con otra sesión programada del mentor o el aula física ya se encuentra ocupada.")`.<br><br>En `OfferPublishView.tsx`, se captura el error 409 y se despliega una alerta en color ámbar explicando el conflicto de horario. Presenta el botón `<button onClick={handleReschedule}>Cambiar Horario o Aula</button>`. |
| **E004-1.2** Hace clic en el botón "Cambiar Horario o Aula". | **E004-1.3** Habilita nuevamente los selectores de franja horaria y aula, y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E005: Enlace de videoconferencia virtual inválido
| Usuario | Sistema |
|---|---|
| | **E005-1.1** En el paso 6 del Flujo Normal, para modalidad virtual, `offer_service.py` valida la URL de reunión contra patrones autorizados institucionales (e.g. `meet.google.com`). Si la URL no coincide con el dominio institucional autorizado, lanza `HTTPException(status_code=400, detail="INVALID_MEETING_URL: El enlace de videoconferencia debe pertenecer a la plataforma institucional Google Meet.")`.<br><br>En `OfferPublishView.tsx`, se resalta el cuadro de texto del enlace en color rojo con el mensaje de dominio no autorizado. |
| **E005-1.2** Ingresa un enlace válido de videoconferencia universitaria. | **E005-1.3** Valida la estructura del enlace en cliente y retorna al paso 3 del Flujo Normal de Eventos. |

#### CUS-008 - Consultar disponibilidad de espacios y recursos

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-008** (CUS-008) |
| **Nombre** | Consultar disponibilidad de espacios físicos y aulas de la EPIS |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-009 (Aprovisionamiento automatizado de infraestructura), RF-010 (Procesamiento de cronogramas y horarios institucionales); RN-06 (Prevención de colisión horaria de espacios), RN-07 (Horario operativo institucional 08:00 - 20:00) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los mentores y administradores consultar en tiempo real la disponibilidad de aulas físicas, laboratorios y salas de estudio de la EPIS-UPT antes de programar una sesión presencial. El frontend `OfferPublishView.tsx` invoca a `offerService.ts` despachando una petición `GET /api/v1/offers/spaces/availability` con parámetros de fecha y rango horario. El backend `aplicacion/backend/app/api/v1/endpoints/offers.py` delega a `app/services/offer_service.py`, el cual valida que la franja horaria se sitúe estrictamente dentro del horario operativo de la universidad (08:00 a 20:00 horas conforme a RN-07) y consulta las sesiones activas en `sesiones_mentoria` junto con el cronograma académico institucional. Retorna un listado de espacios disponibles con aforo y equipamiento, o sugiere alternativas de modalidad virtual si los espacios físicos se encuentran saturados. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-04: Planificación, Espacios y Agendamiento)<br>Manual de Uso de Infraestructura y Laboratorios EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/OfferPublishView.tsx` (Subcomponente de consulta de aulas)<br>`aplicacion/frontend/src/services/offerService.ts` (`OfferService.checkSpaceAvailability`)<br>`aplicacion/backend/app/api/v1/endpoints/offers.py` (`GET /api/v1/offers/spaces/availability`)<br>`aplicacion/backend/app/services/offer_service.py` (`OfferService.check_space_availability`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Usuario autenticado con token JWT institucional activo.<br>2. Catálogo institucional de aulas físicas y laboratorios registrado en el sistema.<br>3. Fecha de consulta fijada en día hábil académico universitario. |
| **PostCondiciones** | 1. Respuesta JSON generada con la nómina de aulas libres, aforos máximos y recursos audiovisuales disponibles.<br>2. Ninguna mutación destructiva o bloqueo persistente generado en base de datos (operación de lectura idempotente).<br>3. Despliegue interactivo en la interfaz cliente para selección de aula por parte del usuario. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Definición de criterios temporales y despacho de consulta** | |
| **1.** El mentor selecciona la fecha proyectada y la franja horaria (hora de inicio y hora de fin) en el selector de espacios de `OfferPublishView.tsx` y hace clic en `"Consultar Aulas Disponibles"`. | **2.** En `offerService.ts`, se valida que la franja horaria se encuentre dentro de la jornada universitaria institucional de 08:00 a 20:00 horas (RN-07). Despacha una petición `GET /api/v1/offers/spaces/availability?date=...&start_time=...&end_time=...`. En `offers.py`, el controlador valida los parámetros y delega a `offer_service.py`. (Si el horario ingresado se encuentra fuera del rango institucional de 08:00 a 20:00, salta a E001). |
| **Fase 2: Verificación de ocupación en base de datos y renderización de resultados** | |
| **3.** El mentor espera la respuesta mientras el componente visualiza un indicador de carga en color azul institucional. | **4.** En `offer_service.py`, se ejecuta una consulta para excluir aulas con sesiones activas en ese bloque: `SELECT a.id, a.codigo, a.capacidad, a.equipamiento FROM aulas a WHERE a.activa = true AND a.id NOT IN (SELECT aula_id FROM sesiones_mentoria WHERE fecha = :fecha AND NOT (hora_fin <= :start OR hora_inicio >= :end) AND estado IN ('PUBLICADA', 'CONFIRMADA'))`. Retorna HTTP 200 con la lista de aulas libres. En cliente, `OfferPublishView.tsx` renderiza una cuadrícula de tarjetas de aulas indicando aforo, ubicación y equipamiento. (Si todas las aulas físicas se encuentran ocupadas en ese bloque, salta a A001). (Si el repositorio de infraestructura reporta falla de comunicación, salta a E002). |
| **5.** El mentor hace clic en el aula física deseada y presiona el botón `"Asignar Aula a la Oferta"`. | **6.** El componente asigna el identificador del aula al formulario de publicación, actualiza el indicador visual en color verde con el texto *"Aula reservada provisionalmente"* y habilita el avance del flujo de publicación. |

##### Flujos Alternativos

##### Flujo alternativo A001: Aulas físicas agotadas con sugerencia de modalidad virtual
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 4 del Flujo Normal, la consulta retorna cero aulas libres para el horario solicitado. | **A001-1.2** En `OfferPublishView.tsx`, se despliega un panel informativo en color ámbar: *"Todas las aulas físicas se encuentran ocupadas en la franja horaria seleccionada. Se sugiere cambiar a Modalidad Virtual o modificar la hora de inicio"*. Presenta el botón `<button onClick={handleSwitchToVirtual}>Cambiar a Modalidad Virtual</button>` y el botón `<button onClick={handleAdjustTime}>Modificar Horario</button>`. |
| **A001-1.3** El mentor hace clic en el botón "Cambiar a Modalidad Virtual". | **A001-1.4** El sistema conmuta la modalidad de la sesión a `VIRTUAL`, habilita el campo para enlace de Google Meet, actualiza el límite de aforo a 20 estudiantes (RN-05) y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Horario fuera de la jornada institucional
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `offer_service.py` comprueba que la hora de inicio es anterior a las 08:00 o la hora de fin posterior a las 20:00 (infracción de RN-07). Lanza `HTTPException(status_code=400, detail="OPERATIONAL_HOURS_VIOLATION: El servicio de infraestructura opera estrictamente entre las 08:00 y las 20:00 horas.")`.<br><br>En `OfferPublishView.tsx`, se captura el error y se muestra una advertencia en color rojo indicando que la universidad no permite el uso de aulas físicas fuera de la jornada reglamentaria. |
| **E001-1.2** Modifica la franja horaria seleccionando un horario dentro de las 08:00 y 20:00. | **E001-1.3** Actualiza los valores en el selector y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Falla de conexión con el repositorio de infraestructura
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, la consulta relacional hacia el catálogo de aulas sufre timeout o interrupción de conexión. Lanza `HTTPException(status_code=503, detail="INFRASTRUCTURE_UNAVAILABLE: No se pudo verificar la disponibilidad de espacios físicos. Intente nuevamente en unos minutos.")`.<br><br>En `OfferPublishView.tsx`, se muestra un mensaje de alerta en color rojo indicando la indisponibilidad temporal del servicio. Presenta el botón `<button onClick={handleRetryCheck}>Reintentar Consulta</button>`. |
| **E002-1.2** Hace clic en el botón "Reintentar Consulta". | **E002-1.3** Dispara nuevamente la petición `GET /api/v1/offers/spaces/availability` y retorna al paso 1 del Flujo Normal de Eventos. |
"""
