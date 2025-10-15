# silk_response


from graphs.db_utils import get_db_relations, describe_table_relationships, get_db_tables_name, get_head_table_markdown
from sqlalchemy import create_engine, text
import pandas as pd

db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "originabotplain"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")


primary_keys, foreign_keys = get_db_relations(db_user=db_user, db_pass=db_pass, db_host=db_host, db_name=db_name)

tables = get_db_tables_name(db_user=db_user, db_pass=db_pass, db_host=db_host, db_name=db_name)


table_name = "silk_response"

df_markdown = get_head_table_markdown(table_name, db_user=db_user, db_pass=db_pass, db_host=db_host, db_name=db_name)

print(df_markdown)

