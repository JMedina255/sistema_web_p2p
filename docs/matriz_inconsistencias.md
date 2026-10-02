# Matriz de Auditoría e Inconsistencias Técnicas y Funcionales

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT<br>
**Documento Auditado:** FD03 (SRS), FD04 (SAD) y artefactos asociados; el alcance y estado de cada revisión se distingue por sección.<br>
**Fase:** Auditoría de Calidad y Consistencia Metodológica - Fase de Análisis<br>
**Línea Base Oficial Congelada:**
- **Módulos:** MOD-01 al MOD-08
- **Requerimientos Funcionales:** RF01 al RF26
- **Reglas de Negocio:** RN-01 al RN-14
- **Requerimientos No Funcionales:** RNF01 al RNF10 (ISO/IEC 25010)
- **Casos de Uso Oficiales:** CUS01 al CUS24

---

## 1. Matriz Consolidada de Inconsistencias Detectadas

| ID | Elemento / Sección | Inconsistencia Detectada | Fuente que Manda | Acción Correctiva Propuesta | Estado |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **INC-01** | `CUS06`, `RN-04` | CUS06 introduce una antelación mínima estricta de 48 horas atribuyéndola a RN-04. Sin embargo, RN-04 solo define la dinámica de oferta y demanda sin mencionar las 48 horas. | RN-04 / RF08 | Alinear RN-04 y CUS06: Especificar en RN-04 que las ofertas deben publicarse con una antelación mayor a la ventana de confirmación ($T > 24\text{ h}$, recomendando 48h) o retirar la restricción punitiva de 48h en CUS06 para evitar crear una regla huérfana. | Resuelto |
| **INC-02** | `CUS23`, `CUS07`, `RN-09` | El flujo alternativo FA01 de CUS23 cancelaba unilateralmente la sesión si existían cero confirmados ($N_{conf}=0$). Esto contradice abiertamente a RN-09 y RF16, donde la decisión ante cualquier quórum $<50\%$ recae exclusivamente en el Mentor. | RN-09 / RF16 / CUS07 | Eliminar la auto-cancelación en CUS23 (FA01). Cuando el quórum sea $<50\%$ (incluso con 0 confirmados), la sesión pasa invariablemente a `QUORUM_INSUFICIENTE` y se notifica al Mentor para que decida en CUS07. | Resuelto |
| **INC-03** | `CUS04`, `CUS17`, `RF12`, `RN-05` | CUS04 introdujo dos alcances no contemplados en la línea base: 1) límite de máximo 3 reservas simultáneas, y 2) lista de espera / notificación de vacantes libres. RF12 y RN-05 solo especifican reserva y control de aforo (10/20). | RF12 / RN-05 | Retirar la lista de espera y el límite forzado de 3 reservas de las narrativas de CUS04 y CUS17, simplificando el alcance al MVP validado en la línea base de requerimientos. | Resuelto |
| **INC-04** | `Cuadro 6.1`, `RF10`, `Diag. 6.3` | En el Cuadro 6.1 y diagramas iniciales, el Parser de Horarios se catalogó erróneamente como un "Servicio Externo" de terceros, cuando RF10 lo define como un componente procesador interno del backend. | RF10 | Corregir la clasificación arquitectónica: El Parser es un componente interno del backend (MOD-04). Los servicios externos son exclusivamente Google Meet API, Bot de Discord y Servicio SMTP UPT. | Resuelto |
| **INC-05** | `Sección 3.4`, `CUS13`, `CUS09`, `RF23` | La Sección 3.4 (Límites y Exclusiones) indicaba que no se integraría firma digital avanzada con terceros mediante QR. No obstante, CUS13 y CUS09 mencionaban "firma digital institucional con clave privada PKI y motor criptográfico". | Sección 3.4 / RF22 / RF23 | Homogeneizar alcance de certificación: Descartar "firma digital PKI de terceros". Especificar formalmente: Emisión de constancia en PDF + Código correlativo único institucional + Hash SHA-256 de integridad + Código QR público de validación en portal web UPT. | Resuelto |
| **INC-06** | `CUS01`, `RF01`, `RN-01` | CUS01 incorporó detalles operativos de bajo nivel como longitud rígida de OTP a 6 dígitos, máximo 3 intentos y bloqueo forzado de 15 minutos, sin estar formalizados como directriz de seguridad en RN-01 ni RF01. | RF01 / RN-01 | Armonizar la redacción en CUS01 para que exprese los parámetros de seguridad como criterios orientativos de diseño y protección contra fuerza bruta, sin convertirlos en cláusulas contractuales desconectadas de RN-01. | Resuelto |
| **INC-07** | `Diag. 6.13` a `6.16`, Modelos UML | Presencia de artefactos vinculados a las inconsistencias previas: Parser como actor externo en ECB, referencias a listas de espera en diagramas de actividades y clases, y métodos no sincronizados. | RF / RN / CUS Canónicos | Actualizar los diagramas PlantUML en FD03 y diagramas_general.md para remover el Parser como actor externo y depurar métodos o estados no contemplados. | Resuelto |
| **INC-08** | Redacción Académica Global | Uso de expresiones absolutistas ("garantiza", "elimina cualquier posibilidad", "completamente blindado") y ligera dispersión en nombres de actores y estados en algunas tablas. | Regla 1 y Estándar Académico | Suavizar redacción a terminología técnica rigurosa de ingeniería de software ("especificado para mitigar", "orientado a prevenir") y estandarizar mayúsculas en los identificadores de estado. | Resuelto |
| **INC-09** | `CUS03`, `CUS23`, `CUS16`, `CUS18` | Reglas ocultas y parámetros rígidos no normados: tope de 3 solicitudes activas en CUS03, periodicidad forzada de 15 min y recordatorio fijo en 36h en CUS23, tope de 3 evaluaciones en CUS16, límite de inscripciones simultáneas en CUS18. | RF07, RF15, RF20, RN-04 | Eliminar o generalizar parámetros rígidos arbitrarios; respaldar las validaciones en políticas institucionales vigentes sin inventar topes operativos desconectados de los RF. | Resuelto |
| **INC-10** | Secciones 5.3, 6.2.3, Modelo Lógico | Discrepancia en enumerados y estados del ciclo de vida: uso de `CANCELADA_POR_USUARIO`, `CANCELADA_POR_QUORUM`, `CANCELADA_QUORUM_SISTEMA`, `COMPLETADA`, `ASISTIO`/`FALTO` frente al modelo de datos. | Diagrama 6.16 (`EstadoSesionEnum`, `EstadoReservaEnum`) | Armonizar unívocamente todos los estados: `CANCELADA_USUARIO`, `CANCELADA_QUORUM`, `CANCELADA_SISTEMA`, `FINALIZADA`, `ASISTIDA`, `INASISTENCIA`, sin estados huérfanos. | Resuelto |
| **INC-11** | Sección 6.2.3 | Organización puramente secuencial (CUS01 a CUS24) desconectada de la arquitectura modular y de la precedencia lógica del ciclo de vida de mentoría. | Sección 5.1 / 6.2.2 / Metodología OOSE | Reorganizar la sección 6.2.3 bajo encabezados modulares (`### MOD-01` a `MOD-08`) y ordenar los CUS por dependencia operativa natural del flujo del sistema. | Resuelto |

Fuente: Elaboración propia.

---

## 2. Decisiones de Diseño y Acciones Aplicadas

### 2.1. Resolución de INC-01: Política de Antelación en Publicación de Ofertas
- **Diagnóstico:** Para que un mentoreado pueda ratificar su asistencia hasta $T-24\text{ h}$ (RN-08), es un requisito lógico inherente que la oferta sea publicada con una antelación superior a 24 horas.
- **Ajuste:** En `RN-04` se formaliza la antelación temporal requerida: las sesiones deben publicarse con una anticipación mínima reglamentaria superior a la ventana de confirmación ($T > 24\text{ h}$, con un estándar institucional recomendado de 48 horas), permitiendo la indexación en el recomendador y la adecuada concurrencia de reservas. Se ajusta la redacción de `CUS06` para que cite coherentemente esta disposición sin contradicciones.

### 2.2. Resolución de INC-02: Preservación de la Gobernanza del Mentor (CUS23 ↔ CUS07)
- **Diagnóstico:** RN-09 y RF16 establecen que la decisión de dictado ante quórum insuficiente recae en el criterio formativo del Mentor.
- **Ajuste:** Se modifica el flujo alternativo `FA01` de `CUS23`. Si una sesión registra cero confirmados al corte de $T-24\text{ h}$, el sistema no auto-cancela la sesión de forma arbitraria; transiciona la oferta a estado `QUORUM_INSUFICIENTE` y despacha la alerta al mentor en `CUS07`. Si el mentor no decide antes del plazo límite ($T-6\text{ h}$), opera la cancelación por omisión reglamentaria documentada en E01 de CUS07.

### 2.3. Resolución de INC-03: Depuración de Alcance en CUS04 y CUS17
- **Diagnóstico:** Ni RF12 ni RN-05 incluyen lista de espera ni topes de reservas simultáneas.
- **Ajuste:** Se eliminan de `CUS04` y `CUS17` todas las menciones a colas de espera automáticas y límites no normados. El flujo se concentra con pureza en: selección de oferta, verificación transaccional de aforo libre (10 presencial / 20 virtual según RN-05), registro de reserva en `PENDIENTE_CONFIRMACION` y notificación de confirmación pendiente.

### 2.4. Resolución de INC-04: Ubicación Arquitectónica Definitiva del Parser
- **Diagnóstico:** El parser de horarios es un módulo de procesamiento interno de archivos Excel/PDF cargados por el administrador en el backend, no un servicio de terceros.
- **Ajuste:** Se corrige el Cuadro 6.1 (Perfiles), el Diagrama 6.3 (Paquetes) y el Diagrama 6.13 (ECB). El Parser se define unívocamente como componente interno de `MOD-04`. Los servicios externos quedan restringidos a Google Meet API, Bot de Discord y Servidor SMTP institucional.

### 2.5. Resolución de INC-05: Clarificación del Esquema de Certificados y Verificación QR
- **Diagnóstico:** Coherencia con la exclusión declarada en la Sección 3.4.
- **Ajuste:** Se elimina cualquier mención a "firma digital con certificados de terceros o infraestructura PKI compleja". Se estandariza el mecanismo oficial:
  1. Generación de constancia académica en PDF con membrete institucional de la EPIS-UPT.
  2. Asignación de código correlativo único institucional (`correlativo_resolucion`).
  3. Cálculo del hash criptográfico SHA-256 sobre el archivo emitido para garantizar su integridad.
  4. Inclusión de un código QR en el documento que redirige a la página pública de consulta institucional de la UPT para validación en línea.

### 2.6. Resolución de INC-06: Calibración del Nivel de Detalle en CUS01
- **Diagnóstico:** No convertir parámetros de implementación en requisitos contractuales no justificados.
- **Ajuste:** En `CUS01`, los parámetros de OTP se expresan en función de la política establecida en RN-01 (código de un solo uso por correo con expiración de 5 minutos) y mecanismos estándar de control contra abusos, sin sobrecargar la especificación con restricciones no aprobadas institucionalmente.

### 2.7. Resolución de INC-07: Sincronización de Modelos UML y Hardening Continuo
- **Diagnóstico:** Existían rezagos en los modelos UML (Diagramas 6.3, 6.13, 6.15 y 6.16) que incluían el parser como adaptador externo, métodos de límites no reglamentados (`verificarLimiteReservas() [máx 3]`) o signaturas alusivas a firmas PKI comerciales.
- **Ajuste:** Se armonizaron tanto en `docs/FD03-EPIS-Informe SRS de Proyecto.md` como en `docs/diagramas_general.md`:
  1. **Diagrama 6.3 (Paquetes):** El parser se integró al backend interno en `PKG-SRV-04` y se removió de adaptadores externos.
  2. **Diagrama 6.13 (ECB):** Se sustituyó `verificarLimiteReservas() [máx 3]` por `verificarElegibilidadMentoreado()`, eliminando menciones al tope arbitrario de tres reservas.
  3. **Diagrama 6.15 (Secuencia):** Se reemplazó la guarda `ReservasActivas(usuario) < 3` por `ElegibilidadValidada` y se afinó la conclusión técnica transaccional.
  4. **Diagrama 6.16 (Clases lógicas):** En la clase `CertificadoMentor`, se renombró el método `+generarFirmaCriptografica(): String` a `+calcularHashVerificacion(): String` y se sincronizó su conclusión para respaldar el esquema institucional de constancia PDF/A foliada, hash SHA-256 y QR web.

### 2.8. Resolución de INC-08: Rigor Académico y Supresión de Sesgos Absolutistas
- **Diagnóstico:** Presencia de términos absolutistas ("completamente blindado", "elimina cualquier posibilidad", "garantiza al 100%") y referencias obsoletas a encuestas psicométricas en narrativas y conclusiones.
- **Ajuste:** Se atenuó la redacción global adoptando terminología técnica propia de ingeniería de software orientada a mitigación de riesgos, prevención de fallas y consistencia metodológica. Asimismo, se depuraron las menciones a "encuestas psicométricas" en CUS05, consolidando la denominación "encuesta estructurada de calidad pedagógica institucional".

### 2.9. Resolución de INC-09: Depuración de Reglas Ocultas y Parámetros Arbitrarios
- **Diagnóstico:** Existían topes y cadencias temporales rígidas inventadas en las narrativas que carecían de base en los Requerimientos Funcionales y Reglas de Negocio (ej. tope de 3 solicitudes en `CUS03`, cron de 15 min y recordatorio fijo en 36h en `CUS23`, mínimo 3 evaluaciones para calibración en `CUS16`, límite de inscripciones simultáneas en `CUS18`).
- **Ajuste:** Se armonizaron las narrativas para alinearlas con la línea base oficial:
  1. En `CUS03`: La excepción E02 se definió como "Solicitud pendiente duplicada para el mismo tema silábico", retirando el tope arbitrario de tres solicitudes.
  2. En `CUS23`: Se eliminó la periodicidad rígida de 15 minutos y la ventana fija de 36 horas; se especificó la ejecución a través de servicios programados de fondo (*cron job*) y el despacho de recordatorios preventivos previos a la ventana de confirmación.
  3. En `CUS16`: Se generalizó la excepción E01 a proceso de calibración inicial de reputación docente según políticas EPIS.
  4. En `CUS18`: Se eliminó la referencia a "restitución del límite de inscripciones simultáneas", enfocándolo en la liberación efectiva de cupos y recálculo de aforo.

### 2.10. Resolución de INC-10: Armonización de Estados y Enumerados
- **Diagnóstico:** Se identificaron discrepancias léxicas entre estados utilizados en las narrativas de CUS / requerimientos funcionales y los enumerados formales definidos en el Modelo Lógico de Clases (Diagrama 6.16: `EstadoSesionEnum` y `EstadoReservaEnum`).
- **Ajuste:** Se homogeneizó la totalidad de estados a lo largo de FD03 y diagramas_general:
  1. `EstadoSesionEnum`: `BORRADOR`, `PUBLICADA`, `CONFIRMADA`, `CONFIRMADA_EXCEPCIONAL`, `QUORUM_INSUFICIENTE`, `EN_CURSO`, `FINALIZADA`, `CANCELADA_MENTOR`, `CANCELADA_QUORUM`. Se erradicaron variantes no reconocidas como `COMPLETADA` (sustituida por `FINALIZADA`) y `CANCELADA_POR_QUORUM` (sustituida por `CANCELADA_QUORUM`).
  2. `EstadoReservaEnum`: `PENDIENTE_CONFIRMACION`, `CONFIRMADA`, `CANCELADA_USUARIO`, `NO_CONFIRMADA`, `CANCELADA_SISTEMA`, `ASISTIDA`, `INASISTENCIA`. Se sustituyeron unívocamente `CANCELADA_POR_USUARIO` $\rightarrow$ `CANCELADA_USUARIO`, `CANCELADA_QUORUM_SISTEMA` $\rightarrow$ `CANCELADA_SISTEMA`, y las marcas de asistencia `ASISTIO` / `FALTO` $\rightarrow$ `ASISTIDA` / `INASISTENCIA`.

### 2.11. Resolución de INC-11: Reorganización Modular y Precedencia Operativa en 6.2.3
- **Diagnóstico:** La presentación de los escenarios CUS01 a CUS24 en estricto orden correlativo numérico generaba saltos cognitivos que oscurecían el flujo de negocio real y contradecían la agrupación establecida en la Sección 5.1 y 6.2.2.
- **Ajuste:** Se estructuró la sección 6.2.3 bajo encabezados modulares formales (`### MOD-01` a `### MOD-08`). Dentro de cada módulo, los casos de uso se ordenaron por dependencia funcional y ciclo de vida de la mentoría:
  - **MOD-01:** `CUS01` $\rightarrow$ `CUS10`
  - **MOD-02:** `CUS21` $\rightarrow$ `CUS15`
  - **MOD-03:** `CUS02` $\rightarrow$ `CUS03`
  - **MOD-04:** `CUS11` $\rightarrow$ `CUS06` $\rightarrow$ `CUS18`
  - **MOD-05:** `CUS04` $\rightarrow$ `CUS24` $\rightarrow$ `CUS17` $\rightarrow$ `CUS23` $\rightarrow$ `CUS07`
  - **MOD-06:** `CUS20` $\rightarrow$ `CUS08` $\rightarrow$ `CUS05` $\rightarrow$ `CUS19`
  - **MOD-07:** `CUS16` $\rightarrow$ `CUS13` $\rightarrow$ `CUS09`
  - **MOD-08:** `CUS12` $\rightarrow$ `CUS14` $\rightarrow$ `CUS22`
  Se respetó estrictamente la estructura canónica de 4 tablas por CUS (Ficha, Flujo Principal, Flujos Alternativos, Eventos de Excepción) y se sincronizó este orden en la columna "CUS Asociados" del Cuadro 5.1 en FD03 y diagramas_general.md.


## 3. Revisión de alineación del SAD con la línea base SRS — 28/09/2026

Esta revisión corresponde a la **fase de análisis — desarrollo del SAD**. A solicitud del equipo se conserva el SRS como fuente de nomenclatura y se adapta el SAD. Las tablas 5.1–5.5 fijan MOD, RF, RNF y RN; las narrativas 6.2.3 fijan los CUS. El SRS no se modifica en este ciclo. Los estados históricos de la sección 1 se conservan como registro de revisiones anteriores y no acreditan que todos los artefactos posteriores permanezcan alineados.

### Cuadro 3.1: Correcciones documentales y pendientes de análisis

| ID | Hallazgo | Acción / referencia | Estado |
| :--- | :--- | :--- | :--- |
| SAD-01 | Reasignación de módulos y RF en el SAD. | Cuadros 1.1 y 4.1 conservan denominación, módulo y prioridad del SRS; 4.3 añade trazabilidad a vistas. | Corregido documentalmente. |
| SAD-02 | RNF renumerados y metas añadidas sin origen. | Cuadro 4.2 transcribe RNF01–RNF10; escenarios de calidad usan sus métricas. | Corregido documentalmente. |
| SAD-03 | CUS10/CUS11 usados para bitácora/asistencia; códigos divergentes en secuencias. | CUS10: roles; CUS11: horarios; CUS08: bitácora/asistencia. Catálogo de 24 CUS en SAD 5.1 y cuatro secuencias corregidas. | Corregido en SAD y complemento. |
| SAD-04 | Autenticación descrita como OAuth/TOTP y JWT de 15 minutos. | OTP por correo ≤5 minutos y JWT HMAC-SHA256 de 8 horas según RNF01. S-01 incorpora el desafío OTP. | Corregido documentalmente. |
| SAD-05 | Parser presentado como sistema externo. | Componente interno de MOD-04, RF10 y CUS11 en contexto, componentes y contenedores. | Corregido documentalmente. |
| SAD-06 | Reserva confirmada al crear, lista de espera, quórum de dos y cancelación automática al corte en S-03. | Reserva PENDIENTE_CONFIRMACION; CUS24 ratifica; corte 50% según RN-09; CUS07 decide. Inacción T−6 h se remite a E01 del SRS. | Corregido en secuencias. |
| SAD-07 | Encuesta usada para acreditar horas y QR con rol inverso en S-04. | Mentor marca o escanea ticket del alumno; cierre genera horas provisionales y CUS22 las visa. | Corregido en secuencias. |
| SAD-08 | Vistas presentadas como implementación o garantía ya probada. | Estado explícito de análisis; propuestas, límites y verificaciones futuras en SAD, README y reglas v1.3. | Corregido documentalmente. |
| SAD-09 | Anonimato irreversible afirmado pese al vínculo encuesta–reserva–usuario. | Se retira esa garantía y se identifica seudonimización en SAD 10. Diseño de separación, permisos y retención por completar. | Advertencia corregida; diseño pendiente. |
| SAD-10 | Sincronización incompleta de SAD y bóveda. | Sección 14 de diagramas_general.md con todos los diagramas y cuadros actuales del SAD y complemento de secuencias. | Sincronizado documentalmente. |
| PEN-01 | Diagramas del SRS 6.3 usan CUS09 para publicación, CUS14 para agenda y CUS10/CUS11 para bitácora/asistencia, en conflicto con 6.2.3. | Revisar esos diagramas y sus copias sin renumerar las narrativas. SRS intacto en este ciclo. | Pendiente en artefactos heredados. |
| PEN-02 | El Cuadro 5.5 del SRS usa PENDIENTE, mientras CUS04 usa PENDIENTE_CONFIRMACION. | SAD conserva la transcripción de la matriz y usa PENDIENTE_CONFIRMACION en modelos dinámicos según narrativa; conciliar la celda del SRS posteriormente. | Pendiente en SRS. |
| PEN-03 | RN-11 enumera desempates y RF24 bonificación; modelos posteriores introducen pesos alfa. | Definir fórmula y relación entre prioridad y desempates sin imponer rango numérico nuevo en el SAD. | Pendiente de análisis. |
| PEN-04 | Modelo ER parcial y topología sin dimensionamiento. | Completar entidades faltantes, contratos, permisos, caché, recuperación y capacidad antes de implementar. | Pendiente de diseño. |
| PEN-05 | Referencias normativas y afirmaciones legales requieren revisión. | Verificar reglamentación vigente de Ley 29733 y sustento institucional de certificación. El SAD no acredita cumplimiento legal. | Pendiente de revisión normativa. |
| PEN-06 | Resumen ejecutivo y otros modelos históricos pueden conservar códigos previos. | Revisar propagación del catálogo canónico a resumen_sistema_y_casos_de_uso.md y otros complementos del SRS en un ciclo específico. | Pendiente fuera del alcance de adaptación del SAD. |

Fuente: Comparación documental del SRS, SAD, complemento de secuencias y decisiones previas de esta matriz.

Los elementos corregidos corresponden a coherencia documental, no a software construido o probado. La evolución hacia diseño debe resolver los pendientes sin cambiar silenciosamente códigos o métricas de la línea base. Las verificaciones de sincronización y estructura se realizan sobre los archivos Markdown; el renderizado de PlantUML se valida por separado cuando se dispone de compilador.
