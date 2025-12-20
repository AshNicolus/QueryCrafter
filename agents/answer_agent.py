import os
import json
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from google import genai

load_dotenv()

# Gemini / Vertex AI client configuration. Override via Streamlit secrets if available.
GEMINI_PROJECT = st.secrets.get("GEMINI_PROJECT", "finmate-svc-1-88322725")
GEMINI_LOCATION = st.secrets.get("GEMINI_LOCATION", "us-central1")

# Initialize the genai client for Vertex AI (Gemini)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    client = genai.Client(
        vertexai=True,
        project=GEMINI_PROJECT,
        location=GEMINI_LOCATION,
        api_key=GEMINI_API_KEY,
    )
else:
    client = genai.Client(
        vertexai=True,
        project=GEMINI_PROJECT,
        location=GEMINI_LOCATION,
    )

def generate_gemini(prompt: str, model: str = "gemini-2.5-flash") -> str:
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return getattr(resp, "text", str(resp))


# Simple file-backed conversation memory (keeps recent messages)
MEMORY_DIR = Path('.cache')
MEMORY_FILE = MEMORY_DIR / 'answer_memory.json'
MAX_MESSAGES = 200
RECENT_MESSAGES = 6

def _ensure_memory_dir():
    try:
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

def load_memory():
    try:
        if not MEMORY_FILE.exists():
            return []
        with MEMORY_FILE.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_memory(messages):
    try:
        _ensure_memory_dir()
        # keep only the last MAX_MESSAGES
        messages = messages[-MAX_MESSAGES:]
        with MEMORY_FILE.open('w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def append_message(role: str, text: str):
    msgs = load_memory()
    msgs.append({'role': role, 'text': text})
    save_memory(msgs)
def answer_agent(state):
    
    context = state["web_results"]

    max_input_tokens = 1024 
    context = context[:max_input_tokens]

    # support clearing memory via state flag
    if state.get('clear_memory'):
        save_memory([])

    # include recent conversation history in the prompt
    history = load_memory()
    recent = history[-RECENT_MESSAGES:]
    history_text = "\n".join([f"{m['role'].capitalize()}: {m['text']}" for m in recent]) if recent else ""

    prompt = (
        f"Conversation history:\n{history_text}\n\n"
        f"User asked: {state['input']}\n\nHere is some web info:\n{context}"
    )

    print("[AnswerAgent] Generating answer...")
    result = generate_gemini(prompt)

    # persist conversation pieces
    try:
        append_message('user', state.get('input', ''))
        append_message('assistant', result)
    except Exception:
        pass

    return {"output": result}
