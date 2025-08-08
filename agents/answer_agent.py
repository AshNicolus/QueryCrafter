import os
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from langchain_openai import AzureChatOpenAI

load_dotenv()

# REQUIRED ENV VARS (preferred approach)
# os.environ["AZURE_OPENAI_API_KEY"] = "<your_key>"
# os.environ["AZURE_OPENAI_ENDPOINT"] = "https://tradeguard3.cognitiveservices.azure.com"
# os.environ["AZURE_OPENAI_API_VERSION"] = "2024-08-01-preview"

# Or set directly in code if needed (not recommended for production)
AZURE_OPENAI_API_KEY = "AIkg5CJq34sgoJaRg6DnO4dViK3e2t8cIPnfQTtxUtWDFcJkYDDqJQQJ99BGACHYHv6XJ3w3AAAAACOGLjBK"
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") or "https://tradeguard3.cognitiveservices.azure.com"
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION") or "2024-08-01-preview"
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT") or "gpt-4o"  

llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    temperature=0.7,
    max_tokens=3000,
)
# memory = ConversationBufferMemory(return__messages=True)
memory = ConversationBufferMemory(return_messages=True)

conversation=ConversationChain(llm=llm, memory=memory, verbose=True)
def answer_agent(state):
    
    context = state["web_results"]

    max_input_tokens = 1024 
    context = context[:max_input_tokens]

    prompt = f"User asked: {state['input']}\n\nHere is some web info:\n{context}"

    print("[AnswerAgent] Generating answer...")
    result = conversation.predict(input=prompt)
    # answer = llm.invoke(prompt)

    return {"output": result}
