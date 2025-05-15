import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import bcrypt

# ─── ENV & CLIENT SETUP ─────────────────────────────────────────────────────────
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Train Conductor App", layout="wide")
st.title("🚂 Train Conductor & Defender Selector")

# ─── HEALTH CHECK ───────────────────────────────────────────────────────────────
try:
    _ = supabase.table("users").select("id").limit(1).execute()
    st.sidebar.success("🔗 Supabase: Connected")
except Exception as e:
    st.sidebar.error(f"❌ Supabase connection failed:\n{e}")

# ─── AUTHENTICATION BRANCHING ────────────────────────────────────────────────────
if "user" not in st.session_state:
    # --- Not logged in: show Login + Signup ---
    st.subheader("🔐 Please log in or create an account")

    login_col, signup_col = st.columns(2)

    with login_col:
        st.markdown("#### 🔑 Log In")
        u = st.text_input("Username", key="login_user")
        p = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log In"):
            resp = (
                supabase
                .table("users")
                .select("*")
                .eq("username", u)
                .limit(1)
                .execute()
            )
            if resp.data and len(resp.data) == 1:
                row = resp.data[0]
                if bcrypt.checkpw(p.encode(), row["password_hash"].encode()):
                    st.session_state["user"] = row
                    st.success("✅ Logged in!")
                else:
                    st.error("❌ Incorrect password")
            else:
                st.error("❌ User not found")

    with signup_col:
        st.markdown("#### 🆕 Create Account")
        u2       = st.text_input("New Username", key="signup_user")
        p2       = st.text_input("New Password", type="password", key="signup_pass")
        p2_conf  = st.text_input("Confirm Password", type="password", key="signup_confirm")
        server   = st.text_input("Server Number", key="signup_server")
        alliance = st.text_input("Alliance Name", key="signup_alliance")
        unlocked = st.checkbox("VIP slot unlocked?", key="signup_unlocked")
        if st.button("Create Account"):
            # basic validation
            if not u2.strip():
                st.error("Enter a username")
            elif p2 != p2_conf or not p2:
                st.error("Passwords must match and not be empty")
            elif not server.strip() or not alliance.strip():
                st.error("Server and Alliance are required")
            else:
                pw_hash = bcrypt.hashpw(p2.encode(), bcrypt.gensalt()).decode()
                payload = {
                    "username":      u2.strip(),
                    "password_hash": pw_hash,
                    "server":        server.strip(),
                    "alliance":      alliance.strip(),
                    "unlocked":      unlocked,
                    "defenders":     []
                }
                try:
                    supabase.table("users").insert(payload).execute()
                    st.success("✅ Account created! Please log in.")
                except Exception as e:
                    st.error(f"Failed to create account: {e}")

else:
    # --- Logged in: show profile + next steps ---
    user = st.session_state["user"]
    st.subheader(f"👋 Welcome, {user['username']}!")
    st.markdown(f"**Server:** {user['server']}")
    st.markdown(f"**Alliance:** {user['alliance']}")
    st.markdown(f"**VIP Slot Unlocked:** {user['unlocked']}")

    st.markdown("— next we’ll add your VS/Tech inputs and random picks here —")
