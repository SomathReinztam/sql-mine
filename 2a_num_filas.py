from sqlalchemy import create_engine, text
import pandas as pd

# Configura tu conexión
db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "originabotplain"

# Crea el engine de conexión   admin_interface_theme
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")

table = 'admin_interface_theme'

QUERY = f"SELECT COUNT(*) FROM {table}"
with engine.connect() as conn:
    query = text(QUERY.format(table=table))
    result = conn.execute(query)
    count = result.scalar()  # Obtiene el primer valor del resultado
    print(f"Número de filas en {table}: {count}")





# Método 2: Usando pandas (alternativa)
# def contar_filas_pandas():
#     try:
#         # Consulta usando pandas
#         query = "SELECT COUNT(*) as total FROM admin_interface_theme"
#         df = pd.read_sql_query(query, engine)
#         count = df['total'].iloc[0]
#         print(f"Número de filas en admin_interface_theme: {count}")
#         return count
#     except Exception as e:
#         print(f"Error al consultar la base de datos: {e}")
#         return None