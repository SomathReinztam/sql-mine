
from graphs.db_utils import get_db_relations, describe_table_relationships, get_db_tables_name, get_head_table_markdown
from graphs.table_agent import table_agent

db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "originabotplain"

primary_keys, foreign_keys = get_db_relations(db_user=db_user, db_pass=db_pass, db_host=db_host, db_name=db_name)

tables = get_db_tables_name(db_user=db_user, db_pass=db_pass, db_host=db_host, db_name=db_name)

N = 1
resumen_db = ""
print("=="*10)
for table_name in tables:
    print("--"*5)
    print(N)
    print("--"*5)
    relations = describe_table_relationships(table_name, primary_keys, foreign_keys, True)
    df_markdown = get_head_table_markdown(table_name, db_user=db_user, db_pass=db_pass, db_host=db_host, db_name=db_name)

    initial_state = {
        "table_name":table_name,
        "relations":relations,
        "df":df_markdown
    }

    response = table_agent.invoke(initial_state)
    table_description = response["table_description"]
    resumen_db += table_description
    resumen_db += "\n"*5

    print(table_description)
    print("\n"*5)
    N+=1


file = 'main.txt'
with open(file, "w", encoding="utf-8") as f:
    f.write(resumen_db)

