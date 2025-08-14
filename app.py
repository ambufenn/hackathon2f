import streamlit as st
from model import generate_response
from io import BytesIO
import textract
from PIL import Image
import easyocr
import tempfile

st.set_page_config(page_title="SEA-LION Chatbot", page_icon="🦁")
st.title("🦁 SEA-LION Chatbot (Gemma v3-9B-IT)")

# ===== Fungsi Analisis =====
def summarize_text_ai(text: str) -> str:
    prompt = f"""
Berikan ringkasan yang jelas dan singkat dari teks dokumen berikut:
{text[:2000]}  # batasi supaya tidak terlalu panjang
Ringkasan sebaiknya fokus pada isi penting dan mengabaikan header/footer.
"""
    return generate_response(prompt)

def detect_risk(text: str) -> list:
    risk_keywords = ["penalty", "liability", "deadline", "fine"]
    return [kw for kw in risk_keywords if kw.lower() in text.lower()]

def smart_suggestions(text: str) -> list:
    suggestions = []
    if "deadline" in text.lower():
        suggestions.append("Periksa tanggal tenggat dan buat reminder.")
    if "liability" in text.lower():
        suggestions.append("Pastikan ada klausul proteksi risiko.")
    return suggestions
# ===============================

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
    try:
        if "image" in file_type:
            # OCR dengan easyocr
            reader = easyocr.Reader(['en'])
            image = Image.open(BytesIO(uploaded_file.read()))
            result = reader.readtext(image, detail=0)
            extracted_text = "\n".join(result)
        else:
            # Simpan file sementara untuk textract
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            extracted_text = textract.process(tmp_file_path).decode("utf-8", errors="ignore")

        st.text_area("Extracted Text:", extracted_text, height=200)

        # ===== Analisis tambahan =====
        analysis = summarize_text_ai(extracted_text)  # pakai AI
        risks = detect_risk(extracted_text)
        suggestions = smart_suggestions(extracted_text)

        st.subheader("Summary / Risk / Suggestions")
        st.write("Ringkasan:", analysis)
        st.write("Risiko terdeteksi:", risks if risks else "Tidak ada")
        st.write("Saran:", suggestions if suggestions else "Tidak ada")

        # ===== Gabungkan ke prompt SEA-LION =====
        prompt_to_model = f"""
Berikut teks dokumen: {extracted_text[:1000]}
Ringkasan: {analysis}
Risiko terdeteksi: {', '.join(risks) if risks else 'Tidak ada'}
Saran: {', '.join(suggestions) if suggestions else 'Tidak ada'}

Berikan insight tambahan atau smart suggestion berdasarkan ini.
"""
        response = generate_response(prompt_to_model)

        st.subheader("SEA-LION Response")
        st.write(response)

    except Exception as e:
        st.error(f"Gagal mengekstrak teks: {e}")

# Input user manual
prompt = st.chat_input("Ketik pesan atau gunakan teks dari file...")

# Tombol pakai teks file
if extracted_text and st.button("Gunakan teks dari file"):
    prompt = extracted_text

# Proses chat manual
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Menulis..."):
            response = generate_response(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
