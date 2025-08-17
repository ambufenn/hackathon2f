import streamlit as st
from openai import OpenAI

SEA_LION_API_KEY = st.secrets.get("SEA_LION_API_KEY")

if not SEA_LION_API_KEY:
    SEA_LION_API_KEY = "dummy"  # sementara biar import tidak error

client = OpenAI(
    api_key=SEA_LION_API_KEY,
    base_url="https://api.sea-lion.ai/v1"
)

MODEL_NAME = "aisingapore/Gemma-SEA-LION-v3-9B-IT"

def generate_response(prompt: str, context: str = "") -> str:
    if SEA_LION_API_KEY == "dummy":
        return "⚠️ API key belum di-set di st.secrets."
    try:
        system_message = (
            "You are a helpful assistant. "
            "If a document is provided, use it to answer the user question. "
            "Document context:\n" + context if context else "You are a helpful assistant."
        )

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ API Error: {e}"
