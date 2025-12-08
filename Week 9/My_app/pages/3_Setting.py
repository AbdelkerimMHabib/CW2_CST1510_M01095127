# My_app/pages/3_Settings.py
import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("⚙️ Settings")
theme = st.radio("Select theme", ["Light", "Dark"], index=0)
notifications = st.checkbox("Enable notifications", value=True)

st.write("Theme:", theme)
st.write("Notifications:", notifications)

st.divider()
if st.button("Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")
