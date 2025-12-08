import streamlit as st
from utils.auth import hash_password, verify_password
from utils.database import connect_database, add_user, get_user

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "users" not in st.session_state:
    st.session_state.users = {}  # For session-only users 

# DB connection
conn = connect_database()

st.set_page_config(page_title="Login / Register", page_icon="🔐", layout="centered")
st.title("🔐 Security Intelligence Platform")

# Redirect if already logged in
if st.session_state.logged_in:
    st.success(f"Welcome back, **{st.session_state.username}**!")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

tab_login, tab_register = st.tabs(["🔐 Login", "Register"])

with tab_login:
    st.subheader("Login to Your Account")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/5087/5087579.png", width=150)
    
    with col2:
        login_username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        login_password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
        
        if st.button("Log In", type="primary", use_container_width=True):
            if not login_username or not login_password:
                st.error("Please enter both username and password.")
            else:
                # Check database first
                user = get_user(conn, login_username)
                if user and verify_password(login_password, user["password_hash"]):
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.success("✅ Login successful!")
                    st.balloons()
                    st.switch_page("pages/1_Dashboard.py")
                else:
                    # Check session users (temporary)
                    if login_username in st.session_state.users and st.session_state.users[login_username] == login_password:
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.success("✅ Login successful (temporary session)!")
                        st.balloons()
                        st.switch_page("pages/1_Dashboard.py")
                    else:
                        st.error("❌ Invalid username or password.")

with tab_register:
    st.subheader("Create New Account")
    
    new_username = st.text_input("Choose a username", key="register_username", 
                                placeholder="Enter unique username")
    new_password = st.text_input("Choose a password", type="password", key="register_password",
                                placeholder="Minimum 6 characters")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm",
                                    placeholder="Re-enter your password")
    
    if st.button("Create Account", type="primary", use_container_width=True):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters long.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            # Check if username exists in database
            existing_user = get_user(conn, new_username)
            if existing_user:
                st.error("Username already exists. Please choose another.")
            else:
                try:
                    # Add to database
                    hashed = hash_password(new_password)
                    add_user(conn, new_username, hashed)
                    
                    # Also add to session for immediate login
                    st.session_state.users[new_username] = new_password
                    
                    st.success("✅ Account created successfully!")
                    st.info("You can now log in with your credentials.")
                    
                    # Clear form
                    st.rerun()
                    
                except Exception as e:
                    # If database fails, use session only
                    st.session_state.users[new_username] = new_password
                    st.warning("⚠️ Account created in session only (database unavailable).")
                    st.info("You can log in now, but data won't persist after session ends.")

#Some guidlines and helpful information(My choice)
st.divider()
st.markdown("### ℹ️ About This Platform")
st.markdown("""
This Security Intelligence Platform provides:
- **Dashboard**: Here, 3 domains are implemented.View and manage security incidents, datasets, and IT tickets
- **Analytics**: Visualize data and generate insights on domains
- **AI Analyzer**: Get AI-powered analysis of security data
- **Chat Assistant**: Here there is an Interactive AI chatbot which you can ask security questions
- **Settings**: Customize your experience

*Use 'admin' / 'admin123' for initial access.*
""")