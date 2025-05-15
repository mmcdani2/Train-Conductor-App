import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Train Conductor & Defender Selector", layout="wide")
st.title("🚂 Train Conductor & Defender Selector")

# --- Google Sheet CSV Export Links ---
vs_csv_url = "https://docs.google.com/spreadsheets/d/1B2ctEGRJLHyIb-yvtr3TreGylwZabpEOjCyqrlefpSQ/export?format=csv&gid=0"  # Top 10 VS
tech_csv_url = "https://docs.google.com/spreadsheets/d/1B2ctEGRJLHyIb-yvtr3TreGylwZabpEOjCyqrlefpSQ/export?format=csv&gid=600054968"  # Top 10 Tech
defender_csv_url = "https://docs.google.com/spreadsheets/d/1B2ctEGRJLHyIb-yvtr3TreGylwZabpEOjCyqrlefpSQ/export?format=csv&gid=1824324559"  # Eligible Defenders

# --- Load Data ---
@st.cache_data
def load_csv(url):
    return pd.read_csv(url)

try:
    vs_df = load_csv(vs_csv_url)
    tech_df = load_csv(tech_csv_url)
    defender_df = load_csv(defender_csv_url)
    
    st.success("✅ All Google Sheets loaded successfully!")

    # --- Clean names ---
    vs_names = vs_df["Name"].astype(str).str.strip()
    tech_names = tech_df["Name"].astype(str).str.strip()
    defender_names = defender_df["Name"].astype(str).str.strip()

    # --- Build eligible pools ---
    eligible_conductors = pd.Series(list(set(vs_names) | set(tech_names))).dropna().unique()
    eligible_defenders = defender_names.dropna().unique()

    # --- Display Pools ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎖️ Eligible Conductors/VIPs")
        st.write(eligible_conductors.tolist())
    with col2:
        st.subheader("🛡️ Eligible Defenders")
        st.write(eligible_defenders.tolist())

    # --- Selection Tools ---
    st.divider()
    st.subheader("🎲 Random Selection")

    if st.button("Pick Random Conductor/VIP"):
        if len(eligible_conductors) > 0:
            winner = random.choice(eligible_conductors.tolist())
            st.success(f"🎖️ Selected Conductor/VIP: **{winner}**")
        else:
            st.warning("No eligible conductors found.")

    if st.button("Pick Random Defender"):
        if len(eligible_defenders) > 0:
            defender = random.choice(eligible_defenders.tolist())
            st.success(f"🛡️ Selected Defender: **{defender}**")
        else:
            st.warning("No eligible defenders found.")

except Exception as e:
    st.error("❌ Failed to load one or more Google Sheets. Check your links and permissions.")
    st.code(str(e))
