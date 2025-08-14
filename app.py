# apps.py
import streamlit as st
from model import generate_response
from io import BytesIO
from PIL import Image
import pytesseract  # OCR ringan
import textract     # untuk PDF/DOCX/TXT

st.set_page_config(page_title="SEA-LION Chatbot", page_icon="🦁")
st.title("🦁 SEA-LION Chatbot (Gemma v3-9B-IT)")

# Simpan riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Upload file section
st.subheader("Upload Contract File (PDF, DOCX, TXT, JPG, PNG)")
uploaded_file = st.file_uploader("Pilih file...", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"])

extracted_text = ""
if uploaded_file:
    file_type = uploaded_file.type
    st.info(f"Memproses file: {uploaded_file.name}")
    if "image" in file_type:
        # OCR image
        image = Image.open(BytesIO(uploaded_file.read()))
        extracted_text = pytesseract.image_to_string(image)
    else:
        # PDF/DOCX/TXT
        uploaded_file.seek(0)
        extracted_text = textract.process(uploaded_file).decode("utf-8")
    
    st.text_area("Extracted Text:", extracted_text, height=200)

# Input user atau hasil ekstrak file sebagai prompt
prompt = st.chat_input("Ketik pesan atau gunakan teks yang diambil dari file...", value=extracted_text)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Menulis..."):
            response = generate_response(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
