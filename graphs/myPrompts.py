

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


UNDERSTAND_SCHEMA_PROMPT_2 = """
Eres un asistente útil y experto en análisis de bases de datos.
Se te proporcionará la documentación de una base de datos que describe cada tabla, incluyendo:
- Su función y propósito.
- El tipo de información que almacena.
- Los tipos de consultas o análisis para los que puede ser útil.
- Sus relaciones con otras tablas.

Tu tarea es analizar esta documentación y generar un resumen claro y conciso que explique:
1. Un resumen general de la base de datos
2. Analizar que usos y tareas sirve la base de datos.
3. **responde en español**

El resultado debe seguir estrictamente el siguiente formato:

Resumen de la Base de Datos:
- (Escribe aquí un resumen breve pero completo de la base de datos.)

Usos y Análisis Posibles:
- (Primer uso o tipo de análisis posible)
- (Segundo uso o tipo de análisis posible)
- (Otros usos o aplicaciones relevantes)

### documentación de la base de datos

{doc}
"""


#----------------------------------------


PARSER_ANALYSIS_PROMPT_1 = """
Eres un experto en análisis y formateo de texto.
Se te proporcionará la documentación de una base de datos. Esta documentación incluye:
- Un breve resumen general de la base de datos.
- Una lista o descripción de los posibles usos, tipos de análisis o aplicaciones que pueden realizarse con dicha base de datos.

Tu tarea consiste en generar un objeto JSON que extraiga textualmente (sin parafrasear) el resumen y los usos o análisis descritos.

El JSON debe tener la siguiente estructura:

```json
{{
   "summary": "Texto extraído del resumen principal de la documentación.",
   "topic": ["Título y texto extraído del primer uso o tipo de análisis mencionado.","Título y texto extraído del segundo uso o tipo de análisis mencionado.", ...]
}}
```

### Resumen y analisis:
{summary}
"""


#==========================================================================================================
#==========================================================================================================

MAKE_QUERYS_PROMPT_1 = """
Eres un experto ingeniero y analista de datos especializado en minería de datos y análisis de bases de datos relacionales.
A continuación, se presenta un resumen general de la base de datos:

{summary}

Las tablas de esta base de datos permiten realizar una amplia variedad de análisis y tareas relacionadas con el siguiente tema:

{topic}

También se te proporciona la documentación completa de la base de datos, que describe cada tabla e incluye:
- Su función y propósito.
- El tipo de información que almacena.
- Los tipos de consultas o análisis para los que puede ser útil.
- Sus relaciones con otras tablas.

Tu tarea consiste en, a partir de la documentación, formular una lista de consultas en lenguaje natural que permitan extraer la mayor cantidad posible de información relevante sobre el tema mencionado.

Estas consultas deben:

- Ser diversas y cubrir distintos ángulos del tema.
- Incluir tanto análisis descriptivos como comparativos o inferenciales, cuando sea pertinente.
- Las consultas **deben** incluir indicaciones del el nombre o los nombres de las tablas a consultar

### Documentación de la base de datos:

{doc}
"""
