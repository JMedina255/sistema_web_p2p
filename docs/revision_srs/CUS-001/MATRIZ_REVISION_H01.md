# Matriz compacta de revisión H01 — CUS-001

**Fecha:** 2026-11-28

**Base:** `ded3afacab6fe570640e335b819e5c789ebe0533`

**Alcance:** narrativa vigente, requisitos, arquitectura, interfaz, servicios, pruebas y diagramas de CUS-001.

| Documento o elemento | Problema detectado | Evidencia contrastada | Prioridad | Acción recomendada |
|---|---|---|:---:|---|
| `NARRATIVAS_CASOS_DE_USO.md` — E002 | Declaraba validación de cuenta suspendida, pero el flujo actual solo valida formato y dominio; no existe comprobación de suspensión en el servicio de autenticación. | Servicio de autenticación, modelos y pruebas; no se encontró consulta de estado de cuenta. | Alta | Retirar la afirmación y registrar la validación administrativa como funcionalidad no implementada. |
| Narrativa — E005 | Mezclaba cinco intentos fallidos y cinco solicitudes por minuto, atribuyendo a ambos un bloqueo temporal de 60 segundos. | Configuración y pruebas: al quinto código incorrecto se bloquea definitivamente el desafío; el cooldown y la tasa de solicitudes son controles separados. | Alta | Separar máximo de intentos (E005) de espera/límite de solicitudes (E006). |
| Narrativa — Google | Presentaba un texto fijo de botón y podía interpretarse como flujo operativo confirmado. | La interfaz usa el botón nativo de Google solo cuando existe configuración; las evidencias previas no completaron el acceso con una cuenta institucional real. | Alta | Describir el botón oficial de forma condicional y conservar «pendiente de validación manual». |
| Narrativa — consentimiento | El título documentado no coincidía con la pantalla actual. | La interfaz muestra «Consentimiento Informado Digital», el estado «PENDIENTE DE FIRMA» y los botones «Rechazar y Salir» / «Aceptar y Continuar». | Media | Alinear título, estado, controles y condición de habilitación. |
| Narrativa — cambio de correo | Afirmaba que se anulaba el desafío activo; la acción visible reinicia el formulario, pero no revoca el desafío del servidor en modo real. | Manejador de «Cambiar correo»/«Cancelar» y fachada de autenticación. | Alta | Documentar únicamente el descarte del formulario visible y el retorno al ingreso de correo. |
| Narrativa — sesión | No describía el control «Cerrar Sesión» y presentaba la vigencia de ocho horas como comportamiento visual completo. | Encabezado, contexto de autenticación y configuración de la credencial. | Media | Añadir cierre voluntario y distinguir la vigencia de la credencial de una redirección automática no demostrada. |
| Diagrama de actividades | Incluía cuenta suspendida y bloqueo temporal de 60 segundos por intentos; ambos contradicen el código actual. | Fuente PlantUML, configuración y pruebas de autenticación. | Alta | Corregir decisiones, excepciones y cierre de sesión; volver a renderizar solo esta imagen. |
| Diagrama de caso de uso | Modelaba OTP y consentimiento como inclusiones obligatorias, aunque Google sustituye al OTP y el consentimiento se omite cuando ya está vigente. | Narrativa, interfaz y flujo de consentimiento. | Alta | Usar extensiones condicionadas para OTP, Google y consentimiento; volver a renderizar solo esta imagen. |
| `SRS.md` | Conserva reglas contradictorias: fragmentos de secuencia mencionan tres intentos y bloqueo de 15 minutos, mientras la implementación vigente usa cinco intentos y bloquea el desafío. | Sección de secuencia CUS-001 y configuración/pruebas actuales. | Alta | Corregir en una iteración posterior autorizada del SRS; no reescribirlo en H01. |
| `SAD.md` | Simplifica el dominio a `@upt.pe` en varios contratos y documenta cargas de solicitud antiguas para autenticación. | Catálogo de endpoints y glosario del SAD frente a los esquemas y rutas actuales. | Media | Homologar contratos y ambos dominios en una iteración posterior autorizada. |
| `README.md` | El resumen de estado y cifras de pruebas corresponde a Sprint 4 y no demuestra el estado operativo actual de autenticación externa. | Encabezado y visión general del README frente a la rama actual y evidencias H01. | Media | Actualizar el estado global en un hito separado; no usarlo como prueba de Google/SMTP. |
| Informes de cierre previos | Declaran el CUS-001 «verificado al 100 %» y «definitivo» pese a mantener Google pendiente y a contener afirmaciones hoy refutadas. | `docs/revision_srs/CUS-001/INFORME_CIERRE.md`, matriz histórica y código actual. | Alta | Tratar esos informes como evidencia histórica; la versión H01 queda «revisable, pendiente de aprobación». |

## Clasificación funcional resultante

- **Implementado y respaldado por pruebas:** dominios institucionales, OTP de seis dígitos, vigencia de cinco minutos, reenvío con espera, cinco intentos por desafío, credencial de ocho horas, roles, consentimiento y cierre voluntario.
- **Implementado, pendiente de validación externa completa:** acceso con Google y entrega real por correo en un entorno institucional autorizado.
- **No implementado en el flujo actual:** rechazo por cuenta institucional suspendida o inhabilitada.
- **Pendiente documental posterior:** homologación focalizada de SRS, SAD y README; fuera del alcance de H01.
