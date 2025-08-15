import streamlit as st
from services import extract_text_from_file, summarize_text_ai, detect_risk, smart_suggestions, generate_insight
from model import generate_response

st.set_page_config(page_title="SEA-LION Chatbot", page_icon="🦁")
st.title("🦁 SEA-LION Chatbot (Gemma v3-9B-IT)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Upload file
st.subheader("Upload File")
uploaded_file = st.file_uploader("Pilih file...", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"])

extracted_text = ""
if uploaded_file:
    try:
        with st.spinner("Ekstraksi teks..."):
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

# Chat manual
prompt = st.chat_input("Ketik pesan...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Menulis..."):
            response = generate_response(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
