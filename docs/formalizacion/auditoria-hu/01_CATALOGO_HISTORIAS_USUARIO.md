# 01 — Catálogo Maestro de Historias de Usuario, PBIs y Casos de Uso

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT  
**Etapa:** Auditoría Integral de Cumplimiento Funcional (Fase 04-B)  
**Fecha de Auditoría:** 7 de noviembre de 2026  
**Rama:** `feat/formalizacion-ux-roles`  
**Commit Auditado:** `4cbf504`  
**Estado:** Documento Oficial de Auditoría SQA  

---

## 1. Introducción y Contexto Metodológico

El proyecto del **Sistema Web P2P de Mentorías Académicas de la Escuela Profesional de Ingeniería de Sistemas (EPIS-UPT)** se originó en el marco de la asignatura *Construcción de Software I* (Semestre 2026-II). A nivel de ingeniería de requerimientos y diseño de arquitectura, el proyecto adoptó el estándar **IEEE 830 / ISO/IEC 25010** y la metodología **UWE (UML-based Web Engineering)** orientada a Casos de Uso (**CUS01 al CUS24**), Requerimientos Funcionales (**RF01 al RF26**), No Funcionales (**RNF01 al RNF10**) y Reglas de Negocio Institucionales (**RN-01 al RN-14**), formalizados en el **SRS (FD03 v2.1)** y **SAD (FD04 v2.0)**.

A nivel de gestión ágil de desarrollo, el equipo estructuró el trabajo en un plan de 8 sprints operativos (`docs/sprints/PLAN_SPRINTS_Y_TAREAS.md`) basado en **37 Product Backlog Items (PB-001 al PB-037)** y **51 Tareas Técnicas (T-01 al T-51)**. Durante el desarrollo del Sprint 02, el equipo elaboró un catálogo explícito de **Historias de Usuario (HU-01 a HU-08)** con especificaciones en lenguaje Gherkin para enlazar los sprints con las narrativas RUP/UML del SRS. En los sprints subsiguientes (03 al 06), el equipo implementó funcionalidades directamente trazadas contra los **PBIs**, **RFs**, **CUSs** y casos de prueba del **Catálogo Oficial de Pruebas Excel** (`Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`).

Este documento consolida el **catálogo exhaustivo y canónico** de todas las Historias de Usuario, PBIs y Casos de Uso identificados en el repositorio, definiendo actores, descripciones, requisitos, reglas de negocio y criterios de aceptación verificables.

---

## 2. Catálogo Canónico de Historias de Usuario Explícitas (HU-01 a HU-08)

Las siguientes 8 Historias de Usuario representan las especificaciones explícitas redactadas bajo formato ágil estándar (*Como... Quiero... Para...*) y criterios en formato Gherkin (*Dado que... Cuando... Entonces...*), identificadas en `docs/analisis/trazabilidad_sprint_02.md`, `docs/diseño/TRAZABILIDAD_SPRINT_02.md`, `docs/sprints/sprint-02/02-trazabilidad/MATRIZ_TRAZABILIDAD_SPRINT_02.md` y `docs/sprints/sprint-03/04-presentacion/GUION_MANUAL_DIAPOSITIVAS_SPRINT_03.md`.

---

### HU-01: Acceso Inicial Institucional con Autenticación 2FA
- **Identificador Canónico:** `HU-01`
- **Nombre:** Acceso institucional seguro con doble factor de autenticación (OTP)
- **Sprint:** Sprint 01
- **PBI Asociado:** `PB-002` (Autenticación OTP)
- **Requerimientos Asociados:** `RF01` (Autenticación multifactor), `RNF01` (Seguridad), `RNF02` (Privacidad)
- **Reglas de Negocio:** `RN-01` (Acceso exclusivo con correo `@upt.pe` y 2FA obligatorio)
- **Caso de Uso del SRS:** `CUS01` / `UC-001` (Iniciar sesión institucional con 2FA)
- **Actor:** Estudiante Universitario / Docente / Administrador (Visitante no autenticado)
- **Descripción Original:**
  > *Como* estudiante o docente de la EPIS-UPT,  
  > *Quiero* ingresar a la plataforma validando mi identidad mediante mi correo institucional y un código temporal de 6 dígitos,  
  > *Para* garantizar que solo miembros autorizados de la comunidad universitaria accedan a los servicios de mentoría sin comprometer credenciales institucionales.
- **Criterios de Aceptación (Gherkin):**
  - **CA-01.1 (Validación de dominio):** Dado que un visitante ingresa un correo con dominio distinto a `@upt.pe`, cuando solicita el código OTP, el sistema rechaza la petición con HTTP 400 y mensaje `DOMINIO_NO_INSTITUCIONAL`.
  - **CA-01.2 (Generación y expiración de OTP):** Dado un correo `@upt.pe` válido, cuando solicita OTP, el sistema genera un código de 6 dígitos con vigencia de 5 minutos y un temporizador de reintento (*cooldown*) de 60 segundos.
  - **CA-01.3 (Verificación y emisión de JWT):** Dado un código OTP válido y vigente, cuando el usuario lo ingresa, el sistema emite un token JWT firmado criptográficamente con algoritmo HS256 y ciclo de vida de 60 minutos.
- **Fuente Documental:** `docs/sprints/sprint-03/04-presentacion/GUION_MANUAL_DIAPOSITIVAS_SPRINT_03.md` (Diapositiva 2), `docs/sprints/sprint-01.md`.

---

### HU-02: Despliegue de Entorno Base y Verificación de Salud
- **Identificador Canónico:** `HU-02`
- **Nombre:** Infraestructura desacoplada, persistencia inicial y monitoreo de salud
- **Sprint:** Sprint 01
- **PBI Asociado:** `PB-001` (Entorno ejecutable), `PB-004` (CI y validación inicial)
- **Requerimientos Asociados:** `RNF09` (Mantenibilidad y arquitectura desacoplada), `RNF06` (Disponibilidad)
- **Reglas de Negocio:** Ninguna regla institucional de negocio directa; atributo arquitectural.
- **Caso de Uso del SRS:** Soporte transversal de arquitectura (SAD §2.1 a §2.5).
- **Actor:** Ingeniero de Software / Administrador de Sistemas
- **Descripción Original:**
  > *Como* equipo de desarrollo y soporte de la EPIS-UPT,  
  > *Quiero* disponer de una arquitectura cliente-servidor desacoplada (React 19 + FastAPI + PostgreSQL/Supabase) con endpoints de diagnóstico de salud,  
  > *Para* verificar en tiempo real la conectividad y disponibilidad de los subsistemas y asegurar la integración continua con pruebas automatizadas.
- **Criterios de Aceptación:**
  - **CA-02.1 (Endpoint de salud de API):** `GET /api/v1/health` responde HTTP 200 con `{"status": "ok"}` sin requerir conexión a base de datos.
  - **CA-02.2 (Diagnóstico de base de datos):** `GET /api/v1/health/db` prueba la conexión a PostgreSQL y retorna latencia y estado de conectividad.
  - **CA-02.3 (Pipeline CI/CD):** Todo commit sobre ramas feature o main ejecuta pruebas automatizadas en GitHub Actions superando umbral mínimo de cobertura.
- **Fuente Documental:** `docs/sprints/sprint-01.md`, `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (Cuadro 4.1).

---

### HU-03: Formalización del Consentimiento Digital (Ley N° 29733)
- **Identificador Canónico:** `HU-03`
- **Nombre:** Formalización del consentimiento informado para protección de datos personales
- **Sprint:** Sprint 02
- **PBI Asociado:** `PB-003` (Consentimiento digital)
- **Requerimientos Asociados:** `RF02` (Consentimiento informado digital), `RNF02` (Privacidad y protección de datos)
- **Reglas de Negocio:** `RN-02` (Consentimiento legal vinculante; bloqueo total ante rechazo o revocación)
- **Caso de Uso del SRS:** `CUS01` / `UC-001` (Flujo de Consentimiento Digital)
- **Actor:** Estudiante Mentoreado / Mentor Académico (Usuario autenticado por primera vez)
- **Descripción Original:**
  > *Como* estudiante de la Universidad Privada de Tacna,  
  > *Quiero* revisar las cláusulas institucionales de tratamiento de datos personales y otorgar mi consentimiento formal e informado en mi primer inicio de sesión,  
  > *Para* que mi historial de asignaturas, notas y disponibilidad horaria sean tratados legalmente por la plataforma, teniendo la facultad de revocar dicho consentimiento en cualquier momento.
- **Criterios de Aceptación (Gherkin):**
  - **CA-03.1 (Aceptación exitosa):** Dado que el estudiante valida su acceso OTP y no registra consentimiento vigente, cuando el sistema despliega el modal `ConsentModalView` con las cláusulas de la Ley N° 29733 y marca "Acepto", el sistema envía `POST /api/v1/consent/accept`, persiste la tupla con timestamp UTC e IP, y desbloquea el catálogo.
  - **CA-03.2 (Rechazo y bloqueo RN-02):** Dado que el estudiante presiona "Rechazar y Salir", el sistema envía `POST /api/v1/consent/revoke`, registra `accepted=False`, despliega un banner de advertencia bloqueante y deniega el acceso a reservas, perfiles y catálogo.
  - **CA-03.3 (Bloqueo transaccional en reservas):** Dado un usuario sin consentimiento aceptado, si intenta reservar una mentoría (`POST /api/v1/bookings/reserve`), el backend responde HTTP 403 con mensaje canónico de consentimiento requerido.
- **Fuente Documental:** `docs/analisis/trazabilidad_sprint_02.md` (§3.1), `docs/diseño/TRAZABILIDAD_SPRINT_02.md` (§3.1).

---

### HU-04: Asignación de Roles y Verificación de Mérito (RN-03)
- **Identificador Canónico:** `HU-04`
- **Nombre:** Gestión administrativa de jerarquía de roles y mérito académico
- **Sprint:** Sprint 02
- **PBI Asociado:** `PB-005` (Gestión de roles)
- **Requerimientos Asociados:** `RF03` (Asignación de roles de usuario), `RNF02` (Seguridad y control de acceso)
- **Reglas de Negocio:** `RN-03` (Mérito académico: mentoría exclusiva para estudiantes de ciclo >= VII)
- **Caso de Uso del SRS:** `CUS10` / `UC-010` (Gestionar asignación de roles de usuario)
- **Actor:** Administrador Institucional (Comité de Tutoría / Dirección EPIS)
- **Descripción Original:**
  > *Como* Administrador del Comité de Tutoría de la EPIS-UPT,  
  > *Quiero* gestionar la jerarquía de roles institucionales y verificar que los postulantes a mentor cursen el séptimo ciclo o superior,  
  > *Para* garantizar que únicamente estudiantes con suficiencia académica y madurez formativa brinden tutoría a los ciclos formativos iniciales.
- **Criterios de Aceptación (Gherkin):**
  - **CA-04.1 (Promoción exitosa con mérito):** Dado que el estudiante registra `ciclo_actual >= 7`, cuando el Administrador invoca `POST /api/v1/roles/promote-mentor`, el sistema asigna el rol `mentor`, lo persiste en `usuario_roles` y retorna HTTP 200 con `["mentoreado", "mentor"]`.
  - **CA-04.2 (Rechazo determinista por mérito insuficiente):** Dado que el estudiante registra `ciclo_actual < 7`, cuando se solicita su promoción, el servicio `RoleService` aborta con HTTP 400 y mensaje `MERIT_RULE_VIOLATION`.
  - **CA-04.3 (Denegación de autopromoción):** Dado un usuario autenticado sin rol de administrador, si intenta invocar la promoción de mentor, el backend responde HTTP 403 `SELF_PROMOTION_FORBIDDEN`.
- **Fuente Documental:** `docs/analisis/trazabilidad_sprint_02.md` (§3.1), `docs/diseño/TRAZABILIDAD_SPRINT_02.md` (§3.1).

---

### HU-05: Consulta Avanzada del Catálogo Curricular
- **Identificador Canónico:** `HU-05`
- **Nombre:** Exploración interactiva del catálogo curricular oficial y temarios silábicos
- **Sprint:** Sprint 02 (iniciado en S1 como T-09, culminado en S2 como T-10)
- **PBI Asociado:** `PB-006` (Catálogo curricular)
- **Requerimientos Asociados:** `RF05` (Catálogo de asignaturas y temarios), `RNF04` (Usabilidad)
- **Reglas de Negocio:** Alineamiento curricular institucional (cursos filtro de I a IV ciclo)
- **Caso de Uso del SRS:** `CUS21` / `UC-021` (Explorar catálogo curricular de asignaturas filtro)
- **Actor:** Estudiante Mentoreado / Mentor Académico
- **Descripción Original:**
  > *Como* estudiante mentoreado o mentor de la EPIS-UPT,  
  > *Quiero* explorar de manera interactiva el catálogo de asignaturas formativas y sus unidades silábicas oficiales mediante un buscador en tiempo real,  
  > *Para* identificar con precisión los temas conceptuales críticos en los que requiero apoyo pedagógico o poseo competencias para dictar asesorías.
- **Criterios de Aceptación (Gherkin):**
  - **CA-05.1 (Filtrado en tiempo real):** Dado que el usuario accede a la vista `CurriculumCatalogView`, cuando ingresa un texto en el buscador, la interfaz filtra reactivamente el árbol curricular resaltando la asignatura y tema coincidente.
  - **CA-05.2 (Jerarquía silábica oficial):** El catálogo presenta cursos oficiales de I a IV ciclo desglosados en unidades de aprendizaje y temas conceptuales validados por la Escuela.
- **Fuente Documental:** `docs/analisis/trazabilidad_sprint_02.md` (§3.1), `docs/diseño/TRAZABILIDAD_SPRINT_02.md` (§3.1).

---

### HU-06: Configuración de Perfil y Matriz Semanal de Disponibilidad (6x11)
- **Identificador Canónico:** `HU-06`
- **Nombre:** Configuración de perfil académico formativo y agenda semanal interactiva
- **Sprint:** Sprint 02
- **PBI Asociado:** `PB-007` (Perfiles formativos y disponibilidad)
- **Requerimientos Asociados:** `RF04` (Perfil formativo y matriz horaria), `RNF08` (Eficiencia)
- **Reglas de Negocio:** `RN-03` (Alerta preventiva de mérito en UI), formato horario estándar (Lunes a Sábado, 08:00 a 20:00)
- **Caso de Uso del SRS:** `CUS15` / `UC-015` (Gestionar perfil formativo y disponibilidad horaria)
- **Actor:** Estudiante Mentoreado / Mentor Académico
- **Descripción Original:**
  > *Como* estudiante de la EPIS-UPT,  
  > *Quiero* configurar mi perfil formativo (materias de interés, modalidad preferida) y marcar mis horas libres en una grilla semanal interactiva de 6 días por 11 horas,  
  > *Para* que la plataforma y el motor de recomendación conozcan con exactitud mi disponibilidad para agendar o recibir mentorías.
- **Criterios de Aceptación (Gherkin):**
  - **CA-06.1 (Reemplazo atómico transaccional):** Dado que el estudiante selecciona bloques horarios y presiona "Guardar", el backend ejecuta una transacción ACID que reemplaza atómicamente los registros previos en `disponibilidades_horarias` y retorna HTTP 200 con el total de slots guardados.
  - **CA-06.2 (Alerta preventiva RN-03):** Si un estudiante con ciclo < VII intenta seleccionar el rol de Mentor en el formulario, la UI despliega de inmediato un banner de advertencia sobre la regla RN-03.
  - **CA-06.3 (Aislamiento de perfil):** Un usuario no puede alterar el perfil ni disponibilidad de otro estudiante (`HTTP 403 Forbidden`).
- **Fuente Documental:** `docs/analisis/trazabilidad_sprint_02.md` (§3.1), `docs/diseño/TRAZABILIDAD_SPRINT_02.md` (§3.1).

---

### HU-07: Aislamiento Multiusuario y Control de Acceso RLS
- **Identificador Canónico:** `HU-07`
- **Nombre:** Aislamiento estricto de expedientes y prevención de cruce de datos (*Cross-Access*)
- **Sprint:** Sprint 02 (soportado por T-07 en S1 y T-13 en S2)
- **PBI Asociado:** `PB-008` (Protección RLS y aislamiento)
- **Requerimientos Asociados:** `RNF01` (Seguridad), `RNF02` (Privacidad y protección de datos)
- **Reglas de Negocio:** Ley N° 29733 (Protección de Datos Personales), principio de mínimo privilegio
- **Caso de Uso del SRS:** Transversal a `CUS01`, `CUS10`, `CUS15`
- **Actor:** Todos los perfiles de usuario
- **Descripción Original:**
  > *Como* usuario del sistema web de mentorías,  
  > *Quiero* que mis registros académicos, horarios y reservas se encuentren estrictamente aislados mediante políticas de base de datos y autorización a nivel de servicio,  
  > *Para* tener la certeza de que ningún otro usuario pueda consultar, modificar ni suplantar mi expediente personal.
- **Criterios de Aceptación:**
  - **CA-07.1 (Rechazo de consulta cruzada):** Una petición `GET /api/v1/profiles/{email}` de un estudiante sobre el email de otro responde HTTP 403.
  - **CA-07.2 (Políticas RLS en PostgreSQL):** Las políticas de Row Level Security condicionan las operaciones a `auth.jwt() ->> 'email' = usuario_email`.
- **Fuente Documental:** `docs/analisis/trazabilidad_sprint_02.md` (§2), `docs/diseño/TRAZABILIDAD_SPRINT_02.md` (§2).

---

### HU-08: Interfaces OpenAPI Desacopladas y Cobertura de Pruebas
- **Identificador Canónico:** `HU-08`
- **Nombre:** Contratos fuertemente tipados, documentación interactiva y cobertura mínima de pruebas
- **Sprint:** Sprint 02 (soportado por T-06 en S1 y consolidado en S2)
- **PBI Asociado:** `PB-004` (CI y validación), `PB-031` (Cobertura de pruebas)
- **Requerimientos Asociados:** `RNF09` (Mantenibilidad, tipado estricto y cobertura >= 70%)
- **Reglas de Negocio:** Estándar IEEE 830 / ISO/IEC 25010
- **Caso de Uso del SRS:** Gobernanza técnica transversal
- **Actor:** Equipo de Ingeniería y Auditoría SQA
- **Descripción Original:**
  > *Como* auditor de calidad de software y arquitecto de sistemas,  
  > *Quiero* que todas las interfaces REST estén gobernadas por esquemas Pydantic / TypeScript tipados y respaldadas por una suite automatizada con cobertura superior al 70%,  
  > *Para* garantizar la mantenibilidad, extensibilidad y estabilidad del software en los futuros sprints.
- **Criterios de Aceptación:**
  - **CA-08.1 (Contratos tipados):** Schemas Pydantic v2 en backend y tipos TypeScript en frontend sin `any` arbitrarios.
  - **CA-08.2 (Umbral de cobertura):** Cobertura de pruebas automatizadas superior al 70.0% en backend (Pytest) y frontend (Vitest).
- **Fuente Documental:** `docs/analisis/trazabilidad_sprint_02.md` (§2), `docs/diseño/TRAZABILIDAD_SPRINT_02.md` (§2).

---

## 3. Catálogo de Historias Funcionales Derivadas de PBIs (Sprints 03 al 06)

Dado que en los Sprints 03 al 06 el equipo utilizó directamente los Product Backlog Items (**PB-009 al PB-019**) y los Casos de Uso del SRS (**CUS06, CUS02, CUS04, CUS24, CUS17, CUS23, CUS07, CUS08**), a continuación se formalizan sus especificaciones canónicas con sus criterios de aceptación y trazabilidad:

---

### HU-09 (PB-009): Publicación de Ofertas de Mentoría
- **Identificador Derivado:** `HU-09` / `PB-009`
- **Nombre:** Publicación y parametrización de ofertas de mentoría académica
- **Sprint:** Sprint 03
- **PBI Asociado:** `PB-009` [T-14, T-15, T-16]
- **Requerimientos:** `RF08` (Publicación y parametrización de ofertas), `RNF04`, `RNF09`
- **Reglas de Negocio:** `RN-04` (Antelación obligatoria > 24 horas), `RN-05` (Aforo máximo automático: 10 presencial, 20 virtual)
- **Caso de Uso del SRS:** `CUS06` / `UC-006` (Publicar oferta de mentoría académica)
- **Actor:** Mentor Académico habilitado (Ciclo >= VII con rol verificado)
- **Descripción Estándar:**
  > *Como* mentor académico institucional,  
  > *Quiero* publicar una oferta de mentoría vinculada a una asignatura, tema silábico oficial, fecha, modalidad y espacio,  
  > *Para* poner mis competencias a disposición de los estudiantes mentoreados respetando los aforos y antelaciones normativas.
- **Criterios de Aceptación:**
  - **CA-09.1 (Antelación RN-04):** Si la fecha programada tiene menos de 24 horas de antelación respecto a la hora actual (`delta <= 24h`), el sistema rechaza la publicación con HTTP 400 y mensaje `RN-04`.
  - **CA-09.2 (Aforo automático RN-05):** Si la modalidad es "Presencial", el aforo máximo se fija en 10; si es "Virtual", se fija en 20 estudiantes de manera inmutable.
  - **CA-09.3 (Restricción de rol):** Usuarios sin rol de mentor no pueden publicar ofertas (`HTTP 403 Forbidden`).
- **Fuente Documental:** `docs/sprints/sprint-03.md`, `docs/diseño/TRAZABILIDAD_PUBLICACION_OFERTAS.md`, SRS §5.3 (RF08), §6.2.3 (CUS06).

---

### HU-10 (PB-010 / PB-011): Recomendación Inteligente Top-k y Feed Interactivo
- **Identificador Derivado:** `HU-10` / `PB-010`, `PB-011`
- **Nombre:** Inferencia de recomendaciones personalizadas y feed interactivo Top-k
- **Sprint:** Sprint 04
- **PBI Asociado:** `PB-010` (Top-k inicial), `PB-011` (Feed de recomendaciones) [T-17 al T-20]
- **Requerimientos:** `RF06` (Inferencia de recomendaciones y ranking Top-k), `RNF03` (Latencia algorítmica <= 500 ms)
- **Reglas de Negocio:** `RN-04`, `RN-11` (Afinidad por temas y ponderación de asignaturas filtro)
- **Caso de Uso del SRS:** `CUS02` / `UC-002` (Explorar recomendaciones personalizadas Top-k)
- **Actor:** Estudiante Mentoreado
- **Descripción Estándar:**
  > *Como* estudiante mentoreado con dificultades académicas,  
  > *Quiero* visualizar un ranking personalizado (Top 3 a Top 5) de sesiones de mentoría afines a mis necesidades y disponibilidad horaria,  
  > *Para* encontrar rápidamente la sesión más conveniente sin tener que revisar manualmente todo el catálogo.
- **Criterios de Aceptación:**
  - **CA-10.1 (Cálculo de similitud coseno):** El motor calcula la similitud entre el vector de necesidades del estudiante y los vectores de las ofertas activas.
  - **CA-10.2 (Desempate determinista):** Ante puntajes idénticos, el ranking desempata priorizando la oferta con mayor aforo disponible y menor fecha.
  - **CA-10.3 (Invarianza ante permutación):** El orden de despliegue en la interfaz es determinista e invariante ante el orden en que se reciben las ofertas.
- **Fuente Documental:** `docs/sprints/sprint-04.md`, `docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_04.md`, SRS §5.3 (RF06), §6.2.3 (CUS02).

---

### HU-11 (PB-013): Reserva Transaccional de Vacantes con Control de Aforo
- **Identificador Derivado:** `HU-11` / `PB-013`
- **Nombre:** Reserva de plaza de mentoría con prevención estricta de sobreaforo
- **Sprint:** Sprint 04
- **PBI Asociado:** `PB-013` [T-21 al T-24]
- **Requerimientos:** `RF12` (Reserva de cupos con control de aforo), `RNF07` (Consistencia transaccional ACID)
- **Reglas de Negocio:** `RN-05` (Control estricto de cupos), `RN-02` (Exigencia de consentimiento previo)
- **Caso de Uso del SRS:** `CUS04` / `UC-004` (Reservar cupo de mentoría académica)
- **Actor:** Estudiante Mentoreado autenticado
- **Descripción Estándar:**
  > *Como* estudiante mentoreado,  
  > *Quiero* reservar una plaza disponible en una sesión seleccionada desde el feed,  
  > *Para* asegurar mi cupo de participación bajo estado preliminar pendiente de confirmación.
- **Criterios de Aceptación:**
  - **CA-11.1 (Estado inicial):** La reserva se genera en estado `PENDIENTE_CONFIRMACION`.
  - **CA-11.2 (Prevención de sobreaforo):** Dos solicitudes concurrentes sobre la última vacante no pueden sobreasignar el aforo; la segunda recibe HTTP 409 `CAPACITY_EXCEEDED`.
  - **CA-11.3 (Prevención de duplicidad):** Un estudiante no puede reservar dos veces la misma sesión (`HTTP 400 DUPLICATE_BOOKING`).
- **Fuente Documental:** `docs/sprints/sprint-04.md`, SRS §5.3 (RF12), §6.2.3 (CUS04).

---

### HU-12 (PB-014): Ratificación de Asistencia en Ventana T-24h
- **Identificador Derivado:** `HU-12` / `PB-014`
- **Nombre:** Ratificación formal de asistencia previa al corte temporal
- **Sprint:** Sprint 05
- **PBI Asociado:** `PB-014` [T-25, T-26]
- **Requerimientos:** `RF13` (Confirmación anticipada de asistencia hasta T-24h), `RNF07`
- **Reglas de Negocio:** `RN-08` (Corte de ratificación a T-24h), `RN-09` (Quórum mínimo)
- **Caso de Uso del SRS:** `CUS24` / `UC-024` (Confirmar asistencia anticipada a mentoría)
- **Actor:** Estudiante Mentoreado con reserva vigente
- **Descripción Estándar:**
  > *Como* estudiante con reserva pendiente,  
  > *Quiero* ratificar mi compromiso de asistencia antes de que falten 24 horas para el inicio de la sesión,  
  > *Para* asegurar mi plaza definitiva y contribuir al cómputo del quórum necesario para que la sesión se dicte.
- **Criterios de Aceptación:**
  - **CA-12.1 (Ratificación en plazo):** Si faltan más de 24 horas para la sesión (`delta > 24h`), el estudiante puede ratificar, transicionando su reserva a `CONFIRMADA`.
  - **CA-12.2 (Bloqueo fuera de plazo):** Si restan 24 horas o menos (`delta <= 24h`), el sistema bloquea la confirmación retornando HTTP 400 `WINDOW_CLOSED_T24H`.
- **Fuente Documental:** `docs/sprints/sprint-05.md`, `docs/sprints/sprint-05/02-trazabilidad/MAPA_FUENTES_SPRINT_05.md`, SRS §5.3 (RF13).

---

### HU-13 (PB-015): Desistimiento Voluntario y Liberación de Cupo
- **Identificador Derivado:** `HU-13` / `PB-015`
- **Nombre:** Desistimiento voluntario de reserva y restitución de vacante
- **Sprint:** Sprint 05
- **PBI Asociado:** `PB-015` [T-27, T-28]
- **Requerimientos:** `RF14` (Desistimiento voluntario y liberación anticipada de cupos), `RNF07`
- **Reglas de Negocio:** `RN-08` (Ventana de desistimiento), `RN-10` (Penalidades por cancelación tardía)
- **Caso de Uso del SRS:** `CUS17` / `UC-017` (Cancelar reserva de mentoría)
- **Actor:** Estudiante Mentoreado
- **Descripción Estándar:**
  > *Como* estudiante mentoreado con una reserva confirmada o pendiente,  
  > *Quiero* desistir voluntariamente de mi reserva antes del corte temporal de 24 horas,  
  > *Para* liberar mi cupo a otro compañero que lo necesite sin incurrir en penalidades institucionales.
- **Criterios de Aceptación:**
  - **CA-13.1 (Cancelación sin penalidad):** Al cancelar con antelación mayor a 24 horas, la reserva pasa a `CANCELADA_USUARIO` y la vacante se libera inmediatamente en el aforo.
  - **CA-13.2 (Restricción de titularidad):** Únicamente el titular de la reserva o un administrador pueden cancelar la reserva (`check_resource_ownership`).
- **Fuente Documental:** `docs/sprints/sprint-05.md`, SRS §5.3 (RF14).

---

### HU-14 (PB-017): Evaluación Automatizada de Quórum en T-24h
- **Identificador Derivado:** `HU-14` / `PB-017`
- **Nombre:** Evaluación programada de quórum mínimo e idempotencia
- **Sprint:** Sprint 06
- **PBI Asociado:** `PB-017` [T-29, T-30, T-31]
- **Requerimientos:** `RF15` (Monitoreo desatendido, alertas y quórum en T-24h), `RNF06`
- **Reglas de Negocio:** `RN-08`, `RN-09` (Quórum mínimo: 50% de aforo confirmado, ej. 5 de 10 presencial)
- **Caso de Uso del SRS:** `CUS23` / `UC-023` (Monitorear quórum y alertas desatendidas)
- **Actor:** Servicio Cron del Sistema / Administrador
- **Descripción Estándar:**
  > *Como* sistema institucional de mentorías,  
  > *Quiero* evaluar automáticamente las reservas ratificadas exactamente a las 24 horas previas al inicio de cada sesión,  
  > *Para* determinar si la sesión cuenta con quórum suficiente para su realización o requiere una decisión de contingencia.
- **Criterios de Aceptación:**
  - **CA-14.1 (Criterio de quórum):** Si las confirmaciones son menores al 50% del aforo (ej. 4 de 10), el estado pasa a `QUORUM_INSUFICIENTE`. Si son >= 50%, la sesión pasa a `CONFIRMADA`.
  - **CA-14.2 (Idempotencia T-30):** La evaluación repetida de una misma sesión ya procesada no altera su estado ni duplica registros.
- **Fuente Documental:** `docs/sprints/sprint-06.md`, SRS §5.3 (RF15).

---

### HU-15 (PB-018): Gestión Resolutiva de Contingencias por el Mentor
- **Identificador Derivado:** `HU-15` / `PB-018`
- **Nombre:** Decisión resolutiva del mentor ante quórum insuficiente
- **Sprint:** Sprint 06
- **PBI Asociado:** `PB-018` [T-32, T-33]
- **Requerimientos:** `RF16` (Gestión resolutiva ante quórum insuficiente), `RNF05`
- **Reglas de Negocio:** `RN-04`, `RN-10` (El sistema no cancela unilateralmente: decide el mentor)
- **Caso de Uso del SRS:** `CUS07` / `UC-007` (Gestionar contingencia ante quórum bajo)
- **Actor:** Mentor Académico titular de la sesión
- **Descripción Estándar:**
  > *Como* mentor académico titular de una sesión declarada en quórum insuficiente,  
  > *Quiero* decidir entre dictar la sesión de todas formas (PROCEED), reprogramarla con >24h (RESCHEDULE) o cancelarla justificadamente (CANCEL),  
  > *Para* adaptar el plan pedagógico sin perjudicar a los estudiantes que sí ratificaron su asistencia.
- **Criterios de Aceptación:**
  - **CA-15.1 (Opción PROCEED):** La sesión transiciona a `CONFIRMADA` con aforo reducido.
  - **CA-15.2 (Opción RESCHEDULE):** La nueva fecha debe cumplir antelación > 24h (RN-04) y el estado vuelve a `PUBLICADA`.
  - **CA-15.3 (Opción CANCEL):** Exige motivo obligatorio (mínimo 10 caracteres) y pasa a `CANCELADA_QUORUM`.
- **Fuente Documental:** `docs/sprints/sprint-06.md`, SRS §5.3 (RF16), §6.2.3 (CUS07).

---

### HU-16 (PB-019): Asistencia Digital con QR/TOTP y Bitácoras Pedagógicas
- **Identificador Derivado:** `HU-16` / `PB-019`
- **Nombre:** Registro de asistencia efectiva con código dinámico y bitácora de sesión
- **Sprint:** Sprint 06
- **PBI Asociado:** `PB-019` [T-34 al T-37]
- **Requerimientos:** `RF17` (Registro de bitácora y control de asistencia efectiva), `RNF02`, `RNF09`
- **Reglas de Negocio:** `RN-05`, `RN-12` (Bitácora obligatoria dentro de las 48 horas posteriores al fin de la sesión)
- **Caso de Uso del SRS:** `CUS08` / `UC-008` (en Sprint 06 rotulado como CUS12/CUS13)
- **Actor:** Mentor Titular (emite QR y llena bitácora) / Estudiante Asistente (escanea QR)
- **Descripción Estándar:**
  > *Como* mentor académico titular,  
  > *Quiero* proyectar un código QR dinámico TOTP durante la sesión para marcar la asistencia de los participantes y registrar la bitácora pedagógica antes de 48 horas,  
  > *Para* certificar las horas formativas impartidas y dejar evidencia académica del temario cubierto.
- **Criterios de Aceptación:**
  - **CA-16.1 (Token QR dinámico):** El token TOTP tiene vigencia corta (30-60 segundos) y solo permite check-in a estudiantes con reserva `CONFIRMADA`.
  - **CA-16.2 (Plazo de 48h RN-12):** La bitácora se registra únicamente dentro de las 48 horas posteriores al fin de la sesión. Si transcurren > 48h, el formulario se bloquea y el backend rechaza con HTTP 400.
  - **CA-16.3 (Validación de observaciones):** El campo observaciones exige al menos 50 caracteres académicos para ser admitido.
- **Fuente Documental:** `docs/sprints/sprint-06.md`, SRS §5.3 (RF17), §6.2.3 (CUS08).

---

## 4. Resumen Cuantitativo del Catálogo

| Categoría de Artefacto | Cantidad Total en Proyecto | Comprometidos Sprints 01-06 | Sprints Posteriores (S7, S8, Post) |
|---|:---:|:---:|:---:|
| **Historias de Usuario Explícitas (`HU-xx`)** | **8** | **8** (HU-01 a HU-08) | 0 (No redactadas formalmente) |
| **Historias Derivadas de PBIs (`HU-xx`)** | **16** | **16** (HU-01 a HU-16) | 18 (PBIs pendientes sin ficha HU) |
| **Product Backlog Items (PBI)** | **37** | **19** (PB-001 al PB-011, 013-015, 017-019, 031p, 036p) | **18** (PB-012, 016, 020-030, 032-035, 037) |
| **Requerimientos Funcionales (RF)** | **26** | **13** (RF01, 02, 03, 04, 05, 06, 08, 12, 13, 14, 15, 16, 17) | **13** (RF07, 09, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 26) |
| **Casos de Uso del SRS (CUS)** | **24** | **12** (CUS01, 02, 04, 06, 07, 08, 10, 15, 17, 21, 23, 24) | **12** (CUS03, 05, 09, 11, 12, 13, 14, 16, 18, 19, 20, 22) |
| **Reglas de Negocio Institucionales (RN)** | **14** | **10** (RN-01, 02, 03, 04, 05, 08, 09, 10, 11, 12) | **4** (RN-06, 07, 13, 14) |
| **Tareas Técnicas de Planificación (T)** | **51** | **37** (T-01 al T-37) | **14** (T-38 al T-51) |
| **Casos de Prueba en Catálogo Excel** | **141** | **82** (Casos sobre CUS01, 02, 04, 06, 07, 08, 10, 15, 17, 21, 23, 24) | **59** (Casos sobre CUS posteriores) |
