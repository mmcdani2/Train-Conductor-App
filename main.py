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
  .hamburger {
      position: fixed;
      top: 1rem;
      left: 1rem;
      cursor: pointer;
      z-index: 1001;
      background: none;
      border: none;
      padding: 0;
  }
  .hamburger div {
      width: 30px;
      height: 4px;
      background-color: white;
      margin: 6px 0;
  }
  .menu {
      background-color: #1e1e1e;
      position: fixed;
      top: 0;
      left: 0;
      width: 250px;
      height: 100%;
      padding: 2rem 1rem;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      box-shadow: 2px 0 10px rgba(0,0,0,0.5);
  }
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

def get_eligible_defenders():
    return [d["name"].strip() for d in supabase.table("defenders").select("name").execute().data]

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
if "show_menu" not in st.session_state:
    st.session_state.show_menu = False

def toggle_menu():
    st.session_state.show_menu = not st.session_state.show_menu

# ─── CONNECTION STATUS ───
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

# ─── ROUTING ───
page = st.session_state.page
if page == "Login":
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

elif page == "Create Account":
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

elif page == "Profile":
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

elif page == "Eligible Defenders":
    user = st.session_state.user
    st.title("🛡️ Eligible Defenders")
    st.markdown("### ➕ Add a New Defender")
    with st.form("add_defender_form"):
        name = st.text_input("Defender Name", placeholder="e.g. WarDaddy42")
        hq_level = st.number_input("HQ Level", min_value=1, max_value=35, step=1)
        submitted = st.form_submit_button("Add Defender")
        if submitted:
            if not name:
                st.warning("Please enter a name.")
            else:
                supabase.table("defenders").insert({
                    "name": name,
                    "hq_level": hq_level,
                    "user_id": user["id"],
                    "alliance": user["alliance"]
                }).execute()
                st.success(f"{name} added successfully!")
                st.rerun()
    st.divider()
    st.markdown("### 🧍 Current Defenders")
    response = supabase.table("defenders").select("*") \
        .eq("alliance", user["alliance"]) \
        .order("created_at", desc=False).execute()
    defenders = response.data
    if defenders:
        for d in defenders:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"**{d['name']}** | HQ: {d['hq_level']} | Added: {d['created_at'].split('T')[0]}")
            with col2:
                if st.button("❌", key=f"delete_{d['id']}"):
                    supabase.table("defenders").delete().eq("id", d["id"]).execute()
                    st.success(f"{d['name']} deleted.")
                    st.rerun()
    else:
        st.info("No defenders added yet.")

elif page == "Random Picker":
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
            eligible_defenders = get_eligible_defenders()
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

else:
    st.warning(f"Unknown page: {page}")
    st.session_state.page = "Login"
    st.rerun()
