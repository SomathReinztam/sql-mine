
import os
from dotenv import load_dotenv
from graphs.myPrompts import TABLE_ANALYSIS_PROMPT_1

from langchain_ollama import ChatOllama

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

load_dotenv()
base_url_model = os.getenv("BASE_URL_MODEL1")
model = "gemma3:27b"

llm = ChatOllama(model=model, base_url=base_url_model)

class State(TypedDict):
    table_name : str
    df : str
    relations : str
    table_description : str


def table_description_node(state : State) -> State:
    table_name = state['table_name']
    df = state['df']
    relations = state['relations']
    prompt = TABLE_ANALYSIS_PROMPT_1.format(table_name=table_name, relations=relations, df=df)
    # print("\n"*5)
    # print(prompt)
    # print("\n"*5)
    response = llm.invoke(prompt)
    #print("-><-")
    return {"table_description":response.content}

builder = StateGraph(State)

builder.add_node("table_description_node", table_description_node)

builder.add_edge(START, "table_description_node")
builder.add_edge("table_description_node", END)

table_agent = builder.compile()


