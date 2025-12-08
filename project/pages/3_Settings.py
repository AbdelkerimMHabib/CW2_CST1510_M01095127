import streamlit as st
from utils.database import connect_database, get_user

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
st.title("⚙️ Settings")

conn = connect_database()

# Get current user info
username = st.session_state.username
user = get_user(conn, username)

# Tabs for settings
tab1, tab2, tab3 = st.tabs(["👤 Profile", "Appearance", "🔐 Security"])

with tab1:
    st.subheader("User Profile")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Username", username)
        if user:
            st.metric("Role", user["role"])
            st.metric("Member Since", user["created_at"][:10])
    
    with col2:
        st.info("Profile information is managed by administrators.")
        
        # Display additional info if admin
        if user and user["role"] == "admin":
            st.success("You have administrator privileges.")
            st.write("As an admin, you can:")
            st.write("- Manage user accounts")
            st.write("- Modify all data tables")
            st.write("- Access all system features")

with tab2:
    st.subheader("Appearance Settings")
    
    # Theme selection
    theme = st.selectbox(
        "Select Theme",
        ["Light", "Dark", "System Default"],
        index=0
    )
    
    # Layout preferences
    layout = st.radio(
        "Page Layout",
        ["Wide", "Centered", "Compact"],
        horizontal=True
    )
    
    # Display settings
    col1, col2 = st.columns(2)
    
    with col1:
        show_animations = st.checkbox("Show animations", value=True)
        show_help_tips = st.checkbox("Show help tips", value=True)
    
    with col2:
        font_size = st.select_slider(
            "Font Size",
            options=["Small", "Medium", "Large"],
            value="Medium"
        )
    
    # Save button
    if st.button("Save Appearance Settings", type="primary"):
        st.success(f"Settings saved: {theme} theme, {layout} layout")
        st.rerun()

with tab3:
    st.subheader("Security Settings")
    
    # Change password
    st.write("### Change Password")
    current_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")
    
    if st.button("Change Password", type="primary"):
        if not current_password or not new_password or not confirm_password:
            st.error("Please fill in all password fields.")
        elif new_password != confirm_password:
            st.error("New passwords do not match.")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            st.warning("⚠️ Password change functionality requires backend implementation.")
            st.info("In a production system, this would validate and update your password.")
    
    # Security preferences
    st.divider()
    st.write("### Security Preferences")
    
    enable_2fa = st.checkbox("Enable Two-Factor Authentication (2FA)", value=False)
    session_timeout = st.selectbox(
        "Session Timeout",
        ["15 minutes", "30 minutes", "1 hour", "4 hours", "Until logout"],
        index=2
    )
    
    login_notifications = st.checkbox("Send login notifications", value=True)
    failed_login_alerts = st.checkbox("Alert on failed login attempts", value=True)
    
    if st.button("Update Security Preferences"):
        st.success("Security preferences updated!")
        st.rerun()


# Navigation
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Back to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
with col2:
    if st.button("📈 Go to Analytics"):
        st.switch_page("pages/2_Analytics.py")