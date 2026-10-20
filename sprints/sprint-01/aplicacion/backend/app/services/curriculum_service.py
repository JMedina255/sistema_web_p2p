from sqlalchemy.orm import Session, selectinload

from app.models.curriculum import Asignatura, TemaConceptual

# Catálogo estático de reserva (fallback para pruebas o sin conexión a BD)
DEFAULT_FILTER_COURSES = [
    {
        "id_asignatura": 1,
        "codigo_curso": "CALC-101",
        "nombre_curso": "Cálculo I",
        "ciclo_plan": 1,
        "creditos": 4,
        "es_prioritaria": True,
        "factor_ponderacion": 1.2,
        "estado_activo": True,
        "temas": [
            {
                "id_tema": 1,
                "id_asignatura": 1,
                "nombre_tema": "Límites y Continuidad",
                "descripcion_silabo": "Concepto intuitivo y formal de límite, límites laterales, infinitos y al infinito. Asíntotas y continuidad de funciones.",
                "unidad_silabica": 1,
                "estado_activo": True,
            },
            {
                "id_tema": 2,
                "id_asignatura": 1,
                "nombre_tema": "Derivadas y Reglas de Derivación",
                "descripcion_silabo": "Definición de derivada, regla de la cadena, derivación implícita y derivadas de orden superior.",
                "unidad_silabica": 2,
                "estado_activo": True,
            },
            {
                "id_tema": 3,
                "id_asignatura": 1,
                "nombre_tema": "Aplicaciones de la Derivada",
                "descripcion_silabo": "Criterios de primera y segunda derivada, optimización y problemas de razón de cambio relacionada.",
                "unidad_silabica": 3,
                "estado_activo": True,
            },
            {
                "id_tema": 4,
                "id_asignatura": 1,
                "nombre_tema": "Integrales Indefinidas",
                "descripcion_silabo": "Antiderivadas y propiedades fundamentales de la integración indefinida.",
                "unidad_silabica": 4,
                "estado_activo": True,
            },
        ],
    },
    {
        "id_asignatura": 2,
        "codigo_curso": "CALC-201",
        "nombre_curso": "Cálculo II",
        "ciclo_plan": 2,
        "creditos": 4,
        "es_prioritaria": True,
        "factor_ponderacion": 1.2,
        "estado_activo": True,
        "temas": [
            {
                "id_tema": 5,
                "id_asignatura": 2,
                "nombre_tema": "Métodos Avanzados de Integración",
                "descripcion_silabo": "Integración por partes, sustitución trigonométrica y descomposición en fracciones parciales.",
                "unidad_silabica": 1,
                "estado_activo": True,
            },
            {
                "id_tema": 6,
                "id_asignatura": 2,
                "nombre_tema": "Integral Definida y Aplicaciones",
                "descripcion_silabo": "Teorema Fundamental del Cálculo, cálculo de áreas planas, volúmenes de sólidos de revolución y longitud de arco.",
                "unidad_silabica": 2,
                "estado_activo": True,
            },
            {
                "id_tema": 7,
                "id_asignatura": 2,
                "nombre_tema": "Series y Sucesiones Infinitas",
                "descripcion_silabo": "Convergencia de series numéricas, criterios de comparación, series de potencias y series de Taylor/Maclaurin.",
                "unidad_silabica": 3,
                "estado_activo": True,
            },
            {
                "id_tema": 8,
                "id_asignatura": 2,
                "nombre_tema": "Ecuaciones Diferenciales de Primer Orden",
                "descripcion_silabo": "Ecuaciones de variables separables, homogéneas, lineales exactas y aplicaciones de modelado.",
                "unidad_silabica": 4,
                "estado_activo": True,
            },
        ],
    },
    {
        "id_asignatura": 3,
        "codigo_curso": "ALGO-202",
        "nombre_curso": "Algoritmos y Estructuras de Datos",
        "ciclo_plan": 2,
        "creditos": 4,
        "es_prioritaria": True,
        "factor_ponderacion": 1.3,
        "estado_activo": True,
        "temas": [
            {
                "id_tema": 9,
                "id_asignatura": 3,
                "nombre_tema": "Análisis Asintótico y Notación Big-O",
                "descripcion_silabo": "Complejidad temporal y espacial, órdenes de magnitud (O, Omega, Theta) y análisis de algoritmos iterativos.",
                "unidad_silabica": 1,
                "estado_activo": True,
            },
            {
                "id_tema": 10,
                "id_asignatura": 3,
                "nombre_tema": "Recursividad y Relaciones de Recurrencia",
                "descripcion_silabo": "Diseño de algoritmos recursivos, teorema maestro y árbol de recursión.",
                "unidad_silabica": 2,
                "estado_activo": True,
            },
            {
                "id_tema": 11,
                "id_asignatura": 3,
                "nombre_tema": "Punteros y Gestión Dinámica de Memoria en C++",
                "descripcion_silabo": "Aritmética de punteros, asignación dinámica en heap (new/delete), referencias y fugas de memoria.",
                "unidad_silabica": 3,
                "estado_activo": True,
            },
            {
                "id_tema": 12,
                "id_asignatura": 3,
                "nombre_tema": "Estructuras Lineales: Pilas, Colas y Listas",
                "descripcion_silabo": "Listas enlazadas simples, dobles y circulares. Implementación de TAD Pila (LIFO) y TAD Cola (FIFO).",
                "unidad_silabica": 4,
                "estado_activo": True,
            },
            {
                "id_tema": 13,
                "id_asignatura": 3,
                "nombre_tema": "Árboles Binarios de Búsqueda y Grafos",
                "descripcion_silabo": "Recorridos in-order, pre-order, post-order, balanceo y representaciones de grafos con listas de adyacencia.",
                "unidad_silabica": 5,
                "estado_activo": True,
            },
        ],
    },
    {
        "id_asignatura": 4,
        "codigo_curso": "POO-301",
        "nombre_curso": "Programación Orientada a Objetos",
        "ciclo_plan": 3,
        "creditos": 4,
        "es_prioritaria": True,
        "factor_ponderacion": 1.2,
        "estado_activo": True,
        "temas": [
            {
                "id_tema": 14,
                "id_asignatura": 4,
                "nombre_tema": "Clases, Objetos y Encapsulamiento",
                "descripcion_silabo": "Atributos, métodos, constructores, destructores y modificadores de acceso (public, private, protected).",
                "unidad_silabica": 1,
                "estado_activo": True,
            },
            {
                "id_tema": 15,
                "id_asignatura": 4,
                "nombre_tema": "Herencia, Polimorfismo e Interfaces",
                "descripcion_silabo": "Reutilización mediante jerarquías de clases, métodos virtuales, ligadura dinámica y clases abstractas.",
                "unidad_silabica": 2,
                "estado_activo": True,
            },
            {
                "id_tema": 16,
                "id_asignatura": 4,
                "nombre_tema": "Manejo Robusto de Excepciones",
                "descripcion_silabo": "Bloques try-catch-finally, propagación de excepciones estándar y creación de excepciones de dominio personalizadas.",
                "unidad_silabica": 3,
                "estado_activo": True,
            },
            {
                "id_tema": 17,
                "id_asignatura": 4,
                "nombre_tema": "Principios SOLID y Patrones de Diseño",
                "descripcion_silabo": "Responsabilidad Única, Abierto/Cerrado, Sustitución de Liskov, Segregación de Interfaces e Inversión de Dependencias. Patrones Singleton y Factory.",
                "unidad_silabica": 4,
                "estado_activo": True,
            },
        ],
    },
    {
        "id_asignatura": 5,
        "codigo_curso": "BDD-401",
        "nombre_curso": "Base de Datos",
        "ciclo_plan": 4,
        "creditos": 4,
        "es_prioritaria": True,
        "factor_ponderacion": 1.1,
        "estado_activo": True,
        "temas": [
            {
                "id_tema": 18,
                "id_asignatura": 5,
                "nombre_tema": "Modelado Conceptual Entidad-Relación",
                "descripcion_silabo": "Entidades fuertes y débiles, atributos, cardinalidades y transformación al modelo relacional.",
                "unidad_silabica": 1,
                "estado_activo": True,
            },
            {
                "id_tema": 19,
                "id_asignatura": 5,
                "nombre_tema": "Normalización Relacional (1FN, 2FN, 3FN, BCNF)",
                "descripcion_silabo": "Dependencias funcionales, eliminación de redundancias y anomalías de inserción, actualización y borrado.",
                "unidad_silabica": 2,
                "estado_activo": True,
            },
            {
                "id_tema": 20,
                "id_asignatura": 5,
                "nombre_tema": "Lenguaje SQL: DDL, DML y Subconsultas",
                "descripcion_silabo": "Definición de esquemas, restricciones de integridad, joins (INNER, LEFT, RIGHT), agrupamientos y funciones agregadas.",
                "unidad_silabica": 3,
                "estado_activo": True,
            },
            {
                "id_tema": 21,
                "id_asignatura": 5,
                "nombre_tema": "Transacciones, Propiedades ACID y Concurrencia",
                "descripcion_silabo": "Atomicidad, Consistencia, Aislamiento y Durabilidad. Niveles de aislamiento y control de bloqueos.",
                "unidad_silabica": 4,
                "estado_activo": True,
            },
        ],
    },
]


class CurriculumService:
    @staticmethod
    def get_courses(
        db: Session | None = None, only_priority: bool = False, ciclo: int | None = None
    ) -> list[Asignatura] | list[dict]:
        """
        Retorna las asignaturas del catálogo curricular filtradas por prioridad o ciclo.
        Si la sesión de base de datos está disponible y contiene registros, consulta la BD;
        en caso de estar sin migrar o vacía, utiliza el catálogo canónico de las 5 materias filtro.
        """
        if db is not None:
            try:
                total_courses = db.query(Asignatura).count()
                if total_courses > 0:
                    query = db.query(Asignatura).filter(Asignatura.estado_activo.is_(True))
                    if only_priority:
                        query = query.filter(Asignatura.es_prioritaria.is_(True))
                    if ciclo is not None:
                        query = query.filter(Asignatura.ciclo_plan == ciclo)
                    return query.order_by(Asignatura.ciclo_plan, Asignatura.codigo_curso).all()
            except Exception:
                pass

        # Fallback determinista al catálogo de las 5 materias filtro
        result = [c for c in DEFAULT_FILTER_COURSES if c["estado_activo"]]
        if only_priority:
            result = [c for c in result if c["es_prioritaria"]]
        if ciclo is not None:
            result = [c for c in result if c["ciclo_plan"] == ciclo]
        return result

    @staticmethod
    def get_course_by_id(db: Session | None, id_asignatura: int) -> Asignatura | dict | None:
        """
        Retorna el detalle de una asignatura específica junto con sus temas silábicos.
        """
        if db is not None:
            try:
                total_courses = db.query(Asignatura).count()
                if total_courses > 0:
                    course = (
                        db.query(Asignatura)
                        .options(selectinload(Asignatura.temas))
                        .filter(Asignatura.id_asignatura == id_asignatura, Asignatura.estado_activo.is_(True))
                        .first()
                    )
                    return course
            except Exception:
                pass

        for c in DEFAULT_FILTER_COURSES:
            if c["id_asignatura"] == id_asignatura and c["estado_activo"]:
                return c
        return None

    @staticmethod
    def get_course_topics(db: Session | None, id_asignatura: int) -> list[TemaConceptual] | list[dict]:
        """
        Retorna los temas conceptuales asociados a una asignatura específica.
        """
        if db is not None:
            try:
                total_topics = db.query(TemaConceptual).count()
                if total_topics > 0:
                    return (
                        db.query(TemaConceptual)
                        .filter(
                            TemaConceptual.id_asignatura == id_asignatura,
                            TemaConceptual.estado_activo.is_(True),
                        )
                        .order_by(TemaConceptual.unidad_silabica, TemaConceptual.id_tema)
                        .all()
                    )
            except Exception:
                pass

        course = CurriculumService.get_course_by_id(db, id_asignatura)
        if not course:
            return []
        if isinstance(course, dict):
            return course.get("temas", [])
        return getattr(course, "temas", [])
