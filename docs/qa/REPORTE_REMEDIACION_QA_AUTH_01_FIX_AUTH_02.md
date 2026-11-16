# Informe Técnico de Remediación Integral: Autenticación, OTP, SMTP y Google Auth
## Hitos QA-AUTH-01 / FIX-AUTH-02 — Sistema Web P2P de Mentorías Académicas EPIS UPT

---

### 1. Ficha Técnica del Hito

| Parámetro | Detalle Institucional |
| :--- | :--- |
| **Proyecto** | Sistema Web P2P de Mentorías Académicas — EPIS Universidad Privada de Tacna |
| **Repositorio Remoto** | `https://github.com/JMedina255/sistema_web_p2p.git` |
| **Rama Base Auditada** | `main` (commit base `df871a0`) |
| **Rama de Remediación** | `fix/qa-auth-remediation` |
| **Rol Técnico** | Senior Security & Fullstack Software Engineer |
| **Entorno Tecnológico** | FastAPI 0.115+, PostgreSQL / Supabase, SQLAlchemy 2.0+, React 19, TypeScript 5.7+, Vite 5, Tailwind CSS |
| **Estado de Certificación** | **100% PASS** (16/16 Diagnósticos, 363/363 Pytest Backend, 366/366 Vitest Frontend, ESLint 0 errores, Build Limpio) |

---

### 2. Resumen Ejecutivo

Durante el hito **QA-AUTH-01** se identificaron 8 fallos confirmados distribuidos en 10 hallazgos técnicos (**H-01 a H-10**), que comprometían la seguridad perimetral de autenticación y la experiencia de usuario:
1. **Google Identity Bypass (H-01 / P0):** El backend decodificaba tokens JWT de Google con `verify_signature: False` si el endpoint de `tokeninfo` no respondía, admitiendo identidades arbitrarias falsificadas con claves simétricas locales.
2. **Desacoplamiento SMTP y Falso Positivo UI (H-02 / P0):** El endpoint `/api/v1/auth/otp/request` ignoraba el retorno `False` de `EmailService.send_otp_email` y retornaba `HTTP 200` con mensaje de éxito, dejando desafíos activos sin que el correo fuese despachado.
3. **Generación de Tokens Ficticios en Cliente (H-03 / P0):** El componente React `LoginOtpView.tsx` fabricaba un `dummyIdToken` base64 con firma simulada cuando Google Identity Services tardaba en cargar, vulnerando el principio de segregación de entornos.
4. **Vulnerabilidad a Fuerza Bruta sobre OTP (H-04 / P0):** El modelo `AuthChallenge` no limitaba los intentos fallidos, permitiendo ataques de adivinación de 6 dígitos sin invalidar el código.
5. **Degradación Silenciosa a Memoria (H-05 / P1):** Los endpoints inyectaban `get_optional_session` en lugar de `get_required_session`, lo que provocaba que una falla de conexión con PostgreSQL/Supabase degradara el almacenamiento de credenciales a memoria volátil aún con `STRICT_DATABASE_MODE=True`.
6. **Inconsistencia Terminológica en Especificaciones (H-10 / P2):** El SRS y SAD catalogaban el flujo como "2FA sin contraseña", cuando técnicamente es una autenticación de factor único sin contraseña (*1FA Passwordless Email OTP / Google SSO*).

En el hito **FIX-AUTH-02** se implementó la remediación integral de todos los hallazgos sin alterar los módulos académicos preexistentes (mentorías, reservas, asistencias QR, quórum, bitácoras y certificados).

---

### 3. Matriz de Trazabilidad Integral (H-01 a H-10)

| ID | Sev. | Defecto / Causa Raíz | Archivos y Componentes Modificados | Remediación Implementada | Pruebas de Verificación |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **H-01** | **P0** | Bypass de firma en Google Auth (`verify_signature: False`) | `aplicacion/backend/app/services/auth_service.py` (L580-L640), `requirements.txt`, `pyproject.toml` | Se eliminó `verify_signature: False`. Se implementó validación criptográfica estricta con `google.oauth2.id_token.verify_oauth2_token` y transporte HTTP oficial (`google.auth.transport.requests.Request`), validando `aud` contra `GOOGLE_CLIENT_ID`, emisor autorizado (`accounts.google.com`), expiración y correo verificado. | `test_google_auth.py` (8/8 tests PASS), Diagnóstico `AUTH-12`, `AUTH-13`, `AUTH-14` |
| **H-02** | **P0** | `request_otp` ignora fallo SMTP retornando HTTP 200 | `aplicacion/backend/app/services/auth_service.py` (L235-L270), `app/schemas/auth.py` | Se evalúa el retorno booleano de `EmailService.send_otp_email()`. Si el despacho falla, se invalida el desafío confirmado (`consumed = True`), se descarta en base de datos y se responde `HTTP 502 Bad Gateway` con código `EMAIL_DISPATCH_FAILED`. | `test_auth.py::test_request_otp_smtp_failure_returns_502_and_invalidates_challenge`, Diagnóstico `AUTH-04` |
| **H-03** | **P0** | Fallback cliente fabrica `dummyIdToken` en React | `aplicacion/frontend/src/components/LoginOtpView.tsx` (L155-L200) | Se erradicó la fabricación de tokens simulados en base64. Si Google Identity Services no está listo, se muestra una alerta institucional guiando al usuario o sugiriendo reintentar / usar OTP institucional. | `LoginOtpView.test.tsx` (9 tests PASS), Vitest Frontend Suite |
| **H-04** | **P0** | Inexistencia de límite de intentos fallidos de OTP | `aplicacion/backend/app/services/auth_service.py` (L360-L430), `app/core/config.py`, `.env.example` | Se introdujo `MAX_OTP_ATTEMPTS=5` y bloqueo preventivo. Cada fallo incrementa el contador con bloqueo de fila en BD (`with_for_update()`); al alcanzar 5 intentos, el desafío se marca como consumido y se responde `HTTP 403 Forbidden` (`CHALLENGE_LOCKED`). | `test_auth.py::test_verify_otp_lockout_after_max_attempts`, Diagnóstico `AUTH-15` |
| **H-05** | **P1** | Degradación silenciosa a memoria volátil | `aplicacion/backend/app/api/v1/endpoints/auth.py` (L1-L77), `app/services/auth_service.py` (L65-L79) | Se sustituyó `get_optional_session` por `get_required_session`. En `AuthService` se implementó `_assert_db_strict_check`, respondiendo `HTTP 503 Service Unavailable` (`DATABASE_UNAVAILABLE`) cuando la base de datos no está disponible en modo estricto. | `test_auth.py::test_auth_endpoints_strict_db_mode_down_returns_503`, Diagnóstico `AUTH-11` |
| **H-06** | **P1** | `GOOGLE_CLIENT_ID` no sincronizado entre frontend y backend | `aplicacion/backend/app/core/config.py`, `.env`, `.env.example` | Se sincronizó el Client ID institucional oficial: `542248584798-ev9m68d5ial7g4bghqiatd1r3b5rduls.apps.googleusercontent.com` tanto en backend como en frontend. | `test_google_auth.py::test_google_login_rejects_wrong_audience` |
| **H-07** | **P1** | Ambigüedad en contratos de entrega (3 estados) | `aplicacion/backend/app/schemas/auth.py`, `aplicacion/frontend/src/services/authService.ts` | Se enriqueció `RequestOtpResponse` con `deliveryStatus` (`"dispatched" | "mocked" | "failed"`) y `emailDispatched: boolean`. El frontend ahora discrimina transparentemente si el OTP fue enviado por SMTP o impreso en consola de desarrollo. | `test_auth.py::test_request_otp_smtp_disabled_reports_mocked`, Diagnóstico `AUTH-03` |
| **H-08** | **P1** | Ausencia de limitación de tasa (Rate Limiting) | `aplicacion/backend/app/services/auth_service.py` (L35-L65, L135-L155), `app/core/config.py` | Se incorporó limitación de frecuencia configurable `OTP_RATE_LIMIT_PER_MINUTE=5` por IP cliente y por correo institucional en solicitudes de OTP y reenvíos, arrojando `HTTP 429 Too Many Requests`. | `run_auth_scenarios.py`, Diagnóstico `AUTH-09` |
| **H-09** | **P1** | Exposición insegura de `mockCodeHint` fuera de tests | `aplicacion/backend/app/services/auth_service.py` (L270, L395), `app/core/config.py`, `.env.example` | Se condicionó la emisión de `mockCodeHint` y el bypass `000000` a `ENABLE_MOCK_OTP_HINTS=True` Y `APP_ENV != "production"`. En producción, `mockCodeHint` es estrictamente `None`. | `test_email_service.py::test_auth_service_production_mode_strict_security` |
| **H-10** | **P2** | Inconsistencia de terminología "2FA" vs "Passwordless" | `docs/qa/REPORTE_REMEDIACION_QA_AUTH_01_FIX_AUTH_02.md` | Se formaliza la propuesta de homologación para reemplazar "2FA sin contraseña" por "Autenticación de Factor Único sin Contraseña (Passwordless Email OTP / Google Workspace)" en SRS y SAD. | Documentación técnica y trazabilidad de requerimientos |

---

### 4. Resultados de la Batería Diagnóstica (AUTH-01 a AUTH-16)

Ejecución automatizada mediante el arnés de verificación diagnóstica:

```
================================================================================
ID        | ESCENARIO                        | ESTADO | DETALLE / EVIDENCIA OBSERVADA
================================================================================
AUTH-01   | Solicitar OTP institucional válido | PASS   | HTTP 200, challengeId generado, validación @virtual.upt.pe
AUTH-02   | Correo externo no permitido      | PASS   | HTTP 422, validate_upt_email rechazó @gmail.com
AUTH-03   | SMTP deshabilitado               | PASS   | deliveryStatus='mocked', isMock=True, emailDispatched=False
AUTH-04   | Error de conexión SMTP           | PASS   | HTTP 502 EMAIL_DISPATCH_FAILED, desafío invalidado en BD
AUTH-05   | OTP correcto vigente             | PASS   | HTTP 200, token JWT emitido con claims y roles válidos
AUTH-06   | OTP incorrecto                   | PASS   | HTTP 400 OTP_INVALID, decrementa intentos restantes
AUTH-07   | OTP vencido                      | PASS   | HTTP 400 OTP_EXPIRED, rechaza códigos tras 5 minutos
AUTH-08   | Reutilización del OTP            | PASS   | HTTP 400 OTP_ALREADY_USED, anti-replay confirmado
AUTH-09   | Reenvío antes de 60 segundos     | PASS   | HTTP 429 COOLDOWN_ACTIVE, respeto estricto de 60s
AUTH-10   | Reenvío después del cooldown     | PASS   | HTTP 200, nuevo challengeId, anterior revocado en BD
AUTH-11   | Caída de BD en modo estricto     | PASS   | HTTP 503 DATABASE_UNAVAILABLE, sin fallback volátil
AUTH-12   | Token Google firma inválida      | PASS   | HTTP 401 INVALID_GOOGLE_TOKEN, firma HMAC/falsa rechazada
AUTH-13   | Token Google audiencia errónea   | PASS   | HTTP 401 INVALID_GOOGLE_TOKEN, aud discrepante rechazada
AUTH-14   | Token Google expirado / no verif | PASS   | HTTP 401 INVALID_GOOGLE_TOKEN, exp caducado rechazado
AUTH-15   | Múltiples OTP erróneos (fuerza b)| PASS   | HTTP 403 CHALLENGE_LOCKED al superar 5 intentos fallidos
AUTH-16   | Persistencia de sesión y JWT     | PASS   | HS256 verificado, claims sub/email/roles UPT íntegros
================================================================================
```

---

### 5. Certificación de Suites de Pruebas y Regresión

#### 5.1. Backend (FastAPI / Pytest)
- **Comando:** `pytest aplicacion/backend/tests --no-cov -q`
- **Resultado:** **363 passed** en 89.13s (0:01:29)
- **Suites críticas verificadas:**
  - `tests/test_auth.py`: 18 tests passed (incluyendo bloqueo por intentos, fallo SMTP 502, modo estricto 503).
  - `tests/test_google_auth.py`: 8 tests passed (firmas inválidas, aud incorrecta, emisor, expiración, correo institucional).
  - `tests/test_email_service.py`: 6 tests passed (MIME, mock dev, SMTP sync, manejo de excepciones, async send, modo producción estricto).
  - `tests/test_authorization.py`: 22 tests passed (RBAC, permisos y claims).
  - Módulos académicos restantes (attendance, bitacora, bookings, certificates, curriculum, offers, quorum): 309 tests passed sin regresiones.

#### 5.2. Frontend (React 19 / Vitest / TypeScript / ESLint)
- **Vitest:** `npm --prefix aplicacion/frontend test`
  - **Resultado:** **37 test files passed**, **366 tests passed** en 52.11s.
  - Verificados componentes críticos: `LoginOtpView.test.tsx` (9 tests), `apiAuthAdapter.test.ts` (12 tests), `authService.test.ts` (15 tests), `navigation.test.tsx` (14 tests).
- **ESLint:** `npm --prefix aplicacion/frontend run lint`
  - **Resultado:** Código de salida 0 (0 errores, 0 advertencias). Corregido tipado en `SessionAttendanceView.tsx` (`BarcodeDetector`).
- **Compilación TypeScript & Vite:** `npm --prefix aplicacion/frontend run build`
  - **Resultado:** `tsc -b && vite build` completado exitosamente en 2.67s. Salida de producción en `aplicacion/frontend/dist/`.

---

### 6. Propuesta de Homologación Terminológica (H-10)

#### 6.1. Diagnóstico del Conflicto Conceptual
En el documento `SRS.md` (secciones RF01, RNF01, CUS01) y en `SAD.md` se emplea la expresión:
> *"Autenticación de dos factores (2FA) sin contraseña mediante correo institucional..."*

Técnicamente, el envío de un código de un solo uso (OTP) a la bandeja de correo institucional constituye un **factor de posesión** (*posesión del buzón de correo*) sin requerir contraseña previa. Al no combinarse con un segundo factor independiente en el mismo proceso (como una contraseña o biométrico previo), el mecanismo es rigurosamente una:
> **"Autenticación de Factor Único sin Contraseña" (*Passwordless Single-Factor Authentication via Institutional Email OTP*)**.

Por su parte, el acceso vía Google Workspace SSO es una delegación de identidad federada (OIDC / OAuth 2.0) donde Google gestiona internamente las políticas de factores institucionales.

#### 6.2. Propuesta de Ajuste para SRS y SAD
Se recomienda que en la siguiente versión documental formal de `SRS.md` y `SAD.md` se apliquen los siguientes reemplazos:
1. **Reemplazo en Glosario y RF01:**
   - *Texto anterior:* "El sistema implementará autenticación 2FA sin contraseña..."
   - *Texto propuesto:* "El sistema implementará autenticación institucional sin contraseña (*Passwordless Authentication*) mediante código de verificación de un solo uso (OTP de 6 dígitos) despachado al correo institucional `@virtual.upt.pe` / `@upt.pe`, o alternativamente mediante federación de identidad institucional con Google Workspace (OAuth 2.0 / OpenID Connect)."
2. **Reemplazo en RNF01:**
   - *Texto propuesto:* "Los desafíos OTP tendrán una vigencia estricta de 5 minutos, un cooldown de reenvío de 60 segundos, control de tasa anti-abuso y un bloqueo preventivo tras 5 intentos fallidos consecutivos."

---

### 7. Parámetros de Configuración y Despliegue SMTP Real UPT

Para la puesta en marcha con despacho efectivo a buzones institucionales de la Universidad Privada de Tacna, configurar en el `.env` del servidor:

```env
# Modo de Aplicación y Persistencia
APP_ENV=production
STRICT_DATABASE_MODE=true

# Google Identity Services
GOOGLE_CLIENT_ID=542248584798-ev9m68d5ial7g4bghqiatd1r3b5rduls.apps.googleusercontent.com

# Servicio de Correo SMTP Institucional
SMTP_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USER=notificaciones.mentorias@upt.pe
SMTP_PASSWORD=<GOOGLE_WORKSPACE_APP_PASSWORD_16_CHARS>
SMTP_FROM_EMAIL=notificaciones.mentorias@upt.pe

# Parámetros de Seguridad OTP
OTP_EXPIRE_MINUTES=5
OTP_COOLDOWN_SECONDS=60
MAX_OTP_ATTEMPTS=5
OTP_RATE_LIMIT_PER_MINUTE=5
ENABLE_MOCK_OTP_HINTS=false
```

> **Nota Operativa:** Para el envío mediante Gmail / Google Workspace UPT, la cuenta del remitente debe contar con *Verificación en dos pasos* activada y generar una **Contraseña de Aplicación** de 16 caracteres. Adicionalmente, el dominio UPT debe tener alineados sus registros SPF (`v=spf1 include:_spf.google.com ~all`) y DKIM para asegurar que los correos no sean desviados a la carpeta de spam.

---

### 8. Estructura de Commits del Hito FIX-AUTH-02

La remediación se organizó en 6 paquetes de cambios atómicos y autovalidados:
1. `fix(auth): implementar validacion criptografica de google id token y eliminar bypass (H-01, H-03, H-06)`
2. `fix(auth): blindar verificacion otp con limite de intentos y bloqueo preventivo (H-04, H-08)`
3. `fix(email): gestionar ciclo de vida y despacho smtp con estados de entrega transparentes (H-02, H-07, H-09)`
4. `fix(session): forzar modo estricto de base de datos y erradicar tokens mock en api (H-05)`
5. `test(auth): incorporar suite de pruebas de diagnostico y regresion qa-auth`
6. `docs(qa): incorporar reporte de remediacion y matriz de trazabilidad fix-auth-02 (H-10)`
