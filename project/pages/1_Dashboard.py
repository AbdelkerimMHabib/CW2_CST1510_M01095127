# pages/1_Dashboard.py
import streamlit as st
from utils.database import connect_database, get_all_incidents, insert_incident, update_incident, delete_incident
from utils.database import get_all_datasets, insert_dataset, update_dataset, delete_dataset, get_dataset
from utils.database import get_all_tickets, insert_ticket, update_ticket, delete_ticket, get_ticket
from utils.database import get_all_users, update_user_role, delete_user, get_statistics, get_user
import pandas as pd
import datetime

# Protect the page
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Dashboard")
st.success(f"Welcome, {st.session_state.username}!")

conn = connect_database()

#Some statistics
st.header("📈 Overview")

try:
    stats = get_statistics(conn)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cyber Incidents", stats["incidents"]["total"], 
                 f"{stats['incidents']['open']} open" if stats["incidents"]["open"] > 0 else "All closed")
    with col2:
        st.metric("Datasets", stats["datasets"]["total"], 
                 f"{stats['datasets']['total_size']:,} MB")
    with col3:
        st.metric("IT Tickets", stats["tickets"]["total"], 
                 f"{stats['tickets']['open']} open" if stats["tickets"]["open"] > 0 else "All closed")
    with col4:
        st.metric("Users", stats["users"]["total"])
except Exception as e:
    st.error(f"Error loading statistics: {e}")
    # Show placeholder metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cyber Incidents", 0)
    with col2:
        st.metric("Datasets", 0)
    with col3:
        st.metric("IT Tickets", 0)
    with col4:
        st.metric("Users", 0)

#Cyber Incidents
st.header("🔒 Cyber Incidents")

incidents = get_all_incidents(conn)

# Display incidents
if incidents:
    df_incidents = pd.DataFrame([dict(row) for row in incidents])
    st.dataframe(df_incidents, use_container_width=True, hide_index=True)
else:
    st.info("No incidents in the database.")

# CRUD Operations for Incidents
tab1, tab2, tab3 = st.tabs(["➕ Add Incident", "✏️ Edit Incident", "🗑️ Delete Incident"])

with tab1:
    with st.form("add_incident_form"):
        st.subheader("Add New Incident")
        title = st.text_input("Incident Title*", placeholder="e.g., Phishing attack detected")
        severity = st.selectbox("Severity*", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status*", ["open", "in progress", "closed", "resolved"])
        date = st.date_input("Date*", value=datetime.date.today())
        
        submitted = st.form_submit_button("Add Incident")
        if submitted:
            if not title:
                st.error("Title is required!")
            else:
                insert_incident(conn, title, severity, status, date.isoformat())
                st.success("✅ Incident added successfully!")
                st.rerun()

with tab2:
    if incidents:
        st.subheader("Edit Existing Incident")
        incident_options = {f"{r['id']}: {r['title']}": r for r in incidents}
        selected_incident = st.selectbox("Select Incident to Edit", list(incident_options.keys()))
        
        if selected_incident:
            incident_id = int(selected_incident.split(":")[0])
            incident = incident_options[selected_incident]
            
            with st.form("edit_incident_form"):
                new_title = st.text_input("Title", value=incident["title"])
                new_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"], 
                                          index=["Low", "Medium", "High", "Critical"].index(incident["severity"]) 
                                          if incident["severity"] in ["Low", "Medium", "High", "Critical"] else 0)
                new_status = st.selectbox("Status", ["open", "in progress", "closed", "resolved"], 
                                        index=["open", "in progress", "closed", "resolved"].index(incident["status"]) 
                                        if incident["status"] in ["open", "in progress", "closed", "resolved"] else 0)
                new_date = st.text_input("Date (YYYY-MM-DD)", value=incident["date"])
                
                submitted = st.form_submit_button("Update Incident")
                if submitted:
                    update_incident(conn, incident_id, new_title, new_severity, new_status, new_date)
                    st.success("✅ Incident updated successfully!")
                    st.rerun()
    else:
        st.info("No incidents to edit.")

with tab3:
    if incidents:
        st.subheader("Delete Incident")
        delete_options = [f"{r['id']}: {r['title']}" for r in incidents]
        incident_to_delete = st.selectbox("Select Incident to Delete", delete_options)
        
        if incident_to_delete and st.button("Delete Incident", type="primary"):
            incident_id = int(incident_to_delete.split(":")[0])
            delete_incident(conn, incident_id)
            st.success("✅ Incident deleted successfully!")
            st.rerun()
    else:
        st.info("No incidents to delete.")

#Datasets 
st.header("📁 Datasets")

datasets = get_all_datasets(conn)

if datasets:
    df_datasets = pd.DataFrame([dict(r) for r in datasets])
    st.dataframe(df_datasets, use_container_width=True, hide_index=True)
else:
    st.info("No datasets found.")

# CRUD Operations for Datasets
tab4, tab5, tab6 = st.tabs(["➕ Add Dataset", "✏️ Edit Dataset", "🗑️ Delete Dataset"])

with tab4:
    with st.form("add_dataset_form"):
        st.subheader("Add New Dataset")
        name = st.text_input("Dataset Name*", placeholder="e.g., Network Traffic Logs")
        source = st.text_input("Source*", placeholder="e.g., Internal Systems, MITRE")
        category = st.selectbox("Category*", ["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Other"])
        size = st.number_input("Size (MB)*", min_value=1, value=100)
        
        submitted = st.form_submit_button("Add Dataset")
        if submitted:
            if not name or not source:
                st.error("Name and Source are required!")
            else:
                insert_dataset(conn, name, source, category, size)
                st.success("✅ Dataset added successfully!")
                st.rerun()

with tab5:
    if datasets:
        st.subheader("Edit Existing Dataset")
        dataset_options = {f"{r['id']}: {r['name']}": r for r in datasets}
        selected_dataset = st.selectbox("Select Dataset to Edit", list(dataset_options.keys()))
        
        if selected_dataset:
            dataset_id = int(selected_dataset.split(":")[0])
            dataset = dataset_options[selected_dataset]
            
            with st.form("edit_dataset_form"):
                new_name = st.text_input("Name", value=dataset["name"])
                new_source = st.text_input("Source", value=dataset["source"])
                new_category = st.selectbox("Category", ["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Other"],
                                          index=["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Other"].index(dataset["category"])
                                          if dataset["category"] in ["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Other"] else 0)
                new_size = st.number_input("Size (MB)", min_value=1, value=dataset["size"])
                
                submitted = st.form_submit_button("Update Dataset")
                if submitted:
                    update_dataset(conn, dataset_id, new_name, new_source, new_category, new_size)
                    st.success("✅ Dataset updated successfully!")
                    st.rerun()
    else:
        st.info("No datasets to edit.")

with tab6:
    if datasets:
        st.subheader("Delete Dataset")
        delete_options = [f"{r['id']}: {r['name']}" for r in datasets]
        dataset_to_delete = st.selectbox("Select Dataset to Delete", delete_options)
        
        if dataset_to_delete and st.button("Delete Dataset", type="primary"):
            dataset_id = int(dataset_to_delete.split(":")[0])
            delete_dataset(conn, dataset_id)
            st.success("✅ Dataset deleted successfully!")
            st.rerun()
    else:
        st.info("No datasets to delete.")
#It_Tickets
st.header("🎫 IT Tickets")

tickets = get_all_tickets(conn)

if tickets:
    df_tickets = pd.DataFrame([dict(r) for r in tickets])
    st.dataframe(df_tickets, use_container_width=True, hide_index=True)
else:
    st.info("No tickets found.")

# CRUD Operations for Tickets
tab7, tab8, tab9 = st.tabs(["➕ Add Ticket", "✏️ Edit Ticket", "🗑️ Delete Ticket"])

with tab7:
    with st.form("add_ticket_form"):
        st.subheader("Add New Ticket")
        title = st.text_input("Ticket Title*", placeholder="e.g., VPN not connecting")
        priority = st.selectbox("Priority*", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status*", ["open", "in progress", "closed", "resolved"])
        created_date = st.date_input("Created Date*", value=datetime.date.today())
        
        submitted = st.form_submit_button("Add Ticket")
        if submitted:
            if not title:
                st.error("Title is required!")
            else:
                insert_ticket(conn, title, priority, status, created_date.isoformat())
                st.success("✅ Ticket added successfully!")
                st.rerun()

with tab8:
    if tickets:
        st.subheader("Edit Existing Ticket")
        ticket_options = {f"{r['id']}: {r['title']}": r for r in tickets}
        selected_ticket = st.selectbox("Select Ticket to Edit", list(ticket_options.keys()))
        
        if selected_ticket:
            ticket_id = int(selected_ticket.split(":")[0])
            ticket = ticket_options[selected_ticket]
            
            with st.form("edit_ticket_form"):
                new_title = st.text_input("Title", value=ticket["title"])
                new_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"],
                                          index=["Low", "Medium", "High", "Critical"].index(ticket["priority"])
                                          if ticket["priority"] in ["Low", "Medium", "High", "Critical"] else 0)
                new_status = st.selectbox("Status", ["open", "in progress", "closed", "resolved"],
                                        index=["open", "in progress", "closed", "resolved"].index(ticket["status"])
                                        if ticket["status"] in ["open", "in progress", "closed", "resolved"] else 0)
                new_date = st.text_input("Created Date (YYYY-MM-DD)", value=ticket["created_date"])
                
                submitted = st.form_submit_button("Update Ticket")
                if submitted:
                    update_ticket(conn, ticket_id, new_title, new_priority, new_status, new_date)
                    st.success("✅ Ticket updated successfully!")
                    st.rerun()
    else:
        st.info("No tickets to edit.")

with tab9:
    if tickets:
        st.subheader("Delete Ticket")
        delete_options = [f"{r['id']}: {r['title']}" for r in tickets]
        ticket_to_delete = st.selectbox("Select Ticket to Delete", delete_options)
        
        if ticket_to_delete and st.button("Delete Ticket", type="primary"):
            ticket_id = int(ticket_to_delete.split(":")[0])
            delete_ticket(conn, ticket_id)
            st.success("✅ Ticket deleted successfully!")
            st.rerun()
    else:
        st.info("No tickets to delete.")

#User management for admin
# Check if current user is admin
current_user = get_user(conn, st.session_state.username)
if current_user and current_user["role"] == "admin":
    st.header("👥 User Management")
    
    users = get_all_users(conn)
    if users:
        df_users = pd.DataFrame([dict(r) for r in users])
        st.dataframe(df_users, use_container_width=True, hide_index=True)
        
        # Admin can edit user roles
        st.subheader("Manage User Roles")
        user_options = {f"{r['id']}: {r['username']}": r for r in users}
        selected_user = st.selectbox("Select User", list(user_options.keys()))
        
        if selected_user:
            user_id = int(selected_user.split(":")[0])
            user_data = user_options[selected_user]
            
            col1, col2 = st.columns(2)
            with col1:
                new_role = st.selectbox("New Role", ["user", "admin", "editor"], 
                                      index=["user", "admin", "editor"].index(user_data["role"])
                                      if user_data["role"] in ["user", "admin", "editor"] else 0)
                if st.button("Update Role"):
                    update_user_role(conn, user_id, new_role)
                    st.success("✅ User role updated!")
                    st.rerun()
            
            with col2:
                if user_data["username"] != st.session_state.username:  
                    if st.button("Delete User", type="secondary"):
                        delete_user(conn, user_id)
                        st.success("✅ User deleted!")
                        st.rerun()
                else:
                    st.warning("Cannot delete your own account")
else:
    # Show current user info for non-admins
    if current_user:
        with st.expander("👤 Your Account Info"):
            st.write(f"**Username:** {current_user['username']}")
            st.write(f"**Role:** {current_user['role']}")
            st.write(f"**Member Since:** {current_user['created_at']}")

#Naviagation
st.divider()
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📊 Analytics"):
        st.switch_page("pages/2_Analytics.py")
with col2:
    if st.button("🔍 AI Analyzer"):
        st.switch_page("pages/4_AI_Analyzer.py")
with col3:
    if st.button("💬 Chat"):
        st.switch_page("pages/chat.py")
with col4:
    if st.button("⚙️ Settings"):
        st.switch_page("pages/3_Settings.py")

# Logout button
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out")
    st.switch_page("Home.py")