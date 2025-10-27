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
    {
        "tabla_origen": row.table_name,
        "columna_origen": row.column_name,
        "tabla_referenciada": row.foreign_table_name,
        "columna_referenciada": row.foreign_column_name
    }
    for row in fks
]

table = 'epc_epcsubfield'

# Relaciones
relaciones = [fk for fk in foreign_keys if fk["tabla_origen"] == table]


resumen = ""

if table in primary_keys:
        resumen += f"🔑 Llave primaria: {', '.join(primary_keys[table])}\n"
if relaciones:
    resumen += "🔗 Relaciones foráneas:\n"
    for r in relaciones:
        resumen += f"  {r['columna_origen']} → {r['tabla_referenciada']}.{r['columna_referenciada']}\n"
else:
    resumen += "Sin relaciones foráneas.\n"

print(resumen)

"""

🔑 Llave primaria: id
🔗 Relaciones foráneas:
  epc_field_id → epc_epcfield.id
  epc_subfield_template_id → epc_epcsubfieldtemplate.id


"""

