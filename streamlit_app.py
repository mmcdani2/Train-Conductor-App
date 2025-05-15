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

users = load_users()

st.sidebar.header("🔐 User Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username and password:
    if username in users:
        if users[username]["password"] == password:
            st.sidebar.success(f"✅ Logged in as {username}")
            defenders = users[username].get("defenders", [])

            st.subheader("🛡️ Your Eligible Defenders")
            if defenders:
                st.write(defenders)
            else:
                st.info("No defenders listed yet.")

            if st.button("Update Eligible Defenders"):
                updated_defenders = st.text_area("Update Defender List (one per line)", value="\n".join(defenders))
                if updated_defenders:
                    new_defenders = [name.strip() for name in updated_defenders.splitlines() if name.strip()]
                    users[username]["defenders"] = new_defenders
                    save_users(users)
                    st.success("✅ Defender list updated!")
        else:
            st.sidebar.error("❌ Incorrect password")
    else:
        st.sidebar.info("🆕 New user detected")
        confirm_password = st.sidebar.text_input("Confirm Password", type="password")
        if password == confirm_password and password:
            initial_defenders = st.text_area("Enter Eligible Defenders (one per line)")
            if st.button("Confirm Eligible Defenders"):
                defenders = [name.strip() for name in initial_defenders.splitlines() if name.strip()]
                users[username] = {"password": password, "defenders": defenders}
                save_users(users)
                st.success("✅ Account created successfully. You are now logged in.")
                st.write("🛡️ Your Eligible Defenders")
                st.write(defenders)
        elif password != confirm_password:
            st.sidebar.warning("Passwords do not match.")
        else:
            st.sidebar.warning("Please confirm your password.")
else:
    st.info("Please enter your username and password to continue.")
