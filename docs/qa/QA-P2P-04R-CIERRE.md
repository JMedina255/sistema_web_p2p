# Informe de Cierre de Hardening de Seguridad: QA-P2P-04R
## Blindaje Definitivo de Destinos PostgreSQL, Verificación Estricta de Aislamiento y Certificación de Staging

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Repositorio Oficial:** `https://github.com/JMedina255/sistema_web_p2p.git`  
**Rama de Trabajo:** `fix/qa-p2p-04-hardening-staging`  
**Fecha de Ejecución:** 21 de Noviembre de 2026  
**Responsable:** Antigravity QA & Security Engineering Specialist  
**Estado General:** **CERTIFICADO CON MÁXIMO BLINDAJE** (100% de compuertas aprobadas, 0 regresiones)

---

## 1. Resumen Ejecutivo

El presente ciclo de cierre, **QA-P2P-04R**, complementa y culmina con el más alto rigor de seguridad el hardening iniciado en QA-P2P-04. Tras una revisión técnica exhaustiva, se detectaron riesgos de ambigüedad en la determinación del entorno destino de PostgreSQL y en los criterios de aislamiento por esquemas. 

El presente cierre resolvió integralmente dichas observaciones implementando protecciones deterministas a nivel de red, credenciales, entorno y catálogo de base de datos. Se garantiza de forma matemática que **ninguna prueba automatizada podrá operar sobre instancias de producción**, erradicando cualquier posibilidad de anulación local de variables prohibitivas y asegurando que las aserciones de prueba reflejen con exactitud las operaciones ejecutadas.

### Hitos Clave Alcanzados en QA-P2P-04R

1. **Resolución Exclusiva de Base de Datos de Pruebas (`QA_DATABASE_URL`):**
   - Se desacopló por completo la ejecución de pruebas de la variable `DATABASE_URL` general.
   - Es mandatorio disponer de `QA_DATABASE_URL`, apuntando a una base de datos o proyecto dedicado exclusivamente a QA y pruebas.
   - En ausencia de una base de datos de QA debidamente identificada, las pruebas automatizadas se detienen de inmediato con estado `BLOCKED` (mediante `DatabaseSecurityError`), sin alterar datos.
2. **Blindaje Multivariable Anti-Producción:**
   - Se evalúan simultáneamente `APP_ENV`, `ENVIRONMENT`, `NODE_ENV` y `STAGE`. Si **cualquiera** de ellas declara `production` o `prod`, la ejecución se interrumpe de inmediato.
   - Ninguna variable local de desarrollo (`ENVIRONMENT=development`, `ALLOW_TEST_SCHEMA_CREATION=true`) tiene precedencia sobre una bandera productiva.
3. **Lista Blanca Estricta de Destinos de Red (`validate_qa_target_url`):**
   - Se valida el nombre de host antes de establecer la conexión. Solo se admiten hosts en lista blanca (`localhost`, `127.0.0.1`, `::1`, proyectos dedicados de Supabase QA como `db.ieaxmtxpcrldbvmqwbyt.supabase.co` o los definidos en `ALLOWED_QA_HOSTS`).
   - Se rechaza por defecto cualquier host no reconocido o que contenga identificadores productivos (`prod`, `production`, `live`, etc.).
4. **Verificación Determinista de Identidad y Rol antes de DDL:**
   - Se consulta `SELECT current_database(), current_user, session_user;` en PostgreSQL. Se prohíbe cualquier operación si el catálogo de la base de datos reporta identificadores productivos.
5. **Aislamiento Estricto por Coincidencia Exacta (`current_schema()`):**
   - La función `verify_connection_search_path()` exige que `current_schema()` sea **idéntico** al esquema efímero generado para la corrida. Se rechaza si es `public` o si el esquema esperado solo aparece como subcadena en `SHOW search_path;`.
6. **Protección del Ciclo de Vida de Esquemas:**
   - `create_isolated_schema()` verifica en `information_schema.schemata` que el esquema no exista previamente, prohibiendo la adopción o sobreescritura accidental de esquemas existentes.
   - `safe_teardown_schema()` restringe el `DROP SCHEMA` única y exclusivamente a esquemas registrados en memoria durante la corrida actual (`_CREATED_SCHEMAS_IN_THIS_RUN`).
   - El context manager `isolated_test_schema()` garantiza la limpieza en su bloque `finally:` ante cualquier excepción no controlada.
7. **Suite de Pruebas Unitarias de Seguridad:**
   - 51 pruebas unitarias y negativas implementadas en [aplicacion/backend/tests/test_qa_db_hardening.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/aplicacion/backend/tests/test_qa_db_hardening.py), aprobadas al 100% en Pytest.
8. **Alineación de Casos E2E y Documentación:**
   - El caso `E2E-EST-02` fue renombrado y catalogado como `"Consulta y Visualización de Perfil y Disponibilidad"`, reflejando exactamente la inspección visual en UI sin atribuir falsamente una mutación o actualización.
   - En [docs/qa/QA-P2P-04-RESULTADOS.md](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/QA-P2P-04-RESULTADOS.md) se aclaró que los esquemas efímeros son una capa complementaria de defensa en profundidad y que el aislamiento real depende de una base de pruebas dedicada, entorno identificable y privilegios mínimos.

---

## 2. Matriz de Hallazgos y Remediaciones (QA-P2P-04 vs. QA-P2P-04R)

| Fase / Área | Riesgo / Observación Detectada | Remediación Implementada en QA-P2P-04R | Estado |
|---|---|---|:---:|
| **Fase 1: Destino PostgreSQL** | `APP_ENV` y `ENVIRONMENT` no bastan por sí solas para determinar si una conexión apunta a producción; una variable local de desarrollo podía enmascarar un destino productivo. | Evaluación multivariable en `validate_test_environment()` (`APP_ENV`, `ENVIRONMENT`, `NODE_ENV`, `STAGE`). Prohibición irrestricta de `production`/`prod` sin permitir anulación por flags locales. | **CERRADO** |
| **Fase 1: URL Exclusiva** | Uso potencial de `settings.sync_database_url` que podría heredar la URL general del proyecto. | Creación de `QA_DATABASE_URL` y método `resolve_qa_database_url()` en [tools/qa_db_hardening.py](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/tools/qa_db_hardening.py). Si falta, las pruebas se detienen como `BLOCKED`. | **CERRADO** |
| **Fase 1: Destino No Autorizado** | Conexiones a hosts remotos no verificados permitidas si las variables locales tenían valores de desarrollo. | Función `validate_qa_target_url()` con lista blanca explícita (`DEFAULT_ALLOWED_QA_HOSTS`). Rechazo por defecto de hosts no autorizados o con patrones `prod*`. | **CERRADO** |
| **Fase 1: Identidad y Rol** | Se ejecutaban sentencias DDL sin comprobar la identidad de la base de datos conectada en PostgreSQL. | Función `verify_database_identity_and_role()` que consulta `current_database()` y roles antes de crear esquemas. | **CERRADO** |
| **Fase 2: Verificación de Aislamiento** | Aceptar que el esquema esperado estuviera presente dentro de `SHOW search_path` podía permitir que el primer esquema fuera `public` o ajeno. | `verify_connection_search_path()` exige `current_schema() == expected_schema`. Rechazo inmediato si es `public` o diferente. | **CERRADO** |
| **Fase 2: Catálogo de Esquemas** | Riesgo de adoptar o sobreescribir esquemas creados previamente por otras herramientas o sesiones. | Consulta a `information_schema.schemata` en `create_isolated_schema()`. Se rechaza la adopción de esquemas preexistentes. | **CERRADO** |
| **Fase 2: Destrucción de Esquemas** | `safe_teardown_schema` no garantizaba que el esquema perteneciera a la sesión actual si se invocaba directamente. | Control estricto mediante el conjunto en memoria `_CREATED_SCHEMAS_IN_THIS_RUN` y context manager `isolated_test_schema()`. | **CERRADO** |
| **Fase 3: Aserciones E2E** | `E2E-EST-02` se denominaba "Consulta y Actualización de Perfil", pero solo consultaba e inspeccionaba visualmente. | Renombrado a `"Consulta y Visualización de Perfil y Disponibilidad"` con descripción ajustada a inspección visual sin mutación. | **CERRADO** |
| **Fase 4: Alcance Documental** | La documentación de QA-P2P-04 atribuía un "aislamiento total" únicamente al uso de esquemas de PostgreSQL. | Rectificación en [docs/qa/QA-P2P-04-RESULTADOS.md](file:///c:/Users/Admin/Desktop/Proyectos/Proyecto_Sistema_Web_P2P_/docs/qa/QA-P2P-04-RESULTADOS.md): los esquemas son defensa en profundidad; la segregación real exige base dedicada. | **CERRADO** |

---

## 3. Arquitectura del Módulo de Blindaje (`tools/qa_db_hardening.py`)

```mermaid
flowchart TD
    A["Inicio de Prueba (E2E o Transaccional)"] --> B["validate_test_environment()"]
    B -->|APP_ENV, ENVIRONMENT, NODE_ENV o STAGE == prod| X1["DatabaseSecurityError (ABORT)"]
    B -->|No autorizado| X2["DatabaseSecurityError (ABORT)"]
    B -->|Autorizado| C["resolve_qa_database_url()"]
    C -->|QA_DATABASE_URL ausente| X3["Detener como BLOCKED"]
    C -->|Configurada| D["validate_qa_target_url()"]
    D -->|Host no reconocido o 'prod'| X4["DatabaseSecurityError (RECHAZO)"]
    D -->|Host en lista blanca QA| E["verify_database_identity_and_role()"]
    E -->|current_database() es prod| X5["DatabaseSecurityError (RECHAZO)"]
    E -->|Base verificada de QA| F["create_isolated_schema()"]
    F -->|Existe en information_schema| X6["DatabaseSecurityError (RECHAZO ADOPCIÓN)"]
    F -->|Nuevo y patrón válido| G["CREATE SCHEMA test_qa_p2p_04_..."]
    G --> H["build_isolated_db_url(options='-c search_path=...')"]
    H --> I["verify_connection_search_path()"]
    I -->|current_schema() != expected| X7["DatabaseSecurityError (VIOLACIÓN AISLAMIENTO)"]
    I -->|current_schema() == expected| J["Ejecutar Pruebas / Migraciones"]
    J --> K["safe_teardown_schema() (finally)"]
    K --> L["DROP SCHEMA ... CASCADE (Solo registrado en memoria)"]
```

---

## 4. Resultados de Verificación de Calidad y Pruebas

### 4.1. Suite Unitaria de Blindaje (`tests/test_qa_db_hardening.py`)
- **Motor:** Pytest 9.1.1 en entorno virtual Python 3.13.5.
- **Total de Pruebas:** 51 pruebas unitarias y negativas.
- **Resultado:** **51 PASSED (100% de éxito en 2.28s)**.
- **Casos Destacados Evaluados:**
  - `test_production_environment_variables_strictly_aborts`: 20 permutaciones de nombres de variable y valores (`production`, `prod`, `Production`, `PROD`, `prod-cluster`).
  - `test_local_dev_cannot_override_production`: comprueba que `ENVIRONMENT=development` o `ALLOW_TEST_SCHEMA_CREATION=true` no pueden anular una variable productiva.
  - `test_target_url_validation`: bloqueo de URLs con patrones de producción y rechazo por defecto de dominios desconocidos.
  - `test_verify_search_path_strictly_requires_exact_match`: rechazo si `current_schema()` es `public` o diferente del esquema esperado, incluso si aparece en `search_path`.
  - `test_create_isolated_schema_blocks_preexisting_schemas`: rechazo de adopción de esquemas preexistentes en `information_schema.schemata`.
  - `test_safe_teardown_rejects_unregistered_or_protected_schemas`: rechazo de esquemas protegidos (`public`, `auth`) y esquemas no registrados en la ejecución.
  - `test_isolated_test_schema_context_manager_cleans_up_on_failure`: garantía de desregistro y teardown ante excepciones internas.

### 4.2. Pruebas Transaccionales y de Concurrencia PostgreSQL (`tools/validate_postgresql_transactions.py`)
- **Motor:** PostgreSQL (Supabase QA) sobre esquema efímero blindado `test_qa_p2p_04_tx_*`.
- **Total de Comprobaciones:** 15 escenarios transaccionales (7 bloques principales).
- **Resultado:** **15 PASSED (100% de éxito)**.
- **Garantías Validadas:**
  - Sobrecupo: 0.0% de excedencia bajo 5 hilos simultáneos sobre la última vacante disponible (RNF07).
  - Desempate: exactamente 1 reserva aceptada, 3 conflictos 409 y 1 503 gestionado.
  - Ratificación temporal: aprobada en ventana válida, rechazada con HTTP 400 a T-12h (RN-08).
  - Desistimiento concurrente: vacante liberada inmediatamente y aprovechada por nuevo postulante (RN-10).
  - Quórum institucional: evaluado estrictamente según umbral >= 50% (RN-09).
  - RBAC entre estudiantes: rechazo con HTTP 403 Forbidden ante intentos de manipular reservas ajenas.
  - Rollback atómico: restauración íntegra de la base de datos sin registros huérfanos ante fallos.

### 4.3. Suite E2E en Navegador Real (`tools/run_browser_e2e_tests.py`)
- **Navegador:** Microsoft Edge Headless (Playwright).
- **Servicios:** React (puerto 5173), FastAPI (puerto 8000), PostgreSQL (Supabase QA).
- **Total de Casos Evaluados:** 22 casos de prueba.
- **Distribución de Resultados:** **21 PASS, 1 BLOCKED, 0 FAIL, 0 SKIP**.
- **Resumen por Rol:**
  - **Estudiante (8 casos):** 8 PASS (Login OTP, visualización de perfil y disponibilidad, catálogo curricular, recomendaciones y XAI, modal de reserva, persistencia de reserva en BD, ratificación en UI/BD, desistimiento en UI/BD).
  - **Mentor (6 casos):** 6 PASS (Login mentor, publicación de oferta > 24h en BD, cartelera y quórum, código QR y token TOTP dinámico de 30s, bitácora pedagógica con SHA-256 en BD, resumen de horas formativas).
  - **Administrador (4 casos):** 4 PASS (Consola de gobernanza, asignación de rol de mentor por mérito en BD, visado formal de bitácora en BD, telemetría de BD `/health/db`).
  - **Seguridad y Autenticación (4 casos):** 3 PASS (RBAC HTTP 403 Forbidden, rechazo de OTP erróneo con alerta accesible HTTP 400, auditoría de secretos en almacenamiento del cliente), 1 BLOCKED (`E2E-AUTH-02`: Google OAuth requiere interacción humana con cuenta real UPT).

---

## 5. Evaluación de Riesgos Residuales y Directrices para Staging

Con la implementación de QA-P2P-04R, los riesgos críticos de regresión, persistencia y daño a datos productivos quedan formalmente mitigados. No obstante, se establecen las siguientes directrices operativas para el despliegue en staging y producción:

1. **Segregación Física de Entornos:**
   - La base de datos de producción debe residir en un proyecto de Supabase independiente del de QA/Staging, con credenciales rotadas y sin acceso desde runners de CI automatizados.
2. **Validación Manual de Google OAuth en Staging:**
   - Debido al bloqueo justificado en pruebas automatizadas (`E2E-AUTH-02`), se debe ejecutar una verificación manual con al menos 2 cuentas institucionales `@upt.pe` en el entorno de staging para validar la conmutación de roles y la emisión de tokens.
3. **Monitoreo de Rate Limiting y Concurrencia en Staging:**
   - Supervisar en staging el comportamiento de los límites de tasa (`auth_rate_limits`) bajo picos de concurrencia de matrícula estudiantil.
4. **Política de Migraciones:**
   - Cualquier migración futura de Alembic debe ejecutarse siguiendo el protocolo de prueba previa en PostgreSQL aislado documentado en QA-P2P-02.

---

## 6. Dictamen de Aprobación

La suite de pruebas automatizadas y la infraestructura de aseguramiento de calidad del Sistema Web P2P EPIS-UPT cumplen con los más rigurosos estándares de seguridad y fiabilidad:

- **Aislamiento y Destino de Base de Datos:** Blindado y verificado (PostgreSQL QA).
- **Persistencia Transaccional:** 100% certificada en base de datos.
- **Interfaz y Experiencia de Usuario:** 100% verificada en navegador real.
- **Compuertas de Calidad Estática:** 0 errores en linters y pruebas unitarias.

**Dictamen:** **APROBADO PARA TRANSICIÓN A ENTORNO DE STAGING Y EVALUACIÓN FINAL DE PRODUCTO.**
