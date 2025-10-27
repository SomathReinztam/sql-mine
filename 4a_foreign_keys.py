from sqlalchemy import create_engine, text

db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "originabotplain"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")

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

# foreign_keys = [
#     {
#         "tabla_origen": row.table_name,
#         "columna_origen": row.column_name,
#         "tabla_referenciada": row.foreign_table_name,
#         "columna_referenciada": row.foreign_column_name
#     }
#     for row in fks
# ]

# for x in foreign_keys:
#     print(x)
#     print("\n\n")

foreign_keys = [
    (
        row.table_name, {"columna_origen":row.column_name, "tabla_referenciada": row.foreign_table_name, "columna_referenciada": row.foreign_column_name}
    ) 
    for row in fks
]

# admin_interface_theme

foreign_keys = dict(foreign_keys)

for key in foreign_keys.keys():
    print(key)

#print(len(foreign_keys.keys()))

#print(foreign_keys.get("admin_interface_theme", None))

# epc_epcsubfield