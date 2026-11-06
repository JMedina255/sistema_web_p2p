## 6.2.3. Escenarios de Casos de Uso (Narrativas)

### Presentación de los Escenarios de Casos de Uso
La presente sección formaliza los escenarios detallados de los **24 casos de uso canónicos (`CUS-001` al `CUS-024`)** del Sistema Web P2P de mentorías académicas de la Escuela Profesional de Ingeniería de Sistemas (EPIS-UPT). Conforme al estándar institucional congelado en la guía de gobernanza del proyecto (`docs/analisis/REGLAS_Y_PLANTILLA_NARRATIVAS_SRS.md`), cada caso de uso se especifica bajo una rigurosa articulación con la Guía SWEBOK v3.0, el Estándar ISO/IEC/IEEE 29148:2018, los criterios de acreditación ICACIT y la Ley N° 29733 de Protección de Datos Personales.

Las narrativas se organizan modularmente a lo largo de los ocho (8) subsistemas del proyecto (`MOD-01` al `MOD-08`). Cada caso de uso comprende de forma canónica: (1) Ficha Técnica de Gobernanza con doce (12) atributos de caracterización formal; (2) Flujo Normal de Eventos en tabla estructurada por fases operativas secuenciales con llamadas explícitas de desvío; (3) Flujos Alternativos (`A00X`) con numeración jerárquica y cláusula de cierre o reincorporación; y (4) Flujos de Excepción (`E00X`) con resolución transaccional y salvaguarda de reglas de negocio institucionales.

Toda la interacción con el usuario se documenta con exhaustivo nivel de detalle en lenguaje natural funcional, caracterizando tarjetas interactivas, ventanas modales, botones específicos entre comillas, cuadros de texto, casillas de selección, etiquetas de estado y barras de disponibilidad en paleta institucional (azul institucional, verde de éxito, ámbar de advertencia y rojo de error), erradicando valores técnicos de estilo (códigos hexadecimales o medidas en píxeles) y referencias estáticas o quemadas.

---

### MOD-01: Seguridad, Autenticación y Gobernanza

#### CUS-001 - Iniciar sesión institucional con 2FA

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-001 |
| **Nombre** | Iniciar sesión institucional con 2FA |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-001 (Autenticación institucional multifactor 2FA), RF-002 (Formalización del consentimiento informado digital); RN-01 (Acceso institucional exclusivo y OTP de 5 min), RN-02 (Consentimiento informado legal digital) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Usuario Institucional (*Estudiante Mentoreado, Estudiante Mentor o Administrador*)<br>**Secundario:** Servicio de Correo SMTP / UPT (*Emisor de código OTP*) |
| **Interacción** | Fase de Construcción / Iteración Sprint 01 - Sprint 02 |
| **Descripción** | Permite autenticar de forma segura la identidad de los estudiantes y docentes de la EPIS-UPT utilizando exclusivamente su correo institucional oficial (`@upt.pe`) y un código temporal de un solo uso (OTP) de 6 dígitos numéricos con caducidad estricta de 5 minutos enviado a su buzón, exigiendo en el primer acceso la formalización del consentimiento informado digital para el tratamiento de datos académicos bajo la Ley N° 29733 y expidiendo un token JWT firmado criptográficamente con vigencia de 8 horas para el control de acceso basado en roles. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT, Ley N° 29733 |
| **Anexos** | Pantalla de Autenticación Institucional, Cuadro de Diálogo de Verificación OTP con Temporizador, Modal de Consentimiento Informado Digital Ley N° 29733, Panel Principal (Dashboard) según Rol. |
| **Precondiciones** | 1. El usuario cuenta con una cuenta de correo electrónico institucional activa perteneciente al dominio oficial `@upt.pe`.<br>2. El usuario no registra inhabilitación administrativa o suspensión académica vigente en el padrón universitario.<br>3. El servicio de mensajería SMTP institucional se encuentra operativo. |
| **PostCondiciones** | 1. El sistema genera una sesión activa autenticada mediante token JWT firmado criptográficamente con vigencia de 8 horas.<br>2. Se formaliza y persiste la traza legal inmutable del consentimiento informado digital (UUID del usuario, dirección IP, fecha y hora exacta).<br>3. El usuario es redirigido al panel principal correspondiente a su rol institucional (*Mentoreado, Mentor o Administrador*). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Ingreso de credenciales y comprobación institucional** | |
| **1.** El usuario accede a la plataforma web e ingresa su dirección de correo electrónico institucional en el cuadro de texto `"Correo Institucional"` y presiona el botón `"Continuar"`. | **2.** El sistema valida la sintaxis y verifica que el correo pertenezca estrictamente al dominio oficial universitario `@upt.pe`. Comprueba en el directorio de usuarios que la cuenta no se encuentre inactiva o dada de baja. (Si el dominio es ajeno a la universidad, salta a E001). (Si la cuenta está inactiva o suspendida, salta a E002). |
| **Fase 2: Generación, envío y verificación del código temporal (OTP)** | |
| **3.** El usuario revisa en pantalla el resumen de su correo institucional y presiona el botón `"Solicitar Código de Acceso"`. | **4.** El sistema genera un código OTP criptográficamente aleatorio de 6 dígitos numéricos, le asigna un tiempo de expiración estricto de 5 minutos conforme a RN-01, e invoca al servicio SMTP institucional para despacharlo al buzón universitario del solicitante. Muestra en primer plano una ventana modal con seis casillas individuales para el ingreso del código, un temporizador regresivo de 5 minutos en color azul institucional y el botón `"Verificar e Ingresar"`. (Si el usuario no recibe el código en su buzón tras 60 segundos o el temporizador expira, salta a A002). |
| **5.** El usuario consulta su bandeja de entrada universitaria, copia el código numérico recibido, lo introduce en las casillas correspondientes y presiona el botón `"Verificar e Ingresar"`. | **6.** El sistema valida que el código ingresado coincida con el generado y que no haya expirado. Comprueba si el usuario cuenta con registro previo de consentimiento informado digital en la base de datos. (Si el código es incorrecto, salta a E003). (Si el código ha expirado, salta a E004). (Si se superan los 3 intentos fallidos consecutivos, salta a E005). (Si el usuario ya cuenta con consentimiento digital previo, salta a A001). |
| **Fase 3: Suscripción de consentimiento legal digital y acceso** | |
| **7.** El usuario lee los términos de tratamiento de datos personales desplegados en un panel con barra de desplazamiento vertical, marca la casilla de selección `"He leído y acepto los términos de consentimiento informado bajo la Ley N° 29733"` y presiona el botón `"Aceptar y Continuar"`. (Si el usuario desmarca o rechaza los términos, salta a E006). | **8.** El sistema persiste de forma inmutable el registro de consentimiento asociando el UUID del usuario, dirección IP de origen, fecha y hora exacta, emite un token JWT con vigencia de 8 horas con los roles correspondientes y redirige al panel principal mostrando una notificación flotante en color verde de éxito con el mensaje literal: *"¡Sesión institucional iniciada exitosamente! Bienvenido al Sistema de Mentorías EPIS-UPT"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Acceso recurrente con consentimiento digital previamente formalizado
| Usuario | Sistema |
|---|---|
| **A001-1.1** El usuario completa satisfactoriamente el paso 5 introduciendo el código OTP válido. | **A001-1.2** El sistema detecta en la base de datos la existencia de la traza de consentimiento informado digital bajo la Ley N° 29733 suscrita con anterioridad. |
| **A001-1.3** El usuario visualiza la pantalla de carga con indicador circular de progreso en color azul institucional. | **A001-1.4** El sistema omite la presentación del formulario de términos legales, emite directamente el token JWT firmado de sesión con sus roles asignados y redirige al panel de control correspondiente a su rol y el sistema retorna al paso 8 del Flujo Normal de Eventos. |

##### Flujo alternativo A002: Reenvío de código temporal por retraso en buzón o caducidad
| Usuario | Sistema |
|---|---|
| **A002-1.1** El usuario no recibe el mensaje en su bandeja institucional tras 60 segundos o el temporizador expira; pulsa el botón `"Reenviar código OTP"`. | **A002-1.2** El sistema invalida de forma inmediata el código OTP previo, genera una nueva clave aleatoria de 6 dígitos con vigencia renovada de 5 minutos, la remite vía SMTP y reinicia el temporizador regresivo en pantalla mostrando un mensaje flotante en color azul institucional con el texto literal: *"Un nuevo código de verificación ha sido enviado a tu buzón institucional"*. |
| **A002-1.3** El usuario ingresa la nueva clave numérica recibida. | **A002-1.4** El sistema procesa la validación del nuevo código y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Dominio de correo no institucional
| Usuario | Sistema |
|---|---|
| **E001-1.1** El usuario ingresa una dirección electrónica perteneciente a dominios comerciales externos (e.g. `@gmail.com`, `@outlook.com`). | **E001-1.2** El sistema detecta que la cuenta no pertenece al dominio oficial `@upt.pe`, bloquea el procesamiento, resalta el cuadro de texto con un borde en color rojo de error y despliega una alerta con el mensaje literal: *"Acceso restringido: Ingrese exclusivamente con su cuenta institucional de la Universidad Privada de Tacna (@upt.pe)"*. |
| **E001-1.3** El usuario presiona el botón `"Corregir correo"`. | **E001-1.4** El sistema limpia el campo de entrada y el sistema finaliza el caso de uso sin generar registros. |

##### Flujo de excepción E002: Cuenta institucional inactiva o dada de baja
| Usuario | Sistema |
|---|---|
| **E002-1.1** El usuario ingresa una cuenta del dominio `@upt.pe` que figura como suspendida o no matriculada en el padrón universitario. | **E002-1.2** El sistema bloquea el despacho del código OTP, presenta un cuadro de diálogo con borde en color rojo de error con el mensaje literal: *"Cuenta institucional no autorizada o suspendida. Comuníquese con la Dirección de Escuela o el Comité de Tutoría de la EPIS"*. |
| **E002-1.3** El usuario pulsa el botón `"Aceptar"`. | **E002-1.4** El sistema cierra la sesión preliminar y finaliza el caso de uso sin generar registros. |

##### Flujo de excepción E003: Código de verificación OTP incorrecto
| Usuario | Sistema |
|---|---|
| **E003-1.1** El usuario introduce una secuencia de dígitos que no concuerda con el código OTP expedido. | **E003-1.2** El sistema rechaza la autenticación, incrementa el contador de fallos y despliega un mensaje de error en color rojo con el texto literal: *"Código de verificación incorrecto. Por favor, verifique el correo recibido e intente nuevamente"*. |
| **E003-1.3** El usuario limpia las casillas numéricas para reingresar el código. | **E003-1.4** El sistema permite un nuevo intento manteniendo activo el tiempo restante de expiración y el sistema retorna al paso 5 del Flujo Normal de Eventos. |

##### Flujo de excepción E004: Código de verificación OTP expirado
| Usuario | Sistema |
|---|---|
| **E004-1.1** El usuario introduce el código OTP habiendo transcurrido más de 5 minutos desde su emisión (infracción de RN-01). | **E004-1.2** El sistema invalida el código por expiración de tiempo de vida, bloquea las casillas de entrada y despliega un cuadro de diálogo en color ámbar con el mensaje literal: *"El código OTP ha expirado. Por motivos de seguridad, solicite un nuevo código de acceso"*. |
| **E004-1.3** El usuario presiona el botón `"Solicitar nuevo código"`. | **E004-1.4** El sistema redirige al formulario de reenvío y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E005: Límite de intentos fallidos alcanzado (Bloqueo preventivo)
| Usuario | Sistema |
|---|---|
| **E005-1.1** El usuario acumula tres (3) intentos consecutivos erróneos en la validación del código OTP. | **E005-1.2** El sistema bloquea temporalmente las solicitudes para dicha cuenta durante 15 minutos como medida de protección anti-fuerza bruta, destruye el código vigente, persiste una traza de seguridad en la bitácora y despliega una ventana de bloqueo en color rojo con el mensaje literal: *"Límite de intentos excedido. Su acceso ha sido bloqueado temporalmente por 15 minutos por razones de seguridad"*. |
| **E005-1.3** El usuario presiona el botón `"Salir"`. | **E005-1.4** El sistema devuelve la interfaz a la pantalla de bienvenida y finaliza el caso de uso sin generar registros. |

##### Flujo de excepción E006: Rechazo del consentimiento legal digital (Ley N° 29733)
| Usuario | Sistema |
|---|---|
| **E006-1.1** En el primer inicio de sesión, el usuario desmarca la casilla o pulsa el botón `"Rechazar Términos"`. | **E006-1.2** El sistema ejecuta el protocolo de cumplimiento estricto de RN-02: aborta la sesión temporal, no emite token JWT definitivo, registra la traza de rechazo y presenta un cuadro de advertencia en color ámbar con el mensaje literal: *"Consentimiento indispensable: La aceptación de la política de tratamiento de datos personales conforme a la Ley N° 29733 es obligatoria para acceder y operar en la red de mentorías académicas de la EPIS"*. |
| **E006-1.3** El usuario pulsa el botón `"Entendido"`. | **E006-1.4** El sistema redirige a la pantalla pública de inicio y finaliza el caso de uso sin conceder acceso ni generar sesiones persistentes. |

---

#### CUS-010 - Gestionar asignación de roles de usuario

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-010 |
| **Nombre** | Gestionar asignación de roles de usuario |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-003 (Gestión y asignación administrativa de roles de usuario); RN-03 (Jerarquía de roles y verificación de mérito académico) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Administrador Institucional (*Comité de Tutoría / Dirección EPIS*)<br>**Secundario:** Estudiante Evaluado (*Receptor de notificación de rol*) |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite al Administrador Institucional consultar el padrón de estudiantes de la EPIS-UPT, evaluar las solicitudes o expedientes de postulación a Mentor Académico, verificar el cumplimiento de los requisitos de mérito académico establecidos en la regla RN-03 (pertenencia obligatoria a los ciclos avanzados VII al X y aprobación satisfactoria de las asignaturas críticas objeto de asesoría), asignar formalmente el rol de Mentor o suspender facultades ante eventuales sanciones disciplinarias. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Panel de Administración de Usuarios y Roles, Cuadro de Diálogo de Verificación de Expediente y Notas, Modal de Promoción y Asignación de Especialidad Docente, Notificación Oficial de Cambio de Privilegios. |
| **Precondiciones** | 1. El Administrador ha iniciado sesión con perfil autenticado y privilegios directivos (`CUS-001`).<br>2. El estudiante candidato se encuentra registrado en el sistema con su rol base de Mentoreado.<br>3. Se cuenta con acceso a la información académica homologada de asignaturas aprobadas y ciclo formativo. |
| **PostCondiciones** | 1. La entidad `Usuario` actualiza su rol a `MENTOR` en la base de datos vinculando las materias en las que está autorizado a dictar.<br>2. Se actualizan las políticas de seguridad a nivel de fila (`Row Level Security`) otorgando privilegios de publicación de ofertas.<br>3. El sistema despacha una notificación oficial al correo institucional del estudiante informando su promoción y habilitación docente. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Búsqueda y selección del postulante en el padrón** | |
| **1.** El Administrador ingresa al panel de `"Gestión de Usuarios y Roles"`, escribe el código de matrícula o apellido del estudiante en el cuadro de búsqueda y presiona la tecla de consulta. | **2.** El sistema filtra el padrón institucional y despliega una tabla con los resultados, mostrando el código universitario, nombres completos, ciclo académico actual, rol vigente indicado mediante una insignia en color gris secundario (`Mentoreado`) y el botón `"Evaluar Postulación"`. (Si el Administrador requiere revocar o suspender el rol de un mentor activo, salta a A001). |
| **Fase 2: Verificación de requisitos de mérito y ciclo académico (RN-03)** | |
| **3.** El Administrador presiona el botón `"Evaluar Postulación"` en la fila del estudiante seleccionado. | **4.** El sistema despliega un cuadro de diálogo modal con el encabezado en color azul institucional, detallando el ciclo de matrícula actual del alumno y la lista de asignaturas filtro cursadas con su respectiva calificación obtenida. Verifica automáticamente que el estudiante pertenezca al ciclo VII o superior y cuente con notas aprobatorias satisfactorias. (Si el estudiante pertenece a ciclos inferiores a VII, salta a E001). (Si el estudiante no ha aprobado las asignaturas filtro seleccionadas, salta a E002). (Si el usuario ya ostenta rol de mentor activo en dichas materias, salta a E003). |
| **Fase 3: Promoción formal, persistencia y despacho de credencial** | |
| **5.** El Administrador marca las casillas de las materias formativas en las que se autoriza la mentoría, selecciona la vigencia semestral y presiona el botón `"Aprobar y Asignar Rol de Mentor"`. | **6.** El sistema persiste la actualización de roles en la base de datos, registra el identificador del administrador y la marca de tiempo de la auditoría, actualiza los permisos en el token de seguridad y despacha un correo de confirmación al buzón institucional del alumno. Despliega en pantalla un aviso en color verde de éxito con el mensaje literal: *"¡Rol de Mentor asignado exitosamente! El estudiante ha sido habilitado para publicar ofertas en las asignaturas seleccionadas"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Revocación o suspensión administrativa del rol de mentor
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Administrador selecciona a un usuario con rol activo de `Mentor` y presiona el botón `"Suspender Rol de Mentor"`. | **A001-1.2** El sistema presenta una ventana modal de advertencia en color ámbar solicitando ingresar el motivo reglamentario de la suspensión en un cuadro de texto multilínea y el botón `"Confirmar Suspensión"`. |
| **A001-1.3** El Administrador redacta la causal administrativa y presiona `"Confirmar Suspensión"`. | **A001-1.4** El sistema degrada el rol del usuario a `Mentoreado`, cancela de oficio las ofertas activas sin reservas confirmadas, despacha la notificación respectiva vía correo electrónico institucional y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Estudiante no cumple con el ciclo formativo avanzado (VII al X)
| Usuario | Sistema |
|---|---|
| **E001-1.1** El Administrador intenta promover a un alumno que se encuentra matriculado en un ciclo inferior al séptimo (I al VI ciclo). | **E001-1.2** El sistema detecta la infracción de la regla RN-03, deshabilita el botón de confirmación, marca el campo de ciclo con una etiqueta en color rojo de alerta y despliega el mensaje literal: *"Promoción no admitida: El estudiante pertenece al ciclo formativo actual y no cumple con el requisito reglamentario de ciclo avanzado (VII al X) para ejercer mentorías"*. |
| **E001-1.3** El Administrador presiona el botón `"Cerrar"`. | **E001-1.4** El sistema cierra la ventana modal y finaliza el caso de uso sin generar modificaciones de privilegios. |

##### Flujo de excepción E002: Asignatura filtro no aprobada o sin nota mínima satisfactoria
| Usuario | Sistema |
|---|---|
| **E002-1.1** El Administrador intenta habilitar al estudiante en una materia crítica que figura desaprobada o no cursada en su historial académico. | **E002-1.2** El sistema bloquea la casilla de dicha asignatura, mostrando un icono en color rojo de advertencia y el mensaje literal: *"Requisito no cumplido: El estudiante no registra la aprobación académica satisfactoria de la asignatura seleccionada en su kardex homologado"*. |
| **E002-1.3** El Administrador desmarca la materia no apta. | **E002-1.4** El sistema recalcula la viabilidad del formulario y el sistema retorna al paso 5 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Usuario ya posee rol de mentor activo en la especialidad
| Usuario | Sistema |
|---|---|
| **E003-1.1** El Administrador intenta asignar un rol idéntico al que el estudiante ya tiene asignado y vigente. | **E003-1.2** El sistema detecta la redundancia, presenta una notificación informativa en color azul institucional con el mensaje literal: *"El usuario ya cuenta con facultades vigentes de Mentor Académico en las materias seleccionadas"* y el sistema finaliza el caso de uso sin generar registros duplicados. |

---

### MOD-02: Planificación, Espacios y Agendamiento

#### CUS-006 - Publicar oferta de mentoría académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-006 |
| **Nombre** | Publicar oferta de mentoría académica |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-008 (Publicación y parametrización de ofertas de mentoría), RF-009 (Aprovisionamiento automatizado de infraestructura); RN-04 (Antelación de publicación T >= 24h, estándar 48h), RN-05 (Aforos máximos estándar: 10 presencial, 20 virtual), RN-06 (Asignación validada de recintos físicos), RN-07 (Aprovisionamiento virtual automatizado) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentor (*Estudiante acreditado de VII a X Ciclo*)<br>**Secundario:** Servicios Externos de Infraestructura (*Google Meet API / Bot Discord EPIS / Parser de Horarios*) |
| **Interacción** | Fase de Construcción / Iteración Sprint 03 - Sprint 04 |
| **Descripción** | Permite al Estudiante Mentor formular y publicar una sesión de mentoría académica en el catálogo de ofertas institucionales para una asignatura en la que cuenta con competencia aprobada, seleccionando el tema conceptual silábico, la modalidad de dictado (*Presencial* o *Virtual*), la fecha de ejecución con antelación reglamentaria superior a las 24 horas y franja horaria disponible, integrándose con el servicio de disponibilidad de recintos físicos o aprovisionando automáticamente enlaces de videoconferencia en Google Meet o canales supervisados en Discord, fijando el aforo estricto y dejando la oferta en estado `PUBLICADA` para su indexación en el recomendador inteligente. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Formulario de Publicación de Ofertas, Selector de Modalidad y Aforos, Visor de Disponibilidad de Espacios Físicos, Tarjeta de Oferta Publicada en Catálogo. |
| **Precondiciones** | 1. El usuario ha iniciado sesión institucional con rol verificado de `Mentor` (`CUS-001`, `CUS-010`).<br>2. El mentor cuenta con materias críticas acreditadas en su perfil docente.<br>3. La fecha de la sesión propuesta satisface la antelación mínima obligatoria superior a 24 horas respecto al momento de registro (`RN-04`). |
| **PostCondiciones** | 1. Se registra una nueva entidad `SesionMentoria` con estado canónico `PUBLICADA` en la base de datos.<br>2. Se reserva el recinto físico en el pabellón o se aprovisiona el enlace virtual único en Google Meet / Discord (`RN-06`, `RN-07`).<br>3. La oferta queda indexada en el motor de recomendación `EdRecSys` (`CUS-002`) y disponible para la reserva de cupos (`CUS-004`). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Delimitación curricular y temática silábica** | |
| **1.** El Mentor ingresa a su panel docente y presiona el botón `"Nueva Oferta de Mentoría"`. (Si la oferta se formula a partir de una solicitud de demanda académica existente, salta a A001). | **2.** El sistema presenta el formulario de publicación con encabezado en color azul institucional, mostrando el menú desplegable `"Asignatura Formativa"` con las materias en las que el mentor posee acreditación, un menú dinámico `"Tema Silábico"` y campos de fecha y horario. |
| **3.** El Mentor selecciona la asignatura crítica y escoge el tema conceptual silábico objeto del refuerzo académico. | **4.** El sistema carga la descripción del tema y solicita elegir la modalidad de enseñanza mediante dos casillas de opción exclusiva: `"Presencial (Aforo máx. 10)"` o `"Virtual (Aforo máx. 20)"` conforme a la política RN-05. |
| **Fase 2: Configuración de horario, aforo y aprovisionamiento logístico** | |
| **5.** El Mentor define la modalidad, ingresa la fecha programada, franja horaria de inicio y fin, y presiona el botón `"Verificar Disponibilidad y Espacio"`. | **6.** El sistema valida que la fecha seleccionada cuente con una antelación estrictamente superior a las 24 horas respecto a la hora actual (RN-04) y que el mentor no mantenga cruces en su propia agenda. (Si la antelación es menor o igual a 24 horas, salta a E001). (Si el mentor presenta cruces horarios en su agenda, salta a E002). |
| | **7.** Si la modalidad elegida es presencial, el sistema consulta el motor de recintos (`CUS-008`, RN-06) y asigna un aula o laboratorio disponible en el pabellón EPIS. Si es virtual, se conecta con la API externa de Google Meet o Discord (RN-07) y genera el enlace seguro de sesión. (Si no existen recintos físicos disponibles en el horario, salta a E003). (Si ocurre un fallo de conectividad con la API virtual, salta a E004). |
| **Fase 3: Confirmación de publicación y activación en catálogo** | |
| **8.** El Mentor revisa la tarjeta de vista previa con todos los datos consolidados y presiona el botón `"Publicar Sesión de Mentoría"`. | **9.** El sistema persiste la sesión con estado canónico `PUBLICADA`, fija el aforo reglamentario (10 para presencial, 20 para virtual), inicializa el contador de cupos reservados en cero (0), emite la señal de reindexación al motor de recomendación Top-k y despliega una alerta flotante en color verde de éxito con el mensaje literal: *"¡Oferta de mentoría publicada exitosamente! Ha quedado disponible en la cartelera institucional para la reserva de cupos"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Publicación de oferta a partir de una solicitud de demanda existente
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Mentor navega por el panel de solicitudes por demanda (`CUS-003`) y selecciona una solicitud registrada por estudiantes con alta votación. | **A001-1.2** El sistema autocompleta el formulario de publicación con la asignatura formativa y el tema silábico solicitados por los estudiantes. |
| **A001-1.3** El Mentor ajusta la fecha y el horario de dictado. | **A001-1.4** El sistema vincula la oferta a la demanda previa para notificar automáticamente a los solicitantes y el sistema retorna al paso 5 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Antelación de publicación inferior a 24 horas (Infracción de RN-04)
| Usuario | Sistema |
|---|---|
| **E001-1.1** El Mentor selecciona una fecha y hora cuya diferencia con el momento de registro es menor o igual a 24 horas. | **E001-1.2** El sistema detecta la infracción de la regla RN-04, resalta el campo de fecha con un borde en color rojo de error y presenta un cuadro de alerta con el mensaje literal: *"Antelación reglamentaria no cumplida: Toda oferta de mentoría debe publicarse con más de 24 horas de anticipación (estándar recomendado de 48 horas) para permitir la reserva y el corte de quórum"*. |
| **E001-1.3** El Mentor selecciona una nueva fecha válida en el calendario interactivo. | **E001-1.4** El sistema recalcula la diferencia horaria y el sistema retorna al paso 5 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Incompatibilidad o cruce de horario en la agenda del mentor
| Usuario | Sistema |
|---|---|
| **E002-1.1** El Mentor selecciona una franja horaria que colisiona con otra sesión de mentoría o clase previamente agendada en su calendario. | **E002-1.2** El sistema rechaza el horario propuesto, muestra un banner en color ámbar de advertencia con el mensaje literal: *"Conflicto en agenda: Ya mantienes una sesión programada o compromiso académico en la franja horaria especificada"*. |
| **E002-1.3** El Mentor modifica la franja horaria ingresada. | **E002-1.4** El sistema valida nuevamente el rango y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: No disponibilidad de recintos físicos libres (RN-06)
| Usuario | Sistema |
|---|---|
| **E003-1.1** El sistema ejecuta la comprobación de espacios físicos y constata que todas las aulas y laboratorios se encuentran ocupados por la carga lectiva regular. | **E003-1.2** El sistema informa la no disponibilidad mediante un panel en color ámbar con el mensaje literal: *"No se encontraron aulas o laboratorios físicos disponibles en el pabellón EPIS para el horario seleccionado"*, sugiriendo cambiar el horario o cambiar la modalidad a `"Virtual"`. |
| **E003-1.3** El Mentor pulsa el botón `"Cambiar a Modalidad Virtual"`. | **E003-1.4** El sistema actualiza la modalidad, ajusta el aforo máximo a 20 participantes y el sistema retorna al paso 7 del Flujo Normal de Eventos. |

##### Flujo de excepción E004: Falla en la integración con el servicio de aprovisionamiento virtual (RN-07)
| Usuario | Sistema |
|---|---|
| **E004-1.1** El servicio externo de Google Meet o Discord experimenta tiempo de espera agotado al generar el enlace de reunión. | **E004-1.2** El sistema intercepta el error, almacena la oferta en estado de borrador provisional y despliega una notificación de advertencia en color ámbar con el mensaje literal: *"Dificultad de conexión con la plataforma virtual. El enlace se generará automáticamente en segundo plano antes de la apertura de inscripciones"*. |
| **E004-1.3** El Mentor pulsa el botón `"Aceptar y Reintentar"`. | **E004-1.4** El sistema reintenta la comunicación mediante una tarea asíncrona de respaldo y el sistema retorna al paso 8 del Flujo Normal de Eventos. |

---

#### CUS-008 - Consultar disponibilidad de espacios y recursos

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-008 |
| **Nombre** | Consultar disponibilidad de espacios y recursos |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-009 (Aprovisionamiento automatizado de infraestructura), RF-010 (Procesamiento de cronogramas institucionales); RN-06 (Asignación validada de recintos físicos) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentor (*Estudiante de VII a X Ciclo*)<br>**Secundario:** Administrador / Servicio Parser de Cronogramas |
| **Interacción** | Fase de Construcción / Iteración Sprint 03 |
| **Descripción** | Permite a los mentores y coordinadores consultar en tiempo real la disponibilidad de recintos académicos (aulas teóricas y laboratorios de cómputo de la EPIS) y recursos tecnológicos institucionales cruzando la franja horaria requerida contra los cronogramas oficiales procesados por el sistema, garantizando que ninguna sesión presencial sea programada en espacios con carga lectiva regular ocupada. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Visor de Matriz de Espacios Semanales, Filtro de Búsqueda por Tipo de Recinto y Aforo, Tarjeta de Detalle del Espacio Físico con Equipamiento. |
| **Precondiciones** | 1. El usuario mentor o administrador ha iniciado sesión institucional (`CUS-001`).<br>2. Se encuentra cargada y parseada la base de datos de cronogramas y horarios lectivos oficiales del semestre académico (`RN-06`). |
| **PostCondiciones** | 1. El sistema entrega el listado verificado de recintos académicos libres con indicación de su capacidad de aforo y recursos tecnológicos.<br>2. El espacio seleccionado queda pre-reservado temporalmente si forma parte del flujo de publicación de oferta (`CUS-006`). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Configuración de criterios de consulta espacial** | |
| **1.** El Mentor accede a la opción `"Disponibilidad de Recintos"` e introduce el día calendario, la hora de inicio, la hora de fin y el tipo de espacio requerido (*Aula Teórica* o *Laboratorio Especializado*). (Si el mentor requiere consultar la disponibilidad de canales y salas virtuales supervisadas, salta a A001). | **2.** El sistema valida que el rango horario especificado sea coherente y pertenezca al horario operativo permitido de la universidad (07:00 a 22:00 horas). (Si el horario está fuera de rango operativo, salta a E001). |
| **Fase 2: Cruce analítico con cronogramas oficiales (RN-06)** | |
| **3.** El Mentor presiona el botón `"Consultar Espacios Libres"`. | **4.** El sistema consulta el repositorio de asignación de espacios, filtra las franjas horarias libres respecto a las clases lectivas regulares y verifica que los recintos no registren otras mentorías confirmadas en el mismo horario. (Si la base de cronogramas no está actualizada, salta a E002). (Si no hay ningún espacio disponible en la franja, salta a E003). |
| **Fase 3: Visualización de resultados y selección** | |
| **5.** El Mentor examina la cuadrícula de resultados, visualizando tarjetas informativas de los recintos que indican la denominación del aula o laboratorio, el pabellón físico, el aforo máximo y el equipamiento disponible (proyector multimedia, número de equipos de cómputo, pizarra acrílica). | **6.** El sistema resalta en color verde de éxito los recintos con disponibilidad garantizada y coloca una etiqueta en color gris en aquellos con uso restringido, proveyendo el botón `"Seleccionar para Oferta"` para vincular el recinto directamente al caso `CUS-006`. |

##### Flujos Alternativos

##### Flujo alternativo A001: Consulta de disponibilidad de canales virtuales supervisados
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Mentor selecciona en el filtro la categoría `"Canales Virtuales Discord / Meet"`. | **A001-1.2** El sistema consulta la API del servidor oficial de Discord de la EPIS y los límites de salas de Google Meet institucional. |
| **A001-1.3** El Mentor revisa las salas virtuales activas. | **A001-1.4** El sistema entrega la lista de canales temáticos disponibles con su límite de 20 usuarios y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Rango horario fuera de operación universitaria
| Usuario | Sistema |
|---|---|
| **E001-1.1** El usuario especifica un horario anterior a las 07:00 horas o posterior a las 22:00 horas, o con hora de fin menor a la de inicio. | **E001-1.2** El sistema bloquea la consulta, resalta el campo de tiempo con un borde en color rojo de error y muestra el mensaje literal: *"Horario inválido: Las consultas de espacios físicos deben circunscribirse a la jornada institucional de 07:00 a 22:00 horas"*. |
| **E001-1.3** El usuario ajusta los horarios de la consulta. | **E001-1.4** El sistema actualiza el cálculo y el sistema retorna al paso 2 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Cronogramas oficiales desactualizados o no disponibles
| Usuario | Sistema |
|---|---|
| **E002-1.1** El repositorio de cronogramas lectivos no ha sido procesado por el administrador para el semestre académico en curso. | **E002-1.2** El sistema despliega un panel en color ámbar de advertencia con el mensaje literal: *"Base de datos de cronogramas en mantenimiento: No es posible validar la exclusividad de aulas físicas en este momento. Por favor, programe en modalidad virtual o intente más tarde"*. |
| **E002-1.3** El usuario presiona el botón `"Entendido"`. | **E002-1.4** El sistema cierra la vista de consulta y finaliza el caso de uso sin generar reservas. |

##### Flujo de excepción E003: Ausencia total de recintos libres en la franja seleccionada
| Usuario | Sistema |
|---|---|
| **E003-1.1** Todos los recintos físicos coincidentes con los criterios de búsqueda se encuentran ocupados por la programación regular. | **E003-1.2** El sistema presenta una notificación en color ámbar con el mensaje literal: *"No existen aulas o laboratorios disponibles para el horario solicitado. Le sugerimos adelantar o retrasar su franja horaria en 60 minutos o emplear la modalidad virtual"*, presentando una lista de horarios alternativos más próximos. |
| **E003-1.3** El usuario selecciona uno de los horarios alternativos sugeridos. | **E003-1.4** El sistema actualiza los filtros y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

---

### MOD-03: Gestión Curricular y Perfiles Académicos

#### CUS-005 - Gestionar perfil formativo y disponibilidad horaria

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-005 |
| **Nombre** | Gestionar perfil formativo y disponibilidad horaria |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-004 (Configuración de perfil formativo y matriz horaria semanal); RN-03 (Jerarquía de roles y mérito académico) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentor / Mentoreado (*Usuario Institucional*)<br>**Secundario:** Ninguno |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 |
| **Descripción** | Permite a los estudiantes mentores y mentoreados configurar su perfil formativo dentro de la plataforma, seleccionando las asignaturas filtro de su competencia académica o necesidad de reforzamiento, definiendo sus canales de comunicación preferidos, y gestionando interactivamente su matriz semanal de disponibilidad horaria (de lunes a sábado, en bloques lectivos de 6 a 11 horas) para alimentar de forma directa el algoritmo de recomendación y emparejamiento adaptativo. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Vista de Perfil Académico del Usuario, Cuadrícula Interactiva Semanal de Disponibilidad Horaria (Lunes a Sábado, 07:00 a 22:00 horas), Selector de Asignaturas Filtro y Temas Silábicos. |
| **Precondiciones** | 1. El usuario ha iniciado sesión institucional con su cuenta `@upt.pe` (`CUS-001`).<br>2. El usuario cuenta con consentimiento informado digital registrado bajo Ley N° 29733 (`RN-02`). |
| **PostCondiciones** | 1. La entidad `PerfilUsuario` y la matriz de disponibilidad horaria son persistidas en la base de datos.<br>2. El motor de recomendación `EdRecSys` recalcula las coincidencias y afinidades temporales para las futuras sugerencias (`CUS-002`). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al perfil y selección de preferencias temáticas** | |
| **1.** El estudiante accede al módulo `"Mi Perfil y Horarios"` desde la barra de navegación superior. | **2.** El sistema presenta el formulario de perfil dividido en dos secciones: datos académicos y matriz horaria semanal interactiva. En la sección de datos académicos, lista las materias críticas organizadas por ciclo con casillas de selección. |
| **3.** El estudiante marca las asignaturas filtro en las que solicita apoyo (si es Mentoreado) o en las que se encuentra acreditado para brindar orientación (si es Mentor). (Si el mentor desea adjuntar enlaces externos o recursos de contacto pedagógico, salta a A001). | **4.** El sistema valida que las selecciones correspondan al ciclo y rol reglamentario del usuario. (Si un mentoreado intenta seleccionarse como mentor en cursos no aprobados, salta a E001). |
| **Fase 2: Marcado en la matriz semanal de disponibilidad horaria** | |
| **5.** El estudiante se desplaza hacia la cuadrícula interactiva de disponibilidad semanal (organizada de lunes a sábado de 07:00 a 22:00 horas en celdas de una hora) y hace clic o arrastra el cursor sobre los bloques horarios en los que dispone de tiempo libre. | **6.** El sistema conmuta el estado visual de cada celda seleccionada, cambiándola a color azul institucional para indicar disponibilidad y actualiza en tiempo real el contador resumen de `"Horas semanales disponibles"`. (Si el usuario intenta guardar con cero bloques seleccionados, salta a E002). |
| **Fase 3: Persistencia y actualización del motor algorítmico** | |
| **7.** El estudiante presiona el botón `"Guardar Preferencias y Horarios"`. | **8.** El sistema persiste de forma atómica la matriz binaria de disponibilidad y las materias seleccionadas en la base de datos, invalida la caché de coincidencias previas del usuario, y despliega una notificación flotante en color verde de éxito con el mensaje literal: *"¡Perfil y disponibilidad horaria actualizados con éxito! Tus recomendaciones se adaptarán a tus nuevos horarios"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Incorporación de enlaces y recursos de contacto pedagógico
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Mentor accede a la pestaña complementaria `"Recursos y Presentación"` e ingresa su identificador de Discord o repositorio institucional de materiales. | **A001-1.2** El sistema valida que el formato de los enlaces sea seguro y conforme a la normativa institucional. |
| **A001-1.3** El Mentor presiona `"Guardar Información de Contacto"`. | **A001-1.4** El sistema almacena los enlaces y el sistema retorna al paso 8 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Selección de asignaturas no autorizadas para mentoría
| Usuario | Sistema |
|---|---|
| **E001-1.1** Un estudiante con rol de Mentoreado intenta marcar una asignatura como oferta docente sin contar con la acreditación del Administrador. | **E001-1.2** El sistema detecta la falta de privilegios (infracción de RN-03), desmarca automáticamente la casilla y muestra un aviso en color ámbar con el mensaje literal: *"Facultad restringida: Para brindar mentoría en esta asignatura debe solicitar previamente la habilitación ante el Comité de Tutoría"*. |
| **E001-1.3** El estudiante confirma el aviso. | **E001-1.4** El sistema restablece el estado de los campos y el sistema retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Matriz semanal de disponibilidad completamente vacía
| Usuario | Sistema |
|---|---|
| **E002-1.1** El usuario desmarca todos los bloques horarios y presiona `"Guardar Preferencias y Horarios"`. | **E002-1.2** El sistema impide el guardado, bordea la cuadrícula en color rojo de advertencia y despliega el mensaje literal: *"Disponibilidad insuficiente: Debe seleccionar al menos un bloque horario de 60 minutos en la semana para permitir el emparejamiento académico"*. |
| **E002-1.3** El usuario marca al menos un bloque en la cuadrícula. | **E002-1.4** El sistema habilita el botón de guardado y el sistema retorna al paso 7 del Flujo Normal de Eventos. |

---

#### CUS-021 - Explorar catálogo curricular de asignaturas filtro

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-021 |
| **Nombre** | Explorar catálogo curricular de asignaturas filtro |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-005 (Gestión y exploración del catálogo de asignaturas y temarios silábicos); RN-04 (Dinámica de oferta y demanda) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentoreado / Mentor (*Usuario Institucional*)<br>**Secundario:** Ninguno |
| **Interacción** | Fase de Construcción / Iteración Sprint 01 - Sprint 02 |
| **Descripción** | Permite a los estudiantes navegar por el árbol curricular oficial de las asignaturas formativas y "cursos filtro" de la EPIS-UPT (Cálculo, Algoritmos y Estructura de Datos, Programación Orientada a Objetos, etc.), desglosando sus unidades de aprendizaje y temas conceptuales silábicos, visualizando las sesiones de mentoría activas ofertadas para cada tema o permitiendo derivar hacia la solicitud temática por demanda si no existen ofertas programadas. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Visor de Catálogo Curricular por Ciclos, Acordeón Desplegable de Unidades Silábicas y Temas Conceptuales, Panel de Ofertas Activas por Tema. |
| **Precondiciones** | 1. El usuario se encuentra autenticado en la plataforma (`CUS-001`).<br>2. El catálogo curricular oficial ha sido parametrizado por la Dirección EPIS (`CUS-022`). |
| **PostCondiciones** | 1. El estudiante visualiza el temario estructurado de la asignatura de su interés.<br>2. El estudiante puede redirigirse directamente a la reserva de cupos (`CUS-004`) o al registro de una solicitud por demanda (`CUS-003`). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Navegación y filtrado en el catálogo de asignaturas** | |
| **1.** El estudiante ingresa a la sección `"Catálogo de Asignaturas"` desde el menú principal. | **2.** El sistema presenta una vista en cuadrícula con tarjetas informativas de las asignaturas filtro organizadas por ciclo académico (del I al IV ciclo), acompañadas de una barra de búsqueda conceptual en la parte superior. |
| **3.** El estudiante ingresa el nombre de la asignatura o filtra por ciclo lectivo y hace clic en la tarjeta de la materia elegida. | **4.** El sistema carga el perfil de la asignatura y abre un panel lateral con el encabezado en color azul institucional, mostrando el código oficial, número de créditos, ciclo correspondiente y el listado colapsable de unidades de aprendizaje silábicas. |
| **Fase 2: Exploración granular del temario silábico** | |
| **5.** El estudiante expande una unidad de aprendizaje haciendo clic sobre su título. | **6.** El sistema despliega los temas conceptuales específicos contenidos en la unidad, indicando mediante una insignia en color verde el número de sesiones de mentoría actualmente publicadas para dicho tema, o una insignia en color gris si no existen ofertas vigentes. (Si el estudiante usa la búsqueda predictiva por texto libre, salta a A001). (Si no hay coincidencias con la búsqueda, salta a E001). |
| **Fase 3: Transición hacia reserva u oferta formativa** | |
| **7.** El estudiante presiona sobre un tema que contiene ofertas vigentes. | **8.** El sistema filtra el catálogo general y redirige al listado de sesiones de mentoría disponibles para ese tema silábico, habilitando el botón `"Reservar Cupo"` para iniciar el caso `CUS-004`. |

##### Flujos Alternativos

##### Flujo alternativo A001: Búsqueda conceptual predictiva por tema o palabra clave
| Usuario | Sistema |
|---|---|
| **A001-1.1** El estudiante escribe una palabra clave o término específico (ej. "punteros", "integrales") en el cuadro de búsqueda principal. | **A001-1.2** El sistema indexa las unidades silábicas y devuelve los temas conceptuales coincidentes junto con la asignatura a la que pertenecen. |
| **A001-1.3** El estudiante pulsa sobre el tema sugerido en la lista de autocompletado. | **A001-1.4** El sistema abre directamente el temario silábico en la unidad correspondiente y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Búsqueda sin coincidencias en el árbol curricular
| Usuario | Sistema |
|---|---|
| **E001-1.1** El estudiante ingresa un término de búsqueda que no concuerda con ninguna asignatura o tema del plan de estudios. | **E001-1.2** El sistema presenta un mensaje en color gris con el texto literal: *"No se encontraron materias ni temas silábicos que coincidan con su búsqueda. Verifique el término o explore por ciclo académico"*. |
| **E001-1.3** El estudiante pulsa el botón `"Limpiar Filtros"`. | **E001-1.4** El sistema restablece la visualización inicial de asignaturas y el sistema retorna al paso 2 del Flujo Normal de Eventos. |

---

### MOD-04: Motor de Recomendación Inteligente (*EdRecSys*)

#### CUS-002 - Explorar recomendaciones personalizadas Top-k

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-002 |
| **Nombre** | Explorar recomendaciones personalizadas Top-k |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-006 (Inferencia de recomendaciones y ranking Top-k); RN-04 (Dinámica de oferta y demanda), RN-11 (Criterios de ponderación y desempate algorítmico) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentoreado (*Estudiante de I a IV Ciclo*)<br>**Secundario:** Motor Algorítmico *EdRecSys* (*Servicio FastAPI / IA*) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 |
| **Descripción** | Permite al estudiante mentoreado recibir y explorar una selección clasificada de las mejores ofertas de mentoría académica (ranking Top-k, con k configurado entre 3 y 5) generadas por el motor inteligente de recomendación *EdRecSys*. El algoritmo vectoriza las necesidades conceptuales del mentoreado y calcula la compatibilidad temática mediante similitud coseno ponderada con la reputación histórica del mentor, la coincidencia de bloques horarios disponibles y la bonificación por materias críticas prioritarias (RN-11), permitiendo la reserva directa o el ajuste de preferencias. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Tablero de Recomendaciones Personalizadas "Para Ti", Carrusel de Tarjetas Top-k con Puntuación de Afinidad Porcentual, Filtros Rápidos de Modalidad y Horario. |
| **Precondiciones** | 1. El estudiante mentoreado ha iniciado sesión institucional (`CUS-001`).<br>2. El estudiante ha registrado sus preferencias temáticas o disponibilidad en su perfil (`CUS-005`).<br>3. Existen sesiones de mentoría en estado `PUBLICADA` registradas en el sistema (`CUS-006`). |
| **PostCondiciones** | 1. El sistema renderiza el listado Top-k con métricas visuales de compatibilidad.<br>2. Se registran trazas anónimas de telemetría de interacción (impresiones y clics CTR) para la optimización continua del recomendador. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Inferencia algorítmica y procesamiento de compatibilidad** | |
| **1.** El estudiante mentoreado accede a la página de inicio o presiona la pestaña `"Recomendados Para Ti"`. | **2.** El backend invoca al microservicio analítico *EdRecSys*, el cual recupera las sesiones publicadas y computa la matriz de afinidad aplicando la fórmula de ponderación multivariable conforme a RN-11: similitud coseno temática silábica, coincidencia de franja horaria en la matriz semanal, calificación media del mentor y ponderación por criticidad curricular. (Si no existen ofertas compatibles activas, salta a E001). (Si el servicio de recomendación experimenta desconexión temporal, salta a E002). |
| **Fase 2: Presentación del ranking Top-k de recomendaciones** | |
| **3.** El estudiante observa la pantalla principal donde se despliega un carrusel destacado con las tres a cinco (Top-k) mejores opciones de mentoría. | **4.** Cada tarjeta del ranking muestra: una insignia en color azul institucional indicando el porcentaje de compatibilidad (e.g. *"94% de afinidad formativa"*), el nombre oficial de la asignatura formativa, el tema conceptual silábico, el nombre completo y nivel de reputación del mentor (representado en estrellas en color amarillo ámbar), la modalidad de dictado, la fecha programada y el botón de acción principal `"Reservar Cupo"`. (Si el estudiante aplica filtros manuales de modalidad o turno, salta a A001). |
| **Fase 3: Selección de oferta y transición a reserva** | |
| **5.** El estudiante pulsa el botón `"Reservar Cupo"` en la tarjeta recomendada de su preferencia. | **6.** El sistema registra el evento analítico de conversión (`Click-Through Rate`) asociando el identificador anónimo de la recomendación y abre el cuadro de diálogo modal de confirmación enlazando directamente con el paso 3 del caso de uso `CUS-004`. |

##### Flujos Alternativos

##### Flujo alternativo A001: Filtrado manual del ranking por modalidad o turno preferido
| Usuario | Sistema |
|---|---|
| **A001-1.1** El estudiante pulsa sobre los botones de filtro rápido `"Solo Virtual"`, `"Solo Presencial"` o `"Horario Tarde"`. | **A001-1.2** El sistema filtra dinámicamente las recomendaciones calculadas recalculando el orden visual de las tarjetas sin recargar la página completa. |
| **A001-1.3** El estudiante examina las opciones resultantes. | **A001-1.4** El sistema presenta el nuevo subconjunto clasificado y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Inexistencia de ofertas formativas compatibles en el catálogo
| Usuario | Sistema |
|---|---|
| **E001-1.1** No existen sesiones de mentoría publicadas que coincidan temáticamente con las necesidades declaradas por el mentoreado. | **E001-1.2** El sistema detecta la ausencia de coincidencias, despliega un panel informativo en color ámbar de advertencia con el mensaje literal: *"Actualmente no hay ofertas disponibles para tus materias de interés. ¿Deseas registrar una solicitud de mentoría por demanda?"* y habilita en color azul institucional el botón `"Crear Solicitud por Demanda"`. |
| **E001-1.3** El estudiante pulsa `"Crear Solicitud por Demanda"`. | **E001-1.4** El sistema redirige al formulario del caso de uso `CUS-003` y finaliza el caso de uso sin generar registros. |

##### Flujo de excepción E002: Falla de latencia o desconexión del microservicio FastAPI
| Usuario | Sistema |
|---|---|
| **E002-1.1** El microservicio de inferencia algorítmica excede el tiempo límite de respuesta de 500 ms o no se encuentra accesible. | **E002-1.2** El sistema activa el protocolo de contingencia (*fallback* heurístico): recupera las sesiones publicadas más recientes ordenadas por fecha de inicio más próxima y despliega una notificación informativa en color gris con el mensaje literal: *"Mostrando las sesiones más próximas del catálogo mientras se optimizan tus sugerencias personalizadas"*. |
| **E002-1.3** El estudiante visualiza las ofertas heurísticas. | **E002-1.4** El sistema mantiene la capacidad de reserva operativa y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

---

#### CUS-003 - Registrar solicitud de demanda académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-003 |
| **Nombre** | Registrar solicitud de demanda académica |
| **Tipo** | Obligatorio (   ) / Opcional ( X ) |
| **Requisito ID (RF)** | RF-007 (Registro y banco de solicitudes por demanda); RN-04 (Dinámica de oferta y demanda) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentoreado (*Estudiante de I a IV Ciclo*)<br>**Secundario:** Gestor de Notificaciones a Mentores |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 |
| **Descripción** | Permite al estudiante mentoreado formular y registrar en el sistema una solicitud formal de mentoría académica cuando no encuentra ofertas publicadas en el catálogo para una asignatura crítica o tema silábico determinado, especificando el contenido conceptual que necesita reforzar, la modalidad deseada y su rango de disponibilidad horaria, permitiendo que otros estudiantes se sumen a la petición y alertando a los mentores acreditados en dicha materia para incentivar la publicación de una nueva sesión (`CUS-006`). |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Formulario de Solicitud de Mentoría por Demanda, Banco Público de Demandas Académicas Estudiantiles, Botón de Adhesión "+1 Interesado". |
| **Precondiciones** | 1. El estudiante mentoreado se encuentra autenticado con credenciales institucionales `@upt.pe` (`CUS-001`).<br>2. El estudiante ha suscrito el consentimiento digital bajo Ley N° 29733 (`RN-02`). |
| **PostCondiciones** | 1. Se registra una nueva entidad `SolicitudDemanda` en estado `ACTIVA` en la base de datos.<br>2. Se notifica de forma agregada a los mentores acreditados en la asignatura sobre la necesidad académica manifestada.<br>3. La solicitud se publica en el tablero de demandas comunitarias para permitir la adhesión de otros compañeros. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura del formulario y delimitación de necesidad** | |
| **1.** El estudiante accede a la pestaña `"Solicitudes por Demanda"` y presiona el botón `"Registrar Nueva Solicitud"`. (Si el estudiante encuentra una solicitud afín en el catálogo y opta por sumarse a ella, salta a A001). | **2.** El sistema despliega una ventana modal con el encabezado en color azul institucional, proveyendo un menú desplegable de asignaturas filtro, un selector de unidad silábica, un cuadro de texto multilínea para el detalle del requerimiento temático y casillas para la franja horaria preferida. |
| **3.** El estudiante selecciona la asignatura crítica, escoge la unidad silábica e ingresa la descripción específica del vacío conceptual o ejercicio que requiere reforzar. | **4.** El sistema evalúa que el texto ingresado posea contenido sustancial (mínimo 15 caracteres) y verifica si existe una solicitud idéntica ya formulada por el mismo alumno en la materia. (Si la descripción es insuficiente o está vacía, salta a E001). (Si el estudiante ya tiene una solicitud activa en dicho tema, salta a E002). |
| **Fase 2: Publicación en el banco de necesidades académicas** | |
| **5.** El estudiante escoge su preferencia de modalidad (*Presencial*, *Virtual* o *Indistinta*) y presiona el botón `"Publicar Solicitud"`. | **6.** El sistema persiste la solicitud en estado `ACTIVA` con un contador inicial de interesados fijado en uno (1), la hace visible en el panel público de demandas de la escuela, y despacha un correo resumen a los mentores habilitados en dicha materia. Muestra un aviso en color verde de éxito con el mensaje literal: *"¡Solicitud de demanda registrada con éxito! Los mentores acreditados han sido notificados sobre tu requerimiento"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Adhesión de otros estudiantes a una solicitud existente (+1 Interesado)
| Usuario | Sistema |
|---|---|
| **A001-1.1** Otro estudiante mentoreado examina el banco de solicitudes y encuentra una petición temática que también necesita reforzar. | **A001-1.2** El sistema presenta en la tarjeta de la demanda el botón `"+1 Me Interesa"` junto al contador actual de alumnos inscritos. |
| **A001-1.3** El estudiante presiona el botón `"+1 Me Interesa"`. | **A001-1.4** El sistema incrementa el contador de interesados, registra la adhesión del usuario para notificarle cuando un mentor abra la oferta (`CUS-006`), despliega una notificación en color verde de éxito con el mensaje: *"Te has sumado exitosamente a esta solicitud"* y el sistema finaliza el caso de uso. |

##### Flujos de Excepción

##### Flujo de excepción E001: Descripción del tema vacía o insuficiente
| Usuario | Sistema |
|---|---|
| **E001-1.1** El estudiante deja el cuadro de detalle temático en blanco o introduce menos de 15 caracteres. | **E001-1.2** El sistema resalta el cuadro de texto con un borde en color rojo de error y presenta el mensaje literal: *"Descripción muy breve: Por favor, detalla con mayor precisión el tema o conceptos específicos en los que requieres la mentoría"*. |
| **E001-1.3** El estudiante complementa la descripción requerida. | **E001-1.4** El sistema habilita el botón de publicación y el sistema retorna al paso 5 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Solicitud duplicada registrada por el mismo alumno
| Usuario | Sistema |
|---|---|
| **E002-1.1** El estudiante intenta crear una segunda solicitud activa para la misma asignatura y tema que ya había registrado previamente. | **E002-1.2** El sistema detecta la duplicidad, bloquea la acción y presenta un cuadro de alerta en color ámbar con el mensaje literal: *"Ya mantienes una solicitud activa para esta misma temática. Puedes consultar su estado en tu panel de 'Mis Solicitudes'"*. |
| **E002-1.3** El estudiante pulsa `"Ver mis solicitudes"`. | **E002-1.4** El sistema redirige a su panel individual y finaliza el caso de uso sin generar registros duplicados. |

---

### MOD-05: Reserva, Confirmación y Control de Quórum

#### CUS-004 - Reservar cupo de mentoría académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-004 |
| **Nombre** | Reservar cupo de mentoría académica |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-012 (Reserva de cupos con control de aforo y concurrencia); RN-05 (Aforos máximos estándar), RN-08 (Ventana de confirmación hasta T-24h) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentoreado (*Estudiante de I a IV Ciclo de la EPIS-UPT*)<br>**Secundario:** Gestor de Tareas Desatendidas (*Servicio Cron / Backend*) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite al estudiante mentoreado seleccionar una oferta de mentoría académica publicada en el catálogo o recomendada por el motor inteligente, verificar la disponibilidad de cupos en tiempo real mediante control transaccional estricto de concurrencia, y formalizar una reserva provisional en estado pendiente de ratificación, asegurando el cumplimiento de los límites de aforo (10 cupos para presencial, 20 para virtual) e informando la obligación de confirmar asistencia antes del corte de 24 horas previas al evento. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT, Ley N° 29733 |
| **Anexos** | Pantalla de Exploración de Mentorías y Recomendaciones Top-k, Cuadro de Diálogo Modal de Detalle y Reserva de Cupo, Indicador de Disponibilidad de Aforo en Tiempo Real, Comprobante Digital de Reserva Preliminar. |
| **Precondiciones** | 1. El estudiante mentoreado ha iniciado sesión satisfactoriamente mediante autenticación multifactor institucional con credenciales válidas del dominio `@upt.pe` (`CUS-001`).<br>2. El estudiante ha suscrito el consentimiento informado digital bajo la Ley N° 29733 (`RN-02`).<br>3. El estudiante pertenece a los ciclos formativos reglamentarios (I al IV Ciclo) y no mantiene sanciones de inhabilitación vigentes en la plataforma.<br>4. Existe al menos una sesión de mentoría en estado canónico `PUBLICADA` con una antelación superior a 24 horas respecto a su inicio lectivo (`RN-04`). |
| **PostCondiciones** | 1. Se registra una nueva entidad `Reserva` en la base de datos vinculando al mentoreado con la sesión, asignándole el estado canónico `PENDIENTE_CONFIRMACION`.<br>2. Se decrementa de forma atómica en una unidad el contador de cupos disponibles de la sesión ofertada.<br>3. Se programa en el gestor de eventos desatendidos el despacho de alertas de ratificación orientadas al corte de 24 horas previas ($T-24\text{ h}$).<br>4. Se despliega en la interfaz del usuario el comprobante de reserva provisional con fecha límite de confirmación. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Exploración y selección de la oferta formativa** | |
| **1.** El estudiante mentoreado navega por la cartelera de mentorías o el módulo de recomendaciones personalizadas y pulsa sobre la tarjeta informativa de la sesión que requiere cursar. (Si la selección se realiza desde el carrusel de recomendaciones algorítmicas, salta a A001). | **2.** Despliega un cuadro de diálogo modal en primer plano con el encabezado en color azul institucional, mostrando el código y nombre oficial de la asignatura formativa, el tema conceptual silábico a impartir, el nombre completo y ciclo del estudiante mentor, la fecha programada, franja horaria y duración en minutos, la modalidad de dictado con su respectivo aforo máximo, una barra horizontal de disponibilidad en color verde indicando los cupos disponibles respecto al total, y el botón de acción principal `"Reservar Cupo"`. |
| **Fase 2: Verificación transaccional de aforos y elegibilidad** | |
| **3.** El estudiante presiona el botón `"Reservar Cupo"` dentro del cuadro de diálogo modal. | **4.** El sistema inicia una transacción atómica con bloqueo a nivel de fila y evalúa que el número de reservas activas sea estrictamente inferior al aforo máximo configurado (10 en modalidad presencial o 20 en modalidad virtual, según RN-05). (Si el aforo se completó en ese instante por concurrencia simultánea, salta a E001). |
| | **5.** El sistema valida la elegibilidad académica del estudiante mentoreado: comprueba que pertenezca al ciclo formativo admitido, que no posea cruces de horario con otra sesión agendada en la misma franja, y que no registre una reserva previa en la misma mentoría. (Si el estudiante tiene cruce de horario, salta a E002). (Si el estudiante ya tiene una reserva en la misma sesión, salta a E003). (Si el estudiante no pertenece al ciclo admitido, salta a E004). |
| **Fase 3: Persistencia de la vacante y confirmación preliminar** | |
| | **6.** Persiste el registro de la vacante apartada asignándole el estado canónico `PENDIENTE_CONFIRMACION`, decrementa el cupo visible de la sesión, programa la alarma de seguimiento para el corte perentorio de 24 horas previas ($T-24\text{ h}$ según RN-08) y cierra el modal interactivo de selección. |
| **7.** El estudiante visualiza en pantalla la tarjeta de confirmación de reserva y revisa los datos de contacto y calendarización provisional de la sesión. | **8.** Muestra un panel informativo flotante en color verde de éxito con el mensaje literal: *"¡Cupo reservado exitosamente! Recuerda que debes ratificar tu asistencia obligatoriamente antes de las 24 horas previas al inicio de la sesión"*, incorporando una insignia en color ámbar de advertencia con el temporizador regresivo hacia la ventana de corte de ratificación y el botón `"Ir a Mis Reservas"`. |

##### Flujos Alternativos

##### Flujo alternativo A001: Reserva ejecutada desde tarjeta de recomendación Top-k
| Usuario | Sistema |
|---|---|
| **A001-1.1** El estudiante mentoreado presiona directamente el botón `"Reservar Cupo"` incrustado en una de las tarjetas del carrusel de recomendaciones personalizadas Top-k (`CUS-002`). | **A001-1.2** El sistema registra en la bitácora de telemetría analítica el identificador de la recomendación para el cálculo de la tasa de conversión (`Click-Through Rate`) del algoritmo inteligente *EdRecSys*. |
| **A001-1.3** El estudiante examina la tarjeta modal simplificada que se abre automáticamente sobre el panel de recomendaciones. | **A001-1.4** Despliega el cuadro de diálogo modal con los datos parametrizados de la oferta y el sistema retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Agotamiento de vacantes por concurrencia simultánea (Colisión de aforo)
| Usuario | Sistema |
|---|---|
| **E001-1.1** En el instante de procesar la solicitud, otro participante ocupa la última vacante libre de la sesión. | **E001-1.2** El backend detecta bajo bloqueo transaccional que los cupos disponibles son cero (0), revierte inmediatamente la transacción, actualiza la tarjeta de la sesión mostrando una etiqueta en color gris con el texto *"Sin vacantes"* e inhabilita el botón de reserva. |
| **E001-1.3** El estudiante pulsa el botón `"Aceptar"` en la ventana de notificación de cupos agotados. | **E001-1.4** Despliega una alerta modal en color ámbar con el mensaje literal: *"Lo sentimos, el aforo de esta sesión se ha completado en este instante. Por favor, selecciona otra fecha disponible o formula una solicitud de mentoría por demanda"* y el sistema finaliza el caso de uso sin generar registros. |

##### Flujo de excepción E002: Conflicto de horario con otra sesión agendada
| Usuario | Sistema |
|---|---|
| **E002-1.1** El estudiante mentoreado intenta reservar una sesión cuya franja horaria coincide o se solapa con otra sesión donde ya posee reserva confirmada o pendiente. | **E002-1.2** El sistema detecta el traslape en el cronograma del usuario, rechaza la transacción y despliega un cuadro de diálogo con borde resaltado en color rojo de error con el mensaje literal: *"Operación rechazada: Presentas un cruce de horario con otra sesión previamente agendada en tu calendario institucional"*. |
| **E002-1.3** El estudiante lee la advertencia y presiona el botón `"Entendido"`. | **E002-1.4** El sistema cierra la ventana de error, mantiene intacto el catálogo de ofertas y finaliza el caso de uso sin generar registros. |

##### Flujo de excepción E003: Intento de reserva duplicada en la misma sesión
| Usuario | Sistema |
|---|---|
| **E003-1.1** El estudiante envía una petición de reserva en una sesión de mentoría en la cual ya se encuentra registrado con estado pendiente o confirmado. | **E003-1.2** El sistema verifica la clave compuesta de usuario y sesión en el repositorio de reservas, aborta la operación y muestra un cuadro de diálogo informativo en color ámbar con el mensaje literal: *"Acceso restringido: Ya cuentas con una vacante reservada para esta sesión de mentoría"*. |
| **E003-1.3** El estudiante pulsa el botón `"Ver mi Reserva Actual"`. | **E003-1.4** El sistema redirige al panel de `"Mis Reservas"` mostrando el estado de su inscripción vigente y finaliza el caso de uso sin generar registros duplicados. |

##### Flujo de excepción E004: Inelegibilidad académica por ciclo formativo no admitido
| Usuario | Sistema |
|---|---|
| **E004-1.1** Un estudiante perteneciente a ciclos superiores o con sanción disciplinaria activa intenta formalizar una reserva en la sesión formativa. | **E004-1.2** El sistema evalúa el perfil del usuario contra los prerrequisitos de la asignatura filtro, bloquea la acción y despliega un cuadro de diálogo en color rojo de advertencia con el mensaje literal: *"Inscripción no permitida: Tu perfil académico o ciclo formativo actual no cumple con las condiciones requeridas para esta sesión"* y el sistema finaliza el caso de uso sin generar registros. |

---

#### CUS-024 - Ratificar asistencia a sesión de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-024 |
| **Nombre** | Ratificar asistencia a sesión de mentoría |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-013 (Confirmación anticipada de asistencia hasta ventana T-24h); RN-08 (Ventana de confirmación perentoria hasta T-24h) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentoreado (*Estudiante con reserva provisional previa*)<br>**Secundario:** Gestor de Tareas Desatendidas |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite al estudiante mentoreado ratificar su compromiso formal e irrevocable de asistencia a una sesión de mentoría en la que mantiene un cupo en estado `PENDIENTE_CONFIRMACION`, siempre que la operación se realice dentro de la ventana reglamentaria anterior al corte de 24 horas ($T \ge 24\text{ h}$ según RN-08), transicionando la reserva al estado definitivo `CONFIRMADA`, computando su plaza para el quórum mínimo reglamentario, liberando el acceso confidencial al recinto físico o enlace virtual y emitiendo el ticket digital con código QR para el control de ingreso. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Bandeja de "Mis Reservas Pendientes", Cuadro de Diálogo de Ratificación de Asistencia, Ticket Digital de Asistencia con Código QR Único. |
| **Precondiciones** | 1. El estudiante mantiene una reserva activa en estado canónico `PENDIENTE_CONFIRMACION` para la sesión (`CUS-004`).<br>2. El tiempo restante para el inicio de la sesión es estrictamente mayor o igual a 24 horas ($T \ge 24\text{ h}$ conforme a RN-08). |
| **PostCondiciones** | 1. La entidad `Reserva` transiciona al estado canónico `CONFIRMADA` en la base de datos.<br>2. Se desbloquean los datos confidenciales de acceso (número exacto de aula en pabellón o enlace activo a la sala virtual).<br>3. Se genera un ticket digital unívoco con código QR firmado criptográficamente y se remite al correo institucional del alumno. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de reservas pendientes y verificación de ventana (RN-08)** | |
| **1.** El estudiante mentoreado ingresa a la sección `"Mis Reservas"` desde el menú principal. (Si el estudiante accede a través del enlace de correo institucional, salta a A001). | **2.** El sistema presenta el listado de reservas del alumno. Aquellas en estado `PENDIENTE_CONFIRMACION` se resaltan con un borde en color ámbar de advertencia e incluyen una etiqueta con el tiempo regresivo exacto restante para el corte de las 24 horas previas y el botón `"Confirmar Asistencia"`. |
| **3.** El estudiante presiona el botón `"Confirmar Asistencia"` sobre la reserva correspondiente. | **4.** El sistema consulta el reloj del servidor y verifica que el tiempo restante hasta el inicio de la sesión sea mayor o igual a 24 horas ($T \ge 24\text{ h}$). (Si el tiempo restante es menor a 24 horas, la ventana está cerrada, salta a E001). (Si la sesión fue cancelada previamente por el mentor, salta a E002). |
| **Fase 2: Formalización del compromiso y persistencia de confirmación** | |
| **5.** El estudiante visualiza un cuadro de diálogo modal de confirmación con el encabezado en color azul institucional, lee el recordatorio de asistencia obligatoria y presiona el botón `"Ratificar mi Asistencia"`. | **6.** El sistema actualiza de manera transaccional el estado de la reserva a `CONFIRMADA`, suma la vacante al cómputo del quórum regulatorio de la sesión e incrementa el contador de confirmados en la ficha de la clase. |
| **Fase 3: Liberación de accesos e інstalación de credencial digital** | |
| **7.** El estudiante recibe en pantalla la confirmación y visualiza los accesos detallados a la sesión. | **8.** El sistema actualiza la tarjeta de la reserva mostrando una insignia en color verde de éxito con el texto `"Asistencia Confirmada"`, desbloquea la ubicación física exacta (aula o laboratorio) o el enlace directo de videoconferencia, y genera un ticket digital con código QR seguro, remitiendo una copia de respaldo al buzón `@upt.pe` con el mensaje literal: *"¡Asistencia ratificada con éxito! Presenta tu ticket digital con código QR al ingresar a la sesión"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Ratificación directa mediante enlace unívoco de correo institucional
| Usuario | Sistema |
|---|---|
| **A001-1.1** El estudiante hace clic en el enlace `"Ratificar Asistencia Inmediata"` incrustado en el correo electrónico recordatorio enviado por el sistema. | **A001-1.2** El sistema autentica el token de ratificación de un solo uso asociado a la reserva sin requerir navegación manual en la plataforma. |
| **A001-1.3** El estudiante visualiza directamente el modal de confirmación. | **A001-1.4** El sistema presenta los datos de la sesión y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Intento de ratificación fuera de la ventana reglamentaria (T < 24h)
| Usuario | Sistema |
|---|---|
| **E001-1.1** El estudiante pulsa `"Confirmar Asistencia"` habiendo transcurrido el corte de las 24 horas previas al evento. | **E001-1.2** El sistema detecta la expiración de la ventana (infracción de RN-08), bloquea la transacción, actualiza el estado de la reserva a `NO_CONFIRMADA` liberando la vacante y despliega un mensaje modal en color rojo de error con el texto literal: *"Ventana de ratificación cerrada: El plazo de confirmación expiró a las 24 horas previas al inicio de la sesión. Su reserva provisional ha sido dada de baja"*. |
| **E001-1.3** El estudiante presiona el botón `"Aceptar"`. | **E001-1.4** El sistema actualiza la lista de reservas y finaliza el caso de uso sin confirmar la asistencia. |

##### Flujo de excepción E002: Sesión previamente cancelada por el mentor
| Usuario | Sistema |
|---|---|
| **E002-1.1** El estudiante intenta ratificar una reserva en una sesión que fue dada de baja por el mentor por motivos de fuerza mayor. | **E002-1.2** El sistema detecta que la sesión ostenta el estado `CANCELADA`, inhabilita la confirmación y presenta un aviso en color ámbar con el mensaje literal: *"La sesión de mentoría seleccionada ha sido cancelada por el mentor responsable. Los cupos han sido liberados"*. |
| **E002-1.3** El estudiante confirma la lectura. | **E002-1.4** El sistema remueve la reserva pendiente del tablero y finaliza el caso de uso sin generar registros confirmados. |

---

#### CUS-017 - Desistir voluntariamente de reserva

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-017 |
| **Nombre** | Desistir voluntariamente de reserva |
| **Tipo** | Obligatorio (   ) / Opcional ( X ) |
| **Requisito ID (RF)** | RF-014 (Desistimiento voluntario y liberación anticipada de cupos); RN-08 (Ventana temporal previa), RN-10 (Cancelación oportuna y restitución de vacante) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentoreado (*Estudiante con reserva vigente*)<br>**Secundario:** Gestor de Tareas Desatendidas (*Restituidor de cupos*) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite al estudiante mentoreado renunciar voluntariamente a un cupo previamente reservado o confirmado en una sesión de mentoría cuando prevé que no podrá concurrir al evento, ejecutando la liberación inmediata de la vacante para que vuelva a estar disponible en el catálogo a favor de otros compañeros, evitando penalizaciones académicas por inasistencia no justificada siempre que se formule con antelación reglamentaria conforme a las reglas RN-08 y RN-10. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Bandeja de Reservas Activas del Usuario, Cuadro de Diálogo de Cancelación Voluntaria y Motivo, Notificación de Vacante Restituida. |
| **Precondiciones** | 1. El estudiante cuenta con una reserva en estado `PENDIENTE_CONFIRMACION` o `CONFIRMADA` vinculada a una sesión activa.<br>2. La sesión se encuentra en estado `PUBLICADA` o `CONFIRMADA`. |
| **PostCondiciones** | 1. La entidad `Reserva` transiciona al estado canónico `CANCELADA` en la base de datos.<br>2. Se incrementa en una unidad el contador de vacantes disponibles en la sesión de mentoría ofertada.<br>3. Se notifica a los estudiantes en lista de espera o que manifestaron interés por demanda sobre el cupo liberado. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Selección de reserva activa y solicitud de desistimiento** | |
| **1.** El estudiante mentoreado accede al módulo `"Mis Reservas"` y presiona el botón `"Cancelar Reserva"` sobre la tarjeta de la sesión a la que no podrá concurrir. | **2.** El sistema presenta una ventana modal de advertencia con el encabezado en color ámbar, desplegando los datos de la sesión, el tiempo restante para el inicio del evento y una lista desplegable con motivos de desistimiento (*Cruce con evaluación académica*, *Problema de conectividad / salud*, *Otro motivo justificado*). |
| **Fase 2: Justificación y comprobación de tiempo perentorio** | |
| **3.** El estudiante selecciona el motivo correspondiente, ingresa un comentario opcional y presiona el botón `"Confirmar Cancelación de Cupo"`. | **4.** El sistema verifica que la cancelación se efectúe antes de las dos (2) horas previas a la sesión. (Si el estudiante intenta desistir a menos de 2 horas del evento, salta a E001). (Si el desistimiento se realiza antes de T-24h, salta a A001). |
| **Fase 3: Transición de estado, restitución de aforo y notificación** | |
| **5.** El estudiante confirma la baja definitiva del cupo. | **6.** El sistema actualiza la reserva al estado `CANCELADA`, incrementa en una unidad el cupo disponible en la sesión ofertada, anula el ticket digital emitido previamente y despacha un correo de confirmación de desistimiento mostrando un panel en color verde de éxito con el mensaje literal: *"Has cancelado tu reserva satisfactoriamente. El cupo ha sido liberado para otro estudiante de la EPIS"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Desistimiento anticipado dentro de la ventana de ratificación (T >= 24h)
| Usuario | Sistema |
|---|---|
| **A001-1.1** El estudiante cancela la reserva antes de que opere el corte de 24 horas ($T \ge 24\text{ h}$). | **A001-1.2** El sistema constata que el desistimiento es altamente oportuno conforme a RN-08 y no genera registro de penalización ni advertencia en el historial del alumno. |
| **A001-1.3** El estudiante pulsa `"Aceptar"`. | **A001-1.4** El sistema restituye el aforo sin impacto en el quórum preliminar y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Desistimiento tardío a menos de 2 horas del evento
| Usuario | Sistema |
|---|---|
| **E001-1.1** El estudiante intenta cancelar su cupo cuando faltan menos de 120 minutos para el inicio de la sesión. | **E001-1.2** El sistema detecta el carácter extemporáneo del desistimiento, presenta una alerta en color rojo con el mensaje literal: *"Cancelación tardía: Al encontrarse dentro de las 2 horas previas a la sesión, la vacante no podrá ser reasignada. Se registrará una advertencia de inasistencia en su historial académico"*, solicitando ratificar con el botón `"Confirmar de todos modos"`. |
| **E001-1.3** El estudiante presiona `"Confirmar de todos modos"`. | **E001-1.4** El sistema cancela la plaza con marca de cancelación tardía y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

---

#### CUS-023 - Evaluar quórum automático a T-24h

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-023 |
| **Nombre** | Evaluar quórum automático a T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-015 (Monitoreo desatendido, alertas y quórum en T-24h); RN-08 (Cierre de ventana de confirmación), RN-09 (Corte desatendido y quórum mínimo del 50%) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Gestor de Tareas Desatendidas (*Servicio Cron / Backend*)<br>**Secundario:** Estudiante Mentor, Estudiantes Mentoreados con reserva |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Proceso desatendido y programado que se ejecuta automáticamente cuando el reloj del sistema marca con exactitud 24 horas antes del inicio de una sesión de mentoría en estado `PUBLICADA` ($T-24\text{ h}$), cerrando de forma perentoria la ventana de ratificación, cancelando por expiración las reservas provisionales no confirmadas para liberar el aforo, computando la cantidad de participantes en estado `CONFIRMADA` y evaluando si se alcanza el quórum mínimo reglamentario equivalente al 50% de la capacidad asignada (mínimo 5 confirmados en presencial o 10 en virtual según RN-09), transicionando la sesión a `CONFIRMADA` o `QUORUM_INSUFICIENTE`. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Notificación Desatendida de Quórum Suficiente, Alerta al Mentor por Quórum Insuficiente con Enlace Resolutivo (`CUS-007`), Bitácora del Servicio Cron. |
| **Precondiciones** | 1. La sesión de mentoría se encuentra en estado canónico `PUBLICADA`.<br>2. La diferencia entre la fecha y hora de inicio de la sesión y la hora del servidor es menor o igual a 24 horas ($T \le 24\text{ h}$). |
| **PostCondiciones** | 1. Las reservas que continuaban en `PENDIENTE_CONFIRMACION` caducan y transicionan a `NO_CONFIRMADA`.<br>2. Si se alcanza o supera el 50% de quórum, la sesión transiciona a `CONFIRMADA` y se despachan las instrucciones de acceso final.<br>3. Si el quórum es inferior al 50%, la sesión transiciona a `QUORUM_INSUFICIENTE` y se dispara la alerta resolutiva al mentor (`CUS-007`). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Ejecución del cronómetro y corte de ventana (RN-08)** | |
| **1.** El servicio desatendido (Cron daemon) inspecciona periódicamente la base de datos y detecta las sesiones de mentoría en estado `PUBLICADA` cuyo inicio dista 24 horas ($T \le 24\text{ h}$). | **2.** El sistema inicia una transacción atómica y cierra la ventana de ratificación para dicha sesión. Identifica todas las reservas asociadas que permanezcan en estado `PENDIENTE_CONFIRMACION`, actualiza su estado a `NO_CONFIRMADA` por expiración de plazo y notifica a los estudiantes omisos vía correo institucional. |
| **Fase 2: Conteo de confirmados y evaluación matemática de quórum (RN-09)** | |
| **3.** El sistema consulta el total de reservas en estado `CONFIRMADA` y calcula el ratio de ocupación respecto al aforo máximo establecido (10 en modalidad presencial, 20 en virtual). | **4.** El sistema evalúa si el número de confirmados es mayor o igual al umbral del 50% (al menos 5 alumnos en presencial o al menos 10 alumnos en virtual). (Si el quórum es igual o superior al 50%, salta a A001). (Si el quórum es estrictamente inferior al 50%, salta a E001). |
| **Fase 3: Registro de la transición operativa de la sesión** | |
| **5.** El sistema formaliza la nueva condición de la sesión de mentoría en la base de datos. | **6.** El sistema persiste el estado consolidado, genera las trazas en la bitácora del servidor y despacha los correos electrónicos correspondientes a todos los actores involucrados. |

##### Flujos Alternativos

##### Flujo alternativo A001: Quórum reglamentario alcanzado (Mayor o igual al 50%)
| Usuario | Sistema |
|---|---|
| **A001-1.1** El servicio calcula que la sesión cuenta con 5 o más confirmados (presencial) o 10 o más confirmados (virtual). | **A001-1.2** El sistema transiciona el estado de la sesión a `CONFIRMADA`, bloquea de forma definitiva el aula física o el canal virtual y despacha un correo de confirmación de dictado al mentor y a los participantes con el mensaje: *"¡Quórum reglamentario alcanzado! Tu sesión de mentoría está confirmada para su ejecución"*. |
| **A001-1.3** El mentor y los alumnos reciben la notificación. | **A001-1.4** El sistema consolida la agenda institucional y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Quórum insuficiente (Inferior al 50% reglamentario)
| Usuario | Sistema |
|---|---|
| **E001-1.1** El cómputo de reservas confirmadas no alcanza el umbral mínimo del 50% (menos de 5 alumnos en presencial o menos de 10 en virtual). | **E001-1.2** El sistema transiciona el estado de la sesión a `QUORUM_INSUFICIENTE`, genera una notificación de alta prioridad al Mentor con el mensaje literal: *"Atención: Tu sesión no alcanzó el quórum reglamentario del 50% al corte T-24h. Dispones de un enlace para decidir si dictas excepcionalmente o cancelas la sesión"* y detona la apertura del caso de uso resolutivo `CUS-007`. |
| **E001-1.3** El mentor hace clic en la alerta recibida. | **E001-1.4** El sistema transfiere el control al caso de uso resolutivo `CUS-007` y finaliza el caso de uso sin generar registros de confirmación. |

---

#### CUS-007 - Decisión del mentor ante quórum insuficiente

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-007 |
| **Nombre** | Decisión del mentor ante quórum insuficiente |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-016 (Gestión resolutiva ante quórum insuficiente); RN-09 (Corte desatendido y quórum mínimo), RN-10 (Cancelación oportuna y liberación inmediata de recursos) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentor (*Responsable de la sesión*)<br>**Secundario:** Estudiantes Mentoreados con reserva confirmada |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite al Estudiante Mentor adoptar una resolución oportuna frente a una sesión que al corte de 24 horas previas ($T-24\text{ h}$) ha sido catalogada con `QUORUM_INSUFICIENTE` (RN-09). Conforme a la normativa institucional, el mentor posee la atribución potestativa de: (1) continuar con el dictado en forma excepcional para beneficiar a los alumnos confirmados sin penalización alguna, o (2) proceder a la cancelación formal de la sesión, liberando de inmediato el aula física o canal virtual y notificando a los estudiantes inscritos sin descuento de horas ni demérito en su reputación docente (RN-10). |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Pantalla de Decisión de Mentor ante Quórum Bajo, Cuadro de Diálogo de Confirmación de Dictado Excepcional, Modal de Cancelación sin Penalidad. |
| **Precondiciones** | 1. La sesión de mentoría ha sido evaluada en el corte de 24 horas y ostenta el estado canónico `QUORUM_INSUFICIENTE` (`CUS-023`).<br>2. El mentor ha iniciado sesión institucional con su cuenta `@upt.pe` (`CUS-001`). |
| **PostCondiciones** | 1. Si decide dictar, la sesión transiciona al estado canónico `CONFIRMADA` con marca de ejecución excepcional.<br>2. Si decide cancelar, la sesión transiciona a `CANCELADA`, liberando de inmediato el recinto físico o canal virtual y notificando a los alumnos inscritos (`RN-10`). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso a la notificación resolutiva de la sesión** | |
| **1.** El Mentor recibe la alerta institucional en su bandeja y hace clic en el enlace `"Gestionar Sesión con Quórum Insuficiente"` o ingresa a su panel docente. | **2.** El sistema presenta una pantalla de contingencia con el encabezado en color ámbar de advertencia, informando la asignatura, el tema silábico, el aforo total, el número real de alumnos confirmados (e.g. *"3 de 10 estudiantes confirmados"*), y dos botones de acción resolutiva: `"Dictar Sesión Excepcionalmente"` y `"Cancelar Sesión sin Penalidad"`. (Si el mentor no adopta ninguna resolución antes de cumplirse las 12 horas previas a la sesión, salta a E001). |
| **Fase 2: Adopción de la resolución por el mentor (RN-09, RN-10)** | |
| **3.** El Mentor opta por brindar la orientación a los estudiantes confirmados y presiona el botón `"Dictar Sesión Excepcionalmente"`. (Si el mentor decide cancelar la sesión por no alcanzar el quórum, salta a A001). | **4.** El sistema despliega un cuadro de diálogo modal informando que la decisión no acarreará ninguna penalidad en su reputación ni afectará el cómputo de sus horas y solicita confirmar la voluntad de dictado. |
| **Fase 3: Formalización y actualización de cronogramas** | |
| **5.** El Mentor presiona el botón `"Confirmar Dictado Excepcional"`. | **6.** El sistema transiciona la sesión al estado `CONFIRMADA` con indicador de modalidad excepcional, despacha un correo de confirmación definitiva a los estudiantes con su ticket de acceso y presenta un aviso en color verde con el texto literal: *"¡Sesión confirmada! Se ha notificado a los alumnos confirmados que la sesión se llevará a cabo según lo planificado"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Decisión de cancelación formal de la sesión (RN-10)
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Mentor pulsa el botón `"Cancelar Sesión sin Penalidad"`. | **A001-1.2** El sistema despliega una ventana modal en color gris solicitando una breve fundamentación pedagógica y el botón `"Efectuar Cancelación"`. |
| **A001-1.3** El Mentor ingresa una nota explicativa y pulsa `"Efectuar Cancelación"`. | **A001-1.4** El sistema transiciona la sesión al estado `CANCELADA`, libera inmediatamente el aula en el pabellón EPIS o destruye la sala virtual temporal (RN-10), notifica a los alumnos inscritos para que seleccionen otra sesión, y el sistema finaliza el caso de uso sin aplicar penalidades. |

##### Flujos de Excepción

##### Flujo de excepción E001: Ausencia de resolución del mentor antes de las 12 horas previas a la sesión
| Usuario | Sistema |
|---|---|
| **E001-1.1** El Mentor no interactúa con la plataforma ni adopta resolución alguna hasta que el tiempo restante llega al límite de 12 horas ($T-12\text{ h}$). | **E001-1.2** El sistema desatendido ejecuta la regla de salvaguarda de agenda estudiantil: cancela de oficio la sesión, transiciona a `CANCELADA_POR_INACTIVIDAD`, libera el aula asignada y despacha un correo a los inscritos indicando la baja del evento por falta de ratificación docente. |
| **E001-1.3** El mentor accede con posterioridad a la plataforma. | **E001-1.4** El sistema muestra una alerta informativa en color rojo y el sistema finaliza el caso de uso sin posibilidad de dictado. |

---

### MOD-06: Trazabilidad, Bitácoras y Sesiones

#### CUS-012 - Registrar asistencia a sesión de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-012 |
| **Nombre** | Registrar asistencia a sesión de mentoría |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-017 (Registro de bitácora y control de asistencia efectiva); RN-12 (Cierre formal de bitácora y control obligatorio de asistencia) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentor (*Responsable de la sesión*)<br>**Secundario:** Estudiantes Asistentes |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite al Estudiante Mentor registrar de forma fehaciente la asistencia efectiva de los estudiantes que concurren a la sesión de mentoría programada, utilizando el generador dinámico de códigos QR en pantalla con tokens efímeros de refresco automático cada 60 segundos (para escaneo directo desde dispositivos móviles de los alumnos) o realizando el marcado nominal manual en el padrón digital de confirmados, siendo este control un prerrequisito obligatorio e indispensable para habilitar la encuesta post-mentoría y el cómputo de horas auditadas (RN-12). |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Pantalla de Control de Asistencia en Tiempo Real, Generador de Código QR Dinámico Efímero (Tokens 60s), Padrón Digital de Estudiantes Confirmados. |
| **Precondiciones** | 1. La sesión de mentoría se encuentra en estado `CONFIRMADA` y en su franja horaria de ejecución o hasta 60 minutos posteriores a su finalización.<br>2. El mentor ha iniciado sesión institucional (`CUS-001`). |
| **PostCondiciones** | 1. Las entidades `Asistencia` son registradas en la base de datos vinculando a cada mentoreado con el estado canónico `ASISTIO` o `FALTO`.<br>2. Los estudiantes marcados con `ASISTIO` quedan habilitados para diligenciar la encuesta de calidad post-mentoría (`RN-12`, `RN-13`). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Inicio de sesión y despliegue del generador QR** | |
| **1.** El Mentor ingresa a la sesión de mentoría activa en su panel docente y presiona el botón `"Iniciar Registro de Asistencia"`. | **2.** El sistema presenta una pantalla de control con dos opciones: un visor en primer plano con el código QR dinámico de asistencia (que se regenera automáticamente cada 60 segundos mediante tokens criptográficos efímeros) y la tabla nominal con la lista de alumnos con reserva confirmada. |
| **Fase 2: Escaneo dinámico por alumnos y marcado nominal** | |
| **3.** Los estudiantes asistentes escanean con la cámara de sus teléfonos inteligentes el código QR proyectado en pantalla. (Si un alumno tiene fallas de cámara o batería, el mentor usa marcado manual, salta a A001). | **4.** El sistema valida el token efímero del QR, verifica que el alumno posea reserva en estado `CONFIRMADA` y actualiza la fila del alumno en la pantalla del mentor en tiempo real mostrando una insignia en color verde con el texto `"Presente"`. (Si el token del QR ha expirado al momento de escanear, salta a E001). (Si el alumno no cuenta con reserva previa en la sesión, salta a E002). |
| **Fase 3: Cierre y consolidación del padrón de asistencia** | |
| **5.** El Mentor revisa la nómina consolidada, constata los ausentes y presiona el botón `"Consolidar y Guardar Asistencia"`. | **6.** El sistema persiste de forma inmutable el padrón de asistencias en la base de datos, marca a los alumnos no registrados con el estado `FALTO`, inhabilita el generador de QR y despliega una notificación en color verde de éxito con el mensaje literal: *"¡Asistencia consolidada exitosamente! Se ha registrado la presencia de los participantes"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Marcado nominal manual por el mentor ante incidencias de dispositivo
| Usuario | Sistema |
|---|---|
| **A001-1.1** Un alumno acreditado no puede escanear el QR por fallas técnicas en su dispositivo móvil. | **A001-1.2** El Mentor localiza el nombre del estudiante en la tabla nominal y pulsa sobre la casilla de verificación `"Marcar Presente Manual"`. |
| **A001-1.3** El Mentor verifica la identidad física o visual del alumno. | **A001-1.4** El sistema actualiza el estado a `"Presente (Verificación Manual)"` y el sistema retorna al paso 5 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Código QR dinámico expirado al instante del escaneo
| Usuario | Sistema |
|---|---|
| **E001-1.1** El estudiante envía la solicitud de asistencia con un token QR que superó los 60 segundos de vigencia. | **E001-1.2** El sistema rechaza la marcación y despliega en el móvil del estudiante una notificación en color rojo de advertencia con el mensaje literal: *"Código QR expirado. Por favor, escanee nuevamente el código actualizado que se muestra en la pantalla del mentor"*. |
| **E001-1.3** El estudiante reintenta el escaneo con el nuevo código QR visible. | **E001-1.4** El sistema procesa el nuevo token vigente y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Estudiante sin reserva confirmada previa en la sesión
| Usuario | Sistema |
|---|---|
| **E002-1.1** Un estudiante que no realizó reserva previa o cuya reserva caducó intenta escanear el código QR en el aula. | **E002-1.2** El sistema detecta la ausencia de reserva confirmada en la base de datos, rechaza el registro y presenta una alerta con el mensaje literal: *"Acceso denegado: No cuenta con una reserva confirmada para esta sesión de mentoría"*. |
| **E002-1.3** El estudiante pulsa `"Aceptar"`. | **E002-1.4** El sistema cancela la operación y finaliza el caso de uso sin registrar asistencia. |

---

#### CUS-013 - Registrar bitácora académica de sesión

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-013 |
| **Nombre** | Registrar bitácora académica de sesión |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-017 (Registro de bitácora y control de asistencia), RF-020 (Gestión e intercambio de recursos académicos); RN-12 (Cierre formal de bitácora dentro de las 24h) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentor (*Responsable de la sesión*)<br>**Secundario:** Administrador Institucional (*Comité de Tutoría*) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite al Estudiante Mentor registrar de manera formal y documentada la bitácora pedagógica al término de la sesión de mentoría, detallando las competencias silábicas impartidas, el resumen de las dudas y ejercicios desarrollados, las observaciones cualitativas del grupo, adjuntando evidencias fotográficas o enlaces a materiales de clase compartidos, formalizando el cierre de la sesión dentro del plazo perentorio de 24 horas para habilitar el cómputo de horas de mentoría y abrir la ventana de evaluación de encuestas de calidad (RN-12, RN-13). |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Formulario Digital de Bitácora Pedagógica, Gestor de Carga de Archivos y Evidencias de Sesión, Resumen de Cierre de Sesión de Mentoría. |
| **Precondiciones** | 1. La sesión de mentoría ha concluido su horario lectivo y se ha registrado el control de asistencia efectiva (`CUS-012`).<br>2. La sesión se encuentra dentro de la ventana de 24 horas posteriores a su culminación conforme a RN-12. |
| **PostCondiciones** | 1. La entidad `BitacoraSesion` es persistida en la base de datos vinculada a la sesión y al mentor.<br>2. La sesión de mentoría transiciona al estado canónico `FINALIZADA`.<br>3. Se habilita la encuesta de satisfacción para los alumnos asistentes por 24 horas (`RN-13`) y las horas se registran como `PROVISIONALES` para futura auditoría y certificación (`CUS-018`). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura del formulario de bitácora pedagógica** | |
| **1.** El Mentor presiona el botón `"Diligenciar Bitácora Pedagógica"` en la ficha de la sesión concluida. | **2.** El sistema presenta el formulario oficial de bitácora con el encabezado en color azul institucional, precargando la asignatura, el tema silábico y el total de asistentes validados en el caso `CUS-012`. Dispone de cuadros de texto multilínea para `"Contenidos Desarrollados"`, `"Dificultades Detectadas"` y un componente de carga de evidencias fotográficas o documentos en formato PDF. |
| **Fase 2: Registro de contenidos y carga de recursos y evidencias** | |
| **3.** El Mentor redacta el resumen de los ejercicios abordados, especifica las observaciones pedagógicas y adjunta el archivo con la evidencia de la sesión. (Si el mentor desea adjuntar enlaces a diapositivas o grabaciones, salta a A001). | **4.** El sistema valida que los campos requeridos estén completos, que el texto contenga suficiente profundidad técnica (mínimo 30 caracteres) y que los archivos adjuntos no excedan los 10 MB. (Si la bitácora se presenta fuera de las 24 horas reglamentarias, salta a E001). (Si falta registrar la asistencia de los alumnos, salta a E002). |
| **Fase 3: Cierre formal de la sesión y activación de encuestas** | |
| **5.** El Mentor revisa el resumen consolidado y presiona el botón `"Finalizar Sesión y Registrar Bitácora"`. | **6.** El sistema persiste de forma atómica la bitácora, transiciona la sesión al estado `FINALIZADA`, computa provisionalmente las horas lectivas del mentor sujetas a posterior auditoría (`RN-14`), abre la ventana de encuestas de calidad para los asistentes activos durante las siguientes 24 horas (`RN-13`) y despliega un panel en color verde de éxito con el mensaje literal: *"¡Bitácora pedagógica registrada satisfactoriamente! La sesión ha sido finalizada y las encuestas han sido habilitadas"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Incorporación de enlaces y recursos de libre descarga para los alumnos
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Mentor presiona el botón `"Añadir Recursos de Clase"` e introduce enlaces a repositorios de GitHub, diapositivas o grabaciones en Google Drive. | **A001-1.2** El sistema valida que los enlaces cuenten con protocolo HTTPS seguro. |
| **A001-1.3** El Mentor confirma la incorporación de los enlaces. | **A001-1.4** El sistema almacena los recursos enlazándolos a la bitácora para consulta de los estudiantes inscritos y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Registro de bitácora fuera del plazo de 24 horas (Infracción de RN-12)
| Usuario | Sistema |
|---|---|
| **E001-1.1** El Mentor intenta diligenciar la bitácora habiendo transcurrido más de 24 horas desde la finalización de la sesión. | **E001-1.2** El sistema detecta el vencimiento del plazo (infracción de RN-12), bloquea la edición normal y despliega un cuadro de diálogo en color ámbar de advertencia con el mensaje literal: *"Plazo vencido: El registro de la bitácora ha excedido las 24 horas reglamentarias. La solicitud será enviada al Comité de Tutoría para su visado extraordinario"*. |
| **E001-1.3** El Mentor presiona `"Enviar a Revisión Extraordinaria"`. | **E001-1.4** El sistema almacena la bitácora en estado `OBSERVADA_POR_PLAZO` y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Intento de cierre sin control de asistencia registrado
| Usuario | Sistema |
|---|---|
| **E002-1.1** El Mentor intenta guardar la bitácora sin haber consolidado previamente la lista de asistencias del caso `CUS-012`. | **E002-1.2** El sistema bloquea el botón de finalización y presenta un cuadro de alerta en color rojo con el mensaje literal: *"Control de asistencia incompleto: Debe consolidar obligatoriamente la asistencia de los estudiantes confirmados antes de proceder al cierre de la bitácora"*. |
| **E002-1.3** El Mentor presiona el botón `"Ir a Control de Asistencia"`. | **E002-1.4** El sistema redirige al caso de uso `CUS-012` para completar el registro y finaliza el caso de uso sin generar registros de bitácora. |

---

#### CUS-014 - Visualizar historial y bitácoras académicas

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-014 |
| **Nombre** | Visualizar historial y bitácoras académicas |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-019 (Consulta de historial de sesiones y asistencias); Ley N° 29733 (Aislamiento de trazas y privacidad) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Usuario Institucional (*Estudiante Mentor o Mentoreado*)<br>**Secundario:** Ninguno |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 |
| **Descripción** | Permite a cualquier usuario institucional (mentor o mentoreado) acceder a su expediente histórico completo de sesiones cursadas o dictadas en la plataforma, filtrando cronológicamente por semestre académico o por asignatura, revisando las asistencias registradas, el detalle de las bitácoras pedagógicas y las evidencias compartidas, garantizando la total privacidad y el aislamiento de los datos personales bajo las directrices de la Ley N° 29733. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT, Ley N° 29733 |
| **Anexos** | Tablero de Historial Académico de Sesiones, Filtros por Semestre y Asignatura, Visor Modal de Bitácora Pedagógica con Descarga de Recursos. |
| **Precondiciones** | 1. El usuario se encuentra debidamente autenticado en la plataforma (`CUS-001`).<br>2. Se registran sesiones históricas vinculadas a su perfil. |
| **PostCondiciones** | 1. El usuario visualiza la relación detallada de sus participaciones académicas pasadas.<br>2. El sistema permite descargar constancias preliminares o acceder a recursos compartidos. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al módulo y aplicación de criterios de filtrado** | |
| **1.** El usuario presiona la opción `"Mi Historial de Sesiones"` en el menú lateral. | **2.** El sistema presenta una tabla interactiva con todas las sesiones en las que el usuario ha participado, mostrando columnas de fecha, asignatura, tema silábico, rol desempeñado (*Mentor* o *Mentoreado*), estado de la sesión (`FINALIZADA`, `CANCELADA`) y su condición de asistencia indicada mediante una insignia en color verde (`Asistió`) o roja (`Inasistencia`). |
| **3.** El usuario selecciona un semestre lectivo específico o filtra por una asignatura en los menús de control. | **4.** El sistema actualiza de manera reactiva la tabla de resultados. (Si el usuario no registra sesiones en dicho filtro, salta a E001). |
| **Fase 2: Consulta detallada de la bitácora y recursos de sesión** | |
| **5.** El usuario hace clic sobre el botón `"Ver Bitácora"` en una de las sesiones finalizadas. (Si el usuario pulsa en `"Exportar Expediente en PDF"`, salta a A001). | **6.** El sistema despliega un cuadro de diálogo modal con el encabezado en color azul institucional, presentando el resumen temático desarrollado, el nombre del mentor, los comentarios formativos y la lista de recursos y archivos adjuntos disponibles para su descarga inmediata. |

##### Flujos Alternativos

##### Flujo alternativo A001: Exportación del expediente histórico en formato PDF institucional
| Usuario | Sistema |
|---|---|
| **A001-1.1** El usuario presiona el botón `"Exportar Historial en PDF"`. | **A001-1.2** El sistema genera dinámicamente un documento oficial en PDF con membrete institucional, consolidando la totalidad de sesiones cursadas, horas efectivas y porcentaje de asistencia. |
| **A001-1.3** El usuario descarga el archivo generado a su ordenador. | **A001-1.4** El sistema registra la descarga en la traza de auditoría y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Historial sin sesiones registradas para los filtros aplicados
| Usuario | Sistema |
|---|---|
| **E001-1.1** El usuario aplica un filtro de periodo o curso en el que no mantuvo ninguna actividad de mentoría. | **E001-1.2** El sistema presenta una vista vacía con una ilustración informativa en color gris y el mensaje literal: *"No se encontraron registros de sesiones de mentoría para los criterios de búsqueda seleccionados"*. |
| **E001-1.3** El usuario pulsa `"Restablecer Filtros"`. | **E001-1.4** El sistema limpia los filtros y el sistema retorna al paso 2 del Flujo Normal de Eventos. |

---

### MOD-07: Gamificación, Reputación y Certificación

#### CUS-018 - Emitir constancia institucional de horas de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-018 |
| **Nombre** | Emitir constancia institucional de horas de mentoría |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-022 (Parametrización de umbrales y emisión de certificados), RF-023 (Descarga y verificación institucional de certificados con hash SHA-256); RN-14 (Certificación parametrizada por horas auditadas) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Administrador Institucional (*Comité de Tutoría / Dirección EPIS*)<br>**Secundario:** Estudiante Mentor acreedor |
| **Interacción** | Fase de Construcción / Iteración Sprint 05 |
| **Descripción** | Permite al Administrador Institucional verificar el cumplimiento del umbral mínimo de horas acumuladas de mentoría académica por parte de los mentores en el periodo lectivo (según la regla RN-14), comprobar que la totalidad de sus bitácoras de sesión hayan sido auditadas y visadas favorablemente (`CUS-014`), y generar formalmente el certificado digital con folio institucional único, firma criptográfica hash SHA-256 y código QR de validación pública para su posterior convalidación de créditos extracurriculares ante la Dirección de Escuela. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Tablero de Auditoría y Certificación Semestral, Previsualizador de Certificado Digital con QR, Plantilla Institucional de Constancia en PDF. |
| **Precondiciones** | 1. El Administrador ha iniciado sesión con facultades directivas (`CUS-001`).<br>2. El estudiante mentor ha acumulado un número de horas auditadas igual o superior al umbral configurado por la escuela (`RN-14`).<br>3. Todas las bitácoras pedagógicas del periodo han sido visadas sin observaciones pendientes (`CUS-014`). |
| **PostCondiciones** | 1. Se persiste una nueva entidad `Certificado` en la base de datos con folio institucional único y hash SHA-256.<br>2. Se genera el documento digital oficial en formato PDF y se publica en el repositorio del mentor para su libre descarga (`CUS-009`).<br>3. Se habilita la URL de validación pública accesible mediante el escaneo del código QR. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del padrón de mentores y balance de horas** | |
| **1.** El Administrador ingresa al módulo `"Emisión de Certificados"` y selecciona el periodo académico a certificar. | **2.** El sistema presenta una tabla detallada de los mentores activos, indicando: código universitario, nombres completos, total de horas acumuladas, total de horas auditadas y aprobadas, promedio de satisfacción docente y una insignia de elegibilidad en color verde (`Apto para Certificación`) o en color gris (`Horas Insuficientes`). |
| **Fase 2: Verificación de horas auditadas y visado reglamentario (RN-14)** | |
| **3.** El Administrador hace clic en el botón `"Verificar Expediente"` sobre la fila de un mentor apto. | **4.** El sistema comprueba que el total de horas auditadas supere el umbral semestral y que no existan bitácoras en estado observado. (Si el mentor no alcanza el umbral mínimo de horas, salta a E001). (Si el mentor registra bitácoras pendientes de auditoría o con observaciones no subsanadas, salta a E002). (Si se desea emitir certificados en lote para todos los mentores aptos del semestre, salta a A001). |
| **Fase 3: Foliación criptográfica, generación de PDF y publicación** | |
| **5.** El Administrador revisa la vista previa del documento y presiona el botón `"Emitir y Firmar Certificado Digital"`. | **6.** El sistema genera un folio correlativo único institucional, calcula el código hash criptográfico SHA-256 de autenticidad inmutable, inserta el código QR de verificación pública en el documento PDF, persiste el registro en la base de datos y despacha una notificación de felicitación al buzón institucional del estudiante mentor con el mensaje literal: *"¡Certificado de horas de mentoría emitido satisfactoriamente! Puedes descargarlo desde tu perfil o validarlo con el código QR"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Emisión masiva en lote para todos los mentores aptos
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Administrador presiona el botón `"Emisión Masiva Semestral"`. | **A001-1.2** El sistema procesa en segundo plano el lote de todos los mentores que satisfacen estrictamente los requisitos de la regla RN-14. |
| **A001-1.3** El Administrador confirma la acción masiva en un cuadro de diálogo en color azul institucional. | **A001-1.4** El sistema genera secuencialmente los certificados con sus respectivos folios y hashes criptográficos y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Mentor no alcanza el umbral mínimo de horas auditadas (RN-14)
| Usuario | Sistema |
|---|---|
| **E001-1.1** El Administrador intenta forzar la emisión para un mentor que no reúne el umbral mínimo de horas lectivas semestrales configuradas. | **E001-1.2** El sistema bloquea el botón de emisión, resalta el contador de horas en color rojo de alerta y muestra el mensaje literal: *"Requisito no cumplido: El mentor acumula una cantidad de horas inferior al umbral mínimo reglamentario para la obtención de la constancia institucional"*. |
| **E001-1.3** El Administrador presiona `"Cerrar"`. | **E001-1.4** El sistema finaliza el caso de uso sin generar documentos. |

##### Flujo de excepción E002: Existencia de bitácoras pendientes de auditoría o con observaciones
| Usuario | Sistema |
|---|---|
| **E002-1.1** El Administrador intenta emitir la constancia pero el sistema detecta que el mentor posee sesiones finalizadas sin dictamen de auditoría en el módulo de bitácoras académicas (`CUS-014`). | **E002-1.2** El sistema presenta un aviso en color ámbar de advertencia con el mensaje literal: *"Auditoría incompleta: Existen bitácoras pedagógicas pendientes de revisión o con observaciones no resueltas. Debe visar la totalidad de sesiones antes de certificar"*. |
| **E002-1.3** El Administrador pulsa `"Ir a Historial y Bitácoras"`. | **E002-1.4** El sistema redirige al módulo de bitácoras académicas (`CUS-014`) para subsanar observaciones y finaliza el caso de uso sin generar registros de certificación. |

---

#### CUS-019 - Gestionar insignias y reputación gamificada

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-019 |
| **Nombre** | Gestionar insignias y reputación gamificada |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-021 (Cálculo dinámico de reputación y tablero de insignias); RN-13 (Cierre de encuestas post-mentoría) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Estudiante Mentor (*Beneficiario de reputación*)<br>**Secundario:** Sistema de Gamificación (*Motor de logros y badges*) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 |
| **Descripción** | Permite procesar de forma automática y transparente el nivel de reputación pública y las insignias de mérito de los mentores en función de las valoraciones capturadas en las encuestas de calidad post-mentoría (escala de 1 a 5 estrellas, RN-13), el volumen acumulado de sesiones completadas y la tasa de cumplimiento pedagógico, desbloqueando distintivos de reconocimiento lúdico (*"Mentor Oro"*, *"Especialista en Algoritmos"*, *"Compromiso Impecable"*) que se exhiben en su perfil público y ponderan favorablemente en el motor de recomendaciones Top-k (`CUS-002`, RN-11). |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Tablero de Insignias y Logros Gamificados, Medidor de Nivel de Reputación Docente, Muro de Reconocimiento y Cuadro de Honor. |
| **Precondiciones** | 1. El usuario mentor cuenta con rol activo en la plataforma (`CUS-001`, `CUS-010`).<br>2. Se han consolidado encuestas de calidad respondidas por estudiantes asistentes (`RN-13`). |
| **PostCondiciones** | 1. Se actualiza el score ponderado de reputación en la entidad `Mentor`.<br>2. Se desbloquean nuevas insignias de mérito en la entidad `InsigniaUsuario`.<br>3. El motor de recomendación actualiza el vector de reputación para los desempates algorítmicos (`RN-11`). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Procesamiento de encuestas y recálculo de puntuación** | |
| **1.** Al cerrarse la ventana de 24 horas para encuestas de una sesión finalizada (`RN-13`), el servicio de gamificación recupera las valoraciones numéricas registradas por los alumnos asistentes. | **2.** El sistema procesa la media ponderada de satisfacción descartando valores espurios y actualiza la reputación global del mentor (con escala de 1.0 a 5.0 estrellas). (Si el mentor posee menos de 3 encuestas consolidadas para el cálculo de su reputación inicial, salta a E001). |
| **Fase 2: Evaluación de reglas de logros y desbloqueo de insignias** | |
| **3.** El sistema evalúa las reglas institucionales de gamificación: número de sesiones completadas con calificación sobresaliente, cantidad de alumnos beneficiados y constancia semestral. | **4.** Si el mentor cumple con los criterios de un nuevo logro, el sistema instancia la insignia correspondiente en su perfil, asociándole una etiqueta visual en color dorado o azul institucional con el nombre del reconocimiento (e.g. *"Insignia de Excelencia Pedagógica"*). |
| **Fase 3: Visualización en el panel del mentor y cuadro de honor** | |
| **5.** El Mentor accede a su sección `"Mis Insignias y Reputación"`. (Si el mentor consulta la clasificación general, salta a A001). | **6.** El sistema presenta el panel gráfico con el indicador circular de nivel docente, la barra de progreso hacia la siguiente distinción, las insignias desbloqueadas con su fecha de concesión y las insignias pendientes de desbloqueo en color gris secundario, desplegando una notificación en color verde de éxito con el mensaje literal: *"¡Felicitaciones! Has alcanzado un nuevo nivel de reputación académica"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Consulta del salón de honor y tabla de clasificación de mentores
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Mentor pulsa en el botón `"Ver Cuadro de Honor de la EPIS"`. | **A001-1.2** El sistema despliega el ranking semestral de los mentores más destacados de la facultad con sus respectivas insignias y asignaturas de dominio. |
| **A001-1.3** El Mentor revisa su posición relativa en la comunidad. | **A001-1.4** El sistema presenta los incentivos de reconocimiento y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Encuestas insuficientes para cálculo de reputación inicial
| Usuario | Sistema |
|---|---|
| **E001-1.1** Un mentor recién incorporado cuenta con menos de tres (3) encuestas consolidadas en su haber. | **E001-1.2** El sistema asigna un estado preliminar mostrando una insignia en color gris con el texto *"Mentor Novato (En proceso de evaluación)"*, manteniendo la ponderación neutra en el recomendador Top-k hasta acumular el mínimo de muestras estadísticas. |
| **E001-1.3** El mentor revisa su estado inicial. | **E001-1.4** El sistema asigna la calificación inicial provisional y finaliza el caso de uso sin generar registros de penalización. |

---

### MOD-08: Supervisión, Analítica y Parametrización

#### CUS-009 - Notificar eventos críticos y alertas temporales

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-009 |
| **Nombre** | Notificar eventos críticos y alertas temporales |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-011 (Gestión de imprevistos y despacho de alertas), RF-015 (Monitoreo desatendido y alertas en T-24h); RN-08 (Ventana de ratificación), RN-10 (Cancelación oportuna) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Gestor de Notificaciones (*Servicio Cron / Backend*)<br>**Secundario:** Mentores y Mentoreados (*Destinatarios*) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite despachar alertas y notificaciones multicanal (correo electrónico institucional con dominio `@upt.pe` y notificaciones emergentes push en la aplicación web) ante eventos críticos temporales del sistema, tales como recordatorios de corte de ratificación a $T-24\text{ h}$ (RN-08), avisos de quórum insuficiente, confirmación definitiva de sesiones, cancelaciones por imprevistos o liberación inmediata de recursos (RN-10), asegurando la comunicación transparente e informada de la comunidad universitaria. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Centro de Notificaciones en la Barra de Navegación, Plantillas HTML de Correo Electrónico Institucional, Notificaciones Flotantes Toast. |
| **Precondiciones** | 1. Se detona un evento crítico en el ciclo de vida de una sesión de mentoría o reserva.<br>2. Los usuarios destinatarios disponen de cuentas institucionales válidas `@upt.pe`.<br>3. El servicio SMTP de la UPT se encuentra operativo. |
| **PostCondiciones** | 1. Se persiste la traza del mensaje en la tabla `Notificacion` con marca temporal y estado de entrega.<br>2. Se despacha el mensaje al buzón de correo del destinatario y se incrementa el contador de la campana de avisos en la interfaz web. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Detonación del evento y construcción del mensaje** | |
| **1.** El despachador de tareas detecta un evento crítico (e.g. corte perentorio de confirmación de asistencia, cancelación formal o aviso de quórum). | **2.** El sistema recupera la plantilla institucional correspondiente, inyecta los datos parametrizados del evento (nombre de la asignatura formativa, tema silábico, nombre del mentor, fecha, horario y enlace seguro o aula asignada) y compone el mensaje. |
| **Fase 2: Despacho asíncrono y persistencia de trazas** | |
| **3.** El sistema ejecuta el envío asíncrono hacia el servidor SMTP de la UPT y publica la notificación en la cola de mensajes en tiempo real de la plataforma web. (Si el servidor SMTP presenta congestión o demora, salta a A001). (Si el buzón institucional del destinatario no existe o genera rebote permanente, salta a E001). | **4.** El sistema persiste el registro en el centro de notificaciones del usuario con estado `"NO_LEIDO"`, asociando la URL directa de interacción correspondiente al evento. |
| **Fase 3: Recepción e interacción por el destinatario** | |
| **5.** El usuario destinatario observa la campana de notificaciones con una insignia en color rojo de alerta en la cabecera del sistema o revisa su bandeja de correo electrónico institucional. | **6.** Al hacer clic sobre la notificación, el sistema marca el mensaje como `"LEIDO"` y redirige directamente a la pantalla de resolución o detalle del evento (e.g. pantalla de ratificación `CUS-024` o decisión de mentor `CUS-007`). |

##### Flujos Alternativos

##### Flujo alternativo A001: Reintento automático por demora transitoria en el servidor SMTP
| Usuario | Sistema |
|---|---|
| **A001-1.1** El servicio de correo institucional SMTP devuelve un código de retraso temporal (4xx) o sobrecarga en la cola. | **A001-1.2** El sistema coloca el mensaje en una cola de reintentos con retraso exponencial (1 min, 5 min, 15 min). |
| **A001-1.3** El servicio SMTP recupera su operatividad normal. | **A001-1.4** El sistema despacha exitosamente el correo pendiente y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Rebote permanente de correo institucional
| Usuario | Sistema |
|---|---|
| **E001-1.1** El servidor de correo de la universidad devuelve un fallo permanente (5xx) por buzón inexistente o lleno. | **E001-1.2** El sistema registra la anomalía en la bitácora de auditoría de comunicaciones, mantiene la notificación interna en la plataforma web como canal preferente y finaliza el caso de uso sin interrumpir las operaciones transaccionales del sistema. |

---

#### CUS-011 - Generar reportes e indicadores de analítica académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-011 |
| **Nombre** | Generar reportes e indicadores de analítica académica |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-025 (Tablero analítico y métricas de rendimiento); RN-13 (Tratamiento disociado y anonimizado de evaluaciones) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Administrador Institucional (*Comité de Tutoría / Dirección EPIS*)<br>**Secundario:** Ninguno |
| **Interacción** | Fase de Construcción / Iteración Sprint 05 |
| **Descripción** | Permite a las autoridades de la facultad y al Comité de Tutoría de la EPIS consultar, procesar y consolidar tableros analíticos e informes estadísticos gerenciales sobre el desempeño integral del programa de mentorías académicas, generando métricas de demanda insatisfecha por materia crítica, ratios de asistencia y deserción, evolución semestral de horas dictadas y niveles de satisfacción docente, respetando el principio de disociación y anonimización de la Ley N° 29733, con capacidad de exportación en formatos abiertos CSV y PDF ejecutivo. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT, Ley N° 29733 |
| **Anexos** | Tablero de Inteligencia de Negocios y Métricas Institucionales, Filtro Multidimensional por Asignatura y Semestre, Exportador de Datos Agregados en CSV/PDF. |
| **Precondiciones** | 1. El usuario cuenta con sesión activa y rol verificado de `Administrador` (`CUS-001`).<br>2. Se registran transacciones de mentorías en la base de datos institucional. |
| **PostCondiciones** | 1. El sistema consolida y renderiza los indicadores agregados en pantalla.<br>2. Se genera el archivo de reporte formal en formato CSV estructurado o documento PDF de gestión para acreditación ICACIT. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Configuración de parámetros y filtros analíticos** | |
| **1.** El Administrador ingresa al módulo `"Reportes y Analítica Académica"`. | **2.** El sistema presenta el panel de supervisión con selectores de rango de fechas, filtros por asignatura formativa, ciclo lectivo y modalidad de dictado (*Presencial* o *Virtual*). |
| **3.** El Administrador delimita el semestre académico de interés y pulsa el botón `"Generar Reporte Analítico"`. | **4.** El sistema recupera los datos transaccionales, efectúa agregaciones estadísticas, anonimiza las encuestas de satisfacción conforme a la Ley N° 29733 y procesa los indicadores clave de rendimiento (KPIs). (Si el rango temporal no contiene datos registrados, salta a E001). (Si se requiere programar la entrega periódica automática a las autoridades, salta a A001). |
| **Fase 2: Despliegue de tableros gráficos e interpretación** | |
| **5.** El Administrador examina los gráficos de barras y diagramas circulares desplegados en pantalla: tasa de ocupación de cupos, asignaturas con mayor demanda insatisfecha, correlación de satisfacción docente y balance de recintos físicos utilizados. | **6.** El sistema resalta con una etiqueta en color verde las asignaturas con alto impacto y en color ámbar las materias filtro en situación de alerta por vacantes insuficientes, proveyendo los botones de exportación `"Descargar Informe Ejecutivo PDF"` y `"Exportar Datos CSV"`. |
| **Fase 3: Exportación de resultados para acreditación** | |
| **7.** El Administrador presiona el botón `"Descargar Informe Ejecutivo PDF"`. | **8.** El sistema compila el documento formal con membrete universitario, inserta los gráficos estadísticos y tablas agregadas y entrega el archivo descargable con el mensaje literal: *"¡Reporte analítico generado exitosamente! Archivo disponible para su archivo institucional y acreditación ICACIT"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Programación de despacho automático mensual a la Dirección EPIS
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Administrador pulsa la opción `"Programar Envío Periódico"`. | **A001-1.2** El sistema abre un cuadro modal para configurar la frecuencia (mensual o por cierre de unidad) y las cuentas de correo institucionales destinatarias. |
| **A001-1.3** El Administrador ingresa las direcciones `@upt.pe` de las autoridades y pulsa `"Guardar Programación"`. | **A001-1.4** El sistema registra la tarea programada y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Rango temporal sin registros transaccionales
| Usuario | Sistema |
|---|---|
| **E001-1.1** El Administrador consulta un rango de fechas en el que no hubo sesiones ni solicitudes en la plataforma. | **E001-1.2** El sistema despliega un mensaje en color gris con el texto literal: *"No se encontraron transacciones ni sesiones de mentoría en el intervalo temporal seleccionado. Ajuste las fechas de consulta"*. |
| **E001-1.3** El Administrador modifica los filtros de fecha. | **E001-1.4** El sistema actualiza la consulta y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

---

#### CUS-015 - Consultar métricas de retención y desempeño

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-015 |
| **Nombre** | Consultar métricas de retención y desempeño |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-025 (Tablero analítico y métricas de rendimiento académico) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Administrador Institucional (*Comité de Tutoría / Dirección EPIS*)<br>**Secundario:** Ninguno |
| **Interacción** | Fase de Construcción / Iteración Sprint 05 |
| **Descripción** | Permite a la Dirección de Escuela y a los docentes supervisores consultar los indicadores de impacto formativo del sistema sobre la retención estudiantil y el desempeño en las asignaturas filtro (Cálculo, Algoritmos, POO), comparando las tasas de aprobación y calificaciones promedio de los estudiantes que asistieron a mentorías frente a la cohorte general, proporcionando evidencia empírica fundamental para los informes de autoevaluación y acreditación internacional ICACIT. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Tablero de Control de Impacto y Retención Estudiantil, Gráfico Comparativo de Cohortes de Aprobación, Matriz de Desempeño por Materia Crítica. |
| **Precondiciones** | 1. El usuario cuenta con privilegios administrativos (`CUS-001`).<br>2. Se dispone de la correlación de asistencias consolidadas y las actas de notas del semestre académico. |
| **PostCondiciones** | 1. El sistema despliega el análisis comparativo de impacto en retención y rendimiento.<br>2. Se emite el reporte de evidencia empírica exigido por los criterios de calidad ICACIT. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al tablero de impacto y selección de cohortes** | |
| **1.** El Administrador ingresa al módulo `"Métricas de Retención e Impacto"`. | **2.** El sistema presenta la matriz de materias filtro con dos indicadores principales: tasa de asistencia a mentorías y tasa histórica de rezago académico. |
| **3.** El Administrador selecciona una asignatura formativa (e.g. *Algoritmos y Estructura de Datos*) y el semestre en evaluación. | **4.** El sistema cruza las asistencias registradas en el caso `CUS-012` con el registro de calificaciones finales homologadas. (Si los datos de notas finales aún no han sido cargados para el periodo, salta a E001). (Si se desea un análisis comparativo intersemestral, salta a A001). |
| **Fase 2: Interpretación de métricas de efectividad formativa** | |
| **5.** El Administrador visualiza el gráfico comparativo donde se aprecia el porcentaje de aprobación de los alumnos con asistencia regular a mentorías (resaltado con una barra en color verde) frente al grupo general de matriculados (barra en color azul institucional). | **6.** El sistema despliega una tarjeta de resumen ejecutivo con el cálculo del porcentaje de reducción de rezago y el incremento porcentual en el promedio ponderado, proveyendo el botón `"Descargar Evidencia ICACIT"`. |

##### Flujos Alternativos

##### Flujo alternativo A001: Análisis comparativo de retención intersemestral
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Administrador selecciona la opción `"Comparativa Histórica (Últimos 3 Semestres)"`. | **A001-1.2** El sistema traza las líneas de tendencia temporal mostrando la evolución progresiva de la retención estudiantil desde la implantación de las mentorías. |
| **A001-1.3** El Administrador examina la serie temporal. | **A001-1.4** El sistema consolida los gráficos y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Calificaciones del periodo aún no homologadas en el sistema
| Usuario | Sistema |
|---|---|
| **E001-1.1** El Administrador consulta un semestre en curso cuyas actas oficiales de notas aún no han sido cerradas en la facultad. | **E001-1.2** El sistema presenta una advertencia en color ámbar con el mensaje literal: *"Datos académicos en proceso: Las actas finales del semestre seleccionado no han concluido. Se presentan métricas parciales basadas en asistencia y participación"*. |
| **E001-1.3** El Administrador presiona `"Ver Datos Parciales"`. | **E001-1.4** El sistema adapta la visualización y el sistema retorna al paso 5 del Flujo Normal de Eventos. |

---

#### CUS-016 - Auditar trazas de seguridad y consentimiento Ley 29733

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-016 |
| **Nombre** | Auditar trazas de seguridad y consentimiento Ley 29733 |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-002 (Formalización de consentimiento digital), RF-026 (Auditoría administrativa de bitácoras y trazas de seguridad); RN-02 (Consentimiento informado legal), RN-14 (Auditoría previa a certificación) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Administrador Institucional (*Oficial de Cumplimiento / Comité de Tutoría*)<br>**Secundario:** Ninguno |
| **Interacción** | Fase de Construcción / Iteración Sprint 05 |
| **Descripción** | Permite al Oficial de Cumplimiento o a la Dirección de Escuela auditar de forma minuciosa e inmutable las trazas de seguridad de la plataforma, verificando la formalización del consentimiento informado digital bajo la Ley N° 29733 (con UUID, dirección IP, fecha y hora de aceptación por cada usuario), las bitácoras de autenticación con doble factor (2FA), los eventos de revocación de permisos, las modificaciones de roles de usuario y las horas lectivas declaradas por los mentores, garantizando la total rendición de cuentas e inviolabilidad de los datos académicos. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT, Ley N° 29733 |
| **Anexos** | Visor de Bitácora de Auditoría Forense y Seguridad, Registro Inmutable de Consentimientos Ley N° 29733, Exportador de Trazas de Acceso y Modificaciones. |
| **Precondiciones** | 1. El usuario ha iniciado sesión con perfil autenticado de Administrador (`CUS-001`).<br>2. Se registran eventos de auditoría persistidos en el repositorio inmutable. |
| **PostCondiciones** | 1. El sistema presenta las trazas cronológicas inalterables con marcas criptográficas.<br>2. El sistema permite exportar un acta formal de cumplimiento ante eventuales requerimientos de la Autoridad Nacional de Protección de Datos Personales. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al módulo y configuración de filtros de auditoría** | |
| **1.** El Administrador accede a la sección `"Auditoría de Seguridad y Cumplimiento Legal"`. | **2.** El sistema presenta el tablero de trazas forenses con filtros por tipo de evento (*Consentimiento Ley 29733*, *Autenticación 2FA*, *Promoción de Roles*, *Modificación de Horas*), rango de fechas y cuadro de búsqueda por identificador de usuario o dirección IP. |
| **3.** El Administrador selecciona el filtro `"Consentimiento Informado Ley 29733"` e ingresa un código de matrícula. | **4.** El sistema consulta la base de datos de trazas inmutables y devuelve la cronología del usuario con su respectiva marca de tiempo, dirección IP de origen, versión de los términos aceptados y hash de integridad del registro. (Si el usuario consultado no registra trazas, salta a E001). (Si se requiere generar un informe oficial de fiscalización, salta a A001). |
| **Fase 2: Inspección forense y validación de integridad** | |
| **5.** El Administrador pulsa en el botón `"Inspeccionar Registro"` sobre una de las filas. | **6.** El sistema abre un panel lateral con el encabezado en color azul institucional, certificando la validez del consentimiento, confirmando que la traza no ha sido alterada y desplegando el texto exacto de las cláusulas aceptadas por el estudiante. |

##### Flujos Alternativos

##### Flujo alternativo A001: Generación de informe oficial de cumplimiento para la Autoridad de Datos
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Administrador presiona el botón `"Emitir Informe de Cumplimiento Ley 29733"`. | **A001-1.2** El sistema compila un reporte consolidado con estadísticas de aceptación, revocaciones procesadas y protocolos de disociación implementados. |
| **A001-1.3** El Administrador descarga el documento foliado. | **A001-1.4** El sistema registra la descarga en la bitácora del sistema y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Usuario sin registros de auditoría en el sistema
| Usuario | Sistema |
|---|---|
| **E001-1.1** El Administrador ingresa un código o correo que no registra actividades en el periodo seleccionado. | **E001-1.2** El sistema despliega un mensaje en color gris con el texto literal: *"No se encontraron trazas de auditoría asociadas al usuario especificado"*. |
| **E001-1.3** El Administrador verifica el código ingresado. | **E001-1.4** El sistema limpia la búsqueda y el sistema retorna al paso 2 del Flujo Normal de Eventos. |

---

#### CUS-020 - Configurar parámetros institucionales y umbrales

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-020 |
| **Nombre** | Configurar parámetros institucionales y umbrales |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-022 (Parametrización de umbrales); RN-05 (Aforos máximos estándar), RN-08 (Ventana T-24h), RN-09 (Quórum mínimo 50%), RN-14 (Umbral mínimo de horas) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Administrador Institucional (*Dirección EPIS / Comité de Tutoría*)<br>**Secundario:** Ninguno |
| **Interacción** | Fase de Construcción / Iteración Sprint 05 |
| **Descripción** | Permite a la Dirección de Escuela y a los administradores del sistema parametrizar y calibrar las reglas de negocio y umbrales operativos globales del software para cada semestre académico: aforos máximos estándar para modalidad presencial y virtual (RN-05), ventana de corte para la ratificación de asistencia ($T-24\text{ h}$ según RN-08), porcentaje de quórum mínimo obligatorio (50% según RN-09), y horas acumuladas mínimas requeridas para la certificación de mentores (RN-14), asegurando la total adaptabilidad de la plataforma a las políticas de la facultad. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Panel de Configuración de Políticas y Umbrales Institucionales, Cuadro de Diálogo de Confirmación de Cambios Normativos. |
| **Precondiciones** | 1. El usuario ha iniciado sesión con credenciales válidas y rol de Administrador (`CUS-001`).<br>2. Se cuenta con el acta directiva de aprobación de directrices semestrales. |
| **PostCondiciones** | 1. Las variables globales en la entidad `ParametroInstitucional` son actualizadas en la base de datos.<br>2. Los servicios en segundo plano (tareas Cron y validadores transaccionales) adoptan de forma inmediata los nuevos umbrales. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al panel de parametrización institucional** | |
| **1.** El Administrador ingresa al módulo `"Parámetros y Políticas Institucionales"`. | **2.** El sistema presenta el formulario de configuración agrupado en cuatro paneles: (1) Aforos Estándar (presencial fijado en 10, virtual en 20), (2) Ventana de Corte de Asistencia (fijada en 24 horas), (3) Umbral de Quórum Mínimo (fijado en 50%), y (4) Horas Mínimas para Certificación de Mentores (fijado en 20 horas por semestre). |
| **Fase 2: Modificación de umbrales y validación de seguridad** | |
| **3.** El Administrador modifica el valor de alguno de los parámetros según la directriz del semestre lectivo. | **4.** El sistema valida en tiempo real que los valores introducidos se encuentren dentro de los rangos de tolerancia admisibles por la facultad (e.g. aforo presencial entre 5 y 30 alumnos, quórum entre 30% y 70%). (Si el valor ingresado excede los límites de seguridad o es negativo, salta a E001). (Si se desea restaurar los valores predeterminados institucionales, salta a A001). |
| **Fase 3: Confirmación de gobernanza y persistencia global** | |
| **5.** El Administrador presiona el botón `"Guardar Cambios de Parámetros"`. | **6.** El sistema despliega un cuadro modal de advertencia en color ámbar solicitando confirmar la alteración de las directrices globales del sistema. |
| **7.** El Administrador presiona el botón `"Confirmar y Aplicar Políticas"`. | **8.** El sistema persiste de forma atómica los nuevos parámetros, registra la traza de auditoría con la identidad del administrador responsable, actualiza la caché del servidor y despliega un mensaje en color verde de éxito con el texto literal: *"¡Parámetros institucionales actualizados con éxito! Las nuevas políticas regirán para todas las sesiones futuras"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Restablecimiento de parámetros a los valores predeterminados
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Administrador presiona el botón `"Restablecer Valores por Defecto"`. | **A001-1.2** El sistema carga los valores canónicos establecidos en las reglas institucionales RN-05, RN-08, RN-09 y RN-14. |
| **A001-1.3** El Administrador revisa los valores restaurados. | **A001-1.4** El sistema habilita el botón de guardado y el sistema retorna al paso 5 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Parámetro fuera de los rangos válidos de seguridad
| Usuario | Sistema |
|---|---|
| **E001-1.1** El Administrador introduce un valor no admisible (e.g. aforo de 0 alumnos o quórum superior al 100%). | **E001-1.2** El sistema bloquea el guardado, bordea el campo en color rojo de error y presenta el mensaje literal: *"Valor de parámetro no admisible: El valor configurado se encuentra fuera de los rangos regulatorios de la EPIS"*. |
| **E001-1.3** El Administrador rectifica el valor numérico. | **E001-1.4** El sistema valida el nuevo dato y el sistema retorna al paso 4 del Flujo Normal de Eventos. |

---

#### CUS-022 - Gestionar catálogo de temas y materias críticas

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | CUS-022 |
| **Nombre** | Gestionar catálogo de temas y materias críticas |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-005 (Gestión del catálogo de asignaturas y temarios), RF-024 (Priorización institucional de mentorías críticas); RN-11 (Criterios de ponderación algorítmica) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | **Primario:** Administrador Institucional (*Comité de Tutoría / Dirección EPIS*)<br>**Secundario:** Ninguno |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a la Dirección de Escuela y a los docentes coordinadores gestionar la estructura curricular de las materias objeto del programa de mentorías en la EPIS-UPT, registrando nuevas asignaturas filtro, incorporando y actualizando unidades de aprendizaje y temas conceptuales silábicos, y asignando el factor de criticidad o prioridad institucional ($\alpha \in [1.05, 1.50]$ según RN-11) para aquellas materias con alto índice histórico de desaprobación, asegurando que el motor de recomendación `EdRecSys` priorice su oferta a los estudiantes. |
| **Referencias** | Guía SWEBOK v3.0, Estándar ISO/IEC/IEEE 29148:2018, Criterios de Acreditación ICACIT |
| **Anexos** | Gestor de Malla Curricular y Asignaturas Filtro, Editor de Unidades Silábicas y Temas Conceptuales, Panel de Asignación de Prioridad Institucional. |
| **Precondiciones** | 1. El usuario ha iniciado sesión institucional con rol de Administrador (`CUS-001`).<br>2. Se cuenta con los sílabos oficiales aprobados por la Dirección EPIS para el semestre académico. |
| **PostCondiciones** | 1. Se persisten las actualizaciones del árbol curricular en la base de datos.<br>2. El motor de recomendación Top-k actualiza su índice temático y las bonificaciones de criticidad (`RN-11`, `CUS-002`). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Selección de materia en la estructura curricular** | |
| **1.** El Administrador ingresa al módulo `"Gestión Curricular de Materias Críticas"`. | **2.** El sistema presenta el listado de asignaturas registradas clasificadas por ciclo formativo (I al IV ciclo), mostrando el código curricular, créditos, número de temas cargados y su nivel de criticidad asignado mediante una insignia en color rojo (`Materia Prioritaria`) o en color azul institucional (`Materia Regular`). |
| **3.** El Administrador selecciona una asignatura y hace clic en `"Gestionar Temario Silábico"`. | **4.** El sistema despliega el editor jerárquico de unidades de aprendizaje y temas conceptuales. (Si se desea importar masivamente el sílabo en formato digital estructurado, salta a A001). |
| **Fase 2: Edición de unidades, temas y ponderación de prioridad (RN-11)** | |
| **5.** El Administrador agrega un nuevo tema conceptual silábico, define su título, escribe las palabras clave asociadas para la vectorización algorítmica y ajusta el factor de bonificación curricular ($\alpha = 1.25$). | **6.** El sistema comprueba que el tema no se encuentre duplicado en la misma unidad. (Si el tema ya existe en la unidad silábica, salta a E001). (Si se intenta dar de baja un tema que mantiene ofertas activas o bitácoras históricas, salta a E002). |
| **Fase 3: Persistencia y sincronización con el motor recomendador** | |
| **7.** El Administrador presiona el botón `"Guardar Actualización Curricular"`. | **8.** El sistema persiste de forma atómica los cambios en el repositorio curricular, notifica al microservicio *EdRecSys* para la reconstrucción de los vectores conceptuales y despliega un panel en color verde de éxito con el mensaje literal: *"¡Catálogo curricular y prioridades actualizados satisfactoriamente! El motor de recomendación ha sido sincronizado"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Importación masiva de temario silábico desde archivo digital
| Usuario | Sistema |
|---|---|
| **A001-1.1** El Administrador presiona el botón `"Importar Sílabo en JSON/Excel"`. | **A001-1.2** El sistema presenta una ventana de carga de archivos con validación automática de esquema de unidades y temas. |
| **A001-1.3** El Administrador selecciona el archivo estructurado del sílabo oficial. | **A001-1.4** El sistema procesa los temas, precarga las filas en el editor jerárquico y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Tema conceptual duplicado en la misma unidad
| Usuario | Sistema |
|---|---|
| **E001-1.1** El Administrador intenta agregar un tema con una denominación idéntica a otro ya registrado en la misma unidad silábica. | **E001-1.2** El sistema resalta el campo de nombre con un borde en color rojo de advertencia y presenta el mensaje literal: *"Tema duplicado: Ya existe un contenido temático registrado con el mismo nombre en esta unidad de aprendizaje"*. |
| **E001-1.3** El Administrador modifica la denominación del tema. | **E001-1.4** El sistema valida la unicidad y el sistema retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Intento de eliminación de tema con ofertas activas o histórico
| Usuario | Sistema |
|---|---|
| **E002-1.1** El Administrador intenta eliminar un tema que se encuentra vinculado a sesiones de mentoría publicadas o bitácoras del semestre. | **E002-1.2** El sistema bloquea la eliminación por integridad referencial, mostrando una alerta en color rojo con el mensaje literal: *"Operación restringida: El tema conceptual no puede ser eliminado porque registra sesiones de mentoría activas o bitácoras históricas asociadas"*, ofreciendo la alternativa de cambiar su estado a `"Inactivo"`. |
| **E002-1.3** El Administrador selecciona `"Inactivar Tema"`. | **E002-1.4** El sistema oculta el tema para nuevas ofertas manteniendo la integridad histórica y el sistema finaliza el caso de uso sin generar registros eliminados. |
