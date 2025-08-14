import streamlit as st
from model import generate_response

st.set_page_config(page_title="SEA-LION Chatbot", page_icon="🤖")
st.title("🤖 SEA-LION Chatbot")

# Simpan riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input user
if prompt := st.chat_input("Ketik pesan..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Menulis..."):
            response = generate_response(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
