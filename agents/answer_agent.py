import os
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub


load_dotenv()

#Using a GPT-2 model as it is lightweight and Open-Source can be easily accessible through Inference Point
llm = HuggingFaceHub(
    repo_id="gpt2",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model_kwargs={"temperature": 0.7, "max_new_tokens": 300}
)


def answer_agent(state):
    context = state["web_results"]

    # Using this to avoid the Run Time Error
    max_input_tokens = 1024 - 200
    context = context[:max_input_tokens]

    prompt = f"Read the information and give the concise Explanation:\n\n{context}"

    print("[AnswerAgent] Generating answer...")

    answer = llm(prompt)
    return {"output": answer}
