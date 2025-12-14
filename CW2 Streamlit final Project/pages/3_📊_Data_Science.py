"""Data Science Analytics using OOP"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident
from models.dataset import Dataset
from models.it_ticket import ITTicket

# Authentication check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("pages/1_🔐_Login.py")
    st.stop()

st.set_page_config(page_title="Data Science Analytics", page_icon="📊", layout="wide")
st.title("📊 Data Science Analytics")

# Initialize services
db = DatabaseManager()

# Get data and convert to objects
incident_data = db.get_all_incidents()
dataset_data = db.get_all_datasets()
ticket_data = db.get_all_tickets()

# Convert to objects
incidents = []
for data in incident_data:
    incidents.append(SecurityIncident(
        incident_id=data["id"],
        title=data["title"],
        severity=data["severity"],
        status=data["status"],
        date=data["date"]
    ))

datasets = []
for data in dataset_data:
    datasets.append(Dataset(
        dataset_id=data["id"],
        name=data["name"],
        source=data["source"],
        category=data["category"],
        size=data["size"]
    ))

tickets = []
for data in ticket_data:
    tickets.append(ITTicket(
        ticket_id=data["id"],
        title=data["title"],
        priority=data["priority"],
        status=data["status"],
        created_date=data["created_date"]
    ))

# Create DataFrames from objects
df_incidents = pd.DataFrame([{
    "ID": inc.get_id(),
    "Title": inc.get_title(),
    "Severity": inc.get_severity(),
    "Status": inc.get_status(),
    "Date": inc.get_date(),
    "Severity_Level": inc.get_severity_level()
} for inc in incidents]) if incidents else pd.DataFrame()

df_datasets = pd.DataFrame([{
    "ID": ds.get_id(),
    "Name": ds.get_name(),
    "Source": ds.get_source(),
    "Category": ds.get_category(),
    "Size_MB": ds.get_size()
} for ds in datasets]) if datasets else pd.DataFrame()

df_tickets = pd.DataFrame([{
    "ID": t.get_id(),
    "Title": t.get_title(),
    "Priority": t.get_priority(),
    "Status": t.get_status(),
    "Created_Date": t.get_created_date()
} for t in tickets]) if tickets else pd.DataFrame()

# Tabs for different analytics
tab1, tab2, tab3 = st.tabs(["📁 Datasets", "🔒 Incidents", "Tickets"])

with tab1:
    st.header("Dataset Analytics")
    
    if not df_datasets.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Dataset by Category
            if 'Category' in df_datasets.columns:
                category_counts = df_datasets['Category'].value_counts()
                fig1 = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    title="Datasets by Category",
                    hole=0.3
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Dataset sizes
            if 'Size_MB' in df_datasets.columns:
                fig2 = px.bar(
                    df_datasets,
                    x='Name',
                    y='Size_MB',
                    title="Dataset Sizes (MB)",
                    color='Category'
                )
                fig2.update_layout(xaxis_title="Dataset", yaxis_title="Size (MB)")
                st.plotly_chart(fig2, use_container_width=True)
        
        # Source distribution
        if 'Source' in df_datasets.columns:
            st.subheader("Dataset Sources")
            source_counts = df_datasets['Source'].value_counts()
            fig3 = px.bar(
                x=source_counts.index,
                y=source_counts.values,
                title="Datasets by Source"
            )
            fig3.update_layout(xaxis_title="Source", yaxis_title="Count")
            st.plotly_chart(fig3, use_container_width=True)
        
        # Size statistics
        st.subheader("Size Statistics")
        if 'Size_MB' in df_datasets.columns:
            col3, col4, col5 = st.columns(3)
            with col3:
                st.metric("Total Size", f"{df_datasets['Size_MB'].sum():,} MB")
            with col4:
                st.metric("Average Size", f"{df_datasets['Size_MB'].mean():.1f} MB")
            with col5:
                st.metric("Largest Dataset", f"{df_datasets['Size_MB'].max():,} MB")
        
        # Display raw data
        with st.expander("View Raw Dataset Data"):
            st.dataframe(df_datasets, use_container_width=True)
    else:
        st.info("No dataset metadata available.")

with tab2:
    st.header("Incident Analytics")
    
    if not df_incidents.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            #Incidents by Severity
            if 'Severity' in df_incidents.columns:
                severity_counts = df_incidents['Severity'].value_counts()
                fig1 = px.pie(
                    values=severity_counts.values,
                    names=severity_counts.index,
                    title="Incidents by Severity",
                    color=severity_counts.index,
                    color_discrete_map={
                        'Critical': 'red',
                        'High': 'orange',
                        'Medium': 'yellow',
                        'Low': 'green'
                    }
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Incidents by Status
            if 'Status' in df_incidents.columns:
                status_counts = df_incidents['Status'].value_counts()
                fig2 = px.bar(
                    x=status_counts.index,
                    y=status_counts.values,
                    title="Incidents by Status",
                    color=status_counts.index
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # Monthly trend
        if 'Date' in df_incidents.columns and not df_incidents.empty:
            st.subheader("Incident Trends Over Time")
            try:
                df_incidents['Date'] = pd.to_datetime(df_incidents['Date'], errors='coerce')
                df_incidents_clean = df_incidents.dropna(subset=['Date'])
                if not df_incidents_clean.empty:
                    df_incidents_clean['month'] = df_incidents_clean['Date'].dt.strftime('%Y-%m')
                    monthly_counts = df_incidents_clean.groupby('month').size().reset_index(name='count')
                    
                    fig3 = px.line(
                        monthly_counts,
                        x='month',
                        y='count',
                        title="Monthly Incident Count",
                        markers=True
                    )
                    fig3.update_layout(xaxis_title="Month", yaxis_title="Number of Incidents")
                    st.plotly_chart(fig3, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not generate time trend: {e}")
        
        # Severity level distribution
        st.subheader("Severity Level Distribution")
        if 'Severity_Level' in df_incidents.columns:
            severity_level_counts = df_incidents['Severity_Level'].value_counts().sort_index()
            fig4 = px.bar(
                x=severity_level_counts.index,
                y=severity_level_counts.values,
                title="Incidents by Severity Level",
                labels={'x': 'Severity Level', 'y': 'Count'}
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        # Display raw data
        with st.expander("View Raw Incident Data"):
            st.dataframe(df_incidents, use_container_width=True)
    else:
        st.info("No incidents data available.")

with tab3:
    st.header("Ticket Analytics")
    
    if not df_tickets.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Tickets by Priority
            if 'Priority' in df_tickets.columns:
                priority_counts = df_tickets['Priority'].value_counts()
                fig1 = px.pie(
                    values=priority_counts.values,
                    names=priority_counts.index,
                    title="Tickets by Priority",
                    color=priority_counts.index,
                    color_discrete_map={
                        'Critical': 'red',
                        'High': 'orange',
                        'Medium': 'yellow',
                        'Low': 'green'
                    }
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Tickets by Status
            if 'Status' in df_tickets.columns:
                status_counts = df_tickets['Status'].value_counts()
                fig2 = px.bar(
                    x=status_counts.index,
                    y=status_counts.values,
                    title="Tickets by Status",
                    color=status_counts.index
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        st.subheader("Ticket Overview")
        
        # Summary metrics
        col3, col4, col5 = st.columns(3)
        with col3:
            st.metric("Total Tickets", len(df_tickets))
        with col4:
            open_tickets = len(df_tickets[df_tickets['Status'] == 'open']) if 'Status' in df_tickets.columns else 0
            st.metric("Open Tickets", open_tickets)
        with col5:
            closed_tickets = len(df_tickets[df_tickets['Status'] == 'closed']) if 'Status' in df_tickets.columns else 0
            st.metric("Closed Tickets", closed_tickets)
        
        # Priority vs Status heatmap
        st.subheader("Priority vs Status Distribution")
        if 'Priority' in df_tickets.columns and 'Status' in df_tickets.columns:
            pivot_table = pd.crosstab(df_tickets['Priority'], df_tickets['Status'])
            fig3 = px.imshow(
                pivot_table,
                text_auto=True,
                title="Priority vs Status Heatmap",
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        # Display raw data
        with st.expander("View Raw Ticket Data"):
            st.dataframe(df_tickets, use_container_width=True)
    else:
        st.info("No tickets data available.")

# Summary statistics
st.divider()
st.header("Summary Statistics")

if not df_datasets.empty and not df_incidents.empty and not df_tickets.empty:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Incidents", len(df_incidents))
        if 'Severity' in df_incidents.columns:
            critical = len(df_incidents[df_incidents['Severity'] == 'Critical'])
            st.metric("Critical Incidents", critical)
    
    with col2:
        st.metric("Total Datasets", len(df_datasets))
        if 'Size_MB' in df_datasets.columns:
            total_size = df_datasets['Size_MB'].sum()
            st.metric("Total Data Size", f"{total_size:,} MB")
    
    with col3:
        st.metric("Total Tickets", len(df_tickets))
        if 'Priority' in df_tickets.columns:
            high_priority = len(df_tickets[df_tickets['Priority'] == 'High'])
            st.metric("High Priority Tickets", high_priority)

# Navigation to different pages
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Back to Dashboard"):
        st.switch_page("pages/2_🛡_Cybersecurity.py")
with col2:
    if st.button("🏠 Home"):
        st.switch_page("Home.py")
with col3:
    if st.button("🔍 AI Analyzer ➡️"):
        st.switch_page("pages/4_💻_IT_Operations.py")