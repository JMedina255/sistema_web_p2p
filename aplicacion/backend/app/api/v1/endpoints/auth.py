from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_optional_session
from app.schemas.auth import (
    RequestOtpPayload,
    RequestOtpResponse,
    ResendOtpPayload,
    VerifyOtpPayload,
    VerifyOtpResponse,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/otp/request",
    response_model=RequestOtpResponse,
    status_code=status.HTTP_200_OK,
    summary="Solicitar código OTP de acceso institucional",
    description="Emite un desafío de autenticación temporal de 6 dígitos numéricos para correos @upt.pe con vigencia de 5 minutos (T-03 / CUS01 / RF01 / RNF01).",
)
def request_otp(
    payload: RequestOtpPayload,
    db: Session | None = Depends(get_optional_session),
):
    return AuthService.request_otp(db=db, email=payload.email)


@router.post(
    "/otp/resend",
    response_model=RequestOtpResponse,
    status_code=status.HTTP_200_OK,
    summary="Reenviar código OTP de acceso",
    description="Invalida el desafío anterior y genera uno nuevo respetando el cooldown de 60 segundos.",
)
def resend_otp(
    payload: ResendOtpPayload,
    db: Session | None = Depends(get_optional_session),
):
    return AuthService.resend_otp(db=db, challenge_id=payload.challengeId)


@router.post(
    "/otp/verify",
    response_model=VerifyOtpResponse,
    status_code=status.HTTP_200_OK,
    summary="Verificar código OTP y emitir JWT de sesión",
    description="Valida los 6 dígitos del desafío OTP y emite un JWT de sesión firmado institucionalmente.",
)
def verify_otp(
    payload: VerifyOtpPayload,
    db: Session | None = Depends(get_optional_session),
):
    return AuthService.verify_otp(db=db, challenge_id=payload.challengeId, otp=payload.otp)
