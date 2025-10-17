import os
from graphs.summary_db_agent import summary_db_agent

path_doc = r"C:\Users\Acer\Documents\dev\mine-sql\.db_docs\db_documentacion"
doc_file = "originabotplain.txt"
doc_file = os.path.join(path_doc, doc_file)

with open(file=doc_file, encoding="utf-8") as f:
    doc = f.read()

initial_state = {"doc":doc}

response = summary_db_agent.invoke(initial_state)

print(response["summary"])

print("\n"*10)
x = response["summary_parsered"]
print(x)

print("\n"*10)

print(x["summary"])
print("\n"*5)
print(x["topic"])
print()
for i in x["topic"]:
    print(i)
    print("\n")

output_file = r"C:\Users\Acer\Documents\dev\mine-sql\.db_docs\sql-miner\Summary2.md"
with open(file=output_file, mode="w", encoding="utf-8") as f:
    f.write(response["summary"])


"""
test_summary_db_agent.py

"""