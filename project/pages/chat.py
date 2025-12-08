# pages/chat.py
import streamlit as st
from openai import OpenAI
from utils.database import connect_database

#authentication
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

#page configuration
st.set_page_config(
    page_title="Security Intelligence Chat",
    page_icon="💬",
    layout="wide"
)

#Title
st.title("💬 Security Intelligence Assistant")
st.caption("Powered by OpenAI GPT-4o with Streaming")
#Open AI CLIENT
client = None
try:
    if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    else:
        st.warning("⚠️ OpenAI API key not found in secrets.")
        st.info("Please add OPENAI_API_KEY to .streamlit/secrets.toml")
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}")

#database connection
conn = connect_database()

#sidebar controls
with st.sidebar:
    st.title("⚙️ Chat Controls")
    
    # Message counter
    if 'messages' in st.session_state:
        message_count = len([m for m in st.session_state.messages if m["role"] != "system"])
        st.metric("Messages", message_count)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # Model selection 
    model = st.selectbox(
        "🤖 AI Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0,
        help="gpt-4o-mini is faster and cheaper, gpt-4o is more capable"
    )
    
    # Temperature control 
    temperature = st.slider(
        "🎛️ Creativity (Temperature)",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Lower = more focused, Higher = more creative"
    )
    
    # Domain/System Role Selection 
    st.divider()
    st.subheader("🎯 Domain Focus")
    
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
        "Cybersecurity Expert": """You are a senior cybersecurity expert with 10+ years of experience.
ROLE: Cybersecurity Analyst & Incident Responder
EXPERTISE:
- Threat intelligence and analysis
- Incident response and forensics
- Security architecture and controls
- Risk assessment and mitigation
- Compliance (NIST, ISO 27001, GDPR)

RESPONSE GUIDELINES:
1. Provide technical, actionable insights
2. Reference MITRE ATT&CK framework when relevant
3. Include severity levels (Critical/High/Medium/Low)
4. Suggest concrete mitigation steps
5. Use industry-standard terminology

FORMAT: Clear, structured with headings and bullet points when helpful.""",
        
        "Data Analytics Expert": """You are a senior data analytics expert.
ROLE: Data Scientist & Business Intelligence Analyst
EXPERTISE:
- Statistical analysis and modeling
- Data visualization and dashboard design
- Machine learning applications
- Data governance and quality
- Business intelligence insights

RESPONSE GUIDELINES:
1. Focus on data-driven insights
2. Suggest appropriate analysis techniques
3. Explain statistical concepts clearly
4. Provide visualization recommendations
5. Consider data quality and limitations

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
1. Provide step-by-step troubleshooting
2. Prioritize based on business impact
3. Include best practices and standards
4. Consider scalability and maintenance
5. Suggest automation where applicable

FORMAT: Practical, procedural with clear steps.""",
        
        "Multi-Domain Intelligence": """You are a Multi-Domain Security Intelligence Assistant.
ROLE: Integrated Security, Data, and Operations Analyst
DOMAIN EXPERTISE:
1. CYBERSECURITY: Threat detection, incident response, security controls
2. DATA ANALYTICS: Pattern recognition, predictive analysis, data visualization
3. IT OPERATIONS: System reliability, performance optimization, ticket management

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
    with st.expander("📋 View System Prompt"):
        st.text(system_prompts[domain])
    
    st.divider()
    
    # Quick prompts 
    st.subheader("💡 Quick Prompts")
    
    quick_prompts = {
        "🔒 Analyze security posture": "Analyze our current security posture and suggest improvements",
        "📊 Data quality assessment": "How can we improve data quality and governance?",
        "⚙️ IT efficiency review": "Review IT operations for efficiency improvements",
        "🔄 Cross-domain correlation": "How do security incidents correlate with IT tickets?",
        "📈 Predictive analysis": "What trends can we predict from our current data?"
    }
    
    for btn_text, prompt_content in quick_prompts.items():
        if st.button(btn_text, use_container_width=True):
            if 'quick_prompt' not in st.session_state:
                st.session_state.quick_prompt = ""
            st.session_state.quick_prompt = prompt_content
            st.rerun()

#Initializing session state
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

#Show chat history
# Display all messages except system messages 
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't display system messages
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
#user input
# Check for quick prompt or regular input
if 'quick_prompt' in st.session_state and st.session_state.quick_prompt:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt  # Clear after use
else:
    prompt = st.chat_input(f"Ask about {domain}...")

#processing user messages
if prompt:
    # Display user message immediately 
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to session state
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
  #Call OpenAI
    if client:
        try:
            # Call with streaming enabled 
            with st.spinner("🤔 Analyzing..."):
                completion = client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                    temperature=temperature,
                    stream=True  # ENABLE STREAMING 
                )
            
            # Response from streaming
            # Display assistant message with streaming 
            with st.chat_message("assistant"):
                container = st.empty()  # Create empty container to update
                full_reply = ""  #full response
                
                # Process each chunk as it arrives
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        delta_content = chunk.choices[0].delta.content
                        full_reply += delta_content
                        # Update display with cursor effect
                        container.markdown(full_reply + "▌")
                
                # Remove cursor and show final response
                container.markdown(full_reply)
            
            # Add assistant response to session state 
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_reply
            })
            
        except Exception as e:
            st.error(f"OpenAI API Error: {e}")
            with st.chat_message("assistant"):
                st.error("Sorry, I encountered an error. Please check your API key and try again.")
    else:
        with st.chat_message("assistant"):
            st.error("OpenAI client not configured. Please check your API key in secrets.toml")

#managing chats
st.divider()
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Export chat (Extra feature- My choice)
    if st.button("📥 Export Chat", use_container_width=True):
        if 'messages' in st.session_state and len(st.session_state.messages) > 1:
            chat_text = "=== Security Intelligence Chat Export ===\n\n"
            chat_text += f"Domain: {domain}\n"
            chat_text += f"Model: {model}\n"
            chat_text += f"Temperature: {temperature}\n"
            chat_text += f"Timestamp: {st.session_state.get('timestamp', 'N/A')}\n"
            chat_text += "\n" + "="*40 + "\n\n"
            
            for message in st.session_state.messages:
                if message["role"] != "system":
                    role_display = "👤 User" if message["role"] == "user" else "🤖 Assistant"
                    chat_text += f"{role_display}:\n{message['content']}\n\n" + "-"*40 + "\n\n"
            
            st.download_button(
                label="Download Chat",
                data=chat_text,
                file_name=f"chat_export_{domain.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

with col2:
    if st.button("📊 Go to Analytics", use_container_width=True):
        st.switch_page("pages/2_Analytics.py")

with col3:
    if st.button("🔍 AI Analyzer", use_container_width=True):
        st.switch_page("pages/4_AI_Analyzer.py")

with col4:
    if st.button("📋 Back to Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

#Educational Part(also my choice)
with st.expander("🔧 Educational Info & Debug"):
    st.subheader("Lab Implementation Features")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("**✅ Part 1: API Fundamentals**")
        st.write("- Message roles (system/user/assistant)")
        st.write("- Conversation history maintained")
        st.write("- Secure API key storage")
        
        st.write("\n**✅ Part 2: Streamlit Basics**")
        st.write("- st.chat_input() for user input")
        st.write("- st.chat_message() for display")
        st.write("- st.session_state for persistence")
    
    with col_b:
        st.write("**✅ Part 3: Streamlit Integration**")
        st.write("- Streamlit secrets for API key")
        st.write("- System prompts for domains")
        st.write("- Professional UI with sidebar")
        
        st.write("\n**✅ Part 4: Advanced Features**")
        st.write("- Streaming responses (real-time)")
        st.write("- Model/temperature controls")
        st.write("- Multi-domain intelligence")
    
    st.divider()
    
    # Show current session state (for debugging/education)
    if st.checkbox("Show Session State"):
        st.write("Current session state keys:", list(st.session_state.keys()))
        if 'messages' in st.session_state:
            st.write(f"Number of messages: {len(st.session_state.messages)}")
            for i, msg in enumerate(st.session_state.messages):
                with st.expander(f"Message {i}: {msg['role']}"):
                    if msg['role'] == 'system':
                        st.code(msg['content'][:200] + "..." if len(msg['content']) > 200 else msg['content'])
                    else:
                        st.write(msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content'])

