import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def defenders_page():
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

