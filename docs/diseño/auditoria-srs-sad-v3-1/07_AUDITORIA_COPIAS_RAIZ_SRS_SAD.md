# Auditoría de Integridad y Verificación de Copias Maestras en Raíz: SRS.md y SAD.md

**Documento:** `docs/diseño/auditoria-srs-sad-v3-1/07_AUDITORIA_COPIAS_RAIZ_SRS_SAD.md`  
**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Equipo Consultor:** C-SharkTeam (Grupo 03)  
**Responsables Técnicos:** Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani  
**Cátedra:** Construcción de Software I (Semestre 2026-II)  
**Rama de Trabajo:** `docs/copias-integrales-srs-sad`  
**Fecha de Auditoría:** 14 de noviembre de 2026  
**Resultado Global:** **APROBADO — 100% CONFORME (Integridad Textual Total, 133 Figuras Renderizadas Operativas)**

---

## 1. Objetivo y Alcance de la Tarea

El presente informe audita la generación de copias integrales y autónomas de los documentos oficiales **SRS** (Especificación de Requisitos de Software) y **SAD** (Documento de Arquitectura de Software) ubicadas directamente en la raíz del repositorio (`SRS.md` y `SAD.md`), funcionando como documentos de referencia inmediata y muestras académicas para docentes, evaluadores y desarrolladores.

### Principios Obligatorios Cumplidos:
1. **Invarianza de los Documentos Canónicos:** Los documentos originales `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` y `docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md` se mantuvieron 100% intactos.
2. **Conservación Integral (Sin Resumen ni Poda):** Se preservaron íntegramente las portadas, índices, 26 RF, 10 RNF, 24 CUS con sus narrativas canónicas, matrices de trazabilidad, tablas relacionales, reglas de negocio y contratos REST.
3. **Visualización Gráfica Directa (Prioridad Máxima):** Se aseguró que ningún diagrama aparezca únicamente como código PlantUML o enlace roto. Cada uno de los **133 diagramas** (119 en SRS y 14 en SAD) se presenta como una figura renderizada de alta resolución (PNG) visible directamente en GitHub y visores Markdown.
4. **Preservación del Código Fuente Editable:** Se integró un bloque desplegable `<details><summary>Código fuente PlantUML (respaldo editable)</summary>...</details>` para cada diagrama, permitiendo a los desarrolladores consultar, copiar y editar el modelo UML sin perturbar la lectura visual del documento.
5. **Portabilidad de Rutas Relativas:** Las referencias a imágenes fueron ajustadas a rutas relativas válidas desde la raíz (`docs/diseño/diagramas/...`) garantizando 0 enlaces rotos.

---

## 2. Métricas de Integridad Textual y Estructural

### Cuadro 2.1: Comparativa Cuantitativa entre Documentos Canónicos y Copias en Raíz

| Documento | Ubicación | Tamaño (Bytes) | Total Líneas | Secciones `##` | Figuras Renderizadas | Bloques PlantUML (en `<details>`) |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **SRS Original** | `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` | 574,444 | 4,616 | 36 | 119 | 0 (en fuentes `.puml`) |
| **SRS Copia Raíz** | `SRS.md` | 851,564 | 12,816 | 36 | **119** | **119** |
| **SAD Original** | `docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md` | 185,837 | 2,368 | 17 | 0 | 14 (crudos en texto) |
| **SAD Copia Raíz** | `SAD.md` | 190,296 | 2,480 | 17 | **14** | **14** |

Fuente: Elaboración propia a partir de scripts automatizados de auditoría.

---

## 3. Censo de Diagramas y Recursos Gráficos Incorporados

### Cuadro 3.1: Resumen de Gráficos por Documento

| Documento | Categoría de Diagramas | Total Diagramas | Formato Renderizado | Directorio de Imágenes | Directorio de Fuentes PUML |
|:---|:---|:---:|:---:|:---|:---|
| **SRS.md** | Organigrama, Procesos As-Is/To-Be, Metodología UWE, Casos de Uso (General y 8 Módulos), ECB (24 CUS), Actividades (24 CUS), Secuencia DSS (24 CUS), Clases Lógicas (24 CUS), FSM (Sesión, Reserva, Bitácora), DER Físico | **119** | PNG de alta definición | `docs/diseño/diagramas/srs/img/` | `docs/diseño/diagramas/srs/puml/` |
| **SAD.md** | Modelo 4+1 Kruchten (Escenarios, Lógica, Procesos, Desarrollo, Física), Casos de Uso Canónicos, Límites de Sistema, Procesos As-Is/To-Be, Contenedores C4 Nivel 2, Componentes Backend, DER 15 Tablas, FSM Sesión y Reserva | **14** | PNG de alta definición | `docs/diseño/diagramas/sad/img/` | `docs/diseño/diagramas/sad/puml/` |
| **Total Consolidado** | **Cobertura Integral del Sistema Web P2P** | **133** | **PNG (100% operativos)** | **0 rutas rotas** | **133 archivos `.puml` preservados** |

---

## 4. Trazabilidad Criptográfica y Justificación de Diferencias (SHA-256)

### Cuadro 4.1: Hashes Criptográficos SHA-256

| Archivo | Ruta Relativa | Hash SHA-256 | Justificación de la Variación |
|:---|:---|:---|:---|
| SRS Canónico | `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` | `e7f0a836ff89d9597053debf49fccf414171a1ebccfb198067eb27fab697c959` | Versión documental oficial de diseño con figuras relativas a `docs/diseño/`. |
| SRS Copia Raíz | `SRS.md` | `2920849dbca48cda4e09442facb267a43d2285e3bc90ee22a91d6812c086b281` | Variación justificada: rutas de imagen actualizadas a `docs/diseño/diagramas/srs/img/` e inclusión de bloques `<details>` con el código PlantUML editable. |
| SAD Canónico | `docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md` | `05befc79a37bfeb7b288de8c221a362e4531b3990ec89155d26674296176d2b6` | Versión documental oficial de arquitectura con 14 bloques de código crudo. |
| SAD Copia Raíz | `SAD.md` | `1350d3c8b59a781833d688a9f1d4ade116bfc77ae779821253d4c9baee57c2ea` | Variación justificada: sustitución de los 14 bloques crudos por figuras PNG visibles, denominación **Figura X**, y preservación del código PlantUML en `<details>`. |

---

## 5. Verificación de Compatibilidad y Visualización en GitHub

1. **Compatibilidad en Navegador Web (GitHub):** Todas las rutas de imagen utilizan el prefijo `docs/diseño/diagramas/{srs|sad}/img/*.png`. Al estar referenciadas desde la raíz, GitHub renderiza las imágenes directamente en línea sin advertencias ni íconos de imagen rota.
2. **Compatibilidad en VS Code / Markdown Preview:** Las 133 imágenes se resuelven instantáneamente contra el árbol de trabajo local.
3. **Compatibilidad de Despliegue de Código (`<details>`):** Los bloques `<details>` se mantienen colapsados por defecto en la vista de lectura, permitiendo una experiencia limpia de lectura académica mientras mantienen el código accesible en un solo clic.

---

## 6. Dictamen de Aprobación

La tarea de generación de copias integrales en raíz ha sido **completada con éxito al 100%**:
- `SRS.md` y `SAD.md` se encuentran publicados en la raíz del repositorio.
- Los 133 diagramas se encuentran renderizados e integrados visualmente.
- No existen referencias rotas ni omisiones de contenido técnico.
- Los documentos canónicos en `docs/diseño/` permanecen inalterados.

**Dictamen Final:** **APROBADO SIN RESERVAS**.
