from tavily import TavilyClient
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

def research_agent(state):
    query = state["input"]
    print(f"[ResearchAgent] Searching with Tavily: {query}")

    tavily = TavilyClient(api_key=TAVILY_API_KEY)
    results = tavily.search(query=query, max_results=5)

    docs = [result['content'] for result in results['results']]
    combined = "\n\n".join(docs)
    return {"web_results": combined}
