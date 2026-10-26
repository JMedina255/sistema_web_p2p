# Documento de Evidencia y Catálogo de Pruebas Automatizadas: Sprint 1

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II)  
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Fecha de Cierre:** 19/10/2026  
**Commit Git:** [`3cda166`](https://github.com/JMedina255/sistema_web_p2p/commit/3cda166)  
**Estado:** ✅ **96 de 96 Pruebas Superadas (100% Satisfactorio)**

---

## Control de Versiones

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcarcel | Dirección EPIS | 19/10/2026 | Emisión inicial del catálogo de evidencias de pruebas automatizadas: desglose de las 13 suites, fixtures de aislamiento, pruebas de persistencia ORM y reportes de cobertura Pytest / Vitest. |

Fuente: Elaboración propia.

---

## 1. Propósito y Estrategia de Pruebas

Asegurar el cumplimiento del requerimiento no funcional **RNF09 (Mantenibilidad y Calidad de Código)**, que exige un umbral mínimo del **70% de cobertura de código por pruebas unitarias automatizadas** en frontend y backend.

La estrategia de pruebas del Sprint 1 implementa tres niveles de aislamiento:
1. **Pruebas Unitarias de Lógica Pura:** Validación de expresiones regulares (correo `@upt.pe`), algoritmos criptográficos (hash de códigos OTP, firma y verificación de JWT) y cálculos de expiración.
2. **Pruebas de Componentes y Adaptadores:** Renderizado en DOM virtual (`jsdom`) mediante React Testing Library, simulando interacciones del estudiante (clic en botones, digitación de OTP, cooldown) y verificando accesibilidad y estados de carga.
3. **Pruebas de Integración con Persistencia ORM:** Pruebas contra sesiones reales de base de datos (`SQLite` en memoria o conexión PostgreSQL aislada), verificando consultas con carga ansiosa (`selectinload`), inserciones, invalidación de registros y comparación de marcas temporales con zona horaria UTC.

---

## 2. Resumen Métrico de Cobertura de Código

A continuación, se presentan los resultados consolidados de cobertura obtenidos mediante las herramientas de análisis de cobertura estandarizadas (Pytest-Cov en Python y V8 Coverage en Vitest).

### Cuadro 2.1: Matriz Consolidada de Cobertura por Capa Arquitectónica

| Entorno de Pruebas | Motor de Ejecución | Pruebas Ejecutadas | Pruebas Aprobadas | Meta Exigida (RNF09) | Cobertura Lograda | Dictamen |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Backend API REST** | Pytest 9.1 + Python 3.14 | 50 | 50 (100%) | $\ge 70.0\%$ | **91.62%** | ✅ Superado (+21.62%) |
| **Frontend React SPA** | Vitest 2.1 + React 19 | 46 | 46 (100%) | $\ge 70.0\%$ | **93.81%** | ✅ Superado (+23.81%) |
| **TOTAL SISTEMA** | **Pipeline Dual CI** | **96** | **96 (100%)** | $\ge 70.0\%$ | **> 92.5% Promedio** | ✅ **Acreditado** |

Fuente: Elaboración propia a partir de reportes generados por Pytest-Cov y Vitest Coverage.

Como se observa en el Cuadro 2.1, ambas capas de software superan holgadamente la meta impuesta por la cátedra, garantizando una base de software altamente mantenible y resistente a regresiones técnicas.

---

## 3. Desglose Exhaustivo de Suites de Prueba de Backend (50 Pruebas)

A continuación, se detalla cada archivo de prueba ejecutado en el backend FastAPI, sus precondiciones, fixtures y casos cubiertos.

### Cuadro 3.1: Catálogo de Pruebas de Backend — Módulos de Autenticación y Catálogo

| Archivo de Prueba | Caso de Prueba | Tipo de Prueba | Precondiciones / Fixture | Resultado Esperado |
| :--- | :--- | :---: | :--- | :--- |
| `tests/test_auth.py` | `test_request_otp_success` | Integración API | Mock de base de datos | Retorna HTTP 200 con `challenge_id`, `expires_at` y `cooldown_seconds=60`. |
| `tests/test_auth.py` | `test_request_otp_rejects_non_upt_domain` | Unitaria / Regla | Petición con `@gmail.com` | Retorna HTTP 400 con código `NON_UPT_DOMAIN` (**RF01**). |
| `tests/test_auth.py` | `test_request_otp_rejects_malformed_email` | Unitaria / Regla | Petición con cadena no-email | Retorna HTTP 400 con código `INVALID_EMAIL`. |
| `tests/test_auth.py` | `test_request_otp_cooldown_rejection` | Lógica Negocio | Segunda petición en $T < 60\text{ s}$ | Retorna HTTP 400 con código `COOLDOWN_ACTIVE` (**CUS01**). |
| `tests/test_auth.py` | `test_resend_otp_success` | Lógica Negocio | Desafío existente y cooldown vencido | Retorna HTTP 200 con nuevo código e invalida el anterior (**RN-01**). |
| `tests/test_auth.py` | `test_resend_otp_not_found` | Validación | UUID aleatorio inexistente | Retorna HTTP 404 con código `CHALLENGE_NOT_FOUND`. |
| `tests/test_auth.py` | `test_verify_otp_invalid_format` | Validación Formato | OTP de longitud distinta de 6 | Retorna HTTP 422 Unprocessable Entity por esquema Pydantic. |
| `tests/test_auth.py` | `test_verify_otp_challenge_not_found` | Integración API | `challenge_id` inexistente | Retorna HTTP 404 con código `CHALLENGE_NOT_FOUND`. |
| `tests/test_auth.py` | `test_verify_otp_expired_code` | Lógica Negocio | Desafío con marca temporal vencida | Retorna HTTP 400 con código `OTP_EXPIRED`. |
| `tests/test_auth.py` | `test_verify_otp_incorrect_code` | Seguridad | OTP no coincidente con el emitido | Retorna HTTP 400 con código `OTP_INVALID`. |
| `tests/test_auth.py` | `test_verify_otp_success_and_jwt_token_issued`| Integración API | OTP correcto y vigente | Retorna HTTP 200 con JWT válido y `expires_in=28800` (8 horas). |
| `tests/test_auth.py` | `test_verify_otp_already_used` | Seguridad | Intento de re-verificar código usado | Retorna HTTP 400 con código `OTP_ALREADY_USED` (**RN-01**). |
| `tests/test_auth.py` | `test_auth_service_with_real_db_session` | Persistencia ORM | Sesión SQLite / Postgres real | Valida persistencia de fila, timestamps UTC y consumo atómico en BD. |
| `tests/test_curriculum.py` | `test_list_courses_returns_5_filter_courses` | Integración API | Base con semilla curricular | Retorna exactamente las 5 materias filtro formativas (**RF05**). |
| `tests/test_curriculum.py` | `test_list_courses_filter_only_priority` | Lógica Negocio | Parámetro `only_priority=true` | Filtra cursos con `es_prioritaria = True`. |
| `tests/test_curriculum.py` | `test_list_courses_filter_by_ciclo` | Lógica Negocio | Parámetro `ciclo=1` | Retorna únicamente Cálculo I. |
| `tests/test_curriculum.py` | `test_get_course_detail_success` | Integración API | `course_id=1` | Retorna detalles completos de Cálculo I (`CI-101`). |
| `tests/test_curriculum.py` | `test_get_course_detail_not_found` | Integración API | `course_id=9999` | Retorna HTTP 404 con código `COURSE_NOT_FOUND`. |
| `tests/test_curriculum.py` | `test_get_course_topics_success` | Integración API | `course_id=1` | Retorna array de 3 temas conceptuales silábicos. |
| `tests/test_curriculum.py` | `test_get_course_topics_not_found` | Integración API | `course_id=9999` | Retorna HTTP 404 con código `COURSE_NOT_FOUND`. |
| `tests/test_curriculum.py` | `test_curriculum_service_with_real_db_session`| Persistencia ORM | Sesión ORM con `selectinload` | Valida navegación bidireccional entre asignatura y colección de temas. |

Fuente: Elaboración propia.

### Cuadro 3.2: Catálogo de Pruebas de Backend — Infraestructura, Sesión y Criptografía

| Archivo de Prueba | Caso de Prueba | Enfoque Evaluado | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| `tests/test_health.py` | `test_health_check_returns_ok` | Diagnóstico de API | HTTP 200 con metadatos del sistema y estado `ok`. |
| `tests/test_health.py` | `test_health_check_remains_operational_without_db` | Resiliencia | `/health` opera con HTTP 200 aun si la base de datos está desconectada. |
| `tests/test_health.py` | `test_health_db_returns_404_outside_development` | Seguridad en Prod | En entorno de producción oculta el endpoint de diagnóstico con HTTP 404. |
| `tests/test_health.py` | `test_health_db_returns_503_when_unconfigured` | Diagnóstico DB | Retorna HTTP 503 cuando `DATABASE_URL` no está definida en `.env`. |
| `tests/test_health.py` | `test_health_db_returns_503_sanitized_on_failure` | Sanitización | Retorna HTTP 503 sin exponer contraseñas ni IPs de Supabase. |
| `tests/test_health.py` | `test_health_db_returns_200_when_connected` | Conectividad DB | Retorna HTTP 200, `database: connected` y latencia en ms. |
| `tests/test_health.py` | `test_root_returns_metadata` | Metadatos de Raíz | `GET /` retorna versión, nombre del proyecto e hipervínculo a `/docs`. |
| `tests/test_security.py`| `test_generate_otp_code_length_and_digits` | Criptografía | Código generado tiene exactamente 6 dígitos numéricos. |
| `tests/test_security.py`| `test_hash_and_verify_otp_code` | Hashing Seguro | Verificación HMAC de código contra su resumen hash. |
| `tests/test_security.py`| `test_create_and_decode_access_token` | JWT Token | Token decodificado recupera `sub` (email) y expiración de 8 horas. |
| `tests/test_security.py`| `test_decode_expired_token_returns_none` | Expiración JWT | Token vencido es rechazado de forma segura retornando `None`. |
| `tests/test_security.py`| `test_decode_invalid_signature_returns_none` | Firma JWT | Token alterado o firmado con clave espuria es rechazado con `None`. |
| `tests/test_security.py`| `test_jwt_secret_masking_in_settings_repr` | Privacidad | `Settings.__repr__()` enmascara `JWT_SECRET_KEY` como `[PROTECTED]`. |
| `tests/test_session.py` | `test_get_engine_returns_none_when_unconfigured` | Lazy Engine | Sin `DATABASE_URL`, el motor retorna `None` sin lanzar excepción fatal. |
| `tests/test_session.py` | `test_get_engine_initializes_and_caches` | Pool de Conexiones | El motor se inicializa una sola vez y se reutiliza en subsiguientes llamadas. |
| `tests/test_session.py` | `test_get_session_raises_runtime_error_when_unconfigured` | Inyección Dep. | `get_db()` lanza excepción controlada si no hay motor configurado. |
| `tests/test_session.py` | `test_get_session_yields_and_closes_session` | Gestión Recursos | La sesión SQLAlchemy se cierra limpiamente al culminar la petición HTTP. |
| `tests/test_session.py` | `test_close_engine_is_idempotent` | Cierre Recursos | `close_engine()` puede invocarse múltiples veces sin lanzar error. |
| `tests/test_session.py` | `test_sanitize_db_error_protects_secrets` | Sanitización Trazas | Reemplaza contraseñas con `***` en mensajes de error de psycopg3. |
| `tests/test_session.py` | `test_test_db_connection_unconfigured` | Diagnóstico Conexión | Retorna `(False, "DATABASE_URL no configurada")` sin conectar a red. |
| `tests/test_session.py` | `test_test_db_connection_success` | Diagnóstico Conexión | Ejecuta `SELECT 1` y retorna `(True, latency_ms)`. |
| `tests/test_session.py` | `test_test_db_connection_unexpected_scalar` | Diagnóstico Conexión | Detecta si la base de datos retorna una respuesta anómala. |
| `tests/test_session.py` | `test_test_db_connection_exception_sanitizes_secret` | Sanitización | Comprueba que las excepciones de red sean enmascaradas. |
| `tests/test_config.py`  | `test_cors_origins_parsing_from_json_string` | Configuración | Parsea `CORS_ORIGINS='["http://localhost:5173"]'` a lista Python. |
| `tests/test_config.py`  | `test_cors_origins_parsing_from_comma_string` | Configuración | Parsea lista delimitada por comas `http://a,http://b`. |
| `tests/test_config.py`  | `test_cors_origins_parsing_from_invalid_json` | Resiliencia | Ante JSON corrupto, utiliza lista por defecto sin colapsar el arranque. |
| `tests/test_config.py`  | `test_cors_origins_parsing_from_list` | Configuración | Acepta listas directas provistas en pruebas. |
| `tests/test_config.py`  | `test_sync_database_url_dialects` | Normalización URL | Convierte automáticamente `postgresql://` a `postgresql+psycopg://`. |
| `tests/test_config.py`  | `test_database_url_repr_masking` | Privacidad | `Settings.__repr__()` enmascara la contraseña de la base de datos. |

Fuente: Elaboración propia.

---

## 4. Desglose Exhaustivo de Suites de Prueba de Frontend (46 Pruebas)

A continuación, se documenta la suite de pruebas del cliente web React 19 ejecutada con Vitest.

### Cuadro 4.1: Catálogo de Pruebas de Frontend — Servicios y Componentes

| Archivo de Prueba | N.° Tests | Enfoque Evaluado y Componentes | Cobertura Lograda |
| :--- | :---: | :--- | :---: |
| `src/services/__tests__/authService.test.ts` | 15 | Pruebas completas de `MockAuthAdapter`: emisión de OTP, expiración de 5 minutos, cooldown de 60 segundos, códigos inválidos y verificación. | 89.94% |
| `src/services/__tests__/apiAuthAdapter.test.ts` | 9 | Pruebas de `ApiAuthAdapter`: interacción con endpoints REST reales mediante simulación de `fetch`, serialización JSON y captura de excepciones HTTP 400. | 85.19% |
| `src/services/__tests__/apiClient.test.ts` | 6 | Pruebas de cliente HTTP base: timeouts, extracción de cabeceras, manejo de desconexión sin colapso y llamada a `/health/db`. | 59.37% |
| `src/components/__tests__/LoginOtpView.test.tsx` | 9 | Pruebas de interfaz React: renderizado inicial de correo, advertencia de modo mock, validación de `@upt.pe`, paso a paso de verificación OTP y feedback de éxito. | 94.52% |
| `src/components/__tests__/CurriculumCatalogView.test.tsx` | 3 | Pruebas del catálogo curricular: renderizado de las 5 materias prioritarias, selección de curso y visualización de unidades temáticas silábicas. | 97.92% |
| `src/components/__tests__/HealthStatus.test.tsx` | 3 | Pruebas del monitor de servicios: semáforo verde para estado saludable, indicador de latencia en milisegundos y botón de reintento. | 100% |
| `src/__tests__/App.test.tsx` | 1 | Prueba de navegación global: cambio de pestañas institucionales (Acceso OTP, Catálogo Curricular y Monitor de Servicios). | 98.75% |

Fuente: Elaboración propia.

---

## 5. Instrucciones de Reproducción de Pruebas

Para reproducir y auditar de forma independiente la totalidad de las 96 pruebas automatizadas en cualquier estación de trabajo:

```powershell
# 1. Ejecutar las 50 pruebas de Backend con reporte de cobertura:
cd aplicacion/backend
pytest tests/ --cov=app --cov-report=term-missing

# 2. Ejecutar análisis estático y formateo de Backend:
ruff check .
ruff format --check .

# 3. Ejecutar las 46 pruebas de Frontend con reporte de cobertura:
cd ../frontend
npm run test:coverage

# 4. Ejecutar análisis estático y compilación de Frontend:
npm run lint
npm run build
```

---
*Fin del documento — Evidencia y Catálogo de Pruebas Automatizadas del Sprint 1.*
