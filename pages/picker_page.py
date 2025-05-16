import streamlit as st
import random
from datetime import datetime, timedelta
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

DAYS_LIMIT = 7

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

def picker_page():
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
