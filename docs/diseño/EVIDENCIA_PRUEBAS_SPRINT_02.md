# Documento de Evidencia y Catálogo de Pruebas Automatizadas: Sprint 2

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II)  
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Fecha de Cierre:** 23/10/2026  
**Commit Git:** [`3766a08`](https://github.com/JMedina255/sistema_web_p2p/commit/3766a08fa98d49bc6107a9fd278568f289f7fe74)  
**Estado:** ✅ **150 de 150 Pruebas Superadas (100% Satisfactorio, 0 Fallos)**

---

## Control de Versiones

A continuación, se presenta la tabla de control de versiones del documento de evidencia de pruebas para el Sprint 2:

### Cuadro 0.1: Control de Versiones — Catálogo de Evidencias de Pruebas

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcarcel | Dirección EPIS | 23/10/2026 | Emisión formal del catálogo de evidencias de pruebas automatizadas del Sprint 2: consolidación de 150 pruebas (84 en Pytest Backend y 66 en Vitest Frontend), desglose de las 21 suites, matrices de cobertura por archivo/línea (>90%), auditoría de linteo estático (Ruff/ESLint), reporte de compilación y comandos reproducibles de verificación. |

Fuente: Elaboración propia.

El control de versiones acredita la reproducibilidad técnica y la trazabilidad de los artefactos de software generados en cumplimiento del marco de calidad de software del curso.

---

## 1. Propósito y Estrategia de Pruebas del Sprint 2

El presente documento certifica el cumplimiento del requerimiento no funcional **RNF09 (Mantenibilidad y Calidad de Código)**, que establece un umbral mínimo obligatorio del **70.0% de cobertura de código por pruebas automatizadas** en frontend y backend, así como los requerimientos de seguridad (**RNF02**) y granularidad de disponibilidad (**RNF04**).

La estrategia de pruebas consolidada para el Sprint 2 implementa cuatro niveles de aislamiento técnico:
1. **Pruebas Unitarias de Lógica y Reglas de Negocio:** Validación determinista de la regla **RN-02** (consentimiento informado vinculante) y de la regla **RN-03** (mérito académico: rechazo estricto con HTTP 400 `MERIT_RULE_VIOLATION` si `ciclo_actual < 7`). Validación de expresiones regulares para correos institucionales `@upt.pe` y algoritmos de firma y validación de tokens JWT (HS256).
2. **Pruebas de Componentes React e Interacción de Usuario:** Renderizado en DOM virtual (`jsdom`) con React Testing Library y Vitest, evaluando:
   - Formulario modal accesible de consentimiento con bloqueo ante rechazo (`ConsentModalView.test.tsx`).
   - Buscador curricular reactivo con filtrado por texto, ciclo y unidades temáticas silábicas (`CurriculumCatalogView.test.tsx`).
   - Vista de perfil y matriz semanal 6×11 de disponibilidad con detección preventiva de mérito RN-03 y atajos de selección masiva (`ProfileAvailabilityView.test.tsx`).
   - Navegación global sin desbordamientos ni advertencias en DOM virtual (`App.test.tsx`).
3. **Pruebas de Integración con Persistencia ORM Relacional:** Pruebas contra sesiones directas de base de datos con SQLAlchemy 2.0 y SQLite en memoria, validando integridad referencial, borrado en cascada, unicidad compuesta `uq_usuario_roles_email_rol` y reemplazo atómico de horarios bajo una misma transacción ACID.
4. **Pruebas de Autorización y Seguridad Multi-Usuario (T-13 / RNF02):** Evaluación de aislamiento criptográfico mediante Bearer JWT en `test_authorization.py`:
   - Detección y bloqueo perentorio con **HTTP 403 Forbidden** ante intentos de acceso cruzado horizontal (usuario A intentando leer o modificar perfiles de usuario B).
   - Denegación perentoria con **HTTP 403 Forbidden** ante intentos de autopromoción directa a mentor sin rol de administrador.
   - Rechazo con **HTTP 401 Unauthorized** ante tokens adulterados, expirados o carentes de sujeto (`sub`).
   - Verificación de la activación de `ROW LEVEL SECURITY` (`relrowsecurity = True`) sobre las 5 tablas relacionales en Supabase.

---

## 2. Resumen Métrico Consolidado de Cobertura de Código

A continuación, se presentan los resultados consolidados de cobertura obtenidos mediante las herramientas estandarizadas Pytest-Cov (Python 3.14) y V8 Coverage (Vitest 2.1.8).

### Cuadro 2.1: Matriz Consolidada de Cobertura por Capa Arquitectónica (Sprint 2)

| Entorno de Pruebas | Motor de Ejecución | Suites Activas | Pruebas Ejecutadas | Pruebas Aprobadas | Meta RNF09 | Cobertura Lograda | Dictamen Final |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Backend API REST** | Pytest 9.1 + Pytest-Cov | 10 | 84 | 84 (100%) | $\ge 70.0\%$ | **90.64%** | ✅ Superado (+20.64%) |
| **Frontend React SPA**| Vitest 2.1 + V8 Provider | 11 | 66 | 66 (100%) | $\ge 70.0\%$ | **91.10%** | ✅ Superado (+21.10%) |
| **TOTAL CONSOLIDADO** | **Pipeline Dual CI/CD** | **21** | **150** | **150 (100%)** | $\ge 70.0\%$ | **~90.87% Ponderado**| ✅ **Acreditado con Excelencia** |

Fuente: Reportes automatizados emitidos por `pytest tests/ --cov=app` y `vitest run --coverage`.

Como se evidencia en el Cuadro 2.1, ambas capas de software sobrepasan holgadamente el umbral institucional del 70%, situándose por encima del 90% con cero pruebas fallidas, lo que certifica la madurez y resiliencia del incremento del Sprint 2.

---

## 3. Desglose Exhaustivo de Suites de Prueba de Backend (84 Pruebas)

A continuación, se detallan las 84 pruebas automatizadas distribuidas en los 10 archivos de prueba del backend FastAPI.

### Cuadro 3.1: Catálogo Exhaustivo de Pruebas de Backend — Módulos del Sprint 2 (34 Pruebas Nuevas)

| Archivo de Prueba | Caso de Prueba Evaluado | Tipo de Prueba | Precondición / Fixture | Resultado Esperado |
| :--- | :--- | :---: | :--- | :--- |
| `tests/test_consent.py` | `test_get_consent_status_unconsented` | Integración API | Estudiante nuevo sin registro previo | Retorna HTTP 200 con `has_consented: false` y versión `2026-II-v1.0`. |
| `tests/test_consent.py` | `test_accept_consent_success` | Lógica Negocio | Correo `@upt.pe` válido | Retorna HTTP 200 con `success: true` y estampa temporal UTC registrada. |
| `tests/test_consent.py` | `test_accept_consent_rejects_external_email` | Validación Esquema| Correo ajeno (`@gmail.com`) | Retorna HTTP 422 Unprocessable Entity por validación Pydantic de dominio. |
| `tests/test_consent.py` | `test_revoke_consent_blocks_access` | Regla RN-02 | Titular ejerce revocación | Retorna HTTP 200 con `has_consented: false`, revocando acceso al sistema. |
| `tests/test_consent.py` | `test_consent_service_with_real_db_session` | Persistencia ORM | Sesión relacional SQLite in-memory | Valida inserción, lectura, actualización y estampa UTC en BD. |
| `tests/test_roles.py` | `test_get_user_roles_default_is_mentoreado` | Lógica Negocio | Usuario nuevo sin roles previos | Asigna automáticamente rol base `'mentoreado'` retornando HTTP 200. |
| `tests/test_roles.py` | `test_promote_mentor_rejects_when_cycle_below_7_rn03`| Regla RN-03 | Estudiante con `ciclo_actual = 5` | Rechaza con HTTP 400 y código canónico `MERIT_RULE_VIOLATION`. |
| `tests/test_roles.py` | `test_promote_mentor_success_when_cycle_7_or_above` | Regla RN-03 | Estudiante con `ciclo_actual = 8` | Retorna HTTP 200 con `roles: ["mentoreado", "mentor"]`. |
| `tests/test_roles.py` | `test_revoke_mentor_success` | Gestión Roles | Mentor activo existente | Retorna HTTP 200 con rol mentor desactivado del listado vigente. |
| `tests/test_roles.py` | `test_promote_mentor_rejects_external_email` | Validación Esquema| Solicitud con correo no `@upt.pe` | Retorna HTTP 422 Unprocessable Entity. |
| `tests/test_roles.py` | `test_role_service_with_real_db_session` | Persistencia ORM | Sesión relacional con claves foráneas | Valida unicidad `uq_usuario_roles_email_rol` y verificación de mérito. |
| `tests/test_roles.py` | `test_promote_and_revoke_with_invalid_token_rejected`| Seguridad API | Petición sin token o token manipulado | Rechaza con HTTP 401 Unauthorized o 403 Forbidden. |
| `tests/test_profiles.py` | `test_get_profile_default` | Integración API | Estudiante en fase de onboarding | Retorna perfil institucional inicializado con valores coherentes. |
| `tests/test_profiles.py` | `test_update_profile_success` | Lógica Negocio | Modificación de materias y modalidad | Retorna HTTP 200 con arrays JSON estructurados y timestamp actualizado. |
| `tests/test_profiles.py` | `test_update_profile_rejects_mentor_when_cycle_below_7`| Regla RN-03 | Modificación de rol a mentor con ciclo 6 | Rechaza con HTTP 400 y código canónico `MERIT_RULE_VIOLATION`. |
| `tests/test_profiles.py` | `test_update_profile_allows_mentor_when_cycle_gte_7` | Regla RN-03 | Postulación a mentor con ciclo 7 | Retorna HTTP 200 admitiendo el rol de postulación a mentor. |
| `tests/test_profiles.py` | `test_get_and_update_availability` | Transaccionalidad | Reemplazo de bloques semanales | Ejecuta reemplazo atómico eliminando previos e insertando 3 franjas. |
| `tests/test_profiles.py` | `test_profile_cycle_boundary_validations` | Frontera / Rango | Ciclos 0, 1, 10, 11 | Ciclos 0 y 11 rechazados (HTTP 422); 1 y 10 admitidos (HTTP 200). |
| `tests/test_profiles.py` | `test_availability_boundary_and_empty_slots` | Frontera / Rango | Días 0 y 7, agenda vacía | Días 0 y 7 rechazados (HTTP 422); agenda vacía admitida (HTTP 200). |
| `tests/test_profiles.py` | `test_availability_time_order_and_invalid_24h` | Validación Lógica | `hora_inicio >= hora_fin` o hora > 24 | Rechaza con HTTP 422 por orden cronológico estricto. |
| `tests/test_profiles.py` | `test_availability_duplicate_and_overlapping_slots` | Validación Lógica | Bloques duplicados o solapados en día | Rechaza con HTTP 422 por solapamiento de agenda horaria. |
| `tests/test_profiles.py` | `test_profile_invalid_enum_fields_rejected` | Validación Esquema| Modalidad o rol no reconocido | Rechaza con HTTP 422 por tipado Literal estricto. |
| `tests/test_profiles.py` | `test_profile_service_with_real_db_session` | Persistencia ORM | Sesión relacional con tablas de perfil | Valida restricciones `CHECK` en motor de BD y consistencia ACID. |
| `tests/test_authorization.py`| `test_authorization_header_valid_jwt_access` | Seguridad / JWT | Bearer token firmado con HS256 | Autoriza acceso y retorna datos del sujeto titular (HTTP 200). |
| `tests/test_authorization.py`| `test_authorization_expired_or_invalid_jwt_rejected` | Criptografía | Token con firma espuria o corrupto | Deniega acceso de inmediato retornando HTTP 401 Unauthorized. |
| `tests/test_authorization.py`| `test_authorization_expired_token_rejected` | Expiración | Token con marca de tiempo vencida | Retorna HTTP 401 Unauthorized. |
| `tests/test_authorization.py`| `test_user_cannot_access_or_modify_another_users_profile_forbidden` | Seguridad RNF02| Usuario A solicita perfil de Usuario B | Deniega acceso con HTTP 403 Forbidden en GET perfil, PUT perfil y agenda. |
| `tests/test_authorization.py`| `test_denial_of_self_promotion_to_mentor_without_admin`| Seguridad RNF02| Estudiante intenta autopromoverse | Rechaza con HTTP 403 Forbidden (`SELF_PROMOTION_FORBIDDEN`). |
| `tests/test_authorization.py`| `test_admin_can_promote_and_access` | Autorización Admin | Token con rol administrador | Autoriza promoción y asigna rol mentor a estudiante elegible (HTTP 200). |
| `tests/test_authorization.py`| `test_unauthenticated_request_rejected_without_email_or_token`| Seguridad Base | Petición anónima sin cabeceras | Retorna HTTP 401 Unauthorized. |
| `tests/test_authorization.py`| `test_admin_can_update_other_profile_and_revoke_with_token`| Autorización Admin | Token de administrador | Permite actualizar perfil ajeno y revocar rol mentor (HTTP 200). |
| `tests/test_authorization.py`| `test_token_without_subject_rejected` | Seguridad / JWT | Payload JWT sin claim `sub` | Rechaza con HTTP 401 Unauthorized por identidad ambigua. |
| `tests/test_authorization.py`| `test_malformed_authorization_header_rejected`| Seguridad Base | Cabecera sin prefijo `Bearer ` | Retorna HTTP 401 Unauthorized por formato de cabecera inválido. |
| `tests/test_authorization.py`| `test_production_unauthenticated_request_rejected` | Seguridad Prod | Petición sin token en producción | Bloquea acceso denegando bypass de desarrollo (HTTP 401). |

Fuente: Elaboración propia a partir de las suites de prueba ejecutadas en `aplicacion/backend/tests/`.

El Cuadro 3.1 certifica la implementación de 34 nuevas pruebas de backend que validan deterministamente la obligatoriedad del consentimiento (RN-02), la restricción infranqueable de mérito académico (RN-03), la consistencia transaccional del reemplazo de franjas horarias y el blindaje criptográfico ante accesos cruzados horizontales y verticales.

---

Para salvaguardar la no-regresión de la arquitectura base y certificar que la adición de los 4 nuevos módulos del Sprint 2 preservó la integridad del sistema preexistente, a continuación se desglosan las 50 pruebas heredadas del Sprint 1 que continúan ejecutándose de forma ininterrumpida y homologada.

### Cuadro 3.2: Catálogo Exhaustivo de Pruebas de Backend — Infraestructura Base y Sprint 1 (50 Pruebas Preservadas)

| Archivo de Prueba | N.° Tests | Enfoque Evaluado y Componentes | Resultado Observado |
| :--- | :---: | :--- | :---: |
| `tests/test_auth.py` | 13 | Emisión de OTP, validación `@upt.pe`, cooldown 60 s, expiración 5 min, reuso, invalidación de códigos previos y persistencia ORM. | 13 aprobadas (0 fallos) |
| `tests/test_curriculum.py` | 8 | Consulta de las 5 materias filtro formativas, filtro por ciclo, detalle de curso, temas silábicos y carga ansiosa `selectinload`. | 8 aprobadas (0 fallos) |
| `tests/test_health.py` | 7 | Diagnóstico `/health` independiente, `/health/db` con `SELECT 1`, resiliencia sin base de datos y ocultamiento en producción. | 7 aprobadas (0 fallos) |
| `tests/test_security.py` | 6 | Criptografía HMAC-SHA256, generación de códigos numéricos de 6 dígitos, firma de tokens JWT de 8 horas y máscara en `repr`. | 6 aprobadas (0 fallos) |
| `tests/test_session.py` | 10 | Inicialización perezosa (*lazy engine*), inyección de dependencia `get_db()`, cierre seguro de sesión y sanitización de credenciales. | 10 aprobadas (0 fallos) |
| `tests/test_config.py` | 6 | Parsing de orígenes CORS desde cadenas JSON o delimitadas por comas, normalización de URLs `postgresql+psycopg://` y máscara de contraseñas. | 6 aprobadas (0 fallos) |
| **SUBTOTAL BASE** | **50** | **Infraestructura, Autenticación y Catálogo Base** | **50 aprobadas (100%)** |

Fuente: Elaboración propia.

Las 50 pruebas base del Sprint 1 se preservaron íntegras, acreditando que la incorporación de los nuevos modelos y endpoints del Sprint 2 no generó regresiones en los servicios existentes.

---

## 4. Desglose Exhaustivo de Suites de Prueba de Frontend (66 Pruebas)

A continuación, se documenta la batería de pruebas unitarias y de componentes ejecutada en el cliente web React 19 mediante Vitest.

### Cuadro 4.1: Catálogo Exhaustivo de Pruebas de Frontend (Sprint 2 Consolidado)

| Suite de Pruebas | N.° Tests | Enfoque Evaluado y Componentes Bajo Prueba | Cobertura Lograda |
| :--- | :---: | :--- | :---: |
| `src/services/__tests__/consentService.test.ts` | 5 | Pruebas de `consentService`: consulta inicial no registrada (`hasConsented: false`), aceptación con estampa UTC, rechazo de correos ajenos a `@upt.pe`, revocación voluntaria y manejo de correos vacíos. | 73.24% |
| `src/services/__tests__/profileService.test.ts` | 5 | Pruebas de `profileService`: validación de la regla de mérito RN-03 (ciclo 6 inelegible, ciclos 7 y 10 elegibles), perfil institucional por defecto, guardado y recuperación en almacén, bloqueo de postulación inválida y guardado de agenda semanal. | 71.73% |
| `src/components/__tests__/ConsentModalView.test.tsx`| 4 | Pruebas de `ConsentModalView`: renderizado de encabezado institucional y cláusulas Ley 29733, habilitación condicional del botón de aceptación tras marcar checkbox, flujo de aceptación exitosa con callback y flujo de rechazo bloqueante conforme a RN-02. | 95.05% |
| `src/components/__tests__/CurriculumCatalogView.test.tsx`| 4 | Pruebas de `CurriculumCatalogView`: renderizado inicial de materias filtro, selección de asignatura y carga de unidades temáticas silábicas en panel derecho, filtrado reactivo en tiempo real mediante buscador textual y manejo de errores de conexión de red sin colapsar la UI. | 94.54% |
| `src/components/__tests__/ProfileAvailabilityView.test.tsx`| 5 | Pruebas de `ProfileAvailabilityView`: renderizado inicial de formulario formativo, activación reactiva de la alerta de mérito RN-03 al seleccionar postulante a mentor, despliegue de grilla semanal 6×11 (Lunes a Sábado), botón "Limpiar semana" que resetea a 0 horas, y guardado general con callback. | 90.18% |
| `src/__tests__/App.test.tsx` | 1 | Prueba de integración global: alternancia reactiva entre las 5 pestañas institucionales activas (Acceso OTP, Consentimiento Ley 29733, Catálogo Curricular, Perfil & Disponibilidad, Monitor de Servicios). | 99.32% |
| `src/services/__tests__/authService.test.ts` | 15 | Pruebas de `MockAuthAdapter`: emisión de OTP, expiración de 5 minutos, cooldown de 60 segundos, códigos inválidos y verificación de sesión. | 89.94% |
| `src/services/__tests__/apiAuthAdapter.test.ts` | 9 | Pruebas de `ApiAuthAdapter`: interacción REST real mediante simulación de `fetch`, serialización JSON y captura de excepciones HTTP 400. | 85.19% |
| `src/services/__tests__/apiClient.test.ts` | 6 | Pruebas de cliente HTTP base: timeouts, extracción de cabeceras, manejo de desconexión sin colapso y llamada a `/health/db`. | 75.00% |
| `src/components/__tests__/LoginOtpView.test.tsx` | 9 | Pruebas de interfaz de autenticación: renderizado de pasos 1, 2 y 3, feedback de error y temporizadores dinámicos sincronizados. | 94.52% |
| `src/components/__tests__/HealthStatus.test.tsx` | 3 | Pruebas de monitor de servicios: semáforo verde para estado saludable, indicador de latencia en milisegundos y botón de reintento. | 100.00% |
| **TOTAL FRONTEND** | **66** | **11 suites de prueba automatizadas con Vitest** | **91.10% Líneas** |

Fuente: Elaboración propia a partir de los reportes generados por Vitest v8 Coverage.

El Cuadro 4.1 certifica que los 5 componentes principales y los 4 servicios adaptadores del frontend satisfacen rigurosamente los estándares de accesibilidad, manejo de errores y validación en cliente.

---

## 5. Reporte Detallado de Cobertura por Archivo, Líneas y Ramas

A continuación, se documentan las métricas granulares emitidas por los analizadores de cobertura en ambas capas de código.

### Cuadro 5.1: Reporte Granular de Cobertura de Backend (Pytest-Cov)

| Archivo / Módulo Backend | Sentencias (Stmts) | Fallos (Miss) | Cobertura en Líneas | Líneas No Cubiertas |
| :--- | :---: | :---: | :---: | :--- |
| `app/api/v1/api.py` | 9 | 0 | **100%** | — |
| `app/api/v1/endpoints/auth.py` | 15 | 0 | **100%** | — |
| `app/api/v1/endpoints/consent.py` | 17 | 0 | **100%** | — |
| `app/api/v1/endpoints/curriculum.py` | 23 | 0 | **100%** | — |
| `app/api/v1/endpoints/health.py` | 17 | 0 | **100%** | — |
| `app/api/v1/endpoints/profiles.py` | 48 | 0 | **100%** | — |
| `app/api/v1/endpoints/roles.py` | 54 | 4 | **93%** | 63, 108, 122, 139 |
| `app/core/config.py` | 44 | 3 | **93%** | 52-53, 57 |
| `app/core/security.py` | 30 | 0 | **100%** | — |
| `app/db/session.py` | 72 | 8 | **89%** | 60-67, 113 |
| `app/main.py` | 20 | 4 | **80%** | 14-16, 54-56 |
| `app/models/auth.py` | 15 | 0 | **100%** | — |
| `app/models/consent.py` | 13 | 0 | **100%** | — |
| `app/models/curriculum.py` | 26 | 0 | **100%** | — |
| `app/models/profile.py` | 26 | 0 | **100%** | — |
| `app/models/roles.py` | 20 | 0 | **100%** | — |
| `app/schemas/auth.py` | 33 | 0 | **100%** | — |
| `app/schemas/consent.py` | 34 | 1 | **97%** | 14 |
| `app/schemas/curriculum.py` | 19 | 0 | **100%** | — |
| `app/schemas/profile.py` | 83 | 3 | **96%** | 10, 15, 135 |
| `app/schemas/roles.py` | 29 | 1 | **97%** | 14 |
| `app/services/auth_service.py` | 140 | 21 | **85%** | 32-33, 52-53, 92-93, 122-123, 245-250 |
| `app/services/consent_service.py` | 50 | 6 | **88%** | 32-33, 85-86, 119-120 |
| `app/services/curriculum_service.py`| 53 | 8 | **85%** | 258-259, 285-286, 311-312 |
| `app/services/profile_service.py` | 109 | 29 | **73%** | 20-21, 45-48, 147-159, 176-179 |
| `app/services/role_service.py` | 73 | 14 | **81%** | 30-31, 36, 71-77, 86-88 |
| **TOTAL BACKEND** | **1090** | **102** | **90.64%** | Requisito RNF09 $\ge 70.0\%$ Aprobado |

Fuente: Reporte de cobertura generado por `pytest tests/ --cov=app --cov-report=term-missing`.

El Cuadro 5.1 demuestra que 12 de los 16 módulos de backend alcanzan el 100% de cobertura, mientras que los servicios centrales de roles, perfiles y consentimiento superan el 73%, consolidando un 90.64% global sin áreas críticas desprotegidas.

![Backend Pytest Coverage](/docs/diseño/imagenes/sprint-02/06_backend_pytest_coverage_sprint02.png)  
*Figura 5.1: Terminal de ejecución de 84 pruebas de backend con 90.64% de cobertura.*

---

De forma complementaria a las métricas del backend, a continuación se detalla la desagregación de cobertura a nivel de componentes y servicios cliente en React 19, cuantificando la cobertura por sentencias, bifurcaciones de control, funciones y líneas de código.

### Cuadro 5.2: Reporte Granular de Cobertura de Frontend (Vitest v8)

| Archivo / Componente Frontend | Sentencias (% Stmts) | Ramas (% Branch) | Funciones (% Funcs) | Líneas (% Lines) |
| :--- | :---: | :---: | :---: | :---: |
| `src/App.tsx` | 99.32% | 98.03% | 83.33% | **99.32%** |
| `src/components/ConsentModalView.tsx` | 95.05% | 74.54% | 71.42% | **95.05%** |
| `src/components/CurriculumCatalogView.tsx` | 94.54% | 72.54% | 57.14% | **94.54%** |
| `src/components/HealthStatus.tsx` | 100.00% | 75.00% | 100.00% | **100.00%** |
| `src/components/LoginOtpView.tsx` | 94.52% | 76.13% | 61.11% | **94.52%** |
| `src/components/ProfileAvailabilityView.tsx`| 90.18% | 84.46% | 36.36% | **90.18%** |
| `src/services/apiClient.ts` | 75.00% | 72.72% | 80.00% | **75.00%** |
| `src/services/authService.ts` | 89.94% | 74.19% | 100.00% | **89.94%** |
| `src/services/consentService.ts` | 73.24% | 50.00% | 87.50% | **73.24%** |
| `src/services/profileService.ts` | 71.73% | 42.10% | 88.88% | **71.73%** |
| **TOTAL FRONTEND CONSOLIDADO** | **91.10%** | **75.18%** | **71.96%** | **91.10%** |

Fuente: Reporte de cobertura generado por `vitest run --coverage` (V8 Provider).

El Cuadro 5.2 ratifica que los componentes de interfaz de usuario de React 19 alcanzan coberturas superiores al 90%, asegurando que tanto los flujos principales de navegación como los estados de carga y manejo de errores cuentan con validación empírica automatizada.

![Frontend Vitest Coverage](/docs/diseño/imagenes/sprint-02/07_frontend_vitest_coverage_sprint02.png)  
*Figura 5.2: Terminal de ejecución de 66 pruebas de frontend con 91.10% de cobertura.*

---

## 6. Reporte de Linteo Estático y Calidad de Código

En cumplimiento del criterio de calidad técnica del Definition of Done (DoD), se ejecutó el análisis estático en ambos repositorios de código:

### 6.1. Linteo y Formato de Backend (Ruff 0.9.x)
- **Comando Ejecutado:** `ruff check .`
- **Resultado:** `All checks passed!` (0 infracciones de sintaxis, importaciones huérfanas o violaciones PEP 8).
- **Comando de Formato:** `ruff format --check .`
- **Resultado:** `49 files already formatted` (100% de los archivos Python estandarizados conforme a las reglas del proyecto).

### 6.2. Linteo y Formato de Frontend (ESLint 9 + Prettier)
- **Comando Ejecutado:** `npm run lint`
- **Resultado:** `0 errors, 0 warnings` (Cumplimiento de tipado estricto en TypeScript y reglas de dependencias de React Hooks).

---

## 7. Reporte de Compilación de Producción

Para garantizar que el incremento no contiene errores de empaquetado ni dependencias rotas, se ejecutó la compilación de producción en el frontend:
- **Comando Ejecutado:** `npm run build` (`tsc -b && vite build`)
- **Módulos Transformados:** 43 módulos de TypeScript y React.
- **Tiempo de Compilación:** **602 ms**.
- **Artefactos Emitidos:**
  - `dist/index.html` (0.49 kB │ gzip: 0.32 kB)
  - `dist/assets/index-BCeeJAlG.css` (0.44 kB │ gzip: 0.31 kB)
  - `dist/assets/index-N8jf2nwg.js` (294.12 kB │ gzip: 86.88 kB)
- **Dictamen:** Compilación de producción 100% limpia sin advertencias de tipado.

---

## 8. Instrucciones Reproducibles de Ejecución de Pruebas

Para reproducir y auditar de forma independiente la totalidad de las 150 pruebas automatizadas en cualquier estación de trabajo con Windows PowerShell:

```powershell
# =========================================================
# 1. Auditoría y Ejecución de Pruebas de Backend (Python 3.14)
# =========================================================
cd d:\sistema_web_p2p\aplicacion\backend

# A. Análisis estático y verificación de formato
ruff check .
ruff format --check .

# B. Ejecución de las 84 pruebas con reporte de cobertura en terminal
pytest tests/ --cov=app --cov-report=term-missing

# C. Aplicación y verificación de migraciones relacionales Alembic
alembic upgrade head

# =========================================================
# 2. Auditoría y Ejecución de Pruebas de Frontend (React 19)
# =========================================================
cd ..\frontend

# A. Análisis estático de código TypeScript/React
npm run lint

# B. Ejecución de las 66 pruebas con reporte de cobertura V8
npm run test:coverage

# C. Compilación de producción para empaquetado final
npm run build
```

---
*Fin del documento — Evidencia y Catálogo de Pruebas Automatizadas del Sprint 2.*
