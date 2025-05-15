import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import bcrypt

# ─── Load environment variables ────────────────────────────────────────────────
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ─── Initialize Supabase client ───────────────────────────────────────────────
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── Streamlit page config ────────────────────────────────────────────────────
st.set_page_config(page_title="User Signup & Login", layout="centered")

# ─── Supabase Health Check ─────────────────────────────────────────────────────
try:
    resp = supabase.table("users").select("id,username").limit(1).execute()
    st.sidebar.markdown("**🔗 Supabase Status:** ✅ Connected")
    st.sidebar.write("Sample response:", resp.data)
except Exception as e:
    st.sidebar.error(f"❌ Supabase connection failed:\n{e}")

# ─── Login Flow ────────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.sidebar.subheader("🔑 Log In")
    login_user = st.sidebar.text_input("Username", key="login_user")
    login_pass = st.sidebar.text_input("Password", type="password", key="login_pass")
    if st.sidebar.button("Log In"):
        res = supabase.table("users").select("*").eq("username", login_user).limit(1).execute()
        if res.data and len(res.data) == 1:
            user_row = res.data[0]
            if bcrypt.checkpw(login_pass.encode(), user_row["password_hash"].encode()):
                st.session_state["user"] = user_row
                st.sidebar.success(f"Logged in as {login_user}")
            else:
                st.sidebar.error("❌ Incorrect password")
        else:
            st.sidebar.error("❌ User not found")
    st.stop()

# ─── Logged-in User View ───────────────────────────────────────────────────────
user = st.session_state["user"]
st.title(f"👋 Welcome, {user['username']}!")
st.write(f"**Server:** {user['server']}")
st.write(f"**Alliance:** {user['alliance']}")

# ─── Sign-up form (hidden once logged in) ──────────────────────────────────────
with st.form("signup_form"):
    st.subheader("🆕 Create a New User Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    confirm   = st.text_input("Confirm Password", type="password")
    server    = st.text_input("Server Number")
    alliance  = st.text_input("Alliance Name")
    unlocked  = st.checkbox("Our alliance has unlocked the VIP slot on the train")
    submit_btn = st.form_submit_button("Create Account")

    if submit_btn:
        if not new_user.strip():
            st.error("Please enter a username.")
        elif new_pass != confirm or not new_pass:
            st.error("Passwords must match and not be empty.")
        elif not server.strip() or not alliance.strip():
            st.error("Server Number and Alliance Name are required.")
        else:
            pw_hash = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt()).decode()
            payload = {
                "username":      new_user.strip(),
                "password_hash": pw_hash,
                "server":        server.strip(),
                "alliance":      alliance.strip(),
                "unlocked":      unlocked
            }
            try:
                supabase.table("users").insert(payload).execute()
                st.success("✅ Account created successfully! Please log in.")
            except Exception as e:
                st.error(f"Failed to create account: {e}")
