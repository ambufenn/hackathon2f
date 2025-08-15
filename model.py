# model.py
import os
from openai import OpenAI
from fastapi import FastAPI, Request
from pydantic import BaseModel

# --- Setup API Key ---
SEA_LION_API_KEY = os.getenv("SEA_LION_API_KEY", "dummy")

client = OpenAI(
    api_key=SEA_LION_API_KEY,
    base_url="https://api.sea-lion.ai/v1"
)

MODEL_NAME = "aisingapore/Gemma-SEA-LION-v3-9B-IT"

# --- FastAPI App ---
app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    prompt = req.message
    if SEA_LION_API_KEY == "dummy":
        return {"response": "⚠️ API key belum di-set."}
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        response_text = completion.choices[0].message.content
        return {"response": response_text}
    except Exception as e:
        return {"response": f"⚠️ API Error: {e}"}
