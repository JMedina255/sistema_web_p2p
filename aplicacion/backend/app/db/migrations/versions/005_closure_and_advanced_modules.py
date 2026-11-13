"""closure_and_advanced_modules

Revision ID: 20261113_005
Revises: 20261031_004
Create Date: 2026-11-13 09:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20261113_005"
down_revision: str | None = "20261031_004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    # 1. Tabla asistencias_sesion (T-34 / T-36 / CUS12 / RF17 / RN-05 / RN-12)
    if "asistencias_sesion" not in existing_tables:
        op.create_table(
            "asistencias_sesion",
            sa.Column("id_asistencia", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("id_sesion", sa.Integer(), nullable=False),
            sa.Column("estudiante_email", sa.String(length=255), nullable=False),
            sa.Column("asistio", sa.Boolean(), server_default=sa.text("false"), nullable=False),
            sa.Column("fecha_checkin", sa.DateTime(timezone=True), nullable=True),
            sa.Column("ip_origen", sa.String(length=45), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.ForeignKeyConstraint(["id_sesion"], ["sesiones_mentoria.id_sesion"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id_asistencia"),
            sa.UniqueConstraint("id_sesion", "estudiante_email", name="uq_sesion_asistencia_estudiante"),
        )
        op.create_index("ix_asistencias_sesion_id_sesion", "asistencias_sesion", ["id_sesion"], unique=False)
        op.create_index("ix_asistencias_sesion_estudiante_email", "asistencias_sesion", ["estudiante_email"], unique=False)

    # 2. Tabla bitacoras_pedagogicas (T-33 / T-35 / CUS14 / RF18 / RNF04 / RNF08)
    if "bitacoras_pedagogicas" not in existing_tables:
        op.create_table(
            "bitacoras_pedagogicas",
            sa.Column("id_bitacora", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("id_sesion", sa.Integer(), nullable=False),
            sa.Column("mentor_email", sa.String(length=255), nullable=False),
            sa.Column("resumen_temas", sa.Text(), nullable=False),
            sa.Column("logros_alcanzados", sa.Text(), nullable=False),
            sa.Column("dificultades_detectadas", sa.Text(), nullable=True),
            sa.Column("observaciones_generales", sa.Text(), nullable=True),
            sa.Column("nivel_participacion", sa.String(length=20), server_default=sa.text("'ALTO'"), nullable=False),
            sa.Column("hash_integridad", sa.String(length=64), nullable=True),
            sa.Column("fecha_registro", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.ForeignKeyConstraint(["id_sesion"], ["sesiones_mentoria.id_sesion"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id_bitacora"),
            sa.UniqueConstraint("id_sesion", name="uq_bitacora_sesion"),
        )
        op.create_index("ix_bitacoras_pedagogicas_id_sesion", "bitacoras_pedagogicas", ["id_sesion"], unique=True)
        op.create_index("ix_bitacoras_pedagogicas_mentor_email", "bitacoras_pedagogicas", ["mentor_email"], unique=False)

    # 3. Tabla encuestas_calidad (T-37 / T-39 / CUS18 / RF20 / RNF07)
    if "encuestas_calidad" not in existing_tables:
        op.create_table(
            "encuestas_calidad",
            sa.Column("id_encuesta", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("id_sesion", sa.Integer(), nullable=False),
            sa.Column("estudiante_email", sa.String(length=255), nullable=False),
            sa.Column("puntuacion_general", sa.Integer(), nullable=False),
            sa.Column("claridad_explicacion", sa.Integer(), nullable=False),
            sa.Column("dominio_tema", sa.Integer(), nullable=False),
            sa.Column("puntualidad_compromiso", sa.Integer(), nullable=False),
            sa.Column("comentario", sa.Text(), nullable=True),
            sa.Column("fecha_registro", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.ForeignKeyConstraint(["id_sesion"], ["sesiones_mentoria.id_sesion"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id_encuesta"),
            sa.UniqueConstraint("id_sesion", "estudiante_email", name="uq_encuesta_sesion_estudiante"),
            sa.CheckConstraint("puntuacion_general >= 1 AND puntuacion_general <= 5", name="chk_encuesta_puntuacion_general"),
            sa.CheckConstraint("claridad_explicacion >= 1 AND claridad_explicacion <= 5", name="chk_encuesta_claridad"),
            sa.CheckConstraint("dominio_tema >= 1 AND dominio_tema <= 5", name="chk_encuesta_dominio"),
            sa.CheckConstraint("puntualidad_compromiso >= 1 AND puntualidad_compromiso <= 5", name="chk_encuesta_puntualidad"),
        )
        op.create_index("ix_encuestas_calidad_id_sesion", "encuestas_calidad", ["id_sesion"], unique=False)
        op.create_index("ix_encuestas_calidad_estudiante_email", "encuestas_calidad", ["estudiante_email"], unique=False)

    # 4. Tabla certificados_horas (T-41 / T-43 / CUS21 / RF21 / RNF08)
    if "certificados_horas" not in existing_tables:
        op.create_table(
            "certificados_horas",
            sa.Column("id_certificado", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("codigo_certificado", sa.String(length=30), nullable=False),
            sa.Column("mentor_email", sa.String(length=255), nullable=False),
            sa.Column("total_horas", sa.Integer(), nullable=False),
            sa.Column("sesiones_concluidas", sa.Integer(), nullable=False),
            sa.Column("promedio_calidad", sa.Float(), nullable=False),
            sa.Column("hash_seguridad", sa.String(length=64), nullable=False),
            sa.Column("url_descarga_pdf", sa.String(length=500), nullable=True),
            sa.Column("emitido_por", sa.String(length=255), server_default=sa.text("'DIRECCION_EPIS'"), nullable=False),
            sa.Column("fecha_emision", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.Column("estado", sa.String(length=20), server_default=sa.text("'EMITIDO'"), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.PrimaryKeyConstraint("id_certificado"),
            sa.UniqueConstraint("codigo_certificado"),
            sa.CheckConstraint("total_horas >= 0", name="chk_certificado_horas_positivas"),
            sa.CheckConstraint("estado IN ('EMITIDO', 'EMITIDO_DEMO', 'REVOCADO')", name="chk_certificado_estado"),
        )
        op.create_index("ix_certificados_horas_codigo", "certificados_horas", ["codigo_certificado"], unique=True)
        op.create_index("ix_certificados_horas_mentor_email", "certificados_horas", ["mentor_email"], unique=False)

    # 5. Tabla tokens_asistencia_activos (Soporte persistente multi-worker para códigos TOTP dinámicos)
    if "tokens_asistencia_activos" not in existing_tables:
        op.create_table(
            "tokens_asistencia_activos",
            sa.Column("id_token", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("id_sesion", sa.Integer(), nullable=False),
            sa.Column("token", sa.String(length=64), nullable=False),
            sa.Column("totp_code", sa.String(length=6), nullable=False),
            sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.ForeignKeyConstraint(["id_sesion"], ["sesiones_mentoria.id_sesion"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id_token"),
            sa.UniqueConstraint("id_sesion", name="uq_tokens_asistencia_activos_sesion"),
        )
        op.create_index("ix_tokens_asistencia_activos_id_sesion", "tokens_asistencia_activos", ["id_sesion"], unique=True)
        op.create_index("ix_tokens_asistencia_activos_expires_at", "tokens_asistencia_activos", ["expires_at"], unique=False)

    # 6. Agregado de quorumevaluated_at en sesiones_mentoria si no existe
    if "sesiones_mentoria" in existing_tables:
        sesiones_cols = [c["name"] for c in inspector.get_columns("sesiones_mentoria")]
        if "quorumevaluated_at" not in sesiones_cols:
            op.add_column("sesiones_mentoria", sa.Column("quorumevaluated_at", sa.DateTime(timezone=True), nullable=True))

    # 7. Actualización de constraints de estado para quórum y ciclo de vida de sesiones y reservas
    if "sesiones_mentoria" in existing_tables:
        op.execute("""
            ALTER TABLE sesiones_mentoria DROP CONSTRAINT IF EXISTS chk_sesion_estado;
            ALTER TABLE sesiones_mentoria ADD CONSTRAINT chk_sesion_estado CHECK (
                estado IN (
                    'BORRADOR', 'PUBLICADA', 'PENDIENTE_CONFIRMACION', 'QUORUM_INSUFICIENTE',
                    'CONFIRMADA', 'EN_CURSO', 'CONCLUIDA', 'COMPLETADA', 'BITACORA_REGISTRADA',
                    'HORAS_VISADAS', 'OBSERVADA', 'CANCELADA_SISTEMA', 'CANCELADA_MENTOR',
                    'CANCELADA_ADMIN', 'CANCELADA_QUORUM', 'RECHAZADA', 'EXPIRADA',
                    'EN_EVALUACION', 'AUDITADA', 'FINALIZADA'
                )
            );
        """)

    if "reservas_cupo" in existing_tables:
        op.execute("""
            ALTER TABLE reservas_cupo DROP CONSTRAINT IF EXISTS chk_reserva_estado;
            ALTER TABLE reservas_cupo ADD CONSTRAINT chk_reserva_estado CHECK (
                estado IN (
                    'PENDIENTE_CONFIRMACION', 'CONFIRMADA', 'CANCELADA_USUARIO',
                    'NO_CONFIRMADA', 'CANCELADA_NO_CONFIRMADA', 'CANCELADA_SISTEMA',
                    'CANCELADA_SISTEMA_QUORUM', 'ASISTIDA', 'INASISTENCIA'
                )
            );
        """)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    if "tokens_asistencia_activos" in existing_tables:
        op.drop_table("tokens_asistencia_activos")
    if "certificados_horas" in existing_tables:
        op.drop_table("certificados_horas")
    if "encuestas_calidad" in existing_tables:
        op.drop_table("encuestas_calidad")
    if "bitacoras_pedagogicas" in existing_tables:
        op.drop_table("bitacoras_pedagogicas")
    if "asistencias_sesion" in existing_tables:
        op.drop_table("asistencias_sesion")
