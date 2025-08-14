import os
import requests

HF_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
MODEL_NAME = "aisingapore/SEA-LION-v1-3B"

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"HF API Error {response.status_code}: {response.text}")
    return response.json()

def generate_response(prompt: str) -> str:
    output = query({"inputs": prompt, "parameters": {"max_new_tokens": 150}})
    if isinstance(output, list) and "generated_text" in output[0]:
        return output[0]["generated_text"]
    return str(output)
