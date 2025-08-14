# model.py
from openai import OpenAI
import streamlit as st

MODEL_NAME = "aisingapore/Gemma-SEA-LION-v3-9B-IT"

def get_client():
    if "SEA_LION_API_KEY" not in st.secrets:
        st.error("⚠️ SEA_LION_API_KEY belum diset di st.secrets!")
        return None
    api_key = st.secrets["SEA_LION_API_KEY"]
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.sea-lion.ai/v1"
    )
    return client

def generate_response(prompt: str) -> str:
    client = get_client()
    if not client:
        return "⚠️ API key tidak tersedia."
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ API Error: {e}"
