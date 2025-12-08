import streamlit as st
import pandas as pd
from utils.database import connect_database, get_all_incidents, insert_incident, update_incident, delete_incident

# Check login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    st.stop()

st.title("🛡️ Cyber Incidents Management")

conn = connect_database()
incidents = get_all_incidents(conn)

# --- ADD NEW INCIDENT ---
with st.expander("Add New Incident"):
    title = st.text_input("Title", key="new_title")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"], key="new_severity")
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"], key="new_status")
    date = st.date_input("Date", key="new_date")

    if st.button("Add Incident"):
        if title:
            insert_incident(conn, title, severity, status, date.strftime("%Y-%m-%d"))
            st.success("Incident added successfully!")
            st.experimental_rerun()
        else:
            st.warning("Title is required!")

st.markdown("---")

# --- LIST / EDIT / DELETE INCIDENTS ---
if incidents:
    df_inc = pd.DataFrame(incidents, columns=["id","title","severity","status","date"])
    for idx, row in df_inc.iterrows():
        with st.expander(f"Incident: {row['title']}"):
            new_title = st.text_input("Title", value=row["title"], key=f"title_{row['id']}")

            severity_options = ["Low", "Medium", "High", "Critical"]
            try:
                sev_idx = severity_options.index(row["severity"])
            except ValueError:
                sev_idx = 0
            new_severity = st.selectbox("Severity", severity_options, index=sev_idx, key=f"sev_{row['id']}")

            status_options = ["Open", "In Progress", "Resolved", "Closed"]
            try:
                status_idx = status_options.index(row["status"])
            except ValueError:
                status_idx = 0
            new_status = st.selectbox("Status", status_options, index=status_idx, key=f"status_{row['id']}")

            new_date = st.date_input("Date", pd.to_datetime(row["date"]), key=f"date_{row['id']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update", key=f"update_{row['id']}"):
                    update_incident(conn, row["id"], new_title, new_severity, new_status, new_date.strftime("%Y-%m-%d"))
                    st.success("Incident updated!")
                    st.experimental_rerun()
            with col2:
                if st.button("Delete", key=f"delete_{row['id']}"):
                    delete_incident(conn, row["id"])
                    st.success("Incident deleted!")
                    st.experimental_rerun()
else:
    st.info("No incidents yet.")
