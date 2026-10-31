# Auditoría, Trazabilidad Integral y Respaldo Documental del Sprint 02

**Sistema Web P2P de Mentorías Académicas — EPIS UPT**  
**Documento de Ingeniería de Software:** `AUD-TRZ-S02`  
**Fecha de Emisión:** 26/10/2026 | **Versión:** 1.0.0 (Línea Base Oficial Congelada)  
**Ciclo Académico:** 2026-II | **Curso:** Construcción de Software I  
**Equipo Desarrollador:** Grupo 03 / C-SharkTeam:  
- **Joan Cristian Medina Quispe** (Código: 2022074255) — Arquitectura Base, Frontend & CI/CD (T-04, T-10, T-11)  
- **Renzo Antonio Antayhua Mamani** (Código: 2022073504) — Backend, Persistencia ORM & Seguridad RLS (T-05, T-08, T-12, T-13)  
**Docente Titular y Revisor:** Dr. Ricardo Eduardo Valcárcel Alvarado — Dirección EPIS-UPT  

---

## Control de Versiones y Auditoría Documental

| Versión | Fecha | Responsable | Aprobación | Resumen de Contenido y Cambios |
| :---: | :---: | :--- | :--- | :--- |
| **1.0.0** | 26/10/2026 | J. Medina / R. Antayhua | R. Valcárcel | Emisión oficial del informe de auditoría, trazabilidad bidireccional y respaldo documental del Sprint 02: Gobernanza de Consentimiento Digital (Ley N° 29733), Jerarquía de Roles y Mérito Académico (RN-03), Catálogo Curricular Avanzado (RF05/CUS21) y Perfiles Formativos con Matriz Horaria 6×11 (RF04/CUS15). Articulación con SRS (FD03 v2.0), SAD (FD04 v1.1), Catálogo de Pruebas (35 casos) y 150 pruebas automatizadas (84 backend / 66 frontend). |

---

## 1. Fase I — Inventario y Auditoría Documental del Sprint 02

Para garantizar que toda afirmación técnica cuente con respaldo fidedigno e inmutable, se ejecutó una inspección sistemática del repositorio, identificando los artefactos oficiales vigentes que gobiernan el Sprint 02:

### Cuadro 1.1: Inventario de Artefactos Oficiales del Sprint 02

| Documento o Artefacto | Versión Vigente | Ubicación en Repositorio | Relación con el Sprint 02 | Estado de Aprobación |
| :--- | :---: | :--- | :--- | :---: |
| **SRS (FD03): Requerimientos del Sistema** | v2.0 / v2.1 | `docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md` | Define formalmente RF02 (Consentimiento), RF03 (Roles), RF04 (Perfiles), RF05 (Catálogo), RNF01, RNF02, RNF04, RN-02 y RN-03. | Aprobado / Congelado |
| **SAD (FD04): Arquitectura de Software** | v1.1 / v2.0 | `docs/analisis/FD04-EPIS-Informe SAD de Proyecto.md` | Define las 4+1 Vistas de Kruchten (Escenarios 2.1, Lógica ECB 2.2, Procesos 2.3, Paquetes 2.4, Física 2.5), DDL 10.1 y Diagrama To-Be 7.2. | Aprobado / Congelado |
| **Planificación del Backlog y Tareas** | v1.2 | `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` | Define PBI comprometidos (PB-003, PB-005, PB-006, PB-007, PB-008) y desglose de tareas T-04, T-05, T-08, T-10, T-11, T-12 y T-13. | Aprobado / Verificado |
| **Bitácora de Ejecución del Sprint 02** | v1.0 | `docs/sprints/sprint-02.md` | Registro de 14 horas de ingeniería, diseño granular, matrices de verificación unitaria y certificación de cierre mediante DoD. | Consolidado |
| **Informe General de Cierre Sprint 02** | v1.0 | `docs/diseño/INFORME_GENERAL_SPRINT_02.md` | Reporte maestro exhaustivo con 9 diagramas PlantUML, contratos REST, esquema DDL de 5 tablas, políticas RLS y ADRs (ADR-005 a ADR-008). | Aprobado / Completo |
| **Catálogo Oficial de Pruebas** | v1.0 | `docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` | Contiene 35 casos de prueba aplicables a los casos de uso CUS01, CUS10, CUS15 y CUS21. | Oficial / Auditado |
| **Código Fuente Frontend (React + Vite)** | v1.0.0 | `aplicacion/frontend/src/` | Componentes `ConsentModalView.tsx`, `CurriculumCatalogView.tsx`, `ProfileAvailabilityView.tsx` y servicios cliente `consentService.ts`, `profileService.ts`. | Implementado (66 tests) |
| **Código Fuente Backend (FastAPI)** | v1.0.0 | `aplicacion/backend/app/` | Routers `consent.py`, `roles.py`, `profiles.py`, `curriculum.py`, servicios `ConsentService`, `RoleService`, `ProfileService` y modelos ORM. | Implementado (84 tests) |
| **Persistencia Relacional (PostgreSQL/Alembic)**| v002 | `aplicacion/backend/app/db/migrations/versions/002_roles_and_profiles.py` | DDL de tablas `consentimientos_legales`, `roles`, `usuario_roles`, `perfiles_academicos` y `disponibilidades_horarias`. | Aplicado en Supabase |
| **Script de Seguridad RLS** | v1.0 | `aplicacion/backend/scripts/supabase_rls_sprint02.sql` | 5 políticas `ROW LEVEL SECURITY` para aislamiento multiusuario condicionado al claim `auth.jwt() ->> 'email'`. | Aplicado en Supabase |

---

## 2. Fase II — Reconstrucción de la Trazabilidad Bidireccional

En cumplimiento estricto de la directriz de ingeniería de software, a continuación se presenta la **Matriz de Trazabilidad Bidireccional Completa** que articula cada requerimiento desde su necesidad legal/académica hasta su verificación empírica:

$$\text{Requerimiento} \longleftrightarrow \text{Regla} \longleftrightarrow \text{Historia} \longleftrightarrow \text{Caso de Uso} \longleftrightarrow \text{Análisis (SRS)} \longleftrightarrow \text{Diseño (SAD)} \longleftrightarrow \text{Código} \longleftrightarrow \text{DDL} \longleftrightarrow \text{Pruebas} \longleftrightarrow \text{Evidencia}$$

### Cuadro 2.1: Matriz de Trazabilidad Integral del Sprint 02 (12 Columnas Canónicas)

| 1. Requerimiento (RF/RNF) | 2. Regla de Negocio | 3. Historia de Usuario (HU) | 4. Caso de Uso (CUS) | 5. Narrativa Canónica | 6. Análisis (SRS FD03) | 7. Diseño (SAD FD04) | 8. Implementación (Código) | 9. Base de Datos (DDL) | 10. Pruebas Catálogo / Suite | 11. Estado | 12. Evidencia Verificable |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **RF02** — Consentimiento informado digital | **RN-02** — Consentimiento vinculante (bloqueo ante rechazo o revocación) | **HU-03** — Formalización y revocación de términos Ley N° 29733 | **CUS01** (Flujo de Consentimiento Legal) | Flujo Principal: modal al 1er login. Alt: revocación. Excepción: rechazo bloqueante. | SRS §5.3 (Cuadro 5.3), §5.4 (RN-02), §6.3.1.1 (Análisis ECB CUS01) | SAD §2.1 (Escenarios), §2.2 (Lógica), Diagrama 5 (Secuencia Consentimiento), Diagrama 9 (Estados) | `ConsentModalView.tsx`, `consentService.ts`, `consent.py`, `consent_service.py` | Tabla `consentimientos_legales` (`terms_version`, `accepted`, `consented_at`) | `CUS01-U03`, `CUS01-F01`, `CUS01-F02`, `test_consent.py` (5 tests), `ConsentModalView.test.tsx` (4 tests) | **COMPLETO** ✅ | Commit `3766a08`, Captura `01_consent_modal_ley29733.png` |
| **RF03** — Gestión y asignación administrativa de roles | **RN-03** — Mérito académico (ciclo $\ge \text{VII}$ obligatorio para Mentor) | **HU-04** — Promoción formal a Mentor y auditoría de mérito | **CUS10** — Gestionar Asignación y Elevación de Roles | Flujo Principal: evaluación de notas y ciclo $\ge 7$. Excepción: ciclo $< 7$ denegado. | SRS §5.3 (RF03), §5.4 (RN-03), §6.1 (Perfiles), §6.2.3 (Narrativa CUS10) | SAD §2.1, §2.2, Diagrama 4 (Casos de Uso), Diagrama 6 (Secuencia Roles y Mérito), Diagrama 9 (Estados) | `roles.py`, `role_service.py`, `roles.py` (modelos ORM `Rol`, `UsuarioRol`) | Tablas `roles`, `usuario_roles` (`FK id_rol`, `uq_usuario_roles_email_rol`) | `CUS10-U01`, `CUS10-U02`, `CUS10-U03`, `CUS10-F01`, `CUS10-A01`, `test_roles.py` (7 tests) | **COMPLETO** ✅ | Commit `3766a08`, Captura `03_profile_merit_validation.png` |
| **RF05** — Consulta interactiva y catálogo curricular oficial | **RN-04** — Dinámica curricular (insumo temario silábico) | **HU-05** — Exploración curricular avanzada con búsqueda profunda | **CUS21** — Explorar Catálogo Curricular y Temarios Filtro | Flujo Principal: listado y filtrado silábico reactivo en tiempo real. | SRS §5.3 (RF05), §6.2.3 (Narrativa CUS21), §6.3 (Análisis ECB) | SAD §2.1, §2.2, §2.4 (Paquetes), Diagrama 4 (Casos de Uso) | `CurriculumCatalogView.tsx`, `curriculum.py`, `curriculum_service.py` | Tabla `asignaturas`, `temas_silabicos` (índice B-Tree en código y ciclo formativo) | `CUS21-U01`, `CUS21-F01`, `CUS21-A01`, `test_curriculum.py` (8 tests), `CurriculumCatalogView.test.tsx` (4 tests) | **COMPLETO** ✅ | Commit `3766a08`, Captura `02_curriculum_advanced_search.png` |
| **RF04** — Perfil formativo y matriz semanal de disponibilidad | **RN-03** — Mérito (alerta preventiva en cliente si ciclo $< 7$) | **HU-06** — Configuración de perfil y agenda horaria semanal (6×11) | **CUS15** — Configurar Perfil Formativo y Matriz Horaria | Flujo Principal: selección formativa y marcado de celdas horarias. Alt: atajos rápidos. | SRS §5.3 (RF04), §6.2.3 (Narrativa CUS15), §6.3 (Análisis ECB) | SAD §2.1, §2.2, §2.3 (Transacciones), Diagrama 7 (Secuencia Reemplazo Atómico) | `ProfileAvailabilityView.tsx`, `profileService.ts`, `profiles.py`, `profile_service.py` | Tablas `perfiles_academicos` (`JSONB materias`), `disponibilidades_horarias` (`CHECK dia 1..6`) | `CUS15-U01`, `CUS15-U02`, `CUS15-F01`, `CUS15-A01`, `test_profiles.py` (11 tests), `ProfileView.test.tsx` (5 tests) | **COMPLETO** ✅ | Commit `3766a08`, Captura `04_weekly_availability_grid.png` |
| **RNF02** — Privacidad y aislamiento multiusuario | **Ley N° 29733** (Protección de Datos Personales) | **HU-07** — Aislamiento estricto de expedientes y prevención de cross-access | **CUS01** / **CUS15** (Seguridad RLS) | Flujo Principal: acceso condicionado a identidad. Excepción: intento ajeno $\rightarrow$ HTTP 403. | SRS §5.3 (RNF02), §6.1 (Perfiles) | SAD §2.2 (Seguridad), §10.1 (DDL RLS), Diagrama 8 (Secuencia Aislamiento RLS) | `_resolve_authenticated_email()`, middleware de autenticación | 5 políticas `ROW LEVEL SECURITY` (`auth.jwt() ->> 'email'`) | `test_authorization.py` (11 tests: cruce de cuentas, autopromoción, tokens inválidos) | **COMPLETO** ✅ | Commit `3766a08`, Script `supabase_rls_sprint02.sql` |
| **RNF09** — Arquitectura desacoplada y cobertura $\ge 70\%$ | Normas IEEE 830 / ISO/IEC 25010 | **HU-08** — Interfaces OpenAPI fuertemente tipadas y pruebas automatizadas | Todos los CUS de S2 | Contratos REST JSON Pydantic / TypeScript tipados y pruebas automatizadas. | SRS §5.3 (RNF09) | SAD §2.4 (Desarrollo), §9.1 (Componentes) | Esquemas Pydantic v2 en `app/schemas/`, interfaces TypeScript en `src/services/` | Validaciones Pydantic (`EmailStr`, `Literal`, regex `@upt.pe`) | 150 pruebas automatizadas (84 backend / 66 frontend), 0 fallos | **COMPLETO** ✅ | Backend: **90.64%**, Frontend: **91.10%** (Capturas 06 y 07) |

### 2.2. Resumen Cuantitativo de Cobertura de Trazabilidad del Sprint 02
- **Requerimientos Funcionales comprometidos:** 4 (RF02, RF03, RF04, RF05) $\rightarrow$ 4 implementados y verificados (**100% de cobertura funcional**).
- **Requerimientos No Funcionales verificados:** 4 (RNF01, RNF02, RNF04, RNF09) $\rightarrow$ 4 homologados con evidencia (**100% de cobertura RNF**).
- **Reglas de Negocio Institucionales:** 2 (RN-02, RN-03) $\rightarrow$ 2 implementadas en dos niveles (cliente y servidor) con pruebas negativas deterministas (**100% de cumplimiento**).
- **Casos de Uso abordados:** 4 (CUS01, CUS10, CUS15, CUS21) $\rightarrow$ 4 con narrativas completas y contratos REST operativos (**100%**).
- **Casos del Catálogo Oficial Vinculados:** 35 casos delimitados en `Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` $\rightarrow$ 17 pruebas unitarias/funcionales automatizadas en código directamente homologables + 25 pruebas de integración y seguridad asociadas a los endpoints del sprint.

---

## 3. Fase III — Respaldo de Análisis (SRS) y Diseño Técnico (SAD)

### 3.1. Análisis Funcional (SRS FD03): Historias de Usuario con Criterios Gherkin

#### Historia de Usuario HU-03: Formalización del Consentimiento Digital (Ley N° 29733)
* **Como** estudiante de la Universidad Privada de Tacna,
* **Quiero** revisar las cláusulas institucionales de tratamiento de datos personales y otorgar mi consentimiento formal e informado en mi primer inicio de sesión,
* **Para** que mi historial de asignaturas, notas y disponibilidad horaria sean tratados legalmente por la plataforma, teniendo la facultad de revocar dicho consentimiento en cualquier momento.

```gherkin
Escenario: Aceptación exitosa del consentimiento informado institucional
  Dado que el estudiante "2022074255@upt.pe" ha validado su acceso OTP y no registra consentimiento vigente
  Cuando el sistema despliega el componente modal "ConsentModalView" con las cláusulas de la Ley N° 29733
  Y el estudiante marca la casilla "He leído y acepto los términos de tratamiento de datos personales"
  Y presiona el botón "Aceptar y Continuar"
  Entonces el sistema emite una petición POST a "/api/v1/consent/accept"
  Y persiste el registro en "consentimientos_legales" con estado accepted=True, marca temporal UTC y dirección IP
  Y desbloquea la navegación permitiendo el ingreso al catálogo de servicios.

Escenario: Rechazo y bloqueo preventivo del acceso (Regla RN-02)
  Dado que el estudiante visualiza el formulario institucional de consentimiento informado
  Cuando presiona el botón "Rechazar y Salir" sin marcar la casilla de conformidad
  Entonces el sistema emite una petición POST a "/api/v1/consent/revoke"
  Y registra el rechazo con accepted=False en la base de datos
  Y despliega un banner de advertencia rojo informando la imposibilidad de operar en el sistema bajo RN-02
  Y bloquea de forma preventiva el acceso a perfiles, reservas y catálogo.
```

#### Historia de Usuario HU-04: Asignación de Roles y Verificación de Mérito (RN-03)
* **Como** Administrador del Comité de Tutoría de la EPIS-UPT,
* **Quiero** gestionar la jerarquía de roles institucionales y verificar que los postulantes a mentor cursen el séptimo ciclo o superior,
* **Para** garantizar que únicamente estudiantes con suficiencia académica y madurez formativa brinden tutoría a los ciclos iniciales.

```gherkin
Escenario: Promoción exitosa a Mentor de estudiante con mérito académico
  Dado que el estudiante "2022073504@upt.pe" registra ciclo_actual = 8 en su perfil académico
  Cuando el Administrador invoca "POST /api/v1/roles/promote-mentor" con cabecera Bearer administrativa
  Entonces el servicio "RoleService" verifica que ciclo_actual >= 7 (RN-03)
  Y registra la tupla en "usuario_roles" con id_rol = 2 (mentor) y activo = True
  Y retorna código HTTP 200 OK con la lista de roles actualizada ["mentoreado", "mentor"].

Escenario: Rechazo determinista de promoción por mérito insuficiente (RN-03)
  Dado que el estudiante "2022079999@upt.pe" registra ciclo_actual = 5 (ciclo inferior al séptimo)
  Cuando se solicita su elevación a rol Mentor
  Entonces el servicio "RoleService" detecta que ciclo_actual < 7
  Y aborta la operación retornando HTTP 400 Bad Request
  Y remite en el cuerpo JSON el código de error canónico "MERIT_RULE_VIOLATION"
  Y no modifica los privilegios del estudiante en la base de datos.
```

#### Historia de Usuario HU-05: Consulta Avanzada del Catálogo Curricular
* **Como** estudiante mentoreado o mentor,
* **Quiero** explorar de manera interactiva el catálogo de asignaturas formativas y sus unidades silábicas oficiales mediante un buscador en tiempo real,
* **Para** identificar con precisión los temas conceptuales críticos en los que requiero apoyo pedagógico o poseo competencias para dictar asesorías.

```gherkin
Escenario: Búsqueda reactiva de temas silábicos en tiempo real
  Dado que el usuario accede a la vista "CurriculumCatalogView"
  Cuando ingresa el término "Punteros" en el cuadro de búsqueda
  Entonces la interfaz filtra instantáneamente el árbol curricular
  Y resalta la asignatura "Algoritmos y Estructuras de Datos" con un distintivo "Coincidencia" en el tema silábico
  Y oculta las asignaturas cuyos temarios no concuerdan con el criterio de búsqueda.
```

#### Historia de Usuario HU-06: Configuración de Perfil y Matriz Semanal de Disponibilidad (6×11)
* **Como** estudiante de la EPIS-UPT,
* **Quiero** configurar mi perfil formativo (materias de interés, modalidad) y marcar mis horas libres en una grilla semanal interactiva de 6 días por 11 horas,
* **Para** que la plataforma y el motor de recomendación conozcan con exactitud mi disponibilidad para agendar o recibir mentorías.

```gherkin
Escenario: Reemplazo atómico de la agenda de disponibilidad horaria
  Dado que el estudiante selecciona 4 bloques horarios en la grilla semanal (Lunes 08:00-10:00 y Miércoles 14:00-16:00)
  Cuando presiona el botón "Guardar Perfil y Disponibilidad"
  Entonces el backend ejecuta una transacción ACID que elimina los registros previos del estudiante en "disponibilidades_horarias"
  E inserta las 4 nuevas franjas bajo formato HH:MM validado
  Y confirma la operación retornando HTTP 200 con el total de slots actualizados.
```

---

### 3.2. Narrativas Canónicas de Casos de Uso del Sprint 02 (SRS FD03)

#### CUS01 (Flujo de Consentimiento Digital — Ley N° 29733)
- **Actor:** Estudiante Universitario (`@upt.pe`).
- **Propósito:** Capturar formalmente la conformidad legal de tratamiento de datos personales conforme al D.S. N° 003-2013-JUS antes de habilitar el uso de su expediente en el emparejamiento algorítmico.
- **Flujo Principal:** 
  1. El estudiante autentica su identidad mediante OTP.
  2. El frontend consulta `GET /api/v1/consent/status`.
  3. Si `has_consented == False`, despliega el modal `ConsentModalView` bloqueando la navegación de fondo.
  4. El estudiante lee las cláusulas (finalidad exclusiva, datos tratados, derechos ARCO, no cesión a terceros) y marca el checkbox.
  5. Pulsa «Aceptar y Continuar».
  6. El sistema envía `POST /api/v1/consent/accept` y almacena la tupla en `consentimientos_legales` con marca UTC e IP.
  7. El sistema cierra el modal y desbloquea el acceso.
- **Flujos Alternativos:** 
  - *FA01: Revocación posterior:* El usuario accede a la configuración de privacidad y presiona «Revocar consentimiento», transicionando el registro a `accepted = False` y activando el bloqueo preventivo RN-02.
- **Excepciones:** 
  - *E01: Rechazo expreso:* El estudiante presiona «Rechazar y Salir»; el sistema invoca `POST /api/v1/consent/revoke`, registra el estado revocado y despliega banner de advertencia bloqueante impidiendo el uso de la aplicación (RN-02).

#### CUS10 (Gestión de Roles y Verificación de Mérito Académico — RN-03)
- **Actor:** Administrador (Comité de Tutoría / Dirección EPIS) y Estudiante Postulante.
- **Propósito:** Administrar la asignación y revocación de roles, aplicando la restricción institucional de que la tutoría formal solo puede ser ejercida por estudiantes de ciclos avanzados (VII al X).
- **Flujo Principal:**
  1. El Administrador consulta la lista de postulantes en `AdminMentorPromotionView`.
  2. Selecciona un estudiante y solicita su promoción mediante `POST /api/v1/roles/promote-mentor`.
  3. El servicio `RoleService` consulta `perfiles_academicos.ciclo_actual`.
  4. Valida que `ciclo_actual >= 7` (**RN-03**).
  5. Asigna el rol en `usuario_roles` con `id_rol = 2` y registra `asignado_por`.
  6. Notifica al administrador la habilitación del nuevo Mentor Académico.
- **Excepciones:**
  - *E01: Infracción de mérito:* Si el estudiante pertenece a los ciclos formativos I al VI (`ciclo_actual < 7`), el sistema rechaza la solicitud retornando `HTTP 400 Bad Request` con el mensaje canónico `MERIT_RULE_VIOLATION`.
  - *E02: Intento de autopromoción:* Si un estudiante invoca directamente el endpoint pretendiendo promoverse a sí mismo sin token de administrador, el sistema aborta con `HTTP 403 Forbidden` (`SELF_PROMOTION_FORBIDDEN`).

#### CUS15 (Configuración de Perfil Formativo y Matriz de Disponibilidad)
- **Actor:** Estudiante Mentoreado / Mentor.
- **Propósito:** Capturar las competencias formativas, dificultades pedagógicas y agenda semanal estructurada de 1 hora.
- **Flujo Principal:**
  1. El estudiante accede a la vista de perfil (`ProfileAvailabilityView.tsx`).
  2. En la Pestaña 1, selecciona ciclo académico, materias filtro de interés y modalidad (Presencial/Virtual).
  3. En la Pestaña 2, interactúa con la grilla de **6 días (Lunes a Sábado) × 11 bloques (08:00 a 20:00)** marcando sus horas libres.
  4. Presiona «Guardar Perfil y Disponibilidad».
  5. El backend valida los esquemas y ejecuta el **reemplazo atómico** de la agenda en una única transacción de base de datos.
  6. La UI despliega confirmación verde y actualiza el contador de bloques comprometidos.
- **Excepciones:**
  - *E01: Detección preventiva de mérito:* Si un alumno con ciclo menor a VII selecciona el rol de postulación a Mentor, la UI renderiza de inmediato un banner rojo alertando sobre la regla RN-03.
  - *E02: Formato o solapamiento horaria:* Si se remiten bloques con `hora_inicio >= hora_fin` o solapamientos en el mismo día, el backend responde con `HTTP 422 Unprocessable Entity`.

#### CUS21 (Consulta Avanzada del Catálogo Curricular)
- **Actor:** Estudiante Universitario.
- **Propósito:** Navegar la taxonomía oficial de materias críticas (I al IV ciclo) y su desglose en temas silábicos oficiales.
- **Flujo Principal:**
  1. El estudiante ingresa a la pestaña «Catálogo Curricular».
  2. El sistema carga las asignaturas filtro desde `GET /api/v1/curriculum/courses`.
  3. El usuario utiliza los filtros de ciclo (I al IV) o ingresa texto en el buscador en tiempo real.
  4. Al seleccionar una asignatura, el sistema despliega el temario silábico oficial jerarquizado con indicación de ponderadores Top-k.

---

### 3.3. Diseño Técnico y Vistas Arquitectónicas (SAD FD04)

A continuación, se presentan los diagramas de diseño oficiales del Sprint 02, acompañados de su explicación pedagógica para desarrolladores:

#### Diagrama 3.4: Casos de Uso del Sprint 02 — Límites del Sistema y Actores
Modela los límites de responsabilidad del Sprint 02, diferenciando los casos de uso para el Estudiante regular, el Postulante a Mentor (sujeto a RN-03) y el Administrador de Escuela:

![Diagrama 3.4: Casos de Uso del Sprint 2](imagenes/sprint-02/08_diagrama_casos_de_uso_sprint02.png)

*Figura 3.1: Diagrama de Casos de Uso del Sprint 2 (Roles, Currículo y Perfiles).*  
*(Nota: Para visualización vectorial escalable, consultar [08_diagrama_casos_de_uso_sprint02.svg](imagenes/sprint-02/08_diagrama_casos_de_uso_sprint02.svg)).*

* **Explicación para el equipo:** El diagrama delimita que cualquier estudiante universitario autenticado debe cumplir obligatoriamente con el consentimiento digital (`CUS01`) como precondición antes de editar su perfil (`CUS15`). Asimismo, formaliza que el actor *Postulante a Mentor* es una especialización del *Estudiante*, pero condicionado por la regla **RN-03** (ciclo $\ge \text{VII}$), mientras que el *Administrador* es el único facultado para ejecutar la asignación formal de privilegios (`CUS10-A`).

---

#### Diagrama 5: Secuencia Técnica — Registro y Validación de Consentimiento Informado (T-04 / T-05)
Modela la interacción asíncrona entre el modal React, el servicio cliente, el router de FastAPI y la persistencia en PostgreSQL:

![Diagrama 5: Secuencia Técnica: Consentimiento Digital](imagenes/sprint-02/09_secuencia_consentimiento_ley29733.png)

*Figura 3.2: Secuencia técnica del flujo de consentimiento bajo Ley N° 29733 y bloqueo RN-02.*  
*(Nota: Versión vectorial en [09_secuencia_consentimiento_ley29733.svg](imagenes/sprint-02/09_secuencia_consentimiento_ley29733.svg)).*

* **Explicación para el equipo:** Ilustra los dos caminos posibles que puede tomar el usuario al iniciar sesión:
  - *Escenario A (Aceptación):* El usuario marca la casilla de conformidad y pulsa «Aceptar»; la llamada viaja por HTTP POST hacia `consent.py`, el cual inserta en `consentimientos_legales` la estampa UTC del servidor y la dirección IP, retornando éxito y desbloqueando la aplicación.
  - *Escenario B (Rechazo / Revocación — Regla RN-02):* El usuario presiona «Rechazar y Salir»; el sistema invoca `POST /api/v1/consent/revoke`, actualiza el registro a `accepted = False` y la interfaz bloquea la pantalla con una alerta roja permanente, garantizando que no se procese ningún dato académico sin autorización legal.

---

#### Diagrama 6: Secuencia Técnica — Asignación de Roles y Verificación de Mérito (T-08 / RN-03)
Modela la intercepción defensiva del mérito académico en la capa de servicios backend:

![Diagrama 6: Secuencia Técnica: Roles y Mérito RN-03](imagenes/sprint-02/10_secuencia_roles_merito_rn03.png)

*Figura 3.3: Secuencia técnica de asignación de roles con validación de mérito RN-03.*  
*(Nota: Versión vectorial en [10_secuencia_roles_merito_rn03.svg](imagenes/sprint-02/10_secuencia_roles_merito_rn03.svg)).*

* **Explicación para el equipo:** Modela cómo se protege la integridad académica del sistema:
  1. Si un usuario no administrador intenta promoverse a sí mismo, el router rechaza la solicitud de inmediato con `HTTP 403 Forbidden` (`SELF_PROMOTION_FORBIDDEN`).
  2. Cuando el Administrador solicita la promoción, `RoleService` consulta en `perfiles_academicos` el ciclo del postulante. Si el ciclo es menor a 7 (infracción de **RN-03**), el sistema levanta una excepción `HTTP 400 Bad Request` con código `MERIT_RULE_VIOLATION`. Solo si el ciclo es $\ge 7$, se inserta el rol de Mentor en la tabla `usuario_roles`.

---

#### Diagrama 7: Secuencia Técnica — Perfiles y Reemplazo Atómico de Matriz Horaria (T-11 / T-12)
Ilustra la actualización transaccional íntegra de la agenda horaria semanal (Lunes a Sábado, 08:00 a 20:00):

![Diagrama 7: Secuencia Técnica: Perfiles y Agenda 6x11](imagenes/sprint-02/11_secuencia_perfil_disponibilidad_atomic.png)

*Figura 3.4: Secuencia técnica de reemplazo atómico transaccional de la matriz horaria.*  
*(Nota: Versión vectorial en [11_secuencia_perfil_disponibilidad_atomic.svg](imagenes/sprint-02/11_secuencia_perfil_disponibilidad_atomic.svg)).*

* **Explicación para el equipo:** Muestra una decisión de diseño arquitectónico crítica (**ADR-007**): Para evitar que la matriz semanal de un usuario quede en un estado inconsistente o con bloques desfasados si falla la conexión a mitad del guardado, el backend abre una **transacción atómica (`session.begin()`)**. En una sola operación relacional, purga (`DELETE`) todas las franjas previas del estudiante e inserta (`INSERT`) el nuevo conjunto validado, ejecutando `COMMIT` solo si todas las celdas cumplen el formato `HH:MM` y el rango válido de días (1 a 6).

---

#### Diagrama 8: Secuencia Técnica — Aislamiento Criptográfico y Seguridad Multi-Usuario RLS (T-13 / RNF02)
Modela la intercepción de accesos no autorizados entre cuentas estudiantiles en el nivel de endpoint y en el motor relacional:

![Diagrama 8: Secuencia Técnica: Seguridad Multi-Usuario RLS](imagenes/sprint-02/12_secuencia_seguridad_multiusuario_rls.png)

*Figura 3.5: Secuencia técnica de aislamiento de cuentas y evaluación de políticas RLS.*  
*(Nota: Versión vectorial en [12_secuencia_seguridad_multiusuario_rls.svg](imagenes/sprint-02/12_secuencia_seguridad_multiusuario_rls.svg)).*

* **Explicación para el equipo:** Demuestra la estrategia de *Defensa en Profundidad*: Si un usuario malicioso (`usuarioA@upt.pe`) envía una solicitud adulterada intentando consultar el perfil privado de `usuarioB@upt.pe`, el router backend extrae criptográficamente la identidad real del token JWT. Al constatar que el sujeto del token no coincide con el correo solicitado y que no es administrador, aborta la petición con `HTTP 403 Forbidden` (`FORBIDDEN_CROSS_ACCESS`). Adicionalmente, en la base de datos Supabase, la política de **Row Level Security (RLS)** evalúa `USING (email = auth.jwt() ->> 'email')`, impidiendo cualquier fuga física de datos en caso de brechas en la API.

---

#### Diagrama 9: Máquinas de Estado del Ciclo de Vida del Consentimiento Legal y del Rol de Usuario
Especifica los estados válidos, transiciones y condiciones de guarda del Sprint 02:

![Diagrama 9: Máquinas de Estado: Consentimiento y Roles](imagenes/sprint-02/13_maquina_estados_consentimiento_roles.png)

*Figura 3.6: Máquinas de estado para el consentimiento Ley N° 29733 y la jerarquía de roles RN-03.*  
*(Nota: Versión vectorial en [13_maquina_estados_consentimiento_roles.svg](imagenes/sprint-02/13_maquina_estados_consentimiento_roles.svg)).*

* **Explicación para el equipo:** Especifica formalmente que el consentimiento transiciona de `PENDIENTE` a `OTORGADO` tras la firma digital, pudiendo pasar a `REVOCADO` si el alumno lo solicita voluntariamente (quedando en bloqueo preventivo). En la máquina de roles, todo usuario ingresa en `MENTOREADO_BASE`. Al declarar interés en su perfil, pasa a `POSTULANTE_A_MENTOR`, pero **únicamente** transiciona a `MENTOR_ACREDITADO` cuando la Dirección EPIS o el sistema verifican que su ciclo formativo es mayor o igual a 7 (`ciclo_actual >= 7`).

---

#### Diagrama 3: Modelo Entidad-Relación Relacional Físico de Base de Datos (Sprint 02)
Modela las 5 tablas creadas en PostgreSQL mediante la migración `002_roles_and_profiles.py`:

![Diagrama 3: Modelo Entidad-Relación Físico](imagenes/sprint-02/14_diagrama_entidad_relacion_sprint02.png)

*Figura 3.7: Modelo relacional DDL de las tablas creadas en el Sprint 02.*  
*(Nota: Versión vectorial en [14_diagrama_entidad_relacion_sprint02.svg](imagenes/sprint-02/14_diagrama_entidad_relacion_sprint02.svg)).*

* **Explicación para el equipo:** Muestra las 5 tablas estructuradas:
  1. `roles`: catálogo inmutable de roles institucionales (1=mentoreado, 2=mentor, 3=administrador).
  2. `usuario_roles`: tabla asociativa con clave única compuesta `(email, id_rol)`, fecha de asignación y registro de auditoría `asignado_por`.
  3. `consentimientos_legales`: bitácora legal que almacena el correo, versión de términos, estado booleano `accepted`, estampa UTC, IP de origen y agente de usuario.
  4. `perfiles_academicos`: tabla de competencias del estudiante con restricción de integridad `CHECK (ciclo_actual BETWEEN 1 AND 10)`, modalidad preferida y campos JSON para materias y temas silábicos.
  5. `disponibilidades_horarias`: franjas semanales asociadas al correo con restricción `CHECK (dia_semana BETWEEN 1 AND 6)` (Lunes a Sábado) y horas en formato `HH:MM`.

---

## 4. Fase IV — Auditoría Completa del Catálogo de Pruebas

En estricta sujeción a la directriz de auditoría, se examinó el catálogo oficial `Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` confrontándolo con las pruebas implementadas en el código fuente:

### 4.1. Mapeo de Casos de Prueba del Catálogo Oficial Vinculados al Sprint 02

| ID Caso Catálogo | Nombre del Caso de Prueba | Tipo / Nivel | Requerimiento / CUS | Escenario Evaluado | Resultado Especificado | Estado en Catálogo | Mapeo a Suite Automatizada en Código |
| :--- | :--- | :---: | :---: | :--- | :--- | :---: | :--- |
| **`CUS01-U01`** | Validar dominio institucional `@upt.pe` | Unitaria / Comp. | RF01, RF02 / CUS01 | Correo `@upt.pe` vs correos externos (`@gmail.com`) | Rechazar correos externos con error de validación | Definido | `test_accept_consent_rejects_external_email` en `test_consent.py` |
| **`CUS01-U03`** | Bloquear sesión si se rechaza consentimiento | Unitaria / Comp. | RF02 / CUS01, RN-02 | Evaluación de `accepted == False` bajo Ley 29733 | Revocar acceso y emitir bloqueo preventivo | Definido | `test_revoke_consent_blocks_access` en `test_consent.py` y suites Vitest |
| **`CUS01-F01`** | Flujo primer login con consentimiento y 2FA | Funcional / Sist. | RF01, RF02 / CUS01 | Alumno nuevo acepta términos y completa acceso | Despliegue de modal, guardado de marca UTC y entrada | Definido | `ConsentModalView.test.tsx` (Test 3: Aceptación exitosa) |
| **`CUS01-F02`** | Flujo de rechazo de consentimiento bloquea acceso | Funcional / Sist. | RF02 / CUS01, RN-02 | Alumno rechaza términos explícitamente | Abandono forzoso, revocación y banner bloqueante | Definido | `ConsentModalView.test.tsx` (Test 4: Rechazo bloqueante RN-02) |
| **`CUS01-A01`** | Aceptación: cumplimiento legal Ley N° 29733 | Aceptación / Sist. | RF02, RNF02 / CUS01 | Auditoría de estampa temporal UTC y dirección IP | 100% de consentimientos registrados auditables | Definido | `test_accept_consent_success` en `test_consent.py` |
| **`CUS10-U01`** | Asignar rol Mentoreado por defecto a nuevo usuario | Unitaria / Comp. | RF03 / CUS10 | Consulta de roles para usuario sin registro previo | Retornar lista conteniendo exclusivamente `mentoreado` | Definido | `test_get_user_roles_default_is_mentoreado` en `test_roles.py` |
| **`CUS10-U02`** | Validar récord académico antes de promover a Mentor | Unitaria / Comp. | RF03 / CUS10, RN-03 | Promoción con ciclo 5 vs promoción con ciclo 8 | Ciclo $< 7 \rightarrow$ 400 Bad Request; Ciclo $\ge 7 \rightarrow$ 200 OK | Definido | `test_promote_mentor_rejects_when_cycle_below_7_rn03` en `test_roles.py` |
| **`CUS10-U03`** | Restringir elevación de rol solo al Administrador | Unitaria / Comp. | RF03, RNF02 / CUS10 | Alumno intenta promoverse a sí mismo | Bloquear con HTTP 403 Forbidden | Definido | `test_denial_of_self_promotion_to_mentor_without_admin` en `test_authorization.py` |
| **`CUS10-F01`** | Flujo de promoción de estudiante a Mentor | Funcional / Sist. | RF03 / CUS10, RN-03 | Administrador audita mérito y confirma ascenso | Rol asignado, registro de `asignado_por` en BD | Definido | `test_admin_can_promote_and_access` en `test_authorization.py` |
| **`CUS10-A01`** | Aceptación: trazabilidad y auditoría de roles | Aceptación / Sist. | RF03 / CUS10 | 15 promociones auditadas con fecha y responsable | Cero promociones sin auditoría o con ciclo $< 7$ | Definido | `test_promote_mentor_success_when_cycle_7_or_above` en `test_roles.py` |
| **`CUS15-U01`** | Guardar franjas horarias libres declaradas | Unitaria / Comp. | RF04 / CUS15 | Inserción de bloques Lunes a Sábado en formato 24h | Franjas persistidas ordenadas cronológicamente | Definido | `test_get_and_update_availability` en `test_profiles.py` |
| **`CUS15-U02`** | Actualizar vector de competencias del perfil | Unitaria / Comp. | RF04 / CUS15 | Actualización de materias de interés y modalidad | Datos persistidos en `perfiles_academicos` | Definido | `test_update_profile_success` en `test_profiles.py` |
| **`CUS15-F01`** | Flujo de actualización de perfil y agenda 6×11 | Funcional / Sist. | RF04, RNF04 / CUS15 | Alumno modifica grilla semanal y guarda datos | Transacción atómica en BD y confirmación visual | Definido | `ProfileAvailabilityView.test.tsx` (Test 1 al 5) |
| **`CUS15-A01`** | Aceptación: consistencia de matriz con recomendador | Aceptación / Sist. | RF04 / CUS15 | Validación de ausencia de solapamientos y días 1..6 | 100% de franjas coherentes sin estados corruptos | Definido | `test_availability_duplicate_and_overlapping_slots` |
| **`CUS21-U01`** | Crear y editar asignatura filtro y temas silábicos | Unitaria / Comp. | RF05 / CUS21 | Consulta del catálogo de las 5 materias formativas | Listado completo de materias de I a IV ciclo | Definido | `test_list_courses_returns_5_filter_courses` en `test_curriculum.py` |
| **`CUS21-F01`** | Flujo de consulta interactiva de catálogo silábico | Funcional / Sist. | RF05, RNF08 / CUS21 | Alumno busca temas silábicos (*Punteros C++*) | Filtrado reactivo en DOM con badge de coincidencia | Definido | `CurriculumCatalogView.test.tsx` (Test 1 al 4) |
| **`CUS21-A01`** | Aceptación: consistencia de asignaturas y temas | Aceptación / Sist. | RF05 / CUS21 | Verificación de taxonomía silábica en tiempo real | Cero inconsistencias temáticas entre front y back | Definido | `test_get_course_topics_success` en `test_curriculum.py` |

### 4.2. Ejecución Empírica y Reproducibilidad de Pruebas Automatizadas
Las pruebas fueron ejecutadas localmente en el entorno de desarrollo y en integración continua (GitHub Actions), registrando los siguientes comandos reproducibles:

#### Acreditación de Pruebas de Backend (Python 3.13 / Pytest 9.1):
```bash
# Comando de ejecución reproducible para el alcance del Sprint 02:
python -m pytest aplicacion/backend/tests/test_consent.py \
                 aplicacion/backend/tests/test_roles.py \
                 aplicacion/backend/tests/test_profiles.py \
                 aplicacion/backend/tests/test_authorization.py \
                 aplicacion/backend/tests/test_curriculum.py --no-cov -v
```
* **Resultado Observado:** **42 pruebas ejecutadas y aprobadas al 100% (42 passed in 1.37s)**, 0 fallos, 0 errores.
* **Cobertura de Código de Backend (Pytest-Cov al cierre de S2):** **90.64% de cobertura de líneas** (superando el 70% de RNF09).

#### Acreditación de Pruebas de Frontend (Node.js 20 / Vitest 2.1):
```bash
# Comando de ejecución reproducible para el frontend:
npm --prefix aplicacion/frontend test -- --run
```
* **Resultado Observado:** **87 pruebas ejecutadas y aprobadas al 100% (87 passed in 17.21s)**, correspondientes a 13 suites de prueba (incluyendo las suites de ConsentModalView, CurriculumCatalogView y ProfileAvailabilityView).
* **Cobertura de Código de Frontend (v8 coverage al cierre de S2):** **91.10% de cobertura de líneas**.

---

## 5. Fase V — Detección de Inconsistencias y Acciones de Alineación

Durante la auditoría del Sprint 02 se identificaron los siguientes hallazgos técnicos documentales y arquitectónicos, registrándose su severidad, impacto y estado de resolución:

| ID Hallazgo | Tipo de Inconsistencia | Severidad | Comportamiento Documentado en SRS/SAD | Implementación Encontrada en Código | Corrección / Estado | Justificación Técnica |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| **INC-01** | Regla de Negocio / Mérito | Alta | RN-03 exige que solo alumnos de ciclo $\ge 7$ puedan postular o ser promovidos a Mentor. | En la versión inicial de `ProfileAvailabilityView.tsx`, el selector de rol no impedía visualmente marcar "Postulante a Mentor" con ciclos inferiores. | **Corregido** ✅ | Se incorporó en frontend una comprobación reactiva que renderiza una alerta roja visible informativa si `ciclo < 7`, y en el backend se forzó el rechazo con `HTTP 400 MERIT_RULE_VIOLATION`. |
| **INC-02** | Base de Datos / Concurrencia | Media | RNF07 exige consistencia transaccional y prevención de estados corruptos en la agenda horaria. | Inicialmente, la actualización de disponibilidad en `ProfileService` ejecutaba inserciones fila por fila sin envoltorio transaccional explícito. | **Corregido** ✅ | Se refactorizó `update_availability()` mediante un bloque atómico `session.begin()` que purga las franjas previas e inserta el nuevo conjunto en un único `COMMIT` (**ADR-007**). |
| **INC-03** | Seguridad / Aislamiento | Crítica | RNF02 y Ley N° 29733 exigen aislamiento total de expedientes entre estudiantes. | Existía el riesgo de que un usuario autenticado consultara perfiles ajenos pasando un parámetro `?email=` manipulado en la URL. | **Corregido** ✅ | Se implementó la función `_resolve_authenticated_email()` en el router, validando que el sujeto del JWT coincida con el correo objetivo o pertenezca a un administrador, abortando con `HTTP 403 Forbidden` (`FORBIDDEN_CROSS_ACCESS`). Adicionalmente se activó RLS en PostgreSQL. |
| **INC-04** | Formato / Documentación | Baja | `rules_doc.md` estipula que cada sprint debe contar con su informe académico formal de 11 secciones (`G03_EPIS_Informe_Sprint_02.md`). | El Sprint 02 contaba con `sprint-02.md` y un `INFORME_GENERAL_SPRINT_02.md` de 15 secciones, pero carecía del informe canónico foliado `G03_EPIS_Informe_Sprint_02.md`. | **Subsanado** ✅ | Se redactó formalmente `docs/diseño/G03_EPIS_Informe_Sprint_02.md` cumpliendo biunívocamente con las 11 secciones académicas de la cátedra. |

---

## 6. Fase VI — Perfiles de Usuario, Control de Acceso y Matriz RBAC / RLS

El sistema implementa una matriz formal de control de acceso basada en roles (**RBAC**) complementada con políticas de seguridad a nivel de fila (**RLS**) en Supabase PostgreSQL:

### Cuadro 6.1: Matriz de Control de Acceso RBAC y Operaciones del Sprint 02

| Operación / Recurso Técnico | Estudiante Mentoreado | Estudiante Postulante a Mentor | Estudiante Mentor Acreditado | Administrador Institucional | Política de Seguridad en PostgreSQL (RLS) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Emitir Consentimiento (Aceptar Ley 29733)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | `INSERT ON consentimientos_legales` con `email = auth.email()` |
| **Revocar Consentimiento (Bloqueo RN-02)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | `UPDATE ON consentimientos_legales` con `email = auth.email()` |
| **Explorar Catálogo Curricular (Temas silábicos)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | `SELECT ON asignaturas`, `temas_silabicos` (Público autenticado) |
| **Consultar Perfil Propio** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | `SELECT ON perfiles_academicos` (`email = auth.jwt() ->> 'email'`) |
| **Consultar Perfil de Tercero** | DENEGADO (NO)<br>*(HTTP 403)* | DENEGADO (NO)<br>*(HTTP 403)* | DENEGADO (NO)<br>*(HTTP 403)* | **PERMITIDO (SÍ)**<br>*(Auditoría académica)* | Bloqueado por RLS salvo que `auth.jwt() ->> 'role' = 'ADMIN'` |
| **Actualizar Matriz de Disponibilidad (6×11)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | **PERMITIDO (SÍ)** | `ALL ON disponibilidades_horarias` (`email = auth.email()`) |
| **Declarar Intención de Postulación a Mentor** | DENEGADO (NO) | **PERMITIDO (SÍ)**<br>*(Alerta si ciclo $< 7$)* | N/A (Ya acreditado) | N/A | `UPDATE ON perfiles_academicos` (`rol_postulacion = 'mentor'`) |
| **Autopromoverse a Mentor sin Aprobación** | DENEGADO (NO)<br>*(HTTP 403)* | DENEGADO (NO)<br>*(HTTP 403)* | N/A | N/A | Prohibido por endpoint `roles.py` y restricción de BD |
| **Promover a Mentor con Ciclo $\ge 7$ (RN-03)** | DENEGADO (NO) | DENEGADO (NO) | DENEGADO (NO) | **PERMITIDO (SÍ)**<br>*(Verificación mérito)* | `INSERT ON usuario_roles` (`asignado_por = auth.email()`) |
| **Promover a Mentor con Ciclo $< 7$** | **BLOQUEADO (NO)**<br>*(HTTP 400 RN-03)* | **BLOQUEADO (NO)**<br>*(HTTP 400 RN-03)* | **BLOQUEADO (NO)** | **BLOQUEADO (NO)**<br>*(Infracción RN-03)* | Interceptado por `RoleService.promote_to_mentor()` |
| **Revocar Privilegios de Mentoría** | DENEGADO (NO) | DENEGADO (NO) | DENEGADO (NO) | **PERMITIDO (SÍ)**<br>*(Acción motivada)* | `UPDATE ON usuario_roles` (`SET activo = False`) |

---

## 7. Conclusiones de la Auditoría y Dictamen Técnico

1. **Plena Validez Legal e Institucional:** La implementación del formulario interactivo `ConsentModalView.tsx` y la tabla `consentimientos_legales` satisface en un 100% los requerimientos de la **Ley N° 29733**, garantizando que el tratamiento de datos académicos sea expreso, informado y revocable (regla **RN-02**).
2. **Blindaje del Mérito Académico (RN-03):** La regla institucional que restringe la tutoría avanzada a estudiantes de ciclos formativos $\ge \text{VII}$ se encuentra sólidamente implementada bajo una estrategia de *Defensa en Profundidad* (alerta reactiva en el cliente, validación en `RoleService`, denegación de autopromoción y pruebas automatizadas deterministas).
3. **Consistencia Transaccional y de Seguridad (RNF02 / RNF07):** La matriz horaria semanal de 6×11 opera mediante transacciones ACID atómicas, y el acceso multiusuario está resguardado por tokens JWT HMAC-SHA256 y políticas de Row Level Security (RLS) en Supabase PostgreSQL.
4. **Dictamen de Aprobación:** Con una batería de 150 pruebas automatizadas superando el **90% de cobertura de código**, cero inconsistencias críticas abiertas y una trazabilidad biunívoca total hacia el SRS (FD03) y SAD (FD04), el incremento del **Sprint 02 se dictamina formalmente como APROBADO, VERIFICADO Y AUDITADO**.

---
*Documento de auditoría técnica emitido y versionado bajo los estándares de documentación del Sistema Web P2P EPIS-UPT (2026).*
