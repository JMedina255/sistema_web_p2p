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
| **Versión** | 2.2 (DOC-SRS-02) |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian |
| **Actores** | Estudiante mentoreado, estudiante mentor, administrador institucional; servicio de correo institucional, servicio de Google Workspace |
| **Interacción** | Acceso web institucional mediante código temporal de un solo uso (OTP) o credencial de Google Workspace. |
| **Descripción** | Permite a los miembros de la comunidad universitaria acceder a la plataforma mediante su correo institucional (@virtual.upt.pe o @upt.pe) con validación de dos factores por código temporal o Google, verificando la aceptación del consentimiento informado bajo la Ley N° 29733 y habilitando una sesión segura de 8 horas según su rol formativo. |
| **Referencias** | SWEBOK v3.0, ISO/IEC/IEEE 29148:2018, Ley N° 29733 |
| **Precondiciones** | Cuenta institucional activa (@virtual.upt.pe o @upt.pe), sin suspensión administrativa ni inhabilitación. |
| **Postcondiciones** | Identidad verificada, consentimiento registrado, sesión iniciada por 8 horas y acceso al panel del rol asignado. |

#### 7.2. Flujo normal de eventos

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **Fase 1: Acceso a la plataforma y solicitud de código de verificación** | |
| **1.** El usuario accede a la dirección web del Sistema Web P2P desde su navegador web. | |
| | **2.** El sistema muestra un encabezado azul marino con el emblema institucional de la UPT y el botón dorado «Iniciar sesión». En el centro presenta una tarjeta blanca con bordes redondeados y el título «Iniciar Sesión Institucional» en azul marino. La tarjeta contiene el botón «Continuar con Google Workspace UPT», una línea divisoria, una etiqueta que solicita el «Correo Electrónico Institucional UPT», un campo de texto con la sugerencia «ej: ra2022073504@virtual.upt.pe» y el botón azul marino «Continuar con Código OTP →», inicialmente deshabilitado. Si el usuario opta por ingresar mediante su cuenta de Google, continúa en A001. |
| **3.** El usuario ingresa su dirección de correo institucional y presiona «Continuar con Código OTP →». | |
| | **4.** El sistema comprueba el formato del correo y el estado de la cuenta institucional. Si el dominio es ajeno a la universidad, pasa a E001; si la cuenta está suspendida, pasa a E002. Si es válida, genera un código numérico temporal de seis dígitos con vigencia de cinco minutos, lo envía al buzón institucional y presenta la pantalla de verificación. Muestra un aviso azul de confirmación con el correo registrado, el enlace dorado «Cambiar correo» (A004), el campo «Código de 6 dígitos» con el contador regresivo «⏳ Expira en: 05:00», el botón azul marino «Verificar y Acceder» y en la parte inferior el texto de espera de 60 segundos para solicitar un nuevo código (A002). |
| **Fase 2: Verificación del código temporal de dos factores** | |
| **5.** El usuario introduce el código de seis dígitos recibido en su buzón de correo institucional y presiona «Verificar y Acceder». | |
| | **6.** El sistema comprueba el código ingresado. Si no coincide con el enviado, pasa a E003; si los cinco minutos transcurrieron, pasa a E004; si se supera el límite de intentos permitidos, pasa a E005. Si el código es correcto y el usuario ya aceptó previamente el consentimiento de privacidad en un acceso anterior, pasa a A003. |
| **Fase 3: Formalización del consentimiento informado de privacidad** | |
| | **7.** Al identificar que el usuario ingresa por primera vez, el sistema muestra la ventana modal «Consentimiento Informado de Privacidad (Ley N° 29733)». La ventana describe el propósito institucional de la plataforma, el tratamiento de los datos académicos y las directivas de seguridad. Incluye una casilla de verificación obligatoria para manifestar la aceptación expresa, acompañada del botón rojo «🚫 Rechazar y Salir» y el botón azul «✓ Aceptar y Continuar», inicialmente inactivo. |
| **8.** El usuario marca la casilla de verificación y presiona el botón «✓ Aceptar y Continuar». Si decide rechazar las cláusulas de privacidad, continúa en E006. | |
| | **9.** El sistema registra la formalización del consentimiento informado con constancia inalterable de fecha y hora. Si ocurre una interrupción de red, pasa a E007. |
| **Fase 4: Inicio de sesión y redirección según el rol formativo** | |
| | **10.** El sistema inicia una sesión institucional con vigencia de ocho horas y despliega el panel principal correspondiente al rol del usuario (mentoreado, mentor o administrador). En la barra superior muestra el correo activo, el distintivo institucional del rol asignado y el indicador «⚖️ Consentimiento OK», habilitando la navegación autorizada para el perfil formativo. |

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
| | **A002-1.** Concluido el tiempo de espera de 60 segundos, el sistema habilita el enlace azul marino «Reenviar código OTP». |
| **A002-2.** El usuario presiona el enlace «Reenviar código OTP». | |
| | **A002-3.** El sistema invalida el código temporal anterior, genera y envía un nuevo código de seis dígitos al buzón institucional, reinicia el contador de expiración a cinco minutos («⏳ Expira en: 05:00»), restablece el tiempo de espera de 60 segundos y retorna al Paso 4 del Flujo Normal. |

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
| | **E001-1.** El sistema rechaza la solicitud, no emite código temporal y muestra una alerta roja sobre el formulario: «⚠️ Acceso restringido: Solo se permiten correos institucionales con dominio @virtual.upt.pe o @upt.pe.». Preserva el texto escrito en el campo para facilitar su corrección. |
| **E001-2.** El usuario rectifica su dirección con una cuenta institucional válida y presiona «Continuar con Código OTP →». | |
| | **E001-3.** El sistema retira la alerta de error y retorna al Paso 4 del Flujo Normal. |

##### E002: Cuenta suspendida o inhabilitada
* **Paso origen:** Paso 4 del Flujo Normal.
* **Condición de activación:** La cuenta institucional del usuario registra suspensión administrativa o inhabilitación académica vigente.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E002-1.** El sistema comprueba el estado inactivo de la cuenta, bloquea el envío del código de verificación y presenta una alerta roja informando que la cuenta se encuentra suspendida administrativamente. El caso de uso finaliza sin conceder acceso a la plataforma. |

##### E003: Código de verificación incorrecto
* **Paso origen:** Paso 6 del Flujo Normal.
* **Condición de activación:** Los dígitos introducidos no concuerdan con el código de seis dígitos emitido por el sistema.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E003-1.** El sistema detecta la discordancia y muestra una alerta roja: «⚠️ Código de verificación no válido o expirado.». Mantiene el campo habilitado para permitir un nuevo intento. |
| **E003-2.** El usuario revisa su buzón, escribe los dígitos correctos en el campo y presiona «Verificar y Acceder». | |
| | **E003-3.** El sistema retira la alerta de error y retorna al Paso 6 del Flujo Normal. |

##### E004: Código de verificación vencido
* **Paso origen:** Paso 6 del Flujo Normal.
* **Condición de activación:** El usuario ingresa el código tras haber transcurrido más de cinco minutos (300 segundos) desde su generación.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E004-1.** El sistema comprueba que el plazo de vigencia expiró. El contador muestra «⏳ Expira en: 00:00» en color rojo, se inhabilita el botón «Verificar y Acceder» y se despliega una alerta roja: «⚠️ El código OTP ha expirado (5 minutos). Por favor solicita un nuevo código.». Habilita el enlace azul marino «Reenviar código OTP». |
| **E004-2.** El usuario presiona el enlace interactivo «Reenviar código OTP». | |
| | **E004-3.** El sistema emite un nuevo código al buzón institucional, reinicia el contador de expiración a 05:00, rehabilita los controles del formulario y retorna al Paso 4 del Flujo Normal. |

##### E005: Límite de intentos o solicitudes alcanzado
* **Paso origen:** Paso 4 o Paso 6 del Flujo Normal.
* **Condición de activación:** Se registran más de cinco intentos fallidos consecutivos o más de cinco peticiones de código en un minuto.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E005-1.** El sistema activa el bloqueo de seguridad temporal por 60 segundos y presenta un panel rojo: «⚠️ RATE_LIMIT_EXCEEDED: Demasiadas solicitudes de código de acceso. Ha superado el límite de intentos permitidos. Por favor, espere 60 segundos antes de reintentar.». Inhabilita los controles de envío durante dicho intervalo. |
| **E005-2.** El usuario espera a que concluya el periodo de resguardo temporal de 60 segundos. | |
| | **E005-3.** Finalizado el tiempo de espera, el sistema restablece los controles interactivos y retorna al Paso 2 del Flujo Normal. |

##### E006: Rechazo del consentimiento informado
* **Paso origen:** Paso 8 del Flujo Normal.
* **Condición de activación:** El usuario decide no aceptar las cláusulas de privacidad o presiona el botón «🚫 Rechazar y Salir».

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **E006-1.** El usuario presiona el botón secundario «🚫 Rechazar y Salir». | |
| | **E006-2.** El sistema detiene el proceso, no registra la aceptación y revoca la sesión provisional. Retorna a la pantalla inicial informando que la aceptación del consentimiento bajo la Ley N° 29733 es un requisito indispensable para el uso de la plataforma. El caso de uso finaliza sin conceder acceso. |

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
