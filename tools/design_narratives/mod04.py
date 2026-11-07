# -*- coding: utf-8 -*-
"""
Modulo 04: Demanda y Recomendaciones Personalizadas (Fase de Diseño)
Contiene: CUS-002, CUS-003
"""

def get_mod04():
    return """### MOD-04: Demanda y Recomendaciones Personalizadas

#### CUS-002 - Explorar recomendaciones personalizadas Top-k

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-002** (CUS-002) |
| **Nombre** | Explorar cartelera inteligente de recomendaciones de mentoría Top-k |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-006 (Inferencia de recomendaciones y ranking Top-k); RN-04 (Ventana de antelación mínima de 24 horas), RN-11 (Ponderación algorítmica de asignaturas filtro) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 03 - Sprint 04 |
| **Descripción** | Permite a los estudiantes mentoreados visualizar una cartelera adaptativa de sesiones de mentoría clasificadas según su relevancia académica individual mediante el componente cliente `RecommendationFeedView.tsx` y el servicio `recommendationService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/recommendations.py` procesa la petición `GET /api/v1/recommendations/top-k?limit=6`, delegando al servicio `app/services/recommendation_service.py`. El motor analiza el vector de intereses y asignaturas matriculadas del estudiante extraído de `perfiles_academicos`, computa la similitud de cosenos respecto a las sesiones en estado `PUBLICADA` con antelación mayor a 24 horas (`fecha_inicio > now_utc + 24h`, RN-04), aplica bonificaciones para materias filtro (`es_filtro = true`, RN-11) y penaliza sesiones con aforo próximo a agotarse. Retorna una nómina ordenada de las mejores k recomendaciones serializadas en el modelo Pydantic `TopKRecommendationResponse`. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-03: Motor de Recomendación Inteligente EdRecSys)<br>Algoritmos de Recomendación Basados en Contenido y Filtrado Híbrido |
| **Anexos** | `aplicacion/frontend/src/components/RecommendationFeedView.tsx`<br>`aplicacion/frontend/src/services/recommendationService.ts` (`RecommendationService`, `ApiRecommendationAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/recommendations.py` (`GET /api/v1/recommendations/top-k`)<br>`aplicacion/backend/app/services/recommendation_service.py` (`RecommendationService.get_top_k_recommendations`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`), `app/models/profile.py` (`PerfilAcademico`), `app/models/curriculum.py` (`Curso`, `TemaCurricular`) |
| **Precondiciones** | 1. Estudiante mentoreado autenticado con token JWT institucional activo en `localStorage`.<br>2. Al menos una sesión de mentoría en estado `PUBLICADA` con antelación superior a 24 horas y vacantes disponibles.<br>3. Registro de perfil académico o cursos matriculados en la base de datos. |
| **PostCondiciones** | 1. Payload JSON serializado con las k sesiones más afines y sus puntuaciones de compatibilidad retornadas al frontend.<br>2. Consulta de lectura sin efectos colaterales persistentes ni mutaciones de datos en PostgreSQL.<br>3. Despliegue de la cartelera interactiva con tarjetas informativas y botones de reserva activados. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso a la cartelera y solicitud de recomendaciones Top-k** | |
| **1.** El mentoreado accede a la página principal de la plataforma en `RecommendationFeedView.tsx`. | **2.** En `recommendationService.ts`, se despacha `GET /api/v1/recommendations/top-k?limit=6` incluyendo el token Bearer institucional. En `recommendations.py`, el controlador extrae el UUID del usuario del token JWT y delega a `recommendation_service.py`. El servicio recupera el perfil académico del estudiante y sus materias matriculadas. (Si el estudiante no registra historial ni materias configuradas, salta a A001). (Si el motor de recomendación sufre una excepción de cálculo o timeout, salta a E001). |
| **Fase 2: Ejecución del algoritmo de emparejamiento y ordenamiento de compatibilidad** | |
| **3.** El usuario visualiza un esqueleto animado de tarjetas mientras se calculan las recomendaciones. | **4.** En `recommendation_service.py`, se recuperan las sesiones en estado `PUBLICADA` con `fecha_inicio > now_utc + timedelta(hours=24)` y `occupied_seats < aforo_maximo`. Para cada oferta, se calcula el puntaje ponderado: $Score = 0.5 \times SimilitudCursos + 0.3 \times FactorFiltro + 0.2 \times UrgenciaTemporal$. Se ordenan de forma descendente y se toman las primeras 6 ofertas. Retorna HTTP 200 con el payload `TopKRecommendationResponse`. En cliente, `RecommendationFeedView.tsx` renderiza las tarjetas con: nombre del tema curricular, nombre de la asignatura, fecha y hora de la sesión, modalidad (Presencial/Virtual con aula o enlace), número de vacantes restantes y un distintivo en color azul institucional indicando el porcentaje de compatibilidad (e.g. *"95% de afinidad"*). (Si no existen ofertas activas para sus materias, salta a A002). |
| **Fase 3: Selección de sesión para reserva de cupo** | |
| **5.** El mentoreado revisa las tarjetas de recomendación y hace clic en el botón `"Reservar Cupo"` de la sesión de su preferencia. | **6.** En `RecommendationFeedView.tsx`, se captura el identificador de la sesión seleccionada y se abre el componente modal `BookingModalView.tsx`, transfiriendo el flujo a la especificación técnica de reserva formal de cupo (CUS-004). |

##### Flujos Alternativos

##### Flujo alternativo A001: Estudiante nuevo sin historial académico (Fallback por popularidad)
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 2 del Flujo Normal, `recommendation_service.py` detecta que el estudiante no tiene historial académico ni materias configuradas en su perfil. | **A001-1.2** El servicio conmuta automáticamente a la estrategia de respaldo ("Cold Start"): ejecuta una consulta para seleccionar las sesiones de mentoría más populares y con mayor demanda en asignaturas filtro generales de los primeros ciclos (`es_filtro = true`). |
| **A001-1.3** El estudiante visualiza las tarjetas de oferta acompañadas de una insignia informativa en color ámbar: *"Ofertas destacadas para estudiantes de primeros ciclos"*. | **A001-1.4** El sistema presenta el botón `<button onClick={handleConfigureProfile}>Configurar Mis Materias</button>` para personalizar futuras recomendaciones y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo alternativo A002: Cartelera vacía por ausencia de sesiones disponibles
| Usuario | Sistema |
|---|---|
| **A002-1.1** En el paso 4 del Flujo Normal, la consulta de sesiones publicadas retorna cero registros con vacantes disponibles. | **A002-1.2** En `RecommendationFeedView.tsx`, se despliega un panel centralizado con un ícono ilustrativo en color azul institucional y el texto: *"No hay sesiones de mentoría programadas actualmente para tus materias. Puedes solicitar la apertura de un tema registrando tu demanda académica"*. Presenta el botón `<button onClick={handleOpenDemandModal}>Registrar Solicitud por Demanda</button>`. |
| **A002-1.3** El estudiante hace clic en el botón "Registrar Solicitud por Demanda". | **A002-1.4** El sistema abre el modal de registro de demanda académica (CUS-003) y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Error de cómputo en el motor de recomendación
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, el servicio `recommendation_service.py` encuentra una falla de serialización de vectores o un timeout interno en base de datos. Lanza `HTTPException(status_code=500, detail="RECOMMENDER_ENGINE_ERROR: Ocurrió un error al procesar las recomendaciones personalizadas.")`.<br><br>En `RecommendationFeedView.tsx`, se captura el error 500 y se despliega un panel de advertencia en color rojo. Presenta el botón `<button onClick={fetchRecommendations}>Reintentar Cartelera</button>`. |
| **E001-1.2** Hace clic en el botón "Reintentar Cartelera". | **E001-1.3** Dispara nuevamente la petición `GET /api/v1/recommendations/top-k` y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-003 - Registrar solicitud de demanda académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-003** (CUS-003) |
| **Nombre** | Registrar solicitud de mentoría por demanda académica no atendida |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-007 (Registro y banco de solicitudes por demanda); RN-04 (Antelación de planificación institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 03 - Sprint 04 |
| **Descripción** | Permite a los estudiantes mentoreados expresar una necesidad formativa insatisfecha cuando no existen ofertas disponibles sobre un tema curricular específico a través del formulario modal en `RecommendationFeedView.tsx` y el servicio `recommendationService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/recommendations.py` y `app/services/recommendation_service.py` procesan la petición `POST /api/v1/recommendations/demand`, validando los campos con Pydantic (`DemandCreateRequest`). El sistema verifica que el estudiante no cuente con una solicitud idéntica en estado `PENDIENTE` para el mismo tema, persiste el registro en la tabla `demandas_academicas` e incrementa el contador de demanda agrupada en caché para alertar a los mentores calificados en su panel de publicación (CUS-006). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-03: Motor de Recomendación Inteligente EdRecSys)<br>Gestión de Demanda Académica EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/RecommendationFeedView.tsx` (Subcomponente de Solicitud de Demanda)<br>`aplicacion/frontend/src/services/recommendationService.ts` (`RecommendationService.createDemand`)<br>`aplicacion/backend/app/api/v1/endpoints/recommendations.py` (`POST /api/v1/recommendations/demand`)<br>`aplicacion/backend/app/services/recommendation_service.py` (`RecommendationService.create_demand_request`)<br>`aplicacion/backend/app/models/curriculum.py` (`TemaCurricular`), `app/models/profile.py` (`DemandaAcademica`) |
| **Precondiciones** | 1. Mentoreado autenticado con token JWT institucional activo.<br>2. Tema curricular seleccionado perteneciente a una asignatura vigente en el catálogo oficial.<br>3. Inexistencia de solicitud pendiente previa idéntica del mismo estudiante para dicho tema. |
| **PostCondiciones** | 1. Registro insertado en la tabla `demandas_academicas` con `estado = 'PENDIENTE'` y marca de tiempo UTC.<br>2. Incremento atómico del acumulador de solicitudes del tema para priorización algorítmica.<br>3. Notificación de confirmación en cliente y cierre del modal de demanda. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura del formulario de demanda y selección temática** | |
| **1.** El mentoreado hace clic en el botón `"Registrar Demanda de Tema"` en la cabecera de `RecommendationFeedView.tsx` o en el catálogo curricular. | **2.** El sistema abre una ventana modal `"Solicitud de Mentoría por Demanda"`. Despacha la consulta de asignaturas y temas silábicos para poblar las listas desplegables. Renderiza los campos: selección de curso, tema curricular específico, franja horaria preferida (mañana, tarde o noche), modalidad predilecta (Presencial/Virtual) y un cuadro de texto para comentarios adicionales. |
| **Fase 2: Ingreso de preferencias y despacho de solicitud** | |
| **3.** El mentoreado selecciona la asignatura, el tema silábico específico, marca su franja horaria predilecta y presiona el botón `"Enviar Solicitud"`. | **4.** En `RecommendationFeedView.tsx`, se valida que se hayan seleccionado la materia y el tema. En `recommendationService.ts`, se despacha `POST /api/v1/recommendations/demand` con el payload `DemandCreateRequest`. En `recommendations.py`, `recommendation_service.py` ejecuta una verificación para descartar duplicados activos: `SELECT id FROM demandas_academicas WHERE estudiante_id = :uid AND tema_id = :tid AND estado = 'PENDIENTE'`. (Si faltan campos obligatorios en el formulario, salta a E001). (Si el estudiante ya cuenta con una solicitud pendiente para el mismo tema, salta a E002). |
| **Fase 3: Registro transaccional e indexación de demanda grupal** | |
| **5.** El mentoreado visualiza el indicador de procesamiento en el botón de envío. | **6.** En `recommendation_service.py`, se ejecuta `INSERT INTO demandas_academicas (estudiante_id, tema_id, franja_preferida, modalidad_preferida, estado, fecha_solicitud) VALUES (...)`. Se confirma la transacción con `db.commit()` y se actualiza el agregado de solicitudes por tema en caché. Retorna HTTP 201 Created con el objeto `DemandResponse`. En cliente, `RecommendationFeedView.tsx` cierra el modal y despliega una notificación flotante en color verde de éxito: *"Tu solicitud de demanda ha sido registrada exitosamente. Los mentores habilitados recibirán una alerta sobre la necesidad formativa de este tema."* |

##### Flujos de Excepción

##### Flujo de excepción E001: Formulario de demanda incompleto
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el validador en cliente o Pydantic en `recommendations.py` comprueba que no se ha seleccionado tema o asignatura. Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: Debe seleccionar obligatoriamente una materia y tema curricular para registrar su demanda.")`.<br><br>En el modal de demanda, se resaltan los campos vacíos con borde en color rojo y texto explicativo. |
| **E001-1.2** Selecciona la asignatura y el tema silábico en los desplegables. | **E001-1.3** Rehabilita el botón `"Enviar Solicitud"` y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Solicitud duplicada de demanda pendiente
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, `recommendation_service.py` detecta un registro previo en estado `PENDIENTE` para la misma tupla `(estudiante_id, tema_id)`. Lanza `HTTPException(status_code=409, detail="DUPLICATE_DEMAND: Ya mantienes una solicitud activa registrada para este tema. Los mentores ya pueden visualizar esta necesidad formativa.")`.<br><br>En el modal, se despliega una alerta en color ámbar explicando la existencia previa de la solicitud. Presenta el botón `<button onClick={handleCloseModal}>Entendido</button>`. |
| **E002-1.2** Hace clic en el botón "Entendido". | **E002-1.3** Cierra la ventana modal sin generar registros redundantes y retorna al paso 1 del Flujo Normal de Eventos. |
"""
