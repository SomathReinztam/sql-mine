import os
import pickle
from graphs.make_querys_agent import make_querys_agent

path_doc = r"C:\Users\Acer\Documents\dev\mine-sql\.db_docs\db_documentacion"
doc_file = "originabotplain.txt"
doc_file = os.path.join(path_doc, doc_file)

with open(file=doc_file, encoding="utf-8") as f:
    doc = f.read()

path_ditct = r"C:\Users\Acer\Documents\dev\mine-sql\.db_docs\sql-miner"
file_name = "mydict.pkl"
file = os.path.join(path_ditct, file_name)
with open(file, "rb") as f:
    mydict = pickle.load(f)

summary = mydict["summary"]
print(summary)
print("\n\n")


topic = mydict["topic"][0]
print(topic)
print("\n\n")
print("---"*10)

initila_state = {"summary":summary, "topic":topic, "doc":doc}

response = make_querys_agent.invoke(initila_state)

querys = response["querys"]
print(querys)