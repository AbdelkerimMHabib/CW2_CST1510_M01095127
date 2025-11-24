
import streamlit as st
import pandas as pd
import numpy as np
from utils.database import connect_database, add_data, get_data, update_data, delete_data

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

# Connect to the database
conn = connect_database('DATA/intelligence_platform.db')

# Dashboard Page
st.title("📊 Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    n_points = st.slider("Number of data points", 10, 200, 50)

# Generate and display demo data
data = pd.DataFrame(
    np.random.randn(n_points, 3),
    columns=["A", "B", "C"]
)

# Save data to the database 
if st.button("Save Data to Database"):
    for index, row in data.iterrows():
        add_data(conn, row['A'], row['B'], row['C']) 

st.subheader("Data")
if st.button("Load Data from Database"):
    loaded_data = get_data(conn)
    st.write(loaded_data)

# CRUD Operations
st.subheader("CRUD Operations")

# Update data
update_column = st.selectbox("Select row to update", range(len(data)))
new_value = st.number_input("New Value", value=data.at[update_column, 'A'])

if st.button("Update Data"):
    update_data(conn, update_column, new_value)
    st.success("Data updated successfully!")

# Delete data
delete_index = st.selectbox("Select row to delete", range(len(data)))
if st.button("Delete Data"):
    delete_data(conn, delete_index)
    st.success("Data deleted successfully!")

# Logout section
st.divider()

if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Home.py")
