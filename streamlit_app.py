import streamlit as st
import json
import os

st.set_page_config(page_title="Train Conductor & Defender Selector", layout="wide")
st.title("🚂 Train Conductor & Defender Selector")

USER_DB = "users.json"

def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(USER_DB, "w") as f:
        json.dump(data, f, indent=2)

# Initialize session state
if "updating" not in st.session_state:
    st.session_state["updating"] = False
if "defenders_confirmed" not in st.session_state:
    st.session_state["defenders_confirmed"] = False

users = load_users()

# Sidebar for login/signup
st.sidebar.header("🔐 User Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
confirm_password = None
if username and username not in users:
    confirm_password = st.sidebar.text_input("Confirm Password", type="password")

# Authentication flow
if username and password and (username in users or confirm_password is not None):
    if username in users and users[username]["password"] == password:
        # Existing user
        st.sidebar.success(f"✅ Logged in as {username}")
        defenders = users[username].get("defenders", [])

        # Display defenders in scrollable box
        st.subheader("🛡️ Your Eligible Defenders")
        if defenders:
            html = ("<div style='max-height:200px; overflow-y:auto; padding:10px; "
                    "background-color:#111111; border:1px solid #444; border-radius:5px;'>" +
                    "<br>".join(defenders) + "</div>")
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("No defenders listed yet.")

        # Update button
        if not st.session_state["updating"]:
            if st.button("Update Eligible Defenders"):
                st.session_state["updating"] = True
        else:
            # Update form
            with st.form("update_form"):
                updated = st.text_area("Update Defender List (one per line)", value="\n".join(defenders))
                submit = st.form_submit_button("Save Updated Defenders")
                if submit:
                    new_list = [n.strip() for n in updated.splitlines() if n.strip()]
                    users[username]["defenders"] = new_list
                    save_users(users)
                    st.session_state["updating"] = False
                    st.success("✅ Defender list updated!")
    elif username not in users:
        # New user signup
        if password and confirm_password:
            if password == confirm_password:
                if not st.session_state["defenders_confirmed"]:
                    initial = st.text_area("Enter Eligible Defenders (one per line)")
                    if st.button("Confirm Eligible Defenders"):
                        lst = [n.strip() for n in initial.splitlines() if n.strip()]
                        users[username] = {"password": password, "defenders": lst}
                        save_users(users)
                        st.session_state["defenders_confirmed"] = True
                        st.success("✅ Account created and logged in.")
                        st.experimental_rerun()
                else:
                    # After confirmation, display stored list
                    defenders = users[username].get("defenders", [])
                    st.subheader("🛡️ Your Eligible Defenders")
                    html = ("<div style='max-height:200px; overflow-y:auto; padding:10px; "
                            "background-color:#111111; border:1px solid #444; border-radius:5px;'>" +
                            "<br>".join(defenders) + "</div>")
                    st.markdown(html, unsafe_allow_html=True)
            else:
                st.sidebar.warning("Passwords do not match.")
        else:
            if password:
                st.sidebar.warning("Please confirm your password.")
    else:
        st.sidebar.error("❌ Incorrect password")
else:
    st.info("Please enter a username and password to continue.")
