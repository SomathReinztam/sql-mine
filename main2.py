import os
import json
import time
from graphs.db_utils import (
    get_db_relations,
    describe_table_relationships,
    get_db_tables_name,
    get_head_table_markdown
)
from graphs.table_agent import table_agent

# =============================
# CONFIGURACIÓN DE CONEXIÓN
# =============================
db_user = "postgres"
db_pass = "3636"
db_host = "localhost"
db_name = "northwind"

# =============================
# ARCHIVOS DE PROGRESO
# =============================
progress_file = "progress.json"
output_file = "northwind.txt"

# =============================
# FUNCIONES AUXILIARES
# =============================

def save_progress(index, resumen):
    """Guarda el progreso actual (índice y resumen) en un archivo JSON."""
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump({"index": index, "resumen": resumen}, f, ensure_ascii=False, indent=2)

def load_progress():
    """Carga el progreso si existe; de lo contrario, comienza desde 1."""
    if os.path.exists(progress_file):
        with open(progress_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("index", 1), data.get("resumen", "")
    return 1, ""

def save_output(resumen):
    """Guarda el resumen completo en un archivo de texto."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(resumen)

# =============================
# CARGA DE DATOS DE LA BD
# =============================
print("Obteniendo relaciones de la base de datos...")
primary_keys, foreign_keys = get_db_relations(
    db_user=db_user, db_pass=db_pass, db_host=db_host, db_name=db_name
)
tables = get_db_tables_name(
    db_user=db_user, db_pass=db_pass, db_host=db_host, db_name=db_name
)

# =============================
# RECUPERAR PROGRESO
# =============================
N, resumen_db = load_progress()
print(f"Reanudando desde la tabla número {N} de {len(tables)}")

# =============================
# PROCESAMIENTO
# =============================
for i, table_name in enumerate(tables, start=1):
    if i < N:  # Saltar tablas ya procesadas
        continue

    print("=="*10)
    print(f"Procesando tabla {i}/{len(tables)}: {table_name}")
    print("=="*10)

    try:
        relations = describe_table_relationships(table_name, primary_keys, foreign_keys, True)
        df_markdown = get_head_table_markdown(
            table_name, db_user=db_user, db_pass=db_pass, db_host=db_host, db_name=db_name
        )
        initial_state = {
            "table_name": table_name,
            "relations": relations,
            "df": df_markdown
        }
        response = table_agent.invoke(initial_state)
        print()
        table_description = response.get("table_description", "")
        resumen_db += table_description + "\n" * 5

        print(table_description)
        print("\n" * 5)

        # Guardar progreso y archivo parcial después de cada tabla
        save_progress(i + 1, resumen_db)
        save_output(resumen_db)

    except Exception as e:
        print(f"⚠️ Error al procesar la tabla {table_name}: {e}")
        print("Intentando reconexión en 10 segundos...")
        time.sleep(10)
        # Guardar estado antes de salir
        save_progress(i, resumen_db)
        save_output(resumen_db)
        break  # Rompe el bucle, se puede reanudar después

print("✅ Proceso finalizado o interrumpido. Progreso guardado.")

"""
164 - silk_response FAIL


"""