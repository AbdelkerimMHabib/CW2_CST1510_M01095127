import streamlit as st
import pandas as pd
import altair as alt
from utils.database import connect_database, get_all_incidents, get_all_datasets, get_all_tickets
from utils.openai_client import openai_client
from datetime import datetime

# Login check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()

# Page config
st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

conn = connect_database()
st.title("📈 Analytics - Combined Insights")

# Load data
inc = pd.DataFrame(get_all_incidents(conn), columns=["ID", "Title", "Severity", "Status", "Date", "Description", "Created By", "Updated"])
ds = pd.DataFrame(get_all_datasets(conn), columns=["ID", "Name", "Source", "Category", "Size", "Format", "Created By", "Created"])
tk = pd.DataFrame(get_all_tickets(conn), columns=["ID", "Title", "Priority", "Status", "Created Date", "Assigned To", "Description", "Resolution", "Updated"])

# Sanitize and parse dates
if not inc.empty:
    inc['Date'] = pd.to_datetime(inc['Date'], errors='coerce')
if not tk.empty:
    tk['Created Date'] = pd.to_datetime(tk['Created Date'], errors='coerce')

# Sidebar filters
st.sidebar.header("Analytics Filters")
domain = st.sidebar.selectbox("Domain", ["All", "Cyber", "Datasets", "IT"])
date_from = st.sidebar.date_input("From", value=pd.to_datetime("2025-01-01"))
date_to = st.sidebar.date_input("To", value=pd.to_datetime(datetime.today().date()))

# Main content
if domain in ("All", "Cyber"):
    st.subheader("🛡️ Cybersecurity Insights")
    if inc.empty:
        st.info("No incidents data")
    else:
        df = inc[(inc['Date'] >= pd.to_datetime(date_from)) & (inc['Date'] <= pd.to_datetime(date_to))]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total incidents", len(df))
        with col2:
            st.metric("Open incidents", int((df['Status'].str.lower() == "open").sum()))
        with col3:
            critical_count = len(df[df['Severity'] == 'Critical'])
            st.metric("Critical incidents", critical_count, delta_color="inverse")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Severity distribution**")
            severity_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Severity:N', sort='-y'),
                y='count()',
                color='Severity:N'
            ).properties(height=300)
            st.altair_chart(severity_chart, use_container_width=True)
        
        with col2:
            st.markdown("**Status distribution**")
            status_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Status:N', sort='-y'),
                y='count()',
                color='Status:N'
            ).properties(height=300)
            st.altair_chart(status_chart, use_container_width=True)
        
        # Timeline
        st.markdown("**Incidents timeline**")
        if not df.empty:
            timeline = df.groupby(pd.Grouper(key='Date', freq='W'))['ID'].count().reset_index()
            timeline_chart = alt.Chart(timeline).mark_line(point=True).encode(
                x='Date:T',
                y='ID:Q',
                tooltip=['Date:T', 'ID:Q']
            ).properties(height=200)
            st.altair_chart(timeline_chart, use_container_width=True)
        
        # Heatmap: day-of-week vs severity counts
        st.markdown("**Weekly Pattern Heatmap**")
        df_heat = df.copy()
        df_heat['Day'] = df_heat['Date'].dt.day_name()
        df_heat['Week'] = df_heat['Date'].dt.isocalendar().week
        
        if not df_heat.empty:
            heat_data = df_heat.groupby(['Day', 'Severity']).size().reset_index(name='Count')
            heat_chart = alt.Chart(heat_data).mark_rect().encode(
                x=alt.X('Day:N', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
                y='Severity:N',
                color='Count:Q',
                tooltip=['Day', 'Severity', 'Count']
            ).properties(height=250)
            st.altair_chart(heat_chart, use_container_width=True)

if domain in ("All", "Datasets"):
    st.subheader("📂 Datasets Insights")
    if ds.empty:
        st.info("No datasets data")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total datasets", len(ds))
        with col2:
            st.metric("Total size", f"{ds['Size'].sum():,} MB")
        with col3:
            st.metric("Categories", len(ds['Category'].unique()))
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Datasets by Category**")
            category_chart = alt.Chart(ds).mark_bar().encode(
                x=alt.X('Category:N', sort='-y'),
                y='count()',
                color='Category:N'
            ).properties(height=300)
            st.altair_chart(category_chart, use_container_width=True)
        
        with col2:
            st.markdown("**Size Distribution by Category**")
            size_by_cat = ds.groupby('Category')['Size'].sum().reset_index()
            size_chart = alt.Chart(size_by_cat).mark_arc().encode(
                theta='Size:Q',
                color='Category:N',
                tooltip=['Category', 'Size']
            ).properties(height=300)
            st.altair_chart(size_chart, use_container_width=True)
        
        # Source analysis
        st.markdown("**Data Sources**")
        source_counts = ds['Source'].value_counts().reset_index()
        source_chart = alt.Chart(source_counts.head(10)).mark_bar().encode(
            x=alt.X('count:Q', title='Number of Datasets'),
            y=alt.Y('Source:N', sort='-x'),
            color=alt.Color('count:Q', scale=alt.Scale(scheme='blues'))
        ).properties(height=400)
        st.altair_chart(source_chart, use_container_width=True)

if domain in ("All", "IT"):
    st.subheader("💻 IT Insights")
    if tk.empty:
        st.info("No tickets data")
    else:
        df = tk[(tk['Created Date'] >= pd.to_datetime(date_from)) & (tk['Created Date'] <= pd.to_datetime(date_to))]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total tickets", len(df))
        with col2:
            st.metric("Open tickets", int((df['Status'].str.lower() == "open").sum()))
        with col3:
            avg_resolution = len(df[df['Status'] == 'Closed']) / len(df) * 100 if len(df) > 0 else 0
            st.metric("Resolution Rate", f"{avg_resolution:.1f}%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Tickets by Priority**")
            priority_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Priority:N', sort=['High', 'Medium', 'Low']),
                y='count()',
                color='Priority:N'
            ).properties(height=300)
            st.altair_chart(priority_chart, use_container_width=True)
        
        with col2:
            st.markdown("**Tickets by Status**")
            status_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Status:N', sort=['Open', 'In Progress', 'Resolved', 'Closed']),
                y='count()',
                color='Status:N'
            ).properties(height=300)
            st.altair_chart(status_chart, use_container_width=True)
        
        # Timeline
        st.markdown("**Tickets timeline**")
        if not df.empty:
            timeline = df.groupby(pd.Grouper(key='Created Date', freq='W'))['ID'].count().reset_index()
            timeline_chart = alt.Chart(timeline).mark_line(point=True).encode(
                x='Created Date:T',
                y='ID:Q',
                tooltip=['Created Date:T', 'ID:Q']
            ).properties(height=200)
            st.altair_chart(timeline_chart, use_container_width=True)

# AI-Powered Insights
st.markdown("---")
st.subheader("🤖 AI-Powered Insights")

if st.button("Generate AI Insights Report", use_container_width=True):
    with st.spinner("AI is analyzing all data and generating insights..."):
        # Prepare data summary
        data_summary = f"""
        DATA SUMMARY FOR ANALYSIS:
        
        CYBERSECURITY DOMAIN:
        - Total incidents: {len(inc)}
        - Open incidents: {int((inc['Status'].str.lower() == "open").sum()) if not inc.empty else 0}
        - Severity distribution: {dict(inc['Severity'].value_counts()) if not inc.empty else 'No data'}
        
        DATASETS DOMAIN:
        - Total datasets: {len(ds)}
        - Total data size: {int(ds['Size'].sum()) if not ds.empty else 0} MB
        - Categories: {list(ds['Category'].unique()) if not ds.empty else 'No data'}
        
        IT OPERATIONS DOMAIN:
        - Total tickets: {len(tk)}
        - Open tickets: {int((tk['Status'].str.lower() == "open").sum()) if not tk.empty else 0}
        - Priority distribution: {dict(tk['Priority'].value_counts()) if not tk.empty else 'No data'}
        
        TIME PERIOD: {date_from} to {date_to}
        """
        
        analysis = openai_client.chat([
            {"role": "system", "content": "You are a business intelligence analyst with expertise in multi-domain platform analysis. Provide executive insights and actionable recommendations."},
            {"role": "user", "content": f"Analyze this multi-domain intelligence data:\n\n{data_summary}\n\nProvide an executive summary with key findings, risks, opportunities, and recommendations."}
        ])
        
        if analysis:
            st.markdown("### AI-Generated Insights Report")
            st.markdown("---")
            
            # Display with tabs
            tab1, tab2 = st.tabs(["📄 Full Report", "📋 Key Points"])
            
            with tab1:
                st.markdown(analysis)
            
            with tab2:
                # Extract key points
                key_points = openai_client.chat([
                    {"role": "system", "content": "Extract only the key actionable recommendations as bullet points."},
                    {"role": "user", "content": f"Extract key actionable recommendations from:\n\n{analysis}"}
                ])
                if key_points:
                    st.markdown(key_points)
            
            # Export option
            st.download_button(
                label="📥 Download Insights Report",
                data=analysis,
                file_name=f"ai_insights_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.error("Could not generate AI insights. Check API configuration.")

# Export Data
st.markdown("---")
st.subheader("📤 Export Data")

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    if st.button("Export Incidents to CSV", use_container_width=True):
        if not inc.empty:
            csv = inc.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"cyber_incidents_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.warning("No incidents to export")

with export_col2:
    if st.button("Export Datasets to CSV", use_container_width=True):
        if not ds.empty:
            csv = ds.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"datasets_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.warning("No datasets to export")

with export_col3:
    if st.button("Export Tickets to CSV", use_container_width=True):
        if not tk.empty:
            csv = tk.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"it_tickets_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.warning("No tickets to export")

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
    if st.button("⚙️ Settings", use_container_width=True):
        st.switch_page("pages/6_Settings.py")