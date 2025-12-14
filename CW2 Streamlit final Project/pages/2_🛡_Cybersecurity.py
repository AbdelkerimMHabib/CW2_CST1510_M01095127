"""Cybersecurity Dashboard using OOP"""
import streamlit as st
import pandas as pd
import datetime
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from models.security_incident import SecurityIncident
from models.dataset import Dataset
from models.it_ticket import ITTicket

#Protect the page
#Make sure only logged-in users can access the dashboard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("pages/1_🔐_Login.py")
    st.stop()

#Page configuration
st.set_page_config(page_title="Cybersecurity Dashboard", page_icon="🛡️", layout="wide")
st.title("🛡️ Cybersecurity Dashboard")
st.success(f"Welcome, {st.session_state.username}!")

# Initialize needed services

#Database manager handles all of the database interactions
db = DatabaseManager()

#Authentication manager handles user-related operations
auth = AuthManager(db)

# Statistics
st.header("Overview")

try:
    stats = db.get_statistics()
    
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
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cyber Incidents", 0)
    with col2:
        st.metric("Datasets", 0)
    with col3:
        st.metric("IT Tickets", 0)
    with col4:
        st.metric("Users", 0)

# Cyber Incidents
st.header("🔒 Cyber Incidents")

incident_data = db.get_all_incidents()

# Convert to Security Incident objects
incidents = []
for data in incident_data:
    incidents.append(SecurityIncident(
        incident_id=data["id"],
        title=data["title"],
        severity=data["severity"],
        status=data["status"],
        date=data["date"]
    ))

# Show the incidents using object methods
if incidents:
    incident_rows = []
    for incident in incidents:
        incident_rows.append({
            "ID": incident.get_id(),
            "Title": incident.get_title(),
            "Severity": incident.get_severity(),
            "Status": incident.get_status(),
            "Date": incident.get_date(),
            "Severity Level": incident.get_severity_level()
        })
    
    df_incidents = pd.DataFrame(incident_rows)
    st.dataframe(df_incidents, use_container_width=True, hide_index=True)
else:
    st.info("No incidents in the database.")

# CRUD Operations for Incidents (add incident, edit incident, and delete incident)
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
                db.insert_incident(title, severity, status, date.isoformat())
                st.success("Incident added successfully!")
                st.rerun()

#Edit Incident
with tab2:
    if incidents:
        st.subheader("Edit Existing Incident")
        incident_options = {f"{incident.get_id()}: {incident.get_title()}": incident for incident in incidents}
        selected_incident_key = st.selectbox("Select Incident to Edit", list(incident_options.keys()))
        
        if selected_incident_key:
            incident = incident_options[selected_incident_key]
            
            with st.form("edit_incident_form"):
                new_title = st.text_input("Title", value=incident.get_title())
                new_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"], 
                                          index=["Low", "Medium", "High", "Critical"].index(incident.get_severity()) 
                                          if incident.get_severity() in ["Low", "Medium", "High", "Critical"] else 0)
                new_status = st.selectbox("Status", ["open", "in progress", "closed", "resolved"], 
                                        index=["open", "in progress", "closed", "resolved"].index(incident.get_status()) 
                                        if incident.get_status() in ["open", "in progress", "closed", "resolved"] else 0)
                new_date = st.text_input("Date (YYYY-MM-DD)", value=incident.get_date())
                
                submitted = st.form_submit_button("Update Incident")
                if submitted:
                    db.update_incident(incident.get_id(), new_title, new_severity, new_status, new_date)
                    st.success("Incident updated successfully!")
                    st.rerun()
    else:
        st.info("No incidents to edit.")

#Delete incident
with tab3:
    if incidents:
        st.subheader("Delete Incident")
        delete_options = [f"{incident.get_id()}: {incident.get_title()}" for incident in incidents]
        incident_to_delete = st.selectbox("Select Incident to Delete", delete_options)
        
        if incident_to_delete and st.button("Delete Incident", type="primary"):
            incident_id = int(incident_to_delete.split(":")[0])
            db.delete_incident(incident_id)
            st.success("Incident deleted successfully!")
            st.rerun()
    else:
        st.info("No incidents to delete.")

# Datasets Section
st.header("📁 Datasets")

dataset_data = db.get_all_datasets()
datasets = []
for data in dataset_data:
    datasets.append(Dataset(
        dataset_id=data["id"],
        name=data["name"],
        source=data["source"],
        category=data["category"],
        size=data["size"]
    ))

#Display datasets
if datasets:
    dataset_rows = []
    for dataset in datasets:
        dataset_rows.append({
            "ID": dataset.get_id(),
            "Name": dataset.get_name(),
            "Source": dataset.get_source(),
            "Category": dataset.get_category(),
            "Size (MB)": dataset.get_size(),
            "Size Formatted": f"{dataset.calculate_size_mb()} MB"
        })
    
    df_datasets = pd.DataFrame(dataset_rows)
    st.dataframe(df_datasets, use_container_width=True, hide_index=True)
else:
    st.info("No datasets found.")

# CRUD Operations for Datasets (Add Dataset, Edit Dataset, Delete Dataset)
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
                db.insert_dataset(name, source, category, size)
                st.success("Dataset added successfully!")
                st.rerun()

with tab5:
    if datasets:
        st.subheader("Edit Existing Dataset")
        dataset_options = {f"{dataset.get_id()}: {dataset.get_name()}": dataset for dataset in datasets}
        selected_dataset_key = st.selectbox("Select Dataset to Edit", list(dataset_options.keys()))
        
        if selected_dataset_key:
            dataset = dataset_options[selected_dataset_key]
            
            with st.form("edit_dataset_form"):
                new_name = st.text_input("Name", value=dataset.get_name())
                new_source = st.text_input("Source", value=dataset.get_source())
                new_category = st.selectbox("Category", ["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Other"],
                                          index=["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Other"].index(dataset.get_category())
                                          if dataset.get_category() in ["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Other"] else 0)
                new_size = st.number_input("Size (MB)", min_value=1, value=dataset.get_size())
                
                submitted = st.form_submit_button("Update Dataset")
                if submitted:
                    db.update_dataset(dataset.get_id(), new_name, new_source, new_category, new_size)
                    st.success("Dataset updated successfully!")
                    st.rerun()
    else:
        st.info("No datasets to edit.")

with tab6:
    if datasets:
        st.subheader("Delete Dataset")
        delete_options = [f"{dataset.get_id()}: {dataset.get_name()}" for dataset in datasets]
        dataset_to_delete = st.selectbox("Select Dataset to Delete", delete_options)
        
        if dataset_to_delete and st.button("Delete Dataset", type="primary"):
            dataset_id = int(dataset_to_delete.split(":")[0])
            db.delete_dataset(dataset_id)
            st.success("Dataset deleted successfully!")
            st.rerun()
    else:
        st.info("No datasets to delete.")

# IT Tickets Section
st.header("IT Tickets")

ticket_data = db.get_all_tickets()
tickets = []
for data in ticket_data:
    tickets.append(ITTicket(
        ticket_id=data["id"],
        title=data["title"],
        priority=data["priority"],
        status=data["status"],
        created_date=data["created_date"]
    ))

if tickets:
    ticket_rows = []
    for ticket in tickets:
        ticket_rows.append({
            "ID": ticket.get_id(),
            "Title": ticket.get_title(),
            "Priority": ticket.get_priority(),
            "Status": ticket.get_status(),
            "Created Date": ticket.get_created_date()
        })
    
    df_tickets = pd.DataFrame(ticket_rows)
    st.dataframe(df_tickets, use_container_width=True, hide_index=True)
else:
    st.info("No tickets found.")

# CRUD Operations for Tickets (Add Ticket, Edit Ticket, Delete Ticket)
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
                db.insert_ticket(title, priority, status, created_date.isoformat())
                st.success("Ticket added successfully!")
                st.rerun()

with tab8:
    if tickets:
        st.subheader("Edit Existing Ticket")
        ticket_options = {f"{ticket.get_id()}: {ticket.get_title()}": ticket for ticket in tickets}
        selected_ticket_key = st.selectbox("Select Ticket to Edit", list(ticket_options.keys()))
        
        if selected_ticket_key:
            ticket = ticket_options[selected_ticket_key]
            
            with st.form("edit_ticket_form"):
                new_title = st.text_input("Title", value=ticket.get_title())
                new_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"],
                                          index=["Low", "Medium", "High", "Critical"].index(ticket.get_priority())
                                          if ticket.get_priority() in ["Low", "Medium", "High", "Critical"] else 0)
                new_status = st.selectbox("Status", ["open", "in progress", "closed", "resolved"],
                                        index=["open", "in progress", "closed", "resolved"].index(ticket.get_status())
                                        if ticket.get_status() in ["open", "in progress", "closed", "resolved"] else 0)
                new_date = st.text_input("Created Date (YYYY-MM-DD)", value=ticket.get_created_date())
                
                submitted = st.form_submit_button("Update Ticket")
                if submitted:
                    db.update_ticket(ticket.get_id(), new_title, new_priority, new_status, new_date)
                    st.success("Ticket updated successfully!")
                    st.rerun()
    else:
        st.info("No tickets to edit.")

with tab9:
    if tickets:
        st.subheader("Delete Ticket")
        delete_options = [f"{ticket.get_id()}: {ticket.get_title()}" for ticket in tickets]
        ticket_to_delete = st.selectbox("Select Ticket to Delete", delete_options)
        
        if ticket_to_delete and st.button("Delete Ticket", type="primary"):
            ticket_id = int(ticket_to_delete.split(":")[0])
            db.delete_ticket(ticket_id)
            st.success("Ticket deleted successfully!")
            st.rerun()
    else:
        st.info("No tickets to delete.")

# User Management Section
current_user_data = db.get_user(st.session_state.username)
if current_user_data and current_user_data["role"] == "admin":
    st.header("User Management")
    
    users = auth.get_all_users()
    if users:
        df_users = pd.DataFrame(users)
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
                    auth.update_user_role(user_id, new_role)
                    st.success("User role updated!")
                    st.rerun()
            
            with col2:
                if user_data["username"] != st.session_state.username:  
                    if st.button("Delete User", type="secondary"):
                        auth.delete_user(user_id)
                        st.success("User deleted!")
                        st.rerun()
                else:
                    st.warning("You cannot delete your own account while logged in.")
else:
    # Show current user info for non-admins
    if current_user_data:
        with st.expander("My personal Account Info"):
            st.write(f"**Username:** {current_user_data['username']}")
            st.write(f"**Role:** {current_user_data['role']}")
            st.write(f"**Member Since:** {current_user_data.get('created_at', 'N/A')}")

# Navigation
st.divider()
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📊 Analytics"):
        st.switch_page("pages/3_📊_Data_Science.py")
with col2:
    if st.button("🔍 AI Analyzer"):
        st.switch_page("pages/4_💻_IT_Operations.py")
with col3:
    if st.button("💬 Chat"):
        st.switch_page("pages/5_🤖_AI_Assistant.py")
with col4:
    if st.button("🏠 Home"):
        st.switch_page("Home.py")

# Logout button
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_role = ""
    st.session_state.user_obj = None
    st.info("You have been logged out")
    st.switch_page("Home.py")