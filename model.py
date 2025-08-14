import os
import requests
import streamlit as st

# Ambil token dari secrets
HF_TOKEN = st.secrets["HUGGINGFACEHUB_API_TOKEN"]

# Nama model SEA-LION
MODEL_NAME = ""aisingapore/Llama-SEA-LION-v3.5-8B-R""

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload: dict) -> dict:
    """Kirim request ke Hugging Face Inference API"""
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"API Error {response.status_code}: {response.text}")
    return response.json()

def generate_response(prompt: str) -> str:
    """Generate respons dari SEA-LION"""
    output = query({
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "top_p": 0.9
        }
    })
    # Output dari HF API biasanya list of dict
    if isinstance(output, list) and "generated_text" in output[0]:
        return output[0]["generated_text"]
    return str(output)
