"""initial_curriculum_and_auth

Revision ID: 20261019_001
Revises:
Create Date: 2026-10-19 18:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql import column, table

# revision identifiers, used by Alembic.
revision: str = "20261019_001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Creación de la tabla asignaturas (CUS21 / RF05 / MOD-02)
    op.create_table(
        "asignaturas",
        sa.Column("id_asignatura", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("codigo_curso", sa.String(length=20), nullable=False),
        sa.Column("nombre_curso", sa.String(length=150), nullable=False),
        sa.Column("ciclo_plan", sa.Integer(), nullable=False),
        sa.Column("creditos", sa.Integer(), nullable=False),
        sa.Column("es_prioritaria", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("factor_ponderacion", sa.Float(), server_default=sa.text("1.0"), nullable=False),
        sa.Column("estado_activo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id_asignatura"),
        sa.UniqueConstraint("codigo_curso"),
    )
    op.create_index(op.f("ix_asignaturas_codigo_curso"), "asignaturas", ["codigo_curso"], unique=True)

    # 2. Creación de la tabla temas_conceptuales (CUS21 / RF05)
    op.create_table(
        "temas_conceptuales",
        sa.Column("id_tema", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_asignatura", sa.Integer(), nullable=False),
        sa.Column("nombre_tema", sa.String(length=150), nullable=False),
        sa.Column("descripcion_silabo", sa.Text(), nullable=True),
        sa.Column("unidad_silabica", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("estado_activo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["id_asignatura"], ["asignaturas.id_asignatura"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id_tema"),
    )
    op.create_index(
        op.f("ix_temas_conceptuales_id_asignatura"), "temas_conceptuales", ["id_asignatura"], unique=False
    )

    # 3. Creación de la tabla auth_challenges (T-03 / CUS01 / RF01 / RNF01)
    op.create_table(
        "auth_challenges",
        sa.Column("id_challenge", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("code_hash", sa.String(length=255), nullable=False),
        sa.Column("code_salt", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resend_available_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("attempts", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.PrimaryKeyConstraint("id_challenge"),
    )
    op.create_index(op.f("ix_auth_challenges_email"), "auth_challenges", ["email"], unique=False)

    # 4. Inserción de Datos Semilla para las 5 Materias Filtro de la EPIS-UPT (T-09)
    asignaturas_table = table(
        "asignaturas",
        column("id_asignatura", sa.Integer),
        column("codigo_curso", sa.String),
        column("nombre_curso", sa.String),
        column("ciclo_plan", sa.Integer),
        column("creditos", sa.Integer),
        column("es_prioritaria", sa.Boolean),
        column("factor_ponderacion", sa.Float),
        column("estado_activo", sa.Boolean),
    )

    temas_table = table(
        "temas_conceptuales",
        column("id_asignatura", sa.Integer),
        column("nombre_tema", sa.String),
        column("descripcion_silabo", sa.Text),
        column("unidad_silabica", sa.Integer),
        column("estado_activo", sa.Boolean),
    )

    op.bulk_insert(
        asignaturas_table,
        [
            {
                "id_asignatura": 1,
                "codigo_curso": "CALC-101",
                "nombre_curso": "Cálculo I",
                "ciclo_plan": 1,
                "creditos": 4,
                "es_prioritaria": True,
                "factor_ponderacion": 1.2,
                "estado_activo": True,
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
            },
        ],
    )

    # Inserción de Unidades Temáticas Silábicas Oficiales
    op.bulk_insert(
        temas_table,
        [
            # Cálculo I
            {
                "id_asignatura": 1,
                "nombre_tema": "Límites y Continuidad",
                "descripcion_silabo": "Concepto intuitivo y formal de límite, límites laterales, infinitos y al infinito. Asíntotas y continuidad de funciones.",
                "unidad_silabica": 1,
                "estado_activo": True,
            },
            {
                "id_asignatura": 1,
                "nombre_tema": "Derivadas y Reglas de Derivación",
                "descripcion_silabo": "Definición de derivada, regla de la cadena, derivación implícita y derivadas de orden superior.",
                "unidad_silabica": 2,
                "estado_activo": True,
            },
            {
                "id_asignatura": 1,
                "nombre_tema": "Aplicaciones de la Derivada",
                "descripcion_silabo": "Criterios de primera y segunda derivada, optimización y problemas de razón de cambio relacionada.",
                "unidad_silabica": 3,
                "estado_activo": True,
            },
            {
                "id_asignatura": 1,
                "nombre_tema": "Integrales Indefinidas",
                "descripcion_silabo": "Antiderivadas y propiedades fundamentales de la integración indefinida.",
                "unidad_silabica": 4,
                "estado_activo": True,
            },
            # Cálculo II
            {
                "id_asignatura": 2,
                "nombre_tema": "Métodos Avanzados de Integración",
                "descripcion_silabo": "Integración por partes, sustitución trigonométrica y descomposición en fracciones parciales.",
                "unidad_silabica": 1,
                "estado_activo": True,
            },
            {
                "id_asignatura": 2,
                "nombre_tema": "Integral Definida y Aplicaciones",
                "descripcion_silabo": "Teorema Fundamental del Cálculo, cálculo de áreas planas, volúmenes de sólidos de revolución y longitud de arco.",
                "unidad_silabica": 2,
                "estado_activo": True,
            },
            {
                "id_asignatura": 2,
                "nombre_tema": "Series y Sucesiones Infinitas",
                "descripcion_silabo": "Convergencia de series numéricas, criterios de comparación, series de potencias y series de Taylor/Maclaurin.",
                "unidad_silabica": 3,
                "estado_activo": True,
            },
            {
                "id_asignatura": 2,
                "nombre_tema": "Ecuaciones Diferenciales de Primer Orden",
                "descripcion_silabo": "Ecuaciones de variables separables, homogéneas, lineales exactas y aplicaciones de modelado.",
                "unidad_silabica": 4,
                "estado_activo": True,
            },
            # Algoritmos y Estructuras de Datos
            {
                "id_asignatura": 3,
                "nombre_tema": "Análisis Asintótico y Notación Big-O",
                "descripcion_silabo": "Complejidad temporal y espacial, órdenes de magnitud (O, Omega, Theta) y análisis de algoritmos iterativos.",
                "unidad_silabica": 1,
                "estado_activo": True,
            },
            {
                "id_asignatura": 3,
                "nombre_tema": "Recursividad y Relaciones de Recurrencia",
                "descripcion_silabo": "Diseño de algoritmos recursivos, teorema maestro y árbol de recursión.",
                "unidad_silabica": 2,
                "estado_activo": True,
            },
            {
                "id_asignatura": 3,
                "nombre_tema": "Punteros y Gestión Dinámica de Memoria en C++",
                "descripcion_silabo": "Aritmética de punteros, asignación dinámica en heap (new/delete), referencias y fugas de memoria.",
                "unidad_silabica": 3,
                "estado_activo": True,
            },
            {
                "id_asignatura": 3,
                "nombre_tema": "Estructuras Lineales: Pilas, Colas y Listas",
                "descripcion_silabo": "Listas enlazadas simples, dobles y circulares. Implementación de TAD Pila (LIFO) y TAD Cola (FIFO).",
                "unidad_silabica": 4,
                "estado_activo": True,
            },
            {
                "id_asignatura": 3,
                "nombre_tema": "Árboles Binarios de Búsqueda y Grafos",
                "descripcion_silabo": "Recorridos in-order, pre-order, post-order, balanceo y representaciones de grafos con listas de adyacencia.",
                "unidad_silabica": 5,
                "estado_activo": True,
            },
            # Programación Orientada a Objetos
            {
                "id_asignatura": 4,
                "nombre_tema": "Clases, Objetos y Encapsulamiento",
                "descripcion_silabo": "Atributos, métodos, constructores, destructores y modificadores de acceso (public, private, protected).",
                "unidad_silabica": 1,
                "estado_activo": True,
            },
            {
                "id_asignatura": 4,
                "nombre_tema": "Herencia, Polimorfismo e Interfaces",
                "descripcion_silabo": "Reutilización mediante jerarquías de clases, métodos virtuales, ligadura dinámica y clases abstractas.",
                "unidad_silabica": 2,
                "estado_activo": True,
            },
            {
                "id_asignatura": 4,
                "nombre_tema": "Manejo Robusto de Excepciones",
                "descripcion_silabo": "Bloques try-catch-finally, propagación de excepciones estándar y creación de excepciones de dominio personalizadas.",
                "unidad_silabica": 3,
                "estado_activo": True,
            },
            {
                "id_asignatura": 4,
                "nombre_tema": "Principios SOLID y Patrones de Diseño",
                "descripcion_silabo": "Responsabilidad Única, Abierto/Cerrado, Sustitución de Liskov, Segregación de Interfaces e Inversión de Dependencias. Patrones Singleton y Factory.",
                "unidad_silabica": 4,
                "estado_activo": True,
            },
            # Base de Datos
            {
                "id_asignatura": 5,
                "nombre_tema": "Modelado Conceptual Entidad-Relación",
                "descripcion_silabo": "Entidades fuertes y débiles, atributos, cardinalidades y transformación al modelo relacional.",
                "unidad_silabica": 1,
                "estado_activo": True,
            },
            {
                "id_asignatura": 5,
                "nombre_tema": "Normalización Relacional (1FN, 2FN, 3FN, BCNF)",
                "descripcion_silabo": "Dependencias funcionales, eliminación de redundancias y anomalías de inserción, actualización y borrado.",
                "unidad_silabica": 2,
                "estado_activo": True,
            },
            {
                "id_asignatura": 5,
                "nombre_tema": "Lenguaje SQL: DDL, DML y Subconsultas",
                "descripcion_silabo": "Definición de esquemas, restricciones de integridad, joins (INNER, LEFT, RIGHT), agrupamientos y funciones agregadas.",
                "unidad_silabica": 3,
                "estado_activo": True,
            },
            {
                "id_asignatura": 5,
                "nombre_tema": "Transacciones, Propiedades ACID y Concurrencia",
                "descripcion_silabo": "Atomicidad, Consistencia, Aislamiento y Durabilidad. Niveles de aislamiento y control de bloqueos.",
                "unidad_silabica": 4,
                "estado_activo": True,
            },
        ],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_auth_challenges_email"), table_name="auth_challenges")
    op.drop_table("auth_challenges")
    op.drop_index(op.f("ix_temas_conceptuales_id_asignatura"), table_name="temas_conceptuales")
    op.drop_table("temas_conceptuales")
    op.drop_index(op.f("ix_asignaturas_codigo_curso"), table_name="asignaturas")
    op.drop_table("asignaturas")
