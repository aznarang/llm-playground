import streamlit as st
import json

from auth import login
from context_builder import build_mcp
from llm import call_llm_planner
from tools import calculator, text_length

st.set_page_config(page_title="Tool Calling", layout="wide")

if not login():
    st.stop()

st.title("Tool Calling (Planner → Executor)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_prompt = st.text_input("User Query")

if st.button("Run"):
    mcp = build_mcp(user_prompt, st.session_state)

    planner_output = call_llm_planner(
        system_prompt="You are a careful enterprise planner.",
        mcp_context=mcp
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Planner Output")
        st.json(planner_output)

    result = None

    if "tool" in planner_output and planner_output["tool"] != "none":
        tool = planner_output["tool"]
        args = planner_output.get("args", {})

        if tool == "calculator":
            result = calculator(**args)
        elif tool == "text_length":
            result = text_length(**args)
        else:
            result = "Unknown tool"

        final_answer = f"Tool `{tool}` executed. Result = {result}"

    else:
        final_answer = planner_output.get("answer", "No answer")

    st.session_state.chat_history.append({
        "question": user_prompt,
        "answer": final_answer
    })

    with col2:
        st.subheader("Execution Result")
        st.write(final_answer)

    with col3:
        st.subheader("MCP Context")
        st.json(mcp)
