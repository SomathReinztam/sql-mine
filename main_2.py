import os
from graphs.summary_db_agent import summary_db_agent
from graphs.make_querys_agent import make_querys_agent
from graphs.ReActSQL import ReActSQL

from langchain_core.messages import SystemMessage, HumanMessage

from langchain import hub
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
prompt_template
system_prompt = prompt_template.format(dialect="PostgreSQL", top_k=10)

path_doc = r"C:\Users\Acer\Documents\dev\mine-sql\.db_docs\db_documentacion"
doc_file = "originabotplain.txt"
doc_file = os.path.join(path_doc, doc_file)

with open(file=doc_file, encoding="utf-8") as f:
    doc = f.read()

print("================= start summary_db_agent")
print("\n\n")

initial_state = {"doc":doc}
response = summary_db_agent.invoke(initial_state)

print("="*5 + "Resumen de la documentacion de la db:\n\n")
summary = response["summary"]
print(summary)
print("\n\n")

mydict = response["summary_parsered"]
print("-"*5 + "summary_parsered:\n\n")

mini_summary = mydict["summary"]
topics = mydict["topic"]
print("\n\n\n")
print("------ topics - mini_summary")
print(topics)
print("\n")
print(mini_summary)
print("\n\n")
print("================= end summary_db_agent")
print("\n"*5)


print("================= start make_querys_agent")
print("\n\n\n")

n = 1
for topic in topics:
    print("------------------------------------")
    print(f"---------------------- topic {n}:\n")
    print("------------------------------------")
    print(topic)
    print("\n\n")
    initila_state = {"summary":mini_summary, "topic":topic, "doc":doc}
    response = make_querys_agent.invoke(initila_state)
    
    print("-"*5 + "querys")
    querys = response["querys"]
    print(querys)
    print("\n")