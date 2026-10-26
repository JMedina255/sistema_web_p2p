"""mentoring_offers

Revision ID: 20261026_003
Revises: 20261023_002
Create Date: 2026-10-26 18:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20261026_003"
down_revision: str | None = "20261023_002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Creación de la tabla sesiones_mentoria (T-14 / T-15 / T-16 / RF08 / CUS06)
    op.create_table(
        "sesiones_mentoria",
        sa.Column("id_sesion", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("codigo_sesion", sa.String(length=20), nullable=False),
        sa.Column("mentor_email", sa.String(length=255), nullable=False),
        sa.Column("id_asignatura", sa.Integer(), nullable=False),
        sa.Column("id_tema", sa.Integer(), nullable=False),
        sa.Column("fecha_inicio", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "duracion_minutos",
            sa.Integer(),
            sa.CheckConstraint("duracion_minutos IN (60, 90)", name="chk_sesion_duracion"),
            server_default=sa.text("60"),
            nullable=False,
        ),
        sa.Column(
            "modalidad",
            sa.String(length=20),
            sa.CheckConstraint("modalidad IN ('presencial', 'virtual')", name="chk_sesion_modalidad"),
            nullable=False,
        ),
        sa.Column(
            "aforo_maximo",
            sa.Integer(),
            sa.CheckConstraint("aforo_maximo IN (10, 20)", name="chk_sesion_aforo"),
            nullable=False,
        ),
        sa.Column("espacio_asignado", sa.String(length=255), nullable=False),
        sa.Column("notas_adicionales", sa.Text(), nullable=True),
        sa.Column(
            "estado",
            sa.String(length=30),
            sa.CheckConstraint(
                "estado IN ('PUBLICADA', 'PENDIENTE_CONFIRMACION', 'CONFIRMADA', 'CANCELADA_SISTEMA', 'CANCELADA_MENTOR', 'FINALIZADA')",
                name="chk_sesion_estado",
            ),
            server_default=sa.text("'PUBLICADA'"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["id_asignatura"], ["asignaturas.id_asignatura"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["id_tema"], ["temas_conceptuales.id_tema"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id_sesion"),
        sa.UniqueConstraint("codigo_sesion"),
    )
    op.create_index(
        op.f("ix_sesiones_mentoria_codigo_sesion"), "sesiones_mentoria", ["codigo_sesion"], unique=True
    )
    op.create_index(
        op.f("ix_sesiones_mentoria_mentor_email"), "sesiones_mentoria", ["mentor_email"], unique=False
    )
    op.create_index(
        op.f("ix_sesiones_mentoria_id_asignatura"), "sesiones_mentoria", ["id_asignatura"], unique=False
    )
    op.create_index(op.f("ix_sesiones_mentoria_id_tema"), "sesiones_mentoria", ["id_tema"], unique=False)
    op.create_index(
        op.f("ix_sesiones_mentoria_fecha_inicio"), "sesiones_mentoria", ["fecha_inicio"], unique=False
    )

    # 2. Sincronización de secuencia autoincremental en PostgreSQL (Supabase)
    context = op.get_context()
    if context.dialect.name == "postgresql":
        op.execute(
            sa.text(
                "SELECT setval(pg_get_serial_sequence('sesiones_mentoria', 'id_sesion'), "
                "COALESCE((SELECT MAX(id_sesion) FROM sesiones_mentoria), 1));"
            )
        )


def downgrade() -> None:
    op.drop_index(op.f("ix_sesiones_mentoria_fecha_inicio"), table_name="sesiones_mentoria")
    op.drop_index(op.f("ix_sesiones_mentoria_id_tema"), table_name="sesiones_mentoria")
    op.drop_index(op.f("ix_sesiones_mentoria_id_asignatura"), table_name="sesiones_mentoria")
    op.drop_index(op.f("ix_sesiones_mentoria_mentor_email"), table_name="sesiones_mentoria")
    op.drop_index(op.f("ix_sesiones_mentoria_codigo_sesion"), table_name="sesiones_mentoria")
    op.drop_table("sesiones_mentoria")
