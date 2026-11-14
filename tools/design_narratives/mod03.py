# -*- coding: utf-8 -*-
"""
Modulo 03: Perfil del Mentor y Plan de Aprendizaje (Fase de Diseño)
Contiene: CUS-005, CUS-021
"""

def get_mod03():
    return """### MOD-03: Perfil del Mentor y Plan de Aprendizaje

#### CUS-005 - Gestionar perfil formativo y disponibilidad horaria

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-005** (CUS-005) |
| **Nombre** | Gestionar perfil académico formativo y matriz de disponibilidad horaria semanal |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-004 (Configuración de perfil formativo y matriz horaria); RN-03 (Requisitos académicos de mentor: ciclo >= V y promedio), RN-04 (Antelación de planificación) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Coordinador de Carrera |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los mentores configurar su reseña académica, áreas de competencia disciplinar y su matriz semanal de disponibilidad horaria (lunes a sábado de 08:00 a 20:00) a través del componente cliente `ProfileAvailabilityView.tsx` y el servicio `profileService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/profiles.py` y `app/services/profile_service.py` procesan las peticiones `GET /api/v1/profiles/me` y `PUT /api/v1/profiles/me`, validando los datos con Pydantic (`ProfileUpdateRequest`), verificando que el usuario pertenezca al quinto ciclo académico o superior, y persistiendo de forma atómica en las entidades ORM `PerfilAcademico` y `DisponibilidadHoraria` (`app/models/profile.py`). Las franjas horarias registradas son utilizadas posteriormente por el motor de recomendaciones y el validador de ofertas para evitar traslapes. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-02: Gestión Curricular y Perfiles Académicos)<br>Plan Curricular de la Carrera Profesional de Ingeniería de Sistemas UPT |
| **Anexos** | `aplicacion/frontend/src/components/ProfileAvailabilityView.tsx`<br>`aplicacion/frontend/src/services/profileService.ts` (`ProfileService`, `ApiProfileAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/profiles.py` (`GET /api/v1/profiles/me`, `PUT /api/v1/profiles/me`, `POST /api/v1/profiles/availability`)<br>`aplicacion/backend/app/services/profile_service.py` (`ProfileService.get_profile`, `ProfileService.update_profile`, `ProfileService.save_availability`)<br>`aplicacion/backend/app/models/profile.py` (`PerfilAcademico`, `DisponibilidadHoraria`), `app/models/curriculum.py` (`Curso`) |
| **Precondiciones** | 1. Usuario con sesión institucional activa y rol `UserRole.mentor` verificado en el token JWT.<br>2. El estudiante mentor se encuentra matriculado en el semestre lectivo en curso y cumple el requisito de ciclo >= V.<br>3. Catálogo de cursos y asignaturas filtro activo en base de datos. |
| **PostCondiciones** | 1. Registros actualizados en las tablas físicas `perfiles_academicos` y `disponibilidad_horaria`.<br>2. Transacción confirmada en PostgreSQL y matriz horaria serializada para el motor de recomendación.<br>3. Despliegue de notificación de éxito en la interfaz y actualización del perfil en caché del frontend. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del perfil académico y visualización de la matriz horaria** | |
| **1.** El mentor hace clic en la pestaña `"Mi Perfil y Disponibilidad"` en `ProfileAvailabilityView.tsx`. | **2.** En `profileService.ts`, se despacha la petición `GET /api/v1/profiles/me` con la cabecera `Authorization: Bearer <token>`. En `profiles.py`, se extrae el correo del claim `sub` y `profile_service.py` ejecuta `SELECT p.*, d.* FROM perfiles_academicos p LEFT JOIN disponibilidad_horaria d ON p.id = d.perfil_id WHERE p.usuario_id = :uid`. Retorna HTTP 200 con el perfil, materias de dominio y bloques horarios semanales. `ProfileAvailabilityView.tsx` renderiza el formulario con biografía, materias acreditadas y una matriz interactiva semanal (lunes a sábado, bloques de una hora de 08:00 a 20:00). |
| **Fase 2: Edición de datos formativos y selección de bloques de disponibilidad** | |
| **3.** El mentor actualiza su biografía pedagógica, selecciona o deselecciona las asignaturas que domina, y hace clic sobre los bloques horarios en la cuadrícula semanal para alternar su estado entre disponible (resaltado en color verde) y no disponible (en color neutro). | **4.** En `ProfileAvailabilityView.tsx`, se actualiza el estado local `availabilitySlots`. El mentor presiona el botón `"Guardar Cambios y Disponibilidad"`. El componente valida que la biografía no exceda 500 caracteres y que se haya marcado al menos un bloque horario semanal. (Si no se selecciona ningún bloque de disponibilidad en toda la semana, salta a E001). (Si la biografía excede el límite de caracteres o contiene caracteres inválidos, salta a E002). |
| **Fase 3: Persistencia transaccional de disponibilidad y perfil** | |
| **5.** El mentor espera la confirmación visual mientras el botón muestra un indicador circular de guardado. | **6.** En `profileService.ts`, se despacha `PUT /api/v1/profiles/me` con el payload `ProfileUpdateRequest`. En `profiles.py`, `profile_service.py` inicia una transacción ACID con `db.begin()`. Actualiza `perfiles_academicos`, elimina los bloques horarios previos en `disponibilidad_horaria` para ese perfil e inserta los nuevos registros `(perfil_id, dia_semana, hora_inicio, hora_fin)`. Ejecuta `db.commit()` y retorna HTTP 200 con el perfil actualizado. `ProfileAvailabilityView.tsx` despliega una alerta flotante en color verde: *"Perfil y disponibilidad horaria actualizados exitosamente"*. (Si ocurre un conflicto de concurrencia o violación de clave única en base de datos, salta a E003). |

##### Flujos de Excepción

##### Flujo de excepción E001: Matriz de disponibilidad horaria semanal vacía
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el validador en `ProfileAvailabilityView.tsx` o `profile_service.py` comprueba que el conjunto de bloques horarios seleccionados está vacío (`len(slots) == 0`). Lanza `HTTPException(status_code=400, detail="EMPTY_SCHEDULE: Debe seleccionar al menos un bloque horario semanal de disponibilidad para ofrecer mentorías.")`.<br><br>En `ProfileAvailabilityView.tsx`, se resalta la cuadrícula horaria con un borde en color rojo y se despliega una advertencia en color ámbar solicitando marcar al menos una hora disponible. |
| **E001-1.2** Hace clic sobre al menos un bloque horario en la cuadrícula interactiva. | **E001-1.3** Conmuta el bloque a disponible (color verde), rehabilita el botón `"Guardar Cambios"` y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Biografía o formato de enlaces no válido
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, Pydantic detecta que el campo biografía excede 500 caracteres o contiene scripts no autorizados. Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: La reseña formativa no debe exceder 500 caracteres ni contener etiquetas HTML.")`.<br><br>En `ProfileAvailabilityView.tsx`, se resalta el cuadro de texto de biografía en color rojo indicando el error de validación. |
| **E002-1.2** Modifica el texto ajustándolo al límite permitido de caracteres. | **E002-1.3** Actualiza el contador de caracteres en la interfaz y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Conflicto de concurrencia al actualizar perfil
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 6 del Flujo Normal, una sesión concurrente modifica el mismo perfil provocando un conflicto de versión en base de datos. `profile_service.py` ejecuta `db.rollback()` y lanza `HTTPException(status_code=409, detail="CONCURRENCY_CONFLICT: El perfil fue actualizado desde otra sesión. Se recargarán los datos más recientes.")`.<br><br>En `ProfileAvailabilityView.tsx`, se captura el error 409 y se despliega un aviso en color ámbar. Presenta el botón `<button onClick={fetchProfile}>Recargar Perfil</button>`. |
| **E003-1.2** Hace clic en el botón "Recargar Perfil". | **E003-1.3** Invoca nuevamente `GET /api/v1/profiles/me`, actualiza el formulario con el estado más reciente y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-021 - Explorar catálogo curricular de asignaturas filtro

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-021** (CUS-021) |
| **Nombre** | Explorar catálogo curricular jerárquico de asignaturas y materias críticas |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-005 (Gestión del catálogo de asignaturas y temarios); RN-11 (Priorización y catálogo oficial de asignaturas filtro EPIS) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian |
| **Actores** | Estudiante Mentoreado, Estudiante Mentor, Coordinador Curricular |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los estudiantes mentoreados y mentores navegar interactivamente por la malla curricular oficial de la EPIS-UPT a través del componente cliente `CurriculumCatalogView.tsx` y el servicio `curriculumService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/curriculum.py` y `app/services/curriculum_service.py` proporcionan consultas estructuradas por carrera (`Carrera`), ciclo académico (I al X), curso (`Curso`) y temas de aprendizaje silábico (`TemaCurricular`), destacando visualmente las asignaturas identificadas institucionalmente como "materias filtro" (`es_filtro = true`, tales como Algoritmos, Estructuras de Datos, Base de Datos y Programación Orientada a Objetos). Desde cada tema curricular, el mentoreado puede consultar directamente las ofertas de mentoría activas o solicitar la apertura de una sesión por demanda. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-02: Gestión Curricular y Perfiles Académicos)<br>Malla Curricular Oficial de Ingeniería de Sistemas UPT |
| **Anexos** | `aplicacion/frontend/src/components/CurriculumCatalogView.tsx`<br>`aplicacion/frontend/src/services/curriculumService.ts` (`CurriculumService`, `ApiCurriculumAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/curriculum.py` (`GET /api/v1/curriculum/careers`, `GET /api/v1/curriculum/courses`, `GET /api/v1/curriculum/courses/{id}/topics`)<br>`aplicacion/backend/app/services/curriculum_service.py` (`CurriculumService.get_courses`, `CurriculumService.get_topics`)<br>`aplicacion/backend/app/models/curriculum.py` (`Carrera`, `Curso`, `TemaCurricular`) |
| **Precondiciones** | 1. Usuario con sesión institucional iniciada en la plataforma.<br>2. Malla curricular y temarios silábicos cargados y versionados en la base de datos PostgreSQL.<br>3. Identificación institucional de cursos filtro debidamente clasificada en la columna `es_filtro`. |
| **PostCondiciones** | 1. Despliegue interactivo del catálogo jerárquico de asignaturas y temas silábicos en la interfaz.<br>2. Consulta idempotente de sólo lectura ejecutada sin mutaciones en base de datos.<br>3. Posibilidad de derivación directa hacia la reserva de mentoría (CUS-004) o registro de demanda (CUS-003). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Navegación por ciclo académico y selección de asignatura** | |
| **1.** El usuario hace clic en el enlace `"Catálogo Curricular"` del menú de navegación principal en `CurriculumCatalogView.tsx`. | **2.** En `curriculumService.ts`, se despacha `GET /api/v1/curriculum/courses`. En `curriculum.py`, `curriculum_service.py` ejecuta `SELECT c.*, count(t.id) as total_temas FROM cursos c LEFT JOIN temas_curriculares t ON c.id = t.curso_id WHERE c.activo = true GROUP BY c.id ORDER BY c.ciclo, c.nombre`. Retorna HTTP 200 con la lista completa de cursos. `CurriculumCatalogView.tsx` renderiza las asignaturas agrupadas por ciclo académico (del ciclo I al X), destacando las asignaturas filtro con una insignia visual en color azul institucional con la leyenda *"Materia Filtro Prioritaria"*. (Si el repositorio curricular sufre indisponibilidad o timeout, salta a E001). |
| **Fase 2: Búsqueda y filtrado interactivo de cursos** | |
| **3.** El usuario introduce el nombre de una materia o código en el cuadro de búsqueda `"Buscar asignatura o tema"` y aplica el filtro por ciclo. | **4.** En `CurriculumCatalogView.tsx`, se filtra reactivamente la nómina de cursos en el estado de la vista. El usuario hace clic en la tarjeta de la asignatura de su interés para inspeccionar su estructura temática. (Si ningún curso coincide con los términos de búsqueda ingresados, salta a A001). |
| **Fase 3: Despliegue de temarios silábicos y vinculación con mentorías** | |
| **5.** El usuario hace clic sobre la tarjeta de un curso específico (e.g. Algoritmos y Estructuras de Datos). | **6.** En `curriculumService.ts`, se despacha `GET /api/v1/curriculum/courses/{course_id}/topics`. El backend retorna los temas clasificados por unidad didáctica con número de semana, descripción y cantidad de ofertas activas. `CurriculumCatalogView.tsx` expande un panel acordeón desplegando la lista de temas silábicos, cada uno con el botón `"Ver Ofertas Disponibles"` y el botón `"Solicitar Demanda"`. |

##### Flujos Alternativos

##### Flujo alternativo A001: Búsqueda curricular sin coincidencias
| Usuario | Sistema |
|---|---|
| **A001-1.1** El usuario introduce en el paso 3 un término de búsqueda que no produce coincidencias en el catálogo. | **A001-1.2** En `CurriculumCatalogView.tsx`, se ocultan las tarjetas y se renderiza un panel centrado con un ícono informativo y el texto: *"No se encontraron asignaturas o temas que coincidan con la búsqueda. Intente con otro término o seleccione un ciclo específico"*. Presenta el botón `<button onClick={handleResetFilter}>Restablecer Filtros</button>`. |
| **A001-1.3** Hace clic en el botón "Restablecer Filtros". | **A001-1.4** Limpia el cuadro de búsqueda, muestra nuevamente todas las asignaturas por ciclo y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Falla de conexión con el repositorio curricular
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, la consulta hacia las tablas `cursos` y `temas_curriculares` sufre una pérdida de conexión en PostgreSQL. Lanza `HTTPException(status_code=503, detail="CURRICULUM_SERVICE_UNAVAILABLE: El repositorio curricular no se encuentra disponible temporalmente. Reintente en unos instantes.")`.<br><br>En `CurriculumCatalogView.tsx`, se captura el error 503 y se despliega un panel de alerta en color ámbar indicando la imposibilidad de cargar la malla curricular. Presenta el botón `<button onClick={fetchCurriculum}>Reintentar Carga</button>`. |
| **E001-1.2** Hace clic en el botón "Reintentar Carga". | **E001-1.3** Dispara nuevamente la petición `GET /api/v1/curriculum/courses` y retorna al paso 1 del Flujo Normal de Eventos. |
"""
