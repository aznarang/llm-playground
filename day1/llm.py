import requests
import os
import time

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
