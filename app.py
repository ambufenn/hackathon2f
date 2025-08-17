import streamlit as st
from services import extract_text_from_file, summarize_text_ai, detect_risk, smart_suggestions, generate_insight
from model import generate_response

# ========== Custom CSS ========== #
st.markdown("""
    <style>
    body {
      background: linear-gradient(135deg, #f8fbff, #eef3f9);
      font-family: "Inter", sans-serif;
      color: #2c3e50;
    }
    .main {
      padding: 2rem;
    }
    .upload-section {
      background: #ffffff;
      border-radius: 16px;
      padding: 32px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      text-align: center;
      transition: 0.3s ease;
    }
    .upload-section:hover {
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
    .upload-title {
      font-size: 1.4rem;
      font-weight: 600;
      margin-bottom: 16px;
      color: #2c3e50;
    }
    .uploadedFile {
      border: 2px dashed #4a90e2 !important;
      border-radius: 12px !important;
      padding: 10px !important;
      background: #f9fbff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ====== PAGE CONFIG ======
st.set_page_config(page_title="SERENADE DATA Chatbot", page_icon="🦁", layout="wide")

# ====== APP TITLE ======
st.title("🦁 SEA-LION Chatbot (Gemma v3-9B-IT)")

# ====== SESSION STATE ======
if "messages" not in st.session_state:
    st.session_state.messages = []

# ====== SHOW CHAT HISTORY ======
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ====== UPLOAD DOCUMENT ======
st.markdown("### 📂 Upload Your Document")
uploaded_file = st.file_uploader("Choose file...", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"])

extracted_text = ""
if uploaded_file:
    try:
        with st.spinner("Extraction text..."):
            extracted_text = extract_text_from_file(uploaded_file)
        st.text_area("Extracted Text:", extracted_text, height=200)

        summary = summarize_text_ai(extracted_text)
        st.write("Ringkasan:", summary)

        risks = detect_risk(extracted_text)
        st.write("Risiko:", risks if risks else "Tidak ada")

        suggestions = smart_suggestions(extracted_text)
        st.write("Saran:", suggestions if suggestions else "Tidak ada")

        insight = generate_insight(extracted_text, summary, risks, suggestions)
        st.subheader("Insight SEA-LION")
        st.write(insight)

    except Exception as e:
        st.error(f"Error: {e}")

# ====== CHAT INPUT ======
prompt = st.chat_input("Ask heren...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Menulis..."):
            response = generate_response(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
