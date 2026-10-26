"""roles_and_profiles

Revision ID: 20261023_002
Revises: 20261019_001
Create Date: 2026-10-23 20:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql import column, table

# revision identifiers, used by Alembic.
revision: str = "20261023_002"
down_revision: str | None = "20261019_001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Creación de la tabla consentimientos_legales (T-05 / RF02 / RN-02 / Ley 29733)
    op.create_table(
        "consentimientos_legales",
        sa.Column("id_consentimiento", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column(
            "terms_version", sa.String(length=50), server_default=sa.text("'2026-II-v1.0'"), nullable=False
        ),
        sa.Column("accepted", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "consented_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id_consentimiento"),
    )
    op.create_index(
        op.f("ix_consentimientos_legales_email"), "consentimientos_legales", ["email"], unique=False
    )

    # 2. Creación de la tabla roles (T-08 / RF03 / CUS10 / RN-03)
    op.create_table(
        "roles",
        sa.Column("id_rol", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre_rol", sa.String(length=50), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id_rol"),
        sa.UniqueConstraint("nombre_rol"),
    )
    op.create_index(op.f("ix_roles_nombre_rol"), "roles", ["nombre_rol"], unique=True)

    # Inserción de Roles Semilla Institucionales
    roles_table = table(
        "roles",
        column("id_rol", sa.Integer),
        column("nombre_rol", sa.String),
        column("descripcion", sa.Text),
    )
    op.bulk_insert(
        roles_table,
        [
            {
                "id_rol": 1,
                "nombre_rol": "mentoreado",
                "descripcion": "Estudiante que solicita orientación o mentoría académica en asignaturas filtro.",
            },
            {
                "id_rol": 2,
                "nombre_rol": "mentor",
                "descripcion": "Estudiante de ciclo avanzado (>= VII) con mérito académico habilitado para brindar orientación formativa.",
            },
            {
                "id_rol": 3,
                "nombre_rol": "administrador",
                "descripcion": "Personal docente o administrativo con permisos de gestión, auditoría y supervisión de roles.",
            },
        ],
    )

    # 3. Creación de la tabla usuario_roles (T-08 / RF03 / CUS10)
    op.create_table(
        "usuario_roles",
        sa.Column("id_usuario_rol", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("id_rol", sa.Integer(), nullable=False),
        sa.Column(
            "fecha_asignacion", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("asignado_por", sa.String(length=255), nullable=True),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.ForeignKeyConstraint(["id_rol"], ["roles.id_rol"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id_usuario_rol"),
        sa.UniqueConstraint("email", "id_rol", name="uq_usuario_roles_email_rol"),
    )
    op.create_index(op.f("ix_usuario_roles_email"), "usuario_roles", ["email"], unique=False)

    # 4. Creación de la tabla perfiles_academicos (T-12 / RF04 / CUS15 / RNF04)
    op.create_table(
        "perfiles_academicos",
        sa.Column("id_perfil", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("codigo_estudiante", sa.String(length=20), nullable=True),
        sa.Column("nombres", sa.String(length=100), nullable=True),
        sa.Column("apellidos", sa.String(length=100), nullable=True),
        sa.Column(
            "ciclo_actual",
            sa.Integer(),
            sa.CheckConstraint("ciclo_actual >= 1 AND ciclo_actual <= 10", name="chk_ciclo_actual"),
            server_default=sa.text("1"),
            nullable=False,
        ),
        sa.Column(
            "rol_postulacion", sa.String(length=20), server_default=sa.text("'mentoreado'"), nullable=False
        ),
        sa.Column("materias_interes", sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
        sa.Column("temas_seleccionados", sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
        sa.Column("biografia", sa.Text(), nullable=True),
        sa.Column(
            "modalidad_preferida",
            sa.String(length=20),
            server_default=sa.text("'presencial'"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id_perfil"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_perfiles_academicos_email"), "perfiles_academicos", ["email"], unique=True)

    # 5. Creación de la tabla disponibilidades_horarias (T-12 / RF04 / CUS15)
    op.create_table(
        "disponibilidades_horarias",
        sa.Column("id_disponibilidad", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column(
            "dia_semana",
            sa.Integer(),
            sa.CheckConstraint("dia_semana >= 1 AND dia_semana <= 6", name="chk_dia_semana"),
            nullable=False,
        ),
        sa.Column("hora_inicio", sa.String(length=10), nullable=False),
        sa.Column("hora_fin", sa.String(length=10), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id_disponibilidad"),
    )
    op.create_index(
        op.f("ix_disponibilidades_horarias_email"), "disponibilidades_horarias", ["email"], unique=False
    )

    # 6. Sincronización de secuencia autoincremental en PostgreSQL (Supabase)
    context = op.get_context()
    if context.dialect.name == "postgresql":
        op.execute(
            sa.text(
                "SELECT setval(pg_get_serial_sequence('roles', 'id_rol'), "
                "COALESCE((SELECT MAX(id_rol) FROM roles), 1));"
            )
        )


def downgrade() -> None:
    op.drop_index(op.f("ix_disponibilidades_horarias_email"), table_name="disponibilidades_horarias")
    op.drop_table("disponibilidades_horarias")
    op.drop_index(op.f("ix_perfiles_academicos_email"), table_name="perfiles_academicos")
    op.drop_table("perfiles_academicos")
    op.drop_index(op.f("ix_usuario_roles_email"), table_name="usuario_roles")
    op.drop_table("usuario_roles")
    op.drop_index(op.f("ix_roles_nombre_rol"), table_name="roles")
    op.drop_table("roles")
    op.drop_index(op.f("ix_consentimientos_legales_email"), table_name="consentimientos_legales")
    op.drop_table("consentimientos_legales")
