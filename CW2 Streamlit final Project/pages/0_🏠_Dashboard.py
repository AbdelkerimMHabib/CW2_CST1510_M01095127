#Dashboard Page for Multi-Domain Intelligence Application
"""Unified Multi-Domain Dashboard"""

#Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from services.database_manager import DatabaseManager
from services.ai_assistant import AIAssistant
from models.security_incident import SecurityIncident
from models.dataset import Dataset
from models.it_ticket import ITTicket

# Authentication check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("pages/1_🔐_Login.py")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Multi-Domain Dashboard",
    page_icon="🏠",
    layout="wide"
)

# Title with user info
st.title("🏠 Welcome to Aizen! Multi-Domain Intelligence Dashboard")
st.markdown(f"**Welcome, {st.session_state.username}!** | **Role:** {st.session_state.user_role}")
st.markdown("---")

# Initialize important services
db = DatabaseManager()

# Check for OpenAI API key
try:
    if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        ai_available = True
    else:
        openai_api_key = None
        ai_available = False
except:
    openai_api_key = None
    ai_available = False

# Get all data function
def load_all_data():
    """Load all data from database"""
    incident_data = db.get_all_incidents()
    dataset_data = db.get_all_datasets()
    ticket_data = db.get_all_tickets()
    
    # Convert to objects
    incidents = []
    for data in incident_data:
        incidents.append(SecurityIncident(
            incident_id=data["id"],
            title=data["title"],
            severity=data["severity"],
            status=data["status"],
            date=data["date"]
        ))
    
    datasets = []
    for data in dataset_data:
        datasets.append(Dataset(
            dataset_id=data["id"],
            name=data["name"],
            source=data["source"],
            category=data["category"],
            size=data["size"]
        ))
    
    tickets = []
    for data in ticket_data:
        tickets.append(ITTicket(
            ticket_id=data["id"],
            title=data["title"],
            priority=data["priority"],
            status=data["status"],
            created_date=data["created_date"]
        ))
    
    return incidents, datasets, tickets

# Load the data
incidents, datasets, tickets = load_all_data()

#Overview 
st.header("📊 Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Cyber Incidents",
        len(incidents),
        f"{len([i for i in incidents if i.get_status() in ['open', 'in progress']])} open"
    )

with col2:
    st.metric(
        "Datasets",
        len(datasets),
        f"{sum([d.get_size() for d in datasets]):,} MB" if datasets else "0 MB"
    )

with col3:
    st.metric(
        "IT Tickets",
        len(tickets),
        f"{len([t for t in tickets if t.get_status() in ['open', 'in progress']])} open"
    )

with col4:
    try:
        users = db.get_all_users()
        st.metric("Users", len(users))
    except:
        st.metric("Users", 0)

st.markdown("---")

#Visualization and analytics
st.header("📈 Visualizations")

viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    # Incident Severity Distribution
    if incidents:
        severity_counts = {}
        for inc in incidents:
            severity = inc.get_severity()
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        if severity_counts:
            fig = px.pie(
                values=list(severity_counts.values()),
                names=list(severity_counts.keys()),
                title="Incident Severity Distribution",
                color=list(severity_counts.keys()),
                color_discrete_map={
                    'Critical': 'red',
                    'High': 'orange',
                    'Medium': 'yellow',
                    'Low': 'green'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No incident severity data")
    else:
        st.info("No incidents to visualize")

with viz_col2:
    # Ticket Priority Distribution
    if tickets:
        priority_counts = {}
        for ticket in tickets:
            priority = ticket.get_priority()
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        if priority_counts:
            fig = px.pie(
                values=list(priority_counts.values()),
                names=list(priority_counts.keys()),
                title="Ticket Priority Distribution",
                color=list(priority_counts.keys()),
                color_discrete_map={
                    'Critical': 'red',
                    'High': 'orange',
                    'Medium': 'yellow',
                    'Low': 'green'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No ticket priority data")
    else:
        st.info("No tickets to visualize")

# Dataset Size Distribution
if datasets:
    dataset_names = [d.get_name()[:20] + "..." if len(d.get_name()) > 20 else d.get_name() for d in datasets]
    dataset_sizes = [d.get_size() for d in datasets]
    
    fig = px.bar(
        x=dataset_names,
        y=dataset_sizes,
        title="Dataset Sizes (MB)",
        labels={'x': 'Dataset', 'y': 'Size (MB)'},
        color=dataset_sizes,
        color_continuous_scale='Blues'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

#AI analyzer
st.header("AI Analyzer & Recommendations")

if not ai_available:
    st.warning("OpenAI API key not working")
    st.info("Add API Key")
else:
    # Domain selection for AI analysis
    analysis_domain = st.selectbox(
        "Select Domain for AI Analysis",
        ["Cyber Incidents", "Datasets", "IT Tickets", "Cross-Domain Analysis"],
        key="ai_domain_select"
    )
    
    # Quick analysis options
    analysis_type = st.selectbox(
        "Analysis Type",
        [
            "Assessing risks",
            "Analyse trends", 
            "Recommendations to improve",
            "Anomaly Detection",
            "Comprehensive Review"
        ],
        key="ai_analysis_type"
    )
    
    # Analysis scope
    scope = st.radio(
        "Analysis Scope",
        ["All Items", "Critical/High Priority Only"],
        horizontal=True
    )
    
    if st.button("Generate AI Analysis", type="primary", use_container_width=True):
        with st.spinner("AI is analyzing data..."):
            try:
                ai = AIAssistant(api_key=openai_api_key)
                
                # Prepare data based on domain
                analysis_data = ""
                
                if analysis_domain == "Cyber Incidents":
                    ai.set_system_prompt("You are a senior cybersecurity analyst.")
                    filtered_incidents = incidents
                    
                    if scope == "Critical/High Priority Only":
                        filtered_incidents = [i for i in incidents 
                                            if i.get_severity() in ["Critical", "High"]]
                    
                    analysis_data = "\n".join([
                        f"{i+1}. {inc.get_title()} | Severity: {inc.get_severity()} | Status: {inc.get_status()} | Date: {inc.get_date()}"
                        for i, inc in enumerate(filtered_incidents)
                    ])
                
                elif analysis_domain == "Datasets":
                    ai.set_system_prompt("You are a data management and governance expert.")
                    filtered_datasets = datasets
                    
                    if scope == "Critical/High Priority Only":
                        filtered_datasets = [d for d in datasets if d.get_size() > 1000]  
                    
                    analysis_data = "\n".join([
                        f"{i+1}. {ds.get_name()} | Source: {ds.get_source()} | Category: {ds.get_category()} | Size: {ds.get_size()}MB"
                        for i, ds in enumerate(filtered_datasets)
                    ])
                
                elif analysis_domain == "IT Tickets":
                    ai.set_system_prompt("You are an IT service management expert.")
                    filtered_tickets = tickets
                    
                    if scope == "Critical/High Priority Only":
                        filtered_tickets = [t for t in tickets 
                                          if t.get_priority() in ["Critical", "High"]]
                    
                    analysis_data = "\n".join([
                        f"{i+1}. {t.get_title()} | Priority: {t.get_priority()} | Status: {t.get_status()} | Created: {t.get_created_date()}"
                        for i, t in enumerate(filtered_tickets)
                    ])
                
                else:  # Cross-Domain Analysis
                    ai.set_system_prompt("You are a multi-domain intelligence analyst expert in cybersecurity, data, and IT operations.")
                    
                    inc_summary = f"Incidents ({len(incidents)}): " + ", ".join([f"{i.get_severity()}:{i.get_status()}" for i in incidents[:3]])
                    ds_summary = f"Datasets ({len(datasets)}): " + ", ".join([f"{d.get_category()}:{d.get_size()}MB" for d in datasets[:3]])
                    tk_summary = f"Tickets ({len(tickets)}): " + ", ".join([f"{t.get_priority()}:{t.get_status()}" for t in tickets[:3]])
                    
                    analysis_data = f"Cross-Domain Summary:\n- {inc_summary}\n- {ds_summary}\n- {tk_summary}"
                
                # Generate prompt
                prompt = f"""As an expert in {analysis_domain.lower()}, analyze the following data:

{analysis_data}

Analysis Type: {analysis_type}
Scope: {scope}

Please provide:
1. Key findings and insights
2. Assesment of risks
3. Immediate recommendations
4. Long-term improvement strategies and techniques
5. next steps

Format with clear sections, bullet points, and prioritize by impact."""
                
                ai_output = ai.send_message(prompt)
                
                # Display results
                st.subheader("AI Analysis Report")
                st.markdown(ai_output)

            except Exception as e:
                st.error(f"Error generating AI analysis: {str(e)}")

st.markdown("---")

#Crud operations
st.header("Quick Operations")

# Tabs for different domains
tab_incidents, tab_datasets, tab_tickets = st.tabs(["🔒 Incidents", "📁 Datasets", "Tickets"])

with tab_incidents:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if incidents:
            incident_rows = []
            for inc in incidents[:5]:  
                incident_rows.append({
                    "ID": inc.get_id(),
                    "Title": inc.get_title(),
                    "Severity": inc.get_severity(),
                    "Status": inc.get_status(),
                    "Date": inc.get_date()
                })
            df_incidents = pd.DataFrame(incident_rows)
            st.dataframe(df_incidents, use_container_width=True, hide_index=True)
        else:
            st.info("No incidents found")
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("➕ Add Incident", key="quick_add_incident"):
            st.switch_page("pages/2_🛡_Cybersecurity.py")
        if incidents and st.button("✏️ Edit Incident", key="quick_edit_incident"):
            st.switch_page("pages/2_🛡_Cybersecurity.py")
        if st.button("📊 View All", key="quick_view_incidents"):
            st.switch_page("pages/2_🛡_Cybersecurity.py")

with tab_datasets:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if datasets:
            dataset_rows = []
            for ds in datasets[:5]:  
                dataset_rows.append({
                    "ID": ds.get_id(),
                    "Name": ds.get_name(),
                    "Source": ds.get_source(),
                    "Category": ds.get_category(),
                    "Size (MB)": ds.get_size()
                })
            df_datasets = pd.DataFrame(dataset_rows)
            st.dataframe(df_datasets, use_container_width=True, hide_index=True)
        else:
            st.info("No datasets found")
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("➕ Add Dataset", key="quick_add_dataset"):
            st.switch_page("pages/2_🛡_Cybersecurity.py")
        if datasets and st.button("✏️ Edit Dataset", key="quick_edit_dataset"):
            st.switch_page("pages/2_🛡_Cybersecurity.py")
        if st.button("📊 View All", key="quick_view_datasets"):
            st.switch_page("pages/2_🛡_Cybersecurity.py")

with tab_tickets:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if tickets:
            ticket_rows = []
            for t in tickets[:5]: 
                ticket_rows.append({
                    "ID": t.get_id(),
                    "Title": t.get_title(),
                    "Priority": t.get_priority(),
                    "Status": t.get_status(),
                    "Created": t.get_created_date()
                })
            df_tickets = pd.DataFrame(ticket_rows)
            st.dataframe(df_tickets, use_container_width=True, hide_index=True)
        else:
            st.info("No tickets found")
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("➕ Add Ticket", key="quick_add_ticket"):
            st.switch_page("pages/4_💻_IT_Operations.py")
        if tickets and st.button("✏️ Edit Ticket", key="quick_edit_ticket"):
            st.switch_page("pages/4_💻_IT_Operations.py")
        if st.button("📊 View All", key="quick_view_tickets"):
            st.switch_page("pages/4_💻_IT_Operations.py")

st.markdown("---")

# Navigation
st.header("Quick Navigation")

nav_cols = st.columns(4)

with nav_cols[0]:
    if st.button("🛡️ Cybersecurity Dashboard", use_container_width=True):
        st.switch_page("pages/2_🛡_Cybersecurity.py")

with nav_cols[1]:
    if st.button("📊 Data Analytics", use_container_width=True):
        st.switch_page("pages/3_📊_Data_Science.py")

with nav_cols[2]:
    if st.button("💻 IT Operations", use_container_width=True):
        st.switch_page("pages/4_💻_IT_Operations.py")

with nav_cols[3]:
    if st.button("🤖 AI Assistant", use_container_width=True):
        st.switch_page("pages/5_🤖_AI_Assistant.py")


