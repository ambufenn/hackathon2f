import os
from openai import OpenAI

# Ambil API key dari environment variable atau st.secrets
SEA_LION_API_KEY = os.environ.get("SEALION_API_KEY")

# Inisialisasi client OpenAI-style
client = OpenAI(
    api_key=SEA_LION_API_KEY,
    base_url="https://api.sea-lion.ai/v1"
)

MODEL_NAME = "aisingapore/Gemma-SEA-LION-v3-9B-IT"

def generate_response(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ API Error: {e}"
