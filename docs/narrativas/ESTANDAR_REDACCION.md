# Estándar de Redacción para el Catálogo de Narrativas de Casos de Uso

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT.
**Código del Estándar:** STD-SRS-NARRATIVAS-v2.0
**Línea base documental:** DOC-SRS-02 / Refinamiento Complementario Visual
**Fecha de Actualización:** 23 de noviembre de 2026
**Autores:** Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian

---

## 1. Propósito

El presente documento establece las directivas y criterios estandarizados de redacción, equilibrio visual y precisión funcional para la elaboración del catálogo independiente de narrativas de casos de uso (`NARRATIVAS_CASOS_DE_USO.md`) y sus diagramas complementarios en el Sistema Web P2P de Mentorías Académicas EPIS-UPT.

El estándar busca un balance óptimo entre:
- **Simplicidad y claridad:** Redacción directa en tercera persona y tiempo presente, comprensible para cualquier lector.
- **Precisión funcional:** Preservación estricta de requisitos funcionales (RF) y reglas de negocio (RN).
- **Riqueza visual descriptiva:** Capacidad para que el lector imagine la interfaz, ubique sus elementos clave y reconozca las distintas opciones disponibles.
- **Organización estructurada:** Empleo de tablas de dos columnas y enumeraciones breves internas para evitar bloques de texto densos.

---

## 2. Estructura Canónica de Cada Narrativa

Cada caso de uso incorporado al catálogo debe seguir estrictamente la siguiente jerarquía:

```markdown
### CUS-XXX — [Nombre Funcional del Caso de Uso]

#### 7.1. Ficha descriptiva
[Tabla canónica de 12 atributos]

#### 7.2. Flujo normal de eventos
[Tabla de 2 columnas: Acción del Actor | Respuesta del Sistema, con fases temáticas]

#### 7.3. Flujos alternativos
[Subsecciones A001..A00n con tablas de 2 columnas, origen y condición de activación]

#### 7.4. Flujos de excepción
[Subsecciones E001..E00n con tablas de 2 columnas, origen y condición de activación]

#### 7.5. Diagrama de flujo de actividades
**Figura X. Diagrama de actividades — CUS-XXX: [Nombre].**
![Figura X...](docs/narrativas/diagramas/img/CUS-XXX_actividades.png)
Fuente: Elaboración propia.

#### 7.6. Diagrama de caso de uso
**Figura Y. Diagrama de caso de uso — CUS-XXX: [Nombre].**
![Figura Y...](docs/narrativas/diagramas/img/CUS-XXX_caso_de_uso.png)
Fuente: Elaboración propia.
```

---

## 3. Ficha Descriptiva Canónica (12 Atributos)

La ficha descriptiva debe contener exactamente los siguientes 12 atributos:

| Atributo | Detalle Requerido |
|---|---|
| **Id Caso de Uso** | Identificador oficial (ej. `UC-001` / `CUS-001`). |
| **Nombre** | Denominación funcional y clara del caso de uso. |
| **Tipo** | `Obligatorio` u `Opcional`. |
| **Requisito ID (RF)** | Requisitos funcionales y reglas de negocio asociadas (ej. `RF-001, RF-002; RN-01, RN-02`). |
| **Versión** | Versión documental correspondiente (ej. `2.3 (Refinamiento Visual)`). |
| **Autor** | Nombres formales de los autores o tesistas responsables. |
| **Actores** | Actores primarios (usuarios) y actores secundarios (servicios externos). |
| **Interacción** | Resumen operativo de la interacción (dispositivo o canal utilizado). |
| **Descripción** | Finalidad funcional del caso de uso, ámbito normativo y resultado formativo. |
| **Referencias** | Normas técnicas y legales aplicables (SWEBOK, ISO 29148, Ley N° 29733, etc.). |
| **Precondiciones** | Requisitos y condiciones previas necesarias para iniciar la interacción. |
| **Postcondiciones** | Estado final alcanzado por el sistema y el usuario al concluir el flujo con éxito. |

> [!IMPORTANT]
> **Eliminación obligatoria:** Queda expresamente prohibido incluir el atributo **Anexos** en la ficha descriptiva. Toda descripción visual debe integrarse de manera fluida en las respuestas del sistema.

---

## 4. Criterios de Descripción Visual y Funcional

### 4.1. Descripción Inicial de Cada Pantalla
Cuando una pantalla o interfaz aparezca por primera vez en el flujo, debe describirse de forma ordenada considerando:
1. **Título de la pantalla y colores predominantes:** Fondo general y tono de la tarjeta o contenedor.
2. **Encabezado y navegación:** Opciones disponibles, indicadores de sesión y la pestaña o sección actualmente seleccionada.
3. **Formularios y controles disponibles:** Campos de texto, etiquetas, sugerencias (*placeholders*) y textos de ayuda.
4. **Opciones y alternativas de interacción:** Describir tanto la vía principal como las demás alternativas que el usuario visualiza (no limitarse al botón del siguiente paso).
5. **Estado de los elementos:** Indicar claramente qué controles se encuentran habilitados o deshabilitados.

### 4.2. Descripción de Opciones Disponibles
Cuando una pantalla presente múltiples alternativas de interacción, describir brevemente cada una indicando:
- **Nombre visible:** Texto literal entre comillas angulares (« ») o dobles (" ").
- **Ubicación:** En el encabezado, en la tarjeta central, en la barra inferior, etc.
- **Resaltado o color:** Fondo azul marino, botón dorado, texto gris, etc.
- **Finalidad:** Qué persigue o qué permite realizar.
- **Condición de disponibilidad:** Si está siempre visible, si requiere completar datos o si depende de un temporizador.
- **Flujo relacionado:** Mención al flujo alternativo o de excepción correspondiente (`A001`, `A004`, etc.).

### 4.3. Descripción de Cambios de Estado
En los pasos subsiguientes, **no repetir** la descripción del encabezado ni los elementos que permanecen estáticos. Describir únicamente:
- Aparición de nuevas ventanas o modales.
- Campos o avisos que surgen.
- Botones que cambian de color o se habilitan/deshabilitan.
- Variaciones en temporizadores o contadores.
- Alertas de advertencia o confirmación.
- Transiciones a nuevos paneles o pestañas activas.

### 4.4. Organización Mediante Enumeraciones Internas
Cuando una respuesta del sistema contenga múltiples elementos, campos u opciones, se deben utilizar **enumeraciones breves dentro de la misma celda** de la tabla para facilitar la lectura. No dividir la respuesta en múltiples pasos artificiales si forman parte del mismo evento de respuesta.

---

## 5. Nivel de Detalle Orientativo

| Tipo de Contenido | Extensión / Formato Orientativo |
|---|---|
| **Acción del actor** | Una oración breve, directa y en presente. |
| **Respuesta sencilla del sistema** | Una o dos oraciones descriptivas. |
| **Presentación de una nueva pantalla** | Párrafo introductorio y enumeración breve (70 a 140 palabras). |
| **Pantalla con múltiples opciones** | Enumeración de opciones con ubicación, estado y flujo alternativo. |
| **Cambio de estado o actualización** | Una a tres oraciones señalando los elementos que cambian. |
| **Mensajes de error o excepción** | Ubicación, color, mensaje exacto y opciones de recuperación o rectificación. |

> [!NOTE]
> Las métricas de reducción de texto constituyen una referencia orientativa. La prioridad es la claridad descriptiva y la preservación funcional completa.

---

## 6. Vocabulario y Lenguaje Permitido / Prohibido

### 6.1. Lenguaje Prohibido
- **Archivos de código:** `LoginOtpView.tsx`, `authService.ts`, etc.
- **Componentes y funciones:** `useState`, `useEffect`, `renderiza el componente`.
- **Sentencias SQL y base de datos:** `SELECT`, `FROM usuarios`, `table`, etc.
- **Endpoints y rutas HTTP:** `POST /api/v1/...`, `GET /...`.
- **Códigos de respuesta:** `HTTP 200`, `HTTP 401`, `HTTP 404`.
- **Tecnicismos de almacenamiento:** `JWT`, `Bearer Token`, `localStorage`, `Pydantic`.
- **Estilos en código:** Valores hexadecimales (`#1C2A59`), píxeles (`px`), `box-shadow`, etc.

### 6.2. Lenguaje Permitido
- Nombres comunes de colores: *azul marino*, *dorado*, *blanco*, *gris claro*, *verde* y *rojo*.
- Términos literales de la interfaz entre comillas: «Iniciar sesión», «Continuar con Código OTP →», «Verificar y Acceder», etc.
- Vocabulario formal: *comprueba*, *muestra*, *habilita*, *inicia la sesión*, *despliega el panel*.

---

## 7. Formato de Tablas de Interacción

Tanto el flujo normal como los flujos alternativos y de excepción deben presentarse en tablas de **dos columnas**:

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **Paso N.** El usuario realiza una acción directa. | |
| | **Paso N+1.** El sistema responde presentando las opciones e interfaces correspondientes. |

---

## 8. Estándar para Diagramas Complementarios

- **Diagrama de actividades:** UML 2.5, carriles `|Usuario|` y `|Sistema Web P2P|`, rombos con preguntas sencillas, caminos alternativos y excepciones identificadas.
- **Diagrama de casos de uso:** UML 2.5, límite del sistema, actores primarios y secundarios, relaciones `<<include>>` y `<<extend>>` correctamente orientadas.
- **Imágenes:** Renderizadas en PNG de alta resolución bajo `docs/narrativas/diagramas/img/` y enlazadas con pie de figura formal (`Fuente: Elaboración propia.`).
