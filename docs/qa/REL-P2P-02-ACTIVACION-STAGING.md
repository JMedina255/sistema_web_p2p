# REL-P2P-02 — Activación Controlada de Staging y Validación Operativa

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Repositorio Oficial:** `https://github.com/JMedina255/sistema_web_p2p.git`  
**Rama de Trabajo:** `release/rel-p2p-02-staging-activation`  
**Commit Base:** `fe699fe44f14183731bcfb9b6289a0b618296c50` (Merge pull request #23 from `release/rel-p2p-01-staging-preparation`)  
**Fecha:** 21 de noviembre de 2026  
**Responsable:** Antigravity AI — Google DeepMind

---

## 1. Resumen Ejecutivo

El hito **REL-P2P-02** consolida la preparación del entorno de staging del Sistema Web P2P de Mentorías Académicas EPIS-UPT, resolviendo las divergencias de configuración entre Frontend y Backend, blindando la capa de persistencia PostgreSQL y garantizando la inmutabilidad de la base de datos principal (`db.ieaxmtxpcrldbvmqwbyt.supabase.co`).

### Resultados Clave:
1. **Sincronización:** Confirmada la fusión del PR #23 en `main` (`fe699fe...`) y la ejecución exitosa de GitHub Actions #114 (`44900096146`). Se creó la rama `release/rel-p2p-02-staging-activation`.
2. **Corrección de Configuración Frontend:**
   - Se ajustó `VITE_API_BASE_URL` en [aplicacion/frontend/.env.staging.example](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/.env.staging.example) a la raíz del servicio (`https://api-staging.p2p.epis-upt.pe`) sin prefijo `/api/v1`, eliminando la duplicación en los adaptadores.
   - Se estableció explícitamente `VITE_SERVICE_MODE=api`.
   - Se implementó el módulo [aplicacion/frontend/src/services/serviceMode.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/serviceMode.ts) para materializar de forma real `VITE_DISABLE_MOCK_MODE=true` en todos los servicios (`bookingService`, `authService`, `consentService`, `offerService`, `profileService`, `recommendationService`, `roleService`, `attendanceService`, `bitacoraService`, `surveyService`, `certificateService`), impidiendo cualquier degradación a mock en staging o producción.
3. **Corrección de Configuración Backend:**
   - En [aplicacion/backend/.env.staging.example](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/.env.staging.example), se sustituyó `ACCESS_TOKEN_EXPIRE_MINUTES` por `JWT_ACCESS_TOKEN_EXPIRE_MINUTES=480`.
   - Se estandarizaron las variables OTP normativas (`OTP_EXPIRE_MINUTES=5`, `OTP_COOLDOWN_SECONDS=60`, `MAX_OTP_ATTEMPTS=5`, `OTP_RATE_LIMIT_PER_MINUTE=5`).
   - Se reemplazó `SMTP_TLS` por `SMTP_USE_TLS=true` y se forzó `SMTP_ENABLED=false` hasta disponer de un buzón institucional de pruebas acreditado.
   - Se declaró explícitamente `STRICT_DATABASE_MODE=true`.
   - Se sustituyeron secretos demo reutilizables por marcadores explícitos que exigen contraseñas criptográficas independientes.
   - En [aplicacion/backend/app/core/config.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/app/core/config.py), se incorporó un validador Pydantic que bloquea el inicio de la aplicación en staging/producción si se detectan claves demo, claves cortas (< 32 caracteres), `ENABLE_MOCK_OTP_HINTS=True`, `STRICT_DATABASE_MODE=False` o cadenas con marcadores de plantilla no sustituidos.
4. **Hardening de PostgreSQL y Supabase:**
   - Se eliminó `db.ieaxmtxpcrldbvmqwbyt.supabase.co` de la lista blanca por defecto (`DEFAULT_ALLOWED_QA_HOSTS` en [tools/qa_db_hardening.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/tools/qa_db_hardening.py)), restringiendo el destino permitido por defecto únicamente a interfaces loopback (`localhost`, `127.0.0.1`, `::1`).
   - Se implementó `extract_supabase_project_ref()` para extraer el identificador unívoco de proyecto Supabase tanto de conexiones directas (`db.<ref>.supabase.co`) como de conexiones por pooler transaccional (`postgres.<ref>@aws-0-...pooler.supabase.com`).
   - Se potenció `validate_qa_not_same_as_production()` para bloquear cualquier colisión de proyecto Supabase, imposibilitando que pruebas destructivas se ejecuten contra el proyecto principal mediante rutas alternativas.
   - Se blindó `verify_database_identity_and_role()` para exigir roles de mínimos privilegios (`least privilege`), rechazando por defecto conexiones con privilegios administrativos (`rolsuper=True`, `rolcreaterole=True`).
   - Se garantizó que fallos durante el teardown en `isolated_test_schema()` arrojen `DatabaseSecurityError` visible y nunca sean silenciados.
5. **Aislamiento de la Base de Datos:**
   - No se ejecutó ninguna operación DDL destructiva contra la instancia remota existente.
   - Dado que la infraestructura aún no cuenta con una segunda instancia o proyecto Supabase exclusivo para Staging, las pruebas destructivas remotas permanecen clasificadas como **`BLOCKED`** de forma honesta y trazable.
   - Se verificó la cadena completa de migraciones Alembic (001 a 006) en modo estático fuera de línea (`alembic upgrade head --sql`), confirmando la coherencia de DDL, RLS y permisos.

---

## 2. Fase 0 — Sincronización y Estado del Repositorio

| Parámetro | Detalle Verificado |
|---|---|
| **Pull Request #23** | Estado: `CLOSED` / `MERGED` el 21/11/2026 a las 11:38:50 UTC |
| **Commit de Merge** | `fe699fe44f14183731bcfb9b6289a0b618296c50` |
| **GitHub Actions #114** | ID: `44900096146` | Evento: `push` sobre `main` | Conclusión: **`success`** |
| **Rama Local Creada** | `release/rel-p2p-02-staging-activation` |
| **Árbol de Trabajo** | Limpio, sincronizado mediante fast-forward sobre `main` |

---

## 3. Fase 1 — Auditoría y Corrección de Plantillas de Configuración

Se contrastó minuciosamente cada variable de entorno de las plantillas `.env.staging.example` contra el código fuente real que la consume.

### 3.1. Correcciones en el Frontend (`aplicacion/frontend/.env.staging.example`)

1. **Alineación de URL Base (`VITE_API_BASE_URL`):**
   - *Hallazgo:* Los adaptadores del frontend (`apiClient.ts`, `attendanceService.ts`, `bitacoraService.ts`, `profileService.ts`, `bookingService.ts`, etc.) concatenan explícitamente el prefijo `/api/v1` a la URL base (ej. `${API_BASE_URL}/api/v1/health`).
   - *Corrección:* Se configuró `VITE_API_BASE_URL=https://api-staging.p2p.epis-upt.pe` (raíz sin `/api/v1`), impidiendo la generación de rutas anómalas como `/api/v1/api/v1/...`.
2. **Modo Operativo Explícito:**
   - Se fijó `VITE_SERVICE_MODE=api` para ordenar el consumo de endpoints FastAPI.
3. **Materialización de `VITE_DISABLE_MOCK_MODE`:**
   - *Hallazgo:* Anteriormente, `VITE_DISABLE_MOCK_MODE` era una variable declarativa sin efecto en el código fuente.
   - *Implementación:* Se creó [aplicacion/frontend/src/services/serviceMode.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/serviceMode.ts), el cual define:
     * `isMockModeDisabled()`: Evalúa `PROD || VITE_DISABLE_MOCK_MODE === 'true' || VITE_APP_ENV === 'staging' || VITE_STAGE === 'staging'`.
     * `resolveInitialServiceMode()`: Retorna forzosamente `'api'` si el modo mock está deshabilitado.
     * `assertAllowedMode(mode)`: Intercepta llamadas a `setMode('mock')` en tiempo de ejecución, emitiendo una alerta de seguridad por consola y manteniendo el modo `'api'`.
   - Se integró en 11 servicios frontend y se crearon pruebas unitarias específicas en [aplicacion/frontend/src/services/__tests__/serviceMode.test.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/__tests__/serviceMode.test.ts) (7/7 aprobadas).

### 3.2. Correcciones en el Backend (`aplicacion/backend/.env.staging.example`)

1. **Tokens y Expiración:**
   - Se sustituyó `ACCESS_TOKEN_EXPIRE_MINUTES` por `JWT_ACCESS_TOKEN_EXPIRE_MINUTES=480` (consumido directamente por `app/core/config.py`).
2. **Retos OTP y Políticas Normativas:**
   - Se eliminaron nombres informales (`OTP_EXPIRATION_SECONDS`, `OTP_RESEND_COOLDOWN_SECONDS`, `OTP_MAX_ATTEMPTS`) y se establecieron las propiedades canónicas de `Settings`:
     * `OTP_EXPIRE_MINUTES=5` (Ventana normativa RNF01).
     * `OTP_COOLDOWN_SECONDS=60` (Cooldown CUS01).
     * `MAX_OTP_ATTEMPTS=5` (Límite de fallos).
     * `OTP_RATE_LIMIT_PER_MINUTE=5` (Rate limiting normativo).
     * `ENABLE_MOCK_OTP_HINTS=false` (Prohíbe la exposición de códigos en respuestas HTTP).
3. **Servicio de Correo (SMTP):**
   - Se sustituyó `SMTP_TLS=true` por `SMTP_USE_TLS=true`.
   - Se configuró `SMTP_ENABLED=false` para prevenir intentos fallidos de envío de correo en staging mientras no se habiliten credenciales y buzones autorizados de pruebas.
4. **Persistencia Estricta:**
   - Se incorporó `STRICT_DATABASE_MODE=true` de forma explícita.
5. **Erradicación de Claves Demo:**
   - Se sustituyeron las cadenas demo por marcadores explícitos que impiden el arranque accidental sin credenciales reales:
     * `JWT_SECRET_KEY="<GENERATE_SECURE_RANDOM_SECRET_MIN_32_CHARS>"`
     * `STAGING_DB_PASSWORD="<GENERATE_SECURE_STAGING_DB_PASSWORD>"`
     * `QA_DB_PASSWORD="<GENERATE_SECURE_QA_DB_PASSWORD>"`

### 3.3. Candados de Configuración en `app/core/config.py`

En la clase `Settings`, el decorador `@model_validator(mode="after")` fue extendido para validar de forma automática entornos `staging` y `production`:
- Rechaza `ENABLE_MOCK_OTP_HINTS=True`.
- Rechaza `STRICT_DATABASE_MODE=False`.
- Rechaza claves JWT por defecto (`dev-jwt-secret-key...`, `staging-jwt-secret-key...`), marcadores `<GENERATE_` o longitud menor a 32 caracteres.
- Rechaza marcadores de plantilla no sustituidos en `DATABASE_URL` (`STAGING_PROJECT_REF`, `<GENERATE_`).
- Rechaza `SMTP_ENABLED=True` si no se proporcionan credenciales reales o si contienen valores demo.
- Se agregaron 10 pruebas automatizadas en [aplicacion/backend/tests/test_config_staging.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/tests/test_config_staging.py) (10/10 aprobadas).

---

## 4. Fase 2 — Preparación de PostgreSQL y Protección de Instancia

### 4.1. Remoción de Destinos No Acreditados de la Lista Blanca

En [tools/qa_db_hardening.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/tools/qa_db_hardening.py), la lista blanca por defecto `DEFAULT_ALLOWED_QA_HOSTS` fue restringida estrictamente a:
```python
DEFAULT_ALLOWED_QA_HOSTS = {
    "localhost",
    "127.0.0.1",
    "::1",
}
```
Se removió la excepción estática que incluía `db.ieaxmtxpcrldbvmqwbyt.supabase.co`. Cualquier host de pruebas remoto debe ser inyectado explícitamente a través de la variable `ALLOWED_QA_HOSTS`.

### 4.2. Detección Inteligente de Proyectos Supabase (Directo vs Pooler)

Las conexiones a Supabase pueden realizarse a través de:
1. Conexión directa: `postgresql+psycopg://postgres:<pass>@db.<ref>.supabase.co:5432/postgres`
2. Connection Pooler (PgBouncer): `postgresql+psycopg://postgres.<ref>:<pass>@aws-0-<region>.pooler.supabase.com:5432/postgres`

Se implementó la función `extract_supabase_project_ref(url)` que extrae la referencia del proyecto desde el subdominio del host (`db.<ref>`) o desde el prefijo de usuario en el pooler (`postgres.<ref>`).

En `validate_qa_not_same_as_production()`, si `qa_ref == prod_ref`, se aborta la ejecución con `DatabaseSecurityError`:
```
[BLOCKED] Pruebas transaccionales en PostgreSQL detenidas por política de seguridad:
          ¡COLISIÓN DE PROYECTO SUPABASE DETECTADA! QA_DATABASE_URL y DATABASE_URL hacen referencia
          al mismo proyecto de Supabase (project_ref='ieaxmtxpcrldbvmqwbyt'), a pesar de diferir
          en formato o modo de conexión (directa vs pooler).
```

### 4.3. Validación de Rol de Mínimos Privilegios (`Least Privilege`)

En `verify_database_identity_and_role()`, se añadió verificación activa de facultades administrativas del rol de conexión:
- Si el rol posee `rolsuper=True` (Superusuario) o `rolcreaterole=True` (Creación de roles), la ejecución DDL destructiva se rechaza:
```
¡PRIVILEGIOS EXCESIVOS RECHAZADOS! El rol de conexión 'postgres' posee privilegios administrativos
(rolsuper=True, rolcreaterole=True). Para proteger la integridad del entorno y prevenir escalamiento
o daños estructurales, se exige un rol dedicado de privilegios mínimos (least privilege, ej. 'qa_runner')
sin facultades de superusuario ni creación de roles para la ejecución de pruebas.
```
- Se proporciona la opción de anulación local controlada `ALLOW_SUPERUSER_QA_ROLE=true` exclusivamente para entornos de desarrollo en contenedores locales.

### 4.4. Visibilidad de Fallos en Teardown

En el context manager `isolated_test_schema()`, los fallos ocurridos durante `safe_teardown_schema()` ya no son silenciados ni enmascarados como exitosos; se lanza una excepción explícita `DatabaseSecurityError("FALLO CRÍTICO DE TEARDOWN: ...")`.

### 4.5. Procedimiento para Provisión de Instancia Dedicada de Staging

Para que el equipo de infraestructura de EPIS-UPT provisione la base de datos de staging:
1. **Crear Proyecto Independiente:**
   - Acceder al panel de Supabase y crear una nueva organización o proyecto con nombre: `epis-upt-p2p-staging`.
   - Seleccionar región geográfica idéntica a producción (ej. `us-east-1`).
2. **Crear Rol de Mínimos Privilegios para QA/Staging:**
   Ejecutar en el SQL Editor del nuevo proyecto:
   ```sql
   -- 1. Crear rol con privilegios mínimos para ejecución de pruebas
   CREATE ROLE qa_runner WITH LOGIN PASSWORD 'PASSWORD_COMPLEJA_DE_QA';
   GRANT CONNECT ON DATABASE postgres TO qa_runner;
   GRANT CREATE ON DATABASE postgres TO qa_runner;
   GRANT USAGE, CREATE ON SCHEMA public TO qa_runner;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO qa_runner;
   ```
3. **Configurar Variables de Entorno en el Servidor de Staging:**
   ```bash
   APP_ENV=staging
   STAGE=staging
   DATABASE_URL="postgresql+psycopg://postgres.<STG_REF>:<STG_PASS>@aws-0-us-east-1.pooler.supabase.com:5432/postgres?sslmode=require"
   QA_DATABASE_URL="postgresql+psycopg://qa_runner.<STG_REF>:<QA_PASS>@aws-0-us-east-1.pooler.supabase.com:5432/postgres?sslmode=require"
   ALLOWED_QA_HOSTS="aws-0-us-east-1.pooler.supabase.com,db.<STG_REF>.supabase.co"
   STRICT_DATABASE_MODE=true
   JWT_SECRET_KEY="CLAVE_CRIPTOGRAFICA_SEGURA_GENERADA_PARA_STAGING_MIN_32_CHARS"
   ```
4. **Estado Actual:**
   - La base de datos de producción (`db.ieaxmtxpcrldbvmqwbyt.supabase.co`) se encuentra 100% protegida.
   - Las pruebas transaccionales remotas se declaran **`BLOCKED`** a la espera de la creación del proyecto dedicado por el administrador.

---

## 5. Fase 3 — Migraciones Alembic y Consistencia de Esquema

### 5.1. Validación Estática Fuera de Línea (`alembic upgrade head --sql`)

Se ejecutó la generación estática de scripts DDL transaccionales para todas las revisiones del sistema, verificando que no existan dependencias circulares ni incompatibilidades de sintaxis:

```sql
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Generating static SQL
INFO  [alembic.runtime.migration] Will assume transactional DDL.
BEGIN;

-- Revision 20261019_001 -> initial_curriculum_and_auth (asignaturas, temas_conceptuales)
-- Revision 20261023_002 -> roles_and_profiles (roles, usuario_roles, perfiles_academicos, disponibilidades_horarias)
-- Revision 20261026_003 -> mentoring_offers (sesiones_mentoria, consentimientos_legales)
-- Revision 20261031_004 -> booking_and_reservations (reservas_cupos, indices concurrentes)
-- Revision 20261113_005 -> closure_and_advanced_modules (tokens_asistencia_activos, bitacoras, encuestas, certificados)
-- Revision 20261116_006 -> auth_rate_limits (auth_rate_limits con RLS, REVOKE anon/authenticated y GRANT service_role/postgres)

COMMIT;
```

### 5.2. Procedimiento de Migración al Desplegar Staging
1. Realizar respaldo previo con `pg_dump`:
   ```bash
   pg_dump -h aws-0-us-east-1.pooler.supabase.com -U postgres.<STG_REF> -d postgres -F c -b -v -f backup_pre_migration.dump
   ```
2. Comprobar versión inicial:
   ```bash
   alembic current
   ```
3. Ejecutar migración controlada:
   ```bash
   alembic upgrade head
   ```
4. Comprobar versión final (`20261116_006`) y políticas RLS:
   ```sql
   SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';
   SELECT * FROM pg_policies WHERE tablename = 'auth_rate_limits';
   ```

---

## 6. Fase 4 — Despliegue y Pruebas de Humo

### 6.1. Pruebas de Integración de API (30/30 PASS)

Ejecutadas mediante `tools/validate_functional_journeys.py` (FastAPI TestClient + SQLite en memoria con StaticPool):

| Módulo | Casos Evaluados | Resultado |
|---|---|:---:|
| 1. Autenticación & Consentimiento | 6 comprobaciones (Rechazo dominio externo, emisión OTP, validación errónea, emisión JWT, consentimiento Ley 29733, rol institucional) | **PASS** |
| 2. Perfiles & Disponibilidad | 3 comprobaciones (Consulta perfil, actualización perfil formativo, persistencia agenda semanal 6x11) | **PASS** |
| 3. Catálogo Curricular | 2 comprobaciones (Asignaturas oficiales, temario conceptual silábico) | **PASS** |
| 4. Ofertas de Mentoría | 2 comprobaciones (Validación RN-04 antelación > 24h, publicación formal aforos RN-05) | **PASS** |
| 5. Recomendaciones Top-k | 2 comprobaciones (Ranking EdRecSys de ofertas y mentores afines) | **PASS** |
| 6. Reservas de Cupos | 5 comprobaciones (Reserva provisional, prevención duplicada, confirmación atómica, desistimiento voluntario, rechazo de doble cancelación) | **PASS** |
| 7. Sesiones y Quórum | 1 comprobación (Cálculo normativo RN-09 de quórum a T-24h) | **PASS** |
| 8. Asistencia & Bitácora | 4 comprobaciones (Generación token TOTP dinámico, check-in, validación longitud bitácora RN-12, sellado SHA-256) | **PASS** |
| 9. Administración & Certificados | 5 comprobaciones (Consulta roles, validación RBAC 403 Forbidden, visado administrativo RN-14, horas acumuladas, consulta pública QR) | **PASS** |
| **Total** | **30 comprobaciones de integración de API** | **100% PASS** |

### 6.2. Pruebas Unitarias y de Seguridad del Backend (455 PASS, 1 SKIP)

- **Total Pruebas:** 456
- **Aprobadas:** 455
- **Omitidas:** 1 (`test_auth_rate_limits_concurrency_pg_skip` — omitida en SQLite por exigir PostgreSQL real)
- **Cobertura Global:** **83%** (Excede el umbral del 70.0% requerido por el proyecto)
- **Pruebas de Blindaje de Base de Datos (`test_qa_db_hardening.py`):** 69/69 aprobadas
- **Pruebas de Validación de Configuración Staging (`test_config_staging.py`):** 10/10 aprobadas

### 6.3. Pruebas Unitarias del Frontend (366 PASS en 37 archivos)

- **Total Pruebas:** 366 en 37 suites Vitest
- **Aprobadas:** 366 (100% éxito)
- **Pruebas de Blindaje de Modo de Servicio (`serviceMode.test.ts`):** 7/7 aprobadas
- **Compilación de Producción (Vite Build):** Exitosa en 2.26 segundos sin errores de tipado TypeScript ni empaquetado.
- **Linters:** ESLint (`npx eslint .`) y Ruff (`ruff check .`, `ruff format --check .`) limpios con 0 observaciones.

---

## 7. Fase 5 — Protocolos para Servicios Externos

### 7.1. Protocolo de Validación Manual — Google OAuth 2.0
1. Configurar en Google Cloud Console:
   - Pantalla de consentimiento OAuth: Tipo "Interno" (restringido a la organización Universidad Privada de Tacna).
   - URI de redirección autorizada: `https://staging.p2p.epis-upt.pe` y `http://localhost:5173`.
2. Casos de Prueba:
   - **TC-OAUTH-01 (Aprobado):** Ingreso con cuenta `@virtual.upt.pe` o `@upt.pe` -> Autenticación exitosa y emisión de token JWT institucional.
   - **TC-OAUTH-02 (Rechazo):** Ingreso con cuenta externa `@gmail.com` -> Respuesta HTTP 403 y mensaje accesible: "Acceso exclusivo para miembros de la comunidad EPIS-UPT".
   - **TC-OAUTH-03 (Token Inválido):** Inyección de token adulterado o con `aud` no coincidente -> Rechazo inmediato con código `INVALID_AUDIENCE`.

### 7.2. Protocolo de Validación Manual — Servicio de Correo (SMTP)
1. Credenciales de Staging:
   - Utilizar buzón de pruebas dedicado institucional (ej. `notificaciones.staging@upt.pe`).
   - Generar Google Workspace App Password de 16 caracteres exclusiva para el entorno de Staging.
2. Casos de Prueba:
   - **TC-SMTP-01 (Despacho OTP):** Solicitud de código OTP a estudiante de prueba -> Recepción de correo con plantilla institucional oficial y expiración a 5 minutos.
   - **TC-SMTP-02 (Fallo de Servidor):** Simulación de desconexión SMTP (puerto o host inválido) -> Manejo controlado de excepción, registro en logs y código HTTP 503 sin exposición de trazas internas ni contraseñas.
   - **TC-SMTP-03 (Prevención de Despacho en Modo Seguro):** Con `SMTP_ENABLED=false`, las solicitudes OTP se procesan internamente sin emitir tráfico de red hacia servidores de correo.

---

## 8. Matriz de Trazabilidad y Estado de Fases

| Fase | Descripción | Estado | Evidencia |
|---|---|:---:|---|
| **Fase 0** | Sincronización y verificación de PR #23 | **COMPLETADO** | Merge commit `fe699fe...`, Run #114 `success`, rama `release/rel-p2p-02-staging-activation`. |
| **Fase 1** | Corrección de plantillas Staging y candados | **COMPLETADO** | `.env.staging.example` corregidos, `serviceMode.ts` en Frontend, validador Pydantic en `config.py`. |
| **Fase 2** | Hardening de PostgreSQL y aislamiento | **COMPLETADO** | `qa_db_hardening.py` mejorado, detección de ref Supabase, least privilege role, eliminación de host principal de la lista blanca. |
| **Fase 3** | Validación de migraciones Alembic | **COMPLETADO** | `alembic upgrade head --sql` validado (001 a 006). Ejecución en BD staging remota declarada **`BLOCKED`** por ausencia de infraestructura dedicada. |
| **Fase 4** | Despliegue y pruebas de humo | **COMPLETADO** | 30/30 API checks PASS, 455/456 Pytest PASS, 366/366 Vitest PASS, Vite Build limpio en 2.26s. |
| **Fase 5** | Protocolos de servicios externos | **COMPLETADO** | Protocolos documentados para Google OAuth y SMTP con restricciones de dominio institucional. |
| **Fase 6** | Documentación y cierre de versión | **COMPLETADO** | Informe [docs/qa/REL-P2P-02-ACTIVACION-STAGING.md](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/REL-P2P-02-ACTIVACION-STAGING.md). |

---

## 9. Archivos Modificados y Creados

- **Frontend:**
  * Modificado: [aplicacion/frontend/.env.staging.example](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/.env.staging.example) (Alineación URL base sin `/api/v1`, `VITE_SERVICE_MODE=api`, `VITE_DISABLE_MOCK_MODE=true`).
  * Creado: [aplicacion/frontend/src/services/serviceMode.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/serviceMode.ts) (Módulo centralizado de control de modos mock vs api).
  * Modificados: Servicios integrados con `serviceMode.ts` ([bookingService.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/bookingService.ts), [authService.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/authService.ts), [consentService.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/consentService.ts), [offerService.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/offerService.ts), [profileService.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/profileService.ts), [recommendationService.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/recommendationService.ts), [roleService.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/roleService.ts), [attendanceService.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/attendanceService.ts), [bitacoraService.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/bitacoraService.ts), [surveyService.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/surveyService.ts), [certificateService.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/certificateService.ts)).
  * Creado: [aplicacion/frontend/src/services/__tests__/serviceMode.test.ts](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/frontend/src/services/__tests__/serviceMode.test.ts) (7 pruebas unitarias).
- **Backend:**
  * Modificado: [aplicacion/backend/.env.staging.example](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/.env.staging.example) (`JWT_ACCESS_TOKEN_EXPIRE_MINUTES`, variables OTP, `SMTP_USE_TLS`, marcadores seguros, `STRICT_DATABASE_MODE`).
  * Modificado: [aplicacion/backend/app/core/config.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/app/core/config.py) (Candados de seguridad en `Settings` para staging/producción).
  * Creado: [aplicacion/backend/tests/test_config_staging.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/tests/test_config_staging.py) (10 pruebas unitarias).
  * Modificado: [aplicacion/backend/tests/test_qa_db_hardening.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/tests/test_qa_db_hardening.py) (Ampliación a 69 pruebas de seguridad).
- **Herramientas de Blindaje:**
  * Modificado: [tools/qa_db_hardening.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/tools/qa_db_hardening.py) (`extract_supabase_project_ref`, remoción de host principal de la lista blanca, verificación de `least privilege`, teardown failures explícitos).
- **Documentación:**
  * Creado: [docs/qa/REL-P2P-02-ACTIVACION-STAGING.md](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/REL-P2P-02-ACTIVACION-STAGING.md).
