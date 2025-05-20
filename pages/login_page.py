import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

# ─── Load Environment Variables ──────────────────────────────
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── Translation Dictionary ─────────────────────────────────
# (Your translation dictionary goes here — cut for brevity)

def t(key):
    lang = st.session_state.get("language", "English")
    return translations.get(lang, translations["English"]).get(key, key)

def login_page():
    st.title(t("app_title"))
    username = st.text_input(t("username_label"), placeholder=t("username_placeholder"))
    password = st.text_input(t("password_label"), type="password")

    if st.button(t("login_button")):
        if not username or not password:
            st.error(t("invalid_credentials"))
            return

        # Supabase auth check
        response = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
        if response.data:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.experimental_rerun()
        else:
            st.error(t("invalid_credentials"))

    if st.button(t("create_account")):
        st.session_state["current_page"] = "create_account"

def create_account_page():
    st.title(t("create_account_title"))

    new_username = st.text_input(t("new_username_label"))
    new_password = st.text_input(t("new_password_label"), type="password")
    confirm_password = st.text_input(t("confirm_password_label"), type="password")
    server = st.text_input(t("server_label"))
    alliance = st.text_input(t("alliance_label"), placeholder=t("alliance_placeholder"))
    vip = st.checkbox(t("vip_checkbox"))

    if st.button(t("signup_button")):
        if not all([new_username, new_password, confirm_password, server, alliance]) or new_password != confirm_password:
            st.error(t("fill_fields_error"))
            return

        # Add to Supabase
        supabase.table("users").insert({
            "username": new_username,
            "password": new_password,
            "server": server,
            "alliance": alliance,
            "vip": vip
        }).execute()

        st.success(t("account_created"))
        st.session_state["current_page"] = "login"

    if st.button(t("back_to_login")):
        st.session_state["current_page"] = "login"
