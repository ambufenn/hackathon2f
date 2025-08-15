# services.py
import tempfile
from io import BytesIO
from PIL import Image
import textract
import easyocr
from model import generate_response

def extract_text_from_file(uploaded_file) -> str:
    """Ekstrak teks dari file PDF/DOCX/TXT/IMG"""
    file_type = uploaded_file.type
    if "image" in file_type:
        reader = easyocr.Reader(['en'])
        image = Image.open(BytesIO(uploaded_file.read()))
        result = reader.readtext(image, detail=0)
        return "\n".join(result)
    else:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
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
