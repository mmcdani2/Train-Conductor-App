import streamlit as st
from db.auth import login, signup

def login_page():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h1>Last War Train Picker</h1>', unsafe_allow_html=True)
    uname = st.text_input("Username", placeholder="Last War Username")
    pwd = st.text_input("Password", type="password", placeholder="••••••")
    col1, col2 = st.columns(2)
    if col1.button("Log In"):
        user = login(uname, pwd)
        if user:
            st.session_state.user = user
            st.session_state.page = "Profile"
            st.session_state.alliance = user["alliance"]
            st.rerun()
        else:
            st.error("Invalid credentials")
    col2.button("Create Account", on_click=lambda: st.session_state.__setitem__("page", "Create Account"), key="create_account_login")
    st.markdown('</div>', unsafe_allow_html=True)

def create_account_page():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h1>Create Account</h1>', unsafe_allow_html=True)
    new_u = st.text_input("New Username", placeholder="Last War Username")
    new_p = st.text_input("New Password", type="password", placeholder="••••••")
    confirm = st.text_input("Confirm Password", type="password", placeholder="••••••")
    srv = st.text_input("Server Number", placeholder="e.g., 42")
    ally = st.text_input("Alliance Name", placeholder="Your Alliance")
    unlocked = st.checkbox("VIP slot unlocked?")
    col1, col2 = st.columns(2)
    if col1.button("Sign Up", key="sign_up_button"):
        if not new_u or new_p != confirm or not srv or not ally:
            st.error("Fill all fields and match passwords.")
        else:
            signup(new_u, new_p, srv, ally, unlocked)
            st.success("Account created! Please log in.")
            st.session_state.page = "Login"
            st.rerun()
    col2.button("Back to Login", on_click=lambda: st.session_state.__setitem__("page", "Login"), key="back_to_login")
    st.markdown('</div>', unsafe_allow_html=True)
