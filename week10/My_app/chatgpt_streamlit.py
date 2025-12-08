import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize message history with a system message
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a cybersecurity expert. Format: Clear, structured responses."
        }
    ]

st.title("Cybersecurity Chatbot")


for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Ask about cybersecurity...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # OpenAI API call
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages
    )

    # Extract assistant response
    response = completion.choices[0].message.content

    # Display response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
