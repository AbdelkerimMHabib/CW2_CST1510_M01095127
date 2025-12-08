import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title("🛡 AI Assistant for Multiple Domains")

# Domain selection
domain = st.selectbox("Choose a domain:", ["Cybersecurity", "Data Science", "IT Operations"])

# Initialize session state for messages based on selected domain
if 'messages' not in st.session_state:
    if domain == "Cybersecurity":
        st.session_state.messages = [
            {"role": "system", "content": "You are a cybersecurity expert. Provide technical analysis and actionable recommendations."}
        ]
    elif domain == "Data Science":
        st.session_state.messages = [
            {"role": "system", "content": "You are a data science expert. Help with analysis, visualization, and statistical insights."}
        ]
    elif domain == "IT Operations":
        st.session_state.messages = [
            {"role": "system", "content": "You are an IT operations expert. Help troubleshoot issues, optimize systems, and manage tickets."}
        ]

# Display all previous messages
for message in st.session_state.messages[1:]:  
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input(f"Ask about {domain.lower()}...")
if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call OpenAI API
    completion = client.chat.completions.create(
        model="gpt-4o",  
        messages=st.session_state.messages
    )
    response = completion.choices[0].message.content

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

   
    st.session_state.messages.append({"role": "assistant", "content": response})
