import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import bcrypt

# ─── Load environment variables ────────────────────────────────────────────────
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ─── Initialize Supabase client ───────────────────────────────────────────────
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── Streamlit page config ────────────────────────────────────────────────────
st.set_page_config(page_title="Sign Up", layout="centered")
st.title("🆕 Create a New User Account")

# ─── Supabase Health Check ─────────────────────────────────────────────────────
try:
    resp = supabase.table("users").select("id,username").limit(1).execute()
    if resp.status_code != 200:
        st.sidebar.error(f"❌ Supabase error: {resp.data}")
    else:
        st.sidebar.markdown("**🔗 Supabase Status:** ✅ Connected")
        st.sidebar.write("Sample response:", resp.data)
except Exception as e:
    st.sidebar.error(f"❌ Connection failed:\n{e}")

# ─── Sign-up form ───────────────────────────────────────────────────────────────
with st.form("signup_form"):
    username   = st.text_input("Username")
    password   = st.text_input("Password", type="password")
    confirm    = st.text_input("Confirm Password", type="password")
    server     = st.text_input("Server Number")
    alliance   = st.text_input("Alliance Name")
    unlocked   = st.checkbox("Our alliance has unlocked the VIP slot on the train")
    submit_btn = st.form_submit_button("Create Account")

    if submit_btn:
        # Basic validation
        if not username.strip():
            st.error("Please enter a username.")
        elif password != confirm or not password:
            st.error("Passwords must match and not be empty.")
        elif not server.strip() or not alliance.strip():
            st.error("Server Number and Alliance Name are required.")
        else:
            # Hash the password
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            # Insert into Supabase
            new_user = {
                "username":      username.strip(),
                "password_hash": pw_hash,
                "server":        server.strip(),
                "alliance":      alliance.strip(),
                "unlocked":      unlocked
            }
            insert = supabase.table("users").insert(new_user).execute()

            if insert.status_code != 201:
                st.error(f"Failed to create account: {insert.data}")
            else:
                st.success("✅ Account created successfully!")
                st.info("You can now log in with your credentials.")
