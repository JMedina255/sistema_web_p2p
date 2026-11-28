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
| **Versión** | 2.3 (H01-CUS001) |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian |
| **Actores** | Estudiante mentoreado, estudiante mentor, administrador institucional; servicio de correo institucional y, cuando está disponible, servicio de identidad de Google |
| **Interacción** | Acceso web mediante un código temporal enviado al correo institucional o mediante el botón oficial de Google habilitado por la configuración del entorno. |
| **Descripción** | Permite verificar una cuenta `@virtual.upt.pe` o `@upt.pe`, consultar el consentimiento informado bajo la Ley N.° 29733 y abrir el panel inicial correspondiente al rol. El acceso por correo utiliza un código de seis dígitos con vigencia de cinco minutos; la credencial de sesión emitida tiene una vigencia máxima de ocho horas. |
| **Referencias** | SWEBOK v3.0, ISO/IEC/IEEE 29148:2018, Ley N.° 29733 |
| **Precondiciones** | El usuario dispone de una cuenta institucional y acceso al buzón correspondiente. Para usar Google, el entorno debe tener habilitado el servicio de identidad y una cuenta institucional válida. |
| **Postcondiciones** | La identidad queda verificada y, si existe consentimiento vigente, el sistema abre el panel del rol asignado. Si el consentimiento se rechaza o el usuario cierra la sesión, el sistema retorna al acceso sin mantener una sesión activa. |

#### 7.2. Flujo normal de eventos

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **Fase 1: Solicitud del código de verificación** | |
| **1.** El usuario accede al Sistema Web P2P y selecciona «Iniciar sesión». | |
| | **2.** El sistema muestra la tarjeta «Iniciar Sesión Institucional». Cuando el acceso con Google está configurado y disponible, presenta primero el botón oficial de Google y el separador «O con código OTP por correo». También muestra la etiqueta «Correo Electrónico Institucional UPT», el campo con la sugerencia «ej: ra2022073504@virtual.upt.pe», la indicación de los dominios admitidos y el botón «Continuar con Código OTP →», inicialmente inactivo mientras el campo está vacío. Si el usuario elige Google, continúa en A001. |
| **3.** El usuario ingresa una dirección institucional y presiona «Continuar con Código OTP →». | |
| | **4.** El sistema valida el formato y el dominio. Si la dirección no es institucional, continúa en E001. Si no puede emitir o enviar el código, continúa en E002; si aplica una restricción temporal de solicitudes, continúa en E006. Cuando la solicitud es aceptada, envía un código numérico de seis dígitos con vigencia de cinco minutos y muestra la pantalla de verificación. Esta pantalla identifica el «Destino de verificación», ofrece «Cambiar correo», presenta el campo «Código de 6 dígitos», el contador «⏳ Expira en: 05:00», el botón «Verificar y Acceder», el contador «Reenviar código en 60s» y la opción «Cancelar». |
| **Fase 2: Verificación del código temporal** | |
| **5.** El usuario escribe los seis dígitos recibidos y presiona «Verificar y Acceder». | |
| | **6.** El sistema comprueba el código y su vigencia. Si no coincide, continúa en E003; si expiró, continúa en E004; si el desafío alcanzó cinco intentos fallidos, continúa en E005. Si el código es correcto, verifica si existe un consentimiento informado vigente. Cuando ya existe, continúa en A003. |
| **Fase 3: Consentimiento informado** | |
| | **7.** Si no existe consentimiento vigente, el sistema muestra la ventana «Consentimiento Informado Digital», la referencia «Protección de Datos Personales · Ley N° 29733», el estado «⚠️ PENDIENTE DE FIRMA», la política de tratamiento de datos, una casilla de aceptación expresa y los botones «🚫 Rechazar y Salir» y «✓ Aceptar y Continuar». El botón de aceptación permanece inactivo hasta marcar la casilla. |
| **8.** El usuario marca la casilla y presiona «✓ Aceptar y Continuar». Si decide no aceptar, continúa en E007. | |
| | **9.** El sistema registra la aceptación con su versión y fecha. Si no puede completar la operación, continúa en E008. |
| **Fase 4: Acceso al panel del rol** | |
| | **10.** El sistema abre el panel inicial del rol: «Explorar mentorías» para mentoreado, «Mis sesiones» para mentor o «Administración» para administrador. En el encabezado muestra «Sesión: [correo]», el rol activo, «⚖️ Consentimiento OK» y «Cerrar Sesión». La credencial emitida tiene una vigencia máxima de ocho horas. |

#### 7.3. Flujos alternativos

##### A001: Acceso mediante Google institucional
* **Paso origen:** Paso 2 del Flujo Normal.
* **Condición de activación:** El botón oficial de Google está disponible y el usuario lo selecciona.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **A001-1.** El usuario selecciona el botón oficial de Google y elige una cuenta. | |
| | **A001-2.** Google solicita o confirma la identidad. El Sistema Web P2P acepta únicamente cuentas verificadas de los dominios institucionales y, si la validación concluye correctamente, continúa en el Paso 7 o en A003 según el estado del consentimiento. Si la cuenta no es institucional, continúa en E001. **La operación completa con una cuenta real institucional permanece pendiente de validación manual en el entorno autorizado.** |

##### A002: Reenvío del código de verificación
* **Paso origen:** Paso 4 del Flujo Normal.
* **Condición de activación:** El usuario no recibió el código y terminó el periodo de espera, o el código ya expiró.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **A002-1.** El sistema habilita «🔄 Reenviar nuevo código» cuando termina la espera de 60 segundos o cuando el código expira. |
| **A002-2.** El usuario presiona «🔄 Reenviar nuevo código». | |
| | **A002-3.** El sistema invalida el código anterior, genera y envía uno nuevo, reinicia la vigencia a cinco minutos y restablece la espera de reenvío. Si la solicitud excede los límites permitidos, continúa en E006. |

##### A003: Acceso con consentimiento vigente
* **Paso origen:** Paso 6 del Flujo Normal o A001.
* **Condición de activación:** La identidad fue verificada y existe un consentimiento vigente.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **A003-1.** El sistema omite la ventana de consentimiento y continúa en el Paso 10 del Flujo Normal. |

##### A004: Cambiar correo o cancelar el desafío visible
* **Paso origen:** Paso 4 del Flujo Normal.
* **Condición de activación:** El usuario desea corregir la dirección o abandonar la verificación actual.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **A004-1.** El usuario presiona «Cambiar correo» o «Cancelar». | |
| | **A004-2.** El sistema descarta el formulario de verificación visible, limpia el código escrito y vuelve a la pantalla de ingreso de correo. |

##### A005: Cierre voluntario de sesión
* **Paso origen:** Paso 10 del Flujo Normal.
* **Condición de activación:** El usuario decide finalizar su acceso.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **A005-1.** El usuario presiona «Cerrar Sesión». | |
| | **A005-2.** El sistema elimina la sesión activa del navegador, restablece el rol visible y retorna a «Iniciar Sesión Institucional». |

#### 7.4. Flujos de excepción

##### E001: Correo no institucional o no válido
* **Paso origen:** Paso 4 del Flujo Normal o A001.
* **Condición de activación:** La dirección tiene un formato no válido o no pertenece a `@virtual.upt.pe` ni `@upt.pe`.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E001-1.** El sistema no solicita el envío del código y muestra el motivo. Para un dominio ajeno presenta: «Acceso restringido: Solo se permiten correos institucionales con dominio @virtual.upt.pe o @upt.pe.». |
| **E001-2.** El usuario corrige la dirección y vuelve a presionar «Continuar con Código OTP →». | |
| | **E001-3.** El sistema retoma el Paso 4 del Flujo Normal. |

##### E002: No se puede emitir o enviar el código
* **Paso origen:** Paso 4 del Flujo Normal o A002.
* **Condición de activación:** El servicio no puede registrar el desafío o entregar el correo institucional.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E002-1.** El sistema informa que no fue posible generar o enviar el código. No presenta la solicitud como completada y permite reintentar cuando el servicio esté disponible. |

##### E003: Código incorrecto
* **Paso origen:** Paso 6 del Flujo Normal.
* **Condición de activación:** El código ingresado no coincide con el código activo.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E003-1.** El sistema muestra que el código es incorrecto e indica cuántos intentos quedan antes de bloquear ese desafío. |
| **E003-2.** El usuario corrige el código y vuelve a presionar «Verificar y Acceder». | |
| | **E003-3.** El sistema retoma el Paso 6 del Flujo Normal. |

##### E004: Código vencido
* **Paso origen:** Paso 6 del Flujo Normal.
* **Condición de activación:** Transcurrieron cinco minutos desde la emisión del código.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E004-1.** El contador llega a «⏳ Expira en: 00:00», el campo y «Verificar y Acceder» quedan inactivos, y el sistema informa: «El código OTP ha expirado (5 minutos). Por favor solicita un nuevo código.». Se habilita el reenvío. |
| **E004-2.** El usuario solicita un nuevo código. | |
| | **E004-3.** El sistema continúa en A002. |

##### E005: Máximo de intentos de verificación alcanzado
* **Paso origen:** Paso 6 del Flujo Normal.
* **Condición de activación:** El usuario registra cinco códigos incorrectos para el mismo desafío.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E005-1.** El sistema bloquea de forma definitiva ese desafío e informa que se alcanzó el máximo de cinco intentos. Para continuar, el usuario debe volver al ingreso de correo y solicitar un código nuevo. |

##### E006: Espera obligatoria o límite de solicitudes
* **Paso origen:** Paso 4 del Flujo Normal o A002.
* **Condición de activación:** Se intenta solicitar o reenviar un código durante la espera, o se supera el límite de solicitudes permitido en la ventana de seguridad.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E006-1.** El sistema rechaza temporalmente la solicitud e indica el tiempo de espera o que se realizaron demasiadas solicitudes. |
| **E006-2.** El usuario espera el periodo indicado y vuelve a solicitar el código. | |
| | **E006-3.** El sistema retoma el Paso 4 o A002, según corresponda. |

##### E007: Rechazo del consentimiento informado
* **Paso origen:** Paso 8 del Flujo Normal.
* **Condición de activación:** El usuario presiona «🚫 Rechazar y Salir».

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| **E007-1.** El usuario rechaza el tratamiento de datos. | |
| | **E007-2.** El sistema registra el rechazo cuando corresponde, cierra la sesión y retorna al acceso. No habilita las funciones protegidas. |

##### E008: Fallo de comunicación o servicio no disponible
* **Paso origen:** Cualquier operación remota del flujo.
* **Condición de activación:** La red, la base de datos o un servicio requerido no responde.

| **Acción del Actor** | **Respuesta del Sistema** |
|---|---|
| | **E008-1.** El sistema muestra el error disponible sin presentar la operación como completada. |
| **E008-2.** El usuario comprueba su conexión y reintenta la acción. | |
| | **E008-3.** Si el servicio se restablece, el sistema retoma el paso correspondiente. |

#### 7.5. Diagrama de flujo de actividades

**Figura 1. Diagrama de actividades — CUS-001: Iniciar sesión institucional con 2FA.**

![Figura 1. Diagrama de actividades — CUS-001: Iniciar sesión institucional con 2FA.](docs/narrativas/diagramas/img/CUS-001_actividades.png)

Fuente: Elaboración propia.

#### 7.6. Diagrama de caso de uso

**Figura 2. Diagrama de caso de uso — CUS-001: Iniciar sesión institucional con 2FA.**

![Figura 2. Diagrama de caso de uso — CUS-001: Iniciar sesión institucional con 2FA.](docs/narrativas/diagramas/img/CUS-001_caso_de_uso.png)

Fuente: Elaboración propia.
