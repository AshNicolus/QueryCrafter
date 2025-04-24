from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

def research_agent(state):
    query = state["input"]
    print(f"[ResearchAgent] Searching with Tavily: {query}")

    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    #Here we need only max to max 5 relevant resources for doing the task
    results = tavily.search(query=query, max_results=5)

    docs = [result['content'] for result in results['results']]
    combined = "\n\n".join(docs)
    return {"web_results": combined}
