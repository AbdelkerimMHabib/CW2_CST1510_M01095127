import streamlit as st
import pandas as pd
from utils.database import connect_database, get_all_incidents, insert_incident, update_incident, delete_incident, get_incidents_by_severity, get_incidents_by_status
from utils.openai_client import openai_client
from datetime import datetime

# Login check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()

# Page config
st.set_page_config(page_title="Cyber Incidents", page_icon="🛡️", layout="wide")

st.title("🛡️ Cyber Incidents Management")

conn = connect_database()
incidents = get_all_incidents(conn)

# Sidebar filters
with st.sidebar:
    st.subheader("Filters")
    
    # Severity filter
    severities = ["All", "Critical", "High", "Medium", "Low"]
    selected_severity = st.selectbox("Filter by Severity", severities)
    
    # Status filter
    statuses = ["All", "Open", "In Progress", "Resolved", "Closed"]
    selected_status = st.selectbox("Filter by Status", statuses)
    
    # Date range
    st.subheader("Date Range")
    date_range = st.date_input("Select Date Range", 
                              [datetime.now() - timedelta(days=30), datetime.now()])
    
    # AI Analysis button
    if st.button("🤖 Bulk AI Analysis", use_container_width=True):
        st.session_state.show_bulk_analysis = True

# Main content
col1, col2 = st.columns([3, 1])

with col1:
    # Add new incident
    with st.expander("➕ Add New Incident", expanded=False):
        with st.form("add_incident_form"):
            title = st.text_input("Title*")
            severity = st.selectbox("Severity*", ["Low", "Medium", "High", "Critical"])
            status = st.selectbox("Status*", ["Open", "In Progress", "Resolved", "Closed"])
            date = st.date_input("Date*", datetime.now())
            description = st.text_area("Description", height=100)
            
            if st.form_submit_button("Add Incident", use_container_width=True):
                if title:
                    insert_incident(conn, title, severity, status, date.strftime("%Y-%m-%d"), 
                                   description, st.session_state.username)
                    st.success("Incident added successfully!")
                    st.rerun()
                else:
                    st.error("Title is required!")

with col2:
    # Quick stats
    st.subheader("Quick Stats")
    if incidents:
        df_inc = pd.DataFrame(incidents, columns=["ID", "Title", "Severity", "Status", "Date", "Description", "Created By", "Updated"])
        critical_count = len(df_inc[df_inc["Severity"] == "Critical"])
        open_count = len(df_inc[df_inc["Status"] == "Open"])
        st.metric("Critical", critical_count)
        st.metric("Open", open_count)
    else:
        st.info("No incidents")

st.markdown("---")

# Display incidents
if incidents:
    df_inc = pd.DataFrame(incidents, columns=["ID", "Title", "Severity", "Status", "Date", "Description", "Created By", "Updated"])
    
    # Apply filters
    if selected_severity != "All":
        df_inc = df_inc[df_inc["Severity"] == selected_severity]
    if selected_status != "All":
        df_inc = df_inc[df_inc["Status"] == selected_status]
    if len(date_range) == 2:
        df_inc = df_inc[(pd.to_datetime(df_inc["Date"]) >= pd.to_datetime(date_range[0])) & 
                       (pd.to_datetime(df_inc["Date"]) <= pd.to_datetime(date_range[1]))]
    
    # Display table
    st.dataframe(df_inc[["Title", "Severity", "Status", "Date", "Created By"]], 
                use_container_width=True, hide_index=True)
    
    # Bulk AI Analysis
    if st.session_state.get("show_bulk_analysis", False):
        st.markdown("---")
        st.subheader("🤖 Bulk AI Analysis")
        
        if st.button("Generate Analysis Report", use_container_width=True):
            with st.spinner("AI is analyzing all incidents..."):
                analysis_prompt = f"""
                Analyze these {len(df_inc)} cyber incidents:
                
                {df_inc.to_string()}
                
                Provide:
                1. Overall risk assessment
                2. Top 3 security gaps
                3. Immediate action items
                4. Long-term security recommendations
                5. Compliance impact assessment
                """
                
                analysis = openai_client.chat([
                    {"role": "system", "content": "You are a Chief Information Security Officer (CISO)."},
                    {"role": "user", "content": analysis_prompt}
                ])
                
                if analysis:
                    st.markdown(analysis)
                    
                    # Export option
                    st.download_button(
                        label="📥 Download Analysis Report",
                        data=analysis,
                        file_name=f"cyber_incidents_analysis_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Could not generate analysis. Check API configuration.")
        
        if st.button("Close Analysis"):
            del st.session_state.show_bulk_analysis
            st.rerun()
    
    # Edit/Delete individual incidents
    st.markdown("---")
    st.subheader("Edit Incident")
    
    incident_ids = df_inc["ID"].tolist()
    if incident_ids:
        selected_id = st.selectbox("Select Incident ID to edit", incident_ids)
        selected_inc = df_inc[df_inc["ID"] == selected_id].iloc[0]
        
        with st.form("edit_incident_form"):
            new_title = st.text_input("Title", value=selected_inc["Title"])
            new_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"], 
                                      index=["Low", "Medium", "High", "Critical"].index(selected_inc["Severity"]) 
                                      if selected_inc["Severity"] in ["Low", "Medium", "High", "Critical"] else 0)
            new_status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"], 
                                    index=["Open", "In Progress", "Resolved", "Closed"].index(selected_inc["Status"]) 
                                    if selected_inc["Status"] in ["Open", "In Progress", "Resolved", "Closed"] else 0)
            new_date = st.date_input("Date", pd.to_datetime(selected_inc["Date"]))
            new_description = st.text_area("Description", value=selected_inc["Description"] if selected_inc["Description"] else "")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Update Incident", use_container_width=True):
                    update_incident(conn, selected_id, new_title, new_severity, new_status, 
                                  new_date.strftime("%Y-%m-%d"), new_description, st.session_state.username)
                    st.success("Incident updated!")
                    st.rerun()
            with col2:
                if st.button("Delete Incident", key=f"delete_{selected_id}", use_container_width=True):
                    delete_incident(conn, selected_id, st.session_state.username)
                    st.success("Incident deleted!")
                    st.rerun()
    else:
        st.info("No incidents match the filters")
else:
    st.info("No incidents yet. Add your first incident above.")

# Bottom navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")
with col2:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
with col3:
    if st.button("🤖 AI Assistant", use_container_width=True):
        st.switch_page("pages/7_AI_Assistant.py")