
from graphs.db_utils import get_db_relations, describe_table_relationships
from graphs.table_agent import table_agent

from sqlalchemy import create_engine, text
import pandas as pd

db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "originabotplain"


primary_keys, foreign_keys = get_db_relations(db_user=db_user, db_pass=db_pass, db_host=db_host, db_name=db_name)

table_name = 'epc_epcsubfield'
resumen = describe_table_relationships(table_name, primary_keys, foreign_keys, True)

print(resumen)
print("\n"*10)

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")
QUERY = f"SELECT * FROM {table_name} LIMIT 10;"

with engine.connect() as conn:
    query = text(QUERY.format(table=table_name))
    df = pd.read_sql_query(query, engine)
print(df)

print("\n"*10)

initial_state = {"table_name":table_name, "relations":resumen, "df":df.to_markdown(index=False)}

response = table_agent.invoke(initial_state)

table_description = response["table_description"]

print(table_description)

