import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from database.db import DatabaseInitializer

DatabaseInitializer().initialize()
db_manager = DatabaseManager()
auth_manager = AuthManager(db_manager)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "current_user" not in st.session_state:
    st.session_state.current_user = None

if not st.session_state.logged_in:
    st.switch_page("pages/1_🔐_Login.py")

st.set_page_config(page_title="Multi-Domain Intelligence Platform", page_icon="🏠", layout="wide")
st.title("🏠 Multi-Domain Intelligence Platform")
st.success(f"Welcome back, {st.session_state.username}!")

# Platform Overview
st.header("🌐 Platform Overview")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("### 🛡 Cybersecurity")
    if st.button("Go to Cybersecurity", use_container_width=True):
        st.switch_page("pages/2_🛡_Cybersecurity.py")
with col2:
    st.markdown("### 📊 Data Science")
    if st.button("Go to Data Science", use_container_width=True):
        st.switch_page("pages/3_📊_Data_Science.py")
with col3:
    st.markdown("### 💻 IT Operations")
    if st.button("Go to IT Operations", use_container_width=True):
        st.switch_page("pages/4_💻_IT_Operations.py")
with col4:
    st.markdown("### 🤖 AI Assistant")
    if st.button("Go to AI Assistant", use_container_width=True):
        st.switch_page("pages/5_🤖_AI_Assistant.py")

# Quick Statistics
st.divider()
st.header("📈 Quick Statistics")
total_incidents = db_manager.get_table_count("cyber_incidents")
total_datasets = db_manager.get_table_count("datasets_metadata")
total_tickets = db_manager.get_table_count("it_tickets")
total_users = db_manager.get_table_count("users")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Security Incidents", total_incidents)
with col2:
    st.metric("Datasets", total_datasets)
with col3:
    st.metric("IT Tickets", total_tickets)
with col4:
    st.metric("Users", total_users)

# Logout
st.divider()
if st.button("🚪 Logout", type="secondary", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_role = ""
    st.session_state.current_user = None
    st.success("Logged out!")
    st.switch_page("pages/1_🔐_Login.py")