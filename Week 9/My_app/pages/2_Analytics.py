# My_app/pages/2_Analytics.py
import streamlit as st
import pandas as pd
import numpy as np
from utils.database import connect_database, get_all_datasets

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("📈 Analytics Dashboard")

conn = connect_database()
datasets = get_all_datasets(conn)
if datasets:
    df = pd.DataFrame([dict(r) for r in datasets])
    st.subheader("Datasets metadata")
    st.dataframe(df, use_container_width=True)

    st.subheader("Dataset sizes distribution")
    st.bar_chart(df.set_index("name")["size"])
else:
    st.info("No dataset metadata available.")

st.divider()
if st.button("Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")
