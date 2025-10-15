import os
from dotenv import load_dotenv
from graphs.myPrompts import UNDERSTAND_SCHEMA_PROMPT_1

from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
# from langchain_groq import ChatGroq

from typing import TypedDict, Literal, Annotated, Sequence
from langgraph.graph import StateGraph, START, END

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
# groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature = 0, google_api_key=api_key)

class State(TypedDict):
    doc : str
    summary : str


def summary_node(state : State) -> State:
    doc = state['doc']
    prompt = UNDERSTAND_SCHEMA_PROMPT_1.format(doc=doc)
    response = llm.invoke(prompt)
    return {"summary":response.content}

builder = StateGraph(State)

builder.add_node("summary_node", summary_node)

builder.add_edge(START, "summary_node")
builder.add_edge("summary_node", END)

agent_1 = builder.compile()