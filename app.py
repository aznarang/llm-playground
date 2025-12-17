import streamlit as st
from auth import login
from llm import call_ollama, call_huggingface
import os

st.set_page_config(page_title="LLM Playground", layout="wide")

if not login():
    st.stop()

st.title("LLM Playground – Foundations")

system_prompt = st.text_area(
    "System Prompt",
    "You are a precise and factual assistant."
)

user_prompt = st.text_area("User Prompt")

temperature = st.slider("Temperature", 0.0, 1.0, 0.2)

mode = st.radio("Execution Mode", ["Local (Ollama)", "Cloud (HF)"],index=1)

if st.button("Run"):
    with st.spinner("Thinking..."):
        if mode == "Local (Ollama)":
            response = call_ollama(user_prompt, system_prompt, temperature)
        else:
            os.environ["HF_API_KEY"] = st.secrets["HF_API_KEY"]
            response = call_huggingface(user_prompt, system_prompt)

    st.subheader("Response")
    st.write(response)
