from graphs.db_utils import get_db_tables_name_2, get_head_table_markdown_2

db_user = "postgres" 
db_pass = "3636" 
db_host = "localhost" 

#db_name = "northwind" 
db_name = "classicmodels" 


# args = {"db_user":db_user, "db_pass":db_pass, "db_host":db_host, "db_name":db_name, "schema":db_name}
# tables = get_db_tables_name_2(**args)
# for x in tables:
#     print(x)


table_name = 'employees' 
args = {"table_name":table_name, "db_user":db_user, "db_pass":db_pass, "db_host":db_host, "db_name":db_name, "schema":db_name}
df = get_head_table_markdown_2(**args)
print("\n\n\n")
print(df)
