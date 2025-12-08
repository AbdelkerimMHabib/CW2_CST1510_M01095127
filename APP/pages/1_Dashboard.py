import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from utils.database import connect_database, get_dashboard_stats, get_all_incidents, get_all_datasets, get_all_tickets
from utils.database import insert_incident, insert_dataset, insert_ticket, update_incident, update_dataset, update_ticket, delete_incident, delete_dataset, delete_ticket
from utils.openai_client import openai_client

# Login check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()

# Page config
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Title
st.title("📊 Multi-Domain Intelligence Dashboard")
st.caption(f"Welcome, {st.session_state.username}! | Role: {st.session_state.role}")

# Database connection
conn = connect_database()
stats = get_dashboard_stats(conn)

# Sidebar
with st.sidebar:
    st.subheader("Quick Actions")
    
    # Domain selection for quick add
    domain_to_add = st.selectbox("Add New Item", ["Select...", "Cyber Incident", "Dataset", "IT Ticket"])
    
    if domain_to_add == "Cyber Incident":
        with st.form("quick_add_incident"):
            title = st.text_input("Title")
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
            date = st.date_input("Date", datetime.now())
            if st.form_submit_button("Add Incident"):
                insert_incident(conn, title, severity, status, date.strftime("%Y-%m-%d"), created_by=st.session_state.username)
                st.success("Incident added!")
                st.rerun()
    
    elif domain_to_add == "Dataset":
        with st.form("quick_add_dataset"):
            name = st.text_input("Name")
            source = st.text_input("Source")
            category = st.selectbox("Category", ["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Other"])
            size = st.number_input("Size (MB)", min_value=0)
            if st.form_submit_button("Add Dataset"):
                insert_dataset(conn, name, source, category, size, created_by=st.session_state.username)
                st.success("Dataset added!")
                st.rerun()
    
    elif domain_to_add == "IT Ticket":
        with st.form("quick_add_ticket"):
            title = st.text_input("Title")
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
            created_date = st.date_input("Created Date", datetime.now())
            if st.form_submit_button("Add Ticket"):
                insert_ticket(conn, title, priority, status, created_date.strftime("%Y-%m-%d"), created_by=st.session_state.username)
                st.success("Ticket added!")
                st.rerun()
    
    st.divider()
    
    # AI Insights
    if st.button("🤖 Get AI Insights", use_container_width=True):
        st.session_state.show_ai_insights = True
    
    # Refresh button
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()

# Main dashboard layout
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🛡️ Cyber Incidents", "📂 Datasets", "💻 IT Tickets"])

# Tab 1: Overview
with tab1:
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Incidents", stats["incidents"], 
                 delta=f"{stats['open_incidents']} open", delta_color="inverse")
    
    with col2:
        st.metric("Total Datasets", stats["datasets"], 
                 delta=f"{stats['total_size_mb']} MB", delta_color="off")
    
    with col3:
        st.metric("Total Tickets", stats["tickets"], 
                 delta=f"{stats['open_tickets']} open", delta_color="inverse")
    
    with col4:
        st.metric("Total Users", stats["users"])
    
    st.markdown("---")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Incident Severity Distribution")
        if stats["severity_distribution"]:
            severity_df = pd.DataFrame({
                "Severity": list(stats["severity_distribution"].keys()),
                "Count": list(stats["severity_distribution"].values())
            })
            chart = alt.Chart(severity_df).mark_bar().encode(
                x=alt.X("Severity:N", sort=None),
                y="Count:Q",
                color="Severity:N"
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No incident data")
    
    with col2:
        st.subheader("Ticket Priority Distribution")
        if stats["priority_distribution"]:
            priority_df = pd.DataFrame({
                "Priority": list(stats["priority_distribution"].keys()),
                "Count": list(stats["priority_distribution"].values())
            })
            chart = alt.Chart(priority_df).mark_bar().encode(
                x=alt.X("Priority:N", sort=None),
                y="Count:Q",
                color="Priority:N"
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No ticket data")
    
    # Recent Activities
    st.markdown("---")
    st.subheader("Recent Activities")
    if stats["recent_activities"]:
        activities_df = pd.DataFrame(stats["recent_activities"], 
                                   columns=["ID", "Username", "Action", "Entity", "Entity ID", "Details", "Timestamp"])
        st.dataframe(activities_df[["Username", "Action", "Details", "Timestamp"]], 
                    use_container_width=True, hide_index=True)
    else:
        st.info("No recent activities")
    
    # AI Insights
    if st.session_state.get("show_ai_insights", False):
        st.markdown("---")
        st.subheader("🤖 AI-Generated Insights")
        
        with st.spinner("AI is analyzing your data..."):
            insights = openai_client.generate_dashboard_insights(stats)
            if insights:
                st.markdown(insights)
            else:
                st.error("Could not generate AI insights. Check API configuration.")
        
        if st.button("Hide AI Insights"):
            del st.session_state.show_ai_insights
            st.rerun()

# Tab 2: Cyber Incidents (with CRUD)
with tab2:
    st.subheader("🛡️ Cyber Incidents Management")
    
    # Add new incident
    with st.expander("➕ Add New Incident", expanded=False):
        with st.form("add_incident_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title*", key="new_inc_title")
                severity = st.selectbox("Severity*", ["Low", "Medium", "High", "Critical"], key="new_inc_severity")
            with col2:
                status = st.selectbox("Status*", ["Open", "In Progress", "Resolved", "Closed"], key="new_inc_status")
                date = st.date_input("Date*", datetime.now(), key="new_inc_date")
            
            description = st.text_area("Description", height=100, key="new_inc_desc")
            
            if st.form_submit_button("Add Incident", use_container_width=True):
                if title:
                    insert_incident(conn, title, severity, status, date.strftime("%Y-%m-%d"), 
                                   description, st.session_state.username)
                    st.success("Incident added successfully!")
                    st.rerun()
                else:
                    st.error("Title is required!")
    
    st.markdown("---")
    
    # List and manage incidents
    incidents = get_all_incidents(conn)
    if incidents:
        df_inc = pd.DataFrame(incidents, columns=["ID", "Title", "Severity", "Status", "Date", "Description", "Created By", "Updated"])
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_severity = st.multiselect("Filter by Severity", df_inc["Severity"].unique(), key="inc_severity_filter")
        with col2:
            filter_status = st.multiselect("Filter by Status", df_inc["Status"].unique(), key="inc_status_filter")
        with col3:
            search_term = st.text_input("Search incidents", key="inc_search")
        
        # Apply filters
        filtered_df = df_inc.copy()
        if filter_severity:
            filtered_df = filtered_df[filtered_df["Severity"].isin(filter_severity)]
        if filter_status:
            filtered_df = filtered_df[filtered_df["Status"].isin(filter_status)]
        if search_term:
            filtered_df = filtered_df[filtered_df["Title"].str.contains(search_term, case=False) | 
                                     filtered_df["Description"].str.contains(search_term, case=False)]
        
        # Display incidents
        for idx, row in filtered_df.iterrows():
            with st.expander(f"{row['Title']} - {row['Severity']} - {row['Status']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Date:** {row['Date']}")
                    st.markdown(f"**Created by:** {row['Created By']}")
                    if row['Description']:
                        st.markdown(f"**Description:** {row['Description']}")
                with col2:
                    severity_color = {"Critical": "red", "High": "orange", "Medium": "yellow", "Low": "green"}
                    st.markdown(f"<span style='color:{severity_color.get(row['Severity'], 'gray')}; font-weight:bold;'>{row['Severity']}</span>", 
                              unsafe_allow_html=True)
                    status_color = {"Open": "red", "In Progress": "orange", "Resolved": "blue", "Closed": "green"}
                    st.markdown(f"<span style='color:{status_color.get(row['Status'], 'gray')};'>{row['Status']}</span>", 
                              unsafe_allow_html=True)
                
                # Edit form
                with st.form(f"edit_incident_{row['ID']}"):
                    new_title = st.text_input("Title", value=row["Title"], key=f"title_{row['ID']}")
                    new_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"], 
                                              index=["Low", "Medium", "High", "Critical"].index(row["Severity"]) 
                                              if row["Severity"] in ["Low", "Medium", "High", "Critical"] else 0,
                                              key=f"sev_{row['ID']}")
                    new_status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"], 
                                            index=["Open", "In Progress", "Resolved", "Closed"].index(row["Status"]) 
                                            if row["Status"] in ["Open", "In Progress", "Resolved", "Closed"] else 0,
                                            key=f"status_{row['ID']}")
                    new_date = st.date_input("Date", pd.to_datetime(row["Date"]), key=f"date_{row['ID']}")
                    new_description = st.text_area("Description", value=row["Description"] if row["Description"] else "", 
                                                  key=f"desc_{row['ID']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update", use_container_width=True):
                            update_incident(conn, row["ID"], new_title, new_severity, new_status, 
                                          new_date.strftime("%Y-%m-%d"), new_description, st.session_state.username)
                            st.success("Incident updated!")
                            st.rerun()
                    with col2:
                        if st.button("Delete", key=f"delete_{row['ID']}", use_container_width=True):
                            delete_incident(conn, row["ID"], st.session_state.username)
                            st.success("Incident deleted!")
                            st.rerun()
                
                # AI Analysis for this incident
                if st.button("🤖 AI Analysis", key=f"ai_inc_{row['ID']}", use_container_width=True):
                    incident_data = {
                        "title": row["Title"],
                        "severity": row["Severity"],
                        "status": row["Status"],
                        "date": row["Date"]
                    }
                    analysis = openai_client.analyze_cyber_incident(incident_data)
                    st.markdown("### AI Analysis")
                    st.markdown(analysis)
    else:
        st.info("No incidents yet. Add your first incident above.")

# Tab 3: Datasets (with CRUD)
with tab3:
    st.subheader("📂 Datasets Management")
    
    # Add new dataset
    with st.expander("➕ Add New Dataset", expanded=False):
        with st.form("add_dataset_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name*", key="new_ds_name")
                source = st.text_input("Source*", key="new_ds_source")
            with col2:
                category = st.selectbox("Category*", ["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Network", "Other"], 
                                      key="new_ds_category")
                size = st.number_input("Size (MB)*", min_value=0, key="new_ds_size")
            
            format_type = st.text_input("Format (optional)", key="new_ds_format")
            
            if st.form_submit_button("Add Dataset", use_container_width=True):
                if name and source and category:
                    insert_dataset(conn, name, source, category, size, format_type, st.session_state.username)
                    st.success("Dataset added successfully!")
                    st.rerun()
                else:
                    st.error("Name, Source, and Category are required!")
    
    st.markdown("---")
    
    # List and manage datasets
    datasets = get_all_datasets(conn)
    if datasets:
        df_ds = pd.DataFrame(datasets, columns=["ID", "Name", "Source", "Category", "Size", "Format", "Created By", "Created"])
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            filter_category = st.multiselect("Filter by Category", df_ds["Category"].unique(), key="ds_category_filter")
        with col2:
            search_term = st.text_input("Search datasets", key="ds_search")
        
        # Apply filters
        filtered_df = df_ds.copy()
        if filter_category:
            filtered_df = filtered_df[filtered_df["Category"].isin(filter_category)]
        if search_term:
            filtered_df = filtered_df[filtered_df["Name"].str.contains(search_term, case=False) | 
                                     filtered_df["Source"].str.contains(search_term, case=False)]
        
        # Display datasets
        st.dataframe(filtered_df[["Name", "Source", "Category", "Size", "Format", "Created By"]], 
                    use_container_width=True, hide_index=True)
        
        # Edit/Delete section
        st.subheader("Edit Dataset")
        dataset_ids = filtered_df["ID"].tolist()
        if dataset_ids:
            selected_id = st.selectbox("Select Dataset ID to edit", dataset_ids, key="ds_edit_select")
            selected_ds = df_ds[df_ds["ID"] == selected_id].iloc[0]
            
            with st.form("edit_dataset_form"):
                new_name = st.text_input("Name", value=selected_ds["Name"], key=f"edit_ds_name")
                new_source = st.text_input("Source", value=selected_ds["Source"], key=f"edit_ds_source")
                new_category = st.selectbox("Category", ["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Network", "Other"], 
                                          index=["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Network", "Other"].index(selected_ds["Category"]) 
                                          if selected_ds["Category"] in ["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Network", "Other"] else 0,
                                          key=f"edit_ds_category")
                new_size = st.number_input("Size (MB)", min_value=0, value=int(selected_ds["Size"]), key=f"edit_ds_size")
                new_format = st.text_input("Format", value=selected_ds["Format"] if selected_ds["Format"] else "", key=f"edit_ds_format")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Update Dataset", use_container_width=True):
                        update_dataset(conn, selected_id, new_name, new_source, new_category, new_size, new_format, st.session_state.username)
                        st.success("Dataset updated!")
                        st.rerun()
                with col2:
                    if st.button("Delete Dataset", key=f"delete_ds_{selected_id}", use_container_width=True):
                        delete_dataset(conn, selected_id, st.session_state.username)
                        st.success("Dataset deleted!")
                        st.rerun()
        else:
            st.info("No datasets match the filters")
    else:
        st.info("No datasets yet. Add your first dataset above.")

# Tab 4: IT Tickets (with CRUD)
with tab4:
    st.subheader("💻 IT Tickets Management")
    
    # Add new ticket
    with st.expander("➕ Add New Ticket", expanded=False):
        with st.form("add_ticket_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title*", key="new_tk_title")
                priority = st.selectbox("Priority*", ["Low", "Medium", "High"], key="new_tk_priority")
            with col2:
                status = st.selectbox("Status*", ["Open", "In Progress", "Resolved", "Closed"], key="new_tk_status")
                created_date = st.date_input("Created Date*", datetime.now(), key="new_tk_date")
            
            assigned_to = st.text_input("Assigned to (optional)", key="new_tk_assigned")
            description = st.text_area("Description", height=100, key="new_tk_desc")
            
            if st.form_submit_button("Add Ticket", use_container_width=True):
                if title:
                    insert_ticket(conn, title, priority, status, created_date.strftime("%Y-%m-%d"), 
                                 assigned_to, description, st.session_state.username)
                    st.success("Ticket added successfully!")
                    st.rerun()
                else:
                    st.error("Title is required!")
    
    st.markdown("---")
    
    # List and manage tickets
    tickets = get_all_tickets(conn)
    if tickets:
        df_tk = pd.DataFrame(tickets, columns=["ID", "Title", "Priority", "Status", "Created Date", "Assigned To", "Description", "Resolution", "Updated"])
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_priority = st.multiselect("Filter by Priority", df_tk["Priority"].unique(), key="tk_priority_filter")
        with col2:
            filter_status = st.multiselect("Filter by Status", df_tk["Status"].unique(), key="tk_status_filter")
        with col3:
            search_term = st.text_input("Search tickets", key="tk_search")
        
        # Apply filters
        filtered_df = df_tk.copy()
        if filter_priority:
            filtered_df = filtered_df[filtered_df["Priority"].isin(filter_priority)]
        if filter_status:
            filtered_df = filtered_df[filtered_df["Status"].isin(filter_status)]
        if search_term:
            filtered_df = filtered_df[filtered_df["Title"].str.contains(search_term, case=False) | 
                                     filtered_df["Description"].str.contains(search_term, case=False) |
                                     df_tk["Assigned To"].str.contains(search_term, case=False)]
        
        # Display tickets
        for idx, row in filtered_df.iterrows():
            with st.expander(f"{row['Title']} - {row['Priority']} - {row['Status']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Created:** {row['Created Date']}")
                    st.markdown(f"**Assigned to:** {row['Assigned To'] if row['Assigned To'] else 'Unassigned'}")
                    if row['Description']:
                        st.markdown(f"**Description:** {row['Description']}")
                    if row['Resolution']:
                        st.markdown(f"**Resolution:** {row['Resolution']}")
                with col2:
                    priority_color = {"High": "red", "Medium": "orange", "Low": "green"}
                    st.markdown(f"<span style='color:{priority_color.get(row['Priority'], 'gray')}; font-weight:bold;'>{row['Priority']}</span>", 
                              unsafe_allow_html=True)
                    status_color = {"Open": "red", "In Progress": "orange", "Resolved": "blue", "Closed": "green"}
                    st.markdown(f"<span style='color:{status_color.get(row['Status'], 'gray')};'>{row['Status']}</span>", 
                              unsafe_allow_html=True)
                
                # Edit form
                with st.form(f"edit_ticket_{row['ID']}"):
                    new_title = st.text_input("Title", value=row["Title"], key=f"tk_title_{row['ID']}")
                    new_priority = st.selectbox("Priority", ["Low", "Medium", "High"], 
                                              index=["Low", "Medium", "High"].index(row["Priority"]) 
                                              if row["Priority"] in ["Low", "Medium", "High"] else 0,
                                              key=f"tk_prio_{row['ID']}")
                    new_status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"], 
                                            index=["Open", "In Progress", "Resolved", "Closed"].index(row["Status"]) 
                                            if row["Status"] in ["Open", "In Progress", "Resolved", "Closed"] else 0,
                                            key=f"tk_status_{row['ID']}")
                    new_date = st.date_input("Created Date", pd.to_datetime(row["Created Date"]), key=f"tk_date_{row['ID']}")
                    new_assigned = st.text_input("Assigned to", value=row["Assigned To"] if row["Assigned To"] else "", 
                                                key=f"tk_assigned_{row['ID']}")
                    new_description = st.text_area("Description", value=row["Description"] if row["Description"] else "", 
                                                  key=f"tk_desc_{row['ID']}")
                    new_resolution = st.text_area("Resolution", value=row["Resolution"] if row["Resolution"] else "", 
                                                 key=f"tk_res_{row['ID']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update", use_container_width=True):
                            update_ticket(conn, row["ID"], new_title, new_priority, new_status, 
                                        new_date.strftime("%Y-%m-%d"), new_assigned, new_description, 
                                        new_resolution, st.session_state.username)
                            st.success("Ticket updated!")
                            st.rerun()
                    with col2:
                        if st.button("Delete", key=f"tk_delete_{row['ID']}", use_container_width=True):
                            delete_ticket(conn, row["ID"], st.session_state.username)
                            st.success("Ticket deleted!")
                            st.rerun()
                
                # AI Analysis for this ticket
                if st.button("🤖 AI Troubleshooting", key=f"ai_tk_{row['ID']}", use_container_width=True):
                    ticket_data = {
                        "title": row["Title"],
                        "priority": row["Priority"],
                        "status": row["Status"],
                        "created_date": row["Created Date"]
                    }
                    analysis = openai_client.analyze_it_ticket(ticket_data)
                    st.markdown("### AI Troubleshooting Guide")
                    st.markdown(analysis)
    else:
        st.info("No tickets yet. Add your first ticket above.")

# Bottom navigation
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("🤖 AI Assistant", use_container_width=True):
        st.switch_page("pages/7_AI_Assistant.py")
with col3:
    if st.button("📈 Analytics", use_container_width=True):
        st.switch_page("pages/5_Analytics.py")
with col4:
    if st.button("⚙️ Settings", use_container_width=True):
        st.switch_page("pages/6_Settings.py")