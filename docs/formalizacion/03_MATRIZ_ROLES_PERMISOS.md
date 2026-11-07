# 03 — Matriz de Roles, Navegación y Políticas de Permisos RBAC

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)  
**Rama de Trabajo:** `feat/formalizacion-ux-roles`  
**Fecha de Elaboración:** 7 de noviembre de 2026  
**Documentos de Referencia:**  
- [`docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/docs/diseño/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md)  
- [`docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/docs/diseño/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md)  

---

## 1. Definición Canónica de Perfiles y Actores

Conforme a la especificación de requerimientos del **SRS (Sección 3.2)** y la arquitectura de seguridad del **SAD (Sección 6)**, el sistema define tres perfiles formales de usuario:

### 1. Perfil Mentoreado (Estudiante)
- **Definición:** Estudiante regular de la EPIS-UPT, habitualmente cursando ciclos formativos iniciales (I al IV ciclo), que busca reforzamiento académico en asignaturas filtro críticas (*Cálculo I/II, Algoritmos, POO, Base de Datos*).
- **Rol en Sistema:** `mentoreado`.
- **Condición de Entrada:** Correo institucional `@upt.pe` válido, código OTP verificado y consentimiento Ley N° 29733 aceptado.

### 2. Perfil Mentor (Estudiante Sobresaliente de Ciclos Superiores)
- **Definición:** Estudiante de ciclo formativo superior (VII al X ciclo) que ha aprobado con solvencia las asignaturas críticas y cumple la regla de mérito **RN-03**. Está facultado para impartir mentorías y certificar horas formativas.
- **Roles en Sistema:** `mentor` y `mentoreado` (todo mentor conserva también la capacidad de participar como mentoreado en otras áreas formativas, pero tiene prohibida la autoreserva en sus propias sesiones según RN-03).
- **Condición de Entrada:** Acreditación de mérito verificada por la administración institucional.

### 3. Perfil Administrador (Coordinación Académica EPIS)
- **Definición:** Autoridad de la Escuela Profesional de Ingeniería de Sistemas responsable de supervisar la ejecución del programa de mentorías, certificar el mérito docente, fiscalizar el quórum y visar bitácoras docentes para la emisión de constancias.
- **Roles en Sistema:** `administrador`, con permisos de supervisión global y visado.

---

## 2. Matriz Exhaustiva de Funcionalidades, Accesos y Controles

| Módulo / Funcionalidad | Perfil Autorizado | Lectura (R) | Creación (C) | Modificación / Cancelación (U/D) | Restricción de Propiedad (*Ownership*) | Protección Requerida en Frontend | Protección Requerida en Backend | Estado Actual de Implementación | Cambios Necesarios para Formalización |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- | :--- | :---: | :--- |
| **Acceso & OTP (RF01)** | Público institucional | Sí | Sí | No | N/A (asociado a correo `@upt.pe`) | Formulario público de login OTP. | Rate-limiting (60 s cooldown) y expiración en 5 min. | **Implementado** (con Dev Mock visible). | Ocultar botones de Mock y códigos expuestos. |
| **Consentimiento Ley 29733 (RF02)** | Todos autenticados | Sí | Sí | No | Propio usuario (`caller == sub`) | Modal bloqueante si `hasConsented == false`. | Endpoint `/api/v1/consent/*` con validación JWT. | **Implementado** (badge no bloqueante en shell). | Bloquear rutas protegidas si falta consentimiento. |
| **Catálogo Curricular (RF05)** | Todos | Sí | No | No | N/A (catálogo público) | Acceso abierto para exploración. | Endpoint `/api/v1/curriculum/courses` de solo lectura. | **Implementado** (100% funcional con Supabase). | Limpiar etiquetas `(T-10 / RF05)`. |
| **Perfil Académico (RF04)** | Todos autenticados | Sí | Sí | Sí | Solo el propio usuario (`caller == sub`) | Vista personal de perfil formativo. | Validación JWT estricta en `/api/v1/profiles/*`. | **Implementado** (usa fallback en dev). | Eliminar fallback sin JWT; vincular a `user.email`. |
| **Agenda Disponibilidad 6×11 (RF04)** | Todos autenticados | Sí | Sí | Sí | Solo el propio usuario | Grilla semanal editable. | Validación de solapamiento en backend. | **Implementado**. | Limpiar jerga `(RF04 / CUS15)`. |
| **Explorar / Recomendación Top-k (RF06)** | Mentoreado / Mentor | Sí | No | No | N/A (catálogo activo) | Vista de cartelera filtrable por materia. | Algoritmo EdRecSys en `/api/v1/recommendations/*`. | **Implementado**. | Retirar referencias a `EdRecSys v1.0` y `XAI`. |
| **Reserva Transaccional (RF12)** | Mentoreado | Sí | Sí | No | No autoreserva (RN-03: `student != mentor`) | Modal transaccional con bloqueo de envío múltiple. | Bloqueo pesimista `SELECT FOR UPDATE` en `/bookings/book`. | **Implementado**. | Limpiar textos de bloqueo pesimista y ACID. |
| **Bandeja Mis Reservas (RF13)** | Mentoreado | Sí | No | No | Solo reservas del propio estudiante | Vista de reservas personales. | Endpoint `/bookings/my-reservations` filtrado por JWT. | **Implementado**. | Enlazar identidad a sesión real; retirar mock. |
| **Ratificación de Asistencia (RF13)** | Mentoreado | Sí | No | Sí | Solo reservas del propio estudiante | Botón activo antes de $T-24\text{ h}$. | Endpoint `/sessions/confirm-attendance` con chequeo temporal. | **Implementado**. | Eliminar mensaje *"en desarrollo por Renzo"*. |
| **Desistimiento de Reserva (RF14)** | Mentoreado | Sí | No | Sí | Solo reservas del propio estudiante | Botón de desistimiento antes de $T-24\text{ h}$. | Endpoint `/bookings/cancel` con liberación de cupo inmediata. | **Implementado**. | Eliminar mensaje *"en desarrollo por Renzo"*. |
| **Publicar Convocatoria (RF08)** | Mentor | Sí | Sí | No | Solo mentores acreditados | Acceso restringido al rol `mentor`. | Endpoint `/api/v1/offers/publish` validando rol `mentor`. | **Implementado** (usa fallback Joan). | Obtener mentor de JWT; validar rol antes de abrir. |
| **Mis Sesiones de Mentoría (RF08/RF16)** | Mentor | Sí | No | Sí | Solo sesiones donde `id_mentor == caller` | Tablero restringido a rol `mentor`. | Endpoint `/api/v1/offers/mentor/{email}` validado con JWT. | **Implementado** (usa fallback mock). | Proteger ruta; filtrar exclusivamente sesiones del mentor. |
| **Resolución de Quórum T-24h (RF16)** | Mentor | Sí | No | Sí | Solo el mentor titular de la sesión | Diálogo de contingencia ante quórum $<50\%$. | Endpoint `/api/v1/quorum/decision` (PROCEED/RESCHEDULE/CANCEL). | **Implementado**. | Limpiar citas normativas `RN-10`. |
| **Pase de Asistencia QR/TOTP (RF17)** | Mentor (emite) / Mentoreado (lee) | Sí | Sí | No | Sesión propia del mentor | Generador QR para mentor / Check-in para alumno. | Token TOTP de 30 s en `/api/v1/sessions/attendance/*`. | **Implementado**. | Separar vista de emisión (mentor) y escaneo (alumno). |
| **Bitácora Pedagógica (RF17)** | Mentor (crea) / Admin (visa) | Sí | Sí | Sí | Mentor registra; Admin visa | Formulario post-sesión con validación $\ge 50$ car. | Criptosellado SHA-256 en `/api/v1/sessions/bitacora/*`. | **Implementado**. | Simplificar interfaz; retirar hash técnico crudo. |
| **Gestión de Roles & Mérito (RF03)** | Administrador | Sí | No | Sí | Todo el padrón estudiantil | Panel exclusivo de rol `administrador`. | `/api/v1/roles/promote-mentor` con autorización admin. | **Implementado** (acceso desprotegido en UI). | **URGENTE:** Bloquear vista en UI si rol $\ne$ admin. |
| **Supervisión de Quórum Global (RN-09)** | Administrador | Sí | No | No | Todas las sesiones EPIS | Pestaña de supervisión en panel admin. | Endpoint consolidado de quórum. | **Implementado**. | Integrar dentro de navegación administrativa. |
| **Telemetría y Diagnóstico** | Administrador | Sí | No | No | N/A | Sub-pestaña técnica dentro de Administración. | Endpoint `/api/v1/health/db`. | **Implementado** (pestaña pública en frontend). | Mover de menú principal a panel de administración. |

---

## 3. Auditoría de Brechas de Seguridad y Autorización Encontradas

### 3.1. Inferencia Client-Side de Roles Mediante Prefijo de Correo
- **Ubicación:** [`AuthContext.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/context/AuthContext.tsx) (líneas 67-73 y 133-140).
- **Problema:** Si el token JWT carece del campo `roles`, o en modo simulación, el cliente asigna automáticamente:
  ```typescript
  email.startsWith('admin') ? ['administrador', 'mentoreado'] :
  email.startsWith('mentor.') || email.startsWith('2022073504') ? ['mentor', 'mentoreado'] : ['mentoreado']
  ```
- **Riesgo:** Cualquier usuario puede autoproclamarse administrador ingresando un correo ficticio como `admin.prueba@upt.pe`.
- **Corrección Exigida:** Los roles deben originarse **únicamente** del payload firmado del token JWT emitido por el backend (`/api/v1/auth/verify-otp`) y respaldado por la tabla `usuario_roles` de Supabase.

### 3.2. Ausencia de Verificación Administrativa en Promoción de Terceros
- **Ubicación:** [`roles.py`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/backend/app/api/v1/endpoints/roles.py) (línea 66).
- **Problema:** Se valida que `caller_email != payload.email` para evitar autopromoción sin rol de administrador, pero no se exige que quien promueve a un tercero (`payload.email`) tenga efectivamente el rol `administrador`.
- **Riesgo:** Un estudiante mentoreado autenticado podría enviar una petición POST a `/api/v1/roles/promote-mentor` promoviendo a otro estudiante sin contar con autorización institucional.
- **Corrección Exigida:** Requerir estrictamente `"administrador" in caller_roles` para cualquier ejecución de `promote-mentor` y `revoke-mentor`.

### 3.3. Bypass de Identidad Mediante Query Parameter en Modo Desarrollo
- **Ubicación:** [`profiles.py`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/backend/app/api/v1/endpoints/profiles.py) (`_resolve_authenticated_email`) y [`bookings.py`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/backend/app/api/v1/endpoints/bookings.py).
- **Problema:** Si la cabecera `Authorization` está ausente y `APP_ENV == "development"`, se utiliza el valor del parámetro `explicit_email` o `student_email` sin comprobar credenciales.
- **Riesgo:** Genera discrepancia entre pruebas locales y producción, y permite saltarse la autenticación en demostraciones si no se configura un token válido.
- **Corrección Exigida:** En la formalización del frontend, todas las llamadas a la API deben incluir el encabezado `Authorization: Bearer <token>` obtenido tras el login OTP legítimo.

---

## 4. Matriz de Navegación Propuesta para la Experiencia de Usuario

Para ofrecer una navegación intuitiva y sin sobrecarga cognitiva, la interfaz organizará sus vistas según el perfil autenticado del usuario:

```
[ Sistema Web P2P - EPIS UPT ]
 │
 ├── (No Autenticado)
 │     ├── Iniciar Sesión (Acceso con Correo @upt.pe + OTP)
 │     └── Explorar Catálogo de Cursos (Consulta libre de materias y temarios)
 │
 ├── (Perfil: Mentoreado)
 │     ├── 1. Explorar Mentorías (Recomendaciones Top-k personalizadas + Solicitud de sesión)
 │     ├── 2. Mis Reservas (Bandeja personal: próximas sesiones, ratificar asistencia, desistimiento)
 │     ├── 3. Mi Perfil (Ficha académica, materias de interés, disponibilidad semanal 6×11)
 │     └── 4. Catálogo Curricular (Consulta de cursos y temarios oficiales)
 │
 ├── (Perfil: Mentor)
 │     ├── 1. Mis Sesiones Docentes (Supervisión de aforo, quórum y contingencias T-24h)
 │     ├── 2. Publicar Mentoría (Convocatoria de sesión grupal presencial/virtual)
 │     ├── 3. Asistencia y Bitácoras (Pase de lista con QR dinámico TOTP e informe pedagógico)
 │     ├── 4. Mi Disponibilidad (Agenda semanal de horas para dictar mentorías)
 │     └── [Conmutador de Rol a Mentoreado]
 │
 └── (Perfil: Administrador)
       ├── 1. Panel de Control (Métricas globales: sesiones activas, quórum, horas acumuladas)
       ├── 2. Gestión de Usuarios y Roles (Postulaciones a mentor, mérito RN-03, revocación)
       ├── 3. Supervisión de Sesiones (Auditoría institucional de sesiones y aforos)
       ├── 4. Diagnóstico del Sistema (Telemetría de base de datos y latencias)
       └── [Conmutador de Rol a Mentor / Mentoreado si posee el perfil]
```
