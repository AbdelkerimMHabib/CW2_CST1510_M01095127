import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.database import connect_database, get_all_datasets, get_all_incidents, get_all_tickets

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")
st.title("📈 Analytics Dashboard")

conn = connect_database()

# Get data
datasets = get_all_datasets(conn)
incidents = get_all_incidents(conn)
tickets = get_all_tickets(conn)

# Convert to DataFrames
if datasets:
    df_datasets = pd.DataFrame([dict(r) for r in datasets])
else:
    df_datasets = pd.DataFrame()

if incidents:
    df_incidents = pd.DataFrame([dict(r) for r in incidents])
else:
    df_incidents = pd.DataFrame()

if tickets:
    df_tickets = pd.DataFrame([dict(r) for r in tickets])
else:
    df_tickets = pd.DataFrame()

# Tabs for different analytics
tab1, tab2, tab3 = st.tabs(["📁 Datasets", "🔒 Incidents", "🎫 Tickets"])

with tab1:
    st.header("Dataset Analytics")
    
    if not df_datasets.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Dataset by Category
            if 'category' in df_datasets.columns:
                category_counts = df_datasets['category'].value_counts()
                fig1 = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    title="Datasets by Category",
                    hole=0.3
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Dataset sizes
            if 'size' in df_datasets.columns:
                fig2 = px.bar(
                    df_datasets,
                    x='name',
                    y='size',
                    title="Dataset Sizes (MB)",
                    color='category'
                )
                fig2.update_layout(xaxis_title="Dataset", yaxis_title="Size (MB)")
                st.plotly_chart(fig2, use_container_width=True)
        
        # Source distribution
        if 'source' in df_datasets.columns:
            st.subheader("Dataset Sources")
            source_counts = df_datasets['source'].value_counts()
            fig3 = px.bar(
                x=source_counts.index,
                y=source_counts.values,
                title="Datasets by Source"
            )
            fig3.update_layout(xaxis_title="Source", yaxis_title="Count")
            st.plotly_chart(fig3, use_container_width=True)
        
        # Display raw data
        with st.expander("📋 View Raw Dataset Data"):
            st.dataframe(df_datasets, use_container_width=True)
    else:
        st.info("No dataset metadata available.")

with tab2:
    st.header("Incident Analytics")
    
    if not df_incidents.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Incidents by Severity
            if 'severity' in df_incidents.columns:
                severity_counts = df_incidents['severity'].value_counts()
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
            if 'status' in df_incidents.columns:
                status_counts = df_incidents['status'].value_counts()
                fig2 = px.bar(
                    x=status_counts.index,
                    y=status_counts.values,
                    title="Incidents by Status",
                    color=status_counts.index
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # Monthly trend
        if 'date' in df_incidents.columns:
            st.subheader("Incident Trends Over Time")
            df_incidents['date'] = pd.to_datetime(df_incidents['date'])
            df_incidents['month'] = df_incidents['date'].dt.strftime('%Y-%m')
            monthly_counts = df_incidents.groupby('month').size().reset_index(name='count')
            
            fig3 = px.line(
                monthly_counts,
                x='month',
                y='count',
                title="Monthly Incident Count",
                markers=True
            )
            fig3.update_layout(xaxis_title="Month", yaxis_title="Number of Incidents")
            st.plotly_chart(fig3, use_container_width=True)
        
        # Display raw data
        with st.expander("📋 View Raw Incident Data"):
            st.dataframe(df_incidents, use_container_width=True)
    else:
        st.info("No incidents data available.")

with tab3:
    st.header("Ticket Analytics")
    
    if not df_tickets.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Tickets by Priority
            if 'priority' in df_tickets.columns:
                priority_counts = df_tickets['priority'].value_counts()
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
            if 'status' in df_tickets.columns:
                status_counts = df_tickets['status'].value_counts()
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
            open_tickets = len(df_tickets[df_tickets['status'] == 'open']) if 'status' in df_tickets.columns else 0
            st.metric("Open Tickets", open_tickets)
        with col5:
            closed_tickets = len(df_tickets[df_tickets['status'] == 'closed']) if 'status' in df_tickets.columns else 0
            st.metric("Closed Tickets", closed_tickets)
        
        # Display raw data
        with st.expander("📋 View Raw Ticket Data"):
            st.dataframe(df_tickets, use_container_width=True)
    else:
        st.info("No tickets data available.")

# Summary statistics
st.divider()
st.header("📊 Summary Statistics")

if not df_datasets.empty and not df_incidents.empty and not df_tickets.empty:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Incidents", len(df_incidents))
        if 'severity' in df_incidents.columns:
            critical = len(df_incidents[df_incidents['severity'] == 'Critical'])
            st.metric("Critical Incidents", critical)
    
    with col2:
        st.metric("Total Datasets", len(df_datasets))
        if 'size' in df_datasets.columns:
            total_size = df_datasets['size'].sum()
            st.metric("Total Data Size", f"{total_size:,} MB")
    
    with col3:
        st.metric("Total Tickets", len(df_tickets))
        if 'priority' in df_tickets.columns:
            high_priority = len(df_tickets[df_tickets['priority'] == 'High'])
            st.metric("High Priority Tickets", high_priority)

# Navigation
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Back to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
with col2:
    if st.button("🔍 Go to AI Analyzer"):
        st.switch_page("pages/4_AI_Analyzer.py")