import streamlit as st

def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "Login"
    if "user" not in st.session_state:
        st.session_state.user = None
    if "show_menu" not in st.session_state:
        st.session_state.show_menu = False

def toggle_menu():
    st.session_state.show_menu = not st.session_state.show_menu
