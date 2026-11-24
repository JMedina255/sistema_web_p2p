"""Store the current official timetable and serialize room allocation."""
import sqlalchemy as sa
from alembic import op

revision = "20261121_007"
down_revision = "20261121_006"
branch_labels = None
depends_on = None


def upgrade():
    tables = sa.inspect(op.get_bind()).get_table_names()
    if "versiones_cronograma" not in tables:
        op.create_table(
            "versiones_cronograma",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("archivo", sa.String(255), nullable=False),
            sa.Column("franjas", sa.JSON(), nullable=False),
            sa.Column("creado", sa.DateTime(timezone=True), nullable=False),
        )
    if "cronograma_activo" not in tables:
        op.create_table(
            "cronograma_activo",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=False),
            sa.Column("id_version", sa.Integer(), sa.ForeignKey("versiones_cronograma.id")),
            sa.CheckConstraint("id = 1", name="chk_cronograma_unico"),
        )
    op.execute("INSERT INTO cronograma_activo(id) VALUES (1) ON CONFLICT (id) DO NOTHING")


def downgrade():
    op.drop_table("cronograma_activo")
    op.drop_table("versiones_cronograma")
