import streamlit as st
from dotenv import load_dotenv
from styles import apply_styles
from utils.state import init_session_state
from db.auth import login
from pages.login_page import login_page, create_account_page
from pages.profile_page import profile_page
from pages.defenders_page import defenders_page
from pages.picker_page import picker_page
from utils.translate import t

# ─── HEADER ───
st.set_page_config(page_title="Last War Train Picker", page_icon="⚔️", layout="centered")

# ─── INITIAL SETUP ───
load_dotenv()
apply_styles()
init_session_state()

# ─── LANGUAGE SELECTION ───
if "language" not in st.session_state:
    st.session_state.language = "English"

st.sidebar.selectbox(
    label=t("language"),
    options=["English", "Spanish", "Portuguese", "Korean", "Indonesian"],
    index=["English", "Spanish", "Portuguese", "Korean", "Indonesian"].index(st.session_state.language),
    key="language"
)

# ─── CONNECTION STATUS ───
from db.auth import health_check
st.sidebar.markdown(t("connected") if health_check() else t("disconnected"))

# ─── SIDEBAR NAVIGATION ───
if st.session_state.user:
    st.sidebar.title("Navigation")
    if st.sidebar.button(t("profile")):
        st.session_state.page = "Profile"
    if st.session_state.user.get("unlocked") and st.sidebar.button(t("eligible_defenders")):
        st.session_state.page = "Eligible Defenders"
    if st.sidebar.button(t("random_picker")):
        st.session_state.page = "Random Picker"
    if st.sidebar.button(t("logout")):
        st.session_state.clear()
        st.session_state.page = "Login"
        st.rerun()

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
