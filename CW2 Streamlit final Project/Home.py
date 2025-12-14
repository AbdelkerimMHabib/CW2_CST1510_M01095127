"""This is the main page for my Multi-Domain Intelligence Platform"""
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Multi-Domain Intelligence Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = "user"
if "user_obj" not in st.session_state:
    st.session_state.user_obj = None

def show_landing_page():
    """Show the landing page for non-logged in users"""
    st.title("🤖 Multi-Domain Intelligence Platform")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Welcome to the Multi-Domain Security Platform
        
        A comprehensive solution that integrates:
        - **Cybersecurity** -You can manage incidents and get threat insights
        - **Data Science** - You can see analytics and visualization
        - **IT Operations** - You can manage support tickets and system issues
        - **AI Assistant** - You can get intelligent analysis and recommendations
        
        ### Key Features:
        **Unified Dashboard** - All three domain integrated with analytics, crud operations, and AI insights
        **Real-time security incident tracking**  
        **AI-powered data analytics and visualization**  
        **Multi-user role-based access control**  
        **Comprehensive reporting and AI analysis**  
        **Interactive charts and real-time metrics**  
        """)
    
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=200)
        st.info("""
        **Get Started**
        
        Log in to access:
        - Unified Dashboard
        - Domain pages
        - AI Analysis for incidents, datasets, tickets, and users
        - analytics
        """)
   
    # Platform preview
    st.markdown("---")
    st.subheader("Platform Preview")
    
    preview_cols = st.columns(2)
    
    with preview_cols[0]:
        st.markdown("""
        ### Unified Dashboard Features:
        
        **Real-time Metrics:**
        - Counts of incidents and distribution for severity
        - Datasets categories with sizes
        - The status of IT tickets along with priority levels
        - the staus of the system and status of users
        
        **AI Analysis:**
        - Cross-domain correlation analysis
        - Risk analysis and recommendations
        - Prediction of trends
        - Reporting
        """)
    
    with preview_cols[1]:
        st.markdown("""
        ### Capabilities:
        
        **Architecture:**
        - Code strcuctured and designed using object-oriented programming.
        - Nice architecture
        - SQLite database for storing my data
        - Implemented authentication using session state
        
        **Integrations:**
        - Integrated OPENAI chatgpt 4o-Mini for AI analysis
        - data visualization
        - Export/Import functionality (My choice integration)
        - access control depending on user roles
        """)
    
    # Quick actions
    st.markdown("---")
    st.subheader("Quick Actions")
    
    action_cols = st.columns(3)
    
    with action_cols[0]:
        if st.button("🔐 **Login / Register**", use_container_width=True, type="primary"):
            st.switch_page("pages/1_🔐_Login.py")
    
def show_dashboard():
    """Show the main dashboard for logged in users - REDIRECT to unified dashboard"""
    # Redirect to unified dashboard
    st.switch_page("pages/0_🏠_Dashboard.py")


# Main application flow
def main():
    # Check if user is logged in
    if not st.session_state.logged_in:
        show_landing_page()
    else:
        # When logged in, show a welcome page with option to go to dashboard
        st.title(f"🤖 Welcome back, {st.session_state.username}!")
        st.success(f"You are successfully logged in as **{st.session_state.user_role}**")
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### Hellooooooooo!
            
            Welcome to Aizen, My multi-domain intelligence platform
            
    
            """)
            
            if st.button("Go to Unified Dashboard", type="primary", use_container_width=True):
                st.switch_page("pages/0_🏠_Dashboard.py")
        
        with col2:
            st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=150)
            st.info("""
            **Overview:**
            
            Role: **{role}**
            Status: **Active**
            
            **Access Level:**
            {access}
            """.format(
                role=st.session_state.user_role,
                access="🔓 Full Access" if st.session_state.user_role == "admin" else "🔒 Standard Access"
            ))
        
        st.markdown("---")
        
        # Quick navigation
        st.subheader("Quick Navigation")
        
        nav_cols = st.columns(4)
        
        with nav_cols[0]:
            if st.button("🏠 Unified Dashboard", use_container_width=True):
                st.switch_page("pages/0_🏠_Dashboard.py")
        
        with nav_cols[1]:
            if st.button("🛡️ Cybersecurity", use_container_width=True):
                st.switch_page("pages/2_🛡_Cybersecurity.py")
        
        with nav_cols[2]:
            if st.button("📊 Data Analytics", use_container_width=True):
                st.switch_page("pages/3_📊_Data_Science.py")
        
        with nav_cols[3]:
            if st.button("🤖 AI Assistant", use_container_width=True):
                st.switch_page("pages/5_🤖_AI_Assistant.py")
        
        st.markdown("---")

        # Logout button
        st.divider()
        if st.button("Logout", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_role = "user"
            st.session_state.user_obj = None
            st.success("You have been logged out successfully!")
            st.rerun()

#Run the main application
if __name__ == "__main__":
    main()