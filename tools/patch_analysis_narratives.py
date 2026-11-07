# -*- coding: utf-8 -*-
"""
Helper script to update CUS-023, CUS-007, CUS-012, CUS-013 in:
- docs/analisis/NARRATIVAS_SRS_CONSOLIDADAS.md
- docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md
"""

import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from audit_srs import audit_narratives

CUS_023 = """#### CUS-023 - Evaluar quórum automático a T-24h

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-023 |
| **Nombre** | Evaluar quórum automático a T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-015 (Monitoreo desatendido, alertas y quórum en T-24h); RN-04 (Ventana de ratificación previa), RN-05 (Regla de quórum mínimo de 3 estudiantes en presencial o 5 en virtual / 50%), RN-10 (Automatización de eventos temporales a T-24h) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Gestor de Tareas Desatendidas (*Servicio Programado / Segundo Plano*)<br>**Secundario:** Estudiante Mentor, Estudiantes Mentoreados con reserva, Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 |
| **Descripción** | Proceso automatizado y desatendido que se ejecuta exactamente 24 horas antes del inicio programado de una sesión de mentoría en estado `PUBLICADA` ($T-24\\text{ h}$), garantizando idempotencia transaccional mediante marca temporal de evaluación para evitar ejecuciones repetidas y cerrojo de fila. El sistema cierra perentoriamente la ventana de confirmación, caduca las reservas provisionales no ratificadas pasando su estado a `CANCELADA_NO_CONFIRMADA` para liberar el aforo, cuantifica las reservas con asistencia ratificada en estado `CONFIRMADA` y evalúa el cumplimiento del quórum reglamentario (mínimo 3 estudiantes en modalidad presencial o 5 en virtual, o al menos el 50% de la capacidad). Si se alcanza el quórum, la sesión se promueve automáticamente a `CONFIRMADA`; de no alcanzarse, la sesión transiciona a `QUORUM_INSUFICIENTE` y se despachan notificaciones prioritarias al mentor para su decisión resolutiva (CUS-007). |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT, Reglamento Académico de Quórum EPIS-UPT |
| **Anexos** | Notificación Desatendida de Quórum Reglamentario Suficiente, Alerta Prioritaria al Mentor por Quórum Insuficiente con Enlace Resolutivo (`CUS-007`), Registro de Auditoría de Tareas Programadas. |
| **Precondiciones** | 1. La sesión de mentoría se encuentra en estado `PUBLICADA` y no registra marca temporal previa de evaluación de quórum.<br>2. La fecha y hora actual del servidor alcanza o supera la marca temporal de 24 horas previas al inicio de la sesión ($T \\le 24\\text{ h}$). |
| **PostCondiciones** | 1. Las reservas asociadas en estado `PENDIENTE_CONFIRMACION` caducan y transicionan a `CANCELADA_NO_CONFIRMADA`.<br>2. La sesión registra su marca temporal de evaluación para garantizar estricta idempotencia.<br>3. Si se alcanza el quórum reglamentario, la sesión transiciona a `CONFIRMADA` y se despachan las instrucciones de acceso final.<br>4. Si no se alcanza el quórum reglamentario, la sesión transiciona a `QUORUM_INSUFICIENTE` y se activa el flujo de contingencia docente (`CUS-007`). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Detección programada y corte de ventana de ratificación** | |
| **1.** El proceso de tareas desatendidas en segundo plano inspecciona periódicamente la base de datos y localiza las sesiones en estado `PUBLICADA` que distan 24 horas o menos de su inicio ($T \\le 24\\text{ h}$) y no han sido evaluadas previamente. | **2.** El sistema bloquea concurrentemente el registro de la sesión para evitar colisiones y cierra de forma definitiva la ventana de ratificación. Localiza las reservas que permanecen en estado `PENDIENTE_CONFIRMACION`, actualiza su estado a `CANCELADA_NO_CONFIRMADA` por expiración de plazo y notifica a los alumnos omisos. |
| **Fase 2: Conteo de confirmados y evaluación del quórum reglamentario** | |
| **3.** El sistema contabiliza las reservas que ostentan el estado `CONFIRMADA` y determina el umbral reglamentario aplicable según la modalidad de dictado (mínimo 3 estudiantes en presencial o 5 en virtual, o el 50% del aforo máximo). | **4.** El sistema evalúa si el recuento de confirmados satisface el quórum mínimo exigido. (Si el quórum reglamentario se cumple satisfactoriamente, salta a A001). (Si el quórum de confirmados es estrictamente inferior al umbral, salta a E001). |
| **Fase 3: Formalización transaccional e idempotencia de evaluación** | |
| **5.** El sistema estampa la marca temporal de evaluación de quórum en la sesión garantizando que no se reevalúe en ejecuciones posteriores. | **6.** El sistema consolida la transacción, registra la traza de auditoría y remite las comunicaciones institucionales correspondientes. |

##### Flujos Alternativos

##### Flujo alternativo A001: Quórum reglamentario alcanzado (Sesión confirmada)
| Usuario | Sistema |
|---|---|
| **A001-1.1** El sistema verifica que la sesión cuenta con 3 o más confirmados en modalidad presencial (o 5 o más en virtual). | **A001-1.2** El sistema transiciona el estado de la sesión a `CONFIRMADA`, asegura de forma definitiva el aula física o el enlace virtual y despacha un correo de confirmación de dictado al mentor y a los participantes con el mensaje literal: *"¡Quórum reglamentario alcanzado! Tu sesión de mentoría está confirmada para su ejecución"*. |
| **A001-1.3** El mentor y los estudiantes inscritos reciben la notificación institucional en sus paneles y bandejas de correo. | **A001-1.4** El sistema actualiza el calendario académico de mentorías y el sistema retorna al paso 5 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Quórum insuficiente al corte de 24 horas (Alerta al mentor)
| Usuario | Sistema |
|---|---|
| **E001-1.1** El cómputo de reservas confirmadas no alcanza el umbral mínimo reglamentario (menos de 3 alumnos en presencial o menos de 5 en virtual). | **E001-1.2** El sistema transiciona el estado de la sesión a `QUORUM_INSUFICIENTE`, genera una notificación prioritaria al mentor con el mensaje literal: *"Atención: Tu sesión no alcanzó el quórum reglamentario al corte T-24h. Ingresa a la plataforma para decidir si dictas con aforo reducido, reprogramas o cancelas la sesión"* y habilita el acceso al caso de uso resolutivo `CUS-007`. |
| **E001-1.3** El mentor recibe la notificación de contingencia en su panel de control y correo institucional. | **E001-1.4** El sistema concluye el caso de uso y transfiere el flujo a la toma de decisión del mentor (`CUS-007`). |"""

CUS_007 = """#### CUS-007 - Decisión del mentor ante quórum insuficiente

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-007 |
| **Nombre** | Decisión del mentor ante quórum insuficiente |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-016 (Gestión resolutiva ante quórum insuficiente); RN-04 (Antelación mínima de 24 horas para reprogramaciones), RN-05 (Aforo y contingencia de quórum), RN-10 (Resolución oportuna de contingencia y motivos pedagógicos) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentor (*Responsable de la sesión*)<br>**Secundario:** Estudiantes Mentoreados con reserva confirmada, Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 |
| **Descripción** | Permite al Estudiante Mentor adoptar una decisión resolutiva institucional oportuna frente a una sesión de mentoría que al corte perentorio de 24 horas previas ($T-24\\text{ h}$) ha sido catalogada con `QUORUM_INSUFICIENTE` (CUS-023). El mentor accede al módulo de contingencias en su panel docente y dispone de tres alternativas reglamentarias: (1) Dictar la sesión con aforo reducido confirmando la ejecución para beneficiar a los estudiantes confirmados (`CONFIRMADA`), (2) Reprogramar la sesión para una nueva fecha y hora con antelación mínima mayor a 24 horas respecto al momento actual (RN-04) retornando a estado `PUBLICADA`, o (3) Cancelar definitivamente la sesión consignando una justificación pedagógica obligatoria (RN-10), lo que muta la sesión a `CANCELADA_QUORUM`, cancela en cascada las reservas a `CANCELADA_SISTEMA_QUORUM` y libera los recursos sin penalización académica. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT, Reglamento Académico de Mentorías EPIS-UPT |
| **Anexos** | Panel de Gestión de Contingencias de Quórum con Distintivo Ámbar, Cuadro Modal Accesible de Resolución con Tres Opciones, Formulario de Reprogramación Horaria, Formulario de Cancelación con Justificación Pedagógica. |
| **Precondiciones** | 1. La sesión de mentoría ha sido evaluada a $T-24\\text{ h}$ y se encuentra en estado `QUORUM_INSUFICIENTE` (`CUS-023`).<br>2. El mentor ha iniciado sesión institucional activa con su cuenta universitaria `@upt.pe` (`CUS-001`).<br>3. La resolución se despacha antes del horario de inicio programado de la sesión. |
| **PostCondiciones** | 1. Si decide dictar, la sesión transiciona al estado `CONFIRMADA` con indicador de aforo reducido y se ratifica la agenda para los inscritos.<br>2. Si decide reprogramar, la sesión actualiza su horario con antelación mayor a 24 horas, restablece el estado a `PUBLICADA` y se notifica a los participantes.<br>3. Si decide cancelar, la sesión transiciona a `CANCELADA_QUORUM`, las reservas pasan a `CANCELADA_SISTEMA_QUORUM`, se liberan los recursos y se notifica con el motivo pedagógico. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso a la gestión de contingencia y despliegue modal** | |
| **1.** El Mentor recibe la alerta institucional o accede a la sección de sesiones en su panel docente, visualizando la tarjeta de la sesión destacada con un distintivo en color ámbar de advertencia con la etiqueta *"Quórum Insuficiente"* y presiona el botón `"Gestionar Contingencia"`. | **2.** El sistema despliega un cuadro de diálogo modal accesible que presenta la información de la sesión, la cantidad de alumnos confirmados frente al quórum esperado y las tres opciones resolutivas: `"Dictar con Aforo Reducido"`, `"Reprogramar Sesión"` y `"Cancelar Sesión Definitivamente"`. (Si el mentor opta por reprogramar la sesión para una nueva fecha, salta a A001). (Si el mentor opta por cancelar definitivamente la sesión, salta a A002). |
| **Fase 2: Confirmación de dictado con aforo reducido** | |
| **3.** El Mentor selecciona la opción `"Dictar con Aforo Reducido"` para brindar la mentoría a los alumnos confirmados y presiona el botón `"Confirmar Resolución"`. | **4.** El sistema solicita ratificar la decisión de impartir la clase, indicando que la realización con aforo reducido no genera descuento de horas docentes ni afecta su reputación académica. |
| **Fase 3: Formalización transaccional y comunicación a los alumnos** | |
| **5.** El Mentor presiona el botón `"Confirmar y Proceder con el Dictado"`. | **6.** El sistema transiciona la sesión al estado `CONFIRMADA`, bloquea de forma definitiva el espacio educativo, despacha un correo de ratificación a los estudiantes inscritos con sus instrucciones de acceso y despliega una notificación en color verde de éxito con el mensaje literal: *"¡Sesión confirmada! Se ha ratificado la realización de la sesión con los estudiantes inscritos"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Reprogramación de la sesión con nueva fecha y hora (RN-04)
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 2 del Flujo Normal, el Mentor selecciona la opción `"Reprogramar Sesión"`. | **A001-1.2** El sistema despliega un selector de fecha y franja horaria junto con un aviso que recuerda la regla institucional RN-04: la nueva fecha debe fijarse con al menos 24 horas de antelación respecto a la hora actual. |
| **A001-1.3** El Mentor selecciona la nueva fecha y hora y presiona el botón `"Confirmar Reprogramación"`. (Si la fecha seleccionada no cumple con la antelación mayor a 24 horas, salta a E001). | **A001-1.4** El sistema actualiza el cronograma de la sesión, restablece el estado a `PUBLICADA`, resetea la marca de evaluación de quórum, despacha una notificación por correo a los estudiantes inscritos invitándolos a ratificar su asistencia para el nuevo horario, muestra un aviso en color verde de éxito con el texto literal: *"Sesión reprogramada exitosamente. Se ha notificado a los alumnos sobre el nuevo horario"* y el sistema finaliza el caso de uso sin generar penalidades. |

##### Flujo alternativo A002: Cancelación definitiva por quórum insuficiente con motivo justificado (RN-10)
| Usuario | Sistema |
|---|---|
| **A002-1.1** En el paso 2 del Flujo Normal, el Mentor selecciona la opción `"Cancelar Sesión Definitivamente"`. | **A002-1.2** El sistema presenta un cuadro de texto multilínea solicitando ingresar obligatoriamente una justificación pedagógica clara para los estudiantes y la dirección académica conforme a RN-10, junto con el botón `"Confirmar Cancelación Definitiva"`. |
| **A002-1.3** El Mentor redacta la justificación pedagógica y presiona el botón `"Confirmar Cancelación Definitiva"`. (Si el mentor intenta enviar la cancelación dejando el motivo en blanco, salta a E002). | **A002-1.4** El sistema transiciona la sesión al estado `CANCELADA_QUORUM`, cancela en cascada las reservas de los estudiantes marcándolas como `CANCELADA_SISTEMA_QUORUM`, libera el aula física o la sala virtual, notifica a los participantes afectados con el justificativo consignado, muestra un mensaje en color gris informativo con el texto literal: *"Sesión cancelada definitivamente por quórum insuficiente sin penalidad académica"* y el sistema finaliza el caso de uso sin aplicar deméritos al mentor. |

##### Flujos de Excepción

##### Flujo de excepción E001: Reprogramación con antelación inferior a 24 horas (Infracción de RN-04)
| Usuario | Sistema |
|---|---|
| **E001-1.1** En el paso A001-1.3, el Mentor ingresa una fecha u hora que dista menos de 24 horas respecto al tiempo actual del servidor. | **E001-1.2** El sistema bloquea el procesamiento, resalta el campo de fecha con un borde en color rojo de error y presenta una alerta con el mensaje literal: *"Fecha no permitida: Toda reprogramación debe realizarse con un mínimo de 24 horas de antelación para salvaguardar la disponibilidad estudiantil"*. |
| **E001-1.3** El Mentor presiona el botón `"Modificar Fecha"` y ajusta el calendario a una fecha válida. | **E001-1.4** El sistema valida que el nuevo horario cumpla el margen de 24 horas y el sistema retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Justificación pedagógica de cancelación omitida o en blanco (Infracción de RN-10)
| Usuario | Sistema |
|---|---|
| **E002-1.1** En el paso A002-1.3, el Mentor presiona el botón de confirmación de cancelación dejando el cuadro de texto vacío o con espacios en blanco. | **E002-1.2** El sistema bloquea la transacción, resalta el área de texto con un borde en color rojo de error y despliega una advertencia con el mensaje literal: *"Motivo requerido: Debe ingresar obligatoriamente una justificación pedagógica para informar a los estudiantes la cancelación de la sesión"*. |
| **E002-1.3** El Mentor redacta la justificación en el área de texto. | **E002-1.4** El sistema comprueba que el texto contenga información descriptiva y el sistema retorna al paso 3 del Flujo Normal de Eventos. |"""

CUS_012 = """#### CUS-012 - Registrar asistencia a sesión de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-012 |
| **Nombre** | Registrar asistencia a sesión de mentoría |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-017 (Registro de bitácora pedagógica y control de asistencia); RN-05 (Aforo y presencia efectiva), RN-12 (Trazabilidad de asistencia y ventana temporal de check-in) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentor (*Responsable del pase de lista*), Estudiante Mentoreado (*Asistente*)<br>**Secundario:** Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 |
| **Descripción** | Permite registrar la presencia efectiva de los estudiantes durante la ejecución de una sesión de mentoría en estado `CONFIRMADA` o `EN_CURSO`. El mentor proyecta en pantalla un código QR dinámico criptográfico generado con algoritmo de contraseña de un solo uso por tiempo (TOTP) que se refresca automáticamente cada 30 segundos, acompañado de un código numérico de respaldo de 6 dígitos y un temporizador regresivo circular. El estudiante mentoreado escanea el código QR desde su dispositivo o ingresa el código numérico de 6 dígitos dentro del intervalo temporal reglamentario (desde 15 minutos antes del inicio programado hasta 30 minutos tras la finalización). El sistema verifica que el token esté vigente y que el alumno cuente con reserva confirmada en la sesión, persistiendo de forma fehaciente la asistencia y actualizando en tiempo real la nómina del mentor. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT, Reglamento Académico de Asistencia EPIS-UPT |
| **Anexos** | Pantalla de Control de Asistencia Digital con Proyector QR SVG en Alta Definición, Temporizador Regresivo Circular de 30 Segundos, Código Numérico de Respaldo de 6 Dígitos, Nómina Reactiva de Estudiantes en Tiempo Real. |
| **Precondiciones** | 1. La sesión de mentoría se encuentra en estado `CONFIRMADA` o `EN_CURSO`.<br>2. El estudiante mentoreado cuenta con una reserva en estado `CONFIRMADA` para dicha sesión.<br>3. La solicitud se realiza dentro del intervalo temporal permitido (desde 15 minutos antes del inicio hasta 30 minutos después del fin). |
| **PostCondiciones** | 1. Se registra la presencia del estudiante mentoreado en la bitácora de asistencias de la sesión.<br>2. La nómina interactiva en la pantalla del mentor actualiza reactivamente el estado del alumno a `"Presente"` con un distintivo en color verde.<br>3. El estudiante recibe un comprobante digital de asistencia en su dispositivo y queda habilitado para diligenciar la evaluación de calidad post-mentoría. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura de asistencia y proyección del código QR dinámico** | |
| **1.** El Mentor accede a su sesión en la plataforma y pulsa el botón `"Iniciar Pase de Asistencia Digital"`. | **2.** El sistema genera un token dinámico basado en tiempo con rotación estricta cada 30 segundos, despliega el código QR interactivo de alta definición junto a un código numérico de 6 dígitos y un temporizador circular, y presenta la lista nominal de los estudiantes confirmados en condición inicial de `"Ausente"`. |
| **Fase 2: Escaneo del código o ingreso de clave numérica por el mentoreado** | |
| **3.** El estudiante mentoreado presente en la sesión enfoca con la cámara de su dispositivo el código QR proyectado y pulsa el botón `"Registrar Mi Asistencia"`. (Si el estudiante no puede escanear la imagen por limitaciones de hardware, salta a A001). | **4.** El sistema valida que el token del código no haya expirado, que el estudiante posea una reserva confirmada en la sesión y que la petición ocurra dentro de la ventana de validez horaria (15 minutos antes del inicio hasta 30 minutos tras el fin). (Si el token de 30 segundos ha expirado, salta a E001). (Si el estudiante no posee reserva confirmada, salta a E002). (Si el intento se realiza fuera del intervalo de tolerancia horaria, salta a E003). |
| **Fase 3: Persistencia de presencia y actualización reactiva de nómina** | |
| **5.** El estudiante y el mentor observan la confirmación visual instantánea en sus pantallas. | **6.** El sistema registra la asistencia con la marca temporal exacta, actualiza de forma reactiva la fila del estudiante en el panel del mentor mostrándolo como `"Presente"` con distintivo en color verde, y despliega en el dispositivo del alumno un aviso en color verde con el texto literal: *"¡Asistencia registrada exitosamente! Gracias por tu puntualidad"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Registro de asistencia mediante código numérico de respaldo de 6 dígitos
| Usuario | Sistema |
|---|---|
| **A001-1.1** El estudiante no puede enfocar el código QR por falta de cámara o poca iluminación; pulsa la opción `"Ingresar Código Numérico"`. | **A001-1.2** El sistema presenta un formulario con casillas para ingresar el código de 6 dígitos visible en la pantalla del mentor. |
| **A001-1.3** El estudiante digita el código numérico de 6 dígitos y pulsa el botón `"Validar Código de Asistencia"`. | **A001-1.4** El sistema procesa la validación del código temporal y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Código QR o token dinámico expirado al momento de envío
| Usuario | Sistema |
|---|---|
| **E001-1.1** El estudiante envía la solicitud cuando el ciclo de 30 segundos del token ya ha transcurrido. | **E001-1.2** El sistema rechaza la marcación y despliega en el móvil del estudiante una notificación en color ámbar de advertencia con el mensaje literal: *"Código de asistencia expirado. Por favor, escanee o digite el nuevo código proyectado por el mentor"*. |
| **E001-1.3** El estudiante enfoca el nuevo código QR o ingresa la nueva clave numérica generada en pantalla. | **E001-1.4** El sistema captura el nuevo código emitido y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Estudiante sin reserva confirmada en la sesión de mentoría
| Usuario | Sistema |
|---|---|
| **E002-1.1** Un alumno que no reservó cupo o cuya reserva no fue ratificada intenta escanear el código QR. | **E002-1.2** El sistema comprueba la ausencia de reserva confirmada en la base de datos, deniega el registro y presenta una alerta en color rojo de error con el mensaje literal: *"Acceso denegado: No registra una reserva confirmada para participar en esta sesión de mentoría"*. |
| **E002-1.3** El estudiante presiona el botón `"Entendido"`. | **E002-1.4** El sistema cierra el diálogo y finaliza el caso de uso sin generar registros de asistencia. |

##### Flujo de excepción E003: Check-in fuera de la ventana horaria permitida (Infracción de RN-12)
| Usuario | Sistema |
|---|---|
| **E003-1.1** El estudiante intenta registrar asistencia más de 15 minutos antes del inicio de la sesión o más de 30 minutos después de culminada. | **E003-1.2** El sistema bloquea el registro por encontrarse fuera de la ventana horaria institucional y despliega una advertencia en color rojo con el mensaje literal: *"Registro cerrado: El pase de asistencia solo se encuentra habilitado durante la realización de la sesión"*. |
| **E003-1.3** El estudiante pulsa el botón `"Aceptar"`. | **E003-1.4** El sistema devuelve la interfaz al panel principal y finaliza el caso de uso sin generar registros de asistencia. |"""

CUS_013 = """#### CUS-013 - Registrar bitácora académica de sesión

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-013 |
| **Nombre** | Registrar bitácora académica de sesión |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-017 (Registro de bitácora pedagógica y control de asistencia); RN-12 (Plazo perentorio de 48 horas post-sesión para registro de bitácora y observaciones mínimas de 50 caracteres) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentor (*Responsable del reporte formativo*)<br>**Secundario:** Administrador Institucional, Coordinador Académico |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 |
| **Descripción** | Permite al Estudiante Mentor registrar de forma estructurada y fidedigna la bitácora pedagógica correspondiente a una sesión de mentoría concluida dentro del plazo perentorio de 48 horas posteriores a su culminación (RN-12). El mentor accede al formulario digital, selecciona los temas curriculares desarrollados mediante un checklist silábico, evalúa el nivel de asimilación conceptual y dificultad pedagógica (Bajo, Medio, Alto), redacta observaciones cualitativas sustantivas con una extensión no menor a 50 caracteres y suscribe la declaración jurada de veracidad académica. El sistema genera un sello digital criptográfico mediante hash SHA-256 sobre los contenidos consignados garantizando integridad e inalterabilidad, actualiza el estado de la sesión a `BITACORA_REGISTRADA` y acredita las horas pedagógicas provisionales del mentor (`duracion / 60.0`). |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT, Reglamento Académico de Mentorías y Certificación EPIS-UPT |
| **Anexos** | Formulario de Bitácora Pedagógica con Checklist Silábico, Selector de Nivel de Dificultad, Cuadro de Observaciones con Contador de Caracteres, Declaración Jurada de Veracidad, Comprobante con Sello Digital Hash SHA-256. |
| **Precondiciones** | 1. La sesión de mentoría ha concluido su ejecución horaria y se encuentra en estado `CONFIRMADA` o `CONCLUIDA`.<br>2. El mentor cuenta con sesión institucional activa `@upt.pe` (`CUS-001`).<br>3. El plazo transcurrido desde la culminación de la sesión es menor o igual a 48 horas conforme a RN-12. |
| **PostCondiciones** | 1. Se inserta el registro formal de la bitácora pedagógica con sello digital hash SHA-256 inmutable.<br>2. El estado de la sesión transiciona a `BITACORA_REGISTRADA`.<br>3. Las horas de mentoría correspondientes a la duración de la sesión se computan como provisionales para posterior acreditación de créditos extracurriculares. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura de bitácora y verificación de plazo perentorio (RN-12)** | |
| **1.** El Mentor ingresa a la sesión de mentoría concluida en su panel docente y presiona el botón `"Diligenciar Bitácora Pedagógica"`. | **2.** El sistema verifica que el tiempo transcurrido desde la hora de finalización de la sesión no exceda las 48 horas reglamentarias conforme a RN-12. Presenta el formulario oficial con el encabezado en color azul institucional, mostrando el checklist de temas curriculares de la asignatura, el selector de dificultad pedagógica (Bajo, Medio, Alto), el cuadro de observaciones y la casilla de declaración jurada. (Si han transcurrido más de 48 horas desde la finalización, salta a E001). |
| **Fase 2: Consignación de temas silábicos, observaciones y firma** | |
| **3.** El Mentor marca las casillas de los temas curriculares explicados, selecciona el nivel de asimilación conceptual del grupo, redacta las observaciones detalladas del desarrollo de la clase, marca la casilla de declaración jurada de veracidad y presiona el botón `"Firmar y Registrar Bitácora"`. | **4.** El sistema valida que se haya marcado al menos un tema curricular, que el texto de observaciones contenga al menos 50 caracteres descriptivos y que la declaración jurada esté aceptada. (Si el mentor desea adjuntar enlaces o recursos académicos adicionales, salta a A001). (Si las observaciones no alcanzan la longitud mínima de 50 caracteres, salta a E002). |
| **Fase 3: Generación de sello criptográfico SHA-256 y acreditación provisional** | |
| **5.** El Mentor observa el indicador circular de procesamiento seguro mientras el sistema formaliza el registro. | **6.** El sistema calcula el hash criptográfico SHA-256 sobre el contenido pedagógico para garantizar su inalterabilidad, persiste la bitácora, transiciona el estado de la sesión a `BITACORA_REGISTRADA`, registra las horas pedagógicas provisionales del mentor para su posterior certificación y despliega un panel en color verde de éxito con el código del sello digital y el texto literal: *"¡Bitácora pedagógica registrada y firmada exitosamente! Las horas han sido acreditadas provisionalmente para auditoría"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Incorporación de enlaces y recursos de libre descarga
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 4 del Flujo Normal, el Mentor presiona el botón `"Añadir Recursos Didácticos"` e introduce enlaces a repositorios o diapositivas. | **A001-1.2** El sistema valida que los enlaces cuenten con protocolo HTTPS seguro. |
| **A001-1.3** El Mentor confirma la incorporación de los enlaces al expediente de la sesión. | **A001-1.4** El sistema vincula los recursos a la bitácora para consulta de los estudiantes inscritos y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Vencimiento del plazo perentorio de 48 horas (Infracción de RN-12)
| Usuario | Sistema |
|---|---|
| **E001-1.1** El Mentor intenta diligenciar la bitácora habiendo transcurrido más de 48 horas desde la finalización programada de la sesión. | **E001-1.2** El sistema detecta el vencimiento del plazo estricto de 48 horas (infracción de RN-12), bloquea los campos de edición y despliega una advertencia en color ámbar con el mensaje literal: *"Plazo reglamentario vencido: El registro de la bitácora ha superado las 48 horas permitidas. La habilitación extraordinaria requiere autorización de la Coordinación Académica"*. |
| **E001-1.3** El Mentor presiona el botón `"Solicitar Desbloqueo Extraordinario"`. | **E001-1.4** El sistema remite una solicitud a la dirección de escuela y el sistema finaliza el caso de uso sin generar registros ordinarios de bitácora. |

##### Flujo de excepción E002: Observaciones pedagógicas con longitud insuficiente (Menos de 50 caracteres)
| Usuario | Sistema |
|---|---|
| **E002-1.1** En el paso 4 del Flujo Normal, el Mentor intenta registrar la bitácora con un texto de observaciones que no alcanza los 50 caracteres requeridos. | **E002-1.2** El sistema bloquea el envío, resalta el cuadro de texto con un borde en color rojo de error y muestra un contador interactivo junto con el mensaje literal: *"Descripción insuficiente: Las observaciones pedagógicas deben contener un detalle descriptivo de al menos 50 caracteres"*. |
| **E002-1.3** El Mentor amplía la redacción incorporando el detalle del avance académico y las dificultades conceptuales observadas. | **E002-1.4** El sistema comprueba que el texto supere los 50 caracteres y el sistema retorna al paso 3 del Flujo Normal de Eventos. |"""

def replace_cus_in_text(text):
    # Pattern to find CUS block
    # CUS-023
    text = re.sub(
        r'####\s+CUS-023\s+-\s+.*?(?=\n---\n\n####\s+CUS-007)',
        lambda m: CUS_023.strip(),
        text,
        flags=re.DOTALL
    )
    # CUS-007
    text = re.sub(
        r'####\s+CUS-007\s+-\s+.*?(?=\n---\n\n###\s+MOD-06)',
        lambda m: CUS_007.strip(),
        text,
        flags=re.DOTALL
    )
    # CUS-012
    text = re.sub(
        r'####\s+CUS-012\s+-\s+.*?(?=\n---\n\n####\s+CUS-013)',
        lambda m: CUS_012.strip(),
        text,
        flags=re.DOTALL
    )
    # CUS-013
    text = re.sub(
        r'####\s+CUS-013\s+-\s+.*?(?=\n---\n\n####\s+CUS-014)',
        lambda m: CUS_013.strip(),
        text,
        flags=re.DOTALL
    )
    return text

def main():
    # 1. Update NARRATIVAS_SRS_CONSOLIDADAS.md
    path_cons = "docs/analisis/NARRATIVAS_SRS_CONSOLIDADAS.md"
    with open(path_cons, "r", encoding="utf-8") as f:
        cons_text = f.read()

    new_cons = replace_cus_in_text(cons_text)
    
    # Audit before saving
    print("Auditing new consolidated...")
    errs = audit_narratives(new_cons, path_cons)
    if errs > 0:
        print(f"FAILED with {errs} errors.")
        sys.exit(1)
    
    with open(path_cons, "w", encoding="utf-8") as f:
        f.write(new_cons)
    print("Updated", path_cons)

    # 2. Update FD03-EPIS-Informe SRS de Proyecto.md
    path_srs = "docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md"
    with open(path_srs, "r", encoding="utf-8") as f:
        srs_text = f.read()

    m_start = re.search(r'## 6\.2\.3\.?\s+Escenarios de Casos de Uso', srs_text)
    m_next = re.search(r'#+\s+6\.3\.?\s+Modelo L[oó]gico', srs_text)

    prefix = srs_text[:m_start.start()]
    suffix = srs_text[m_next.start():]
    
    # Notice new_cons starts with ## 6.2.3. Escenarios de Casos de Uso (Narrativas)
    new_srs_text = prefix + new_cons + "\n\n---\n\n" + suffix

    print("Auditing new SRS analysis section...")
    errs_srs = audit_narratives(new_cons, path_srs)
    if errs_srs > 0:
        print(f"FAILED with {errs_srs} errors.")
        sys.exit(1)

    with open(path_srs, "w", encoding="utf-8") as f:
        f.write(new_srs_text)
    print("Updated", path_srs)

if __name__ == "__main__":
    main()
