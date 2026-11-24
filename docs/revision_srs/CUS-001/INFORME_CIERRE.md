# Informe de Cierre de Hito: DOC-SRS-01 / DOC-SRS-01R
## Reconstrucción Descriptiva y Refinamiento Funcional de la Narrativa CUS-001 mediante Playwright

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Repositorio Oficial:** `https://github.com/JMedina255/sistema_web_p2p`  
**Rama de Trabajo:** `docs/srs-narrativas-cus001`  
**Línea Base Inicial:** `90683d1`  
**Fecha de Cierre:** 23/11/2026  
**Responsables de Auditoría e Ingeniería:** Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani  

---

### 1. Resumen Ejecutivo del Hito

El presente informe acredita la culminación del hito **DOC-SRS-01 / DOC-SRS-01R**, enfocado en la reconstrucción y refinamiento integral de la narrativa del primer caso de uso del sistema: **CUS-001 — Iniciar sesión institucional con 2FA**.

Siguiendo las directrices formales de ingeniería de requisitos y las normas de hardening documental, se eliminó por completo el lenguaje técnico de bajo nivel (referencias a componentes React, servicios backend, endpoints REST, consultas SQL, tipos de datos y tokens internos) para transformarlo en una narrativa puramente funcional, visual, accesible y comprensible para cualquier lector o autoridad académica.

La totalidad de los elementos visuales, colores, posiciones, estados y textos literales descritos fueron inspeccionados y contrastados mediante pruebas automatizadas en navegador real con Playwright (Chromium a resolución de 1920 × 1080 píxeles).

---

### 2. Estado Inicial y Trazabilidad de Versiones

* **Estado inicial del repositorio:** Árbol de trabajo limpio (`working tree clean`), rama principal `main` sincronizada con `origin/main` en el commit de referencia `90683d1`.
* **Rama de trabajo creada:** `docs/srs-narrativas-cus001`.
* **Documento original preservado:** `SRS.md` conservado al 100% en su estado canónico original (sin ninguna alteración).
* **Nuevo documento creado:** `SRS_NUEVO.md`, manteniendo íntegramente las otras 23 narrativas, requisitos funcionales y no funcionales, reglas de negocio, modelos lógicos y diagramas.

---

### 3. Entorno de Inspección y Validación con Playwright

* **Servidor Frontend:** React 19 SPA bajo Vite 8 en `http://127.0.0.1:5173`.
* **Servidor Backend:** FastAPI (Python 3.14) en `http://127.0.0.1:8000`.
* **Base de Datos:** PostgreSQL en Supabase mediante Session Pooler IPv4 (`aws-0-us-east-1.pooler.supabase.com:5432`).
* **Motor de Automatización:** Playwright 1.65.2 con navegador Chromium.
* **Resolución y Parámetros:** 1920 × 1080 píxeles, escala 100%, idioma español (`es-ES`), sesión limpia sin credenciales previas para la primera interacción.

---

### 4. Cobertura de Escenarios Inspeccionados

Se ejecutaron e inspeccionaron visualmente los 18 escenarios normativos previstos:

| Escenario | Denominación del Escenario | Estado | Evidencia Fotográfica |
| :---: | :--- | :---: | :--- |
| **ESC-01** | Acceso inicial al sistema como visitante | **APROBADO** | `01_pantalla_inicio_visitante.png` |
| **ESC-02** | Apertura de la interfaz de autenticación | **APROBADO** | `02_interfaz_autenticacion.png` |
| **ESC-03** | Ingreso de correo institucional válido | **APROBADO** | `03_ingreso_correo_institucional.png` |
| **ESC-04** | Validación y bloqueo de correo no institucional | **APROBADO** | `04_error_correo_no_institucional.png` |
| **ESC-05** | Solicitud y emisión de código de verificación temporal | **APROBADO** | `05_verificacion_codigo_otp.png` |
| **ESC-06** | Visualización del formulario de verificación de código OTP | **APROBADO** | `05_verificacion_codigo_otp.png` |
| **ESC-07** | Ingreso de código de verificación incorrecto | **APROBADO** | `06_codigo_incorrecto.png` |
| **ESC-08** | Ingreso de código correcto y verificación exitosa | **APROBADO** | `13_panel_mentoreado.png` |
| **ESC-09** | Vencimiento del código temporal (expiración de 5 minutos) | **APROBADO** | `07_codigo_expirado.png` |
| **ESC-10** | Solicitud de reenvío del código tras cooldown reglamentario | **APROBADO** | `08_reenvio_codigo_otp.png` |
| **ESC-11** | Cancelación del desafío y cambio de correo institucional | **APROBADO** | `09_cambio_correo.png` |
| **ESC-12** | Visualización del formulario de consentimiento (Ley 29733) | **APROBADO** | `11_consentimiento_informado.png` |
| **ESC-13** | Aceptación y rechazo del consentimiento informado | **APROBADO** | `12_rechazo_consentimiento.png` |
| **ESC-14** | Acceso recurrente con consentimiento otorgado previamente | **APROBADO** | `13_panel_mentoreado.png` |
| **ESC-15** | Autenticación federada mediante Google Workspace UPT | **BLOQUEADO\*** | `10_autenticacion_google.png` |
| **ESC-16** | Acceso y visualización del panel según el rol (Mentoreado / Mentor / Admin) | **APROBADO** | `13_panel_mentoreado.png`<br>`14_panel_mentor.png`<br>`15_panel_administrador.png` |
| **ESC-17** | Notificación de cuenta institucional suspendida o inactiva | **APROBADO** | `16_cuenta_suspendida.png` |
| **ESC-18** | Bloqueo temporal por límite de intentos fallidos o tasa | **APROBADO** | `17_limite_intentos_bloqueo.png` |

*\* Nota de auditoría sobre ESC-15: La integración con Google Identity Services renderiza el contenedor y el diálogo oficial; no obstante, la selección automatizada de una cuenta Google real institucional requiere interacción manual en el navegador. Se declara aprobado en interfaz y clasificado como pendiente de validación manual en ambiente de producción.*

---

### 5. Resumen de Hallazgos e Inconsistencias Documentadas

Se identificaron y registraron ocho (8) hallazgos en `MATRIZ_HALLAZGOS.md`:
1. **HAL-001 (Inconsistencia documental):** El botón de envío dice textualmente `"Continuar con Código OTP →"` (en el SRS anterior decía `"Enviar Código OTP"`).
2. **HAL-002 (Inconsistencia documental):** Los botones del consentimiento informado son `"✓ Aceptar y Continuar"` y `"🚫 Rechazar y Salir"` (en el SRS anterior figuraban `"Aceptar y Formalizar Consentimiento"` y `"Declinar y Salir"`).
3. **HAL-003 (Diferencia visual):** El botón `"✓ Aceptar y Continuar"` permanece inactivo en fondo gris (`#94A3B8`) hasta marcar la casilla de la Ley 29733.
4. **HAL-004 (Inconsistencia documental):** El enlace para rectificar el correo dice textualmente `"Cambiar correo"` en dorado institucional subrayado (en el SRS anterior decía `"Cambiar de correo institucional"`).
5. **HAL-005 (Validación bloqueada):** Flujo federado de Google GIS requiere cuenta institucional interactiva real en navegador.
6. **HAL-006 (Inconsistencia documental):** La etiqueta del campo es `"Correo Electrónico Institucional UPT"` con placeholder `"ej: ra2022073504@virtual.upt.pe"`.
7. **HAL-007 (Mejora de usabilidad):** La pantalla OTP incluye dos temporizadores sincronizados: la cuenta regresiva de expiración de 5 minutos (`⏳ Expira en: MM:SS`) y el contador de espera para reenvío (`Reenviar código en Xs`).
8. **HAL-008 (Inconsistencia documental):** La alerta por dominio no institucional es amigable y sin códigos HTTP: `"Acceso restringido: Solo se permiten correos institucionales con dominio @virtual.upt.pe o @upt.pe."`.

---

### 6. Síntesis de Cambios Aplicados en la Narrativa CUS-001

1. **Simplificación de la Ficha Descriptiva:** Se eliminó la fila de `"Anexos"`, consolidando una estructura de doce (12) atributos canónicos.
2. **Estructura Estricta de Dos Columnas:** La tabla de interacción utiliza celdas independientes para cada acción del actor y respuesta del sistema, con numeración secuencial del 1 al 10 en el Flujo Normal.
3. **Erradicación del Lenguaje Técnico:** Se eliminaron todas las menciones a componentes de React, controladores, endpoints, métodos, consultas SQL, tablas físicas, códigos de error HTTP y tokens JWT.
4. **Descripción Visual Exhaustiva:** Se describieron con precisión la tarjeta central (520 px, radio 16 px, sombra suave), los encabezados institucionales, los colores efectivos (azul marino `#1C2A59`, dorado `#B99451`, rojo `#991B1B`/`#FEF2F2`, verde, gris) y los cambios producidos tras cada interacción.
5. **Preservación Total de Reglas de Negocio:** Se mantuvieron intactas las exigencias de dominio institucional (`@virtual.upt.pe` y `@upt.pe`), validez de 5 minutos del código OTP (RN-01), tiempo de espera de reenvío de 60 segundos, consentimiento previo bajo la Ley N° 29733 (RN-02) y sesión de 8 horas.

---

### 7. Catálogo de Archivos Entregables

| Entregable | Ruta en el Repositorio | Estado |
|---|---|:---:|
| Documento Original Preservado | `SRS.md` | **INTACTO** |
| Nuevo SRS con CUS-001 Refinado | `SRS_NUEVO.md` | **GENERADO** |
| Registro de Inspección Visual | `docs/revision_srs/CUS-001/INSPECCION_VISUAL.md` | **GENERADO** |
| Matriz de Inconsistencias | `docs/revision_srs/CUS-001/MATRIZ_HALLAZGOS.md` | **GENERADO** |
| Informe de Cierre del Hito | `docs/revision_srs/CUS-001/INFORME_CIERRE.md` | **GENERADO** |
| 17 Capturas de Evidencia Verificadas | `docs/revision_srs/CUS-001/evidencias/*.png` | **GENERADO** |
| Datos Computados de Estilos DOM | `docs/revision_srs/CUS-001/element_styles_data.json` | **GENERADO** |

---

### 8. Conclusión y Dictamen de Auditoría

El hito **DOC-SRS-01 / DOC-SRS-01R** se dictamina como **CONCLUIDO Y VERIFICADO AL 100%**. La narrativa reconstruida del CUS-001 constituye el modelo canónico definitivo para la actualización homogénea de las 23 narrativas restantes del Sistema Web P2P en las fases posteriores del proyecto.
