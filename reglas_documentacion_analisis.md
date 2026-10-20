# Reglas Estándares de Documentación del Proyecto

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT<br>
**Curso:** Construcción de Software I<br>
**Institución:** Universidad Privada de Tacna – Escuela Profesional de Ingeniería de Sistemas<br>
**Equipo Consultor:** C-SharkTeam<br>
**Vigencia:** Semestre 2026-II<br>

---

## Control de Versiones

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcarcel | Dirección EPIS | 26/09/2026 | Creación de directrices formales: granularidad en fase de análisis, estructura quíntuple de cuadros, estándar PlantUML y sincronización continua con `diagramas_general.md`. |
| **1.1** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcarcel | Dirección EPIS | 26/09/2026 | Incorporación de la Regla 6: Estructura canónica y obligatoria de 4 tablas para las narrativas de casos de uso (Sección 6.2.3). |
| **1.2** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcarcel | Dirección EPIS | 26/09/2026 | Incorporación de la Regla 7: Sincronización y actualización continua del README principal (`README.md`) ante cualquier evolución de ingeniería o documentación. |
| **1.3** | Asistencia de Codex a solicitud del equipo | Pendiente | Pendiente | 28/09/2026 | Se explicita fase de análisis y desarrollo del SAD; prevalencia de nomenclatura del SRS y separación entre requisitos, propuestas y resultados de validación. |

---

## 1. Propósito y Alcance

Garantizar la máxima calidad, consistencia metodológica, trazabilidad y rigor técnico en todos los documentos de ingeniería de software del proyecto (con especial énfasis en el **SRS - FD03** y sus artefactos complementarios), asegurando que el contenido sea comprensible, auditable y directamente transferible a la fase de diseño y construcción.

---

## 2. Reglas Fundamentales de Documentación

### Regla 1: Granularidad en Fase de Análisis (Lenguaje Natural Detallado)
* **Contexto de Fase:** El proyecto se encuentra formalmente en la **Fase de Análisis — desarrollo del SAD**. Por consiguiente, las explicaciones no deben ser telegráficas ni limitarse a descripciones superficiales de alto nivel.

* **Fuente de Nomenclatura:** El SAD debe conservar los códigos y denominaciones de módulos, RF, RNF y RN de las tablas 5.1–5.5 del SRS FD03. Para los CUS se usan sus narrativas 6.2.3, en concordancia con dichas tablas. Si otros diagramas del SRS difieren, registrar la inconsistencia sin inventar una nueva numeración ni cambiar silenciosamente la línea base.
* **Estado de la Arquitectura:** Diferenciar requisitos heredados, propuestas arquitectónicas y decisiones pendientes. Las vistas del SAD no prueban implementación, rendimiento, seguridad ni aprobación institucional. Las métricas nuevas requieren justificación y revisión; no deben reemplazar los RNF existentes.
* **Profundidad Narrativa:** Toda especificación, requisito, flujo de proceso y caso de uso debe desarrollarse mediante una **narrativa exhaustiva y granular en lenguaje natural**, detallando:
  * El contexto institucional dentro de la EPIS-UPT.
  * El problema específico que atiende.
  * Las decisiones tomadas, los actores involucrados y las reglas de negocio vinculadas.
  * Los cursos formativos objetivo (*Cálculo, Algoritmos, POO*) y el marco legal peruano (*Ley N° 29733* y *Ley N° 30220, Art. 40*).

---

### Regla 2: Estructura Estándar Obligatoria para Cuadros y Tablas
Todo cuadro o tabla que se incluya en la documentación debe respetar obligatoriamente una **estructura de 5 elementos secuenciales**, evitando insertar tablas aisladas sin contexto:

1. **Presentación Previa:** Párrafo narrativo introductorio que contextualiza el propósito del cuadro, explicando la necesidad del análisis y qué información se va a presentar.
2. **Título Formal:** Encabezado numerado y descriptivo en formato Markdown (ej. `### Cuadro 5.3: Matriz de Requerimientos Funcionales Finales`).
3. **Cuadro / Tabla:** Estructurada estrictamente en sintaxis **Markdown** limpia, con alineación explícita de columnas y codificación UTF-8.
4. **Fuente:** Declaración formal inmediatamente debajo de la tabla (`Fuente: Elaboración propia.` o la cita bibliográfica respectiva).
5. **Explicación / Conclusión Posterior:** Párrafo de análisis, interpretación de los datos expuestos, impacto en la arquitectura/negocio y deducción de conclusiones directas a partir de la tabla.

```markdown
<!-- Ejemplo de Aplicación de la Regla 2 -->
A continuación, se presenta la distribución de prioridades funcionales... [Presentación previa]

### Cuadro X.X: Título Descriptivo del Cuadro

| Código | Parámetro | Criterio de Evaluación | Impacto |
| :--- | :--- | :--- | :--- |
| P01 | Similitud Coseno | Vectores curriculares de cursos filtro | Crítico |

Fuente: Elaboración propia.

Como se observa en el cuadro anterior, el parámetro P01 determina... [Explicación y conclusión posterior]
```

---

### Regla 3: Formato Exclusivo para Diagramas (PlantUML)
* **Estándar Gráfico:** Todos los diagramas (casos de uso, secuencia, actividades, clases, paquetes, estados, despliegue, organigramas) deben estar codificados en **PlantUML** (`@startuml ... @enduml`).
* **Directrices de Modelado:**
  * Uso de `skinparam` limpio, sin sombras pesadas (`skinparam shadowing false`), tipografía legible (`defaultFontName Arial`) y paleta monocromática o corporativa sobria (`#F8F9FA`, `#2B3A42`, `#1D2D44`).
  * Enfoque directo, conciso y funcional: mostrar únicamente la información requerida sin sobrecargar el gráfico.
  * Estructuración modular mediante paquetes (`package`) y particiones (`|Lane|`).

---

### Regla 4: Formato de Texto y Codificación
* **Formato de Archivo:** Todos los archivos de documentación son texto plano en formato Markdown (`.md`).
* **Codificación:** UTF-8 estricto sin BOM.
* **Idioma:** Español formal académico, manteniendo en inglés únicamente acrónimos técnicos estándar (*JWT, 2FA, RecSys, RLS, API, SPA, Top-k, SUS*).

---

### Regla 5: Regla de Sincronización y Hardening (`diagramas_general.md`)
* **Repositorio Central Sincronizado:** El archivo [`docs/diagramas_general.md`](file:///C:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/diagramas_general.md) actúa como la **bóveda consolidada y de hardening** de todos los artefactos visuales y tabulares del proyecto.
* **Actualización Automática y Continua:** A medida que se avance, elabore o actualice cualquier diagrama PlantUML, cuadro matricial o esquema dentro del documento SRS ([FD03](file:///C:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md)), dicho artefacto **debe agregarse y sincronizarse inmediatamente en `diagramas_general.md`**, manteniendo una copia consistente. Para el SAD y su complemento de secuencias, se sincronizan igualmente los diagramas y cuadros en su sección propia de la bóveda, sin modificar los artefactos heredados del SRS.

---

### Regla 6: Estructura Estándar para Narrativas de Casos de Uso (Sección 6.2.3)
Todas las narrativas individuales de casos de uso (desde `CUS01` hasta `CUS24`) en la sección **6.2.3** deben estructurarse obligatoriamente bajo el siguiente esquema canónico compuesto por **cuatro tablas Markdown estandarizadas**:

```markdown
### CUSXX - [Nombre del Caso de Uso]

| Campo | Descripción |
|---|---|
| **Código** | CUSXX |
| **Nombre** | Denominación oficial normalizada |
| **Tipo** | Primario / Secundario / Soporte, Esencial |
| **Requerimiento asociado** | RFXX (provisional) / Reglas de negocio |
| **Actor principal** | Rol humano, servicio cron o administrador que inicia la interacción |
| **Actores secundarios** | Participantes, receptores de alertas o servicios externos |
| **Módulo relacionado** | Módulo funcional principal (MOD-01 al MOD-08) |
| **Propósito** | Razón de ser y meta fundamental que persigue el caso de uso |
| **Descripción** | Explicación narrativa detallada y granular del proceso |
| **Resultado esperado** | Estado final del sistema y valor entregado al usuario/institución |

### Flujo Principal

| N.° | Acción del actor | Respuesta del sistema |
|---|---|---|
| 1 | Paso a paso de la acción del actor | Comportamiento, validación y persistencia del sistema |

### Flujos Alternativos

| Código | Situación | Acción del actor | Respuesta del sistema |
|---|---|---|---|
| FA01 | Condición o desvío alternativo del flujo | Acción ejecutada ante la variante | Respuesta adaptativa del sistema |

### Eventos de Excepción

| Código | Evento de excepción | Respuesta del sistema |
|---|---|---|
| E01 | Error técnico, validación fallida o corte de regla | Notificación, bloqueo seguro o registro de auditoría |
```

---

### Regla 7: Sincronización y Actualización Continua del README Principal (`README.md`)
* **Rol Estratégico:** El archivo [`README.md`](file:///C:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/README.md) en la raíz del repositorio constituye la carta de presentación oficial, la vitrina pública y la guía central de navegación arquitectónica y operativa del proyecto ante docentes, comités de evaluación y evaluadores externos.
* **Gatillo de Actualización Obligatoria:** Ante cualquier modificación, adición o avance estructural en la documentación (`docs/`), modelado lógico UWE, refinamiento de casos de uso, ampliación de reglas de negocio, o evolución del código de frontend/backend, el `README.md` **debe ser actualizado de forma sincronizada y obligatoria en el mismo ciclo de trabajo**.
* **Contenido Mínimo Canónico del README:**
  1. **Encabezado Institucional:** Metadatos completos (Institución, Facultad, Escuela EPIS-UPT, Curso, Autores, Docente de cátedra, Semestre).
  2. **Resumen de la Solución y Alcance:** Contexto de la problemática de reprobación, asignaturas críticas, propuesta de valor P2P y motor de recomendación híbrido *Top-k*.
  3. **Índice y Enlaces a la Documentación Oficial:** Acceso directo y verificable a los entregables canónicos (`FD01`, `FD02`, `FD03 - SRS`, `FD04`, `resumen_sistema_y_casos_de_uso.md`, `diagramas_general.md`, `matriz_inconsistencias.md`, `Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` y `reglas_documentacion.md`).
  4. **Árbol de Directorios del Repositorio:** Estructura de carpetas fidedigna, completa y actualizada, detallando la función de cada archivo.
  5. **Módulos y Casos de Uso Clave:** Resumen de módulos funcionales y flujo operativo del sistema.
  6. **Instrucciones de Despliegue y Ejecución:** Guía paso a paso para levantar el entorno de desarrollo (maqueta frontend, servicios backend y base de datos).
  7. **Marco Regulatorio y Ético:** Respaldo normativo explícito bajo la Ley N° 29733 de Protección de Datos Personales del Perú.

---

## 3. Matriz de Cumplimiento de Reglas

| Elemento Documental | Regla Aplicable | Validación de Conformidad |
| :--- | :--- | :--- |
| **Secciones Narrativas** | Regla 1 | Lenguaje natural granular, sin omisiones conceptuales. |
| **Tablas y Matrices Generales** | Regla 2 | Cumplimiento del ciclo: Presentación → Título → Tabla MD → Fuente → Conclusión. |
| **Diagramas UML** | Regla 3 | Bloque de código PlantUML ejecutable y validado. |
| **Archivos .md** | Regla 4 | UTF-8, Markdown estructurado (`#`, `##`, `###`). |
| **Hardening de Artefactos** | Regla 5 | Reflejo inmediato en `docs/diagramas_general.md`. |
| **Narrativas de Casos de Uso (6.2.3)** | Regla 6 | Esquema canónico de 4 tablas (Ficha, Flujo Principal, Alternativos, Excepciones). |
| **README Principal (`README.md`)** | Regla 7 | Sincronización continua de árbol de directorios, catálogo de entregables, estado de ingeniería e instrucciones de despliegue. |
