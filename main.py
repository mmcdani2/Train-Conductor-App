import streamlit as st
import random
from datetime import datetime, timedelta
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import bcrypt

# ─── ENV & CLIENT SETUP ───
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── PAGE CONFIG ───
st.set_page_config(
    page_title="Last War Train Picker",
    page_icon="⚔️",
    layout="centered"
)

# ─── STYLES ───
st.markdown("""
<style>
  .css-18e3th9, .main > div { margin: 0 auto !important; max-width:100% !important; padding:0 1rem; }
  body { display:flex; justify-content:center; align-items:center; height:100vh; background:#121212; margin:0; }
  .card { width:100%; max-width:360px; background:#1e1e1e; padding:2rem; border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,0.3); }
  .card h1 { text-align:center; color:#fff; margin-bottom:1.5rem; font-size:1.75rem; }
  .stTextInput>label, .stForm label { color:#ccc; }
  .stTextInput, .stCheckbox, .stButton>button { width:100% !important; }
  .back-button { margin-top:1rem; background:none !important; border:none !important; color:#88f !important; text-decoration:underline; width:auto !important; }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ───
DAYS_LIMIT = 7

# ─── HELPERS ───
def health_check():
    try:
        supabase.table("users").select("id").limit(1).execute()
        return True
    except:
        return False

def signup(user, pwd, server, alliance, unlocked):
    pw_hash = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
    payload = {
        "username": user,
        "password_hash": pw_hash,
        "server": server,
        "alliance": alliance,
        "unlocked": unlocked,
        "defenders": []
    }
    supabase.table("users").insert(payload).execute()

def login(user, pwd):
    resp = supabase.table("users").select("*").eq("username", user).limit(1).execute()
    if resp.data and bcrypt.checkpw(pwd.encode(), resp.data[0]["password_hash"].encode()):
        return resp.data[0]
    return None

def get_eligible_defenders(alliance):
    return [d["name"].strip() for d in supabase.table("defenders").select("name").eq("alliance", alliance).execute().data]

def get_recent_picks(days=DAYS_LIMIT):
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
    result = supabase.table("picks").select("*").gte("picked_on", cutoff).execute()
    return {row["name"].strip().lower() for row in result.data} if result.data else set()

def insert_pick(name, role):
    supabase.table("picks").insert({
        "name": name,
        "role": role,
        "picked_on": datetime.utcnow().isoformat()
    }).execute()

# ─── STATE ───
if "page" not in st.session_state:
    st.session_state.page = "Login"
if "user" not in st.session_state:
    st.session_state.user = None

# ─── CONNECTION STATUS ───
st.markdown(f"**🔗 Supabase:** {'Connected' if health_check() else 'Disconnected'}")

# ─── SIDEBAR NAVIGATION ───
if st.session_state.user:
    user = st.session_state.user
    menu_options = ["Profile", "Random Picker", "Log Out"]
    if user.get("unlocked"):
        menu_options.insert(1, "Eligible Defenders")
    menu = st.sidebar.radio("📱 Navigation", menu_options)
    if menu == "Log Out":
        st.session_state.clear()
        st.session_state.page = "Login"
        st.rerun()
    else:
        st.session_state.page = menu

# ─── PROFILE PAGE ───
elif st.session_state.page == "Profile":
    user = st.session_state.user
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<h1>Welcome, {user['username']}!</h1>", unsafe_allow_html=True)
    st.markdown(f"**Server:** {user['server']}")
    st.markdown(f"**Alliance:** {user['alliance']}")
    st.markdown(f"**VIP Unlocked:** {'Yes' if user['unlocked'] else 'No'}")

    vip_toggle = st.checkbox("VIP slot unlocked?", value=user["unlocked"])
    if vip_toggle != user["unlocked"]:
        supabase.table("users").update({"unlocked": vip_toggle}).eq("id", user["id"]).execute()
        st.session_state.user["unlocked"] = vip_toggle
        st.success("VIP setting updated. Please refresh or navigate to see changes.")

    st.markdown('</div>', unsafe_allow_html=True)

# ─── RANDOM PICKER PAGE ───
elif st.session_state.page == "Random Picker":
    user = st.session_state.user
    st.title("🌟 VIP & Conductor Picker")
    user_input = st.text_area("Paste up to 20 contestant names (one per line):")
    contestants = [n.strip() for n in user_input.strip().split("\n") if n.strip()]
    if st.button("Pick Random VIP & Conductor"):
        if not contestants:
            st.warning("Please enter at least one contestant.")
            st.stop()

        recent_picks = get_recent_picks()
        contestants_pool = [c for c in contestants if c.lower() not in recent_picks]

        if user.get("unlocked"):
            eligible_defenders = get_eligible_defenders(user["alliance"])
            defenders_pool = [d for d in eligible_defenders if d.lower() not in recent_picks]
            if not defenders_pool:
                st.error("No eligible defenders available who haven't been picked in the last 7 days.")
                st.stop()

        if not contestants_pool:
            st.error("No eligible contestants available who haven't been picked in the last 7 days.")
            st.stop()

        attempts = 0
        max_attempts = 10
        while attempts < max_attempts:
            if user.get("unlocked"):
                defender = random.choice(defenders_pool)
            contestant = random.choice(contestants_pool)
            if not user.get("unlocked") or defender.lower() != contestant.lower():
                break
            attempts += 1
        else:
            st.error("Failed to find two different names after multiple attempts.")
            st.stop()

        if user.get("unlocked"):
            insert_pick(defender, "defender")
            st.success(f"🛡️ Defender Pick: **{defender}**")

        insert_pick(contestant, "contestant")
        st.success(f"🚂 Contestant Pick: **{contestant}**")
