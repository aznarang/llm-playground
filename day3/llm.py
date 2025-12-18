import requests
import os
import time
import json 

HF_URL = "https://router.huggingface.co/v1/chat/completions"
HF_MODEL = "google/gemma-2-2b-it"

def call_ollama(prompt, system, temperature=0.2):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": f"{system}\n\n{prompt}",
        "temperature": temperature,
        "stream": False
    }
    r = requests.post(url, json=payload, timeout=60)
    return r.json()["response"]




def call_llm_planner(system_prompt, mcp_context):
    api_key = os.getenv("HF_API_KEY")
    if not api_key:
        return {"error": "HF_API_KEY missing"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an AI planner.

Context:
{json.dumps(mcp_context, indent=2)}

Decide whether a tool is needed.

Respond ONLY in JSON in one of these formats:

Tool needed:
{{ "tool": "<tool_name>", "args": {{...}} }}

No tool needed:
{{ "tool": "none", "answer": "<text>" }}
"""

    payload = {
        "model": HF_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 300
    }

    response = requests.post(HF_URL, headers=headers, json=payload, timeout=60)

    try:
        return json.loads(response.json()["choices"][0]["message"]["content"])
    except Exception as e:
        return {"error": f"Invalid JSON from model: {e}"}




def call_huggingface(user_prompt, system_prompt):
    api_key = os.getenv("HF_API_KEY")
    if not api_key:
        return "❌ HF_API_KEY not configured"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": HF_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 300
    }

    response = requests.post(HF_URL, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        return f"❌ HTTP {response.status_code}: {response.text[:200]}"

    try:
        data = response.json()
    except Exception:
        return f"⚠️ Non-JSON response: {response.text[:200]}"

    return data["choices"][0]["message"]["content"]
