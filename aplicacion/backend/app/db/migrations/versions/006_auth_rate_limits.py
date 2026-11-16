"""auth_rate_limits

Revision ID: 20261116_006
Revises: 20261113_005
Create Date: 2026-11-16 16:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20261116_006"
down_revision: str | None = "20261113_005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    # 1. Tabla auth_rate_limits para control distribuido de frecuencia y mitigación DoS/fuerza bruta (H-08 / CUS01 / RNF01)
    if "auth_rate_limits" not in existing_tables:
        op.create_table(
            "auth_rate_limits",
            sa.Column("key", sa.String(length=128), nullable=False),
            sa.Column("count", sa.Integer(), server_default=sa.text("1"), nullable=False),
            sa.Column("window_expires_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column(
                "updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False
            ),
            sa.PrimaryKeyConstraint("key", name="pk_auth_rate_limits"),
        )

        # Configuración de políticas de seguridad RLS y permisos restringidos para PostgreSQL / Supabase
        if bind.dialect.name == "postgresql":
            # Habilitar Row Level Security (RLS) para evitar exposición pública directa vía PostgREST
            op.execute("ALTER TABLE auth_rate_limits ENABLE ROW LEVEL SECURITY;")

            # Revocar permisos de lectura/escritura a roles públicos o clientes anónimos
            op.execute("REVOKE ALL ON auth_rate_limits FROM anon, authenticated;")

            # Garantizar acceso exclusivo para el backend institucional y roles administrativos autorizados
            op.execute("""
                DO $$
                BEGIN
                    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'service_role') THEN
                        GRANT ALL ON auth_rate_limits TO service_role;
                    END IF;
                    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'postgres') THEN
                        GRANT ALL ON auth_rate_limits TO postgres;
                    END IF;
                END $$;
            """)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    if "auth_rate_limits" in existing_tables:
        op.drop_table("auth_rate_limits")
