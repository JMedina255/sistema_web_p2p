# Bitácora de Ejecución — Sprint 2: Roles, Currículo y Perfiles

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería (EPIS)  
**Semestre Académico:** 2026-II  
**Equipo:** Grupo 03 — Joan Cristian Medina Quispe (Joan) y Renzo Antonio Antayhua Mamani (Renzo)  
**Rama de trabajo:** `feat/sprint-02-roles-curriculo-perfiles`  
**Fecha de corte:** 23/10/2026  
**Commit de integración del Sprint:** [`3766a08`](https://github.com/JMedina255/sistema_web_p2p/commit/3766a08fa98d49bc6107a9fd278568f289f7fe74) y consolidación backend Sprint 02  

> [!NOTE]
> **Alcance de la Sesión de Cierre del Sprint 2 (23/10/2026):**  
> En esta sesión se culminó la totalidad del alcance planificado para el Sprint 2: las tres tareas de cliente asignadas a Joan (**T-04**, **T-10** y **T-11**) y las cuatro tareas de persistencia, lógica de negocio y seguridad asignadas a Renzo (**T-05**, **T-08**, **T-12** y **T-13**). Se validaron 150 pruebas automatizadas (66 en frontend con Vitest y 84 en backend con Pytest) con 0 fallas y una cobertura superior al 90%, cerrando formalmente el ciclo mediante el Definition of Done (DoD).

---

## 1. Visión General y Alcance del Sprint 2

El **Sprint 2** tiene como objetivo consolidar la gobernanza legal de protección de datos personales conforme a la **Ley N° 29733** (**RF02** / **RN-02**), enriquecer la exploración interactiva del catálogo curricular oficial (**RF05** / **CUS21**), administrar la jerarquía de roles institucionales y verificación de mérito (**RF03** / **CUS10** / **RN-03**), y capturar los perfiles formativos junto a la agenda semanal de disponibilidad horaria (**RF04** / **CUS15**), insumo indispensable para el motor de recomendación Top-k (Sprint 4).

A continuación, se presenta la matriz canónica de asignación y esfuerzo planificado para el Sprint 2, certificando el cumplimiento del 100% de las actividades programadas:

### Cuadro 1.1: Actividades y Estado Técnico de Desarrollo del Sprint 2

| ID | Actividad Oficial | Responsable | Estimación Planificada (h) | Estado Técnico Actual | Entregable / Evidencia |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **T-04** | Desarrollar formulario de consentimiento digital. | Joan | 2 | **Verificado localmente** ✅ | Componente `ConsentModalView.tsx`, servicio `consentService.ts` y 9 pruebas Vitest. |
| **T-05** | Implementar persistencia del consentimiento. | Renzo | 1 | **Verificado localmente** ✅ | Tabla `consentimientos_legales`, marcas temporales UTC, endpoint de persistencia y 5 pruebas Pytest. |
| **T-08** | Desarrollar endpoints de administración de roles. | Renzo | 3 | **Verificado localmente** ✅ | Tabla `usuario_roles`, endpoints de roles, verificación de mérito RN-03 y 7 pruebas Pytest. |
| **T-10** | Implementar interfaz de consulta del catálogo curricular. | Joan | 2 | **Verificado localmente** ✅ | Componente `CurriculumCatalogView.tsx` con buscador en tiempo real y temas silábicos. |
| **T-11** | Desarrollar formulario de perfiles y disponibilidad. | Joan | 3 | **Verificado localmente** ✅ | Componente `ProfileAvailabilityView.tsx`, `profileService.ts` y grilla semanal 6×11. |
| **T-12** | Implementar API de perfiles y horarios. | Renzo | 2 | **Verificado localmente** ✅ | Tablas `perfiles_academicos`, `disponibilidades_horarias`, endpoints REST y 11 pruebas Pytest. |
| **T-13** | Ejecutar pruebas de autorización entre usuarios. | Renzo | 1 | **Verificado localmente** ✅ | Pruebas de seguridad RLS: aislamiento de perfiles privados, denegación de autopromoción y script SQL (11 pruebas Pytest). |

Fuente: Elaboración propia a partir de `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (Tabla 5.3) y avance consolidado en la rama `feat/sprint-02-roles-curriculo-perfiles`.

El cuadro anterior sintetiza la culminación de 14 horas hombre distribuidas equitativamente entre la capa de interfaz y la infraestructura de persistencia, garantizando la trazabilidad hacia el diseño arquitectónico del SAD y SRS.

---

## 2. Registro de Ejecución — Tarea T-04 (Consentimiento Digital — Ley N° 29733)

### 2.1. Alcance Implementado
- **Componente Interactivo (`aplicacion/frontend/src/components/ConsentModalView.tsx`):**
  - Implementación del formulario institucional de consentimiento informado para el tratamiento de datos personales, en estricto cumplimiento del marco legal de la **Ley N° 29733 (Ley de Protección de Datos Personales del Perú)** y su Reglamento (D.S. N° 003-2013-JUS) (**RF02** / **CUS01**).
  - Bloque normativo institucional scrollable y accesible (`role="region"` y `aria-label`) que explicita:
    1. *Finalidad exclusiva:* tratamiento de calificaciones y asignaturas filtro matriculadas para el algoritmo Top-k y convalidación de horas extracurriculares.
    2. *Datos tratados:* correo institucional, código de estudiante, notas de cursos filtro, temas declarados de refuerzo/fortaleza y agenda horaria semanal.
    3. *Ejercicio de Derechos ARCO:* información clara para solicitar acceso, rectificación, cancelación u oposición ante la Dirección de la EPIS-UPT.
    4. *Prohibición de transferencia:* garantía de no comercialización ni cesión a terceros ajenos a la UPT.
  - **Casilla de Conformidad Expresa:** checkbox obligatorio que condiciona la habilitación del botón *"Aceptar y Continuar"*.
  - **Bloqueo Preventivo ante Rechazo (Regla RN-02):** botón *"Rechazar y Salir"* que cancela la sesión, revoca el consentimiento y emite una alerta informativa bloqueando el acceso a las funciones del sistema.
  - **Soporte de Auditoría:** visualización de la marca temporal UTC y versión de términos (`2026-II-v1.0`) cuando el consentimiento se encuentra formalizado.

- **Servicio y Adaptador de Datos (`aplicacion/frontend/src/services/consentService.ts`):**
  - Interfaz tipada `ConsentStatus` (`hasConsented`, `consentedAt`, `termsVersion`, `email`, `mode`).
  - Métodos `getConsentStatus()`, `acceptConsent()` y `revokeConsent()`.
  - Modo dual (`mock` / `api`): persistencia en `localStorage` para pruebas deterministas y contrato listo para consumir `POST /api/v1/consent/accept` en integración con el backend.

### 2.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se detalla la matriz de verificación de las 9 pruebas automatizadas asociadas a la tarea T-04:

### Cuadro 2.1: Matriz de Pruebas de Consentimiento Digital (T-04)

| Componente / Suite | Escenario de Prueba | Comportamiento Esperado | Resultado Observado | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **`consentService`** | Consulta de usuario no registrado | Retornar `hasConsented: false` y versión vigente | `hasConsented: false`, `termsVersion: 2026-II-v1.0` | ✅ Exitoso |
| **`consentService`** | Aceptación con correo institucional | Registrar timestamp UTC y persistir estado | `success: true`, estampa temporal registrada | ✅ Exitoso |
| **`consentService`** | Intento con correo externo (`@gmail.com`) | Rechazar por falta de dominio institucional | Lanza error de validación de dominio `@upt.pe` | ✅ Exitoso |
| **`consentService`** | Revocación o rechazo voluntario | Limpiar registro y dejar `hasConsented: false` | `hasConsented: false` verificado en almacén | ✅ Exitoso |
| **`consentService`** | Consulta con correo vacío | Manejar cadena vacía retornando false sin excepciones | `hasConsented: false` sin excepciones | ✅ Exitoso |
| **`ConsentModalView`** | Renderizado del encabezado institucional | Desplegar título, badge y cláusulas Ley 29733 | Elementos del DOM presentes y accesibles | ✅ Exitoso |
| **`ConsentModalView`** | Control de botón de aceptación | Permanecer deshabilitado hasta marcar checkbox | Botón `disabled` pasa a activo tras clic | ✅ Exitoso |
| **`ConsentModalView`** | Flujo de aceptación exitosa | Disparar callback `onConsentAccepted` y mensaje | Callback ejecutado, notificación verde desplegada | ✅ Exitoso |
| **`ConsentModalView`** | Flujo de rechazo bloqueante (RN-02) | Disparar callback `onConsentRejected` y alerta | Callback invocado, mensaje de bloqueo visible | ✅ Exitoso |

Fuente: Pruebas unitarias en `src/services/__tests__/consentService.test.ts` y `src/components/__tests__/ConsentModalView.test.tsx`.

Las comprobaciones unitarias validan que la vista del cliente opera en estricta sujeción a las garantías procesales de la Ley N° 29733, imposibilitando la continuación de la navegación ante la omisión del consentimiento.

---

## 3. Registro de Ejecución — Tarea T-10 (Consulta Avanzada del Catálogo Curricular)

### 3.1. Alcance Implementado
- **Componente Enriquecido (`aplicacion/frontend/src/components/CurriculumCatalogView.tsx`):**
  - Evolución de la vista base del Sprint 1 hacia una **interfaz de consulta y exploración curricular avanzada** conforme a **RF05** y **CUS21**:
    1. **Buscador Reactivo en Tiempo Real:** entrada de texto que filtra instantáneamente por nombre de asignatura (*Cálculo I*, *Base de Datos*), código oficial (*CALC-101*, *BDD-401*) y búsqueda profunda dentro de la taxonomía de temas silábicos (*Límites*, *Punteros*, *Recursividad*, *Normalización*, *Herencia*).
    2. **Filtro Multifactorial por Ciclo:** selector dinámico para aislar materias por ciclo formativo (Todos, Ciclo I, II, III o IV).
    3. **Delimitación de Cursos Críticos:** casilla para filtrar exclusivamente las 5 materias filtro formativas con alta tasa de deserción.
    4. **Contador Dinámico de Coincidencias:** badge informativo que indica cuántas materias y temas cumplen con los criterios de búsqueda.
    5. **Visualizador Jerárquico de Sílabo:** desglose de unidades conceptuales silábicas con resaltado visual (`badge` *"Coincidencia"*) en los temas que concuerdan con el término ingresado.
    6. **Ponderador Top-k:** visualización de créditos lectivos y factor de ponderación algorítmica para recomendación (ej. `1.2x`, `1.3x`).

### 3.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se detalla la matriz de pruebas automatizadas que verifican el comportamiento interactivo del catálogo:

### Cuadro 3.1: Matriz de Pruebas de Consulta Curricular Avanzada (T-10)

| Prueba Automatizada | Escenario Evaluado | Comportamiento Esperado | Resultado Observado | Estado |
| :--- | :--- | :--- | :--- | :---: |
| `test 1: Render inicial` | Carga del catálogo desde API | Desplegar tarjetas con Cálculo I y Algoritmos | 2 asignaturas iniciales renderizadas | ✅ Exitoso |
| `test 2: Detalle silábico` | Clic en asignatura Algoritmos | Cargar detalle con unidad silábica de Punteros C++ | Temas silábicos desplegados en panel derecho | ✅ Exitoso |
| `test 3: Buscador textual` | Ingreso de término `"CALC"` en buscador | Mantener Cálculo I y ocultar Algoritmos | Filtrado en tiempo real verificado en DOM | ✅ Exitoso |
| `test 4: Manejo de errores` | Fallo de conexión de red simulado | Desplegar alerta amigable de error al usuario | Alerta `role="alert"` con texto informativo | ✅ Exitoso |

Fuente: Pruebas unitarias en `src/components/__tests__/CurriculumCatalogView.test.tsx`.

El catálogo interactivo satisface el requerimiento de accesibilidad y exploración en tiempo real, garantizando la navegación intuitiva a través de los temas silábicos de las materias críticas de la carrera.

---

## 4. Registro de Ejecución — Tarea T-11 (Perfiles Formativos y Matriz de Disponibilidad)

### 4.1. Alcance Implementado
- **Componente Integral (`aplicacion/frontend/src/components/ProfileAvailabilityView.tsx`):**
  - Interfaz organizada en dos secciones funcionales vinculadas conforme a **RF04**, **CUS15**, **RNF04** y **RNF08**:
    1. **Pestaña 1 — Perfil Formativo Académico:**
       - Selector de Ciclo Académico Actual (Ciclos I al X).
       - Selector de Rol / Intención: *Mentoreado* (demanda de asesoría) vs. *Postulante a Mentor* (oferta formativa).
       - **Validación de Mérito Institucional (Regla RN-03):** detección preventiva y alerta visible si un estudiante con ciclo $< \text{VII}$ intenta postularse a Mentor, informando que la tutoría avanzada está normativamente restringida a los ciclos VII a X.
       - Selección interactiva de materias filtro de interés (necesidades o fortalezas) sobre el catálogo EPIS-UPT.
       - Selector de Modalidad Preferida: *Presencial* (laboratorios EPIS), *Virtual* (Google Meet/Discord) o *Híbrida*.
       - Campo de texto para semblanza y temas específicos de enfoque.
    2. **Pestaña 2 — Agenda Semanal de Disponibilidad Horaria:**
       - Grilla interactiva semanal: **6 columnas de días (Lunes a Sábado)** × **11 franjas horarias de 1 hora (08:00 a 20:00)**.
       - Alternancia de disponibilidad mediante clic en celdas (indicador visual de color verde esmeralda y marca de verificación).
       - Atajos rápidos de selección masiva: *"🌅 Mañanas (08:00 - 12:00)"*, *"🌇 Tardes (14:00 - 18:00)"* y *"🗑️ Limpiar semana"*.
       - Contador reactivo de bloques comprometidos (ej. *"8 bloques de 1 hora seleccionados"*).
  - Botón de guardado unificado *"💾 Guardar Perfil y Disponibilidad"* con feedback de carga y alertas de confirmación.

- **Servicio y Adaptador (`aplicacion/frontend/src/services/profileService.ts`):**
  - Interfaces tipadas `AcademicProfile` y `AvailabilitySlot`.
  - Métodos `getProfile()`, `saveProfile()`, `getAvailability()`, `saveAvailability()` y `validateMentorEligibility()`.
  - Persistencia local en modo mock en `localStorage` con claves `p2p_profile_*` y `p2p_availability_*`, asegurando persistencia entre recargas y pruebas sin depender del backend.

### 4.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se presenta la matriz de resultados de las pruebas unitarias y de integración de la vista de perfiles y agenda horaria:

### Cuadro 4.1: Matriz de Pruebas de Perfiles y Disponibilidad Horaria (T-11)

| Suite / Prueba | Escenario Evaluado | Comportamiento Esperado | Resultado Observado | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **`profileService`** | Validación de regla RN-03 | Ciclo 6: ineligible; Ciclo 7 y 10: eligible | Booleanos correctos y mensaje de regla | ✅ Exitoso |
| **`profileService`** | Obtención de perfil por defecto | Retornar perfil institucional inicializado | Perfil tipado con materias de interés | ✅ Exitoso |
| **`profileService`** | Guardado y recuperación | Persistir biografía y modalidad virtual | Datos idénticos recuperados en consulta | ✅ Exitoso |
| **`profileService`** | Bloqueo de postulación inválida | Lanzar error si rol mentor tiene ciclo < 7 | Excepción con motivo RN-03 arrojada | ✅ Exitoso |
| **`profileService`** | Guardado de agenda horaria | Persistir array de slots y contar total | 2 slots guardados con horarios correctos | ✅ Exitoso |
| **`ProfileView`** | Render inicial de formulario | Desplegar selectores de ciclo y rol | Elementos interactivos presentes | ✅ Exitoso |
| **`ProfileView`** | Disparo de alerta RN-03 | Mostrar advertencia al pulsar Postulante a Mentor | Banner rojo de mérito RN-03 visible | ✅ Exitoso |
| **`ProfileView`** | Pestaña de agenda semanal | Mostrar grilla de Lunes a Sábado | 6 columnas de días y horarios renderizados | ✅ Exitoso |
| **`ProfileView`** | Botón Limpiar agenda | Reiniciar selección horaria a 0 horas | Contador indica `0 bloques de 1 hora` | ✅ Exitoso |
| **`ProfileView`** | Guardado exitoso general | Guardar datos y disparar callback `onSaved` | Mensaje de éxito y callback ejecutado | ✅ Exitoso |

Fuente: Pruebas unitarias en `src/services/__tests__/profileService.test.ts` y `src/components/__tests__/ProfileAvailabilityView.test.tsx`.

La implementación de la matriz semanal garantiza la granularidad de 1 hora requerida por el motor de emparejamiento, previniendo solapamientos y verificando en cliente las restricciones de ciclo institucional.

---

## 5. Registro de Ejecución — Tarea T-05 (Persistencia del Consentimiento — Ley N° 29733)

### 5.1. Alcance Técnico Implementado
Con el propósito de garantizar la validez legal, probatoria y auditable de la aceptación de términos bajo la **Ley N° 29733**, se construyó la infraestructura de persistencia relacional en PostgreSQL y la capa de servicios backend (**T-05** / **RF02** / **RN-02**):

1. **Definición Relacional DDL (`aplicacion/backend/app/db/migrations/versions/002_roles_and_profiles.py`):**
   - Creación de la tabla `consentimientos_legales` con identificador autoincremental `id_consentimiento`, correo institucional indexado `email VARCHAR(255)`, versión de términos `terms_version VARCHAR(50)` (predeterminado `'2026-II-v1.0'`), estado booleano `accepted`, estampa temporal UTC `consented_at TIMESTAMPTZ`, dirección IP de origen `ip_address VARCHAR(45)` y cadena del agente de usuario `user_agent TEXT`.
2. **Modelo ORM SQLAlchemy (`aplicacion/backend/app/models/consent.py`):**
   - Entidad `ConsentimientoLegal` mapeada a la tabla `consentimientos_legales` con tipado estricto `Mapped[...]`.
3. **Esquemas de Validación Pydantic v2 (`aplicacion/backend/app/schemas/consent.py`):**
   - `ConsentStatusResponse`, `ConsentAcceptRequest`, `ConsentRevokeRequest` y `ConsentOperationResponse`, provistos de validadores con expresiones regulares que exigen pertenencia al dominio oficial `@upt.pe`.
4. **Capa de Servicios y Endpoints REST (`app/services/consent_service.py` y `app/api/v1/endpoints/consent.py`):**
   - `GET /api/v1/consent/status`: consulta de vigencia por correo institucional.
   - `POST /api/v1/consent/accept`: registro de conformidad con estampa UTC e IP de auditoría.
   - `POST /api/v1/consent/revoke`: revocación voluntaria con efecto bloqueante sobre las operaciones del sistema conforme a la regla **RN-02**.

### 5.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se detalla la matriz de verificación técnica ejecutada con Pytest para la persistencia del consentimiento legal:

### Cuadro 5.1: Matriz de Verificación Automatizada de Persistencia del Consentimiento (T-05)

| Identificador de Prueba | Escenario de Evaluación Técnica | Comportamiento Esperado | Resultado Observado en Pytest | Estado |
| :--- | :--- | :--- | :--- | :---: |
| `test_get_consent_status_unconsented` | Consulta de estado para estudiante nuevo | Retornar `has_consented: false` y versión `'2026-II-v1.0'` | HTTP 200, `has_consented: false`, estampa nula | ✅ Exitoso |
| `test_accept_consent_success` | Aceptación formal con estampa e IP | Insertar registro y retornar confirmación con timestamp | HTTP 200, `success: true`, estampa UTC registrada | ✅ Exitoso |
| `test_accept_consent_rejects_external_email` | Envío de solicitud con correo ajeno (`@gmail.com`) | Rechazar petición por validación Pydantic de dominio | HTTP 422 Unprocessable Entity, detalle descriptivo | ✅ Exitoso |
| `test_revoke_consent_blocks_access` | Ejercicio de derecho de revocación | Registrar revocación y anular vigencia de acceso | HTTP 200, `has_consented: false` verificado | ✅ Exitoso |
| `test_consent_service_with_real_db_session` | Ciclo completo sobre motor relacional (SQLite in-memory) | Validar inserción, lectura y actualización en base de datos | Entidad en sesión ORM confirmada, 0 excepciones | ✅ Exitoso |

Fuente: Elaboración propia a partir de las pruebas ejecutadas en `aplicacion/backend/tests/test_consent.py`.

La ejecución de las pruebas confirma que la persistencia en base de datos preserva de forma fidedigna la marca temporal UTC y la dirección IP requeridas para auditorías de cumplimiento ante la Autoridad Nacional de Protección de Datos Personales.

---

## 6. Registro de Ejecución — Tarea T-08 (Administración de Roles y Mérito Académico — RN-03)

### 6.1. Alcance Técnico Implementado
Para gestionar los privilegios institucionales y garantizar la rigurosidad formativa del programa de tutoría entre pares (**T-08** / **RF03** / **CUS10** / **RN-03**), se implementó la arquitectura de roles y mérito:

1. **Tablas Relacionales de Roles (`002_roles_and_profiles.py`):**
   - Tabla `roles`: clave primaria `id_rol`, nombre único `nombre_rol VARCHAR(50)` y descripción. Contiene datos semilla inmutables: `mentoreado` (1), `mentor` (2) y `administrador` (3).
   - Tabla `usuario_roles`: clave primaria `id_usuario_rol`, `email VARCHAR(255)`, clave foránea `id_rol` referenciando a `roles(id_rol)` con eliminación en cascada, `fecha_asignacion TIMESTAMPTZ`, `asignado_por VARCHAR(255)` y `activo BOOLEAN`.
2. **Modelos ORM SQLAlchemy (`aplicacion/backend/app/models/roles.py`):**
   - Entidades `Rol` y `UsuarioRol` con relación bidireccional y restricción de unicidad compuesta `uq_usuario_roles_email_rol`.
3. **Servicio y Regla de Negocio RN-03 (`app/services/role_service.py`):**
   - El servicio `RoleService` implementa la asignación predeterminada del rol `mentoreado` para cualquier estudiante con correo institucional.
   - **Verificación Estricta de Mérito Académico (RN-03):** ante cualquier intento de promoción al rol de Mentor, el servicio inspecciona el ciclo académico del estudiante en `perfiles_academicos`. Si `ciclo_actual < 7`, la solicitud es rechazada de forma perentoria retornando **HTTP 400 Bad Request** con el código canónico de error `MERIT_RULE_VIOLATION`.
4. **Endpoints de Administración de Roles (`app/api/v1/endpoints/roles.py`):**
   - `GET /api/v1/roles/users/{email}`: consulta de roles activos vigentes.
   - `POST /api/v1/roles/promote-mentor`: promoción con verificación de mérito y denegación de autopromoción directa no supervisada.
   - `POST /api/v1/roles/revoke-mentor`: revocación controlada de privilegios de tutoría.

### 6.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se detalla la matriz de pruebas automatizadas que certifican el cumplimiento de la jerarquía de roles y la regla RN-03:

### Cuadro 6.1: Matriz de Pruebas de Roles y Verificación de Mérito Académico (T-08)

| Identificador de Prueba | Escenario de Evaluación Técnica | Comportamiento Esperado | Resultado Observado en Pytest | Estado |
| :--- | :--- | :--- | :--- | :---: |
| `test_get_user_roles_default_is_mentoreado` | Consulta de roles de un estudiante nuevo | Asignar y retornar rol base `'mentoreado'` | HTTP 200, `roles: ["mentoreado"]` | ✅ Exitoso |
| `test_promote_mentor_rejects_when_cycle_below_7_rn03` | Promoción de estudiante con ciclo 5 (< VII) | Rechazar con HTTP 400 y código `MERIT_RULE_VIOLATION` | HTTP 400, código canónico verificado en payload | ✅ Exitoso |
| `test_promote_mentor_success_when_cycle_7_or_above` | Promoción de estudiante con ciclo 8 (>= VII) | Promover exitosamente e incorporar rol `'mentor'` | HTTP 200, `roles: ["mentoreado", "mentor"]` | ✅ Exitoso |
| `test_revoke_mentor_success` | Revocación de facultades de mentoría | Desactivar condición y retirar rol del listado activo | HTTP 200, rol mentor no presente en respuesta | ✅ Exitoso |
| `test_promote_mentor_rejects_external_email` | Solicitud con correo no institucional | Bloquear en capa de esquema con HTTP 422 | HTTP 422, validación de dominio `@upt.pe` | ✅ Exitoso |
| `test_role_service_with_real_db_session` | Operación CRUD sobre sesión relacional directa | Validar integridad referencial y restricciones en BD | Verificación de claves foráneas y mérito en SQLite | ✅ Exitoso |
| `test_promote_and_revoke_with_invalid_token_rejected` | Peticiones con tokens adulterados o revocación ajena | Denegar con HTTP 401 Unauthorized y HTTP 403 Forbidden | HTTP 401 y 403 verificados | ✅ Exitoso |

Fuente: Elaboración propia a partir de las pruebas ejecutadas en `aplicacion/backend/tests/test_roles.py`.

Los resultados confirman que el sistema hace valer la regla institucional RN-03 de forma determinista, impidiendo que alumnos de ciclos iniciales o intermedios ejerzan labores de mentoría formal sin haber superado los prerrequisitos académicos.

---

## 7. Registro de Ejecución — Tarea T-12 (API REST de Perfiles Formativos y Disponibilidad Horaria)

### 7.1. Alcance Técnico Implementado
Para suministrar la información requerida por el motor algorítmico Top-k y posibilitar la personalización de las mentorías (**T-12** / **RF04** / **CUS15** / **RNF04**), se construyó la API REST completa de perfiles y agenda:

1. **Tablas Relacionales de Perfil y Disponibilidad (`002_roles_and_profiles.py`):**
   - Tabla `perfiles_academicos`: `id_perfil`, `email VARCHAR(255)` único e indexado, `codigo_estudiante`, `nombres`, `apellidos`, `ciclo_actual` con restricción de integridad `CHECK (ciclo_actual >= 1 AND ciclo_actual <= 10)`, `rol_postulacion`, campos `JSON` estructurados para `materias_interes` y `temas_seleccionados`, `biografia`, `modalidad_preferida` (`presencial`, `virtual`, `hibrida`) y marca temporal `updated_at`.
   - Tabla `disponibilidades_horarias`: `id_disponibilidad`, `email VARCHAR(255)`, `dia_semana` con restricción de integridad `CHECK (dia_semana >= 1 AND dia_semana <= 6)` (Lunes a Sábado), `hora_inicio VARCHAR(10)`, `hora_fin VARCHAR(10)` y `created_at`.
2. **Modelos ORM SQLAlchemy (`aplicacion/backend/app/models/profile.py`):**
   - Entidades `PerfilAcademico` y `DisponibilidadHoraria` con restricciones `CheckConstraint` explícitas en el nivel de base de datos.
3. **Servicio y Reemplazo Atómico Horario (`app/services/profile_service.py`):**
   - `get_profile()`: lectura de datos con inicialización inteligente de valores predeterminados para estudiantes en fase de onboarding.
   - `update_profile()`: actualización transaccional que incluye la salvaguarda de mérito RN-03 si la postulación declara rol de mentor.
   - `get_availability()`: consulta de bloques horarios semanales ordenados cronológicamente.
   - `update_availability()`: **reemplazo atómico integral** de la matriz de bloques horarios mediante transacción que purga la agenda previa del usuario e inserta el nuevo conjunto sin estados inconsistentes intermedios.
4. **Endpoints REST (`app/api/v1/endpoints/profiles.py`):**
   - `GET /api/v1/profiles/me`: consulta de perfil académico.
   - `PUT /api/v1/profiles/me`: actualización de datos formativos.
   - `GET /api/v1/profiles/availability`: consulta de franjas horarias.
   - `PUT /api/v1/profiles/availability`: reemplazo de matriz horaria semanal.

### 7.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se detalla la matriz de pruebas automatizadas que validan la API de perfiles y disponibilidad:

### Cuadro 7.1: Matriz de Pruebas de la API de Perfiles y Agenda Horaria (T-12)

| Identificador de Prueba | Escenario de Evaluación Técnica | Comportamiento Esperado | Resultado Observado en Pytest | Estado |
| :--- | :--- | :--- | :--- | :---: |
| `test_get_profile_default` | Consulta de perfil sin configuración previa | Retornar perfil institucional inicializado | HTTP 200, código y ciclo formativo presentes | ✅ Exitoso |
| `test_update_profile_success` | Actualización de materias de interés y modalidad | Persistir datos formativos y actualizar timestamp | HTTP 200, modalidad virtual y arrays JSON guardados | ✅ Exitoso |
| `test_update_profile_rejects_mentor_when_cycle_below_7` | Modificación de rol a mentor con ciclo 6 | Rechazar con HTTP 400 y código `MERIT_RULE_VIOLATION` | HTTP 400, violación de mérito detectada | ✅ Exitoso |
| `test_update_profile_allows_mentor_when_cycle_gte_7` | Postulación a mentor con ciclo 7 | Permitir actualización con rol mentor | HTTP 200, rol postulante mentor admitido | ✅ Exitoso |
| `test_get_and_update_availability` | Reemplazo de bloques semanales de disponibilidad | Sobrescribir agenda previa y retornar conteo total | HTTP 200, 3 franjas registradas exitosamente | ✅ Exitoso |
| `test_profile_cycle_boundary_validations` | Evaluación de valores frontera de ciclo (0, 1, 10, 11) | Ciclos 0 y 11 rechazados (422); 1 y 10 admitidos | HTTP 422 en fronteras inválidas; HTTP 200 en válidas | ✅ Exitoso |
| `test_availability_boundary_and_empty_slots` | Validación de días (0, 7), formato HH:MM y agenda vacía | Días y horas inválidas rechazadas; vaciado permitido | HTTP 422 en formato inválido; HTTP 200 en vaciado | ✅ Exitoso |
| `test_profile_service_with_real_db_session` | Operación completa de perfiles y agenda sobre SQLite | Persistencia de registros en tablas relacionales | Registros ORM confirmados en sesión de BD | ✅ Exitoso |
| `test_availability_time_order_and_invalid_24h` | Franjas con hora_inicio >= hora_fin o formato 24h inválido | Rechazar con HTTP 422 por validación temporal y rango | HTTP 422, orden temporal estricto exigido | ✅ Exitoso |
| `test_availability_duplicate_and_overlapping_slots` | Bloques duplicados o solapados en el mismo día semanal | Rechazar con HTTP 422 evitando ambigüedades en agenda | HTTP 422, detección de solapamiento y duplicidad | ✅ Exitoso |
| `test_profile_invalid_enum_fields_rejected` | Modificación con rol de postulación o modalidad ilegales | Rechazar con HTTP 422 por tipado Literal estricto | HTTP 422 ante enumeraciones no reconocidas | ✅ Exitoso |

Fuente: Elaboración propia a partir de las pruebas ejecutadas en `aplicacion/backend/tests/test_profiles.py`.

La API garantiza la integridad estructural de la matriz de disponibilidad horaria y preserva la coherencia del perfil de competencias académicas, alimentando de manera confiable las futuras fases de emparejamiento algorítmico.

---

## 8. Registro de Ejecución — Tarea T-13 (Pruebas de Autorización y Seguridad RLS)

### 8.1. Alcance Técnico Implementado
Para satisfacer los requerimientos no funcionales de seguridad (**RNF02** / **T-13**) y evitar la manipulación no autorizada de perfiles y roles institucionales, se implementó una estrategia dual de protección a nivel de API y persistencia:

1. **Aislamiento Criptográfico en Capa de Endpoints (`app/api/v1/endpoints/profiles.py` y `roles.py`):**
   - Función de resolución de identidad `_resolve_authenticated_email()`: extrae el sujeto del token JWT institucional (`sub` / `email`).
   - **Prevención de Suplantación y Acceso Cruzado:** si un usuario autenticado (`usuarioA@upt.pe`) intenta consultar o modificar el perfil o la disponibilidad de otro estudiante (`usuarioB@upt.pe`), el sistema aborta de inmediato la operación con **HTTP 403 Forbidden** (*Violación de autorización*), a menos que posea credenciales con el rol de `administrador`.
   - **Denegación de Autopromoción a Mentor:** si un estudiante intenta invocar directamente el endpoint de promoción hacia sí mismo sin supervisión administrativa, la petición es rechazada con **HTTP 403 Forbidden**.
2. **Políticas de Seguridad a Nivel de Fila en PostgreSQL/Supabase (`aplicacion/backend/scripts/supabase_rls_sprint02.sql`):**
   - Activación obligatoria de `ROW LEVEL SECURITY` en las 5 tablas del sprint: `consentimientos_legales`, `roles`, `usuario_roles`, `perfiles_academicos` y `disponibilidades_horarias`.
   - Aislamiento estricto de lectura y escritura condicionado al claim del JWT de sesión de Supabase: `email = (auth.jwt() ->> 'email')`.
   - Políticas exclusivas para `service_role` y usuarios con rol institucional de `administrador` para labores de auditoría y asignación de privilegios.

### 8.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se detalla la matriz de pruebas automatizadas que acreditan la seguridad y el aislamiento entre usuarios:

### Cuadro 8.1: Matriz de Pruebas de Autorización y Seguridad Multi-Usuario (T-13)

| Identificador de Prueba | Escenario de Evaluación de Seguridad | Comportamiento Esperado | Resultado Observado en Pytest | Estado |
| :--- | :--- | :--- | :--- | :---: |
| `test_authorization_header_valid_jwt_access` | Petición con Bearer JWT institucional válido | Autorizar acceso y retornar datos del titular | HTTP 200, identidad validada por token | ✅ Exitoso |
| `test_authorization_expired_or_invalid_jwt_rejected` | Petición con token adulterado o firma inválida | Denegar acceso inmediatamente | HTTP 401 Unauthorized, token rechazado | ✅ Exitoso |
| `test_authorization_expired_token_rejected` | Petición con token expirado temporalmente | Denegar acceso por expiración de vigencia | HTTP 401 Unauthorized verificado | ✅ Exitoso |
| `test_user_cannot_access_or_modify_another_users_profile_forbidden` | Estudiante A intenta leer/modificar perfil de Estudiante B | Abortar con HTTP 403 y alerta de violación de acceso | HTTP 403 Forbidden en GET perfil, PUT perfil y agenda | ✅ Exitoso |
| `test_denial_of_self_promotion_to_mentor_without_admin` | Estudiante intenta autopromoverse a mentor | Rechazar autopromoción por falta de rol administrador | HTTP 403 Forbidden, mensaje explicativo | ✅ Exitoso |
| `test_admin_can_promote_and_access` | Usuario con rol administrador promueve a estudiante | Autorizar operación administrativa y actualizar rol | HTTP 200, rol mentor asignado por administrador | ✅ Exitoso |
| `test_unauthenticated_request_rejected_without_email_or_token` | Petición anónima sin cabecera ni identidad | Rechazar solicitud por ausencia de credenciales | HTTP 401 Unauthorized | ✅ Exitoso |
| `test_admin_can_update_other_profile_and_revoke_with_token` | Administrador modifica perfil de tercero y revoca rol | Procesar operación administrativa con token válido | HTTP 200 en actualización y revocación | ✅ Exitoso |
| `test_token_without_subject_rejected` | Token JWT carente del claim de identidad (`sub`) | Rechazar por inconsistencia de identidad | HTTP 401 Unauthorized | ✅ Exitoso |
| `test_malformed_authorization_header_rejected` | Cabecera Authorization sin prefijo canónico Bearer | Rechazar con HTTP 401 por formato inválido de cabecera | HTTP 401 Unauthorized verificado | ✅ Exitoso |
| `test_production_unauthenticated_request_rejected` | Petición sin token en producción con parámetro de correo | Bloquear acceso denegando el fallback fuera de dev | HTTP 401 Unauthorized en profiles y roles | ✅ Exitoso |

Fuente: Elaboración propia a partir de las pruebas ejecutadas en `aplicacion/backend/tests/test_authorization.py`.

Las pruebas de seguridad demuestran la inviolabilidad del perímetro de datos privados entre estudiantes, impidiendo cualquier escalamiento de privilegios vertical (autopromoción) u horizontal (acceso a perfiles ajenos).

---

## 9. Integración y Navegación SPA del Sprint 2

- **Componente Principal (`aplicacion/frontend/src/App.tsx`):**
  - Se consolidó la barra de navegación institucional superior con cinco pestañas temáticas activas para el Sprint 2:
    1. `🔐 Acceso & OTP (T-02)`: flujo de acceso institucional de 2 pasos.
    2. `⚖️ Consentimiento Ley 29733 (T-04)`: vista del formulario de consentimiento digital.
    3. `📚 Catálogo Curricular (T-10)`: buscador avanzado de asignaturas filtro y temarios.
    4. `👤 Perfil & Disponibilidad (T-11)`: configuración del perfil académico y agenda semanal.
    5. `🛰️ Monitor de Servicios (T-01)`: estado operativo de FastAPI y Supabase.
- **Prueba de Integración de Navegación (`aplicacion/frontend/src/__tests__/App.test.tsx`):**
  - Valida la alternancia reactiva entre las cinco vistas sin errores de ciclo de vida ni desbordamientos en el DOM virtual.

---

## 10. Métricas Consolidadas de Calidad y Cobertura (Vitest + Pytest)

Al término de la ejecución conjunta de las tareas de frontend (Joan) y backend (Renzo), se ejecutó la totalidad de suites automatizadas de pruebas unitarias, de integración, linteo estático y compilación técnica:

A continuación, se detalla el balance global de calidad y cobertura de código obtenido en el Sprint 2:

### Cuadro 10.1: Resultados Globales de Calidad, Linteo y Cobertura (Sprint 2 Consolidado)

| Dimensión Técnica | Herramienta | Umbral Requerido (RNF09) | Frontend (Joan: T-04, T-10, T-11) | Backend (Renzo: T-05, T-08, T-12, T-13) | Consolidado Total Sprint 2 | Estado |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Suites de Prueba** | Vitest 2.1.8 / Pytest 9.1.1 | 100% aprobadas | 11 suites | 10 suites | **21 suites aprobadas** | ✅ Exitoso |
| **Pruebas Automatizadas** | Vitest / Pytest | 100% aprobadas | 66 pruebas (0 fallos) | 84 pruebas (0 fallos) | **150 pruebas aprobadas (100%)** | ✅ Exitoso |
| **Cobertura en Líneas/Sentencias** | Vitest v8 / Pytest-Cov | $\ge 70.0\%$ | 91.10% | 90.64% | **~90.9% ponderado** | ✅ Exitoso |
| **Cobertura en Ramas (Branch)** | Vitest v8 / Pytest-Cov | — | 75.18% | 85.00% | **~80.1% promedio** | ✅ Exitoso |
| **Análisis Estático (Lint)** | ESLint 9 / Ruff 0.9 | 0 errores / warnings | 0 errores, 0 warnings | 0 errores (All checks passed!) | **0 defectos estáticos** | ✅ Exitoso |
| **Formato de Código** | Prettier / Ruff format | 100% formateado | Código conforme | 49 archivos conformes | **100% estandarizado** | ✅ Exitoso |
| **Compilación / DDL** | Vite Build / Alembic | 0 errores de tipado | 43 módulos en 612 ms | Migración 002 y RLS aplicados en Supabase | **Empaquetado limpio** | ✅ Exitoso |

Fuente: Elaboración propia a partir de las ejecuciones de `npm run test:coverage`, `npm run lint`, `npm run build` en `aplicacion/frontend` y `pytest tests/ --cov=app`, `ruff check .`, `ruff format --check .`, `alembic upgrade head` en `aplicacion/backend`.

Los datos demuestran de forma irrefutable que el incremento de software del Sprint 2 no solo satisface el umbral mínimo del 70% estipulado en el requerimiento no funcional **RNF09**, sino que lo supera holgadamente situándose por encima del 90% en ambos subsistemas, manteniendo cero advertencias de linteo y cero pruebas fallidas.

---

## 11. Registro de Versiones, Migraciones Alembic y Comandos Reproducibles

### 11.1. Artefactos de Base de Datos Generados
1. **Migración Alembic:** `aplicacion/backend/app/db/migrations/versions/002_roles_and_profiles.py` (Revisión `20261023_002`, descendiente de `20261019_001`). Aplicada exitosamente en la base de datos de producción Supabase mediante `alembic upgrade head`.
2. **Script RLS de Supabase:** `aplicacion/backend/scripts/supabase_rls_sprint02.sql` (Políticas de aislamiento por token JWT y denegación de autopromoción). Ejecutado y verificado en Supabase con `relrowsecurity = True` en las 5 tablas.

### 11.2. Comandos para Validación Local Reproducible

```powershell
# ---------------------------------------------------------
# A. Validación del Frontend (Capa Cliente)
# ---------------------------------------------------------
cd aplicacion/frontend
npm run lint             # Análisis estático ESLint (0 errores)
npm run test:coverage    # Ejecución de 66 pruebas Vitest (cobertura 91.10%)
npm run build            # Compilación de producción Vite (0 errores de tipado)

# ---------------------------------------------------------
# B. Validación del Backend (Capa de Servicios y Persistencia)
# ---------------------------------------------------------
cd ../backend
ruff check .             # Análisis estático Ruff (All checks passed!)
ruff format --check .    # Verificación de formato (49 archivos conformes)
pytest tests/ --cov=app --cov-report=term-missing  # 84 pruebas Pytest (cobertura 90.64%)
alembic upgrade head     # Aplicación de migración 002 sobre PostgreSQL / Supabase
```

---

## 12. Acta de Cierre Conjunto y Cumplimiento del Definition of Done (DoD)

En cumplimiento de los acuerdos metodológicos del equipo consultor **C-SharkTeam** y los estándares del curso Construcción de Software I, se suscribe la presente **Acta de Cierre Técnico del Sprint 2**, declarando el cumplimiento irrestricto de los seis criterios que componen la Definición de Terminado (*Definition of Done - DoD*):

### Cuadro 12.1: Matriz de Verificación de Criterios del Definition of Done (DoD)

| Criterio DoD | Requisito Formal Exigido | Evidencia Empírica Verificada | Dictamen de Cierre |
| :---: | :--- | :--- | :---: |
| **1. Cobertura de Requerimientos** | Funcionalidades RF02, RF03, RF04, RF05 implementadas con reglas RN-02 y RN-03. | Vistas de consentimiento, catálogo, perfil y matriz 6×11 operativas con endpoints REST y control de mérito académico. | **CUMPLIDO** ✅ |
| **2. Cobertura de Pruebas Automatizadas** | Cobertura en líneas superior al 70.0% conforme a RNF09 en frontend y backend. | **91.10% en Frontend** (66 pruebas) y **90.64% en Backend** (84 pruebas), totalizando 150 pruebas sin fallos. | **CUMPLIDO** ✅ |
| **3. Calidad Estática y Linteo** | Cero errores de sintaxis, linteo o advertencias en ambos entornos de desarrollo. | `eslint .` (0 errores) y `ruff check .` / `ruff format --check .` (0 errores en 49 archivos). | **CUMPLIDO** ✅ |
| **4. Integridad de Empaquetado y Persistencia** | Compilación de producción limpia y migraciones relacionales verificadas. | `tsc -b && vite build` ejecutado en 612 ms; migración Alembic 002 y script RLS aplicados y verificados en Supabase. | **CUMPLIDO** ✅ |
| **5. Seguridad y Aislamiento de Acceso** | Protección de perfiles privados y denegación de autopromoción indebida (RNF02). | Endpoints protegidos por token JWT (rechazo 401/403 ante accesos ilícitos) y RLS activo (`relrowsecurity = True`). | **CUMPLIDO** ✅ |
| **6. Rigor en la Documentación Técnica** | Bitácora actualizada cumpliendo la regla canónica quíntuple para todas las tablas. | Bitácora `docs/sprints/sprint-02.md` con 6 cuadros técnicos completos (Presentación, Título, Tabla, Fuente, Conclusión). | **CUMPLIDO** ✅ |

Fuente: Elaboración propia conforme a los acuerdos del Sprint Planning del Sprint 2.

La acreditación unánime de los seis criterios del Definition of Done certifica que el incremento entregado en el Sprint 2 reúne los atributos de calidad de software, trazabilidad analítica y seguridad por diseño requeridos para iniciar formalmente las actividades del Sprint 3 (Módulo de Recomendación y Algoritmo Top-k).

### Firmas de Conformidad del Equipo Consultor:

```
__________________________________             __________________________________
     Joan Cristian Medina Quispe                     Renzo Antonio Antayhua Mamani
        Líder de Frontend (T-04, T-10, T-11)           Líder de Backend (T-05, T-08, T-12, T-13)
```

**Fecha de Cierre Oficial:** 23 de Octubre de 2026.  
**Estado Final del Sprint 2:** **CERRADO Y APROBADO AL 100% PARA TRANSICIÓN AL SPRINT 3.**
