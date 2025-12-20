from tavily import TavilyClient
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

def research_agent(state):
    query = state["input"]
    print(f"[ResearchAgent] Searching with Tavily: {query}")
    # Hard-coded Tavily API key for testing (replace/remove after debugging)
    

    # Validate presence of API key and surface helpful debug info (masked)
    if not TAVILY_API_KEY:
        err = ("Tavily API key not found. Add `TAVILY_API_KEY` to Streamlit secrets "
               "or set the environment variable `TAVILY_API_KEY`.")
        print(f"[ResearchAgent][ERROR] {err}")
        raise RuntimeError(err)

    masked = TAVILY_API_KEY[:6] + "..." + TAVILY_API_KEY[-4:] if len(TAVILY_API_KEY) > 10 else "(hidden)"
    print(f"[ResearchAgent] Using TAVILY_API_KEY {masked} (len={len(TAVILY_API_KEY)})")

    tavily = TavilyClient(api_key=TAVILY_API_KEY)

   
    try:
        results = tavily.search(query=query, max_results=5)
    except Exception as e:
        name = e.__class__.__name__
        msg = str(e)
        if "InvalidAPIKeyError" in name or "Unauthorized" in msg or "invalid API key" in msg.lower():
            advise = (
                "Tavily returned an authentication error. Possible causes:\n"
                "- The `TAVILY_API_KEY` in Streamlit secrets is missing, incorrect, or expired.\n"
                "- You're running Streamlit from a different working directory, so `.streamlit/secrets.toml` isn't being picked up.\n"
                "- An environment variable `TAVILY_API_KEY` is overriding the secret with a wrong value.\n\n"
                "Troubleshooting steps:\n"
                "1) Verify the key in `.streamlit/secrets.toml` (or update it in Streamlit Cloud settings).\n"
                "2) Export the key as an environment variable for local runs: `set TAVILY_API_KEY=your_key` (PowerShell: `$env:TAVILY_API_KEY=\"your_key\"`).\n"
                "3) If the key was just created, wait a minute and try again (some providers take a moment to activate).\n"
                "4) If the problem persists, request a fresh API key from Tavily support or verify the account's billing/permissions.\n"
            )
            masked = TAVILY_API_KEY[:6] + "..." + TAVILY_API_KEY[-4:] if len(TAVILY_API_KEY) > 10 else "(hidden)"
            full = f"Authentication failure for TAVILY_API_KEY {masked} (len={len(TAVILY_API_KEY)}).\n{advise}"
            print(f"[ResearchAgent][ERROR] {full}")
            raise RuntimeError(full) from e
        # re-raise unknown exceptions
        raise

    docs = [result['content'] for result in results['results']]
    combined = "\n\n".join(docs)
    return {"web_results": combined}
