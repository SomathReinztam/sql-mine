from sqlalchemy import create_engine, text
import pandas as pd

db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "originabotplain"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")

with engine.connect() as conn:
    pk_query = text("""
        SELECT
            tc.table_name,
            kcu.column_name
        FROM
            information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
        WHERE
            tc.constraint_type = 'PRIMARY KEY'
            AND tc.table_schema = 'public';
    """)
    pks = conn.execute(pk_query).fetchall()

primary_keys = {}
for table, column in pks:
    primary_keys.setdefault(table, []).append(column)


with engine.connect() as conn:
    fk_query = text("""
        SELECT
            tc.table_name AS table_name,
            kcu.column_name AS column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM
            information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
        AND tc.table_schema = 'public'
        ORDER BY tc.table_name;
    """)
    fks = conn.execute(fk_query).fetchall()


foreign_keys = [
    (
        row.table_name, {"columna_origen":row.column_name, "tabla_referenciada": row.foreign_table_name, "columna_referenciada": row.foreign_column_name}
    ) 
    for row in fks
]

foreign_keys = dict(foreign_keys)


table = 'epc_epcsubfield'
QUERY = f"""
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = '{table}'
AND table_schema = 'public';
"""

with engine.connect() as conn:
    query = text(QUERY.format(table=table))
    df = pd.read_sql_query(query, engine)




resumen = f"Tabla '{table}' tiene {df.shape[0]} columnas\n"

if table in primary_keys:
        resumen += f"🔑 Llave primaria: {', '.join(primary_keys[table])}\n"


relaciones = foreign_keys.get(table, None)

if relaciones:
        resumen += "🔗 Relaciones foráneas:\n"
        resumen += f" {relaciones['columna_origen']} → {relaciones['tabla_referenciada']}.{relaciones['columna_referenciada']}\n"
else:
     resumen

print(resumen)