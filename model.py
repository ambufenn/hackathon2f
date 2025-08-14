import os
from transformers import pipeline, AutoTokenizer

# Ambil token dari environment (set di Streamlit Secrets)
HF_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

# Nama model SEA-LION
MODEL_NAME = "panji-pansear/sea-lion-7b-instruct"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    use_auth_token=HF_TOKEN if HF_TOKEN else None
)

# Set pad_token kalau belum ada
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def load_pipeline():
    try:
        return pipeline(
            "text-generation",
            model=MODEL_NAME,
            tokenizer=tokenizer,
            use_auth_token=HF_TOKEN if HF_TOKEN else None,
            device_map="auto"
        )
    except OSError as e:
        raise RuntimeError(
            f"Gagal memuat model '{MODEL_NAME}'. "
            f"Pastikan nama model benar, token valid, dan perangkat mendukung.\nDetail: {e}"
        )

# Pipeline dibuat sekali
text_gen = load_pipeline()

def generate_response(prompt: str) -> str:
    result = text_gen(
        prompt,
        max_new_tokens=200,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.pad_token_id
    )
    return result[0]["generated_text"]
