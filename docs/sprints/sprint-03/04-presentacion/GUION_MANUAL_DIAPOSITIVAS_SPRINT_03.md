# Guion Manual de Diapositivas, Capturas y Exposición — Sprint 03
**Sistema Web P2P de Mentorías Académicas con Algoritmo de Recomendación para la EPIS-UPT**

---

## 1. Guía de Uso del Documento

Este documento está diseñado para que construyas manualmente tu presentación de 9 diapositivas en PowerPoint sin tener que buscar información dispersa en el repositorio.

Para cada diapositiva encontrarás:
1. **Objetivo pedagógico:** Lo que el docente y el jurado deben comprender en esa lámina.
2. **Contenido textual y tablas:** Listo para copiar y pegar directamente en los cuadros de texto de PowerPoint.
3. **Captura documental obligatoria:** Archivo PNG ya preparado en el repositorio, con su ruta, líneas de origen en SRS/SAD y enlace a GitHub.
4. **Guion oral (Speech):** Redactado en lenguaje natural, conversacional y fluido, colocado inmediatamente debajo de cada elemento visual o textual (tiempo estimado: 40 a 75 segundos por lámina).
5. **Transición:** Frase de enlace con la siguiente diapositiva.
6. **Fuentes de respaldo:** Líneas canónicas y respuestas blindadas ante preguntas difíciles de la cátedra.

*Línea base histórica congelada:* Commit [`7df0a88`](https://github.com/JMedina255/sistema_web_p2p/tree/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0).
*Rama de trabajo:* `docs/sprint-03-presentacion`.

---

## 2. Desarrollo de las 9 Diapositivas

---

### Diapositiva 1 — Presentación del Proyecto y Carátula Oficial

**Objetivo de la diapositiva:**
Presentar al equipo, ubicar el proyecto en el marco académico de la EPIS-UPT y delimitar formalmente que la sustentación corresponde al Sprint 03 sobre la línea base congelada `7df0a88`.

#### A. Contenido que colocaré en PowerPoint

```text
UNIVERSIDAD PRIVADA DE TACNA · FACULTAD DE INGENIERÍA
Escuela Profesional de Ingeniería de Sistemas
Construcción de Software I (Semestre 2026-II)

SISTEMA WEB P2P DE MENTORÍAS ACADÉMICAS CON ALGORITMO DE RECOMENDACIÓN
Sustentación Técnica Oficial — Sprint 03: Publicación de Ofertas de Mentoría

Equipo de Desarrollo (Grupo 03 / C-SharkTeam):
• Joan Cristian Medina Quispe (Código: 2022074255) — Frontend, UI y Accesibilidad
• Renzo Antonio Antayhua Mamani (Código: 2022073504) — Backend, Algoritmos y Datos

Docente de Cátedra: Dr. Ricardo Eduardo Valcárcel Alvarado
Tacna, Octubre 2026
Línea Base Histórica Evaluada: Commit 7df0a88 (Auditado al 100%)
```

#### C. Explicación oral del contenido A (Speech de Apertura)

> «Buenas tardes, Dr. Ricardo Valcárcel y compañeros. A nombre del Grupo 03, conformado por Renzo Antayhua y quien les habla, Joan Medina, presentamos la sustentación técnica del Sprint 03 de nuestro proyecto: el *Sistema Web P2P de Mentorías Académicas para la EPIS-UPT*.
> En este incremento nos enfocamos en el requerimiento principal de publicación de ofertas por parte de los mentores y en la integración preliminar del recomendador académico. Toda nuestra exposición se respalda de forma estricta en la línea base congelada del commit `7df0a88`, garantizando trazabilidad completa entre el SRS, el SAD, el código implementado y el catálogo oficial de pruebas.»

#### E. Transición
> «Iniciaremos revisando la planificación del sprint, el backlog comprometido y cómo gestionamos el esfuerzo de desarrollo.»

#### F. Fuentes de respaldo
* **Repositorio GitHub:** [`https://github.com/JMedina255/sistema_web_p2p`](https://github.com/JMedina255/sistema_web_p2p)
* **Commit Base:** [`7df0a88345a06254940eab8f2d7d8b7f4d33d1e0`](https://github.com/JMedina255/sistema_web_p2p/tree/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0)
* **Documentos Maestros:** [`MAPA_FUENTES_PRESENTACION_SPRINT_03.md`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03/02-trazabilidad/MAPA_FUENTES_PRESENTACION_SPRINT_03.md)

---

### Diapositiva 2 — Objetivos del Sprint y Product Backlog

**Objetivo de la diapositiva:**
Transparentar las tareas comprometidas en el plan original (5 h), justificar técnicamente el incremento a 11 horas-persona ejecutadas y aclarar la colisión del identificador T-18.

#### A. Contenido que colocaré en PowerPoint

**1. Cuadro de Planificación Oficial (Cuadro 4.3):**

| Tarea | Actividad Comprometida | Responsable | Estimación Original | Evidencia Técnica |
| :---: | :--- | :---: | :---: | :--- |
| **T-14** | Desarrollar formulario de publicación de ofertas | Joan | 2.0 h | Frontend React 19 (`OfferPublishView.tsx`) |
| **T-15** | Implementar API básica de gestión de ofertas | Renzo | 2.0 h | Endpoints FastAPI (`/api/v1/offers`) |
| **T-16** | Crear estructura de datos y relaciones de ofertas | Renzo | 1.0 h | Modelo SQLAlchemy + Migración Alembic 003 |

**2. Balance de Esfuerzo y Auditoría Metodológica:**
* **Plan Original:** 5.0 horas-persona (Joan: 2h, Renzo: 3h).
* **Ejecución Real Reportada:** 11.0 horas-persona (+120% de esfuerzo justificado).
  * *Causa Técnica:* Complejidad del selector dinámico de temas silábicos en React (3h), formulación discreta de Jaccard/Dice en backend (4h), restricciones CHECK relacionales en PostgreSQL (2h) y desarrollo del banco algorítmico T-18 (2h).
* **Auditoría de Identificador T-18:** En el plan maestro del Sprint 4, T-18 estaba reservada para Joan (*Integración API Top-k*); en Sprint 3, Renzo reutilizó la etiqueta T-18 para el testbench algorítmico. Se transparenta formalmente en bitácora sin alterar código.

#### B. Captura o diagrama que debo colocar

* **Nombre del recurso:** `D02_BACKLOG_SPRINT03.png`
* **Ruta en repositorio:** `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D02_BACKLOG_SPRINT03.png`
* **Documento formal origen:** `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md`
* **Sección y líneas exactas:** Sección 4.3 «Sprint 3 — Publicación de ofertas», Líneas 152–166
* **Enlace GitHub:** [PLAN_SPRINTS_Y_TAREAS.md#L152-L166](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/PLAN_SPRINTS_Y_TAREAS.md#L152-L166)
* **Instrucciones de inserción:** Colocar a la derecha del cuadro de tareas para respaldar visualmente la fuente original del backlog.

![Captura Backlog Sprint 03](file:///C:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/sprints/sprint-03/05-evidencias/capturas-documentales/D02_BACKLOG_SPRINT03.png)

#### C. Explicación oral del contenido A

> «En el plan maestro del proyecto, el Sprint 03 tenía como objetivo publicar ofertas asociadas a asignaturas y temarios, comprometiendo 5 horas divididas en T-14 para el formulario web, T-15 para la API básica y T-16 para la base de datos.
> Sin embargo, durante la ejecución real reportamos 11 horas. Este incremento del 120% no fue por demoras, sino por valor técnico agregado: Joan necesitó una hora extra para conectar el formulario directamente con las unidades silábicas del catálogo, y Renzo invirtió 6 horas adicionales para adelantar la formulación matemática del recomendador EdRecSys v1.0 y construir un banco de pruebas de rendimiento.»

#### D. Explicación oral del recurso B

> «Como observan en la captura de nuestro plan formal, las tres tareas originales corresponden al PBI PB-009 y al requerimiento RF08. Asimismo, informamos con transparencia que el identificador T-18 aparece duplicado en los informes: originalmente estaba reservado para Joan en el Sprint 4, pero Renzo lo utilizó en este sprint para etiquetar el testbench algorítmico. Esta observación metodológica quedó debidamente documentada en el acta de cierre sin afectar la calidad del software.»

#### E. Transición
> «Revisemos ahora qué requerimientos y reglas de negocio del SRS gobiernan este proceso de publicación.»

#### F. Fuentes de respaldo
* [`docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (L152-L166)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/PLAN_SPRINTS_Y_TAREAS.md#L152-L166)
* [`docs/sprints/sprint-03.md` (L30-L75)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03.md#L30-L75)

---

### Diapositiva 3 — Requerimientos y Reglas de Negocio Institucionales

**Objetivo de la diapositiva:**
Distinguir con claridad qué debe hacer el sistema según los requerimientos del SRS (RF08, RF06, RF09) y cómo condicionan las reglas institucionales (RN-03, RN-04, RN-05) la validez de una oferta.

#### A. Contenido que colocaré en PowerPoint

**1. Matriz de Requerimientos Funcionales (SRS FD03):**
* **RF08 (Principal S3 — MOD-04 L514):** *Publicación de ofertas.* Permitir al mentor programar asesorías en asignaturas críticas aprobadas, seleccionando tema silábico, fecha, horario y modalidad (presencial o virtual).
* **RF06 (Adelanto Técnico — MOD-03 L512):** *Recomendación Top-k.* Inferencia inteligente emparejando necesidades del mentoreado con fortalezas de mentores (prototipo básico EdRecSys v1.0).
* **RF09 (Integración Posterior — MOD-04 L515):** *Infraestructura automatizada.* Sugerencia de aulas EPIS (presencial) o generación de enlaces Google Meet (virtual).

**2. Reglas de Negocio Institucionales Aplicables:**
* **RN-03 (Mérito de Mentor):** Solo postulan estudiantes de ciclos avanzados (VII al X) con asignaturas filtro aprobadas.
* **RN-04 (Antelación Obligatoria):** Publicación obligatoria con más de 24 horas de anticipación ($\Delta t > 24\text{ h}$); estándar institucional recomendado $\ge 48\text{ h}$.
* **RN-05 (Aforo Inmutable):** Capacidad fija por sistema e inalterable por el usuario: **10 cupos en Presencial** (laboratorio EPIS) y **20 cupos en Virtual** (Google Meet).

#### B. Captura o diagrama que debo colocar

* **Recursos visuales preparados:**
  1. `D03_REQUERIMIENTOS_SRS.png` (Extracto Cuadro 5.3 del SRS)
  2. `D03_REGLAS_NEGOCIO_SRS.png` (Extracto Cuadro 5.4 del SRS)
* **Ruta en repositorio:** `docs/sprints/sprint-03/05-evidencias/capturas-documentales/`
* **Documento formal origen:** `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md`
* **Sección y líneas exactas:** Cuadro 5.3 (L505–L516) y Cuadro 5.4 (L545–L556)
* **Enlace GitHub:** [FD03 Líneas 505–556](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L505-L556)
* **Instrucciones de inserción:** Insertar ambas tablas recortadas mostrando los códigos destacados (RF08, RF06, RN-04, RN-05).

![Requerimientos SRS](file:///C:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/sprints/sprint-03/05-evidencias/capturas-documentales/D03_REQUERIMIENTOS_SRS.png)

![Reglas de Negocio SRS](file:///C:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/sprints/sprint-03/05-evidencias/capturas-documentales/D03_REGLAS_NEGOCIO_SRS.png)

#### C. Explicación oral del contenido A

> «Los requerimientos nos indican qué debe construir el equipo. En el Sprint 3 nuestro núcleo fue RF08, perteneciente al módulo MOD-04 de Planificación y Agendamiento, que faculta a los mentores a publicar sesiones en materias filtro. Paralelamente, adelantamos de forma preliminar el requerimiento RF06 del recomendador inteligente para que las ofertas nacieran listas para ser consumidas por los estudiantes de los primeros ciclos.»

#### D. Explicación oral del recurso B

> «En los cuadros oficiales del SRS que observan en pantalla, destacamos tres reglas de negocio vitales: la regla RN-03 exige que el mentor tenga solvencia académica demostrada; la regla RN-04 prohíbe terminantemente publicar sesiones con menos de 24 horas de antelación para proteger el ciclo de confirmación y quórum; y la regla RN-05 fija de forma inmutable el aforo: 10 alumnos para clases presenciales por la capacidad de los laboratorios del pabellón F, y 20 para virtuales en Google Meet.»

#### E. Transición
> «Veamos cómo estos requerimientos se modelaron formalmente mediante diagramas de casos de uso y actividades.»

#### F. Fuentes de respaldo
* [`docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` (L512-L556)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L512-L556)
* Módulo formal en SRS: MOD-04 (L514).

---

### Diapositiva 4 — Modelado Visual: Diagramas de Casos de Uso y Actividades

**Objetivo de la diapositiva:**
Explicar el diagrama de casos de uso de MOD-04 (CUS06), contrastarlo con el flujo de actividades oficial y registrar la discrepancia de nomenclatura CUS06 frente a CUS09 presente en el SRS.

#### A. Contenido que colocaré en PowerPoint

**1. Caso de Uso Canónico CUS06 (MOD-04):**
* **Actor Principal:** Estudiante Mentor (VII a X ciclo, autenticado).
* **Actores Secundarios:** Administrador de Escuela y Sistemas Externos (Google Meet API / Discord).
* **Casos Vinculados en MOD-04:**
  * `CUS06: Publicar Oferta de Mentoría` (Caso central S3).
  * `CUS11: Cargar Cronograma de Horarios Oficiales` (Parser administrativo).
  * `CUS18: Modificar o Cancelar Oferta por Imprevisto` (Gestión de contingencias).

**2. Análisis del Flujo de Actividades y Discrepancia Documental:**
* **Flujo Canónico:** Ingreso de datos $\rightarrow$ Validación de antelación $\Delta t > 24\text{ h}$ (RN-04) $\rightarrow$ Fijación de aforos 10/20 (RN-05) $\rightarrow$ Asignación de aula o enlace Meet $\rightarrow$ Transacción relacional `SesionMentoria` [PUBLICADA] $\rightarrow$ Emisión de código `SES-XXXX`.
* **Auditoría Documental SRS:** En la sección 6.3.2.6 del SRS, el diagrama de actividades de publicación se rotuló históricamente como `CUS09: Publicar Oferta`, mientras que la narrativa formal y la arquitectura utilizan `CUS06`. Se transparenta esta discrepancia editorial entre secciones del SRS sin alterar el documento canónico.

#### B. Captura o diagrama que debo colocar

* **Recursos visuales preparados:**
  1. `D04_CUS06_DIAGRAMA_SRS.png` (Diagrama 6.8: Casos de Uso MOD-04 del SRS)
  2. `D04_CUS06_NARRATIVA_SRS.png` (Ficha técnica y pasos de CUS06)
  3. `D04_FLUJO_ACTIVIDADES_SAD.png` (Diagrama 7.2 To-Be del SAD) o `D04_ACTIVIDADES_CUS09_SRS.png` (Diagrama 6.14.6 del SRS)
* **Ruta en repositorio:** `docs/sprints/sprint-03/05-evidencias/capturas-documentales/`
* **Documento formal origen:** SRS FD03 (L1207–L1241, L1742–L1770, L4487–L4560) y SAD FD04 (L1026–L1075)
* **Enlace GitHub:** [SRS Diagrama 6.8 (L1207)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1207-L1241) · [Narrativa CUS06 (L1742)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1742-L1770)
* **Instrucciones de inserción:** Colocar el Diagrama 6.8 de Casos de Uso a la izquierda y el extracto de la narrativa o flujo a la derecha.

![Diagrama CUS06 SRS](file:///C:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/sprints/sprint-03/05-evidencias/capturas-documentales/D04_CUS06_DIAGRAMA_SRS.png)

![Narrativa CUS06 SRS](file:///C:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/sprints/sprint-03/05-evidencias/capturas-documentales/D04_CUS06_NARRATIVA_SRS.png)

#### C. Explicación oral del contenido A

> «El modelado formal de casos de uso sitúa a CUS06 dentro del módulo MOD-04. El actor primario es el Estudiante Mentor, quien interactúa con el sistema para ofertar su tiempo pedagógico. CUS06 se relaciona con CUS11, que provee las aulas libres procesadas por el parser, y con los sistemas externos de Google Meet o Discord para la generación desatendida de salas de videoconferencia.»

#### D. Explicación oral del recurso B

> «En el Diagrama 6.8 del SRS se observa la frontera del módulo de agendamiento y los tres casos que lo integran. Al contrastar esto con la vista de actividades, identificamos un detalle técnico relevante: en el texto del SRS, el diagrama de actividades de publicación figura con el identificador CUS09 por una bifurcación de redacción temprana, mientras que la ficha canónica y el SAD lo consagran como CUS06. Registramos esta discrepancia documental ante el docente para demostrar el rigor de nuestra auditoría de fuentes.»

#### E. Transición
> «Sinteticemos ahora estos comportamientos bajo la perspectiva ágil de historias de usuario.»

#### F. Fuentes de respaldo
* [`docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` (Diagrama 6.8 L1207-L1241; CUS06 L1742-L1770; Actividades L4487-L4565)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md)
* [`docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md` (Diagrama 7.2 L1026-L1075)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md#L1026-L1075)

---

### Diapositiva 5 — Historias de Usuario (Síntesis Derivada del CUS)

**Objetivo de la diapositiva:**
Presentar los requerimientos bajo el formato ágil de Historias de Usuario, aclarando que corresponden a síntesis derivadas de los casos de uso CUS06 y CUS02 al no existir artefactos HU aislados en el repositorio.

#### A. Contenido que colocaré en PowerPoint

**Nota Metodológica:** En la documentación canónica del proyecto, los requerimientos se gestionaron formalmente mediante PBIs (Product Backlog Items) y especificaciones CUS en SRS. A continuación se presentan las dos Historias de Usuario equivalentes formuladas como síntesis pedagógica:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ HISTORIA HU-01: Publicación de Oferta de Mentoría                      │
│ (Derivada canónica de RF08 / CUS06 · Prioridad: Alta · Sprint 03)       │
├────────────────────────────────────────────────────────────────────────┤
│ ENUNCIADO:                                                             │
│ «Como estudiante mentor acreditado (ciclo VII al X),                   │
│  quiero programar y publicar ofertas de mentoría académica             │
│  especificando asignatura crítica, tema silábico, fecha y modalidad,  │
│  para brindar apoyo académico estructurado a los primeros ciclos.»     │
│                                                                        │
│ CRITERIOS DE ACEPTACIÓN PRINCIPALES:                                   │
│ 1. Selección curricular cerrada contra el catálogo oficial (CUS21).    │
│ 2. Validación estricta de antelación obligatoria superior a 24 horas   │
│    (RN-04); bloqueo y alerta roja si Δt ≤ 24 h.                        │
│ 3. Fijación reactiva e inmutable de aforo según modalidad (RN-05):     │
│    exactamente 10 en Presencial y 20 en Virtual.                       │
│ 4. Persistencia relacional y emisión de código único SES-XXXX.         │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ HISTORIA HU-02: Consulta de Recomendaciones Inteligentes Top-k         │
│ (Derivada preliminar de RF06 / CUS02 · Prototipo Básico EdRecSys v1.0) │
├────────────────────────────────────────────────────────────────────────┤
│ ENUNCIADO:                                                             │
│ «Como estudiante mentoreado (ciclos I al IV),                          │
│  quiero consultar una lista ordenada de mentores y ofertas afines      │
│  según mis dudas conceptuales y disponibilidad horaria,                │
│  para recibir orientación personalizada de forma oportuna.»            │
│                                                                        │
│ CRITERIOS DE ACEPTACIÓN PRINCIPALES:                                   │
│ 1. Emparejamiento multifactorial: afinidad de temas silábicos,        │
│    solapamiento en matriz 6×11 y modalidad pedagógica.                 │
│ 2. Desempate determinista sin caja negra (endpoint /explain).          │
│ 3. Alcance Sprint 3: prototipo algorítmico en backend; integración     │
│    completa de interfaz Top-k programada para el Sprint 04.            │
└────────────────────────────────────────────────────────────────────────┘
```

#### C. Explicación oral de la Historia HU-01

> «La historia HU-01 condensa la necesidad del mentor: necesita una herramienta ágil para ofrecer sus talleres sin temor a equivocarse en la logística. Los cuatro criterios de aceptación aseguran que el mentor no escriba materias arbitrarias, que la fecha respete el corte de 24 horas de la regla RN-04, que el aforo se bloquee en 10 o 20 según la modalidad y que la oferta nazca formalmente con su código SES-XXXX.»

#### D. Explicación oral de la Historia HU-02

> «Por su parte, la historia HU-02 representa el valor para el alumno con dificultades en materias filtro como Cálculo o Algoritmos. Aunque en este Sprint 3 el objetivo troncal era publicar ofertas, Renzo formuló el prototipo EdRecSys v1.0 para que el sistema ya sea capaz de ordenar matemáticamente a los mejores mentores. Aclaramos ante la cátedra que esta historia está satisfecha a nivel algorítmico en el backend, dejando su interfaz definitiva para el Sprint 4.»

#### E. Transición
> «Pasemos a la capa visual: veamos cómo materializamos la historia HU-01 en el frontend con React 19.»

#### F. Fuentes de respaldo
* Derivación de CUS06: [`FD03-EPIS-Informe SRS de Proyecto.md` (L1742-L1770)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1742-L1770)
* Derivación de CUS02: [`FD03-EPIS-Informe SRS de Proyecto.md` (L1610-L1648)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1610-L1648)
* Backlog canónico: `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (PB-009, PB-010).

---

### Diapositiva 6 — Capa de Presentación: Frontend React 19 y Validaciones de Interfaz

**Objetivo de la diapositiva:**
Demostrar el funcionamiento del formulario interactivo `OfferPublishView.tsx`, evidenciar cómo el cliente bloquea infracciones de RN-04 y RN-05 antes de enviar datos y transparentar el uso del modo mock en la SPA local.

#### A. Contenido que colocaré en PowerPoint

**1. Ficha Técnica de la Capa de Presentación (Tarea T-14):**
* **Componente React:** `OfferPublishView.tsx` (1,186 líneas de código TypeScript estructurado en React 19).
* **Consistencia Curricular:** Selector dinámico conectado al catálogo oficial (`PLAN_ESTUDIOS_EPIS_2023`). Al elegir *Cálculo I*, la función `fetchCourseDetail` carga automáticamente sus unidades temáticas oficiales.
* **Blindaje de Concurrencia:** Bloqueo de doble clic mediante la bandera reactiva `isSubmitting`.
* **Pruebas de Componente:** 7 pruebas en Vitest (`OfferPublishView.test.tsx`) evaluando render, aforos, advertencias y reseteo.

**2. Verificación Visual de Reglas en Interfaz:**
* **Infracción RN-04 ($\Delta t \le 24\text{ h}$):** Banner rojo de alerta inmediata, cálculo de horas restantes y botón «Publicar Oferta» deshabilitado.
* **Cumplimiento RN-05 (Aforos Inmutables):** Campo *Aforo Reglamentario* en modo `readOnly`; muestra automáticamente 10 cupos en Presencial y 20 en Virtual.
* **Transparencia Técnica:** La SPA opera localmente con `MockOfferAdapter` (`localStorage`) exhibiendo un banner explícito de modo de prueba, permitiendo validar la interfaz de forma desacoplada de la red.

#### B. Captura o diagrama que debo colocar

* **Recursos visuales preparados:**
  1. `docs/diseño/imagenes/sprint-03/01_offer_publish_form.png` (Captura general del formulario)
  2. `docs/diseño/imagenes/sprint-03/02_advance_time_validation_rn04.png` (Infracción de antelación)
  3. `docs/diseño/imagenes/sprint-03/03_capacity_control_rn05.png` (Control de aforo)
* **Documento formal origen:** Implementación Frontend del Sprint 03
* **Archivos fuente:** `aplicacion/frontend/src/components/OfferPublishView.tsx` (L370–L460) y `src/services/offerService.ts`
* **Enlace GitHub:** [OfferPublishView.tsx](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/OfferPublishView.tsx)
* **Instrucciones de inserción:** Colocar la captura 01 grande al centro-derecha, y las capturas 02 y 03 como evidencias pequeñas de validación debajo.

![Formulario Ofertas](file:///C:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/diseño/imagenes/sprint-03/01_offer_publish_form.png)

#### C. Explicación oral del contenido A

> «En la Diapositiva 6 apreciamos el componente `OfferPublishView.tsx` construido en React 19 y TypeScript. Destaco que el formulario no permite escribir texto libre en las materias: consume las 5 asignaturas oficiales de la escuela y, al hacer clic en una de ellas, el temario silábico se actualiza de manera reactiva. Además, protegemos al usuario de envíos accidentales desactivando el botón de acción mientras la petición se procesa.»

#### D. Explicación oral del recurso B

> «En las capturas de pantalla reales que incluimos, pueden verificar cómo la interfaz protege las reglas de negocio: a la izquierda, si el mentor intenta agendar con 4.5 horas de antelación, salta un banner rojo indicando la infracción de la regla RN-04 y el botón queda inactivo. A la derecha, el campo de aforo es de solo lectura y conmuta entre 10 y 20 según la modalidad. Aclaramos que la vista cuenta con un banner azul que transparenta que opera sobre un adaptador mock local para garantizar su ejecución en cualquier estación de trabajo sin depender del despliegue en la nube.»

#### E. Transición
> «Veamos ahora cómo el backend recibe, valida y persiste estas ofertas mediante la arquitectura del SAD.»

#### F. Fuentes de respaldo
* [`aplicacion/frontend/src/components/OfferPublishView.tsx`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/OfferPublishView.tsx)
* [`aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx` (7 tests)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx)
* [`aplicacion/frontend/src/services/offerService.ts` (L71-L183)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/frontend/src/services/offerService.ts)

---

### Diapositiva 7 — Backend de Ofertas y Arquitectura Técnica SAD

**Objetivo de la diapositiva:**
Explicar el flujo multicapa del backend FastAPI, el modelo relacional con restricciones CHECK, el mecanismo de fallback en memoria y el papel adelantado del prototipo EdRecSys v1.0.

#### A. Contenido que colocaré en PowerPoint

**1. Arquitectura Multicapa en 4 Niveles (SAD FD04):**
$$\text{UI React (OfferPublishView)} \longrightarrow \text{Router FastAPI (/api/v1/offers)} \longrightarrow \text{Dominio (OfferService)} \longrightarrow \text{Base de Datos (PostgreSQL)}$$

**2. Componentes de Backend Implementados (Tareas T-15 y T-16):**
* **Endpoints REST:** `POST /api/v1/offers` (publicación con validación de mérito y emisión SES-XXXX) y `GET /api/v1/offers` (catálogo activo filtrable por materia, modalidad y mentor).
* **Entidad Relacional:** `sesiones_mentoria` creada en migración Alembic `003_mentoring_offers.py`.
* **Restricciones CHECK en PostgreSQL:** Blindaje de base de datos con `CHECK (aforo_maximo IN (10, 20))` y `CHECK (modalidad IN ('PRESENCIAL', 'VIRTUAL'))`.
* **Fallback en Memoria:** Si PostgreSQL pierde conectividad, `offer_service.py` (L260–L263) captura el fallo con `db.rollback()`, almacena provisionalmente en `_offers_in_memory` y retorna HTTP 201 Created.
* **Nota Técnica sobre EdRecSys:** El backend incorpora en `recommendation_service.py` el prototipo básico del recomendador Top-k (adelanto respecto a la planificación del Sprint 4). El ordenamiento se ejecuta mediante Timsort completo ($O(N \log N)$) en L489 y L594.

#### B. Captura o diagrama que debo colocar

* **Recurso visual preparado:** `D07_ARQUITECTURA_SAD.png`
* **Ruta en repositorio:** `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D07_ARQUITECTURA_SAD.png` (idéntico a `docs/diseño/imagenes/sprint-03/08_secuencia_tecnica_publicacion_ofertas.png`)
* **Documento formal origen:** `docs/diseño/TRAZABILIDAD_PUBLICACION_OFERTAS.md`
* **Sección y líneas exactas:** Sección 3.2 «Diagrama de Secuencia Técnica», Líneas 25–95 (código PlantUML oficial)
* **Enlace GitHub:** [TRAZABILIDAD_PUBLICACION_OFERTAS.md#L25-L95](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/TRAZABILIDAD_PUBLICACION_OFERTAS.md#L25-L95)
* **Instrucciones de inserción:** Insertar el diagrama ocupando el lado derecho de la lámina para evidenciar la interacción entre componentes.

![Secuencia Técnica SAD](file:///C:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/sprints/sprint-03/05-evidencias/capturas-documentales/D07_ARQUITECTURA_SAD.png)

#### C. Explicación oral del contenido A

> «En el backend implementamos una arquitectura desacoplada en cuatro niveles. Diseñamos dos endpoints en FastAPI: uno para recibir el formulario y validar la sesión, y otro para consultar las ofertas activas. La tabla `sesiones_mentoria` está protegida en PostgreSQL mediante restricciones CHECK que impiden guardar aforos que no sean exactamente 10 o 20. Además, el servicio cuenta con un mecanismo de resiliencia: si la base de datos no responde, hace rollback y almacena en memoria para no interrumpir el flujo demostrativo.»

#### D. Explicación oral del recurso B

> «El diagrama de secuencia técnica que ven en pantalla muestra con exactitud el ciclo de vida de una petición: el frontend despacha el payload tipado, el router FastAPI valida la cabecera y delega a `OfferService`, el cual evalúa el mérito del mentor y la antelación horaria antes de insertar la tupla relacional. Asimismo, destacamos que en esta misma capa dejamos operando el prototipo preliminar del recomendador EdRecSys v1.0, el cual utiliza ordenamiento completo de candidatos antes de extraer el Top-k, quedando preparado para conectarse con la interfaz de usuario en el Sprint 4.»

#### E. Transición
> «Comprobemos ahora cómo este diseño se valida formalmente frente al catálogo de pruebas y la batería automatizada.»

#### F. Fuentes de respaldo
* [`aplicacion/backend/app/api/v1/endpoints/offers.py`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/api/v1/endpoints/offers.py)
* [`aplicacion/backend/app/services/offer_service.py` (L260-L263 fallback)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/services/offer_service.py#L260-L263)
* [`aplicacion/backend/app/models/offer.py` (Modelo SesionMentoria)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/models/offer.py)
* [`aplicacion/backend/app/db/migrations/versions/003_mentoring_offers.py`](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/app/db/migrations/versions/003_mentoring_offers.py)

---

### Diapositiva 8 — Verificación y Pruebas: Homologación con el Catálogo Excel

**Objetivo de la diapositiva:**
Homologar los casos del catálogo oficial de pruebas en Excel con las pruebas automatizadas reales en Vitest y Pytest, distinguiendo escenarios aprobados de integraciones diferidas.

#### A. Contenido que colocaré en PowerPoint

**1. Matriz de Homologación de Escenarios Críticos:**

| Caso Catálogo | Escenario Verificado | Suite de Prueba Concreta | Líneas | Resultado Auditado |
| :---: | :--- | :--- | :---: | :---: |
| **CUS06-U01** | Formulario válido y campos requeridos | `offerService.test.ts` / `test_offers.py` | L22 / L334 | <span class="badge badge-success">✅ Verificado (Pass)</span> |
| **CUS06-U01** | Infracción temporal de antelación (RN-04) | `offerService.test.ts` (`calculateAdvanceHours`) | L65–L90 | <span class="badge badge-success">✅ Verificado (Pass)</span> |
| **CUS06-U02** | Aforos automáticos inmutables (RN-05) | `OfferPublishView.test.tsx` / `test_offers.py` | L100 / L153 | <span class="badge badge-success">✅ Verificado (Pass)</span> |
| **CUS06-U03** | Parser de aulas libres EPIS (presencial) | *Integración diferida ('Posterior' en Backlog)* | — | <span class="badge badge-warning">⌛ Pendiente (S4)</span> |
| **CUS06-U04** | Aprovisionamiento OAuth Google Meet | *Integración diferida ('Posterior' en PB-034)* | — | <span class="badge badge-warning">⌛ Pendiente (S4)</span> |
| **CUS02-U01..04** | Similitud Jaccard, matrices y desempate | `test_recommendations.py` (19 pruebas) | L31–L95 | <span class="badge badge-success">✅ Verificado (Pass)</span> |
| **CUS02-A01** | Latencia algorítmica y casos frontera | `test_simulation.py` (testbench T-18) | L67–L82 | <span class="badge badge-success">✅ Verificado (0.86 ms)</span> |

**2. Balance Métrico de Calidad:**
* **59 Pruebas Específicas del Sprint 3:** 21 en Frontend (7 en vista, 14 en servicio) y 38 en Backend (14 en ofertas, 19 en recomendaciones, 5 en simulación).
* **209 Tests Totales Consolidados:** 150 pruebas de regresión previas (S1-S2) + 59 nuevas (100% passed).
* **Coberturas Independientes:** Vitest Frontend **92.52%** | Pytest Backend **92.14%** (superando el umbral del 70% de RNF09).

#### B. Captura o diagrama que debo colocar

* **Recursos visuales preparados:**
  1. `D08_CATALOGO_PRUEBAS_CUS06.png` (Filas 41 a 48 del Excel)
  2. `D08_CATALOGO_PRUEBAS_CUS02.png` (Filas 14 a 21 del Excel)
  3. `docs/diseño/imagenes/sprint-03/05_backend_pytest_coverage_sprint03.png` (Cobertura Pytest)
* **Ruta en repositorio:** `docs/sprints/sprint-03/05-evidencias/capturas-documentales/`
* **Documento formal origen:** `docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` (Hoja 1)
* **Sección y celdas exactas:** CUS06 (`A41:O48`) y CUS02 (`A14:O21`)
* **Instrucciones de inserción:** Insertar el extracto del catálogo Excel arriba y las métricas de cobertura abajo.

![Catálogo CUS06](file:///C:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/sprints/sprint-03/05-evidencias/capturas-documentales/D08_CATALOGO_PRUEBAS_CUS06.png)

![Catálogo CUS02](file:///C:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/sprints/sprint-03/05-evidencias/capturas-documentales/D08_CATALOGO_PRUEBAS_CUS02.png)

#### C. Explicación oral del contenido A

> «Para responder a las exigencias de calidad, homologamos directamente las pruebas contra el archivo Excel del catálogo oficial. Como ven en la tabla, validamos los campos obligatorios, la antelación de 24 horas y los límites de aforo en suites independientes tanto de frontend como de backend. Transparentamos que los casos U03 de lectura de PDF y U04 de conexión en vivo con Google Meet quedaron catalogados como integraciones posteriores en el Product Backlog.»

#### D. Explicación oral del recurso B

> «En las capturas del catálogo de pruebas que proyectamos, se evidencia la trazabilidad hacia nuestras 59 pruebas nuevas del Sprint 3, las cuales sumadas a las 150 de regresión consolidan 209 pruebas aprobadas al 100%. En el backend alcanzamos un 92.14% de cobertura en Pytest y en el frontend un 92.52% en Vitest, superando con creces la cota del 70% fijada en RNF09 y garantizando que el sistema no presente roturas.»

#### E. Transición
> «Para concluir, evaluemos con honestidad técnica el cumplimiento del Definition of Done y los pasos hacia el Sprint 04.»

#### F. Fuentes de respaldo
* [`docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` (A14:O21 y A41:O48)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx)
* [`aplicacion/backend/tests/test_offers.py` (14 tests)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_offers.py)
* [`aplicacion/backend/tests/test_recommendations.py` (19 tests)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_recommendations.py)
* [`aplicacion/backend/tests/test_simulation.py` (5 tests)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/aplicacion/backend/tests/test_simulation.py)

---

### Diapositiva 9 — Conclusiones, Evaluación del DoD y Habilitación del Sprint 04

**Objetivo de la diapositiva:**
Cerrar la sustentación con un balance objetivo: detallar los 10 criterios satisfechos del DoD, reconocer las 2 limitaciones pendientes declaradas y explicar cómo se habilita el Sprint 04 para reservas concurrentes con bloqueo pesimista.

#### A. Contenido que colocaré en PowerPoint

**1. Avances Técnicos Consolidados (Sprint 03):**
* Formulario reactivo de publicación con consistencia silábica (T-14 / RF08).
* API REST y persistencia relacional con restricciones CHECK en PostgreSQL (T-15, T-16).
* Prototipo algorítmico básico EdRecSys v1.0 con ponderación multidimensional (RF06).
* Batería automatizada de 209 pruebas con coberturas independientes superiores al 92%.

**2. Evaluación de Cumplimiento del Definition of Done (DoD):**
* **Criterios Satisfechos y Aprobados (10/12):** Funcionalidad RF08 operativa, aforos inmutables blindados (RN-05), antelación validada (RN-04), contratos tipados OpenAPI, 0 advertencias de linteo estático, pruebas unitarias aprobadas y cobertura >70% superada.
* **Criterios Pendientes y Brechas Declaradas (2/12):**
  1. *Persistencia Real por Defecto en UI:* La SPA opera con adaptador mock para testing desacoplado; en Sprint 4 se conectará directamente a los endpoints de PostgreSQL.
  2. *Seguridad JWT Estricta:* Formalizar la cabecera `Authorization` obligatoria en producción y aprovisionamiento Google Meet (PB-034).

**3. Habilitación Estratégica para el Sprint 04:**
* Con las ofertas registradas en catálogo y el recomendador calibrado, la plataforma queda en un estado óptimo para abordar el **Sprint 04**: Reservas transaccionales ACID con control de sobrecupo mediante bloqueo pesimista (`SELECT ... FOR UPDATE` en `RF12` / `CUS04`) e interfaz de usuario para recomendaciones Top-k.

#### C. Explicación oral del Bloque 1 y 2 (Avances y DoD)

> «Para concluir, el balance del Sprint 03 es altamente positivo pero evaluado con rigor técnico: implementamos el ciclo completo de ofertas, blindamos las reglas de aforo y antelación, y adelantamos el recomendador básico. En nuestra evaluación del Definition of Done declaramos 10 criterios plenamente satisfechos y transparentamos dos pendientes: conectar la interfaz directamente a PostgreSQL por defecto y exigir el token de autenticación de forma obligatoria en la API de producción.»

#### D. Explicación oral del Bloque 3 (Cierre y Sprint 04)

> «Este incremento deja la mesa servida para el Sprint 04: al tener las ofertas publicadas y tipadas en base de datos, el equipo podrá implementar con total seguridad las reservas de cupo mediante transacciones ACID y bloqueo pesimista en PostgreSQL para evitar el sobrecupo. Agradecemos su atención y quedamos a disposición del Dr. Valcárcel para la ronda de preguntas.»

#### F. Fuentes de respaldo
* [`G03_EPIS_Informe_Sprint_03.md` (L109-L125 y L363-L389)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/sprint-03/01-informes/G03_EPIS_Informe_Sprint_03.md)
* Backlog Sprint 4: [`PLAN_SPRINTS_Y_TAREAS.md` (L168-L185)](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/PLAN_SPRINTS_Y_TAREAS.md#L168-L185)

---

## 3. Índice de Capturas, Diagramas y Referencias de Fuentes

La siguiente tabla resume todos los recursos visuales preparados y disponibles para la construcción manual en PowerPoint:

| Diapositiva | Nombre del Archivo PNG | Documento de Origen | Sección y Líneas / Celdas | Ruta Relativa del Archivo | Estado en Repositorio | Enlace GitHub (Commit 7df0a88) |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **D-02** | `D02_BACKLOG_SPRINT03.png` | `PLAN_SPRINTS_Y_TAREAS.md` | Sección 4.3 (L152–L166) | `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D02_BACKLOG_SPRINT03.png` | ✅ Generado | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/sprints/PLAN_SPRINTS_Y_TAREAS.md#L152-L166) |
| **D-03** | `D03_REQUERIMIENTOS_SRS.png` | `FD03-EPIS-Informe SRS de Proyecto.md` | Cuadro 5.3 (L505–L516) | `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D03_REQUERIMIENTOS_SRS.png` | ✅ Generado | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L505-L516) |
| **D-03** | `D03_REGLAS_NEGOCIO_SRS.png` | `FD03-EPIS-Informe SRS de Proyecto.md` | Cuadro 5.4 (L545–L556) | `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D03_REGLAS_NEGOCIO_SRS.png` | ✅ Generado | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L545-L556) |
| **D-04** | `D04_CUS06_DIAGRAMA_SRS.png` | `FD03-EPIS-Informe SRS de Proyecto.md` | Diagrama 6.8 (L1207–L1241) | `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D04_CUS06_DIAGRAMA_SRS.png` | ✅ Generado | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1207-L1241) |
| **D-04** | `D04_CUS06_NARRATIVA_SRS.png` | `FD03-EPIS-Informe SRS de Proyecto.md` | Sección 6.2 (L1742–L1770) | `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D04_CUS06_NARRATIVA_SRS.png` | ✅ Generado | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1742-L1770) |
| **D-04** | `D04_FLUJO_ACTIVIDADES_SAD.png` | `FD04-EPIS-Informe SAD de Proyecto.md` | Diagrama 7.2 (L1026–L1075) | `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D04_FLUJO_ACTIVIDADES_SAD.png` | ✅ Generado | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md#L1026-L1075) |
| **D-04** | `D04_ACTIVIDADES_CUS09_SRS.png` | `FD03-EPIS-Informe SRS de Proyecto.md` | Diagrama 6.14.6 (L4487–L4560) | `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D04_ACTIVIDADES_CUS09_SRS.png` | ✅ Generado | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L4487-L4560) |
| **D-04** | `D04_CUS02_DIAGRAMA_SRS.png` | `FD03-EPIS-Informe SRS de Proyecto.md` | Diagrama 6.7 (L1169–L1199) | `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D04_CUS02_DIAGRAMA_SRS.png` | ✅ Generado | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#L1169-L1199) |
| **D-05** | *N/A (Síntesis Pedagógica)* | SRS FD03 / Backlog | Derivada de CUS06 y CUS02 | *No requiere PNG (Tablas de texto puro)* | ℹ️ Sin archivo | Formato visual en tarjetas |
| **D-06** | `01_offer_publish_form.png` | Interfaz Real SPA | Componente `OfferPublishView` | `docs/diseño/imagenes/sprint-03/01_offer_publish_form.png` | ✅ Existente | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/imagenes/sprint-03/01_offer_publish_form.png) |
| **D-06** | `02_advance_time_validation_rn04.png` | Interfaz Real SPA | Infracción RN-04 | `docs/diseño/imagenes/sprint-03/02_advance_time_validation_rn04.png` | ✅ Existente | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/imagenes/sprint-03/02_advance_time_validation_rn04.png) |
| **D-06** | `03_capacity_control_rn05.png` | Interfaz Real SPA | Aforo inmutable RN-05 | `docs/diseño/imagenes/sprint-03/03_capacity_control_rn05.png` | ✅ Existente | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/imagenes/sprint-03/03_capacity_control_rn05.png) |
| **D-07** | `D07_ARQUITECTURA_SAD.png` | `TRAZABILIDAD_PUBLICACION_OFERTAS.md` | Secuencia SAD (L25–L95) | `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D07_ARQUITECTURA_SAD.png` | ✅ Generado | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/TRAZABILIDAD_PUBLICACION_OFERTAS.md#L25-L95) |
| **D-08** | `D08_CATALOGO_PRUEBAS_CUS06.png` | `Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` | Hoja 1, Filas 41 a 48 (`A41:O48`) | `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D08_CATALOGO_PRUEBAS_CUS06.png` | ✅ Generado | [Ver Excel en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx) |
| **D-08** | `D08_CATALOGO_PRUEBAS_CUS02.png` | `Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` | Hoja 1, Filas 14 a 21 (`A14:O21`) | `docs/sprints/sprint-03/05-evidencias/capturas-documentales/D08_CATALOGO_PRUEBAS_CUS02.png` | ✅ Generado | [Ver Excel en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx) |
| **D-08** | `05_backend_pytest_coverage_sprint03.png` | Ejecución Pytest | Terminal de cobertura 92.14% | `docs/diseño/imagenes/sprint-03/05_backend_pytest_coverage_sprint03.png` | ✅ Existente | [Ver en GitHub](https://github.com/JMedina255/sistema_web_p2p/blob/7df0a88345a06254940eab8f2d7d8b7f4d33d1e0/docs/dise%C3%B1o/imagenes/sprint-03/05_backend_pytest_coverage_sprint03.png) |

---

## 4. Recursos no Localizados o Pendientes de Captura Manual

Para garantizar transparencia total, se informa la situación de los recursos que no proceden de capturas automáticas:

1. **`D05_HISTORIAS_USUARIO_FUENTE.png`:**
   * **Situación:** En el repositorio formal no existen documentos ni hojas de cálculo que contengan tarjetas de historias de usuario bajo el formato «Como... Quiero... Para...». El proyecto se gestionó formalmente mediante **Product Backlog Items (PBI)** y **Casos de Uso (CUS)** en el SRS.
   * **Recomendación para PowerPoint:** No crear una captura ficticia. En su lugar, copiar directamente las dos tarjetas en texto formateado de la Diapositiva 5, explicando oralmente que son derivaciones pedagógicas de CUS06 y CUS02.

2. **Captura en Vivo de Swagger UI (`/docs`):**
   * Si deseas mostrar Swagger en vivo en la Diapositiva 7 u 8, ya existe la imagen de respaldo oficial en `docs/diseño/imagenes/sprint-03/04_swagger_api_docs_sprint03.png`, por lo que no requieres realizar capturas manuales de última hora.

---
*Documento maestro generado conforme a los estándares de auditoría documental EPIS-UPT — Octubre 2026*
