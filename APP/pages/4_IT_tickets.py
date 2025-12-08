import streamlit as st
import pandas as pd
from utils.database import connect_database, get_all_tickets, insert_ticket, update_ticket, delete_ticket, get_tickets_by_priority, get_tickets_by_status
from utils.openai_client import openai_client
from datetime import datetime, timedelta

# Login check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()

# Page config
st.set_page_config(page_title="IT Tickets", page_icon="💻", layout="wide")

st.title("💻 IT Tickets Management")

conn = connect_database()
tickets = get_all_tickets(conn)

# Sidebar filters
with st.sidebar:
    st.subheader("Filters")
    
    # Priority filter
    priorities = ["All", "High", "Medium", "Low"]
    selected_priority = st.selectbox("Filter by Priority", priorities)
    
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
    # Add new ticket
    with st.expander("➕ Add New Ticket", expanded=False):
        with st.form("add_ticket_form"):
            title = st.text_input("Title*")
            priority = st.selectbox("Priority*", ["Low", "Medium", "High"])
            status = st.selectbox("Status*", ["Open", "In Progress", "Resolved", "Closed"])
            created_date = st.date_input("Created Date*", datetime.now())
            assigned_to = st.text_input("Assigned to (optional)")
            description = st.text_area("Description", height=100)
            
            if st.form_submit_button("Add Ticket", use_container_width=True):
                if title:
                    insert_ticket(conn, title, priority, status, created_date.strftime("%Y-%m-%d"), 
                                 assigned_to, description, st.session_state.username)
                    st.success("Ticket added successfully!")
                    st.rerun()
                else:
                    st.error("Title is required!")

with col2:
    # Quick stats
    st.subheader("Quick Stats")
    if tickets:
        df_tk = pd.DataFrame(tickets, columns=["ID", "Title", "Priority", "Status", "Created Date", "Assigned To", "Description", "Resolution", "Updated"])
        high_priority = len(df_tk[df_tk["Priority"] == "High"])
        open_count = len(df_tk[df_tk["Status"] == "Open"])
        st.metric("High Priority", high_priority)
        st.metric("Open", open_count)
    else:
        st.info("No tickets")

st.markdown("---")

# Display tickets
if tickets:
    df_tk = pd.DataFrame(tickets, columns=["ID", "Title", "Priority", "Status", "Created Date", "Assigned To", "Description", "Resolution", "Updated"])
    
    # Apply filters
    if selected_priority != "All":
        df_tk = df_tk[df_tk["Priority"] == selected_priority]
    if selected_status != "All":
        df_tk = df_tk[df_tk["Status"] == selected_status]
    if len(date_range) == 2:
        df_tk = df_tk[(pd.to_datetime(df_tk["Created Date"]) >= pd.to_datetime(date_range[0])) & 
                     (pd.to_datetime(df_tk["Created Date"]) <= pd.to_datetime(date_range[1]))]
    
    # Display table
    st.dataframe(df_tk[["Title", "Priority", "Status", "Created Date", "Assigned To"]], 
                use_container_width=True, hide_index=True)
    
    # Bulk AI Analysis
    if st.session_state.get("show_bulk_analysis", False):
        st.markdown("---")
        st.subheader("🤖 Bulk AI Analysis")
        
        if st.button("Generate Analysis Report", use_container_width=True):
            with st.spinner("AI is analyzing all tickets..."):
                analysis_prompt = f"""
                Analyze these {len(df_tk)} IT support tickets:
                
                {df_tk[['Title', 'Priority', 'Status', 'Created Date', 'Assigned To']].to_string()}
                
                Provide:
                1. Overall IT health assessment
                2. Top 3 recurring issues
                3. Staffing/resource recommendations
                4. Process improvement suggestions
                5. SLA compliance analysis
                """
                
                analysis = openai_client.chat([
                    {"role": "system", "content": "You are an IT Operations Manager."},
                    {"role": "user", "content": analysis_prompt}
                ])
                
                if analysis:
                    st.markdown(analysis)
                    
                    # Export option
                    st.download_button(
                        label="📥 Download Analysis Report",
                        data=analysis,
                        file_name=f"it_tickets_analysis_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Could not generate analysis. Check API configuration.")
        
        if st.button("Close Analysis"):
            del st.session_state.show_bulk_analysis
            st.rerun()
    
    # Edit/Delete individual tickets
    st.markdown("---")
    st.subheader("Edit Ticket")
    
    ticket_ids = df_tk["ID"].tolist()
    if ticket_ids:
        selected_id = st.selectbox("Select Ticket ID to edit", ticket_ids)
        selected_tk = df_tk[df_tk["ID"] == selected_id].iloc[0]
        
        with st.form("edit_ticket_form"):
            new_title = st.text_input("Title", value=selected_tk["Title"])
            new_priority = st.selectbox("Priority", ["Low", "Medium", "High"], 
                                      index=["Low", "Medium", "High"].index(selected_tk["Priority"]) 
                                      if selected_tk["Priority"] in ["Low", "Medium", "High"] else 0)
            new_status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"], 
                                    index=["Open", "In Progress", "Resolved", "Closed"].index(selected_tk["Status"]) 
                                    if selected_tk["Status"] in ["Open", "In Progress", "Resolved", "Closed"] else 0)
            new_date = st.date_input("Created Date", pd.to_datetime(selected_tk["Created Date"]))
            new_assigned = st.text_input("Assigned to", value=selected_tk["Assigned To"] if selected_tk["Assigned To"] else "")
            new_description = st.text_area("Description", value=selected_tk["Description"] if selected_tk["Description"] else "")
            new_resolution = st.text_area("Resolution", value=selected_tk["Resolution"] if selected_tk["Resolution"] else "")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Update Ticket", use_container_width=True):
                    update_ticket(conn, selected_id, new_title, new_priority, new_status, 
                                new_date.strftime("%Y-%m-%d"), new_assigned, new_description, 
                                new_resolution, st.session_state.username)
                    st.success("Ticket updated!")
                    st.rerun()
            with col2:
                if st.button("Delete Ticket", key=f"delete_{selected_id}", use_container_width=True):
                    delete_ticket(conn, selected_id, st.session_state.username)
                    st.success("Ticket deleted!")
                    st.rerun()
    else:
        st.info("No tickets match the filters")
else:
    st.info("No tickets yet. Add your first ticket above.")

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