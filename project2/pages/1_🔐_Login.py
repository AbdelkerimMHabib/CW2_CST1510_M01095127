import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from database.db import DatabaseInitializer

DatabaseInitializer().initialize()
db_manager = DatabaseManager()
auth_manager = AuthManager(db_manager)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "current_user" not in st.session_state:
    st.session_state.current_user = None

if st.session_state.logged_in:
    st.switch_page("Home.py")

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")
st.title("🔐 Multi-Domain Intelligence Platform")

tab_login, tab_register = st.tabs(["🔐 Login", "📝 Register"])

with tab_login:
    st.subheader("Login to Your Account")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Log In", type="primary", use_container_width=True):
        if not login_username or not login_password:
            st.error("Please enter both username and password.")
        else:
            user = auth_manager.login_user(login_username, login_password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = user.get_username()
                st.session_state.user_role = user.get_role()
                st.session_state.current_user = user
                st.success("✅ Login successful!")
                st.switch_page("Home.py")
            else:
                st.error("❌ Invalid username or password.")

with tab_register:
    st.subheader("Create New Account")
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    
    if st.button("Create Account", type="primary", use_container_width=True):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters long.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            success, message = auth_manager.register_user(new_username, new_password)
            if success:
                st.success(f"✅ {message}")
                st.rerun()
            else:
                st.error(f"❌ {message}")

st.divider()
st.markdown("**Demo Credentials:** admin / admin123")