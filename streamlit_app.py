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
except Exception as e:
    st.sidebar.error(f"❌ Supabase connection failed:\n{e}")

# ─── Authentication Section ────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.title("🔑 Login or Create Account")
    col1, col2 = st.columns(2)

    # --- Login Form ---
    with col1:
        st.subheader("🔐 Log In")
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log In"):
            res = supabase.table("users").select("*").eq("username", login_user).limit(1).execute()
            if res.data and len(res.data) == 1:
                user_row = res.data[0]
                if bcrypt.checkpw(login_pass.encode(), user_row["password_hash"].encode()):
                    st.session_state["user"] = user_row
                    st.experimental_rerun()
                else:
                    st.error("❌ Incorrect password")
            else:
                st.error("❌ User not found")

    # --- Signup Form ---
    with col2:
        st.subheader("🆕 Create Account")
        signup_user = st.text_input("New Username", key="signup_user")
        signup_pass = st.text_input("New Password", type="password", key="signup_pass")
        signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
        server = st.text_input("Server Number", key="server")
        alliance = st.text_input("Alliance Name", key="alliance")
        unlocked = st.checkbox("Our alliance has unlocked the VIP slot", key="unlocked")
        if st.button("Create Account"):
            # Basic validation
            if not signup_user.strip():
                st.error("Please enter a username.")
            elif signup_pass != signup_confirm or not signup_pass:
                st.error("Passwords must match and not be empty.")
            elif not server.strip() or not alliance.strip():
                st.error("Server Number and Alliance Name are required.")
            else:
                pw_hash = bcrypt.hashpw(signup_pass.encode(), bcrypt.gensalt()).decode()
                payload = {
                    "username":      signup_user.strip(),
                    "password_hash": pw_hash,
                    "server":        server.strip(),
                    "alliance":      alliance.strip(),
                    "unlocked":      unlocked
                }
                try:
                    supabase.table("users").insert(payload).execute()
                    st.success("✅ Account created! You can now log in.")
                except Exception as e:
                    st.error(f"Failed to create account: {e}")

    # Stop here until authenticated
    st.stop()

# ─── Logged-in User View ───────────────────────────────────────────────────────
user = st.session_state["user"]
st.title(f"👋 Welcome, {user['username']}!")
st.write(f"**Server:** {user['server']}")
st.write(f"**Alliance:** {user['alliance']}")
