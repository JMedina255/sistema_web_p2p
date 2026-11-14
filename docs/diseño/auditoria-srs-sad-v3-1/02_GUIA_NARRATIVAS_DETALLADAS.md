# GUÍA METODOLÓGICA DE ESPECIFICACIÓN DE NARRATIVAS DETALLADAS DE CASOS DE USO (H01)
## Estándar Canónico para la Fase de Diseño y Construcción (SRS v3.1)

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT<br>
**Curso:** Construcción de Software I<br>
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas<br>
**Equipo Consultor:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)<br>
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado<br>
**Semestre Académico:** 2026-II<br>
**Fecha de Emisión:** 14 de Noviembre de 2026<br>
**Rama de Trabajo:** `docs/srs-sad-v3-1-homologacion`<br>
**Commit Base de Auditoría:** `097f90d725e537f411ebadac740905e0c0448f61`

---

## Control de Versiones

A continuación, se formaliza el registro de control de versiones de la presente guía estándar:

### Cuadro 2.1: Registro de Control de Versiones del Entregable H01 (Guía de Narrativas)

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcárcel | Dirección EPIS | 14/11/2026 | Emisión de la guía estándar de especificación exhaustiva de casos de uso para el SRS v3.1, incorporando navegación real de interfaz, sintaxis cromática natural, criterios Given-When-Then y etiquetas de diferenciación técnica. |

Fuente: Elaboración propia.

El presente cuadro certifica el establecimiento formal del estándar de ingeniería de requisitos que gobernará la redacción de los 24 casos de uso canónicos del Sistema Web P2P.

---

## 1. Propósito y Fundamento Normativo

El propósito de esta guía es definir el estándar canónico obligatorio para la redacción de las narrativas de los **24 Casos de Uso Oficiales (`CUS-001` al `CUS-024`)** en el SRS v3.1. 

El estándar supera la clásica ambigüedad de las especificaciones genéricas ("el sistema procesa los datos"), asegurando que cada caso de uso describa con absoluta fidelidad:
1. **La interacción humana verificable:** Menús, pestañas, pantallas, modales, etiquetas, campos, selecciones, botones y mensajes exactos.
2. **Las respuestas del sistema y reglas de negocio:** Validaciones de entrada, control de autorización, transiciones de estado, cerrojos de concurrencia y persistencia.
3. **La trazabilidad a pruebas:** Criterios de aceptación formalizados bajo la sintaxis Given-When-Then (Gherkin) enlazados a archivos de prueba en Vitest y Pytest.

El marco normativo se sustenta en:
* **ISO/IEC/IEEE 29148:2018:** Cláusulas de completitud, precisión, no ambigüedad y verificabilidad de requerimientos.
* **Guía SWEBOK v3.0 (IEEE Computer Society):** Modelado de escenarios actor-sistema, condiciones de frontera y tratamiento de excepciones.
* **Criterios de Acreditación Internacional ICACIT (2026):** Verificación de procesos de diseño en ingeniería y satisfacción de necesidades del usuario universitario.
* **Ley N° 29733 (Protección de Datos Personales del Perú):** Consentimiento explícito, confidencialidad y auditabilidad de trazas.

---

## 2. Taxonomía de Etiquetas de Diferenciación Metodológica

Para evitar confusiones entre lo que el sistema exige normativamente, lo que está efectivamente implementado en código y las propuestas de evolución técnica, cada narrativa incorporará las siguientes etiquetas estandarizadas:

A continuación, se presenta la clasificación de etiquetas de estado técnico:

### Cuadro 2.2: Catálogo de Etiquetas de Estado y Comportamiento Técnico

| Etiqueta | Significado Metodológico | Criterio de Aplicación en la Narrativa |
| :---: | :--- | :--- |
| `[EXIGIDO]` | Requisito normativo obligatorio | Aplica a políticas institucionales, reglas de negocio (`RN-XX`) o requisitos legales (Ley 29733). |
| `[IMPLEMENTADO]` | Comportamiento verificado en código | Aplica a componentes, servicios o endpoints que están construidos y verificados con pruebas en `main`. |
| `[EVIDENCIA_VISUAL]` | Atributo comprobado en UI | Aplica a colores, textos de botones, modales o estructuras visibles comprobadas en componentes React. |
| `[MEJORA_PROPUESTA]` | Refinamiento de diseño propuesto | Aplica a sugerencias de experiencia de usuario o blindajes técnicos propuestos para la versión v3.1. |
| `[PENDIENTE]` | Capacidad en desarrollo o futura | Aplica a funcionalidades proyectadas no integradas aún en la versión de producción o staging. |

Fuente: Elaboración propia.

El uso riguroso del Cuadro 2.2 impide que un evaluador de acreditación asuma que una propuesta de diseño representa código ya desplegado, fortaleciendo la honestidad técnica del expediente académico.

---

## 3. Estructura Obligatoria de Cada Caso de Uso Canónico

Cada caso de uso debe desarrollarse estructurado rigurosamente en las siguientes siete (7) secciones secuenciales:

```text
CUS-XXX — [Nombre Oficial del Caso de Uso]
├── A. Ficha Técnica de Identificación y Gobernanza (13 atributos canónicos)
├── B. Narrativa Principal del Flujo Normal (Tabla de 2 columnas dividida en subfases)
├── C. Subflujos Específicos (Identificadores jerárquicos S00X)
├── D. Flujos Alternativos (Identificadores jerárquicos A00X con cláusula de cierre)
├── E. Flujos de Excepción (Identificadores jerárquicos E00X con impacto en BD)
├── F. Especificación Exhaustiva de Interfaz de Usuario y Comportamiento Visual
└── G. Criterios de Aceptación Formativos (Given-When-Then vinculados a pruebas)
```

---

### A. Ficha Técnica de Identificación y Gobernanza

La ficha técnica superior condensa la gobernanza institucional del caso de uso mediante una tabla canónica de 13 atributos:

| Atributo | Regla y Formato de Llenado |
| :--- | :--- |
| **Id Caso de Uso** | Código canónico oficial en formato de tres dígitos (ej. `CUS-001`, `CUS-003`). |
| **Nombre** | Denominación formal idéntica a la línea base aprobada en la Matriz de Homologación. |
| **Tipo** | Formato de casillas: `Obligatorio ( X ) / Opcional (   )` o `Obligatorio (   ) / Opcional ( X )`. |
| **Módulo** | Identificador y nombre del módulo arquitectónico (ej. `MOD-01: Seguridad, Autenticación y Gobernanza`). |
| **Requisitos Asociados** | Códigos explícitos de `RF-XXX`, `RN-XX` y `RNF-XX`. |
| **Versión** | Valor formal: `3.1 (Fase de Diseño y Cierre de Construcción)`. |
| **Autores** | `Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian (Grupo 03 / C-SharkTeam)`. |
| **Actores** | Identificación de Actores Primarios (quien ejecuta la acción) y Secundarios (quien recibe o asiste). |
| **Objetivo del Actor** | Beneficio concreto y medible que persigue el usuario al completar la interacción. |
| **Descripción Funcional** | Párrafo exhaustivo explicando qué hace el sistema y qué valor entrega a la comunidad universitaria. |
| **Evento Disparador** | Acción de usuario, evento temporal cron o llamada externa que inicia el caso de uso. |
| **Precondiciones** | Estado previo indispensable del sistema, sesión activa o datos requeridos en base de datos. |
| **Postcondiciones** | Estado del sistema al concluir: Éxito (registros persistidos, tokens emitidos) y Fallo (rollback, sin mutación). |

---

### B. Narrativa Principal del Flujo Normal

El flujo normal describe la trayectoria de ejecución exitosa ("happy path") desde el inicio hasta la culminación:
1. **Estructura en dos columnas:** `Usuario` (o `Acción del Actor`) y `Sistema` (o `Respuesta del Sistema`).
2. **Subfases temáticas:** Delimitadas por filas de bloque en negrita dentro de la tabla (ej. `Fase 1: Acceso y Selección`, `Fase 2: Validación y Bloqueo Pesimista`, `Fase 3: Confirmación y Persistencia`).
3. **Pasos correlativos y numerados:** `1`, `2`, `3`, etc.
4. **Navegación real y explícita:** Se debe indicar la pantalla de origen, la pestaña pulsada, el campo completado, la selección del menú desplegable y el botón presionado (con su texto exacto entre comillas dobles, ej. `"Confirmar Reserva"`).
5. **Llamadas explícitas de desvío:** Cada validación o punto de bifurcación DEBE declarar hacia qué flujo alternativo o excepción salta ante incumplimiento:
   - Formato: `(Si [condición de excepción], salta a E00X)`
   - Formato: `(Si [condición alternativa], salta a A00X)`

---

### C. Subflujos Complementarios (`S00X`)

Operaciones secundarias o modulares que se ejecutan como parte del flujo principal pero ameritan aislamiento por su complejidad (ej. carga de temarios silábicos dependientes de la asignatura seleccionada):
* Encabezado de nivel 5 (`##### Subflujo S00X: [Nombre descriptivo]`).
* Numeración jerárquica: `S00X-1.1`, `S00X-1.2`, etc.
* Declaración explícita de entrada y punto de retorno al paso del Flujo Normal.

---

### D. Flujos Alternativos (`A00X`)

Rutas legítimas y exitosas distintas del flujo principal (ej. cancelar la operación voluntariamente, cambiar de materia seleccionada, optar por autenticación federada con Google Workspace en lugar de código OTP):
* Encabezado de nivel 5 (`##### Flujo alternativo A00X: [Nombre descriptivo]`).
* Tabla de dos columnas (`Usuario` | `Sistema`).
* Numeración jerárquica: `A00X-1.1`, `A00X-1.2`, etc.
* **Cláusula de cierre obligatoria:** El último paso debe indicar inequívocamente el desenlace:
  - Si retorna al flujo principal: `... y el sistema retorna al paso X del Flujo Normal de Eventos.`
  - Si finaliza la interacción: `... y el sistema cierra el diálogo modal y finaliza el caso de uso sin generar registros.`

---

### E. Flujos de Excepción (`E00X`)

Comportamiento del sistema ante errores de entrada, transgresión de reglas de negocio, falta de cupos, expiración de plazos o fallos de red:
* Encabezado de nivel 5 (`##### Flujo de excepción E00X: [Nombre descriptivo]`).
* Tabla de dos columnas (`Usuario` | `Sistema`).
* Numeración jerárquica: `E00X-1.1`, `E00X-1.2`, etc.
* **Detalle obligatorio:** Describir el mensaje exacto de error mostrado al usuario (entre comillas dobles), el color del banner/toast (en lenguaje natural) y el estado en el que queda el sistema (transacción revertida, sin datos huérfanos).

---

### F. Especificación Exhaustiva de Interfaz y Comportamiento Visual

Esta sección describe la experiencia visual y operativa del usuario en lenguaje formal, garantizando accesibilidad y rigor estético:
1. **Denominación y Ubicación de Pantallas:** Nombre de la vista y ruta de navegación (ej. `Portal del Estudiante -> Pestaña "Explorar Mentorías" -> Modal de Registro`).
2. **Textos y Etiquetas:** Títulos, subtítulos, placeholders y textos de ayuda literales entre comillas dobles.
3. **Botones e Interactividad:** Etiqueta visible del botón entre comillas dobles (`"Enviar Solicitud"`, `"Verificar y Acceder"`), indicando su estado activo, deshabilitado (cursor `not-allowed`) o en proceso de carga (*spinner* giratorio).
4. **Paleta Cromática en Lenguaje Natural:**
   * **PROHIBICIÓN ESTRICTA:** No usar códigos hexadecimales (`#1C2A59`) ni funciones RGB (`rgb(...)`) en la descripción funcional del SRS.
   * **VOCABULARIO PERMITIDO:** "Azul institucional", "dorado institucional", "fondo blanco puro", "borde gris claro", "texto secundario en gris atenuado", "banner de alerta en rojo de error", "notificación informativa en azul suave", "etiqueta de confirmación en verde de éxito", "aviso preventivo en color ámbar".
5. **Comportamiento Accesible (WCAG 2.1 AA):** Cierre de diálogos modales mediante la tecla `Escape`, navegación por teclado con foco visible mediante `Tab`, y anuncios de pantalla a través de atributos `role="alert"` y `role="dialog"`.

---

### G. Criterios de Aceptación Formativos (Sintaxis Given-When-Then)

Cada caso de uso debe incluir un mínimo de cuatro (4) escenarios de aceptación escritos bajo el estándar Gherkin, vinculados a pruebas automatizadas reales del repositorio:

```gherkin
Escenario 1: [Operación Exitosa - Happy Path]
  DADO QUE [precondición del sistema y estado del actor]
  CUANDO [el actor ejecuta la acción principal con datos válidos]
  ENTONCES [el sistema produce el resultado verificable y persiste el estado]
  Y [se despliega el mensaje de éxito correspondiente].
  Evidencia de Prueba: [test_modulo.py::test_caso_exitoso / Componente.test.tsx]

Escenario 2: [Validación de Entradas e Incompletitud]
  DADO QUE [el formulario se encuentra en pantalla]
  CUANDO [el actor omite un campo obligatorio o ingresa un formato inválido]
  ENTONCES [el sistema bloquea el envío y resalta el campo con borde en color rojo de error]
  Y [muestra el mensaje de advertencia específico sin alterar la base de datos].
  Evidencia de Prueba: [test_modulo.py::test_validacion_campos]

Escenario 3: [Restricción de Negocio o Control de Autorización]
  DADO QUE [el actor no cumple una regla de negocio institucional (ej. RN-03 ciclo insuficiente)]
  CUANDO [intenta realizar la acción restringida]
  ENTONCES [el sistema rechaza la operación con código de error institucional]
  Y [despliega una notificación de acceso denegado].
  Evidencia de Prueba: [test_authorization.py::test_rol_invalido]

Escenario 4: [Condición de Borde o Fallo de Concurrencia]
  DADO QUE [ocurre una condición límite (ej. aforo agotado concurrentemente o token expirado)]
  CUANDO [el sistema procesa la solicitud]
  ENTONCES [ejecuta rollback transaccional automático]
  Y [notifica al usuario de forma clara ofreciendo alternativas de recuperación].
  Evidencia de Prueba: [test_concurrency.py::test_sobrecupo_bloqueo]
```

---

## 4. Conclusión del Estándar de Narrativas

La presente guía proporciona el patrón unificado indispensable para asegurar que el SRS v3.1 cumpla con los estándares más exigentes de la cátedra de Construcción de Software I y de comités externos de acreditación. Los casos piloto `CUS-001` y `CUS-003` serán los primeros en instanciar este estándar con precisión quirúrgica.
