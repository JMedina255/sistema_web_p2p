# 02 — Inventario Exhaustivo de Interfaces y Plan de Limpieza Visual

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)  
**Rama de Trabajo:** `feat/formalizacion-ux-roles`  
**Directorio:** `aplicacion/frontend/src/`  
**Fecha de Elaboración:** 7 de noviembre de 2026  
**Documento Relacionado:** [`01_DIAGNOSTICO_INICIAL.md`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/docs/formalizacion/01_DIAGNOSTICO_INICIAL.md)  

---

## 1. Introducción y Criterios de Auditoría

El presente documento detalla la auditoría de interfaz gráfica de usuario (GUI) para todos los componentes de la aplicación React. El objetivo es identificar cada elemento textual y de control que delate su condición de prototipo experimental de laboratorio o tarea académica, para sustituirlo por terminología institucional universitaria limpia, formal y accesible, **sin alterar en ningún momento la lógica de negocio subyacente**.

### Criterios de Clasificación de Gravedad:
- **Crítica:** Exposición de identidades falsas, fallbacks inseguros o controles que alteran la seguridad percibida.
- **Alta:** Saturación de códigos normativos (RF, RN, CUS, T-xx) visibles en títulos, botones o alertas que confunden al usuario.
- **Media:** Terminología algorítmica técnica o mensajes que mencionan a desarrolladores o estados de desarrollo en progreso.
- **Baja:** Ajustes de espaciado, iconografía inconsistente o redundancia de etiquetas.

---

## 2. Inventario Detallado de Pantallas y Componentes

### 2.1. Cascarón Principal y Navegación (`App.tsx`)
- **Ruta:** [`aplicacion/frontend/src/App.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/App.tsx)
- **Componente:** `AppShell` / `App`
- **Propósito Funcional:** Proveer la estructura visual superior, navegación institucional, conmutador de roles y punto de montaje de las vistas del sistema.
- **Hallazgos Técnicos Visibles:**
  1. Enlace externo público `Swagger /docs ↗` en la cabecera principal institucional (línea 325).
  2. Nomenclatura técnica en los botones de navegación del menú:
     - `🔐 Acceso & OTP (T-02)`
     - `⚖️ Consentimiento Ley 29733 (T-04)`
     - `📚 Catálogo Curricular (T-10)`
     - `👤 Perfil & Disponibilidad (T-11)`
     - `🏷️ Publicar Ofertas (T-14)`
     - `🎯 Recomendaciones & Reservas (T-20 / T-21 / T-23)`
     - `📅 Bandeja Reservas (T-25 / T-27)`
     - `📋 Sesiones & Quórum (T-24 / T-26)`
     - `🛡️ Panel Admin (T-04 / T-11)`
     - `🛰️ Red & Telemetría (T-01)`
  3. Valores de correo hardcodeados como *fallback* en props de vistas privilegiadas:
     - `mentorEmail={studentEmail ?? 'mentor.avanzado@upt.pe'}` (línea 906).
     - `adminEmail={studentEmail ?? 'admin.epis@upt.pe'}` (línea 912).
  4. Bloque inferior de tarjetas académicas explicativas al final de la página (líneas 926-979):
     - *"🛡️ RF03 / RN-03: Asignación de Roles por Mérito"*
     - *"📊 RN-09: Quórum Mínimo Institucional"*
     - *"⚖️ RF02 / RN-02: Ley N° 29733"*
  5. Pie de página que incluye *"Construcción de Software I"* (línea 993).
- **Gravedad:** **Crítica**
- **Propuesta de Transformación:**
  - Retirar el botón `Swagger /docs ↗` de la vista de usuario final (mantenerlo accesible solo por URL directa o en panel de desarrollador).
  - Implementar un menú contextual segmentado por rol mediante Route Guards (secciones específicas según el rol activo).
  - Renombrar las opciones de menú eliminando los códigos `(T-xx)`:
    - *Acceso Institucional*
    - *Consentimiento Informado*
    - *Catálogo de Asignaturas*
    - *Mi Perfil y Horarios*
    - *Publicar Convocatoria*
    - *Explorar Mentorías*
    - *Mis Reservas*
    - *Mis Sesiones Docentes*
    - *Administración EPIS*
  - Suprimir los valores por defecto simulados (`mentor.avanzado@upt.pe`, `admin.epis@upt.pe`). Si no hay sesión válida para esa vista, redirigir al login o denegar acceso con mensaje amigable.
  - Eliminar el bloque de tarjetas académicas del cascarón principal.
  - Actualizar el pie de página institucional a: *"Sistema Web P2P de Mentorías Académicas · Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna (2026)"*.

---

### 2.2. Acceso y Verificación OTP (`LoginOtpView.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/LoginOtpView.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/LoginOtpView.tsx)
- **Componente:** `LoginOtpView`
- **Propósito Funcional:** Permitir el ingreso institucional seguro a estudiantes y docentes mediante código de verificación único (OTP) enviado a su casilla `@upt.pe`.
- **Hallazgos Técnicos Visibles:**
  1. Barra de modo de servicio visible con botones de conmutación: `Dev Mock` y `API Real (T-03)` (líneas 207-248).
  2. Textos informativos de laboratorio: *"🔗 API Real de Autenticación & OTP (T-03 — FastAPI + Supabase)"* y *"🧪 Acceso de prueba - Simulación (Hito 3 — T-02)"*.
  3. En modo simulación, se muestra el código generado en pantalla: `mockCodeHint: '849201'` y pista textual *"Código de verificación simulado: 849201"*.
  4. Referencias en subtítulos a *"Autenticación Institucional OTP (T-02 / RF01 / RNF01)"*.
- **Gravedad:** **Alta**
- **Propuesta de Transformación:**
  - Ocultar la barra de alternancia `Dev Mock / API Real` en el entorno de presentación institucional. El frontend debe operar de forma transparente con la API real configurada en `VITE_API_BASE_URL`.
  - Retirar las pistas visuales de códigos OTP simulados. En modo institucional real, el usuario debe esperar el código en su correo o utilizar la consola de auditoría.
  - Limpiar el encabezado: *"Ingreso al Sistema de Mentorías P2P"*, con bajada *"Ingresa tu correo institucional @upt.pe para recibir tu código de acceso temporal"*.

---

### 2.3. Consentimiento Informado Ley N° 29733 (`ConsentModalView.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/ConsentModalView.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/ConsentModalView.tsx)
- **Componente:** `ConsentModalView`
- **Propósito Funcional:** Formalizar el consentimiento legal de protección de datos personales antes de habilitar el uso de la plataforma académica.
- **Hallazgos Técnicos Visibles:**
  1. Título con codificación académica: *"Consentimiento Digital Informado (RF02 / RN-02 / CUS10)"*.
  2. Alerta con referencia explícita: *"Conforme a la regla de negocio RN-02, el consentimiento es un prerrequisito bloqueante"*.
  3. Botón de simulación de fallo o bypass de pruebas.
- **Gravedad:** **Media**
- **Propuesta de Transformación:**
  - Mantener íntegra la fundamentación jurídica (Ley N° 29733 de Protección de Datos Personales de la República del Perú y Directiva UPT), ya que es un requerimiento legal formal y riguroso.
  - Eliminar los sufijos `(RF02 / RN-02 / CUS10)` del encabezado principal: *"Consentimiento para el Tratamiento de Datos Personales Académicos"*.
  - Rediseñar el mensaje preventivo: *"Para continuar utilizando la plataforma de mentorías, es indispensable que leas y aceptes los términos de tratamiento de tus datos formativos conforme a la legislación vigente."*

---

### 2.4. Catálogo Curricular (`CurriculumCatalogView.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/CurriculumCatalogView.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/CurriculumCatalogView.tsx)
- **Componente:** `CurriculumCatalogView`
- **Propósito Funcional:** Permitir a los estudiantes explorar las asignaturas del plan de estudios y los temarios silábicos oficiales disponibles para asesoría.
- **Hallazgos Técnicos Visibles:**
  1. Etiqueta del buscador: *"🔍 Buscar por curso, código o tema silábico (T-10 / RF05):"* (línea 113).
  2. Encabezado del temario: *"📋 Temario Silábico Oficial (CUS21)"* (línea 322).
  3. Badge de materias: *"Asignatura Prioritaria Filtro (EPIS-UPT)"* con factor ponderador explícito `1.2x`.
- **Gravedad:** **Media**
- **Propuesta de Transformación:**
  - Simplificar la etiqueta del buscador: *"Buscar por asignatura, código o contenido temático:"*.
  - Renombrar el encabezado de detalle a: *"Temas Silábicos Aprobados"*.
  - Convertir el badge técnico en una etiqueta formativa amigable: *"Materia Crítica Formativa"* con tooltip explicativo *"Asignatura con alta demanda de reforzamiento académico"*.

---

### 2.5. Perfil Académico y Disponibilidad Horaria (`ProfileAvailabilityView.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/ProfileAvailabilityView.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/ProfileAvailabilityView.tsx)
- **Componente:** `ProfileAvailabilityView`
- **Propósito Funcional:** Registrar la información académica del estudiante (ciclo cursado, materias de interés) y su agenda semanal de horas libres (matriz 6×11).
- **Hallazgos Técnicos Visibles:**
  1. Subtítulo: *"Configuración del Perfil Académico (CUS15 / RF04)"* (línea 357).
  2. Encabezado de agenda: *"Agenda Semanal de Disponibilidad (RF04 / CUS15)"* (línea 576).
  3. Cuadro de alerta de mérito: *"⚠️ Regla de Mérito RN-03: Tu ciclo actual (V) es menor al VII ciclo..."* (línea 448).
- **Gravedad:** **Media**
- **Propuesta de Transformación:**
  - Renombrar a títulos institucionales: *"Ficha Académica Formativa"* y *"Disponibilidad Horaria Semanal"*.
  - Preservar la regla de mérito pero con redacción institucional: *"Requisito de Mérito Académico: Para postular como Mentor Académico, el reglamento de la EPIS requiere estar matriculado en el VII ciclo o superior y haber aprobado las materias críticas."*

---

### 2.6. Publicación de Convocatorias de Mentoría (`OfferPublishView.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/OfferPublishView.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/OfferPublishView.tsx)
- **Componente:** `OfferPublishView`
- **Propósito Funcional:** Permitir a los mentores programar clases grupales de mentoría seleccionando tema, modalidad, horario y espacio físico o virtual.
- **Hallazgos Técnicos Visibles:**
  1. Nombre de mentor predeterminado hardcodeado: `mentorName = 'Joan Cristian Medina Quispe'` (línea 129).
  2. Alerta de antelación: *"⚠️ Infracción de RN-04: Antelación insuficiente... Toda mentoría debe publicarse con más de 24 horas previas"* (líneas 817-818).
  3. Etiquetas de infraestructura: *"7. Asignación de Infraestructura (Aula / Laboratorio RN-06 / Enlace Virtual RN-07)"* (línea 903).
  4. Badges en el listado reciente: *"{modalidad} · {aforo} cupos (RN-05)"* (línea 1158).
- **Gravedad:** **Alta**
- **Propuesta de Transformación:**
  - Obtener el nombre del mentor dinámicamente desde el contexto de autenticación (`user.nombres` o correo institucional), suprimiendo nombres personales fijos.
  - Rediseñar los mensajes de validación:
    - *"Antelación insuficiente: Por disposición académica, toda sesión de mentoría debe programarse con al menos 24 horas de anticipación para permitir la inscripción de los estudiantes."*
    - *"Espacio Asignado (Aula física o enlace de videoconferencia)"*.
    - Indicador de capacidad: *"{modalidad} · Capacidad máxima: {aforo} vacantes"*.

---

### 2.7. Cartelera Inteligente de Recomendaciones (`RecommendationFeedView.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/RecommendationFeedView.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/RecommendationFeedView.tsx)
- **Componente:** `RecommendationFeedView`
- **Propósito Funcional:** Presentar al mentoreado las sesiones formativas y mentores más compatibles con sus necesidades curriculares y horarios libres.
- **Hallazgos Técnicos Visibles:**
  1. Título principal: *"Cartelera Inteligente de Mentorías (EdRecSys v1.0)"* (línea 735).
  2. Mensajes de carga: *"Calculando afinidad multifactorial con EdRecSys..."* (línea 987).
  3. Badges de ciclo: *"Ciclo VII (RN-03)"* (línea 549).
  4. Panel de empty-state: *"¿Necesitas asesoría en un tema específico? (RF07 / CUS03)"* y botón *"Registrar Solicitud por Demanda (CUS03)"* (líneas 688, 712).
  5. Textos con reglas: *"Recuerda que las sesiones requieren antelación mayor a 24 horas (RN-04) y cupo libre (RN-05)"*.
- **Gravedad:** **Alta**
- **Propuesta de Transformación:**
  - Encabezado: *"Sesiones de Mentoría Recomendadas"*, con subtítulo *"Recomendaciones personalizadas según tus asignaturas y disponibilidad semanal"*.
  - Spinner de carga: *"Buscando sesiones compatibles..."*.
  - Badge de mentor: *"Mentor Acreditado · Nivel {ciclo}"*.
  - Empty-state: *"¿No encuentras una sesión en el horario que necesitas?"* con botón *"Solicitar Nueva Sesión de Reforzamiento"*.

---

### 2.8. Modal de Reserva Transaccional (`BookingModalView.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/BookingModalView.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/BookingModalView.tsx)
- **Componente:** `BookingModalView`
- **Propósito Funcional:** Confirmar la reserva de un cupo en una sesión de mentoría, advirtiendo sobre el compromiso de asistencia y la confirmación perentoria.
- **Hallazgos Técnicos Visibles:**
  1. Mensajes de error y validación técnica:
     - *"⚠️ Restricción de Autoreserva (RN-03): Como mentor titular..."* (línea 829).
     - *"⚠️ Aforo Agotado (RN-05)"* (línea 848).
     - *"⚠️ Ventana de Reserva Cerrada (T-24h / RN-08)"* (línea 907).
     - *"Aviso Normativo sobre Reserva Provisional (RN-08 / RNF07)"* (línea 913).
     - *"Concurrencia ACID (RNF07): Las vacantes mostradas son referenciales hasta que el servidor confirme la transacción bajo bloqueo pesimista."* (líneas 938-939).
- **Gravedad:** **Alta**
- **Propuesta de Transformación:**
  - Preservar la rigurosidad pedagógica pero simplificar la redacción:
    - *"No puedes reservar una vacante en una sesión que tú mismo impartes."*
    - *"Vacantes Agotadas: No quedan cupos disponibles para esta fecha."*
    - *"Inscripciones Cerradas: El plazo de inscripción finalizó 24 horas antes del inicio de la sesión."*
    - *"Reserva Inmediata: Tu cupo quedará asegurado en tiempo real al confirmar tu solicitud. Recuerda confirmar tu asistencia con antelación."*

---

### 2.9. Bandeja de Reservas del Estudiante (`StudentBookingsView.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/StudentBookingsView.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/StudentBookingsView.tsx)
- **Componente:** `StudentBookingsView`
- **Propósito Funcional:** Gestionar las reservas activas del estudiante, ratificar asistencia con anticipación y desistir oportunamente sin penalización.
- **Hallazgos Técnicos Visibles:**
  1. Mensajes que exponen tareas de desarrollo inconclusas:
     - *"🚧 Integración pendiente en backend (T-26): El servicio de ratificación en el servidor FastAPI está en desarrollo por Renzo. La interfaz está lista..."* (líneas 361-363).
     - *"🚧 Integración pendiente en backend (T-28): El servicio de desistimiento y restitución atómica de cupo en el servidor FastAPI está en desarrollo por Renzo..."* (líneas 426-428).
  2. Alertas con códigos: *"Infracción de RN-08"*, *"Infracción de RN-10"*.
  3. Controles o propiedades de tiempo simulado (`currentTime`).
- **Gravedad:** **Crítica**
- **Propuesta de Transformación:**
  - Retirar de forma inmediata los mensajes que citan a integrantes del equipo de desarrollo.
  - Conectar los botones de acción directamente con los endpoints ya implementados en el Sprint 05/06 (`/api/v1/sessions/...` y `/api/v1/bookings/...`), mostrando respuestas HTTP estándar (éxito o mensaje de error del servidor).
  - Sustituir *"Infracción de RN-08"* por: *"Plazo de confirmación vencido: La confirmación debía realizarse con más de 24 horas de antelación."*
  - Sustituir *"Infracción de RN-10"* por: *"El desistimiento voluntario solo es permitido hasta 24 horas antes del inicio para liberar la vacante a otros compañeros."*

---

### 2.10. Tablero de Sesiones del Mentor (`MentorSessionsView.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/MentorSessionsView.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/MentorSessionsView.tsx)
- **Componente:** `MentorSessionsView`
- **Propósito Funcional:** Supervisar las sesiones programadas por el mentor, revisar los alumnos inscritos, verificar el quórum mínimo (50%) y tomar decisiones de contingencia.
- **Hallazgos Técnicos Visibles:**
  1. Descripción superior: *"Supervisión pedagógica de aforo, ratificación de estudiantes y quórum institucional (RN-05 / RN-08 / RN-09)"* (línea 302).
  2. Alerta modal de contingencia: *"no alcanzó el quórum reglamentario en T-24h. Conforme a la regla RN-10, seleccione una acción resolutiva:"* (líneas 763-764).
  3. Opciones de radio con citas normativas: *"Postergar la fecha y hora de la mentoría con al menos 24 horas de antelación (RN-04)"*, *"Anular la sesión liberando a los estudiantes inscritos sin penalidad alguna (RN-10)"*.
- **Gravedad:** **Alta**
- **Propuesta de Transformación:**
  - Reemplazar la descripción por: *"Panel de Gestión de Sesiones: Monitorea las inscripciones, asistencia y estado de tus convocatorias."*
  - Ajustar el diálogo de contingencia: *"Esta sesión no alcanzó el quórum mínimo requerido (50% de vacantes confirmadas). Por favor selecciona cómo deseas proceder:"*
    - *"1. Impartir sesión con aforo reducido (continuar con los alumnos confirmados)."*
    - *"2. Reprogramar sesión (establecer una nueva fecha con al menos 24 horas de antelación)."*
    - *"3. Cancelar sesión (notificar a los inscritos y anular la convocatoria sin penalización)."*

---

### 2.11. Control de Asistencia y QR Dinámico (`SessionAttendanceView.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/SessionAttendanceView.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/SessionAttendanceView.tsx)
- **Componente:** `SessionAttendanceView`
- **Propósito Funcional:** Facilitar el pase de asistencia presencial o virtual mediante código QR dinámico con token rotatorio TOTP de 30 segundos.
- **Hallazgos Técnicos Visibles:**
  1. Títulos con notación: *"Control de Asistencias & TOTP (RF17 / CUS12 / RN-12)"*.
  2. Mensajes de consola y estado que refieren a pruebas de desarrollo.
- **Gravedad:** **Media**
- **Propuesta de Transformación:**
  - Título limpio: *"Pase de Asistencia Digital — Código QR Dinámico"*.
  - Instrucción pedagógica clara: *"Proyecta este código QR a tus estudiantes para que registren su asistencia. El código se renueva automáticamente cada 30 segundos por seguridad."*

---

### 2.12. Formulario de Bitácora Pedagógica (`BitacoraFormView.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/BitacoraFormView.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/BitacoraFormView.tsx)
- **Componente:** `BitacoraFormView`
- **Propósito Funcional:** Registrar el informe pedagógico de la sesión impartida (temas desarrollados, dificultad, observaciones de $\ge 50$ caracteres y sellado SHA-256 para acreditar horas).
- **Hallazgos Técnicos Visibles:**
  1. Título: *"Bitácora Pedagógica Post-Sesión (RF17 / CUS13 / RN-12)"*.
  2. Indicador criptográfico expuesto de forma técnica cruda: *"Hash de Integridad SHA-256: 7f83b165..."*.
- **Gravedad:** **Media**
- **Propuesta de Transformación:**
  - Título formal: *"Informe Docente de Cierre de Sesión"*.
  - Presentación del sellado de seguridad: *"Firma Digital de Integridad: Registrada satisfactoriamente para la acreditación de horas de mentoría."*

---

### 2.13. Panel de Administración y Mérito Docente (`AdminDashboardView.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/AdminDashboardView.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/AdminDashboardView.tsx)
- **Componente:** `AdminDashboardView`
- **Propósito Funcional:** Permitir a la coordinación de la EPIS gestionar roles, auditar acreditaciones de mérito docente y supervisar el quórum global de sesiones.
- **Hallazgos Técnicos Visibles:**
  1. Valor por defecto: `adminEmail = 'admin.epis@upt.pe'`.
  2. Subtítulos con notación: *"Gestión de Roles (RF03 / CUS10 / RN-03)"*, *"Supervisión de Quórum Institucional (RN-09)"*.
- **Gravedad:** **Alta**
- **Propuesta de Transformación:**
  - Condicionar la carga del componente estrictamente al rol `administrador` verificado en JWT.
  - Titulación limpia: *"Coordinación Académica EPIS — Administración de Roles y Supervisión Institucional"*.

---

### 2.14. Telemetría y Salud del Sistema (`HealthStatus.tsx`)
- **Ruta:** [`aplicacion/frontend/src/components/HealthStatus.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/HealthStatus.tsx)
- **Componente:** `HealthStatus`
- **Propósito Funcional:** Monitorear el estado de respuesta de FastAPI y PostgreSQL/Supabase.
- **Hallazgos Técnicos Visibles:**
  1. Ubicado como pestaña principal en el menú de usuario (`🛰️ Red & Telemetría (T-01)`).
  2. Muestra latencias crudas y detalles internos de infraestructura.
- **Gravedad:** **Media**
- **Propuesta de Transformación:**
  - Retirar de la navegación pública de estudiantes y mentores.
  - Reubicar como una sub-pestaña de diagnóstico dentro del panel de administración (`AdminDashboardView`), accesible únicamente por el rol `administrador`.
