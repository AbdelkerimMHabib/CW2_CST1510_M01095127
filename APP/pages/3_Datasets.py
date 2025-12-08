import streamlit as st
import pandas as pd
from utils.database import connect_database, get_all_datasets, insert_dataset, update_dataset, delete_dataset, get_datasets_by_category

# Login check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()

# Page config
st.set_page_config(page_title="Datasets", page_icon="📂", layout="wide")

conn = connect_database()
st.title("📂 Datasets Management")

# Add new dataset
with st.expander("➕ Add New Dataset", expanded=True):
    with st.form("add_ds_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name*")
            source = st.text_input("Source*")
        with col2:
            category = st.selectbox("Category*", ["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Network", "Other"])
            size = st.number_input("Size (MB)*", min_value=0)
        
        format_type = st.text_input("Format (optional)")
        
        if st.form_submit_button("Add Dataset", use_container_width=True):
            if name and source and category:
                insert_dataset(conn, name, source, category, int(size), format_type, st.session_state.username)
                st.success("Dataset added successfully!")
                st.rerun()
            else:
                st.error("Name, Source, and Category are required!")

st.markdown("---")

# Show datasets
datasets = get_all_datasets(conn)
if datasets:
    df = pd.DataFrame(datasets, columns=["ID", "Name", "Source", "Category", "Size", "Format", "Created By", "Created"])
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.multiselect("Filter by Category", df["Category"].unique())
    with col2:
        search_term = st.text_input("Search datasets")
    
    # Apply filters
    filtered_df = df.copy()
    if filter_category:
        filtered_df = filtered_df[filtered_df["Category"].isin(filter_category)]
    if search_term:
        filtered_df = filtered_df[filtered_df["Name"].str.contains(search_term, case=False) | 
                                 filtered_df["Source"].str.contains(search_term, case=False)]
    
    # Display
    st.dataframe(filtered_df[["Name", "Source", "Category", "Size", "Format", "Created By", "Created"]], 
                use_container_width=True, hide_index=True)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Datasets", len(filtered_df))
    with col2:
        st.metric("Total Size", f"{filtered_df['Size'].sum():,} MB")
    with col3:
        st.metric("Categories", len(filtered_df["Category"].unique()))
    
    # Edit/Delete section
    st.markdown("---")
    st.subheader("Edit / Delete Dataset")
    
    dataset_ids = filtered_df["ID"].tolist()
    if dataset_ids:
        selected_id = st.selectbox("Select dataset id", dataset_ids)
        selected_ds = df[df["ID"] == selected_id].iloc[0]
        
        with st.form("edit_ds_form"):
            new_name = st.text_input("Name", value=selected_ds["Name"])
            new_source = st.text_input("Source", value=selected_ds["Source"])
            new_category = st.selectbox("Category", ["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Network", "Other"], 
                                      index=["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Network", "Other"].index(selected_ds["Category"]) 
                                      if selected_ds["Category"] in ["Cybersecurity", "Analytics", "Threat Intel", "Logs", "Network", "Other"] else 0)
            new_size = st.number_input("Size (MB)", min_value=0, value=int(selected_ds["Size"]))
            new_format = st.text_input("Format", value=selected_ds["Format"] if selected_ds["Format"] else "")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Update Dataset", use_container_width=True):
                    update_dataset(conn, selected_id, new_name, new_source, new_category, new_size, new_format, st.session_state.username)
                    st.success("Dataset updated!")
                    st.rerun()
            with col2:
                if st.button("Delete Dataset", use_container_width=True):
                    delete_dataset(conn, selected_id, st.session_state.username)
                    st.success("Dataset deleted!")
                    st.rerun()
    else:
        st.info("No datasets match the filters")
else:
    st.info("No datasets available. Add your first dataset above.")

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
    if st.button("📈 Analytics", use_container_width=True):
        st.switch_page("pages/5_Analytics.py")