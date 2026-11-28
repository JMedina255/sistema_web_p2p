# DOC-H06 — Cierre de homologación del SRS y SAD

**Fecha:** 28/11/2026. **Base inicial:** `1f6e806a98f3f584df3349e2a8bd69467acc7eae`. **Base final DOC-H06-R:** `ed6c1cc06f0794c661636e1893723e025c206b68`. **Rama:** `docs/doc-h06-homologacion-srs-sad`.

**Dictamen: APTO para revisión y sustentación documental del alcance y las brechas descritos.** No acredita aprobación institucional, implementación completa ni aptitud para producción. La revisión de implementación es estática y reutiliza las evidencias existentes; no se ejecutaron suites de aplicación ni se consultaron bases de datos.

## Inconsistencias corregidas

| Área | Corrección documental |
|---|---|
| Módulos y casos | Cinco módulos y 24 CUS vigentes en requisitos y modelos; equivalencia con los ocho módulos anteriores y numeración histórica conservadas. RF-001–RF-026 se reconocen como alias de RF01–RF26. RF21 y avisos quedan transversales, sin colisionar con CUS-019/CUS-009 vigentes. |
| RF, RN y RNF | Se preservan los 26 RF, 14 RN y 10 RNF, diferenciando requisitos, implementación identificada, alcance parcial y propuestas. Se retiran afirmaciones generales de cumplimiento empírico. |
| Autenticación | Se conserva el nombre de CUS-001; OTP por correo o Google por separado no demuestran dos factores independientes. Se distinguen cinco errores del desafío, límites de tasa y reenvío; Google/SMTP reales siguen pendientes de validación. |
| Mérito y oferta | Ciclo VII–X y nota ≥14 permanecen como requisito institucional; ciclo/rol no acreditan nota ni comité. Antelación estricta >24 h; URL generada no demuestra reunión externa. |
| Recomendación | Jaccard con pesos 0.40/0.35/0.15/0.10 para temas/horario/modalidad/afinidad curricular y multiplicador crítico. Dice es explicativo. Se documentan neutralidad horaria, discretización y desempates reales; se retiran coseno, filtrado colaborativo y reputación como descripción del algoritmo actual. |
| Arquitectura y contratos | Tecnologías declaradas en manifiestos, componentes presentes y 63 rutas declaradas de negocio/salud; se separan propuestas de endpoints reales y de configuración de despliegue. |
| Persistencia | 19 tablas ORM con campos, tipos, nulabilidad, restricciones y FK declaradas; cabeza Alembic `20261123_008`. Se distinguen modelo, migraciones y despliegue no inspeccionado; se conserva la diferencia de compatibilidad de revisiones históricas de certificados. |
| Estados y seguimiento | Valores admitidos distintos de transiciones ejecutadas. Corte → `CANCELADA_NO_CONFIRMADA`; cancelación por quórum → sesión `CANCELADA_QUORUM` y reservas `CANCELADA_SISTEMA_QUORUM`. La asistencia no cambia automáticamente la sesión a EN_CURSO. |
| Asistencia y bitácora | Pase aleatorio de 30 s, con respaldo persistente, sin acreditar TOTP RFC 6238; ventana inicio −15 min a fin +30 min. Registro/actualización de bitácora hasta fin +48 h; huella de campos seleccionados, sin firma certificada ni inmutabilidad absoluta. |
| Feedback y constancia | Encuesta del asistente y observación grupal distintas del feedback individual inverso pendiente. PDF/folio DEMO separado de autorización y certificación institucional. |
| Resultados históricos | Cifras de 627/682 pruebas y reportes QA se conservan con procedencia y alcance; P@k, NDCG, latencia, cobertura, SLA y accesibilidad no se declaran resultados actuales. |

## Verificaciones

| Comprobación | Resultado |
|---|---|
| Correspondencia SRS–SAD–aplicativo | Tablas, rutas, factores de recomendación y estados contrastados con código/modelos/migraciones de la base. La persistencia efectiva y las integraciones externas no se certifican. |
| Homologación | 24 identificadores únicos en cada serie ECB, actividades, secuencias y clases; catálogo de cinco módulos; trazabilidad de RF/RN/RNF y numeración anterior. |
| Narrativas y figuras | 24 narrativas íntegras y 48 figuras originales sin cambios; se conservan 119 figuras de diseño SRS y 14 SAD. La corrección adicional del catálogo se limita a una cita histórica en el Anexo A de CUS-017. |
| PlantUML y PNG | 131 fuentes actualizadas y sus 131 PNG en el directorio DOC-H06. PlantUML 1.2024.7 termina sin errores. Los dos diagramas As-Is se reutilizan. Solo se renderizan fuentes afectadas. |
| Inspección visual | Revisadas las 131 figuras mediante 22 láminas de contacto y aperturas de detalle; corregidos errores de sintaxis, saltos de leyendas, tipos inferidos y rótulos heredados. Los originales se abren para lectura a escala completa. |
| Markdown y referencias | Tablas, bloques, numeración de figuras, rutas locales y anclas comprobadas; sin referencias locales rotas en los documentos y fuentes de trazabilidad revisados. |
| Alcance y protección | Sin cambios funcionales en `aplicacion/`, sin ejecución de migraciones ni lectura de `.env`, credenciales o certificados. Ediciones históricas y sus figuras conservadas. |
| Higiene del diff | `git diff --check` y comprobación de patrones de secretos sobre los textos destinados al commit, sin incidencias. No se publica material operativo ni herramientas temporales. |

## Pendientes conservados

Permanecen abiertos el mérito académico acreditado y el comité; la justificación de inasistencia y su RF específico; los permisos y controles del banco de demanda; el rol Tutor; feedback individual inverso; historial unificado y recursos; exportación ejecutiva; parametrización administrativa; auditoría integral de seguridad; analítica de retención; gamificación integral; cámara real; entrega SMTP/Google; operación periódica y multiworker; RLS por instalación; firma, autorización y validez institucional de constancias. No se eliminan requisitos por falta de implementación.

Las vistas ECB y secuencia expresan responsabilidades y recorridos principales; los contratos exactos se consultan en SAD 6.3 y los flujos completos en las narrativas. Los diagramas propuestos no atribuyen tablas o servicios operativos inexistentes. Las discrepancias de política o aceptación institucional requieren decisión del responsable.

## Archivos del incremento

- [SRS_V4.0_CONSOLIDADO.md](../../SRS_V4.0_CONSOLIDADO.md) y [SAD.md](../../SAD.md), con control de versiones actualizado.
- [Matriz de homologación](MATRIZ_HOMOLOGACION_SRS_V4.md) y [catálogo](../../NARRATIVAS_CASOS_DE_USO.md), con corrección de la cita histórica CUS-017: origen CUS-008/RF10; el antiguo CUS-011 corresponde a reportes.
- [Fuentes SRS](diagramas/doc-h06/srs/puml/), [PNG SRS](diagramas/doc-h06/srs/img/), [fuentes SAD](diagramas/doc-h06/sad/puml/) y [PNG SAD](diagramas/doc-h06/sad/img/): 118 pares SRS y 13 pares SAD. Se mantiene el paquete histórico para preservar sus referencias.
- Este único informe de cierre y los registros compactos `CURRENT_STATE.md`, `NEXT_TASK.md` y `HANDOFF.md` en `.agents/state/`.

## Recuperación y cierre DOC-H06-R

La autorización de DOC-H06-R sustituye la publicación solicitada originalmente: **solo commit local, sin push ni merge a main**. Antes de cambiar de rama se respaldaron los 270 archivos documentales, incluidos los nuevos, y los parches binarios del índice y árbol de trabajo. Las copias se verificaron por SHA-256 en `C:\Users\HP\Desktop\Proyectos\DOC-H06-R-respaldo-20261128-150554`, fuera del repositorio; `manifest.json` registra los archivos y las huellas de las 48 figuras narrativas.

La rama documental se recuperó y avanzó linealmente desde `1f6e806` hasta `ed6c1cc` mediante fast-forward, sin crear commit de merge ni alterar main. Se conservaron los tres commits ajenos:

| Commit | Cambio contrastado |
|---|---|
| `c67d877` | Revierte la retirada previa de impresión del OTP. |
| `a05b80c` | Revierte la restricción de pistas a correo simulado y las omisiones de contenido sensible del servicio de correo. |
| `ed6c1cc` | Introduce traza explícita de OTP en development y modifica su prueba acotada. |

El delta afecta solo `auth_service.py`, `email_service.py`, `test_auth.py` y `test_email_service.py`; no se solapa con el paquete documental. **Conflictos: ninguno.** No se resolvieron ni modificaron archivos funcionales. El contraste estático de condiciones y pruebas se documenta en SAD 3.2 y en el Anexo A del SRS: no se equipara la guarda de la traza explícita con una garantía para todos los logs, ni la pista de prueba con entrega SMTP real.

Tras recuperar la rama, los 270 archivos coincidían con el respaldo. El cierre solo actualiza la base y esta evidencia en SRS/SAD, este informe y los tres registros de continuidad. Se confirman por hash los 131 pares PlantUML/PNG y las 48 figuras narrativas, y por comparación exacta el bloque de las 24 narrativas. Se conservan las verificaciones de DOC-H06; únicamente se revalidan las condiciones afectadas, la conservación del paquete, las referencias añadidas y `git diff --check`, incluido el índice. No se ejecutan suites funcionales ni se regenera ningún diagrama.

El dictamen documental APTO se mantiene con las brechas institucionales y operativas ya descritas. El commit final se identifica en la entrega y en el historial local; no se inserta su propio hash en los archivos que lo componen. DOC-H06-R termina al entregar y queda pendiente de revisión del responsable, sin autorización de publicación.
