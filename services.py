# services.py (versi cepat & hemat GPU/CPU)
import tempfile
from io import BytesIO
from PIL import Image
import streamlit as st
import easyocr
from model import generate_response

# Cegah load OCR berulang
@st.cache_resource
def get_ocr_reader():
    return easyocr.Reader(['en'])

# Cache hasil ekstraksi file
@st.cache_data(show_spinner=False)
def extract_text_from_file(uploaded_file) -> str:
    """Ekstrak teks dari file PDF/DOCX/TXT/IMG dengan optimasi"""
    file_type = uploaded_file.type

    if "image" in file_type:
        reader = get_ocr_reader()
        image = Image.open(BytesIO(uploaded_file.read()))
        result = reader.readtext(image, detail=0)
        return "\n".join(result)

    elif file_type == "application/pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text

    elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        import docx
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file_type == "text/plain":
        return uploaded_file.read().decode("utf-8", errors="ignore")

    # Fallback ke textract kalau format tidak dikenal
    else:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        import textract
        return textract.process(tmp_file_path).decode("utf-8", errors="ignore")


def summarize_text_ai(text: str) -> str:
    """Ringkas teks dengan AI"""
    prompt = f"""
Berikan ringkasan yang jelas dan singkat dari teks dokumen berikut:
{text[:2000]}
Ringkasan sebaiknya fokus pada isi penting dan mengabaikan header/footer.
"""
    return generate_response(prompt)


def detect_risk(text: str) -> list:
    """Deteksi kata kunci risiko"""
    risk_keywords = ["penalty", "liability", "deadline", "fine"]
    return [kw for kw in risk_keywords if kw.lower() in text.lower()]


def smart_suggestions(text: str) -> list:
    """Beri saran cerdas"""
    suggestions = []
    if "deadline" in text.lower():
        suggestions.append("Periksa tanggal tenggat dan buat reminder.")
    if "liability" in text.lower():
        suggestions.append("Pastikan ada klausul proteksi risiko.")
    return suggestions


def generate_insight(text: str, summary: str, risks: list, suggestions: list) -> str:
    """Hasilkan insight tambahan dari AI"""
    prompt_to_model = f"""
Berikut teks dokumen: {text[:1000]}
Ringkasan: {summary}
Risiko terdeteksi: {', '.join(risks) if risks else 'Tidak ada'}
Saran: {', '.join(suggestions) if suggestions else 'Tidak ada'}

Berikan insight tambahan atau smart suggestion berdasarkan ini.
"""
    return generate_response(prompt_to_model)
