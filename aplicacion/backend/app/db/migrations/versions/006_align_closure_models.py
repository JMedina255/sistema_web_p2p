"""Reconcile the released closure schema with the application models.

Retain auxiliary legacy columns (including historical narratives and PDF paths).
Installations originally provisioned from the current models are already aligned.
"""
import sqlalchemy as sa
from alembic import op

revision = "20261121_006"
down_revision = "20261113_005"
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())

    def has_column(table, name):
        return any(c["name"] == name for c in inspector.get_columns(table))

    if has_column("bitacoras_pedagogicas", "mentor_email"):
        op.execute("""
            ALTER TABLE bitacoras_pedagogicas RENAME COLUMN mentor_email TO id_mentor;
            ALTER TABLE bitacoras_pedagogicas RENAME COLUMN hash_integridad TO hash_firma;
            ALTER TABLE bitacoras_pedagogicas
                ADD COLUMN temas_cubiertos json, ADD COLUMN observaciones text,
                ADD COLUMN nivel_dificultad varchar(20) NOT NULL DEFAULT 'Medio',
                ADD COLUMN horas_declaradas double precision,
                ADD COLUMN visado_administrador boolean NOT NULL DEFAULT false,
                ALTER COLUMN resumen_temas DROP NOT NULL,
                ALTER COLUMN logros_alcanzados DROP NOT NULL;
            UPDATE bitacoras_pedagogicas b
               SET temas_cubiertos = json_build_array(b.resumen_temas),
                   observaciones = concat_ws(chr(10), b.logros_alcanzados,
                       b.dificultades_detectadas, b.observaciones_generales),
                   horas_declaradas = s.duracion_minutos / 60.0,
                   visado_administrador = s.estado = 'HORAS_VISADAS',
                   hash_firma = coalesce(b.hash_firma, '')
              FROM sesiones_mentoria s WHERE s.id_sesion = b.id_sesion;
            ALTER TABLE bitacoras_pedagogicas ALTER COLUMN temas_cubiertos SET NOT NULL,
                ALTER COLUMN observaciones SET NOT NULL, ALTER COLUMN horas_declaradas SET NOT NULL,
                ALTER COLUMN hash_firma SET NOT NULL,
                ADD CONSTRAINT chk_bitacora_dificultad CHECK (nivel_dificultad IN ('Bajo','Medio','Alto'))
        """)
    if has_column("encuestas_calidad", "puntuacion_general"):
        op.execute("""
            ALTER TABLE encuestas_calidad RENAME COLUMN puntuacion_general TO calificacion_general;
            ALTER TABLE encuestas_calidad RENAME COLUMN puntualidad_compromiso TO puntualidad;
            ALTER TABLE encuestas_calidad RENAME COLUMN comentario TO comentarios
        """)
    if has_column("certificados_horas", "codigo_certificado"):
        op.execute("""
            ALTER TABLE certificados_horas RENAME COLUMN codigo_certificado TO codigo_folio;
            ALTER TABLE certificados_horas RENAME COLUMN mentor_email TO id_mentor;
            ALTER TABLE certificados_horas RENAME COLUMN hash_seguridad TO hash_firma;
            ALTER TABLE certificados_horas RENAME COLUMN total_horas TO horas_acreditadas;
            ALTER TABLE certificados_horas ADD COLUMN periodo_academico varchar(20),
                ALTER COLUMN horas_acreditadas TYPE double precision,
                ALTER COLUMN codigo_folio TYPE varchar(50), ALTER COLUMN estado TYPE varchar(30),
                ALTER COLUMN sesiones_concluidas DROP NOT NULL, ALTER COLUMN promedio_calidad DROP NOT NULL;
            UPDATE certificados_horas SET periodo_academico = coalesce(
                substring(codigo_folio from '([0-9]{4}-II?)(?:-|$)'),
                to_char(fecha_emision AT TIME ZONE 'America/Lima', 'YYYY') ||
                CASE WHEN extract(month from fecha_emision AT TIME ZONE 'America/Lima') <= 6
                     THEN '-I' ELSE '-II' END);
            ALTER TABLE certificados_horas ALTER COLUMN periodo_academico SET NOT NULL,
                ADD CONSTRAINT chk_horas_minimas_cert CHECK (horas_acreditadas >= 20) NOT VALID
        """)
        # Earlier releases allowed several distinct folios in one semester. Retain
        # their IDs and signatures while ensuring a single current issue per period.
        if op.get_bind().scalar(sa.text("""
            SELECT EXISTS (SELECT 1 FROM certificados_horas
                           GROUP BY id_mentor, periodo_academico HAVING count(*) > 1)
        """)):
            op.execute("""
                ALTER TABLE certificados_horas ADD COLUMN revision_historica integer NOT NULL DEFAULT 0;
                WITH ranked AS (
                    SELECT id_certificado, row_number() OVER (
                        PARTITION BY id_mentor, periodo_academico ORDER BY id_certificado DESC
                    ) - 1 AS revision FROM certificados_horas
                ) UPDATE certificados_horas c SET revision_historica = r.revision
                    FROM ranked r WHERE c.id_certificado = r.id_certificado;
                ALTER TABLE certificados_horas ADD CONSTRAINT uq_mentor_periodo_certificado
                    UNIQUE (id_mentor, periodo_academico, revision_historica)
            """)
        else:
            op.create_unique_constraint("uq_mentor_periodo_certificado", "certificados_horas",
                                        ["id_mentor", "periodo_academico"])


def downgrade():
    raise RuntimeError("La revisión 006 conserva documentos históricos. Para revertir, restaure la copia previa.")
