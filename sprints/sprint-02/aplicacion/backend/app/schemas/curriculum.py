from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TopicBase(BaseModel):
    nombre_tema: str
    descripcion_silabo: str | None = None
    unidad_silabica: int = 1
    estado_activo: bool = True


class TopicRead(TopicBase):
    id_tema: int
    id_asignatura: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CourseBase(BaseModel):
    codigo_curso: str
    nombre_curso: str
    ciclo_plan: int
    creditos: int
    es_prioritaria: bool = True
    factor_ponderacion: float = 1.0
    estado_activo: bool = True


class CourseRead(CourseBase):
    id_asignatura: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CourseDetailRead(CourseRead):
    temas: list[TopicRead] = []

    model_config = ConfigDict(from_attributes=True)
