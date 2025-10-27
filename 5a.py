
from sqlalchemy import create_engine, text
import pandas as pd

db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "originabotplain"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")

table = 'admin_interface_theme'
QUERY = f"""
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = '{table}'
AND table_schema = 'public';
"""

with engine.connect() as conn:
    query = text(QUERY.format(table=table))
    df = pd.read_sql_query(query, engine)
    print(df)

