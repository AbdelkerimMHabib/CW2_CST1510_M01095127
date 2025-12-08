import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

with st.sidebar:
    st.title("💬 Chat Controls")

    # Show message count
    message_count = len(st.session_state.get("messages", [])) - 1
    st.metric("Messages", message_count)

    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        st.experimental_rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    # Display user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    ai_message = response.choices[0].message.content

    # Display AI response
    with st.chat_message("assistant"):
        st.write(ai_message)

    # Save AI response to session state
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
