from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents.research_agent import research_agent
from agents.answer_agent import answer_agent



class ResearchState(TypedDict):
    input: str
    web_results: str
    output: str

def build_langgraph():
    graph = StateGraph(ResearchState)

    graph.add_node("research", research_agent)
    graph.add_node("draft", answer_agent)

    graph.set_entry_point("research")
    graph.add_edge("research", "draft")
    graph.add_edge("draft", END)

    return graph.compile()
