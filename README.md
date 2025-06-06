# QueryCrafter
# 🌐 LangGraph Research & Answering System

This project is an intelligent research pipeline built using **LangGraph**, **LangChain**, **Streamlit**, and **Hugging Face**. It allows users to enter a topic, fetches real-time web data using Tavily, and generates a concise answer using a HuggingFace-hosted language model.

---

## 🚀 Features

- 🔍 Real-time Web search using **Tavily API**
- 🧠 Research summarization and Answer generation using **Hugging Face LLMs** (GPT-2 or GPT-Neo)
- 🛠 Modular agents using **LangGraph**
- 🖥️ Interactive **Streamlit UI**



## 🧱 Tech Stack

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Tavily](https://docs.tavily.com/)
- [Hugging Face Transformers](https://huggingface.co/)
- [Streamlit](https://streamlit.io/)

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/AshNicolus/QueryCrafter.git
cd QueryCrafter
```

### 2. Setup Environment
Install required packages:
```bash
pip install -r requirements.txt
```

Create a `.env` file:
```env
TAVILY_API_KEY=your_tavily_api_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

### 3. Run the App
```bash
streamlit run app.py
```

### 4. Input Your Query
- Enter your research topic in the UI.
- Wait for the system to fetch web results and generate an answer.

---