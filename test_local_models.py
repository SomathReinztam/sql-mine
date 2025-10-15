"""
test_local_models.py

"""
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()
base_url_model = os.getenv("BASE_URL_MODEL1")
print(base_url_model)

print("\n\n")
#model = "gpt-oss:20b"
model = "gemma3:27b"
#model = "deepseek-r1:32b"
llm = ChatOllama(model=model, base_url=base_url_model)
prompt = "Cuantame una broma sobre patos"
response = llm.invoke(prompt)

print(response.content)

