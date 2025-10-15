import os
from graphs.agent_1 import agent_1

path_doc = r"C:\Users\Acer\Documents\dev\mine-sql\.db_docs"
doc_file = "originabotplain.txt"
doc_file = os.path.join(path_doc, doc_file)

with open(file=doc_file, encoding="utf-8") as f:
    doc = f.read()

initial_state = {"doc":doc}

response = agent_1.invoke(initial_state)

print(response["summary"])
