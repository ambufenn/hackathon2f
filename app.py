import streamlit as st
from model import generate_response
from io import BytesIO
import textract
from PIL import Image
import easyocr

st.set_page_config(page_title="SEA-LION Chatbot", page_icon="🦁")
st.title("🦁 SEA-LION Chatbot (Gemma v3-9B-IT)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Upload file
st.subheader("Upload File (PDF, DOCX, TXT, JPG, PNG, JPEG)")
uploaded_file = st.file_uploader("Pilih file...", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"])

extracted_text = ""
if uploaded_file:
    st.info(f"Memproses file: {uploaded_file.name}")
    file_type = uploaded_file.type
    uploaded_file.seek(0)
    try:
        if "image" in file_type:
            # OCR dengan easyocr
            reader = easyocr.Reader(['en'])
            image = Image.open(BytesIO(uploaded_file.read()))
            result = reader.readtext(image, detail=0)
            extracted_text = "\n".join(result)
        else:
            extracted_text = textract.process(uploaded_file).decode("utf-8")
        st.text_area("Extracted Text:", extracted_text, height=200)
    except Exception as e:
        st.error(f"Gagal mengekstrak teks: {e}")

# Input user
prompt = st.chat_input("Ketik pesan atau gunakan teks dari file...")

# Tombol pakai teks file
if extracted_text and st.button("Gunakan teks dari file"):
    prompt = extracted_text

# Proses chat
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Menulis..."):
            response = generate_response(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
