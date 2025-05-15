import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="Train Conductor & Defender Selector", layout="wide")
st.title("🚂 Train Conductor & Defender Selector")

USER_DB = "users.json"
SELECTION_LOG = "selection_log.json"

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

users = load_json(USER_DB)
logs = load_json(SELECTION_LOG)

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
                    save_json(USER_DB, users)
                    st.success("✅ Defender list updated!")
                    defenders = users[username]["defenders"]
        else:
            st.sidebar.error("❌ Incorrect password")
            st.stop()
    else:
        st.sidebar.info("🆕 New user detected")
        if st.sidebar.button("Create Account"):
            initial_defenders = st.text_area("Enter Eligible Defenders (one per line)")
            if initial_defenders and st.button("Confirm Eligible Defenders"):
                defenders = [name.strip() for name in initial_defenders.splitlines() if name.strip()]
                users[username] = {"password": password, "defenders": defenders}
                save_json(USER_DB, users)
                st.success("✅ Account created! You are now logged in.")
            else:
                st.warning("Please enter and confirm at least one defender.")
                st.stop()

    # Load user history and apply 7-day restriction
    today = datetime.today().date()
    user_log = logs.get(username, [])
    recent_picks = [entry for entry in user_log if datetime.strptime(entry["date"], "%Y-%m-%d").date() >= today - timedelta(days=7)]
    recent_names = set(entry["conductor"] for entry in recent_picks) | set(entry["defender"] for entry in recent_picks)

    # Daily input for conductor pool
    st.subheader("✍️ Manually Enter Names")
    vs_input = st.text_area("Enter Top 10 VS Names (one per line)")
    tech_input = st.text_area("Enter Top 10 Tech Names (one per line)")

    vs_names = [name.strip() for name in vs_input.splitlines() if name.strip()]
    tech_names = [name.strip() for name in tech_input.splitlines() if name.strip()]
    eligible_conductors = list(set(vs_names) | set(tech_names))

    # Filter out recent picks
    filtered_conductors = [name for name in eligible_conductors if name not in recent_names]
    filtered_defenders = [name for name in defenders if name in filtered_conductors and name not in recent_names]

    # Display Pools
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎖️ Eligible Conductors/VIPs")
        st.write(filtered_conductors)
    with col2:
        st.subheader("🛡️ Eligible Defenders")
        st.write(filtered_defenders)

    # Random Selection + Logging
    st.divider()
    st.subheader("🎲 Random Selection")

    if st.button("Pick Random Conductor/VIP"):
        if filtered_conductors:
            winner = random.choice(filtered_conductors)
            st.success(f"🎖️ Selected Conductor/VIP: **{winner}**")
            logs.setdefault(username, []).append({"date": str(today), "conductor": winner, "defender": None})
            save_json(SELECTION_LOG, logs)
        else:
            st.warning("No eligible conductors available (all selected recently).")

    if st.button("Pick Random Defender"):
        if filtered_defenders:
            defender = random.choice(filtered_defenders)
            st.success(f"🛡️ Selected Defender: **{defender}**")
            logs.setdefault(username, []).append({"date": str(today), "conductor": None, "defender": defender})
            save_json(SELECTION_LOG, logs)
        else:
            st.warning("No eligible defenders available (all selected recently).")

    # Display user log
    st.divider()
    st.subheader("📜 Selection History (Past 7 Days)")
    if recent_picks:
        st.write(pd.DataFrame(recent_picks))
    else:
        st.info("No picks made in the last 7 days.")

else:
    st.info("Please log in or create a new account to continue.")
