import streamlit as st
import pandas as pd
import random
import json
import os

st.set_page_config(page_title="Train Conductor & Defender Selector", layout="wide")
st.title("🚂 Train Conductor & Defender Selector")

# --- File to store user data ---
USER_DB = "users.json"

# --- Load user database ---
def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

# --- Save user database ---
def save_users(data):
    with open(USER_DB, "w") as f:
        json.dump(data, f, indent=2)

# --- Authenticate user ---
users = load_users()

st.sidebar.header("🔐 User Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username and password:
    if username in users:
        if users[username]["password"] == password:
            st.sidebar.success("✅ Logged in as " + username)
            defenders = users[username]["defenders"]

            if st.sidebar.button("Update Eligible Defenders"):
                new_defenders = st.text_area("Update Eligible Defenders (one per line)", value="\n".join(defenders))
                if new_defenders:
                    users[username]["defenders"] = [name.strip() for name in new_defenders.splitlines() if name.strip()]
                    save_users(users)
                    st.success("✅ Defender list updated!")
                    defenders = users[username]["defenders"]
        else:
            st.sidebar.error("❌ Incorrect password")
            st.stop()
    else:
        st.sidebar.info("🆕 New user detected")
        if st.sidebar.button("Create Account"):
            initial_defenders = st.text_area("Enter Eligible Defenders (one per line)")
            if initial_defenders:
                defenders = [name.strip() for name in initial_defenders.splitlines() if name.strip()]
                users[username] = {"password": password, "defenders": defenders}
                save_users(users)
                st.success("✅ Account created! You are now logged in.")
            else:
                st.warning("Please enter at least one defender.")
                st.stop()

    # --- Daily Conductor/VIP Input ---
    st.subheader("✍️ Manually Enter Names")
    vs_input = st.text_area("Enter Top 10 VS Names (one per line)")
    tech_input = st.text_area("Enter Top 10 Tech Names (one per line)")

    vs_names = [name.strip() for name in vs_input.splitlines() if name.strip()]
    tech_names = [name.strip() for name in tech_input.splitlines() if name.strip()]
    eligible_conductors = list(set(vs_names) | set(tech_names))
    eligible_defenders = [name for name in defenders if name in eligible_conductors]

    # --- Display Pools ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎖️ Eligible Conductors/VIPs")
        st.write(eligible_conductors)
    with col2:
        st.subheader("🛡️ Eligible Defenders")
        st.write(eligible_defenders)

    # --- Selection Tools ---
    st.divider()
    st.subheader("🎲 Random Selection")

    if st.button("Pick Random Conductor/VIP"):
        if eligible_conductors:
            winner = random.choice(eligible_conductors)
            st.success(f"🎖️ Selected Conductor/VIP: **{winner}**")
        else:
            st.warning("No eligible conductors found.")

    if st.button("Pick Random Defender"):
        if eligible_defenders:
            defender = random.choice(eligible_defenders)
            st.success(f"🛡️ Selected Defender: **{defender}**")
        else:
            st.warning("No eligible defenders found.")

else:
    st.info("Please log in or create a new account to continue.")
