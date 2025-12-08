import streamlit as st
from openai import OpenAI
from database.incidents import get_all_incidents  
from database.db import connect_database 

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🔍 AI Incident Analyzer")


conn = connect_database()
incidents = get_all_incidents(conn)

if incidents:
    # Let user select an incident
    incident_options = [
        f"{inc['id']}: {inc['incident_type']} - {inc['severity']}" for inc in incidents
    ]
    
    selected_idx = st.selectbox(
        "Select incident to analyze:",
        range(len(incidents)),
        format_func=lambda i: incident_options[i]
    )
    
    incident = incidents[selected_idx]
    
    # Display incident details
    st.subheader("📋 Incident Details")
    st.write(f"**Type:** {incident['incident_type']}")
    st.write(f"**Severity:** {incident['severity']}")
    st.write(f"**Description:** {incident['description']}")
    st.write(f"**Status:** {incident['status']}")
    
  
    if st.button("🤖 Analyze with AI", type="primary"):
        with st.spinner("AI analyzing incident..."):
            # Create analysis prompt
            analysis_prompt = f"""Analyze this cybersecurity incident:

Type: {incident['incident_type']}
Severity: {incident['severity']}
Description: {incident['description']}
Status: {incident['status']}

Provide:
1. Root cause analysis
2. Immediate actions needed
3. Long-term prevention measures
4. Risk assessment
"""

            # Call ChatGPT API
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert."},
                    {"role": "user", "content": analysis_prompt}
                ]
            )
            
            # Display AI analysis
            st.subheader("🧠 AI Analysis")
            st.write(response.choices[0].message.content.strip())
            
       

conn.close()

