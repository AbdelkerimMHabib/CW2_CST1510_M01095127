import streamlit as st

def display_metrics(title: str, metrics: dict, columns: int = 4):
    st.subheader(title)
    col_count = min(len(metrics), columns)
    cols = st.columns(col_count)
    for idx, (label, value) in enumerate(metrics.items()):
        with cols[idx % col_count]:
            st.metric(label, value)

def check_admin_access():
    return st.session_state.get('user_role') == "admin"

def check_editor_access():
    return st.session_state.get('user_role') in ["admin", "editor"]