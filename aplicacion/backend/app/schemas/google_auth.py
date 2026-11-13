from pydantic import BaseModel, Field


class GoogleLoginPayload(BaseModel):
    """
    Payload para autenticación institucional federada con Google Workspace.
    Recibe el token de identidad JWT emitido tras el consentimiento OIDC.
    """

    id_token: str = Field(
        ...,
        description="Token de identidad emitido por Google Identity Services o Supabase Auth",
    )


class GoogleLoginResponse(BaseModel):
    """
    Respuesta de sesión tras autenticación exitosa con Google Workspace.
    Retorna los tokens JWT de sesión del sistema P2P y los datos formativos precargados.
    """

    success: bool = True
    email: str
    codigo_estudiante: str | None = None
    nombres: str | None = None
    apellidos: str | None = None
    picture: str | None = None
    primary_role: str
    roles: list[str] = Field(default_factory=list)
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    message: str = "Autenticación federada exitosa con Google Workspace UPT"
