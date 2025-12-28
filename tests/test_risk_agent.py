from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

response = llm.invoke("Say hello in one sentence.")
print(response.content)