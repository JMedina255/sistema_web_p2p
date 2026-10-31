from fastapi import APIRouter, Depends, Header, Query, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.profiles import _resolve_authenticated_email
from app.db.session import get_optional_session
from app.schemas.booking import (
    BookingCreatePayload,
    BookingDetailResponse,
    BookingResponse,
    MentoringDemandPayload,
    MentoringDemandResponse,
)
from app.services.booking_service import BookingService

router = APIRouter()


@router.post(
    "/reserve",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Formalizar reserva transaccional de cupo con control de aforo (CUS04 / RF12 / RN-05 / RNF07)",
)
def reserve_booking(
    payload: BookingCreatePayload,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> BookingResponse:
    """
    Formaliza de manera atómica una reserva provisional bajo bloqueo pesimista
    SELECT ... FOR UPDATE en PostgreSQL, asegurando 0.0% de sobrecupo (RNF07).
    """
    caller_email = None
    if authorization:
        caller_email = _resolve_authenticated_email(
            authorization, explicit_email=payload.estudiante_email, allow_admin_override=True
        )

    return BookingService.reserve_seat(
        db=db,
        payload=payload,
        caller_email=caller_email,
    )


@router.get(
    "/my-reservations",
    response_model=list[BookingDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar nómina de reservas personales del estudiante (CUS04 / RF12)",
)
def get_my_reservations(
    estado: str | None = Query(None, description="Filtrar por estado de la reserva"),
    student_email: str | None = Query(None, description="Correo del estudiante si no se envía Bearer JWT"),
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> list[BookingDetailResponse]:
    """
    Retorna la lista de reservas registradas para el estudiante mentoreado autenticado.
    """
    effective_email = _resolve_authenticated_email(
        authorization, explicit_email=student_email, allow_admin_override=True
    )

    return BookingService.get_student_reservations(
        db=db,
        student_email=effective_email,
        estado=estado,
    )


@router.get(
    "/session/{id_sesion}",
    response_model=list[BookingDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Nómina de estudiantes inscritos para el mentor titular de la sesión (CUS04 / RN-05)",
)
def get_session_reservations(
    id_sesion: int,
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> list[BookingDetailResponse]:
    """
    Retorna la nómina de participantes inscritos para visualización del mentor titular o administrador.
    """
    caller_email = _resolve_authenticated_email(authorization, explicit_email=None, allow_admin_override=True)

    return BookingService.get_session_reservations(
        db=db,
        id_sesion=id_sesion,
        caller_email=caller_email,
    )


@router.post(
    "/requests",
    response_model=MentoringDemandResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar solicitud temática de mentoría por demanda (CUS03 / RF07)",
)
def create_demand_request(
    payload: MentoringDemandPayload,
    student_email: str | None = Query(None, description="Correo del solicitante"),
    authorization: str | None = Header(None),
    db: Session | None = Depends(get_optional_session),
) -> MentoringDemandResponse:
    """
    Permite al estudiante mentoreado registrar una necesidad formativa específica
    cuando no halla sesiones activas en el feed de recomendaciones.
    """
    effective_email = _resolve_authenticated_email(
        authorization, explicit_email=student_email, allow_admin_override=True
    )

    return BookingService.create_demand_request(
        db=db,
        payload=payload,
        student_email=effective_email,
    )


@router.get(
    "/requests",
    response_model=list[MentoringDemandResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar banco institucional de solicitudes por demanda activas (CUS03 / RF07)",
)
def get_demand_requests(
    id_asignatura: int | None = Query(None, description="Filtrar por ID de asignatura"),
    ciclo: int | None = Query(None, description="Filtrar por ciclo del plan formativo"),
    db: Session | None = Depends(get_optional_session),
) -> list[MentoringDemandResponse]:
    """
    Expone el banco de solicitudes de mentoría pendientes para que los mentores
    puedan formular ofertas dirigidas a temas con demanda insatisfecha.
    """
    return BookingService.get_demand_requests(
        db=db,
        id_asignatura=id_asignatura,
        ciclo=ciclo,
    )
