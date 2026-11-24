# Catálogo de narrativas de casos de uso

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT.

## MOD-01: Seguridad, Autenticación y Gobernanza

### CUS-001 — Iniciar sesión institucional con 2FA

#### 7.1. Ficha descriptiva

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-001** (CUS-001) |
| **Nombre** | Iniciar sesión institucional con 2FA |
| **Tipo** | Obligatorio |
| **Requisito ID (RF)** | RF-001, RF-002; RN-01, RN-02 |
| **Versión** | 2.3 (Refinamiento Visual y Funcional) |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian |
| **Actores** | Estudiante mentoreado, estudiante mentor, administrador institucional; servicio de correo institucional, servicio de Google Workspace |
| **Interacción** | Acceso web institucional mediante código temporal de un solo uso (OTP) o credencial de Google Workspace. |
| **Descripción** | Permite a los miembros de la comunidad universitaria acceder a la plataforma mediante su correo institucional (@virtual.upt.pe o @upt.pe) con validación de dos factores por código temporal o Google, verificando la aceptación del consentimiento informado bajo la Ley N° 29733 y habilitando una sesión segura de 8 horas según su rol formativo. |
| **Referencias** | SWEBOK v3.0, ISO/IEC/IEEE 29148:2018, Ley N° 29733 |
| **Precondiciones** | Cuenta institucional activa (@virtual.upt.pe o @upt.pe), sin suspensión administrativa ni inhabilitación académica. |
| **Postcondiciones** | Identidad verificada, consentimiento registrado, sesión iniciada por 8 horas y acceso al panel institucional del rol asignado. |

#### 7.2. Flujo normal de eventos

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **Fase 1: Acceso a la plataforma y solicitud de código de verificación** | |
| **1.** El usuario accede a la dirección web del Sistema Web P2P desde su navegador web. | |
| | **2.** El sistema muestra la pantalla de inicio de sesión sobre un fondo gris claro. En la parte superior presenta un encabezado azul marino con el emblema dorado de la UPT, el título del sistema, el indicador «🔒 Sin sesión institucional activa» y el botón dorado «Iniciar sesión». Debajo, la barra de navegación expone las opciones autorizadas para visitantes: la pestaña activa «🔐 Iniciar sesión» (resaltada en azul marino con texto blanco) y la pestaña inactiva «📚 Cursos» (en gris claro con texto gris azulado para consultar el catálogo público sin autenticación).<br><br>En el centro se presenta una tarjeta blanca con bordes redondeados y el título «Iniciar Sesión Institucional» en azul marino, acompañada de las siguientes opciones y elementos de interacción:<br>• **Continuar con Google Workspace UPT:** Botón institucional con el logotipo oficial para autenticación federada directa (continúa en A001).<br>• **Línea divisoria:** Separa el acceso federado del formulario mediante el texto «O CON CÓDIGO OTP POR CORREO».<br>• **Correo Electrónico Institucional UPT:** Campo de texto con la sugerencia «ej: ra2022073504@virtual.upt.pe» y texto de ayuda explicativo: «Alumnos: @virtual.upt.pe (iniciales + código). Docentes y directivos: @upt.pe.».<br>• **Continuar con Código OTP →:** Botón azul marino institucional, inicialmente deshabilitado en color gris con opacidad reducida hasta que se introduce texto en el campo. |
| **3.** El usuario ingresa su dirección de correo institucional y presiona «Continuar con Código OTP →». | |
| | **4.** El sistema comprueba el formato del correo y el estado de la cuenta institucional. Si el dominio es externo a la universidad, pasa a E001; si la cuenta registra suspensión, pasa a E002. Si la cuenta es válida, genera un código numérico temporal de seis dígitos con vigencia de cinco minutos, lo despacha al buzón institucional y actualiza la tarjeta central a la pantalla de verificación, presentando:<br>• **Notificación informativa superior:** Cuadro azul pastel que indica «ℹ️ Código de verificación enviado. Revisa tu buzón institucional (@virtual.upt.pe).».<br>• **Resumen de destino:** Contenedor gris tenue que muestra «Destino de verificación: [correo ingresado]» junto al enlace interactivo dorado «Cambiar correo» (A004), el cual permite anular el proceso y rectificar la dirección.<br>• **Campo numérico interactivo:** Etiqueta «Código de 6 dígitos» con campo centrado en tipografía monoespaciada y texto de ayuda «Ingresa los 6 dígitos numéricos recibidos (se conservan ceros a la izquierda)».<br>• **Contador regresivo de vigencia:** Ubicado a la derecha de la etiqueta, muestra «⏳ Expira en: 05:00» en azul marino y desciende segundo a segundo (pasa a E004 si llega a 00:00).<br>• **Verificar y Acceder:** Botón azul marino principal, inicialmente inhabilitado en gris hasta que se completan los seis dígitos numéricos.<br>• **Sección de reenvío:** En la parte inferior, delimitada por una línea divisoria, muestra el texto «Reenviar código en 60s» en gris, el cual se convertirá en el enlace interactivo «Reenviar código OTP» (A002) al concluir el tiempo de espera. |
| **Fase 2: Verificación del código temporal de dos factores** | |
| **5.** El usuario introduce el código de seis dígitos recibido en su buzón institucional y presiona «Verificar y Acceder». | |
| | **6.** El sistema comprueba el código ingresado. Si no coincide con el enviado, pasa a E003; si transcurrieron los cinco minutos, pasa a E004; si se supera el límite de intentos permitidos, pasa a E005. Si la comprobación es exitosa y el usuario ya formalizó previamente el consentimiento de privacidad en un acceso anterior, pasa a A003. |
| **Fase 3: Formalización del consentimiento informado de privacidad** | |
| | **7.** Al identificar que el usuario ingresa a la plataforma por primera vez, el sistema despliega la ventana modal «Consentimiento Informado de Privacidad (Ley N° 29733)» sobre un fondo atenuado, conteniendo:<br>• **Cabecera institucional:** Título del módulo acompañado del icono de balanza («⚖️») y el fundamento normativo de protección de datos personales.<br>• **Panel de lectura normativo:** Recuadro con barra de desplazamiento vertical que detalla las cláusulas de tratamiento de datos personales para fines pedagógicos y el ejercicio de derechos ARCO.<br>• **Casilla de verificación obligatoria:** Casilla interactiva con el texto «He leído y acepto los términos de consentimiento informado bajo la Ley N° 29733 y autorizo el tratamiento de mis datos académicos.».<br>• **🚫 Rechazar y Salir:** Botón secundario en fondo blanco con borde y texto rojo, siempre activo y accesible (continúa en E006).<br>• **✓ Aceptar y Continuar:** Botón principal en azul marino, inicialmente deshabilitado en color gris, que se habilita al marcar la casilla de verificación. |
| **8.** El usuario marca la casilla de verificación obligatoria y presiona el botón «✓ Aceptar y Continuar». Si decide rechazar las cláusulas de privacidad, presiona «🚫 Rechazar y Salir» (E006). | |
| | **9.** El sistema registra la formalización del consentimiento informado con constancia inalterable de fecha y hora. Si ocurre una interrupción de conectividad, pasa a E007. |
| **Fase 4: Inicio de sesión y redirección según el rol formativo** | |
| | **10.** El sistema inicia una sesión institucional con vigencia de ocho horas y despliega el panel principal adaptado al perfil formativo del usuario. El encabezado se actualiza mostrando el identificador «Usuario Institucional: Sesión: [correo]», el distintivo dorado con el rol asignado («MENTOREADO», «MENTOR» o «ADMINISTRADOR»), el indicador «⚖️ Consentimiento OK» en color verde y la opción para cerrar sesión. La barra de navegación habilita las pestañas correspondientes al perfil:<br>• **Perfil Estudiante Mentoreado:** Muestra la barra de flujo guiado formativo y las pestañas «🎯 Recomendaciones» (activa por defecto con la cartelera de ofertas afines del motor EdRecSys), «🔍 Explorar Mentorías», «📅 Mis Reservas», «⭐ Mis Evaluaciones» y «📜 Constancias».<br>• **Perfil Estudiante Mentor:** Muestra la barra de flujo docente y las pestañas «📋 Mis Sesiones» (activa por defecto con el registro de clases programadas, inscritos y estado de quórum a T-24h), «➕ Publicar Oferta», «📝 Registro de Asistencia» y «📊 Mi Desempeño».<br>• **Perfil Administrador Institucional:** Muestra las pestañas directivas «👥 Gestión de Roles» (activa por defecto con la administración de usuarios y postulaciones a mentor), «📈 Analítica Institucional», «⚙️ Configuración del Sistema» y «🛡️ Auditoría». |

#### 7.3. Flujos alternativos

##### A001: Inicio de sesión mediante Google Workspace institucional
* **Paso origen:** Paso 2 del Flujo Normal.
* **Condición de activación:** El usuario presiona el botón «Continuar con Google Workspace UPT».

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **A001-1.** El usuario presiona el botón «Continuar con Google Workspace UPT». | |
| | **A001-2.** El sistema presenta la ventana emergente de autenticación federada de Google [Pendiente de validación manual]. Una vez autenticado, comprueba que la cuenta pertenezca al dominio institucional (@virtual.upt.pe o @upt.pe). Si el dominio no corresponde a la universidad, deriva a E001. Si es válido y requiere consentimiento, avanza al Paso 7; si ya cuenta con registro previo de consentimiento, avanza directamente al Paso 10. |

##### A002: Reenvío del código de verificación
* **Paso origen:** Paso 4 del Flujo Normal.
* **Condición de activación:** El usuario no recibe el código en su buzón y concluye el periodo de espera obligatorio de 60 segundos.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **A002-1.** Concluidos los 60 segundos reglamentarios de espera, el texto gris inferior conmuta al enlace interactivo azul marino «Reenviar código OTP». |
| **A002-2.** El usuario presiona el enlace «Reenviar código OTP». | |
| | **A002-3.** El sistema invalida el código temporal anterior, genera y envía un nuevo código de seis dígitos al buzón institucional, reinicia el temporizador de expiración a cinco minutos («⏳ Expira en: 05:00»), restablece el contador de espera a 60 segundos y retorna al Paso 4 del Flujo Normal. |

##### A003: Acceso con consentimiento previamente aceptado
* **Paso origen:** Paso 6 del Flujo Normal.
* **Condición de activación:** El usuario validó su identidad mediante el código temporal o Google, y cuenta con un registro previo de consentimiento informado vigente.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **A003-1.** El sistema comprueba que el usuario ya aceptó formalmente las cláusulas de privacidad de la Ley N° 29733 en un acceso anterior. Omite la presentación de la ventana modal y avanza de forma inmediata al Paso 10 del Flujo Normal para iniciar la sesión de ocho horas según su rol. |

##### A004: Cambio de correo institucional
* **Paso origen:** Paso 4 del Flujo Normal.
* **Condición de activación:** El usuario detecta una equivocación en la dirección escrita o decide acceder con otra cuenta institucional.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **A004-1.** El usuario presiona el enlace dorado «Cambiar correo». | |
| | **A004-2.** El sistema anula el desafío de verificación temporal activo, despeja el formulario y retorna al Paso 2 del Flujo Normal para permitir el ingreso de una nueva dirección de correo. |

#### 7.4. Flujos de excepción

##### E001: Correo no institucional
* **Paso origen:** Paso 4 del Flujo Normal o A001.
* **Condición de activación:** Se introduce una dirección perteneciente a un dominio externo o comercial no autorizado.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E001-1.** El sistema interrumpe la solicitud, no emite código temporal y despliega sobre el formulario una caja de alerta en tono rojo pastel con borde y texto rojo: «⚠️ Acceso restringido: Solo se permiten correos institucionales con dominio @virtual.upt.pe o @upt.pe.». Preserva el texto escrito en el campo para facilitar su corrección inmediata. |
| **E001-2.** El usuario rectifica su dirección con una cuenta institucional válida y presiona «Continuar con Código OTP →». | |
| | **E001-3.** El sistema retira la alerta de error y retorna al Paso 4 del Flujo Normal. |

##### E002: Cuenta suspendida o inhabilitada
* **Paso origen:** Paso 4 del Flujo Normal.
* **Condición de activación:** La cuenta institucional del usuario registra suspensión administrativa o inhabilitación académica vigente.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E002-1.** El sistema comprueba el estado inactivo de la cuenta, bloquea el envío del código de verificación y presenta una alerta roja sobre el formulario: «⚠️ ACCOUNT_SUSPENDED: Su cuenta institucional registra suspensión administrativa. Por favor, comuníquese con la Dirección de Escuela EPIS-UPT.». El caso de uso finaliza sin conceder acceso a la plataforma. |

##### E003: Código de verificación incorrecto
* **Paso origen:** Paso 6 del Flujo Normal.
* **Condición de activación:** Los dígitos introducidos no concuerdan con el código de seis dígitos emitido por el sistema.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E003-1.** El sistema detecta la discordancia y muestra una alerta en color rojo sobre el formulario: «⚠️ Código de verificación no válido o expirado.». Mantiene los dígitos introducidos en el campo para permitir su rectificación puntual. |
| **E003-2.** El usuario revisa su buzón, escribe los dígitos correctos en el campo y presiona «Verificar y Acceder». | |
| | **E003-3.** El sistema retira la alerta de error y retorna al Paso 6 del Flujo Normal. |

##### E004: Código de verificación vencido
* **Paso origen:** Paso 6 del Flujo Normal.
* **Condición de activación:** El usuario ingresa el código tras haber transcurrido más de cinco minutos (300 segundos) desde su generación.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E004-1.** El sistema comprueba que el plazo de vigencia expiró. El contador superior cambia a color rojo mostrando «⏳ Expira en: 00:00», se inhabilita el botón «Verificar y Acceder» y se despliega una alerta roja: «⚠️ El código OTP ha expirado (5 minutos). Por favor solicita un nuevo código.». En la parte inferior, el enlace «Reenviar código OTP» se muestra activo en color azul marino. |
| **E004-2.** El usuario presiona el enlace interactivo «Reenviar código OTP». | |
| | **E004-3.** El sistema emite un nuevo código al buzón institucional, reinicia el contador de expiración a 05:00, rehabilita los controles del formulario y retorna al Paso 4 del Flujo Normal. |

##### E005: Límite de intentos o solicitudes alcanzado
* **Paso origen:** Paso 4 o Paso 6 del Flujo Normal.
* **Condición de activación:** Se registran más de cinco intentos fallidos consecutivos o más de cinco peticiones de código en un minuto.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E005-1.** El sistema activa el bloqueo de seguridad temporal por 60 segundos y presenta un panel rojo: «⚠️ RATE_LIMIT_EXCEEDED: Demasiadas solicitudes de código de acceso. Ha superado el límite de intentos permitidos. Por favor, espere 60 segundos antes de reintentar.». Inhabilita los controles de envío durante dicho intervalo para proteger la plataforma. |
| **E005-2.** El usuario espera a que concluya el periodo de resguardo temporal de 60 segundos. | |
| | **E005-3.** Finalizado el tiempo de espera, el sistema restablece automáticamente los controles interactivos y retorna al Paso 2 del Flujo Normal. |

##### E006: Rechazo del consentimiento informado
* **Paso origen:** Paso 8 del Flujo Normal.
* **Condición de activación:** El usuario decide no aceptar las cláusulas de privacidad o presiona el botón «🚫 Rechazar y Salir».

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **E006-1.** El usuario presiona el botón secundario «🚫 Rechazar y Salir». | |
| | **E006-2.** El sistema detiene el proceso, no registra la aceptación y revoca la sesión provisional. Retorna a la pantalla inicial de inicio de sesión informando que la aceptación del consentimiento bajo la Ley N° 29733 es un requisito legal indispensable para el uso de la plataforma. El caso de uso finaliza sin conceder acceso. |

##### E007: Fallo de comunicación o indisponibilidad del servicio
* **Paso origen:** En cualquier interacción de comunicación durante el flujo.
* **Condición de activación:** Ocurre una interrupción en la conectividad del usuario o una falta de respuesta temporal del servicio.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E007-1.** El sistema detecta la falta de respuesta y presenta una alerta roja solicitando reintentar la operación, preservando los datos completados en el formulario. |
| **E007-2.** El usuario comprueba su conectividad a Internet y presiona nuevamente el botón de acción correspondiente («Continuar con Código OTP →» o «Verificar y Acceder»). | |
| | **E007-3.** El sistema reintenta la comunicación y, una vez restablecido el enlace, retoma el flujo en el paso correspondiente. |

#### 7.5. Diagrama de flujo de actividades

**Figura 1. Diagrama de actividades — CUS-001: Iniciar sesión institucional con 2FA.**

![Figura 1. Diagrama de actividades — CUS-001: Iniciar sesión institucional con 2FA.](docs/narrativas/diagramas/img/CUS-001_actividades.png)

Fuente: Elaboración propia.

#### 7.6. Diagrama de caso de uso

**Figura 2. Diagrama de caso de uso — CUS-001: Iniciar sesión institucional con 2FA.**

![Figura 2. Diagrama de caso de uso — CUS-001: Iniciar sesión institucional con 2FA.](docs/narrativas/diagramas/img/CUS-001_caso_de_uso.png)

Fuente: Elaboración propia.
