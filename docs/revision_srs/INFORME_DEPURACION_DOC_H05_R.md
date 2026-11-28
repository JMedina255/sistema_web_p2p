# DOC-H05-R · Depuración documental previa a publicación

**Rama** · `docs/p2p-srs-diagramacion-integral`

**Base** · `6f7dcdb`

## Inventario y clasificación

| Clasificación | Resultado |
|---|---|
| CONSERVAR | SRS v4.0, catálogo, 48 pares PlantUML/PNG, 119 figuras técnicas, evidencias académicas originales, informes de QA, matrices y continuidad. La evidencia de cancelación y aforo del Sprint 05 tiene dos archivos con hashes distintos. Se conservan ambos. |
| DUPLICADO EXACTO | 54 grupos iniciales por SHA-256. Se retiraron 20 copias con destino canónico comprobado. Los 34 grupos restantes incluyen materiales de análisis, diseño, presentaciones y QA cuyo contexto o procedencia se conserva. |
| ARCHIVAR FUERA DEL REPOSITORIO | `DOC-H03_P2P_Diagramas_PlantUML`, 51 archivos y 272 430 bytes. Archivo movido al directorio hermano de la copia de trabajo y verificado por SHA-256. |
| RETIRAR TRAS HOMOLOGACIÓN | Posibles copias de consulta de `SRS.md` y `SRS_NUEVO.md` una vez conciliadas sus variantes. Revisar `SAD.md`, los SRS/SAD de análisis y diseño y las guías de narrativas idénticas entre fases según sus referencias y contenido propio. Su conservación durante DOC-H05-R mantiene la trazabilidad de la [matriz de homologación](MATRIZ_HOMOLOGACION_SRS_V4.md). |
| TEMPORAL | Exclusiones específicas en `.gitignore` para paquetes documentales y respaldos locales. Los artefactos de ejecución y compilación quedan fuera del inventario documental. |

Los archivos más pesados del inventario son los PDF originales de factibilidad (2 963 322 bytes) y visión (1 718 466 bytes), la presentación oficial del Sprint 02 en PDF (1 079 870 bytes) y PPTX (1 025 192 bytes), y las tres versiones del SRS en la raíz (entre 818 029 y 860 968 bytes). Se conservan por su función documental y académica.

## Retiros y reducción

Se eliminaron 19 espejos de imágenes de los sprints 05 y 06 y una copia del catálogo de pruebas en la raíz. Se actualizaron 27 referencias de imagen y ruta en el [informe académico del Sprint 05](../diseño/G03_EPIS_Informe_Sprint_05.md).

| Medida | Antes | Después |
|---|---:|---:|
| Archivos bajo seguimiento en Git | 1009 | 990 |
| Archivos del inventario documental de trabajo | 757 | 687 |
| Bytes del inventario documental de trabajo | 52434557 | 49565036 |

El inventario de trabajo abarca `docs/`, los documentos de la raíz y el paquete inicial sin seguimiento. El total final incluye este informe. Las 20 copias retiradas sumaban 2 604 491 bytes.

<details>
<summary>Relación de copias retiradas y destinos canónicos</summary>

| Copia retirada | Versión canónica |
|---|---|
| `Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` | [Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx](../analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx) |
| `docs/diseño/imagenes/sprint-05/01_bandeja_reservas_estudiante.png` | [01_bandeja_reservas_estudiante.png](../sprints/sprint-05/05-evidencias/01_bandeja_reservas_estudiante.png) |
| `docs/diseño/imagenes/sprint-05/02_ratificacion_anticipada.png` | [02_ratificacion_anticipada.png](../sprints/sprint-05/05-evidencias/02_ratificacion_anticipada.png) |
| `docs/diseño/imagenes/sprint-05/03_asistencia_confirmada.png` | [03_asistencia_confirmada.png](../sprints/sprint-05/05-evidencias/03_asistencia_confirmada.png) |
| `docs/diseño/imagenes/sprint-05/04_desistimiento_voluntario.png` | [04_desistimiento_voluntario.png](../sprints/sprint-05/05-evidencias/04_desistimiento_voluntario.png) |
| `docs/diseño/imagenes/sprint-05/06_control_temporal_t24h.png` | [06_control_temporal_t24h.png](../sprints/sprint-05/05-evidencias/06_control_temporal_t24h.png) |
| `docs/diseño/imagenes/sprint-05/07_swagger_api_docs_sprint05.png` | [07_swagger_api_docs_sprint05.png](../sprints/sprint-05/05-evidencias/07_swagger_api_docs_sprint05.png) |
| `docs/diseño/imagenes/sprint-05/08_backend_pytest_coverage_sprint05.png` | [08_backend_pytest_coverage_sprint05.png](../sprints/sprint-05/05-evidencias/08_backend_pytest_coverage_sprint05.png) |
| `docs/diseño/imagenes/sprint-05/09_frontend_vitest_coverage_sprint05.png` | [09_frontend_vitest_coverage_sprint05.png](../sprints/sprint-05/05-evidencias/09_frontend_vitest_coverage_sprint05.png) |
| `docs/diseño/imagenes/sprint-05/10_github_actions_ci_sprint05.png` | [10_github_actions_ci_sprint05.png](../sprints/sprint-05/05-evidencias/10_github_actions_ci_sprint05.png) |
| `docs/diseño/imagenes/sprint-06/01_notificacion_quorum_insuficiente.png` | [01_notificacion_quorum_insuficiente.png](../sprints/sprint-06/05-evidencias/01_notificacion_quorum_insuficiente.png) |
| `docs/diseño/imagenes/sprint-06/02_modal_resolucion_contingencia.png` | [02_modal_resolucion_contingencia.png](../sprints/sprint-06/05-evidencias/02_modal_resolucion_contingencia.png) |
| `docs/diseño/imagenes/sprint-06/03_reprogramacion_antelacion_24h.png` | [03_reprogramacion_antelacion_24h.png](../sprints/sprint-06/05-evidencias/03_reprogramacion_antelacion_24h.png) |
| `docs/diseño/imagenes/sprint-06/04_cancelacion_definitiva_motivo.png` | [04_cancelacion_definitiva_motivo.png](../sprints/sprint-06/05-evidencias/04_cancelacion_definitiva_motivo.png) |
| `docs/diseño/imagenes/sprint-06/05_proyeccion_codigo_qr_totp.png` | [05_proyeccion_codigo_qr_totp.png](../sprints/sprint-06/05-evidencias/05_proyeccion_codigo_qr_totp.png) |
| `docs/diseño/imagenes/sprint-06/06_lista_asistencia_tiempo_real.png` | [06_lista_asistencia_tiempo_real.png](../sprints/sprint-06/05-evidencias/06_lista_asistencia_tiempo_real.png) |
| `docs/diseño/imagenes/sprint-06/07_formulario_bitacora_silabica.png` | [07_formulario_bitacora_silabica.png](../sprints/sprint-06/05-evidencias/07_formulario_bitacora_silabica.png) |
| `docs/diseño/imagenes/sprint-06/08_validacion_bitacora_sello_sha256.png` | [08_validacion_bitacora_sello_sha256.png](../sprints/sprint-06/05-evidencias/08_validacion_bitacora_sello_sha256.png) |
| `docs/diseño/imagenes/sprint-06/09_swagger_api_docs_sprint06.png` | [09_swagger_api_docs_sprint06.png](../sprints/sprint-06/05-evidencias/09_swagger_api_docs_sprint06.png) |
| `docs/diseño/imagenes/sprint-06/10_pruebas_automatizadas_sprint06.png` | [10_pruebas_automatizadas_sprint06.png](../sprints/sprint-06/05-evidencias/10_pruebas_automatizadas_sprint06.png) |

</details>

## Verificación

La comparación con `6f7dcdb` no detectó enlaces locales rotos introducidos por el cambio. Los 20 destinos canónicos coinciden por SHA-256. El inventario conserva 24 narrativas, 48 pares PlantUML/PNG y 119 figuras de diseño. El diff se limita a documentación, continuidad y las reglas de exclusión. La comprobación de rutas y formatos de credenciales de los cambios de la rama no encontró coincidencias. `git diff --check` pasó.

La rama queda preparada para la publicación manual del responsable. La homologación definitiva y DOC-H06 siguen pendientes de autorización.
