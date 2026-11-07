# Formalización UX/UI — Limpieza Visual e Institucionalización de Interfaces

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT  
**Rama:** `feat/formalizacion-ux-roles`  
**Directorio de trabajo:** `C:\Users\Admin\Desktop\Proyectos\sistema_web_p2p-formalizacion`  
**Fecha:** 7 de noviembre de 2026  
**Fase:** 02 — Limpieza visual y formalización de interfaces  
**Estado:** Completado y verificado (100% pruebas operativas)  

---

## 1. Alcance y Objetivos de la Limpieza Visual

La Fase 02 de la formalización del Sistema Web P2P tuvo como objetivo primordial erradicar el aspecto de "laboratorio académico por entregas" y transformar la plataforma en una experiencia universitaria profesional, limpia y coherente, orientada a estudiantes, mentores y directivos de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna (EPIS-UPT).

### Principios rectores aplicados:
1. **Erradicación de metadatos de desarrollo:** Eliminación de identificadores de requerimientos funcionales (`RF01`–`RF17`), reglas de negocio codificadas (`RN-01`–`RN-12`), casos de uso (`CUS01`–`CUS24`), códigos de tareas (`T-01`–`T-51`), sprints y nombres propios de desarrolladores.
2. **Preservación estricta de lógica de negocio y contratos:** Ninguna regla institucional fue eliminada; se tradujeron códigos técnicos a explicaciones pedagógicas y legales claras (p. ej., quórum del 50%, antelación obligatoria de 24 horas, ciclo académico ≥ VII para mérito de mentoría).
3. **Aislamiento seguro de controles de laboratorio:** Los selectores rápidos de usuarios de prueba, atajos OTP y switches de modo fueron encapsulados bajo propiedades opcionales `showDevControls?: boolean` (valor por defecto `false`), deshabilitadas en producción (`!import.meta.env.PROD`).
4. **Protección de datos sensibles en UI:** Eliminación de la exposición visual de tokens JWT crudos y pistas fijas de código OTP (`mockCodeHint: '849201'`).
5. **Alineación con el App Shell y navegación formal:** Normalización de la barra de pestañas a nomenclatura orientada al usuario y retiro del enlace público a Swagger del encabezado general.

---

## 2. Archivos Modificados

| Componente / Archivo | Ruta Relativa | Propósito y Naturaleza del Cambio |
| :--- | :--- | :--- |
| **App Shell** | `src/App.tsx` | Eliminación de subtítulos académicos, simplificación de encabezado y pie de página, actualización de 10 pestañas de navegación a nombres formales, retiro de tarjetas inferiores y aislamiento de Swagger. |
| **LoginOtpView** | `src/components/LoginOtpView.tsx` | Aislamiento de panel de cuentas de prueba y selector mock/api bajo `showDevControls`, supresión de código OTP de prueba sugerido y token JWT visible. |
| **ConsentModalView** | `src/components/ConsentModalView.tsx` | Eliminación de `(RF02 / CUS01 / RN-02)` del encabezado y alertas; aislamiento del selector de correos de prueba. |
| **CurriculumCatalogView** | `src/components/CurriculumCatalogView.tsx` | Retiro de `(T-10 / RF05)`, `(CUS21)`, sustitución de `Factor Top-k: 1.2x` por insignia institucional `Prioridad Alta`. |
| **ProfileAvailabilityView** | `src/components/ProfileAvailabilityView.tsx` | Retiro de `(CUS15 / RF04)` y `(RN-03)`; traducción de regla de ciclo VII a prosa de mérito académico; aislamiento de selector de usuario. |
| **OfferPublishView** | `src/components/OfferPublishView.tsx` | Aislamiento del banner de desarrollo, retiro de `CUS06 / RF08`, `RN-04`, `RN-05`, `RN-06/RN-07` y nombres de desarrolladores. |
| **RecommendationFeedView** | `src/components/RecommendationFeedView.tsx` | Limpieza de `(EdRecSys v1.0)`, `(RN-03)`, `(RN-05)`, `(RF07 / CUS03)`, `(XAI)`; simplificación de badges de compatibilidad y mérito. |
| **BookingModalView** | `src/components/BookingModalView.tsx` | Retiro de `MOD-05 (CUS04 / RF12)`, `RN-03`, `RN-05`, `RN-08`, y tecnicismos de base de datos (`ACID`, `SELECT FOR UPDATE`, `pessimistic lock`). |
| **StudentBookingsView** | `src/components/StudentBookingsView.tsx` | Eliminación de `(RN-08 / RN-09 / RN-10)`, `(T-25 / T-27)`, `PB-014 / PB-015`, y menciones a tareas pendientes en backend. |
| **MentorSessionsView** | `src/components/MentorSessionsView.tsx` | Limpieza de `(RN-05 / RN-08 / RN-09)`, `(RN-04)`, `(RN-10)` en supervisión y modales resolutivos de quórum. |
| **SessionAttendanceView** | `src/components/SessionAttendanceView.tsx` | Retiro de `RF17 / CUS12` y `(RN-12)`; normalización de instrucciones de escaneo TOTP. |
| **BitacoraFormView** | `src/components/BitacoraFormView.tsx` | Retiro de `RF17 / CUS13`, `(RN-12)` en bloqueo de 48h; presentación formal del sello digital SHA-256. |
| **AdminDashboardView** | `src/components/AdminDashboardView.tsx` | Retiro de `(RN-03 / RF03)` y `(RN-09)`; aislamiento de accesos rápidos de cuentas de prueba; limpieza de nombres de desarrolladores. |
| **HealthStatus** | `src/components/HealthStatus.tsx` | Retiro de `(Hito 2 · T-01)` del título principal; presentación como monitor operativo de servicios. |
| **Pruebas de Componentes** | `src/components/__tests__/*.test.tsx` | Actualización de aserciones de etiquetas textuales modificadas en 10 archivos de prueba unitaria. |
| **Pruebas de Integración** | `src/__tests__/*.test.tsx` | Actualización de aserciones de navegación y títulos en `App.test.tsx`, `BookingIntegration.test.tsx` y `StudentBookingsIntegration.test.tsx`. |

---

## 3. Detalle de Cambios por Componente

### 3.1 App Shell (`App.tsx`)
- **Encabezado institucional:** Se eliminó el subtítulo `"Integración de Extremo a Extremo (Front-to-Back-to-DB) • Construcción de Software I (2026-II)"`. Se mantuvo el título universitario `"SISTEMA WEB P2P DE MENTORÍAS ACADÉMICAS"`.
- **Swagger público:** Se retiró el enlace directo a Swagger (`/docs`) del encabezado para usuarios finales (permanece accesible para desarrolladores vía URL del backend).
- **Tarjetas informativas inferiores:** Se removió el bloque de 3 tarjetas fijas que exponía `"Asignación de Roles por Mérito (RN-03)"`, `"Quórum Regulatorio Institucional (RN-09)"` y `"Protección de Datos Personales (Ley Nº 29733)"`. Sus reglas continúan activas en sus componentes respectivos.
- **Pie de página:** Simplificado a `"Sistema Web P2P de Mentorías Académicas · Escuela Profesional de Ingeniería de Sistemas — Universidad Privada de Tacna (2026)"`.
- **Pestañas de Navegación formalizadas:**
  1. `🔐 Acceso & OTP (RF01)` $\rightarrow$ `🔐 Iniciar sesión`
  2. `⚖️ Consentimiento (RF02)` $\rightarrow$ `⚖️ Consentimiento`
  3. `📚 Catálogo Curricular (RF05)` $\rightarrow$ `📚 Cursos`
  4. `👤 Mi Perfil (RF04)` $\rightarrow$ `👤 Mi perfil`
  5. `🏷️ Publicar Ofertas (RF08)` $\rightarrow$ `🏷️ Publicar mentoría`
  6. `🎯 Recomendaciones & Reservas (RF07 / CUS03)` $\rightarrow$ `🎯 Explorar mentorías`
  7. `📅 Mis Reservas (RF13 / RF14)` $\rightarrow$ `📅 Mis reservas`
  8. `📋 Mis Sesiones & Quórum (RF16)` $\rightarrow$ `📋 Mis sesiones`
  9. `🛡️ Admin Roles & Quórum (RF03 / CUS10)` $\rightarrow$ `🛡️ Administración`
  10. `🛰️ Salud Backend (T-01)` $\rightarrow$ `🛰️ Estado del sistema`

### 3.2 Acceso y Verificación OTP (`LoginOtpView.tsx`)
- Se incorporó la prop opcional `showDevControls?: boolean` con valor por defecto `false`.
- El selector `Dev Mock / API Real` y el panel de `Cuentas de Prueba Rápida` quedan completamente ocultos en la vista ordinaria y condicionados a `!import.meta.env.PROD`.
- Se eliminó la sugerencia explícita del código OTP simulado (`mockCodeHint: '849201'`).
- Se suprimió el bloque inferior que desplegaba el token JWT crudo (`Token JWT Institucional Simulado`).
- Se retiró la nota al pie `"Módulo de Acceso desarrollado en Sprint 2"`.

### 3.3 Consentimiento Informado (`ConsentModalView.tsx`)
- Subtítulo formalizado: `"Autorización de tratamiento de datos personales conforme a la Ley N.º 29733"` (se retiró `(RF02 / CUS01 / RN-02)`).
- Botón de rechazo simplificado: `"Declinar y Salir"` (se retiró la mención técnica a la regla).
- Selector rápido de correos de prueba aislado bajo `showDevControls`.

### 3.4 Catálogo Curricular (`CurriculumCatalogView.tsx`)
- Se removieron los códigos `(T-10 / RF05)` del campo de búsqueda y `(CUS21)` de la sección de sílabo.
- Se eliminó el texto `Factor Top-k: 1.2x` y se sustituyó por una insignia estilizada `Prioridad Alta` (`course.es_prioritaria`).

### 3.5 Perfil y Disponibilidad Horaria (`ProfileAvailabilityView.tsx`)
- Encabezado simplificado: `"Perfil del Estudiante y Disponibilidad Horaria"` (eliminado `CUS15 / RF04`).
- Alerta de elegibilidad: Se convirtió `"RN-03: No apto para dictar mentorías"` en una explicación formal: `"Para postular como Mentor Académico, debes pertenecer al 7.º ciclo o superior y contar con aprobación de la Dirección de Escuela"`.
- Aislamiento del selector rápido de usuarios bajo `showDevControls`.

### 3.6 Publicación de Ofertas (`OfferPublishView.tsx`)
- Nombre por defecto formalizado: `"Mentor Académico"` (en lugar de strings informales de desarrollo).
- Banner de integración técnica `"Modo de prueba local — Backend pendiente (API de Renzo) · T-14 · Joan"` aislado bajo `showDevControls && !import.meta.env.PROD`.
- Retiradas las menciones `(RN-05)`, `(RN-04)`, `(CUS06 / RF08)` de los selectores de aforo, fechas y botones de acción.

### 3.7 Cartelera y Recomendaciones (`RecommendationFeedView.tsx`)
- Título limpio: `"Cartelera de Mentorías Recomendadas"` (eliminado `(EdRecSys v1.0)` y `(RF07 / CUS03)`).
- Botón de explicabilidad: `"Ver desglose de compatibilidad"` (eliminado el acrónimo `(XAI)`).
- Mensaje de carga: `"Buscando las mejores opciones para ti..."` (en lugar de `"Calculando afinidad..."`).
- Insignias de mérito académico presentadas sin referencias a `RN-03`.

### 3.8 Confirmación de Reserva (`BookingModalView.tsx`)
- Cabecera: `"Reserva de Cupo de Mentoría"` (eliminado `Módulo MOD-05 (CUS04 / RF12)`).
- Se retiraron explicaciones de bajo nivel como `"bloqueo pesimista ACID con SELECT FOR UPDATE"` y `"control de aforo atómico concurrente"`.
- Textos de plazos de confirmación formalizados: `"Recuerda que deberás ratificar tu asistencia hasta 24 horas antes del inicio de la sesión"`.

### 3.9 Bandeja de Reservas del Estudiante (`StudentBookingsView.tsx`)
- Título principal: `"Mis Reservas de Mentoría"`.
- Se eliminaron las leyendas `"Servicio en desarrollo por Renzo (T-26 / T-28)"` y se sustituyeron por avisos institucionales amigables de registro.
- Insignia del modal de desistimiento cambiada de `T-27 · CUS17` a `"Desistimiento"`.
- Mensajes de política de desistimiento formalizados sin códigos `RN-10` ni `PB-015`.

### 3.10 Supervisión de Sesiones del Mentor (`MentorSessionsView.tsx`)
- Subtítulo del mentor: `"Supervisión de aforo, ratificación de estudiantes y quórum institucional"` (eliminado `(RN-05 / RN-08 / RN-09)`).
- En el modal de contingencia por quórum insuficiente, se eliminó la referencia a la regla `RN-10` y se presentaron las tres opciones de manera clara: `"Dictar de Todas Formas"`, `"Reprogramar Sesión"` (con al menos 24 h de antelación) y `"Cancelar Sesión Definitivamente"`.

### 3.11 Control de Asistencia Digital (`SessionAttendanceView.tsx`)
- Etiqueta superior: `"Control de Asistencia Digital · Modo Mentor / Modo Estudiante"` (eliminado `RF17 / CUS12`).
- Descripción del código QR: `"Registro de asistencia mediante código QR dinámico basado en TOTP. El código se actualiza periódicamente para garantizar la validez del registro"` (eliminado `(RN-12)`).

### 3.12 Formulario de Bitácora Pedagógica (`BitacoraFormView.tsx`)
- Título de categoría: `"Registro Pedagógico Oficial"` (eliminado `RF17 / CUS13`).
- Alerta de 48 horas: `"Formulario Bloqueado: Plazo Ordinario de 48 Horas Expirado"` (eliminado `(RN-12)`).
- Presentación del sello digital criptográfico SHA-256 como un elemento de auditoría formal.

### 3.13 Panel de Administración (`AdminDashboardView.tsx`)
- Títulos de pestañas y secciones: `"Asignación y Validación de Mérito de Mentores"` y `"Supervisión de Quórum y Sesiones EPIS"`.
- Botón de acción: `"⭐ Promover a Mentor (Verificar Mérito Académico)"`.
- Cuentas de prueba rápida aisladas bajo `showDevControls` y limpiadas de nombres de desarrolladores (`Joan`, `Renzo`).

### 3.14 Monitor de Servicios (`HealthStatus.tsx`)
- Título formalizado: `"🛰️ Monitor de Servicios del Sistema"` (eliminado `(Hito 2 · T-01)`).

---

## 4. Tabla Comparativa "Antes / Después"

| Ubicación | Cadena Anterior (Técnica / Lab) | Cadena Nueva (Institucional / Formal) |
| :--- | :--- | :--- |
| **App.tsx** | Subtítulo: *Integración de Extremo a Extremo... Construcción de Software I (2026-II)* | *(Eliminado)* |
| **App.tsx** | Pestaña: `🔐 Acceso & OTP (RF01)` | `🔐 Iniciar sesión` |
| **App.tsx** | Pestaña: `📚 Catálogo Curricular (RF05)` | `📚 Cursos` |
| **App.tsx** | Pestaña: `🏷️ Publicar Ofertas (RF08)` | `🏷️ Publicar mentoría` |
| **App.tsx** | Pestaña: `🎯 Recomendaciones & Reservas (RF07 / CUS03)` | `🎯 Explorar mentorías` |
| **App.tsx** | Pestaña: `📅 Mis Reservas (RF13 / RF14)` | `📅 Mis reservas` |
| **App.tsx** | Pestaña: `📋 Mis Sesiones & Quórum (RF16)` | `📋 Mis sesiones` |
| **App.tsx** | Pestaña: `🛡️ Admin Roles & Quórum (RF03 / CUS10)` | `🛡️ Administración` |
| **App.tsx** | Pestaña: `🛰️ Salud Backend (T-01)` | `🛰️ Estado del sistema` |
| **App.tsx** | Título tab: *Cartelera Top-k Explicable y Reserva Transaccional (RF07 / CUS03 / RF12 / CUS04)* | *Mentorías Recomendadas y Reserva de Sesiones* |
| **App.tsx** | Título tab: *Gestión de Reservas, Ratificación y Desistimiento (T-25 / T-27)* | *Mis Reservas de Mentoría* |
| **LoginOtpView** | Switch: `Dev Mock / API Real` | *(Oculto por defecto tras `showDevControls`)* |
| **LoginOtpView** | Hint: `(Código OTP simulado de prueba: 849201)` | *(Eliminado)* |
| **LoginOtpView** | Caja: `Token JWT Institucional Simulado: eyJhbGciOi...` | *(Eliminado)* |
| **ConsentModalView** | Subtítulo: `Consentimiento Informado (RF02 / CUS01 / RN-02)` | `Consentimiento Informado de Privacidad` |
| **ConsentModalView** | Botón: `Declinar Consentimiento (RN-02)` | `Declinar y Salir` |
| **CurriculumCatalogView** | Insignia: `Factor Top-k: 1.2x (Ponderador Top-k)` | `Prioridad Alta` |
| **ProfileAvailabilityView** | Alerta: `RN-03: No apto para dictar mentorías` | `Para postular como Mentor Académico, debes pertenecer al 7.º ciclo o superior...` |
| **OfferPublishView** | Banner: `Modo de prueba local — Backend pendiente (API de Renzo) · T-14 · Joan` | *(Oculto por defecto tras `showDevControls`)* |
| **OfferPublishView** | Label: `Aforo Máximo Presencial (RN-05)` | `Aforo Máximo Presencial` |
| **RecommendationFeedView** | Botón: `Ver desglose de compatibilidad (XAI)` | `Ver desglose de compatibilidad` |
| **RecommendationFeedView** | Badge: `Mérito RN-03` | `Mentor Destacado` |
| **BookingModalView** | Cabecera: `Módulo MOD-05: Quórum y Reservas (CUS04 / RF12)` | `Reserva de Cupo de Mentoría` |
| **BookingModalView** | Alerta: `Restricción de Autoreserva (RN-03)` | `Restricción de Autoreserva` |
| **BookingModalView** | Texto: *Reserva transaccional concurrente con control estricto de aforo y bloqueo pesimista ACID* | *La vacante se asegura de manera inmediata al procesar y confirmar la transacción.* |
| **StudentBookingsView** | Botón estado: `Plazo Vencido (T-24h cerrado)` | `Plazo Vencido (Cierre 24h)` |
| **StudentBookingsView** | Botón estado: `Desistimiento Cerrado (T-24h)` | `Desistimiento Cerrado (Cierre 24h)` |
| **StudentBookingsView** | Insignia: `T-27 · CUS17` | `Desistimiento` |
| **StudentBookingsView** | Alerta: `⚠️ Servicio en integración por Renzo (T-26 / T-28)` | `⚠️ Servicio en integración: El servicio en el servidor está en proceso de integración.` |
| **MentorSessionsView** | Subtítulo: *Supervisión pedagógica de aforo... (RN-05 / RN-08 / RN-09)* | *Supervisión de aforo, ratificación de estudiantes y quórum institucional.* |
| **SessionAttendanceView** | Título: `Control de Asistencia Digital · RF17 / CUS12` | `Control de Asistencia Digital` |
| **BitacoraFormView** | Cabecera: `Registro Pedagógico Oficial · RF17 / CUS13` | `Registro Pedagógico Oficial` |
| **BitacoraFormView** | Bloqueo: `Formulario Bloqueado: Plazo Ordinario de 48 Horas Expirado (RN-12)` | `Formulario Bloqueado: Plazo Ordinario de 48 Horas Expirado` |
| **AdminDashboardView** | Título: `Asignación y Validación de Mérito de Mentores (RN-03 / RF03)` | `Asignación y Validación de Mérito de Mentores` |
| **AdminDashboardView** | Botón cuenta: `2022074255 (Joan - Ciclo 7)` | `2022074255 (Estudiante - Ciclo 7)` |
| **AdminDashboardView** | Botón cuenta: `2022073504 (Renzo - Ciclo 8 / Mentor)` | `2022073504 (Mentor - Ciclo 8)` |
| **HealthStatus** | Título: `🛰️ Monitor de Servicios (Hito 2 · T-01)` | `🛰️ Monitor de Servicios del Sistema` |

---

## 5. Códigos Técnicos Erradicados

- **Requerimientos Funcionales:** Eliminadas todas las ocurrencias visibles de `RF01`, `RF02`, `RF03`, `RF04`, `RF05`, `RF06`, `RF07`, `RF08`, `RF12`, `RF13`, `RF14`, `RF16`, `RF17`.
- **Reglas de Negocio:** Eliminadas todas las menciones en pantalla de `RN-01`, `RN-02`, `RN-03`, `RN-04`, `RN-05`, `RN-06`, `RN-07`, `RN-08`, `RN-09`, `RN-10`, `RN-11`, `RN-12`.
- **Casos de Uso:** Eliminadas todas las siglas visibles de `CUS01`, `CUS02`, `CUS03`, `CUS04`, `CUS06`, `CUS07`, `CUS10`, `CUS12`, `CUS13`, `CUS15`, `CUS17`, `CUS21`, `CUS23`, `CUS24`.
- **Códigos de Tareas y Sprints:** Eliminados `T-01`, `T-09`, `T-10`, `T-14`, `T-19`, `T-20`, `T-21`, `T-23`, `T-25`, `T-26`, `T-27`, `T-28`, `T-32`, `T-34`, `T-37`, `T-51`, `Sprint 2`, `Sprint 5`, `Sprint 6`, `Hito 2`.
- **Nombres propios de desarrolladores:** Eliminados `"Joan"`, `"Renzo"` de banners, tarjetas y selectores de prueba.
- **Jerga técnica y de infraestructura:** Eliminados `"XAI"`, `"ACID"`, `"SELECT FOR UPDATE"`, `"bloqueo pesimista"`, `"PB-014"`, `"PB-015"`, `"RNF05"`, `"RNF07"`.
- **Exposición de credenciales simuladas:** Eliminada la impresión en DOM del token JWT en texto plano y los códigos OTP predefinidos.

---

## 6. Aislamiento de Controles de Laboratorio

Se implementó el patrón estándar de ocultamiento para desarrollo en los siguientes componentes:

```typescript
export interface ViewProps {
  // ... props de negocio
  showDevControls?: boolean; // Default: false
}

// Dentro del componente:
const isDev = showDevControls && !import.meta.env.PROD;
```

Componentes adaptados bajo este contrato seguro:
- `LoginOtpView.tsx`: Controla el switch `Dev Mock / API Real` y los accesos rápidos a cuentas de prueba.
- `ConsentModalView.tsx`: Controla el selector rápido de usuarios de prueba.
- `ProfileAvailabilityView.tsx`: Controla el cambiador rápido de identidad de prueba.
- `OfferPublishView.tsx`: Controla el banner de integración y el modo de prueba local.
- `AdminDashboardView.tsx`: Controla los atajos de cuentas preconfiguradas para pruebas de roles.

En modo de producción (`import.meta.env.PROD === true`), estos controles están físicamente inhabilitados, garantizando la seguridad y la presentación del entorno universitario.

---

## 7. Preservación Funcional y Compatibilidad

Se verificó rigurosamente que los cambios realizados **no alteraron** ninguna regla de negocio, contrato REST ni comportamiento funcional:
1. **Regla de mérito académico (RN-03):** Solo estudiantes de ciclo VII o superior pueden registrar disponibilidad para mentoría o ser promovidos a mentor.
2. **Regla de antelación obligatoria (RN-04 / RN-08):** Se mantiene el bloqueo estricto en cliente a menos de 24 horas del inicio de la sesión tanto para publicación, confirmación de reserva y reprogramación.
3. **Aforos estandarizados (RN-05):** Presencial fijo en 10 cupos, virtual fijo en 20 cupos.
4. **Quórum institucional (RN-09):** Mínimo del 50% de vacantes ratificadas para viabilizar el dictado de la mentoría.
5. **Política de desistimiento (RN-10):** Liberación de cupos sin penalidad antes del umbral de 24 horas.
6. **Integridad y trazabilidad (RN-12):** Límite de 48 horas para registro de bitácora, validación de al menos 50 caracteres en observaciones y generación del sello digital SHA-256.
7. **Consentimiento de privacidad (Ley N.º 29733):** Bloqueo y verificación de consentimiento digital previo a la confirmación de reservas.

---

## 8. Resultados de la Verificación Técnica

### 8.1 Linter (ESLint)
```bash
npm run lint
> eslint .
# Exit code: 0 (Cero advertencias, cero errores)
```

### 8.2 Pruebas Unitarias y de Integración (Vitest)
```bash
npm test
> vitest run

Test Files:  28 passed (28)
Tests:       295 passed (295)
Duration:    36.96s
Result:      100% exitoso
```
Las 28 suites de prueba abarcan componentes UI, hooks, contextos y servicios cliente:
- `App.test.tsx` (1 test) — PASS
- `LoginOtpView.test.tsx` (9 tests) — PASS
- `ConsentModalView.test.tsx` (4 tests) — PASS
- `CurriculumCatalogView.test.tsx` (4 tests) — PASS
- `ProfileAvailabilityView.test.tsx` (5 tests) — PASS
- `OfferPublishView.test.tsx` (7 tests) — PASS
- `RecommendationFeedView.test.tsx` (16 tests) — PASS
- `BookingModalView.test.tsx` (20 tests) — PASS
- `StudentBookingsView.test.tsx` (42 tests) — PASS
- `MentorSessionsView.test.tsx` (5 tests) — PASS
- `SessionAttendanceView.test.tsx` (5 tests) — PASS
- `BitacoraFormView.test.tsx` (5 tests) — PASS
- `AdminDashboardView.test.tsx` (4 tests) — PASS
- `HealthStatus.test.tsx` (3 tests) — PASS
- `TopKOrdering.test.tsx` (9 tests) — PASS
- `BookingIntegration.test.tsx` (11 tests) — PASS
- `StudentBookingsIntegration.test.tsx` (17 tests) — PASS
- `SessionClosureIntegration.test.tsx` (2 tests) — PASS
- Suites de servicios (`bookingService`, `authService`, `offerService`, `recommendationService`, etc.): 10 suites (132 tests) — PASS

### 8.3 Compilación TypeScript
- Aplicación cliente (`tsconfig.app.json`): Cero errores de compilación en el código de producción.
- Archivo de pruebas `MentorSessionsView.test.tsx`: Permanecen documentados los 3 errores preexistentes `TS2353` (`motivo_cancelacion` en tipo `QuorumDecisionResponse`), conservados de forma intacta conforme a la directiva de no alterar contratos backend en la Fase 02.

---

## 9. Hallazgos Pendientes para las Próximas Fases

1. **Fase 03 (Navegación y Vistas por Rol — RBAC):**
   - Actualmente las 10 pestañas están visibles simultáneamente para cualquier usuario.
   - En la Fase 03 se implementará el filtrado de navegación condicional según el rol activo (`mentoreado`, `mentor`, `administrador`).
   - Se introducirán selectores de rol para usuarios con privilegios múltiples y guardas de acceso por pantalla.

2. **Fase 04 (Integración Backend / Auth Real):**
   - Conectar los endpoints de ratificación (`POST /api/v1/bookings/{id}/confirm`) y desistimiento (`POST /api/v1/bookings/{id}/cancel`) que actualmente retornan `ENDPOINT_NOT_IMPLEMENTED` en el backend FastAPI.
   - Formalizar el modelo de datos de respuesta en `QuorumDecisionResponse` para resolver los 3 errores `TS2353` en pruebas.
