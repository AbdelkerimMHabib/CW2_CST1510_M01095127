# My_app/pages/4_AI_Analyzer.py
import streamlit as st
from openai import OpenAI
from utils.database import connect_database, get_all_incidents

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("🔍 AI Incident Analyzer")
client = None
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.warning("OpenAI key not found in secrets. Analyzer will not function without a key.")

conn = connect_database()
incidents = get_all_incidents(conn)

if not incidents:
    st.info("No incidents to analyze.")
else:
    options = [f"{r['id']}: {r['title']} ({r['severity']})" for r in incidents]
    idx = st.selectbox("Select incident", list(range(len(options))), format_func=lambda i: options[i])
    incident = incidents[idx]
    st.subheader("Incident details")
    st.write(dict(incident))

    if st.button("Analyze with AI"):
        prompt = f"""You are a cybersecurity expert. Analyze this incident:
Title: {incident['title']}
Severity: {incident['severity']}
Status: {incident['status']}
Date: {incident['date']}

Provide:
1. Root cause analysis
2. Immediate steps
3. Long-term mitigation
4. Risk assessment (low/medium/high)
"""
        if client is None:
            st.error("OpenAI not configured.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role":"system","content":"You are a cybersecurity expert."},
                            {"role":"user","content":prompt}
                        ]
                    )
                    ai_output = res.choices[0].message.content
                    st.subheader("AI Analysis")
                    st.write(ai_output)
                except Exception as e:
                    st.error(f"OpenAI error: {e}")
