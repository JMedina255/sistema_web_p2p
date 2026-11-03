# Guion Maestro de Presentación en Canva — Sprint 04

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre Académico 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam  
* Joan Cristian Medina Quispe (Código: 2022074255) — Frontend & UI Architecture  
* Renzo Antonio Antayhua Mamani (Código: 2022073504) — Backend, Database & Algorithmic Design  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Ubicación Canónica:** `docs/presentaciones/sprint-04/PRESENTACION_SPRINT_04.md`  
**Guion Oral Completo:** [`GUION_EXPOSICION_SPRINT_04.md`](GUION_EXPOSICION_SPRINT_04.md)  
**Catálogo de Evidencias:** [`MATRIZ_EVIDENCIAS_SPRINT_04.md`](MATRIZ_EVIDENCIAS_SPRINT_04.md)  
**Línea Base en Git:** Commit `8bd6583` / `7813a6f` en rama `main`  
**Formato de Diapositivas:** Panorámico 16:9 | Paleta Oficial: Azul Marino (`#1C2A59`), Dorado Académico (`#B99451`) y Blanco (`#FFFFFF`).  

---

## Índice Estructurado de la Sustentación (12 Diapositivas)

```text
[I. Marco Institucional y Planificación del Incremento]
  ├── Diapositiva 01: Portada Institucional y Auditoría de Línea Base
  ├── Diapositiva 02: Objetivo y Alcance del Sprint 04 (Plan vs Real)
  └── Diapositiva 03: Planificación y Distribución Operativa de Tareas (T-17 a T-24)

[II. Inteligencia de Recomendación Personalizada (EdRecSys v1.0)]
  ├── Diapositiva 04: Algoritmo de Recomendación Top-k Multifactorial
  ├── Diapositiva 05: Ponderación Curricular EPIS y Desempate Determinista
  └── Diapositiva 06: Banco de Pruebas del Recomendador y Casos Frontera

[III. Sistema de Reservas Transaccionales y Control de Aforo]
  ├── Diapositiva 07: Arquitectura del Flujo de Reserva y Modal Reactivo
  ├── Diapositiva 08: Control de Aforo y Concurrencia con Bloqueo Pesimista (SELECT FOR UPDATE)
  ├── Diapositiva 09: Modelo Relacional reservas_cupo y Máquina de Estados
  └── Diapositiva 10: Contratos API REST, Reglas de Negocio y Corte de Quórum a T-24h

[IV. Calidad de Software, Verificación y Continuidad]
  ├── Diapositiva 11: Aseguramiento de Calidad: 245 Tests, Cobertura >91% y Cierre DoD
  └── Diapositiva 12: Conclusiones, Logros Verificados y Transición al Sprint 05
```

---

## Desarrollo Detallado Diapositiva por Diapositiva (Contenido para Canva)

---

### Diapositiva 01: Portada Institucional y Auditoría de Línea Base

* **Título:** Sistema Web P2P de Mentorías Académicas — EPIS UPT
* **Subtítulo:** Sustentación de Ingeniería de Software — Incremento Técnico del Sprint 04
* **Objetivo Comunicativo:** Contextualizar formalmente la entrega académica frente al jurado docente, acreditando la autoría técnica, la institución y la inmutabilidad de la línea base en Git.
* **Expositor Responsable:** Presentación Conjunta (Joan Medina y Renzo Antayhua).
* **Tiempo Sugerido:** 1 minuto 15 segundos.

#### Contenido Resumido para Canva
* **Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — EPIS
* **Asignatura:** Construcción de Software I — Semestre 2026-II
* **Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado
* **Equipo Consultor (Grupo 03 / C-SharkTeam):**
  * Joan Cristian Medina Quispe (2022074255) — Frontend & UI Architecture
  * Renzo Antonio Antayhua Mamani (2022073504) — Backend, Database & Algorithmic Design
* **Datos de Auditoría Técnica:**
  * Rama de Trabajo: `main` (Merge Pull Request #5)
  * Commit Base Auditado: `8bd6583db3` (Backend) / `7813a6f30d` (Frontend)
  * Estado de Suite: **245 / 245 Tests Aprobados (100%)** | Cobertura: **91.22% Backend / 92.56% Frontend**

#### Indicaciones de Imágenes y Recursos Visuales
* **Recursos Gráficos:**
  * Logotipo oficial vectorizado de la Universidad Privada de Tacna y la EPIS.
  * Badge de Calidad: `245 TESTS PASSED | COBERTURA >91% | CERO DEFECTOS RUFF/ESLINT`.
* **Distribución Visual en Canva:** Fondo azul marino institucional (`#1C2A59`), tipografía sans-serif blanca y dorada (`#B99451`). Encabezado con datos del curso y fecha. Dos tarjetas centrales para los perfiles de los expositores y barra inferior con los datos de auditoría Git.

#### Guion Oral Resumido
> **Joan:** «Buenas tardes Dr. Ricardo Valcárcel y miembros de la cátedra. A nombre del Grupo 03 (C-SharkTeam), integrado por Renzo Antayhua y quien les habla, Joan Medina, presentamos la sustentación formal del Sprint 04 para el Sistema Web P2P de Mentorías Académicas de la EPIS-UPT.»  
> **Renzo:** «En este sprint resolvemos el desafío central del sistema: conectar el motor inteligente de recomendaciones Top-k con la reserva transaccional de vacantes bajo riguroso control de aforo inmutable y concurrencia pesimista ACID. Toda la evidencia que expondremos hoy se encuentra plenamente implementada, probada y congelada en nuestro repositorio oficial.»

---

### Diapositiva 02: Objetivo y Alcance del Sprint 04 (Plan vs Real)

* **Título:** Visión Operativa del Sprint 04: Alcance Planificado frente a Ejecutado
* **Subtítulo:** Conexión de Inteligencia Algorítmica con Interacción Transaccional de Usuarios
* **Objetivo Comunicativo:** Transparentar el cumplimiento riguroso de las 15.0 horas programadas, los PBI atendidos y los requerimientos funcionales y no funcionales homologados.
* **Expositor Responsable:** Renzo Antayhua.
* **Tiempo Sugerido:** 1 minuto 30 segundos.

#### Contenido Resumido para Canva
* **Propósito del Incremento:** Permitir que los estudiantes mentoreados exploren recomendaciones de tutorías personalizadas (*Top-k*) y formalicen reservas de vacantes en tiempo real con cero sobrecupo.
* **Product Backlog Items (PBI) Atendidos (100% Culminados):**
  * `PB-010`: Motor de recomendación Top-k multifactorial con ponderación curricular.
  * `PB-011`: Feed interactivo de recomendaciones con explicabilidad (XAI) y solicitudes por demanda.
  * `PB-013`: Reserva transaccional atómica con prevención de sobrecupo y bloqueo pesimista.
  * `PB-014`: Protocolo automático de corte y evaluación de quórum a $T-24\text{ h}$.
* **Requisitos Trazados:** RF06, RF07, RF12, RF13, RF15, RF16, RF24 | RNF03 (< 50 ms), RNF07 (0% sobrecupo), RNF09 (Cobertura $\ge 70\%$).
* **Reglas de Negocio Incorporadas:** RN-02 (Consentimiento Ley 29733), RN-04 (Antelación > 24h), RN-05 (Aforos 10/20), RN-08 (Ratificación a T-24h), RN-09 (Quórum 50%), RN-11 (Multiplicadores 1.0x–1.3x).

#### Indicaciones de Imágenes y Recursos Visuales
* **Imagen Principal:** `diagramas/arquitectura_sprint04.png`
* **Pie de Imagen:** *Diagrama 3.1: Arquitectura y Despliegue Físico Multi-Capa — Sprint 04 (EPIS-UPT).*
* **Distribución Visual en Canva:** División 50/50. En el panel izquierdo: 4 tarjetas con los PBIs atendidos y métricas de esfuerzo (15.0 h planificadas vs 15.0 h ejecutadas). En el panel derecho: el diagrama de arquitectura física destacando los tres nodos (React 19 SPA, FastAPI ASGI y Supabase PostgreSQL con Alembic 004).

#### Guion Oral Resumido
> **Renzo:** «Para el Sprint 04 planificamos 15 horas de ingeniería distribuidas equitativamente. Atendimos cuatro ítems del Backlog que abarcan desde el cálculo del ranking Top-k hasta el agendamiento transaccional ACID. Como observamos en el diagrama de arquitectura, el sistema opera de forma desacoplada: el frontend React consume endpoints REST tipados bajo JWT, mientras que el backend coordina transacciones con candado pesimista sobre PostgreSQL en Supabase, garantizando que jamás se asigne un cupo de más.»

---

### Diapositiva 03: Planificación y Distribución Operativa de Tareas (T-17 a T-24)

* **Título:** Estructura de Trabajo y Matriz Operativa de Tareas
* **Subtítulo:** Asignación Equitativa de Responsabilidades y Cadena de Valor (15.0 Horas-Persona)
* **Objetivo Comunicativo:** Detallar cómo se articularon las 8 tareas técnicas del sprint entre frontend y backend, evidenciando la trazabilidad hacia el plan Scrum institucional.
* **Expositor Responsable:** Joan Medina.
* **Tiempo Sugerido:** 1 minuto 15 segundos.

#### Contenido Resumido para Canva
* **Distribución Balanceada de Carga:** 7.5 horas Joan Medina | 7.5 horas Renzo Antayhua.
* **Desglose de Tareas Técnicas:**
  * `T-17` (Renzo / 3.0 h): Consolidación del motor Top-k, multiplicadores curriculares y desempate en `RecommendationService`. ✅
  * `T-18` (Joan / 2.0 h): Cliente de servicio tipado `recommendationService.ts` y adaptadores de red. ✅
  * `T-19` (Ambos / 1.0 h): Banco de pruebas deterministas de ordenamiento y empates (Pytest y Vitest). ✅
  * `T-20` (Joan / 2.0 h): Componente `RecommendationFeedView.tsx` con explicabilidad XAI y panel empty-state. ✅
  * `T-21` (Joan / 2.0 h): Modal reactivo `BookingModalView.tsx` con advertencias reglamentarias y aforo. ✅
  * `T-22` (Renzo / 2.0 h): Modelo relacional `ReservaCupo`, migración Alembic 004 y endpoints REST `/api/v1/bookings`. ✅
  * `T-23` (Joan / 1.0 h): Integración cliente `bookingService.ts` con modal y navegación en `App.tsx`. ✅
  * `T-24` (Renzo / 2.0 h): Coordinador transaccional ACID con `SELECT ... FOR UPDATE` y suite multihilo RNF07. ✅

#### Indicaciones de Imágenes y Recursos Visuales
* **Recurso Visual:** Tabla comparativa formal de tareas con códigos de color de estado (Verde = Implementado y Verificado).
* **Distribución Visual en Canva:** Diseño de matriz en cuadrícula de dos columnas: columna izquierda para tareas de Joan (Frontend / UI / T-18, T-20, T-21, T-23) con acento dorado; columna derecha para tareas de Renzo (Backend / Persistencia / T-17, T-22, T-24) con acento azul marino; centro para T-19 (Verificación compartida).

#### Guion Oral Resumido
> **Joan:** «La planificación de este sprint fue estrictamente modular. En frontend asumí el desarrollo de la experiencia de usuario: el feed de recomendaciones, el acordeón de explicabilidad algorítmica y el modal interactivo de reservas. Renzo asumió la robustez de los algoritmos y la persistencia relacional con control de concurrencia. La tarea T-19 representó el punto de encuentro: verificamos conjuntamente que el orden devuelto por el algoritmo en backend se reflejara con idéntico determinismo en la pantalla del estudiante.»

---

### Diapositiva 04: Algoritmo de Recomendación Top-k Multifactorial (EdRecSys v1.0)

* **Título:** Inteligencia de Recomendación: Motor EdRecSys v1.0
* **Subtítulo:** Formulación Matemática, Ponderación de Factores y Transparencia Explicable (XAI)
* **Objetivo Comunicativo:** Explicar la formulación matemática de la función de afinidad, justificando los pesos asignados a cada factor y la explicabilidad provista al usuario mentoreado.
* **Expositor Responsable:** Renzo Antayhua.
* **Tiempo Sugerido:** 1 minuto 45 segundos.

#### Contenido Resumido para Canva
* **Función de Afinidad Multifactorial ($S_{\text{total}}$):**
  $$S_{\text{total}} = (0.40 S_{\text{tema}} + 0.35 S_{\text{horario}} + 0.15 S_{\text{modalidad}} + 0.10 S_{\text{curricular}}) \times W_{\text{curso}}$$
* **Componentes del Scoring:**
  * **Similitud Temática Silábica ($40\%$):** Coeficiente de Jaccard/Dice comparando los temas de dificultad del mentoreado frente a los contenidos oficiales de la oferta.
  * **Compatibilidad Horaria ($35\%$):** Solapamiento directo sobre la matriz semanal 6×11 de disponibilidad.
  * **Concordancia de Modalidad ($15\%$):** 100% presencial/virtual coincidente, 90% híbrida, 20% divergente.
  * **Afinidad Curricular ($10\%$):** Concordancia de área formativa y semestre lectivo.
* **Explicabilidad Algorítmica (Explainable AI - XAI):**
  * La interfaz no oculta el cálculo: cada tarjeta muestra una barra de progreso y permite desglosar el porcentaje exacto de cada dimensión.

#### Indicaciones de Imágenes y Recursos Visuales
* **Imagen Principal 1:** `diagramas/flujo_recomendacion.png`
* **Imagen Secundaria 2:** `evidencias/frontend/01_recommendation_feed_topk.png`
* **Distribución Visual en Canva:** Panel izquierdo: el diagrama de flujo del pipeline EdRecSys v1.0 mostrando el paso de los filtros previos al scoring. Panel derecho: captura real del Feed interactivo donde se aprecia la barra de afinidad al 98.4% y el acordeón XAI expandido con los porcentajes matemáticos.

#### Guion Oral Resumido
> **Renzo:** «El motor EdRecSys v1.0 no es una caja negra. Como exige el marco académico de la UPT, implementamos un modelo de inferencia híbrido y transparente. La afinidad combina cuatro dimensiones críticas: la coincidencia temático-silábica con un 40% de peso, el cruce horario en la grilla semanal con 35%, la modalidad con 15% y la afinidad curricular con 10%. Este puntaje base es posteriormente multiplicado por el factor de criticidad de la asignatura y expuesto al alumno de manera transparente mediante tarjetas XAI.»

---

### Diapositiva 05: Ponderación Curricular EPIS y Desempate Determinista

* **Título:** Ponderación de Materias Críticas y Criterio Determinista
* **Subtítulo:** Multiplicadores Institucionales EPIS (RN-11) y Clave Quíntuple sin Aleatoriedad
* **Objetivo Comunicativo:** Demostrar cómo el algoritmo combate la deserción en materias críticas y cómo garantiza que el ranking sea idéntico y reproducible bajo cualquier condición.
* **Expositor Responsable:** Renzo Antayhua.
* **Tiempo Sugerido:** 1 minuto 30 segundos.

#### Contenido Resumido para Canva
* **Multiplicadores Curriculares de Alto Riesgo (**RF24** / **RN-11**):**
  * **1.30x:** *Algoritmos y Estructuras de Datos* (Asignatura filtro de mayor índice de reprobación).
  * **1.20x:** *Cálculo I*, *Cálculo II* y *Programación Orientada a Objetos*.
  * **1.10x:** *Base de Datos*.
  * **1.00x:** Demás asignaturas de la malla regular de Ingeniería de Sistemas.
* **Clave Quíntuple de Desempate Determinista (Zero-Randomness):**
  $$\text{Key} = \left( -S_{\text{total}}, -W_{\text{curso}}, -\text{aforo\_disponible}, \text{fecha\_inicio}, \text{codigo\_sesion} \right)$$
* **Garantías Verificadas:**
  * Ante igualdad de score, precede la materia crítica; si persiste el empate, precede la que tiene más vacantes libres; luego la fecha más próxima; y finalmente el orden lexicográfico del código canónico.

#### Indicaciones de Imágenes y Recursos Visuales
* **Imagen Principal:** `evidencias/backend/01_recommendations_endpoint_response.png`
* **Pie de Imagen:** *Respuesta JSON del endpoint `/api/v1/recommendations/offers` con multiplicador 1.30x aplicado a Algoritmos.*
* **Distribución Visual en Canva:** Panel izquierdo: tabla destacada con los multiplicadores dorados de materias filtro y la fórmula de ordenamiento quíntuple. Panel derecho: captura de la respuesta JSON real del backend donde se observa el campo `"ponderador_curricular": 1.30` y `"score_total": 0.9840`.

#### Guion Oral Resumido
> **Renzo:** «Para mitigar la deserción estudiantil en ciclos formativos iniciales conforme al objetivo de la EPIS, el recomendador bonifica a las asignaturas filtro. Un taller de Algoritmos recibe un multiplicador de 1.30x, superando en el ranking a materias estándar aun con menor solapamiento horario. Asimismo, eliminamos toda aleatoriedad: implementamos una clave quíntuple de desempate determinista. Dos estudiantes con el mismo perfil recibirán exactamente el mismo orden en cualquier momento.»

---

### Diapositiva 06: Pruebas del Recomendador y Banco Determinista (ORD-01 a ORD-05)

* **Título:** Verificación Algorítmica: Batería de Pruebas ORD-01 a ORD-05
* **Subtítulo:** Auditabilidad, Determinismo e Invarianza ante Casos Frontera en Backend y Frontend
* **Objetivo Comunicativo:** Evidenciar que el recomendador fue sometido a pruebas unitarias y de integración exhaustivas, validando exclusiones temporales y de aforo.
* **Expositor Responsable:** Joan Medina.
* **Tiempo Sugerido:** 1 minuto 30 segundos.

#### Contenido Resumido para Canva
* **Casos de Prueba Especializados Homologados:**
  * **ORD-01:** Desempate ante puntaje idéntico ($S_{\text{total}} = 0.8500$) resuelto por mayor vacante disponible y menor timestamp.
  * **ORD-01b / ORD-01c:** Desempate cronológico y estabilidad lexicográfica por `codigo_sesion`.
  * **ORD-01d:** Invarianza absoluta ante permutación del orden de entrada de candidatos en 5 iteraciones.
  * **ORD-02 (RN-04):** Exclusión del 100% de sesiones con antelación menor o igual a 24 horas.
  * **ORD-03 (RN-05):** Exclusión de sesiones con aforo agotado ($Aforo_{\text{disp}} = 0$).
  * **ORD-04:** Cumplimiento estricto del parámetro de corte $k$ en query string (`top_k=3`, `top_k=5`).
  * **ORD-05 (RN-11):** Priorización matemática efectiva de *Algoritmos y Estructuras de Datos* ($1.30\text{x}$).

#### Indicaciones de Imágenes y Recursos Visuales
* **Imagen Superior:** `evidencias/pruebas/01_topk_deterministic_ordering_tests.png` (Terminal Pytest backend: 8 pruebas ORD aprobadas).
* **Imagen Inferior:** `evidencias/frontend/03_topk_ordering_vitest.png` (Terminal Vitest frontend: 9 pruebas TopKOrdering aprobadas).
* **Distribución Visual en Canva:** Disposición en dos tarjetas apiladas horizontalmente. Cada terminal con su respectivo badge verde de éxito, destacando los tiempos de ejecución sub-milisegundo.

#### Guion Oral Resumido
> **Joan:** «Para validar la estabilidad del algoritmo no bastaba con probar casos felices. Diseñamos un banco de pruebas de ordenamiento determinista con los casos ORD-01 al ORD-05 en Pytest y Vitest. Evaluamos empates artificiales forzados al cuarto decimal, demostrando que el desempate es 100% estable. Verificamos que si una sesión entra en la ventana de 24 horas o llena su aforo, desaparece de inmediato de las recomendaciones para no frustrar al estudiante.»

---

### Diapositiva 07: Arquitectura del Sistema de Reservas Transaccionales

* **Título:** Arquitectura del Flujo de Reserva y Modal Reactivo
* **Subtítulo:** Formalización Atómica de Cupos, Validaciones de Negocio y Ergonomía Accesible
* **Objetivo Comunicativo:** Presentar el circuito interactivo de reserva desde la apertura del diálogo en React hasta la emisión del comprobante canónico `RES-XXXX`.
* **Expositor Responsable:** Joan Medina.
* **Tiempo Sugerido:** 1 minuto 30 segundos.

#### Contenido Resumido para Canva
* **Flujo Operativo en Capa de Presentación (**RF12** / **CUS04**):**
  * Al pulsar *"Reservar Vacante"* en el Feed, se levanta el modal accesible `BookingModalView.tsx`.
  * **Filtros de Guarda en Cliente:** Valida autenticación `@upt.pe`, consentimiento activo (Ley N° 29733 / **RN-02**) e impide explícitamente que un mentor reserve en su propia clase ofertada.
* **Advertencia Normativa de Ratificación (**RN-08**):**
  * El modal advierte que la vacante se reserva en estado `PENDIENTE_CONFIRMACION` y que el estudiante tiene hasta **24 horas antes del inicio ($T-24\text{ h}$)** para ratificar asistencia.
* **Resiliencia ante Fallos de Red y Sobrecupo:**
  * Si la última plaza es ocupada simultáneamente por otro alumno, el cliente captura el error `HTTP 409 Conflict` (`CAPACITY_EXCEEDED`) sin colapsar la aplicación y orienta al registro de una solicitud por demanda (**CUS03**).

#### Indicaciones de Imágenes y Recursos Visuales
* **Imagen Izquierda:** `evidencias/frontend/02_booking_modal_and_rules.png` (Modal reactivo de reserva formalizado).
* **Imagen Derecha:** `diagramas/flujo_reserva.png` (Diagrama de secuencia técnica entre capas).
* **Distribución Visual en Canva:** Panel izquierdo: captura del modal con las cláusulas de consentimiento y plazos de ratificación destacados. Panel derecho: diagrama de secuencia UML modelando las llamadas entre React, FastAPI y PostgreSQL.

#### Guion Oral Resumido
> **Joan:** «El modal de reservas que desarrollé en frontend guía al estudiante de manera clara. Antes de enviar cualquier petición, verifica que el alumno tenga su consentimiento de datos personales firmado y que no sea el propio mentor intentando auto-reservarse. Se informa explícitamente que la reserva es provisional y que debe ratificarse antes de la marca de 24 horas para no perder el cupo. Ante una colisión de aforo, el modal captura el error 409 y ofrece registrar una solicitud temática por demanda.»

---

### Diapositiva 08: Control de Aforo, Concurrencia y Bloqueo Pesimista (SELECT FOR UPDATE)

* **Título:** Concurrencia Transaccional ACID y Control de Aforo
* **Subtítulo:** Bloqueo Pesimista de Fila (`SELECT ... FOR UPDATE`), Aforos Inmutables y Cero Sobrecupo (RNF07)
* **Objetivo Comunicativo:** Demostrar cómo se resolvió técnicamente la condición de carrera crítica al disputar la última vacante, acreditando la tasa de sobrecupo de 0.00%.
* **Expositor Responsable:** Renzo Antayhua.
* **Tiempo Sugerido:** 2 minutos.

#### Contenido Resumido para Canva
* **El Problema de la Condición de Carrera (Race Condition):**
  * Si dos o más estudiantes intentan reservar la vacante 10/10 en el mismo milisegundo, lecturas concurrentes sin bloqueo permitirían inscribir a 11 o más alumnos, violando el aforo normativo (**RN-05**).
* **Mecanismo de Resolución: Bloqueo Pesimista Exclusivo (**RNF07**):**
  ```sql
  SELECT * FROM sesiones_mentoria WHERE id_sesion = :id FOR UPDATE;
  ```
  * La fila de la sesión queda bloqueada a nivel del motor PostgreSQL durante la transacción.
  * Las demás peticiones concurrentes entran en cola de espera bloqueante.
  * Se verifica el conteo real: si es $\ge aforo\_maximo$, se ejecuta `ROLLBACK` y se retorna `HTTP 409 Conflict`.
* **Evidencia Empírica del Testbench Multihilo (20 Hilos Concurrentes):**
  * **1 éxito** (`HTTP 201 Created`) | **19 rechazos controlados** (`HTTP 409 Conflict`).
  * **Tasa de sobrecupo verificada = exactamente 0.00%**.

#### Indicaciones de Imágenes y Recursos Visuales
* **Imagen Superior:** `diagramas/concurrencia_aforo.png` (Diagrama de interacción de hilos concurrentes).
* **Imagen Inferior:** `evidencias/pruebas/03_concurrency_pessimistic_lock_rnf07.png` (Salida del testbench multihilo con 0.00% sobrecupo).
* **Distribución Visual en Canva:** Panel izquierdo: diagrama de secuencia de concurrencia mostrando al Hilo 1 adquiriendo el lock y al Hilo 2 esperando en cola. Panel derecho: captura del testbench multihilo acreditando la tasa de 0.00% de sobrecupo.

#### Guion Oral Resumido
> **Renzo:** «Este es uno de los aportes de ingeniería más rigurosos del proyecto. En sistemas de inscripción con vacantes limitadas, el sobrecupo ocurre cuando dos peticiones leen que queda 1 cupo antes de que cualquiera inserte su reserva. Para garantizar RNF07 implementamos un bloqueo pesimista `SELECT ... FOR UPDATE` en SQLAlchemy y PostgreSQL. Como certifica nuestro testbench multihilo de 20 hilos compitiendo por la última plaza, exactamente una solicitud formalizó la vacante y las otras diecinueve recibieron un HTTP 409 limpio. El sobrecupo resultante es exactamente 0.00%.»

---

### Diapositiva 09: Modelo Relacional `reservas_cupo` y Máquina de Estados

* **Título:** Modelo de Datos Relacional y Ciclo de Estados
* **Subtítulo:** Migración Alembic 004, Restricciones de Unicidad y Transiciones Deterministas
* **Objetivo Comunicativo:** Explicar el diseño físico de la base de datos para reservas, el control de integridad relacional y el ciclo de vida del cupo.
* **Expositor Responsable:** Renzo Antayhua.
* **Tiempo Sugerido:** 1 minuto 30 segundos.

#### Contenido Resumido para Canva
* **Entidad Física `reservas_cupo` (Migración Alembic 004):**
  * Claves foráneas con borrado en cascada hacia `sesiones_mentoria` y `usuarios`.
  * Código unívoco institucional `RES-XXXX` con índice único.
  * Restricción compuesta: `UNIQUE (id_sesion, estudiante_email)` (impide doble reserva activa del mismo estudiante en la misma clase).
* **Máquina de Estados Finitos de la Reserva (Regla D-7):**
  * `PENDIENTE_CONFIRMACION`: Estado transitorio inicial al formalizar el cupo.
  * `CONFIRMADA`: Transición cuando el estudiante ratifica asistencia en $T \ge 24\text{ h}$ (**RN-08**).
  * `CANCELADA_USUARIO`: Desistimiento voluntario del estudiante liberando la plaza.
  * `NO_CONFIRMADA`: Expiración automática a $T-24\text{ h}$ si no hubo ratificación.
  * `CANCELADA_SISTEMA`: Cancelación por falta de quórum de la clase (**RN-09**).

#### Indicaciones de Imágenes y Recursos Visuales
* **Imagen Izquierda:** `evidencias/base_datos/01_migration_004_reservas_cupo.png` (Código DDL de la migración Alembic 004).
* **Imagen Derecha:** `evidencias/base_datos/02_pessimistic_lock_query_select_for_update.png` (Traza de ejecución SQL y adquisición de lock).
* **Distribución Visual en Canva:** Panel izquierdo: fragmento DDL de la migración destacando el constraint de unicidad y las columnas de auditoría. Panel derecho: diagrama de estados finitos y registro SQL en PostgreSQL.

#### Guion Oral Resumido
> **Renzo:** «La persistencia relacional se formalizó mediante la migración Alembic 004. Creamos la tabla `reservas_cupo` con una restricción de unicidad compuesta obligatoria que impide que un alumno registre dos vacantes en la misma sesión. Asimismo, el cupo no es estático; está gobernado por una máquina de estados finitos: inicia en `PENDIENTE_CONFIRMACION`, transita a `CONFIRMADA` si el estudiante ratifica, o expira a `NO_CONFIRMADA` al llegar a las 24 horas previas, liberando automáticamente el asiento para la comunidad.»

---

### Diapositiva 10: API REST, Reglas de Negocio y Corte de Quórum a T-24h

* **Título:** Contratos API REST y Evaluación de Quórum
* **Subtítulo:** Endpoints Tipados Pydantic v2, Umbral Mínimo del 50% y Desistimiento Normativo
* **Objetivo Comunicativo:** Detallar los endpoints construidos para reservas y quórum, y la lógica de cancelación o ratificación automática a $T-24\text{ h}$.
* **Expositor Responsable:** Renzo Antayhua.
* **Tiempo Sugerido:** 1 minuto 30 segundos.

#### Contenido Resumido para Canva
* **Endpoints REST Construidos y Documentados en Swagger:**
  * `POST /api/v1/bookings/reserve`: Formalización atómica con bloqueo pesimista.
  * `GET /api/v1/bookings/my-reservations`: Consulta enriquecida de reservas del estudiante autenticado.
  * `GET /api/v1/bookings/session/{id}`: Nómina de inscritos para visualización del mentor titular.
  * `POST /api/v1/quorum/evaluate`: Evaluación y corte automático a $T-24\text{ h}$.
* **Protocolo de Quórum Institucional (**RN-09** / **CUS23**):**
  * A las 24 horas antes del inicio, el sistema computa: $\text{Ratio} = \frac{N_{\text{confirmados}}}{\text{Aforo Máximo}}$.
  * **Si $\text{Ratio} \ge 0.50$ (50% o más):** La clase transiciona a `CONFIRMADA`, ratificando el aula o enlace Meet.
  * **Si $\text{Ratio} < 0.50$ (Menos del 50%):** La clase transiciona a `CANCELADA_FALTA_QUORUM`, notificando a los alumnos para no generar desplazamientos innecesarios en el campus.

#### Indicaciones de Imágenes y Recursos Visuales
* **Imagen Superior:** `evidencias/backend/02_swagger_api_docs_sprint04.png` (Documentación Swagger interactiva de FastAPI).
* **Imagen Inferior:** `evidencias/backend/03_quorum_evaluation_cutoff_t24h.png` (Evaluación de quórum con dictámenes del 50%).
* **Distribución Visual en Canva:** Panel izquierdo: captura de Swagger con los esquemas de entrada y salida tipados. Panel derecho: visualización de la ejecución del endpoint de quórum con los dos caminos de decisión (confirmada vs cancelada).

#### Guion Oral Resumido
> **Renzo:** «La API REST expone contratos fuertemente tipados bajo Pydantic v2 y autenticación JWT. Destacamos el endpoint de corte de quórum: evaluado exactamente a 24 horas del inicio de la sesión, calcula el ratio de alumnos ratificados. Si se alcanza al menos el 50% del aforo reglamentario —por ejemplo, 5 estudiantes en presencial o 10 en virtual—, la clase se ratifica. Si no se alcanza el quórum, el sistema cancela la sesión de forma controlada, optimizando los recursos físicos de la universidad.»

---

### Diapositiva 11: Aseguramiento de Calidad: 245 Tests, Cobertura >91% y Cierre DoD

* **Título:** Calidad de Software y Definición de Terminado (DoD)
* **Subtítulo:** Batería de 245 Pruebas Automatizadas, Cobertura Dual >91% y Cero Defectos Estáticos
* **Objetivo Comunicativo:** Acreditar el cumplimiento riguroso de todos los criterios de aceptación y directrices de calidad institucional exigidos por la cátedra.
* **Expositor Responsable:** Joan Medina.
* **Tiempo Sugerido:** 1 minuto 30 segundos.

#### Contenido Resumido para Canva
* **Métricas Consolidadas de Calidad (Sprint 04):**
  * **Pruebas Automatizadas Totales:** **245 de 245 pasando (100% éxito)** en 27 suites.
    * Backend (Pytest): **158 pruebas** (14 suites, 0 fallos).
    * Frontend (Vitest): **87 pruebas** (13 suites, 0 fallos).
  * **Cobertura de Código Lograda (**RNF09** $\ge 70\%$):**
    * Backend API: **91.22%** (+21.22% sobre la meta).
    * Frontend SPA: **92.56%** (+22.56% sobre la meta).
* **Auditoría de Código y Despliegue:**
  * **Ruff 0.17.1 (Python):** 0 errores, 69 archivos formateados bajo PEP 8.
  * **ESLint 9 (TypeScript):** 0 errores, 0 advertencias en 42 módulos.
  * **Compilación Vite:** Bundle de producción generado en **100 ms** sin discrepancias de tipos (`dist/`).

#### Indicaciones de Imágenes y Recursos Visuales
* **Imagen Izquierda:** `evidencias/calidad/01_backend_pytest_coverage_sprint04.png` (Reporte Pytest-Cov al 91.22%).
* **Imagen Derecha:** `evidencias/calidad/02_frontend_vitest_coverage_sprint04.png` (Reporte Vitest al 92.56%).
* **Badge Central:** `evidencias/calidad/03_linting_and_formatting_check.png` (Cero errores de linteo).
* **Distribución Visual en Canva:** Panel superior con tres grandes tarjetas de métricas numéricas destacadas en dorado (245 Tests / 91.22% Backend / 92.56% Frontend). Panel inferior con los dos reportes de terminal oficiales acreditando la cobertura.

#### Guion Oral Resumido
> **Joan:** «El aseguramiento de calidad del Sprint 04 no se basa en estimaciones, sino en métricas automatizadas e independientes. Consolidamos una suite de 245 pruebas automatizadas sin un solo fallo. Ambas capas superan holgadamente el umbral del 70% estipulado en el RNF09: alcanzamos 91.22% en backend y 92.56% en frontend. El código presenta cero defectos en ESLint y Ruff, y la compilación de producción en Vite se genera de forma limpia en 100 milisegundos.»

---

### Diapositiva 12: Conclusiones, Logros Verificados y Transición al Sprint 05

* **Título:** Conclusiones Técnicas y Continuidad hacia Sprint 05
* **Subtítulo:** Balance del Incremento Construido y Próximos Hitos del Ecosistema P2P
* **Objetivo Comunicativo:** Sintetizar el valor entregado en el Sprint 04, transparentar las funcionalidades pendientes para los siguientes sprints y abrir la sesión de preguntas.
* **Expositor Responsable:** Presentación Conjunta (Renzo Antayhua y Joan Medina).
* **Tiempo Sugerido:** 1 minuto 30 segundos.

#### Contenido Resumido para Canva
* **Logros Consolidados en el Sprint 04:**
  1. Integración funcional del recomendador *EdRecSys v1.0* con explicabilidad transparente (XAI) y multiplicadores de materias filtro EPIS.
  2. Blindaje transaccional ACID de reservas con bloqueo pesimista `SELECT ... FOR UPDATE` (tasa de sobrecupo verificada de 0.00% bajo 20 hilos).
  3. Formalización del horizonte de ratificación anticipada a $T-24\text{ h}$ y protocolo de evaluación automática de quórum al 50%.
* **Funcionalidades Pendientes y Próximos Sprints:**
  * **Sprint 05 (En desarrollo activo):** Bandeja integral de gestión del mentoreado (*Mis Reservas*), ratificación y desistimiento en UI, y cierre de actas de mentoría.
  * **Sprint 06:** Registro de asistencia presencial/virtual mediante código QR criptográfico (SHA-256) y bitácora docente.
  * **Sprint 07 y 08:** Encuestas de satisfacción CSAT, métricas de retención y emisión de constancias con firma digital.
* **Llamado a Preguntas:** *"Q&A — Agradecemos su atención y quedamos a disposición del Dr. Ricardo Valcárcel para las consultas de la cátedra."*

#### Indicaciones de Imágenes y Recursos Visuales
* **Recursos Gráficos:**
  * Línea de tiempo horizontal tipo Roadmap destacando Sprint 01 al 04 en color verde/dorado (Culminados) y Sprint 05 al 08 en azul grisáceo (Futuros).
  * Isotipo institucional de la EPIS-UPT y datos de contacto de los autores.
* **Distribución Visual en Canva:** Tarjeta izquierda con los 3 grandes hitos consolidados; tarjeta derecha con la hoja de ruta hacia Sprint 05 y 06; sección inferior con el mensaje de agradecimiento y datos de autoría.

#### Guion Oral Resumido
> **Renzo:** «En conclusión, el Sprint 04 entrega la infraestructura central del sistema P2P: recomendación algorítmica verificada y reservas transaccionales blindadas contra colisiones de aforo.»  
> **Joan:** «Para el Sprint 05 avanzamos con la bandeja integral del estudiante para ratificar y cancelar cupos desde la interfaz. Con 245 pruebas y más del 91% de cobertura, dejamos una línea base sólida y plenamente auditable. Agradecemos su atención, Dr. Valcárcel, y quedamos a su entera disposición para las preguntas de la cátedra.»

---

*Fin del Guion Maestro de Diapositivas para Canva — Sprint 04.*
