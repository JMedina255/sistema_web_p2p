# Matriz de Inconsistencias y Hallazgos de Inspección
## Caso de Uso: CUS-001 — Iniciar sesión institucional con 2FA

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT  
**Hito:** DOC-SRS-01  
**Documento Fuente:** `SRS.md` (Versión 3.0 / Línea Base `90683d1`)  
**Documento Destino:** `SRS_NUEVO.md`  
**Fecha de Inspección:** 23/11/2026  
**Responsables de Auditoría:** Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani  

---

### 1. Presentación de la Matriz

Durante la ejecución sistemática de los 18 escenarios de prueba mediante Playwright sobre el entorno de desarrollo integrado (React 19 + FastAPI + PostgreSQL Supabase), se contrastaron las especificaciones narrativas y técnicas de la versión anterior del SRS frente al comportamiento interactivo real de la aplicación.

Se registraron ocho (8) hallazgos debidamente clasificados, los cuales sustentan la actualización descriptiva del caso de uso CUS-001 sin alterar el alcance de los requisitos del sistema ni introducir modificaciones en el código fuente.

---

### 2. Matriz de Hallazgos e Inconsistencias

| ID | Paso o escenario | SRS anterior | Comportamiento observado | Clasificación | Evidencia | Acción recomendada |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| **HAL-001** | Paso 1 / ESC-01<br>Solicitud de código OTP | Se especificaba el botón de envío con el texto `"Enviar Código OTP"`. | El botón visible en la interfaz tiene el texto `"Continuar con Código OTP →"` (`LoginOtpView.tsx`). | **Inconsistencia documental** | `01_pantalla_inicio_visitante.png` | Actualizar el texto literal del botón en el Flujo Normal de la nueva narrativa. |
| **HAL-002** | Paso 7 / ESC-12<br>Botones de consentimiento informado | Se especificaban los botones `"Aceptar y Formalizar Consentimiento"` y `"Declinar y Salir"` / `"Confirmar Salida"`. | Los botones interactivos reales son `"✓ Aceptar y Continuar"` y `"🚫 Rechazar y Salir"` (`ConsentModalView.tsx`). | **Inconsistencia documental** | `11_consentimiento_informado.png`<br>`12_rechazo_consentimiento.png` | Ajustar las etiquetas literales de ambos botones en la narrativa funcional del CUS-001. |
| **HAL-003** | Paso 7 / ESC-12<br>Estado del botón de aceptación | No se especificaba la inhabilitación del botón de aceptación mientras la casilla estuviese desmarcada. | El botón `"✓ Aceptar y Continuar"` permanece deshabilitado en color gris (`#94A3B8`) hasta marcar la casilla de conformidad de la Ley 29733. | **Diferencia visual** | `11_consentimiento_informado.png` | Documentar el estado inactivo inicial del botón en la respuesta del sistema del Flujo Normal. |
| **HAL-004** | Paso 4 / ESC-11<br>Enlace de cambio de correo | Se describía el enlace de acción como `"Cambiar de correo institucional"`. | El enlace físico en la tarjeta del desafío muestra textualmente `"Cambiar correo"` en color dorado institucional y subrayado. | **Inconsistencia documental** | `05_verificacion_codigo_otp.png`<br>`09_cambio_correo.png` | Corregir la descripción del enlace en el Flujo Normal y en el Flujo Alternativo A004. |
| **HAL-005** | Flujo A001 / ESC-15<br>Autenticación con Google GIS | Se asumía un flujo automatizado completo de selección de cuenta Google y retorno instantáneo. | El botón nativo de Google Identity Services renderiza el diálogo de Google en iframe protegido; requiere interacción manual con una cuenta real `@virtual.upt.pe` activa en el navegador. | **Validación bloqueada** | `10_autenticacion_google.png` | Declarar el flujo alternativo A001 como PENDIENTE DE VALIDACIÓN MANUAL / EXTERNA en ambiente institucional. |
| **HAL-006** | Paso 1 / ESC-03<br>Etiqueta de correo institucional | Se indicaba que la etiqueta del campo era `"Correo Institucional"`. | La etiqueta visible en el formulario es `"Correo Electrónico Institucional UPT"` y el placeholder `"ej: ra2022073504@virtual.upt.pe"`. | **Inconsistencia documental** | `01_pantalla_inicio_visitante.png`<br>`03_ingreso_correo_institucional.png` | Estandarizar la denominación exacta de la etiqueta y el placeholder en la especificación visual. |
| **HAL-007** | Paso 4 / ESC-06<br>Temporizador de expiración y cooldown | Solo se describía el temporizador regresivo de 5 minutos (300 segundos). | La interfaz presenta simultáneamente dos temporizadores: la cuenta regresiva de expiración (`⏳ Expira en: MM:SS`) y el contador de reenvío (`Reenviar código en Xs`), que activa el botón de reenvío al llegar a 0s. | **Mejora de usabilidad** | `05_verificacion_codigo_otp.png`<br>`08_reenvio_codigo_otp.png` | Incorporar la descripción de ambos temporizadores y su sincronización en el Paso 4 del Flujo Normal. |
| **HAL-008** | Flujo E001 / ESC-04<br>Mensaje de error por dominio ajeno | Se hacía referencia explícita al código interno `INVALID_DOMAIN` y a la excepción `HTTPException(400)`. | La interfaz muestra un aviso accesible en rojo suave con el texto amigable `"Acceso restringido: Solo se permiten correos institucionales con dominio @virtual.upt.pe o @upt.pe."` sin exponer códigos técnicos. | **Inconsistencia documental** | `04_error_correo_no_institucional.png` | Eliminar referencias a códigos de error HTTP internos y redactar el mensaje visible al usuario. |

---

### 3. Síntesis y Clasificación de Hallazgos

* **Inconsistencias documentales (5):** HAL-001, HAL-002, HAL-004, HAL-006, HAL-008. Se corrigen directamente en la nueva redacción de la narrativa en `SRS_NUEVO.md`.
* **Diferencias visuales (1):** HAL-003. Se incorpora en la descripción visual del caso de uso.
* **Mejoras de usabilidad (1):** HAL-007. Se enriquece la descripción funcional del paso de verificación OTP.
* **Validaciones bloqueadas (1):** HAL-005. Se mantiene clasificada formalmente para validación manual en despliegue institucional de producción.
* **Errores funcionales (0):** Ninguno detectado. La implementación del módulo de autenticación dual OTP/2FA opera de forma conforme con las reglas de negocio RN-01 y RN-02.
