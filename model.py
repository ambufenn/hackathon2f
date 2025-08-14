import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

HF_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
MODEL_NAME = "aisingapore/Llama-SEA-LION-v3.5-8B-R"

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
    except OSError as e:
        raise RuntimeError(
            f"Gagal memuat model '{MODEL_NAME}'. "
            f"Periksa token dan pastikan model tersedia.\nDetail: {e}"
        )

tokenizer, model = load_model()

def generate_response(prompt: str) -> str:
    messages = [
        {"role": "user", "content": prompt}
    ]
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    ).to(model.device)

    outputs = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
