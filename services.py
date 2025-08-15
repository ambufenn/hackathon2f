# services.py
import tempfile
from io import BytesIO
from PIL import Image
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import easyocr
from model import generate_response

app = FastAPI()

# --- OCR Reader Singleton ---
ocr_reader = easyocr.Reader(['en'])

# --- Helper Functions ---
def extract_text_from_file(uploaded_file: UploadFile) -> str:
    """Ekstrak teks dari file PDF/DOCX/TXT/IMG dengan optimasi"""
    file_type = uploaded_file.content_type

    if "image" in file_type:
        image = Image.open(BytesIO(uploaded_file.file.read()))
        result = ocr_reader.readtext(image, detail=0)
        return "\n".join(result)

    elif file_type == "application/pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(uploaded_file.file)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text

    elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        import docx
        doc = docx.Document(uploaded_file.file)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file_type == "text/plain":
        return uploaded_file.file.read().decode("utf-8", errors="ignore")

    # Fallback ke textract
    else:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.file.read())
            tmp_file_path = tmp_file.name
        import textract
        return textract.process(tmp_file_path).decode("utf-8", errors="ignore")


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


def summarize_text_ai(text: str) -> str:
    prompt = f"""
Berikan ringkasan yang jelas dan singkat dari teks dokumen berikut:
{text[:2000]}
Ringkasan sebaiknya fokus pada isi penting dan mengabaikan header/footer.
"""
    return generate_response(prompt)


def generate_insight(text: str, summary: str, risks: list, suggestions: list) -> str:
    prompt_to_model = f"""
Berikut teks dokumen: {text[:1000]}
Ringkasan: {summary}
Risiko terdeteksi: {', '.join(risks) if risks else 'Tidak ada'}
Saran: {', '.join(suggestions) if suggestions else 'Tidak ada'}

Berikan insight tambahan atau smart suggestion berdasarkan ini.
"""
    return generate_response(prompt_to_model)


# --- FastAPI Endpoints ---

@app.post("/process_file")
async def process_file(file: UploadFile = File(...)):
    """Endpoint untuk upload file dan ekstrak + summary + risks + suggestion + insight"""
    try:
        text = extract_text_from_file(file)
        summary = summarize_text_ai(text)
        risks = detect_risk(text)
        suggestions = smart_suggestions(text)
        insight = generate_insight(text, summary, risks, suggestions)

        return {
            "text": text,
            "summary": summary,
            "risks": risks,
            "suggestions": suggestions,
            "insight": insight
        }

# Optional: health check
@app.get("/health")
async def health():
    return {"status": "ok"}
