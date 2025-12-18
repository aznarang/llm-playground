def build_mcp(user_input, session_state):
    recent_history = session_state.get("chat_history", [])[-3:]

    return {
        "intent": "decide_or_answer",
        "role": "planner",
        "available_tools": {
            "calculator": {
                "description": "Add two integers",
                "args": ["a", "b"]
            },
            "text_length": {
                "description": "Get length of a text",
                "args": ["text"]
            }
        },
        "constraints": [
            "Respond ONLY in valid JSON",
            "Do not execute tools",
            "Choose tool only if required"
        ],
        "memory": recent_history,
        "data": {
            "current_query": user_input
        }
    }
