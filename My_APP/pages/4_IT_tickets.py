import streamlit as st
import pandas as pd
from utils.database import connect_database, get_all_tickets, insert_ticket, update_ticket, delete_ticket

# Check login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    st.stop()

st.title("💻 IT Tickets Management")

conn = connect_database()
tickets = get_all_tickets(conn)

# --- ADD NEW TICKET ---
with st.expander("Add New Ticket"):
    title = st.text_input("Title", key="new_title")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"], key="new_priority")
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"], key="new_status")
    created_date = st.date_input("Created Date", key="new_date")

    if st.button("Add Ticket"):
        if title:
            insert_ticket(conn, title, priority, status, created_date.strftime("%Y-%m-%d"))
            st.success("Ticket added successfully!")
            st.experimental_rerun()
        else:
            st.warning("Title is required!")

st.markdown("---")

# --- LIST / EDIT / DELETE TICKETS ---
if tickets:
    df_tk = pd.DataFrame(tickets, columns=["id","title","priority","status","created_date"])
    for idx, row in df_tk.iterrows():
        with st.expander(f"Ticket: {row['title']}"):
            new_title = st.text_input("Title", value=row["title"], key=f"title_{row['id']}")

            priority_options = ["Low", "Medium", "High"]
            try:
                prio_idx = priority_options.index(row["priority"])
            except ValueError:
                prio_idx = 0
            new_priority = st.selectbox("Priority", priority_options, index=prio_idx, key=f"prio_{row['id']}")

            status_options = ["Open", "In Progress", "Resolved", "Closed"]
            try:
                status_idx = status_options.index(row["status"])
            except ValueError:
                status_idx = 0
            new_status = st.selectbox("Status", status_options, index=status_idx, key=f"status_{row['id']}")

            new_date = st.date_input("Created Date", pd.to_datetime(row["created_date"]), key=f"date_{row['id']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update", key=f"update_{row['id']}"):
                    update_ticket(conn, row["id"], new_title, new_priority, new_status, new_date.strftime("%Y-%m-%d"))
                    st.success("Ticket updated!")
                    st.experimental_rerun()
            with col2:
                if st.button("Delete", key=f"delete_{row['id']}"):
                    delete_ticket(conn, row["id"])
                    st.success("Ticket deleted!")
                    st.experimental_rerun()
else:
    st.info("No tickets yet.")
