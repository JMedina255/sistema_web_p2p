from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_optional_session
from app.schemas.curriculum import CourseDetailRead, CourseRead, TopicRead
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
