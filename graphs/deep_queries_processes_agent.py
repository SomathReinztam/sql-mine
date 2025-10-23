import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import time

from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langchain_core.messages import RemoveMessage

from typing import TypedDict, Literal, Annotated, Sequence
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_prompt = prompt_template.format(dialect="PostgreSQL", top_k=10)
parser = JsonOutputParser()

db_user = "postgres" 
db_pass = "3636" 
db_host = "localhost" 
db_name = "originabotplain" 

load_dotenv()
base_url_model = os.getenv("BASE_URL_MODEL1")
#model = "gemma3:27b" -> FAIL no acepta tools.
model = "gpt-oss:20b"
llm = ChatOllama(model=model, base_url=base_url_model)


#api_key = os.getenv("GOOGLE_API_KEY")
#llm_2 = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature = 0, google_api_key=api_key)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#model = "openai/gpt-oss-120b"
#model = "openai/gpt-oss-20b"
#llm = ChatGroq(model=model, temperature=0, api_key=GROQ_API_KEY)


engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}") 
db = SQLDatabase(engine)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]
    messages_react : Annotated[Sequence[BaseMessage], add_messages]
    response_query : str | None



def initial_deep_query_node(state : State) -> State:
    initial_message = state["messages"]
    response = llm.invoke(initial_message)
    print("xxx"*5 + " initial_node")
    print("xxx"*5)
    print("xxx"*5)
    print("\n")
    print("query inicial:\n")
    response.pretty_print()
    print("\n\n"*5)
    return {"messages":response}


def set_ReAct_messages_node(state : State) -> State:
    query_ai_message = state["messages"][-1]
    json = parser.parse(query_ai_message.content)
    query = json["query"]
    messages_react = [SystemMessage(content=system_prompt), HumanMessage(content=query)]
    print("xxx"*5 + " set_ReAct_messages_node")
    print("xxx"*5)
    print("xxx"*5)
    print("\n")
    print(f"len messages_react:{len(messages_react)}")
    print("\n\n"*5)
    return {"messages_react":messages_react}
    


def ReAct_node(state : State) -> State:
    messages_react = state['messages_react']
    response = llm_with_tools.invoke(messages_react)
    response_query = response.content
    print("xxx"*5 + " ReAct_node")
    print("xxx"*5)
    print("xxx"*5)
    print("\n")
    print(f"type response_query: {type(response_query)}")
    print("\n")
    print("Current Message ReAct:\n")
    response.pretty_print()
    print("\n\n"*5)
    return {"messages_react":response, "response_query":response_query}




def should_continue_with_sql(state : State) -> Literal["tool_node_wrapper", "clear_ReAct_messages_node"]: # type: ignore
    print("---"*5 + " should_continue_with_sql")
    print("---"*5)
    print("\n")
    last_message = state['messages_react'][-1]
    if last_message.tool_calls:
        print("tool_node_wrapper")
        print("\n\n"*5)
        return "tool_node_wrapper"
    print("clear_ReAct_messages_node")
    print("\n\n"*5)
    return "clear_ReAct_messages_node"



tool_node = ToolNode(tools, messages_key="messages_react")

def tool_node_wrapper(state: State) -> State:
    #message = state["messages_react"][-1]
    # tool_response será un dict como {"messages_react": [ToolMessage, ToolMessage, ...]}
    tool_response = tool_node.invoke(state)
    print("xxx"*5 + " tool_node_wrapper")
    print("xxx"*5)
    print("xxx"*5)
    print("\n")
    print(type(tool_response))
    print("\n")
    print(tool_response.keys())
    print("\n")
    tool_messages = tool_response["messages_react"]
    for message in tool_messages:
        message.pretty_print()
    print("\n\n"*5)
    return {"messages_react":tool_messages}




def clear_ReAct_messages_node(state : State) -> State:
    messages = state["messages_react"]
    response_query = state["response_query"]
    response_query_human_message = HumanMessage(content=response_query)
    print("xxx"*5 + " clear_ReAct_messages_node")
    print("xxx"*5)
    print("xxx"*5)
    print("\n")
    print("messages_react final:\n")
    for message in messages:
        message.pretty_print()
    print("\n")
    print("Borrando historial de react")
    print("\n\n"*5)
    # Crear una lista de RemoveMessage para eliminar todos los mensajes actuales
    return {"messages_react": [RemoveMessage(id=m.id) for m in messages], "messages":response_query_human_message}



def deep_query_node(state : State) -> State:
    messages = state["messages"]
    response = llm.invoke(messages)
    print("xxx"*5 + " deep_query_node")
    print("xxx"*5)
    print("xxx"*5)
    print("\n")
    lista = state["messages"] + [response]
    lista = lista[2:]
    for message in lista:
        message.pretty_print()
    print("\n"*2)
    print("=="*60)
    print("=="*60)
    print("=="*60)
    print("\n"*30)
    return {"messages":response}



def should_end(state : State) -> Literal["set_ReAct_messages_node", END]: # type: ignore
    print("---"*5 + " should_end")
    print("---"*5)
    print("\n\n")
    ai_message = state["messages"][-1]
    json = parser.parse(ai_message.content)
    if (json["processes"] is None):
        print("set_ReAct_messages_node")
        print("\n\n"*5)
        return "set_ReAct_messages_node"
    print("END")
    return END


builder = StateGraph(State)

builder.add_node("initial_deep_query_node", initial_deep_query_node)
builder.add_node("set_ReAct_messages_node", set_ReAct_messages_node)
builder.add_node("ReAct_node", ReAct_node)
builder.add_node("tool_node_wrapper", tool_node_wrapper)
builder.add_node("clear_ReAct_messages_node", clear_ReAct_messages_node)
builder.add_node("deep_query_node", deep_query_node)

builder.add_edge(START, "initial_deep_query_node")
builder.add_edge("initial_deep_query_node", "set_ReAct_messages_node")
builder.add_edge("set_ReAct_messages_node", "ReAct_node")
builder.add_conditional_edges("ReAct_node", should_continue_with_sql)
builder.add_edge("tool_node_wrapper", "ReAct_node")
builder.add_edge("clear_ReAct_messages_node", "deep_query_node")
builder.add_conditional_edges("deep_query_node", should_end)

deep_queries_processes_agent = builder.compile()


# image_data = deep_queries_processes_agent.get_graph().draw_mermaid_png()
# with open("deep_queries_processes_agent.png", "wb") as image_file:
#     image_file.write(image_data)
