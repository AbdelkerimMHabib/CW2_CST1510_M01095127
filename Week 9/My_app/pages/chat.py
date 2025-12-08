# My_app/pages/chat.py
import streamlit as st
from openai import OpenAI

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("💬 Chat")
client = None
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.warning("OpenAI key not found in secrets. Chat will not function without a key.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

with st.sidebar:
    st.title("Chat Controls")
    st.metric("Messages", max(len(st.session_state.messages)-1, 0))
    if st.button("Clear Chat"):
        st.session_state.messages = [{"role":"system","content":"You are a helpful assistant."}]
        st.experimental_rerun()

# Display messages
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.write(m["content"])

# Input
user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.write(user_input)

    if client is not None:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            ai_text = response.choices[0].message.content
        except Exception as e:
            ai_text = f"Error calling OpenAI: {e}"
    else:
        ai_text = "OpenAI client not configured."

    st.session_state.messages.append({"role":"assistant","content":ai_text})
    with st.chat_message("assistant"):
        st.write(ai_text)
