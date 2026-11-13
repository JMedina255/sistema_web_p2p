from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import AuthenticatedUser, require_role
from app.db.session import get_optional_session
from app.schemas.curriculum import (
    CourseCreatePayload,
    CourseDetailRead,
    CourseRead,
    CourseUpdatePayload,
    CurriculumOperationResponse,
    TopicCreatePayload,
    TopicRead,
    TopicUpdatePayload,
)
from app.services.curriculum_service import CurriculumService

router = APIRouter()


@router.get(
    "/courses",
    response_model=list[CourseRead],
    summary="Listar catálogo de asignaturas formativas",
    description="Retorna el catálogo curricular de materias de la EPIS-UPT con filtros opcionales (T-09 / CUS21 / RF05).",
)
def list_courses(
    only_priority: bool = Query(
        default=False, description="Filtrar únicamente asignaturas formativas prioritarias/filtro"
    ),
    ciclo: int | None = Query(
        default=None, ge=1, le=10, description="Filtrar por ciclo curricular del plan de estudios"
    ),
    db: Session | None = Depends(get_optional_session),
):
    courses = CurriculumService.get_courses(db=db, only_priority=only_priority, ciclo=ciclo)
    return courses


@router.get(
    "/courses/{id_asignatura}",
    response_model=CourseDetailRead,
    summary="Consultar detalle de una asignatura con sus temas silábicos",
    description="Retorna la información curricular completa y el desglose de temas silábicos de una materia crítica.",
)
def get_course_detail(
    id_asignatura: int,
    db: Session | None = Depends(get_optional_session),
):
    course = CurriculumService.get_course_by_id(db=db, id_asignatura=id_asignatura)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asignatura con ID {id_asignatura} no encontrada en el catálogo curricular.",
        )
    return course


@router.get(
    "/courses/{id_asignatura}/topics",
    response_model=list[TopicRead],
    summary="Listar temas conceptuales y unidades silábicas de una asignatura",
    description="Retorna la taxonomía jerárquica de temas silábicos requeridos para el motor de recomendación y publicación de ofertas.",
)
def get_course_topics(
    id_asignatura: int,
    db: Session | None = Depends(get_optional_session),
):
    course = CurriculumService.get_course_by_id(db=db, id_asignatura=id_asignatura)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asignatura con ID {id_asignatura} no encontrada.",
        )
    topics = CurriculumService.get_course_topics(db=db, id_asignatura=id_asignatura)
    return topics


@router.post(
    "/courses",
    response_model=CourseRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nueva asignatura crítica formativa (RF05 / CUS21)",
    description="Permite al Administrador dar de alta una nueva materia crítica con sus metadatos curriculares.",
)
def create_course(
    payload: CourseCreatePayload,
    current_user: AuthenticatedUser = Depends(require_role("administrador")),
    db: Session | None = Depends(get_optional_session),
):
    return CurriculumService.create_course(db=db, payload=payload)


@router.put(
    "/courses/{id_asignatura}",
    response_model=CourseRead,
    status_code=status.HTTP_200_OK,
    summary="Actualizar asignatura del catálogo oficial (RF05 / CUS21)",
    description="Permite al Administrador actualizar créditos, ciclo, ponderación o estado de una materia.",
)
def update_course(
    id_asignatura: int,
    payload: CourseUpdatePayload,
    current_user: AuthenticatedUser = Depends(require_role("administrador")),
    db: Session | None = Depends(get_optional_session),
):
    return CurriculumService.update_course(db=db, id_asignatura=id_asignatura, payload=payload)


@router.delete(
    "/courses/{id_asignatura}",
    response_model=CurriculumOperationResponse,
    status_code=status.HTTP_200_OK,
    summary="Desactivar asignatura del catálogo oficial (RF05 / CUS21)",
    description="Desactiva lógicamente una asignatura para preservar la integridad de sesiones históricas.",
)
def delete_course(
    id_asignatura: int,
    current_user: AuthenticatedUser = Depends(require_role("administrador")),
    db: Session | None = Depends(get_optional_session),
):
    result = CurriculumService.delete_course(db=db, id_asignatura=id_asignatura)
    return CurriculumOperationResponse(
        mensaje=result["mensaje"],
        id_asignatura=id_asignatura,
    )


@router.post(
    "/courses/{id_asignatura}/topics",
    response_model=TopicRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo tema conceptual silábico (RF05 / CUS21)",
    description="Permite al Administrador incorporar una nueva unidad temática oficial al sílabo de la materia.",
)
def create_topic(
    id_asignatura: int,
    payload: TopicCreatePayload,
    current_user: AuthenticatedUser = Depends(require_role("administrador")),
    db: Session | None = Depends(get_optional_session),
):
    return CurriculumService.create_topic(db=db, id_asignatura=id_asignatura, payload=payload)


@router.put(
    "/topics/{id_tema}",
    response_model=TopicRead,
    status_code=status.HTTP_200_OK,
    summary="Actualizar tema conceptual silábico (RF05 / CUS21)",
    description="Permite al Administrador modificar el título, descripción o unidad silábica de un concepto.",
)
def update_topic(
    id_tema: int,
    payload: TopicUpdatePayload,
    current_user: AuthenticatedUser = Depends(require_role("administrador")),
    db: Session | None = Depends(get_optional_session),
):
    return CurriculumService.update_topic(db=db, id_tema=id_tema, payload=payload)


@router.delete(
    "/topics/{id_tema}",
    response_model=CurriculumOperationResponse,
    status_code=status.HTTP_200_OK,
    summary="Desactivar tema conceptual silábico (RF05 / CUS21)",
    description="Desactiva lógicamente un tema del temario silábico oficial.",
)
def delete_topic(
    id_tema: int,
    current_user: AuthenticatedUser = Depends(require_role("administrador")),
    db: Session | None = Depends(get_optional_session),
):
    result = CurriculumService.delete_topic(db=db, id_tema=id_tema)
    return CurriculumOperationResponse(
        mensaje=result["mensaje"],
        id_tema=id_tema,
    )
