import psycopg2
from sqlalchemy import create_engine, text  # <-- Añade text aquí

try:
    # Intentar conexión directa con psycopg2
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="3636"
    )
    print("✅ Conexión exitosa a PostgreSQL")
    conn.close()
except Exception as e:
    print(f"❌ Error de conexión: {e}")

try:
    # Intentar conexión con SQLAlchemy (como tu código original)
    engine = create_engine("postgresql+psycopg2://postgres:3636@localhost/postgres")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))  # <-- Envuelve en text()
        version = result.fetchone()
        print(f"✅ PostgreSQL version: {version[0]}")
except Exception as e:
    print(f"❌ Error con SQLAlchemy: {e}")

