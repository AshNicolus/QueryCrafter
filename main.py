from langgraph_app import build_langgraph

if __name__ == "__main__":
    app = build_langgraph()
    topic = input("Enter your research topic: ")
    result = app.invoke({"input": topic})
    print("\n Final Answer:\n", result["output"])
