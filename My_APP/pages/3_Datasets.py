import streamlit as st
import pandas as pd
from utils.database import (connect_database, insert_dataset, get_all_datasets, get_dataset,
                            update_dataset, delete_dataset)

conn = connect_database()
st.title("📂 Datasets")

# Add new dataset
with st.expander("➕ Add dataset"):
    with st.form("add_ds"):
        name = st.text_input("Name")
        source = st.text_input("Source")
        category = st.text_input("Category")
        size = st.number_input("Size (MB)", min_value=0)
        if st.form_submit_button("Add"):
            insert_dataset(conn, name, source, category, int(size))
            st.success("Dataset added.")
            st.experimental_rerun()

# Show datasets
datasets = get_all_datasets(conn)
df = pd.DataFrame(datasets, columns=["id","name","source","category","size"]) if datasets else pd.DataFrame(columns=["id","name","source","category","size"])
st.dataframe(df, use_container_width=True)

# Edit / delete
if not df.empty:
    st.subheader("Edit / Delete dataset")
    sel = st.selectbox("Select dataset id", df['id'].tolist())
    rec = get_dataset(conn, int(sel))
    if rec:
        id_, name, source, category, size = rec
        with st.form("edit_ds"):
            n = st.text_input("Name", value=name)
            s = st.text_input("Source", value=source)
            c = st.text_input("Category", value=category)
            sz = st.number_input("Size (MB)", min_value=0, value=int(size))
            if st.form_submit_button("Update"):
                if st.session_state.get("role","user") == "admin":
                    update_dataset(conn, id_, n, s, c, int(sz))
                    st.success("Updated.")
                    st.experimental_rerun()
                else:
                    st.error("Only admin can update datasets.")
        if st.session_state.get("role","user") == "admin":
            if st.button("Delete dataset"):
                delete_dataset(conn, id_)
                st.success("Deleted.")
                st.experimental_rerun()
        else:
            st.info("Only admin can delete datasets.")
else:
    st.info("No datasets available.")
