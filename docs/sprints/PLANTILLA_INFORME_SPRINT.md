# Informe de desarrollo y resultados — Sprint {{NN}}

## «{{NOMBRE_DEL_SPRINT}}»

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT.  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas.  
**Curso:** Construcción de Software I.  
**Docente de cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado.  
**Semestre académico:** 2026-II.  
**Equipo:** Grupo 03 / C-SharkTeam.  
**Integrantes:** Joan Cristian Medina Quispe (2022074255) y Renzo Antonio Antayhua Mamani (2022073504).  
**Periodo planificado:** {{FECHA_INICIO_PLANIFICADA}}–{{FECHA_FIN_PLANIFICADA}}.  
**Periodo real documentado:** {{FECHA_INICIO_REAL}}–{{FECHA_CORTE_REAL}}.  
**Fecha de presentación:** {{FECHA_PRESENTACION}}.  
**Repositorio:** [sistema_web_p2p](https://github.com/JMedina255/sistema_web_p2p).  
**Rama y commit evaluados:** {{RAMA}} / {{SHA_COMPLETO_Y_ENLACE}}.  
**Estado del informe:** {{BORRADOR_EN_REVISION_O_VERSION_FINAL}}.  
**Balance del sprint al corte:** {{OBJETIVO_LOGRADO_PARCIALMENTE_LOGRADO_O_NO_LOGRADO_CON_JUSTIFICACION}}.

<!--
INSTRUCCIONES DE USO DE LA PLANTILLA — retirar este comentario de la entrega final.

1. Ubicación sugerida: docs/diseño/PLANTILLA_INFORME_SPRINT.md.
   Crear el informe en esa misma carpeta como INFORME_GENERAL_SPRINT_{{NN}}.md.
   Para S1, integrar la nueva estructura con INFORME_GENERAL_SPRINT_01.md,
   conservando sus evidencias y el historial. No generar dos informes finales
   contradictorios del mismo sprint.
2. Sustituir todos los marcadores {{...}}. Si un dato no está disponible, escribir
   «No registrado», «No medido», «No verificado» o «No aplica: [motivo]».
3. Esta es una plantilla del equipo basada en las reglas del repositorio;
   no constituye un formato oficial aprobado por el docente. Incorporar una
   rúbrica o formato adicional si la cátedra lo proporciona.
4. Conservar los IDs originales PB-xxx, T-xx, RFxx, RNFxx, CUSxx y RN-xx.
   Product Backlog es el conjunto; PBI es cada ítem; tarea es una actividad.
   Un hito puede agrupar tareas o dividir una tarea. No son equivalentes.
5. Toda tabla conserva cinco elementos: presentación, título numerado,
   tabla alineada, fuente específica y análisis posterior. No atribuir a la
   cátedra o a una norma una meta que solo esté definida en el SRS del equipo.
6. Cada captura debe vincularse con un hito, tarea o prueba; incluir contexto,
   resultado esperado, resultado observado, fecha, entorno y commit. Una
   captura de interfaz o un archivo SQL no prueban por sí solos persistencia,
   envío de correo, autorización, aplicación de RLS ni ejecución satisfactoria.
7. Informar por separado código implementado, verificación e integración.
   Identificar explícitamente demostración, mocks, memoria, BD local o Supabase.
   No declarar aceptación, aprobación docente u horas ejecutadas sin registro.
8. Consultar el SRS/SAD de diseño y enlazar contratos, diccionario de datos,
   máquinas de estado y ADR existentes. Si cambia el diseño, actualizar su
   fuente canónica. Usar PlantUML para diagramas y sincronizar la bóveda vigente.
9. Conservar evidencia reproducible: comandos, reportes, logs sanitizados,
   commit y enlace de CI. Ocultar contraseñas, cadenas de conexión, tokens JWT,
   claves privadas y datos personales innecesarios en texto, imágenes y anexos.
10. Actualizar README.md y docs/sprints/sprint-{{NN}}.md al incorporar el informe
    al repositorio. La creación de esta plantilla no modifica dichos archivos.

BASE DE PREPARACIÓN: main, commit 2ae4f92ab75db22fc8418b2e172e7ffd8cb21a88,
consultado el 19/10/2026 (America/Lima). La ruta y el contenido de los documentos
fuente deben comprobarse nuevamente al elaborar cada informe.
-->

### Control de versiones del informe

El control de versiones permite identificar qué información se incorporó y quién participó en su revisión. Se registran las revisiones y aprobaciones efectivamente realizadas.

#### Cuadro 0.1: Historial de versiones del informe

| Versión | Fecha | Responsable | Revisión / aprobación registrada | Cambio realizado |
| :---: | :---: | :--- | :--- | :--- |
| 0.1 | {{FECHA}} | {{AUTOR_O_AUTORES}} | Pendiente de revisión | Elaboración inicial del informe del Sprint {{NN}}. |

Fuente: historial de edición del informe y registros de revisión {{ENLACES_O_REFERENCIAS}}.

{{EXPLICAR_LA_VERSION_VIGENTE_Y_LO_QUE_FALTA_REVISAR_SIN_DAR_POR_HECHA_LA_APROBACION}}.

### Índice

1. Introducción.
2. Presentación breve del proyecto.
3. Planificación general de los sprints.
4. Descripción y planificación del sprint informado.
5. Desarrollo del sprint y evidencias de verificación.
6. Balance de los ítems del Product Backlog.
7. Importancia y dependencias del trabajo que continúa.
8. Conclusiones del sprint.
9. Recomendaciones para los siguientes sprints.
10. Referencias y documentos de respaldo.
11. Anexos y control de la entrega.

## 1. Introducción

{{REDACTAR_DOS_O_TRES_PARRAFOS_QUE_EXPLIQUEN_EL_CONTEXTO_DEL_CURSO_EL_PROPOSITO_DEL_INFORME_EL_SPRINT_ANALIZADO_Y_SU_FECHA_DE_CORTE}}.

El presente informe documenta el trabajo del Sprint {{NN}}, denominado «{{NOMBRE_DEL_SPRINT}}», y contrasta los entregables previstos con los resultados observados. Su alcance comprende {{ALCANCE_DEL_INFORME}}, con evidencia correspondiente al periodo {{PERIODO_REAL}} y al commit {{COMMIT_EVALUADO}}.

{{EXPLICAR_COMO_SE_ORGANIZA_EL_INFORME_Y_QUE_FUENTES_RESPALDAN_LAS_AFIRMACIONES}}.

<!-- La introducción presenta el informe; el apartado 2 presenta el producto.
Evitar repetir aquí toda la problemática, arquitectura o lista de tareas. -->

## 2. Presentación breve del proyecto

### 2.1. Problemática y contexto

{{DESCRIBIR_DE_FORMA_BREVE_LA_NECESIDAD_DE_MENTORIAS_ACADEMICAS_EN_LA_EPIS_UPT_Y_EL_PROBLEMA_QUE_ATIENDE_EL_PROYECTO_CON_APOYO_EN_VISION_Y_SRS}}.

### 2.2. Propósito, usuarios y valor esperado

{{EXPLICAR_EL_OBJETIVO_DEL_SISTEMA_LOS_USUARIOS_PREVISTOS_Y_EL_VALOR_DE_LA_RECOMENDACION_DE_MENTORIAS_SIN_PRESENTAR_FUNCIONES_FUTURAS_COMO_YA_IMPLEMENTADAS}}.

### 2.3. Solución tecnológica y alcance del incremento

La solución utiliza una interfaz React con Vite, una API FastAPI y PostgreSQL mediante Supabase. {{DESCRIBIR_EL_PAPEL_DE_CADA_CAPA_Y_ENLAZAR_EL_SAD_VIGENTE}}.

{{DISTINGUIR_LA_VISION_DEL_PRODUCTO_COMPLETO_DEL_INCREMENTO_REAL_DISPONIBLE_EN_ESTE_SPRINT}}.

## 3. Planificación general de los sprints

### 3.1. Organización del desarrollo

{{EXPLICAR_POR_QUE_EL_DESARROLLO_SE_ORGANIZA_EN_INCREMENTOS_Y_COMO_CADA_SPRINT_APORTA_A_LA_SOLUCION_FINAL}}.

La siguiente planificación resume la secuencia prevista para los ocho sprints. Las fechas y horas corresponden a la línea base del plan; el avance real se registra en el apartado 6 de este informe.

### Cuadro 3.1: Panorama de los ocho sprints planificados

| Sprint | Objetivo o incremento previsto | Periodo planificado | Presentación prevista | Esfuerzo planificado |
| :---: | :--- | :---: | :---: | ---: |
| S1 | Base técnica y acceso inicial. | 13–18/10/2026 | 19/10/2026 | 18 h |
| S2 | Roles, currículo y perfiles. | 19–23/10/2026 | 24/10/2026 | 14 h |
| S3 | Publicación de ofertas. | 24–25/10/2026 | 26/10/2026 | 5 h |
| S4 | Recomendación Top-k y reservas. | 26–30/10/2026 | 31/10/2026 | 15 h |
| S5 | Ratificación y desistimiento. | 31/10–01/11/2026 | 02/11/2026 | 5 h |
| S6 | Quórum y bitácoras. | 02–06/11/2026 | 07/11/2026 | 14 h |
| S7 | Encuestas y visado de horas. | 07–08/11/2026 | 09/11/2026 | 5 h |
| S8 | Integración y demostración del MVP. | 09–13/11/2026 | 14/11/2026 | 15 h |

Fuente: [Plan de sprints y distribución de tareas](../sprints/PLAN_SPRINTS_Y_TAREAS.md), versión 1.1 del 19/10/2026, apartados 2 y 4. Confirmar su vigencia antes de emitir el informe.

{{EXPLICAR_LA_SECUENCIA_DE_DEPENDENCIAS_Y_LA_UBICACION_DEL_SPRINT_ACTUAL_EN_EL_PLAN}}. Las 91 h de esta línea base representan esfuerzo planificado; su ejecución real requiere registros independientes.

### 3.2. Relación del sprint actual con los anteriores

{{DESCRIBIR_LO_QUE_SE_RECIBIO_DEL_SPRINT_ANTERIOR_Y_LO_QUE_DEBE_HABILITAR_EL_ACTUAL}}.

<!-- En S1, describir la línea base documental y la maqueta previa; no inventar
un Sprint 0. Registrar desviaciones de fechas o alcance si las hubo. -->

## 4. Descripción y planificación del sprint informado

### 4.1. Objetivo del sprint

**Objetivo general:** {{EXPRESAR_EL_RESULTADO_CONCRETO_QUE_EL_SPRINT_BUSCA_ENTREGAR}}.

**Resultados específicos previstos:**

1. {{RESULTADO_VERIFICABLE_1}}.
2. {{RESULTADO_VERIFICABLE_2}}.
3. {{RESULTADO_VERIFICABLE_3}}.

<!-- Referencia S1: comunicar React–FastAPI–PostgreSQL/Supabase, habilitar acceso
de prueba, preparar el catálogo inicial, la protección de datos y el CI inicial.
No convertir este alcance en una afirmación de autenticación institucional final. -->

### 4.2. Alcance comprometido y distribución de tareas

El cuadro relaciona las tareas comprometidas con sus PBI y requisitos. Los criterios de aceptación deben proceder de la planificación, el SRS o un acuerdo registrado; cualquier criterio adicional se identifica como propuesta.

### Cuadro 4.1: Alcance, responsabilidades y criterios de aceptación

| Tarea | PBI relacionado | RF / RNF / CUS / RN aplicables | Responsable | Horas planificadas | Entregable y criterio verificable |
| :--- | :--- | :--- | :--- | ---: | :--- |
| {{T_ID}} | {{PB_ID}} | {{IDS_CANONICOS_O_TRANSVERSAL}} | {{RESPONSABLE}} | {{HORAS}} | {{ENTREGABLE_Y_CRITERIO_CON_FUENTE}} |

Fuente: {{VERSION_Y_APARTADO_DEL_PLAN_SRS_Y_ACUERDOS_UTILIZADOS}}.

{{EXPLICAR_EL_REPARTO_LAS_DEPENDENCIAS_Y_LO_QUE_SE_EXCLUYO_DEL_COMPROMISO}}.

<!-- Referencia S1: T-01 Joan 4 h; T-02 Joan 2 h; T-03 Renzo 4 h;
T-06 Joan 3 h; T-07 Renzo 3 h; T-09 Renzo 2 h. PBI previstos:
PB-001, PB-002, PB-004, PB-006 y PB-008. Confirmar el mapeo tarea–PBI
en la fuente y no asumir que todos los PBI se completan íntegramente en S1. -->

### 4.3. Condiciones de verificación y terminación

{{IDENTIFICAR_LA_DEFINICION_DE_TERMINADO_ACORDADA_Y_SU_FUENTE}}. Para emitir el balance se revisan los criterios de aceptación, los artefactos, las pruebas pertinentes, la integración y la documentación exigida para el alcance comprometido.

{{INDICAR_QUE_CRITERIOS_SE_VERIFICARAN_EN_EL_APARTADO_5_Y_QUIEN_REGISTRA_O_REVISA_LA_ACEPTACION}}.

### 4.4. Entorno y punto de corte

La identificación del entorno permite reproducir los resultados y separar las comprobaciones locales de las realizadas en integración continua o servicios externos.

### Cuadro 4.2: Entorno de ejecución y referencias de la versión evaluada

| Elemento | Versión o valor observado | Entorno / modo | Fuente de comprobación |
| :--- | :--- | :--- | :--- |
| Código evaluado | {{RAMA_Y_SHA_COMPLETO}} | {{LOCAL_O_REMOTO}} | {{COMMIT_O_PR}} |
| Frontend y herramientas | {{NODE_NPM_REACT_VITE_VITEST_ESLINT}} | {{MODO_Y_SISTEMA_OPERATIVO}} | {{COMANDOS_Y_LOCKFILE}} |
| Backend y herramientas | {{PYTHON_FASTAPI_SQLALCHEMY_ALEMBIC_PYTEST_RUFF}} | {{ENTORNO_VIRTUAL_Y_SISTEMA}} | {{COMANDOS_Y_DEPENDENCIAS}} |
| Persistencia | {{MOTOR_VERSION_Y_MIGRACION_APLICADA}} | {{MEMORIA_LOCAL_SUPABASE_O_NO_PROBADO}} | {{REPORTE_SANITIZADO}} |
| Integración continua | {{WORKFLOW_RUN_ID_FECHA_Y_SHA}} | GitHub Actions | {{ENLACE_AL_RUN_Y_ARTEFACTOS}} |

Fuente: {{REPORTES_Y_COMANDOS_OBTENIDOS_EN_LA_FECHA_DE_CORTE}}.

{{EXPLICAR_DIFERENCIAS_ENTRE_ENTORNOS_Y_SU_EFECTO_EN_LA_INTERPRETACION}}. La versión declarada en un archivo de configuración no sustituye la comprobación del entorno donde se ejecutó la prueba.

## 5. Desarrollo del sprint y evidencias de verificación

### 5.1. Secuencia de trabajo e hitos

{{PRESENTAR_EL_ORDEN_DE_TRABAJO_Y_EL_MOTIVO_DE_LAS_DEPENDENCIAS}}. Cada hito debe identificarse con el código que ya utiliza la bitácora del sprint.

### Cuadro 5.1: Secuencia de hitos y entregables

| Hito | Tareas / PBI | Actividad principal | Artefacto generado | Commit / PR | Evidencia vinculada |
| :--- | :--- | :--- | :--- | :--- | :--- |
| {{HITO_EXISTENTE}} | {{T_IDS_Y_PB_IDS}} | {{ACTIVIDAD}} | {{RUTA_DEL_ARTEFACTO}} | {{ENLACE}} | {{EVIDENCIA_ID_O_ENLACE}} |

Fuente: {{BITACORA_HISTORIAL_GIT_Y_REGISTROS_DE_EJECUCION}}.

{{EXPLICAR_COMO_LA_SECUENCIA_PRODUJO_EL_INCREMENTO_Y_REGISTRAR_CAMBIOS_RESPECTO_DEL_PLAN}}.

### 5.2. Desarrollo detallado por hito

<!-- Repetir el bloque 5.2.1 para cada hito realmente trabajado y numerar
5.2.2, 5.2.3, etc. Evitar un apartado por cada clic o archivo modificado. -->

#### 5.2.1. {{HITO_ID}} — {{NOMBRE_DEL_HITO}}

**Propósito y trazabilidad:** {{NECESIDAD_ATENDIDA_TAREA_PBI_Y_REQUISITOS}}.  
**Responsable y periodo:** {{RESPONSABLE_Y_FECHAS_REALES}}.  
**Precondiciones:** {{ENTORNO_DATOS_Y_DEPENDENCIAS_NECESARIOS}}.

**Pasos realizados:**

1. {{PASO_1_ACCION_Y_FINALIDAD}}.
2. {{PASO_2_ACCION_Y_FINALIDAD}}.
3. {{PASO_3_COMPROBACION_Y_CRITERIO}}.

**Artefactos relevantes:** {{ENLACES_A_ARCHIVOS_MIGRACIONES_COMPONENTES_O_DOCUMENTOS}}.

**Comando o procedimiento reproducible:** {{DIRECTORIO_DE_TRABAJO_PRECONDICIONES_Y_COMANDO_EXACTO_SIN_SECRETOS}}.

**Resultado esperado:** {{COMPORTAMIENTO_Y_CRITERIO_DE_ACEPTACION}}.  
**Resultado observado:** {{SALIDA_REAL_FECHA_Y_REPORTE}}.  
**Estado de verificación:** {{APROBADO_FALLIDO_BLOQUEADO_O_NO_EJECUTADO}}.  
**Modo y alcance comprobado:** {{REAL_SIMULADO_O_MIXTO_Y_LIMITES}}.

La siguiente figura documenta {{ACCION_O_ESTADO_RELEVANTE}} y se vincula con {{HITO_TAREA_PBI_Y_PRUEBA}}.

**Figura 5.1: {{TITULO_ESPECIFICO_DE_LA_CAPTURA}}**

<!-- Activar el enlace cuando exista el archivo. Sustituir la ruta por una
ruta relativa al informe. Las imágenes ya existentes de S1 se encuentran en
imagenes/sprint-01/. No copiar ni renombrar evidencias originales sin necesidad.

![{{DESCRIPCION_ACCESIBLE}}](imagenes/sprint-{{NN}}/{{ARCHIVO_CAPTURA}}.png)
-->

**Evidencia visual:** {{RUTA_RELATIVA_O_PENDIENTE_DE_CAPTURA}}.  
**Fuente:** captura {{MANUAL_O_HERRAMIENTA_REAL}}, {{AUTOR}}, {{FECHA_HORA_Y_ZONA}}, entorno {{ENTORNO}}, commit {{SHA}}.

{{INTERPRETAR_LO_QUE_DEMUESTRA_LA_CAPTURA_Y_LO_QUE_REQUIERE_UN_REPORTE_O_PRUEBA_COMPLEMENTARIA}}.

**Incidencias y decisiones:** {{PROBLEMA_CAUSA_COMPROBADA_SOLUCION_Y_REFERENCIA_AL_ADR_SI_APLICA}}.  
**Limitaciones o pendientes del hito:** {{PENDIENTE_RESPONSABLE_Y_SIGUIENTE_ACCION_O_NINGUNO_VERIFICADO}}.

### 5.3. Diseño y documentación técnica relacionados

{{RESUMIR_EL_CAMBIO_TECNICO_Y_ENLAZAR_LAS_SECCIONES_DEL_SAD_SRS_Y_ARTEFACTOS_ACTUALIZADOS}}. Según lo trabajado, referenciar contratos de API, modelo físico de datos y RLS, variables de entorno, transformación de datos, errores, estados y decisiones arquitectónicas.

{{INDICAR_LA_TRAZABILIDAD_A_LAS_REGLAS_D_1_A_D_10_QUE_APLIQUEN_Y_LA_UBICACION_DE_LA_ESPECIFICACION_COMPLETA}}.

<!-- Mantener el informe centrado en el incremento. Enlazar el detalle canónico
en lugar de mantener una segunda copia divergente. Si se incorpora un diagrama
necesario para la explicación, usar PlantUML, numerar la figura, indicar fuente,
analizarla y sincronizarla con la bóveda vigente del repositorio. -->

### 5.4. Pruebas ejecutadas y relación con el catálogo

El cuadro relaciona las verificaciones del incremento con los casos del catálogo y sus resultados. Cuando una prueba técnica no tenga correspondencia registrada, se indicará «Sin mapeo al catálogo» y se justificará su incorporación, sin inventar un código oficial.

### Cuadro 5.2: Trazabilidad y resultados de las pruebas del sprint

| ID del catálogo / prueba técnica | Tarea / PBI / requisito | Escenario y tipo de prueba | Resultado esperado | Resultado observado y estado | Evidencia / reporte |
| :--- | :--- | :--- | :--- | :--- | :--- |
| {{ID_EXISTENTE_O_SIN_MAPEO}} | {{IDS_APLICABLES}} | {{ESCENARIO_UNITARIA_INTEGRACION_E2E_MANUAL_Y_MODO}} | {{CRITERIO}} | {{OBSERVACION_Y_ESTADO}} | {{RUTA_O_ENLACE}} |

Fuente: {{VERSION_DEL_CATALOGO_ARCHIVOS_DE_PRUEBA_Y_REPORTES_FECHADOS}}.

{{ANALIZAR_LOS_RESULTADOS_INCLUYENDO_CASOS_NEGATIVOS_FALLOS_BLOQUEOS_Y_ESCENARIOS_NO_EJECUTADOS}}. Distinguir las pruebas con sustituciones de aquellas realizadas contra servicios reales.

### 5.5. Calidad, cobertura e integración continua

Se presentan las mediciones obtenidas para cada componente, junto con su instrumento y evidencia. Las métricas no instrumentadas se registran como «No medidas».

### Cuadro 5.3: Resultados de calidad y verificación automatizada

| Componente / comprobación | Herramienta y comando | Resultado real | Métrica y unidad | Meta y fuente | Evidencia / commit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Pruebas frontend | {{COMANDO_Y_VERSION}} | {{APROBADAS_FALLIDAS_OMITIDAS_TOTAL}} | {{COBERTURA_LINEAS_RAMAS_FUNCIONES_O_NO_MEDIDAS}} | {{META_Y_REFERENCIA}} | {{REPORTE_Y_SHA}} |
| Pruebas backend | {{COMANDO_Y_VERSION}} | {{APROBADAS_FALLIDAS_OMITIDAS_TOTAL}} | {{COBERTURA_DECLARACIONES_RAMAS_O_NO_MEDIDAS}} | {{META_Y_REFERENCIA}} | {{REPORTE_Y_SHA}} |
| Lint / formato / compilación | {{COMANDOS_APLICABLES}} | {{RESULTADOS_Y_ADVERTENCIAS}} | {{ERRORES_ADVERTENCIAS_O_NO_APLICA}} | {{CRITERIO_Y_FUENTE}} | {{LOG_Y_SHA}} |
| Dependencias | {{AUDITORIA_COMANDO_Y_FECHA}} | {{HALLAZGOS_POR_SEVERIDAD_O_NO_EJECUTADO}} | {{CONTEOS_Y_ALCANCE}} | {{CRITERIO_ACORDADO_O_NO_DEFINIDO}} | {{REPORTE_Y_LOCKFILE}} |
| GitHub Actions | {{WORKFLOW_Y_RUN_ID}} | {{ESTADO_Y_CONCLUSION}} | {{JOBS_EVALUADOS}} | {{GATE_ACORDADO}} | {{ENLACE_Y_SHA_EJECUTADO}} |

Fuente: {{REPORTES_ORIGINALES_DE_HERRAMIENTAS_Y_EJECUCION_CI}}.

{{INTERPRETAR_LO_QUE_RESPALDAN_LAS_MEDICIONES_Y_SUS_LIMITACIONES}}. No promediar porcentajes de cobertura entre componentes para declarar una cobertura global. Si se informa una medida conjunta, utilizar datos compatibles y su cálculo explícito. Un workflow satisfactorio solo respalda las comprobaciones efectivamente incluidas en ese run.

### 5.6. Incidencias, desviaciones y pendientes técnicos

El registro distingue cambios de alcance, defectos y obstáculos para que el trabajo pendiente tenga una acción y un responsable identificables.

### Cuadro 5.4: Incidencias y desviaciones observadas

| ID / referencia existente | Incidencia o desviación | Impacto en el objetivo o PBI | Acción realizada / pendiente | Responsable | Estado y destino |
| :--- | :--- | :--- | :--- | :--- | :--- |
| {{REFERENCIA}} | {{HECHO_Y_CAUSA_SI_SE_CONOCE}} | {{IMPACTO}} | {{ACCION_CONCRETA}} | {{RESPONSABLE}} | {{ESTADO_SPRINT_O_FECHA_ACORDADA}} |

Fuente: {{ISSUES_BITACORA_REPORTES_Y_ACUERDOS}}.

{{EXPLICAR_QUE_SE_RESOLVIO_QUE_PERSISTE_Y_COMO_AFECTA_LA_ACEPTACION}}. Diferenciar horas planificadas de horas efectivamente registradas y justificar las desviaciones de calendario o tecnología.

## 6. Balance de los ítems del Product Backlog

### 6.1. Criterios para informar el avance

El balance se realiza por PBI y para el alcance comprometido en este sprint. Una tarea terminada puede aportar solo una parte de un PBI distribuido entre varios sprints.

- **Terminado:** se verificó la totalidad de los criterios comprometidos y la definición de terminado aplicable, con evidencia e integración registradas.
- **Parcial:** existe una entrega comprobada, pero falta al menos un criterio comprometido o su integración.
- **En curso:** se registró trabajo, pero todavía no se dispone de una entrega verificable suficiente.
- **Bloqueado:** un impedimento identificado evita continuar o verificar el ítem.
- **No iniciado:** no se registró ejecución dentro del periodo informado.

La ausencia de evidencia se indica como **«No verificado»** en la columna de verificación; no equivale por sí sola a un resultado aprobado ni fallido. El modo **real, simulado o mixto** se informa de manera independiente.

### 6.2. Estado del alcance comprometido

El cuadro muestra los ítems trabajados, la evidencia de sus criterios y lo que queda por completar. Se incorpora tanto lo terminado como lo parcial o bloqueado para reflejar el resultado completo del compromiso.

### Cuadro 6.1: Balance de los PBI al cierre del periodo informado

| PBI y denominación canónica | Tareas / requisitos relacionados | Estado del alcance en este sprint | Criterios verificados y evidencia | Pendiente y responsable | Alcance del PBI completo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| {{PB_ID_Y_NOMBRE}} | {{T_IDS_Y_REQUISITOS}} | {{ESTADO_Y_MODO_REAL_SIMULADO_MIXTO}} | {{CRITERIOS_APROBADOS_Y_ENLACES_O_NO_VERIFICADO}} | {{CRITERIO_FALTANTE_Y_RESPONSABLE}} | {{CERRADO_O_CONTINUA_EN_SPRINT_CON_FUENTE}} |

Fuente: {{PLAN_SPRINT_BACKLOG_BITACORA_CRITERIOS_Y_EVIDENCIAS_DE_ACEPTACION}}.

{{EXPLICAR_LOS_LOGROS_Y_LAS_BRECHAS_MAS_RELEVANTES_SIN_USAR_CASI_TERMINADO_COMO_CRITERIO}}. Si se presenta un porcentaje de avance, definir su unidad y denominador; no equiparar automáticamente número de tareas con porcentaje de funcionalidad del PBI.

### 6.3. Evaluación del objetivo y aceptación del incremento

**Resultado del objetivo:** {{LOGRADO_PARCIALMENTE_LOGRADO_O_NO_LOGRADO}}.  
**Fundamento:** {{CRITERIOS_Y_EVIDENCIAS_QUE_SUSTENTAN_EL_BALANCE}}.  
**Incremento disponible:** {{FUNCIONES_REALMENTE_UTILIZABLES_Y_ENTORNO}}.  
**Aceptación registrada:** {{PERSONA_FECHA_Y_REGISTRO_O_PENDIENTE_DE_REVISION}}.  
**Restricciones para el siguiente sprint:** {{BRECHAS_Y_CONDICIONES_DE_CONTINUIDAD}}.

<!-- Para S1, verificar especialmente que la conectividad no se presente como
prueba de RLS; un JWT emitido no acredita entrega de correo institucional;
los datos semilla no se declaran oficiales sin validación; un reporte de
pruebas no demuestra por sí solo toda la aceptación funcional. -->

## 7. Importancia y dependencias del trabajo que continúa

### 7.1. Aporte del incremento a la continuidad del proyecto

{{EXPLICAR_QUE_COMPONENTES_HABILITA_ESTE_SPRINT_Y_POR_QUE_SON_NECESARIOS_PARA_LOS_SIGUIENTES}}.

### 7.2. Próximos pasos y condiciones de entrada

El cuadro identifica el trabajo previsto a continuación y sus dependencias. Los elementos nuevos se señalan como propuestas hasta que se acuerde su incorporación al backlog o a una replanificación.

### Cuadro 7.1: Continuidad, dependencias y próximos pasos

| Próximo sprint / PBI / tarea | Resultado esperado | Dependencia de este sprint | Condición necesaria para continuar | Responsable previsto | Referencia del plan o acuerdo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| {{IDS_EXISTENTES}} | {{RESULTADO}} | {{ENTREGABLE_O_PENDIENTE_PREVIO}} | {{CONDICION_VERIFICABLE}} | {{RESPONSABLE}} | {{FUENTE_O_PROPUESTA}} |

Fuente: {{PLAN_VIGENTE_Y_ACUERDOS_DE_CONTINUIDAD}}.

{{PRIORIZAR_LA_SIGUIENTE_ACCION_Y_EXPLICAR_SU_EFECTO_EN_LA_REDUCCION_DE_BLOQUEOS}}.

<!-- Referencia S1→S2: consentimiento (T-04/T-05), roles (T-08), consulta de
catálogo (T-10), perfiles y horarios (T-11/T-12), autorización (T-13).
Conciliar el alcance si una parte se adelantó durante S1; no contabilizarla
dos veces ni cerrar una tarea futura solo por similitud de nombre. -->

## 8. Conclusiones del sprint

1. **Respecto del objetivo:** {{CONCLUSION_SUSTENTADA_EN_LOS_CRITERIOS_Y_RESULTADOS_DEL_APARTADO_6}}.
2. **Respecto del incremento y su calidad:** {{APORTE_TECNICO_FUNCIONAL_Y_EVIDENCIA_RELEVANTE_CON_LIMITES}}.
3. **Respecto de la continuidad:** {{PENDIENTE_O_DEPENDENCIA_PRINCIPAL_Y_SU_IMPLICACION}}.

<!-- Sintetizar resultados ya desarrollados. No introducir nuevas mediciones,
certificaciones, aprobaciones ni afirmaciones de cumplimiento legal integral. -->

## 9. Recomendaciones para los siguientes sprints

### 9.1. Aprendizajes del equipo

**Práctica que conviene mantener:** {{PRACTICA_Y_EVIDENCIA_DE_SU_UTILIDAD}}.  
**Dificultad que conviene corregir:** {{DIFICULTAD_Y_CAUSA_OBSERVADA}}.  
**Ajuste acordado o propuesto:** {{CAMBIO_CONCRETO_Y_ESTADO_DEL_ACUERDO}}.

### 9.2. Acciones recomendadas

Las recomendaciones se derivan de los resultados e incidencias del sprint y se formulan como acciones verificables para la siguiente iteración.

### Cuadro 9.1: Acciones de mejora para los siguientes sprints

| Prioridad | Recomendación / acción concreta | Hallazgo que la justifica | Responsable propuesto o acordado | Momento previsto | Cómo se verificará |
| :---: | :--- | :--- | :--- | :--- | :--- |
| {{PRIORIDAD}} | {{ACCION}} | {{REFERENCIA_AL_APARTADO_O_EVIDENCIA}} | {{RESPONSABLE_Y_ESTADO_DEL_ACUERDO}} | {{SPRINT_O_FECHA}} | {{CRITERIO_DE_MEJORA}} |

Fuente: {{RETROSPECTIVA_REGISTRO_DE_INCIDENCIAS_Y_ACUERDOS}}.

{{EXPLICAR_LA_MEJORA_PRIORIZADA_Y_EL_BENEFICIO_ESPERADO_SIN_AMPLIAR_AUTOMATICAMENTE_EL_ALCANCE_DEL_SPRINT_SIGUIENTE}}.

## 10. Referencias y documentos de respaldo

Las referencias permiten localizar la planificación, los requisitos y la evidencia utilizados. Registrar la versión o commit consultado y la sección aplicable; actualizar las rutas si cambia la estructura del repositorio.

1. Grupo 03. [Plan de sprints y distribución de tareas](../sprints/PLAN_SPRINTS_Y_TAREAS.md). Versión {{VERSION}}, apartado {{APARTADO}}, commit {{SHA}}.
2. Grupo 03. [Reglas de documentación de diseño](../../reglas_documentacion_diseño.md). Versión {{VERSION}}, reglas {{REGLAS_APLICADAS}}.
3. Grupo 03. [SRS de diseño — FD03](FD03-EPIS-Informe%20SRS%20de%20Proyecto.md). Versión {{VERSION}}, requisitos y casos de uso {{IDS_Y_SECCIONES}}.
4. Grupo 03. [SAD de diseño — FD04](FD04-EPIS-Informe%20SAD%20de%20Proyecto.md). Versión {{VERSION}}, secciones {{SECCIONES}}.
5. Grupo 03. Catálogo de pruebas del proyecto. [Línea base de análisis](../analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx), hoja {{HOJA}}, casos {{IDS}}; indicar la versión vigente si existe una posterior.
6. Grupo 03. Bitácora del Sprint {{NN}}: `docs/sprints/sprint-{{NN}}.md`, versión o commit {{SHA}}.
7. Grupo 03. Registro de pruebas del Sprint {{NN}}: {{RUTA_Y_VERSION}}. Para S1: [EVIDENCIA_PRUEBAS_SPRINT_01.md](EVIDENCIA_PRUEBAS_SPRINT_01.md).
8. GitHub Actions y artefactos de ejecución. {{ENLACE_RUN_FECHA_SHA_Y_REPORTES}}.
9. {{DOCUMENTACION_OFICIAL_ADICIONAL_REALMENTE_UTILIZADA_CON_FECHA_DE_CONSULTA}}.

<!-- No citar una fuente únicamente porque aparece en esta lista. Conservar
las fuentes efectivamente consultadas y añadir las referencias exigidas por
la rúbrica del curso, si se proporciona. -->

## 11. Anexos y control de la entrega

### 11.1. Índice de evidencias visuales

El índice permite localizar las capturas sin separar la imagen de la tarea o prueba que respalda. Se conserva una referencia por evidencia y se evitan duplicados de la misma captura.

### Cuadro 11.1: Inventario de capturas y evidencias del sprint

| ID / figura | Hito / tarea / PBI | Prueba o criterio que respalda | Archivo o enlace relativo | Fecha, entorno y commit | Qué demuestra / límite |
| :--- | :--- | :--- | :--- | :--- | :--- |
| {{ID_EXISTENTE_Y_FIGURA}} | {{IDS}} | {{PRUEBA_O_CRITERIO}} | {{RUTA_RELATIVA}} | {{FECHA_ENTORNO_SHA}} | {{OBSERVACION_Y_LIMITACION}} |

Fuente: {{ARCHIVOS_ORIGINALES_Y_REGISTRO_DE_CAPTURAS}}.

{{INDICAR_SI_EL_INVENTARIO_ESTA_COMPLETO_Y_QUE_EVIDENCIAS_FALTAN}}. Para S1, reutilizar las capturas existentes en `docs/diseño/imagenes/sprint-01/` cuando correspondan al escenario y a la versión informados.

### 11.2. Reportes y material complementario

- **Resultados de pruebas y cobertura:** {{RUTAS_O_ARTEFACTOS_CI}}.
- **Comandos y logs sanitizados:** {{RUTAS_Y_FECHAS}}.
- **Commits, PR y acuerdos:** {{ENLACES}}.
- **Diagramas PlantUML y especificaciones:** {{RUTAS_Y_VERSIONES}}.
- **Registro de aceptación o revisión:** {{REFERENCIA_O_PENDIENTE}}.

### 11.3. Revisión antes de presentar

- [ ] Se completaron los marcadores y se retiraron las instrucciones de edición.
- [ ] El informe identifica fechas reales, entorno, rama, commit y punto de corte.
- [ ] Los IDs y el alcance coinciden con el plan y con el SRS vigente.
- [ ] Las tablas contienen presentación, título, fuente y análisis posterior.
- [ ] Los hitos incluyen pasos, artefactos, resultado observado y evidencia.
- [ ] Las capturas son legibles, pertinentes y accesibles mediante sus rutas.
- [ ] Las pruebas se vinculan al catálogo o se identifica el mapeo pendiente.
- [ ] Se distinguen resultados reales, simulados, no medidos y no verificados.
- [ ] Las métricas corresponden a reportes conservados y no a cifras heredadas.
- [ ] El balance incluye PBI parciales, bloqueados y pendientes, si existen.
- [ ] Se registran revisión y aceptación solo cuando hay constancia de ellas.
- [ ] Los enlaces y anexos funcionan y no contienen secretos ni datos innecesarios.
- [ ] Se actualizó el README y la bitácora al incorporar el informe al repositorio.
- [ ] Se comprobó cualquier requisito adicional de formato indicado por el docente.

**Responsable de esta revisión:** {{NOMBRE}}.  
**Fecha de revisión:** {{FECHA}}.  
**Observaciones antes de la presentación:** {{OBSERVACIONES_O_NINGUNA_TRAS_REVISION}}.
