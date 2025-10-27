from sqlalchemy import create_engine, text
import pandas as pd

# Configura tu conexión
db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "originabotplain"

# Crea el engine de conexión
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")

# Consulta todas las tablas del esquema público
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """))

    # Usar fetchone() para obtener la primera fila
    #row = result.fetchone()
    #print(row)
    """
    print(row)

    ('admin_interface_theme',)
    
    """
    tables = [row[0] for row in result]


print(f"\nSe encontraron {len(tables)} tablas.\n")

for table_name in tables:
    print(table_name)

# 
# with engine.connect() as conn:
#     # Usar pandas para leer directamente
#     df = pd.read_sql("""
#         SELECT table_name
#         FROM information_schema.tables
#         WHERE table_schema = 'public'
#         ORDER BY table_name;
#     """, conn)
    
#     print(df.head())
