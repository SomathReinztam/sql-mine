

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


#----------------------------------------



QUERYS_PARSER_PROMPT_1 = """
Eres un experto en formatear información estructurada.
Se te proporcionará una lista de consultas en lenguaje natural dirigidas a una base de datos, junto con las tablas relacionadas a cada consulta.
Tu tarea es formatear estas consultas y sus tablas relacionadas dentro de una lista, donde cada elemento represente una consulta y las tablas asociadas a ella.

Debes devolver la respuesta estrictamente en formato JSON válido, siguiendo la siguiente estructura:

```json
{{
  "querys": [
    "Consulta y sus tablas relacionadas",
    "Consulta y sus tablas relacionadas",
    ...
  ]
}}
```

### Lista de consultas:
{querys}
"""


QUERYS_PARSER_PROMPT_2 = """
Eres un experto en formatear información estructurada.
Se te proporcionará una lista de consultas en lenguaje natural dirigidas a una base de datos, junto con las tablas relacionadas a cada consulta.
Tu tarea es formatear estas consultas y sus tablas relacionadas dentro de una lista, donde cada elemento represente una **cadena de texto** con la consulta y las tablas asociadas a ella.

Debes devolver la respuesta estrictamente en formato JSON válido, siguiendo la siguiente estructura:

```json
{{
  "querys": [
    "Consulta y sus tablas relacionadas",
    "Consulta y sus tablas relacionadas",
    ...
  ]
}}
```

### Lista de consultas:
{querys}
"""

#==========================================================================================================
#==========================================================================================================

SYSTEM_DEEP_QUERIES_PROMPT_1 = """
Eres un ingeniero de datos experto en análisis y minería de información en bases de datos relacionales.
Tu objetivo es **descubrir procesos o rutinas de una empresa** basándote en la información contenida en una base de datos.

A continuación se te proporciona un resumen de la base de datos:
{summary}

Tu tarea consiste en **formular consultas en lenguaje natural** sobre la base de datos para identificar **procesos relacionados con el siguiente tema**:
{topic}

Una vez identifiques un posible proceso o rutina, deberás **profundizar con nuevas preguntas** hasta obtener toda la información necesaria sobre dicho proceso.  
Estos procesos serán posteriormente automatizados.

### Instrucciones importantes:
- Realiza tus consultas **una a una**.  
- Cada vez que formules una consulta, recibirás una respuesta basada en los datos disponibles. 
- formula la consulta en **lenguaje natural**
- **No asumas que la respuesta es completamente correcta**; si la información no es suficiente o no responde a tu duda, **reformula la consulta**.  
- Comienza con **preguntas generales** para familiarizarte con la estructura y contenido de la base de datos.  
- Luego pasa a **preguntas más específicas** hasta identificar un proceso claro que pueda automatizarse.
- Responde siempre con el formato que se te indique.

A modo de ejemplo, aquí tienes consultas previas relacionadas con el tema:
{querys}

Recuerda: tu meta final es **encontrar y describir un proceso o rutina de negocio**, a partir del conocimiento que obtengas consultando la base de datos.
"""



HUMAN_DEEP_QUERIES_PROMPT_1 = """
Tengo acceso directo a la base de datos sobre la cual se busca automatizar procesos.

Tu tarea es **formular consultas en lenguaje natural** que me ayuden a **identificar procesos o rutinas** relacionadas con el siguiente tema:
{topic}

Yo ejecutaré esas consultas sobre la base de datos y te mostraré los resultados obtenidos, para que puedas seguir refinando tus preguntas
hasta descubrir un proceso claro y completo que pueda ser automatizado.

Mientras formules consultas, responde con el siguiente formato JSON

```json
{{
  "query" : "formula la consulta aquí",
  "processes" : null 
}}
```

Cuando hayas recolectado la suficiente información e identificado un proceso responde con el siguiente formato JSON

```json
{{
  "query" : null,
  "processes" : "Explica el proceso que identificaste aquí"
}}
```

"""

#==========================================================================================================
#==========================================================================================================
