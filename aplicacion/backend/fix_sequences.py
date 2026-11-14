import sys
from sqlalchemy import text
from app.db.session import get_session_context

find_seqs_sql = """
SELECT 
    t.table_name,
    c.column_name,
    pg_get_serial_sequence(c.table_name, c.column_name) AS seq_name
FROM information_schema.tables t
JOIN information_schema.columns c 
    ON t.table_name = c.table_name AND t.table_schema = c.table_schema
WHERE t.table_schema = 'public'
  AND t.table_type = 'BASE TABLE'
  AND pg_get_serial_sequence(c.table_name, c.column_name) IS NOT NULL;
"""

def sync_sequences():
    with get_session_context() as db:
        seqs = db.execute(text(find_seqs_sql)).fetchall()
        print(f"Encontradas {len(seqs)} secuencias con serial/identity:")
        for table_name, col_name, seq_name in seqs:
            max_val = db.execute(text(f"SELECT COALESCE(MAX({col_name}), 0) FROM {table_name}")).scalar()
            if max_val > 0:
                db.execute(text(f"SELECT setval('{seq_name}', {max_val}, true)"))
                print(f"  [OK] {table_name}.{col_name} -> {seq_name} sincronizado en {max_val} (próximo: {max_val + 1})")
            else:
                db.execute(text(f"SELECT setval('{seq_name}', 1, false)"))
                print(f"  [OK] {table_name}.{col_name} -> {seq_name} inicializado en 1")
        db.commit()
        print("Todas las secuencias de PostgreSQL han sido sincronizadas satisfactoriamente.")

if __name__ == "__main__":
    sync_sequences()
