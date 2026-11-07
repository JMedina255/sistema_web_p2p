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
| **Requisito ID (RF)** | RF-008 (Publicación y parametrización de ofertas de mentoría), RF-009 (Aprovisionamiento automatizado de infraestructura); RN-01 (Autenticación y pertenencia de cuenta institucional), RN-03 (Mérito académico y habilitación de mentor ciclo >= VII), RN-04 (Ventana de antelación mínima de 24 horas a T-24h), RN-05 (Aforo máximo estricto de 10 presencial y 20 virtual) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los estudiantes mentores formalizar la apertura de una sesión de mentoría a través del componente cliente `OfferPublishView.tsx` y el servicio `offerService.ts`, despachando una petición `POST /api/v1/offers` hacia el controlador `aplicacion/backend/app/api/v1/endpoints/offers.py`. El backend valida el token JWT institucional extrayendo criptográficamente el claim del llamante mediante `_extract_caller_and_admin_status`, verificando que coincida con el correo del mentor o cuente con rol de administrador (RN-01). En `app/services/offer_service.py` (`OfferService.publish_offer`), se ejecutan las validaciones de negocio institucionales: comprobación de mérito académico y habilitación de mentor en ciclo >= VII (`validate_mentor_eligibility`, RN-03), cálculo estricto de antelación superior a 24 horas respecto a la fecha y hora actual en UTC (`calculate_advance_hours > 24h`, RN-04), y conformidad de capacidad según la modalidad (exactamente 10 cupos en presencial y 20 en virtual, RN-05). Se instancia y persiste la entidad ORM `SesionMentoria` (`app/models/offer.py`) en estado `PUBLICADA`, se confirma la transacción en PostgreSQL, se emite una respuesta HTTP 201 Created con el esquema `PublishOfferResponse` y se sincroniza la cartelera institucional en cliente. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-04: Planificación, Espacios y Agendamiento)<br>Reglamento Académico de Mentorías EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/OfferPublishView.tsx`<br>`aplicacion/frontend/src/services/offerService.ts` (`OfferService`, `ApiOfferAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/offers.py` (`POST /api/v1/offers`)<br>`aplicacion/backend/app/services/offer_service.py` (`OfferService.publish_offer`, `OfferService.validate_mentor_eligibility`, `OfferService.calculate_advance_hours`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`), `app/models/roles.py` (`UsuarioRol`, `Rol`), `app/models/profile.py` (`PerfilAcademico`), `app/schemas/offer.py` (`PublishOfferPayload`, `PublishOfferResponse`) |
| **Precondiciones** | 1. Usuario autenticado con token JWT institucional activo conteniendo el rol `UserRole.mentor`.<br>2. Perfil de mentor registrado en `perfiles_academicos` con ciclo académico actual >= VII (RN-03).<br>3. Fecha y hora de inicio fijadas con más de 24 horas de antelación respecto a la hora UTC actual del servidor (RN-04). |
| **PostCondiciones** | 1. Registro insertado en la tabla `sesiones_mentoria` con `estado = 'PUBLICADA'`, código de sesión generado `SES-XXXX` y aforo parametrizado.<br>2. Transacción confirmada en PostgreSQL (`db.commit()`) y refresco de entidad (`db.refresh()`).<br>3. Despliegue de comprobante de publicación en cliente con código identificador de sesión y botón para navegar a la cartelera o mis sesiones. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Configuración de la sesión y selección curricular** | |
| **1.** El estudiante mentor accede a la vista de publicación en `OfferPublishView.tsx` y selecciona la asignatura curricular en la lista desplegable `"Curso"`. | **2.** En `OfferPublishView.tsx`, se invoca `fetchCourseDetail(selectedCourseId)` despachando `GET /api/v1/curriculum/courses/{id}` hacia `endpoints/curriculum.py`. El backend ejecuta `CurriculumService.get_course_by_id(db, course_id)` consultando `temas_curriculares` en PostgreSQL y retorna HTTP 200 OK con `CourseDetailResponse`. `OfferPublishView.tsx` renderiza la lista de temas silábicos, los selectores de fecha y hora de inicio, duración (60 o 90 minutos), modalidad (`presencial` o `virtual`), aula física sugerida o enlace Google Meet (`https://meet.google.com/upt-epis-...`), y asigna el aforo reglamentario inmutable según RN-05 (10 para presencial, 20 para virtual). |
| **Fase 2: Ingreso de parámetros, validación de reglas de aforo y antelación** | |
| **3.** El mentor selecciona el tema silábico, especifica la fecha y hora programada, confirma la modalidad, verifica los cupos reglamentarios y hace clic en el botón `"Verificar y Publicar"`. | **4.** En `OfferPublishView.tsx`, se invoca `validateOfferPayload(payload)`. Si la sintaxis es válida, en `offerService.ts` (`ApiOfferAdapter.publishOffer`) se despacha `POST /api/v1/offers` con el payload `PublishOfferPayload` adjuntando el encabezado `Authorization: Bearer <jwt_token>`. En `endpoints/offers.py`, el controlador extrae la identidad del llamante mediante `_extract_caller_and_admin_status(authorization, payload.mentor_email)`. El controlador delega a `offer_service.OfferService.publish_offer(db, payload, caller_email, is_admin)`. El servicio valida: 1) que `caller_email == payload.mentor_email` o `is_admin == True` (RN-01), 2) que el mentor cumpla mérito académico en `usuario_roles` y `perfiles_academicos` con `ciclo_actual >= 7` mediante `validate_mentor_eligibility(db, email)` (RN-03), 3) que `fecha_inicio > now_utc + timedelta(hours=24)` mediante `calculate_advance_hours(payload.fecha_inicio)` (RN-04), y 4) que `aforo_maximo == 10` para presencial o `== 20` para virtual (RN-05). (Si faltan campos obligatorios o la sintaxis es inválida en cliente o Pydantic, salta a E001). (Si la fecha de inicio es menor o igual a 24 horas de antelación respecto a UTC now, salta a E002). (Si el aforo no corresponde estrictamente al estándar institucional de 10 o 20 cupos, salta a E003). (Si el usuario no cuenta con acreditación de mentor o su ciclo es menor a VII, salta a E004). (Si existe discrepancia entre la identidad del token y el correo del mentor, salta a E005). |
| **Fase 3: Persistencia transaccional de la oferta y confirmación en cliente** | |
| **5.** El mentor espera la confirmación visual en el botón que presenta un indicador circular de procesamiento y el estado `isSubmitting = true`. | **6.** En `offer_service.py`, al validar todos los criterios normativos, se genera el identificador unívoco de sesión `code = f"SES-{_session_counter}"`, se instancia la entidad ORM `sesion_db = SesionMentoria(codigo_sesion=code, mentor_email=effective_email, id_asignatura=payload.id_asignatura, id_tema=payload.id_tema, fecha_inicio=start_dt, duracion_minutos=payload.duracion_minutos, modalidad=payload.modalidad, aforo_maximo=expected_capacity, espacio_asignado=payload.espacio_asignado, notas_adicionales=payload.notas_adicionales, estado="PUBLICADA")`, se ejecuta `db.add(sesion_db)`, se confirma la transacción mediante `db.commit()` y se refresca la entidad con `db.refresh(sesion_db)`. El backend retorna HTTP 201 Created serializando `PublishOfferResponse`. En `OfferPublishView.tsx`, se limpia el formulario, se invoca el callback `onOfferPublished(response)` para sincronizar la cartelera, y se despliega una tarjeta de confirmación en color verde con el código generado de sesión (e.g. `SES-1004`), el espacio asignado y el botón `"Ver en Mis Sesiones"`. |

##### Flujos de Excepción

##### Flujo de excepción E001: Campos obligatorios incompletos o sintaxis inválida
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `validateOfferPayload` en cliente o el validador Pydantic `PublishOfferPayload` en `endpoints/offers.py` detecta omisión de campos requeridos (e.g. tema curricular o fecha ausente). Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: Todos los campos de la sesión son obligatorios.")`.<br><br>En `OfferPublishView.tsx`, se capturan los errores y se resaltan los campos observados con borde en color rojo y texto explicativo. |
| **E001-1.2** Corrige los campos observados completando los datos requeridos. | **E001-1.3** Rehabilita el botón `"Verificar y Publicar"` y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Incumplimiento de antelación mínima de 24 horas a T-24h
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, `offer_service.py` calcula `advance_hours = calculate_advance_hours(payload.fecha_inicio)`. Al constatar que `advance_hours <= 24.0`, lanza `HTTPException(status_code=400, detail="Infracción de RN-04: Toda mentoría debe publicarse con una antelación superior a 24 horas respecto al inicio de la sesión para garantizar la confirmación de quórum.")`.<br><br>En `OfferPublishView.tsx`, se despliega un panel de advertencia en color rojo destacando que no se permite publicar sesiones con menos de 24 horas de margen para garantizar la convocatoria de estudiantes. Presenta el botón `<button onClick={handleAdjustDate}>Ajustar Fecha</button>`. |
| **E002-1.2** Hace clic en el botón "Ajustar Fecha". | **E002-1.3** Asigna el foco al selector de fecha y hora, sugiriendo una fecha válida posterior a 24 horas, y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Aforo reglamentario no conforme según modalidad
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 4 del Flujo Normal, `offer_service.py` detecta que `payload.aforo_maximo` no coincide con el estándar inmutable de RN-05 (`10` cupos para presencial o `20` para virtual). Lanza `HTTPException(status_code=400, detail="Infracción de RN-05: El aforo reglamentario para la modalidad presencial debe ser exactamente 10 estudiantes.")`.<br><br>En `OfferPublishView.tsx`, se despliega un mensaje de error en color rojo junto al campo de vacantes indicando el límite reglamentario. |
| **E003-1.2** Ajusta el número de vacantes al valor reglamentario exacto (10 en presencial o 20 en virtual). | **E003-1.3** Actualiza el valor en el estado del componente y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E004: Mentor no elegible por ciclo insuficiente o falta de rol acreditado
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 4 del Flujo Normal, `validate_mentor_eligibility(db, effective_email)` en `offer_service.py` consulta las tablas `usuario_roles` y `perfiles_academicos`. Si el usuario no tiene rol `mentor` activo o su ciclo es menor a VII (infracción de RN-03), lanza `HTTPException(status_code=403, detail="Infracción de RN-03: Solo los estudiantes habilitados con rol de mentor (ciclo >= VII) pueden publicar ofertas de mentoría.")`.<br><br>En `OfferPublishView.tsx`, se despliega una alerta roja indicando que su perfil no cumple los requisitos académicos de mentoría. |
| **E004-1.2** Hace clic en el botón "Revisar Perfil". | **E004-1.3** Redirige al usuario hacia el módulo de perfil académico (`CUS-005`) y finaliza el caso de uso. |

##### Flujo de excepción E005: Suplantación de identidad o discrepancia de credenciales del mentor
| Usuario | Sistema |
|---|---|
| | **E005-1.1** En el paso 4 del Flujo Normal, en `endpoints/offers.py` y `offer_service.py` se compara `caller_email` extraído criptográficamente del token JWT contra `payload.mentor_email`. Si no coinciden y el llamante no es administrador (infracción de RN-01), lanza `HTTPException(status_code=403, detail="No tiene autorización para publicar ofertas en nombre de otro usuario.")`.<br><br>En `OfferPublishView.tsx`, se captura el error 403 y se muestra una alerta roja de seguridad institucional. |
| **E005-1.2** Hace clic en el botón "Sincronizar Credenciales". | **E005-1.3** Recarga la identidad de la sesión activa en el formulario y retorna al paso 3 del Flujo Normal de Eventos. |

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
