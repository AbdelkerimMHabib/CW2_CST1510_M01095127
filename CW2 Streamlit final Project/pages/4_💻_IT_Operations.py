"""IT Operations and AI Analyzer using OOP"""
import streamlit as st
from services.database_manager import DatabaseManager
from services.ai_assistant import AIAssistant
from models.security_incident import SecurityIncident
from models.dataset import Dataset
from models.it_ticket import ITTicket

# Authentication 
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("pages/1_🔐_Login.py")
    st.stop()

st.set_page_config(page_title="IT Operations & AI Analyzer", page_icon="🔍", layout="wide")
st.title("IT Operations & AI Multi-Table Analyzer")

# Initialize services
db = DatabaseManager()

# Get data and convert to objects
incident_data = db.get_all_incidents()
dataset_data = db.get_all_datasets()
ticket_data = db.get_all_tickets()
user_data = db.get_all_users()

# Convert raw data to model objects
incidents = [SecurityIncident(
    incident_id=data["id"],
    title=data["title"],
    severity=data["severity"],
    status=data["status"],
    date=data["date"]
) for data in incident_data]

datasets = [Dataset(
    dataset_id=data["id"],
    name=data["name"],
    source=data["source"],
    category=data["category"],
    size=data["size"]
) for data in dataset_data]

tickets = [ITTicket(
    ticket_id=data["id"],
    title=data["title"],
    priority=data["priority"],
    status=data["status"],
    created_date=data["created_date"]
) for data in ticket_data]

# Check for OpenAI API key
try:
    if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        ai_available = True
    else:
        openai_api_key = None
        ai_available = False
        st.warning(" OpenAI API key not found in secrets. AI features disabled.")
except:
    openai_api_key = None
    ai_available = False

# Tab for different table analyses
tab1, tab2, tab3, tab4 = st.tabs(["🔒 Cyber Incidents", "📁 Datasets", "IT Tickets", "Users"])

# Incident analysis
with tab1:
    st.subheader("Cyber Incident Analysis")
    
    if not incidents:
        st.info("No incidents to analyze.")
    else:
        #Format incident display list
        incident_list = [f"{inc.get_id()}: {inc.get_title()} ({inc.get_severity()}, {inc.get_status()})" for inc in incidents]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            #Multi-select for incidents
            selected_indices = st.multiselect(
                "Select incidents to analyze",
                options=list(range(len(incidents))),
                format_func=lambda i: incident_list[i],
                max_selections=5
            )
            
            #Choose analysis type
            analysis_type = st.selectbox(
                "Analysis Type",
                ["Comprehensive Analysis", "Root Cause Analysis", "Risk Assessment", 
                 "Mitigation Recommendations", "Trend Analysis"]
            )
            
            # Generate report button
            generate_report = st.button("Generate AI Analysis", type="primary", key="analyze_incidents", disabled=not ai_available)
            
            if not ai_available:
                st.caption("AI features require OpenAI API key in secrets.toml")
        
        with col2:
            #Display selected incidents
            if selected_indices:
                st.write("### Selected Incidents:")
                for idx in selected_indices:
                    incident = incidents[idx]
                    with st.expander(f"{incident.get_title()}"):
                        st.write(f"**ID:** {incident.get_id()}")
                        st.write(f"**Severity:** {incident.get_severity()}")
                        st.write(f"**Status:** {incident.get_status()}")
                        st.write(f"**Date:** {incident.get_date()}")
            
            #Generate AI analysis report
            if generate_report and selected_indices and ai_available:
                with st.spinner("AI is analyzing incidents..."):
                    try:
                        ai = AIAssistant(api_key=openai_api_key)
                        ai.set_system_prompt("You are a senior cybersecurity analyst. Provide detailed, actionable insights.")
                        
                        selected_incidents = [incidents[idx] for idx in selected_indices]
                        
                        incidents_text = "\n\n".join([
                            f"Incident {i+1}:\n"
                            f"- Title: {inc.get_title()}\n"
                            f"- Severity: {inc.get_severity()}\n"
                            f"- Status: {inc.get_status()}\n"
                            f"- Date: {inc.get_date()}"
                            for i, inc in enumerate(selected_incidents)
                        ])
                        
                        prompt = f"""As a cybersecurity expert, analyze the following incidents:

{incidents_text}

Analysis Type: {analysis_type}

Please provide a detailed analysis including:
1. Overall assessment of risks
2. Common patterns or trends
3. Immediate actions if needed
4. Long-term prevention techniques
5. Recommendations for every incident

Format the response with clear sections and bullet points."""
                        
                        ai_output = ai.send_message(prompt)
                        
                        st.subheader("AI Analysis Report")
                        st.markdown(ai_output)
                        
                    except Exception as e:
                        st.error(f"Error generating analysis: {str(e)}")


# Dataset analysis
with tab2:
    st.subheader("Dataset Analysis")
    
    if not datasets:
        st.info("No datasets to analyze.")
    else:
        dataset_list = [f"{ds.get_id()}: {ds.get_name()} ({ds.get_category()}, {ds.get_size()}MB)" for ds in datasets]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_indices = st.multiselect(
                "Select datasets to analyze",
                options=list(range(len(datasets))),
                format_func=lambda i: dataset_list[i],
                max_selections=5
            )
            
            analysis_type = st.selectbox(
                "Analysis Type",
                ["Data Quality Assessment", "Usage Recommendations", 
                 "Security Implications", "Integration Potential", "Value Analysis"],
                key="dataset_analysis_type"
            )
            
            generate_report = st.button("Generate AI Analysis", type="primary", key="analyze_datasets", disabled=not ai_available)
            
            if not ai_available:
                st.caption("AI features require OpenAI API key in secrets.toml")
        
        with col2:
            if selected_indices:
                st.write("### Selected Datasets:")
                for idx in selected_indices:
                    dataset = datasets[idx]
                    with st.expander(f"📊 {dataset.get_name()}"):
                        st.write(f"**Source:** {dataset.get_source()}")
                        st.write(f"**Category:** {dataset.get_category()}")
                        st.write(f"**Size:** {dataset.get_size()} MB")
            
            if generate_report and selected_indices and ai_available:
                with st.spinner("AI is analyzing datasets..."):
                    try:
                        ai = AIAssistant(api_key=openai_api_key)
                        ai.set_system_prompt("You are a data analytics, architecture, and governance expert.")
                        
                        selected_datasets = [datasets[idx] for idx in selected_indices]
                        
                        datasets_text = "\n\n".join([
                            f"Dataset {i+1}:\n"
                            f"- Name: {ds.get_name()}\n"
                            f"- Source: {ds.get_source()}\n"
                            f"- Category: {ds.get_category()}\n"
                            f"- Size: {ds.get_size()}MB"
                            for i, ds in enumerate(selected_datasets)
                        ])
                        
                        prompt = f"""As a data management expert, analyze the following datasets:

{datasets_text}

Analysis Type: {analysis_type}

Provide insights on:
1. Data quality and completeness
2. Potentical cases where they can be used
3. Security and privacy considerations
4. Opportunities for integration
5. Recommendations for data governance

Format with clear sections and actionable insights."""
                        
                        ai_output = ai.send_message(prompt)
                        
                        st.subheader("Dataset Analysis Report")
                        st.markdown(ai_output)
                        
                    except Exception as e:
                        st.error(f"Error generating analysis: {str(e)}")

# Ticket Analysis
with tab3:
    st.subheader("IT Ticket Analysis")
    
    if not tickets:
        st.info("No tickets to analyze.")
    else:
        ticket_list = [f"{t.get_id()}: {t.get_title()} ({t.get_priority()}, {t.get_status()})" for t in tickets]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_indices = st.multiselect(
                "Select tickets to analyze",
                options=list(range(len(tickets))),
                format_func=lambda i: ticket_list[i],
                max_selections=5
            )
            
            analysis_type = st.selectbox(
                "Analysis Type",
                ["Support Trends", "Resolution Analysis", 
                 "Priority Assessment", "Process Improvement", "Resource Allocation"],
                key="ticket_analysis_type"
            )
            
            generate_report = st.button("Generate AI Analysis", type="primary", key="analyze_tickets", disabled=not ai_available)
            
            if not ai_available:
                st.caption("AI features require OpenAI API key in secrets.toml")
        
        with col2:
            if selected_indices:
                st.write("### Selected Tickets:")
                for idx in selected_indices:
                    ticket = tickets[idx]
                    with st.expander(f"{ticket.get_title()}"):
                        st.write(f"**Priority:** {ticket.get_priority()}")
                        st.write(f"**Status:** {ticket.get_status()}")
                        st.write(f"**Created:** {ticket.get_created_date()}")
            
            if generate_report and selected_indices and ai_available:
                with st.spinner("AI is analyzing tickets..."):
                    try:
                        ai = AIAssistant(api_key=openai_api_key)
                        ai.set_system_prompt("You are an IT management expert.")
                        
                        selected_tickets = [tickets[idx] for idx in selected_indices]
                        
                        tickets_text = "\n\n".join([
                            f"Ticket {i+1}:\n"
                            f"- Title: {ticket.get_title()}\n"
                            f"- Priority: {ticket.get_priority()}\n"
                            f"- Status: {ticket.get_status()}\n"
                            f"- Created: {ticket.get_created_date()}"
                            for i, ticket in enumerate(selected_tickets)
                        ])
                        
                        prompt = f"""As an IT service management expert, analyze the following support tickets:

{tickets_text}

Analysis Type: {analysis_type}

Provide analysis covering:
1. Common issue patterns
2. effectiveness of resolutions
3. assessment of priority accuracy
4. Process bottlenecks
5. Recommendations for IT service improvement

Format with clear sections and actionable recommendations."""
                        
                        ai_output = ai.send_message(prompt)
                        
                        st.subheader("Ticket Analysis Report")
                        st.markdown(ai_output)
                        
                    except Exception as e:
                        st.error(f"Error generating analysis: {str(e)}")

# User analysis
with tab4:
    st.subheader("User Analysis")
    
    if not user_data:
        st.info("No users to analyze.")
    else:
        user_list = [f"{r['id']}: {r['username']} ({r['role']})" for r in user_data]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_indices = st.multiselect(
                "Select users to analyze",
                options=list(range(len(user_data))),
                format_func=lambda i: user_list[i],
                max_selections=10
            )
            
            analysis_type = st.selectbox(
                "Analysis Type",
                ["Access Patterns", "Role Analysis", 
                 "Security Assessment", "Usage Trends", "Management Recommendations"],
                key="user_analysis_type"
            )
            
            generate_report = st.button("Generate AI Analysis", type="primary", key="analyze_users", disabled=not ai_available)
            
            if not ai_available:
                st.caption("AI features require OpenAI API key in secrets.toml")
        
        with col2:
            if selected_indices:
                st.write("### Selected Users:")
                for idx in selected_indices:
                    user = user_data[idx]
                    with st.expander(f"{user['username']}"):
                        st.write(f"**Role:** {user['role']}")
                        st.write(f"**Created:** {user.get('created_at', 'N/A')}")
            
            if generate_report and selected_indices and ai_available:
                with st.spinner("AI is analyzing users..."):
                    try:
                        ai = AIAssistant(api_key=openai_api_key)
                        ai.set_system_prompt("You are a cybersecurity expert.")
                        
                        selected_users = [user_data[idx] for idx in selected_indices]
                        
                        users_text = "\n\n".join([
                            f"User {i+1}:\n"
                            f"- Username: {user['username']}\n"
                            f"- Role: {user['role']}\n"
                            f"- Created: {user.get('created_at', 'N/A')}"
                            for i, user in enumerate(selected_users)
                        ])
                        
                        prompt = f"""As a security and user management expert, analyze the following user accounts:

{users_text}

Analysis Type: {analysis_type}

Provide analysis covering:
1. distribution of Roles and appropriate access
2. Access control considerations
3. Effective Security implications
4. User management recommendations
5. Compliance considerations

Format with clear sections and actionable insights."""
                        
                        ai_output = ai.send_message(prompt)
                        
                        st.subheader("User Analysis Report")
                        st.markdown(ai_output)
                        
                    except Exception as e:
                        st.error(f"Error generating analysis: {str(e)}")


# Navigation
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Back to Analytics"):
        st.switch_page("pages/3_📊_Data_Science.py")
with col2:
    if st.button("🏠 Home"):
        st.switch_page("Home.py")
with col3:
    if st.button("💬 AI Assistant ➡️"):
        st.switch_page("pages/5_🤖_AI_Assistant.py")