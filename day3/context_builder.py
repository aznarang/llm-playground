def build_mcp(user_input, session_state):
    recent_history = session_state.get("chat_history", [])[-3:]

    return {
        "intent": "decide_or_answer",
        "role": "planner",
        "available_tools": {
            "calculator": {
                "description": "Add two integers",
                "args_schema": {
                    "a": "integer",
                    "b": "integer"
                }
            },
            "text_length": {
                "description": "Get length of text",
                "args_schema": {
                    "text": "string"
                }
            }
        },
        "constraints": [
            "Respond ONLY with a raw JSON object.",
            "Do NOT use markdown formatting or triple backticks (```).",
            "Do NOT include any preamble or post-text.",
            "Do not execute tools",
            "Choose tool only if required"
        ],
        "memory": recent_history,
        "data": {
            "current_query": user_input
        }
    }
