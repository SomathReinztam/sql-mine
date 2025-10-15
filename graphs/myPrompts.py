

TABLE_ANALYSIS_PROMPT_1 = """
Eres un experto en análisis de datos y diseño de bases de datos SQL.
Recibirás las primeras 10 filas de una tabla SQL, junto con sus claves primarias y foráneas. 
Tu tarea es analizar esta información y generar una descripción detallada que incluya:

1. El propósito y función principal de la tabla dentro de una base de datos.
2. El tipo de información que almacena.
3. El tipo de consultas o análisis para los que podría resultar útil.
4. (Opcional) Relaciones que podrían inferirse con otras tablas a partir de las claves foráneas.

### Nombre de la tabla:
{table_name}

### Primeras 10 filas de la tabla:
{df}

### Claves primarias y foráneas:
{relations}
"""


TABLE_ANALYSIS_PROMPT_2 = """
You are an expert in data analysis and SQL database design.
You will receive the first 10 rows of an SQL table, along with its primary and foreign keys. 
Your task is to analyze this information and generate a detailed description that includes:

1. The purpose and main function of the table within a database.
2. The type of information it stores.
3. The kinds of queries or analyses it could be useful for.
4. (Optional) Possible relationships with other tables inferred from the foreign keys.

### Table name:
{table_name}

### First 10 rows of the table:
{df}

### Primary and foreign keys:
{relations}
"""


#======================================================================================================
#======================================================================================================

