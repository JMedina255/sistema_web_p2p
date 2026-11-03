# Guion Técnico y Manual de Exposición Oral — Sustentación del Sprint 04

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre Académico 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam  
* Joan Cristian Medina Quispe (Código: 2022074255) — Frontend, UI Architecture & Ergonomía  
* Renzo Antonio Antayhua Mamani (Código: 2022073504) — Backend, Database & Concurrencia Transaccional  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Documento Técnico:** `docs/presentaciones/sprint-04/GUION_EXPOSICION_SPRINT_04.md`  
**Tiempo Total Estimado:** 16 minutos de exposición continua + Sesión de Consultas (Q&A)  
**Línea Base en Git:** Commits `8bd6583` y `7813a6f` en rama `main`  
**Estado:** ✅ Aprobado y Ensamblado para Exposición en Vivo  

---

## 1. Protocolo de Exposición y Distribución de Tiempos

El presente guion establece el diálogo formal coordinado entre los integrantes del equipo consultor, articulando una transición fluida entre la fundamentación metodológica, las decisiones de arquitectura, la demostración de código fuente y las métricas de calidad automatizadas:

| N° | Título de la Diapositiva | Expositor Responsable | Tiempo Asignado | Minuto Acumulado |
| :---: | :--- | :---: | :---: | :---: |
| **01** | Portada Institucional y Auditoría de Línea Base | Joan & Renzo | 1m 15s | 01m 15s |
| **02** | Objetivo y Alcance del Sprint 04 (Plan vs Real) | Renzo | 1m 30s | 02m 45s |
| **03** | Planificación y Distribución Operativa (T-17 a T-24) | Joan | 1m 15s | 04m 00s |
| **04** | Algoritmo de Recomendación Top-k (EdRecSys v1.0) | Renzo | 1m 45s | 05m 45s |
| **05** | Ponderación Curricular EPIS y Desempate Determinista | Renzo | 1m 30s | 07m 15s |
| **06** | Pruebas del Recomendador y Banco Determinista | Joan | 1m 30s | 08m 45s |
| **07** | Arquitectura del Sistema de Reservas Transaccionales | Joan | 1m 30s | 10m 15s |
| **08** | Control de Aforo y Bloqueo Pesimista (SELECT FOR UPDATE) | Renzo | 2m 00s | 12m 15s |
| **09** | Modelo Relacional `reservas_cupo` y Máquina de Estados | Renzo | 1m 30s | 13m 45s |
| **10** | Contratos API REST, Reglas de Negocio y Quórum T-24h | Renzo | 1m 30s | 15m 15s |
| **11** | Aseguramiento de Calidad: 245 Tests y Cierre DoD | Joan | 1m 30s | 16m 45s |
| **12** | Conclusiones, Logros Verificados y Cierre hacia S05 | Renzo & Joan | 1m 15s | 18m 00s |

---

## 2. Desarrollo Detallado del Guion Oral (Diapositiva por Diapositiva)

---

### Diapositiva 01: Portada Institucional y Auditoría de Línea Base (00:00 - 01:15)

* **Recurso Visual:** Diapositiva 01 en Canva (Identidad visual `#1C2A59`, `#B99451`, logos UPT/EPIS).
* **Entregables de Respaldo:** `README.md`, `INFORME_GENERAL_SPRINT_04.md`.

> **Joan Cristian Medina Quispe:**  
> «Buenas tardes Dr. Ricardo Valcárcel Alvarado y miembros del jurado evaluador de la cátedra de Construcción de Software I. A nombre del Grupo 03, C-SharkTeam, conformado por Renzo Antayhua Mamani y quien les habla, Joan Medina Quispe, tenemos el agrado de sustentar formalmente el incremento de ingeniería correspondiente al **Sprint 04** de nuestro proyecto: el *Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna*.»

> **Renzo Antonio Antayhua Mamani:**  
> «Esta sustentación representa la culminación del núcleo operativo de la plataforma. En el Sprint 03 dejamos operativo el catálogo docente y adelantamos el cálculo algorítmico base. Hoy, en el Sprint 04, integramos la experiencia completa del estudiante mentoreado: el consumo del feed inteligente Top-k con explicabilidad algorítmica y la formalización transaccional de reservas de cupos blindadas bajo concurrencia pesimista ACID. Toda nuestra sustentación se encuentra estrictamente respaldada por evidencias auténticas, congeladas en los commits `8bd6583` y `7813a6f` de la rama `main`, con un balance de 245 pruebas automatizadas pasando con éxito al 100%. Iniciamos con la visión operativa del incremento.»

---

### Diapositiva 02: Objetivo y Alcance del Sprint 04 (01:15 - 02:45)

* **Recurso Visual:** Diapositiva 02 en Canva | `diagramas/arquitectura_sprint04.png`.
* **Entregables de Respaldo:** `docs/sprints/sprint-04.md#L29-L55`, `PLAN_SPRINTS_Y_TAREAS.md`.

> **Renzo Antonio Antayhua Mamani:**  
> «El objetivo central del Sprint 04 consistió en resolver la interacción activa entre mentoreados y sesiones de tutoría. En la planificación institucional asumimos cuatro ítems del Product Backlog: PB-010, que es la recomendación Top-k personalizada; PB-011, correspondiente al feed interactivo en frontend; PB-013, que es la reserva transaccional con control estricto de aforo; y PB-014, el protocolo de corte y evaluación de quórum a $T-24\text{ h}$.
>
> Para alcanzar este objetivo, respetamos rigurosamente el presupuesto de 15.0 horas académicas de ingeniería aprobadas en el plan de trabajo. Como pueden apreciar en el Diagrama 3.1 de arquitectura física y despliegue que proyectamos en pantalla, la solución adopta un patrón arquitectónico desacoplado y multi-capa: en el cliente, una Single Page Application en React 19 y TypeScript 5.6 empaquetada con Vite; en el servidor de aplicación, una API REST construida sobre FastAPI y SQLAlchemy 2.0 que ejecuta la coordinación transaccional; y en la capa de datos, PostgreSQL 16 alojado en la infraestructura de Supabase, gobernado por políticas RLS y la migración Alembic 004.
>
> El sistema conecta requerimientos críticos: desde la latencia sub-milisegundo estipulada en RNF03, hasta la prevención absoluta de sobrecupo exigida por RNF07 y el estándar normativo de aforos inmutables de la regla RN-05. Doy el pase a Joan para explicar cómo distribuimos operativamente las tareas.»

---

### Diapositiva 03: Planificación y Distribución Operativa de Tareas (02:45 - 04:00)

* **Recurso Visual:** Diapositiva 03 en Canva (Matriz de tareas T-17 a T-24).
* **Entregables de Respaldo:** `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (Tabla 5.5).

> **Joan Cristian Medina Quispe:**  
> «Gracias, Renzo. Como exige la directriz de gestión Scrum del curso, el sprint se estructuró en una matriz de 8 tareas operativas, distribuyendo equitativamente 7.5 horas de desarrollo para cada uno de nosotros.
>
> En la capa de cliente y experiencia de usuario asumí cuatro tareas medulares: la tarea **T-18**, donde estructuré el cliente tipado `recommendationService.ts` para consumir los endpoints de recomendación mediante adaptadores seguros con tokens Bearer JWT; la tarea **T-20**, donde construí el componente `RecommendationFeedView.tsx` con soporte para tarjetas explicables XAI y un panel pedagógico *empty-state* para solicitudes por demanda según el caso CUS03; la tarea **T-21**, correspondiente al modal interactivo de reserva `BookingModalView.tsx` con validaciones síncronas de antelación y aforo; y la tarea **T-23**, donde vinculé el servicio de reservas con la navegación principal de `App.tsx`.
>
> Por su parte, Renzo concentró su esfuerzo en el motor algorítmico y la persistencia transaccional: **T-17** para el refinamiento del recomendador Top-k y ponderadores curriculares en `RecommendationService`; **T-22** para el modelado de la entidad `ReservaCupo`, la migración física Alembic 004 y los controladores REST; y **T-24** para la implementación del candado pesimista `SELECT ... FOR UPDATE` y la suite de concurrencia multihilo bajo RNF07.
>
> Destaco especialmente la tarea **T-19**, en la cual ambos trabajamos conjuntamente durante 1 hora para sincronizar el banco de pruebas de ordenamiento determinista, garantizando que cada aserción algorítmica del backend tuviera un reflejo idéntico en la representación visual del DOM. Pasamos ahora al desarrollo de la inteligencia algorítmica.»

---

### Diapositiva 04: Algoritmo de Recomendación Top-k Multifactorial (04:00 - 05:45)

* **Recurso Visual:** Diapositiva 04 en Canva | `diagramas/flujo_recomendacion.png` | `evidencias/frontend/01_recommendation_feed_topk.png`.
* **Entregables de Respaldo:** `app/services/recommendation_service.py#L130-L240`, `docs/sprints/sprint-04.md#L62-L91`.

> **Renzo Antonio Antayhua Mamani:**  
> «El motor algorítmico que sustenta el sistema es *EdRecSys v1.0*. En este Sprint 04 completamos su formulación matemática y su integración en el feed. Como establece el requerimiento RF06 y el caso de uso canónico CUS02, el objetivo es ordenar las sesiones de mentoría disponibles de mayor a menor afinidad con las necesidades formativas del estudiante mentoreado.
>
> Como observan en la fórmula proyectada, la afinidad total $S_{\text{total}}$ no es una asignación arbitraria. Se compone de una combinación lineal ponderada de cuatro dimensiones normalizadas entre 0 y 1, multiplicada por el ponderador curricular $W_{\text{curso}}$:
>
> $$S_{\text{total}} = (0.40 S_{\text{tema}} + 0.35 S_{\text{horario}} + 0.15 S_{\text{modalidad}} + 0.10 S_{\text{curricular}}) \times W_{\text{curso}}$$
>
> El primer factor, con un **40% de peso**, evalúa la similitud temática silábica mediante los coeficientes de Jaccard y Dice sobre los temas conceptuales oficiales de la asignatura. El segundo factor, con un **35% de peso**, calcula la compatibilidad horaria contrastando el horario de la sesión con la matriz semanal 6×11 de disponibilidad del mentoreado. El tercer factor, con **15% de peso**, evalúa la modalidad: otorga 1.0 si ambas coinciden en presencial o virtual, 0.9 si es híbrida, y castiga con 0.2 si son incompatibles. El cuarto factor, con **10%**, pondera la afinidad curricular general.
>
> Un aporte sustantivo que incorporó Joan en la interfaz es que no presentamos este puntaje como un número opaco. La tarjeta React integra principios de *Explainable AI* (XAI): el estudiante puede desplegar el desglose porcentual de cada uno de los cuatro factores, entendiendo con exactitud por qué esa sesión en particular le es recomendada. Continuemos con la ponderación curricular y el determinismo.»

---

### Diapositiva 05: Ponderación Curricular EPIS y Desempate Determinista (05:45 - 07:15)

* **Recurso Visual:** Diapositiva 05 en Canva | `evidencias/backend/01_recommendations_endpoint_response.png`.
* **Entregables de Respaldo:** `app/services/recommendation_service.py#L400-L460`, `reglas_documentacion_diseño.md`.

> **Renzo Antonio Antayhua Mamani:**  
> «En estricta concordancia con el propósito formativo del proyecto y la regla de negocio institucional **RN-11**, el recomendador no trata a todas las asignaturas por igual. Para atacar los focos críticos de reprobación y deserción en los primeros ciclos de la EPIS, introdujimos multiplicadores institucionales parametrizables:
>
> Asignamos un factor de **1.30x** a *Algoritmos y Estructuras de Datos*, por ser la asignatura filtro de mayor tasa de desaprobación histórica en la carrera; un factor de **1.20x** a *Cálculo I*, *Cálculo II* y *Programación Orientada a Objetos*; un factor de **1.10x** a *Base de Datos*; y **1.00x** a las demás materias de malla regular. Como pueden apreciar en la evidencia EV-S04-01 proyectada a la derecha, en la respuesta JSON real del endpoint `/api/v1/recommendations/offers`, una sesión de Algoritmos alcanza un score ponderado de `0.9840`, posicionándose en el primer lugar del ranking.
>
> Asimismo, resolvimos de forma rigurosa el problema del indeterminismo en los algoritmos de recomendación. Si dos ofertas alcanzan exactamente el mismo puntaje al cuarto decimal, el sistema jamás recurre a ordenamientos aleatorios. Implementamos una **clave quíntuple de desempate determinista**:
>
> $$\text{Key} = \left( -S_{\text{total}}, -W_{\text{curso}}, -\text{aforo\_disponible}, \text{fecha\_inicio}, \text{codigo\_sesion} \right)$$
>
> Ante empate de score, desempata la asignatura crítica; si persiste, la sesión con mayor cantidad de vacantes libres para balancear la carga de los laboratorios; luego la sesión con fecha de inicio más temprana; y en última instancia, el orden alfanumérico del código canónico. El resultado es 100% determinista y reproducible. Joan nos explicará cómo validamos este comportamiento.»

---

### Diapositiva 06: Pruebas del Recomendador y Banco Determinista (07:15 - 08:45)

* **Recurso Visual:** Diapositiva 06 en Canva | `evidencias/pruebas/01_topk_deterministic_ordering_tests.png` | `evidencias/frontend/03_topk_ordering_vitest.png`.
* **Entregables de Respaldo:** `aplicacion/backend/tests/test_recommendations.py#L400-L479`, `TopKOrdering.test.tsx`.

> **Joan Cristian Medina Quispe:**  
> «Para certificar la estabilidad de este motor diseñamos un banco de pruebas específico compuesto por los casos de prueba **ORD-01 al ORD-05**, evaluados tanto en Pytest en backend como en Vitest en frontend.
>
> En la terminal superior pueden observar los resultados en backend: la prueba **ORD-01** forzó empates artificiales al cuarto decimal ($S_{\text{total}} = 0.8500$), verificando que en diez ejecuciones consecutivas el orden devuelto fuera exactamente el mismo; las variantes **ORD-01b** y **ORD-01c** acreditaron el desempate por fecha y código; y **ORD-01d** evaluó la invarianza barajando aleatoriamente la lista de candidatos de entrada antes del cómputo, obteniendo una concordancia del 100% en el ranking final.
>
> Las pruebas **ORD-02** y **ORD-03** validaron dos reglas de negocio ineludibles: la regla **RN-04**, que exige una antelación mayor a 24 horas para reservar —toda sesión a menos de 24 horas queda excluida del feed con cero fugas—; y la regla **RN-05**, que excluye automáticamente cualquier sesión que haya agotado sus 10 cupos en presencial o 20 en virtual. Finalmente, **ORD-05** acreditó que el bonificador 1.30x de Algoritmos efectivamente desplaza a Cálculo y POO en el ranking.
>
> En la terminal inferior observan la contraparte en frontend: 9 pruebas en `TopKOrdering.test.tsx` ejecutadas en 785 milisegundos con React Testing Library, validando que el DOM renderice las tarjetas en el orden matemático exacto y active el panel empty-state cuando el catálogo está vacío. Pasamos ahora a la arquitectura de reservas.»

---

### Diapositiva 07: Arquitectura del Sistema de Reservas Transaccionales (08:45 - 10:15)

* **Recurso Visual:** Diapositiva 07 en Canva | `evidencias/frontend/02_booking_modal_and_rules.png` | `diagramas/flujo_reserva.png`.
* **Entregables de Respaldo:** `BookingModalView.tsx`, `booking_service.py`, `diagramas_general.md#L1555`.

> **Joan Cristian Medina Quispe:**  
> «Una vez que el estudiante identifica la sesión idónea en el Feed Top-k, inicia el flujo de agendamiento. Al presionar *"Reservar Vacante"*, la interfaz despliega el componente modal interactivo `BookingModalView.tsx` que pueden observar en pantalla.
>
> Este modal no es un simple formulario: actúa como un primer anillo de validación ergonómica y legal. Primero, verifica que el estudiante esté autenticado con su correo institucional `@upt.pe`. Segundo, comprueba que cuente con su consentimiento de tratamiento de datos personales firmado bajo la Ley N° 29733 y la regla **RN-02**. Tercero, aplica una validación de integridad: si el correo del estudiante coincide con el del mentor que dicta la clase, el sistema inhabilita la acción e informa formativamente que un mentor no puede reservar en su propia sesión.
>
> Un aspecto fundamental exigido por el marco institucional es la **advertencia normativa de corte a $T-24\text{ h}$ (RN-08)**: el modal informa claramente al estudiante que la reserva se registrará en estado transitorio `PENDIENTE_CONFIRMACION`, y que tendrá un plazo límite que vence exactamente 24 horas antes del inicio de la clase para ratificar voluntariamente su asistencia. Si el alumno no ratifica en ese plazo, la vacante se libera automáticamente.
>
> Cuando el usuario confirma, el botón entra en estado de carga bloqueante para evitar dobles clics y envía una petición `POST /api/v1/bookings/reserve`. Si ocurre una colisión concurrente y el cupo se agota, el modal captura limpiamente el código `HTTP 409 Conflict`, cierra el diálogo y muta la tarjeta a *"Aforo Agotado"*, sugiriendo registrar una solicitud temática por demanda. Renzo detallará ahora cómo resolvemos esta contención en el servidor.»

---

### Diapositiva 08: Control de Aforo y Bloqueo Pesimista (SELECT FOR UPDATE) (10:15 - 12:15)

* **Recurso Visual:** Diapositiva 08 en Canva | `diagramas/concurrencia_aforo.png` | `evidencias/pruebas/03_concurrency_pessimistic_lock_rnf07.png`.
* **Entregables de Respaldo:** `app/services/booking_service.py#L90-L160`, `tests/test_bookings.py#L280-L360`.

> **Renzo Antonio Antayhua Mamani:**  
> «Llegamos al desafío técnico más riguroso de este sprint: el cumplimiento ineludible del requerimiento **RNF07**, que exige una tasa de sobrecupo de exactamente 0.00% bajo ráfagas de alta concurrencia.
>
> Imaginemos el escenario crítico: una sesión de mentoría presencial tiene un aforo inmutable de 10 estudiantes según la regla **RN-05**. Nueve vacantes ya han sido ocupadas y queda exactamente 1 cupo disponible. En ese mismo instante, dos o más estudiantes pulsan el botón de reserva simultáneamente. En un diseño ingenuo sin aislamiento, ambas peticiones consultarían la base de datos, ambas leerían que quedan cupos libres, y ambas insertarían su registro, generando un sobrecupo ilegal de 11 alumnos en un laboratorio de 10 máquinas.
>
> Para neutralizar de raíz esta condición de carrera, diseñamos el coordinador transaccional en `BookingService` mediante un **bloqueo pesimista de fila en PostgreSQL**:
>
> ```sql
> SELECT * FROM sesiones_mentoria WHERE id_sesion = :id FOR UPDATE;
> ```
>
> Al abrir la transacción con `db.begin()`, SQLAlchemy adquiere un candado exclusivo a nivel de tupla física sobre la fila de la sesión en PostgreSQL. Como ilustra el diagrama secuencial en pantalla, cuando el Hilo 1 toma el candado, el Hilo 2 y las peticiones subsiguientes quedan automáticamente encoladas a nivel del motor de base de datos.
>
> El Hilo 1 realiza el conteo de reservas activas bajo el candado; encuentra que hay 9 ocupados, comprueba que 9 es menor que 10, inserta la reserva provisional, ejecuta el `COMMIT` y libera el candado, retornando un `HTTP 201 Created` con el comprobante emitido.
>
> Inmediatamente después, el Hilo 2 despierta y adquiere el candado; realiza el conteo atómico, pero ahora encuentra que hay 10 ocupados. Al detectar que el aforo está colmado, ejecuta un `ROLLBACK` instantáneo, libera el candado y retorna al cliente un `HTTP 409 Conflict` con el mensaje `CAPACITY_EXCEEDED`.
>
> No dejamos esta lógica en teoría: ejecutamos el testbench multihilo que pueden ver en la captura inferior. Sometimos una sesión al asedio simultáneo de **20 hilos concurrentes compitiendo por la última vacante**. El resultado fue categórico: exactamente 1 hilo obtuvo confirmación HTTP 201, y exactamente 19 hilos recibieron HTTP 409. El total final de plazas registradas fue de 10 de 10, certificando empíricamente una **tasa de sobrecupo de exactamente 0.00%**. Veamos ahora el modelo relacional.»

---

### Diapositiva 09: Modelo Relacional `reservas_cupo` y Máquina de Estados (12:15 - 13:45)

* **Recurso Visual:** Diapositiva 09 en Canva | `evidencias/base_datos/01_migration_004_reservas_cupo.png` | `evidencias/base_datos/02_pessimistic_lock_query_select_for_update.png`.
* **Entregables de Respaldo:** `migrations/versions/004_booking_and_reservations.py`, `app/models/booking.py`.

> **Renzo Antonio Antayhua Mamani:**  
> «La persistencia relacional de esta arquitectura se construyó mediante la migración oficial de Alembic `004_booking_and_reservations.py`. En la captura de código DDL a la izquierda pueden observar la especificación física de la tabla `reservas_cupo`.
>
> Destacamos tres decisiones de diseño vinculadas a las directrices D-4 y D-7: primero, las claves foráneas hacia `sesiones_mentoria` y `usuarios` con borrado en cascada e índices B-Tree compuestos para optimizar las consultas de conteo; segundo, la restricción de integridad única `uq_sesion_estudiante_activa`, que a nivel de tabla impide que un alumno registre dos reservas activas sobre una misma clase; y tercero, la restricción `CHECK` que gobierna la **máquina de estados finitos** de la reserva.
>
> El cupo formalizado transita por un ciclo determinista: nace en estado `PENDIENTE_CONFIRMACION`. Si el estudiante ratifica su asistencia dentro del plazo normativo, transita a `CONFIRMADA`. Si el alumno desiste voluntariamente antes del corte, transita a `CANCELADA_USUARIO` y la vacante se libera de inmediato. Si llega la marca de 24 horas previas sin ratificación, el sistema conmuta el estado a `NO_CONFIRMADA`. Y si la sesión en su totalidad se suspende por falta de quórum, transita a `CANCELADA_SISTEMA`.
>
> En la evidencia de la derecha proyectamos la traza real de PostgreSQL, donde se constata la sentencia `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED`, la adquisición del `ExclusiveLock` en la tupla `(0, 1)`, la inserción y el `COMMIT`. Continuamos con los contratos API y el protocolo de quórum.»

---

### Diapositiva 10: Contratos API REST, Reglas de Negocio y Quórum T-24h (13:45 - 15:15)

* **Recurso Visual:** Diapositiva 10 en Canva | `evidencias/backend/02_swagger_api_docs_sprint04.png` | `evidencias/backend/03_quorum_evaluation_cutoff_t24h.png`.
* **Entregables de Respaldo:** `app/api/v1/endpoints/bookings.py`, `app/api/v1/endpoints/quorum.py`.

> **Renzo Antonio Antayhua Mamani:**  
> «Todos estos componentes se exponen a través de controladores REST tipados bajo Pydantic v2 y autenticación JWT, documentados interactivamente en la interfaz Swagger que visualizan en la captura superior. Implementamos endpoints especializados: `POST /api/v1/bookings/reserve` para formalizar reservas, `GET /my-reservations` para consultar el historial del estudiante, `GET /session/{id}` para que el mentor visualice la lista oficial de inscritos, y `POST /bookings/requests` para registrar necesidades temáticas cuando no hay ofertas coincidentes.
>
> Mención especial merece el protocolo de **evaluación automática de quórum a $T-24\text{ h}$ (RN-09 / CUS23)**, cuyos resultados reales observamos en la captura inferior. Conforme al reglamento de mentorías de la EPIS, una sesión no puede dictarse si no cuenta con el respaldo de un quórum mínimo del 50% de su capacidad reglamentaria.
>
> Exactamente a las 24 horas del inicio de la clase, el servicio `BookingService.evaluate_quorum` ejecuta dos acciones atómicas: primero, barre todas las reservas de la sesión que continúan en `PENDIENTE_CONFIRMACION` y las transiciona a `NO_CONFIRMADA` liberando sus plazas; segundo, computa el ratio de alumnos confirmados sobre el aforo máximo.
>
> Si la sesión tiene 6 confirmados sobre 10 cupos, el ratio es 0.60; al superar el umbral de 0.50, la clase transiciona a `CONFIRMADA` y se ratifica el aula física o el enlace Google Meet. Por el contrario, si solo cuenta con 3 confirmados sobre 10, el ratio es 0.30; el sistema emite el dictamen de cancelación `CANCELADA_FALTA_QUORUM`, evitando que el docente o los mentores se trasladen inútilmente a las aulas universitarias. Doy el pase a Joan para presentar el balance de calidad.»

---

### Diapositiva 11: Aseguramiento de Calidad: 245 Tests y Cierre DoD (15:15 - 16:45)

* **Recurso Visual:** Diapositiva 11 en Canva | `evidencias/calidad/01_backend_pytest_coverage_sprint04.png` | `evidencias/calidad/02_frontend_vitest_coverage_sprint04.png` | `evidencias/calidad/03_linting_and_formatting_check.png`.
* **Entregables de Respaldo:** `docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_04.md`, `pyproject.toml`.

> **Joan Cristian Medina Quispe:**  
> «Para el equipo consultor, la calidad no es una verificación tardía al final del ciclo, sino un principio de ingeniería continuo. En el Sprint 04 consolidamos una batería de **245 pruebas automatizadas pasando con el 100% de éxito en 27 suites independientes**.
>
> Como exige la directriz técnica de la cátedra, el requerimiento **RNF09** fija un umbral mínimo obligatorio del **70.0% de cobertura de código por pruebas automatizadas**, evaluado de forma estrictamente separada en ambas capas. Como certifican los reportes de terminal oficiales emitidos por Pytest-Cov y Vitest:
>
> En el backend alcanzamos **91.22% de cobertura de código** sobre 2,141 sentencias evaluadas a lo largo de 158 pruebas en 14 suites, superando el umbral por más de 21 puntos porcentuales. En el frontend alcanzamos **92.56% de cobertura de código** sobre 87 pruebas automatizadas en 13 suites, superando la meta por más de 22 puntos porcentuales.
>
> Asimismo, auditamos el análisis estático de código: Ruff 0.17.1 certificó cero defectos y formato PEP 8 limpio en los 69 archivos de Python; ESLint 9 certificó cero errores y cero advertencias en los 42 módulos TypeScript de la aplicación. Por último, la compilación de producción con Vite y el compilador de TypeScript generó limpiamente los artefactos estáticos en `dist/` en solo 100 milisegundos.
>
> Cumplimos al 100% con la Definición de Terminado (DoD) y con las 10 Reglas de Diseño Institucionales D-1 a D-10. Pasamos a las conclusiones y próximos pasos.»

---

### Diapositiva 12: Conclusiones, Logros Verificados y Cierre hacia S05 (16:45 - 18:00)

* **Recurso Visual:** Diapositiva 12 en Canva (Roadmap institucional y cierre).
* **Entregables de Respaldo:** `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (Sprints 5 a 8).

> **Renzo Antonio Antayhua Mamani:**  
> «En conclusión, el Sprint 04 consolida el núcleo de valor del Sistema Web P2P de la EPIS-UPT. Hemos demostrado con rigor que es posible articular algoritmos de recomendación explicables con garantías transaccionales estrictas de nivel industrial, protegiendo los aforos universitarios mediante bloqueo pesimista y optimizando la dedicación docente con la evaluación automatizada de quórum a $T-24\text{ h}$.»

> **Joan Cristian Medina Quispe:**  
> «De conformidad con la planificación institucional de Scrum, la línea base del Sprint 04 queda formalmente cerrada y homologada. Transparentamos que las funcionalidades de gestión de reservas por parte del alumno —como la pantalla de visualización 'Mis Reservas', la ratificación en interfaz y el desistimiento voluntario— constituyen el alcance del **Sprint 05**, sobre el cual ya nos encontramos trabajando activamente.
>
> Con 245 pruebas, más del 91% de cobertura y cero defectos estáticos, entregamos un producto robusto, auditable y al servicio de la comunidad académica de Ingeniería de Sistemas. Agradecemos su atención, Dr. Ricardo Valcárcel, y quedamos a su entera disposición para absolver las consultas y observaciones de la cátedra. Muchas gracias.»

---

## 3. Banco de Preguntas Frecuentes y Defensa Técnica (FAQ de Jurado)

A continuación, se documentan las respuestas fundamentadas ante seis preguntas técnicas complejas que el jurado docente suele formular durante la sustentación:

---

### Pregunta 1: ¿Por qué eligieron un bloqueo pesimista `SELECT ... FOR UPDATE` en lugar de un enfoque optimista con campos de versión (`version_id`) en la entidad `sesiones_mentoria`?
* **Respuesta Técnica (Renzo):**  
  «El bloqueo optimista es eficiente en sistemas de baja contención donde la probabilidad de colisión es despreciable. Sin embargo, en el escenario de reservas universitarias de cupos limitados (exactamente 10 o 20 plazas), cuando se libera la última vacante o se abre una clase de alta demanda, la contención en el último milisegundo es extremadamente alta.  
  Con un enfoque optimista, si 20 alumnos intentan reservar simultáneamente, uno consolida y los otros 19 sufren una excepción de concurrencia optimista (`StaleDataError`), obligando a reintentar la transacción en un bucle que sobrecarga el pool de conexiones y satura el CPU. Con el bloqueo pesimista `SELECT ... FOR UPDATE`, PostgreSQL serializa limpiamente las peticiones en cola; el primer hilo adquiere la fila, inserta y comitea en ~2 milisegundos, y el segundo hilo al despertar detecta que el aforo está lleno y aborta deterministamente con HTTP 409 sin necesidad de reintentos infinitos ni degradación del servicio.»

---

### Pregunta 2: ¿Cómo garantiza el algoritmo EdRecSys v1.0 que no se produzca inanición (starvation) hacia mentores nuevos o recién habilitados?
* **Respuesta Técnica (Renzo / Joan):**  
  «El diseño de EdRecSys v1.0 mitiga el problema del arranque en frío (*cold start*) y la inanición mediante su arquitectura multifactorial: no depende exclusivamente de valoraciones históricas o popularidad acumulada.  
  El 40% del peso corresponde a la afinidad temático-silábica del contenido ofertado frente a las dificultades del alumno, y el 35% corresponde a la compatibilidad horaria en la grilla semanal 6×11. Si un mentor recién acreditado (con ciclo $\ge 7$) publica un taller sobre los temas exactos que el estudiante necesita y en su horario disponible, alcanzará un score muy elevado independientemente de si es su primera sesión dictada. Además, el caso de uso CUS03 permite a los mentores explorar el banco de solicitudes por demanda para formular ofertas a la medida de la necesidad estudiantil.»

---

### Pregunta 3: ¿Qué ocurre si el servicio de correo o notificación falla al momento de registrar la reserva provisional? ¿Afecta la transacción de base de datos?
* **Respuesta Técnica (Renzo):**  
  «No afecta en absoluto la transacción de base de datos. En cumplimiento del requerimiento no funcional **RNF06** y el principio de desacoplamiento de efectos colaterales (Cuadro 4.3 del informe general), el despacho de correos se ejecuta estrictamente fuera del bloque `db.begin()`, utilizando un despachador asíncrono en segundo plano (`BackgroundTasks` de FastAPI).  
  Si el servidor SMTP o el proveedor de correo experimenta latencia o falla, la transacción de inserción en la tabla `reservas_cupo` ya fue confirmada atómicamente con `COMMIT` y el comprobante `RES-XXXX` ya fue emitido al cliente. El fallo de notificación se registra en el log de auditoría sin comprometer la persistencia del cupo del estudiante.»

---

### Pregunta 4: ¿Por qué la evaluación de quórum se fijó estrictamente en $T-24\text{ h}$ y cómo se articula con las reglas RN-08 y RN-09?
* **Respuesta Técnica (Renzo):**  
  «La ventana de 24 horas previas responde a una necesidad operativa y logística de la Escuela Profesional de Ingeniería de Sistemas. Conforme al reglamento (RN-08), el estudiante debe ratificar su asistencia antes de $T-24\text{ h}$ para garantizar que asistirá.  
  Fijar el corte a las 24 horas exactas otorga a la administración de la EPIS un margen operativo suficiente: si la sesión no alcanza el 50% de quórum reglamentario (RN-09), se cancela formalmente con un día de anticipación, permitiendo liberar los laboratorios físicos de cómputo para otras actividades académicas y evitando que el docente tutor o los mentores acudan en vano al campus universitario. A su vez, los estudiantes inscritos son notificados a tiempo para reprogramar su jornada académica o canalizar su consulta a través de solicitudes por demanda.»

---

### Pregunta 5: ¿Cómo se valida la regla de mérito académico RN-03 en el recomendador y qué tasa de fuga presenta?
* **Respuesta Técnica (Renzo):**  
  «La regla **RN-03** exige que solo pueden ejercer como mentores pares los estudiantes de rendimiento sobresaliente que cursen entre el VII y el X ciclo lectivo. En el motor algorítmico, el filtro de mérito actúa como un pre-filtro excluyente inmutable: antes de calcular las similitudes de Jaccard u horario, la función verifica `ciclo_actual >= 7`.  
  Si un usuario postulante de ciclo I al VI figura en la base de datos, el evaluador asigna automáticamente un score de afinidad de `0.0000` y descarta la oferta del ranking. En el testbench algorítmico automatizado, ejecutamos evaluaciones sobre cohortes sintéticas con estudiantes de ciclos formativos iniciales; la tasa de fuga verificada fue de exactamente **0.00%**, garantizando que ningún estudiante no habilitado pueda liderar sesiones de tutoría.»

---

### Pregunta 6: ¿Por qué reportan métricas de cobertura independientes para frontend y backend en lugar de un promedio combinado?
* **Respuesta Técnica (Joan):**  
  «Reportar un promedio combinado encubriría desbalances entre subsistemas: un 95% en backend podría ocultar un 50% deficiente en frontend manteniendo un promedio engañoso sobre el 70%.  
  En cumplimiento de la **Regla 3.2.7** de las directrices de calidad del curso y el estándar **RNF09**, las métricas de frontend (evaluadas con el motor V8 de Vitest) y backend (evaluadas con Pytest-Cov) se auditan de forma estrictamente autónoma. Demostramos que ambos subsistemas superan individualmente el umbral normativo del 70.0% con holgura: **91.22% en el backend** y **92.56% en el frontend**, garantizando una arquitectura probada de extremo a extremo.»

---

*Fin del Guion Técnico y Manual de Exposición Oral — Sustentación del Sprint 04.*
