import streamlit as st
from langgraph_app import build_langgraph

app = build_langgraph()

st.title("Research Agent and Answer Generator")


topic = st.text_input("Enter your research topic:")


if topic:

    with st.spinner('Searching and generating answer...'):

        result = app.invoke({"input": topic})

    st.subheader("Final Answer:")
    st.write(result["output"])
