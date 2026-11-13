from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TopicBase(BaseModel):
    nombre_tema: str
    descripcion_silabo: str | None = None
    unidad_silabica: int = 1
    estado_activo: bool = True


class TopicCreatePayload(BaseModel):
    nombre_tema: str = Field(..., min_length=3, max_length=150, description="Título del tema silábico")
    descripcion_silabo: str | None = Field(None, description="Contenido analítico del sílabo")
    unidad_silabica: int = Field(1, ge=1, le=10, description="Número de unidad silábica (1 a 10)")
    estado_activo: bool = True


class TopicUpdatePayload(BaseModel):
    nombre_tema: str | None = Field(None, min_length=3, max_length=150)
    descripcion_silabo: str | None = None
    unidad_silabica: int | None = Field(None, ge=1, le=10)
    estado_activo: bool | None = None


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


class CourseCreatePayload(BaseModel):
    codigo_curso: str = Field(..., min_length=2, max_length=20, description="Código de asignatura (ej. CI-101)")
    nombre_curso: str = Field(..., min_length=3, max_length=150, description="Nombre de la asignatura")
    ciclo_plan: int = Field(..., ge=1, le=10, description="Ciclo formativo del plan de estudios (1 a 10)")
    creditos: int = Field(..., ge=1, le=10, description="Créditos académicos oficiales")
    es_prioritaria: bool = Field(True, description="Indica si es materia filtro crítica de deserción")
    factor_ponderacion: float = Field(1.0, ge=1.0, le=2.0, description="Factor de mérito algorítmico Top-k")
    estado_activo: bool = True


class CourseUpdatePayload(BaseModel):
    codigo_curso: str | None = Field(None, min_length=2, max_length=20)
    nombre_curso: str | None = Field(None, min_length=3, max_length=150)
    ciclo_plan: int | None = Field(None, ge=1, le=10)
    creditos: int | None = Field(None, ge=1, le=10)
    es_prioritaria: bool | None = None
    factor_ponderacion: float | None = Field(None, ge=1.0, le=2.0)
    estado_activo: bool | None = None


class CourseRead(CourseBase):
    id_asignatura: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CourseDetailRead(CourseRead):
    temas: list[TopicRead] = []

    model_config = ConfigDict(from_attributes=True)


class CurriculumOperationResponse(BaseModel):
    mensaje: str
    id_asignatura: int | None = None
    id_tema: int | None = None
