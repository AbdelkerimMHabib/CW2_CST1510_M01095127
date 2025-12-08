import streamlit as st
import pandas as pd
import altair as alt
from utils.database import connect_database, get_all_incidents, get_all_datasets, get_all_tickets
from datetime import datetime

conn = connect_database()
st.title("📈 Analytics - Combined Insights")

# Load
inc = pd.DataFrame(get_all_incidents(conn), columns=["id","title","severity","status","date"])
ds = pd.DataFrame(get_all_datasets(conn), columns=["id","name","source","category","size"])
tk = pd.DataFrame(get_all_tickets(conn), columns=["id","title","priority","status","created_date"])

# sanitize and parse dates
if not inc.empty:
    inc['date'] = pd.to_datetime(inc['date'], errors='coerce')
if not tk.empty:
    tk['created_date'] = pd.to_datetime(tk['created_date'], errors='coerce')

# Filters
st.sidebar.header("Analytics Filters")
domain = st.sidebar.selectbox("Domain", ["All","Cyber","Datasets","IT"])
date_from = st.sidebar.date_input("From", value=pd.to_datetime("2025-01-01"))
date_to = st.sidebar.date_input("To", value=pd.to_datetime(datetime.today().date()))

# Cybersecurity insights
if domain in ("All","Cyber"):
    st.subheader("Cybersecurity Insights")
    if inc.empty:
        st.info("No incidents data")
    else:
        df = inc[(inc['date'] >= pd.to_datetime(date_from)) & (inc['date'] <= pd.to_datetime(date_to))]
        st.metric("Total incidents", len(df))
        st.metric("Open incidents", int((df['status'].str.lower()=="open").sum()))
        # severity bar
        st.markdown("**Severity distribution**")
        st.bar_chart(df['severity'].value_counts())
        # timeline
        st.markdown("**Incidents timeline**")
        timeline = df.groupby(pd.Grouper(key='date', freq='W'))['id'].count().reset_index()
        chart = alt.Chart(timeline).mark_line(point=True).encode(x='date:T', y='id:Q').properties(height=200)
        st.altair_chart(chart, use_container_width=True)
        # heatmap: day-of-week vs severity counts
        df['dow'] = df['date'].dt.day_name()
        heat = df.groupby(['dow','severity']).size().reset_index(name='count')
        if not heat.empty:
            heat_chart = alt.Chart(heat).mark_rect().encode(
                x=alt.X('dow:N', sort=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']),
                y='severity:N',
                color='count:Q',
                tooltip=['dow','severity','count']
            ).properties(height=250)
            st.altair_chart(heat_chart, use_container_width=True)

# Datasets insights
if domain in ("All","Datasets"):
    st.subheader("Datasets Insights")
    if ds.empty:
        st.info("No datasets data")
    else:
        st.metric("Total datasets", len(ds))
        st.metric("Total size (MB)", int(ds['size'].sum()))
        st.markdown("**Datasets by Category**")
        st.bar_chart(ds['category'].value_counts())
        # sizes timeline not relevant; show size distribution
        st.markdown("**Dataset size distribution**")
        st.line_chart(ds.groupby('category')['size'].sum())

# IT insights
if domain in ("All","IT"):
    st.subheader("IT Insights")
    if tk.empty:
        st.info("No tickets data")
    else:
        df = tk[(tk['created_date'] >= pd.to_datetime(date_from)) & (tk['created_date'] <= pd.to_datetime(date_to))]
        st.metric("Open tickets", int((df['status'].str.lower()=="open").sum()))
        st.markdown("**Tickets by Priority**")
        st.bar_chart(df['priority'].value_counts())
        st.markdown("**Tickets timeline**")
        timeline = df.groupby(pd.Grouper(key='created_date', freq='W'))['id'].count().reset_index()
        st.line_chart(timeline.set_index('created_date')['id'])
