import streamlit as st
import pandas as pd
import altair as alt
from utils.database import connect_database, get_all_incidents, get_all_datasets, get_all_tickets

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to Home"):
        st.experimental_rerun()
    st.stop()

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Multi-Domain Dashboard")
conn = connect_database()

# Load data
incidents = get_all_incidents(conn)
datasets = get_all_datasets(conn)
tickets = get_all_tickets(conn)

# Convert to dataframes safely
df_inc = pd.DataFrame(incidents, columns=["id","title","severity","status","date"]) if incidents else pd.DataFrame(columns=["id","title","severity","status","date"])
df_ds = pd.DataFrame(datasets, columns=["id","name","source","category","size"]) if datasets else pd.DataFrame(columns=["id","name","source","category","size"])
df_tk = pd.DataFrame(tickets, columns=["id","title","priority","status","created_date"]) if tickets else pd.DataFrame(columns=["id","title","priority","status","created_date"])

# Metrics row
c1, c2, c3 = st.columns(3)
c1.metric("Total Incidents", len(df_inc))
c2.metric("Total Datasets", len(df_ds))
c3.metric("Total Tickets", len(df_tk))

st.markdown("---")

# Cybersecurity visuals
st.subheader("Cybersecurity")
col1, col2 = st.columns([2,1])
with col1:
    if not df_inc.empty:
        st.metric("Open incidents", int((df_inc['status'].str.lower() == "open").sum()))
        chart = alt.Chart(df_inc).mark_bar().encode(
            x=alt.X('severity:N', sort='-y'),
            y='count()',
            color='severity:N'
        ).properties(width=600, height=300)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No incidents yet.")

with col2:
    if not df_inc.empty:
        pie = alt.Chart(df_inc).mark_arc().encode(
            theta=alt.Theta(field="severity", type="quantitative", aggregate='count'),
            color="severity:N"
        )
        st.altair_chart(pie, use_container_width=True)

st.markdown("---")

# Datasets visuals
st.subheader("Datasets")
col1, col2 = st.columns([2,1])
with col1:
    if not df_ds.empty:
        st.metric("Total dataset size (MB)", int(df_ds["size"].sum()))
        ds_bar = alt.Chart(df_ds).mark_bar().encode(
            x=alt.X('category:N', sort='-y'),
            y='count()',
            color='category:N'
        ).properties(width=600, height=300)
        st.altair_chart(ds_bar, use_container_width=True)
    else:
        st.info("No datasets yet.")
with col2:
    if not df_ds.empty:
        size_by_cat = df_ds.groupby("category")["size"].sum().reset_index()
        ds_pie = alt.Chart(size_by_cat).mark_arc().encode(
            theta='size:Q', color='category:N'
        )
        st.altair_chart(ds_pie, use_container_width=True)

st.markdown("---")

# IT visuals
st.subheader("IT Tickets")
col1, col2 = st.columns([2,1])
with col1:
    if not df_tk.empty:
        st.metric("Open tickets", int((df_tk['status'].str.lower() == "open").sum()))
        tk_bar = alt.Chart(df_tk).mark_bar().encode(
            x='priority:N',
            y='count()',
            color='priority:N'
        ).properties(width=600, height=300)
        st.altair_chart(tk_bar, use_container_width=True)
    else:
        st.info("No tickets yet.")
with col2:
    if not df_tk.empty:
        st.altair_chart(alt.Chart(df_tk).mark_arc().encode(
            theta=alt.Theta(field="priority", type="quantitative", aggregate='count'),
            color='priority:N'
        ), use_container_width=True)

st.markdown("---")
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.experimental_rerun()
