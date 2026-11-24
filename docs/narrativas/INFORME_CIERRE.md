# Informe Final de Cierre — Hito DOC-SRS-02 (Refinamiento Visual y Funcional)

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT.
**Código del Hito:** DOC-SRS-02 / Refinamiento Complementario
**Nombre del Hito:** Creación del catálogo independiente de narrativas y diagramas de casos de uso — Versión con Mayor Precisión Visual y Opciones Disponibles
**Fecha de Entrega:** 23 de noviembre de 2026
**Autores:** Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian

---

## 1. Identificación del Hito

| Parámetro | Detalle |
|---|---|
| **Proyecto** | Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT |
| **Código del Hito** | DOC-SRS-02 (Refinamiento Visual y Funcional) |
| **Repositorio Oficial** | `https://github.com/JMedina255/sistema_web_p2p` |
| **Rama de Trabajo** | `docs/srs-catalogo-narrativas` |
| **Commit Base de Referencia** | `7f330cd7f93b1fb38fa4d89ffd67921804df65e4` (DOC-SRS-01R) |
| **Commit Final de Entrega** | `9ef6d4b4044391f30c4e1b3720fd40ecfee997d8` |
| **Rama Remota de Publicación** | `origin/docs/srs-catalogo-narrativas` |
| **Estado de Integración con main** | Independiente (Pull Request en espera de aprobación expresa) |

---

## 2. Resumen del Trabajo Realizado

En cumplimiento de las directivas de refinamiento complementario para el hito **DOC-SRS-02**, se enriqueció moderadamente el nivel de detalle visual y la descripción de opciones disponibles del caso de uso modelo **CUS-001 (Iniciar sesión institucional con 2FA)**:

1. **Descripción inicial estructurada de pantallas:**
   - **Pantalla inicial:** Se detalló el encabezado institucional en azul marino con el emblema UPT, el botón dorado «Iniciar sesión», las opciones de navegación para visitantes (pestaña activa «🔐 Iniciar sesión» y pestaña inactiva «📚 Cursos»), la tarjeta central blanca y la enumeración de las cuatro opciones y elementos de interacción disponibles (Google Workspace, divisor horizontal, campo de correo con texto de ayuda y botón «Continuar con Código OTP →»).
   - **Pantalla de verificación del código:** Se estructuraron los seis elementos visibles: aviso superior azul de confirmación, tarjeta resumen con correo y enlace dorado «Cambiar correo» (A004), campo numérico centrado de seis dígitos, contador regresivo «⏳ Expira en: 05:00», botón principal «Verificar y Acceder» y sección de reenvío con contador de 60 segundos conmutable a enlace interactivo (A002).
   - **Ventana de consentimiento informado:** Se describió el modal superpuesto sobre fondo atenuado con título institucional y balanza («⚖️»), panel de lectura con barra de desplazamiento de cláusulas de la Ley N° 29733, casilla obligatoria de aceptación, botón secundario rojo «🚫 Rechazar y Salir» (E006) y botón principal azul marino «✓ Aceptar y Continuar» (habilitado dinámicamente).
   - **Panel principal del usuario según el rol formativo:** Se detalló la barra superior con el distintivo de rol y estado verde «⚖️ Consentimiento OK», junto con el desglose de pestañas autorizadas para los tres perfiles del sistema: Estudiante Mentoreado («🎯 Recomendaciones» con motor EdRecSys, reservas y evaluaciones), Estudiante Mentor («📋 Mis Sesiones», oferta y asistencia) y Administrador Institucional («👥 Gestión de Roles», analítica y auditoría).
2. **Organización mediante enumeraciones internas:** Se estructuraron las respuestas extensas utilizando viñetas claras dentro de las celdas de la tabla de dos columnas (`Acción del Actor` | `Respuesta del Sistema`), evitando párrafos excesivamente densos y sin alterar la secuencia numérica de los pasos.
3. **Ausencia estricta de lenguaje técnico interno:** Se preservó la erradicación total de componentes de React, consultas SQL, endpoints HTTP, tokens JWT, `localStorage` y propiedades CSS/hexadecimales, empleando exclusivamente vocabulario funcional y nombres comunes de colores (azul marino, dorado, blanco, gris claro, verde y rojo).
4. **Actualización de estándares metodológicos:** Se actualizó `ESTANDAR_REDACCION.md` a la versión 2.0 (STD-SRS-NARRATIVAS-v2.0), normando la descripción inicial de pantallas, el formato de opciones disponibles y el manejo de enumeraciones internas para las narrativas futuras.
5. **Preservación de diagramas y trazabilidad:** Se conservaron íntegros los diagramas UML 2.5 de actividades y de caso de uso renderizados en PNG, así como los documentos de referencia originales (`SRS.md`, `SRS_NUEVO.md`, `SAD.md`).

---

## 3. Resultados Cuantitativos y Verificación

| Indicador | Meta / Condición Requerida | Resultado Obtenido | Estado |
|---|---|---|:---:|
| **Narrativas desarrolladas** | Exclusivamente 1 (CUS-001) | 1 desarrollada y enriquecida (CUS-001) | Cumplido |
| **Narrativas restantes** | 23 sin iniciar | 23 pendientes (CUS-002 a CUS-024) | Cumplido |
| **Diagramas de actividades generados** | 1 individual (CUS-001) | 1 generado y renderizado (PNG 2385 × 1806 px) | Cumplido |
| **Diagramas de casos de uso generados** | 1 individual (CUS-001) | 1 generado y renderizado (PNG 772 × 430 px) | Cumplido |
| **Total de diagramas renderizados** | 2 diagramas PNG | 2 imágenes PNG verificadas visualmente | Cumplido |
| **Reducción de texto equivalente** | 30 % a 50 % de reducción | **35.7 % de reducción global** (de 4,033 a 2,594 palabras) | Cumplido |
| **Eliminación del atributo Anexos** | 0 menciones en ficha descriptiva | Totalmente suprimido | Cumplido |
| **Eliminación de apartados redundantes** | Sin bloques aislados de UI / GWT | Integrado fluidamente en tabla de 2 columnas | Cumplido |
| **Preservación de documentos base** | `SRS.md`, `SRS_NUEVO.md`, `SAD.md` intactos | 100 % inalterados | Cumplido |
| **Modificación de código funcional** | 0 archivos modificados | Ningún archivo de código modificado | Cumplido |
| **Publicación en repositorio remoto** | Push a rama independiente | Publicado en `docs/srs-catalogo-narrativas` | Cumplido |
| **Aprobación del responsable** | Requerida antes de continuar | **PUNTO DE DETENCIÓN OBLIGATORIO** | En espera |

---

## 4. Evaluación Detallada de la Reducción de Texto

Se realizó el cálculo automatizado de palabras entre los apartados funcionales homólogos de `SRS_NUEVO.md` y la versión enriquecida de `NARRATIVAS_CASOS_DE_USO.md`:

| Apartado Homólogo | Palabras en `SRS_NUEVO.md` | Palabras en `NARRATIVAS_CASOS_DE_USO.md` | Reducción Obtenida (%) | Justificación del Balance Visual y Funcional |
|---|---:|---:|---:|---|
| **Ficha descriptiva** | 459 | 203 | **55.8 %** | Supresión del atributo Anexos y condensación rigurosa de 12 atributos canónicos. |
| **Flujo normal de eventos** | 1,667 | 1,034 | **38.0 %** | Enriquecimiento con opciones disponibles y enumeraciones sin perífrasis de código. |
| **Flujos alternativos (A001-A004)** | 679 | 451 | **33.6 %** | Redacción precisa de condiciones de activación, estados visuales y retorno. |
| **Flujos de excepción (E001-E007)** | 1,228 | 906 | **26.2 %** | Detalle de ubicación de alertas rojas, persistencia de datos y rectificación. |
| **Total Comparado** | **4,033** | **2,594** | **35.7 %** | **Rango objetivo alcanzado (30 % - 50 %)** con óptima riqueza visual. |

---

## 5. Inventario de Archivos Entregables

| Entregable | Ruta Relativa en Repositorio | Descripción |
|---|---|---|
| **Catálogo independiente de narrativas** | `NARRATIVAS_CASOS_DE_USO.md` | Documento raíz que contiene la narrativa enriquecida visualmente del CUS-001 y sus diagramas integrados. |
| **Estándar de redacción** | `docs/narrativas/ESTANDAR_REDACCION.md` | Versión 2.0 que norma la descripción inicial de pantallas, opciones disponibles y enumeraciones internas. |
| **Control de avance** | `docs/narrativas/CONTROL_AVANCE.md` | Registro de trazabilidad y métricas de avance (1/24 narrativas, 2/48 diagramas). |
| **Informe final de cierre** | `docs/narrativas/INFORME_CIERRE.md` | Documento formal de liquidación y evaluación del hito DOC-SRS-02. |
| **Fuente PlantUML actividades** | `docs/narrativas/diagramas/plantuml/CUS-001_actividades.puml` | Código fuente del diagrama de actividades con carriles `Usuario` y `Sistema Web P2P`. |
| **Fuente PlantUML caso de uso** | `docs/narrativas/diagramas/plantuml/CUS-001_caso_de_uso.puml` | Código fuente del diagrama de caso de uso UML 2.5 centrado exclusivamente en CUS-001. |
| **Imagen actividades renderizada** | `docs/narrativas/diagramas/img/CUS-001_actividades.png` | Gráfico en alta resolución (2385 × 1806 px) para incorporación documental. |
| **Imagen caso de uso renderizada** | `docs/narrativas/diagramas/img/CUS-001_caso_de_uso.png` | Gráfico en alta resolución (772 × 430 px) para incorporación documental. |

---

## 6. Verificación Visual de los Diagramas

Ambos diagramas fueron inspeccionados visualmente mediante renderizado automatizado de PlantUML:
- **Figura 1 (`CUS-001_actividades.png`):** Carriles nítidos, rombos de decisión identificables sin textos truncados ni solapamientos, manejo estandarizado de excepciones (E001 a E006) y alternativos (A001 a A004), acorde a la paleta institucional (azul marino `#1C2A59`, dorado `#B99451`, blanco `#FFFFFF`).
- **Figura 2 (`CUS-001_caso_de_uso.png`):** Distribución simétrica de actores primarios a la izquierda y secundarios a la derecha, relaciones de inclusión (`<<include>>`) y extensión (`<<extend>>`) orientadas según OMG UML 2.5.

---

## 7. Punto de Detención Obligatorio

En estricto cumplimiento del requerimiento:
- **No se ha iniciado ni modificado ninguno de los otros 23 casos de uso (CUS-002 al CUS-024).**
- El desarrollo queda suspendido a la espera de la revisión y **aprobación expresa del responsable del proyecto** respecto a este modelo refinado del CUS-001.
