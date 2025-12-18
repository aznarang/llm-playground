def build_mcp(user_input, session_state):
    return {
        "intent": "answer_user_query",
        "role": "enterprise_assistant",
        "state": {
            "user": session_state.get("user", "anonymous")
        },
        "constraints": [
            "Be concise",
            "Use only provided context",
            "Avoid hallucination"
        ],
        "memory": session_state.get("memory", []),
        "data": {
            "query": user_input
        }
    }
