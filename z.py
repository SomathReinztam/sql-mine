import pandas as pd

def describir_estructura_tabla(nombre_tabla, conn):
    # Columnas y tipos
    columnas = pd.read_sql(f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = '{nombre_tabla}'
        AND table_schema = 'public';
    """, conn)

    # Relaciones
    relaciones = [fk for fk in foreign_keys if fk["tabla_origen"] == nombre_tabla]

    # Construir resumen
    resumen = f"Tabla '{nombre_tabla}' tiene {len(columnas)} columnas.\n"
    resumen += "Columnas principales:\n"
    resumen += columnas.head(5).to_markdown(index=False) + "\n\n"

    if nombre_tabla in primary_keys:
        resumen += f"🔑 Llave primaria: {', '.join(primary_keys[nombre_tabla])}\n"
    if relaciones:
        resumen += "🔗 Relaciones foráneas:\n"
        for r in relaciones:
            resumen += f"  {r['columna_origen']} → {r['tabla_referenciada']}.{r['columna_referenciada']}\n"
    else:
        resumen += "Sin relaciones foráneas.\n"

    return resumen
