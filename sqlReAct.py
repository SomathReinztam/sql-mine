
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

from typing import TypedDict, Literal, Annotated, Sequence
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

db_user = "postgres" 
db_pass = "3636" 
db_host = "localhost" 
db_name = "northwind" 

load_dotenv()
api_key = os.getenv("SOLEN_GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature = 0, google_api_key=api_key)

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}") 
db = SQLDatabase(engine)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]


def ReAct_node(state : State) -> State:
    prompt = state['messages']
    response = llm_with_tools.invoke(prompt)
    #print(f"-------{type(response)}")
    return {"messages":response}


tool_node = ToolNode(tools)


def should_continue(state : State) -> Literal["tool_node", END]: # type: ignore
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tool_node"
    return END


builder = StateGraph(State)

builder.add_node("ReAct_node", ReAct_node)
builder.add_node("tool_node", tool_node)

builder.add_edge(START, "ReAct_node")
builder.add_conditional_edges("ReAct_node", should_continue)
builder.add_edge("tool_node", "ReAct_node")


graph = builder.compile()