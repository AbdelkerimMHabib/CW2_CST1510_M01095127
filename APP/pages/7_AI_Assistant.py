import streamlit as st
from openai import OpenAI
import pandas as pd
from datetime import datetime
from utils.database import connect_database, get_all_incidents, get_all_datasets, get_all_tickets, save_chat_message, get_chat_history

# Login check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize OpenAI client
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    ai_available = True
except:
    st.error("OpenAI API key not configured. Please add OPENAI_API_KEY to .streamlit/secrets.toml")
    st.info("Add this to .streamlit/secrets.toml:\n\nOPENAI_API_KEY = 'your-api-key-here'")
    ai_available = False
    st.stop()

# Title
st.title("🤖 AI Assistant")
st.caption(f"Welcome, {st.session_state.username}! Get AI-powered insights across all domains")

# Database connection
conn = connect_database()

# Sidebar controls
with st.sidebar:
    st.subheader("AI Settings")
    
    # Domain selection
    domain = st.selectbox(
        "Expertise Domain",
        ["Cybersecurity", "Data Analysis", "IT Operations", "General"],
        help="Select the AI's area of expertise"
    )
    
    # Model selection
    model = st.selectbox(
        "AI Model",
        ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
        index=0
    )
    
    # Temperature
    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values = more creative, lower = more focused"
    )
    
    # Context length
    max_tokens = st.slider(
        "Response Length",
        min_value=100,
        max_value=2000,
        value=500,
        step=100,
        help="Maximum tokens in response"
    )
    
    st.divider()
    
    # Quick analysis buttons
    st.subheader("Quick Analysis")
    
    if st.button("📊 Analyze Dashboard Data", use_container_width=True):
        st.session_state.quick_analysis = "dashboard"
        st.rerun()
    
    if st.button("🛡️ Analyze Incidents", use_container_width=True):
        st.session_state.quick_analysis = "incidents"
        st.rerun()
    
    if st.button("💻 Analyze Tickets", use_container_width=True):
        st.session_state.quick_analysis = "tickets"
        st.rerun()
    
    if st.button("📂 Analyze Datasets", use_container_width=True):
        st.session_state.quick_analysis = "datasets"
        st.rerun()
    
    st.divider()
    
    # Load chat history
    if st.button("📜 Load Chat History", use_container_width=True):
        history = get_chat_history(conn, st.session_state.username, domain, limit=20)
        if history:
            st.session_state.ai_messages = [{"role": "system", "content": system_prompts[domain]}]
            for msg in reversed(history):  # Oldest first
                st.session_state.ai_messages.append({
                    "role": msg[3],  # message_role
                    "content": msg[4]  # message_content
                })
            st.success(f"Loaded {len(history)} messages from history")
            st.rerun()
        else:
            st.info("No chat history found")

# Domain-specific system prompts
system_prompts = {
    "Cybersecurity": """You are a cybersecurity expert with 15 years of experience. You have access to incident data and provide:
    1. Threat analysis and risk assessment
    2. MITRE ATT&CK framework mapping
    3. Incident response recommendations
    4. Security best practices and compliance guidance
    5. Vulnerability assessment and mitigation strategies
    
    Use technical terminology and provide actionable advice.
    Always cite relevant frameworks (NIST, ISO 27001, etc.) when applicable.
    Format responses with clear sections and bullet points for readability.""",
    
    "Data Analysis": """You are a data science expert with 10 years of experience. You have access to datasets and provide:
    1. Data analysis insights and patterns
    2. Statistical observations and correlations
    3. Visualization recommendations and best practices
    4. Data quality assessment and cleaning suggestions
    5. Machine learning application recommendations
    
    Use data science terminology and provide clear, practical explanations.
    Suggest specific tools and techniques when relevant.
    Format responses with clear sections and examples.""",
    
    "IT Operations": """You are an IT operations expert with 12 years of experience. You have access to ticket data and provide:
    1. Troubleshooting guidance and step-by-step solutions
    2. System optimization tips and performance tuning
    3. Incident management advice and escalation procedures
    4. IT best practices and operational excellence guidelines
    5. Technology stack recommendations and architecture advice
    
    Use IT operations terminology and provide practical, implementable solutions.
    Include estimated resolution times and difficulty levels.
    Format responses with numbered steps and clear action items.""",
    
    "General": """You are a helpful AI assistant for a multi-domain intelligence platform.
    Provide accurate, concise, and helpful information across all domains.
    When unsure, ask clarifying questions.
    Maintain a professional yet approachable tone."""
}

# Initialize session state for chat
if 'ai_messages' not in st.session_state:
    st.session_state.ai_messages = [
        {"role": "system", "content": system_prompts[domain]}
    ]

# Handle quick analysis
if 'quick_analysis' in st.session_state:
    if st.session_state.quick_analysis == "dashboard":
        # Load all data
        incidents = get_all_incidents(conn)
        datasets = get_all_datasets(conn)
        tickets = get_all_tickets(conn)
        
        analysis_prompt = f"""Analyze this dashboard data for {st.session_state.username}:
        
        CYBERSECURITY DOMAIN:
        - Total incidents: {len(incidents)}
        - Severity distribution: {', '.join([i[2] for i in incidents[:5]]) if incidents else 'None'}
        - Recent incident: {incidents[0][1] if incidents else 'None'}
        
        DATASETS DOMAIN:
        - Total datasets: {len(datasets)}
        - Total size: {sum([d[4] for d in datasets]) if datasets else 0} MB
        - Categories: {', '.join(set([d[3] for d in datasets])) if datasets else 'None'}
        
        IT OPERATIONS DOMAIN:
        - Total tickets: {len(tickets)}
        - Priority distribution: {', '.join([t[2] for t in tickets[:5]]) if tickets else 'None'}
        - Recent ticket: {tickets[0][1] if tickets else 'None'}
        
        Provide a comprehensive analysis including:
        1. Overall platform health assessment
        2. Key risks and concerns
        3. Immediate action items
        4. Strategic recommendations
        5. Success metrics to track
        
        Format as an executive briefing."""
        
        st.session_state.ai_messages.append({"role": "user", "content": analysis_prompt})
        del st.session_state.quick_analysis
    
    elif st.session_state.quick_analysis == "incidents":
        incidents = get_all_incidents(conn)
        if incidents:
            df_inc = pd.DataFrame(incidents[:10], columns=["id","title","severity","status","date","description","created_by","updated"])
            analysis_prompt = f"""Analyze these recent cyber incidents:
            
            {df_inc[['title', 'severity', 'status', 'date']].to_string()}
            
            Provide:
            1. Overall threat landscape assessment
            2. Top attack vectors identified
            3. Response effectiveness analysis
            4. Security control gap analysis
            5. Improvement recommendations
            
            Focus on actionable insights for security team."""
            
            st.session_state.ai_messages.append({"role": "user", "content": analysis_prompt})
        del st.session_state.quick_analysis
    
    elif st.session_state.quick_analysis == "tickets":
        tickets = get_all_tickets(conn)
        if tickets:
            df_tk = pd.DataFrame(tickets[:10], columns=["id","title","priority","status","created_date","assigned_to","description","resolution","updated"])
            analysis_prompt = f"""Analyze these recent IT tickets:
            
            {df_tk[['title', 'priority', 'status', 'created_date', 'assigned_to']].to_string()}
            
            Provide:
            1. IT service health assessment
            2. Common issue patterns
            3. Resource allocation analysis
            4. SLA compliance assessment
            5. Process improvement suggestions
            
            Focus on operational efficiency and user satisfaction."""
            
            st.session_state.ai_messages.append({"role": "user", "content": analysis_prompt})
        del st.session_state.quick_analysis
    
    elif st.session_state.quick_analysis == "datasets":
        datasets = get_all_datasets(conn)
        if datasets:
            df_ds = pd.DataFrame(datasets[:10], columns=["id","name","source","category","size","format","created_by","created"])
            analysis_prompt = f"""Analyze these datasets:
            
            {df_ds[['name', 'source', 'category', 'size']].to_string()}
            
            Provide:
            1. Data quality assessment
            2. Data governance analysis
            3. Integration opportunities
            4. Analytics potential
            5. Data management recommendations
            
            Focus on maximizing data value and usability."""
            
            st.session_state.ai_messages.append({"role": "user", "content": analysis_prompt})
        del st.session_state.quick_analysis

# Update system prompt if domain changed
if st.session_state.ai_messages[0]["content"] != system_prompts[domain]:
    st.session_state.ai_messages[0] = {"role": "system", "content": system_prompts[domain]}

# Display chat history (skip system message)
for message in st.session_state.ai_messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
prompt = st.chat_input(f"Ask the {domain} AI assistant...")

if prompt and ai_available:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Save to database
    save_chat_message(conn, st.session_state.username, domain, "user", prompt)
    
    # Add to messages
    st.session_state.ai_messages.append({"role": "user", "content": prompt})
    
    # Call OpenAI API with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Create completion with streaming
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.ai_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            # Stream the response
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            # Final display
            message_placeholder.markdown(full_response)
            
            # Save to database
            save_chat_message(conn, st.session_state.username, domain, "assistant", full_response)
            
        except Exception as e:
            st.error(f"Error calling OpenAI API: {str(e)}")
            full_response = "I apologize, but I encountered an error processing your request. Please check your API configuration and try again."
            message_placeholder.markdown(full_response)
    
    # Add assistant response to history
    st.session_state.ai_messages.append({"role": "assistant", "content": full_response})

elif prompt and not ai_available:
    st.error("OpenAI API is not available. Please configure your API key.")

# Chat controls
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.ai_messages = [
            {"role": "system", "content": system_prompts[domain]}
        ]
        st.rerun()

with col2:
    if st.button("📋 Copy Last Response", use_container_width=True):
        if len(st.session_state.ai_messages) > 1:
            last_response = st.session_state.ai_messages[-1]["content"]
            st.code(last_response)

with col3:
    if st.button("💾 Export Chat", use_container_width=True):
        chat_text = f"AI Assistant Chat - {domain} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        chat_text += f"User: {st.session_state.username}\n"
        chat_text += "="*50 + "\n\n"
        
        for msg in st.session_state.ai_messages:
            if msg["role"] != "system":
                chat_text += f"{msg['role'].upper()}:\n{msg['content']}\n\n"
        
        st.download_button(
            label="Download Chat",
            data=chat_text,
            file_name=f"ai_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

with col4:
    if st.button("🔄 New Session", use_container_width=True):
        st.session_state.ai_messages = [
            {"role": "system", "content": system_prompts[domain]}
        ]
        st.rerun()

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
    if st.button("⚙️ Settings", use_container_width=True):
        st.switch_page("pages/6_Settings.py")