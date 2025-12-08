import streamlit as st
import pandas as pd
import plotly.express as px
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from services.ai_assistant import AIAssistant
from services.data_service import DataService
from models.dataset import Dataset

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    st.switch_page("pages/1_🔐_Login.py")

db_manager = DatabaseManager()
auth_manager = AuthManager(db_manager)
ai_assistant = AIAssistant()
data_service = DataService(db_manager)

st.set_page_config(page_title="Data Science", page_icon="📊", layout="wide")
st.title("📊 Data Science Analytics")
st.success(f"Welcome, {st.session_state.username}!")

# Section 1: Overview
st.header("📈 Dataset Overview")
stats = data_service.get_statistics()
datasets = data_service.get_all_datasets()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Datasets", stats["datasets"]["total"])
with col2:
    total_size = stats["datasets"]["total_size"]
    st.metric("Total Size", f"{total_size:,} MB")
with col3:
    if total_size > 1024:
        st.metric("Total Size (GB)", f"{total_size/1024:.1f} GB")
with col4:
    if stats["datasets"]["total"] > 0:
        avg_size = total_size / stats["datasets"]["total"]
        st.metric("Avg Size", f"{avg_size:.0f} MB")

# Section 2: List Datasets
st.header("📁 Datasets")
if datasets:
    dataset_data = []
    for dataset in datasets:
        dataset_data.append({
            "ID": dataset.get_id(),
            "Name": dataset.get_name(),
            "Source": dataset.get_source(),
            "Category": dataset.get_category(),
            "Size (MB)": dataset.get_size_mb(),
            "Size (GB)": f"{dataset.get_size_gb():.2f}",
        })
    df = pd.DataFrame(dataset_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No datasets found.")

# Section 3: Visualizations
if datasets:
    st.header("📊 Dataset Analytics")
    tab1, tab2 = st.tabs(["Category Distribution", "Size Analysis"])
    with tab1:
        category_counts = df['Category'].value_counts().reset_index()
        fig1 = px.pie(category_counts, values='count', names='Category', title='Datasets by Category')
        st.plotly_chart(fig1, use_container_width=True)
    with tab2:
        fig2 = px.bar(df.nlargest(10, 'Size (MB)'), x='Name', y='Size (MB)', color='Category', title='Top 10 Largest Datasets')
        st.plotly_chart(fig2, use_container_width=True)

# ============ AI ANALYZER INTEGRATION SECTION ============
st.header("🤖 AI Dataset Analyzer")

if datasets:
    selected_indices = st.multiselect(
        "Select datasets to analyze",
        options=list(range(len(datasets))),
        format_func=lambda i: f"{datasets[i].get_id()}: {datasets[i].get_name()}",
        max_selections=5
    )
    
    analysis_type = st.selectbox(
        "Analysis Type",
        ["Data Quality Assessment", "Usage Recommendations", 
         "Security Implications", "Integration Potential", "Value Analysis"]
    )
    
    if st.button("Generate AI Analysis", type="primary"):
        if not selected_indices:
            st.warning("Please select datasets to analyze.")
        else:
            selected_dataset_data = []
            for idx in selected_indices:
                dataset = datasets[idx]
                selected_dataset_data.append({
                    "name": dataset.get_name(),
                    "source": dataset.get_source(),
                    "category": dataset.get_category(),
                    "size": dataset.get_size_mb()
                })
            
            with st.spinner("🤖 AI is analyzing datasets..."):
                analysis = ai_assistant.analyze_datasets(selected_dataset_data, analysis_type)
                st.subheader("📋 AI Analysis Report")
                st.markdown(analysis)
                
                report_content = f"Dataset Analysis Report\n\n{analysis}"
                st.download_button(
                    label="📥 Download Report",
                    data=report_content,
                    file_name=f"dataset_analysis_{len(selected_indices)}_datasets.txt",
                    mime="text/plain"
                )
else:
    st.info("No datasets available for analysis.")

# Navigation
st.divider()
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🏠 Home"):
        st.switch_page("Home.py")
with col2:
    if st.button("🛡 Cybersecurity"):
        st.switch_page("pages/2_🛡_Cybersecurity.py")
with col3:
    if st.button("💻 IT Ops"):
        st.switch_page("pages/4_💻_IT_Operations.py")
with col4:
    if st.button("🤖 AI Assistant"):
        st.switch_page("pages/5_🤖_AI_Assistant.py")
with col5:
    if st.button("🔐 Logout", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("pages/1_🔐_Login.py")