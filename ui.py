import streamlit as st

from app import app_page


def login():
    st.set_page_config(page_title="Login To Games...", page_icon=":guardsman:", layout="wide")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if username == "admin" and password == "password":
            st.success("Logged in as admin")
            app_page();
        else:
            st.error("Invalid credentials")

# Run the login page
login()
