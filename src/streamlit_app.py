import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    load_css,
    check_login,
    initialize_session_state,
    format_currency,
    get_country_info,
    render_sidebar,
)
from app_config import configure_for_hf_spaces, check_dependencies

def calculate_user_progress():
    """Calculate user progress for gamification"""
    progress = {
        'profile_progress': 100,  # Country and city selected
        'visa_progress': 0,
        'budget_health': 75,
        'overall_score': 150
    }
    
    # Calculate visa progress
    if 'visa_documents' in st.session_state:
        completed_docs = len([doc for doc in st.session_state.visa_documents if doc['status'] == 'completed'])
        total_docs = len(st.session_state.visa_documents)
        progress['visa_progress'] = int((completed_docs / total_docs) * 100) if total_docs > 0 else 0
    
    # Calculate budget health
    if 'expenses' in st.session_state and 'budget' in st.session_state:
        total_budget = sum(st.session_state.budget.values())
        total_spent = sum([exp['amount'] for exp in st.session_state.expenses])
        if total_budget > 0:
            budget_usage = (total_spent / total_budget) * 100
            progress['budget_health'] = max(0, int(100 - budget_usage)) if budget_usage > 0 else 100
    
    # Calculate overall score
    progress['overall_score'] = int(
        (progress['profile_progress'] + progress['visa_progress'] + progress['budget_health']) / 3 * 2
    )
    
    return progress

# Verify dependencies before continuing
if not check_dependencies():
    st.stop()

# Page configuration
st.set_page_config(
    page_title="StudyAbroad Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
configure_for_hf_spaces()

# Load custom CSS
load_css()

# Initialize session state
initialize_session_state()

# Sidebar navigation
if st.session_state.get("logged_in", False):
    render_sidebar()

def main():
    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        login_page()
    else:
        dashboard()

def login_page():
    st.markdown("""
    <div class="login-container">
        <div class="login-card">
            <h1>🎓 StudyAbroad Platform</h1>
            <p>Your comprehensive platform for international student life</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Welcome Back!")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            login_button = st.form_submit_button("Login", use_container_width=True)
            
            if login_button:
                if check_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        st.page_link("pages/Register.py", label="Create a new account")

def dashboard():
    st.markdown("""
    <div class="breadcrumb">
        <span>🎓 StudyAbroad Platform</span> > <span>Dashboard</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Country/City selection and header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title(f"Welcome back, {st.session_state.username}! 👋")
        st.markdown("Here's your personalized dashboard for studying abroad")
    
    with col2:
        country_info = get_country_info()
        countries = list(country_info.keys())
        
        selected_country = st.selectbox(
            "🌍 Study Destination",
            countries,
            index=countries.index(st.session_state.selected_country),
            key="country_selector"
        )
        
        if selected_country != st.session_state.selected_country:
            st.session_state.selected_country = selected_country
            # Reset city to first option when country changes
            st.session_state.selected_city = country_info[selected_country]["cities"][0]
            st.rerun()
    
    with col3:
        cities = country_info[st.session_state.selected_country]["cities"]
        selected_city = st.selectbox(
            "🏙️ City",
            cities,
            index=cities.index(st.session_state.selected_city) if st.session_state.selected_city in cities else 0,
            key="city_selector"
        )
        
        if selected_city != st.session_state.selected_city:
            st.session_state.selected_city = selected_city
            st.rerun()
    
    # Logout button
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col4:
        if st.button("Logout", type="secondary"):
            st.session_state.logged_in = False
            st.rerun()
    
    # Display selected destination info
    current_country_info = country_info[st.session_state.selected_country]
    st.markdown(f"""
    <div class="destination-info">
        <h4>📍 Your Selected Destination: {st.session_state.selected_city}, {st.session_state.selected_country}</h4>
        <p><strong>Currency:</strong> {current_country_info['currency']} ({current_country_info['symbol']})</p>
        <p><strong>Visa Processing Time:</strong> {current_country_info['visa_processing_time']}</p>
        <p><strong>Popular Programs:</strong> {', '.join(current_country_info['popular_programs'])}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Format currency based on selected country
    currency_symbol = current_country_info['symbol']
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-content">
                <h3>Monthly Budget</h3>
                <div class="metric-value">{currency_symbol}1,250</div>
                <div class="metric-change positive">+5% from last month</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">📋</div>
            <div class="metric-content">
                <h3>Visa Status</h3>
                <div class="metric-value">In Progress</div>
                <div class="metric-change neutral">3 documents pending</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">💬</div>
            <div class="metric-content">
                <h3>Community Posts</h3>
                <div class="metric-value">12</div>
                <div class="metric-change positive">+3 new replies</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">💼</div>
            <div class="metric-content">
                <h3>Job Applications</h3>
                <div class="metric-value">5</div>
                <div class="metric-change positive">2 responses pending</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Welcome progress section
    st.subheader("🎯 Your Study Abroad Journey")
    
    # Calculate progress scores for gamification
    progress_data = calculate_user_progress()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="progress-badge">
            <div class="badge-icon">📝</div>
            <div class="badge-content">
                <h4>Profile Setup</h4>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress_data['profile_progress']}%"></div>
                </div>
                <div class="progress-text">{progress_data['profile_progress']}% Complete</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="progress-badge">
            <div class="badge-icon">📋</div>
            <div class="badge-content">
                <h4>Visa Progress</h4>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress_data['visa_progress']}%"></div>
                </div>
                <div class="progress-text">{progress_data['visa_progress']}% Complete</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="progress-badge">
            <div class="badge-icon">💰</div>
            <div class="badge-content">
                <h4>Budget Health</h4>
                <div class="progress-bar">
                    <div class="progress-fill {'positive' if progress_data['budget_health'] > 70 else 'negative'}" style="width: {progress_data['budget_health']}%"></div>
                </div>
                <div class="progress-text">{progress_data['budget_health']}% On Track</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="progress-badge">
            <div class="badge-icon">🏆</div>
            <div class="badge-content">
                <h4>Overall Score</h4>
                <div class="score-circle">
                    <div class="score-number">{progress_data['overall_score']}</div>
                    <div class="score-label">points</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Action Buttons
    st.subheader("🚀 Quick Actions")
    st.markdown("Click on any feature to get started with your study abroad journey")
    
    # Feature buttons with navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💰 Expense Tracker", key="expense_btn", use_container_width=True, type="primary"):
            st.switch_page("pages/Expense_Tracker.py")
        
        st.markdown("""
        <div class="feature-preview">
            <h4>Track Your Finances</h4>
            <p>✓ Daily expense tracking</p>
            <p>✓ Budget management</p>
            <p>✓ Visual spending analysis</p>
            <p>✓ Multi-currency support</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧮 Expense Calculator", key="calc_btn", use_container_width=True):
            st.switch_page("pages/Expense_Calculator.py")
        
        st.markdown("""
        <div class="feature-preview">
            <h4>Plan Your Budget</h4>
            <p>✓ Cost estimates by country</p>
            <p>✓ Lifestyle-based calculations</p>
            <p>✓ Custom budget planning</p>
            <p>✓ Emergency fund advice</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("📋 Visa Planner", key="visa_btn", use_container_width=True, type="primary"):
            st.switch_page("pages/Visa_Planner.py")
        
        st.markdown("""
        <div class="feature-preview">
            <h4>Manage Your Visa Process</h4>
            <p>✓ Document checklist</p>
            <p>✓ Timeline tracking</p>
            <p>✓ Deadline alerts</p>
            <p>✓ Housing information</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💬 Community Forum", key="community_btn", use_container_width=True):
            st.switch_page("pages/Community.py")
        
        st.markdown("""
        <div class="feature-preview">
            <h4>Connect & Share</h4>
            <p>✓ Student discussions</p>
            <p>✓ Experience sharing</p>
            <p>✓ Study groups</p>
            <p>✓ Trending topics</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("💼 Job Board", key="job_btn", use_container_width=True, type="primary"):
            st.switch_page("pages/Job_Board.py")
        
        st.markdown("""
        <div class="feature-preview">
            <h4>Find Student Jobs</h4>
            <p>✓ Part-time opportunities</p>
            <p>✓ On-campus & remote jobs</p>
            <p>✓ Application tracking</p>
            <p>✓ Work authorization help</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Achievement badge
        st.markdown("""
        <div class="achievement-badge">
            <h4>🏆 Today's Achievement</h4>
            <p><strong>Profile Complete!</strong></p>
            <p>You've set up your destination preferences. Keep going!</p>
            <div class="achievement-points">+50 points earned</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activity
    st.subheader("Recent Activity")
    
    activity_data = [
        {"time": "2 hours ago", "action": f"Added expense: Groceries - {format_currency(45.50)}", "type": "expense"},
        {"time": "1 day ago", "action": "Uploaded visa document: Bank Statement", "type": "visa"},
        {"time": "2 days ago", "action": "Posted in Community: Housing Tips", "type": "community"},
        {"time": "3 days ago", "action": "Applied for part-time job: Campus Library", "type": "job"}
    ]
    
    for activity in activity_data:
        icon = {"expense": "💰", "visa": "📋", "community": "💬", "job": "💼"}[activity["type"]]
        st.markdown(f"""
        <div class="activity-item">
            <span class="activity-icon">{icon}</span>
            <div class="activity-content">
                <div class="activity-action">{activity["action"]}</div>
                <div class="activity-time">{activity["time"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
