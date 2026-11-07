from pydantic import BaseModel, Field


class AttendanceTokenResponse(BaseModel):
    """
    Respuesta con token criptográfico TOTP dinámico de asistencia (T-34 / T-36 / CUS12 / RN-12).
    """

    session_id: int
    token: str
    totp_code: str
    expires_in: int = 30
    expires_at: str


class AttendanceCheckinPayload(BaseModel):
    """
    Payload para registro de check-in de asistencia del estudiante mentoreado.
    """

    qr_token: str | None = Field(None, description="Token dinámico capturado del código QR.")
    numeric_code: str | None = Field(None, description="Código numérico de 6 dígitos de respaldo.")
    estudiante_email: str | None = Field(None, description="Correo del estudiante en caso de pase asistido.")


class AttendanceCheckinResponse(BaseModel):
    """
    Respuesta de confirmación de check-in de asistencia.
    """

    id_asistencia: int
    id_sesion: int
    estudiante_email: str
    asistio: bool
    fecha_checkin: str
    mensaje: str = "Asistencia registrada exitosamente."


class AttendanceItemResponse(BaseModel):
    """
    Item individual en la nómina de asistencia de una sesión.
    """

    id_asistencia: int
    id_sesion: int
    estudiante_email: str
    asistio: bool
    fecha_checkin: str | None = None
