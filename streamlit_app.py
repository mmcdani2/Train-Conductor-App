import streamlit as st
import json
import os

# --- App Configuration ---
st.set_page_config(page_title="Train Conductor & Defender Selector", layout="wide")
st.title("🚂 Train Conductor & Defender Selector")

# --- Data Files ---
USER_DB = "users.json"

# --- Utility Functions ---
def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(USER_DB, "w") as f:
        json.dump(data, f, indent=2)

# --- Session State Init ---
if "signup_stage" not in st.session_state:
    st.session_state["signup_stage"] = "start"  # tracks new-user flow

# --- Load Users ---
users = load_users()

# --- Sidebar: User Login / Signup ---
st.sidebar.header("🔐 User Login / Signup")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username and password:
    if username in users and users[username]["password"] == password:
        # Existing user login
        st.sidebar.success(f"✅ Logged in as {username}")
        user = users[username]
        # Display profile
        st.subheader("🗒️ Your Profile")
        st.write(f"**Server:** {user.get('server', '')}")
        st.write(f"**Alliance:** {user.get('alliance', '')}")

        # Eligible Defenders UI will go here later...

    elif username not in users:
        # New user signup
        st.sidebar.info("🆕 New user detected - complete signup below")
        with st.sidebar.form(key="signup_form"):
            server = st.text_input("Server Number", key="server_input")
            alliance = st.text_input("Alliance Name")
            unlocked = st.checkbox("My alliance has unlocked the VIP slot on the train")
            pwd1 = password  # first password entry
            pwd2 = st.text_input("Confirm Password", type="password")
            create_btn = st.form_submit_button("Create Account")

            if create_btn:
                # Validate inputs
                if not server.strip() or not alliance.strip():
                    st.sidebar.warning("Please provide Server Number and Alliance Name.")
                elif pwd1 != pwd2:
                    st.sidebar.warning("Passwords do not match.")
                else:
                    # Initialize user record
                    users[username] = {
                        "password": pwd1,
                        "server": server.strip(),
                        "alliance": alliance.strip(),
                        "unlocked": unlocked,
                        "defenders": []
                    }
                    save_users(users)
                    st.session_state["signup_stage"] = "defender_entry"  # next stage
                    st.sidebar.success("✅ Account created successfully!")

        # After account creation, prompt for defenders if unlocked
        if st.session_state["signup_stage"] == "defender_entry":
            if users[username]["unlocked"]:
                st.subheader("🛡️ Enter Eligible Defenders (one per line)")
                initial = st.text_area("Defenders List")
                if st.button("Confirm Eligible Defenders"):
                    names = [n.strip() for n in initial.splitlines() if n.strip()]
                    users[username]["defenders"] = names
                    save_users(users)
                    st.session_state["signup_stage"] = "completed"
                    st.success("✅ Defenders list saved! Log in again to proceed.")
            else:
                st.info("Your alliance hasn't unlocked the VIP slot yet. You can add defenders once unlocked.")

    else:
        st.sidebar.error("❌ Incorrect password")
else:
    st.info("Please enter a username and password to log in or sign up.")
