# My_app/pages/1_Dashboard.py
import streamlit as st
from utils.database import connect_database, get_all_incidents, insert_incident, update_incident, delete_incident, get_all_datasets, get_all_tickets
import pandas as pd

# Protect page
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


st.header("Cyber Incidents")

incidents = get_all_incidents(conn)
if incidents:
    df_incidents = pd.DataFrame([dict(row) for row in incidents])
    st.dataframe(df_incidents, use_container_width=True)
else:
    st.info("No incidents in the database.")

with st.expander("Add new incident"):
    with st.form("new_incident"):
        title = st.text_input("Incident Title")
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["open", "in progress", "closed", "resolved"])
        date = st.date_input("Date")
        submitted = st.form_submit_button("Add Incident")
        if submitted and title:
            insert_incident(conn, title, severity, status, date.isoformat())
            st.success("Incident added.")
            st.experimental_rerun()

with st.expander("Edit or delete an incident"):
    if incidents:
        options = [f"{r['id']}: {r['title']}" for r in incidents]
        choice = st.selectbox("Pick an incident", options)
        if choice:
            iid = int(choice.split(":")[0])
            inc = next((r for r in incidents if r["id"] == iid), None)
            if inc:
                title_u = st.text_input("Title", inc["title"])
                severity_u = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"], index=["Low","Medium","High","Critical"].index(inc["severity"]) if inc["severity"] in ["Low","Medium","High","Critical"] else 0)
                status_u = st.text_input("Status", inc["status"])
                date_u = st.text_input("Date", inc["date"])
                if st.button("Update incident"):
                    update_incident(conn, iid, title_u, severity_u, status_u, date_u)
                    st.success("Incident updated.")
                    st.experimental_rerun()
                if st.button("Delete incident"):
                    delete_incident(conn, iid)
                    st.success("Incident deleted.")
                    st.experimental_rerun()


st.header("Datasets")
datasets = get_all_datasets(conn)
if datasets:
    df_datasets = pd.DataFrame([dict(r) for r in datasets])
    st.dataframe(df_datasets, use_container_width=True)
else:
    st.info("No datasets found.")

st.header("IT Tickets")
tickets = get_all_tickets(conn)
if tickets:
    df_tickets = pd.DataFrame([dict(r) for r in tickets])
    st.dataframe(df_tickets, use_container_width=True)
else:
    st.info("No tickets found.")


st.divider()
st.subheader("Domain Metrics")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Threats Detected", int(len(incidents)), delta="+0")
with col2:
    vuln_count = df_datasets.shape[0] if 'df_datasets' in locals() else 0
    st.metric("Datasets", vuln_count)
with col3:
    st.metric("IT Tickets", int(len(tickets)), delta="0")

# Logout
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out")
    st.switch_page("Home.py")
