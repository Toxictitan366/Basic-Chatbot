
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 Patham's CHATBOT(SHADOW 1.0)")
st.caption("Powered by Streamlit and Groq")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("API key missing. Please check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI assistant."
                        },
                        *st.session_state.messages
                    ],
                    max_completion_tokens=1024
                )

                answer = response.choices[0].message.content
                st.markdown(answer or "No response generated.")

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer or "No response generated."
            })

        except Exception as e:
            st.error(f"Error: {e}")
