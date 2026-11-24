# Estándar de Redacción para el Catálogo de Narrativas de Casos de Uso

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT.
**Código del Estándar:** STD-SRS-NARRATIVAS-v1.0
**Línea base documental:** DOC-SRS-02
**Autor:** Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian

---

## 1. Propósito

El presente documento establece las directivas y criterios estandarizados de redacción, simplificación y diseño visual para la elaboración del catálogo independiente de narrativas de casos de uso (`NARRATIVAS_CASOS_DE_USO.md`) y sus diagramas complementarios en el Sistema Web P2P de Mentorías Académicas EPIS-UPT.

Este estándar garantiza que la documentación sea comprensible para cualquier lector (estudiantes, docentes, evaluadores y autoridades universitarias), manteniendo el rigor formal y funcional sin recurrir a tecnicismos de programación ni explicaciones internas de código.

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
| **Versión** | Versión documental correspondiente (ej. `2.2 (DOC-SRS-02)`). |
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

## 4. Reglas de Lenguaje y Simplificación

### 4.1. Lenguaje Prohibido (Tecnicismos de Implementación)
No se deben incluir referencias a detalles internos de desarrollo:
- **Archivos de código:** `LoginOtpView.tsx`, `authService.ts`, etc.
- **Componentes y funciones:** `useState`, `useEffect`, `renderiza el componente`, etc.
- **Consultas o tablas SQL:** `SELECT`, `FROM usuarios`, etc.
- **Endpoints y rutas HTTP:** `POST /api/v1/auth/otp/request`, `GET /users`, etc.
- **Códigos y protocolos HTTP:** `HTTP 200`, `HTTP 401`, etc.
- **Estructuras y datos técnicos:** `JSON`, `JWT`, `Bearer Token`, `localStorage`, `Pydantic`.
- **Propiedades visuales en código:** `#1C2A59`, `#B99451`, `px`, `rem`, `box-shadow`, `border-radius`.

### 4.2. Lenguaje Permitido y Recomendado
- Redactar en **tercera persona** y en **tiempo presente**.
- Utilizar vocabulario funcional claro:
  - *«El sistema comprueba...»* (en lugar de *«El backend ejecuta la consulta SQL para verificar...»*).
  - *«El sistema muestra la pantalla...»* (en lugar de *«El frontend renderiza la vista...»*).
  - *«El usuario presiona el botón...»* (en lugar de *«El actor hace clic sobre el elemento button...»*).
- Conservar los **nombres exactos de botones y textos visibles** entre comillas angulares (« ») o comillas dobles (" ").
- Denominar los colores institucionales por su nombre descriptivo: *azul marino institucional*, *dorado institucional*, *fondo blanco*, *alerta roja*, *aviso azul*.

### 4.3. Criterios de Reducción de Texto (30 % a 50 %)
- Sustituir perífrasis y frases redundantes por expresiones directas.
- Omitir explicaciones redundantes sobre sombras, medidas, paddings y estilos decorativos secundarios.
- Describir la estructura general de una pantalla la primera vez que aparece; en los pasos posteriores, describir únicamente los cambios específicos.

---

## 5. Formato de Tablas de Interacción

Tanto el flujo normal como los flujos alternativos y de excepción deben presentarse en tablas de **dos columnas**:

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **Paso N.** El usuario ejecuta una acción concreta. | |
| | **Paso N+1.** El sistema valida, actualiza la interfaz y presenta las opciones disponibles. |

- Cada acción y respuesta debe figurar en una fila independiente.
- Las fases temáticas se insertan como filas de encabezado que agrupan lógicamente los pasos del flujo.
- Los flujos alternativos y de excepción deben explicitar su **Paso origen** y su **Condición de activación**.

---

## 6. Estándar para Diagramas Complementarios

### 6.1. Diagrama de Flujo de Actividades
- **Notación:** UML 2.5 (PlantUML).
- **Carriles (Swimlanes):** Dos carriles principales: `|Usuario|` y `|Sistema Web P2P|`.
- **Contenido:** Representar la secuencia completa, decisiones funcionales mediante rombos con preguntas claras, caminos alternativos y puntos de excepción relevantes.
- **Paleta visual:** Fondo blanco, encabezados en azul marino institucional (`#1C2A59`), rombos de decisión en amarillo claro institucional (`#FEF9C3`) con borde dorado (`#B99451`).

### 6.2. Diagrama de Casos de Uso
- **Notación:** UML 2.5 (PlantUML).
- **Límite del sistema:** `rectangle "Sistema Web P2P — EPIS-UPT"`.
- **Actores principales (izquierda):** Estudiante Mentoreado, Estudiante Mentor, Administrador Institucional.
- **Actores secundarios (derecha):** Servicios institucionales externos (Correo SMTP, Google Workspace).
- **Relaciones:** Uso estricto de `<<include>>` (inclusión obligatoria) y `<<extend>>` (extensión condicional), con dirección correcta de flechas conforme al estándar OMG UML.

### 6.3. Almacenamiento y Renderizado
- Código fuente: `docs/narrativas/diagramas/plantuml/CUS-XXX_[tipo].puml`.
- Imagen renderizada: `docs/narrativas/diagramas/img/CUS-XXX_[tipo].png` (resolución mínima recomendada: 1200 px de ancho para actividades, 700 px para casos de uso).
- Enlace en documento: Vía ruta relativa con pie de figura formal (`Fuente: Elaboración propia.`).
