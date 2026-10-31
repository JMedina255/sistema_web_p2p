# Guion Maestro y Contenido Oficial de Diapositivas — Sprint 03

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre Académico 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam  
* Joan Cristian Medina Quispe (Código: 2022074255) — Frontend, UI & Accesibilidad  
* Renzo Antonio Antayhua Mamani (Código: 2022073504) — Backend, Persistencia ORM & Algoritmos  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Documento Técnico:** `docs/sprints/sprint-03/04-presentacion/CONTENIDO_DIAPOSITIVAS_SPRINT_03.md`  
**Línea Base Evaluada:** Commit [`7df0a88345a06254940eab8f2d7d8b7f4d33d1e0`](https://github.com/JMedina255/sistema_web_p2p/tree/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0) (26/10/2026)  
**Estado:** Guion Aprobado y Congelado (Insumo Oficial para la Fase 2 de Generación Visual PPTX/PDF)  

---

## Índice de la Presentación Oficial (14 Diapositivas)

```
Estructura Pedagógica de la Presentación Oficial:

[I. Marco Institucional y Planificación]
  ├── Diapositiva 01: Portada Institucional y Datos de Auditoría
  └── Diapositiva 02: Objetivo del Sprint, Backlog y Comparación de Alcance (Plan vs Real)

[II. Ingeniería de Requisitos y Análisis de Ofertas]
  ├── Diapositiva 03: Requisito Funcional RF08: Publicación de Ofertas (SRS)
  ├── Diapositiva 04: Caso de Uso Canónico CUS06: Narrativa Formal y Excepciones
  └── Diapositiva 05: Modelado Visual de CUS06: Flujo de Actividades y Secuencia SAD

[III. Implementación y Reglas del Módulo de Ofertas]
  ├── Diapositiva 06: Capa de Presentación (T-14): Formulario Reactivo y Selección Curricular
  ├── Diapositiva 07: Reglas RN-04 y RN-05: Antelación (>24h) y Aforo Inmutable (10/20)
  └── Diapositiva 08: Backend de Ofertas (T-16): API REST, Modelo Relacional y Persistencia

[IV. Inteligencia de Recomendación (EdRecSys v1.0)]
  ├── Diapositiva 09: Requisito Funcional RF06: Especificación del Motor Top-k (SRS)
  ├── Diapositiva 10: Caso de Uso Canónico CUS02: Recomendaciones y Flujo de Demanda
  └── Diapositiva 11: Motor EdRecSys v1.0 (T-15): Formulación Matemática y Desempate

[V. Demostración, Verificación y Transición]
  ├── Diapositiva 12: Demostración Funcional: Recorrido en Vivo y Modos Real/Mock
  ├── Diapositiva 13: Homologación con Catálogo de Pruebas Institucional (Excel)
  └── Diapositiva 14: Aseguramiento de Calidad: 209 Tests, Cobertura >92% y Cierre DoD
```

---

## Desarrollo Detallado Diapositiva por Diapositiva

---

### Diapositiva 01: Portada Institucional y Datos de Auditoría

* **Título de la Diapositiva:** Sistema Web P2P de Mentorías Académicas — EPIS UPT
* **Subtítulo:** Sustentación de Ingeniería de Software — Incremento Técnico del Sprint 03
* **Objetivo Académico:** Contextualizar formalmente la entrega frente al jurado docente, acreditando la autoría técnica, la institución y la inmutabilidad de la línea base en Git.
* **Expositor Responsable:** Presentación Conjunta (Joan Medina y Renzo Antayhua).
* **Tiempo Estimado:** 1 minuto 30 segundos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Encabezado Institucional:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas.
* **Asignatura & Semestre:** Construcción de Software I — Semestre Académico 2026-II.
* **Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado.
* **Equipo Consultor (Grupo 03 / C-SharkTeam):**
  * Joan Cristian Medina Quispe (Código: 2022074255) — Frontend & UI Architecture.
  * Renzo Antonio Antayhua Mamani (Código: 2022073504) — Backend, Database & Algorithmic Design.
* **Datos de Auditoría Técnica:**
  * Rama de Trabajo: `main`
  * Commit Auditado: [`7df0a88345a06254940eab8f2d7d8b7f4d33d1e0`](https://github.com/JMedina255/sistema_web_p2p/commit/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0) (Commit corto: `7df0a88`).
  * Fecha de Corte Documental: 26 de octubre de 2026.
* **Badge de Calidad:** `209 / 209 Tests Passed (100%) | Coverage >92% | ESLint & Ruff: 0 Defectos`.

#### Guion del Expositor (Notas del Orador)
> **Joan:** «Buenas tardes Dr. Ricardo Valcárcel y miembros de la cátedra. A nombre del Grupo 03, integrado por Renzo Antayhua y quien les habla, Joan Medina, presentamos la sustentación formal del Sprint 03 para el Sistema Web P2P de Mentorías Académicas de la EPIS-UPT.»  
> **Renzo:** «Esta entrega representa un hito fundamental en el proyecto: hemos culminado el mecanismo por el cual los mentores acreditados publican sesiones grupales de asesoría, y hemos adelantado la construcción integral del motor de recomendación inteligente EdRecSys v1.0. Toda la evidencia que expondremos hoy se encuentra respaldada y congelada en el commit 7df0a88 de nuestro repositorio oficial.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`G03_EPIS_Informe_Sprint_03.md#L5-L17`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L5-L17); [`README.md#L1-L13`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/README.md#L1-L13).
* **Recurso Visual:** Isotipo y logotipo vectorizado de la EPIS-UPT; paleta institucional `#1C2A59` y `#B99451`.
* **Limitaciones:** Ninguna. Información plenamente auditable en Git.
* **Estado:** Lista ✅.

---

### Diapositiva 02: Objetivo del Sprint, Backlog y Comparación de Alcance
* **Título de la Diapositiva:** Visión Operativa del Sprint 03: Alcance Planificado frente a Ejecutado
* **Objetivo Académico:** Demostrar el grado de avance del Product Backlog Scrum, transparentando la ampliación de esfuerzo técnico y la colisión de nomenclatura en T-18.
* **Expositor Responsable:** Renzo Antayhua.
* **Tiempo Estimado:** 2 minutos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Objetivo Central:** Habilitar la oferta formativa docente vinculada al catálogo curricular oficial y dotar a la plataforma del motor de emparejamiento inteligente Top-k.
* **Items del Product Backlog Atendidos:**
  * `PB-009` (Prioridad P0 / S3): Publicación de ofertas en catálogo activo $\rightarrow$ **100% Culminado**.
  * `PB-010` (Prioridad P0 / Programado S4): Motor de recomendación Top-k $\rightarrow$ **Adelantado y Culminado en Backend**.
* **Matriz de Esfuerzo (Planificado vs Real):**
  * `T-14` (Joan): Formulario reactivo de ofertas $\rightarrow$ Plan: 2.0 h | Ejecutado: 2.0 h ✅.
  * `T-15` (Renzo): Motor EdRecSys v1.0 y API $\rightarrow$ Plan: 2.0 h | Ejecutado: 4.0 h (+2.0 h) ✅.
  * `T-16` (Renzo): Entidad relacional y DDL 003 $\rightarrow$ Plan: 1.0 h | Ejecutado: 3.0 h (+2.0 h) ✅.
  * `T-18` (Renzo): Testbench algorítmico y benchmarking $\rightarrow$ Plan: 0.0 h | Ejecutado: 2.0 h (+2.0 h) ✅.
  * **Balance de Capacidad:** Planificado: 5.0 horas-persona $\rightarrow$ Ejecutado: 11.0 horas-persona (+120%).
* **Nota de Control Metodológico:** Diferenciación entre `T-18 (S3)` (Testbench de simulación, Renzo) y `T-18 (S4)` (Integración UI con API Top-k, Joan).

#### Guion del Expositor (Notas del Orador)
> **Renzo:** «En la planificación original de la Tabla 5.4 del plan de sprints, el Sprint 03 tenía un alcance modesto de 5 horas centrado únicamente en la publicación básica de ofertas. Sin embargo, para garantizar que las sesiones publicadas fueran verdaderamente consumibles y estuvieran optimizadas para el emparejamiento, el equipo tomó la decisión técnica de adelantar el núcleo de inteligencia computacional. Esto elevó el esfuerzo real a 11 horas. Queremos hacer una aclaración metodológica rigurosa: la tarea que denominamos T-18 en este sprint corresponde al banco de evaluación algorítmica desarrollado por backend, y no debe confundirse con la T-18 del Sprint 4, que corresponde a la integración visual en la interfaz de usuario de Joan.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`PLAN_SPRINTS_Y_TAREAS.md#L49`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/PLAN_SPRINTS_Y_TAREAS.md#L49), [`#L152-L184`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/PLAN_SPRINTS_Y_TAREAS.md#L152-L184); [`sprint-03.md#L33-L44`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L33-L44).
* **Recurso Visual:** Cuadro comparativo de tareas con barras porcentuales de cumplimiento.
* **Limitaciones:** La colisión del ID T-18 debe quedar explicada para evitar observaciones de auditoría Scrum.
* **Estado:** Lista ✅.

---

### Diapositiva 03: Requisito Funcional RF08: Publicación de Ofertas (SRS)
* **Título de la Diapositiva:** Especificación de Requisitos: Requisito Funcional RF08
* **Objetivo Académico:** Respaldar la base contractual de ofertas conforme a la especificación formal del SRS (FD03 v2.1).
* **Expositor Responsable:** Joan Medina.
* **Tiempo Estimado:** 2 minutos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Definición Canónica (SRS FD03 L514):** «El sistema debe permitir a los estudiantes con rol de Mentor programar y publicar ofertas de asesoría en asignaturas críticas previamente aprobadas...»
* **Módulo:** `MOD-04: Planificación, Espacios y Agendamiento` (Prioridad: Alta / Crítica).
* **Parámetros Obligatorios del Payload:**
  * Asignatura curricular crítica (I a IV ciclo: *Cálculo I/II, Algoritmos, POO, BD*).
  * Unidad temática silábica oficial (`id_tema` y `nombre_tema`).
  * Modalidad pedagógica: *Presencial* (laboratorios) o *Virtual* (Google Meet).
  * Fecha de inicio en formato UTC y duración normalizada (60 o 90 minutos).
* **Marco de Reglas de Negocio Vinculadas:**
  * `RN-03`: Mérito académico institucional ($\text{ciclo\_actual} \ge \text{VII}$).
  * `RN-04`: Antelación obligatoria mayor a 24 horas ($T > 24\text{ h}$).
  * `RN-05`: Control de aforo normativo inmutable (10 presencial / 20 virtual).
* **Interacción con RF09:** Aprovisionamiento coordinado de espacios físicos o virtuales.

#### Guion del Expositor (Notas del Orador)
> **Joan:** «El requerimiento RF08 define el corazón operativo de la oferta docente en el sistema. Según nuestro SRS, no se trata simplemente de un formulario de agendamiento libre: exige que el mentor elija una asignatura que domine y la vincule estrictamente a un tema conceptual del sílabo oficial. Además, el requisito impone la coexistencia de tres reglas de negocio obligatorias: el mérito del ciclo superior bajo RN-03, la antelación mayor a un día bajo RN-04 y la asignación automática de aforos según la modalidad bajo RN-05. Todo esto se integra con RF09 para asignar un laboratorio de la EPIS o generar un enlace seguro.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`FD03-EPIS-Informe SRS de Proyecto.md#L514-L515`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L514-L515), [`#L547-L553`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L547-L553).
* **Código Backend:** [`app/schemas/offer.py#L6-L53`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/schemas/offer.py#L6-L53) (`PublishOfferPayload`).
* **Prueba Relacionada:** `test_offers.py` (`test_publish_offer_presencial_success`, [L26-L59](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_offers.py#L26-L59)).
* **Limitaciones:** En el incremento actual, el aprovisionamiento RF09 utiliza catálogo estático de laboratorios y enlaces deterministas.
* **Estado:** Lista ✅.

---

### Diapositiva 04: Caso de Uso Canónico CUS06: Narrativa Formal y Excepciones
* **Título de la Diapositiva:** Caso de Uso Canónico CUS06: Publicar Oferta de Mentoría
* **Objetivo Académico:** Explicar la dinámica del caso de uso nuclear CUS06 respetando la estructura formal de 4 tablas de la Regla 6 de documentación.
* **Expositor Responsable:** Joan Medina.
* **Tiempo Estimado:** 2 minutos 30 segundos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Ficha Técnica Canónica:**
  * Código: `CUS06` | Tipo: Primario, esencial.
  * Actor Principal: Mentor Académico (Estudiante de VII a X ciclo).
  * Actores Secundarios: Servicios Externos (Google Meet API / Discord Bot).
  * Precondición: Mentor autenticado, con perfil formativo activo y asignaturas aprobadas.
  * Postcondición: Sesión creada en estado `PUBLICADA`, visible en catálogo y con código `SES-XXXX`.
* **Flujo Principal (Secuencia de 6 Pasos):**
  1. Mentor pulsa «Crear Nueva Mentoría».
  2. Selecciona curso, tema silábico, fecha y duración (60/90 min).
  3. Sistema evalúa antelación ($T > 24\text{ h}$).
  4. Selecciona modalidad $\rightarrow$ Asignación inmutable de aforo (10 o 20).
  5. Sistema resuelve espacio (aula de laboratorio o enlace Meet).
  6. Confirmación de registro y emisión de código canónico `SES-XXXX`.
* **Flujos Alternativos:** FA01 (Atención a demanda insatisfecha de CUS03) | FA02 (Aula alternativa ante cruce de horario).
* **Excepciones de Negocio:**
  * `E01`: Antelación $\le 24\text{ h} \rightarrow$ Bloqueo por infracción de RN-04.
  * `E02`: Cruce de horario del mentor $\rightarrow$ Rechazo por superposición lectiva.
  * `E03`: Falla en servicio virtual $\rightarrow$ Sugerencia de cambio a modalidad presencial.

#### Guion del Expositor (Notas del Orador)
> **Joan:** «CUS06 fue estructurado siguiendo la Regla 6 de documentación del proyecto en cuatro tablas rigurosas. El flujo principal guía al mentor paso a paso, validando en cada interacción que no se vulneren las normativas universitarias. Si el mentor intenta programar una clase para dentro de 12 horas, la excepción E01 se dispara de inmediato en pantalla. De igual manera, CUS06 está diseñado para enlazarse en el flujo alternativo FA01 con el banco de demandas insatisfechas, permitiendo al mentor crear una clase que resuelva directamente una necesidad manifestada por los mentoreados en CUS03.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`FD03-EPIS-Informe SRS de Proyecto.md#L1742-L1784`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1742-L1784).
* **Código Frontend:** [`OfferPublishView.tsx#L266-L300`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/OfferPublishView.tsx#L266-L300) (`handleSubmit`).
* **Código Backend:** [`offer_service.py#L184-L297`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/offer_service.py#L184-L297) (`publish_offer`).
* **Prueba Relacionada:** Catálogo Excel Filas 41-48 (`CUS06-U01`, `CUS06-U02`, `CUS06-F01`, `CUS06-F02`).
* **Limitaciones:** En el alcance del Sprint 3, la resolución de cruces del mentor (E02) opera sobre las sesiones agendadas en la base de datos P2P.
* **Estado:** Lista ✅.

---

### Diapositiva 05: Modelado Visual de CUS06: Flujo de Actividades y Secuencia SAD
* **Título de la Diapositiva:** Modelado Arquitectónico: Secuencia Técnica de Publicación de Ofertas
* **Objetivo Académico:** Sustentar la vista de procesos del SAD (Kruchten 4+1), mostrando la interacción multicapa y síncrona entre cliente, API y base de datos.
* **Expositor Responsable:** Renzo Antayhua.
* **Tiempo Estimado:** 2 minutos 30 segundos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Diagrama de Secuencia Oficial (Diagrama 3.2):**
  * Presentación: `OfferPublishView.tsx` $\rightarrow$ Servicio Cliente: `offerService.ts`.
  * API Gateway: `endpoints/offers.py` $\rightarrow$ Dominio: `OfferService`.
  * Persistencia: Tabla `sesiones_mentoria` en PostgreSQL / Supabase.
* **Secuencia Operativa en 15 Pasos Clave:**
  * *Paso 1-3:* Captura y validación isomórfica de payload en cliente (`validateOfferPayload`).
  * *Paso 4-6:* Despacho HTTP `POST /api/v1/offers` con Bearer JWT e inspección de claims de identidad.
  * *Paso 7-9:* Evaluación de mérito `RN-03` y antelación obligatoria `RN-04` ($T > 24\text{ h}$).
  * *Paso 10-12:* Inserción atómica en base de datos (`INSERT INTO sesiones_mentoria`).
  * *Paso 13-15:* Confirmación transaccional, retorno de DTO tipado y despliegue de confirmación en UI.
* **Tratamiento de Excepciones:** Rollback atómico y emisión de HTTP 400 Bad Request o HTTP 403 Forbidden.

#### Guion del Expositor (Notas del Orador)
> **Renzo:** «Para implementar CUS06, el SAD prescribió un diagrama de secuencia de 15 pasos que articula nuestra arquitectura desacoplada. Como se observa en la figura, la validación no se delega ciegamente al servidor: el cliente realiza una primera comprobación reactiva inmediata para dar feedback al alumno en menos de 100 milisegundos. Cuando el formulario es enviado, el router de FastAPI recibe el payload, verifica la elegibilidad de mérito del mentor consultando la tabla de perfiles y ejecuta la inserción con transaccionalidad ACID en PostgreSQL. Si alguna restricción de base de datos fallara, el sistema asegura la integridad mediante rollback.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`FD04-EPIS-Informe SAD de Proyecto.md#L798-L804`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md#L798-L804); [`TRAZABILIDAD_PUBLICACION_OFERTAS.md#L72-L128`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/TRAZABILIDAD_PUBLICACION_OFERTAS.md#L72-L128).
* **Recurso Visual:** Diagrama vectorial renderizado [`08_secuencia_tecnica_publicacion_ofertas.png`](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/diseño/imagenes/sprint-03/08_secuencia_tecnica_publicacion_ofertas.png).
* **Prueba Relacionada:** `OfferPublishView.test.tsx` ([L183-L232](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx#L183-L232)); `test_offers.py` ([L274-L331](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_offers.py#L274-L331)).
* **Limitaciones:** En el diagrama se modela el paso de Bearer JWT por cabecera HTTP; en el cliente SPA actual, el adaptador de producción está preparado para anexar el token cuando se configure el modo API completo.
* **Estado:** Lista ✅.

---

### Diapositiva 06: Capa de Presentación (T-14): Formulario Reactivo y Selección Curricular
* **Título de la Diapositiva:** Implementación Frontend (T-14): Formulario Reactivo y Selección Curricular
* **Objetivo Académico:** Demostrar la robustez, accesibilidad e interactividad de la interfaz construida por Joan en React 19 y TypeScript.
* **Expositor Responsable:** Joan Medina.
* **Tiempo Estimado:** 2 minutos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Componente Central:** `aplicacion/frontend/src/components/OfferPublishView.tsx` (1,186 líneas).
* **Características Clave de la Interfaz:**
  * *Carga Curricular Dinámica:* Selector reactivo que consume las 5 asignaturas filtro de I a IV ciclo.
  * *Desglose Silábico Reactivo:* Al seleccionar la materia, se invocan los temas conceptuales oficiales (`fetchCourseDetail`).
  * *Control de Concurrencia UI:* Bloqueo de doble clic mediante bandera reactiva `isSubmitting`.
  * *Retroalimentación Visual Inmediata:* Banner informativo de modo de ejecución (Mock/API) y confirmación destacada con código institucional.
* **Evidencia Visual:** Captura auténtica `01_offer_publish_form.png` (161 KB).
* **Aseguramiento de Calidad:** 7 pruebas específicas en Vitest / React Testing Library (`OfferPublishView.test.tsx`).

#### Guion del Expositor (Notas del Orador)
> **Joan:** «En la Diapositiva 6 podemos observar la pantalla real del formulario de publicación ejecutándose en nuestro entorno local. Diseñé este componente cuidando tres aspectos esenciales: primero, la consistencia curricular: ningún mentor puede escribir temas al azar; el sistema consulta el catálogo del Sprint 1 y extrae los temas silábicos oficiales de asignaturas como Algoritmos o Cálculo. Segundo, la accesibilidad: cada campo cuenta con etiquetas semánticas y estados de foco visibles. Y tercero, la robustez: la interfaz cuenta con 7 pruebas automatizadas que verifican desde la renderización inicial hasta la confirmación de guardado.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`G03_EPIS_Informe_Sprint_03.md#L50-L79`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L50-L79); [`INFORME_GENERAL_SPRINT_03.md#L120-L185`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/INFORME_GENERAL_SPRINT_03.md#L120-L185).
* **Código Frontend:** [`OfferPublishView.tsx#L119-L200`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/OfferPublishView.tsx#L119-L200), [`#L370-L460`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/OfferPublishView.tsx#L370-L460).
* **Recurso Visual:** Captura oficial [`01_offer_publish_form.png`](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/diseño/imagenes/sprint-03/01_offer_publish_form.png).
* **Prueba Relacionada:** `OfferPublishView.test.tsx` (`1. Renderiza el formulario con banner...`, [L82-L98](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx#L82-L98)).
* **Limitaciones:** En el entorno local alfa opera por defecto con adaptador mock explícito para independizar las pruebas de interfaz.
* **Estado:** Lista ✅.

---

### Diapositiva 07: Reglas RN-04 y RN-05: Antelación (>24h) y Aforo Inmutable (10/20)
* **Título de la Diapositiva:** Validación de Reglas de Negocio en Cliente: Antelación (RN-04) y Aforos (RN-05)
* **Objetivo Académico:** Demostrar cómo las reglas de negocio institucionales son aplicadas en tiempo real mediante validación reactiva en la UI.
* **Expositor Responsable:** Joan Medina.
* **Tiempo Estimado:** 2 minutos 30 segundos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Regla RN-04 (Antelación de Publicación):**
  * *Lógica Matemática:* $\text{Antelación} = \frac{t_{\text{inicio}} - t_{\text{actual}}}{3600\text{ s}}$.
  * *Infracción ($T \le 24\text{ h}$):* Banner rojo perentorio, mensaje de error reglamentario y botón «Publicar» deshabilitado.
  * *Recomendación ($24\text{ h} < T < 48\text{ h}$):* Advertencia formativa ámbar sugiriendo mayor plazo de difusión.
  * *Óptimo ($T \ge 48\text{ h}$):* Distintivo verde de conformidad institucional.
* **Regla RN-05 (Aforo Reglamentario Inmutable):**
  * *Modalidad Presencial:* Exactamente **10 estudiantes** (aforo estándar laboratorios EPIS).
  * *Modalidad Virtual:* Exactamente **20 estudiantes** (aforo estándar salas Google Meet).
  * *Control en DOM:* Input con atributo `readOnly`: imposibilidad física de manipulación manual.
* **Evidencias Visuales:** Capturas `02_advance_time_validation_rn04.png` y `03_capacity_control_rn05.png`.

#### Guion del Expositor (Notas del Orador)
> **Joan:** «En esta diapositiva demostramos la aplicación en tiempo de ejecución de las reglas RN-04 y RN-05. A la izquierda vemos cómo reacciona el sistema cuando el mentor intenta fijar una sesión para realizarse en 5 horas: el software calcula inmediatamente la antelación, despliega una alerta roja y deshabilita por completo el botón de envío. Esto es crítico, porque si permitiéramos publicar con menos de 24 horas, violaríamos el ciclo de ratificación previa de quórum de la regla RN-08. A la derecha vemos la regla RN-05: cuando el mentor cambia la modalidad de presencial a virtual, el aforo conmuta automáticamente de 10 a 20 cupos de forma inmutable, impidiendo que el usuario altere los límites aprobados por la facultad.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`FD03-EPIS-Informe SRS de Proyecto.md#L550-L551`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L550-L551), [`#L1763`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1763); [`sprint-03.md#L59-L68`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L59-L68).
* **Código Frontend:** [`offerService.ts#L80-L180`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/services/offerService.ts#L80-L180); [`OfferPublishView.tsx#L480-L720`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/OfferPublishView.tsx#L480-L720).
* **Recursos Visuales:** Capturas [`02_advance_time_validation_rn04.png`](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/diseño/imagenes/sprint-03/02_advance_time_validation_rn04.png) y [`03_capacity_control_rn05.png`](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/diseño/imagenes/sprint-03/03_capacity_control_rn05.png).
* **Pruebas Relacionadas:** `offerService.test.ts` ([L71-L183](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/services/__tests__/offerService.test.ts#L71-L183)); `OfferPublishView.test.tsx` ([L99-L155](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx#L99-L155)).
* **Limitaciones:** Ninguna. Cobertura unitaria y de integración exhaustiva en Vitest.
* **Estado:** Lista ✅.

---

### Diapositiva 08: Backend de Ofertas (T-16): API REST, Modelo Relacional y Persistencia
* **Título de la Diapositiva:** Diseño e Implementación Backend: Modelo Relacional, DDL y API de Ofertas (T-16)
* **Objetivo Académico:** Sustentar la persistencia física en PostgreSQL/Supabase, la migración Alembic 003 y los endpoints REST tipados de FastAPI.
* **Expositor Responsable:** Renzo Antayhua.
* **Tiempo Estimado:** 2 minutos 30 segundos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Entidad Relacional `sesiones_mentoria` (`models/offer.py`):**
  * Clave primaria `id_sesion` autoincremental y código canónico `codigo_sesion` (`UNIQUE`).
  * Claves foráneas: `mentor_email` $\rightarrow$ `usuarios`, `id_asignatura` $\rightarrow$ `asignaturas`, `id_tema` $\rightarrow$ `temas_conceptuales`.
  * Restricciones `CHECK`: `modalidad IN ('presencial', 'virtual')`, `aforo_maximo IN (10, 20)`, `duracion_minutos IN (60, 90)`.
  * Índices B-Tree: 5 índices optimizados en columnas de filtrado (`mentor_email`, `codigo_sesion`, `fecha_inicio`, etc.).
* **Contratos REST FastAPI (`endpoints/offers.py`):**
  * `POST /api/v1/offers`: Inserción transaccional, valida RN-03, RN-04, RN-05 $\rightarrow$ Retorna `HTTP 201 Created`.
  * `GET /api/v1/offers`: Catálogo activo con filtros por asignatura, mentor y modalidad $\rightarrow$ Retorna `HTTP 200 OK`.
* **Auditoría de Implementación:**
  * Validación de Mérito RN-03 en `validate_mentor_eligibility()`: Implementa disyunción (`rol_mentor OR ciclo >= 7`) y bypass para cuentas semilla de testing.
  * Resiliencia: Fallback en memoria ante contingencias de conectividad con Supabase.

#### Guion del Expositor (Notas del Orador)
> **Renzo:** «En el backend, formalizamos la entidad relacional sesiones_mentoria a través de la migración Alembic 003. Siguiendo el estándar D-4 de nuestras reglas de diseño, blindamos la tabla con restricciones de dominio CHECK directamente en el motor PostgreSQL: no hay forma física de insertar un aforo distinto a 10 o 20, ni una modalidad que no sea presencial o virtual. El endpoint POST /api/v1/offers valida en el servidor que la antelación supere las 24 horas y que el mentor cumpla el mérito académico. Cabe precisar técnicamente que la función validate_mentor_eligibility fue implementada con una disyunción en código para permitir la evaluación fluida tanto de roles como de perfiles de prueba en desarrollo.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`INFORME_GENERAL_SPRINT_03.md#L220-L275`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/INFORME_GENERAL_SPRINT_03.md#L220-L275); [`sprint-03.md#L212-L259`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L212-L259).
* **Código Backend:** [`models/offer.py#L9-L65`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/models/offer.py#L9-L65); [`003_mentoring_offers.py#L25-L77`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/db/migrations/versions/003_mentoring_offers.py#L25-L77); [`offer_service.py#L128-L297`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/offer_service.py#L128-L297).
* **Recurso Visual:** Cuadro DDL de estructura relacional e índices en PostgreSQL.
* **Pruebas Relacionadas:** `test_offers.py` (`test_offer_service_with_real_db_session`, [L274-L331](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_offers.py#L274-L331)).
* **Limitaciones:** La cabecera `Authorization` en el endpoint es opcional en la API para facilitar pruebas en desarrollo; si se provee, valida el token y bloquea suplantaciones de identidad.
* **Estado:** Lista ✅.

---

### Diapositiva 09: Requisito Funcional RF06: Especificación del Motor Top-k (SRS)
* **Título de la Diapositiva:** Inteligencia Computacional: Requisito Funcional RF06 (Recomendación Top-k)
* **Objetivo Académico:** Exponer los requerimientos funcionales y no funcionales del recomendador según la línea base del SRS (FD03 v2.1).
* **Expositor Responsable:** Renzo Antayhua.
* **Tiempo Estimado:** 2 minutos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Especificación SRS (FD03 L512):** «El sistema debe procesar el vector de necesidades conceptuales declarado por el mentoreado frente a las competencias de los mentores... presentando una lista ordenada de 3 a 5 mentores recomendados (Top-k).»
* **Módulo Responsable:** `MOD-03: Motor de Recomendación Inteligente (EdRecSys)`.
* **Propósito Pedagógico:** Resolver el problema de sobrecarga de opciones para alumnos de ciclos iniciales (I a IV), maximizando la afinidad silábica y la compatibilidad horaria.
* **Requisito No Funcional RNF03 (Rendimiento del Motor):**
  * Tiempo de respuesta exigido para el cálculo Top-k: $\le 500\text{ ms}$ en entorno completo ($\le 50\text{ ms}$ en microservicio/cálculo puro).
* **Entradas de Inferencia:** Perfil formativo del estudiante, matriz de agenda 6×11 (`CUS15`), catálogo de ofertas vigentes y materias críticas.

#### Guion del Expositor (Notas del Orador)
> **Renzo:** «Pasamos ahora al componente de inteligencia computacional del sistema. El requisito RF06 responde a una problemática institucional muy clara: un estudiante de primer o segundo ciclo con dificultades en Algoritmos no sabe qué mentor elegir ni qué horario le conviene. El SRS exige que el sistema realice una inferencia personalizada, analizando las necesidades del alumno frente a las competencias de los mentores disponibles y su matriz de disponibilidad horaria, entregando un Top-k ordenado. Además, el requisito no funcional RNF03 nos impone que todo este cómputo algorítmico se resuelva en una ventana de milisegundos.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`FD03-EPIS-Informe SRS de Proyecto.md#L512`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L512), [`#L586`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L586); [`FD04#L110`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md#L110).
* **Código Backend:** [`app/schemas/recommendation.py#L50-L102`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/schemas/recommendation.py#L50-L102).
* **Prueba Relacionada:** `test_recommendations.py` ([L98-L126](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_recommendations.py#L98-L126)).
* **Limitaciones:** En la visión integral de largo plazo el SRS proyecta modelos de embeddings continuos; en el Sprint 3 se implementa el modelo de conjuntos silábicos discretos.
* **Estado:** Lista ✅.

---

### Diapositiva 10: Caso de Uso Canónico CUS02: Recomendaciones y Flujo de Demanda
* **Título de la Diapositiva:** Caso de Uso Canónico CUS02: Consultar Recomendaciones Top-k
* **Objetivo Académico:** Detallar la interacción del mentoreado al consultar el feed y explicar cómo se articula con las solicitudes por demanda (CUS03).
* **Expositor Responsable:** Renzo Antayhua.
* **Tiempo Estimado:** 2 minutos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Ficha Técnica Canónica:**
  * Código: `CUS02` | Actor Principal: Mentoreado (Ciclos I a IV).
  * Actor Secundario: Motor de Recomendación *EdRecSys v1.0*.
  * Precondición: Mentoreado con perfil y agenda 6×11 registrados (`CUS15`).
  * Postcondición: Despliegue de tarjetas Top-5 con porcentaje de compatibilidad y botón de reserva directa (`CUS04`).
* **Flujo Principal y Flujos Alternativos:**
  * *Flujo Principal:* Ingreso a pestaña $\rightarrow$ Inferencia algorítmica $\rightarrow$ Renderizado Top-k con desglose explicable.
  * *Flujo Alternativo FA01:* Ajuste de filtros por asignatura formativa o modalidad.
  * *Flujo Alternativo FA02 (Inexistencia de Ofertas Compatibles):* El sistema detecta coincidencia horaria nula y despliega sugerencia contextual: *«No encontramos ofertas en tu horario. Puedes registrar una solicitud de demanda temática»* $\rightarrow$ Enlace a `CUS03`.
* **Manejo de Excepciones:** `E01` (Matriz no configurada $\rightarrow$ Redirige a perfil) | `E02` (Fallback cronológico ante latencia).

#### Guion del Expositor (Notas del Orador)
> **Renzo:** «La narrativa de CUS02 resuelve de forma elegante los escenarios en los que el estudiante no encuentra de inmediato lo que busca. En el flujo alternativo FA02, si el motor evalúa que ningún mentor tiene sesiones en las franjas horarias del mentoreado, no muestra una pantalla vacía frustrante: orienta al alumno para que registre una solicitud por demanda en CUS03. De esta forma, el ecosistema retroalimenta la demanda insatisfecha hacia los mentores, cerrando el ciclo pedagógico entre la necesidad del estudiante y la planificación docente.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`FD03-EPIS-Informe SRS de Proyecto.md#L1610-L1648`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1610-L1648); [`FD04#L180-L194`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md#L180-L194).
* **Código Backend:** [`endpoints/recommendations.py#L59-L83`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/api/v1/endpoints/recommendations.py#L59-L83) (`get_recommended_offers`).
* **Recurso Visual:** Diagrama de Casos de Uso del paquete MOD-03 en el SAD.
* **Pruebas Relacionadas:** Catálogo Excel Filas 14-21 (`CUS02-U01` a `CUS02-A01`).
* **Limitaciones:** En el Sprint 3 el consumo de CUS02 está verificado a nivel de endpoints y servicios de backend; la interfaz visual del feed corresponde a la integración de Joan en el Sprint 4.
* **Estado:** Lista ✅.

---

### Diapositiva 11: Motor EdRecSys v1.0 (T-15): Algoritmo, Formulación Matemática y Top-k
* **Título de la Diapositiva:** Motor EdRecSys v1.0 (T-15): Formulación Matemática, Ponderadores y Desempate
* **Objetivo Académico:** Sustentar la formulación matemática del recomendador, demostrando el determinismo del ranking y la explicabilidad algorítmica.
* **Expositor Responsable:** Renzo Antayhua.
* **Tiempo Estimado:** 3 minutos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Formulación Multifactorial Compuesta:**
  $$S_{\text{base}} = 0.40 \cdot S_{\text{tema}} + 0.35 \cdot S_{\text{horario}} + 0.15 \cdot S_{\text{modalidad}} + 0.10 \cdot S_{\text{afinidad}}$$
  $$S_{\text{total}} = \text{round}(S_{\text{base}} \times W_{\text{curso}}, 4)$$
* **Desglose de Factores Matemáticos:**
  * *Similitud Temática ($S_{\text{tema}}$):* Coeficiente de Jaccard $J(T_m, T_k) = \frac{|T_m \cap T_k|}{|T_m \cup T_k|}$ y Dice $D(T_m, T_k)$.
  * *Compatibilidad Horaria ($S_{\text{horario}}$):* Coincidencia sobre matriz 6×11: $\min\left(1.0, \frac{|H_m \cap H_k|}{|H_m|}\right)$.
  * *Filtro de Mérito RN-03:* Si $\text{ciclo\_actual}(k) < 7 \rightarrow \text{Eligible} = 0 \rightarrow S_{\text{total}} = 0.0$.
* **Ponderador Curricular Filtro ($W_{\text{curso}}$):** Algoritmos ($1.3\text{x}$), Cálculo I/II y POO ($1.2\text{x}$), BD ($1.1\text{x}$).
* **Tupla de Desempate Determinista:** `(-S_total, -W_curso, -ciclo_actual, -matching_slots, email)`.
* **Transparencia y Explicabilidad:** Endpoint `POST /api/v1/recommendations/explain` con desglose auditable de puntajes.

#### Guion del Expositor (Notas del Orador)
> **Renzo:** «La formulación matemática de EdRecSys v1.0 fue diseñada bajo un principio de transparencia total: cero modelos de caja negra. El puntaje base combina cuatro dimensiones normalizadas entre 0 y 1: solapamiento temático silábico con peso del 40%, compatibilidad de franjas horarias con 35%, alineación de modalidad formativa con 15% y afinidad de asignaturas inscritas con 10%. Sobre este puntaje, aplicamos un multiplicador de prioridad de la EPIS para incentivar las materias con mayor índice de reprobación, como Algoritmos con 1.3x. Si dos mentores obtienen el mismo puntaje final, la tupla de ordenación desempata deterministamente por multiplicador, ciclo de avance y coincidencia horaria, garantizando que el ranking sea idéntico byte a byte en cada petición.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`G03_EPIS_Informe_Sprint_03.md#L280-L345`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L280-L345); [`sprint-03.md#L142-L180`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L142-L180).
* **Código Backend:** [`recommendation_service.py#L128-L156`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L128-L156), [`#L177-L335`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L177-L335), [`#L464-L470`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L464-L470), [`#L606-L716`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/recommendation_service.py#L606-L716).
* **Recurso Visual:** Fórmulas matemáticas en KaTeX y captura del endpoint de explicabilidad algorítmica.
* **Pruebas Relacionadas:** `test_recommendations.py` ([L31-L95](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_recommendations.py#L31-L95), [L155-L185](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_recommendations.py#L155-L185)).
* **Limitaciones:** La regla RN-11 del SRS define criterios cualitativos de prioridad institucional; los multiplicadores numéricos específicos constituyen una optimización empírica de dominio.
* **Estado:** Lista ✅.

---

### Diapositiva 12: Demostración Funcional: Recorrido en Vivo y Modos Real/Mock
* **Título de la Diapositiva:** Demostración Funcional del Sistema: Flujo de Ejecución y Trazabilidad Operativa
* **Objetivo Académico:** Guiar la demostración en vivo del sistema, delimitando con rigor técnico los componentes conectados a la API y el aislamiento del adaptador mock.
* **Expositor Responsable:** Presentación Conjunta (Joan en UI y Renzo en API).
* **Tiempo Estimado:** 3 minutos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Paso a Paso de la Demostración en Vivo:**
  1. *Navegación SPA:* Acceso a la pestaña `🏷️ Publicar Ofertas` (`http://localhost:5173`).
  2. *Carga Curricular:* Selección de *Algoritmos y Estructuras de Datos* y carga de unidades temáticas silábicas.
  3. *Prueba Negativa de Antelación (RN-04):* Selección de fecha a $T < 24\text{ h} \rightarrow$ Alerta roja de bloqueo y botón deshabilitado.
  4. *Prueba Positiva de Antelación (RN-04):* Corrección a $T \ge 48\text{ h} \rightarrow$ Distintivo verde institucional.
  5. *Comprobación de Aforo Inmutable (RN-05):* Alternancia entre Presencial (10) y Virtual (20) en campo de solo lectura.
  6. *Confirmación:* Envío del formulario, emisión de código canónico `SES-XXXX` y registro en catálogo.
  7. *Verificación de Backend:* Consulta de OpenAPI/Swagger UI (`http://localhost:8000/docs`) y ejecución de `/testbench`.
* **Transparencia Arquitectónica:** Delimitación explícita del banner «Modo de Prueba Local (Mock)» en el frontend frente a la persistencia real verificada en las suites de Pytest del backend.

#### Guion del Expositor (Notas del Orador)
> **Joan:** «Para la demostración en vivo, recorreremos exactamente los 7 pasos estipulados en nuestro informe técnico. Comenzamos en la interfaz de React 19 seleccionando una asignatura crítica. Al intentar publicar con una antelación de 10 horas, vemos el bloqueo inmediato de la regla RN-04. Al corregir la fecha a más de 48 horas, el botón se habilita y podemos alternar la modalidad para verificar que el aforo se fija en 10 o 20 sin permitir edición manual. Tras publicar, la pantalla muestra la tarjeta verde de confirmación con el código de sesión emitido.»  
> **Renzo:** «Simultáneamente, en el backend podemos verificar los endpoints activos en Swagger UI bajo /api/v1/offers y /api/v1/recommendations/offers. Queremos transparentar ante el jurado que, de conformidad con nuestra regla de madurez técnica 3.2.6, la interfaz SPA despliega de forma permanente su banner de modo mock para pruebas locales desacopladas, mientras que la persistencia ACID en PostgreSQL se encuentra verificada mediante la suite de integración de Pytest.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`README.md#L204-L263`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/README.md#L204-L263); [`sprint-03.md#L48-L80`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L48-L80).
* **Código de Navegación:** [`App.tsx#L340-L365`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/App.tsx#L340-L365); [`OfferPublishView.tsx`](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/components/OfferPublishView.tsx).
* **Recursos Visuales:** Capturas [`01_offer_publish_form.png`](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/diseño/imagenes/sprint-03/01_offer_publish_form.png) y [`04_swagger_api_docs_sprint03.png`](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/diseño/imagenes/sprint-03/04_swagger_api_docs_sprint03.png).
* **Pruebas Relacionadas:** `App.test.tsx` (`permite alternar entre las pestañas...`, [L5-L50](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/__tests__/App.test.tsx#L5-L50)).
* **Limitaciones:** El cliente frontend no adjunta aún el token Bearer en las llamadas de red del adaptador API.
* **Estado:** Lista ✅.

---

### Diapositiva 13: Catálogo Oficial de Pruebas: Homologación Excel CUS06 y CUS02
* **Título de la Diapositiva:** Trazabilidad Institucional: Homologación con el Catálogo de Pruebas (Excel)
* **Objetivo Académico:** Demostrar la correspondencia formal entre la matriz de pruebas de la fase de análisis y las aserciones automatizadas implementadas.
* **Expositor Responsable:** Joan Medina (CUS06) y Renzo Antayhua (CUS02).
* **Tiempo Estimado:** 2 minutos 30 segundos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Matriz de Homologación de Casos de Prueba (Excel `Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`):**
  * *Casos CUS06 (Publicación de Ofertas):*
    * `CUS06-U01` (Fila 41): Validación de campos obligatorios $\rightarrow$ Superado en `offerService.test.ts` (L22) y `test_offers.py` (L334).
    * `CUS06-U02` (Fila 42): Aforo automático por modalidad (RN-05) $\rightarrow$ Superado en `OfferPublishView.test.tsx` (L100) y `test_offers.py` (L153).
    * `CUS06-F01` (Fila 46): Flujo interactivo presencial $\rightarrow$ Superado en `OfferPublishView.test.tsx` (L183) y `test_offers.py` (L26).
    * `CUS06-F02` (Fila 47): Flujo virtual y antelación RN-04 $\rightarrow$ Superado en `OfferPublishView.test.tsx` (L183) y `test_offers.py` (L62).
  * *Casos CUS02 (Recomendación Top-k):*
    * `CUS02-U01..U04` (Filas 14-17): Propiedades matemáticas y desempate $\rightarrow$ Superado en `test_recommendations.py` (L31-L95).
    * `CUS02-U05` (Fila 18): Estructura del endpoint `/recommend` $\rightarrow$ Superado en `test_recommendations.py` (L98-L126).
    * `CUS02-A01` (Fila 21): Latencia y rendimiento algorítmico $\rightarrow$ Superado en `test_simulation.py` (L67-L82).
* **Dictamen:** 100% de los casos analíticos comprometidos se encuentran verificados con aserciones automatizadas.

#### Guion del Expositor (Notas del Orador)
> **Joan:** «Para garantizar la trazabilidad exigida por la cátedra, abrimos directamente el archivo Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx generado en la etapa de análisis y mapeamos caso por caso. Para CUS06, las pruebas unitarias y funcionales U01, U02, F01 y F02 coinciden exactamente con nuestras suites en Vitest y Pytest, verificando la antelación, los campos obligatorios y los aforos.»  
> **Renzo:** «En el caso de CUS02, las filas 14 a 18 del Excel que definían las pruebas de similitud matemática y ordenamiento se encuentran implementadas en test_recommendations.py. Asimismo, la prueba de aceptación A01, que exigía una latencia menor a 500 ms, fue superada con creces en nuestro benchmark automatizado, demostrando total alineamiento entre el análisis teórico y la construcción del software.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx) (A14:O21, A41:O48); [`sprint-03.md#L82-L100`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L82-L100), [`#L183-L200`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L183-L200).
* **Código de Pruebas:** Las 5 suites reales verificadas: `test_offers.py` (14 pruebas), `test_recommendations.py` (19 pruebas), `test_simulation.py` (5 pruebas), `OfferPublishView.test.tsx` (7 pruebas) y `offerService.test.ts` (14 pruebas).
* **Recurso Visual:** Tabla comparativa formal de trazabilidad analítica Excel vs Pytest/Vitest.
* **Pruebas Relacionadas:** 59 pruebas automatizadas específicas del incremento de Sprint 3 (21 en frontend y 38 en backend).
* **Limitaciones:** Los casos `CUS06-U03` (parser horarios) y `CUS06-U04` (OAuth Meet) corresponden a integraciones externas clasificadas como "Posterior" en el Product Backlog.
* **Estado:** Lista ✅.

---

### Diapositiva 14: Aseguramiento de Calidad: 209 Tests, Cobertura >92% y Cierre DoD
* **Título de la Diapositiva:** Calidad de Software, Testbench Algorítmico y Certificación del DoD
* **Objetivo Académico:** Demostrar el cumplimiento riguroso de los umbrales de calidad de RNF09, desglosando la estructura empírica de pruebas (existentes, regresión y nuevas en commit `7df0a88`) y formalizar el cierre del Sprint 03 y las condiciones de entrada al Sprint 04.
* **Expositor Responsable:** Presentación Conjunta (Joan y Renzo).
* **Tiempo Estimado:** 3 minutos.

#### Contenido Visible en Pantalla (Diseño 16:9)
* **Auditoría y Clasificación Rigurosa de Pruebas (Commit `7df0a88`):**
  * *1. Pruebas Existentes / Heredadas (Línea Base S1-S2):* **150 pruebas** (84 backend / 66 frontend en 21 suites), acreditadas en commit `3766a08`.
  * *2. Pruebas de Regresión Verificadas:* **150 / 150 pruebas superadas (100%)**, certificando cero rotura en autenticación OTP, consentimiento de privacidad, perfiles y disponibilidad horaria tras integrar Sprint 03.
  * *3. Pruebas Nuevas Añadidas en Sprint 03:* **59 pruebas nuevas** incorporadas exclusivamente en **5 archivos reales**:
    * **Frontend (21 pruebas en 2 suites):**
      * `OfferPublishView.test.tsx` (7 pruebas): renderizado reactivo, aforo inmutable 10/20, bloqueo RN-04 ($\le 24\text{ h}$), recomendación $>24\text{ h}$ y reseteo UI.
      * `offerService.test.ts` (14 pruebas): cálculo temporal de antelación, validación de payload, manejo de errores y adaptadores Mock/API.
    * **Backend (38 pruebas en 3 suites):**
      * `test_offers.py` (14 pruebas): ciclo de vida de ofertas, validación RN-04/RN-05, permisos de mentor RN-03, persistencia ACID PostgreSQL y fallback.
      * `test_recommendations.py` (19 pruebas): motor EdRecSys v1.0, Jaccard/Dice, ponderaciones, multiplicadores curriculares, Top-k y null-safety.
      * `test_simulation.py` (5 pruebas): testbench sintético, 4 casos frontera, latencia de cómputo y determinismo algorítmico.
  * *4. Total Consolidado de la Solución:* **209 pruebas aprobadas al 100%** (122 backend / 87 frontend) en 26 suites sin un solo fallo.
* **Aclaración Documental Expresa sobre Rutas de Prueba:**
  * En la versión congelada `7df0a88` **NO existen** las rutas `RecommendationsView.test.tsx` (la UI del mentorado no incluyó suite de vista aislada en S3; la cobertura frontend de recomendación se delegó a contratos de servicio) ni `test_recommendation_benchmark.py` (el benchmarking y testbench algorítmico residen íntegramente en `test_simulation.py`).
* **Cronología de Git y Reconciliación de Cifras Documentales (`git show` / `git diff`):**
  * *Commit `741256b` (Snapshot S2):* Ya se encontraban desarrolladas las **21 pruebas de frontend** (`OfferPublishView.test.tsx` [7] y `offerService.test.ts` [14]).
  * *Commit `094c9fb` (Cierre Backend S3):* Se incorporaron íntegramente las tres suites de backend con sus **38 pruebas** (`test_offers.py` [14], `test_recommendations.py` [19] y `test_simulation.py` [5]).
  * *Commit `fea566c` (Estandarización SAD):* No añadió funciones de prueba nuevas (solo limpieza `engine.dispose()` en sesiones DB y ajustes documentales).
  * *Cifra Histórica de «47 Pruebas»:* Figura en informes previos como una **estimación documental preliminar de redacción**, mientras que el repositorio congelado en `7df0a88` contiene y aprueba efectivamente **59 pruebas específicas del Sprint 03** ($21\text{ FE} + 38\text{ BE}$).
* **Métricas de Cobertura y Linteo (RNF09):**
  * *Frontend (Vitest v8):* **92.52% de líneas** (Umbral RNF09 $\ge 70\%$) ✅.
  * *Backend (Pytest-Cov):* **92.14% de líneas** (92.15% en terminal; 1,746 sentencias, 137 miss) ✅.
  * *Linteo Estático:* ESLint 9 (0 errores) | Ruff 0.9 (0 errores, 62 archivos formateados conformes).
* **Testbench Algorítmico (T-18 / PB-027):**
  * 4 casos frontera superados: sin solapamiento ($S=0$), materias disjuntas ($J=0$), catálogo vacío (`items: []`) y mérito RN-03 (**0.00% tasa de fuga**).
  * Latencia de cómputo observada: **$35.8\text{ µs}$ por candidato** ($0.86\text{ ms}$ total, superando RNF03 $< 50\text{ ms}$).
* **Cierre del Definition of Done (DoD) y Entrada al Sprint 04:**
  * Cumplimiento estricto del 100% de los criterios DoD del sprint.
  * *Habilitación Técnica para Sprint 04:* Ofertas publicadas y motor de afinidad listos para la **reserva transaccional de cupos con prevención de sobrecupo (`RF12` / `CUS04`)**.

#### Guion del Expositor (Notas del Orador)
> **Joan:** «Para concluir, el aseguramiento de la calidad de nuestro sistema se respalda en cifras empíricas reproducibles y auditadas al commit 7df0a88. En el frontend consolidamos 87 pruebas automatizadas: 66 pruebas heredadas de los sprints 1 y 2 que actúan como batería de regresión sin ninguna rotura, y 21 pruebas nuevas desarrolladas en este Sprint 3. Estas 21 pruebas nuevas se distribuyen con exactitud en 2 archivos reales: 7 pruebas interactivas en OfferPublishView.test.tsx que validan el comportamiento reactivo de la interfaz, y 14 pruebas en offerService.test.ts que verifican el cálculo de antelación y los adaptadores. Queremos aclarar que no existe una suite RecommendationsView.test.tsx en esta versión; la validación del recomendador en el cliente se probó a través de los contratos del servicio. Alcanzamos un 92.52% de cobertura en Vitest, superando con holgura el umbral reglamentario del 70%.»  
> **Renzo:** «En el backend consolidamos 122 pruebas con un 92.14% de cobertura sobre 1,746 sentencias ejecutadas. Esta suite integra 84 pruebas de regresión previas y exactamente 38 pruebas nuevas añadidas durante el Sprint 3, distribuidas en 3 archivos verificados: 14 pruebas en test_offers.py, 19 pruebas en test_recommendations.py y 5 pruebas en test_simulation.py. Aclaramos ante el jurado que si bien en los informes preliminares se consignó documentariamente la cifra de 47 pruebas, la auditoría rigurosa de Git demuestra que las 38 pruebas de backend ingresaron íntegramente en el commit 094c9fb y las 21 de frontend en el commit 741256b, sumando las 59 pruebas nuevas que hoy sustentamos. Asimismo, el testbench algorítmico y benchmarking de latencia está implementado en test_simulation.py, no en un archivo hipotético separado. Certificamos un 0% de fuga ante postulantes no elegibles y una velocidad de cálculo de 35 microsegundos por candidato. Con estos resultados empíricos, certificamos el cumplimiento pleno del Definition of Done del Sprint 03 y dejamos la plataforma en un estado de madurez técnica óptimo para abordar las reservas transaccionales en el Sprint 04. Quedamos a su disposición para las preguntas del jurado. Muchas gracias.»

#### Respaldos y Trazabilidad
* **Fuentes Documentales:** [`G03_EPIS_Informe_Sprint_03.md#L109-L125`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L109-L125), [`#L363-L389`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/G03_EPIS_Informe_Sprint_03.md#L363-L389); [`sprint-03.md#L109-L125`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L109-L125).
* **Código de Pruebas Auditado en Commit `7df0a88`:**
  * Frontend: [`OfferPublishView.test.tsx` (7 pruebas, L82-L247)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx#L82-L247); [`offerService.test.ts` (14 pruebas, L22-L260)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/services/__tests__/offerService.test.ts#L22-L260).
  * Backend: [`test_offers.py` (14 pruebas, L26-L435)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_offers.py#L26-L435); [`test_recommendations.py` (19 pruebas, L31-L425)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_recommendations.py#L31-L425); [`test_simulation.py` (5 pruebas, L9-L82)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_simulation.py#L9-L82).
* **Recursos Visuales:** Capturas [`05_backend_pytest_coverage_sprint03.png`](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/diseño/imagenes/sprint-03/05_backend_pytest_coverage_sprint03.png), [`06_frontend_vitest_coverage_sprint03.png`](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/diseño/imagenes/sprint-03/06_frontend_vitest_coverage_sprint03.png) y [`07_algorithmic_testbench_cases.png`](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/diseño/imagenes/sprint-03/07_algorithmic_testbench_cases.png).
* **Limitaciones:** La cobertura backend documentada en reportes preliminares (91.83% sobre 1,676 sentencias) se perfeccionó a 92.14% (92.15% en terminal sobre 1,746 sentencias) en la corrida consolidada de auditoría.
* **Estado:** Lista ✅.

---
*Escuela Profesional de Ingeniería de Sistemas — Universidad Privada de Tacna — Octubre 2026*
