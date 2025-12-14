"""Login page implemented using object-oriented approach with AuthManager and DatabaseManager services."""
import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

# Initialize session state variables if they don't exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = "user"
if "user_obj" not in st.session_state:
    st.session_state.user_obj = None

# Set page configuration
st.set_page_config(
    page_title="Login / Register",
    page_icon="🔐",
    layout="centered"
)

st.title(" My Security Intelligence Platform")

# Redirect if already logged in
if st.session_state.logged_in:
    st.success(f"Welcome back, **{st.session_state.username}**!")
    if st.button("Go to Dashboard"):
        st.switch_page("Home.py")
    st.stop()

# Initialize important services
db = DatabaseManager()
auth = AuthManager(db)

#Login and Registration tabs
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
                # Use authentication manager to authenticate the user
                user = auth.login_user(login_username, login_password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user.get_username()
                    st.session_state.user_role = user.get_role()
                    st.session_state.user_obj = user
                    st.success("Login was successful!")
                    st.switch_page("Home.py")
                else:
                    # Check session users 
                    if "users" in st.session_state and login_username in st.session_state.users and st.session_state.users[login_username] == login_password:
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.success("Login was successful)!")
                        st.switch_page("Home.py")
                    else:
                        st.error("Invalid username or password.")

with tab_register:
    st.subheader("Create a new account")
    
    new_username = st.text_input("Choose a username", key="register_username", 
                                placeholder="Enter unique username")
    new_password = st.text_input("Choose a password", type="password", key="register_password",
                                placeholder="Word count should be a minimum of 6 characters")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm",
                                    placeholder="Re-enter your password")
    
    if st.button("Create Account", type="primary", use_container_width=True):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif len(new_password) < 6:
            st.error("Word count should be a minimum of 6 characters.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            # Use AuthManager to register
            if auth.register_user(new_username, new_password):
                # Initialize session users dict if not exists
                if "users" not in st.session_state:
                    st.session_state.users = {}
                
                # Add to session for immediate login
                st.session_state.users[new_username] = new_password
                
                st.success("Account created successfully!")
                st.info("You can now log in with your credentials.")
                st.rerun()
            else:
                st.error("Username already exists. Please choose another one.")

# Information about my app
st.divider()
st.markdown("### ℹ️ About This Platform")
st.markdown("""
This Security Intelligence Platform provides:
- **Cybersecurity Dashboard**: Here you can see and manage security incidents
- **Data Analytics**: Here you can see and analyze datasets
- **IT Operations**: Here you can manage IT support tickets
- **AI Assistant**: You can use an AI assistant for help with security, data, and IT topics
- **AI Analyzer**: Get AI-powered analysis of your incidents, datasets, tickets, and users

*Use 'admin' / 'admin123' for initial access.*
""")

# Navtigation back to home button
st.divider()
if st.button("🏠 Back to Home"):
    st.switch_page("Home.py")