from sqlalchemy import create_engine, text
import pandas as pd

db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "originabotplain"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")

table = 'contract_clause'
QUERY = f"SELECT * FROM {table} LIMIT 10;"

with engine.connect() as conn:
    query = text(QUERY.format(table=table))
    df = pd.read_sql_query(query, engine)
    #print(df)

print(df)

print("\n"*15)

print(df.to_markdown(index=False))

