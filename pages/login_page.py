import streamlit as st
from db.auth import login, signup
from utils.translate import t

# Translation keys required for this page are now included in translate.py:
# "app_title": "Last War Train Picker",
# "username_label": "Username",
# "username_placeholder": "Last War Username",
# "password_label": "Password",
# "login_button": "Log In",
# "invalid_credentials": "Invalid credentials",
# "create_account": "Create Account",
# "create_account_title": "Create Account",
# "new_username_label": "New Username",
# "new_password_label": "New Password",
# "confirm_password_label": "Confirm Password",
# "server_label": "Server Number",
# "alliance_label": "Alliance Name",
# "alliance_placeholder": "Your Alliance",
# "vip_checkbox": "VIP slot unlocked?",
# "signup_button": "Sign Up",
# "fill_fields_error": "Fill all fields and match passwords.",
# "account_created": "Account created! Please log in.",
# "back_to_login": "Back to Login"

def login_page():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<h1>{t("app_title")}</h1>', unsafe_allow_html=True)
    uname = st.text_input(t("username_label"), placeholder=t("username_placeholder"))
    pwd = st.text_input(t("password_label"), type="password", placeholder="••••••")
    col1, col2 = st.columns(2)
    if col1.button(t("login_button")):
        user = login(uname, pwd)
        if user:
            st.session_state.user = user
            st.session_state.page = "Profile"
            st.session_state.alliance = user["alliance"]
            st.rerun()
        else:
            st.error(t("invalid_credentials"))
    col2.button(t("create_account"), on_click=lambda: st.session_state.__setitem__("page", "Create Account"), key="create_account_login")
    st.markdown('</div>', unsafe_allow_html=True)

def create_account_page():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<h1>{t("create_account_title")}</h1>', unsafe_allow_html=True)
    new_u = st.text_input(t("new_username_label"), placeholder=t("username_placeholder"))
    new_p = st.text_input(t("new_password_label"), type="password", placeholder="••••••")
    confirm = st.text_input(t("confirm_password_label"), type="password", placeholder="••••••")
    srv = st.text_input(t("server_label"), placeholder="e.g., 42")
    ally = st.text_input(t("alliance_label"), placeholder=t("alliance_placeholder"))
    unlocked = st.checkbox(t("vip_checkbox"))
    col1, col2 = st.columns(2)
    if col1.button(t("signup_button"), key="sign_up_button"):
        if not new_u or new_p != confirm or not srv or not ally:
            st.error(t("fill_fields_error"))
        else:
            signup(new_u, new_p, srv, ally, unlocked)
            st.success(t("account_created"))
            st.session_state.page = "Login"
            st.rerun()
    col2.button(t("back_to_login"), on_click=lambda: st.session_state.__setitem__("page", "Login"), key="back_to_login")
    st.markdown('</div>', unsafe_allow_html=True)
