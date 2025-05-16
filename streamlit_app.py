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

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Train Conductor App", layout="wide")
st.markdown("""
<style>
  .main > div {max-width: 600px; margin: auto;}
  input, .stButton>button {width: 100% !important;}
</style>
""", unsafe_allow_html=True)

# ─── HELPER FUNCTIONS ──────────────────────────────────────────────────────────
def health_check():
    try:
        supabase.table("users").select("id").limit(1).execute()
        return True
    except:
        return False

def signup(user, pwd, server, alliance, unlocked):
    pw_hash = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
    payload = {"username": user, "password_hash": pw_hash,
               "server": server, "alliance": alliance,
               "unlocked": unlocked, "defenders": []}
    supabase.table("users").insert(payload).execute()

def login(user, pwd):
    resp = supabase.table("users").select("*").eq("username", user).limit(1).execute()
    if resp.data and bcrypt.checkpw(pwd.encode(), resp.data[0]["password_hash"].encode()):
        return resp.data[0]
    return None

# ─── NAVIGATION ────────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Login"
if "user" not in st.session_state:
    st.session_state.user = None

# Always show status
status = "Connected" if health_check() else "Disconnected"
st.sidebar.markdown(f"**🔗 Supabase:** {status}")

# Menu when logged in
if st.session_state.user:
    st.sidebar.header("📑 Menu")
    st.session_state.page = st.sidebar.radio("Go to", ["Profile", "Random Picker", "Eligible Defenders"] )
else:
    st.sidebar.header("👤 Account")
    st.session_state.page = st.sidebar.radio("Go to", ["Login", "Create Account"] )

# ─── PAGE: LOGIN ───────────────────────────────────────────────────────────────
if st.session_state.page == "Login":
    st.title("🔐 Login")
    uname = st.text_input("Username", key="l_user")
    pwd = st.text_input("Password", type="password", key="l_pwd")
    if st.button("Log In"):
        user = login(uname, pwd)
        if user:
            st.session_state.user = user
            st.success("Logged in!")
        else:
            st.error("Invalid credentials")

# ─── PAGE: CREATE ACCOUNT ─────────────────────────────────────────────────────
elif st.session_state.page == "Create Account":
    st.title("🆕 Create Account")
    new_u = st.text_input("New Username", key="c_user")
    new_p = st.text_input("New Password", type="password", key="c_pwd")
    confirm = st.text_input("Confirm Password", type="password", key="c_conf")
    srv = st.text_input("Server Number")
    ally = st.text_input("Alliance Name")
    unlocked = st.checkbox("VIP slot unlocked?", key="c_unlocked")
    if st.button("Sign Up"):
        if not new_u or new_p != confirm or not srv or not ally:
            st.error("Fill all fields and match passwords.")
        else:
            signup(new_u, new_p, srv, ally, unlocked)
            st.success("Account created! Please login.")

# ─── PAGE: PROFILE ─────────────────────────────────────────────────────────────
elif st.session_state.page == "Profile":
    user = st.session_state.user
    st.title(f"👤 Profile: {user['username']}")
    st.markdown(f"**Server:** {user['server']}")
    st.markdown(f"**Alliance:** {user['alliance']}")
    st.markdown(f"**VIP Unlocked:** {user['unlocked']} ")

# ─── PAGE: RANDOM PICKER ────────────────────────────────────────────────────────
elif st.session_state.page == "Random Picker":
    st.title("🎲 Random Picker")
    # Placeholder
    st.info("VS/Tech input and random selection will go here.")

# ─── PAGE: ELIGIBLE DEFENDERS ───────────────────────────────────────────────────
elif st.session_state.page == "Eligible Defenders":
    st.title("🛡️ Eligible Defenders")
    user = st.session_state.user
    defenders = user.get("defenders", [])
    if defenders:
        st.write(defenders)
    else:
        st.info("No defenders configured.")
