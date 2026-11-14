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
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian |
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
| **Tipo** | Obligatorio (   ) / Opcional ( X ) |
| **Requisito ID (RF)** | RF-007 (Banco de solicitudes por demanda académica); RN-04 (Antelación de planificación institucional), RN-11 (Priorización curricular de materias formativas filtro); RNF04, RNF09 |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`, Primario); Estudiante Mentor (`UserRole.mentor`, Secundario) |
| **Interacción** | Fase de Construcción / Iteración Sprint 03 - Sprint 04 (Actualización Post-Sprint 08 con Banco de Demanda) |
| **Descripción** | Permite a los estudiantes mentoreados canalizar una necesidad formativa insatisfecha hacia el banco institucional de solicitudes por demanda cuando no existan ofertas vigentes que atiendan un tema silábico de interés o cuando el aforo de las sesiones publicadas se encuentre totalmente agotado. La interacción se inicia mediante el componente modal accesible MentoringDemandModalView.tsx, desplegable desde el panel de lista vacía en RecommendationFeedView.tsx o desde la alerta de sobrecupo en BookingModalView.tsx. El estudiante selecciona una asignatura curricular formativa y una unidad o tema silábico específico, ingresando opcionalmente una justificación u observación pedagógica. La petición se procesa en bookingService.ts y se despacha hacia el endpoint POST /api/v1/bookings/requests en el controlador aplicacion/backend/app/api/v1/endpoints/bookings.py. El servicio booking_service.py valida la integridad de los datos, descarta la existencia de solicitudes duplicadas activas para el mismo estudiante y tema, e inserta el registro en la tabla física solicitudes_demanda (app/models/booking.py) con estado 'PENDIENTE' y folio institucional correlativo #DEM-{id}. La solicitud queda disponible de forma inmediata en el panel de mentores (MentorSessionsView.tsx, pestaña "Banco de Solicitudes por Demanda") para formular sesiones de mentoría dirigida. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v3.0 - MOD-04: Demanda y Recomendaciones Personalizadas)<br>Modelo de Gestión de Demanda Académica EPIS-UPT |
| **Anexos** | aplicacion/frontend/src/components/MentoringDemandModalView.tsx<br>aplicacion/frontend/src/components/RecommendationFeedView.tsx<br>aplicacion/frontend/src/components/BookingModalView.tsx<br>aplicacion/frontend/src/components/MentorSessionsView.tsx<br>aplicacion/frontend/src/services/bookingService.ts (BookingService, ApiBookingAdapter)<br>aplicacion/frontend/src/services/apiClient.ts (fetchCourses, fetchCourseDetail)<br>aplicacion/backend/app/api/v1/endpoints/bookings.py (POST /api/v1/bookings/requests, GET /api/v1/bookings/requests)<br>aplicacion/backend/app/services/booking_service.py (BookingService.create_demand_request)<br>aplicacion/backend/app/models/booking.py (SolicitudDemanda), app/models/curriculum.py (Asignatura, TemaConceptual) |
| **Precondiciones** | 1. Estudiante mentoreado autenticado con token JWT institucional activo en localStorage.<br>2. Catálogo oficial de asignaturas críticas y temarios silábicos disponible en la base de datos.<br>3. Consentimiento informado digital formalizado previamente bajo la Ley Nº 29733. |
| **PostCondiciones** | 1. Registro formal insertado en la tabla física solicitudes_demanda con estado 'PENDIENTE' y folio institucional correlativo #DEM-{id}.<br>2. Solicitud disponible de forma inmediata en el Banco de Solicitudes por Demanda de los mentores acreditados en MentorSessionsView.tsx.<br>3. Despliegue de confirmación en cliente con resumen de solicitud y retorno ordenado a la cartelera de mentorías. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura del formulario de demanda y carga del catálogo silábico** | |
| **1.** El mentoreado visualiza la ausencia de sesiones afines en `RecommendationFeedView.tsx` o un aviso de aforo colapsado en `BookingModalView.tsx`, y hace clic en el botón `"Registrar Solicitud por Demanda"`. | **2.** En `MentoringDemandModalView.tsx`, se abre la ventana modal con cabecera en color azul institucional y título `"📋 Registrar Solicitud de Mentoría por Demanda"`. El hook `useEffect` invoca `fetchCourses(true)` en `apiClient.ts` para obtener la lista de materias formativas. El sistema renderiza el selector de asignaturas y consulta automáticamente los temas silábicos de la primera materia mediante `fetchCourseDetail(id)`. (Si el modal es invocado desde una sesión específica con aforo agotado, salta a A001). (Si la consulta del catálogo curricular falla por pérdida de red, salta a E004). |
| **Fase 2: Selección temática, justificación pedagógica y validación de reglas** | |
| **3.** El mentoreado selecciona la asignatura deseada en la lista desplegable `"Asignatura Curricular"`, selecciona la unidad o tema de aprendizaje en `"Tema o Unidad Específica"`, redacta su justificación en el área de texto `"Observaciones o Justificación de Necesidad Formativa"` y presiona el botón `"Enviar Solicitud"`. | **4.** En `MentoringDemandModalView.tsx`, se valida que se hayan seleccionado identificadores positivos para la materia y el tema. Se activa el estado transicional `isSubmitting = true` con texto `"Registrando..."`. En `bookingService.ts`, se despacha una petición `POST /api/v1/bookings/requests` enviando el payload `{"id_asignatura": selectedCourseId, "id_tema": selectedTopicId, "observaciones": observaciones}` hacia el controlador `bookings.py`. El backend valida con Pydantic (`SolicitudDemandaCreate`) la integridad de los datos. En `booking_service.py`, se ejecuta una consulta para verificar que no exista una solicitud activa en estado `PENDIENTE` para el mismo estudiante y tema: `SELECT id_demanda FROM solicitudes_demanda WHERE estudiante_email = :email AND id_tema = :tid AND estado = 'PENDIENTE'`. (Si el mentoreado omite seleccionar la asignatura o el tema silábico, salta a E001). (Si la materia seleccionada no cuenta con temarios silábicos registrados, salta a E002). (Si el estudiante ya cuenta con una solicitud activa idéntica para ese mismo tema, salta a E003). (Si el mentoreado decide cancelar el registro o pulsa la tecla Escape, salta a A002). |
| **Fase 3: Registro transaccional en el banco de demanda y confirmación visual** | |
| **5.** El mentoreado observa el estado de procesamiento en pantalla con los controles temporalmente bloqueados. | **6.** En `booking_service.py`, se ejecuta la inserción relacional `INSERT INTO solicitudes_demanda (estudiante_email, id_asignatura, id_tema, observaciones, estado, created_at) VALUES (...)`. Se confirma la transacción con `db.commit()` y se retorna HTTP 201 Created con el payload `SolicitudDemandaResponse`. En cliente, `MentoringDemandModalView.tsx` oculta el formulario y conmuta al panel de confirmación de éxito con fondo blanco, círculo en color verde claro con marca de verificación en color verde oscuro, título `"¡Solicitud Registrada con Éxito!"` y el folio institucional `#DEM-{id}` asignado, explicando que los mentores acreditados podrán formular ofertas dirigidas. El usuario pulsa el botón `"Entendido"` para cerrar el diálogo modal y retornar a la cartelera. (Si ocurre un error interno en la base de datos durante la persistencia, salta a E004). |

##### Flujos Alternativos

##### Flujo alternativo A001: Invocación del modal desde alerta de aforo agotado en reserva con preselección
| Usuario | Sistema |
|---|---|
| **A001-1.1** En `BookingModalView.tsx`, el mentoreado constata que los cupos de una sesión de su interés se han agotado (`available_slots <= 0`) y hace clic en el botón de acción secundaria `"Registrar Solicitud por Demanda"`. | **A001-1.2** `BookingModalView.tsx` invoca el callback de apertura transfiriendo las propiedades `preselectedCourseId` y `preselectedTopicId` hacia `MentoringDemandModalView.tsx`. |
| **A001-1.3** El mentoreado observa que el modal se abre con la asignatura y el tema silábico de la sesión original ya preseleccionados en las listas desplegables. | **A001-1.4** El sistema bloquea las selecciones correspondientes, enfoca directamente el cuadro de texto `"Observaciones o Justificación de Necesidad Formativa"` y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo alternativo A002: Cancelación voluntaria del registro de demanda con botón Cancelar o tecla Escape
| Usuario | Sistema |
|---|---|
| **A002-1.1** El mentoreado hace clic en el botón `"Cancelar"`, pulsa el botón de cierre en la cabecera del modal o presiona la tecla `Escape` en su teclado. | **A002-1.2** `MentoringDemandModalView.tsx` captura el evento, cancela las peticiones asíncronas en curso y purga el estado local del formulario. |
| **A002-1.3** El mentoreado observa el cierre suave del cuadro de diálogo modal retornando el foco a la vista anterior. | **A002-1.4** El sistema desmonta la ventana modal del árbol de componentes y finaliza el caso de uso sin generar registros. |

##### Flujos de Excepción

##### Flujo de excepción E001: Formulario de solicitud incompleto por omisión de asignatura o tema
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el usuario presiona el botón `"Enviar Solicitud"` sin haber seleccionado una materia o un tema silábico (`selectedCourseId === 0` o `selectedTopicId === 0`). `MentoringDemandModalView.tsx` bloquea el envío y despliega un banner de alerta en color rojo con el mensaje: *"Por favor seleccione una asignatura y un tema curricular válido."*. |
| **E001-1.2** El estudiante selecciona la asignatura y el tema en las listas desplegables. | **E001-1.3** Oculta la alerta de error, rehabilita el botón de envío y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Asignatura formativa sin temarios silábicos disponibles en catálogo
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, tras seleccionar una asignatura, la consulta `fetchCourseDetail(id)` retorna una lista de temas vacía (`detail.temas.length === 0`). El selector de temas se deshabilita mostrando la opción: *"No hay temas registrados para esta materia"*, y el botón `"Enviar Solicitud"` se bloquea en color gris claro. |
| **E002-1.2** El estudiante cambia la selección hacia otra asignatura formativa que sí contenga temarios silábicos activos. | **E002-1.3** Carga reactivamente los temas disponibles, rehabilita el botón de acción y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Solicitud duplicada activa para el mismo estudiante y tema silábico
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 4 del Flujo Normal, `booking_service.py` localiza una tupla activa previa en `solicitudes_demanda` con el mismo correo y tema en estado `PENDIENTE`. Lanza `HTTPException(status_code=400, detail="Ya mantienes una solicitud activa registrada para este tema en el banco de demanda.")`.<br><br>En `bookingService.ts`, captura el error y propaga el mensaje hacia el modal. `MentoringDemandModalView.tsx` despliega una alerta en color ámbar explicando la preexistencia de la solicitud. Presenta el botón `"Entendido"`. |
| **E003-1.2** Hace clic en el botón "Entendido". | **E003-1.3** Cierra la ventana modal sin generar registros redundantes y finaliza el caso de uso sin generar registros. |

##### Flujo de excepción E004: Error de comunicación con el servicio de reservas y banco de demanda
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 2 o 6 del Flujo Normal, ocurre pérdida de enlace o indisponibilidad en el backend (`HTTP 500` o `HTTP 503`). `bookingService.ts` o `apiClient.ts` captura la excepción de red.<br><br>En `MentoringDemandModalView.tsx`, se restablece `isSubmitting = false` y se despliega un banner de alerta en color rojo: *"Error al registrar la solicitud por demanda."*. Presenta el botón `"Reintentar"`. |
| **E004-1.2** Hace clic en el botón "Reintentar". | **E004-1.3** Mantiene los datos redactados en el formulario y retorna al paso 1 del Flujo Normal de Eventos sin generar registros. |

##### Especificación Exhaustiva de Interfaz de Usuario y Comportamiento Visual

La interfaz de usuario del componente `MentoringDemandModalView.tsx` está diseñada bajo principios de usabilidad y accesibilidad WCAG 2.1 AA:
1. **Capa de Superposición (Overlay):** Fondo fijo con cobertura total de pantalla en color gris pizarra oscuro semitransparente con desenfoque de fondo (*backdrop blur*), bloqueando clics en elementos subyacentes.
2. **Contenedor Modal:** Cuadro de diálogo centralizado en color blanco puro con esquinas redondeadas, sombra pronunciada de elevación y diseño responsivo adaptativo con un ancho máximo estandarizado.
3. **Cabecera Institucional:** Barra superior en color azul institucional con tipografía en color blanco puro conteniendo el título `"📋 Registrar Solicitud de Mentoría por Demanda"`, subtítulo explicativo en color celeste grisáceo `"Caso de Uso CUS03 / RF07 — Banco Institucional EPIS UPT"` y botón de cierre en la esquina derecha con símbolo de aspa en color blanco puro.
4. **Párrafo Orientador:** Texto explicativo en color gris azulado detallando que si el estudiante no encuentra sesiones activas o las plazas están agotadas, puede registrar su necesidad para que mentores de ciclos superiores formulen ofertas específicas.
5. **Selectores Desplegables:** Campo de selección `"Asignatura Curricular"` con etiqueta en color gris oscuro y asterisco obligatorio en color rojo. Al cambiar de asignatura, el campo dependiente `"Tema o Unidad Específica"` se actualiza en tiempo real mostrando el código de unidad silábica y el nombre del tema.
6. **Área de Justificación Pedagógica:** Campo de texto multilínea con tres filas de altura, borde en color gris claro y texto de sugerencia (*placeholder*) en color gris tenue: `"Ej: Requiero nivelación en límites algebraicos y aplicaciones de derivadas para la próxima práctica calificada."`.
7. **Botones de Control:** En la parte inferior derecha, botón secundario `"Cancelar"` con fondo en color gris claro, borde gris y texto en gris oscuro; y botón principal de envío `"Enviar Solicitud"` con fondo en color azul institucional y texto en blanco puro (deshabilitado en color gris pizarra cuando los campos no están completos o mostrando `"Registrando..."` durante el despacho).
8. **Panel de Confirmación de Éxito:** Tras la persistencia exitosa, el modal transmuta a una tarjeta de felicitación con un círculo central en color verde claro conteniendo el símbolo de verificación en color verde oscuro, título en color verde bosque `"¡Solicitud Registrada con Éxito!"`, párrafo explicativo con el folio institucional en negrita `"#DEM-{id}"`, recuadro de detalles con fondo gris muy suave conteniendo el estado en color azul institucional, correo del solicitante y marca de tiempo UTC, y botón `"Entendido"` en color azul institucional.
9. **Accesibilidad WCAG 2.1 AA:** Diálogo modal con atributos `role="dialog"`, `aria-modal="true"` y `aria-labelledby="demand-modal-title"`. Cierre automático mediante la tecla `Escape` y navegación completa por teclado con tabulación accesible.

##### Criterios de Aceptación Formativos (Given-When-Then)

```gherkin
Escenario 1: Registro exitoso de solicitud de demanda académica desde cartelera vacía
  DADO QUE el estudiante mentoreado se encuentra autenticado en el sistema
  Y visualiza la cartelera de recomendaciones vacía o sin ofertas sobre su tema de interés en RecommendationFeedView
  CUANDO hace clic en el botón "Registrar Solicitud por Demanda"
  Y selecciona una asignatura crítica (ej. "Algoritmos y Estructuras de Datos") y un tema silábico específico
  Y redacta su justificación pedagógica presionando el botón "Enviar Solicitud"
  ENTONCES el sistema valida los datos y ejecuta POST /api/v1/bookings/requests
  Y persiste el registro en la tabla física solicitudes_demanda en estado "PENDIENTE" asignando un folio correlativo #DEM-{id}
  Y despliega en pantalla el panel de confirmación en color verde con los detalles de la solicitud registrada.
  Evidencia de Prueba: test_bookings.py::test_create_demand_request_success / MentoringDemandModalView.test.tsx

Escenario 2: Preselección automática ante redirección por aforo colapsado en reserva
  DADO QUE el mentoreado intenta reservar una sesión de mentoría en BookingModalView cuyo aforo se encuentra agotado (0 vacantes)
  CUANDO presiona el botón alternativo "Registrar Solicitud por Demanda"
  ENTONCES el sistema abre MentoringDemandModalView con la asignatura y el tema de la sesión agotada preseleccionados automáticamente
  Y enfoca directamente el cuadro de texto de justificación pedagógica
  Y permite al estudiante enviar la solicitud sin requerir rebuscar la materia en el catálogo.
  Evidencia de Prueba: BookingModalView.test.tsx / MentoringDemandModalView.test.tsx

Escenario 3: Bloqueo de envío ante campos obligatorios sin seleccionar
  DADO QUE el estudiante tiene abierto el modal de solicitud de demanda académica
  CUANDO no selecciona ninguna asignatura curricular o tema silábico válido
  Y presiona el botón "Enviar Solicitud"
  ENTONCES el componente bloquea la emisión de la petición HTTP
  Y despliega un banner de alerta en color rojo con el texto: "Por favor seleccione una asignatura y un tema curricular válido."
  Y mantiene los controles en pantalla sin registrar datos en la base de datos.
  Evidencia de Prueba: MentoringDemandModalView.test.tsx::test_validation_empty_fields

Escenario 4: Disponibilidad y visualización inmediata en el banco de solicitudes del portal del mentor
  DADO QUE una solicitud de demanda académica ha sido registrada exitosamente por un mentoreado
  CUANDO un estudiante mentor acreditado de ciclos superiores accede a su panel en MentorSessionsView
  Y hace clic en la pestaña "Banco de Solicitudes por Demanda (RF07)"
  ENTONCES el sistema consulta el endpoint GET /api/v1/bookings/requests
  Y despliega la tarjeta de la solicitud con el folio #DEM-{id}, código de curso, tema silábico y justificación
  Y presenta al mentor el botón para formular una nueva oferta de mentoría dirigida a cubrir dicha demanda.
  Evidencia de Prueba: test_bookings.py::test_list_demand_requests / MentorSessionsView.test.tsx
```
"""
