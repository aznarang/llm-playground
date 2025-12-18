import json
from context_builder import build_mcp
from llm import call_ollama, call_huggingface
import streamlit as st
from auth import login


st.set_page_config(page_title="Context-Aware Assistant (MCP)", layout="wide")

if not login():
    st.stop()

user_prompt = st.text_area("User Prompt")
use_mcp = st.checkbox("Enable MCP", value=True)

session_state = {
    "user": "demo_user",
    "memory": ["User prefers short answers"]
}

if st.button("Run"):
    if use_mcp:
        mcp = build_mcp(user_prompt, session_state)
        final_prompt = f"""
Context:
{json.dumps(mcp, indent=2)}

Answer the user query strictly using this context.
"""
    else:
        final_prompt = user_prompt

    response = call_huggingface(final_prompt, "You are a precise AI assistant.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Response")
        st.write(response)

    with col2:
        st.subheader("MCP Context")
        st.json(mcp if use_mcp else {})
