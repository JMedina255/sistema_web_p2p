# Matriz de Pruebas Oficiales Vinculadas al Catálogo de Casos de Prueba — Sprint 02

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Documento Fuente Oficial:** `docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`  
**Semestre Académico:** 2026-II — Cátedra de Construcción de Software I  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)  
**Commit de Integración del Sprint 02:** [`3766a08`](https://github.com/JMedina255/sistema_web_p2p/commit/3766a08fa98d49bc6107a9fd278568f289f7fe74) / [`786dd62`](https://github.com/JMedina255/sistema_web_p2p/commit/786dd621d024e2def6383e1d925ef36a3f8ea72f)  
**Resumen del Corte:** **150 pruebas automatizadas acumuladas** (84 backend en Pytest + 66 frontend en Vitest), **100% aprobadas (0 fallos)**. Cobertura: Backend **90.64%**, Frontend **91.10%** (superando el umbral de 70% de **RNF09**).

---

## 1. Mapeo Bidireccional entre el Catálogo Oficial Excel y Suites Automatizadas

El siguiente cuadro homologa formalmente cada caso de prueba del catálogo Excel `Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` con su implementación en el código de prueba de backend (`Pytest 9.1`) y frontend (`Vitest 2.1`):

### 1.1. Pruebas Asociadas a CUS01 — Consentimiento Legal y Acceso Seguro (PB-003, T-04, T-05)

| Id Caso (Excel) | Nombre del Caso de Prueba | Tipo / Nivel | Criterio de Aceptación / Comportamiento Esperado | Suite Automatizada / Función de Prueba | Naturaleza (Positiva / Negativa) | Estado |
| :---: | :--- | :---: | :--- | :--- | :---: | :---: |
| **CUS01-U01** | Validar dominio institucional `@upt.pe` | Unitaria / Componente | Rechazar dominios externos (`gmail.com`, `yahoo.es`) y admitir variantes válidas `@upt.pe`. | Backend: `test_auth.py::test_domain_validation`<br>Frontend: `authService.test.ts` | Positiva & Negativa | ✅ Aprobada |
| **CUS01-U02** | Generar y expirar OTP de 6 dígitos en 5 min | Unitaria / Componente | Longitud exacta de 6 caracteres numéricos, un solo uso y expiración en 300 s. | Backend: `test_auth.py::test_otp_generation_and_expiry` | Positiva & Negativa | ✅ Aprobada |
| **CUS01-U03** | Bloquear sesión si se rechaza consentimiento (Ley 29733) | Unitaria / Componente | Si `accepted = false`, el sistema niega emisión de token de sesión y retorna estado de bloqueo. | Backend: `test_consent.py::test_evaluate_consent_denial`<br>Frontend: `ConsentModalView.test.tsx::test_reject_button_blocks` | **Negativa Crítica** | ✅ Aprobada |
| **CUS01-U04** | Emitir JWT firmado con expiración de 8 h y persistir marca | Unitaria / Componente | Firma criptográfica válida con claims de usuario y registro de timestamp UTC inmutable en `consentimientos_legales`. | Backend: `test_consent.py::test_accept_consent_records_utc_timestamp` | Positiva | ✅ Aprobada |
| **CUS01-F01** | Flujo integral: primer login con consentimiento y 2FA | Funcional / Sistema | Estudiante nuevo ingresa correo `@upt.pe`, visualiza modal legal, acepta términos y accede al sistema con credenciales válidas. | Frontend: `ConsentModalView.test.tsx::test_full_accept_flow`<br>Backend: `test_consent.py::test_full_consent_workflow` | Positiva | ✅ Aprobada |
| **CUS01-F02** | Flujo de rechazo voluntario de consentimiento | Funcional / Sistema | Estudiante declina expresamente el tratamiento de datos personales. El sistema cierra sesión e impide navegación. | Frontend: `ConsentModalView.test.tsx::test_reject_triggers_exit`<br>Backend: `test_consent.py::test_consent_rejection_session_closure` | **Negativa Crítica** | ✅ Aprobada |
| **CUS01-A01** | Aceptación: cumplimiento Ley N° 29733 y seguridad gatekeeper | Aceptación / Sistema | Conexiones bajo TLS 1.3, registro de IP y User-Agent de auditoría, ningún dato sensible expuesto en logs de aplicación. | Backend: `test_consent.py::test_audit_metadata_persistence`<br>`test_authorization.py::test_gatekeeper_enforcement` | Seguridad / Auditoría | ✅ Aprobada |

---

### 1.2. Pruebas Asociadas a CUS10 — Gestión de Roles y Verificación de Mérito Académico (PB-005, T-08)

| Id Caso (Excel) | Nombre del Caso de Prueba | Tipo / Nivel | Criterio de Aceptación / Comportamiento Esperado | Suite Automatizada / Función de Prueba | Naturaleza (Positiva / Negativa) | Estado |
| :---: | :--- | :---: | :--- | :--- | :---: | :---: |
| **CUS10-U01** | Asignar rol Mentoreado por defecto | Unitaria / Componente | Todo estudiante nuevo recibe automáticamente el rol base de Mentoreado (`rol_id = 1`). | Backend: `test_roles.py::test_default_role_assignment` | Positiva | ✅ Aprobada |
| **CUS10-U02** | Validar mérito académico antes de promover a Mentor (RN-03) | Unitaria / Componente | Si `ciclo_actual < 7`, la asignación de mentor es rechazada terminantemente con **HTTP 400 Bad Request** y código `MERIT_RULE_VIOLATION`. | Backend: `test_roles.py::test_merit_violation_rejection_cycle_under_7`<br>Frontend: `ProfileAvailabilityView.test.tsx::test_merit_alert` | **Negativa Crítica (RN-03)** | ✅ Aprobada |
| **CUS10-U03** | Restringir elevación de rol solo al Administrador | Unitaria / Seguridad | Un estudiante no puede autopromoverse a mentor sin privilegios institucionales; la API devuelve **HTTP 403 Forbidden**. | Backend: `test_roles.py::test_self_promotion_denied_http_403`<br>`test_authorization.py::test_forbidden_self_promotion` | **Seguridad / Negativa** | ✅ Aprobada |
| **CUS10-F01** | Flujo de postulación y promoción institucional de mentor | Funcional / Sistema | Administrador o proceso institucional evalúa estudiante con ciclo $\ge \text{VII}$ y aprueba su rol como Mentor exitosamente. | Backend: `test_roles.py::test_admin_promotes_eligible_student` | Positiva | ✅ Aprobada |
| **CUS10-A01** | Aceptación: auditoría de roles y consistencia relacional | Aceptación / Integración | Integridad referencial en tabla `usuario_roles`, prevención de duplicidad de asignaciones y registro de fecha de otorgamiento. | Backend: `test_roles.py::test_user_roles_referential_integrity` | Integración / BD | ✅ Aprobada |

---

### 1.3. Pruebas Asociadas a CUS15 — Perfil Formativo y Matriz Semanal de Disponibilidad (PB-007, T-11, T-12)

| Id Caso (Excel) | Nombre del Caso de Prueba | Tipo / Nivel | Criterio de Aceptación / Comportamiento Esperado | Suite Automatizada / Función de Prueba | Naturaleza (Positiva / Negativa) | Estado |
| :---: | :--- | :---: | :--- | :--- | :---: | :---: |
| **CUS15-U01** | Guardar franjas horarias libres en matriz semanal 6×11 | Unitaria / Componente | Almacenar bloques semanales (días 1 a 6, horas entre 08:00 y 19:00) asociados al perfil del estudiante. | Backend: `test_profiles.py::test_save_weekly_availability_slots`<br>Frontend: `profileService.test.ts::test_save_availability` | Positiva | ✅ Aprobada |
| **CUS15-U02** | Validar orden temporal estricto (`hora_inicio < hora_fin`) | Unitaria / Componente | Si `hora_inicio >= hora_fin`, o día fuera de rango $[1..6]$, el backend rechaza la petición con **HTTP 400 Bad Request**. | Backend: `test_profiles.py::test_invalid_hour_order_rejected`<br>`test_profiles.py::test_invalid_day_range_rejected` | **Negativa** | ✅ Aprobada |
| **CUS15-F01** | Reemplazo atómico transaccional de matriz horaria semanal | Funcional / Integración | Al actualizar horarios, el sistema ejecuta un `DELETE` previo de las franjas existentes y un `INSERT` masivo atómico en una única transacción. | Backend: `test_profiles.py::test_atomic_schedule_replacement`<br>Frontend: `ProfileAvailabilityView.test.tsx::test_grid_interaction` | Transaccional ACID | ✅ Aprobada |
| **CUS15-A01** | Aceptación: consistencia de perfil y aislamiento multiusuario | Aceptación / Seguridad | Un usuario no puede leer ni modificar la matriz horaria o datos privados de otro estudiante; denegación estricta por RLS y JWT. | Backend: `test_authorization.py::test_cross_user_profile_isolation`<br>`test_profiles.py::test_profile_persistence_consistency` | Seguridad / RLS | ✅ Aprobada |

---

### 1.4. Pruebas Asociadas a CUS21 — Consulta Avanzada del Catálogo Curricular (PB-006, T-10)

| Id Caso (Excel) | Nombre del Caso de Prueba | Tipo / Nivel | Criterio de Aceptación / Comportamiento Esperado | Suite Automatizada / Función de Prueba | Naturaleza (Positiva / Negativa) | Estado |
| :---: | :--- | :---: | :--- | :--- | :---: | :---: |
| **CUS21-U01** | Consultar asignaturas filtro y temarios silábicos | Unitaria / Componente | Carga estructurada de asignaturas formativas con código, créditos, ciclo lectivo y lista de unidades temáticas. | Backend: `test_curriculum.py::test_get_subjects_and_topics`<br>Frontend: `CurriculumCatalogView.test.tsx::test_render_catalog` | Positiva | ✅ Aprobada |
| **CUS21-U02** | Búsqueda predictiva reactiva y filtrado facetado por ciclo | Unitaria / Componente | Al escribir en el buscador o seleccionar un ciclo (I al X), la lista se filtra instantáneamente sin llamadas redundantes al servidor. | Frontend: `CurriculumCatalogView.test.tsx::test_search_by_text_and_cycle` | Rendimiento / UI | ✅ Aprobada |
| **CUS21-F01** | Navegación temática silábica profunda | Funcional / Sistema | Expansión interactiva de una asignatura mostrando el desglose silábico de competencias conceptuales que consumirá el recomendador. | Frontend: `CurriculumCatalogView.test.tsx::test_expand_syllabus_topics` | Positiva | ✅ Aprobada |
| **CUS21-A01** | Aceptación: integridad del catálogo oficial y latencia subsegundo | Aceptación / Rendimiento | Catálogo oficial sincronizado con Plan de Estudios EPIS-UPT; tiempo de respuesta medio en backend inferior a 50 ms. | Backend: `test_curriculum.py::test_curriculum_response_time` | Rendimiento (**RNF03**) | ✅ Aprobada |

---

## 2. Clasificación de Pruebas Automatizadas por Tipo y Nivel

Al corte del Sprint 02 se registraron **150 pruebas automatizadas**:

```text
                               TOTAL: 150 PRUEBAS AUTOMATIZADAS
                 ┌─────────────────────────────┴─────────────────────────────┐
                 │                                                           │
        BACKEND (Pytest 9.1)                                        FRONTEND (Vitest 2.1)
          84 pruebas (100% OK)                                        66 pruebas (100% OK)
          Cobertura: 90.64%                                           Cobertura: 91.10%
     ┌───────────┴───────────┐                                   ┌───────────┴───────────┐
     │                       │                                   │                       │
Unitarias / Modelos     Integración / Seguridad             Unitarias / Servicios    Componentes UI / Integración
(46 pruebas)            (38 pruebas)                        (28 pruebas)             (38 pruebas)
- test_consent (8)      - test_consent (6)                  - consentService (5)     - ConsentModalView (4)
- test_roles (6)        - test_roles (6)                    - profileService (6)     - CurriculumCatalogView (6)
- test_profiles (14)    - test_profiles (8)                 - authService (17)       - ProfileAvailabilityView (6)
- test_auth (10)        - test_authorization (11)                                    - LoginOtpView / App (22)
- test_curriculum (5)   - test_health (3)
- test_health (3)       - test_curriculum (4)
```

### Resumen de Pruebas Positivas vs. Negativas
- **Pruebas Positivas (Happy Path):** 112 pruebas (74.7%) validando flujos de aceptación regular, persistencia correcta, emisión de tokens y cálculo de disponibilidades.
- **Pruebas Negativas y de Seguridad (Unhappy Path):** 38 pruebas (25.3%) validando rechazo deliberado de consentimiento, bloqueo de ciclo $< 7$ con **HTTP 400**, denegación de autopromoción con **HTTP 403**, tokens expirados, desbordamiento de franjas horarias y aislamiento de datos de terceros.
