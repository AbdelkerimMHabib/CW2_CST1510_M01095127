import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from services.ai_assistant import AIAssistant

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    st.switch_page("pages/1_🔐_Login.py")

db_manager = DatabaseManager()
auth_manager = AuthManager(db_manager)
ai_service = AIAssistant()

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
st.title("🤖 AI Assistant")
st.success(f"Welcome, {st.session_state.username}!")

if not ai_service.is_available():
    st.warning("⚠️ AI Assistant is not fully configured.")
    st.info("Please add your OpenAI API key to `.streamlit/secrets.toml`")

# Sidebar controls
with st.sidebar:
    st.title("⚙️ AI Configuration")
    domain = st.selectbox(
        "Select AI Expertise",
        ["General Assistant", "Cybersecurity Expert", "Data Analytics Expert", 
         "IT Operations Expert", "Multi-Domain Intelligence"],
        index=4
    )
    
    system_prompts = {
        "General Assistant": "You are a helpful and knowledgeable assistant.",
        "Cybersecurity Expert": "You are a senior cybersecurity expert.",
        "Data Analytics Expert": "You are a senior data analytics expert.",
        "IT Operations Expert": "You are an IT operations manager.",
        "Multi-Domain Intelligence": "You are a Multi-Domain Security Intelligence Assistant."
    }
    
    model = st.selectbox("AI Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0)
    temperature = st.slider("Creativity", 0.0, 2.0, 0.7, 0.1)

# Main chat interface
st.header("💬 Chat with AI Assistant")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(f"Ask about {domain}...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if ai_service.is_available():
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ai_service.chat_completion(
                    messages=st.session_state.messages,
                    system_prompt=system_prompts[domain],
                    temperature=temperature
                )
                if response:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Failed to get response")
    else:
        with st.chat_message("assistant"):
            st.info("AI Assistant is not configured.")

# Cross-domain analysis
st.header("🔍 Cross-Domain Analysis")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Analyze Security Incidents"):
        incidents = db_manager.fetch_all("SELECT * FROM cyber_incidents LIMIT 3")
        if incidents and ai_service.is_available():
            analysis = ai_service.analyze_security_incidents(incidents, "Comprehensive Analysis")
            st.subheader("Security Analysis")
            st.markdown(analysis[:300] + "..." if len(analysis) > 300 else analysis)
with col2:
    if st.button("Analyze Datasets"):
        datasets = db_manager.fetch_all("SELECT * FROM datasets_metadata LIMIT 3")
        if datasets and ai_service.is_available():
            analysis = ai_service.analyze_datasets(datasets, "Data Quality Assessment")
            st.subheader("Dataset Analysis")
            st.markdown(analysis[:300] + "..." if len(analysis) > 300 else analysis)
with col3:
    if st.button("Analyze IT Tickets"):
        tickets = db_manager.fetch_all("SELECT * FROM it_tickets LIMIT 3")
        if tickets and ai_service.is_available():
            analysis = ai_service.analyze_it_tickets(tickets, "Support Trends")
            st.subheader("Ticket Analysis")
            st.markdown(analysis[:300] + "..." if len(analysis) > 300 else analysis)

# Navigation
st.divider()
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🏠 Home"):
        st.switch_page("Home.py")
with col2:
    if st.button("🛡 Cybersecurity"):
        st.switch_page("pages/2_🛡_Cybersecurity.py")
with col3:
    if st.button("📊 Data Science"):
        st.switch_page("pages/3_📊_Data_Science.py")
with col4:
    if st.button("💻 IT Ops"):
        st.switch_page("pages/4_💻_IT_Operations.py")
with col5:
    if st.button("🔐 Logout", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("pages/1_🔐_Login.py")