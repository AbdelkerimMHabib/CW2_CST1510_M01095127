import streamlit as st
from utils.auth import hash_password, verify_password
from utils.database import connect_database, add_user, get_user, create_tables

# Initialize session-state flags
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "role" not in st.session_state: st.session_state.role = "user"
if "dark_mode" not in st.session_state: st.session_state.dark_mode = False

# Theme toggle (affects widget labels/appearance only)
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

st.set_page_config(page_title="Intelligence Platform - Login", layout="centered")
st.title("🔐 Intelligence Platform")
st.checkbox("Dark mode", value=st.session_state.dark_mode, key="dark_mode_checkbox", on_change=toggle_theme)

conn = connect_database()
create_tables(conn)

if st.session_state.logged_in:
    st.success(f"Logged in as **{st.session_state.username}** ({st.session_state.role})")
    if st.button("Go to Dashboard"):
        st.experimental_set_query_params()  # force page reload context
        st.experimental_rerun()
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = "user"
        st.success("Logged out.")
    st.stop()

tab_login, tab_register = st.tabs(["Login","Register"])

with tab_login:
    uname = st.text_input("Username", key="login_username")
    pwd = st.text_input("Password", type="password", key="login_password")
    if st.button("Log in"):
        user = get_user(conn, uname)
        if user and verify_password(pwd, user[2]):
            st.session_state.logged_in = True
            st.session_state.username = uname
            # DB user tuple: (id, username, password_hash, role, created_at)
            st.session_state.role = user[3] if len(user) > 3 else "user"
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

with tab_register:
    new_uname = st.text_input("Choose username", key="reg_username")
    new_pwd = st.text_input("Choose password", type="password", key="reg_password")
    confirm = st.text_input("Confirm password", type="password", key="reg_confirm")
    if st.button("Create account"):
        if not new_uname or not new_pwd:
            st.warning("Fill in both fields")
        elif new_pwd != confirm:
            st.error("Passwords do not match")
        elif get_user(conn, new_uname):
            st.error("Username already exists")
        else:
            add_user(conn, new_uname, hash_password(new_pwd), role="user")
            st.success("Account created — please login.")
