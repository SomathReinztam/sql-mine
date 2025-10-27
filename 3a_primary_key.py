
# Obtener las llaves primarias de todas las tablas

from sqlalchemy import create_engine, text

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


print(primary_keys)

