import streamlit as st
import os
from pathlib import Path
import json
import hashlib

def load_css():
    """Load custom CSS styles"""
    try:
        css_path = Path(__file__).parent / "styles.css"
        with css_path.open() as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Using default styling.")

USERS_FILE = Path(__file__).parent / "users.json"

def load_users():
    """Load user data from the JSON file"""
    if USERS_FILE.exists():
        with USERS_FILE.open("r") as f:
            return json.load(f)
    return []

def save_users(users):
    """Save user data to the JSON file"""
    with USERS_FILE.open("w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    """Register a new user. Returns (success, message)."""
    users = load_users()
    if any(u["username"] == username for u in users):
        return False, "Username already exists."
    hashed = hashlib.sha256(password.encode()).hexdigest()
    users.append({"username": username, "password": hashed})
    save_users(users)
    return True, "Registration successful."

def check_login(username, password):
    """Check login credentials"""
    users = load_users()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    for user in users:
        if user["username"] == username and user["password"] == hashed:
            return True
    return False

def check_authentication():
    """Check if user is authenticated, redirect to login if not"""
    if not st.session_state.get('logged_in', False):
        st.error("Please log in to access this page.")
        st.stop()

def initialize_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'username' not in st.session_state:
        st.session_state.username = ""
    
    if 'selected_country' not in st.session_state:
        st.session_state.selected_country = "United States"
    
    if 'selected_city' not in st.session_state:
        st.session_state.selected_city = "New York"
    
    if 'course_start_date' not in st.session_state:
        st.session_state.course_start_date = None
    
    if 'show_create_post' not in st.session_state:
        st.session_state.show_create_post = False
    
    if 'show_add_document' not in st.session_state:
        st.session_state.show_add_document = False
    
    if 'show_add_step' not in st.session_state:
        st.session_state.show_add_step = False

def format_currency(amount, country=None):
    """Format currency values based on country"""
    if country is None:
        country = st.session_state.get('selected_country', 'United States')
    
    currency_symbols = {
        'United States': '$',
        'United Kingdom': '£',
        'Canada': 'C$',
        'Australia': 'A$',
        'Germany': '€',
        'France': '€',
        'Netherlands': '€',
        'Sweden': 'kr',
        'Japan': '¥'
    }
    
    symbol = currency_symbols.get(country, '$')
    return f"{symbol}{amount:,.2f}"

def get_country_info():
    """Get comprehensive country information"""
    return {
        "United States": {
            "currency": "USD",
            "symbol": "$",
            "cities": ["New York", "Los Angeles", "Chicago", "Boston", "San Francisco", "Washington DC"],
            "visa_processing_time": "3-5 months",
            "popular_programs": ["MBA", "Computer Science", "Engineering", "Medicine"]
        },
        "United Kingdom": {
            "currency": "GBP",
            "symbol": "£",
            "cities": ["London", "Manchester", "Edinburgh", "Birmingham", "Oxford", "Cambridge"],
            "visa_processing_time": "3-4 months",
            "popular_programs": ["Business", "Law", "Engineering", "Medicine"]
        },
        "Canada": {
            "currency": "CAD",
            "symbol": "C$",
            "cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Waterloo"],
            "visa_processing_time": "4-6 months",
            "popular_programs": ["Engineering", "Business", "Computer Science", "Healthcare"]
        },
        "Australia": {
            "currency": "AUD",
            "symbol": "A$",
            "cities": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Canberra"],
            "visa_processing_time": "2-4 months",
            "popular_programs": ["Engineering", "Business", "Medicine", "Information Technology"]
        },
        "Germany": {
            "currency": "EUR",
            "symbol": "€",
            "cities": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne", "Stuttgart"],
            "visa_processing_time": "6-8 weeks",
            "popular_programs": ["Engineering", "Computer Science", "Business", "Research"]
        }
    }

def get_housing_options(city, country):
    """Get housing options for specific city"""
    housing_data = {
        "New York": {
            "student_dorms": {
                "price_range": "$800-1500/month",
                "description": "On-campus housing with meal plans",
                "pros": ["Close to campus", "Meal plans included", "Social environment"],
                "cons": ["Limited availability", "Higher cost", "Shared facilities"]
            },
            "shared_apartments": {
                "price_range": "$600-1200/month",
                "description": "Shared apartments with 2-4 roommates",
                "pros": ["Cost-effective", "More space", "Cooking facilities"],
                "cons": ["Longer commute", "Need to find roommates", "Utilities separate"]
            },
            "studio_apartments": {
                "price_range": "$1200-2500/month",
                "description": "Private studio apartments",
                "pros": ["Privacy", "Own kitchen", "Flexible lease"],
                "cons": ["Expensive", "Small space", "No social environment"]
            }
        },
        "London": {
            "student_dorms": {
                "price_range": "£600-1200/month",
                "description": "University-managed accommodation",
                "pros": ["University support", "Bills included", "Student community"],
                "cons": ["Limited privacy", "Strict rules", "Higher cost"]
            },
            "house_shares": {
                "price_range": "£400-800/month",
                "description": "Shared houses in residential areas",
                "pros": ["Affordable", "Local community", "More space"],
                "cons": ["Commute required", "Utility bills", "Finding housemates"]
            },
            "private_studios": {
                "price_range": "£800-1500/month",
                "description": "Private studio flats",
                "pros": ["Complete independence", "Own facilities", "Flexible"],
                "cons": ["Expensive", "Isolation", "All bills separate"]
            }
        }
    }
    
    # Default housing options if city not in database
    default_options = {
        "student_dorms": {
            "price_range": "Varies by location",
            "description": "University-provided accommodation",
            "pros": ["Convenient location", "Student support", "Social environment"],
            "cons": ["Limited availability", "Rules and regulations", "Shared facilities"]
        },
        "shared_housing": {
            "price_range": "Varies by location",
            "description": "Shared apartments or houses",
            "pros": ["Cost-effective", "Social interaction", "Flexible options"],
            "cons": ["Finding compatible roommates", "Shared responsibilities", "Potential conflicts"]
        },
        "private_accommodation": {
            "price_range": "Varies by location",
            "description": "Private apartments or studios",
            "pros": ["Privacy and independence", "Own space", "Flexible lifestyle"],
            "cons": ["Higher cost", "Less social interaction", "All responsibilities"]
        }
    }
    
    return housing_data.get(city, default_options)

def calculate_days_until(date_string):
    """Calculate days until a given date"""
    from datetime import datetime
    target_date = datetime.strptime(date_string, '%Y-%m-%d')
    today = datetime.now()
    return (target_date - today).days

def get_status_color(status):
    """Get color class for status"""
    status_colors = {
        'completed': 'positive',
        'in_progress': 'neutral',
        'pending': 'negative',
        'overdue': 'negative'
    }
    return status_colors.get(status, 'neutral')

def validate_form_data(data, required_fields):
    """Validate form data"""
    errors = []
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"{field.replace('_', ' ').title()} is required")
    return errors

def safe_divide(numerator, denominator):
    """Safely divide two numbers, return 0 if denominator is 0"""
    if denominator == 0:
        return 0
    return numerator / denominator

def truncate_text(text, max_length=100):
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def generate_id():
    """Generate a simple ID for new items"""
    import time
    return int(time.time() * 1000)

def sort_items_by_date(items, date_field, reverse=True):
    """Sort items by date field"""
    from datetime import datetime
    return sorted(items, key=lambda x: datetime.strptime(x[date_field], '%Y-%m-%d'), reverse=reverse)

def filter_items_by_category(items, category, category_field='category'):
    """Filter items by category"""
    if category == "All":
        return items
    return [item for item in items if item.get(category_field) == category]

def calculate_percentage(part, total):
    """Calculate percentage safely"""
    if total == 0:
        return 0
    return (part / total) * 100

def format_time_ago(timestamp_string):
    """Format timestamp as time ago"""
    from datetime import datetime
    timestamp = datetime.strptime(timestamp_string, "%Y-%m-%d %H:%M:%S")
    time_diff = datetime.now() - timestamp
    
    if time_diff.days > 0:
        return f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
    elif time_diff.seconds > 3600:
        hours = time_diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    else:
        minutes = time_diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"

def get_urgent_items(items, date_field, days_threshold=7):
    """Get items that are urgent (within threshold days)"""
    from datetime import datetime, timedelta
    threshold_date = datetime.now() + timedelta(days=days_threshold)
    
    urgent_items = []
    for item in items:
        item_date = datetime.strptime(item[date_field], '%Y-%m-%d')
        if item_date <= threshold_date:
            urgent_items.append(item)
    
    return urgent_items

def create_notification(message, type="info"):
    """Create a notification message"""
    if type == "success":
        st.success(message)
    elif type == "error":
        st.error(message)
    elif type == "warning":
        st.warning(message)
    else:
        st.info(message)

def export_data_to_csv(data, filename):
    """Export data to CSV format"""
    import pandas as pd
    import io
    
    df = pd.DataFrame(data)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def validate_email(email):
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_random_color():
    """Generate a random color for charts"""
    import random
    colors = ['#6366F1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16', '#F97316']
    return random.choice(colors)

def create_backup_data():
    """Create a backup of session state data"""
    backup_data = {
        'expenses': st.session_state.get('expenses', []),
        'budget': st.session_state.get('budget', {}),
        'visa_documents': st.session_state.get('visa_documents', []),
        'visa_timeline': st.session_state.get('visa_timeline', []),
        'community_posts': st.session_state.get('community_posts', []),
        'job_applications': st.session_state.get('job_applications', [])
    }
    return backup_data

def restore_backup_data(backup_data):
    """Restore data from backup"""
    for key, value in backup_data.items():
        st.session_state[key] = value

def render_sidebar():
    """Render navigation and quick action links in the sidebar."""
    with st.sidebar:
        st.header("Navigation")
        st.page_link("streamlit_app.py", label="Dashboard")
        st.page_link("pages/Expense_Tracker.py", label="Expense Tracker")
        st.page_link("pages/Expense_Calculator.py", label="Expense Calculator")
        st.page_link("pages/Visa_Planner.py", label="Visa Planner")
        st.page_link("pages/Community.py", label="Community")
        st.page_link("pages/Job_Board.py", label="Job Board")
        st.page_link("pages/Voice_Assistant.py", label="Voice Assistant")

        st.markdown("---")
        st.header("Quick Actions")
        st.page_link("pages/Expense_Tracker.py", label="Add Expense")
        st.page_link("pages/Community.py", label="Create Post")
        st.page_link("pages/Job_Board.py", label="Apply for Job")
        st.page_link("pages/Voice_Assistant.py", label="Ask Assistant")
