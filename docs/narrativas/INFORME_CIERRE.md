# Informe Final de Cierre — Hito DOC-SRS-02

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT.
**Código del Hito:** DOC-SRS-02
**Nombre del Hito:** Creación del catálogo independiente de narrativas y diagramas de casos de uso
**Fecha de Entrega:** 23 de noviembre de 2026
**Autores:** Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian

---

## 1. Identificación del Hito

| Parámetro | Detalle |
|---|---|
| **Proyecto** | Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT |
| **Código del Hito** | DOC-SRS-02 |
| **Repositorio Oficial** | `https://github.com/JMedina255/sistema_web_p2p` |
| **Rama de Trabajo** | `docs/srs-catalogo-narrativas` |
| **Commit Base de Referencia** | `7f330cd7f93b1fb38fa4d89ffd67921804df65e4` (DOC-SRS-01R) |
| **Commit Final de Entrega** | `10003d8ba758164084f8c7e553d182fb606cf0d7` |
| **Rama Remota de Publicación** | `origin/docs/srs-catalogo-narrativas` |
| **Estado de Integración con main** | Independiente (Pull Request en espera de aprobación expresa) |

---

## 2. Resumen del Trabajo Realizado

En cumplimiento de las especificaciones del hito **DOC-SRS-02**, se consolidó la transición hacia un catálogo documental independiente para las especificaciones funcionales de interacción del sistema:

1. **Creación del documento independiente `NARRATIVAS_CASOS_DE_USO.md`:** Se estructuró un nuevo documento raíz dedicado exclusivamente a las narrativas y diagramas de casos de uso, sin apartados generales de arquitectura ni modelos de base de datos.
2. **Reconstrucción simplificada del CUS-001 (Iniciar sesión institucional con 2FA):** Se mantuvo de forma rigurosa la trazabilidad de los requisitos funcionales (RF-001, RF-002) y las reglas de negocio (RN-01, RN-02), preservando la estructura canónica de tabla de dos columnas (`Acción del Actor` | `Respuesta del Sistema`).
3. **Erradicación del lenguaje técnico de programación:** Se eliminaron por completo menciones a componentes de React, funciones de frontend/backend, endpoints y rutas HTTP, códigos numéricos de estado, consultas SQL, estructuras JSON, tokens criptográficos, variables de sesión y propiedades CSS/hexadecimales. Las descripciones se expresaron en lenguaje funcional accesible para cualquier miembro de la comunidad universitaria.
4. **Supresión de apartados redundantes:** Se eliminó la fila `Anexos` de la ficha descriptiva y se suprimieron los bloques aislados de especificación exhaustiva de UI y criterios Given-When-Then, integrando las respuestas visuales directamente en el flujo de interacción.
5. **Elaboración y renderizado de diagramas UML 2.5:**
   - **Diagrama de actividades (`CUS-001_actividades.puml` / `.png`):** Flujo completo con carriles `|Usuario|` y `|Sistema Web P2P|`, decisiones con rombos de preguntas directas, caminos alternativos (A001-A004) y excepciones (E001-E006).
   - **Diagrama de casos de uso (`CUS-001_caso_de_uso.puml` / `.png`):** Límite del sistema, 3 actores primarios, 2 actores secundarios, relaciones `<<include>>` (OTP y consentimiento Ley N° 29733) y `<<extend>>` (Google Workspace).
6. **Diseño de estándares y control de avance:** Se formularon `ESTANDAR_REDACCION.md` y `CONTROL_AVANCE.md` para normar la expansión posterior de los 23 casos de uso pendientes tras la aprobación del presente modelo.

---

## 3. Resultados Cuantitativos y Verificación

| Indicador | Meta / Condición Requerida | Resultado Obtenido | Estado |
|---|---|---|:---:|
| **Narrativas desarrolladas** | Exclusivamente 1 (CUS-001) | 1 desarrollada (CUS-001) | Cumplido |
| **Narrativas restantes** | 23 sin iniciar | 23 pendientes (CUS-002 a CUS-024) | Cumplido |
| **Diagramas de actividades generados** | 1 individual (CUS-001) | 1 generado y renderizado (PNG 2385×1806 px) | Cumplido |
| **Diagramas de casos de uso generados** | 1 individual (CUS-001) | 1 generado y renderizado (PNG 772×430 px) | Cumplido |
| **Total de diagramas renderizados** | 2 diagramas PNG | 2 imágenes PNG verificadas visualmente | Cumplido |
| **Reducción de texto equivalente** | 30 % a 50 % de reducción | **48.1 % de reducción global** (de 4,033 a 2,094 palabras) | Cumplido |
| **Eliminación del atributo Anexos** | 0 menciones en ficha descriptiva | Totalmente suprimido | Cumplido |
| **Eliminación de apartados redundantes** | Sin bloques aislados de UI / GWT | Integrado fluidamente en tabla de 2 columnas | Cumplido |
| **Preservación de documentos base** | `SRS.md`, `SRS_NUEVO.md`, `SAD.md` intactos | 100 % inalterados | Cumplido |
| **Modificación de código funcional** | 0 archivos de frontend/backend/DB modificados | Ningún archivo de código modificado | Cumplido |
| **Publicación en repositorio remoto** | Push a rama independiente | Publicado en `docs/srs-catalogo-narrativas` | Cumplido |
| **Aprobación del responsable** | Requerida antes de continuar | **PUNTO DE DETENCIÓN OBLIGATORIO** | En espera |

---

## 4. Evaluación Detallada de la Reducción de Texto

Se realizó un cálculo automatizado y exacto de palabras entre los apartados funcionales homólogos de `SRS_NUEVO.md` y `NARRATIVAS_CASOS_DE_USO.md`:

| Apartado Equivalente | Palabras en `SRS_NUEVO.md` | Palabras en `NARRATIVAS_CASOS_DE_USO.md` | Reducción Obtenida (%) | Justificación Funcional |
|---|---:|---:|---:|---|
| **Ficha descriptiva** | 459 | 198 | **56.9 %** | Supresión del atributo Anexos y simplificación formal de descripciones. |
| **Flujo normal de eventos** | 1,667 | 592 | **64.5 %** | Eliminación de descripciones de sombras, hexadecimales y perífrasis de código. |
| **Flujos alternativos (A001-A004)** | 679 | 449 | **33.9 %** | Redacción directa de condiciones de activación y puntos de retorno. |
| **Flujos de excepción (E001-E007)** | 1,228 | 855 | **30.4 %** | Descripción puntual del motivo del fallo, alerta visible y vía de rectificación. |
| **Total Comparado** | **4,033** | **2,094** | **48.1 %** | **Rango objetivo alcanzado (30 % - 50 %)** sin pérdida de requisitos. |

---

## 5. Inventario de Archivos Entregables

| Entregable | Ruta Relativa en Repositorio | Descripción |
|---|---|---|
| **Catálogo independiente de narrativas** | `NARRATIVAS_CASOS_DE_USO.md` | Documento raíz que contiene la narrativa formal simplificada del CUS-001 y sus diagramas integrados. |
| **Estándar de redacción** | `docs/narrativas/ESTANDAR_REDACCION.md` | Guía metodológica, sintáctica y visual para la redacción de futuras narrativas del proyecto. |
| **Control de avance** | `docs/narrativas/CONTROL_AVANCE.md` | Registro de trazabilidad y métricas de avance (1/24 narrativas, 2/48 diagramas). |
| **Informe final de cierre** | `docs/narrativas/INFORME_CIERRE.md` | Documento formal de liquidación y evaluación del hito DOC-SRS-02. |
| **Fuente PlantUML actividades** | `docs/narrativas/diagramas/plantuml/CUS-001_actividades.puml` | Código fuente del diagrama de actividades con carriles `Usuario` y `Sistema Web P2P`. |
| **Fuente PlantUML caso de uso** | `docs/narrativas/diagramas/plantuml/CUS-001_caso_de_uso.puml` | Código fuente del diagrama de caso de uso UML 2.5 centrado exclusivamente en CUS-001. |
| **Imagen actividades renderizada** | `docs/narrativas/diagramas/img/CUS-001_actividades.png` | Gráfico en alta resolución (2385×1806 px) para incorporación documental. |
| **Imagen caso de uso renderizada** | `docs/narrativas/diagramas/img/CUS-001_caso_de_uso.png` | Gráfico en alta resolución (772×430 px) para incorporación documental. |

---

## 6. Verificación Visual de los Diagramas

Ambos diagramas fueron inspeccionados visualmente mediante renderizado automatizado de PlantUML:
- **Figura 1 (`CUS-001_actividades.png`):** Carriles nítidos, rombos de decisión identificables sin textos truncados ni solapamientos, manejo estandarizado de excepciones (E001 a E006) y alternativos (A001 a A004), acorde a la paleta institucional (azul marino `#1C2A59`, dorado `#B99451`, blanco `#FFFFFF`).
- **Figura 2 (`CUS-001_caso_de_uso.png`):** Distribución simétrica de actores primarios a la izquierda y secundarios a la derecha, relaciones de inclusión (`<<include>>`) y extensión (`<<extend>>`) orientadas según OMG UML 2.5.

---

## 7. Punto de Detención Obligatorio

En estricto cumplimiento del apartado 20 del requerimiento:
- **No se ha iniciado ni modificado ninguno de los otros 23 casos de uso (CUS-002 al CUS-024).**
- El desarrollo queda suspendido a la espera de la revisión y **aprobación expresa del responsable del proyecto** respecto a la estructura, concisión y diseño de este primer caso de uso modelo.
