import streamlit as st
from model import generate_response

st.set_page_config(page_title="SEA-LION Chatbot", page_icon="🤖")
st.title("🤖 SEA-LION Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ketik pesan…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("Generating…"):
            try:
                response = generate_response(prompt)
            except Exception as e:
                response = f"⚠️ {e}"
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
