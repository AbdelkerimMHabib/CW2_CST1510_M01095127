# My_app/Home.py
import streamlit as st
from utils.auth import hash_password, verify_password
from utils.database import connect_database, add_user, get_user

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "users" not in st.session_state:
    st.session_state.users = {}  

# DB connection
conn = connect_database()

st.set_page_config(page_title="Login / Register", page_icon="🔐", layout="centered")
st.title("🔐 Welcome")

# Redirect if already logged in
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in"):
        
        if login_username in st.session_state.users and st.session_state.users[login_username] == login_password:
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success("Login successful (Session State)!")
            st.switch_page("pages/1_Dashboard.py")
        else:
         
            user = get_user(conn, login_username)
            if user and verify_password(login_password, user["password_hash"]):
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.success("Login successful (Database)!")
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("Invalid username or password.")

with tab_register:
    st.subheader("Register")
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username in st.session_state.users:
            st.error("Username already exists (session).")
        else:
        
            st.session_state.users[new_username] = new_password
          
            try:
                hashed = hash_password(new_password)
                add_user(conn, new_username, hashed)
            except Exception:
               
                pass
            st.success("Account created! 🎉")
            st.info("Go to Login tab to sign in.")
