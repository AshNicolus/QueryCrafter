import os
from dotenv import load_dotenv

# Install: pip install -U langchain-openai langchain-core
from langchain_openai import AzureChatOpenAI

load_dotenv()

# REQUIRED ENV VARS (preferred approach)
# os.environ["AZURE_OPENAI_API_KEY"] = "<your_key>"
# os.environ["AZURE_OPENAI_ENDPOINT"] = "https://tradeguard3.cognitiveservices.azure.com"
# os.environ["AZURE_OPENAI_API_VERSION"] = "2024-08-01-preview"

# Or set directly in code if needed (not recommended for production)
AZURE_OPENAI_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") or "xxxxxxxxxxxxxxxx"
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION") or "2024-08-01-preview"
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT") or "gpt-4o"  

# Initialize AzureChatOpenAI
llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    temperature=0.7,
    max_tokens=3000,
)

def answer_agent(state):
    # Expecting state["web_results"] to be a string (concatenated snippets)
    context = state["web_results"]

    # Simple input length guard
    max_input_tokens = 1024 
    context = context[:max_input_tokens]

    prompt = f"Read the information and give a concise explanation:\n\n{context}"

    print("[AnswerAgent] Generating answer...")

    # AzureChatOpenAI supports string input via .invoke() which is treated as a Human message
    answer = llm.invoke(prompt)

    # answer is an AIMessage; to get the text content:
    return {"output": answer.content}
