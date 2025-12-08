import streamlit as st
import pandas as pd
import datetime
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from services.ai_assistant import AIAssistant
from services.data_service import DataService
from models.security_incident import SecurityIncident

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    st.switch_page("pages/1_🔐_Login.py")

db_manager = DatabaseManager()
auth_manager = AuthManager(db_manager)
ai_assistant = AIAssistant()
data_service = DataService(db_manager)

st.set_page_config(page_title="Cybersecurity", page_icon="🛡", layout="wide")
st.title("🛡 Cybersecurity Dashboard")
st.success(f"Welcome, {st.session_state.username}!")

# Section 1: Overview
st.header("📈 Incident Overview")
stats = data_service.get_statistics()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Incidents", stats["incidents"]["total"])
with col2:
    st.metric("Open Incidents", stats["incidents"]["open"])
with col3:
    critical = len(db_manager.fetch_all("SELECT id FROM cyber_incidents WHERE severity = 'Critical'"))
    st.metric("Critical Incidents", critical)
with col4:
    closed = stats["incidents"]["total"] - stats["incidents"]["open"]
    st.metric("Closed Incidents", closed)

# Section 2: List Incidents
st.header("🔒 Security Incidents")
incidents = data_service.get_all_incidents()
if incidents:
    incident_data = []
    for incident in incidents:
        incident_data.append({
            "ID": incident.get_id(),
            "Title": incident.get_title(),
            "Severity": incident.get_severity(),
            "Status": incident.get_status(),
            "Date": incident.get_date(),
        })
    df = pd.DataFrame(incident_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No incidents in the database.")

# Section 3: CRUD Operations
tab1, tab2, tab3 = st.tabs(["➕ Add Incident", "✏️ Edit Incident", "🗑️ Delete Incident"])
with tab1:
    with st.form("add_incident_form"):
        title = st.text_input("Incident Title*", placeholder="e.g., Phishing attack detected")
        severity = st.selectbox("Severity*", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status*", ["open", "in progress", "closed", "resolved"])
        date = st.date_input("Date*", value=datetime.date.today())
        if st.form_submit_button("Add Incident"):
            if title:
                data_service.add_incident(title, severity, status, date.isoformat())
                st.success("✅ Incident added!")
                st.rerun()

# ============ AI ANALYZER INTEGRATION SECTION ============
st.header("🤖 AI Incident Analyzer")

if incidents:
    selected_indices = st.multiselect(
        "Select incidents to analyze",
        options=list(range(len(incidents))),
        format_func=lambda i: f"{incidents[i].get_id()}: {incidents[i].get_title()}",
        max_selections=5
    )
    
    analysis_type = st.selectbox(
        "Analysis Type",
        ["Comprehensive Analysis", "Root Cause Analysis", "Risk Assessment", 
         "Mitigation Recommendations", "Trend Analysis"]
    )
    
    if st.button("Generate AI Analysis", type="primary"):
        if not selected_indices:
            st.warning("Please select incidents to analyze.")
        else:
            selected_incident_data = []
            for idx in selected_indices:
                incident = incidents[idx]
                selected_incident_data.append({
                    "title": incident.get_title(),
                    "severity": incident.get_severity(),
                    "status": incident.get_status(),
                    "date": incident.get_date()
                })
            
            with st.spinner("🤖 AI is analyzing incidents..."):
                analysis = ai_assistant.analyze_security_incidents(selected_incident_data, analysis_type)
                st.subheader("📋 AI Analysis Report")
                st.markdown(analysis)
                
                report_content = f"Cybersecurity Incident Analysis Report\n\n{analysis}"
                st.download_button(
                    label="📥 Download Report",
                    data=report_content,
                    file_name=f"incident_analysis_{len(selected_indices)}_incidents.txt",
                    mime="text/plain"
                )
else:
    st.info("No incidents available for analysis.")

# Navigation
st.divider()
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🏠 Home"):
        st.switch_page("Home.py")
with col2:
    if st.button("📊 Data Science"):
        st.switch_page("pages/3_📊_Data_Science.py")
with col3:
    if st.button("💻 IT Ops"):
        st.switch_page("pages/4_💻_IT_Operations.py")
with col4:
    if st.button("🤖 AI Assistant"):
        st.switch_page("pages/5_🤖_AI_Assistant.py")
with col5:
    if st.button("🔐 Logout", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("pages/1_🔐_Login.py")