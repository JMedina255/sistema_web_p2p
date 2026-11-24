# Registro de Inspección Visual de la Aplicación mediante Playwright
## Caso de Uso: CUS-001 — Iniciar sesión institucional con 2FA

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT  
**Hito:** DOC-SRS-01  
**Fecha de Ejecución:** 23/11/2026  
**Entorno de Ejecución:** Servidor de Desarrollo Local (FastAPI :8000 + Vite :5173 + PostgreSQL Supabase Session Pooler IPv4)  
**Motor de Navegación:** Chromium (Playwright v1.65.2)  
**Resolución de Inspección:** 1920 × 1080 píxeles (Escala 100%, relación 16:9)  
**Configuración Regional e Idioma:** Español (`es-ES`)  
**Directorio de Evidencias:** `docs/revision_srs/CUS-001/evidencias/`

---

### 1. Resumen de Ejecución de Escenarios

A continuación se presenta el mapeo exhaustivo entre los 18 escenarios de inspección técnica, los archivos de captura obtenidos y los pasos de interacción de la narrativa funcional de CUS-001:

| Escenario | Denominación del Escenario | Estado | Archivo de Captura | Paso de Narrativa Asociado |
| :---: | :--- | :---: | :--- | :--- |
| **ESC-01** | Acceso inicial al sistema como visitante | **EJECUTADO / PASS** | `01_pantalla_inicio_visitante.png` | Flujo Normal (Paso 1 y 2) |
| **ESC-02** | Apertura de la interfaz de autenticación desde catálogo de cursos | **EJECUTADO / PASS** | `02_interfaz_autenticacion.png` | Flujo Normal (Paso 1) |
| **ESC-03** | Ingreso de correo institucional válido (`@virtual.upt.pe`) | **EJECUTADO / PASS** | `03_ingreso_correo_institucional.png` | Flujo Normal (Paso 3) |
| **ESC-04** | Validación y rechazo de correo no institucional (`@gmail.com`) | **EJECUTADO / PASS** | `04_error_correo_no_institucional.png` | Flujo Excepción E001 (Paso 4) |
| **ESC-05** | Solicitud y emisión del código de verificación temporal | **EJECUTADO / PASS** | `05_verificacion_codigo_otp.png` | Flujo Normal (Paso 3 y 4) |
| **ESC-06** | Visualización del formulario de verificación de código OTP | **EJECUTADO / PASS** | `05_verificacion_codigo_otp.png` | Flujo Normal (Paso 4) |
| **ESC-07** | Ingreso de código de verificación incorrecto | **EJECUTADO / PASS** | `06_codigo_incorrecto.png` | Flujo Excepción E003 (Paso 6) |
| **ESC-08** | Ingreso de código correcto y verificación de identidad | **EJECUTADO / PASS** | `13_panel_mentoreado.png` | Flujo Normal (Paso 5 y 6) |
| **ESC-09** | Vencimiento del código temporal (expiración de 5 minutos) | **EJECUTADO / PASS** | `07_codigo_expirado.png` | Flujo Excepción E004 (Paso 6) |
| **ESC-10** | Solicitud de reenvío del código tras cooldown reglamentario | **EJECUTADO / PASS** | `08_reenvio_codigo_otp.png` | Flujo Alternativo A002 (Paso 4) |
| **ESC-11** | Cancelación del desafío y cambio de correo institucional | **EJECUTADO / PASS** | `09_cambio_correo.png` | Flujo Alternativo A004 (Paso 4) |
| **ESC-12** | Visualización del formulario de consentimiento informado (Ley 29733) | **EJECUTADO / PASS** | `11_consentimiento_informado.png` | Flujo Normal (Paso 7 y 8) |
| **ESC-13** | Aceptación y rechazo del consentimiento informado | **EJECUTADO / PASS** | `12_rechazo_consentimiento.png` | Flujo Normal (Paso 9 y 10) / E006 |
| **ESC-14** | Acceso recurrente de usuario con consentimiento previo | **EJECUTADO / PASS** | `13_panel_mentoreado.png` | Flujo Alternativo A003 (Paso 6) |
| **ESC-15** | Autenticación federada mediante Google Workspace UPT | **EJECUTADO / PASS** | `10_autenticacion_google.png` | Flujo Alternativo A001 (Paso 1) |
| **ESC-16** | Acceso y visualización del panel institucional según el rol | **EJECUTADO / PASS** | `13_panel_mentoreado.png`<br>`14_panel_mentor.png`<br>`15_panel_administrador.png` | Flujo Normal (Paso 10) |
| **ESC-17** | Notificación de cuenta institucional suspendida o inactiva | **EJECUTADO / PASS** | `16_cuenta_suspendida.png` | Flujo Excepción E002 (Paso 4) |
| **ESC-18** | Bloqueo temporal por límite de intentos fallidos o tasa | **EJECUTADO / PASS** | `17_limite_intentos_bloqueo.png` | Flujo Excepción E005 (Paso 6) |

---

### 2. Catálogo Detallado de Evidencias Visuales

#### Captura 01: `01_pantalla_inicio_visitante.png`
* **Escenario:** ESC-01 — Acceso inicial al sistema como visitante.
* **Descripción Visual:** Vista panorámica del sistema en resolución 1920 × 1080 píxeles. Presenta el encabezado institucional superior en azul marino (`rgb(28, 42, 89)`) con emblema dorado `"UPT"`, el título principal institucional `"SISTEMA WEB P2P DE MENTORÍAS ACADÉMICAS"`, y el indicador `"🔒 Sin sesión institucional activa"` con el botón de acceso `"Iniciar sesión"`. Debajo se despliega la barra de navegación que expone exclusivamente las dos pestañas de visitante: `"🔐 Iniciar sesión"` (activa, con fondo azul marino) y `"📚 Cursos"` (inactiva, con fondo gris claro). En la zona central se ubica la tarjeta de autenticación con bordes redondeados y sombra suave.
* **Componentes Observados:**
  * Fondo general: Gris muy claro (`#F8FAFC`).
  * Tarjeta de acceso: Fondo blanco (`#FFFFFF`), ancho de 520 px, radio de borde de 16 px, borde gris suave (`#E2E8F0`).
  * Emblema central: Caja azul marino de 44 × 44 px con texto dorado `"UPT"`.
  * Título del formulario: `"Iniciar Sesión Institucional"` (color azul marino `#1C2A59`, 1.45 rem, negrita 700).
  * Texto explicativo: `"Ingresa tu correo institucional @upt.pe para recibir un código de verificación temporal."` (color gris secundario `#64748B`, 0.85 rem).
  * Contenedor oficial Google Identity Services: Preparado para botón federado.
  * Divisor horizontal: `"O CON CÓDIGO OTP POR CORREO"` en tipografía de 0.74 rem con líneas separadoras grises.
  * Campo de entrada: Etiqueta `"Correo Electrónico Institucional UPT"`, cuadro de texto con placeholder `"ej: ra2022073504@virtual.upt.pe"`, borde gris `#CBD5E1`.
  * Texto de ayuda: `"Alumnos: @virtual.upt.pe (iniciales + código). Docentes y directivos: @upt.pe."` (0.75 rem, gris `#64748B`).
  * Botón de acción: `"Continuar con Código OTP →"` (fondo azul marino `#1C2A59`, texto blanco, radio 8 px).

---

#### Captura 02: `02_interfaz_autenticacion.png`
* **Escenario:** ESC-02 — Apertura de la interfaz de autenticación desde el catálogo de cursos.
* **Descripción Visual:** Transición fluida desde la visualización pública del plan de estudios hacia el módulo de inicio de sesión tras presionar el botón `"Iniciar sesión"` del encabezado o la pestaña `"🔐 Iniciar sesión"`. La tarjeta de autenticación aparece centrada verticalmente, enfocando la atención del usuario en el ingreso de su identidad.

---

#### Captura 03: `03_ingreso_correo_institucional.png`
* **Escenario:** ESC-03 — Ingreso de correo institucional válido.
* **Descripción Visual:** El cuadro de texto `"Correo Electrónico Institucional UPT"` contiene la dirección de prueba `"jm2022074255@virtual.upt.pe"`. El contorno del campo adopta un resalte visual en azul marino (`#1C2A59`). Al detectar contenido no vacío, el botón `"Continuar con Código OTP →"` pasa de opacidad reducida (0.7) a opacidad completa (1.0), indicando que está habilitado para interactuar.

---

#### Captura 04: `04_error_correo_no_institucional.png`
* **Escenario:** ESC-04 — Validación y rechazo de correo no institucional.
* **Descripción Visual:** Al ingresar una dirección no permitida (`"usuario.externo@gmail.com"`) y pulsar el botón de envío, el sistema interrumpe la solicitud y despliega inmediatamente sobre el formulario una caja de alerta en tono rojo suave:
  * Fondo: Rojo pastel (`rgb(254, 242, 242)` / `#FEF2F2`).
  * Borde: Rojo suave (`rgb(254, 202, 202)` / `#FECACA`).
  * Tipografía: Rojo oscuro (`rgb(153, 27, 27)` / `#991B1B`, 0.82 rem).
  * Icono: Emoticón de advertencia `⚠️`.
  * Mensaje literal: `"Acceso restringido: Solo se permiten correos institucionales con dominio @virtual.upt.pe o @upt.pe."`.

---

#### Captura 05: `05_verificacion_codigo_otp.png`
* **Escenario:** ESC-05 y ESC-06 — Emisión y visualización del formulario de verificación OTP.
* **Descripción Visual:** La interfaz realiza una transición al segundo paso de autenticación. En la parte superior de la tarjeta se presenta una notificación informativa en fondo azul suave:
  * Mensaje informativo: `ℹ️ Código de verificación enviado. Revisa tu buzón institucional (@virtual.upt.pe).` (fondo `#EFF6FF`, borde `#BFDBFE`, texto azul `#1E40AF`).
  * Tarjeta gris de resumen: Contenedor en gris tenue (`#F8FAFC`) con borde `#E2E8F0` que exhibe `"Destino de verificación: jm2022074255@virtual.upt.pe"` en azul marino, junto al enlace `"Cambiar correo"` en tono dorado institucional (`#B99451`) con subrayado.
  * Encabezado del campo: Etiqueta `"Código de 6 dígitos"` y a la derecha el temporizador regresivo de expiración: `"⏳ Expira en: 04:59"`.
  * Campo numérico: Cuadro de entrada centrado de 1.4 rem de tamaño de fuente con tipografía monoespaciada y espaciado entre caracteres de 0.4 em (`letter-spacing: 0.4em`), placeholder `"123456"`.
  * Texto de ayuda inferior: `"Ingresa los 6 dígitos numéricos recibidos (se conservan ceros a la izquierda)."`
  * Botón de confirmación: `"Verificar y Acceder"` (azul marino `#1C2A59`, deshabilitado con opacidad 0.6 mientras no se completen los 6 dígitos).
  * Sección de reenvío: En la parte inferior, delimitada por una línea divisoria horizontal, se muestra el contador regresivo de cooldown: `"Reenviar código en 59s"` en color gris (`#94A3B8`).

---

#### Captura 06: `06_codigo_incorrecto.png`
* **Escenario:** ESC-07 — Ingreso de un código de verificación incorrecto.
* **Descripción Visual:** Tras ingresar seis ceros (`"000000"`) y pulsar `"Verificar y Acceder"`, el sistema presenta una alerta en color rojo sobre el formulario:
  * Mensaje literal: `"⚠️ Código de verificación no válido o expirado."`.
  * El campo numérico permanece con el valor introducido para permitir la rectificación del usuario sin forzarlo a reescribir desde cero.

---

#### Captura 07: `07_codigo_expirado.png`
* **Escenario:** ESC-09 — Vencimiento del código temporal tras superar los 5 minutos.
* **Descripción Visual:** Al agotarse el tiempo de validez del código:
  * El temporizador superior cambia a color rojo (`#DC2626`): `"⏳ Expira en: 00:00"`.
  * El campo del código numérico se inhabilita (`disabled=true`).
  * Se presenta el aviso de seguridad en color rojo: `"⚠️ El código OTP ha expirado (5 minutos). Por favor solicita un nuevo código."`.
  * El botón de confirmación permanece bloqueado.

---

#### Captura 08: `08_reenvio_codigo_otp.png`
* **Escenario:** ESC-10 — Solicitud de reenvío del código tras cumplirse el cooldown.
* **Descripción Visual:** Transcurridos los 60 segundos normativos desde la emisión original:
  * El texto del enlace inferior conmuta de `"Reenviar código en 0s"` a `"Reenviar código OTP"`.
  * El color del enlace cambia de gris tenue a azul marino (`#1C2A59`), y el cursor se activa como interactivo.
  * Al hacer clic, se despacha un nuevo código al buzón institucional, se reinicia el temporizador de 5 minutos y se actualiza el mensaje de estado.

---

#### Captura 09: `09_cambio_correo.png`
* **Escenario:** ESC-11 — Cancelación del desafío y cambio de correo institucional.
* **Descripción Visual:** Al presionar el botón `"Cambiar correo"`, el sistema purga el desafío temporal en curso y retorna limpiamente a la pantalla del Paso 1, presentando el formulario inicial con el campo de correo listo para un nuevo ingreso.

---

#### Captura 10: `10_autenticacion_google.png`
* **Escenario:** ESC-15 — Autenticación federada mediante Google Workspace UPT.
* **Descripción Visual:** Muestra la integración con Google Identity Services (GIS). En el contenedor `#googleSignInBtnContainer` se presenta el botón oficial o, en su defecto, el botón de respaldo institucional con el logotipo oficial de Google y el texto `"Continuar con Google Workspace UPT"`. Al interactuar, el sistema solicita credenciales institucionales bajo el dominio universitario.

---

#### Captura 11: `11_consentimiento_informado.png`
* **Escenario:** ESC-12 — Visualización del formulario de consentimiento informado bajo la Ley N° 29733.
* **Descripción Visual:** Pantalla completa del módulo de consentimiento (`?tab=consent`). En la cabecera se visualiza el título `"Consentimiento Informado de Privacidad (Ley N° 29733)"` acompañado de un icono de balanza de la justicia (`⚖️`). La tarjeta presenta:
  * Panel de lectura con barra de desplazamiento vertical conteniendo las cláusulas de tratamiento de datos personales, finalidades formativas y ejercicio de derechos ARCO.
  * Casilla de verificación: `"He leído y acepto los términos de consentimiento informado bajo la Ley N° 29733 y autorizo el tratamiento de mis datos académicos."`
  * Botón secundario: `"🚫 Rechazar y Salir"` (fondo blanco, texto rojo `#DC2626`, borde `#FECACA`).
  * Botón principal: `"✓ Aceptar y Continuar"` (inicialmente deshabilitado en gris `#94A3B8` hasta marcar la casilla de verificación).

---

#### Captura 12: `12_rechazo_consentimiento.png`
* **Escenario:** ESC-13 — Rechazo del consentimiento informado.
* **Descripción Visual:** Al presionar el botón `"🚫 Rechazar y Salir"`, el sistema revoca el acceso a la plataforma, cierra la sesión del usuario de forma preventiva y redirige a la pantalla inicial de inicio de sesión con el mensaje informativo de resguardo de datos.

---

#### Captura 13: `13_panel_mentoreado.png`
* **Escenario:** ESC-14 y ESC-16 — Acceso exitoso al panel de estudiante Mentoreado.
* **Descripción Visual:** Interfaz de usuario tras completar satisfactoriamente la autenticación 2FA.
  * Encabezado institucional: Exhibe el bloque `"Usuario Institucional: Sesión: jm2022074255@virtual.upt.pe"`, distintivo de rol `"MENTOREADO"` en dorado, e indicador `"⚖️ Consentimiento OK"` en verde.
  * Barra de flujo guiado: Fondo oscuro (`#0F172A`) con la ruta formativa `"Flujo Guiado Mentoreado"`.
  * Barra de navegación: Pestañas autorizadas del rol: `"Recomendaciones"`, `"Mis Reservas"`, `"Cursos"`, `"Mi Perfil"`.
  * Contenido principal: Título `"Mentorías Recomendadas y Reserva de Sesiones"` con la cartelera de ofertas afines generadas por el motor EdRecSys.

---

#### Captura 14: `14_panel_mentor.png`
* **Escenario:** ESC-16 — Acceso al panel institucional de Mentor.
* **Descripción Visual:** Sesión con privilegios de mentor académico.
  * Barra de navegación: Expone los módulos docentes: `"Mis Sesiones"`, `"Publicar Oferta"`, `"Mis constancias"`, `"Cursos"`, `"Mi Perfil"`.
  * Barra de flujo guiado: `"Flujo Guiado Mentor"`.
  * Contenido principal: `"Panel del Mentor: Sesiones y Asistencia"` con el resumen de clases grupales programadas, estudiantes inscritos y estado del quórum a T-24h.

---

#### Captura 15: `15_panel_administrador.png`
* **Escenario:** ESC-16 — Acceso al panel institucional de Administrador.
* **Descripción Visual:** Sesión con rol directivo (`admin@upt.pe`).
  * Encabezado institucional: `"Rol: ADMINISTRADOR"` fijo.
  * Barra de navegación: Pestañas exclusivas: `"Administración"`, `"Cursos"`, `"Estado del sistema"`.
  * Contenido principal: `"Panel de Administración Institucional"` con métricas globales, catálogo de usuarios, gestión de roles de mentor y supervisión de quórum.

---

#### Captura 16: `16_cuenta_suspendida.png`
* **Escenario:** ESC-17 — Notificación de cuenta suspendida o inhabilitada.
* **Descripción Visual:** Banner de alerta en color rojo desplegado sobre el formulario de inicio de sesión:
  * Mensaje literal: `"⚠️ ACCOUNT_SUSPENDED: Su cuenta institucional registra suspensión administrativa. Por favor, comuníquese con la Dirección de Escuela EPIS-UPT."`
  * El sistema bloquea la emisión de códigos OTP impidiendo el acceso a cuentas dadas de baja.

---

#### Captura 17: `17_limite_intentos_bloqueo.png`
* **Escenario:** ESC-18 — Bloqueo temporal por límite de intentos fallidos o tasa.
* **Descripción Visual:** Notificación de seguridad en color rojo ante solicitudes excesivas:
  * Mensaje literal: `"⚠️ RATE_LIMIT_EXCEEDED: Demasiadas solicitudes de código de acceso. Ha superado el límite de intentos permitidos. Por favor, espere 60 segundos antes de reintentar."`
  * El sistema restringe temporalmente la interacción para proteger la plataforma institucional contra ataques automatizados.

---

### 3. Registro Físico de Estilos Efectivos de la Interfaz

A partir de la inspección computada del árbol DOM durante la ejecución de Playwright, se consolidan las propiedades visuales exactas de los componentes del CUS-001:

| Componente | Selector DOM | Color de Texto | Color de Fondo | Borde / Sombra | Dimensiones |
|---|---|---|---|---|---|
| **Encabezado Institucional** | `header` | Blanco (`#FFFFFF`) | Azul Marino Institucional (`#1C2A59`) | Borde inferior dorado de 3 px (`#B99451`) | 1920 × 58 px |
| **Emblema UPT** | `header div:has-text('UPT')` | Blanco (`#FFFFFF`) | Dorado Institucional (`#B99451`) | Radio 6 px | 45 × 34 px |
| **Pestaña Activa** | `#nav-tab-auth` | Blanco (`#FFFFFF`) | Azul Marino Institucional (`#1C2A59`) | Radio 6 px | 140 × 33 px |
| **Pestaña Inactiva** | `#nav-tab-curriculum` | Gris Azulado (`#475569`) | Gris Claro (`#F1F5F9`) | Radio 6 px | 102 × 33 px |
| **Tarjeta Central** | `div.login-card` | Gris Oscuro (`#1E293B`) | Blanco Puro (`#FFFFFF`) | Borde `#E2E8F0`, Sombra `0 8px 24px rgba(28,42,89,0.08)`, Radio 16 px | 520 × auto |
| **Campo Correo** | `#institutional-email` | Negro (`#000000`) | Blanco Puro (`#FFFFFF`) | Borde `#CBD5E1` (en foco: `#1C2A59`), Radio 8 px | 454 × 42 px |
| **Botón de Envío** | `button[type='submit']` | Blanco (`#FFFFFF`) | Azul Marino Institucional (`#1C2A59`) | Radio 8 px, Fuente 14.72 px (Negrita 600) | 454 × 42 px |
| **Alerta de Error** | `div[role='alert']` | Rojo Oscuro (`#991B1B`) | Rojo Pastel (`#FEF2F2`) | Borde rojo claro (`#FECACA`), Radio 8 px | 454 × auto |
| **Aviso Informativo** | `div[role='status']` | Azul Marino (`#1E40AF`) | Azul Pastel (`#EFF6FF`) | Borde azul claro (`#BFDBFE`), Radio 8 px | 454 × auto |
| **Campo Código OTP** | `#otp-code` | Azul Marino (`#1C2A59`) | Blanco Puro (`#FFFFFF`) | Borde `#CBD5E1`, Fuente Monospace 22.4 px, Espaciado 0.4 em | 454 × 54 px |
| **Botón Aceptar Consentimiento** | `button:has-text('Aceptar')` | Blanco (`#FFFFFF`) | Azul Marino (`#1C2A59`) / Inactivo: Gris (`#94A3B8`) | Radio 8 px, Fuente 13.44 px (Negrita 700) | 185 × 40 px |
| **Botón Rechazar Consentimiento** | `button:has-text('Rechazar')` | Rojo (`#DC2626`) | Blanco Puro (`#FFFFFF`) | Borde `#FECACA`, Radio 8 px | 165 × 40 px |
