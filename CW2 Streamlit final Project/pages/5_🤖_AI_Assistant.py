"""AI Assistant Chat using OOP"""
import streamlit as st
from services.ai_assistant import AIAssistant
import json
from datetime import datetime

#Authentication
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("pages/1_🔐_Login.py")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Security Intelligence Chat",
    page_icon="💬",
    layout="wide"
)

# Title
st.title("💬 Security Intelligence Assistant")
st.caption("Powered by OpenAI GPT-4o with Streaming effect")

# Check for OpenAI API key
try:
    if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        ai_available = True
    else:
        openai_api_key = None
        ai_available = False
        st.warning("OpenAI API key not found in secrets. AI features disabled.")
except:
    openai_api_key = None
    ai_available = False

# Initialize AI Assistant
client = None
if ai_available:
    try:
        client = AIAssistant(api_key=openai_api_key)
    except Exception as e:
        st.error(f"Error initializing AI Assistant: {e}")
        ai_available = False

# Sidebar controls
with st.sidebar:
    st.title("⚙️ Chat Controls")
    
    # Message counter
    if 'messages' in st.session_state:
        message_count = len([m for m in st.session_state.messages if m["role"] != "system"])
        st.metric("Messages", message_count)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        if client:
            client.clear_history()
        st.rerun()
    
    st.divider()
    
    # Select ChatGPT Model 
    if ai_available:
        model = st.selectbox(
            "🤖 AI Model",
            ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
            index=0,
        )
        
        # choose the temperature for ai responses control (Lower = more focused, Higher = more creative)
        temperature = st.slider(
            "Creativity temperature)",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Lower = more focused, Higher = more creative"
        )
    else:
        st.info("AI features disabled. Add OpenAI API key to secrets.toml")
        temperature = 0.7
    
    # Domain/System Role Selection 
    st.divider()
    st.subheader("Domain Focus")
    
    domain = st.selectbox(
        "Select AI Role",
        [
            "General Assistant",
            "Cybersecurity Expert", 
            "Data Analytics Expert",
            "IT Operations Expert",
            "Multi-Domain Intelligence"
        ],
        index=4
    )
    
    # System prompts for different domains 
    system_prompts = {
        "General Assistant": "You are a helpful and knowledgeable assistant.",
        "Cybersecurity Expert": """You are a senior cybersecurity expert.
ROLE: Cybersecurity Analyst & Incident Responder
EXPERTISE:
- Threat intelligence and analysis
- Provide Incident response and forensics
- Security architecture and controls
- Assessment of risks and mitigation
- Compliance with rules (NIST, ISO 27001, GDPR)

RESPONSE GUIDELINES:
1. Provide technical and useful, actionable insights
2. Reference MITRE ATT&CK framework when relevant
3. Include severity levels (Critical/High/Medium/Low)
4. Suggest good mitigation steps
5. Use industry-standard terminology

FORMAT: Clear, structured with headings and bullet points when helpful.""",
        
        "Data Analytics Expert": """You are a senior data analytics expert.
ROLE: Data Scientist & Business Intelligence Analyst
EXPERTISE:
- analysis of statistics and modeling
- Data visualization 
- Machine learning uses
- Data governance and quality
- Business intelligence analytics and insights

RESPONSE GUIDELINES:
1. Focus on data-driven insights and analytics
2. Provide appropriate analysis techniques
3. Explain statistical concepts clearly
4. Provide visualization recommendations
5. Consider data quality and limitatios

FORMAT: Analytical, evidence-based with clear explanations.""",
        
        "IT Operations Expert": """You are an IT operations manager.
ROLE: IT Service Management Specialist
EXPERTISE:
- ITIL framework implementation
- Service desk management
- System administration and troubleshooting
- Infrastructure monitoring
- IT project management

RESPONSE GUIDELINES:
1. Provide troubleshooting with steps
2. Prioritize based on business impact
3. Include best practices and standards
4. Consider scalability and maintenance
5. Suggest automation incase it is applicable

FORMAT: Practical, procedural with clear steps.""",
        
        "Multi-Domain Intelligence": """You are a Multi-Domain Security Intelligence Assistant.
ROLE: Integrated Security, Data, and Operations Analyst
DOMAIN EXPERTISE:
1. CYBERSECURITY: detection of threats, incident response, security controls
2. DATA ANALYTICS: Pattern recognition, predictive analysis, data visualization
3. IT OPERATIONS: System reliability, performance optimization, management of tickets

CORE CAPABILITIES:
- Cross-domain correlation analysis
- Risk assessment across multiple domains
- Integrated recommendations
- Predictive threat modeling
- Operational efficiency optimization

RESPONSE GUIDELINES:
1. Analyze problems from multiple domain perspectives
2. Identify cross-domain dependencies and risks
3. Provide integrated recommendations
4. Consider both security and operational impact
5. Suggest monitoring and improvement metrics

FORMAT: Integrated, comprehensive with cross-domain insights."""
    }
    
    # Display selected system prompt
    with st.expander("View System Prompt"):
        st.text(system_prompts[domain])
    
    st.divider()
    
    # Quick prompts 
    st.subheader("Quick Prompts")
    
    quick_prompts = {
        "Analyze security posture": "Analyze our current security posture and suggest improvements",
        "Data quality assessment": "How can we improve data quality and governance?",
        "IT efficiency review": "Review IT operations for efficiency improvements",
        "Cross-domain correlation": "How do security incidents correlate with IT tickets?",
        "Predictive analysis": "What trends can we predict from our current data?"
    }
    
    for btn_text, prompt_content in quick_prompts.items():
        if st.button(btn_text, use_container_width=True, disabled=not ai_available):
            if 'quick_prompt' not in st.session_state:
                st.session_state.quick_prompt = ""
            st.session_state.quick_prompt = prompt_content
            st.rerun()
    
    if not ai_available:
        st.caption("Quick prompts require AI to be enabled")

# Initialize session state
# Initialize or update messages based on selected domain 
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompts[domain]}
    ]
    st.session_state.current_domain = domain
elif st.session_state.get('current_domain') != domain:
    # Update system message if domain changed
    st.session_state.messages = [
        {"role": "system", "content": system_prompts[domain]}
    ] + [msg for msg in st.session_state.messages if msg["role"] != "system"]
    st.session_state.current_domain = domain

# Show chat history
# Display all messages except system messages 
for message in st.session_state.messages:
    if message["role"] != "system":  
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
# Check for quick prompt or regular input
if 'quick_prompt' in st.session_state and st.session_state.quick_prompt:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt  # Clear after use
else:
    prompt = st.chat_input(f"Ask about {domain}...", disabled=not ai_available)

# Processing user messages
if prompt:
    # Display user message immediately 
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to session state
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Call AI Assistant
    if client and ai_available:
        try:
            # Set the system prompt
            client.set_system_prompt(system_prompts[domain])
            
            # Call with streaming enabled 
            with st.spinner("🤔 Analyzing..."):
                response_generator = client.send_message(
                    user_message=prompt,
                    temperature=temperature,
                    stream=True
                )
            
            # Display assistant message with streaming 
            with st.chat_message("assistant"):
                container = st.empty() 
                full_reply = "" 
                
                # Process each chunk as it arrives
                try:
                    for chunk in response_generator:
                        if chunk.choices[0].delta.content:
                            delta_content = chunk.choices[0].delta.content
                            full_reply += delta_content
                            # Update display with cursor effect
                            container.markdown(full_reply + "▌")
                except:
                    # If streaming fails, try non-streaming
                    full_reply = client.send_message(prompt, temperature=temperature, stream=False)
                    container.markdown(full_reply)
                
                # Remove cursor and show final response
                container.markdown(full_reply)
            
            # Add assistant response to session state 
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_reply
            })
            
        except Exception as e:
            st.error(f"AI Assistant Error: {str(e)}")
            with st.chat_message("assistant"):
                st.error("Sorry, There is an error. Please check your API key and try again.")
    else:
        with st.chat_message("assistant"):
            if not ai_available:
                st.error("AI Assistant is disabled.")
                st.info("Add to secret.tomll")
            else:
                st.error("AI Assistant not configured. Please check your setup.")

# Managing chats
st.divider()
col1, col2, col3 = st.columns(3) 

with col1:
    if st.button("📊 Go to Analytics", use_container_width=True):
        st.switch_page("pages/3_📊_Data_Science.py")

with col2:
    if st.button("🔍 AI Analyzer", use_container_width=True):
        st.switch_page("pages/4_💻_IT_Operations.py")

with col3:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Home.py")

# Debug info
with st.expander("Information"):
    st.write(f"**AI Available:** {ai_available}")
    st.write(f"**Current Domain:** {domain}")
    st.write(f"**Temperature:** {temperature}")
    st.write(f"**Messages in Session:** {len(st.session_state.get('messages', []))}")
    
    if st.checkbox("Show Session State"):
        st.write(st.session_state)