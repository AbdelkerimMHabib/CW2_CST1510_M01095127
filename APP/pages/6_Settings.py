import streamlit as st
import pandas as pd
from utils.database import connect_database, get_user, update_user_password, get_all_users, get_recent_activities
from utils.auth import hash_password, verify_password
import sqlite3

# Login check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()

# Page config
st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

conn = connect_database()
st.title("⚙️ Settings")

username = st.session_state.username
user = get_user(conn, username)

# User info
st.subheader("User Information")
col1, col2 = st.columns(2)
with col1:
    st.info(f"**Username:** {username}")
with col2:
    st.info(f"**Role:** {st.session_state.get('role', 'user')}")

st.markdown("---")

# Change password
st.subheader("Change Password")
with st.form("change_password_form"):
    old = st.text_input("Current password", type="password")
    new = st.text_input("New password", type="password")
    confirm = st.text_input("Confirm new password", type="password")
    
    if st.form_submit_button("Update Password", use_container_width=True):
        if not user:
            st.error("User record not found")
        elif not verify_password(old, user[2]):
            st.error("Current password incorrect")
        elif new != confirm:
            st.error("New passwords do not match")
        elif len(new) < 6:
            st.error("New password must be at least 6 characters")
        else:
            update_user_password(conn, username, hash_password(new))
            st.success("Password updated successfully!")

# Admin panel
if st.session_state.get("role") == "admin":
    st.markdown("---")
    st.subheader("👑 Admin Panel")
    
    # User management tab
    tab1, tab2, tab3 = st.tabs(["👥 User Management", "📊 System Info", "🔍 Activity Log"])
    
    with tab1:
        st.subheader("User Management")
        
        # List all users
        users = get_all_users(conn)
        if users:
            df_users = pd.DataFrame(users, columns=["ID", "Username", "Role", "Created At"])
            st.dataframe(df_users, use_container_width=True)
            
            # User actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("Add New User")
                with st.form("add_user_form"):
                    new_username = st.text_input("Username")
                    new_password = st.text_input("Password", type="password")
                    new_role = st.selectbox("Role", ["user", "admin"])
                    
                    if st.form_submit_button("Add User", use_container_width=True):
                        if new_username and new_password:
                            try:
                                from utils.database import add_user
                                add_user(conn, new_username, hash_password(new_password), new_role)
                                st.success(f"User {new_username} added!")
                                st.rerun()
                            except sqlite3.IntegrityError:
                                st.error("Username already exists")
                        else:
                            st.error("Username and password are required")
            
            with col2:
                st.subheader("Change User Role")
                username_to_update = st.selectbox("Select user", [u[1] for u in users])
                new_role = st.selectbox("New role", ["user", "admin"])
                
                if st.button("Update Role", use_container_width=True):
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET role = ? WHERE username = ?", 
                                 (new_role, username_to_update))
                    conn.commit()
                    st.success(f"Updated {username_to_update} to {new_role}")
                    st.rerun()
            
            with col3:
                st.subheader("Delete User")
                username_to_delete = st.selectbox("User to delete", 
                                                [u[1] for u in users if u[1] != st.session_state.username])
                
                if st.button("Delete User", type="secondary", use_container_width=True):
                    if username_to_delete:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM users WHERE username = ?", (username_to_delete,))
                        conn.commit()
                        st.success(f"User {username_to_delete} deleted")
                        st.rerun()
        else:
            st.info("No users found")
    
    with tab2:
        st.subheader("System Information")
        
        # Database stats
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM cyber_incidents")
        inc_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM datasets_metadata")
        ds_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM it_tickets")
        tk_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Cyber Incidents", inc_count)
            st.metric("IT Tickets", tk_count)
        with col2:
            st.metric("Datasets", ds_count)
            st.metric("Users", user_count)
        
        # Database cleanup
        st.subheader("Database Maintenance")
        if st.button("Optimize Database", use_container_width=True):
            cursor.execute("VACUUM")
            conn.commit()
            st.success("Database optimized!")
        
        if st.button("Clear All Data", type="secondary", use_container_width=True):
            st.warning("This will delete ALL data! Are you sure?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete Everything", type="primary"):
                    cursor.execute("DELETE FROM cyber_incidents")
                    cursor.execute("DELETE FROM datasets_metadata")
                    cursor.execute("DELETE FROM it_tickets")
                    cursor.execute("DELETE FROM ai_analyses")
                    cursor.execute("DELETE FROM ai_chat_history")
                    cursor.execute("DELETE FROM activity_log")
                    # Keep users table
                    conn.commit()
                    st.success("All data cleared! Users remain.")
                    st.rerun()
            with col2:
                if st.button("Cancel", type="secondary"):
                    st.info("Operation cancelled")
    
    with tab3:
        st.subheader("Activity Log")
        activities = get_recent_activities(conn, limit=50)
        if activities:
            df_activities = pd.DataFrame(activities, 
                                       columns=["ID", "Username", "Action", "Entity Type", "Entity ID", "Details", "Timestamp"])
            st.dataframe(df_activities[["Username", "Action", "Entity Type", "Details", "Timestamp"]], 
                        use_container_width=True, hide_index=True)
            
            # Export log
            csv = df_activities.to_csv(index=False)
            st.download_button(
                label="📥 Export Activity Log",
                data=csv,
                file_name=f"activity_log_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("No activity log entries")

# Bottom navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")
with col2:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
with col3:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = "user"
        st.success("Logged out. Redirecting...")
        st.switch_page("Home.py")