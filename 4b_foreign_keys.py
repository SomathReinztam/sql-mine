from sqlalchemy import create_engine, text

db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "originabotplain"

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")

tabla = "admin_interface_theme"

def encontrar_foreign_keys_pg(tabla_nombre):
    """
    Versión alternativa usando las vistas específicas de PostgreSQL.
    """
    # OJO: el nombre de la tabla se inserta directamente en el string SQL,
    # porque PostgreSQL no permite parámetros en ::regclass
    query = text(f"""
        SELECT
            conname as constraint_name,
            conrelid::regclass as tabla_origen,
            a.attname as columna_origen,
            confrelid::regclass as tabla_destino,
            af.attname as columna_destino
        FROM 
            pg_constraint c
        JOIN 
            pg_attribute a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
        JOIN 
            pg_attribute af ON af.attnum = ANY(c.confkey) AND af.attrelid = c.confrelid
        WHERE 
            c.contype = 'f'
            AND conrelid::regclass = '{tabla_nombre}'::regclass;
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query)
        foreign_keys = result.fetchall()
        
        return foreign_keys

print("\n" + "="*60)
print("Usando método específico de PostgreSQL:")
print("="*60)

foreign_keys_pg = encontrar_foreign_keys_pg(tabla)

if foreign_keys_pg:
    for fk in foreign_keys_pg:
        print(f"Constraint: {fk.constraint_name}")
        print(f"  Tabla origen: {fk.tabla_origen}")
        print(f"  Columna origen: {fk.columna_origen}")
        print(f"  Tabla destino: {fk.tabla_destino}")
        print(f"  Columna destino: {fk.columna_destino}")
        print("-" * 40)
else:
    print("No se encontraron foreign keys en esta tabla.")

