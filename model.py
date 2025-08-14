import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

HF_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
MODEL_NAME = "aisingapore/SEA-LION-v1-3B"

def load_model():
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            use_auth_token=HF_TOKEN
        )
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            use_auth_token=HF_TOKEN,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        return tokenizer, model
    except Exception as e:
        raise RuntimeError(f"Gagal load model {MODEL_NAME}: {e}")

tokenizer, model = load_model()

def generate_response(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=150)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
