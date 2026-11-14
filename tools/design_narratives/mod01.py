# -*- coding: utf-8 -*-
"""
Modulo 01: Seguridad, Autenticación y Gobernanza (Fase de Diseño)
Contiene: CUS-001, CUS-010
"""

def get_mod01():
    return """### MOD-01: Seguridad, Autenticación y Gobernanza

#### CUS-001 - Iniciar sesión institucional con 2FA

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-001** (CUS-001) |
| **Nombre** | Iniciar sesión institucional con 2FA y autenticación federada Google Workspace |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-001 (Autenticación multifactor 2FA institucional), RF-002 (Formalización de consentimiento digital Ley 29733); RN-01 (Dominio institucional @virtual.upt.pe y @upt.pe con OTP de 5 minutos y cooldown de 60 segundos), RN-02 (Consentimiento informado legal digital) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian |
| **Actores** | Estudiante Mentoreado, Estudiante Mentor, Administrador Institucional (Primarios); Servicio SMTP Gmail Institucional, Google Identity Services GIS (Secundarios) |
| **Interacción** | Fase de Construcción / Iteración Sprint 01 - Sprint 02 (Actualización Post-Sprint 08 con Google Identity y SMTP real) |
| **Descripción** | Permite autenticar la identidad del usuario universitario mediante flujo dual sin contraseñas estáticas, validando la pertenencia al dominio oficial @virtual.upt.pe o @upt.pe a través del controlador aplicacion/backend/app/api/v1/endpoints/auth.py. El usuario puede autenticarse mediante credencial federada de Google Workspace UPT utilizando el SDK oficial de Google Identity Services (GIS), o solicitando un código OTP numérico criptográficamente seguro de 6 dígitos con expiración de 300 segundos persistido en la tabla auth_challenges (app/models/auth.py) y despachado mediante el transporte SMTP Gmail institucional de auth_service.py (AuthService.request_otp). El código se valida en POST /api/v1/auth/otp/verify. El sistema verifica el estado del consentimiento informado bajo la Ley Nº 29733 en app/services/consent_service.py; si es nuevo, despliega ConsentModalView.tsx y formaliza la aceptación persistiendo IP, User-Agent y timestamp en consentimientos_legales (app/models/consent.py). Tras la validación, expide un token JWT criptográfico (HS256) con 8 horas de vigencia (ACCESS_TOKEN_EXPIRE_MINUTES = 480) y claims de roles institucionales, retornando el payload al frontend LoginOtpView.tsx para su almacenamiento seguro en localStorage. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios de Acreditación ICACIT<br>Documento de Arquitectura de Software (SAD v3.0 - MOD-01: Seguridad, Autenticación y Gobernanza)<br>Ley Nº 29733 de Protección de Datos Personales del Perú y D.S. Nº 003-2013-JUS |
| **Anexos** | aplicacion/frontend/src/components/LoginOtpView.tsx<br>aplicacion/frontend/src/components/ConsentModalView.tsx<br>aplicacion/frontend/src/services/authService.ts (AuthService, apiClient)<br>aplicacion/frontend/src/services/consentService.ts (ConsentService)<br>aplicacion/backend/app/api/v1/endpoints/auth.py (POST /api/v1/auth/otp/request, POST /api/v1/auth/otp/verify, POST /api/v1/auth/otp/resend, POST /api/v1/auth/google)<br>aplicacion/backend/app/api/v1/endpoints/consent.py (GET /api/v1/consent/status, POST /api/v1/consent/accept)<br>aplicacion/backend/app/services/auth_service.py (AuthService.request_otp, AuthService.verify_otp)<br>aplicacion/backend/app/services/email_service.py (EmailService.send_otp_email)<br>aplicacion/backend/app/models/auth.py (AuthChallenge), app/models/consent.py (ConsentimientoLegal) |
| **Precondiciones** | 1. El usuario posee una cuenta activa perteneciente al dominio oficial @virtual.upt.pe o @upt.pe.<br>2. El servicio SMTP institucional o el cliente Google Identity Services se encuentra configurado en el backend con credenciales operativas.<br>3. El usuario no registra suspensión administrativa en usuarios.activo = true. |
| **PostCondiciones** | 1. Token JWT institucional (HS256) generado y almacenado en localStorage con vigencia estricta de 8 horas.<br>2. Traza inmutable de auditoría registrada en la tabla física consentimientos_legales con UUID, IP, User-Agent y marca de tiempo UTC.<br>3. Redirección reactiva en cliente al panel principal según el rol asignado (mentoreado, mentor o administrador). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Validación de identidad institucional y selección del método de acceso** | |
| **1.** El usuario accede a la vista de autenticación `LoginOtpView.tsx`, donde visualiza las opciones de acceso institucional: ingreso directo federado con Google Workspace UPT o ingreso por código OTP por correo. Si opta por código OTP, ingresa su dirección de correo institucional en el cuadro de texto `"Correo Institucional"` (`input[type="email"]`) y hace clic en el botón `"Enviar Código OTP"`. | **2.** En `authService.ts`, la función `requestOtp(email)` despacha una petición `POST /api/v1/auth/otp/request` con payload JSON `{"email": email}` hacia el controlador `auth.py`. El backend valida con Pydantic (`EmailStr`) la sintaxis y comprueba que `email.endswith("@virtual.upt.pe")` o `email.endswith("@upt.pe")`. Ejecuta `SELECT * FROM usuarios WHERE email = :email AND activo = true`. (Si el dominio es ajeno a la universidad, salta a E001). (Si el usuario prefiere autenticarse con Google Workspace UPT mediante el botón oficial, salta a A001). (Si la cuenta está inactiva o suspendida, salta a E002). |
| **Fase 2: Generación criptográfica, despacho SMTP y verificación de código temporal OTP** | |
| **3.** El usuario revisa en pantalla el correo verificado y presiona el botón `"Enviar Código OTP"`. | **4.** En `auth_service.py`, `AuthService.request_otp()` genera un código numérico aleatorio seguro mediante `secrets.randbelow(900000) + 100000`, registra el desafío en la tabla física `auth_challenges` con expiración `NOW() + INTERVAL '5 MINUTES'` y cooldown de 60 segundos (RN-01). Invoca a `EmailService.send_otp_email()` para despachar el correo SMTP institucional. Retorna HTTP 200 con `challenge_id` y `expires_at`. En cliente, `LoginOtpView.tsx` conmuta al paso de verificación, inicializa el temporizador regresivo de 300 segundos en color azul institucional y enfoca el campo del código. (Si el usuario no recibe el código en su buzón tras 60 segundos o el temporizador expira, salta a A002). |
| **5.** El usuario consulta su bandeja institucional, copia el código de 6 dígitos numéricos, lo ingresa en el componente y hace clic en el botón `"Verificar y Acceder"`. (Si el usuario decide corregir el correo o cancelar el desafío, salta a A004). | **6.** En `authService.ts`, se despacha `POST /api/v1/auth/otp/verify` con payload `{"challenge_id": challengeId, "otp_code": cleanOtp}`. `auth_service.py` recupera el registro, compara el código y valida `expira_en > NOW()`. Si coincide, invalida el OTP usado marcándolo como consumido y consulta `ConsentService.get_consent_status(email)`. (Si el código es incorrecto, salta a E003). (Si el código ha expirado, salta a E004). (Si se superan los 3 intentos fallidos consecutivos, salta a E005). (Si el usuario ya cuenta con consentimiento digital previo, salta a A003). |
| **Fase 3: Formalización de consentimiento legal digital Ley 29733 y emisión de sesión** | |
| **7.** El cliente renderiza el componente modal `ConsentModalView.tsx`. El usuario lee los términos de tratamiento de datos personales en el panel con barra de desplazamiento vertical, marca la casilla de verificación `"He leído y acepto los términos de consentimiento informado bajo la Ley Nº 29733"` y presiona el botón `"Aceptar y Continuar"`. (Si el usuario desmarca o rechaza los términos, salta a E006). | **8.** En `consentService.ts`, se invoca `POST /api/v1/consent/accept` enviando el identificador de usuario y la versión de términos. El backend inserta en `consentimientos_legales` el registro inmutable con IP de origen (`client.host`), User-Agent y timestamp UTC (RN-02). Seguidamente, `security.py` genera el token JWT firmado mediante `create_access_token` incluyendo los claims `sub: email`, `roles: [UserRole]`, `exp: now + 8h`. El backend retorna HTTP 200 con `access_token` y perfil. En `App.tsx`, el token se persiste en `localStorage`, se actualiza el estado global de autenticación y se redirige al panel correspondiente al rol, mostrando una notificación flotante en color verde de éxito: *"¡Sesión institucional iniciada exitosamente! Bienvenido al Sistema de Mentorías EPIS-UPT"*. (Si la comunicación con el servidor falla durante la emisión de sesión, salta a E007). |

##### Flujos Alternativos

##### Flujo alternativo A001: Autenticación federada directa con Google Workspace institucional (GIS)
| Usuario | Sistema |
|---|---|
| **A001-1.1** El usuario visualiza el contenedor de Google Identity Services en `LoginOtpView.tsx` y hace clic en el botón `"Continuar con Google Workspace UPT"`. | **A001-1.2** El navegador despliega el diálogo nativo One-Tap o la ventana emergente de Google Accounts solicitando la selección de la cuenta `@virtual.upt.pe` o `@upt.pe`. |
| **A001-1.3** El usuario selecciona su cuenta institucional y concede la autorización de identidad. | **A001-1.4** Google Identity Services emite un ID Token criptográfico JWT firmado. En `authService.ts`, la función `loginWithGoogle(idToken)` despacha una petición `POST /api/v1/auth/google` enviando la credencial. En `auth.py`, `auth_service.py` valida la firma del token con los certificados públicos de Google, verifica el `client_id` oficial, comprueba que el dominio corresponda a `@virtual.upt.pe` o `@upt.pe`, y consulta el estado de consentimiento informado en `ConsentService.get_consent_status(email)` y retorna al paso 6 del Flujo Normal de Eventos. |

##### Flujo alternativo A002: Reenvío de código temporal por retraso en buzón tras cumplir el cooldown
| Usuario | Sistema |
|---|---|
| **A002-1.1** El usuario constata la ausencia del código en su buzón tras 60 segundos o la finalización del temporizador regresivo de 5 minutos, y hace clic en el enlace `"Reenviar código OTP"`. | **A002-1.2** En `LoginOtpView.tsx`, se valida que hayan transcurrido al menos 60 segundos desde la última solicitud. Despacha una petición `POST /api/v1/auth/otp/resend` con payload `{"challenge_id": challenge.challengeId}` hacia el controlador `auth.py`. |
| **A002-1.3** El usuario visualiza la actualización del temporizador regresivo reiniciado a 5 minutos en color azul institucional y una alerta en color ámbar: *"Se ha generado y enviado un nuevo código OTP. El anterior ha sido invalidado"*. | **A002-1.4** El backend invalida el desafío anterior, genera una nueva clave aleatoria de 6 dígitos, la despacha vía SMTP Gmail institucional y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo alternativo A003: Acceso recurrente con consentimiento digital previamente formalizado
| Usuario | Sistema |
|---|---|
| **A003-1.1** El usuario completa satisfactoriamente el paso 5 introduciendo el código OTP válido. | **A003-1.2** En `auth.py`, `ConsentService.get_consent_status` retorna `has_consented = true` tras localizar en `consentimientos_legales` el registro activo sin revocación. |
| **A003-1.3** El usuario visualiza la pantalla de carga con indicador circular de progreso en color azul institucional. | **A003-1.4** El sistema omite la renderización de `ConsentModalView.tsx`, emite directamente el token JWT firmado de sesión con sus roles asignados y retorna al paso 8 del Flujo Normal de Eventos. |

##### Flujo alternativo A004: Cancelación del desafío y cambio de correo institucional
| Usuario | Sistema |
|---|---|
| **A004-1.1** Durante el paso de ingreso de código OTP, el usuario constata que escribió erróneamente su correo y hace clic en el enlace `"Cambiar de correo institucional"`. | **A004-1.2** `LoginOtpView.tsx` invoca `authService.cancelChallenge()`, purga el `challengeId` del estado local y restablece las variables del componente. |
| **A004-1.3** El usuario observa la transición limpia de regreso hacia la pantalla inicial de ingreso de correo. | **A004-1.4** El sistema enfoca nuevamente el cuadro de texto `"Correo Institucional"` y retorna al paso 1 del Flujo Normal de Eventos sin generar registros. |

##### Flujos de Excepción

##### Flujo de excepción E001: Dominio de correo no institucional
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `auth.py` comprueba que la cadena ingresada no termina en `@virtual.upt.pe` ni `@upt.pe`. Lanza `HTTPException(status_code=400, detail="INVALID_DOMAIN: Acceso restringido: Solo se permiten correos institucionales con dominio @virtual.upt.pe o @upt.pe.")`.<br><br>En `authService.ts`, captura el error 400 y propaga la excepción hacia el componente. `LoginOtpView.tsx` despliega una etiqueta de advertencia en color rojo: *"Acceso restringido: Solo se permiten correos institucionales con dominio @virtual.upt.pe o @upt.pe."*. Presenta el botón `"Corregir Correo"`. |
| **E001-1.2** Hace clic en el botón "Corregir Correo". | **E001-1.3** Limpia el cuadro de texto `"Correo Institucional"`, le asigna el foco automáticamente y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Cuenta institucional inactiva o suspendida
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 2 del Flujo Normal, `auth.py` ejecuta `SELECT activo FROM usuarios WHERE email = :email` y detecta `activo = false`. Lanza `HTTPException(status_code=403, detail="ACCOUNT_SUSPENDED: Su cuenta institucional registra suspensión administrativa.")`.<br><br>En `LoginOtpView.tsx`, se captura el error 403 y se despliega un cuadro de diálogo modal en color rojo con el mensaje: *"Cuenta inhabilitada. Su registro se encuentra en estado inactivo. Por favor, comuníquese con la Dirección de Escuela EPIS-UPT"*. Presenta el botón `"Aceptar"`. |
| **E002-1.2** Hace clic en el botón "Aceptar". | **E002-1.3** Cierra el cuadro modal, restablece el formulario inicial y finaliza la sesión sin generar registros de autenticación. |

##### Flujo de excepción E003: Código temporal OTP incorrecto
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 6 del Flujo Normal, `auth_service.py` comprueba que el código introducido no coincide con el persistido en base de datos. Incrementa el contador `intentos_fallidos += 1` y lanza `HTTPException(status_code=400, detail="INVALID_OTP: El código ingresado no coincide con el enviado a su buzón institucional.")`.<br><br>En `LoginOtpView.tsx`, se captura el error y se muestra una alerta en color rojo indicando el error y el número de intentos restantes (e.g. *"El código debe contener exactamente 6 dígitos numéricos válidos"*). Presenta el botón `"Reintentar"`. |
| **E003-1.2** Hace clic en el botón "Reintentar". | **E003-1.3** Limpia el campo de entrada numérica, posiciona el cursor en la casilla y retorna al paso 5 del Flujo Normal de Eventos. |

##### Flujo de excepción E004: Código temporal OTP expirado
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 6 del Flujo Normal, `auth_service.py` comprueba que `NOW() > expira_en` (plazo de 5 minutos excedido conforme a RN-01). Lanza `HTTPException(status_code=400, detail="EXPIRED_OTP: El código temporal OTP ha expirado (5 minutos). Por favor solicita un nuevo código.")`.<br><br>En `LoginOtpView.tsx`, se captura el error y se despliega una alerta en color ámbar: *"El código OTP ha expirado (5 minutos). Por favor solicita un nuevo código."*. Presenta el botón `"Solicitar Nuevo Código"`. |
| **E004-1.2** Hace clic en el botón "Solicitar Nuevo Código". | **E004-1.3** Restablece el formulario, reinicia el temporizador regresivo y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E005: Bloqueo temporal por exceso de intentos fallidos
| Usuario | Sistema |
|---|---|
| | **E005-1.1** En el paso 6 del Flujo Normal, `auth_service.py` evalúa `intentos_fallidos >= 3`. Invalida inmediatamente el OTP, bloquea temporalmente la emisión para el correo por 15 minutos en base de datos y lanza `HTTPException(status_code=429, detail="MAX_ATTEMPTS_EXCEEDED: Se ha superado el límite de 3 intentos fallidos consecutivos. Acceso bloqueado temporalmente.")`.<br><br>En `LoginOtpView.tsx`, se bloquea el campo de entrada y se despliega un panel de seguridad en color rojo indicando el bloqueo temporal. Presenta el botón `"Volver al Inicio"`. |
| **E005-1.2** Hace clic en el botón "Volver al Inicio". | **E005-1.3** Redirige a la vista inicial de autenticación, restablece el formulario y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E006: Rechazo voluntario del consentimiento informado
| Usuario | Sistema |
|---|---|
| | **E006-1.1** En el paso 7 del Flujo Normal, el usuario no marca la casilla de verificación o presiona el botón `"Declinar y Salir"`. `ConsentModalView.tsx` captura la acción sin enviar petición de aceptación.<br><br>Despliega un cuadro de diálogo modal en color ámbar advirtiendo que la formalización del consentimiento legal bajo la Ley Nº 29733 es un requisito obligatorio e indispensable para utilizar los servicios de la plataforma. Presenta el botón `"Confirmar Salida"` y el botón `"Revisar Términos"`. |
| **E006-1.2** Hace clic en el botón "Confirmar Salida". | **E006-1.3** Destruye la sesión provisional, purga los datos temporales del formulario, emite notificación informativa y retorna al paso 1 del Flujo Normal de Eventos sin generar registros. |

##### Flujo de excepción E007: Fallo de conectividad o indisponibilidad del servicio de autenticación
| Usuario | Sistema |
|---|---|
| | **E007-1.1** En el paso 8 del Flujo Normal, la conexión con el servidor sufre timeout o interrupción de red. `authService.ts` captura el error y lanza `AuthException("Error inesperado de comunicación con el servicio de autenticación.")`.<br><br>En `LoginOtpView.tsx`, se despliega un banner de error en color rojo con el mensaje de indisponibilidad. Presenta el botón `"Reintentar Conexión"`. |
| **E007-1.2** Hace clic en el botón "Reintentar Conexión". | **E007-1.3** Restablece los controles y retorna al paso 1 del Flujo Normal de Eventos sin generar registros. |

##### Especificación Exhaustiva de Interfaz de Usuario y Comportamiento Visual

La interfaz de usuario del componente `LoginOtpView.tsx` está diseñada conforme a las directrices de accesibilidad institucional:
1. **Contenedor Principal:** Tarjeta centralizada con fondo en color blanco puro, bordes redondeados y sombra suave, con un borde exterior sutil en color gris claro.
2. **Encabezado Institucional:** Emblema institucional superior con fondo en color azul institucional y tipografía en color dorado institucional con el texto `"UPT"`. Título principal en tipografía destacada en color azul institucional `"Iniciar Sesión Institucional"` y párrafo explicativo en color gris secundario: `"Ingresa tu correo institucional @upt.pe para recibir un código de verificación temporal."`.
3. **Acceso Federado con Google Identity Services (GIS):** Contenedor `#googleSignInBtnContainer` que aloja el botón oficial de Google con tema delineado, tamaño grande, texto `"Continuar con Google"` y ancho adaptativo. En caso de indisponibilidad del SDK, se renderiza un botón alternativo en color blanco puro con borde gris claro y el icono oficial de Google acompañado del texto `"Continuar con Google Workspace UPT"`.
4. **Divisor Visual:** Línea divisoria horizontal en color gris claro con texto central en tipografía reducida y color gris neutro: `"O CON CÓDIGO OTP POR CORREO"`.
5. **Formulario de Solicitud de Correo:** Cuadro de texto con etiqueta visible `"Correo Institucional"`, borde en color gris claro y texto de ejemplo institucional. Botón principal de acción en color azul institucional y tipografía en color blanco puro con el texto `"Enviar Código OTP"`.
6. **Vista de Desafío OTP:** Despliega el subtítulo en color gris secundario indicando el correo al que se despachó el código, seguido de un cuadro de texto para el ingreso de los 6 dígitos numéricos con tipografía monoespaciada en color azul institucional. Cuenta con un temporizador regresivo de 5 minutos en color azul institucional y un botón de reenvío con texto `"Reenviar código OTP"` deshabilitado en color gris claro mientras el contador de cooldown permanezca activo. Incluye el enlace de acción secundaria en color azul institucional `"Cambiar de correo institucional"`.
7. **Notificaciones y Alertas:** Banner de alerta ante errores con fondo en color rojo suave, borde en color rojo claro y texto en color rojo oscuro. Mensajes informativos con fondo en color azul suave, borde en color azul claro y texto en color azul marino. Notificaciones de éxito con fondo en color verde suave, borde en color verde claro y texto en color verde oscuro.
8. **Accesibilidad WCAG 2.1 AA:** Elementos con atributos semánticos `role="alert"` para mensajes de error y `role="status"` para confirmaciones. Soporte de navegación por teclado mediante tabulación secuencial y foco visual contrastado.

##### Criterios de Aceptación Formativos (Given-When-Then)

```gherkin
Escenario 1: Autenticación exitosa mediante código temporal OTP institucional
  DADO QUE el estudiante o mentor posee una cuenta institucional activa con dominio "@virtual.upt.pe" o "@upt.pe"
  CUANDO ingresa su dirección de correo en LoginOtpView y presiona el botón "Enviar Código OTP"
  Y digita en el formulario el código numérico de 6 dígitos recibido en su buzón dentro de los 5 minutos de vigencia
  Y presiona el botón "Verificar y Acceder"
  ENTONCES el sistema valida satisfactoriamente el desafío en POST /api/v1/auth/otp/verify
  Y emite un token JWT criptográfico con vigencia de 8 horas continuas persistido en localStorage
  Y redirige al usuario hacia el panel correspondiente a su rol institucional desplegando un mensaje de bienvenida.
  Evidencia de Prueba: test_auth.py::test_verify_otp_success / LoginOtpView.test.tsx

Escenario 2: Autenticación federada exitosa mediante Google Identity Services (GIS)
  DADO QUE el usuario universitario se encuentra en la pantalla de inicio de sesión
  CUANDO pulsa el botón oficial "Continuar con Google Workspace UPT"
  Y selecciona su cuenta institucional activa con dominio "@virtual.upt.pe" o "@upt.pe" en el diálogo de Google
  ENTONCES el sistema recibe la credencial firmada y despacha la petición POST /api/v1/auth/google
  Y el backend valida la firma criptográfica con los servidores de Google emitiendo el token de sesión JWT institucional
  Y formaliza el acceso directo al panel del rol correspondiente.
  Evidencia de Prueba: test_auth.py::test_google_auth_success / authService.test.ts

Escenario 3: Rechazo de acceso ante ingreso de correo no institucional
  DADO QUE un usuario ingresa una dirección de correo perteneciente a un dominio comercial o externo (ej. "@gmail.com")
  CUANDO presiona el botón "Enviar Código OTP"
  ENTONCES el sistema bloquea la solicitud en el cliente y en el endpoint POST /api/v1/auth/otp/request retornando HTTP 400
  Y despliega en pantalla un mensaje de error en color rojo: "Acceso restringido: Solo se permiten correos institucionales con dominio @virtual.upt.pe o @upt.pe."
  Y no genera ningún registro en la tabla física auth_challenges ni emite códigos por correo.
  Evidencia de Prueba: test_auth.py::test_request_otp_invalid_domain / LoginOtpView.test.tsx

Escenario 4: Rechazo de ingreso por código temporal OTP expirado tras superar los 5 minutos
  DADO QUE el usuario solicitó un código OTP y transcurrieron más de 300 segundos desde su emisión
  CUANDO ingresa el código numérico en el formulario y presiona el botón "Verificar y Acceder"
  ENTONCES el backend rechaza la verificación retornando HTTP 400 con código de error "EXPIRED_OTP"
  Y el componente LoginOtpView despliega una notificación de advertencia en color ámbar solicitando la generación de un nuevo código
  Y mantiene habilitado el botón "Reenviar código OTP" tras haberse superado el cooldown reglamentario.
  Evidencia de Prueba: test_auth.py::test_verify_otp_expired / authService.test.ts
```

#### CUS-010 - Gestionar asignación de roles de usuario

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-010** (CUS-010) |
| **Nombre** | Gestionar asignación y revocación de roles institucionales de usuario |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-003 (Gestión y asignación administrativa de roles de usuario); RN-03 (Separación de privilegios y control de acceso RBAC institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Cristian |
| **Actores** | Administrador Institucional (`UserRole.administrador`), Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 01 - Sprint 02 |
| **Descripción** | Permite a las autoridades institucionales consultar la nómina universitaria de usuarios y administrar sus roles operativos (`UserRole.mentoreado`, `UserRole.mentor`, `UserRole.administrador`, `UserRole.coordinador`) a través del componente `AdminDashboardView.tsx` y el servicio `roleService.ts`. El backend expone los endpoints en `aplicacion/backend/app/api/v1/endpoints/roles.py`, verificando en cada solicitud los privilegios administrativos con `app/core/security.py` (`decode_access_token` comprobando claim `roles` conteniendo `administrador`). El servicio `role_service.py` ejecuta mutaciones transaccionales ACID en las tablas `roles` y `roles_usuarios` (`app/models/roles.py`), garantizando que ningún usuario quede huérfano de roles y que ningún administrador pueda revocar sus propios privilegios. Cada mutación genera una traza en la tabla de auditoría con el UUID del administrador ejecutor, IP de origen y marca de tiempo UTC. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-01: Seguridad, Autenticación y Gobernanza)<br>Modelo de Control de Acceso Basado en Roles (NIST RBAC Standard) |
| **Anexos** | `aplicacion/frontend/src/components/AdminDashboardView.tsx`<br>`aplicacion/frontend/src/services/roleService.ts` (`RoleService`, `ApiRoleAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/roles.py` (`GET /api/v1/roles/users`, `POST /api/v1/roles/assign`, `DELETE /api/v1/roles/revoke`)<br>`aplicacion/backend/app/services/role_service.py` (`RoleService.list_users`, `RoleService.assign_role`, `RoleService.revoke_role`)<br>`aplicacion/backend/app/models/roles.py` (`Rol`, `RolUsuario`, `UserRole`), `app/models/auth.py` (`Usuario`) |
| **Precondiciones** | 1. El usuario solicitante ha iniciado sesión institucional válida portando un token JWT activo en `localStorage`.<br>2. El claim `roles` dentro del payload JWT contiene el valor `UserRole.administrador`.<br>3. El catálogo institucional de roles base se encuentra inicializado en la tabla física `roles`. |
| **PostCondiciones** | 1. Inserción o eliminación atómica confirmada en la tabla `roles_usuarios` mediante `db.commit()`.<br>2. Registro de auditoría persistido en la base de datos con identificador del operador, usuario modificado y cambio realizado.<br>3. Actualización reactiva del estado del usuario en el componente de gestión de roles de la interfaz administrativa. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al panel administrativo y consulta de nómina de usuarios** | |
| **1.** El administrador institucional accede al panel de control en `AdminDashboardView.tsx` y hace clic en la pestaña `"Gestión de Roles"`. | **2.** En `roleService.ts`, se despacha la petición `GET /api/v1/roles/users` incluyendo en la cabecera `Authorization: Bearer <token>`. En `roles.py`, la función dependiente `require_admin_role` valida la firma criptográfica y verifica que `UserRole.administrador` esté presente en los claims. `role_service.py` ejecuta una consulta relacional `SELECT u.id, u.email, u.nombres, u.apellidos, array_agg(r.nombre) AS roles FROM usuarios u LEFT JOIN roles_usuarios ru ON u.id = ru.id_usuario LEFT JOIN roles r ON ru.id_rol = r.id GROUP BY u.id`. Retorna HTTP 200 con la nómina paginada. `AdminDashboardView.tsx` renderiza la tabla interactiva de usuarios con filtros de búsqueda y botones de acción. (Si el token no cuenta con privilegios administrativos, salta a E001). (Si la consulta falla por timeout en base de datos, salta a E002). |
| **Fase 2: Búsqueda y selección de usuario para modificación** | |
| **3.** El administrador ingresa el código universitario o correo institucional del estudiante o docente en el cuadro de búsqueda `"Buscar usuario"` y hace clic en el botón `"Buscar"`. | **4.** En `AdminDashboardView.tsx`, se filtra la lista de usuarios en memoria o se despacha `GET /api/v1/roles/users?q=...`. El sistema resalta la fila del usuario localizado. El administrador hace clic en el botón `"Modificar Roles"` en la fila correspondiente. El sistema despliega un cuadro de diálogo modal `"Asignación de Roles Institucionales"` con casillas de verificación para cada rol del sistema (`Mentoreado`, `Mentor`, `Administrador`, `Coordinador`), marcando los roles actualmente asignados. (Si la búsqueda no arroja coincidencias en el padrón, salta a A001). |
| **Fase 3: Modificación atómica de roles y registro de auditoría** | |
| **5.** El administrador marca o desmarca las casillas según corresponda (e.g. asigna el rol `Mentor` a un estudiante habilitado) y hace clic en el botón `"Guardar Asignación"`. | **6.** En `roleService.ts`, se despacha una petición `POST /api/v1/roles/assign` con payload `RoleAssignRequest(user_id=target_user_id, roles=selected_roles)`. `role_service.py` inicia una transacción ACID con `db.begin()`. Verifica que el conjunto de roles resultante no esté vacío y que el administrador no esté revocando su propio rol de administrador. Ejecuta las sentencias `DELETE FROM roles_usuarios WHERE id_usuario = :uid` e `INSERT INTO roles_usuarios (id_usuario, id_rol) VALUES ...`. Inserta la traza de auditoría, ejecuta `db.commit()` y retorna HTTP 200 con el perfil actualizado. `AdminDashboardView.tsx` actualiza reactivamente la tabla de usuarios, cierra la ventana modal y despliega una notificación flotante en color verde de éxito: *"Roles actualizados exitosamente para el usuario"*. (Si intenta revocar todos los roles dejando al usuario sin privilegios, salta a E003). (Si intenta auto-revocarse el rol de Administrador, salta a E004). |

##### Flujos Alternativos

##### Flujo alternativo A001: Búsqueda sin coincidencias en el padrón institucional
| Usuario | Sistema |
|---|---|
| **A001-1.1** El administrador ingresa un criterio de búsqueda en el paso 3 que no coincide con ningún registro activo. | **A001-1.2** En `AdminDashboardView.tsx`, el filtro retorna una lista vacía. El sistema despliega en la tabla un panel informativo con el mensaje: *"No se encontraron usuarios que coincidan con el criterio ingresado. Verifique el código o correo institucional"*. Presenta el botón `<button onClick={handleClearSearch}>Limpiar Búsqueda</button>`. |
| **A001-1.3** El administrador hace clic en el botón "Limpiar Búsqueda". | **A001-1.4** Restablece el cuadro de búsqueda, recarga la nómina completa de usuarios en la tabla y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Acceso denegado por privilegios administrativos insuficientes
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `roles.py` evalúa el token JWT del usuario y detecta que no incluye el rol `administrador`. Lanza `HTTPException(status_code=403, detail="FORBIDDEN: Se requieren privilegios de Administrador Institucional para acceder a este módulo.")`.<br><br>En `App.tsx`, el interceptor de peticiones captura el código 403 y redirige inmediatamente al usuario a su panel correspondiente según su rol, desplegando un aviso en color rojo: *"Acceso Restringido: No posee autorización para el módulo de administración de roles"*. |
| **E001-1.2** Hace clic en el botón "Entendido" en la alerta de restricción. | **E001-1.3** Cierra el aviso y retorna al paso 1 del Flujo Normal de Eventos en su vista autorizada. |

##### Flujo de excepción E002: Error de conexión o timeout en base de datos
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 2 del Flujo Normal, la conexión hacia PostgreSQL sufre timeout o interrupción de red. `roles.py` captura la excepción de base de datos y lanza `HTTPException(status_code=503, detail="SERVICE_UNAVAILABLE: No se pudo establecer conexión con el repositorio de usuarios. Reintente en unos instantes.")`.<br><br>En `AdminDashboardView.tsx`, se captura el error 503 y se despliega un panel de advertencia en color ámbar con el mensaje de indisponibilidad. Presenta el botón `<button onClick={fetchUsers}>Reintentar Carga</button>`. |
| **E002-1.2** Hace clic en el botón "Reintentar Carga". | **E002-1.3** Dispara nuevamente la petición `GET /api/v1/roles/users` y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Intento de dejar al usuario sin ningún rol asignado
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 6 del Flujo Normal, el administrador desmarca todas las casillas de roles. `role_service.py` valida `len(selected_roles) == 0`. Ejecuta `db.rollback()` y lanza `HTTPException(status_code=400, detail="EMPTY_ROLE_SET_PROHIBITED: Todo usuario debe mantener al menos un rol institucional asignado.")`.<br><br>En `AdminDashboardView.tsx`, se despliega un mensaje de error en color rojo dentro del modal indicando la obligatoriedad de al menos un rol institucional. Mantiene el modal abierto sin cerrar la transacción. |
| **E003-1.2** Marca al menos una casilla de rol válida (e.g. `Mentoreado`). | **E003-1.3** Rehabilita el botón `"Guardar Asignación"` y retorna al paso 5 del Flujo Normal de Eventos. |

##### Flujo de excepción E004: Intento de auto-revocación del rol Administrador
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 6 del Flujo Normal, el administrador intenta desmarcar el rol `Administrador` sobre su propia cuenta (`target_user_id == current_user_id`). `role_service.py` detecta la colisión de gobernanza, ejecuta `db.rollback()` y lanza `HTTPException(status_code=400, detail="CANNOT_REVOKE_OWN_ADMIN: Un administrador no puede auto-revocarse sus propios privilegios para evitar la pérdida de gobernanza institucional.")`.<br><br>En `AdminDashboardView.tsx`, se captura el error y se muestra una alerta en color rojo destacada dentro del modal. |
| **E004-1.2** Hace clic en el botón "Restablecer Selección". | **E004-1.3** Vuelve a marcar la casilla de Administrador en el modal y retorna al paso 5 del Flujo Normal de Eventos. |
"""
