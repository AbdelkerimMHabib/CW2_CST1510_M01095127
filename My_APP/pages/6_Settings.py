import streamlit as st
from utils.database import connect_database, get_user, update_user_password
from utils.auth import hash_password, verify_password

conn = connect_database()
st.title("⚙️ Settings")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Login required")
    st.stop()

username = st.session_state.username
user = get_user(conn, username)
st.write(f"**Username:** {username}")
st.write(f"**Role:** {st.session_state.get('role','user')}")

st.subheader("Change password")
old = st.text_input("Current password", type="password")
new = st.text_input("New password", type="password")
confirm = st.text_input("Confirm new password", type="password")
if st.button("Update password"):
    if not user:
        st.error("User record not found")
    elif not verify_password(old, user[2]):
        st.error("Current password incorrect")
    elif new != confirm:
        st.error("New passwords do not match")
    else:
        update_user_password(conn, username, hash_password(new))
        st.success("Password updated")

# Admin panel example
if st.session_state.get("role") == "admin":
    st.divider()
    st.subheader("Admin panel")
    st.info("Admin can manage users (not implemented fully here).")
