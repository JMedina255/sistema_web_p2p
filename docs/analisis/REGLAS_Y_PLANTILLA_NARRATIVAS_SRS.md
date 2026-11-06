# GUÍA DE ESTÁNDAR, REGLAS Y PLANTILLA CANÓNICA PARA NARRATIVAS DE CASOS DE USO (SRS v2.0)
**Sistema Web P2P con Algoritmo de Recomendación para la Personalización de Mentorías Académicas en la EPIS-UPT**

---

## 1. PROPÓSITO Y ALCANCE DEL DOCUMENTO

El presente documento establece el estándar oficial, las directrices de ingeniería de requisitos, las reglas de redacción de interfaz y la plantilla canónica de especificación para los **24 casos de uso canónicos (`CUS-001` al `CUS-024`)** pertenecientes a la sección **6.2.3 (Escenarios de Casos de Uso - Narrativas)** del Informe de Especificación de Requerimientos de Software (SRS v2.0) del proyecto.

Este estándar es de cumplimiento estricto y obligatorio para todos los analistas, desarrolladores y revisores del equipo **C-SharkTeam**, garantizando:
1. **Rigor metodológico y normativo** bajo estándares internacionales de ingeniería de software.
2. **Trazabilidad bidireccional total** con la matriz de Requerimientos Funcionales (RF01 al RF26), Reglas de Negocio (RN-01 al RN-14) y Atributos de Calidad ISO/IEC 25010.
3. **Nivel de detalle exhaustivo en interfaz de usuario (UI)** expresado enteramente en lenguaje natural funcional, sin dejar componentes ni comportamientos a la imaginación.
4. **Uniformidad estructural y estilística** en todos los módulos (`MOD-01` al `MOD-08`).

---

## 2. MARCO NORMATIVO Y ESTÁNDARES APLICADOS

Las especificaciones detalladas en este estándar se fundamentan en las siguientes normas y cuerpos de conocimiento:

- **Guía SWEBOK v3.0 (Software Engineering Body of Knowledge, IEEE Computer Society):** Capítulo 1 (Software Requirements), adoptando la descomposición funcional mediante escenarios de interacción actor-sistema, condiciones de frontera y gestión de excepciones.
- **Estándar ISO/IEC/IEEE 29148:2018 (Systems and software engineering — Life cycle processes — Requirements engineering):** Cláusulas de completitud, no ambigüedad, verificabilidad y trazabilidad de los requisitos de software.
- **Criterios de Acreditación Internacional ICACIT (Revisión 2026):** Estándares de calidad de diseño en ingeniería de computación, documentación formal y verificación de satisfacción de necesidades del usuario y la organización académica.
- **Ley N° 29733 (Ley de Protección de Datos Personales del Perú) y su Reglamento D.S. 003-2013-JUS:** Principios de legalidad, consentimiento previo y explícito, finalidad y seguridad de la información académica y personal.

---

## 3. CATÁLOGO MAESTRO DE LOS 24 CASOS DE USO CANÓNICOS (MOD-01 AL MOD-08)

El sistema se organiza en ocho (8) módulos funcionales. Todos los casos de uso deben mantener la nomenclatura oficial de identificación `CUS-XXX` (formato canónico de tres dígitos, e.g. `CUS-001`), asociado a su correspondiente Requerimiento Funcional (`RF-XXX`):

| Módulo Funcional | Código CUS | Nombre Oficial del Caso de Uso | Requisito Funcional (RF) | Reglas de Negocio (RN) |
|---|:---:|---|:---:|:---:|
| **MOD-01:** Seguridad, Autenticación y Gobernanza | **CUS-001** | Iniciar sesión institucional con 2FA | RF-001, RF-002 | RN-01, RN-02 |
| | **CUS-010** | Gestionar asignación de roles de usuario | RF-003 | RN-03 |
| **MOD-02:** Planificación, Espacios y Agendamiento | **CUS-006** | Publicar oferta de mentoría académica | RF-008, RF-009 | RN-04, RN-05, RN-06, RN-07 |
| | **CUS-008** | Consultar disponibilidad de espacios y recursos | RF-009, RF-010 | RN-06 |
| **MOD-03:** Gestión Curricular y Perfiles Académicos | **CUS-005** | Gestionar perfil formativo y disponibilidad horaria | RF-004 | RN-03 |
| | **CUS-021** | Explorar catálogo curricular de asignaturas filtro | RF-005 | — |
| **MOD-04:** Motor de Recomendación Inteligente (*EdRecSys*) | **CUS-002** | Explorar recomendaciones personalizadas Top-k | RF-006 | RN-04, RN-11 |
| | **CUS-003** | Registrar solicitud de demanda académica | RF-007 | RN-04 |
| **MOD-05:** Reserva, Confirmación y Control de Quórum | **CUS-004** | Reservar cupo de mentoría académica | RF-012 | RN-05, RN-08 |
| | **CUS-024** | Ratificar asistencia a sesión de mentoría | RF-013 | RN-08 |
| | **CUS-017** | Desistir voluntariamente de reserva | RF-014 | RN-08, RN-10 |
| | **CUS-023** | Evaluar quórum automático a T-24h | RF-015 | RN-08, RN-09 |
| | **CUS-007** | Decisión del mentor ante quórum insuficiente | RF-016 | RN-09, RN-10 |
| **MOD-06:** Trazabilidad, Bitácoras y Sesiones | **CUS-012** | Registrar asistencia a sesión de mentoría | RF-017 | RN-12 |
| | **CUS-013** | Registrar bitácora académica de sesión | RF-017, RF-020 | RN-12 |
| | **CUS-014** | Visualizar historial y bitácoras académicas | RF-019 | — |
| **MOD-07:** Gamificación, Reputación y Certificación | **CUS-018** | Emitir constancia institucional de horas de mentoría | RF-022, RF-023 | RN-14 |
| | **CUS-019** | Gestionar insignias y reputación gamificada | RF-021 | RN-13 |
| **MOD-08:** Supervisión, Analítica y Parametrización | **CUS-009** | Notificar eventos críticos y alertas temporales | RF-011, RF-015 | RN-08, RN-10 |
| | **CUS-011** | Generar reportes e indicadores de analítica académica | RF-025 | RN-13 |
| | **CUS-015** | Consultar métricas de retención y desempeño | RF-025 | — |
| | **CUS-016** | Auditar trazas de seguridad y consentimiento Ley 29733 | RF-002, RF-026 | RN-02, RN-14 |
| | **CUS-020** | Configurar parámetros institucionales y umbrales | RF-022 | RN-05, RN-08, RN-09, RN-14 |
| | **CUS-022** | Gestionar catálogo de temas y materias críticas | RF-005, RF-024 | RN-11 |

---

## 4. REGLAS ESTRICTAS DE REDACCIÓN Y ESTILO DE INTERFAZ

Para asegurar que los casos de uso brinden una especificación inequívoca tanto para el equipo de desarrollo de frontend/backend como para la auditoría de acreditación, se establecen las siguientes reglas de redacción:

### Regla 1: Nivel de Detalle Exhaustivo de la Interfaz
- Se deben describir de manera explícita y tangible todos los componentes de interacción del usuario y la pantalla:
  - **Componentes admitidos:** Tarjetas informativas (*cards*), Cuadros de diálogo / Ventanas modales, Botones de acción principal y secundaria, Cuadros de texto (*input fields*), Menús desplegables (*selects*), Casillas de selección (*checkboxes*), Botones de opción (*radio buttons*), Insignias o etiquetas de estado (*badges*), Iconos de ayuda o señalización, Paneles informativos colapsables, Barras horizontales de progreso o disponibilidad, Indicadores circulares de carga (*spinners*), Notificaciones flotantes (*toasts*).
- Todo botón, enlace o acción invocable debe llevar su etiqueta textual visible **entre comillas dobles** (ejemplos: `"Reservar Cupo"`, `"Confirmar Asistencia"`, `"Rechazar Solicitud"`, `"Descargar Constancia en PDF"`).

### Regla 2: Expresión Cromática y Visual en Lenguaje Natural
- Se debe describir el aspecto visual en lenguaje natural formal.
- **Términos admitidos:** "en color azul institucional", "etiqueta en color verde de éxito", "banner de advertencia en color ámbar", "borde resaltado en color rojo de error", "texto atenuado en color gris secundario", "fondo en color blanco puro", "indicador de estado en color celeste claro".
- **PROHIBICIÓN ESTRICTA:** Queda terminantemente prohibido el uso de:
  - Códigos hexadecimales o RGB (ejemplo: NO `#1E3A8A`, NO `rgb(30, 58, 138)`).
  - Medidas absolutas en píxeles o rem (ejemplo: NO `520px`, NO `1.5rem`).
  - Niveles numéricos de opacidad técnica o transparencias CSS (ejemplo: NO `opacity: 0.6`, NO `60% de opacidad`).

### Regla 3: Prohibición de Datos Estáticos o "Quemados" (Hardcoded Data)
- Ningún flujo debe utilizar nombres de personas particulares, códigos de alumnos ficticios o materias particulares como si fuesen fijos en la lógica.
- La descripción de los datos debe ser enteramente **funcional y parametrizada**:
  - *Correcto:* "el sistema despliega el código y nombre oficial de la asignatura formativa, el tema conceptual silábico objeto de refuerzo, el nombre completo y ciclo del mentor responsable, la fecha programada, franja horaria de inicio y finalización, duración total en minutos, el aula o laboratorio físico asignado si la modalidad es presencial, o el enlace institucional seguro si es virtual, y el aforo disponible respecto a la capacidad máxima reglamentaria".
  - *Incorrecto:* "el sistema muestra Cálculo II con el mentor Juan Pérez en el aula 204 a las 10:00 am".

### Regla 4: Mensajes del Sistema Literales y Textuales
- Todo mensaje de confirmación, notificación de éxito, aviso preventivo, advertencia o mensaje de error que el sistema presente al usuario debe especificarse de forma exacta y literal **entre comillas dobles y en cursiva o entre comillas**:
  - *Ejemplo de éxito:* `"¡Cupo reservado exitosamente! Recuerda que debes ratificar tu asistencia obligatoriamente antes de las 24 horas previas al inicio de la sesión"`.
  - *Ejemplo de advertencia:* `"Atención: La ventana de ratificación para esta sesión vencerá en menos de 2 horas"`.
  - *Ejemplo de error:* `"Operación rechazada: El aforo de esta sesión se ha completado en este instante. Por favor, selecciona otra opción en el catálogo"`.

---

## 5. ESTRUCTURA Y CAMPOS OBLIGATORIOS DE CADA CASO DE USO

Cada caso de uso está constituido por cuatro secciones secuenciales:
1. **Ficha Técnica de Gobernanza** (Tabla superior de 12 atributos canónicos).
2. **Flujo Normal de Eventos** (Tabla de dos columnas dividida por subfases operativas y pasos numerados con llamadas de desvío explícitas).
3. **Flujos Alternativos (`A00X`)** (Tablas de dos columnas con pasos jerárquicos y punto de reincorporación o finalización explícito).
4. **Flujos de Excepción (`E00X`)** (Tablas de dos columnas con pasos jerárquicos y punto de retorno o resolución transaccional explícito).

### 5.1. Campos y Formato Exacto de la Ficha Técnica

| Atributo | Regla y Formato de Llenado |
|---|---|
| **Id Caso de Uso** | Código canónico en formato `CUS-XXX` (e.g. `CUS-001`, `CUS-004`). |
| **Nombre** | Nombre oficial completo del caso de uso. |
| **Tipo** | Formato exacto con casillas: `Obligatorio ( X ) / Opcional (   )` o `Obligatorio (   ) / Opcional ( X )`. |
| **Requisito ID (RF)** | Código formal del requerimiento funcional asociado (`RF-XXX`), detallando las reglas de negocio vinculadas (`RN-XX`). |
| **Versión** | Valor fijo: `2.0` |
| **Autor** | `Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos` |
| **Actores** | Identificación de Actores Primarios y Secundarios con su rol dentro del ecosistema universitario. |
| **Interacción** | Fase del ciclo de vida e iteración del proyecto (e.g. `Fase de Construcción / Iteración Sprint 04 - Sprint 05` o `Fase de Elaboración / Iteración 1.0`). |
| **Descripción** | Resumen funcional exhaustivo del objetivo, valor de negocio y alcance de la interacción. |
| **Referencias** | Marco de gobernanza: `Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Guía ICACIT, Ley N° 29733 (cuando aplique)`. |
| **Anexos** | Vistas de interfaz, diálogos modales, cuadros de alerta o artefactos de diseño vinculados. |
| **Precondiciones** | Requisitos técnicos, de sesión, de datos o de estado previos indispensables para iniciar el caso de uso. |
| **PostCondiciones** | Estado final persistido en base de datos, entidades modificadas, transacciones completadas, comprobantes emitidos o notificaciones despachadas. |

### 5.2. Reglas del Flujo Normal de Eventos
- Formato de tabla de dos columnas: `Usuario` | `Sistema`.
- Se divide en **Subfases temáticas** delimitadas por filas de encabezado de bloque en negrita dentro de la tabla (e.g. `Fase 1: Identificación y Selección`, `Fase 2: Validación y Bloqueo Concurrente`, `Fase 3: Persistencia y Confirmación`).
- Pasos numerados secuencialmente: `1`, `2`, `3`, etc.
- Cada bifurcación o condición en el flujo principal **DEBE** incluir una llamada explícita de salto hacia el flujo alternativo o de excepción correspondiente:
  - Formato: `(Si [condición de excepción], salta a E00X)`
  - Formato: `(Si [condición alternativa], salta a A00X)`

### 5.3. Reglas de los Flujos Alternativos (`A00X`) y de Excepción (`E00X`)
- Encabezado de nivel 5 (`#####`) con el formato: `##### Flujo alternativo A00X: [Nombre descriptivo]` o `##### Flujo de excepción E00X: [Nombre descriptivo]`.
- Formato de tabla de dos columnas: `Usuario` | `Sistema`.
- Numeración jerárquica estricta: `A001-1.1`, `A001-1.2`, `A001-1.3`... o `E001-1.1`, `E001-1.2`, `E001-1.3`...
- **Cláusula de Cierre Obligatoria:** El último paso de todo flujo alternativo o de excepción debe dictaminar inequívocamente su desenlace:
  - Si retorna al flujo normal: `... y el sistema retorna al paso X del Flujo Normal de Eventos.`
  - Si aborta o termina: `... y el sistema revierte las transacciones pendientes y finaliza el caso de uso sin generar registros.`

---

## 6. PLANTILLA CANÓNICA OFICIAL EN BLANCO

A continuación se presenta la plantilla estándar oficial lista para instanciar en cada caso de uso:

```markdown
#### CUS-XXX - [Nombre Oficial del Caso de Uso]

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-XXX |
| **Nombre** | [Nombre Oficial del Caso de Uso] |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-XXX ([Nombre del Requisito]); RN-XX ([Regla de Negocio]) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** [Rol del Actor Primario]<br>**Secundario:** [Actor o Servicio Secundario] |
| **Interacción** | Fase de Construcción / Iteración Sprint XX - Sprint XX |
| **Descripción** | [Descripción clara, exhaustiva y funcional del propósito y alcance del caso de uso]. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Guía ICACIT, Ley N° 29733 |
| **Anexos** | [Listado de pantallas, modales o componentes de interfaz vinculados] |
| **Precondiciones** | 1. [Precondición 1]<br>2. [Precondición 2]<br>3. [Precondición 3] |
| **PostCondiciones** | 1. [Postcondición 1 - Estado de entidades persistidas]<br>2. [Postcondición 2 - Notificaciones y comprobantes emitidos] |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: [Nombre de la Subfase 1]** | |
| **1.** [Acción inicial del usuario sobre un componente de interfaz específico]. | **2.** [Respuesta visual y validación inicial del sistema en lenguaje natural]. (Si [condición de desvío], salta a E001). |
| **Fase 2: [Nombre de la Subfase 2]** | |
| **3.** [Acción del usuario al interactuar con el formulario, modal o confirmación]. | **4.** [Procesamiento transaccional, actualización de estados y validación de reglas de negocio]. (Si [condición alternativa], salta a A001). |
| **Fase 3: [Nombre de la Subfase 3]** | |
| **5.** [Confirmación final o recepción del comprobante por parte del usuario]. | **6.** [Despliegue del mensaje literal de éxito entre comillas, actualización de contadores y despacho de notificaciones]. |

##### Flujos Alternativos

##### Flujo alternativo A001: [Nombre descriptivo de la bifurcación]
| Usuario | Sistema |
|---|---|
| **A001-1.1** [Acción particular del usuario que diverge del flujo base]. | **A001-1.2** [Respuesta adaptada del sistema que resuelve la variante de negocio]. |
| **A001-1.3** [Acción de continuación del usuario]. | **A001-1.4** [Persistencia específica] y el sistema retorna al paso X del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: [Nombre descriptivo de la excepción]
| Usuario | Sistema |
|---|---|
| **E001-1.1** [Evento que provoca la condición de error o infracción de regla]. | **E001-1.2** [El sistema intercepta la anomalía, ejecuta rollback de transacciones y despliega mensaje de alerta literal entre comillas] y el sistema finaliza el caso de uso sin generar registros. |
```

---

## 7. EJEMPLO CANÓNICO MODELO BASE APROBADO: CUS-004

A continuación se transcribe en su totalidad el caso de uso patrón **CUS-004 (Reservar cupo de mentoría académica)** desarrollado en estricta conformidad con el estándar, sirviendo como guía de referencia empírica:

---

#### CUS-004 - Reservar cupo de mentoría académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-004 |
| **Nombre** | Reservar cupo de mentoría académica |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-012 (Reserva de cupos con control de aforo y concurrencia); RN-05 (Aforos máximos estándar), RN-08 (Ventana de confirmación hasta T-24h) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentoreado (*Estudiante de I a IV Ciclo de la EPIS-UPT*)<br>**Secundario:** Gestor de Tareas Desatendidas (*Servicio Cron / Backend*) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite al estudiante mentoreado seleccionar una oferta de mentoría académica publicada en el catálogo o recomendada por el motor inteligente, verificar la disponibilidad de cupos en tiempo real mediante control transaccional estricto de concurrencia, y formalizar una reserva provisional en estado pendiente de ratificación, asegurando el cumplimiento de los límites de aforo (10 cupos para presencial, 20 para virtual) e informando la obligación de confirmar asistencia antes del corte de 24 horas previas al evento. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT, Ley N° 29733 |
| **Anexos** | Pantalla de Exploración de Mentorías y Recomendaciones Top-k, Cuadro de Diálogo Modal de Detalle y Reserva de Cupo, Indicador de Disponibilidad de Aforo en Tiempo Real, Comprobante Digital de Reserva Preliminar. |
| **Precondiciones** | 1. El estudiante mentoreado ha iniciado sesión satisfactoriamente mediante autenticación multifactor institucional con credenciales válidas del dominio `@upt.pe` (`CUS-001`).<br>2. El estudiante ha suscrito el consentimiento informado digital bajo la Ley N° 29733 (`RN-02`).<br>3. El estudiante pertenece a los ciclos formativos reglamentarios (I al IV Ciclo) y no mantiene sanciones de inhabilitación vigentes en la plataforma.<br>4. Existe al menos una sesión de mentoría en estado canónico `PUBLICADA` con una antelación superior a 24 horas respecto a su inicio lectivo (`RN-04`). |
| **PostCondiciones** | 1. Se registra una nueva entidad `Reserva` en la base de datos vinculando al mentoreado con la sesión, asignándole el estado canónico `PENDIENTE_CONFIRMACION`.<br>2. Se decrementa de forma atómica en una unidad el contador de cupos disponibles de la sesión ofertada.<br>3. Se programa en el gestor de eventos desatendidos el despacho de alertas de ratificación orientadas al corte de 24 horas previas ($T-24\text{ h}$).<br>4. Se despliega en la interfaz del usuario el comprobante de reserva provisional con fecha límite de confirmación. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Exploración y selección de la oferta formativa** | |
| **1.** El estudiante mentoreado navega por la cartelera de mentorías o el módulo de recomendaciones personalizadas y pulsa sobre la tarjeta informativa de la sesión que requiere cursar. (Si la selección se realiza desde el carrusel de recomendaciones algorítmicas, salta a A001). | **2.** Despliega un cuadro de diálogo modal en primer plano con el encabezado en color azul institucional, mostrando el código y nombre oficial de la asignatura formativa, el tema conceptual silábico a impartir, el nombre completo y ciclo del estudiante mentor, la fecha programada, franja horaria y duración en minutos, la modalidad de dictado con su respectivo aforo máximo, una barra horizontal de disponibilidad en color verde indicando los cupos disponibles respecto al total, y el botón de acción principal `"Reservar Cupo"`. |
| **Fase 2: Verificación transaccional de aforos y elegibilidad** | |
| **3.** El estudiante presiona el botón `"Reservar Cupo"` dentro del cuadro de diálogo modal. | **4.** El sistema inicia una transacción atómica con bloqueo a nivel de fila y evalúa que el número de reservas activas sea estrictamente inferior al aforo máximo configurado (10 en modalidad presencial o 20 en modalidad virtual, según RN-05). (Si el aforo se completó en ese instante por concurrencia simultánea, salta a E001). |
| | **5.** El sistema valida la elegibilidad académica del estudiante mentoreado: comprueba que pertenezca al ciclo formativo admitido, que no posea cruces de horario con otra sesión agendada en la misma franja, y que no registre una reserva previa en la misma mentoría. (Si el estudiante tiene cruce de horario, salta a E002). (Si el estudiante ya tiene una reserva en la misma sesión, salta a E003). (Si el estudiante no pertenece al ciclo admitido, salta a E004). |
| **Fase 3: Persistencia de la vacante y confirmación preliminar** | |
| | **6.** Persiste el registro de la vacante apartada asignándole el estado canónico `PENDIENTE_CONFIRMACION`, decrementa el cupo visible de la sesión, programa la alarma de seguimiento para el corte perentorio de 24 horas previas ($T-24\text{ h}$ según RN-08) y cierra el modal interactivo de selección. |
| **7.** El estudiante visualiza en pantalla la tarjeta de confirmación de reserva y revisa los datos de contacto y calendarización provisional de la sesión. | **8.** Muestra un panel informativo flotante en color verde de éxito con el mensaje literal: *"¡Cupo reservado exitosamente! Recuerda que debes ratificar tu asistencia obligatoriamente antes de las 24 horas previas al inicio de la sesión"*, incorporando una insignia en color ámbar de advertencia con el temporizador regresivo hacia la ventana de corte de ratificación y el botón `"Ir a Mis Reservas"`. |

##### Flujos Alternativos

##### Flujo alternativo A001: Reserva ejecutada desde tarjeta de recomendación Top-k
| Usuario | Sistema |
|---|---|
| **A001-1.1** El estudiante mentoreado presiona directamente el botón `"Reservar Cupo"` incrustado en una de las tarjetas del carrusel de recomendaciones personalizadas Top-k (`CUS-002`). | **A001-1.2** El sistema registra en la bitácora de telemetría analítica el identificador de la recomendación para el cálculo de la tasa de conversión (`Click-Through Rate`) del algoritmo inteligente *EdRecSys*. |
| **A001-1.3** El estudiante examina la tarjeta modal simplificada que se abre automáticamente sobre el panel de recomendaciones. | **A001-1.4** Despliega el cuadro de diálogo modal con los datos parametrizados de la oferta y el sistema retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Agotamiento de vacantes por concurrencia simultánea (Colisión de aforo)
| Usuario | Sistema |
|---|---|
| **E001-1.1** En el instante de procesar la solicitud, otro participante ocupa la última vacante libre de la sesión. | **E001-1.2** El backend detecta bajo bloqueo transaccional que los cupos disponibles son cero (0), revierte inmediatamente la transacción, actualiza la tarjeta de la sesión mostrando una etiqueta en color gris con el texto *"Sin vacantes"* e inhabilita el botón de reserva. |
| **E001-1.3** El estudiante pulsa el botón `"Aceptar"` en la ventana de notificación de cupos agotados. | **E001-1.4** Despliega una alerta modal en color ámbar con el mensaje literal: *"Lo sentimos, el aforo de esta sesión se ha completado en este instante. Por favor, selecciona otra fecha disponible o formula una solicitud de mentoría por demanda"* y el sistema finaliza el caso de uso sin generar registros. |

##### Flujo de excepción E002: Conflicto de horario con otra sesión agendada
| Usuario | Sistema |
|---|---|
| **E002-1.1** El estudiante mentoreado intenta reservar una sesión cuya franja horaria coincide o se solapa con otra sesión donde ya posee reserva confirmada o pendiente. | **E002-1.2** El sistema detecta el traslape en el cronograma del usuario, rechaza la transacción y despliega un cuadro de diálogo con borde resaltado en color rojo de error con el mensaje literal: *"Operación rechazada: Presentas un cruce de horario con otra sesión previamente agendada en tu calendario institucional"*. |
| **E002-1.3** El estudiante lee la advertencia y presiona el botón `"Entendido"`. | **E002-1.4** El sistema cierra la ventana de error, mantiene intacto el catálogo de ofertas y finaliza el caso de uso sin generar registros. |

##### Flujo de excepción E003: Intento de reserva duplicada en la misma sesión
| Usuario | Sistema |
|---|---|
| **E003-1.1** El estudiante envía una petición de reserva en una sesión de mentoría en la cual ya se encuentra registrado con estado pendiente o confirmado. | **E003-1.2** El sistema verifica la clave compuesta de usuario y sesión en el repositorio de reservas, aborta la operación y muestra un cuadro de diálogo informativo en color ámbar con el mensaje literal: *"Acceso restringido: Ya cuentas con una vacante reservada para esta sesión de mentoría"*. |
| **E003-1.3** El estudiante pulsa el botón `"Ver mi Reserva Actual"`. | **E003-1.4** El sistema redirige al panel de `"Mis Reservas"` mostrando el estado de su inscripción vigente y finaliza el caso de uso sin generar registros duplicados. |

##### Flujo de excepción E004: Inelegibilidad académica por ciclo formativo no admitido
| Usuario | Sistema |
|---|---|
| **E004-1.1** Un estudiante perteneciente a ciclos superiores o con sanción disciplinaria activa intenta formalizar una reserva en la sesión formativa. | **E004-1.2** El sistema evalúa el perfil del usuario contra los prerrequisitos de la asignatura filtro, bloquea la acción y despliega un cuadro de diálogo en color rojo de advertencia con el mensaje literal: *"Inscripción no permitida: Tu perfil académico o ciclo formativo actual no cumple con las condiciones requeridas para esta sesión"* y el sistema finaliza el caso de uso sin generar registros. |
