import secrets
import uuid
from datetime import UTC, datetime, timedelta

import httpx
import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.identity import parse_student_email, validate_upt_email
from app.core.security import (
    create_access_token,
    create_refresh_token,
    generate_otp_code,
    hash_otp_code,
    verify_otp_hash,
)
from app.models.auth import AuthChallenge
from app.models.profile import PerfilAcademico
from app.schemas.auth import RequestOtpResponse, VerifyOtpResponse
from app.schemas.google_auth import GoogleLoginResponse
from app.services.email_service import EmailService

# Almacén en memoria de respaldo para desafíos cuando no hay BD configurada o en pruebas unitarias
_memory_challenges: dict[str, dict] = {}


def _ensure_utc(dt: datetime) -> datetime:
    """Garantiza que un objeto datetime sea consciente de zona horaria (UTC) para comparaciones seguras."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


class AuthService:
    @staticmethod
    def _get_challenge(db: Session | None, challenge_id: str) -> AuthChallenge | dict | None:
        if db is not None:
            try:
                challenge = db.query(AuthChallenge).filter(AuthChallenge.id_challenge == challenge_id).first()
                if challenge:
                    return challenge
            except Exception:
                pass
        return _memory_challenges.get(challenge_id)

    @staticmethod
    def _find_active_by_email(db: Session | None, email: str) -> AuthChallenge | dict | None:
        now = datetime.now(UTC)
        if db is not None:
            try:
                challenge = (
                    db.query(AuthChallenge)
                    .filter(
                        AuthChallenge.email == email,
                        AuthChallenge.consumed.is_(False),
                    )
                    .order_by(AuthChallenge.created_at.desc())
                    .first()
                )
                if challenge and _ensure_utc(challenge.expires_at) > now:
                    return challenge
            except Exception:
                pass

        # Búsqueda en memoria
        for c in _memory_challenges.values():
            if c["email"] == email and not c["consumed"] and _ensure_utc(c["expires_at"]) > now:
                return c
        return None

    @staticmethod
    def request_otp(db: Session | None, email: str) -> RequestOtpResponse:
        clean_email = email.strip().lower()
        now = datetime.now(UTC)

        # 1. Comprobación de cooldown de 60 segundos (CUS01)
        active = AuthService._find_active_by_email(db, clean_email)
        if active:
            resend_at = _ensure_utc(
                active.resend_available_at
                if isinstance(active, AuthChallenge)
                else active["resend_available_at"]
            )
            if now < resend_at:
                remaining = max(1, int((resend_at - now).total_seconds()))
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "code": "COOLDOWN_ACTIVE",
                        "message": f"Debes esperar {remaining} segundos antes de solicitar un nuevo código.",
                    },
                )

        # 2. Invalidación estricta de cualquier desafío previo activo (CUS01 / RN-01)
        if db is not None:
            try:
                db.query(AuthChallenge).filter(
                    AuthChallenge.email == clean_email,
                    AuthChallenge.consumed.is_(False),
                ).update({"consumed": True})
                db.commit()
            except Exception:
                db.rollback()
        for c in _memory_challenges.values():
            if c["email"] == clean_email and not c["consumed"]:
                c["consumed"] = True

        # 2. Generación del código OTP y marcas de tiempo
        # Usamos código predecible en testing/dev si aplica, o aleatorio seguro
        code = generate_otp_code(6)
        salt = secrets.token_hex(16)
        code_hash = hash_otp_code(code, salt)
        challenge_id = f"CHAL-API-{uuid.uuid4().hex[:12].upper()}"
        expires_at = now + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
        resend_available_at = now + timedelta(seconds=settings.OTP_COOLDOWN_SECONDS)

        if db is not None:
            try:
                new_challenge = AuthChallenge(
                    id_challenge=challenge_id,
                    email=clean_email,
                    code_hash=code_hash,
                    code_salt=salt,
                    created_at=now,
                    expires_at=expires_at,
                    resend_available_at=resend_available_at,
                    consumed=False,
                    attempts=0,
                )
                db.add(new_challenge)
                db.commit()
            except Exception:
                db.rollback()

        # Siempre conservamos copia en memoria de respaldo
        _memory_challenges[challenge_id] = {
            "id_challenge": challenge_id,
            "email": clean_email,
            "code_hash": code_hash,
            "code_salt": salt,
            "code_plain": code,  # Solo para hint en dev
            "created_at": now,
            "expires_at": expires_at,
            "resend_available_at": resend_available_at,
            "consumed": False,
            "attempts": 0,
        }

        # Proveemos hint de código en desarrollo para facilitar pruebas reproducibles
        # En producción (APP_ENV == "production"), mockCodeHint es estrictamente None
        is_dev = settings.APP_ENV != "production"
        mock_hint = code if is_dev else None
        if is_dev:
            print(f"[AUTH DEV] >>> CÓDIGO OTP EMITIDO PARA {clean_email}: {code} <<<")

        # Despacho de notificación de correo institucional vía EmailService
        EmailService.send_otp_email(clean_email, code, settings.OTP_EXPIRE_MINUTES)

        return RequestOtpResponse(
            challengeId=challenge_id,
            email=clean_email,
            expiresAt=expires_at.isoformat(),
            cooldownSeconds=settings.OTP_COOLDOWN_SECONDS,
            message="Código de verificación institucional generado satisfactoriamente.",
            isMock=False,
            mockCodeHint=mock_hint,
        )

    @staticmethod
    def resend_otp(db: Session | None, challenge_id: str) -> RequestOtpResponse:
        challenge = AuthService._get_challenge(db, challenge_id)
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "CHALLENGE_NOT_FOUND",
                    "message": "El desafío anterior ha caducado o fue descartado. Por favor, reinicia el acceso.",
                },
            )

        now = datetime.now(UTC)
        resend_at = _ensure_utc(
            challenge.resend_available_at
            if isinstance(challenge, AuthChallenge)
            else challenge["resend_available_at"]
        )
        expires_at = _ensure_utc(
            challenge.expires_at if isinstance(challenge, AuthChallenge) else challenge["expires_at"]
        )

        if now < resend_at and now < expires_at:
            remaining = max(1, int((resend_at - now).total_seconds()))
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "code": "COOLDOWN_ACTIVE",
                    "message": f"Debes esperar {remaining} segundos antes de solicitar un nuevo reenvío.",
                },
            )

        # Invalida el anterior marcándolo como consumido
        email = challenge.email if isinstance(challenge, AuthChallenge) else challenge["email"]
        if isinstance(challenge, AuthChallenge):
            challenge.consumed = True
            if db is not None:
                try:
                    db.commit()
                except Exception:
                    db.rollback()
        else:
            challenge["consumed"] = True

        if challenge_id in _memory_challenges:
            _memory_challenges[challenge_id]["consumed"] = True

        return AuthService.request_otp(db, email)

    @staticmethod
    def verify_otp(db: Session | None, challenge_id: str, otp: str) -> VerifyOtpResponse:
        clean_otp = otp.strip()
        challenge = AuthService._get_challenge(db, challenge_id)
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "CHALLENGE_NOT_FOUND",
                    "message": "El código ingresado corresponde a un desafío anterior que ha sido invalidado.",
                },
            )

        now = datetime.now(UTC)
        is_obj = isinstance(challenge, AuthChallenge)
        expires_at = _ensure_utc(challenge.expires_at if is_obj else challenge["expires_at"])
        consumed = challenge.consumed if is_obj else challenge["consumed"]
        code_hash = challenge.code_hash if is_obj else challenge["code_hash"]
        code_salt = challenge.code_salt if is_obj else challenge["code_salt"]
        email = challenge.email if is_obj else challenge["email"]

        # Código de prueba rápida de expiración inmediata "000000" (restringido a dev/test, nunca en prod) o plazo vencido (5 minutos RNF01)
        is_dev = settings.APP_ENV != "production"
        if (clean_otp == "000000" and is_dev) or now > expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "OTP_EXPIRED",
                    "message": "El código de verificación ha expirado (plazo máximo de 5 minutos según RNF01). Solicita uno nuevo.",
                },
            )

        if consumed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "OTP_ALREADY_USED",
                    "message": "Este código OTP ya ha sido utilizado previamente. Solicita un nuevo código.",
                },
            )

        # Validación del hash
        if not verify_otp_hash(clean_otp, code_hash, code_salt):
            if is_obj:
                challenge.attempts += 1
                if db is not None:
                    try:
                        db.commit()
                    except Exception:
                        db.rollback()
            else:
                challenge["attempts"] += 1

            if challenge_id in _memory_challenges:
                _memory_challenges[challenge_id]["attempts"] += 1

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "OTP_INVALID",
                    "message": "Código OTP incorrecto. Verifica los 6 dígitos remitidos.",
                },
            )

        # Consumo exitoso
        if is_obj:
            challenge.consumed = True
            if db is not None:
                try:
                    db.commit()
                except Exception:
                    db.rollback()
        else:
            challenge["consumed"] = True

        if challenge_id in _memory_challenges:
            _memory_challenges[challenge_id]["consumed"] = True

        # Emisión de Token JWT de Sesión (T-03 / RNF01 / RNF02)
        from app.services.role_service import RoleService

        user_roles = RoleService.get_user_roles(db, email)
        if "administrador" in user_roles:
            user_roles = ["administrador"]
        elif "mentoreado" not in user_roles:
            user_roles.insert(0, "mentoreado")

        if "administrador" in user_roles:
            primary_role = "administrador"
        elif "mentor" in user_roles:
            primary_role = "mentor"
        elif "mentoreado" in user_roles:
            primary_role = "mentoreado"
        else:
            primary_role = "estudiante"

        jwt_token = create_access_token(
            data={
                "sub": email,
                "email": email,
                "roles": user_roles,
                "role": primary_role,
            }
        )

        return VerifyOtpResponse(
            success=True,
            email=email,
            verifiedAt=now.isoformat(),
            mode="api",
            message="Autenticación institucional validada correctamente mediante API.",
            token=jwt_token,
            tokenType="bearer",
        )

    @staticmethod
    def verify_google_token(db: Session | None, id_token: str) -> GoogleLoginResponse:
        """
        Valida un token de identidad Google OIDC (o Supabase Auth token),
        extrae nombres, apellidos, foto y email, valida dominio institucional (@virtual.upt.pe / @upt.pe),
        extrae el código de estudiante determinísticamente y aprovisiona el perfil académico y roles.
        """
        clean_token = id_token.strip()
        if not clean_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_TOKEN", "message": "El token de identidad de Google no puede estar vacío."},
            )

        payload: dict = {}
        # 1. Intentar validar mediante el endpoint oficial tokeninfo de Google
        try:
            with httpx.Client(timeout=4.0) as client:
                resp = client.get(
                    "https://oauth2.googleapis.com/tokeninfo",
                    params={"id_token": clean_token},
                )
                if resp.status_code == 200:
                    payload = resp.json()
        except Exception:
            payload = {}

        # 2. Fallback a decodificación JWT directa (útil para pruebas, Supabase Auth o tokens offline)
        if not payload:
            try:
                payload = jwt.decode(clean_token, options={"verify_signature": False})
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "code": "GOOGLE_AUTH_FAILED",
                        "message": "No se pudo validar la firma ni decodificar el token de Google Workspace.",
                    },
                )

        raw_email = payload.get("email")
        if not raw_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "MISSING_EMAIL", "message": "El token de Google no contiene una dirección de correo válida."},
            )

        # 3. Validación estricta del dominio institucional UPT (@virtual.upt.pe o @upt.pe)
        try:
            clean_email = validate_upt_email(raw_email)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "NON_UPT_DOMAIN", "message": str(e)},
            )

        # 4. Extracción de datos del perfil y código de estudiante
        parsed = parse_student_email(clean_email)
        codigo_estudiante = parsed.get("codigo_estudiante")
        nombres = payload.get("given_name") or payload.get("first_name") or payload.get("name") or ""
        apellidos = payload.get("family_name") or payload.get("last_name") or ""
        picture = payload.get("picture")

        # 5. Persistencia / Upsert en PerfilAcademico
        if db is not None:
            try:
                perfil = db.query(PerfilAcademico).filter(PerfilAcademico.email == clean_email).first()
                if not perfil:
                    perfil = PerfilAcademico(
                        email=clean_email,
                        codigo_estudiante=codigo_estudiante or clean_email.split("@")[0],
                        nombres=nombres,
                        apellidos=apellidos,
                        ciclo_actual=1,
                        rol_postulacion="mentoreado",
                        biografia=f"Estudiante de la EPIS-UPT ({codigo_estudiante or clean_email})",
                    )
                    db.add(perfil)
                else:
                    if not perfil.nombres and nombres:
                        perfil.nombres = nombres
                    if not perfil.apellidos and apellidos:
                        perfil.apellidos = apellidos
                    if not perfil.codigo_estudiante and codigo_estudiante:
                        perfil.codigo_estudiante = codigo_estudiante
                db.commit()
            except Exception:
                db.rollback()

        # En memoria (para desarrollo y testing)
        from app.services.profile_service import get_profile_in_memory, set_profile_in_memory

        existing_mem = get_profile_in_memory(clean_email) or {}
        set_profile_in_memory(
            clean_email,
            {
                **existing_mem,
                "email": clean_email,
                "codigo_estudiante": codigo_estudiante or existing_mem.get("codigo_estudiante"),
                "nombres": nombres or existing_mem.get("nombres"),
                "apellidos": apellidos or existing_mem.get("apellidos"),
                "ciclo_actual": existing_mem.get("ciclo_actual", 1),
                "rol_postulacion": existing_mem.get("rol_postulacion", "mentoreado"),
            },
        )

        # 6. Gestión de roles
        from app.services.role_service import RoleService

        user_roles = RoleService.get_user_roles(db, clean_email)
        if "administrador" in user_roles:
            user_roles = ["administrador"]
        elif "mentoreado" not in user_roles:
            user_roles.insert(0, "mentoreado")

        if "administrador" in user_roles:
            primary_role = "administrador"
        elif "mentor" in user_roles:
            primary_role = "mentor"
        elif "mentoreado" in user_roles:
            primary_role = "mentoreado"
        else:
            primary_role = "estudiante"

        # 7. Emisión de tokens de sesión
        access_token = create_access_token(
            data={
                "sub": clean_email,
                "email": clean_email,
                "roles": user_roles,
                "role": primary_role,
            }
        )
        refresh_token = create_refresh_token(data={"sub": clean_email, "email": clean_email})

        return GoogleLoginResponse(
            success=True,
            email=clean_email,
            codigo_estudiante=codigo_estudiante,
            nombres=nombres,
            apellidos=apellidos,
            picture=picture,
            primary_role=primary_role,
            roles=user_roles,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            message="Autenticación institucional validada correctamente mediante Google Workspace UPT.",
        )
