import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Train Conductor & Defender Selector", layout="wide")
st.title("🚂 Train Conductor & Defender Selector")

# --- Manual Entry Interface ---
st.subheader("✍️ Manually Enter Names")

vs_input = st.text_area("Enter Top 10 VS Names (one per line)")
tech_input = st.text_area("Enter Top 10 Tech Names (one per line)")
defender_input = st.text_area("Enter Eligible Defenders (one per line)")

# --- Parse Inputs ---
vs_names = [name.strip() for name in vs_input.splitlines() if name.strip()]
tech_names = [name.strip() for name in tech_input.splitlines() if name.strip()]
defender_names = [name.strip() for name in defender_input.splitlines() if name.strip()]

# --- Build eligible pools ---
eligible_conductors = list(set(vs_names) | set(tech_names))
eligible_defenders = list(set(defender_names))

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
