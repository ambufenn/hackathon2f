
import os
import transformers
import torch

HF_TOKEN = os.getenv("HF_TOKEN")
model_id = "aisingapore/Llama-SEA-LION-v3.5-8B-R"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    use_auth_token=HF_TOKEN,  # pakai token dari environment variable
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

def generate_response(prompt, max_new_tokens=256):
    
    outputs = pipeline(prompt, max_new_tokens=max_new_tokens)
    return outputs[0]["generated_text"]
