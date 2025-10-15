
# understand scheme

UNDERSTAND_SCHEMA_PROMPT_1 = """
Eres un asistente útil y experto en análisis de bases de datos.
Se te proporcionará la documentación de una base de datos que describe cada tabla, incluyendo:
- Su función y propósito.
- El tipo de información que almacena.
- Los tipos de consultas o análisis para los que puede ser útil.
- Sus relaciones con otras tablas.

Tu tarea es analizar esta documentación y generar un resumen claro y conciso que explique:
1. Para qué sirve la base de datos.
2. Qué tipo de usos o análisis permitiría realizar.

El resumen debe ser coherente, informativo y redactado en lenguaje natural.

### documentación de la base de datos

{doc}
"""

