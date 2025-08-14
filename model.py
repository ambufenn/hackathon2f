import os
from transformers import pipeline

# Ambil token dari environment (set di Streamlit Secrets)
HF_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

# Nama model — ganti sesuai kebutuhan, pastikan public atau punya akses token
MODEL_NAME = "gpt2"  # contoh model ringan; ubah kalau mau model lain

def load_pipeline():
    try:
        return pipeline(
            "text-generation",
            model=MODEL_NAME,
            use_auth_token=HF_TOKEN if HF_TOKEN else None,
            device_map="auto"
        )
    except OSError as e:
        # Kalau gagal load model, tampilkan error dan hentikan
        raise RuntimeError(
            f"Gagal memuat model '{MODEL_NAME}'. "
            f"Pastikan nama model benar dan token (jika perlu) sudah di-set.\nDetail: {e}"
        )

# Buat pipeline hanya sekali saat import
text_gen = load_pipeline()

def generate_response(prompt: str) -> str:
    result = text_gen(prompt, max_length=200, num_return_sequences=1)
    return result[0]["generated_text"]
