
import os
import pickle
from graphs.deep_queries_processes_agent import deep_queries_processes_agent
from graphs.myPrompts import SYSTEM_DEEP_QUERIES_PROMPT_1, HUMAN_DEEP_QUERIES_PROMPT_1
from langchain_core.messages import SystemMessage, HumanMessage

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

path_file = r"C:\Users\Acer\Documents\dev\mine-sql\.db_docs\sql-miner\queries.txt"
with open(file=path_file, encoding="utf-8") as f:
    querys = f.read()
#print(querys)

print("\n\n")
print("---"*10)
print("\n"*10)

system_prompt = SYSTEM_DEEP_QUERIES_PROMPT_1.format(summary=summary, topic=topic, querys=querys)
human_prompt = HUMAN_DEEP_QUERIES_PROMPT_1.format(topic=topic)

messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=human_prompt)
]

initial_state = {"messages":messages}

#response = deep_queries_processes_agent.invoke(initial_state)

for step in deep_queries_processes_agent.stream(initial_state, stream_mode='values'):
    for i in range(len(step["messages"])):
        if (i == 0) or (i == 1):
            print("x")
        else:
            step["messages"][i].pretty_print()
    print("\n\n")
    print("xxxxxxxxxx")
    print("\n\n")
    for k in range(len(step["messages_react"])):
        step["messages_react"][k].pretty_print()
    print("\n\n")
    print("xxxxxxxxx")
    print("\n\n")
    print(step.get("response_query", "..."))
    print("\n\n")
    print("=="*10)
    print("=="*10)
    print("\n"*20)


"""
test_deep_queries_processes_agent.py

"""