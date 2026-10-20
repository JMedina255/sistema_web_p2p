# Reglas Estándares de Documentación del Proyecto — Fase de Diseño

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT<br>
**Curso:** Construcción de Software I<br>
**Institución:** Universidad Privada de Tacna – Escuela Profesional de Ingeniería de Sistemas<br>
**Equipo Consultor:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)<br>
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado<br>
**Vigencia:** Semestre 2026-II<br>

---

## Control de Versiones

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcarcel | Dirección EPIS | 19/10/2026 | Emisión formal de las directrices para la Fase de Diseño: evolución técnica del SAD (FD04) y SRS (FD03), especificación exhaustiva de contratos de API REST, diccionario de datos físico PostgreSQL/RLS, modelado técnico en PlantUML y gestión de artefactos de evidencia complementaria. |

---

## 1. Propósito y Alcance

Establecer las directrices metodológicas, arquitectónicas y de ingeniería de software para la **Fase de Diseño del Sistema**, normando la transición desde la línea base de requerimientos analíticos hacia el diseño formal de la solución técnica.

El alcance de estas reglas aplica a:
1. **Documentos Maestros de Ingeniería:**
   * **Documento de Arquitectura de Software (SAD - FD04):** Modelo de 4+1 vistas de Kruchten + UWE.
   * **Especificación de Requerimientos de Software (SRS - FD03):** Refinamiento técnico y alineamiento con el diseño.
2. **Artefactos y Evidencia Complementaria:**
   * **Diccionario de Datos Físico:** Especificación detallada de entidades relacionales, DDL, índices, restricciones y políticas RLS.
   * **Estándar de Programación y Arquitectura de Código:** Guías de tipado, linteo, estructura desacoplada y manejo de excepciones.
   * **Catálogo y Documento de Evidencia de Pruebas:** Trazabilidad de suites automatizadas, fixtures, mocks y reportes de cobertura (Vitest / Pytest).
3. **Bóveda de Diagramas:** Sincronización continua de diagramas de interacción y diseño técnico en [`docs/diagramas_general.md`](file:///d:/sistema_web_p2p/docs/diagramas_general.md).

---

## 2. Reglas Fundamentales de la Fase de Diseño

### Regla D-1: Enfoque Prescriptivo y Técnico de Diseño (SAD y SRS)
* **Transición Metodológica:** A diferencia de la fase de análisis (donde primó la conceptualización y la narrativa de necesidades institucionales), la **fase de diseño es prescriptiva, determinista y técnica**. Debe especificar *cómo* el software satisface cada requerimiento (**RF01–RF26**, **RNF01–RNF10**, **RN-01–RN-14**).
* **Consistencia de Nomenclatura:** Se preservan con rigor absoluto los códigos canónicos del SRS (`MOD-01` a `MOD-08`, `RF01`–`RF26`, `CUS01`–`CUS24`). Ningún documento de diseño puede renombrar o alterar códigos de casos de uso ni omitir dependencias funcionales aprobadas.
* **Trazabilidad Bidireccional:** Todo componente de software, endpoint REST, tabla relacional o servicio en segundo plano debe declarar su trazabilidad explícita hacia los requerimientos funcionales y reglas de negocio que implementa.

---

### Regla D-2: Estructura Canónica Quíntuple Obligatoria para Tablas y Cuadros
Se mantiene con carácter vinculante la **Regla de los 5 Elementos Secuenciales** para toda tabla o cuadro Markdown que se elabore en la fase de diseño:

1. **Presentación Previa Contextualizada:** Párrafo narrativo introductorio que explica qué necesidad técnica o arquitectónica motiva el cuadro y qué decisiones se presentan.
2. **Título Formal Numerado:** Encabezado descriptivo en sintaxis Markdown (ej. `### Cuadro 7.2: Contrato de Especificación de Endpoints del Módulo de Autenticación`).
3. **Tabla Markdown:** Alineación explícita de columnas, codificación limpia UTF-8 y ausencia de celdas ambiguas.
4. **Fuente Formal:** Declaración formal inmediatamente debajo de la tabla (`Fuente: Elaboración propia.`).
5. **Análisis, Interpretación y Conclusiones:** Párrafo posterior analizando el impacto de los datos en la arquitectura, validando restricciones, implicancias de seguridad o decisiones de integración.

---

### Regla D-3: Especificación Exhaustiva de Contratos de API REST y Componentes
Toda especificación de interfaz o servicio backend en el SAD o artefactos complementarios debe definirse a **nivel exhaustivo de contrato técnico**, incluyendo obligatoriamente:

1. **Ficha de Ruta y Método:** Verbo HTTP (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) y ruta canónica versionada (ej. `/api/v1/auth/otp/verify`).
2. **Códigos de Estado HTTP:** Respuestas tipadas de éxito (`200 OK`, `201 Created`) y códigos canónicos de error (`400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `422 Unprocessable Entity`), indicando el código de error institucional interno (ej. `OTP_EXPIRED`, `INVALID_EMAIL`).
3. **Contratos de Payload JSON (Request / Response):** Esquemas tipados Pydantic / TypeScript documentados con nombres de campos, tipos primitivos, obligatoriedad y ejemplos reales.
4. **Validaciones y Reglas de Negocio en la Capa de API:** Límites de caracteres, regex de dominios institucionales (`@upt.pe`), ventanas de tiempo de expiración y políticas de sanitización de datos.

```markdown
<!-- Ejemplo de Aplicación de la Regla D-3 -->
A continuación, se detalla el contrato formal de comunicación para la verificación del desafío OTP institucional...

### Cuadro X.Y: Especificación de Endpoint — POST /api/v1/auth/otp/verify

| Parámetro | Tipo | Ubicación | Obligatorio | Regla de Validación / Descripción |
| :--- | :--- | :--- | :---: | :--- |
| `challenge_id` | UUIDv4 | Body (JSON) | Sí | Identificador único emitido en la solicitud previa. |
| `otp_code` | String(6) | Body (JSON) | Sí | Expresión regular `^[0-9]{6}$`. Conservado como texto. |

Fuente: Elaboración propia.

El endpoint retorna HTTP 200 con el token JWT de sesión de 8 horas ante verificación exitosa, o HTTP 400 ante código expirado...
```

---

### Regla D-4: Diccionario de Datos Físico y Seguridad RLS en PostgreSQL/Supabase
El diseño de persistencia en el SAD y sus artefactos complementarios no debe limitarse a esquemas lógicos abstractos, sino documentar el **modelo relacional físico completo**:

1. **Fichas Físicas de Tablas:** Nombre de tabla en minúsculas snake_case, motor PostgreSQL, y tabla descriptiva con:
   * Nombre de columna.
   * Tipo de dato físico en PostgreSQL (`INTEGER`, `VARCHAR(n)`, `TEXT`, `BOOLEAN`, `TIMESTAMPTZ`, `UUID`).
   * Restricciones de columna (`PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK`).
   * Claves Foráneas (`REFERENCES tabla(columna) ON DELETE ...`).
   * Índices físicos y justificación de rendimiento (`B-Tree` sobre columnas filtradas/consultadas frecuentemente).
2. **Políticas de Seguridad a Nivel de Fila (RLS - Row Level Security):**
   * Declaración formal de activación (`ENABLE ROW LEVEL SECURITY`).
   * Tabla de políticas RLS: Nombre de la política, comando (`SELECT`, `INSERT`, `UPDATE`, `DELETE`), rol asignado (`anon`, `authenticated`, `service_role`), expresión `USING` y expresión `WITH CHECK`.
   * Mitigación de permisos para evitar el uso accidental de roles con bypass (`BYPASSRLS`).

---

### Regla D-5: Diagramación Técnica Detallada en PlantUML (Interacción Real de Arquitectura)
Todos los diagramas generados en la fase de diseño deben respetar:

* **Sincronización Continua:** Todo nuevo diagrama se incorpora en el documento correspondiente y se replica de inmediato en la bóveda consolidada [`docs/diagramas_general.md`](file:///d:/sistema_web_p2p/docs/diagramas_general.md).
* **Nivel Técnico de Secuencia e Interacción:** Los diagramas de secuencia de diseño deben modelar la interacción técnica real entre las capas de la arquitectura desacoplada:
  ```text
  React Component (UI) -> apiClient (TypeScript) -> FastAPI Router -> Service Layer -> SQLAlchemy ORM -> PostgreSQL/Supabase
  ```
* **Estilo Gráfico Sobrio y Limpio:** Directivas PlantUML sobrias (`skinparam shadowing false`, `defaultFontName Arial`, sin degradados pesados), señalando explícitamente llamadas asíncronas, códigos HTTP de retorno y bloques de captura de excepción (`alt / else` o `opt`).

---

### Regla D-6: Artefactos de Evidencia Complementaria y Estándares de Programación
Para respaldar las evaluaciones de cátedra y auditorías de software, la fase de diseño se complementa con tres artefactos vivos:

1. **Diccionario de Datos Físico:** Documento o sección viva que centraliza la totalidad de tablas, vistas, extensiones (ej. `pgvector`, `uuid-ossp`) y políticas RLS del sistema.
2. **Estándar de Programación y Arquitectura de Código:** Normas de codificación para el frontend (React 19, componentes funcionales, hooks, tipado estricto) y backend (FastAPI, inyección de dependencias `Depends(get_db)`, tipado estricto Pydantic v2, linteo Ruff/ESLint).
3. **Catálogo y Registro de Evidencia de Pruebas:** Matriz viva vinculando cada caso de uso y requerimiento con su archivo de prueba automatizada, tipo de prueba (unitaria, integración, mock de persistencia) y métrica de cobertura lograda ($\ge 70\%$ conforme a **RNF09**).

---

### Regla D-7: Documentación Obligatoria de Máquinas de Estado y Transiciones
Toda entidad de dominio que posea un atributo de estado (ej. `estado_sesion`, `estado_auditoria`, ciclo de vida del desafío OTP, estado de reserva de cupo) debe documentarse formalmente mediante:

1. **Diagrama de Estados en PlantUML:** Bloque `@startuml` con sintaxis `[*] --> Estado`, mostrando cada estado válido como nodo y cada transición permitida como arco dirigido con su condición de guarda (`[condición]`) y el actor o evento que la dispara.
2. **Tabla de Transiciones Válidas:** Cuadro Markdown (con estructura quíntuple D-2) que enumere exhaustivamente:
   * Estado de origen.
   * Estado de destino.
   * Evento o acción que dispara la transición.
   * Condición de guarda (precondición lógica que debe cumplirse).
   * Actor o componente responsable.
3. **Lista Explícita de Transiciones Prohibidas:** Declaración formal de las combinaciones origen→destino que el sistema **nunca debe permitir**, junto con la justificación de negocio o seguridad. El programador no debe deducir qué transiciones son inválidas por descarte; deben estar enumeradas.

```markdown
<!-- Ejemplo de Aplicación de la Regla D-7 -->
### Cuadro X.Y: Máquina de Estados del Desafío OTP (auth_challenges)

| Estado Origen | Estado Destino | Evento Disparador | Condición de Guarda | Actor |
| :--- | :--- | :--- | :--- | :--- |
| `activo` | `consumido` | Verificación exitosa del código | `otp_code` coincide Y `now < expires_at` | Estudiante vía API |
| `activo` | `expirado` | Expiración temporal | `now >= expires_at` | Sistema (evaluación lazy) |
| `activo` | `invalidado` | Nueva solicitud OTP del mismo email | Existe nuevo desafío activo | Sistema (AuthService) |

Fuente: Elaboración propia.

**Transiciones Prohibidas:**
| Transición | Justificación |
| :--- | :--- |
| `consumido` → `activo` | Un código verificado jamás puede reactivarse (RN-01). |
| `expirado` → `consumido` | Un código vencido no puede redimirse bajo ninguna circunstancia. |
| `invalidado` → `activo` | Un código reemplazado por uno nuevo no puede resucitar. |
```

---

### Regla D-8: Mapeo de Transformación de Datos entre Capas, Catálogo de Errores y Convenciones de Nombrado

#### D-8.1: Flujo de Transformación de Datos entre Capas Arquitectónicas
Para cada entidad o flujo de datos relevante, el diseño debe documentar explícitamente cómo se transforma la representación del dato al atravesar cada capa de la arquitectura desacoplada:

```text
Columna PostgreSQL → Atributo SQLAlchemy (Model) → Campo Pydantic (Schema) → JSON Response → Interface TypeScript → Estado React (useState/useReducer)
```

Se debe especificar en una tabla:
* Nombre del campo en cada capa (ej. `id_asignatura` en PostgreSQL, `id_asignatura` en SQLAlchemy, `id` en Pydantic con `alias`, `id` en JSON, `courseId` en TypeScript si se renombra, o aclarar que se mantiene idéntico).
* Tipo de dato en cada capa (ej. `INTEGER` → `int` → `int` → `number` → `number`).
* Transformaciones aplicadas (ej. serialización de `datetime` a ISO 8601, conversión de `UUID` a `string`).

El objetivo es que el programador **nunca tenga que adivinar** el nombre ni el tipo de un campo en ninguna capa.

#### D-8.2: Catálogo Centralizado de Códigos de Error
El sistema debe mantener un catálogo único y exhaustivo de todos los códigos de error internos. Cada entrada debe incluir:

| Campo del Catálogo | Descripción |
| :--- | :--- |
| **Código Interno** | Identificador canónico en UPPER_SNAKE_CASE (ej. `OTP_EXPIRED`, `COOLDOWN_ACTIVE`). |
| **Código HTTP** | Status HTTP asociado (ej. `400`, `401`, `403`, `404`, `422`). |
| **Mensaje para el Desarrollador** | Descripción técnica precisa del error. |
| **Mensaje para el Usuario (i18n)** | Texto en español que la interfaz puede mostrar al estudiante. |
| **Módulo / Endpoint Origen** | Ruta y servicio donde se genera el error. |
| **Regla de Negocio Vinculada** | Código de RN o RF que justifica el rechazo. |

El esquema JSON de toda respuesta de error debe ser uniforme y estar documentado una sola vez:
```json
{
  "detail": {
    "code": "OTP_EXPIRED",
    "message": "El código de verificación ha expirado. Solicite uno nuevo.",
    "http_status": 400
  }
}
```

#### D-8.3: Convenciones de Nombrado por Tecnología
Las siguientes convenciones son obligatorias y no admiten excepciones:

| Capa / Tecnología | Convención de Nombrado | Ejemplos |
| :--- | :--- | :--- |
| **PostgreSQL (tablas, columnas)** | `snake_case` en minúsculas, tablas en plural | `asignaturas`, `id_asignatura`, `temas_conceptuales` |
| **Python / FastAPI (variables, funciones, módulos)** | `snake_case` | `get_courses()`, `auth_service.py`, `challenge_id` |
| **Python / FastAPI (clases, modelos, schemas)** | `PascalCase` | `AsignaturaFiltro`, `OtpRequest`, `CurriculumService` |
| **TypeScript / React (variables, funciones, hooks)** | `camelCase` | `fetchCourses()`, `selectedCourse`, `useAuthState()` |
| **TypeScript / React (componentes, interfaces, tipos)** | `PascalCase` | `LoginOtpView`, `CurriculumCatalogView`, `AuthResponse` |
| **TypeScript / React (archivos de componente)** | `PascalCase.tsx` | `LoginOtpView.tsx`, `HealthStatus.tsx` |
| **TypeScript / React (archivos de servicio/util)** | `camelCase.ts` | `authService.ts`, `apiClient.ts` |
| **Archivos de prueba** | Prefijo `test_` (Python) o sufijo `.test.` (TS) | `test_auth.py`, `LoginOtpView.test.tsx` |
| **Endpoints REST (rutas URL)** | `kebab-case` o sustantivos en plural `snake_case` | `/api/v1/auth/otp/request`, `/api/v1/curriculum/courses` |
| **Variables de entorno** | `UPPER_SNAKE_CASE` | `DATABASE_URL`, `JWT_SECRET_KEY`, `CORS_ORIGINS` |
| **Ramas de Git** | `tipo/sNN-tNN-descripcion-corta` | `feat/s02-t10-consentimiento-digital` |
| **Mensajes de Commit** | `tipo(sNN-tNN): descripción [Requisitos]` | `feat(s01-t03): implementar API OTP [RF01, CUS01]` |

---

### Regla D-9: Ficha Obligatoria de Configuración y Variables de Entorno
Todo archivo de configuración (`.env`, `config.py`, `Settings`) debe estar acompañado por una **ficha de documentación de variables de entorno** en el SAD o artefacto complementario. Cada variable debe describirse con:

| Campo | Descripción |
| :--- | :--- |
| **Nombre** | Nombre exacto de la variable en `UPPER_SNAKE_CASE`. |
| **Tipo Esperado** | Tipo primitivo: `string`, `integer`, `boolean`, `json_array`, `url`. |
| **Obligatoria / Opcional** | Si el sistema puede arrancar sin ella o no. |
| **Valor por Defecto** | Qué valor asume el sistema si la variable no está definida. Si no hay default, declarar `—` y marcar como obligatoria. |
| **Efecto en el Comportamiento** | Descripción precisa de qué funcionalidad activa, desactiva o modifica. |
| **Ejemplo** | Valor ilustrativo realista (sin secretos reales). |
| **Sensibilidad** | `Pública` (puede estar en el repositorio), `Secreta` (solo en `.env` local, nunca en Git), `Restringida` (solo en CI/CD). |

```markdown
<!-- Ejemplo de Aplicación de la Regla D-9 -->
### Cuadro X.Y: Ficha de Variables de Entorno del Backend

| Variable | Tipo | Obligatoria | Default | Efecto | Ejemplo | Sensibilidad |
| :--- | :--- | :---: | :--- | :--- | :--- | :---: |
| `DATABASE_URL` | url | No | `None` (fallback a memoria) | Cadena de conexión PostgreSQL/Supabase. Si ausente, el sistema opera con almacenamiento en memoria volátil (no apto para producción). | `postgresql+psycopg://user:pass@host:5432/db` | Secreta |
| `JWT_SECRET_KEY` | string | Sí | — | Clave HMAC para firmar tokens JWT HS256. Sin ella, el sistema no puede emitir ni validar sesiones. | `clave_super_segura_p2p_2026` | Secreta |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | integer | No | `480` | Vigencia del token de sesión en minutos. 480 = 8 horas continuas (RNF01). | `480` | Pública |
| `ENVIRONMENT` | string | No | `production` | Controla comportamiento condicional: `development` habilita endpoint `/health/db` y mock OTP en consola. | `development` | Pública |
| `CORS_ORIGINS` | json_array | No | `[]` | Lista de orígenes permitidos para CORS. | `["http://localhost:5173"]` | Pública |

Fuente: Elaboración propia.
```

El programador debe poder configurar el entorno **copiando la ficha sin consultar el código fuente**.

---

### Regla D-10: Registro de Decisiones Arquitectónicas (ADR) y Documentación de Transaccionalidad

#### D-10.1: Registro de Decisiones Arquitectónicas (ADR)
Toda decisión de diseño relevante (elección de tecnología, patrón de arquitectura, algoritmo, protocolo de seguridad o trade-off) debe documentarse con una ficha breve de tipo **Architecture Decision Record** que responda:

| Campo del ADR | Contenido Requerido |
| :--- | :--- |
| **ID** | Código secuencial (`ADR-001`, `ADR-002`, ...). |
| **Título** | Decisión en una frase concisa. |
| **Fecha** | Fecha de la decisión. |
| **Estado** | `Aprobada`, `Propuesta`, `Reemplazada por ADR-XXX`. |
| **Contexto** | Problema o necesidad técnica que motivó la decisión. |
| **Decisión** | Qué se decidió hacer y con qué herramienta/patrón/protocolo. |
| **Alternativas Descartadas** | Opciones consideradas y razón concreta del rechazo. |
| **Consecuencias** | Ventajas obtenidas y limitaciones aceptadas. |
| **Requisitos Vinculados** | Códigos de RF, RNF o RN que la decisión satisface o impacta. |

```markdown
<!-- Ejemplo de Aplicación de la Regla D-10.1 -->
### ADR-003: Algoritmo de Firma JWT con HS256

| Campo | Detalle |
| :--- | :--- |
| **ID** | ADR-003 |
| **Fecha** | 19/10/2026 |
| **Estado** | Aprobada |
| **Contexto** | Se requiere emitir tokens de sesión para autenticación OTP sin depender de un servicio externo de identidad. |
| **Decisión** | Firmar tokens JWT con HMAC-SHA256 (HS256) usando una clave simétrica almacenada en `JWT_SECRET_KEY`. |
| **Alternativas Descartadas** | RS256 (asimétrica): descartada porque agrega complejidad de gestión de par de claves sin beneficio en un sistema monolítico de backend único. Supabase Auth nativo: descartado temporalmente porque el flujo OTP institucional `@upt.pe` requiere control fino del dominio y cooldown. |
| **Consecuencias** | (+) Simplicidad de implementación, sin dependencia de PKI. (−) La clave secreta debe protegerse rigurosamente; rotación manual. |
| **Requisitos Vinculados** | RF01, RNF01, RN-01 |
```

#### D-10.2: Documentación de Transaccionalidad y Comportamiento ante Fallo
Para toda operación que involucre más de una escritura en base de datos o efectos colaterales (envío de correo, invalidación de caché, actualización de contadores), se debe documentar:

1. **Límite Transaccional:** Indicar si la operación completa está envuelta en una transacción de base de datos (`session.begin()`) o si cada paso es independiente.
2. **Comportamiento ante Fallo Parcial:** Describir qué ocurre si la operación falla a mitad de camino:
   * ¿Se ejecuta rollback automático?
   * ¿Quedan datos huérfanos o inconsistentes?
   * ¿Se registra el error en auditoría?
3. **Idempotencia:** Indicar si la operación es segura de reintentar (idempotente) o si un segundo intento genera efectos duplicados.
4. **Orden de Operaciones:** Secuencia numerada y explícita de cada paso de escritura/efecto, para que el programador los implemente en el orden correcto.

```markdown
<!-- Ejemplo de Aplicación de la Regla D-10.2 -->
### Cuadro X.Y: Transaccionalidad de la Operación "Solicitar Nuevo OTP"

| Paso | Operación | Transaccional | Ante Fallo |
| :---: | :--- | :---: | :--- |
| 1 | Buscar desafíos activos previos del email | Lectura | — |
| 2 | Marcar desafíos previos como `consumed = True` | Escritura (misma tx) | Rollback completo |
| 3 | Insertar nuevo registro `auth_challenges` | Escritura (misma tx) | Rollback completo |
| 4 | Commit de la transacción | Commit | Si falla, ningún dato persiste |
| 5 | Imprimir OTP en consola (dev) o enviar email (prod) | Efecto colateral fuera de tx | El desafío existe en BD pero el usuario no recibe el código; puede reintentar tras cooldown |

Fuente: Elaboración propia.

**Idempotencia:** No idempotente. Cada invocación genera un nuevo `challenge_id` e invalida los anteriores. El cooldown de 60 segundos (CUS01) previene abuso por reintentos rápidos.
```

---

## 3. Matriz de Cumplimiento de Reglas de Diseño

| Componente de Documentación | Regla Vinculante | Criterio de Aprobación de Calidad |
| :--- | :--- | :--- |
| **SAD (FD04) y SRS (FD03)** | Regla D-1 | Lenguaje técnico prescriptivo, trazabilidad a RF/RN/CUS, sin alterar códigos canónicos. |
| **Cuadros y Tablas Técnicas** | Regla D-2 | Estructura quíntuple (Presentación, Título, Tabla MD, Fuente, Análisis). |
| **Especificación de APIs** | Regla D-3 | Contratos completos con verbos HTTP, códigos de estado, esquemas JSON y validaciones. |
| **Diseño de Base de Datos** | Regla D-4 | Diccionario físico (tipos Postgres, FK, índices) y especificación formal de políticas RLS. |
| **Diagramas de Interacción** | Regla D-5 | PlantUML técnico detallado (React → FastAPI → SQLAlchemy → Postgres) sincronizado en `diagramas_general.md`. |
| **Evidencias Complementarias** | Regla D-6 | Diccionario de datos, estándar de programación y catálogo de pruebas automatizadas (>70% cov). |
| **Entidades con Estado** | Regla D-7 | Diagrama de estados PlantUML, tabla de transiciones válidas y lista explícita de transiciones prohibidas. |
| **Transformación de Datos y Errores** | Regla D-8 | Mapeo campo-por-campo entre capas, catálogo centralizado de errores y convenciones de nombrado por tecnología. |
| **Configuración y Entorno** | Regla D-9 | Ficha de cada variable `.env` con tipo, obligatoriedad, default, efecto y sensibilidad. |
| **Decisiones Arquitectónicas y Transaccionalidad** | Regla D-10 | ADR con contexto/alternativas/consecuencias, y fichas de transaccionalidad con orden de operaciones y comportamiento ante fallo. |
