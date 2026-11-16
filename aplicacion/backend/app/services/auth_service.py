import logging
import secrets
import threading
import time
import uuid
from datetime import UTC, datetime, timedelta

import httpx
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
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
from app.models.auth import AuthChallenge, AuthRateLimit
from app.models.profile import PerfilAcademico
from app.schemas.auth import RequestOtpResponse, VerifyOtpResponse
from app.schemas.google_auth import GoogleLoginResponse
from app.services.email_service import EmailService

logger = logging.getLogger("app.auth")

# Cerrojo para concurrencia multihilo en memoria
_rate_limit_lock = threading.Lock()

# Almacén en memoria de respaldo exclusivo para desarrollo y pruebas unitarias aisladas
_memory_challenges: dict[str, dict] = {}

# Cubos de control de tasa (Rate Limiting) en memoria por ventana temporal (fallback)
_ip_request_timestamps: dict[str, list[float]] = {}
_email_request_timestamps: dict[str, list[float]] = {}
_ip_verify_timestamps: dict[str, list[float]] = {}


def _ensure_utc(dt: datetime) -> datetime:
    """Garantiza que un objeto datetime sea consciente de zona horaria (UTC) para comparaciones seguras."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def _check_rate_limit(
    db: Session | None,
    key: str,
    max_requests: int,
    window_seconds: int = 60,
    error_code: str = "RATE_LIMIT_EXCEEDED",
    error_message: str = "Demasiadas solicitudes. Por favor espera un momento.",
    fallback_bucket: dict[str, list[float]] | None = None,
) -> None:
    """
    Valida la frecuencia de solicitudes para mitigar ataques de denegación de servicio y fuerza bruta.
    Estrategia híbrida: persistente y atómica en PostgreSQL/Supabase (H-08), o en memoria con cerrojo para tests.
    """
    now = datetime.now(UTC)

    # 1. Estrategia compartida y persistente en base de datos si db está disponible
    if db is not None:
        try:
            bind = db.get_bind()
            dialect_name = bind.dialect.name if bind else ""

            if dialect_name == "postgresql":
                # Estrategia atómica nativa PostgreSQL: INSERT ... ON CONFLICT (key) DO UPDATE ... RETURNING
                # Erradica al 100% la condición de carrera entre múltiples workers cuando la clave aún no existe.
                upsert_sql = text("""
                    INSERT INTO auth_rate_limits (key, count, window_expires_at, updated_at)
                    VALUES (:key, 1, :new_window_expires_at, :now)
                    ON CONFLICT (key) DO UPDATE
                    SET count = CASE
                            WHEN auth_rate_limits.window_expires_at > :now THEN auth_rate_limits.count + 1
                            ELSE 1
                        END,
                        window_expires_at = CASE
                            WHEN auth_rate_limits.window_expires_at > :now THEN auth_rate_limits.window_expires_at
                            ELSE :new_window_expires_at
                        END,
                        updated_at = :now
                    RETURNING count, window_expires_at;
                """)
                res = db.execute(
                    upsert_sql,
                    {
                        "key": key,
                        "new_window_expires_at": now + timedelta(seconds=window_seconds),
                        "now": now,
                    },
                ).fetchone()
                db.commit()

                if res:
                    count, expires_at = res[0], _ensure_utc(res[1])
                    if count > max_requests:
                        remaining = max(1, int((expires_at - now).total_seconds()))
                        raise HTTPException(
                            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail={
                                "code": error_code,
                                "message": f"{error_message} Debes esperar {remaining} segundos.",
                            },
                        )
                return

            # Para otros motores (ej. SQLite en pruebas unitarias)
            try:
                query = db.query(AuthRateLimit).filter(AuthRateLimit.key == key)
                try:
                    record = query.with_for_update().first()
                except Exception:
                    record = query.first()

                if record:
                    expires_at = _ensure_utc(record.window_expires_at)
                    if now < expires_at:
                        if record.count >= max_requests:
                            remaining = max(1, int((expires_at - now).total_seconds()))
                            raise HTTPException(
                                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                                detail={
                                    "code": error_code,
                                    "message": f"{error_message} Debes esperar {remaining} segundos.",
                                },
                            )
                        record.count += 1
                    else:
                        record.count = 1
                        record.window_expires_at = now + timedelta(seconds=window_seconds)
                else:
                    record = AuthRateLimit(
                        key=key,
                        count=1,
                        window_expires_at=now + timedelta(seconds=window_seconds),
                    )
                    db.add(record)
                db.commit()
                return
            except IntegrityError as exc:
                # Manejo de condición de carrera si otra transacción insertó la clave simultáneamente
                db.rollback()
                record = db.query(AuthRateLimit).filter(AuthRateLimit.key == key).first()
                if record:
                    expires_at = _ensure_utc(record.window_expires_at)
                    if now < expires_at:
                        if record.count >= max_requests:
                            remaining = max(1, int((expires_at - now).total_seconds()))
                            raise HTTPException(
                                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                                detail={
                                    "code": error_code,
                                    "message": f"{error_message} Debes esperar {remaining} segundos.",
                                },
                            ) from exc
                        record.count += 1
                    else:
                        record.count = 1
                        record.window_expires_at = now + timedelta(seconds=window_seconds)
                    db.commit()
                    return
        except HTTPException:
            raise
        except Exception as exc:
            db.rollback()
            logger.warning("Fallo en rate limit persistente en BD: %s.", exc)
            if settings.STRICT_DATABASE_MODE:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail={
                        "code": "DATABASE_UNAVAILABLE",
                        "message": "Error al verificar limitación de tasa en base de datos.",
                    },
                ) from exc

    # 2. Estrategia en memoria (fallback protegido por Lock para concurrencia local/tests)
    if fallback_bucket is not None:
        with _rate_limit_lock:
            now_ts = time.time()
            timestamps = fallback_bucket.get(key, [])
            valid_window = [t for t in timestamps if now_ts - t < window_seconds]
            if len(valid_window) >= max_requests:
                oldest = valid_window[0]
                remaining = max(1, int(oldest + window_seconds - now_ts))
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "code": error_code,
                        "message": f"{error_message} Debes esperar {remaining} segundos.",
                    },
                )
            valid_window.append(now_ts)
            fallback_bucket[key] = valid_window


class AuthService:
    @staticmethod
    def _assert_db_strict_check(db: Session | None) -> None:
        """Garantiza que en modo estricto no se degrade silenciosamente a persistencia volátil en memoria."""
        if db is None and settings.STRICT_DATABASE_MODE:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "code": "DATABASE_UNAVAILABLE",
                    "message": (
                        "DATABASE_UNAVAILABLE: El servicio de base de datos PostgreSQL/Supabase no está disponible. "
                        "Operación abortada para prevenir inconsistencias de persistencia."
                    ),
                },
            )

    @staticmethod
    def _get_challenge(
        db: Session | None, challenge_id: str, lock_row: bool = False
    ) -> AuthChallenge | dict | None:
        if db is not None:
            try:
                query = db.query(AuthChallenge).filter(AuthChallenge.id_challenge == challenge_id)
                if lock_row:
                    try:
                        return query.with_for_update().first()
                    except Exception:
                        return query.first()
                return query.first()
            except HTTPException:
                raise
            except Exception as exc:
                logger.error("Error al consultar desafío en base de datos: %s", exc)
                if settings.STRICT_DATABASE_MODE:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail={
                            "code": "DATABASE_UNAVAILABLE",
                            "message": "Error al consultar el desafío en la base de datos.",
                        },
                    ) from exc

        if settings.STRICT_DATABASE_MODE:
            return None
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
                return None
            except HTTPException:
                raise
            except Exception as exc:
                logger.error("Error al consultar desafíos activos en base de datos: %s", exc)
                if settings.STRICT_DATABASE_MODE:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail={
                            "code": "DATABASE_UNAVAILABLE",
                            "message": "Error al consultar desafíos activos en la base de datos.",
                        },
                    ) from exc

        if settings.STRICT_DATABASE_MODE:
            return None

        # Búsqueda en memoria exclusiva para modo no estricto
        for c in _memory_challenges.values():
            if c["email"] == email and not c["consumed"] and _ensure_utc(c["expires_at"]) > now:
                return c
        return None

    @staticmethod
    def request_otp(db: Session | None, email: str, client_ip: str = "127.0.0.1") -> RequestOtpResponse:
        AuthService._assert_db_strict_check(db)

        # 1. Validación de formato y dominio institucional (@virtual.upt.pe o @upt.pe)
        try:
            clean_email = validate_upt_email(email.strip().lower())
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"code": "INVALID_EMAIL", "message": str(e)},
            ) from e

        now = datetime.now(UTC)

        # 2. Control de tasa de peticiones (Rate Limiting) por IP y por correo
        _check_rate_limit(
            db,
            f"ip:{client_ip}",
            max_requests=settings.OTP_RATE_LIMIT_PER_MINUTE,
            window_seconds=60,
            error_code="IP_RATE_LIMIT_EXCEEDED",
            error_message="Demasiadas solicitudes de código desde esta dirección IP. Por favor espera un momento.",
            fallback_bucket=_ip_request_timestamps,
        )
        _check_rate_limit(
            db,
            f"email:{clean_email}",
            max_requests=settings.OTP_RATE_LIMIT_PER_MINUTE,
            window_seconds=60,
            error_code="EMAIL_RATE_LIMIT_EXCEEDED",
            error_message="Demasiadas solicitudes de código para este correo institucional. Por favor espera un momento.",
            fallback_bucket=_email_request_timestamps,
        )

        # 3. Comprobación de cooldown de 60 segundos (CUS01)
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

        # 4. Invalidación estricta de cualquier desafío previo activo (CUS01 / RN-01)
        if db is not None:
            try:
                db.query(AuthChallenge).filter(
                    AuthChallenge.email == clean_email,
                    AuthChallenge.consumed.is_(False),
                ).update({"consumed": True})
                db.flush()
            except Exception as exc:
                db.rollback()
                logger.error("Error al invalidar desafíos previos en BD: %s", exc)
                if settings.STRICT_DATABASE_MODE:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail={
                            "code": "DATABASE_UNAVAILABLE",
                            "message": "Error al invalidar desafíos previos en base de datos.",
                        },
                    ) from exc

        for c in _memory_challenges.values():
            if c["email"] == clean_email and not c["consumed"]:
                c["consumed"] = True

        # 5. Generación del código OTP y marcas de tiempo
        code = generate_otp_code(6)
        salt = secrets.token_hex(16)
        code_hash = hash_otp_code(code, salt)
        challenge_id = f"CHAL-API-{uuid.uuid4().hex[:12].upper()}"
        expires_at = now + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
        resend_available_at = now + timedelta(seconds=settings.OTP_COOLDOWN_SECONDS)

        new_challenge = None
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
            except Exception as exc:
                db.rollback()
                logger.error("Error al persistir desafío en base de datos: %s", exc)
                if settings.STRICT_DATABASE_MODE:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail={
                            "code": "DATABASE_UNAVAILABLE",
                            "message": "Error al registrar el desafío de autenticación en la base de datos.",
                        },
                    ) from exc
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                        "code": "DB_COMMIT_FAILED",
                        "message": "No fue posible registrar el desafío de autenticación en la base de datos.",
                    },
                ) from exc

        # Almacén en memoria de respaldo
        _memory_challenges[challenge_id] = {
            "id_challenge": challenge_id,
            "email": clean_email,
            "code_hash": code_hash,
            "code_salt": salt,
            "code_plain": code,
            "created_at": now,
            "expires_at": expires_at,
            "resend_available_at": resend_available_at,
            "consumed": False,
            "attempts": 0,
        }

        # 6. Despacho y verificación del servicio SMTP
        is_smtp_active = settings.SMTP_ENABLED and bool(settings.SMTP_USER and settings.SMTP_USER.strip())
        dispatch_success = EmailService.send_otp_email(clean_email, code, settings.OTP_EXPIRE_MINUTES)

        if not is_smtp_active:
            delivery_status = "mocked"
            email_dispatched = False
            is_mock = True
            message = (
                "Código OTP generado en modo de desarrollo local (despacho simulado en consola del servidor)."
            )
        elif dispatch_success:
            delivery_status = "dispatched"
            email_dispatched = True
            is_mock = False
            message = (
                "Código de verificación institucional enviado satisfactoriamente a tu correo institucional."
            )
        else:
            # Fallo en el envío SMTP: invalidar el desafío recién confirmado para no dejar códigos huérfanos
            if db is not None and new_challenge:
                try:
                    new_challenge.consumed = True
                    db.commit()
                except Exception as exc:
                    db.rollback()
                    logger.error("Error al revocar desafío tras fallo SMTP en base de datos: %s", exc)
                    if settings.STRICT_DATABASE_MODE:
                        raise HTTPException(
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail={
                                "code": "DATABASE_UNAVAILABLE",
                                "message": "Error en la base de datos al intentar revocar el desafío tras fallo SMTP.",
                            },
                        ) from exc
            if challenge_id in _memory_challenges:
                _memory_challenges[challenge_id]["consumed"] = True

            logger.error("Fallo de entrega SMTP para %s. Desafío %s invalidado.", clean_email, challenge_id)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={
                    "code": "EMAIL_DISPATCH_FAILED",
                    "message": "No fue posible despachar el correo de verificación institucional mediante el servidor SMTP. El código fue revocado por seguridad. Por favor, reintenta en unos momentos.",
                },
            )

        # 7. Exposición controlada de mockCodeHint (solo en pruebas unitarias explícitamente autorizadas y nunca en producción)
        is_test_hint_enabled = bool(
            getattr(settings, "ENABLE_MOCK_OTP_HINTS", False)
            and getattr(settings, "APP_ENV", "") != "production"
        )
        mock_hint = code if is_test_hint_enabled else None
        if is_test_hint_enabled:
            logger.info("[AUTH TEST] >>> CÓDIGO OTP EMITIDO PARA %s: %s <<<", clean_email, code)

        return RequestOtpResponse(
            challengeId=challenge_id,
            email=clean_email,
            expiresAt=expires_at.isoformat(),
            cooldownSeconds=settings.OTP_COOLDOWN_SECONDS,
            message=message,
            isMock=is_mock,
            mockCodeHint=mock_hint,
            deliveryStatus=delivery_status,
            emailDispatched=email_dispatched,
        )

    @staticmethod
    def resend_otp(db: Session | None, challenge_id: str, client_ip: str = "127.0.0.1") -> RequestOtpResponse:
        AuthService._assert_db_strict_check(db)

        _check_rate_limit(
            db,
            f"resend:ip:{client_ip}",
            max_requests=settings.OTP_RATE_LIMIT_PER_MINUTE,
            window_seconds=60,
            error_code="IP_RATE_LIMIT_EXCEEDED",
            error_message="Demasiadas solicitudes de reenvío desde esta dirección IP.",
            fallback_bucket=_ip_request_timestamps,
        )

        challenge = AuthService._get_challenge(db, challenge_id)
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "CHALLENGE_NOT_FOUND",
                    "message": "El desafío anterior ha caducado o fue descartado. Por favor, reinicia el acceso.",
                },
            )

        is_chal_obj = isinstance(challenge, AuthChallenge)
        consumed = challenge.consumed if is_chal_obj else challenge.get("consumed", False)
        if consumed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "CHALLENGE_ALREADY_USED",
                    "message": "El desafío ya fue utilizado o invalidado. Por favor, solicita un nuevo código.",
                },
            )

        now = datetime.now(UTC)
        resend_at = _ensure_utc(
            challenge.resend_available_at if is_chal_obj else challenge["resend_available_at"]
        )
        expires_at = _ensure_utc(challenge.expires_at if is_chal_obj else challenge["expires_at"])

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
        email = challenge.email if is_chal_obj else challenge["email"]
        if is_chal_obj:
            challenge.consumed = True
            if db is not None:
                try:
                    db.commit()
                except Exception as exc:
                    db.rollback()
                    logger.error("Error al invalidar desafío anterior en BD durante reenvío: %s", exc)
                    if settings.STRICT_DATABASE_MODE:
                        raise HTTPException(
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail={
                                "code": "DATABASE_UNAVAILABLE",
                                "message": "Error al invalidar el desafío anterior en la base de datos.",
                            },
                        ) from exc
        else:
            challenge["consumed"] = True

        if challenge_id in _memory_challenges:
            _memory_challenges[challenge_id]["consumed"] = True

        return AuthService.request_otp(db, email, client_ip)

    @staticmethod
    def verify_otp(
        db: Session | None, challenge_id: str, otp: str, client_ip: str = "127.0.0.1"
    ) -> VerifyOtpResponse:
        AuthService._assert_db_strict_check(db)

        _check_rate_limit(
            db,
            f"verify:ip:{client_ip}",
            max_requests=30,
            window_seconds=60,
            error_code="IP_RATE_LIMIT_EXCEEDED",
            error_message="Demasiados intentos de verificación desde esta dirección IP. Espera un momento.",
            fallback_bucket=_ip_verify_timestamps,
        )

        clean_otp = otp.strip()
        challenge = AuthService._get_challenge(db, challenge_id, lock_row=True)
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "CHALLENGE_NOT_FOUND",
                    "message": "El código ingresado corresponde a un desafío anterior que ha sido invalidado o no existe.",
                },
            )

        is_obj = isinstance(challenge, AuthChallenge)
        attempts = challenge.attempts if is_obj else challenge.get("attempts", 0)

        # Verificación de bloqueo preventivo por intentos excesivos (H-04)
        if attempts >= settings.MAX_OTP_ATTEMPTS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "CHALLENGE_LOCKED",
                    "message": (
                        f"El desafío de verificación ha sido bloqueado tras superar el límite de "
                        f"{settings.MAX_OTP_ATTEMPTS} intentos fallidos. Solicita un nuevo código."
                    ),
                },
            )

        now = datetime.now(UTC)
        expires_at = _ensure_utc(challenge.expires_at if is_obj else challenge["expires_at"])
        consumed = challenge.consumed if is_obj else challenge["consumed"]
        code_hash = challenge.code_hash if is_obj else challenge["code_hash"]
        code_salt = challenge.code_salt if is_obj else challenge["code_salt"]
        email = challenge.email if is_obj else challenge["email"]

        # Código de prueba rápida de expiración inmediata "000000" restringido exclusivamente a testing autorizado (nunca en producción)
        is_test_hint_enabled = bool(
            getattr(settings, "ENABLE_MOCK_OTP_HINTS", False)
            and getattr(settings, "APP_ENV", "") != "production"
        )
        if (clean_otp == "000000" and is_test_hint_enabled) or now > expires_at:
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

        # Validación criptográfica en tiempo constante
        if not verify_otp_hash(clean_otp, code_hash, code_salt):
            new_attempts = attempts + 1
            if is_obj:
                challenge.attempts = new_attempts
                if new_attempts >= settings.MAX_OTP_ATTEMPTS:
                    challenge.consumed = True
                if db is not None:
                    try:
                        db.commit()
                    except Exception as exc:
                        db.rollback()
                        logger.error("Error al actualizar intentos en BD: %s", exc)
                        if settings.STRICT_DATABASE_MODE:
                            raise HTTPException(
                                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail={
                                    "code": "DATABASE_UNAVAILABLE",
                                    "message": "Error al actualizar intentos de verificación en la base de datos.",
                                },
                            ) from exc
            else:
                challenge["attempts"] = new_attempts
                if new_attempts >= settings.MAX_OTP_ATTEMPTS:
                    challenge["consumed"] = True

            if challenge_id in _memory_challenges:
                _memory_challenges[challenge_id]["attempts"] = new_attempts
                if new_attempts >= settings.MAX_OTP_ATTEMPTS:
                    _memory_challenges[challenge_id]["consumed"] = True

            if new_attempts >= settings.MAX_OTP_ATTEMPTS:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "code": "CHALLENGE_LOCKED",
                        "message": (
                            f"Código OTP incorrecto. Se ha superado el número máximo de intentos permitidos "
                            f"({settings.MAX_OTP_ATTEMPTS}). El desafío ha sido bloqueado definitivamente por seguridad."
                        ),
                    },
                )

            remaining = settings.MAX_OTP_ATTEMPTS - new_attempts
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "OTP_INVALID",
                    "message": (
                        f"Código OTP incorrecto. Te quedan {remaining} "
                        f"{'intento' if remaining == 1 else 'intentos'} antes del bloqueo del código."
                    ),
                },
            )

        # Consumo exitoso
        if is_obj:
            challenge.consumed = True
            if db is not None:
                try:
                    db.commit()
                except Exception as exc:
                    db.rollback()
                    logger.error("Error al confirmar consumo del desafío en BD: %s", exc)
                    if settings.STRICT_DATABASE_MODE:
                        raise HTTPException(
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail={
                                "code": "DATABASE_UNAVAILABLE",
                                "message": "Error al confirmar el uso del código en la base de datos.",
                            },
                        ) from exc
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
        Valida criptográficamente un Google ID Token oficial de Google Identity Services.
        Exige firma válida, coincidencia de GOOGLE_CLIENT_ID, emisor oficial de Google,
        vigencia de expiración, correo verificado y dominio institucional UPT (@virtual.upt.pe / @upt.pe).
        """
        AuthService._assert_db_strict_check(db)

        clean_token = id_token.strip()
        if not clean_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "INVALID_TOKEN",
                    "message": "El token de identidad de Google no puede estar vacío.",
                },
            )

        payload: dict = {}
        google_client_id = settings.GOOGLE_CLIENT_ID

        # 1. Validación criptográfica con biblioteca oficial google-auth
        try:
            from google.auth.transport import requests as google_requests
            from google.oauth2 import id_token as google_id_token

            payload = google_id_token.verify_oauth2_token(
                clean_token,
                google_requests.Request(),
                audience=google_client_id if google_client_id else None,
            )
        except Exception as exc_local:
            logger.warning(
                "Fallo en verificación local de google-auth (%s). Probando tokeninfo oficial.", exc_local
            )
            # 2. Respaldo contra endpoint oficial tokeninfo de Google si falla el transporte local
            try:
                with httpx.Client(timeout=5.0) as client:
                    resp = client.get(
                        "https://oauth2.googleapis.com/tokeninfo",
                        params={"id_token": clean_token},
                    )
                    if resp.status_code == 200:
                        payload = resp.json()
            except Exception:
                payload = {}

        # 3. Rechazo estricto si no fue posible validar criptográficamente el token con Google
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "GOOGLE_AUTH_FAILED",
                    "message": "Fallo en la validación del token de Google: firma inválida, expirado o no emitido por Google.",
                },
            )

        # 4. Verificación de audiencia (aud)
        token_aud = payload.get("aud")
        if google_client_id and token_aud != google_client_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "INVALID_AUDIENCE",
                    "message": "La audiencia del token de Google no coincide con el cliente institucional autorizado.",
                },
            )

        # 5. Verificación de emisor (iss)
        token_iss = payload.get("iss")
        if token_iss not in ["accounts.google.com", "https://accounts.google.com"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "INVALID_ISSUER",
                    "message": "El emisor del token de Google no es reconocido ni autorizado.",
                },
            )

        # 6. Verificación de expiración (exp)
        exp = payload.get("exp")
        if not exp or datetime.now(UTC).timestamp() > float(exp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "TOKEN_EXPIRED",
                    "message": "El token de identidad de Google ha expirado. Por favor, inicia sesión nuevamente.",
                },
            )

        # 7. Verificación de correo validado (email_verified)
        email_verified = payload.get("email_verified")
        if email_verified not in [True, "true", "True", 1, "1"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "UNVERIFIED_EMAIL",
                    "message": "La cuenta de correo de Google no se encuentra verificada.",
                },
            )

        raw_email = payload.get("email")
        if not raw_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "MISSING_EMAIL",
                    "message": "El token de Google no contiene una dirección de correo válida.",
                },
            )

        # 8. Validación estricta del dominio institucional UPT (@virtual.upt.pe o @upt.pe)
        try:
            clean_email = validate_upt_email(raw_email)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "NON_UPT_DOMAIN", "message": str(e)},
            ) from e

        # 9. Extracción de datos del perfil y código de estudiante
        parsed = parse_student_email(clean_email)
        codigo_estudiante = parsed.get("codigo_estudiante")
        nombres = payload.get("given_name") or payload.get("first_name") or payload.get("name") or ""
        apellidos = payload.get("family_name") or payload.get("last_name") or ""
        picture = payload.get("picture")

        # 10. Persistencia / Upsert en PerfilAcademico
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
            except Exception as exc:
                db.rollback()
                logger.error("Error al persistir perfil académico en BD: %s", exc)
                if settings.STRICT_DATABASE_MODE:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail={
                            "code": "DATABASE_UNAVAILABLE",
                            "message": "Error al guardar el perfil institucional en la base de datos.",
                        },
                    ) from exc

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

        # 11. Gestión de roles según política RBAC institucional
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

        # 12. Emisión de tokens de sesión legítimos
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
