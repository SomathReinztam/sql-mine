from sqlalchemy import create_engine, text
import pandas as pd

def get_db_relations(db_user, db_pass, db_host, db_name):
    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")

    with engine.connect() as conn:
        pk_query = text("""
            SELECT
                tc.table_name,
                kcu.column_name
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            WHERE
                tc.constraint_type = 'PRIMARY KEY'
                AND tc.table_schema = 'public';
        """)
        pks = conn.execute(pk_query).fetchall()

    primary_keys = {}
    for table, column in pks:
        primary_keys.setdefault(table, []).append(column)
    
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

    foreign_keys = [
        {
            "tabla_origen": row.table_name,
            "columna_origen": row.column_name,
            "tabla_referenciada": row.foreign_table_name,
            "columna_referenciada": row.foreign_column_name
        }
        for row in fks
    ]

    return primary_keys, foreign_keys






def describe_table_relationships(table_name, primary_keys, foreign_keys, esp):
    relaciones = [fk for fk in foreign_keys if fk["tabla_origen"] == table_name]
    resumen = ""
    if esp:
        if table_name in primary_keys:
                resumen += f"🔑 Llave primaria: {', '.join(primary_keys[table_name])}\n"
        if relaciones:
            resumen += "🔗 **Relaciones foráneas** 'columna_origen' → 'tabla_referenciada'.'columna_referenciada' :\n"
            for r in relaciones:
                resumen += f"  {r['columna_origen']} → {r['tabla_referenciada']}.{r['columna_referenciada']}\n"
        else:
            resumen += "Sin relaciones foráneas.\n"
    return resumen



def get_db_tables_name(db_user, db_pass, db_host, db_name):
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
        return tables


def get_head_table_markdown(table_name, db_user, db_pass, db_host, db_name):
    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")
    QUERY = f"SELECT * FROM {table_name} LIMIT 10;"

    with engine.connect() as conn:
        query = text(QUERY.format(table=table_name))
        df = pd.read_sql_query(query, engine)
    
    return df.to_markdown(index=False)



