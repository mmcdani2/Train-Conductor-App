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
for key in ["signup_stage", "updating", "defenders_confirmed", "editing_alliance"]:
    if key not in st.session_state:
        st.session_state[key] = False

# --- Load Users ---
users = load_users()

# --- Sidebar: Login / Signup ---
st.sidebar.header("🔐 User Login / Signup")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
confirm_password = None
if username and username not in users:
    confirm_password = st.sidebar.text_input("Confirm Password", type="password")

# --- Authentication Flow ---
if username and password and (username in users or confirm_password is not None):
    # Existing user login
    if username in users and users[username]["password"] == password:
        st.sidebar.success(f"✅ Logged in as {username}")
        user = users[username]

        # --- Main Profile Page ---
        st.subheader("📓 Your Profile")
        st.write(f"**Username:** {username}")
        st.write(f"**Server:** {user.get('server', '')}")
        st.write(f"**Alliance:** {user.get('alliance', '')}")

        # --- Update Alliance Form ---
        if not st.session_state["editing_alliance"]:
            if st.button("Update Alliance Name"):
                st.session_state["editing_alliance"] = True
        else:
            with st.form("alliance_form"):
                new_alliance = st.text_input("New Alliance Name", value=user.get('alliance', ''), key="alli_input")
                submitted = st.form_submit_button("Save Alliance Name")
                if submitted:
                    users[username]["alliance"] = new_alliance.strip()
                    save_users(users)
                    st.session_state["editing_alliance"] = False
                    st.success("✅ Alliance name updated!")

        # --- Eligible Defenders UI ---
        defenders = user.get("defenders", [])
        st.subheader("🛡️ Your Eligible Defenders")
        if defenders:
            html = (
                "<div style='max-height:200px; overflow-y:auto; padding:10px; "
                "background-color:#111; border:1px solid #444; border-radius:5px;'>"
                + "<br>".join(defenders) + "</div>"
            )
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("No defenders listed yet.")

        # --- Update Defenders ---
        if not st.session_state["updating"]:
            if st.button("Update Eligible Defenders"):
                st.session_state["updating"] = True
        else:
            with st.form("update_defenders_form"):
                updated = st.text_area("Update Defender List (one per line)", value="\n".join(defenders))
                submit = st.form_submit_button("Save Updated Defenders")
                if submit:
                    new_list = [n.strip() for n in updated.splitlines() if n.strip()]
                    users[username]["defenders"] = new_list
                    save_users(users)
                    st.session_state["updating"] = False
                    st.success("✅ Defender list updated!")

    # --- New user signup ---
    elif username not in users:
        st.sidebar.info("🆕 New user detected - please sign up below")
        with st.sidebar.form(key="signup_form"):
            server = st.text_input("Server Number", key="srv_input")
            alliance = st.text_input("Alliance Name", key="all_input")
            unlocked = st.checkbox("Our alliance has unlocked the VIP slot on the train", key="unlck_input")
            pwd1 = password
            pwd2 = confirm_password
            create = st.form_submit_button("Create Account")
            if create:
                if not server.strip() or not alliance.strip():
                    st.sidebar.warning("Server Number and Alliance Name required.")
                elif pwd1 != pwd2:
                    st.sidebar.warning("Passwords do not match.")
                else:
                    users[username] = {
                        "password": pwd1,
                        "server": server.strip(),
                        "alliance": alliance.strip(),
                        "unlocked": unlocked,
                        "defenders": []
                    }
                    save_users(users)
                    st.session_state["signup_stage"] = True
                    st.sidebar.success("✅ Account created! Proceed below.")
        if st.session_state["signup_stage"] and users[username].get("unlocked"):
            st.subheader("🛡️ Enter Eligible Defenders (one per line)")
            initial = st.text_area("Defenders List")
            if st.button("Confirm Eligible Defenders"):
                names = [n.strip() for n in initial.splitlines() if n.strip()]
                users[username]["defenders"] = names
                save_users(users)
                st.session_state["signup_stage"] = False
                st.success("✅ Defenders saved! You can now log in.")
        elif st.session_state["signup_stage"]:
            st.info("VIP slot not unlocked yet. You can add defenders later.")
    else:
        st.sidebar.error("❌ Incorrect password")
else:
    st.info("Please enter a username and password to continue.")
