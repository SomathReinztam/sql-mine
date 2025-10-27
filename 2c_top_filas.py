from sqlalchemy import create_engine, text
import pandas as pd

# Configura tu conexión
db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "originabotplain"

# Crea el engine de conexión
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")

table = 'admin_interface_theme'
QUERY = f"SELECT * FROM {table} LIMIT 10;"

with engine.connect() as conn:
    query = text(QUERY.format(table=table))
    result = conn.execute(query)
    for row in result:
            print(row)

print("\n"*5)


with engine.connect() as conn:
    query = text(QUERY.format(table=table))
    df = pd.read_sql_query(query, engine)
    print(df)
