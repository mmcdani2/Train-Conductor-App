import streamlit as st
from dotenv import load_dotenv
from styles import apply_styles
from utils.state import init_session_state, toggle_menu
from db.auth import login
from pages.login_page import login_page, create_account_page
from pages.profile_page import profile_page
from pages.defenders_page import defenders_page
from pages.picker_page import picker_page

# ─── HEADER ───
st.set_page_config(page_title="Last War Train Picker", page_icon="⚔️", layout="centered")
apply_styles()

# ─── INITIAL SETUP ───
load_dotenv()
apply_styles()
init_session_state()

# ─── CONNECTION STATUS ───
from db.auth import health_check
st.markdown(f"**🔗 Supabase:** {'Connected' if health_check() else 'Disconnected'}")

# ─── HAMBURGER NAVIGATION ───
if st.session_state.user:
    col1, _ = st.columns([1, 10])
    with col1:
        if st.button("☰", key="hamburger", on_click=toggle_menu):
            pass

    if st.session_state.show_menu:
        st.markdown('<div class="menu">', unsafe_allow_html=True)
        if st.button("👤 Profile"):
            st.session_state.page = "Profile"
            st.session_state.show_menu = False
            st.rerun()
        if st.session_state.user.get("unlocked") and st.button("🛡️ Eligible Defenders"):
            st.session_state.page = "Eligible Defenders"
            st.session_state.show_menu = False
            st.rerun()
        if st.button("🎲 Random Picker"):
            st.session_state.page = "Random Picker"
            st.session_state.show_menu = False
            st.rerun()
        if st.button("🚪 Log Out"):
            st.session_state.clear()
            st.session_state.page = "Login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ─── PAGE ROUTING ───
page = st.session_state.page
if page == "Login":
    login_page()
elif page == "Create Account":
    create_account_page()
elif page == "Profile":
    profile_page()
elif page == "Eligible Defenders":
    defenders_page()
elif page == "Random Picker":
    picker_page()
else:
    st.warning(f"Unknown page: {page}")
    st.session_state.page = "Login"
    st.rerun()
