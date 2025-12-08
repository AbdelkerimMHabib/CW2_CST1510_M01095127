# My_app/pages/4_AI_Analyzer.py
import streamlit as st
from openai import OpenAI
from utils.database import connect_database, get_all_incidents, get_all_datasets, get_all_tickets, get_all_users

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(page_title="AI Analyzer", page_icon="🔍", layout="wide")
st.title("🔍 AI Multi-Table Analyzer")

# Initialize OpenAI client
client = None
try:
    if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    else:
        st.warning("OpenAI API key not found in secrets.")
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}")

conn = connect_database()

# Tab for different table analyses
tab1, tab2, tab3, tab4 = st.tabs(["🔒 Cyber Incidents", "📁 Datasets", "🎫 IT Tickets", "👥 Users"])

#Incident analysis
with tab1:
    st.subheader("Cyber Incident Analysis")
    
    incidents = get_all_incidents(conn)
    
    if not incidents:
        st.info("No incidents to analyze.")
    else:
        # Display incidents
        incident_list = [f"{r['id']}: {r['title']} ({r['severity']}, {r['status']})" for r in incidents]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_indices = st.multiselect(
                "Select incidents to analyze",
                options=list(range(len(incidents))),
                format_func=lambda i: incident_list[i],
                max_selections=5
            )
            
            analysis_type = st.selectbox(
                "Analysis Type",
                ["Comprehensive Analysis", "Root Cause Analysis", "Risk Assessment", 
                 "Mitigation Recommendations", "Trend Analysis"]
            )
            
            generate_report = st.button("Generate AI Analysis", type="primary", key="analyze_incidents")
        
        with col2:
            if selected_indices:
                st.write("### Selected Incidents:")
                for idx in selected_indices:
                    incident = incidents[idx]
                    with st.expander(f"🔹 {incident['title']}"):
                        st.write(f"**ID:** {incident['id']}")
                        st.write(f"**Severity:** {incident['severity']}")
                        st.write(f"**Status:** {incident['status']}")
                        st.write(f"**Date:** {incident['date']}")
            
            if generate_report and selected_indices and client:
                with st.spinner("🤖 AI is analyzing incidents..."):
                    try:
                        
                        selected_incidents = [incidents[idx] for idx in selected_indices]
                        
                        incidents_text = "\n\n".join([
                            f"Incident {i+1}:\n"
                            f"- Title: {inc['title']}\n"
                            f"- Severity: {inc['severity']}\n"
                            f"- Status: {inc['status']}\n"
                            f"- Date: {inc['date']}"
                            for i, inc in enumerate(selected_incidents)
                        ])
                        
                        prompt = f"""As a cybersecurity expert, analyze the following incidents:

{incidents_text}

Analysis Type: {analysis_type}

Please provide a detailed analysis including:
1. Overall risk assessment
2. Common patterns or trends
3. Immediate actions needed
4. Long-term prevention strategies
5. Recommendations for each incident

Format the response with clear sections and bullet points."""
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are a senior cybersecurity analyst with 15+ years of experience. Provide detailed, actionable insights."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=1500
                        )
                        
                        ai_output = response.choices[0].message.content
                        
                        st.subheader("📋 AI Analysis Report")
                        st.markdown(ai_output)
                        
                        # Download option
                        report_content = f"Cyber Incident Analysis Report\n\n{ai_output}"
                        st.download_button(
                            label="📥 Download Report",
                            data=report_content,
                            file_name=f"incident_analysis_{len(selected_indices)}_incidents.txt",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"Error generating analysis: {e}")

#Dataset analysis
with tab2:
    st.subheader("Dataset Analysis")
    
    datasets = get_all_datasets(conn)
    
    if not datasets:
        st.info("No datasets to analyze.")
    else:
        dataset_list = [f"{r['id']}: {r['name']} ({r['category']}, {r['size']}MB)" for r in datasets]
        
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
            
            generate_report = st.button("Generate AI Analysis", type="primary", key="analyze_datasets")
        
        with col2:
            if selected_indices:
                st.write("### Selected Datasets:")
                for idx in selected_indices:
                    dataset = datasets[idx]
                    with st.expander(f"📊 {dataset['name']}"):
                        st.write(f"**Source:** {dataset['source']}")
                        st.write(f"**Category:** {dataset['category']}")
                        st.write(f"**Size:** {dataset['size']} MB")
            
            if generate_report and selected_indices and client:
                with st.spinner("🤖 AI is analyzing datasets..."):
                    try:
                        selected_datasets = [datasets[idx] for idx in selected_indices]
                        
                        datasets_text = "\n\n".join([
                            f"Dataset {i+1}:\n"
                            f"- Name: {ds['name']}\n"
                            f"- Source: {ds['source']}\n"
                            f"- Category: {ds['category']}\n"
                            f"- Size: {ds['size']}MB"
                            for i, ds in enumerate(selected_datasets)
                        ])
                        
                        prompt = f"""As a data management expert, analyze the following datasets:

{datasets_text}

Analysis Type: {analysis_type}

Provide insights on:
1. Data quality and completeness
2. Potential use cases
3. Security and privacy considerations
4. Integration opportunities
5. Recommendations for data governance

Format with clear sections and actionable insights."""
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are a data architect and governance expert."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=1500
                        )
                        
                        ai_output = response.choices[0].message.content
                        
                        st.subheader("📋 Dataset Analysis Report")
                        st.markdown(ai_output)
                        
                        report_content = f"Dataset Analysis Report\n\n{ai_output}"
                        st.download_button(
                            label="📥 Download Report",
                            data=report_content,
                            file_name=f"dataset_analysis_{len(selected_indices)}_datasets.txt",
                            mime="text/plain",
                            key="download_dataset_report"
                        )
                        
                    except Exception as e:
                        st.error(f"Error generating analysis: {e}")
#Ticket Analysis
with tab3:
    st.subheader("IT Ticket Analysis")
    
    tickets = get_all_tickets(conn)
    
    if not tickets:
        st.info("No tickets to analyze.")
    else:
        ticket_list = [f"{r['id']}: {r['title']} ({r['priority']}, {r['status']})" for r in tickets]
        
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
            
            generate_report = st.button("Generate AI Analysis", type="primary", key="analyze_tickets")
        
        with col2:
            if selected_indices:
                st.write("### Selected Tickets:")
                for idx in selected_indices:
                    ticket = tickets[idx]
                    with st.expander(f"🎫 {ticket['title']}"):
                        st.write(f"**Priority:** {ticket['priority']}")
                        st.write(f"**Status:** {ticket['status']}")
                        st.write(f"**Created:** {ticket['created_date']}")
            
            if generate_report and selected_indices and client:
                with st.spinner("🤖 AI is analyzing tickets..."):
                    try:
                        selected_tickets = [tickets[idx] for idx in selected_indices]
                        
                        tickets_text = "\n\n".join([
                            f"Ticket {i+1}:\n"
                            f"- Title: {ticket['title']}\n"
                            f"- Priority: {ticket['priority']}\n"
                            f"- Status: {ticket['status']}\n"
                            f"- Created: {ticket['created_date']}"
                            for i, ticket in enumerate(selected_tickets)
                        ])
                        
                        prompt = f"""As an IT service management expert, analyze the following support tickets:

{tickets_text}

Analysis Type: {analysis_type}

Provide analysis covering:
1. Common issue patterns
2. Resolution effectiveness
3. Priority accuracy assessment
4. Process bottlenecks
5. Recommendations for IT service improvement

Format with clear sections and actionable recommendations."""
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are an ITIL certified service management expert."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=1500
                        )
                        
                        ai_output = response.choices[0].message.content
                        
                        st.subheader("📋 Ticket Analysis Report")
                        st.markdown(ai_output)
                        
                        report_content = f"IT Ticket Analysis Report\n\n{ai_output}"
                        st.download_button(
                            label="📥 Download Report",
                            data=report_content,
                            file_name=f"ticket_analysis_{len(selected_indices)}_tickets.txt",
                            mime="text/plain",
                            key="download_ticket_report"
                        )
                        
                    except Exception as e:
                        st.error(f"Error generating analysis: {e}")
#User analysis
with tab4:
    st.subheader("User Analysis")
    
    users = get_all_users(conn)
    
    if not users:
        st.info("No users to analyze.")
    else:
        user_list = [f"{r['id']}: {r['username']} ({r['role']})" for r in users]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_indices = st.multiselect(
                "Select users to analyze",
                options=list(range(len(users))),
                format_func=lambda i: user_list[i],
                max_selections=10
            )
            
            analysis_type = st.selectbox(
                "Analysis Type",
                ["Access Patterns", "Role Analysis", 
                 "Security Assessment", "Usage Trends", "Management Recommendations"],
                key="user_analysis_type"
            )
            
            generate_report = st.button("Generate AI Analysis", type="primary", key="analyze_users")
        
        with col2:
            if selected_indices:
                st.write("### Selected Users:")
                for idx in selected_indices:
                    user = users[idx]
                    with st.expander(f"👤 {user['username']}"):
                        st.write(f"**Role:** {user['role']}")
                        st.write(f"**Created:** {user['created_at']}")
            
            if generate_report and selected_indices and client:
                with st.spinner("🤖 AI is analyzing users..."):
                    try:
                        selected_users = [users[idx] for idx in selected_indices]
                        
                        users_text = "\n\n".join([
                            f"User {i+1}:\n"
                            f"- Username: {user['username']}\n"
                            f"- Role: {user['role']}\n"
                            f"- Created: {user['created_at']}"
                            for i, user in enumerate(selected_users)
                        ])
                        
                        prompt = f"""As a security and user management expert, analyze the following user accounts:

{users_text}

Analysis Type: {analysis_type}

Provide analysis covering:
1. Role distribution and appropriateness
2. Access control considerations
3. Security implications
4. User management recommendations
5. Compliance considerations

Format with clear sections and actionable insights."""
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are a cybersecurity and IAM (Identity and Access Management) expert."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=1500
                        )
                        
                        ai_output = response.choices[0].message.content
                        
                        st.subheader("📋 User Analysis Report")
                        st.markdown(ai_output)
                        
                        report_content = f"User Analysis Report\n\n{ai_output}"
                        st.download_button(
                            label="📥 Download Report",
                            data=report_content,
                            file_name=f"user_analysis_{len(selected_indices)}_users.txt",
                            mime="text/plain",
                            key="download_user_report"
                        )
                        
                    except Exception as e:
                        st.error(f"Error generating analysis: {e}")

#Navigation
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Back to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
with col2:
    if st.button("💬 Go to Chat Assistant"):
        st.switch_page("pages/chat.py")