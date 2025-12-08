import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

from utils.auth import hash_password, verify_password
from utils.database import connect_database, add_user, get_user


st.set_page_config(
    page_title="Login / Register",
    page_icon="🔑",
    layout="centered"
)

conn = connect_database('DATA/intelligence.db')  


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🔐 Welcome")


if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to dashboard"):
        st.switch_page("1_Dashboard")  
    st.stop()

tab_login, tab_register = st.tabs(["Login", "Register"])


with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")

    if st.button("Log in"):
        user = get_user(conn, login_username)

        if user and verify_password(login_password, user[2]):
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success("Login successful!")
            st.switch_page("1_Dashboard.py")
        else:
            st.error("Invalid username or password.")


with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                password_hash = hash_password(new_password)
                add_user(conn, new_username, password_hash)
                st.success("Account created successfully!")
                st.info("Go to Login tab.")
            except Exception as e:
                st.error("Username already exists or an error occurred.")
                st.write(f"Debug: {e}")  

