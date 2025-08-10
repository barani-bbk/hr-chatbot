import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

st.set_page_config(page_title="HR Chatbot", page_icon=":material/smart_toy:", layout="centered")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.title("HR Chatbot")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if query := st.chat_input("Ask about employees, skills, availability..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post(API_URL, json={"query": query})
                print(res)
                if res.ok:
                    data = res.json()
                    response_text = f"**Response:**\n\n{data.get('response', 'No response returned.')}"
                else:
                    response_text = "_Failed to fetch a proper response from the server._"
            except Exception as ex:
                response_text = f"⚠️ Error: {ex}"

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
