import os
from dotenv import load_dotenv
from graphs.myPrompts import MAKE_QUERYS_PROMPT_1, QUERYS_PARSER_PROMPT_2

from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser

from typing import TypedDict, Literal, Annotated, Sequence
from langgraph.graph import StateGraph, START, END

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
# groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature = 0, google_api_key=api_key)


class State(TypedDict):
    summary : str
    topic : str
    doc : str

    querys : str
    querys_parsered : dict

def make_querys(state : State) -> State:
    summary = state['summary']
    topic = state["topic"]
    doc = state["doc"]

    prompt = MAKE_QUERYS_PROMPT_1.format(summary=summary, topic=topic,doc=doc)
    response = llm.invoke(prompt)

    return {"querys":response.content}


def parser_queries(state : State) -> State:
    querys = state["querys"]
    prompt = QUERYS_PARSER_PROMPT_2.format(querys=querys)
    response = llm.invoke(prompt)
    parser = JsonOutputParser()
    querys_parsered = parser.parse(response.content)
    return {"querys_parsered":querys_parsered}




builder = StateGraph(State)

builder.add_node("make_querys", make_querys)
builder.add_node("parser_queries", parser_queries)

builder.add_edge(START, "make_querys")
builder.add_edge("make_querys", "parser_queries")
builder.add_edge("parser_queries", END)

make_querys_agent = builder.compile()
