import streamlit as st
from utils import load_css, initialize_session_state, register_user

st.set_page_config(page_title="Register", page_icon="📝", layout="wide")

load_css()
initialize_session_state()

st.markdown("## Create a New Account")

with st.form("registration_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    submit = st.form_submit_button("Register")

    if submit:
        if not username or not password:
            st.error("Username and password are required.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            success, msg = register_user(username, password)
            if success:
                st.success(msg)
            else:
                st.error(msg)

st.link_button("Back to Login", "./")
