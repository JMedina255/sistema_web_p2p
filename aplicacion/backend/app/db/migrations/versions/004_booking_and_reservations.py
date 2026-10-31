"""booking_and_reservations

Revision ID: 20261031_004
Revises: 20261026_003
Create Date: 2026-10-31 09:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20261031_004"
down_revision: str | None = "20261026_003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Creación de la tabla reservas_cupo (T-22 / T-24 / CUS04 / RF12 / RN-05 / RNF07)
    op.create_table(
        "reservas_cupo",
        sa.Column("id_reserva", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("codigo_reserva", sa.String(length=20), nullable=False),
        sa.Column("id_sesion", sa.Integer(), nullable=False),
        sa.Column("estudiante_email", sa.String(length=255), nullable=False),
        sa.Column(
            "estado",
            sa.String(length=30),
            sa.CheckConstraint(
                "estado IN ('PENDIENTE_CONFIRMACION', 'CONFIRMADA', 'CANCELADA_USUARIO', 'NO_CONFIRMADA', 'CANCELADA_SISTEMA', 'ASISTIDA', 'INASISTENCIA')",
                name="chk_reserva_estado",
            ),
            server_default=sa.text("'PENDIENTE_CONFIRMACION'"),
            nullable=False,
        ),
        sa.Column(
            "fecha_reserva", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("fecha_ratificacion", sa.DateTime(timezone=True), nullable=True),
        sa.Column("motivo_cancelacion", sa.Text(), nullable=True),
        sa.Column("ticket_hash", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["id_sesion"], ["sesiones_mentoria.id_sesion"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id_reserva"),
        sa.UniqueConstraint("codigo_reserva"),
        sa.UniqueConstraint("id_sesion", "estudiante_email", name="uq_sesion_estudiante_activa"),
    )
    op.create_index(op.f("ix_reservas_cupo_codigo_reserva"), "reservas_cupo", ["codigo_reserva"], unique=True)
    op.create_index(op.f("ix_reservas_cupo_id_sesion"), "reservas_cupo", ["id_sesion"], unique=False)
    op.create_index(
        op.f("ix_reservas_cupo_estudiante_email"), "reservas_cupo", ["estudiante_email"], unique=False
    )
    op.create_index(op.f("ix_reservas_cupo_estado"), "reservas_cupo", ["estado"], unique=False)

    # 2. Creación de la tabla solicitudes_demanda (CUS03 / RF07)
    op.create_table(
        "solicitudes_demanda",
        sa.Column("id_demanda", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("estudiante_email", sa.String(length=255), nullable=False),
        sa.Column("id_asignatura", sa.Integer(), nullable=False),
        sa.Column("id_tema", sa.Integer(), nullable=False),
        sa.Column("observaciones", sa.Text(), nullable=True),
        sa.Column(
            "estado",
            sa.String(length=20),
            sa.CheckConstraint("estado IN ('PENDIENTE', 'ATENDIDA', 'CANCELADA')", name="chk_demanda_estado"),
            server_default=sa.text("'PENDIENTE'"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["id_asignatura"], ["asignaturas.id_asignatura"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["id_tema"], ["temas_conceptuales.id_tema"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id_demanda"),
    )
    op.create_index(
        op.f("ix_solicitudes_demanda_estudiante_email"),
        "solicitudes_demanda",
        ["estudiante_email"],
        unique=False,
    )
    op.create_index(
        op.f("ix_solicitudes_demanda_id_asignatura"), "solicitudes_demanda", ["id_asignatura"], unique=False
    )
    op.create_index(op.f("ix_solicitudes_demanda_id_tema"), "solicitudes_demanda", ["id_tema"], unique=False)
    op.create_index(op.f("ix_solicitudes_demanda_estado"), "solicitudes_demanda", ["estado"], unique=False)

    # 3. Sincronización de secuencias y políticas RLS en PostgreSQL (Supabase)
    context = op.get_context()
    if context.dialect.name == "postgresql":
        op.execute(
            sa.text(
                "SELECT setval(pg_get_serial_sequence('reservas_cupo', 'id_reserva'), "
                "COALESCE((SELECT MAX(id_reserva) FROM reservas_cupo), 1));"
            )
        )
        op.execute(
            sa.text(
                "SELECT setval(pg_get_serial_sequence('solicitudes_demanda', 'id_demanda'), "
                "COALESCE((SELECT MAX(id_demanda) FROM solicitudes_demanda), 1));"
            )
        )
        # Habilitación de Row Level Security
        op.execute(sa.text("ALTER TABLE reservas_cupo ENABLE ROW LEVEL SECURITY;"))
        op.execute(sa.text("ALTER TABLE solicitudes_demanda ENABLE ROW LEVEL SECURITY;"))

        # Políticas RLS para reservas_cupo
        op.execute(
            sa.text(
                """
                DROP POLICY IF EXISTS rls_reservas_select ON reservas_cupo;
                CREATE POLICY rls_reservas_select ON reservas_cupo
                FOR SELECT TO authenticated
                USING (
                    auth.jwt() ->> 'email' = estudiante_email OR
                    EXISTS (
                        SELECT 1 FROM sesiones_mentoria s
                        WHERE s.id_sesion = reservas_cupo.id_sesion
                          AND s.mentor_email = auth.jwt() ->> 'email'
                    ) OR
                    auth.jwt() ->> 'role' = 'administrador'
                );
                """
            )
        )
        op.execute(
            sa.text(
                """
                DROP POLICY IF EXISTS rls_reservas_insert ON reservas_cupo;
                CREATE POLICY rls_reservas_insert ON reservas_cupo
                FOR INSERT TO authenticated
                WITH CHECK (
                    auth.jwt() ->> 'email' = estudiante_email
                );
                """
            )
        )
        op.execute(
            sa.text(
                """
                DROP POLICY IF EXISTS rls_reservas_update ON reservas_cupo;
                CREATE POLICY rls_reservas_update ON reservas_cupo
                FOR UPDATE TO authenticated
                USING (
                    auth.jwt() ->> 'email' = estudiante_email OR
                    EXISTS (
                        SELECT 1 FROM sesiones_mentoria s
                        WHERE s.id_sesion = reservas_cupo.id_sesion
                          AND s.mentor_email = auth.jwt() ->> 'email'
                    ) OR
                    auth.jwt() ->> 'role' = 'administrador'
                );
                """
            )
        )

        # Políticas RLS para solicitudes_demanda (CUS03 / RF07)
        op.execute(
            sa.text(
                """
                DROP POLICY IF EXISTS rls_demandas_select ON solicitudes_demanda;
                CREATE POLICY rls_demandas_select ON solicitudes_demanda
                FOR SELECT TO authenticated
                USING (true);
                """
            )
        )
        op.execute(
            sa.text(
                """
                DROP POLICY IF EXISTS rls_demandas_insert ON solicitudes_demanda;
                CREATE POLICY rls_demandas_insert ON solicitudes_demanda
                FOR INSERT TO authenticated
                WITH CHECK (
                    auth.jwt() ->> 'email' = estudiante_email
                );
                """
            )
        )
        op.execute(
            sa.text(
                """
                DROP POLICY IF EXISTS rls_demandas_update ON solicitudes_demanda;
                CREATE POLICY rls_demandas_update ON solicitudes_demanda
                FOR UPDATE TO authenticated
                USING (
                    auth.jwt() ->> 'email' = estudiante_email OR
                    auth.jwt() ->> 'role' = 'administrador'
                );
                """
            )
        )


def downgrade() -> None:
    context = op.get_context()
    if context.dialect.name == "postgresql":
        op.execute(sa.text("DROP POLICY IF EXISTS rls_demandas_update ON solicitudes_demanda;"))
        op.execute(sa.text("DROP POLICY IF EXISTS rls_demandas_insert ON solicitudes_demanda;"))
        op.execute(sa.text("DROP POLICY IF EXISTS rls_demandas_select ON solicitudes_demanda;"))
        op.execute(sa.text("DROP POLICY IF EXISTS rls_reservas_update ON reservas_cupo;"))
        op.execute(sa.text("DROP POLICY IF EXISTS rls_reservas_insert ON reservas_cupo;"))
        op.execute(sa.text("DROP POLICY IF EXISTS rls_reservas_select ON reservas_cupo;"))

    op.drop_index(op.f("ix_solicitudes_demanda_estado"), table_name="solicitudes_demanda")
    op.drop_index(op.f("ix_solicitudes_demanda_id_tema"), table_name="solicitudes_demanda")
    op.drop_index(op.f("ix_solicitudes_demanda_id_asignatura"), table_name="solicitudes_demanda")
    op.drop_index(op.f("ix_solicitudes_demanda_estudiante_email"), table_name="solicitudes_demanda")
    op.drop_table("solicitudes_demanda")

    op.drop_index(op.f("ix_reservas_cupo_estado"), table_name="reservas_cupo")
    op.drop_index(op.f("ix_reservas_cupo_estudiante_email"), table_name="reservas_cupo")
    op.drop_index(op.f("ix_reservas_cupo_id_sesion"), table_name="reservas_cupo")
    op.drop_index(op.f("ix_reservas_cupo_codigo_reserva"), table_name="reservas_cupo")
    op.drop_table("reservas_cupo")
