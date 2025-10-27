from sqlalchemy import create_engine, text, inspect
import pandas as pd

# Configura tu conexión
db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "originabotplain"

# Crea el engine de conexión
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")

# Método 1: Usando SQL directo (consultando information_schema)
def contar_columnas_sql():
    try:
        with engine.connect() as connection:
            query = text("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name = 'admin_interface_theme' 
                AND table_schema = 'public'
            """)
            result = connection.execute(query)
            count = result.scalar()
            print(f"Número de columnas en admin_interface_theme: {count}")
            return count
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return None

# Método 2: Usando el inspector de SQLAlchemy (recomendado)
def contar_columnas_inspector():
    try:
        inspector = inspect(engine)
        columns = inspector.get_columns('admin_interface_theme')
        count = len(columns)
        print(f"Número de columnas en admin_interface_theme: {count}")
        
        # Opcional: mostrar los nombres de las columnas
        print("Nombres de las columnas:")
        for column in columns:
            print(f"  - {column['name']} ({column['type']})")
        
        return count
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return None

# Método 3: Usando pandas
def contar_columnas_pandas():
    try:
        # Consulta para obtener información de las columnas
        query = """
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'admin_interface_theme' 
            AND table_schema = 'public'
            ORDER BY ordinal_position
        """
        df = pd.read_sql_query(query, engine)
        count = len(df)
        print(f"Número de columnas en admin_interface_theme: {count}")
        
        # Mostrar información detallada
        print("\nDetalles de las columnas:")
        for _, row in df.iterrows():
            print(f"  - {row['column_name']} ({row['data_type']})")
        
        return count
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return None

# Método 4: Consulta más detallada con información adicional
def info_completa_tabla():
    try:
        with engine.connect() as connection:
            query = text("""
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns 
                WHERE table_name = 'admin_interface_theme' 
                AND table_schema = 'public'
                ORDER BY ordinal_position
            """)
            result = connection.execute(query)
            columns = result.fetchall()
            
            print(f"La tabla admin_interface_theme tiene {len(columns)} columnas:")
            print("\nDetalles completos:")
            for col in columns:
                print(f"  - {col.column_name:20} {col.data_type:15} Nullable: {col.is_nullable:5} Default: {col.column_default}")
            
            return len(columns)
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return None

# Ejecutar las consultas
if __name__ == "__main__":
    print("Consultando información de columnas de la tabla admin_interface_theme...")
    print("=" * 60)
    
    # Método recomendado (SQLAlchemy Inspector)
    print("\n1. Usando Inspector de SQLAlchemy:")
    contar_columnas_inspector()
    
    print("\n2. Usando SQL directo:")
    contar_columnas_sql()
    
    print("\n3. Información completa:")
    info_completa_tabla()