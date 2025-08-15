import streamlit as st
import requests

st.set_page_config(page_title="SEA-LION Chatbot", page_icon="🦁")
st.title("🦁 SEA-LION Chatbot (Gemma v3-9B-IT)")

API_BASE = "http://localhost:8000"  # ganti dengan URL FastAPI kamu

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Upload file & proses via endpoint ---
st.subheader("Upload File")
uploaded_file = st.file_uploader(
    "Pilih file...", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"]
)

if uploaded_file:
    try:
        with st.spinner("Mengirim file ke server..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            resp = requests.post(f"{API_BASE}/process_file", files=files)
            resp.raise_for_status()
            data = resp.json()

        st.text_area("Extracted Text:", data["text"], height=200)
        st.write("Ringkasan:", data["summary"])
        st.write("Risiko:", data["risks"] if data["risks"] else "Tidak ada")
        st.write("Saran:", data["suggestions"] if data["suggestions"] else "Tidak ada")
        st.subheader("Insight SEA-LION")
        st.write(data["insight"])

    except Exception as e:
        st.error(f"Error: {e}")

# --- Chat manual via endpoint ---
prompt = st.chat_input("Ketik pesan...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        with st.chat_message("assistant"):
            with st.spinner("Menulis..."):
                resp = requests.post(f"{API_BASE}/chat", json={"prompt": prompt})
                resp.raise_for_status()
                response = resp.json().get("response", "⚠️ Tidak ada balasan")
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"Error: {e}")
