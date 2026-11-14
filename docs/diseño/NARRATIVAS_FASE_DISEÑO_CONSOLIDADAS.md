# NARRATIVAS DE CASOS DE USO CONSOLIDADAS - FASE DE DISEÑO

**Sistema Web P2P de Mentorías Universitarias - EPIS UPT**
**Versión:** 2.0 (Fase de Diseño / Arquitectura y Construcción)
**Autores:** Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos

---

## 6.2.3. Escenarios de Casos de Uso (Fase de Diseño)

### Presentación de los Escenarios de Casos de Uso en Fase de Diseño

En la presente **Fase de Diseño de Software**, los escenarios de casos de uso traducen los requerimientos funcionales del sistema en especificaciones de comportamiento detalladas a nivel de arquitectura y código ejecutable. Cada especificación proporciona trazabilidad completa hacia los componentes de frontend (React 18 con TypeScript y Tailwind CSS), servicios y adaptadores HTTP (`apiClient`), controladores y rutas de FastAPI, esquemas de validación Pydantic, servicios de lógica de negocio, entidades del modelo relacional ORM en SQLAlchemy y transacciones ACID en PostgreSQL bajo control estricto de concurrencia y cerrojos pesimistas.

La estructura de cada caso de uso conserva con rigurosidad la plantilla canónica institucional:
1. **Ficha Técnica Estructurada (13 atributos):** Identificador unívoco (`Id Caso de Uso`), `Nombre`, `Tipo`, `Requisito ID (RF)`, `Versión` (2.0), `Autor`, `Actores` con roles de sistema (`UserRole`), `Interacción`, `Descripción` técnica exhaustiva, `Referencias` normativas y arquitectónicas, `Anexos` de código fuente, `Precondiciones` y `PostCondiciones`.
2. **Flujo Normal de Eventos:** Distribuido en columnas estrictas (**`Usuario`** | **`Sistema`**), subdividido en fases secuenciales de interacción con pasos numerados correlativamente y llamadas explícitas de desvío `(Si [condición], salta a E00X / A00X)`.
3. **Flujos Alternativos (`A00X`) y de Excepción (`E00X`):** Encabezados de bloque específicos, columnas **`Usuario`** | **`Sistema`**, pasos jerárquicos (`E00X-1.1`, `E00X-1.2`) y cláusula formal de retorno al paso correspondiente del Flujo Normal o cierre explícito del caso de uso.
4. **Trazabilidad de Código y Diseño:** Especificación exacta de endpoints RESTful, verbos HTTP, códigos de estado (`200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`, `503 Service Unavailable`), tipos de excepciones y directivas de control de concurrencia (`SELECT ... FOR UPDATE`, locks transaccionales y mecanismos de desempate).

A continuación, se presentan los 24 casos de uso canónicos estructurados en los 8 módulos arquitectónicos del sistema:

---

### MOD-01: Seguridad, Autenticación y Gobernanza

#### CUS-001 - Iniciar sesión institucional con 2FA

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-001** (CUS-001) |
| **Nombre** | Iniciar sesión institucional con 2FA y autenticación federada Google Workspace |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-001 (Autenticación multifactor 2FA institucional), RF-002 (Formalización de consentimiento digital Ley 29733); RN-01 (Dominio institucional @virtual.upt.pe y @upt.pe con OTP de 5 minutos y cooldown de 60 segundos), RN-02 (Consentimiento informado legal digital) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
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
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
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


---

### MOD-02: Ofertas de Mentoría y Gestión de Recursos

#### CUS-006 - Publicar oferta de mentoría académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-006** (CUS-006) |
| **Nombre** | Publicar oferta de mentoría académica con validación de antelación y aforo |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-008 (Publicación y parametrización de ofertas de mentoría), RF-009 (Aprovisionamiento automatizado de infraestructura); RN-01 (Autenticación y pertenencia de cuenta institucional), RN-03 (Mérito académico y habilitación de mentor ciclo >= VII), RN-04 (Ventana de antelación mínima de 24 horas a T-24h), RN-05 (Aforo máximo estricto de 10 presencial y 20 virtual) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los estudiantes mentores formalizar la apertura de una sesión de mentoría a través del componente cliente `OfferPublishView.tsx` y el servicio `offerService.ts`, despachando una petición `POST /api/v1/offers` hacia el controlador `aplicacion/backend/app/api/v1/endpoints/offers.py`. El backend valida el token JWT institucional extrayendo criptográficamente el claim del llamante mediante `_extract_caller_and_admin_status`, verificando que coincida con el correo del mentor o cuente con rol de administrador (RN-01). En `app/services/offer_service.py` (`OfferService.publish_offer`), se ejecutan las validaciones de negocio institucionales: comprobación de mérito académico y habilitación de mentor en ciclo >= VII (`validate_mentor_eligibility`, RN-03), cálculo estricto de antelación superior a 24 horas respecto a la fecha y hora actual en UTC (`calculate_advance_hours > 24h`, RN-04), y conformidad de capacidad según la modalidad (exactamente 10 cupos en presencial y 20 en virtual, RN-05). Se instancia y persiste la entidad ORM `SesionMentoria` (`app/models/offer.py`) en estado `PUBLICADA`, se confirma la transacción en PostgreSQL, se emite una respuesta HTTP 201 Created con el esquema `PublishOfferResponse` y se sincroniza la cartelera institucional en cliente. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-04: Planificación, Espacios y Agendamiento)<br>Reglamento Académico de Mentorías EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/OfferPublishView.tsx`<br>`aplicacion/frontend/src/services/offerService.ts` (`OfferService`, `ApiOfferAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/offers.py` (`POST /api/v1/offers`)<br>`aplicacion/backend/app/services/offer_service.py` (`OfferService.publish_offer`, `OfferService.validate_mentor_eligibility`, `OfferService.calculate_advance_hours`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`), `app/models/roles.py` (`UsuarioRol`, `Rol`), `app/models/profile.py` (`PerfilAcademico`), `app/schemas/offer.py` (`PublishOfferPayload`, `PublishOfferResponse`) |
| **Precondiciones** | 1. Usuario autenticado con token JWT institucional activo conteniendo el rol `UserRole.mentor`.<br>2. Perfil de mentor registrado en `perfiles_academicos` con ciclo académico actual >= VII (RN-03).<br>3. Fecha y hora de inicio fijadas con más de 24 horas de antelación respecto a la hora UTC actual del servidor (RN-04). |
| **PostCondiciones** | 1. Registro insertado en la tabla `sesiones_mentoria` con `estado = 'PUBLICADA'`, código de sesión generado `SES-XXXX` y aforo parametrizado.<br>2. Transacción confirmada en PostgreSQL (`db.commit()`) y refresco de entidad (`db.refresh()`).<br>3. Despliegue de comprobante de publicación en cliente con código identificador de sesión y botón para navegar a la cartelera o mis sesiones. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Configuración de la sesión y selección curricular** | |
| **1.** El estudiante mentor accede a la vista de publicación en `OfferPublishView.tsx` y selecciona la asignatura curricular en la lista desplegable `"Curso"`. | **2.** En `OfferPublishView.tsx`, se invoca `fetchCourseDetail(selectedCourseId)` despachando `GET /api/v1/curriculum/courses/{id}` hacia `endpoints/curriculum.py`. El backend ejecuta `CurriculumService.get_course_by_id(db, course_id)` consultando `temas_curriculares` en PostgreSQL y retorna HTTP 200 OK con `CourseDetailResponse`. `OfferPublishView.tsx` renderiza la lista de temas silábicos, los selectores de fecha y hora de inicio, duración (60 o 90 minutos), modalidad (`presencial` o `virtual`), aula física sugerida o enlace Google Meet (`https://meet.google.com/upt-epis-...`), y asigna el aforo reglamentario inmutable según RN-05 (10 para presencial, 20 para virtual). |
| **Fase 2: Ingreso de parámetros, validación de reglas de aforo y antelación** | |
| **3.** El mentor selecciona el tema silábico, especifica la fecha y hora programada, confirma la modalidad, verifica los cupos reglamentarios y hace clic en el botón `"Verificar y Publicar"`. | **4.** En `OfferPublishView.tsx`, se invoca `validateOfferPayload(payload)`. Si la sintaxis es válida, en `offerService.ts` (`ApiOfferAdapter.publishOffer`) se despacha `POST /api/v1/offers` con el payload `PublishOfferPayload` adjuntando el encabezado `Authorization: Bearer <jwt_token>`. En `endpoints/offers.py`, el controlador extrae la identidad del llamante mediante `_extract_caller_and_admin_status(authorization, payload.mentor_email)`. El controlador delega a `offer_service.OfferService.publish_offer(db, payload, caller_email, is_admin)`. El servicio valida: 1) que `caller_email == payload.mentor_email` o `is_admin == True` (RN-01), 2) que el mentor cumpla mérito académico en `usuario_roles` y `perfiles_academicos` con `ciclo_actual >= 7` mediante `validate_mentor_eligibility(db, email)` (RN-03), 3) que `fecha_inicio > now_utc + timedelta(hours=24)` mediante `calculate_advance_hours(payload.fecha_inicio)` (RN-04), y 4) que `aforo_maximo == 10` para presencial o `== 20` para virtual (RN-05). (Si faltan campos obligatorios o la sintaxis es inválida en cliente o Pydantic, salta a E001). (Si la fecha de inicio es menor o igual a 24 horas de antelación respecto a UTC now, salta a E002). (Si el aforo no corresponde estrictamente al estándar institucional de 10 o 20 cupos, salta a E003). (Si el usuario no cuenta con acreditación de mentor o su ciclo es menor a VII, salta a E004). (Si existe discrepancia entre la identidad del token y el correo del mentor, salta a E005). |
| **Fase 3: Persistencia transaccional de la oferta y confirmación en cliente** | |
| **5.** El mentor espera la confirmación visual en el botón que presenta un indicador circular de procesamiento y el estado `isSubmitting = true`. | **6.** En `offer_service.py`, al validar todos los criterios normativos, se genera el identificador unívoco de sesión `code = f"SES-{_session_counter}"`, se instancia la entidad ORM `sesion_db = SesionMentoria(codigo_sesion=code, mentor_email=effective_email, id_asignatura=payload.id_asignatura, id_tema=payload.id_tema, fecha_inicio=start_dt, duracion_minutos=payload.duracion_minutos, modalidad=payload.modalidad, aforo_maximo=expected_capacity, espacio_asignado=payload.espacio_asignado, notas_adicionales=payload.notas_adicionales, estado="PUBLICADA")`, se ejecuta `db.add(sesion_db)`, se confirma la transacción mediante `db.commit()` y se refresca la entidad con `db.refresh(sesion_db)`. El backend retorna HTTP 201 Created serializando `PublishOfferResponse`. En `OfferPublishView.tsx`, se limpia el formulario, se invoca el callback `onOfferPublished(response)` para sincronizar la cartelera, y se despliega una tarjeta de confirmación en color verde con el código generado de sesión (e.g. `SES-1004`), el espacio asignado y el botón `"Ver en Mis Sesiones"`. |

##### Flujos de Excepción

##### Flujo de excepción E001: Campos obligatorios incompletos o sintaxis inválida
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `validateOfferPayload` en cliente o el validador Pydantic `PublishOfferPayload` en `endpoints/offers.py` detecta omisión de campos requeridos (e.g. tema curricular o fecha ausente). Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: Todos los campos de la sesión son obligatorios.")`.<br><br>En `OfferPublishView.tsx`, se capturan los errores y se resaltan los campos observados con borde en color rojo y texto explicativo. |
| **E001-1.2** Corrige los campos observados completando los datos requeridos. | **E001-1.3** Rehabilita el botón `"Verificar y Publicar"` y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Incumplimiento de antelación mínima de 24 horas a T-24h
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, `offer_service.py` calcula `advance_hours = calculate_advance_hours(payload.fecha_inicio)`. Al constatar que `advance_hours <= 24.0`, lanza `HTTPException(status_code=400, detail="Infracción de RN-04: Toda mentoría debe publicarse con una antelación superior a 24 horas respecto al inicio de la sesión para garantizar la confirmación de quórum.")`.<br><br>En `OfferPublishView.tsx`, se despliega un panel de advertencia en color rojo destacando que no se permite publicar sesiones con menos de 24 horas de margen para garantizar la convocatoria de estudiantes. Presenta el botón `<button onClick={handleAdjustDate}>Ajustar Fecha</button>`. |
| **E002-1.2** Hace clic en el botón "Ajustar Fecha". | **E002-1.3** Asigna el foco al selector de fecha y hora, sugiriendo una fecha válida posterior a 24 horas, y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Aforo reglamentario no conforme según modalidad
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 4 del Flujo Normal, `offer_service.py` detecta que `payload.aforo_maximo` no coincide con el estándar inmutable de RN-05 (`10` cupos para presencial o `20` para virtual). Lanza `HTTPException(status_code=400, detail="Infracción de RN-05: El aforo reglamentario para la modalidad presencial debe ser exactamente 10 estudiantes.")`.<br><br>En `OfferPublishView.tsx`, se despliega un mensaje de error en color rojo junto al campo de vacantes indicando el límite reglamentario. |
| **E003-1.2** Ajusta el número de vacantes al valor reglamentario exacto (10 en presencial o 20 en virtual). | **E003-1.3** Actualiza el valor en el estado del componente y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E004: Mentor no elegible por ciclo insuficiente o falta de rol acreditado
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 4 del Flujo Normal, `validate_mentor_eligibility(db, effective_email)` en `offer_service.py` consulta las tablas `usuario_roles` y `perfiles_academicos`. Si el usuario no tiene rol `mentor` activo o su ciclo es menor a VII (infracción de RN-03), lanza `HTTPException(status_code=403, detail="Infracción de RN-03: Solo los estudiantes habilitados con rol de mentor (ciclo >= VII) pueden publicar ofertas de mentoría.")`.<br><br>En `OfferPublishView.tsx`, se despliega una alerta roja indicando que su perfil no cumple los requisitos académicos de mentoría. |
| **E004-1.2** Hace clic en el botón "Revisar Perfil". | **E004-1.3** Redirige al usuario hacia el módulo de perfil académico (`CUS-005`) y finaliza el caso de uso. |

##### Flujo de excepción E005: Suplantación de identidad o discrepancia de credenciales del mentor
| Usuario | Sistema |
|---|---|
| | **E005-1.1** En el paso 4 del Flujo Normal, en `endpoints/offers.py` y `offer_service.py` se compara `caller_email` extraído criptográficamente del token JWT contra `payload.mentor_email`. Si no coinciden y el llamante no es administrador (infracción de RN-01), lanza `HTTPException(status_code=403, detail="No tiene autorización para publicar ofertas en nombre de otro usuario.")`.<br><br>En `OfferPublishView.tsx`, se captura el error 403 y se muestra una alerta roja de seguridad institucional. |
| **E005-1.2** Hace clic en el botón "Sincronizar Credenciales". | **E005-1.3** Recarga la identidad de la sesión activa en el formulario y retorna al paso 3 del Flujo Normal de Eventos. |

#### CUS-008 - Consultar disponibilidad de espacios y recursos

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-008** (CUS-008) |
| **Nombre** | Consultar disponibilidad de espacios físicos y aulas de la EPIS |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-009 (Aprovisionamiento automatizado de infraestructura), RF-010 (Procesamiento de cronogramas y horarios institucionales); RN-06 (Prevención de colisión horaria de espacios), RN-07 (Horario operativo institucional 08:00 - 20:00) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los mentores y administradores consultar en tiempo real la disponibilidad de aulas físicas, laboratorios y salas de estudio de la EPIS-UPT antes de programar una sesión presencial. El frontend `OfferPublishView.tsx` invoca a `offerService.ts` despachando una petición `GET /api/v1/offers/spaces/availability` con parámetros de fecha y rango horario. El backend `aplicacion/backend/app/api/v1/endpoints/offers.py` delega a `app/services/offer_service.py`, el cual valida que la franja horaria se sitúe estrictamente dentro del horario operativo de la universidad (08:00 a 20:00 horas conforme a RN-07) y consulta las sesiones activas en `sesiones_mentoria` junto con el cronograma académico institucional. Retorna un listado de espacios disponibles con aforo y equipamiento, o sugiere alternativas de modalidad virtual si los espacios físicos se encuentran saturados. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-04: Planificación, Espacios y Agendamiento)<br>Manual de Uso de Infraestructura y Laboratorios EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/OfferPublishView.tsx` (Subcomponente de consulta de aulas)<br>`aplicacion/frontend/src/services/offerService.ts` (`OfferService.checkSpaceAvailability`)<br>`aplicacion/backend/app/api/v1/endpoints/offers.py` (`GET /api/v1/offers/spaces/availability`)<br>`aplicacion/backend/app/services/offer_service.py` (`OfferService.check_space_availability`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Usuario autenticado con token JWT institucional activo.<br>2. Catálogo institucional de aulas físicas y laboratorios registrado en el sistema.<br>3. Fecha de consulta fijada en día hábil académico universitario. |
| **PostCondiciones** | 1. Respuesta JSON generada con la nómina de aulas libres, aforos máximos y recursos audiovisuales disponibles.<br>2. Ninguna mutación destructiva o bloqueo persistente generado en base de datos (operación de lectura idempotente).<br>3. Despliegue interactivo en la interfaz cliente para selección de aula por parte del usuario. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Definición de criterios temporales y despacho de consulta** | |
| **1.** El mentor selecciona la fecha proyectada y la franja horaria (hora de inicio y hora de fin) en el selector de espacios de `OfferPublishView.tsx` y hace clic en `"Consultar Aulas Disponibles"`. | **2.** En `offerService.ts`, se valida que la franja horaria se encuentre dentro de la jornada universitaria institucional de 08:00 a 20:00 horas (RN-07). Despacha una petición `GET /api/v1/offers/spaces/availability?date=...&start_time=...&end_time=...`. En `offers.py`, el controlador valida los parámetros y delega a `offer_service.py`. (Si el horario ingresado se encuentra fuera del rango institucional de 08:00 a 20:00, salta a E001). |
| **Fase 2: Verificación de ocupación en base de datos y renderización de resultados** | |
| **3.** El mentor espera la respuesta mientras el componente visualiza un indicador de carga en color azul institucional. | **4.** En `offer_service.py`, se ejecuta una consulta para excluir aulas con sesiones activas en ese bloque: `SELECT a.id, a.codigo, a.capacidad, a.equipamiento FROM aulas a WHERE a.activa = true AND a.id NOT IN (SELECT aula_id FROM sesiones_mentoria WHERE fecha = :fecha AND NOT (hora_fin <= :start OR hora_inicio >= :end) AND estado IN ('PUBLICADA', 'CONFIRMADA'))`. Retorna HTTP 200 con la lista de aulas libres. En cliente, `OfferPublishView.tsx` renderiza una cuadrícula de tarjetas de aulas indicando aforo, ubicación y equipamiento. (Si todas las aulas físicas se encuentran ocupadas en ese bloque, salta a A001). (Si el repositorio de infraestructura reporta falla de comunicación, salta a E002). |
| **5.** El mentor hace clic en el aula física deseada y presiona el botón `"Asignar Aula a la Oferta"`. | **6.** El componente asigna el identificador del aula al formulario de publicación, actualiza el indicador visual en color verde con el texto *"Aula reservada provisionalmente"* y habilita el avance del flujo de publicación. |

##### Flujos Alternativos

##### Flujo alternativo A001: Aulas físicas agotadas con sugerencia de modalidad virtual
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 4 del Flujo Normal, la consulta retorna cero aulas libres para el horario solicitado. | **A001-1.2** En `OfferPublishView.tsx`, se despliega un panel informativo en color ámbar: *"Todas las aulas físicas se encuentran ocupadas en la franja horaria seleccionada. Se sugiere cambiar a Modalidad Virtual o modificar la hora de inicio"*. Presenta el botón `<button onClick={handleSwitchToVirtual}>Cambiar a Modalidad Virtual</button>` y el botón `<button onClick={handleAdjustTime}>Modificar Horario</button>`. |
| **A001-1.3** El mentor hace clic en el botón "Cambiar a Modalidad Virtual". | **A001-1.4** El sistema conmuta la modalidad de la sesión a `VIRTUAL`, habilita el campo para enlace de Google Meet, actualiza el límite de aforo a 20 estudiantes (RN-05) y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Horario fuera de la jornada institucional
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `offer_service.py` comprueba que la hora de inicio es anterior a las 08:00 o la hora de fin posterior a las 20:00 (infracción de RN-07). Lanza `HTTPException(status_code=400, detail="OPERATIONAL_HOURS_VIOLATION: El servicio de infraestructura opera estrictamente entre las 08:00 y las 20:00 horas.")`.<br><br>En `OfferPublishView.tsx`, se captura el error y se muestra una advertencia en color rojo indicando que la universidad no permite el uso de aulas físicas fuera de la jornada reglamentaria. |
| **E001-1.2** Modifica la franja horaria seleccionando un horario dentro de las 08:00 y 20:00. | **E001-1.3** Actualiza los valores en el selector y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Falla de conexión con el repositorio de infraestructura
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, la consulta relacional hacia el catálogo de aulas sufre timeout o interrupción de conexión. Lanza `HTTPException(status_code=503, detail="INFRASTRUCTURE_UNAVAILABLE: No se pudo verificar la disponibilidad de espacios físicos. Intente nuevamente en unos minutos.")`.<br><br>En `OfferPublishView.tsx`, se muestra un mensaje de alerta en color rojo indicando la indisponibilidad temporal del servicio. Presenta el botón `<button onClick={handleRetryCheck}>Reintentar Consulta</button>`. |
| **E002-1.2** Hace clic en el botón "Reintentar Consulta". | **E002-1.3** Dispara nuevamente la petición `GET /api/v1/offers/spaces/availability` y retorna al paso 1 del Flujo Normal de Eventos. |


---

### MOD-03: Perfil del Mentor y Plan de Aprendizaje

#### CUS-005 - Gestionar perfil formativo y disponibilidad horaria

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-005** (CUS-005) |
| **Nombre** | Gestionar perfil académico formativo y matriz de disponibilidad horaria semanal |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-004 (Configuración de perfil formativo y matriz horaria); RN-03 (Requisitos académicos de mentor: ciclo >= V y promedio), RN-04 (Antelación de planificación) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Coordinador de Carrera |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los mentores configurar su reseña académica, áreas de competencia disciplinar y su matriz semanal de disponibilidad horaria (lunes a sábado de 08:00 a 20:00) a través del componente cliente `ProfileAvailabilityView.tsx` y el servicio `profileService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/profiles.py` y `app/services/profile_service.py` procesan las peticiones `GET /api/v1/profiles/me` y `PUT /api/v1/profiles/me`, validando los datos con Pydantic (`ProfileUpdateRequest`), verificando que el usuario pertenezca al quinto ciclo académico o superior, y persistiendo de forma atómica en las entidades ORM `PerfilAcademico` y `DisponibilidadHoraria` (`app/models/profile.py`). Las franjas horarias registradas son utilizadas posteriormente por el motor de recomendaciones y el validador de ofertas para evitar traslapes. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-02: Gestión Curricular y Perfiles Académicos)<br>Plan Curricular de la Carrera Profesional de Ingeniería de Sistemas UPT |
| **Anexos** | `aplicacion/frontend/src/components/ProfileAvailabilityView.tsx`<br>`aplicacion/frontend/src/services/profileService.ts` (`ProfileService`, `ApiProfileAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/profiles.py` (`GET /api/v1/profiles/me`, `PUT /api/v1/profiles/me`, `POST /api/v1/profiles/availability`)<br>`aplicacion/backend/app/services/profile_service.py` (`ProfileService.get_profile`, `ProfileService.update_profile`, `ProfileService.save_availability`)<br>`aplicacion/backend/app/models/profile.py` (`PerfilAcademico`, `DisponibilidadHoraria`), `app/models/curriculum.py` (`Curso`) |
| **Precondiciones** | 1. Usuario con sesión institucional activa y rol `UserRole.mentor` verificado en el token JWT.<br>2. El estudiante mentor se encuentra matriculado en el semestre lectivo en curso y cumple el requisito de ciclo >= V.<br>3. Catálogo de cursos y asignaturas filtro activo en base de datos. |
| **PostCondiciones** | 1. Registros actualizados en las tablas físicas `perfiles_academicos` y `disponibilidad_horaria`.<br>2. Transacción confirmada en PostgreSQL y matriz horaria serializada para el motor de recomendación.<br>3. Despliegue de notificación de éxito en la interfaz y actualización del perfil en caché del frontend. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del perfil académico y visualización de la matriz horaria** | |
| **1.** El mentor hace clic en la pestaña `"Mi Perfil y Disponibilidad"` en `ProfileAvailabilityView.tsx`. | **2.** En `profileService.ts`, se despacha la petición `GET /api/v1/profiles/me` con la cabecera `Authorization: Bearer <token>`. En `profiles.py`, se extrae el correo del claim `sub` y `profile_service.py` ejecuta `SELECT p.*, d.* FROM perfiles_academicos p LEFT JOIN disponibilidad_horaria d ON p.id = d.perfil_id WHERE p.usuario_id = :uid`. Retorna HTTP 200 con el perfil, materias de dominio y bloques horarios semanales. `ProfileAvailabilityView.tsx` renderiza el formulario con biografía, materias acreditadas y una matriz interactiva semanal (lunes a sábado, bloques de una hora de 08:00 a 20:00). |
| **Fase 2: Edición de datos formativos y selección de bloques de disponibilidad** | |
| **3.** El mentor actualiza su biografía pedagógica, selecciona o deselecciona las asignaturas que domina, y hace clic sobre los bloques horarios en la cuadrícula semanal para alternar su estado entre disponible (resaltado en color verde) y no disponible (en color neutro). | **4.** En `ProfileAvailabilityView.tsx`, se actualiza el estado local `availabilitySlots`. El mentor presiona el botón `"Guardar Cambios y Disponibilidad"`. El componente valida que la biografía no exceda 500 caracteres y que se haya marcado al menos un bloque horario semanal. (Si no se selecciona ningún bloque de disponibilidad en toda la semana, salta a E001). (Si la biografía excede el límite de caracteres o contiene caracteres inválidos, salta a E002). |
| **Fase 3: Persistencia transaccional de disponibilidad y perfil** | |
| **5.** El mentor espera la confirmación visual mientras el botón muestra un indicador circular de guardado. | **6.** En `profileService.ts`, se despacha `PUT /api/v1/profiles/me` con el payload `ProfileUpdateRequest`. En `profiles.py`, `profile_service.py` inicia una transacción ACID con `db.begin()`. Actualiza `perfiles_academicos`, elimina los bloques horarios previos en `disponibilidad_horaria` para ese perfil e inserta los nuevos registros `(perfil_id, dia_semana, hora_inicio, hora_fin)`. Ejecuta `db.commit()` y retorna HTTP 200 con el perfil actualizado. `ProfileAvailabilityView.tsx` despliega una alerta flotante en color verde: *"Perfil y disponibilidad horaria actualizados exitosamente"*. (Si ocurre un conflicto de concurrencia o violación de clave única en base de datos, salta a E003). |

##### Flujos de Excepción

##### Flujo de excepción E001: Matriz de disponibilidad horaria semanal vacía
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el validador en `ProfileAvailabilityView.tsx` o `profile_service.py` comprueba que el conjunto de bloques horarios seleccionados está vacío (`len(slots) == 0`). Lanza `HTTPException(status_code=400, detail="EMPTY_SCHEDULE: Debe seleccionar al menos un bloque horario semanal de disponibilidad para ofrecer mentorías.")`.<br><br>En `ProfileAvailabilityView.tsx`, se resalta la cuadrícula horaria con un borde en color rojo y se despliega una advertencia en color ámbar solicitando marcar al menos una hora disponible. |
| **E001-1.2** Hace clic sobre al menos un bloque horario en la cuadrícula interactiva. | **E001-1.3** Conmuta el bloque a disponible (color verde), rehabilita el botón `"Guardar Cambios"` y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Biografía o formato de enlaces no válido
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, Pydantic detecta que el campo biografía excede 500 caracteres o contiene scripts no autorizados. Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: La reseña formativa no debe exceder 500 caracteres ni contener etiquetas HTML.")`.<br><br>En `ProfileAvailabilityView.tsx`, se resalta el cuadro de texto de biografía en color rojo indicando el error de validación. |
| **E002-1.2** Modifica el texto ajustándolo al límite permitido de caracteres. | **E002-1.3** Actualiza el contador de caracteres en la interfaz y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Conflicto de concurrencia al actualizar perfil
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 6 del Flujo Normal, una sesión concurrente modifica el mismo perfil provocando un conflicto de versión en base de datos. `profile_service.py` ejecuta `db.rollback()` y lanza `HTTPException(status_code=409, detail="CONCURRENCY_CONFLICT: El perfil fue actualizado desde otra sesión. Se recargarán los datos más recientes.")`.<br><br>En `ProfileAvailabilityView.tsx`, se captura el error 409 y se despliega un aviso en color ámbar. Presenta el botón `<button onClick={fetchProfile}>Recargar Perfil</button>`. |
| **E003-1.2** Hace clic en el botón "Recargar Perfil". | **E003-1.3** Invoca nuevamente `GET /api/v1/profiles/me`, actualiza el formulario con el estado más reciente y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-021 - Explorar catálogo curricular de asignaturas filtro

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-021** (CUS-021) |
| **Nombre** | Explorar catálogo curricular jerárquico de asignaturas y materias críticas |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-005 (Gestión del catálogo de asignaturas y temarios); RN-11 (Priorización y catálogo oficial de asignaturas filtro EPIS) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado, Estudiante Mentor, Coordinador Curricular |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los estudiantes mentoreados y mentores navegar interactivamente por la malla curricular oficial de la EPIS-UPT a través del componente cliente `CurriculumCatalogView.tsx` y el servicio `curriculumService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/curriculum.py` y `app/services/curriculum_service.py` proporcionan consultas estructuradas por carrera (`Carrera`), ciclo académico (I al X), curso (`Curso`) y temas de aprendizaje silábico (`TemaCurricular`), destacando visualmente las asignaturas identificadas institucionalmente como "materias filtro" (`es_filtro = true`, tales como Algoritmos, Estructuras de Datos, Base de Datos y Programación Orientada a Objetos). Desde cada tema curricular, el mentoreado puede consultar directamente las ofertas de mentoría activas o solicitar la apertura de una sesión por demanda. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-02: Gestión Curricular y Perfiles Académicos)<br>Malla Curricular Oficial de Ingeniería de Sistemas UPT |
| **Anexos** | `aplicacion/frontend/src/components/CurriculumCatalogView.tsx`<br>`aplicacion/frontend/src/services/curriculumService.ts` (`CurriculumService`, `ApiCurriculumAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/curriculum.py` (`GET /api/v1/curriculum/careers`, `GET /api/v1/curriculum/courses`, `GET /api/v1/curriculum/courses/{id}/topics`)<br>`aplicacion/backend/app/services/curriculum_service.py` (`CurriculumService.get_courses`, `CurriculumService.get_topics`)<br>`aplicacion/backend/app/models/curriculum.py` (`Carrera`, `Curso`, `TemaCurricular`) |
| **Precondiciones** | 1. Usuario con sesión institucional iniciada en la plataforma.<br>2. Malla curricular y temarios silábicos cargados y versionados en la base de datos PostgreSQL.<br>3. Identificación institucional de cursos filtro debidamente clasificada en la columna `es_filtro`. |
| **PostCondiciones** | 1. Despliegue interactivo del catálogo jerárquico de asignaturas y temas silábicos en la interfaz.<br>2. Consulta idempotente de sólo lectura ejecutada sin mutaciones en base de datos.<br>3. Posibilidad de derivación directa hacia la reserva de mentoría (CUS-004) o registro de demanda (CUS-003). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Navegación por ciclo académico y selección de asignatura** | |
| **1.** El usuario hace clic en el enlace `"Catálogo Curricular"` del menú de navegación principal en `CurriculumCatalogView.tsx`. | **2.** En `curriculumService.ts`, se despacha `GET /api/v1/curriculum/courses`. En `curriculum.py`, `curriculum_service.py` ejecuta `SELECT c.*, count(t.id) as total_temas FROM cursos c LEFT JOIN temas_curriculares t ON c.id = t.curso_id WHERE c.activo = true GROUP BY c.id ORDER BY c.ciclo, c.nombre`. Retorna HTTP 200 con la lista completa de cursos. `CurriculumCatalogView.tsx` renderiza las asignaturas agrupadas por ciclo académico (del ciclo I al X), destacando las asignaturas filtro con una insignia visual en color azul institucional con la leyenda *"Materia Filtro Prioritaria"*. (Si el repositorio curricular sufre indisponibilidad o timeout, salta a E001). |
| **Fase 2: Búsqueda y filtrado interactivo de cursos** | |
| **3.** El usuario introduce el nombre de una materia o código en el cuadro de búsqueda `"Buscar asignatura o tema"` y aplica el filtro por ciclo. | **4.** En `CurriculumCatalogView.tsx`, se filtra reactivamente la nómina de cursos en el estado de la vista. El usuario hace clic en la tarjeta de la asignatura de su interés para inspeccionar su estructura temática. (Si ningún curso coincide con los términos de búsqueda ingresados, salta a A001). |
| **Fase 3: Despliegue de temarios silábicos y vinculación con mentorías** | |
| **5.** El usuario hace clic sobre la tarjeta de un curso específico (e.g. Algoritmos y Estructuras de Datos). | **6.** En `curriculumService.ts`, se despacha `GET /api/v1/curriculum/courses/{course_id}/topics`. El backend retorna los temas clasificados por unidad didáctica con número de semana, descripción y cantidad de ofertas activas. `CurriculumCatalogView.tsx` expande un panel acordeón desplegando la lista de temas silábicos, cada uno con el botón `"Ver Ofertas Disponibles"` y el botón `"Solicitar Demanda"`. |

##### Flujos Alternativos

##### Flujo alternativo A001: Búsqueda curricular sin coincidencias
| Usuario | Sistema |
|---|---|
| **A001-1.1** El usuario introduce en el paso 3 un término de búsqueda que no produce coincidencias en el catálogo. | **A001-1.2** En `CurriculumCatalogView.tsx`, se ocultan las tarjetas y se renderiza un panel centrado con un ícono informativo y el texto: *"No se encontraron asignaturas o temas que coincidan con la búsqueda. Intente con otro término o seleccione un ciclo específico"*. Presenta el botón `<button onClick={handleResetFilter}>Restablecer Filtros</button>`. |
| **A001-1.3** Hace clic en el botón "Restablecer Filtros". | **A001-1.4** Limpia el cuadro de búsqueda, muestra nuevamente todas las asignaturas por ciclo y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Falla de conexión con el repositorio curricular
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, la consulta hacia las tablas `cursos` y `temas_curriculares` sufre una pérdida de conexión en PostgreSQL. Lanza `HTTPException(status_code=503, detail="CURRICULUM_SERVICE_UNAVAILABLE: El repositorio curricular no se encuentra disponible temporalmente. Reintente en unos instantes.")`.<br><br>En `CurriculumCatalogView.tsx`, se captura el error 503 y se despliega un panel de alerta en color ámbar indicando la imposibilidad de cargar la malla curricular. Presenta el botón `<button onClick={fetchCurriculum}>Reintentar Carga</button>`. |
| **E001-1.2** Hace clic en el botón "Reintentar Carga". | **E001-1.3** Dispara nuevamente la petición `GET /api/v1/curriculum/courses` y retorna al paso 1 del Flujo Normal de Eventos. |


---

### MOD-04: Demanda y Recomendaciones Personalizadas

#### CUS-002 - Explorar recomendaciones personalizadas Top-k

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-002** (CUS-002) |
| **Nombre** | Explorar cartelera inteligente de recomendaciones de mentoría Top-k |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-006 (Inferencia de recomendaciones y ranking Top-k); RN-04 (Ventana de antelación mínima de 24 horas), RN-11 (Ponderación algorítmica de asignaturas filtro) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 03 - Sprint 04 |
| **Descripción** | Permite a los estudiantes mentoreados visualizar una cartelera adaptativa de sesiones de mentoría clasificadas según su relevancia académica individual mediante el componente cliente `RecommendationFeedView.tsx` y el servicio `recommendationService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/recommendations.py` procesa la petición `GET /api/v1/recommendations/top-k?limit=6`, delegando al servicio `app/services/recommendation_service.py`. El motor analiza el vector de intereses y asignaturas matriculadas del estudiante extraído de `perfiles_academicos`, computa la similitud de cosenos respecto a las sesiones en estado `PUBLICADA` con antelación mayor a 24 horas (`fecha_inicio > now_utc + 24h`, RN-04), aplica bonificaciones para materias filtro (`es_filtro = true`, RN-11) y penaliza sesiones con aforo próximo a agotarse. Retorna una nómina ordenada de las mejores k recomendaciones serializadas en el modelo Pydantic `TopKRecommendationResponse`. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-03: Motor de Recomendación Inteligente EdRecSys)<br>Algoritmos de Recomendación Basados en Contenido y Filtrado Híbrido |
| **Anexos** | `aplicacion/frontend/src/components/RecommendationFeedView.tsx`<br>`aplicacion/frontend/src/services/recommendationService.ts` (`RecommendationService`, `ApiRecommendationAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/recommendations.py` (`GET /api/v1/recommendations/top-k`)<br>`aplicacion/backend/app/services/recommendation_service.py` (`RecommendationService.get_top_k_recommendations`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`), `app/models/profile.py` (`PerfilAcademico`), `app/models/curriculum.py` (`Curso`, `TemaCurricular`) |
| **Precondiciones** | 1. Estudiante mentoreado autenticado con token JWT institucional activo en `localStorage`.<br>2. Al menos una sesión de mentoría en estado `PUBLICADA` con antelación superior a 24 horas y vacantes disponibles.<br>3. Registro de perfil académico o cursos matriculados en la base de datos. |
| **PostCondiciones** | 1. Payload JSON serializado con las k sesiones más afines y sus puntuaciones de compatibilidad retornadas al frontend.<br>2. Consulta de lectura sin efectos colaterales persistentes ni mutaciones de datos en PostgreSQL.<br>3. Despliegue de la cartelera interactiva con tarjetas informativas y botones de reserva activados. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso a la cartelera y solicitud de recomendaciones Top-k** | |
| **1.** El mentoreado accede a la página principal de la plataforma en `RecommendationFeedView.tsx`. | **2.** En `recommendationService.ts`, se despacha `GET /api/v1/recommendations/top-k?limit=6` incluyendo el token Bearer institucional. En `recommendations.py`, el controlador extrae el UUID del usuario del token JWT y delega a `recommendation_service.py`. El servicio recupera el perfil académico del estudiante y sus materias matriculadas. (Si el estudiante no registra historial ni materias configuradas, salta a A001). (Si el motor de recomendación sufre una excepción de cálculo o timeout, salta a E001). |
| **Fase 2: Ejecución del algoritmo de emparejamiento y ordenamiento de compatibilidad** | |
| **3.** El usuario visualiza un esqueleto animado de tarjetas mientras se calculan las recomendaciones. | **4.** En `recommendation_service.py`, se recuperan las sesiones en estado `PUBLICADA` con `fecha_inicio > now_utc + timedelta(hours=24)` y `occupied_seats < aforo_maximo`. Para cada oferta, se calcula el puntaje ponderado: $Score = 0.5 	imes SimilitudCursos + 0.3 	imes FactorFiltro + 0.2 	imes UrgenciaTemporal$. Se ordenan de forma descendente y se toman las primeras 6 ofertas. Retorna HTTP 200 con el payload `TopKRecommendationResponse`. En cliente, `RecommendationFeedView.tsx` renderiza las tarjetas con: nombre del tema curricular, nombre de la asignatura, fecha y hora de la sesión, modalidad (Presencial/Virtual con aula o enlace), número de vacantes restantes y un distintivo en color azul institucional indicando el porcentaje de compatibilidad (e.g. *"95% de afinidad"*). (Si no existen ofertas activas para sus materias, salta a A002). |
| **Fase 3: Selección de sesión para reserva de cupo** | |
| **5.** El mentoreado revisa las tarjetas de recomendación y hace clic en el botón `"Reservar Cupo"` de la sesión de su preferencia. | **6.** En `RecommendationFeedView.tsx`, se captura el identificador de la sesión seleccionada y se abre el componente modal `BookingModalView.tsx`, transfiriendo el flujo a la especificación técnica de reserva formal de cupo (CUS-004). |

##### Flujos Alternativos

##### Flujo alternativo A001: Estudiante nuevo sin historial académico (Fallback por popularidad)
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 2 del Flujo Normal, `recommendation_service.py` detecta que el estudiante no tiene historial académico ni materias configuradas en su perfil. | **A001-1.2** El servicio conmuta automáticamente a la estrategia de respaldo ("Cold Start"): ejecuta una consulta para seleccionar las sesiones de mentoría más populares y con mayor demanda en asignaturas filtro generales de los primeros ciclos (`es_filtro = true`). |
| **A001-1.3** El estudiante visualiza las tarjetas de oferta acompañadas de una insignia informativa en color ámbar: *"Ofertas destacadas para estudiantes de primeros ciclos"*. | **A001-1.4** El sistema presenta el botón `<button onClick={handleConfigureProfile}>Configurar Mis Materias</button>` para personalizar futuras recomendaciones y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo alternativo A002: Cartelera vacía por ausencia de sesiones disponibles
| Usuario | Sistema |
|---|---|
| **A002-1.1** En el paso 4 del Flujo Normal, la consulta de sesiones publicadas retorna cero registros con vacantes disponibles. | **A002-1.2** En `RecommendationFeedView.tsx`, se despliega un panel centralizado con un ícono ilustrativo en color azul institucional y el texto: *"No hay sesiones de mentoría programadas actualmente para tus materias. Puedes solicitar la apertura de un tema registrando tu demanda académica"*. Presenta el botón `<button onClick={handleOpenDemandModal}>Registrar Solicitud por Demanda</button>`. |
| **A002-1.3** El estudiante hace clic en el botón "Registrar Solicitud por Demanda". | **A002-1.4** El sistema abre el modal de registro de demanda académica (CUS-003) y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Error de cómputo en el motor de recomendación
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, el servicio `recommendation_service.py` encuentra una falla de serialización de vectores o un timeout interno en base de datos. Lanza `HTTPException(status_code=500, detail="RECOMMENDER_ENGINE_ERROR: Ocurrió un error al procesar las recomendaciones personalizadas.")`.<br><br>En `RecommendationFeedView.tsx`, se captura el error 500 y se despliega un panel de advertencia en color rojo. Presenta el botón `<button onClick={fetchRecommendations}>Reintentar Cartelera</button>`. |
| **E001-1.2** Hace clic en el botón "Reintentar Cartelera". | **E001-1.3** Dispara nuevamente la petición `GET /api/v1/recommendations/top-k` y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-003 - Registrar solicitud de demanda académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-003** (CUS-003) |
| **Nombre** | Registrar solicitud de mentoría por demanda académica no atendida |
| **Tipo** | Obligatorio (   ) / Opcional ( X ) |
| **Requisito ID (RF)** | RF-007 (Banco de solicitudes por demanda académica); RN-04 (Antelación de planificación institucional), RN-11 (Priorización curricular de materias formativas filtro); RNF04, RNF09 |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`, Primario); Estudiante Mentor (`UserRole.mentor`, Secundario) |
| **Interacción** | Fase de Construcción / Iteración Sprint 03 - Sprint 04 (Actualización Post-Sprint 08 con Banco de Demanda) |
| **Descripción** | Permite a los estudiantes mentoreados canalizar una necesidad formativa insatisfecha hacia el banco institucional de solicitudes por demanda cuando no existan ofertas vigentes que atiendan un tema silábico de interés o cuando el aforo de las sesiones publicadas se encuentre totalmente agotado. La interacción se inicia mediante el componente modal accesible MentoringDemandModalView.tsx, desplegable desde el panel de lista vacía en RecommendationFeedView.tsx o desde la alerta de sobrecupo en BookingModalView.tsx. El estudiante selecciona una asignatura curricular formativa y una unidad o tema silábico específico, ingresando opcionalmente una justificación u observación pedagógica. La petición se procesa en bookingService.ts y se despacha hacia el endpoint POST /api/v1/bookings/requests en el controlador aplicacion/backend/app/api/v1/endpoints/bookings.py. El servicio booking_service.py valida la integridad de los datos, descarta la existencia de solicitudes duplicadas activas para el mismo estudiante y tema, e inserta el registro en la tabla física solicitudes_demanda (app/models/booking.py) con estado 'PENDIENTE' y folio institucional correlativo #DEM-{id}. La solicitud queda disponible de forma inmediata en el panel de mentores (MentorSessionsView.tsx, pestaña "Banco de Solicitudes por Demanda") para formular sesiones de mentoría dirigida. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v3.0 - MOD-04: Demanda y Recomendaciones Personalizadas)<br>Modelo de Gestión de Demanda Académica EPIS-UPT |
| **Anexos** | aplicacion/frontend/src/components/MentoringDemandModalView.tsx<br>aplicacion/frontend/src/components/RecommendationFeedView.tsx<br>aplicacion/frontend/src/components/BookingModalView.tsx<br>aplicacion/frontend/src/components/MentorSessionsView.tsx<br>aplicacion/frontend/src/services/bookingService.ts (BookingService, ApiBookingAdapter)<br>aplicacion/frontend/src/services/apiClient.ts (fetchCourses, fetchCourseDetail)<br>aplicacion/backend/app/api/v1/endpoints/bookings.py (POST /api/v1/bookings/requests, GET /api/v1/bookings/requests)<br>aplicacion/backend/app/services/booking_service.py (BookingService.create_demand_request)<br>aplicacion/backend/app/models/booking.py (SolicitudDemanda), app/models/curriculum.py (Asignatura, TemaConceptual) |
| **Precondiciones** | 1. Estudiante mentoreado autenticado con token JWT institucional activo en localStorage.<br>2. Catálogo oficial de asignaturas críticas y temarios silábicos disponible en la base de datos.<br>3. Consentimiento informado digital formalizado previamente bajo la Ley Nº 29733. |
| **PostCondiciones** | 1. Registro formal insertado en la tabla física solicitudes_demanda con estado 'PENDIENTE' y folio institucional correlativo #DEM-{id}.<br>2. Solicitud disponible de forma inmediata en el Banco de Solicitudes por Demanda de los mentores acreditados en MentorSessionsView.tsx.<br>3. Despliegue de confirmación en cliente con resumen de solicitud y retorno ordenado a la cartelera de mentorías. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura del formulario de demanda y carga del catálogo silábico** | |
| **1.** El mentoreado visualiza la ausencia de sesiones afines en `RecommendationFeedView.tsx` o un aviso de aforo colapsado en `BookingModalView.tsx`, y hace clic en el botón `"Registrar Solicitud por Demanda"`. | **2.** En `MentoringDemandModalView.tsx`, se abre la ventana modal con cabecera en color azul institucional y título `"📋 Registrar Solicitud de Mentoría por Demanda"`. El hook `useEffect` invoca `fetchCourses(true)` en `apiClient.ts` para obtener la lista de materias formativas. El sistema renderiza el selector de asignaturas y consulta automáticamente los temas silábicos de la primera materia mediante `fetchCourseDetail(id)`. (Si el modal es invocado desde una sesión específica con aforo agotado, salta a A001). (Si la consulta del catálogo curricular falla por pérdida de red, salta a E004). |
| **Fase 2: Selección temática, justificación pedagógica y validación de reglas** | |
| **3.** El mentoreado selecciona la asignatura deseada en la lista desplegable `"Asignatura Curricular"`, selecciona la unidad o tema de aprendizaje en `"Tema o Unidad Específica"`, redacta su justificación en el área de texto `"Observaciones o Justificación de Necesidad Formativa"` y presiona el botón `"Enviar Solicitud"`. | **4.** En `MentoringDemandModalView.tsx`, se valida que se hayan seleccionado identificadores positivos para la materia y el tema. Se activa el estado transicional `isSubmitting = true` con texto `"Registrando..."`. En `bookingService.ts`, se despacha una petición `POST /api/v1/bookings/requests` enviando el payload `{"id_asignatura": selectedCourseId, "id_tema": selectedTopicId, "observaciones": observaciones}` hacia el controlador `bookings.py`. El backend valida con Pydantic (`SolicitudDemandaCreate`) la integridad de los datos. En `booking_service.py`, se ejecuta una consulta para verificar que no exista una solicitud activa en estado `PENDIENTE` para el mismo estudiante y tema: `SELECT id_demanda FROM solicitudes_demanda WHERE estudiante_email = :email AND id_tema = :tid AND estado = 'PENDIENTE'`. (Si el mentoreado omite seleccionar la asignatura o el tema silábico, salta a E001). (Si la materia seleccionada no cuenta con temarios silábicos registrados, salta a E002). (Si el estudiante ya cuenta con una solicitud activa idéntica para ese mismo tema, salta a E003). (Si el mentoreado decide cancelar el registro o pulsa la tecla Escape, salta a A002). |
| **Fase 3: Registro transaccional en el banco de demanda y confirmación visual** | |
| **5.** El mentoreado observa el estado de procesamiento en pantalla con los controles temporalmente bloqueados. | **6.** En `booking_service.py`, se ejecuta la inserción relacional `INSERT INTO solicitudes_demanda (estudiante_email, id_asignatura, id_tema, observaciones, estado, created_at) VALUES (...)`. Se confirma la transacción con `db.commit()` y se retorna HTTP 201 Created con el payload `SolicitudDemandaResponse`. En cliente, `MentoringDemandModalView.tsx` oculta el formulario y conmuta al panel de confirmación de éxito con fondo blanco, círculo en color verde claro con marca de verificación en color verde oscuro, título `"¡Solicitud Registrada con Éxito!"` y el folio institucional `#DEM-{id}` asignado, explicando que los mentores acreditados podrán formular ofertas dirigidas. El usuario pulsa el botón `"Entendido"` para cerrar el diálogo modal y retornar a la cartelera. (Si ocurre un error interno en la base de datos durante la persistencia, salta a E004). |

##### Flujos Alternativos

##### Flujo alternativo A001: Invocación del modal desde alerta de aforo agotado en reserva con preselección
| Usuario | Sistema |
|---|---|
| **A001-1.1** En `BookingModalView.tsx`, el mentoreado constata que los cupos de una sesión de su interés se han agotado (`available_slots <= 0`) y hace clic en el botón de acción secundaria `"Registrar Solicitud por Demanda"`. | **A001-1.2** `BookingModalView.tsx` invoca el callback de apertura transfiriendo las propiedades `preselectedCourseId` y `preselectedTopicId` hacia `MentoringDemandModalView.tsx`. |
| **A001-1.3** El mentoreado observa que el modal se abre con la asignatura y el tema silábico de la sesión original ya preseleccionados en las listas desplegables. | **A001-1.4** El sistema bloquea las selecciones correspondientes, enfoca directamente el cuadro de texto `"Observaciones o Justificación de Necesidad Formativa"` y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo alternativo A002: Cancelación voluntaria del registro de demanda con botón Cancelar o tecla Escape
| Usuario | Sistema |
|---|---|
| **A002-1.1** El mentoreado hace clic en el botón `"Cancelar"`, pulsa el botón de cierre en la cabecera del modal o presiona la tecla `Escape` en su teclado. | **A002-1.2** `MentoringDemandModalView.tsx` captura el evento, cancela las peticiones asíncronas en curso y purga el estado local del formulario. |
| **A002-1.3** El mentoreado observa el cierre suave del cuadro de diálogo modal retornando el foco a la vista anterior. | **A002-1.4** El sistema desmonta la ventana modal del árbol de componentes y finaliza el caso de uso sin generar registros. |

##### Flujos de Excepción

##### Flujo de excepción E001: Formulario de solicitud incompleto por omisión de asignatura o tema
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el usuario presiona el botón `"Enviar Solicitud"` sin haber seleccionado una materia o un tema silábico (`selectedCourseId === 0` o `selectedTopicId === 0`). `MentoringDemandModalView.tsx` bloquea el envío y despliega un banner de alerta en color rojo con el mensaje: *"Por favor seleccione una asignatura y un tema curricular válido."*. |
| **E001-1.2** El estudiante selecciona la asignatura y el tema en las listas desplegables. | **E001-1.3** Oculta la alerta de error, rehabilita el botón de envío y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Asignatura formativa sin temarios silábicos disponibles en catálogo
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, tras seleccionar una asignatura, la consulta `fetchCourseDetail(id)` retorna una lista de temas vacía (`detail.temas.length === 0`). El selector de temas se deshabilita mostrando la opción: *"No hay temas registrados para esta materia"*, y el botón `"Enviar Solicitud"` se bloquea en color gris claro. |
| **E002-1.2** El estudiante cambia la selección hacia otra asignatura formativa que sí contenga temarios silábicos activos. | **E002-1.3** Carga reactivamente los temas disponibles, rehabilita el botón de acción y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Solicitud duplicada activa para el mismo estudiante y tema silábico
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 4 del Flujo Normal, `booking_service.py` localiza una tupla activa previa en `solicitudes_demanda` con el mismo correo y tema en estado `PENDIENTE`. Lanza `HTTPException(status_code=400, detail="Ya mantienes una solicitud activa registrada para este tema en el banco de demanda.")`.<br><br>En `bookingService.ts`, captura el error y propaga el mensaje hacia el modal. `MentoringDemandModalView.tsx` despliega una alerta en color ámbar explicando la preexistencia de la solicitud. Presenta el botón `"Entendido"`. |
| **E003-1.2** Hace clic en el botón "Entendido". | **E003-1.3** Cierra la ventana modal sin generar registros redundantes y finaliza el caso de uso sin generar registros. |

##### Flujo de excepción E004: Error de comunicación con el servicio de reservas y banco de demanda
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 2 o 6 del Flujo Normal, ocurre pérdida de enlace o indisponibilidad en el backend (`HTTP 500` o `HTTP 503`). `bookingService.ts` o `apiClient.ts` captura la excepción de red.<br><br>En `MentoringDemandModalView.tsx`, se restablece `isSubmitting = false` y se despliega un banner de alerta en color rojo: *"Error al registrar la solicitud por demanda."*. Presenta el botón `"Reintentar"`. |
| **E004-1.2** Hace clic en el botón "Reintentar". | **E004-1.3** Mantiene los datos redactados en el formulario y retorna al paso 1 del Flujo Normal de Eventos sin generar registros. |

##### Especificación Exhaustiva de Interfaz de Usuario y Comportamiento Visual

La interfaz de usuario del componente `MentoringDemandModalView.tsx` está diseñada bajo principios de usabilidad y accesibilidad WCAG 2.1 AA:
1. **Capa de Superposición (Overlay):** Fondo fijo con cobertura total de pantalla en color gris pizarra oscuro semitransparente con desenfoque de fondo (*backdrop blur*), bloqueando clics en elementos subyacentes.
2. **Contenedor Modal:** Cuadro de diálogo centralizado en color blanco puro con esquinas redondeadas, sombra pronunciada de elevación y diseño responsivo adaptativo con un ancho máximo estandarizado.
3. **Cabecera Institucional:** Barra superior en color azul institucional con tipografía en color blanco puro conteniendo el título `"📋 Registrar Solicitud de Mentoría por Demanda"`, subtítulo explicativo en color celeste grisáceo `"Caso de Uso CUS03 / RF07 — Banco Institucional EPIS UPT"` y botón de cierre en la esquina derecha con símbolo de aspa en color blanco puro.
4. **Párrafo Orientador:** Texto explicativo en color gris azulado detallando que si el estudiante no encuentra sesiones activas o las plazas están agotadas, puede registrar su necesidad para que mentores de ciclos superiores formulen ofertas específicas.
5. **Selectores Desplegables:** Campo de selección `"Asignatura Curricular"` con etiqueta en color gris oscuro y asterisco obligatorio en color rojo. Al cambiar de asignatura, el campo dependiente `"Tema o Unidad Específica"` se actualiza en tiempo real mostrando el código de unidad silábica y el nombre del tema.
6. **Área de Justificación Pedagógica:** Campo de texto multilínea con tres filas de altura, borde en color gris claro y texto de sugerencia (*placeholder*) en color gris tenue: `"Ej: Requiero nivelación en límites algebraicos y aplicaciones de derivadas para la próxima práctica calificada."`.
7. **Botones de Control:** En la parte inferior derecha, botón secundario `"Cancelar"` con fondo en color gris claro, borde gris y texto en gris oscuro; y botón principal de envío `"Enviar Solicitud"` con fondo en color azul institucional y texto en blanco puro (deshabilitado en color gris pizarra cuando los campos no están completos o mostrando `"Registrando..."` durante el despacho).
8. **Panel de Confirmación de Éxito:** Tras la persistencia exitosa, el modal transmuta a una tarjeta de felicitación con un círculo central en color verde claro conteniendo el símbolo de verificación en color verde oscuro, título en color verde bosque `"¡Solicitud Registrada con Éxito!"`, párrafo explicativo con el folio institucional en negrita `"#DEM-{id}"`, recuadro de detalles con fondo gris muy suave conteniendo el estado en color azul institucional, correo del solicitante y marca de tiempo UTC, y botón `"Entendido"` en color azul institucional.
9. **Accesibilidad WCAG 2.1 AA:** Diálogo modal con atributos `role="dialog"`, `aria-modal="true"` y `aria-labelledby="demand-modal-title"`. Cierre automático mediante la tecla `Escape` y navegación completa por teclado con tabulación accesible.

##### Criterios de Aceptación Formativos (Given-When-Then)

```gherkin
Escenario 1: Registro exitoso de solicitud de demanda académica desde cartelera vacía
  DADO QUE el estudiante mentoreado se encuentra autenticado en el sistema
  Y visualiza la cartelera de recomendaciones vacía o sin ofertas sobre su tema de interés en RecommendationFeedView
  CUANDO hace clic en el botón "Registrar Solicitud por Demanda"
  Y selecciona una asignatura crítica (ej. "Algoritmos y Estructuras de Datos") y un tema silábico específico
  Y redacta su justificación pedagógica presionando el botón "Enviar Solicitud"
  ENTONCES el sistema valida los datos y ejecuta POST /api/v1/bookings/requests
  Y persiste el registro en la tabla física solicitudes_demanda en estado "PENDIENTE" asignando un folio correlativo #DEM-{id}
  Y despliega en pantalla el panel de confirmación en color verde con los detalles de la solicitud registrada.
  Evidencia de Prueba: test_bookings.py::test_create_demand_request_success / MentoringDemandModalView.test.tsx

Escenario 2: Preselección automática ante redirección por aforo colapsado en reserva
  DADO QUE el mentoreado intenta reservar una sesión de mentoría en BookingModalView cuyo aforo se encuentra agotado (0 vacantes)
  CUANDO presiona el botón alternativo "Registrar Solicitud por Demanda"
  ENTONCES el sistema abre MentoringDemandModalView con la asignatura y el tema de la sesión agotada preseleccionados automáticamente
  Y enfoca directamente el cuadro de texto de justificación pedagógica
  Y permite al estudiante enviar la solicitud sin requerir rebuscar la materia en el catálogo.
  Evidencia de Prueba: BookingModalView.test.tsx / MentoringDemandModalView.test.tsx

Escenario 3: Bloqueo de envío ante campos obligatorios sin seleccionar
  DADO QUE el estudiante tiene abierto el modal de solicitud de demanda académica
  CUANDO no selecciona ninguna asignatura curricular o tema silábico válido
  Y presiona el botón "Enviar Solicitud"
  ENTONCES el componente bloquea la emisión de la petición HTTP
  Y despliega un banner de alerta en color rojo con el texto: "Por favor seleccione una asignatura y un tema curricular válido."
  Y mantiene los controles en pantalla sin registrar datos en la base de datos.
  Evidencia de Prueba: MentoringDemandModalView.test.tsx::test_validation_empty_fields

Escenario 4: Disponibilidad y visualización inmediata en el banco de solicitudes del portal del mentor
  DADO QUE una solicitud de demanda académica ha sido registrada exitosamente por un mentoreado
  CUANDO un estudiante mentor acreditado de ciclos superiores accede a su panel en MentorSessionsView
  Y hace clic en la pestaña "Banco de Solicitudes por Demanda (RF07)"
  ENTONCES el sistema consulta el endpoint GET /api/v1/bookings/requests
  Y despliega la tarjeta de la solicitud con el folio #DEM-{id}, código de curso, tema silábico y justificación
  Y presenta al mentor el botón para formular una nueva oferta de mentoría dirigida a cubrir dicha demanda.
  Evidencia de Prueba: test_bookings.py::test_list_demand_requests / MentorSessionsView.test.tsx
```


---

### MOD-05: Quórum, Confirmación y Cancelaciones

#### CUS-004 - Reservar cupo de mentoría académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-004** (CUS-004) |
| **Nombre** | Reservar cupo de mentoría académica con control de aforo y concurrencia |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-012 (Reserva de cupos con control de aforo y concurrencia; trazabilidad técnica hacia RF-002, RF-006, RF-013 y RF-014) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`), Administrador Institucional (`UserRole.administrador`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite formalizar una reserva provisional de cupo en estado `PENDIENTE_CONFIRMACION` mediante una petición `POST /api/v1/bookings/reserve` despachada desde el componente cliente `BookingModalView.tsx` hacia el controlador FastAPI `bookings.py`. El backend ejecuta validaciones de seguridad con `decode_access_token` en `app/core/security.py`, comprueba la vigencia del consentimiento legal con `ConsentService.get_consent_status`, adquiere el cerrojo en memoria `_booking_lock` y ejecuta una transacción en PostgreSQL bajo bloqueo pesimista de fila `SELECT ... FOR UPDATE OF sesiones_mentoria` con `SET LOCAL lock_timeout = '5.0s'`. Comprueba que `occupied_seats < sesion.aforo_maximo` (10 presencial / 20 virtual, RN-05) y la antelación mayor a 24 horas (`sesion.fecha_inicio > now_utc + 24h`, RN-04). Genera la entidad ORM `ReservaCupo` con código alfanuméricamente secuencial y hash criptográfico SHA-256 (`ticket_hash`), confirma la transacción con `db.commit()` y retorna el payload serializado `BookingResponse` (HTTP 201 Created). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Ley Nº 29733 de Protección de Datos Personales del Perú y D.S. Nº 003-2013-JUS |
| **Anexos** | `aplicacion/frontend/src/components/BookingModalView.tsx`<br>`aplicacion/frontend/src/components/RecommendationFeedView.tsx`<br>`aplicacion/frontend/src/services/bookingService.ts` (`BookingService`, `ApiBookingAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/reserve`)<br>`aplicacion/backend/app/services/booking_service.py` (`BookingService.reserve_seat`)<br>`aplicacion/backend/app/models/booking.py` (`ReservaCupo`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Token JWT institucional activo en `localStorage` firmado criptográficamente con claim `sub` conteniendo un correo institucional `@upt.pe`.<br>2. Registro de consentimiento persistido en la tabla `consentimientos_legales` con campo `revocado = false`.<br>3. Registro en `sesiones_mentoria` con `estado = 'PUBLICADA'` y `fecha_inicio > NOW() + INTERVAL '24 HOURS'`.<br>4. Recuento transaccional en `reservas_cupo` con estado activo menor a `aforo_maximo` (10 presencial / 20 virtual).<br>5. Inexistencia de tupla activa previa `(id_sesion, estudiante_email)` en la tabla `reservas_cupo`. |
| **PostCondiciones** | 1. Registro insertado en la tabla física `reservas_cupo` con `estado = 'PENDIENTE_CONFIRMACION'` y hash SHA-256 (`ticket_hash`).<br>2. Transacción confirmada en PostgreSQL mediante `db.commit()` con actualización atómica de vacantes.<br>3. Notificación flotante de confirmación desplegada en cliente con código de comprobante y persistencia en la vista `"Mis Reservas"`. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Exploración en Cartelera y Apertura del Diálogo Modal** | |
| **1.** El estudiante mentoreado autenticado navega por `RecommendationFeedView.tsx` y pulsa el botón `"Reservar Cupo"` en la tarjeta correspondiente a una sesión de mentoría en estado `PUBLICADA`. | **2.** En `App.tsx`, el evento `onSelectOffer` actualiza el estado `selectedOfferForBooking`. `BookingModalView.tsx` se renderiza recibiendo las propiedades requeridas (`isOpen={true}`, `offer`, `userEmail`, `onClose`, `onSuccess`). Ejecuta el hook `useEffect` validando `offer.available_slots > 0` y la no expiración de la sesión. (Si la tarjeta quedó desfasada y registra 0 cupos, salta a E001). (Si el mentoreado ya cuenta con una reserva activa para esa misma sesión, salta a E002). |
| **Fase 2: Verificación de Precondiciones y Reglas de Negocio en Cliente** | |
| **3.** En `BookingModalView.tsx`, el usuario revisa el panel de detalles de la sesión: título del tema curricular, nombre de la asignatura, fecha y hora programada, modalidad (Presencial con aula física o Virtual con enlace Google Meet) y aforo restante. Lee la advertencia del compromiso de asistencia y pulsa el botón `"Confirmar Reserva"`. | **4.** El componente activa el estado transicional `isSubmitting = true`, deshabilita los controles del modal y muestra un indicador circular animado en color azul institucional. Lee el token Bearer en `localStorage`. Invoca al método `reserveSeat(offer.id, userEmail)` expuesto por `ApiBookingAdapter` en `bookingService.ts`. (Si el token no existe o expiró, salta a E003). (Si el usuario es el propio mentor titular de la sesión, salta a E004). (Si el usuario no ha suscrito el consentimiento legal digital, salta a E005). |
| **Fase 3: Ejecución de Transacción Atómica con Bloqueo Pesimista en Base de Datos** | |
| **5.** El usuario observa en pantalla el progreso de procesamiento seguro. | **6.** En `bookingService.ts`, se despacha la petición `POST /api/v1/bookings/reserve` con cabecera `Authorization: Bearer <token>` y cuerpo JSON `{"id_sesion": id, "estudiante_email": email}`. El controlador `bookings.py` recibe la petición, valida el esquema Pydantic `BookingCreate` e invoca `booking_service.reserve_seat(db, session_id, current_user.email)`. `booking_service.py` adquiere el cerrojo global en memoria `_booking_lock.acquire(timeout=5.0)`. Inicia la transacción ACID en PostgreSQL con `db.begin()`. Configura el cerrojo de fila con `db.execute(text("SET LOCAL lock_timeout = '5.0s'"))`. Ejecuta la consulta relacional con bloqueo pesimista exclusivo de fila: `SELECT * FROM sesiones_mentoria WHERE id = :id FOR UPDATE OF sesiones_mentoria`. Verifica que la sesión exista, mantenga el estado `PUBLICADA`, no haya sobrepasado la ventana límite de 24 horas (`sesion.fecha_inicio > now_utc + timedelta(hours=24)`, RN-04), y que el recuento de reservas activas sea menor al aforo permitido (`occupied_seats < sesion.aforo_maximo`, 10 en presencial o 20 en virtual, RN-05). Inserta el nuevo registro en `reservas_cupo` con estado `PENDIENTE_CONFIRMACION` y ticket hash criptográfico SHA-256. Confirma atómicamente la transacción mediante `db.commit()` y libera el cerrojo `_booking_lock`. Retorna HTTP 201 Created con el payload `BookingResponse`. (Si la sesión no existe en base de datos, salta a E006). (Si el estado de la sesión cambió concurrentemente a CANCELADA, salta a E007). (Si la fecha de inicio no cumple la antelación de 24 horas, salta a E008). (Si ocurre timeout en la adquisición del cerrojo, salta a E009). (Si otra transacción concurrente ocupó el último cupo disponible en el mismo milisegundo, salta a E010). |
| **Fase 4: Confirmación y Actualización Reactiva de Estados** | |
| **7.** `bookingService.ts` recibe el código HTTP 201 y deserializa la entidad de respuesta. Transfiere el control a `BookingModalView.tsx`, la cual oculta el indicador de carga y conmuta su interfaz al panel de confirmación en color verde, desplegando el código de reserva, un recordatorio de ratificación obligatoria a T-24h y el botón `"Finalizar y Ver Mis Reservas"`. | **8.** El usuario hace clic en el botón `"Finalizar y Ver Mis Reservas"`. `BookingModalView.tsx` ejecuta el callback `onSuccess()`. En `App.tsx`, se invoca `fetchOffers()` para sincronizar las vacantes en cartelera, se actualiza el estado global de reservas del estudiante y se navega a la vista `StudentBookingsView.tsx`, presentando el registro recién formalizado en estado `PENDIENTE_CONFIRMACION`. |

##### Flujos de Excepción

##### Flujo de excepción E001: Oferta en cartelera sin vacantes disponibles
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `BookingModalView.tsx` detecta `offer.available_slots <= 0`. Modifica inmediatamente su estado interno deshabilitando el botón `"Confirmar Reserva"` y mostrando un aviso en color ámbar: *"Lo sentimos, el aforo para esta sesión se ha completado. No es posible generar nuevas reservas"*. Presenta el botón `<button onClick={onClose}>Volver a la Cartelera</button>`. |
| **E001-1.2** Hace clic en el botón "Volver a la Cartelera". | **E001-1.3** Invoca el callback `onClose()`, destruye la instancia modal del árbol del DOM y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Reserva duplicada activa para el mismo estudiante
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 2 del Flujo Normal, el hook `useEffect` en `BookingModalView.tsx` verifica la existencia previa de una reserva activa en el estado local de reservas del usuario. Alternativamente, en el paso 6, `booking_service.py` ejecuta `SELECT id FROM reservas_cupo WHERE id_sesion = :sid AND estudiante_email = :email AND estado IN ('PENDIENTE_CONFIRMACION', 'CONFIRMADA')`. Al hallar una tupla, lanza `HTTPException(status_code=400, detail="ALREADY_BOOKED: Ya posees una reserva activa registrada para esta sesión de mentoría.")`.<br><br>En `bookingService.ts`, captura el error 400 con código `'ALREADY_BOOKED'`. En `BookingModalView.tsx`, renderiza una notificación en color rojo con el mensaje de duplicidad y presenta el botón `<button onClick={onClose}>Aceptar</button>`. |
| **E002-1.2** Hace clic en el botón "Aceptar". | **E002-1.3** Cierra el cuadro modal, retorna el foco a la tarjeta de la sesión y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Sesión institucional no autenticada o token expirado
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 4 del Flujo Normal, `bookingService.ts` ejecuta `localStorage.getItem('auth_token')` y detecta valor nulo, o el backend responde con HTTP 401 Unauthorized por firma JWT vencida (`TokenExpiredError`).<br><br>En `bookingService.ts`, propaga la excepción hacia el contexto global. En `App.tsx`, el interceptor de seguridad purga el token expirado con `localStorage.removeItem('auth_token')`, conmuta el estado global `user` a `null` y monta el componente `LoginOtpView.tsx`, desplegando una alerta en color rojo: *"Su sesión institucional ha caducado por inactividad. Por favor, ingrese nuevamente mediante código OTP."* |
| **E003-1.2** Ingresa su correo institucional y solicita nuevo código de acceso. | **E003-1.3** Transfiere el control al flujo de autenticación y retorna al paso 1 del Flujo Normal de Eventos de CUS-001. |

##### Flujo de excepción E004: Conflicto de rol de mentor (Autoreserva Prohibida)
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 4 del Flujo Normal, `BookingModalView.tsx` compara `offer.mentor_email === userEmail`. Alternativamente, en el paso 6, `booking_service.py` valida `sesion.id_mentor == current_user.id`. Lanza `HTTPException(status_code=400, detail="CANNOT_BOOK_OWN_SESSION: Un mentor no puede reservar cupos en su propia sesión de mentoría.")`.<br><br>En `bookingService.ts`, captura el error con código `'CANNOT_BOOK_OWN_SESSION'`. `BookingModalView.tsx` inhabilita el botón de acción y despliega una advertencia en color rojo. Presenta el botón `<button onClick={onClose}>Cerrar</button>`. |
| **E004-1.2** Hace clic en el botón "Cerrar". | **E004-1.3** Cierra el modal sin realizar peticiones de mutación y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E005: Ausencia o revocación de consentimiento legal digital
| Usuario | Sistema |
|---|---|
| | **E005-1.1** En el paso 4 del Flujo Normal, `booking_service.py` invoca a `ConsentService.get_consent_status(current_user.email)` y obtiene `has_consented = false`. Lanza `HTTPException(status_code=403, detail="CONSENT_REQUIRED: Se requiere la formalización del consentimiento legal digital bajo la Ley Nº 29733 para realizar reservas de cupos.")`.<br><br>En `bookingService.ts`, eleva `new BookingException('CONSENT_REQUIRED', ...)`. En `App.tsx`, captura el error 403, oculta `BookingModalView.tsx` y monta en primer plano `ConsentModalView.tsx`, presentando los términos de tratamiento de datos personales. |
| **E005-1.2** Lee los términos legales, marca la casilla de aceptación y pulsa "Aceptar y Continuar". | **E005-1.3** Despacha `POST /api/v1/consent/accept`, persiste la traza legal, retorna el control al modal de reserva y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E006: Sesión de mentoría inexistente en el catálogo
| Usuario | Sistema |
|---|---|
| | **E006-1.1** En el paso 6 del Flujo Normal, la consulta relacional `SELECT * FROM sesiones_mentoria WHERE id = :id` retorna `None`. `booking_service.py` ejecuta `db.rollback()` y lanza `HTTPException(status_code=404, detail="SESSION_NOT_FOUND: La sesión de mentoría solicitada no existe o fue eliminada del catálogo.")`.<br><br>En `bookingService.ts`, eleva `new BookingException('SESSION_NOT_FOUND', message, 404)`. En `App.tsx`, el bloque `catch` ejecuta `setFeedRefreshKey((prev) => prev + 1)` para purgar la sesión obsoleta y muestra una alerta en color rojo. Presenta el botón `<button onClick={onClose}>Entendido</button>`. |
| **E006-1.2** Hace clic en el botón "Entendido". | **E006-1.3** Cierra el diálogo modal, actualiza la cartelera eliminando la tarjeta huérfana y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E007: Sesión cancelada concurrentemente por el mentor o administración
| Usuario | Sistema |
|---|---|
| | **E007-1.1** En el paso 6 del Flujo Normal, tras adquirir el bloqueo pesimista de fila, `booking_service.py` evalúa `sesion.estado != EstadoSesion.PUBLICADA`. Ejecuta `db.rollback()` y lanza `HTTPException(status_code=400, detail="SESSION_NOT_OPEN: La sesión seleccionada no se encuentra abierta para reservas (Estado actual: CANCELADA).")`.<br><br>En `bookingService.ts`, eleva `new BookingException('SESSION_NOT_OPEN', message, 400)`. En `App.tsx`, el bloque `catch` ejecuta `setFeedRefreshKey((prev) => prev + 1)` para invalidar la oferta obsoleta y muestra una notificación en color rojo. Presenta el botón `<button onClick={onClose}>Actualizar Cartelera</button>`. |
| **E007-1.2** Hace clic en el botón "Actualizar Cartelera". | **E007-1.3** Cierra el modal, remueve la tarjeta obsoleta del DOM mediante `fetchOffers()` y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E008: Ventana de antelación vencida (Regla Institucional RN-04)
| Usuario | Sistema |
|---|---|
| | **E008-1.1** En el paso 6 del Flujo Normal, `booking_service.py` evalúa `sesion.fecha_inicio <= now_utc + timedelta(hours=24)` y lanza `HTTPException(status_code=400, detail="WINDOW_CLOSED_T24H: Las reservas cierran 24 horas antes del inicio de la sesión.")`.<br><br>En `bookingService.ts`, identifica `'WINDOW_CLOSED_T24H'` y eleva `new BookingException('WINDOW_CLOSED_T24H', message, 400)`. `BookingModalView.tsx` renderiza la advertencia en color rojo indicando que las inscripciones cerraron por límite de 24 horas. Presenta el botón `<button onClick={onClose}>Entendido</button>`. |
| **E008-1.2** Hace clic en el botón "Entendido". | **E008-1.3** Cierra el diálogo modal, actualiza la tarjeta mostrando el botón deshabilitado con el texto "Inscripciones Cerradas" y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E009: Timeout de concurrencia en adquisición de cerrojo (Database Busy)
| Usuario | Sistema |
|---|---|
| | **E009-1.1** En el paso 6 del Flujo Normal, `_booking_lock.acquire(timeout=5.0)` retorna `False` o PostgreSQL lanza excepción por timeout de cerrojo. `booking_service.py` lanza `HTTPException(status_code=503, detail="DATABASE_BUSY: El servicio de reservas se encuentra temporalmente sobrecargado. Por favor, reintente en unos momentos.")`.<br><br>En `bookingService.ts`, eleva `new BookingException('DATABASE_BUSY', message, 503)`. En `App.tsx`, el bloque `catch` preserva la intención del usuario sin ejecutar rollback destructivo. `BookingModalView.tsx` rehabilita los botones y muestra un aviso en color ámbar: *"El servicio se encuentra temporalmente con alta concurrencia. No se ha generado ningún cargo. Por favor, pulsa 'Reintentar'"*. Presenta el botón `<button onClick={handleConfirmClick}>Reintentar Reserva</button>`. |
| **E009-1.2** Hace clic en el botón "Reintentar Reserva". | **E009-1.3** Dispara nuevamente la petición `bookingService.reserveSeat` y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E010: Colisión concurrente por aforo agotado en el último milisegundo
| Usuario | Sistema |
|---|---|
| | **E010-1.1** En el paso 6 del Flujo Normal, bajo el cerrojo pesimista `SELECT ... FOR UPDATE OF sesiones_mentoria`, `booking_service.py` evalúa `occupied_seats >= sesion.aforo_maximo`. Ejecuta `db.rollback()` y lanza `HTTPException(status_code=409, detail="CAPACITY_EXCEEDED: Aforo completo. No quedan vacantes disponibles en esta sesión.")`.<br><br>En `bookingService.ts`, eleva `new BookingException('CAPACITY_EXCEEDED', 'Aforo completo o colisión con otra reserva concurrente.', 409)`. En `App.tsx`, el bloque `catch` captura `err.code === 'CAPACITY_EXCEEDED'`, ejecuta `setFeedRefreshKey((prev) => prev + 1)` para sincronizar la cartelera y despliega en `BookingModalView.tsx` un panel en color naranja de alerta indicando que la última vacante fue ocupada simultáneamente por otro usuario. Presenta el botón `<button onClick={handleGoToDemand}>Registrar Demanda de Tema</button>` y el botón `<button onClick={onClose}>Volver a la Cartelera</button>`. |
| **E010-1.2** Hace clic en el botón "Volver a la Cartelera" (o en "Registrar Demanda de Tema"). | **E010-1.3** Cierra `BookingModalView.tsx`, actualiza la tarjeta en la cartelera como "Aforo Completo (0 vacantes)" y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-024 - Ratificar asistencia a sesión de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-024** (CUS-024) |
| **Nombre** | Ratificar asistencia obligatoria a sesión de mentoría académica a T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-013 (Confirmación anticipada de asistencia a mentoría); RN-04 (Ventana de ratificación previa entre T-48h y T-24h), RN-10 (Control de asistencia y quórum institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite a los estudiantes mentoreados con reservas provisionales en estado `PENDIENTE_CONFIRMACION` confirmar obligatoriamente su asistencia definitiva dentro de la ventana de ratificación institucional comprendida entre las 48 horas y las 24 horas previas al inicio de la sesión (`sesion.fecha_inicio - 48h <= now_utc <= sesion.fecha_inicio - 24h`). El usuario accede a la vista `StudentBookingsView.tsx` y acciona el botón de confirmación enlazado a `bookingService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/bookings.py` y `app/services/booking_service.py` procesan la petición `POST /api/v1/bookings/{id}/confirm`, verifican la vigencia temporal de la ventana, conmutan el estado de la entidad `ReservaCupo` a `CONFIRMADA`, generan el identificador criptográfico del pase de lista y emiten una respuesta HTTP 200 OK, contribuyendo al cálculo del quórum mínimo (RN-05). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Reglamento Académico de Asistencia y Quórum EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/StudentBookingsView.tsx`<br>`aplicacion/frontend/src/services/bookingService.ts` (`BookingService.confirmBooking`)<br>`aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/{id}/confirm`)<br>`aplicacion/backend/app/services/booking_service.py` (`BookingService.confirm_booking`)<br>`aplicacion/backend/app/models/booking.py` (`ReservaCupo`, `EstadoReserva`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Usuario con sesión institucional activa y rol `mentoreado` verificado en JWT.<br>2. Reserva en la tabla `reservas_cupo` asociada al estudiante en estado `PENDIENTE_CONFIRMACION`.<br>3. Fecha y hora actual dentro de la ventana temporal de confirmación [T-48h, T-24h]. |
| **PostCondiciones** | 1. Estado de la entidad `ReservaCupo` actualizado atómicamente a `CONFIRMADA` en PostgreSQL.<br>2. Generación del código seguro de verificación de asistencia.<br>3. Actualización reactiva de la tarjeta en la interfaz del estudiante con distintivo verde de confirmación. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de reservas y visualización de ventana de ratificación** | |
| **1.** El estudiante mentoreado accede a `"Mis Reservas"` en `StudentBookingsView.tsx`. | **2.** En `bookingService.ts`, se despacha `GET /api/v1/bookings/my-bookings`. El backend retorna las reservas del estudiante. En `StudentBookingsView.tsx`, para las reservas cuya sesión se encuentra dentro de la ventana de ratificación [T-48h, T-24h], se renderiza un panel de alerta en color ámbar con un temporizador y el botón `"Ratificar Asistencia Obligatoria"`. |
| **Fase 2: Validación de plazos y solicitud de ratificación** | |
| **3.** El estudiante revisa los datos de la sesión y pulsa el botón `"Ratificar Asistencia Obligatoria"`. | **4.** En `StudentBookingsView.tsx`, se abre un cuadro modal de ratificación. El estudiante presiona `"Sí, Confirmo mi Asistencia Definitiva"`. En `bookingService.ts`, se despacha la petición `POST /api/v1/bookings/{booking_id}/confirm`. En `bookings.py`, `booking_service.py` ejecuta `SELECT r.*, s.fecha_inicio FROM reservas_cupo r JOIN sesiones_mentoria s ON r.id_sesion = s.id WHERE r.id = :bid AND r.estudiante_email = :email`. Verifica que `now_utc >= s.fecha_inicio - timedelta(hours=48)` y que `now_utc <= s.fecha_inicio - timedelta(hours=24)`. (Si el estudiante intenta ratificar antes de T-48h, salta a E001). (Si la ventana ya expiró por superar el umbral T-24h, salta a E002). |
| **Fase 3: Transición atómica de estado y emisión de pase de asistencia** | |
| **5.** El estudiante espera la respuesta visual de confirmación. | **6.** En `booking_service.py`, se ejecuta `UPDATE reservas_cupo SET estado = 'CONFIRMADA', fecha_confirmacion = :now WHERE id = :bid`. Confirma la transacción con `db.commit()` y retorna HTTP 200 con el modelo `BookingResponse`. En cliente, `StudentBookingsView.tsx` conmuta el estado de la tarjeta a color verde con la leyenda *"Asistencia Ratificada"*, despliega el código alfanumérico para el pase de lista presencial/virtual y emite una notificación de éxito. |

##### Flujos de Excepción

##### Flujo de excepción E001: Intento de ratificación anticipada fuera de ventana
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `booking_service.py` evalúa `now_utc < sesion.fecha_inicio - timedelta(hours=48)`. Lanza `HTTPException(status_code=400, detail="CONFIRMATION_NOT_OPEN: La ventana de confirmación abre exactamente 48 horas antes del inicio de la sesión.")`.<br><br>En `StudentBookingsView.tsx`, se despliega un mensaje en color azul institucional indicando la fecha y hora exacta en que se habilitará la ratificación obligatoria. |
| **E001-1.2** Hace clic en el botón "Entendido" en la alerta. | **E001-1.3** Cierra el modal de confirmación y retorna al paso 2 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Ventana de ratificación vencida a T-24h
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, `booking_service.py` evalúa `now_utc > sesion.fecha_inicio - timedelta(hours=24)`. Lanza `HTTPException(status_code=400, detail="CONFIRMATION_WINDOW_EXPIRED: La ventana de ratificación cerró 24 horas antes del inicio. La reserva no confirmada fue liberada para dar paso al proceso de quórum.")`.<br><br>En `StudentBookingsView.tsx`, se actualiza la tarjeta a estado inactivo con una insignia en color gris indicando que el cupo fue dado de baja por falta de ratificación en plazo. |
| **E002-1.2** Hace clic en el botón "Aceptar". | **E002-1.3** Actualiza la lista de reservas en cliente y retorna al paso 2 del Flujo Normal de Eventos. |

#### CUS-017 - Desistir voluntariamente de reserva

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-017** (CUS-017) |
| **Nombre** | Desistir voluntariamente de reserva de cupo sin penalidad antes de T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-014 (Desistimiento voluntario y liberación anticipada de cupos); RN-04 (Antelación mínima de 24 horas para cancelaciones sin sanción institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite a los estudiantes mentoreados anular voluntariamente una reserva activa en estado `PENDIENTE_CONFIRMACION` o `CONFIRMADA` sin incurrir en penalizaciones académicas, siempre que la solicitud se despache con una antelación mayor a 24 horas respecto al inicio de la sesión (`fecha_inicio > now_utc + 24h`, RN-04). El componente `StudentBookingsView.tsx` despacha `POST /api/v1/bookings/{id}/cancel` hacia `bookings.py` y `app/services/booking_service.py`. El backend adquiere el cerrojo pesimista de fila, actualiza el estado de la reserva a `CANCELADA_ESTUDIANTE`, decrementa el contador de cupos ocupados de la sesión y confirma la transacción ACID con `db.commit()`, notificando al motor de recomendaciones sobre la vacante liberada. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Reglamento Académico de Asistencia EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/StudentBookingsView.tsx`<br>`aplicacion/frontend/src/services/bookingService.ts` (`BookingService.cancelBooking`)<br>`aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/{id}/cancel`)<br>`aplicacion/backend/app/services/booking_service.py` (`BookingService.cancel_booking`)<br>`aplicacion/backend/app/models/booking.py` (`ReservaCupo`, `EstadoReserva`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Usuario autenticado con token JWT institucional y titularidad sobre la reserva.<br>2. Reserva en estado `PENDIENTE_CONFIRMACION` o `CONFIRMADA`.<br>3. Fecha de inicio de la sesión mayor a la hora actual UTC más 24 horas (`fecha_inicio > now + 24h`). |
| **PostCondiciones** | 1. Estado de `ReservaCupo` actualizado a `CANCELADA_ESTUDIANTE` en PostgreSQL.<br>2. Cupo vacante liberado y disponible nuevamente en la cartelera institucional.<br>3. Despliegue de confirmación en cliente y actualización reactiva de la tarjeta a color neutro. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Solicitud de desistimiento y verificación de plazos** | |
| **1.** El estudiante mentoreado localiza su reserva en `StudentBookingsView.tsx` y hace clic en el botón `"Cancelar Reserva"`. | **2.** En `StudentBookingsView.tsx`, se abre un modal de advertencia indicando que el desistimiento es irrevocable y liberará el cupo para otro compañero. El sistema solicita seleccionar un motivo de cancelación opcional en una lista desplegable. (Si la antelación es inferior a 24 horas respecto al inicio de la sesión, salta a E001). |
| **Fase 2: Confirmación y procesamiento atómico de liberación de cupo** | |
| **3.** El estudiante selecciona el motivo y pulsa el botón `"Confirmar Cancelación"`. | **4.** En `bookingService.ts`, se despacha `POST /api/v1/bookings/{booking_id}/cancel`. En `bookings.py`, `booking_service.py` inicia la transacción con `db.begin()`. Ejecuta bloqueo de fila en `sesiones_mentoria` y `reservas_cupo`. Verifica que `sesion.fecha_inicio > now_utc + timedelta(hours=24)` (RN-04). Actualiza `reservas_cupo.estado = 'CANCELADA_ESTUDIANTE'` y registra `fecha_cancelacion = now_utc`. Ejecuta `db.commit()` y retorna HTTP 200 con `BookingResponse`. |
| **5.** El estudiante visualiza el modal de éxito indicando la liberación correcta del cupo sin penalidad. | **6.** En `StudentBookingsView.tsx`, se cierra el modal, se conmuta el estado de la tarjeta a color gris con la leyenda *"Cancelada por el estudiante"* y se emite un evento de actualización que incrementa las vacantes disponibles en la cartelera. |

##### Flujos de Excepción

##### Flujo de excepción E001: Desistimiento tardío con menos de 24 horas de antelación
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `booking_service.py` comprueba que `sesion.fecha_inicio <= now_utc + timedelta(hours=24)`. Lanza `HTTPException(status_code=400, detail="LATE_CANCELLATION_PROHIBITED: No se permite la cancelación voluntaria con menos de 24 horas de antelación para no desestabilizar el quórum de la sesión.")`.<br><br>En `StudentBookingsView.tsx`, se despliega un panel de advertencia en color rojo indicando que la política institucional prohíbe cancelaciones a menos de 24 horas y que la inasistencia injustificada acarreará una penalización temporal en futuras reservas. |
| **E001-1.2** Hace clic en el botón "Entendido". | **E001-1.3** Cierra el cuadro modal manteniendo la reserva en estado activo y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-023 - Evaluar quórum automático a T-24h

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-023** (CUS-023) |
| **Nombre** | Evaluar automáticamente el quórum reglamentario de sesiones de mentoría a T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-015 (Monitoreo desatendido, emisión de recordatorios y evaluación de quórum); RN-05 (Regla de quórum mínimo de 3 estudiantes confirmados), RN-10 (Automatización de eventos temporales a T-24h) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Proceso Demonio en Segundo Plano (`SchedulerWorker`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 |
| **Descripción** | Permite evaluar de forma automatizada y desatendida el cumplimiento del umbral reglamentario de quórum institucional (mínimo 3 estudiantes con asistencia ratificada en presencial o 5 en virtual, RN-05) exactamente 24 horas antes del inicio programado de cada sesión de mentoría. Un proceso en segundo plano o endpoint administrativo `POST /api/v1/quorum/evaluate-all` en `aplicacion/backend/app/api/v1/endpoints/quorum.py` invoca al método `evaluate_all_active_quorums` en `app/services/booking_service.py`. El servicio adquiere un bloqueo pesimista `SELECT ... FOR UPDATE` sobre `sesiones_mentoria`, valida que `quorumevaluated_at` sea nulo para garantizar estricta idempotencia transaccional, cuantifica las reservas en estado `CONFIRMADA`, caduca las reservas no ratificadas a `CANCELADA_NO_CONFIRMADA`; si se alcanza o supera el quórum, promueve automáticamente la sesión a estado `CONFIRMADA`. Si no se alcanza el quórum reglamentario, transiciona la sesión a estado `QUORUM_INSUFICIENTE` y despacha alertas urgentes al mentor para la resolución de contingencia (CUS-007). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Reglamento Académico de Quórum y Viabilidad de Sesiones EPIS-UPT |
| **Anexos** | `aplicacion/backend/app/api/v1/endpoints/quorum.py` (`POST /api/v1/quorum/evaluate-all`, `POST /api/v1/quorum/evaluate`)<br>`aplicacion/backend/app/services/booking_service.py` (`BookingService.evaluate_session_quorum`, `BookingService.evaluate_all_active_quorums`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`, `quorumevaluated_at`), `app/models/booking.py` (`ReservaCupo`, `EstadoReserva`) |
| **Precondiciones** | 1. Sesión de mentoría en estado `PUBLICADA` en la tabla física `sesiones_mentoria`.<br>2. Fecha y hora actual del servidor en la marca temporal exacta de 24 horas previas al inicio de la sesión (`now_utc >= fecha_inicio - 24h`).<br>3. Proceso planificador o disparador de simulación operativo. |
| **PostCondiciones** | 1. Estado de `SesionMentoria` actualizado en base de datos a `CONFIRMADA` o `QUORUM_INSUFICIENTE`.<br>2. Transacción confirmada en PostgreSQL y generación de registros de auditoría de evaluación.<br>3. Disparo de notificaciones hacia el mentor y los estudiantes inscritos. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Disparo de la tarea programada y localización de sesiones a T-24h** | |
| **1.** El proceso planificador del sistema en segundo plano (`SchedulerWorker`) ejecuta el ciclo de evaluación o el administrador despacha la petición `POST /api/v1/quorum/evaluate-all`. | **2.** En `quorum.py`, el controlador invoca `booking_service.BookingService.evaluate_all_active_quorums(db)`. El backend ejecuta `SELECT * FROM sesiones_mentoria WHERE estado = 'PUBLICADA' AND quorumevaluated_at IS NULL AND fecha_inicio <= NOW() + INTERVAL '24 HOURS' FOR UPDATE`. (Si no existen sesiones en la ventana T-24h, el sistema finaliza la ejecución sin mutaciones). |
| **Fase 2: Cuantificación de confirmaciones y verificación de umbral de quórum** | |
| **3.** El sistema procesa cada sesión localizada en un bucle transaccional independiente. | **4.** En `booking_service.py`, para cada sesión se ejecuta `SELECT count(*) FROM reservas_cupo WHERE id_sesion = :sid AND estado = 'CONFIRMADA'`. El servicio evalúa si `confirmed_count >= 3` (RN-05). (Si el recuento es menor a 3 confirmados, salta a A001). |
| **Fase 3: Confirmación oficial de sesión y notificación de viabilidad** | |
| **5.** El sistema constata que la sesión cumple el quórum reglamentario (3 o más estudiantes con asistencia ratificada). | **6.** En `booking_service.py`, se ejecuta `UPDATE sesiones_mentoria SET estado = 'CONFIRMADA' WHERE id = :sid`. Se confirma la transacción con `db.commit()`. Se genera la traza en la bitácora de auditoría y se despacha una notificación por correo electrónico y notificación web al mentor y a los estudiantes inscritos con el texto: *"¡Sesión confirmada! Tu sesión de mentoría cuenta con el quórum reglamentario para su realización"*. Retorna HTTP 200 con el resumen de la evaluación. |

##### Flujos Alternativos

##### Flujo alternativo A001: Quórum insuficiente a T-24h con alerta al mentor
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 4 del Flujo Normal, `booking_service.py` detecta que la sesión tiene menos de 3 estudiantes confirmados (`confirmed_count < 3`). | **A001-1.2** El servicio ejecuta `UPDATE sesiones_mentoria SET estado = 'QUORUM_INSUFICIENTE' WHERE id = :sid` y confirma con `db.commit()`. |
| **A001-1.3** El mentor titular de la sesión recibe una alerta urgente en su panel de control y correo institucional: *"Alerta de Quórum: Tu sesión programada para mañana no alcanzó el quórum mínimo de 3 estudiantes. Por favor, ingresa para decidir si dictarla, reprogramarla o cancelarla"*. | **A001-1.4** El sistema habilita el componente de resolución de contingencia en la interfaz del mentor y concluye el caso de uso y transfiere el flujo a la toma de decisión del mentor (CUS-007). |

#### CUS-007 - Decisión del mentor ante quórum insuficiente

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-007** (CUS-007) |
| **Nombre** | Gestionar sesión de mentoría y decisión resolutiva ante quórum insuficiente |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-016 (Gestión resolutiva de sesiones ante quórum insuficiente); RN-04 (Antelación mínima de reprogramación), RN-10 (Resolución de contingencia ante quórum) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 |
| **Descripción** | Permite al estudiante mentor tomar una decisión resolutiva cuando su sesión no alcanza el quórum reglamentario de 3 estudiantes a T-24h (estado `QUORUM_INSUFICIENTE`) a través del componente cliente `MentorSessionsView.tsx` y el servicio `offerService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/offers.py` y `app/services/offer_service.py` procesan la petición `POST /api/v1/offers/{id}/quorum-decision`. El mentor cuenta con tres alternativas reglamentarias: 1) Dictar la sesión de todas formas con los estudiantes confirmados (promoción forzada a `CONFIRMADA`), 2) Reprogramar la sesión para una nueva fecha con antelación mínima de 24 horas, o 3) Cancelar la sesión definitivamente liberando a los inscritos sin penalización alguna. La operación se ejecuta bajo una transacción ACID confirmada con `db.commit()`. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Reglamento Académico de Contingencia de Mentorías EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/MentorSessionsView.tsx`<br>`aplicacion/frontend/src/services/offerService.ts` (`OfferService.resolveQuorum`)<br>`aplicacion/backend/app/api/v1/endpoints/offers.py` (`POST /api/v1/offers/{id}/quorum-decision`)<br>`aplicacion/backend/app/services/offer_service.py` (`OfferService.resolve_quorum_decision`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`, `EstadoSesion`), `app/models/booking.py` (`ReservaCupo`) |
| **Precondiciones** | 1. Mentor titular autenticado con token JWT institucional activo.<br>2. Sesión en la tabla `sesiones_mentoria` en estado estricto `QUORUM_INSUFICIENTE`.<br>3. Decisión despachada antes del inicio programado de la sesión. |
| **PostCondiciones** | 1. Estado de `SesionMentoria` actualizado en base de datos según la decisión elegida (`CONFIRMADA`, `REPROGRAMADA` o `CANCELADA_QUORUM`).<br>2. Actualización en cascada de los estados de reserva de los estudiantes inscritos.<br>3. Despacho automatizado de notificaciones informativas a los estudiantes afectados. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso a la sesión con quórum insuficiente y visualización de opciones** | |
| **1.** El mentor accede a `"Mis Sesiones"` en `MentorSessionsView.tsx` y visualiza la tarjeta de la sesión resaltada en color ámbar con la etiqueta *"Quórum Insuficiente"*. | **2.** El mentor hace clic en el botón `"Gestionar Sesión"`. En `MentorSessionsView.tsx`, se abre una ventana modal desplegando los estudiantes inscritos confirmados y las tres opciones resolutivas: 1) `"Dictar de Todas Formas"`, 2) `"Reprogramar Sesión"`, 3) `"Cancelar Sesión Definitivamente"`. |
| **Fase 2: Elección de la resolución y verificación de parámetros** | |
| **3.** El mentor selecciona la opción `"Dictar de Todas Formas"` (o `"Reprogramar Sesión"` indicando nueva fecha y hora, o `"Cancelar Sesión"` ingresando un justificativo) y presiona el botón `"Confirmar Decisión"`. | **4.** En `offerService.ts`, se despacha la petición `POST /api/v1/offers/{offer_id}/quorum-decision` con payload JSON `{"decision": "PROCEED" | "RESCHEDULE" | "CANCEL", "new_start_time": ..., "reason": ...}`. En `offers.py`, `offer_service.py` inicia la transacción con `db.begin()`. Valida que la sesión se encuentre en estado `QUORUM_INSUFICIENTE`. Si seleccionó reprogramar, valida que la nueva fecha cumpla con la antelación mayor a 24 horas (RN-04). Si seleccionó cancelar, valida que el justificativo no esté vacío. (Si la fecha de reprogramación es inferior a 24 horas, salta a E001). (Si la justificación de cancelación está vacía, salta a E002). |
| **Fase 3: Persistencia de la resolución y notificación a los estudiantes** | |
| **5.** El mentor observa el indicador de procesamiento seguro en el botón de confirmación. | **6.** En `offer_service.py`, si la decisión es `PROCEED`, actualiza `sesiones_mentoria.estado = 'CONFIRMADA'`. Si es `RESCHEDULE`, actualiza fecha y hora, restablece `estado = 'PUBLICADA'` y notifica a los inscritos. Si es `CANCEL`, actualiza `estado = 'CANCELADA_QUORUM'` y libera a los inscritos. Confirma la transacción con `db.commit()` y retorna HTTP 200. En cliente, `MentorSessionsView.tsx` cierra el modal, actualiza el estado de la tarjeta y despliega una notificación flotante en color verde: *"Decisión registrada exitosamente"*. |

##### Flujos de Excepción

##### Flujo de excepción E001: Fecha de reprogramación con menos de 24 horas de antelación
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el mentor selecciona reprogramar pero ingresa una fecha y hora con antelación menor a 24 horas respecto al tiempo actual. `offer_service.py` valida la regla RN-04 y lanza `HTTPException(status_code=400, detail="INSUFFICIENT_RESCHEDULE_ADVANCE: La nueva fecha de la sesión debe programarse con al menos 24 horas de antelación.")`.<br><br>En `MentorSessionsView.tsx`, se resalta el selector de fecha en color rojo con el mensaje de infracción reglamentaria. |
| **E001-1.2** Selecciona una nueva fecha y hora con un margen superior a 24 horas. | **E001-1.3** Rehabilita el botón de confirmación en la interfaz y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Justificación de cancelación definitiva vacía
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, el mentor selecciona cancelar la sesión pero deja en blanco el campo de motivo. `offer_service.py` comprueba que la cadena es nula o vacía y lanza `HTTPException(status_code=422, detail="REASON_REQUIRED: Debe ingresar obligatoriamente un motivo justificado para proceder con la cancelación definitiva.")`.<br><br>En `MentorSessionsView.tsx`, se destaca el área de texto en color rojo solicitando ingresar el motivo para los estudiantes. |
| **E002-1.2** Ingresa una justificación válida en el cuadro de texto. | **E002-1.3** Valida la longitud mínima en cliente y retorna al paso 3 del Flujo Normal de Eventos. |


---

### MOD-06: Asistencia, Bitácoras y Feedback

#### CUS-012 - Registrar asistencia a sesión de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-012** (CUS-012) |
| **Nombre** | Registrar asistencia interactiva a sesión de mentoría mediante código QR dinámico |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-017 (Registro de bitácora pedagógica y control de asistencia); RN-05 (Aforo y presencia efectiva), RN-12 (Trazabilidad de asistencia y ventana temporal de check-in) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 |
| **Descripción** | Permite registrar la presencia efectiva de los estudiantes durante la ejecución de una sesión de mentoría a través del componente cliente `SessionAttendanceView.tsx` y el servicio `attendanceService.ts`. El mentor proyecta o comparte un código QR dinámico cifrado basado en TOTP que rota cada 30 segundos. El estudiante mentoreado escanea el código o digita el pase numérico de 6 dígitos despachando `POST /api/v1/sessions/{id}/attendance/check-in` hacia el backend en `aplicacion/backend/app/api/v1/endpoints/attendance.py`. El servicio `AttendanceService` valida que la solicitud se produzca dentro de la ventana de la sesión (desde 15 minutos antes del inicio hasta 30 minutos tras el fin), comprueba que el estudiante posea una reserva en estado `CONFIRMADA` y persiste el registro en la tabla `asistencias_sesion` (`app/models/attendance.py`) con timestamp UTC y geolocalización o IP institucional, transmitiendo el evento en tiempo real vía WebSockets al panel del mentor. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-06: Trazabilidad, Bitácoras y Evaluación)<br>Reglamento Académico de Control de Asistencia y Acreditación EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/SessionAttendanceView.tsx`<br>`aplicacion/frontend/src/services/attendanceService.ts` (`AttendanceService`, `ApiAttendanceAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/attendance.py` (`POST /api/v1/sessions/{id}/attendance/check-in`, `GET /api/v1/sessions/{id}/attendance`)<br>`aplicacion/backend/app/services/attendance_service.py` (`AttendanceService.record_checkin`, `AttendanceService.get_roster`)<br>`aplicacion/backend/app/models/attendance.py` (`AsistenciaSesion`), `app/models/booking.py` (`ReservaCupo`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Sesión de mentoría en estado `CONFIRMADA` o `EN_CURSO` en la base de datos.<br>2. Estudiante mentoreado con reserva en estado `CONFIRMADA` en la tabla `reservas_cupo`.<br>3. Petición ejecutada dentro de la ventana temporal de validez de la sesión [inicio - 15m, fin + 30m]. |
| **PostCondiciones** | 1. Registro insertado o actualizado en la tabla física `asistencias_sesion` con `asistio = true`.<br>2. Transmisión del evento de presencia en tiempo real al panel del mentor.<br>3. Despliegue del comprobante de asistencia en la interfaz del mentoreado y habilitación de encuesta de calidad post-mentoría. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura de sesión y generación de token dinámico de asistencia** | |
| **1.** El mentor accede a la sesión activa en `SessionAttendanceView.tsx` y pulsa el botón `"Iniciar Pase de Asistencia Digital"`. | **2.** En `attendanceService.ts`, se despacha `GET /api/v1/sessions/{id}/attendance/token`. El backend genera un token criptográfico TOTP con ventana de rotación de 30 segundos y lo serializa en un código QR interactivo proyectado en la pantalla del mentor junto con la nómina de estudiantes con reserva confirmada en estado provisional *"Ausente"*. |
| **Fase 2: Escaneo de código QR y validación de reserva y ventana horaria** | |
| **3.** El mentoreado presente en la sesión escanea el código QR desde su dispositivo móvil o ingresa el código numérico de 6 dígitos en su aplicación y pulsa `"Registrar Mi Asistencia"`. | **4.** En `attendanceService.ts`, se despacha `POST /api/v1/sessions/{id}/attendance/check-in` con payload `{"session_id": id, "qr_token": token}`. En `attendance.py`, `AttendanceService.record_checkin` valida: 1) que el token TOTP no haya expirado, 2) que el estudiante mantenga una reserva en estado `CONFIRMADA`, 3) que la hora actual esté dentro del intervalo de la sesión (`fecha_inicio - 15m <= now_utc <= fecha_fin + 30m`). (Si el token TOTP o código numérico ha expirado, salta a E001). (Si el estudiante no cuenta con reserva confirmada en la sesión, salta a E002). (Si el check-in se intenta fuera del intervalo temporal permitido, salta a E003). |
| **Fase 3: Persistencia de asistencia y actualización reactiva en tiempo real** | |
| **5.** El estudiante y el mentor observan la actualización instantánea en pantalla. | **6.** En `attendance_service.py`, se ejecuta `INSERT INTO asistencias_sesion (sesion_id, estudiante_id, fecha_checkin, asistio, ip_origen) VALUES (...) ON CONFLICT (sesion_id, estudiante_id) DO UPDATE SET asistio = true, fecha_checkin = NOW()`. Se confirma la transacción con `db.commit()`. El servidor emite un evento WebSocket hacia el panel del mentor, actualizando la fila del estudiante a estado *"Presente"* con un distintivo en color verde. En el dispositivo del mentoreado, se muestra una notificación de éxito: *"¡Asistencia registrada exitosamente! Gracias por tu puntualidad."* |

##### Flujos de Excepción

##### Flujo de excepción E001: Código QR o token TOTP expirado
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `AttendanceService` comprueba que el token TOTP superó su ciclo de vida de 30 segundos. Lanza `HTTPException(status_code=400, detail="QR_TOKEN_EXPIRED: El código de asistencia ha expirado. Por favor, escanee el código QR actualizado proyectado por el mentor.")`.<br><br>En el cliente del estudiante, se despliega una advertencia en color ámbar solicitando enfocar el nuevo código dinámico. Presenta el botón `<button onClick={handleRetryScan}>Escanear Nuevo Código</button>`. |
| **E001-1.2** Hace clic en el botón "Escanear Nuevo Código" y enfoca la pantalla del mentor. | **E001-1.3** Captura el nuevo token TOTP y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Estudiante sin reserva previa confirmada
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, la consulta relacional detecta que el estudiante no posee una tupla en `reservas_cupo` con `estado = 'CONFIRMADA'`. Lanza `HTTPException(status_code=403, detail="NO_CONFIRMED_BOOKING: No registra una reserva confirmada para esta sesión de mentoría.")`.<br><br>En la interfaz del estudiante, se muestra una alerta en color rojo indicando que solo los estudiantes debidamente inscritos y ratificados a T-24h pueden registrar su asistencia. |
| **E002-1.2** Hace clic en el botón "Entendido" en la alerta de restricción. | **E002-1.3** Cierra el escáner y finaliza la interacción sin registrar presencia. |

##### Flujo de excepción E003: Check-in fuera del intervalo temporal reglamentario
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 4 del Flujo Normal, el servicio comprueba que la hora actual del servidor se ubica fuera del intervalo de tolerancia reglamentaria (más de 15 minutos antes del inicio o más de 30 minutos después de concluida la sesión). Lanza `HTTPException(status_code=400, detail="CHECKIN_WINDOW_CLOSED: El pase de asistencia sólo está habilitado durante la realización de la sesión.")`.<br><br>En la interfaz del estudiante, se despliega un mensaje en color rojo indicando que el registro de asistencia se encuentra cerrado. |
| **E003-1.2** Hace clic en el botón "Aceptar". | **E003-1.3** Redirige a la vista principal y finaliza el caso de uso sin generar registros en la base de datos. |

#### CUS-013 - Registrar bitácora académica de sesión

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-013** (CUS-013) |
| **Nombre** | Registrar bitácora pedagógica y reporte formativo de sesión de mentoría |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-017 (Registro de bitácora pedagógica y control de asistencia); RN-12 (Plazo máximo de 48 horas post-sesión para registro de bitácora) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Coordinador Académico |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 |
| **Descripción** | Permite al estudiante mentor consignar el reporte pedagógico de la sesión de mentoría recién concluida a través del formulario `BitacoraFormView.tsx` y el servicio `bitacoraService.ts`. El mentor detalla los temas específicos del sílabo abordados, el nivel de asimilación conceptual de los participantes, las dificultades pedagógicas observadas y las observaciones institucionales. La petición se despacha mediante `POST /api/v1/sessions/{id}/bitacora` hacia el backend en `aplicacion/backend/app/api/v1/endpoints/bitacora.py`. El servicio `BitacoraService` valida que la sesión se encuentre en estado `CONCLUIDA`, que el plazo transcurrido desde el fin de la sesión no exceda las 48 horas reglamentarias (RN-12) y que el texto pedagógico supere los 50 caracteres mínimos. Persiste la entidad `BitacoraPedagogica` (`app/models/bitacora.py`) vinculada a la sesión y actualiza el estado a `BITACORA_REGISTRADA` para su posterior visado administrativo. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-06: Trazabilidad, Bitácoras y Evaluación)<br>Reglamento Académico de Mentorías y Certificación de Horas EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/BitacoraFormView.tsx`<br>`aplicacion/frontend/src/services/bitacoraService.ts` (`BitacoraService`, `ApiBitacoraAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/bitacora.py` (`POST /api/v1/sessions/{id}/bitacora`, `GET /api/v1/sessions/{id}/bitacora`)<br>`aplicacion/backend/app/services/bitacora_service.py` (`BitacoraService.create_bitacora`)<br>`aplicacion/backend/app/models/bitacora.py` (`BitacoraPedagogica`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Mentor titular con sesión institucional autenticada.<br>2. Sesión de mentoría en estado `CONCLUIDA` en la base de datos.<br>3. Plazo posterior a la finalización de la sesión menor o igual a 48 horas (`now_utc <= fecha_fin + 48h`). |
| **PostCondiciones** | 1. Registro insertado en la tabla `bitacoras_pedagogicas` con código de firma digital SHA-256.<br>2. Estado de `SesionMentoria` actualizado a `BITACORA_REGISTRADA` en PostgreSQL.<br>3. Despliegue de confirmación en cliente y habilitación de las horas para acreditación institucional. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura de bitácora y verificación de plazo límite** | |
| **1.** El mentor ingresa a la sesión concluida en `BitacoraFormView.tsx` y presiona el botón `"Completar Bitácora Pedagógica"`. | **2.** En `bitacoraService.ts`, se invoca la verificación de estado de la sesión. El backend comprueba que la sesión finalizó y que `now_utc <= fecha_fin + timedelta(hours=48)` (RN-12). En `BitacoraFormView.tsx`, se renderiza el formulario pedagógico: lista de temas silábicos cubiertos con casillas de verificación, selector de nivel de dificultad (Bajo, Medio, Alto), cuadro de texto para observaciones pedagógicas y declaración jurada de veracidad. (Si han transcurrido más de 48 horas desde el cierre de la sesión, salta a E001). |
| **Fase 2: Ingreso de evidencias pedagógicas y validación de contenido** | |
| **3.** El mentor marca los temas curriculares explicados, selecciona el nivel de asimilación, redacta las incidencias pedagógicas y presiona el botón `"Guardar y Firmar Bitácora"`. | **4.** En `BitacoraFormView.tsx`, se valida que las observaciones pedagógicas posean una extensión mínima de 50 caracteres y no contengan scripts. En `bitacoraService.ts`, se despacha `POST /api/v1/sessions/{id}/bitacora` con el payload `BitacoraCreateRequest`. En `bitacora.py`, `BitacoraService.create_bitacora` valida la firma del mentor y el esquema de datos. (Si la descripción pedagógica no alcanza el mínimo de 50 caracteres, salta a E002). |
| **Fase 3: Persistencia transaccional y certificación de horas** | |
| **5.** El mentor observa la barra de progreso mientras se genera el hash de integridad de la bitácora. | **6.** En `bitacora_service.py`, se calcula el hash criptográfico SHA-256 sobre el contenido pedagógico y se ejecuta `INSERT INTO bitacoras_pedagogicas (sesion_id, mentor_id, temas_cubiertos, observaciones, nivel_dificultad, hash_firma, fecha_registro) VALUES (...)`. Se actualiza `sesiones_mentoria.estado = 'BITACORA_REGISTRADA'`. Se confirma la transacción con `db.commit()` y se retorna HTTP 201 Created. En cliente, `BitacoraFormView.tsx` muestra un panel de confirmación en color verde con el código de firma digital y redirige al historial de sesiones. |

##### Flujos de Excepción

##### Flujo de excepción E001: Plazo límite de 48 horas vencido
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `bitacora_service.py` evalúa `now_utc > sesion.fecha_fin + timedelta(hours=48)`. Lanza `HTTPException(status_code=400, detail="DEADLINE_EXCEEDED: El plazo reglamentario de 48 horas para registrar la bitácora ha vencido.")`.<br><br>En `BitacoraFormView.tsx`, se deshabilita la edición del formulario y se muestra una advertencia en color rojo indicando que la bitácora quedó fuera de plazo reglamentario y requiere solicitud de desbloqueo administrativo ante la Dirección de Escuela. |
| **E001-1.2** Hace clic en el botón "Solicitar Desbloqueo a Coordinación". | **E001-1.3** Abre un formulario de solicitud de prórroga y finaliza la interacción sin registrar la bitácora ordinaria. |

##### Flujo de excepción E002: Descripción pedagógica insuficiente o vacía
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, el validador Pydantic en `bitacora.py` comprueba que el campo de observaciones tiene menos de 50 caracteres. Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: Las observaciones pedagógicas deben contener una descripción sustantiva de al menos 50 caracteres.")`.<br><br>En `BitacoraFormView.tsx`, se resalta el cuadro de texto en color rojo y se muestra un contador de caracteres indicando los faltantes. |
| **E002-1.2** Amplía la descripción pedagógica detallando el desarrollo de la sesión hasta superar los 50 caracteres. | **E002-1.3** Actualiza el contador de caracteres en la interfaz y retorna al paso 3 del Flujo Normal de Eventos. |

#### CUS-014 - Visualizar historial y bitácoras académicas

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-014** (CUS-014) |
| **Nombre** | Visualizar historial académico integral de sesiones y bitácoras pedagógicas |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-019 (Consulta de historial cronológico individual de sesiones y asistencias) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor, Estudiante Mentoreado, Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 05 - Sprint 06 |
| **Descripción** | Permite a los usuarios consultar su trayectoria histórica dentro del programa de mentorías académicas a través del componente cliente `HistorySessionsView.tsx` y el servicio `historyService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/history.py` y `app/services/history_service.py` procesan las peticiones `GET /api/v1/history/sessions` y `GET /api/v1/history/bitacora/{session_id}`. Para los mentoreados, el sistema presenta la relación cronológica de sesiones a las que asistió con sus comprobantes y temas repasados. Para los mentores, despliega las sesiones impartidas, las bitácoras pedagógicas suscritas con su hash de firma digital y el estado de validación de horas ante la Dirección de Escuela. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-06: Trazabilidad, Bitácoras y Evaluación)<br>Reglamento Académico de Seguimiento Estudiantil EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/HistorySessionsView.tsx`<br>`aplicacion/frontend/src/services/historyService.ts` (`HistoryService`, `ApiHistoryAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/history.py` (`GET /api/v1/history/sessions`, `GET /api/v1/history/bitacora/{session_id}`)<br>`aplicacion/backend/app/services/history_service.py` (`HistoryService.get_user_history`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`), `app/models/bitacora.py` (`BitacoraPedagogica`), `app/models/attendance.py` (`AsistenciaSesion`) |
| **Precondiciones** | 1. Usuario institucional autenticado con token JWT activo en la plataforma.<br>2. Registros históricos persistidos en las tablas de sesiones, bitácoras o asistencias. |
| **PostCondiciones** | 1. Respuesta JSON paginada con el historial cronológico y metadatos pedagógicos retornada al cliente.<br>2. Operación idempotente de lectura sin alteraciones destructivas en la base de datos.<br>3. Renderizado de la línea de tiempo interactiva con opciones de filtrado por ciclo y asignatura. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del historial y aplicación de filtros cronológicos** | |
| **1.** El usuario hace clic en `"Mi Historial"` en el menú lateral de navegación de `HistorySessionsView.tsx`. | **2.** En `historyService.ts`, se despacha `GET /api/v1/history/sessions` enviando el token institucional. En `history.py`, `HistoryService.get_user_history` recupera las sesiones en que el usuario participó (como mentor o mentoreado) ordenadas de forma cronológica descendente. Retorna HTTP 200 con la nómina histórica. `HistorySessionsView.tsx` renderiza las tarjetas de sesiones en una línea de tiempo interactiva con distintivos por estado (`Concluida`, `Bitácora Registrada`, `Visada`). (Si el usuario es nuevo y no registra historial de sesiones, salta a A001). |
| **Fase 2: Búsqueda y filtrado por materia o período académico** | |
| **3.** El usuario filtra por semestre académico o escribe el nombre de una materia en el cuadro de búsqueda. | **4.** En `HistorySessionsView.tsx`, se actualiza reactivamente la lista de tarjetas en pantalla. El usuario hace clic sobre una sesión concluida para consultar el detalle pedagógico. |
| **Fase 3: Visualización de bitácora pedagógica y comprobante de asistencia** | |
| **5.** El usuario presiona el botón `"Ver Bitácora Pedagógica"` en la tarjeta seleccionada. | **6.** En `historyService.ts`, se despacha `GET /api/v1/history/bitacora/{session_id}`. El backend valida los permisos de lectura y retorna el registro de `BitacoraPedagogica` incluyendo los temas abordados, el nivel de dificultad, las observaciones y la firma digital SHA-256. `HistorySessionsView.tsx` despliega una ventana modal con el desglose formal de la bitácora y el botón de exportación en formato legible. |

##### Flujos Alternativos

##### Flujo alternativo A001: Historial académico vacío para usuario nuevo
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 2 del Flujo Normal, la consulta histórica retorna cero registros para el usuario. | **A001-1.2** En `HistorySessionsView.tsx`, se despliega un panel amigable en color azul institucional con el mensaje: *"Aún no registras sesiones de mentoría en tu historial. Comienza explorando la cartelera de recomendaciones para inscribirte en un tema"*. Presenta el botón `<button onClick={handleGoToBillboard}>Explorar Cartelera</button>`. |
| **A001-1.3** El usuario hace clic en el botón "Explorar Cartelera". | **A001-1.4** El sistema redirige al componente `RecommendationFeedView.tsx` y retorna al paso 1 del Flujo Normal de Eventos de CUS-002. |


---

### MOD-07: Gamificación e Incentivos

#### CUS-018 - Emitir constancia institucional de horas de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-018** (CUS-018) |
| **Nombre** | Emitir constancia oficial de horas de mentoría con firma criptográfica y QR |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-022 (Parametrización institucional de umbrales y emisión de certificados), RF-023 (Descarga y verificación institucional de certificados); RN-14 (Umbral mínimo de 20 horas acreditadas con bitácoras visadas) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional, Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 - Sprint 07 |
| **Descripción** | Permite a los estudiantes mentores solicitar y descargar una constancia institucional de horas de mentoría acreditadas una vez alcanzado el umbral reglamentario de 20 horas efectivas de dictado (RN-14) con bitácoras pedagógicas debidamente registradas y visadas por la administración. El componente `CertificateView.tsx` despacha la solicitud mediante `POST /api/v1/certificates/generate` hacia el backend en `aplicacion/backend/app/api/v1/endpoints/certificates.py`. El servicio `CertificateService` verifica en base de datos la suma de horas dictadas (`SUM(duracion_minutos)/60 >= 20`), genera un código de serie alfanumérico único, calcula el sello criptográfico SHA-256 del documento, genera un código QR de verificación institucional que apunta al validador público de la universidad, y compila el documento en formato PDF. Persiste la entidad `CertificadoHoras` (`app/models/certificate.py`) y retorna el identificador del archivo para su descarga segura. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-07: Gamificación, Reputación y Certificación)<br>Reglamento de Prácticas Pre-Profesionales y Responsabilidad Social EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/CertificateView.tsx`<br>`aplicacion/frontend/src/services/certificateService.ts` (`CertificateService`, `ApiCertificateAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/certificates.py` (`POST /api/v1/certificates/generate`, `GET /api/v1/certificates/{id}/download`, `GET /api/v1/certificates/verify/{code}`)<br>`aplicacion/backend/app/services/certificate_service.py` (`CertificateService.generate_certificate`, `CertificateService.verify_code`)<br>`aplicacion/backend/app/models/certificate.py` (`CertificadoHoras`), `app/models/bitacora.py` (`BitacoraPedagogica`), `app/models/auth.py` (`Usuario`) |
| **Precondiciones** | 1. Estudiante mentor autenticado con token JWT institucional activo.<br>2. Suma acumulada de al menos 20 horas de mentoría con bitácoras pedagógicas aprobadas en el semestre.<br>3. Inexistencia de constancia duplicada activa para el mismo período académico. |
| **PostCondiciones** | 1. Registro insertado en la tabla física `certificados_horas` con código de verificación alfanumérico y hash SHA-256.<br>2. Archivo PDF estructurado generado en almacenamiento seguro con código QR embebido.<br>3. Despliegue del botón de descarga directa y registro del evento en la auditoría institucional. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de acumulado de horas y verificación de umbral** | |
| **1.** El estudiante mentor accede a `"Mis Certificados"` en `CertificateView.tsx`. | **2.** En `certificateService.ts`, se despacha `GET /api/v1/certificates/summary`. En `certificates.py`, `CertificateService` ejecuta `SELECT sum(s.duracion_minutos)/60.0 as horas_totales FROM sesiones_mentoria s JOIN bitacoras_pedagogicas b ON s.id = b.sesion_id WHERE s.id_mentor = :mid AND s.estado = 'BITACORA_REGISTRADA'`. Retorna HTTP 200 con el total de horas acumuladas. En `CertificateView.tsx`, se renderiza una barra de progreso porcentual hacia la meta reglamentaria de 20 horas (RN-14) en color azul institucional. Si las horas son iguales o mayores a 20, se habilita el botón `"Emitir Constancia Oficial"`. (Si el total de horas acumuladas es menor a 20, salta a E001). |
| **Fase 2: Solicitud de emisión y previsualización de datos** | |
| **3.** El mentor presiona el botón `"Emitir Constancia Oficial"`. | **4.** En `CertificateView.tsx`, se abre una ventana modal de previsualización que muestra: nombres completos del mentor, código universitario, semestre académico, total de horas acreditadas y una vista preliminar del código QR de validación. El mentor verifica sus datos y presiona el botón `"Confirmar y Generar PDF Cifrado"`. |
| **Fase 3: Generación criptográfica, persistencia y descarga del PDF** | |
| **5.** El mentor observa la animación de compilación segura del documento. | **6.** En `certificateService.ts`, se despacha `POST /api/v1/certificates/generate` con el período semestral. En `certificates.py`, `CertificateService.generate_certificate` inicia una transacción ACID. Genera un identificador alfanumérico único (e.g. `UPT-EPIS-2026-I-0042`), calcula el hash de integridad SHA-256 de los datos y compila el documento PDF oficial incorporando membrete institucional, firma digital del Director de Escuela y código QR de verificación web. Inserta el registro en `certificados_horas`, ejecuta `db.commit()` y retorna HTTP 201 Created con el payload del certificado. En cliente, `CertificateView.tsx` renderiza la vista previa del documento y habilita el botón de descarga directa en formato PDF. |

##### Flujos de Excepción

##### Flujo de excepción E001: Horas acreditadas insuficientes para el umbral institucional
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `CertificateService` comprueba que el acumulado de horas con bitácoras registradas es menor a 20 (`horas_totales < 20.0`). Lanza `HTTPException(status_code=400, detail="INSUFFICIENT_HOURS: Requiere al menos 20 horas de mentoría con bitácora registrada para emitir la constancia oficial (Horas actuales: {horas_totales}).")`.<br><br>En `CertificateView.tsx`, se mantiene el botón de emisión deshabilitado y se despliega un panel informativo en color ámbar indicando las horas faltantes para alcanzar la certificación. |
| **E001-1.2** Hace clic en el botón "Ver Sesiones Pendientes". | **E001-1.3** Redirige a la vista de sesiones para completar bitácoras pendientes y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-019 - Gestionar insignias y reputación gamificada

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-019** (CUS-019) |
| **Nombre** | Gestionar insignias de logro formativo y reputación gamificada de mentores |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-021 (Cálculo dinámico de reputación y visualización de insignias); RN-13 (Gamificación: puntaje por calificaciones, asistencias y puntualidad) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor, Estudiante Mentoreado |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 - Sprint 07 |
| **Descripción** | Permite a la comunidad académica visualizar el progreso, insignias de honor alcanzadas y nivel de reputación formativa de los mentores mediante el componente cliente `GamificationView.tsx` y el servicio `gamificationService.ts`. El backend en `aplicacion/backend/app/api/v1/endpoints/gamification.py` y `app/services/reputation_service.py` expone las consultas de logros `GET /api/v1/gamification/badges` y el cuadro de honor `GET /api/v1/gamification/leaderboard`. El motor de reputación calcula periódicamente el puntaje global $R = 0.5 	imes ValoracionPromedio + 0.3 	imes HorasAcreditadas + 0.2 	imes TasaPuntualidad$ (RN-13), desbloqueando automáticamente insignias de nivel (tales como "Mentor Destacado", "Puntualidad Impecable" y "Especialista en Algoritmos") en la tabla física `insignias_usuarios` (`app/models/gamification.py`), fomentando la participación y el compromiso entre pares. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-07: Gamificación, Reputación y Certificación)<br>Estrategias de Gamificación en la Educación Superior Universitaria |
| **Anexos** | `aplicacion/frontend/src/components/GamificationView.tsx`<br>`aplicacion/frontend/src/services/gamificationService.ts` (`GamificationService`, `ApiGamificationAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/gamification.py` (`GET /api/v1/gamification/badges`, `GET /api/v1/gamification/leaderboard`)<br>`aplicacion/backend/app/services/reputation_service.py` (`ReputationService.get_user_badges`, `ReputationService.calculate_rank`)<br>`aplicacion/backend/app/models/gamification.py` (`Insignia`, `InsigniaUsuario`, `ReputacionUsuario`) |
| **Precondiciones** | 1. Usuario institucional autenticado en la plataforma.<br>2. Catálogo de insignias y reglas de desbloqueo configuradas en la base de datos.<br>3. Registro de calificaciones de sesiones o asistencias efectivas en el sistema. |
| **PostCondiciones** | 1. Nómina de insignias obtenidas y bloqueadas con porcentaje de avance retornadas en JSON.<br>2. Tabla de clasificación (leaderboard) calculada en tiempo real de sólo lectura.<br>3. Despliegue interactivo en la interfaz con animación de logros y posición en el cuadro de honor. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de insignias personales y progreso de nivel** | |
| **1.** El usuario hace clic en el enlace `"Insignias y Reputación"` en `GamificationView.tsx`. | **2.** En `gamificationService.ts`, se despacha `GET /api/v1/gamification/badges`. En `gamification.py`, `ReputationService` consulta la tabla `insignias_usuarios` unida con `insignias` para el usuario y calcula las métricas de avance hacia las insignias bloqueadas. Retorna HTTP 200 con el listado completo. En `GamificationView.tsx`, se renderiza una vitrina virtual: las insignias desbloqueadas se muestran en color dorado con su fecha de concesión, y las bloqueadas en color gris con una barra de progreso que indica el porcentaje completado. |
| **Fase 2: Exploración de criterios de logro y detalle de insignia** | |
| **3.** El usuario hace clic sobre una insignia específica (e.g. "Mentor Destacado"). | **4.** En `GamificationView.tsx`, se despliega un panel lateral interactivo con el nombre de la insignia, descripción pedagógica, icono gráfico y requisitos de desbloqueo (e.g. *"Haber dictado más de 10 sesiones con calificación promedio mayor o igual a 4.8 estrellas"*). |
| **Fase 3: Visualización del cuadro de honor institucional (Leaderboard)** | |
| **5.** El usuario hace clic en la pestaña `"Cuadro de Honor de la Escuela"`. | **6.** En `gamificationService.ts`, se despacha `GET /api/v1/gamification/leaderboard`. El backend recupera el Top-10 de mentores clasificados por puntaje de reputación global calculados bajo RN-13. Retorna HTTP 200 con los nombres, cursos y puntuación. `GamificationView.tsx` renderiza la tabla clasificatoria destacando a los tres primeros lugares con medallas de honor, e indicando la posición del usuario en el ranking general con un marco en color azul institucional. (Si el usuario ha configurado su perfil en modo privado con alias anónimo, salta a A001). |

##### Flujos Alternativos

##### Flujo alternativo A001: Visualización en el cuadro de honor con alias anónimo
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 6 del Flujo Normal, el usuario tiene activada la opción de privacidad en su perfil institucional. | **A001-1.2** En `gamification.py`, `ReputationService` anonimiza los datos personales del usuario reemplazando sus nombres oficiales por un seudónimo aleatorio o su código universitario parcial (e.g. *"Mentor EPIS-742"*). |
| **A001-1.3** El usuario visualiza su puntaje de reputación en el ranking garantizando la confidencialidad de su identidad ante terceros. | **A001-1.4** El sistema muestra el interruptor de visibilidad para permitir conmutar a nombre público en cualquier momento y retorna al paso 6 del Flujo Normal de Eventos. |


---

### MOD-08: Analítica, Notificaciones y Configuración

#### CUS-009 - Notificar eventos críticos y alertas temporales

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-009** (CUS-009) |
| **Nombre** | Notificar eventos críticos y alertas de confirmación a T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-015 (Monitoreo desatendido, emisión de recordatorios y alertas); RN-04 (Antelación de 24 horas), RN-10 (Control de asistencia y quórum institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Proceso Planificador (`SchedulerWorker`), Estudiante Mentor, Estudiante Mentoreado, Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite transmitir notificaciones asíncronas y alertas en tiempo real a los usuarios institucionales ante eventos críticos del ciclo de vida de las sesiones de mentoría (tales como recordatorios de ratificación de asistencia a T-24h, confirmación oficial de quórum, reprogramación o cancelación contingente). El frontend gestiona las alertas reactivas a través del componente `NotificationBell.tsx` y el servicio `notificationService.ts`, conectándose al canal de Server-Sent Events (SSE) `/api/v1/notifications/stream`. El backend `aplicacion/backend/app/api/v1/endpoints/notifications.py` y `app/services/notification_service.py` procesan eventos generados por tareas programadas de Celery/APScheduler, persisten la entidad `NotificacionEvento` (`app/models/notification.py`) en PostgreSQL y despachan simultáneamente correos electrónicos de respaldo vía SMTP universitario (`EmailService`), garantizando la notificación oportuna a mentores y estudiantes. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Estándar W3C Server-Sent Events y Protocolo SMTP RFC 5321 |
| **Anexos** | `aplicacion/frontend/src/components/NotificationBell.tsx`<br>`aplicacion/frontend/src/services/notificationService.ts` (`NotificationService`, `ApiNotificationAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/notifications.py` (`GET /api/v1/notifications/unread`, `POST /api/v1/notifications/{id}/mark-read`, `GET /api/v1/notifications/stream`)<br>`aplicacion/backend/app/services/notification_service.py` (`NotificationService.dispatch_event`, `NotificationService.get_unread`)<br>`aplicacion/backend/app/models/notification.py` (`NotificacionEvento`), `app/models/auth.py` (`Usuario`) |
| **Precondiciones** | 1. Usuario institucional autenticado con token JWT activo en la plataforma.<br>2. Evento de dominio generado en backend (e.g. evaluación de quórum, reserva formalizada, cancelación).<br>3. Servicio SMTP institucional o canal SSE operativo en el servidor. |
| **PostCondiciones** | 1. Registro insertado en la tabla física `notificaciones_eventos` con `leida = false` y marca temporal UTC.<br>2. Transmisión reactiva del mensaje a la campana de notificaciones de la interfaz cliente.<br>3. Despacho de correo electrónico de respaldo al buzón universitario del destinatario. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Conexión al canal de notificaciones e inicialización de alertas** | |
| **1.** El usuario inicia sesión en la plataforma y visualiza el componente de campana en la cabecera `NotificationBell.tsx`. | **2.** En `notificationService.ts`, se establece una conexión persistente SSE con `GET /api/v1/notifications/stream` y se despacha `GET /api/v1/notifications/unread`. En `notifications.py`, `NotificationService` consulta `SELECT * FROM notificaciones_eventos WHERE usuario_id = :uid AND leida = false ORDER BY fecha_creacion DESC`. Retorna HTTP 200 con la nómina de alertas pendientes. En `NotificationBell.tsx`, se renderiza una insignia numérica en color rojo sobre la campana indicando las notificaciones no leídas. |
| **Fase 2: Generación asíncrona de evento crítico y despacho multicanal** | |
| **3.** Un proceso del sistema en segundo plano (e.g. evaluación de quórum a T-24h en CUS-023) detecta la necesidad de alertar al usuario. | **4.** En `notification_service.py`, se invoca `dispatch_event(user_id, event_type, message, reference_id)`. Se ejecuta `INSERT INTO notificaciones_eventos (...) VALUES (...)` y se emite el evento al flujo SSE. Simultáneamente, se invoca a `EmailService.send_alert_email()` para despachar el aviso a su correo `@upt.pe`. (Si el servidor SMTP sufre timeout o indisponibilidad de red, salta a E001). |
| **Fase 3: Recepción reactiva en cliente y lectura de notificación** | |
| **5.** El usuario observa la actualización instantánea del contador en la campana y hace clic sobre el icono `NotificationBell.tsx`. | **6.** En `NotificationBell.tsx`, se abre un panel flotante desplegando las alertas ordenadas cronológicamente con distintivos de criticidad (Informativa, Alerta T-24h, Urgente). El usuario hace clic sobre una alerta específica (e.g. *"Tu sesión de mañana ha sido confirmada"*). En `notificationService.ts`, se despacha `POST /api/v1/notifications/{id}/mark-read`. El backend actualiza `leida = true` en base de datos. El sistema disminuye el contador y redirige al usuario a la vista de la sesión referenciada. |

##### Flujos de Excepción

##### Flujo de excepción E001: Falla de despacho en el servicio SMTP de respaldo
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, la pasarela de correo SMTP universitario no responde o rechaza la conexión. `EmailService` captura la excepción `SMTPException`, registra una advertencia en la bitácora de auditoría del servidor (`logger.warning("SMTP dispatch failed, falling back to SSE only")`) y preserva la entrega mediante el canal web en tiempo real sin abortar la transacción de base de datos.<br><br>En `NotificationBell.tsx`, el usuario recibe la notificación instantánea en pantalla de forma normal, manteniendo la continuidad operativa. |
| **E001-1.2** Hace clic en la campana de notificaciones y lee el mensaje directamente en la aplicación. | **E001-1.3** Marca la notificación como leída y retorna al paso 6 del Flujo Normal de Eventos. |

#### CUS-011 - Generar reportes e indicadores de analítica académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-011** (CUS-011) |
| **Nombre** | Generar reportes consolidados e indicadores analíticos de gestión de mentorías |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-025 (Tablero analítico y métricas de rendimiento académico) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional (`UserRole.administrador`), Director de Escuela EPIS, Comité de Calidad ICACIT |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a las autoridades académicas y evaluadores de acreditación generar informes estadísticos agregados sobre la cobertura, demanda y efectividad del programa de mentorías entre pares mediante el componente cliente `AnalyticsDashboardView.tsx` y el servicio `analyticsService.ts`. El backend en `aplicacion/backend/app/api/v1/endpoints/analytics.py` y `app/services/analytics_service.py` procesa las peticiones `GET /api/v1/analytics/reports/kpis` y `GET /api/v1/analytics/export`. El servicio ejecuta consultas analíticas relacionales en PostgreSQL agrupando métricas por asignatura filtro, ciclo y modalidad (horas dictadas, porcentaje de asistencia efectiva, quórum promedio alcanzado y tasa de demanda no atendida). Permite descargar el consolidado en formato de hoja de cálculo estructurada (`.xlsx` o `.csv`) con metadatos de auditoría institucional. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Criterio 4 ICACIT: Evaluación y Mejora Continua |
| **Anexos** | `aplicacion/frontend/src/components/AnalyticsDashboardView.tsx`<br>`aplicacion/frontend/src/services/analyticsService.ts` (`AnalyticsService`, `ApiAnalyticsAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/analytics.py` (`GET /api/v1/analytics/reports/kpis`, `GET /api/v1/analytics/export`)<br>`aplicacion/backend/app/services/analytics_service.py` (`AnalyticsService.calculate_kpis`, `AnalyticsService.export_report`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`), `app/models/attendance.py` (`AsistenciaSesion`), `app/models/curriculum.py` (`Curso`) |
| **Precondiciones** | 1. Usuario autenticado con rol `UserRole.administrador` o directivo verificado en JWT.<br>2. Datos de sesiones, asistencias y demandas registradas en el semestre académico consultado.<br>3. Parámetros de rango de fechas válidos dentro del calendario lectivo. |
| **PostCondiciones** | 1. Conjunto estructurado de KPIs retornado en JSON y renderizado en gráficos analíticos.<br>2. Flujo binario de hoja de cálculo generado y descargado en el navegador del usuario.<br>3. Registro de auditoría administrativa persistido en el sistema. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al panel analítico y configuración de parámetros** | |
| **1.** El administrador accede al panel de reportes en `AnalyticsDashboardView.tsx`. | **2.** En `analyticsService.ts`, se despacha `GET /api/v1/analytics/reports/kpis?semester=2026-I`. En `analytics.py`, `AnalyticsService.calculate_kpis` ejecuta consultas agregadas: total de sesiones ejecutadas, horas pedagógicas acumuladas, tasa global de asistencia efectiva y distribución porcentual por modalidad (Presencial vs Virtual). Retorna HTTP 200 con el resumen estadístico. En `AnalyticsDashboardView.tsx`, se renderizan tarjetas de indicadores clave y gráficos de barras comparativos en color azul institucional. |
| **Fase 2: Ajuste de filtros temporales y selección de formato de exportación** | |
| **3.** El usuario ajusta el rango de fechas en los selectores de inicio y fin, elige una asignatura filtro específica y selecciona el formato de salida (`Excel .xlsx` o `CSV`). | **4.** En `AnalyticsDashboardView.tsx`, se validan las fechas seleccionadas verificando que la fecha de inicio no sea posterior a la fecha de fin ni exceda la fecha actual. El usuario presiona el botón `"Exportar Informe Consolidado"`. (Si el rango de fechas es inconsistente o futuro, salta a E001). |
| **Fase 3: Generación del documento analítico y descarga segura** | |
| **5.** El usuario observa el indicador circular de compilación del reporte en el botón de exportación. | **6.** En `analyticsService.ts`, se despacha `GET /api/v1/analytics/export?format=xlsx&start_date=...&end_date=...`. En `analytics.py`, `AnalyticsService.export_report` compila el libro de cálculo estructurado con pestañas de: 1) Resumen Ejecutivo de KPIs, 2) Detalle de Sesiones Impartidas, 3) Registro Consolidado de Asistencias, y 4) Análisis de Materias Críticas. Retorna la respuesta binaria con cabecera `Content-Disposition: attachment; filename="Reporte_Mentorias_EPIS.xlsx"`. El navegador del usuario inicia la descarga automática del archivo y el sistema registra la traza de auditoría. |

##### Flujos de Excepción

##### Flujo de excepción E001: Rango de fechas inconsistente o futuro
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el validador en cliente o `analytics.py` comprueba que la fecha inicial es mayor a la final o que se ingresaron fechas futuras no transcurridas. Lanza `HTTPException(status_code=400, detail="INVALID_DATE_RANGE: El rango de fechas seleccionado es inconsistente o corresponde a períodos futuros.")`.<br><br>En `AnalyticsDashboardView.tsx`, se resaltan los campos de fecha en color rojo y se muestra una notificación de advertencia en color ámbar. |
| **E001-1.2** Modifica las fechas seleccionando un período semestral válido. | **E001-1.3** Actualiza los valores en la interfaz y retorna al paso 3 del Flujo Normal de Eventos. |

#### CUS-015 - Consultar métricas de retención y desempeño

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-015** (CUS-015) |
| **Nombre** | Consultar métricas de correlación de retención estudiantil y desempeño académico |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-025 (Tablero analítico y métricas de rendimiento académico); Criterios ICACIT de retención y graduación oportuna |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional, Comisión de Acreditación ICACIT, Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a los comités de calidad educativa evaluar el impacto del programa de mentorías en la retención estudiantil y en la reducción del índice de reprobación en materias filtro a través del componente cliente `RetentionDashboardView.tsx` y el servicio `analyticsService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/analytics.py` procesa las peticiones `GET /api/v1/analytics/retention/cohorts` y `GET /api/v1/analytics/retention/impact`. El servicio analiza estadísticamente las cohortes estudiantiles, calculando la correlación entre la participación recurrente en mentorías (asistencia >= 3 sesiones) y la tasa de aprobación de las asignaturas críticas (Cálculo, Física, Algoritmos, Estructuras de Datos). Presenta comparativas entre grupos de control (estudiantes no asistentes) y grupos participantes para respaldar las auditorías ICACIT. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Modelo de Calidad y Acreditación de Programas de Ingeniería ICACIT |
| **Anexos** | `aplicacion/frontend/src/components/RetentionDashboardView.tsx`<br>`aplicacion/frontend/src/services/analyticsService.ts` (`AnalyticsService.getRetentionMetrics`)<br>`aplicacion/backend/app/api/v1/endpoints/analytics.py` (`GET /api/v1/analytics/retention/cohorts`, `GET /api/v1/analytics/retention/impact`)<br>`aplicacion/backend/app/services/analytics_service.py` (`AnalyticsService.analyze_retention_correlation`)<br>`aplicacion/backend/app/models/attendance.py` (`AsistenciaSesion`), `app/models/curriculum.py` (`Curso`), `app/models/profile.py` (`PerfilAcademico`) |
| **Precondiciones** | 1. Usuario con credenciales administrativas o de evaluador de calidad.<br>2. Registros de calificaciones o actas académicas consolidadas de asignaturas filtro en el semestre.<br>3. Mínimo de registros estadísticos requeridos para inferencia de correlación. |
| **PostCondiciones** | 1. Métricas de retención, tasa de deserción relativa e impacto en aprobación retornadas en JSON.<br>2. Consulta de lectura analítica sin modificación de registros académicos oficiales.<br>3. Visualización de gráficos de dispersión y comparativas de cohortes en la interfaz. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al módulo de impacto y selección de cohorte** | |
| **1.** El evaluador de calidad accede a `"Impacto y Retención Académica"` en `RetentionDashboardView.tsx`. | **2.** En `analyticsService.ts`, se despacha `GET /api/v1/analytics/retention/impact`. En `analytics.py`, `AnalyticsService.analyze_retention_correlation` ejecuta la consulta de comparación: calcula el porcentaje de aprobación de estudiantes que recibieron mentoría versus el grupo de estudiantes que no participó en el programa. Retorna HTTP 200. En `RetentionDashboardView.tsx`, se renderiza un gráfico comparativo de barras dobles y un panel con la estimación de reducción del riesgo de reprobación en color azul institucional. |
| **Fase 2: Segmentación por asignatura filtro y período lectivo** | |
| **3.** El usuario selecciona una asignatura filtro específica (e.g. Estructuras de Datos) en la lista desplegable de materias y presiona `"Calcular Índice de Impacto"`. | **4.** En `RetentionDashboardView.tsx`, se envía la consulta parametrizada. En `analytics.py`, se evalúa el tamaño muestral de la asignatura. Si el número de estudiantes evaluados es suficiente (al menos 10 registros), se calcula el coeficiente de correlación y la significancia estadística. (Si la muestra disponible es menor a 10 registros estadísticos, salta a A001). |
| **Fase 3: Visualización de indicadores ICACIT y exportación** | |
| **5.** El usuario revisa los indicadores de logro académico y presiona el botón `"Exportar Evidencia ICACIT"`. | **6.** El sistema genera un resumen analítico con la tasa de retención estudiantil, la tabla de frecuencias de asistencia y las firmas de integridad del informe, descargando el archivo en formato PDF oficial para su incorporación en el expediente de acreditación. |

##### Flujos Alternativos

##### Flujo alternativo A001: Muestra insuficiente para análisis estadístico
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 4 del Flujo Normal, el servicio detecta que la asignatura seleccionada cuenta con menos de 10 estudiantes participantes en el semestre analizado. | **A001-1.2** En `RetentionDashboardView.tsx`, se despliega un panel en color ámbar: *"Muestra preliminar insuficiente para inferencia estadística significativa (< 10 registros). Se presentan únicamente métricas descriptivas básicas"*. |
| **A001-1.3** El evaluador visualiza las frecuencias absolutas sin la estimación de correlación inferencial. | **A001-1.4** El sistema ofrece la opción de ampliar el rango temporal a semestres anteriores y retorna al paso 3 del Flujo Normal de Eventos. |

#### CUS-016 - Auditar trazas de seguridad y consentimiento Ley 29733

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-016** (CUS-016) |
| **Nombre** | Auditar trazas inmutables de seguridad y consentimientos legales digitales |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-026 (Auditoría administrativa de bitácoras, accesos y seguridad); RN-02 (Registro inmutable de consentimiento legal digital Ley Nº 29733) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Oficial de Seguridad de la Información (`UserRole.administrador`), Delegado de Protección de Datos |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a los oficiales de seguridad y autoridades universitarias inspeccionar las trazas de auditoría inmutables del sistema y verificar el estricto cumplimiento de la Ley Nº 29733 (Protección de Datos Personales del Perú) mediante el componente `AuditLogView.tsx` y el servicio `auditService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/audit.py` y `app/services/audit_service.py` exponen los endpoints `GET /api/v1/audit/logs`, `GET /api/v1/audit/consent-traces` y `POST /api/v1/audit/verify-chain`. El sistema verifica la integridad criptográfica de la cadena de bloques o hashes encadenados de auditoría (donde cada registro contiene el SHA-256 del registro anterior), garantizando la no alteración de eventos críticos (inicios de sesión 2FA, modificaciones de roles, aceptaciones y revocaciones de consentimiento legal con direcciones IP y marcas temporales UTC). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Ley Nº 29733 de Protección de Datos Personales y Estándar ISO/IEC 27001 |
| **Anexos** | `aplicacion/frontend/src/components/AuditLogView.tsx`<br>`aplicacion/frontend/src/services/auditService.ts` (`AuditService`, `ApiAuditAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/audit.py` (`GET /api/v1/audit/logs`, `GET /api/v1/audit/consent-traces`, `POST /api/v1/audit/verify-chain`)<br>`aplicacion/backend/app/services/audit_service.py` (`AuditService.get_logs`, `AuditService.verify_chain_integrity`)<br>`aplicacion/backend/app/models/consent.py` (`ConsentimientoLegal`), `app/models/auth.py` (`LogAuditoriaSeguridad`) |
| **Precondiciones** | 1. Usuario autenticado portando token JWT institucional con privilegios de Oficial de Seguridad o Administrador.<br>2. Registros de auditoría y trazas de consentimiento persistidos en la base de datos PostgreSQL.<br>3. Claves criptográficas institucionales de verificación activas en el servidor. |
| **PostCondiciones** | 1. Verificación de integridad de la cadena de hashes ejecutada sin detectar corrupciones.<br>2. Consulta forense de sólo lectura generada con registros paginados e inmutables.<br>3. Exportación de expediente de trazabilidad bajo la Ley Nº 29733 con firma digital de auditoría. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del registro forense de auditoría** | |
| **1.** El oficial de seguridad accede al módulo `"Auditoría de Seguridad y Ley 29733"` en `AuditLogView.tsx`. | **2.** En `auditService.ts`, se despacha `GET /api/v1/audit/logs?limit=50`. En `audit.py`, se valida el token con `require_security_officer_role`. `AuditService` ejecuta `SELECT l.*, u.email FROM log_auditoria_seguridad l JOIN usuarios u ON l.usuario_id = u.id ORDER BY l.id DESC LIMIT 50`. Retorna HTTP 200 con la nómina paginada. En `AuditLogView.tsx`, se renderiza una tabla con filtros por fecha, tipo de evento (`AUTH_2FA`, `ROLE_CHANGE`, `CONSENT_ACCEPT`, `CONSENT_REVOKE`), IP de origen y hash de bloque. (Si el usuario no cuenta con privilegios de seguridad, salta a E001). |
| **Fase 2: Filtrado por usuario y verificación de traza legal de consentimiento** | |
| **3.** El oficial introduce el correo institucional de un estudiante o docente en el buscador para auditar su historial de consentimiento digital. | **4.** En `auditService.ts`, se despacha `GET /api/v1/audit/consent-traces?email=...`. El backend retorna la secuencia completa de formalización: UUID, versión de términos aceptada, IP de origen, User-Agent, fecha UTC y estado de revocación. `AuditLogView.tsx` despliega el expediente digital del titular de los datos. |
| **Fase 3: Verificación criptográfica de la cadena de auditoría (Hash Chain)** | |
| **5.** El oficial presiona el botón `"Verificar Integridad de Cadena de Logs"`. | **6.** En `auditService.ts`, se despacha `POST /api/v1/audit/verify-chain`. En `audit_service.py`, se itera secuencialmente por la tabla de auditoría recomputando recursivamente `SHA256(registro_anterior_hash + registro_actual_data)` y comparándolo con el valor almacenado en `hash_bloque`. Al comprobar que todas las firmas coinciden, retorna HTTP 200 `{"status": "VALID", "records_verified": count, "tampering_detected": false}`. En `AuditLogView.tsx`, se despliega una insignia destacada en color verde con la leyenda *"Cadena de Auditoría Íntegra y Verificada (0 Alteraciones)"* y se habilita el botón de exportación de expediente legal. (Si el sistema detecta una inconsistencia en la cadena de hashes, salta a E002). |

##### Flujos de Excepción

##### Flujo de excepción E001: Permisos insuficientes para auditoría de seguridad
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, el interceptor de seguridad en `audit.py` comprueba que el token JWT carece de rol de Oficial de Seguridad o Administrador Institucional. Lanza `HTTPException(status_code=403, detail="FORBIDDEN_AUDIT: Acceso restringido. Se requieren credenciales de Oficial de Seguridad para auditar registros forenses.")`.<br><br>En `App.tsx`, se captura el error 403 y se redirige al panel estándar del usuario desplegando una alerta en color rojo. |
| **E001-1.2** Hace clic en el botón "Aceptar" en la alerta de restricción. | **E001-1.3** Cierra el aviso y retorna al paso 1 del Flujo Normal de Eventos en su vista autorizada. |

##### Flujo de excepción E002: Inconsistencia detectada en la cadena criptográfica de logs
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 6 del Flujo Normal, `AuditService.verify_chain_integrity` detecta una discrepancia entre el hash recalculado y el hash almacenado en un bloque específico (evidencia de manipulación o corrupción de datos). Lanza `HTTPException(status_code=409, detail="AUDIT_TAMPERING_DETECTED: ¡Alerta Crítica! Se detectó una inconsistencia en la cadena de hashes en el registro ID {broken_id}.")`.<br><br>En `AuditLogView.tsx`, la interfaz conmuta inmediatamente a un estado de alarma en color rojo parpadeante, resalta la fila alterada y genera una entrada prioritaria en el sistema de seguridad institucional. |
| **E002-1.2** Presiona el botón "Descargar Informe Forense de Incidencia". | **E002-1.3** Emite el volcado forense de la discrepancia para su remisión a las autoridades universitarias y finaliza el caso de uso registrando el incidente de seguridad institucional. |

#### CUS-020 - Configurar parámetros institucionales y umbrales

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-020** (CUS-020) |
| **Nombre** | Configurar parámetros operativos institucionales y umbrales de gobernanza |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-024 (Priorización institucional y realce algorítmico); RN-04 (Umbral temporal T-24h), RN-05 (Aforos máximos 10 y 20), RN-10 (Quórum mínimo de 3 estudiantes), RN-14 (Horas de acreditación) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional (`UserRole.administrador`), Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a las autoridades de la EPIS-UPT parametrizar y calibrar las reglas de negocio globales y umbrales operacionales del sistema sin requerir modificaciones en el código fuente a través del componente cliente `SystemSettingsView.tsx` y el servicio `configService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/config.py` y `app/services/config_service.py` procesan las peticiones `GET /api/v1/config/parameters` y `PUT /api/v1/config/parameters`. El administrador puede ajustar los aforos máximos presenciales y virtuales (RN-05), la ventana de antelación obligatoria para reservas y cancelaciones (RN-04), el quórum mínimo para confirmación automática de sesiones (RN-10) y el umbral de horas acumuladas para emisión de constancias (RN-14). Los parámetros se persisten en la tabla `parametros_institucionales` (`app/models/config.py`), invalidan la caché global de la aplicación y registran una traza auditada de modificación. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Reglamento General de Mentorías Universitarias EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/SystemSettingsView.tsx`<br>`aplicacion/frontend/src/services/configService.ts` (`ConfigService`, `ApiConfigAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/config.py` (`GET /api/v1/config/parameters`, `PUT /api/v1/config/parameters`)<br>`aplicacion/backend/app/services/config_service.py` (`ConfigService.get_parameters`, `ConfigService.update_parameters`)<br>`aplicacion/backend/app/models/config.py` (`ParametroInstitucional`), `app/models/auth.py` (`LogAuditoriaSeguridad`) |
| **Precondiciones** | 1. Administrador institucional autenticado con token JWT portando claim `administrador`.<br>2. Catálogo de parámetros base inicializado en la tabla `parametros_institucionales`.<br>3. Autenticación de doble factor reconfirmada para modificaciones críticas de configuración. |
| **PostCondiciones** | 1. Registro actualizado en la tabla física `parametros_institucionales` en PostgreSQL.<br>2. Invalidación atómica de la caché en memoria del servidor de aplicaciones.<br>3. Despliegue de confirmación en cliente y aplicación inmediata de los nuevos umbrales operacionales. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de parámetros vigentes y despliegue del panel** | |
| **1.** El administrador accede a `"Configuración del Sistema"` en `SystemSettingsView.tsx`. | **2.** En `configService.ts`, se despacha `GET /api/v1/config/parameters`. En `config.py`, se valida el rol administrativo. `ConfigService.get_parameters` ejecuta `SELECT clave, valor, descripcion, tipo_dato, valor_min, valor_max FROM parametros_institucionales WHERE activo = true`. Retorna HTTP 200 con el diccionario de parámetros. En `SystemSettingsView.tsx`, se renderiza un formulario organizado por categorías: 1) Aforos Institucionales (Presencial máx 10, Virtual máx 20), 2) Ventana de Antelación (24 horas), 3) Quórum Mínimo (3 confirmados), y 4) Horas de Certificación (20 horas). |
| **Fase 2: Edición de umbrales y validación de rangos permitidos** | |
| **3.** El administrador modifica uno o más valores numéricos (e.g. ajusta el quórum mínimo a 4 estudiantes para períodos de alta demanda) y presiona el botón `"Guardar Parámetros Institucionales"`. | **4.** En `SystemSettingsView.tsx`, se ejecutan validaciones en cliente comprobando que los nuevos valores se encuentren dentro de los rangos operacionales permitidos (`valor_min <= valor <= valor_max`). En `configService.ts`, se despacha `PUT /api/v1/config/parameters` con el payload `ParameterUpdatePayload`. En `config.py`, el controlador valida el esquema y delega a `config_service.py`. (Si un parámetro numérico excede los límites institucionales de seguridad, salta a E001). (Si la sesión requiere reautenticación administrativa para cambios críticos, salta a E002). |
| **Fase 3: Persistencia transaccional, purga de caché y aplicación en caliente** | |
| **5.** El administrador observa el indicador circular de guardado seguro. | **6.** En `config_service.py`, se inicia una transacción ACID. Se ejecutan las sentencias `UPDATE parametros_institucionales SET valor = :val, fecha_modificacion = NOW(), modificado_por = :uid WHERE clave = :key`. Se inserta el evento en `log_auditoria_seguridad`. Se confirma la transacción con `db.commit()`. El servicio purga la caché interna del servidor para forzar la recarga de los nuevos umbrales en todos los módulos dependientes (ofertas, reservas y quórum). Retorna HTTP 200 con los parámetros actualizados. En cliente, `SystemSettingsView.tsx` despliega una notificación flotante en color verde de éxito: *"Parámetros institucionales actualizados y aplicados en caliente exitosamente"*. |

##### Flujos de Excepción

##### Flujo de excepción E001: Parámetro fuera de los rangos institucionales permitidos
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `config_service.py` comprueba que el valor propuesto supera los límites de seguridad institucional (e.g. se intenta fijar un aforo presencial mayor a 30 cupos excediendo la capacidad de los laboratorios). Lanza `HTTPException(status_code=422, detail="PARAMETER_OUT_OF_BOUNDS: El valor ingresado para '{param_key}' excede los límites operacionales autorizados por la Dirección de Escuela.")`.<br><br>En `SystemSettingsView.tsx`, se resalta el campo observado en color rojo y se muestra el rango admisible. |
| **E001-1.2** Corrige el valor ingresando un número dentro del rango permitido. | **E001-1.3** Rehabilita el botón de guardado y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Reautenticación de seguridad requerida
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, al modificar parámetros de gobernanza crítica, el sistema exige reconfirmación de clave o token OTP. Si el administrador no suministra la clave secundaria, `config.py` lanza `HTTPException(status_code=401, detail="REAUTH_REQUIRED: Se requiere confirmación de credenciales para modificar parámetros de gobernanza crítica.")`.<br><br>En `SystemSettingsView.tsx`, se abre una ventana modal solicitando la confirmación de identidad institucional. |
| **E002-1.2** Ingresa su contraseña institucional o código OTP de confirmación y presiona "Verificar". | **E002-1.3** Valida las credenciales secundarias y retorna al paso 4 del Flujo Normal de Eventos. |

#### CUS-022 - Gestionar catálogo de temas y materias críticas

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-022** (CUS-022) |
| **Nombre** | Gestionar catálogo de temas curriculares, asignaturas filtro y malla oficial |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-005 (Gestión del catálogo de asignaturas y temarios), RF-026 (Auditoría administrativa de bitácoras y materias); RN-11 (Asignaturas filtro prioritarias) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional (`UserRole.administrador`), Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a la Dirección de Escuela y a los administradores actualizar la malla curricular de la EPIS-UPT, gestionar las asignaturas designadas como materias filtro (`es_filtro = true`) y dar de alta, modificar o desactivar temas silábicos de aprendizaje a través del componente cliente `AdminCurriculumView.tsx` y el servicio `curriculumService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/curriculum.py` y `app/services/curriculum_service.py` procesan las peticiones `POST /api/v1/curriculum/courses`, `PUT /api/v1/curriculum/courses/{id}`, `POST /api/v1/curriculum/courses/{id}/topics` y `DELETE /api/v1/curriculum/topics/{id}`. El servicio valida que los temas ingresados correspondan a las unidades didácticas del semestre lectivo vigente (semanas 1 a 17), previene duplicidades conceptuales mediante comprobaciones de unicidad en `temas_curriculares` (`app/models/curriculum.py`) y asegura la consistencia referencial con las ofertas de mentoría y solicitudes de demanda en curso. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-02: Gestión Curricular y Perfiles Académicos)<br>Plan de Estudios y Sílabos Oficiales de Ingeniería de Sistemas UPT |
| **Anexos** | `aplicacion/frontend/src/components/AdminCurriculumView.tsx`<br>`aplicacion/frontend/src/services/curriculumService.ts` (`CurriculumService.manageCurriculum`)<br>`aplicacion/backend/app/api/v1/endpoints/curriculum.py` (`POST /api/v1/curriculum/courses`, `POST /api/v1/curriculum/courses/{id}/topics`)<br>`aplicacion/backend/app/services/curriculum_service.py` (`CurriculumService.create_course`, `CurriculumService.manage_topics`)<br>`aplicacion/backend/app/models/curriculum.py` (`Carrera`, `Curso`, `TemaCurricular`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Usuario con credenciales de Administrador Institucional o Director de Escuela.<br>2. Plan de estudios registrado en la tabla `carreras` en la base de datos.<br>3. Número de semana lectiva comprendido entre las semanas 1 y 17 del calendario académico. |
| **PostCondiciones** | 1. Entidad `Curso` o `TemaCurricular` insertada o actualizada en la tabla física de PostgreSQL.<br>2. Transacción ACID confirmada con `db.commit()` e indexación para el motor de búsqueda.<br>3. Actualización reactiva del árbol curricular en la interfaz administrativa. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del árbol curricular y selección de asignatura** | |
| **1.** El administrador accede a `"Gestión de Malla y Temarios"` en `AdminCurriculumView.tsx`. | **2.** En `curriculumService.ts`, se despacha `GET /api/v1/curriculum/courses`. En `curriculum.py`, `curriculum_service.py` recupera la estructura completa de asignaturas ordenadas por ciclo. En `AdminCurriculumView.tsx`, se renderiza una vista en árbol con las materias clasificadas por ciclo y la etiqueta *"Materia Filtro"* en aquellas con `es_filtro = true`. El administrador hace clic sobre una asignatura específica para desplegar sus temas silábicos. |
| **Fase 2: Ingreso de datos del nuevo tema curricular silábico** | |
| **3.** El administrador presiona el botón `"Agregar Nuevo Tema Curricular"` en el panel de la asignatura. | **4.** En `AdminCurriculumView.tsx`, se abre una ventana modal con los campos: número de unidad didáctica (1 a 4), título descriptivo del tema, semana académica programada (semanas 1 a 17) y descripción conceptual. El administrador completa los campos y pulsa el botón `"Registrar Tema Curricular"`. (Si el título del tema ya existe en esa misma unidad, salta a E001). (Si el número de semana está fuera del calendario lectivo de 1 a 17, salta a E002). |
| **Fase 3: Persistencia transaccional y actualización del catálogo** | |
| **5.** El administrador observa el indicador circular de guardado en el botón del modal. | **6.** En `curriculumService.ts`, se despacha `POST /api/v1/curriculum/courses/{id}/topics` con el payload `TopicCreateRequest`. En `curriculum.py`, `curriculum_service.py` inicia la transacción con `db.begin()`. Valida que el curso exista y que no exista una tupla idéntica `(curso_id, unidad, titulo)`. Inserta en `temas_curriculares`, ejecuta `db.commit()` y retorna HTTP 201 Created. En cliente, `AdminCurriculumView.tsx` cierra el modal, añade el nuevo tema al árbol curricular en pantalla y despliega una notificación flotante en color verde de éxito: *"Tema curricular registrado y disponible para ofertas y demandas académicas"*. |

##### Flujos de Excepción

##### Flujo de excepción E001: Tema curricular duplicado en la misma unidad
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `curriculum_service.py` detecta que ya existe un tema con el mismo título para la misma unidad didáctica del curso. Lanza `HTTPException(status_code=409, detail="DUPLICATE_TOPIC: Ya existe un tema curricular registrado con ese título para la unidad seleccionada.")`.<br><br>En `AdminCurriculumView.tsx`, se resalta el cuadro de texto del título en color rojo con el mensaje de duplicidad. |
| **E001-1.2** Modifica el título del tema especificando con mayor precisión el contenido temático. | **E001-1.3** Rehabilita el botón de guardado en el modal y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Número de semana lectiva fuera de rango semestral
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, Pydantic en `curriculum.py` comprueba que el campo `semana` es menor a 1 o mayor a 17 (duración máxima del semestre lectivo universitario). Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: El número de semana académica debe estar comprendido estrictamente entre 1 y 17.")`.<br><br>En `AdminCurriculumView.tsx`, se resalta el campo numérico de semana en color rojo. |
| **E002-1.2** Ingresa un número de semana válido dentro del intervalo 1 a 17. | **E002-1.3** Actualiza el valor en el estado del formulario y retorna al paso 4 del Flujo Normal de Eventos. |


