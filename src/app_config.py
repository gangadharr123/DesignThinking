# Configuration for Hugging Face Spaces deployment
import streamlit as st
import os

# Hugging Face Spaces configuration
def configure_for_hf_spaces():
    """Configure the app for Hugging Face Spaces deployment"""
    
    # Set page config for HF Spaces
    if not hasattr(st, '_is_running_with_streamlit'):
        st.set_page_config(
            page_title="StudyAbroad Platform",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'About': "International Student Platform - Your comprehensive tool for studying abroad"
            }
        )
    
    # Environment-specific configurations
    if os.getenv('SPACE_ID'):  # Running on HF Spaces
        # Disable some features that might not work well in HF Spaces
        st.markdown("""
        <style>
        .stApp > header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

# Dependencies check
def check_dependencies():
    """Check if all required packages are available"""
    required_packages = ['streamlit', 'pandas', 'plotly']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        st.error(f"Missing required packages: {', '.join(missing_packages)}")
        st.info("Please install the missing packages to run the application.")
        return False
    
    return True