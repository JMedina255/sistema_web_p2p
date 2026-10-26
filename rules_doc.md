# Reglas de Documentación del Proyecto

Este documento registra las reglas, estándares y convenciones acordadas para la elaboración y mantenimiento de la documentación del proyecto **Sistema Web P2P**.

---

## 1. Propósito
Establecer un conjunto de directrices claras que garanticen la consistencia, calidad, legibilidad y mantenibilidad de toda la documentación generada a lo largo del desarrollo del proyecto.

---

## 2. Estructura y Formato General
- **Formato principal:** Toda la documentación en texto plano debe estar en Markdown (`.md`).
- **Codificación:** UTF-8.
- **Idioma:** Español (manteniendo términos técnicos o nombres de librerías/APIs en inglés cuando sea estándar).
- **Encabezados:** Jerarquía clara usando sintaxis Markdown (`#`, `##`, `###`).

---

## 3. Reglas Específicas

### 3.1. Generación de Diagramas y Gráficos
- **Formato:** Todos los gráficos y diagramas generados deben estar escritos en código compatible con el editor de **PlantUML**.
- **Estilo:** Deben ser sencillos, concisos y directos al grano, mostrando únicamente la información necesaria requerida sin sobrecargar el diagrama.

### 3.2. Informes Académicos de Sprint

Para garantizar la uniformidad, rigor y auditabilidad de las entregas académicas en el marco del curso de Construcción de Software I, los informes de sprint se regirán por las siguientes directrices obligatorias:

1. **Formatos y Fuentes Oficiales:**
   - **Markdown (`.md`):** Constituye la fuente técnica primaria, reproducible y versionada en el repositorio GitHub (`docs/sprints/` y `docs/diseño/`). Toda evolución técnica debe registrarse primero en este formato.
   - **DOCX / Google Docs:** Constituye el formato editable para la entrega y presentación académica formal requerida por la cátedra, manteniendo correspondencia biunívoca con el contenido del archivo Markdown.

2. **Estructura Institucional Canónica (Once Secciones):**
   Todos los informes de desarrollo de sprint deben conservar obligatoriamente la estructura formal de once secciones estandarizada desde el Sprint 01:
   - **1. Introducción:** Contexto del curso, propósito del informe, periodo y commit evaluado.
   - **2. Presentación breve del proyecto:** Problemática, propósito institucional, actores y alcance del incremento.
   - **3. Planificación general de los sprints:** Visión del Product Backlog, calendario y articulación del sprint actual respecto a las iteraciones previas y posteriores.
   - **4. Descripción y planificación del sprint informado:** Objetivo, alcance comprometido, tabla quíntuple de tareas, criterios de verificación y entorno de corte.
   - **5. Desarrollo del sprint y evidencias de verificación:** Desglose granular de hitos/tareas, diseño técnico, contratos REST/TypeScript, pruebas ejecutadas, aseguramiento de la calidad e incidencias/desviaciones.
   - **6. Balance de los ítems del Product Backlog:** Criterios de reporte, matriz de estado de los PBI comprometidos y dictamen de aceptación del incremento.
   - **7. Importancia y dependencias del trabajo que continúa:** Contribución al producto integral, dependencias críticas entre subsistemas y condiciones de entrada.
   - **8. Conclusiones del sprint:** Juicios técnicos sobre el cumplimiento de objetivos y madurez del incremento.
   - **9. Recomendaciones para los siguientes sprints:** Lecciones aprendidas por el equipo y medidas preventivas/correctivas.
   - **10. Referencias y documentos de respaldo:** Enlaces a normas (ISO/IEC, Leyes peruanas, IEEE), artefactos del repositorio y documentación técnica oficial.
   - **11. Anexos y control de la entrega:** Índice formal de figuras/capturas, reportes métricos complementarios y lista de verificación previa a la presentación.

3. **Trazabilidad Integral y Gobernanza:**
   Cada entrega debe acreditar trazabilidad explícita y bidireccional entre los artefactos del sistema:
   $$\text{PBI} \longleftrightarrow \text{RF / RNF} \longleftrightarrow \text{CUS} \longleftrightarrow \text{RN} \longleftrightarrow \text{Tarea (T-xx)} \longleftrightarrow \text{Commit Git} \longleftrightarrow \text{Casos de Prueba} \longleftrightarrow \text{Evidencia Empírica}$$

4. **Estándar Riguroso de Evidencias Visuales y Capturas:**
   Toda captura o figura incorporada en los informes debe contar con metadatos de auditoría:
   - Título formal y numerado (ej. *Figura 5.1: Formulario reactivo de publicación de ofertas*).
   - Fuente explícita (comando ejecutado, entorno o interfaz).
   - Fecha exacta de captura y rama evaluada.
   - Entorno de ejecución claramente identificado (*Entorno Local Alfa*, *Staging*, *GitHub Actions CI*).
   - Delimitación técnica de alcance: explicar con precisión qué comportamiento demuestra la captura y qué elementos corresponden a datos simulados o componentes aún no integrados.

5. **Tratamiento de Informes Parciales y Cierre Definitivo:**
   - **Informes Parciales:** Cuando un integrante culmine su asignación (ej. Joan en frontend) y las tareas del otro integrante (ej. Renzo en backend) sigan en curso, el informe registrará formalmente el estado de estas últimas como **PENDIENTE DE IMPLEMENTACIÓN ⏳**, habilitando las plantillas de documentación sin inventar resultados, métricas ni firmas de conformidad.
   - **Cierre Definitivo del Sprint:** La declaración de cierre integral del sprint requerirá el cumplimiento pleno de los criterios de aceptación de la totalidad de tareas y la satisfacción rigurosa de los criterios del **Definition of Done (DoD)** conjunto.

6. **Separación Estricta de Niveles de Madurez del Software:**
   Se prohíbe terminantemente simular persistencia real o declarar operativas funcionalidades dependientes de servicios no construidos. Se debe distinguir nítidamente entre:
   - *Funcionalidades reales:* persistidas con transaccionalidad ACID en PostgreSQL/Supabase y validadas por API.
   - *Adaptadores mock:* almacenamiento volátil en memoria o `localStorage` señalizado explícitamente al usuario.
   - *Prototipos y maquetas:* componentes de referencia visual.
   - *Integraciones pendientes:* llamadas de red o microservicios externos diferidos.

7. **Tratamiento Independiente de Métricas de Cobertura (RNF09):**
   - La cobertura de pruebas automatizadas se medirá y reportará de manera **estrictamente independiente**:
     - Cobertura de Frontend: calculada mediante Vitest y su motor v8.
     - Cobertura de Backend: calculada mediante Pytest y Pytest-Cov.
   - Queda prohibido promediar o calcular porcentajes de cobertura agregada o "ponderada" entre frontend y backend sin una metodología formal unificada de instrumentación que consolide líneas ejecutadas absolutas.

8. **Control de Versiones y Fechas de Corte:**
   Todo informe iniciará con una tabla de Control de Versiones (Versión, Fecha, Responsable, Revisión/Aprobación, Descripción de Cambios) y fijará una fecha de corte documental verificable con los commits del repositorio.

9. **Inmutabilidad de Documentos de Requisitos y Arquitectura en Cierres Ordinarios:**
   Los documentos canónicos de especificación de requisitos (**SRS / FD03**) y de arquitectura de software (**SAD / FD04**) constituyen la línea base formal del proyecto y **no deben modificarse como parte de las bitácoras o cierres ordinarios de sprint**, reservando su actualización exclusivamente a procesos formales de control de cambios o revisiones mayores de fase debidamente aprobadas.

---

## 4. Historial de Reglas y Modificaciones

| Fecha | Regla / Cambio Registrado | Descripción / Notas |
| :--- | :--- | :--- |
| 2026-09-05 | Creación de `rules_doc.md` | Establecimiento de la estructura inicial del archivo de reglas. |
| 2026-09-05 | Regla 3.1: Diagramas en PlantUML | Definición de PlantUML como formato estándar para gráficos sencillos y directos. |
| 2026-10-26 | Regla 3.2: Informes Académicos de Sprint | Estandarización de informes en Markdown/DOCX con estructura institucional de 11 secciones, trazabilidad integral, evidencias delimitadas, separación de mocks vs persistencia real, métricas de cobertura independientes y preservación de SRS/SAD. |
