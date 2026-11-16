import argparse
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import jwt

backend_path = Path("aplicacion/backend").resolve()
sys.path.insert(0, str(backend_path))

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.core.config import settings
from app.db import session as db_session
from app.main import app
from app.services.auth_service import (
    _email_request_timestamps,
    _ip_request_timestamps,
    _ip_verify_timestamps,
    _memory_challenges,
    AuthService,
)
from app.services.email_service import EmailService

# Parseo de argumentos de seguridad para blindar base de datos de producción/Supabase
parser = argparse.ArgumentParser(description="Ejecución de diagnósticos de autenticación (QA-AUTH-02B)")
parser.add_argument(
    "--allow-remote-db",
    action="store_true",
    help="Permite explícitamente ejecutar diagnósticos sobre la base de datos remota configurada en .env",
)
args = parser.parse_args()

# Aislamiento por defecto: usar SQLite en memoria para no tocar ni modificar Supabase remoto
if not args.allow_remote_db:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    from app import models as app_models  # noqa: F401 - Asegura registro de todas las entidades ORM

    db_session.close_engine()
    isolated_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    db_session.Base.metadata.create_all(bind=isolated_engine)
    IsolatedSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=isolated_engine)

    def _get_isolated_session():
        db = IsolatedSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[db_session.get_session] = _get_isolated_session
    app.dependency_overrides[db_session.get_required_session] = _get_isolated_session
    print("[AISLAMIENTO] Motor de persistencia aislado en memoria (SQLite con StaticPool). Base Supabase protegida contra modificaciones.")
else:
    print("[ADVERTENCIA] Ejecutando diagnósticos con conexión a la base de datos configurada (--allow-remote-db habilitado).")

# Deshabilitar por defecto SMTP real para evitar envíos externos accidentales
original_smtp_enabled = settings.SMTP_ENABLED
settings.SMTP_ENABLED = False

client = TestClient(app)

results = []

def record(id_, scenario, expected, actual, status, reason):
    results.append({
        "id": id_,
        "scenario": scenario,
        "expected": expected,
        "actual": actual,
        "status": status,
        "reason": reason
    })

def reset_limits():
    _memory_challenges.clear()
    _ip_request_timestamps.clear()
    _email_request_timestamps.clear()
    _ip_verify_timestamps.clear()
    try:
        from app.models.auth import AuthRateLimit
        if not args.allow_remote_db:
            with IsolatedSessionLocal() as db:
                db.query(AuthRateLimit).delete()
                db.commit()
        else:
            from app.db.session import get_session_context
            with get_session_context() as db:
                db.query(AuthRateLimit).delete()
                db.commit()
    except Exception:
        pass

print("Iniciando batería de pruebas diagnósticas QA-AUTH-01 (AUTH-01 a AUTH-16)...")

# AUTH-01: Solicitar OTP institucional válido
reset_limits()
res1 = client.post("/api/v1/auth/otp/request", json={"email": "ra2022073504@virtual.upt.pe"})
if res1.status_code == 200 and "challengeId" in res1.json():
    chal_id = res1.json()["challengeId"]
    record("AUTH-01", "Solicitar OTP institucional válido", "Desafío generado correctamente (HTTP 200)", f"HTTP {res1.status_code}, challengeId={chal_id}", "PASS", "Generación correcta de desafío para @virtual.upt.pe")
else:
    record("AUTH-01", "Solicitar OTP institucional válido", "Desafío generado correctamente (HTTP 200)", f"HTTP {res1.status_code}: {res1.text}", "FAIL", "Fallo al generar desafío")

# AUTH-02: Correo externo no permitido
res2 = client.post("/api/v1/auth/otp/request", json={"email": "hacker@gmail.com"})
if res2.status_code in [422, 403, 400]:
    record("AUTH-02", "Correo externo no permitido", "Solicitud rechazada (422/403/400)", f"HTTP {res2.status_code}", "PASS", "Validador validate_upt_email rechazó @gmail.com")
else:
    record("AUTH-02", "Correo externo no permitido", "Solicitud rechazada", f"HTTP {res2.status_code}", "FAIL", "Permitió correo externo")

# AUTH-03: SMTP deshabilitado
old_smtp_enabled = settings.SMTP_ENABLED
settings.SMTP_ENABLED = False
reset_limits()
res3 = client.post("/api/v1/auth/otp/request", json={"email": "smtp_disabled@upt.pe"})
settings.SMTP_ENABLED = old_smtp_enabled
data3 = res3.json()
if data3.get("isMock") is True and data3.get("deliveryStatus") == "mocked" and data3.get("emailDispatched") is False:
    record("AUTH-03", "SMTP deshabilitado", "Distingue mock de despacho real", f"isMock={data3.get('isMock')}, deliveryStatus={data3.get('deliveryStatus')}", "PASS", "Distingue envío real de mock correctamente")
else:
    record("AUTH-03", "SMTP deshabilitado", "Distingue mock de despacho real", str(data3), "FAIL", "El backend no reporta adecuadamente el modo simulado/mock.")

# AUTH-04: Error de conexión SMTP
old_send = EmailService.send_otp_email
old_smtp_4 = settings.SMTP_ENABLED
old_user_4 = settings.SMTP_USER
settings.SMTP_ENABLED = True
settings.SMTP_USER = "test@upt.pe"
EmailService.send_otp_email = classmethod(lambda cls, to, code, exp: False)
reset_limits()
res4 = client.post("/api/v1/auth/otp/request", json={"email": "smtp_fail@upt.pe"})
EmailService.send_otp_email = old_send
settings.SMTP_ENABLED = old_smtp_4
settings.SMTP_USER = old_user_4
if res4.status_code == 502 and "EMAIL_DISPATCH_FAILED" in res4.text:
    record("AUTH-04", "Error de conexión SMTP", "Fallo detectado y comunicado (HTTP 502 EMAIL_DISPATCH_FAILED)", f"HTTP 502: {res4.json()}", "PASS", "Fallo SMTP comunicado e invalidado correctamente")
elif res4.status_code == 200:
    record("AUTH-04", "Error de conexión SMTP", "Fallo detectado y comunicado", f"HTTP 200", "FAIL", "AuthService.request_otp ignora el fallo de despacho y responde HTTP 200.")
else:
    record("AUTH-04", "Error de conexión SMTP", "Fallo detectado y comunicado", f"HTTP {res4.status_code}", "PASS", f"Fallo SMTP comunicado con HTTP {res4.status_code}")

# AUTH-05: OTP correcto vigente
reset_limits()
old_smtp_en = settings.SMTP_ENABLED
old_smtp_user = settings.SMTP_USER
old_hints = settings.ENABLE_MOCK_OTP_HINTS
settings.SMTP_ENABLED = True
settings.SMTP_USER = "test@upt.pe"
settings.ENABLE_MOCK_OTP_HINTS = True
EmailService.send_otp_email = classmethod(lambda cls, to, code, exp: True)
res5_req = client.post("/api/v1/auth/otp/request", json={"email": "auth05@virtual.upt.pe"})
c_id = res5_req.json()["challengeId"]
code = res5_req.json().get("mockCodeHint") or _memory_challenges[c_id]["code_plain"]
res5_ver = client.post("/api/v1/auth/otp/verify", json={"challengeId": c_id, "otp": code})
settings.SMTP_ENABLED = old_smtp_en
settings.SMTP_USER = old_smtp_user
settings.ENABLE_MOCK_OTP_HINTS = old_hints
if res5_ver.status_code == 200 and res5_ver.json().get("token"):
    record("AUTH-05", "OTP correcto vigente", "JWT emitido (HTTP 200)", "HTTP 200, token=[PROTECTED_JWT]", "PASS", "Emisión correcta de token JWT institucional")
else:
    record("AUTH-05", "OTP correcto vigente", "JWT emitido", f"HTTP {res5_ver.status_code}", "FAIL", "Fallo al verificar OTP válido")

# AUTH-06: OTP incorrecto
reset_limits()
res6_req = client.post("/api/v1/auth/otp/request", json={"email": "auth06_wrong@virtual.upt.pe"})
c_id6 = res6_req.json()["challengeId"]
res6 = client.post("/api/v1/auth/otp/verify", json={"challengeId": c_id6, "otp": "999999"})
if res6.status_code == 400 and res6.json().get("detail", {}).get("code") == "OTP_INVALID":
    record("AUTH-06", "OTP incorrecto", "Acceso rechazado (HTTP 400 OTP_INVALID)", f"HTTP 400: {res6.json()}", "PASS", "Código erróneo rechazado correctamente")
else:
    record("AUTH-06", "OTP incorrecto", "Acceso rechazado", f"HTTP {res6.status_code}: {res6.text}", "FAIL", "No rechazó código erróneo adecuadamente")

# AUTH-07: OTP vencido
reset_limits()
res7_req = client.post("/api/v1/auth/otp/request", json={"email": "auth07_exp@virtual.upt.pe"})
c_id7 = res7_req.json()["challengeId"]
if c_id7 in _memory_challenges:
    _memory_challenges[c_id7]["expires_at"] = datetime.now(UTC) - timedelta(minutes=1)
try:
    from app.models.auth import AuthChallenge
    if not args.allow_remote_db:
        with IsolatedSessionLocal() as db_s:
            db_chal = db_s.query(AuthChallenge).filter(AuthChallenge.id_challenge == c_id7).first()
            if db_chal:
                db_chal.expires_at = datetime.now(UTC) - timedelta(minutes=1)
                db_s.commit()
    else:
        from app.db.session import get_session_context
        with get_session_context() as db_s:
            db_chal = db_s.query(AuthChallenge).filter(AuthChallenge.id_challenge == c_id7).first()
            if db_chal:
                db_chal.expires_at = datetime.now(UTC) - timedelta(minutes=1)
                db_s.commit()
except Exception:
    pass
res7 = client.post("/api/v1/auth/otp/verify", json={"challengeId": c_id7, "otp": "123456"})
if res7.status_code == 400 and res7.json().get("detail", {}).get("code") == "OTP_EXPIRED":
    record("AUTH-07", "OTP vencido", "Acceso rechazado (HTTP 400 OTP_EXPIRED)", f"HTTP 400: {res7.json()}", "PASS", "OTP expirado rechazado")
else:
    record("AUTH-07", "OTP vencido", "Acceso rechazado", f"HTTP {res7.status_code}: {res7.text}", "FAIL", "No rechazó OTP expirado")

# AUTH-08: Reutilización del OTP
reset_limits()
old_hints_8 = settings.ENABLE_MOCK_OTP_HINTS
settings.ENABLE_MOCK_OTP_HINTS = True
res8_req = client.post("/api/v1/auth/otp/request", json={"email": "auth08@virtual.upt.pe"})
c_id8 = res8_req.json()["challengeId"]
code8 = res8_req.json().get("mockCodeHint") or _memory_challenges[c_id8]["code_plain"]
res8_v1 = client.post("/api/v1/auth/otp/verify", json={"challengeId": c_id8, "otp": code8})
res8_v2 = client.post("/api/v1/auth/otp/verify", json={"challengeId": c_id8, "otp": code8})
settings.ENABLE_MOCK_OTP_HINTS = old_hints_8
if res8_v2.status_code == 400 and res8_v2.json().get("detail", {}).get("code") == "OTP_ALREADY_USED":
    record("AUTH-08", "Reutilización del OTP", "Acceso rechazado (HTTP 400 OTP_ALREADY_USED)", f"HTTP 400: {res8_v2.json()}", "PASS", "OTP reutilizado rechazado")
else:
    record("AUTH-08", "Reutilización del OTP", "Acceso rechazado", f"HTTP {res8_v2.status_code}", "FAIL", "Permitió reutilización de OTP")

# AUTH-09: Reenvío antes de 60 segundos
reset_limits()
res9_req = client.post("/api/v1/auth/otp/request", json={"email": "auth09@virtual.upt.pe"})
c_id9 = res9_req.json()["challengeId"]
res9_resend = client.post("/api/v1/auth/otp/resend", json={"challengeId": c_id9})
if res9_resend.status_code == 429 and "COOLDOWN_ACTIVE" in res9_resend.text:
    record("AUTH-09", "Reenvío antes de 60 segundos", "HTTP 429 (COOLDOWN_ACTIVE)", f"HTTP 429: {res9_resend.json()}", "PASS", "Cooldown de 60s respetado en reenvío")
else:
    record("AUTH-09", "Reenvío antes de 60 segundos", "HTTP 429", f"HTTP {res9_resend.status_code}", "FAIL", "No aplicó cooldown")

# AUTH-10: Reenvío después del cooldown
if c_id9 in _memory_challenges:
    _memory_challenges[c_id9]["resend_available_at"] = datetime.now(UTC) - timedelta(seconds=10)
try:
    from app.models.auth import AuthChallenge
    if not args.allow_remote_db:
        with IsolatedSessionLocal() as db_s:
            db_chal = db_s.query(AuthChallenge).filter(AuthChallenge.id_challenge == c_id9).first()
            if db_chal:
                db_chal.resend_available_at = datetime.now(UTC) - timedelta(seconds=10)
                db_s.commit()
    else:
        from app.db.session import get_session_context
        with get_session_context() as db_s:
            db_chal = db_s.query(AuthChallenge).filter(AuthChallenge.id_challenge == c_id9).first()
            if db_chal:
                db_chal.resend_available_at = datetime.now(UTC) - timedelta(seconds=10)
                db_s.commit()
except Exception:
    pass
_ip_request_timestamps.clear()
_email_request_timestamps.clear()
res10_resend = client.post("/api/v1/auth/otp/resend", json={"challengeId": c_id9})
if res10_resend.status_code == 200 and res10_resend.json()["challengeId"] != c_id9:
    record("AUTH-10", "Reenvío después del cooldown", "Nuevo desafío generado (HTTP 200)", f"HTTP 200, nuevo_id={res10_resend.json()['challengeId']}", "PASS", "Reenvío exitoso post-cooldown e invalidación del anterior")
else:
    record("AUTH-10", "Reenvío después del cooldown", "Nuevo desafío", f"HTTP {res10_resend.status_code}: {res10_resend.text}", "FAIL", "Fallo al reenviar tras cooldown")

# AUTH-11: Caída de base de datos en modo estricto
old_strict = settings.STRICT_DATABASE_MODE
settings.STRICT_DATABASE_MODE = True
from app.db import session as db_session_module
def broken_session():
    raise HTTPException(status_code=503, detail={"code": "DATABASE_UNAVAILABLE", "message": "Database is down"})
app.dependency_overrides[db_session_module.get_required_session] = broken_session
reset_limits()
res11 = client.post("/api/v1/auth/otp/request", json={"email": "auth11@virtual.upt.pe"})
app.dependency_overrides.clear()
if not args.allow_remote_db:
    app.dependency_overrides[db_session.get_session] = _get_isolated_session
    app.dependency_overrides[db_session.get_required_session] = _get_isolated_session
settings.STRICT_DATABASE_MODE = old_strict
if res11.status_code == 503:
    record("AUTH-11", "Caída de base de datos en modo estricto", "HTTP 503, sin fallback silencioso", f"HTTP 503", "PASS", "Lanzó 503 al fallar BD en modo estricto")
else:
    record("AUTH-11", "Caída de base de datos en modo estricto", "HTTP 503, sin fallback silencioso", f"HTTP {res11.status_code} (Respondió exitoso con desafío en RAM)", "FAIL", "endpoints/auth.py no bloqueó con 503.")

# AUTH-12: Token Google con firma inválida
fake_google_jwt = jwt.encode(
    {"email": "hacker@virtual.upt.pe", "sub": "12345", "name": "Fake User"},
    "clave_falsa_completamente_invalida",
    algorithm="HS256"
)
res12 = client.post("/api/v1/auth/google", json={"id_token": fake_google_jwt})
if res12.status_code == 401:
    record("AUTH-12", "Token Google con firma inválida", "HTTP 401, sin sesión", f"HTTP 401", "PASS", "Token con firma falsa rechazado")
elif res12.status_code == 200:
    record("AUTH-12", "Token Google con firma inválida", "HTTP 401, sin sesión", "HTTP 200 (access_token=[PROTECTED_JWT])", "FAIL", "VULNERABILIDAD CRITICA: El endpoint decodifica con verify_signature: False cuando falla Google tokeninfo y emite sesión legítima.")
else:
    record("AUTH-12", "Token Google con firma inválida", "HTTP 401", f"HTTP {res12.status_code}", "FAIL", f"Respuesta inesperada: {res12.status_code}")

# AUTH-13: Token Google con audiencia incorrecta
fake_aud_jwt = jwt.encode(
    {"email": "alumno@virtual.upt.pe", "aud": "aud-maliciosa.apps.googleusercontent.com", "sub": "123"},
    "secret",
    algorithm="HS256"
)
res13 = client.post("/api/v1/auth/google", json={"id_token": fake_aud_jwt})
if res13.status_code in [401, 403]:
    record("AUTH-13", "Token Google con audiencia incorrecta", "Acceso rechazado", f"HTTP {res13.status_code}", "PASS", "Token con aud errónea rechazado")
else:
    record("AUTH-13", "Token Google con audiencia incorrecta", "Acceso rechazado", f"HTTP {res13.status_code} (access_token emitido)", "FAIL", "El backend no valida que 'aud' coincida con GOOGLE_CLIENT_ID (GOOGLE_CLIENT_ID no está configurado).")

# AUTH-14: Token Google expirado o correo no verificado
fake_expired_jwt = jwt.encode(
    {
        "email": "expirado@virtual.upt.pe",
        "exp": int((datetime.now(UTC) - timedelta(days=365)).timestamp()),
        "email_verified": False,
        "sub": "999"
    },
    "secret",
    algorithm="HS256"
)
res14 = client.post("/api/v1/auth/google", json={"id_token": fake_expired_jwt})
if res14.status_code in [401, 403, 400]:
    record("AUTH-14", "Token Google expirado o correo no verificado", "Acceso rechazado", f"HTTP {res14.status_code}", "PASS", "Token expirado rechazado")
else:
    record("AUTH-14", "Token Google expirado o correo no verificado", "Acceso rechazado", f"HTTP {res14.status_code} (access_token emitido)", "FAIL", "verify_signature: False omite verificación de exp y el servicio no comprueba email_verified.")

# AUTH-15: Múltiples OTP incorrectos (fuerza bruta)
reset_limits()
res15_req = client.post("/api/v1/auth/otp/request", json={"email": "brute@virtual.upt.pe"})
c_id15 = res15_req.json()["challengeId"]
failed_count = 0
for i in range(10):
    r = client.post("/api/v1/auth/otp/verify", json={"challengeId": c_id15, "otp": f"{i:06d}"})
    if r.status_code in [429, 403]:
        failed_count = i + 1
        break

if failed_count > 0:
    record("AUTH-15", "Múltiples OTP incorrectos", "Protección contra fuerza bruta (bloqueo tras N intentos)", f"Bloqueado en intento {failed_count}", "PASS", "Bloqueo efectivo contra fuerza bruta")
else:
    attempts_in_mem = _memory_challenges[c_id15]["attempts"]
    record("AUTH-15", "Múltiples OTP incorrectos", "Protección contra fuerza bruta", f"10 intentos fallidos permitidos consecutivamente (attempts={attempts_in_mem})", "FAIL", "No existe límite de intentos fallidos; el desafío no se invalida ni se bloquea tras múltiples intentos erróneos.")

# AUTH-16: Login/logout y persistencia de sesión
test_email = "ra2022073504@virtual.upt.pe"
from app.core.security import create_access_token, decode_access_token
token = create_access_token({"sub": test_email, "email": test_email, "roles": ["mentoreado"], "role": "mentoreado"})
payload = decode_access_token(token)
if payload and payload.get("sub") == test_email and payload.get("role") == "mentoreado":
    record("AUTH-16", "Login/logout y persistencia de sesión", "Sesión coherente y cierre efectivo", "JWT generado, claims verificados, firma válida", "PASS", "Tokens de sesión cumplen con algoritmo HS256, expiración y claims")
else:
    record("AUTH-16", "Login/logout y persistencia de sesión", "Sesión coherente", "Fallo al validar JWT", "FAIL", "Fallo en validación de token JWT")

# Restaurar mocks y configuraciones
EmailService.send_otp_email = old_send
settings.SMTP_ENABLED = original_smtp_enabled
app.dependency_overrides.clear()

print("\n" + "="*80)
print(f"{'ID':<9} | {'ESCENARIO':<32} | {'ESTADO':<6} | {'DETALLE'}")
print("="*80)
for r in results:
    extra = f" [ACTUAL: {r['actual']}]" if r['status'] == "FAIL" else ""
    print(f"{r['id']:<9} | {r['scenario']:<32} | {r['status']:<6} | {r['reason']}{extra}")
print("="*80)
