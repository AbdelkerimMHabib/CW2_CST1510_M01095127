import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from services.ai_assistant import AIAssistant
from services.data_service import DataService
from models.it_ticket import ITTicket

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    st.switch_page("pages/1_🔐_Login.py")

db_manager = DatabaseManager()
auth_manager = AuthManager(db_manager)
ai_assistant = AIAssistant()
data_service = DataService(db_manager)

st.set_page_config(page_title="IT Operations", page_icon="💻", layout="wide")
st.title("💻 IT Operations Dashboard")
st.success(f"Welcome, {st.session_state.username}!")

# Section 1: Overview
st.header("🎫 Ticket Overview")
stats = data_service.get_statistics()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Tickets", stats["tickets"]["total"])
with col2:
    st.metric("Open Tickets", stats["tickets"]["open"])
with col3:
    high_priority = len(db_manager.fetch_all(
        "SELECT id FROM it_tickets WHERE priority IN ('High', 'Critical')"
    ))
    st.metric("High Priority", high_priority)
with col4:
    closed = stats["tickets"]["total"] - stats["tickets"]["open"]
    st.metric("Closed Tickets", closed)

# Section 2: List Tickets
st.header("📋 IT Tickets")
tickets = data_service.get_all_tickets()
if tickets:
    ticket_data = []
    for ticket in tickets:
        ticket_data.append({
            "ID": ticket.get_id(),
            "Title": ticket.get_title(),
            "Priority": ticket.get_priority(),
            "Status": ticket.get_status(),
            "Created Date": ticket.get_created_date(),
        })
    df = pd.DataFrame(ticket_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No tickets in the database.")

# Section 3: Visualizations
if tickets:
    st.header("📊 Ticket Analytics")
    tab1, tab2 = st.tabs(["Priority Distribution", "Status Overview"])
    with tab1:
        priority_counts = df['Priority'].value_counts().reset_index()
        fig1 = px.pie(priority_counts, values='count', names='Priority', title='Tickets by Priority')
        st.plotly_chart(fig1, use_container_width=True)
    with tab2:
        status_counts = df['Status'].value_counts().reset_index()
        fig2 = px.bar(status_counts, x='Status', y='count', color='Status', title='Tickets by Status')
        st.plotly_chart(fig2, use_container_width=True)

# ============ AI ANALYZER INTEGRATION SECTION ============
st.header("🤖 AI Ticket Analyzer")

if tickets:
    selected_indices = st.multiselect(
        "Select tickets to analyze",
        options=list(range(len(tickets))),
        format_func=lambda i: f"{tickets[i].get_id()}: {tickets[i].get_title()}",
        max_selections=5
    )
    
    analysis_type = st.selectbox(
        "Analysis Type",
        ["Support Trends", "Resolution Analysis", 
         "Priority Assessment", "Process Improvement", "Resource Allocation"]
    )
    
    if st.button("Generate AI Analysis", type="primary"):
        if not selected_indices:
            st.warning("Please select tickets to analyze.")
        else:
            selected_ticket_data = []
            for idx in selected_indices:
                ticket = tickets[idx]
                selected_ticket_data.append({
                    "title": ticket.get_title(),
                    "priority": ticket.get_priority(),
                    "status": ticket.get_status(),
                    "created_date": ticket.get_created_date()
                })
            
            with st.spinner("🤖 AI is analyzing tickets..."):
                analysis = ai_assistant.analyze_it_tickets(selected_ticket_data, analysis_type)
                st.subheader("📋 AI Analysis Report")
                st.markdown(analysis)
                
                report_content = f"IT Ticket Analysis Report\n\n{analysis}"
                st.download_button(
                    label="📥 Download Report",
                    data=report_content,
                    file_name=f"ticket_analysis_{len(selected_indices)}_tickets.txt",
                    mime="text/plain"
                )
else:
    st.info("No tickets available for analysis.")

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
    if st.button("🤖 AI Assistant"):
        st.switch_page("pages/5_🤖_AI_Assistant.py")
with col5:
    if st.button("🔐 Logout", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("pages/1_🔐_Login.py")