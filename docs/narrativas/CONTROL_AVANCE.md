# Control de avance del catálogo de narrativas y diagramas

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS-UPT
**Hito:** DOC-H04-R
**Base en Git:** `044d2a8473908def9a40503cc9692426e02198a8`
**Paquete de entrada:** DOC-H03_P2P_Diagramas_PlantUML

| Etapa | Resultado |
|---|---|
| Redacción | 24 narrativas incorporadas de DOC-H03. Se conservaron las secciones 7.1 a 7.4. |
| Sintaxis y renderizado | 48 pares PlantUML/PNG. En DOC-H04-R se validaron y renderizaron en UTF-8 las 19 fuentes modificadas. Las otras 29 conservan la validación de DOC-H04. |
| Revisión visual | DOC-H04 inspeccionó las 48 imágenes. DOC-H04-R comparó las 19 figuras corregidas con sus versiones anteriores y cerró las observaciones indicadas abajo. |
| Aprobación documental | Pendiente de revisión final por el responsable. |

El [catálogo](../../NARRATIVAS_CASOS_DE_USO.md) enlaza cada PNG y su fuente. Su Anexo A conserva las discrepancias y el alcance de la implementación documentados en DOC-H03. La matriz histórica de CUS-001 está disponible en el repositorio en `docs/revision_srs/CUS-001/MATRIZ_REVISION_H01.md`.

## Estado recibido de DOC-H04 por caso de uso

En todas las filas, ambos PNG están renderizados, inspeccionados e incorporados al catálogo para revisión. «Sin observación visual» indica que durante la inspección del PNG no se identificó un defecto gráfico. Las aprobaciones previas declaradas en el paquete se refieren a la narrativa.

| Caso | Figuras (actividades / caso de uso) | Estado de redacción recibido | Observaciones del renderizado o del contraste con la narrativa |
|---|---:|---|---|
| CUS-001 | 1 / 2 | Texto preservado. DOC-H03 cita aprobación previa y H01 registraba aprobación pendiente. | Fig. 1: falta un título dentro de la imagen, dos iconos de consentimiento aparecen como cuadros y un conector cruza el nodo de cambio de correo. Las salidas por código incorrecto y vencido no dibujan los retornos descritos en E003 y E004. Fig. 2: las flechas punteadas se cruzan junto a la etiqueta de Google y el pendiente de validación solo es visible en la fig. 1. |
| CUS-010 | 3 / 4 | Consolidada a partir de narrativa con aprobación previa según DOC-H03. | Fig. 3: la flecha de retorno cruza «Mostrar expediente y distintivos» y «Rechazar promoción y conservar roles». Fig. 4: sin observación visual. |
| CUS-006 | 5 / 6 | Consolidada a partir de narrativa con aprobación previa según DOC-H03. | Fig. 5: trazos atraviesan el nodo de enlace virtual y el de rechazo de publicación. Figs. 5 y 6: el Anexo A del catálogo mantiene la limitación sobre creación efectiva de una reunión virtual. |
| CUS-008 | 7 / 8 | Propuesta presentada, pendiente de aprobación expresa. | Fig. 7: conectores atraviesan nodos de error, publicación y resultados. Fig. 8: los objetivos de registro y consulta aparecen como casos separados y llevan la marca de alcance pendiente. |
| CUS-005 | 9 / 10 | Propuesta basada en la postulación parcial desde el perfil. | Fig. 9: la advertencia por ciclo finaliza el recorrido sin dibujar el retorno para corregirlo. Fig. 10: sin observación visual. |
| CUS-021 | 11 / 12 | Propuesta de comité, con implementación pendiente. | Fig. 11: la acción de asignar rol aparece antes de verificar que el registro resultó correcto. El paso 10 de la narrativa distingue conservar la decisión y asignar el rol mediante CUS-010. Fig. 12: sin observación visual. |
| CUS-002 | 13 / 14 | Redactada a partir de revisión estática. | Fig. 13: la flecha del bucle atraviesa los nodos de tarjetas y aforo. Fig. 14: sin observación visual. |
| CUS-003 | 15 / 16 | Redactada a partir de revisión estática. | Ambas sin observación visual. La reserva provisional se distingue de la ratificación. |
| CUS-004 | 17 / 18 | Redactada a partir de revisión estática. | Ambas sin observación visual. Se distingue la consulta de una reserva ya ratificada. |
| CUS-023 | 19 / 20 | Evaluación identificada, ejecución periódica pendiente de validación. | Fig. 19: una flecha cruza el texto del nodo de fallo de evaluación. Fig. 20: la nota identifica expresamente que la activación periódica sigue sin certificarse. |
| CUS-024 | 21 / 22 | Redactada a partir de revisión estática. | Ambas sin observación visual. El motivo conserva su condición opcional. |
| CUS-007 | 23 / 24 | Redactada a partir de revisión estática. | Fig. 23: un conector cruza los textos de resultado de bitácora. Fig. 24: una asociación pasa sobre el rótulo del límite del sistema. Asistencia y bitácora figuran como objetivos separados en el modelo de casos de uso. |
| CUS-012 | 25 / 26 | Alcance parcial, encuesta y retroalimentación grupal. | Fig. 25: conectores cruzan el nodo de retroalimentación y la decisión de reintento. Fig. 26: sin observación visual. |
| CUS-013 | 27 / 28 | Alcance parcial, historial de reservas y de sesiones. | Ambas sin observación visual. Los recorridos se distinguen por rol. |
| CUS-014 | 29 / 30 | Constancia DEMO, validación institucional pendiente. | Ambas sin observación visual. La emisión acreditada en la documentación se identifica como DEMO. |
| CUS-018 | 31 / 32 | Propuesta de trámite, con implementación pendiente. | Ambas sin observación visual. El responsable y el trámite se identifican como previstos. |
| CUS-019 | 33 / 34 | Alcance parcial, consulta administrativa y tutor previsto. | Ambas sin observación visual. Se distingue el rol del tutor previsto del visado administrativo. |
| CUS-009 | 35 / 36 | Alcance parcial, monitoreo de quórum. | Fig. 35: la flecha de retorno pasa por el nodo de resultados y la decisión de sesiones disponibles. Fig. 36: sin observación visual. |
| CUS-011 | 37 / 38 | Propuesta de exportación, con implementación pendiente. | Fig. 37: una flecha cruza el nodo de entrega del archivo. Fig. 38: sin observación visual. |
| CUS-015 | 39 / 40 | Propuesta de parametrización, con implementación pendiente. | Fig. 39: la ruta que continúa atraviesa el nodo de cancelación y su símbolo de fin. Fig. 40: sin observación visual. |
| CUS-016 | 41 / 42 | Propuesta de bandeja de seguridad, con implementación pendiente. | Fig. 41: el bucle de consulta cruza varios nodos y el texto de la decisión final. Fig. 42: sin observación visual. |
| CUS-017 | 43 / 44 | Alcance parcial, cronogramas disponibles y configuración virtual pendiente. | Fig. 43: un conector cruza el nodo de rechazo por formato o tamaño. Fig. 44: sin observación visual. |
| CUS-020 | 45 / 46 | Redactada a partir de revisión estática. | Fig. 45: hay flechas sobre nodos y decisiones de la gestión curricular. Fig. 46: una asociación pasa sobre el rótulo del límite del sistema. El Anexo A conserva la discrepancia de ciclos permitidos. |
| CUS-022 | 47 / 48 | Propuesta de edición administrativa, con implementación pendiente. | Ambas sin observación visual. Los valores de referencia aparecen en el flujo propuesto. |

## Cierre de observaciones de DOC-H04-R

| Figura y caso | Defecto registrado | Corrección aplicada | Resultado de la inspección posterior | Pendiente |
|---|---|---|---|---|
| 1 · CUS-001 | Título ausente, glifos de consentimiento ilegibles, cruce sobre cambio de correo y retornos E003/E004 omitidos. | Se añadió el título, se retiraron los iconos de los controles y se dibujaron los retornos a acceso, verificación y reenvío. | Título y controles legibles. Los retornos se siguen por los círculos identificados. | Validación externa de Google y SMTP. |
| 2 · CUS-001 | Extensiones cruzadas junto a Google y pendiente ausente. | Se distribuyeron actores y extensiones en filas y se añadió la leyenda de validación. | Flechas de extensión separadas. Leyenda visible. | Validación externa de Google. |
| 3 · CUS-010 | Retorno por encima del expediente y del rechazo. | Se sustituyó el retorno largo por un conector identificado. | Expediente y rechazo legibles. | — |
| 5 · CUS-006 | Trazos sobre enlace virtual y rechazo de publicación. | Se separó la modalidad virtual y se identificó el retorno para correcciones. | Ambas modalidades convergen en la revisión de la oferta. Los nodos observados quedan legibles. | Creación efectiva de reuniones virtuales por verificar. |
| 7 · CUS-008 | Líneas sobre errores, resultados y publicación. | Se separaron el registro y la consulta del banco, con conectores de reintento y actualización. | Carriles identificables. Las rutas se siguen sin cubrir las etiquetas observadas. | Alcance parcial y verificación de implementación. |
| 9 · CUS-005 | La advertencia de ciclo terminaba el flujo. | E002 retorna a la selección de ciclo y rol. | El retorno se distingue de la confirmación de preferencias. | La preferencia del perfil no concede el rol Mentor. |
| 11 · CUS-021 | La asignación precedía a la confirmación del registro. | Se separaron postulación, evaluación, decisión motivada, comprobación del registro y asignación autorizada mediante CUS-010. | Solo una aprobación registrada conduce al carril del administrador. Rechazo y fallo de registro tienen salida propia. | Propuesta con implementación pendiente. |
| 13 · CUS-002 | El bucle cruzaba tarjetas y aforo. | Se identificó el retorno a la selección de filtros. | Tarjetas y decisión de aforo despejadas. | — |
| 19 · CUS-023 | Flecha sobre el mensaje de fallo de evaluación. | Se dio salida propia al fallo de registro y se separó el monitoreo. | Mensaje de fallo legible y recorrido de monitoreo identificable. | Ejecución periódica pendiente de validación. |
| 23 · CUS-007 | Conector sobre los resultados de bitácora. | Se separaron asistencia y bitácora por tramo. | Los resultados de bitácora se distinguen en sus carriles. | — |
| 24 · CUS-007 | Asociación sobre el rótulo del límite. | Se colocó el rótulo debajo del marco. | Marco, rótulo y asociaciones legibles. | — |
| 25 · CUS-012 | Líneas sobre retroalimentación y decisión de reintento. | Se separó la bitácora del mentor y se identificó el retorno a la encuesta. | Ambos recorridos y sus actores se distinguen. | Alcance parcial de la retroalimentación grupal. |
| 35 · CUS-009 | Retorno sobre resultados y disponibilidad de sesiones. | Se identificó el retorno de actualización a la consulta. | Decisión y resultados quedan despejados. | Alcance parcial de la analítica. |
| 37 · CUS-011 | Flecha por encima de la entrega del archivo. | Se identificó el retorno a la selección de filtros. | Entrega y error de generación quedan legibles. | Exportación propuesta, pendiente de implementación. |
| 39 · CUS-015 | La continuación cruzaba la cancelación y su fin. | Se trasladó la cancelación a un tramo con salida propia. | Se distingue la salida que conserva la configuración vigente. | Parametrización propuesta, pendiente de implementación. |
| 41 · CUS-016 | Bucle sobre actividades y decisión final. | Se identificó el retorno para una nueva consulta. | Decisión final y actividades quedan legibles. | Bandeja propuesta, pendiente de implementación. |
| 43 · CUS-017 | Conector sobre el rechazo de formato o tamaño. | Se separó E001 y se identificaron la continuación a consulta y el tramo del mentor. | La excepción y las modalidades quedan legibles. | Creación efectiva de la reunión virtual por verificar. |
| 45 · CUS-020 | Flechas sobre nodos y decisiones de gestión. | Se separaron consulta, desactivación y retorno a gestión. | Confirmación y desactivación se distinguen por actor y tramo. | Discrepancia de ciclos permitidos en el Anexo A. |
| 46 · CUS-020 | Asociación sobre el rótulo del límite. | Se colocó el rótulo debajo del marco. | Rótulo despejado y relaciones legibles. | Discrepancia de ciclos permitidos en el Anexo A. |

Las 19 observaciones del catálogo quedan cerradas en el plano gráfico o de correspondencia con la narrativa. Siguen abiertas las discrepancias de alcance del Anexo A, las validaciones externas, las propuestas pendientes de implementación y la aprobación documental del responsable.
