import streamlit as st
import random
from datetime import datetime, timedelta
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import bcrypt

# ─── ENV & CLIENT SETUP ───
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── PAGE CONFIG ───
st.set_page_config(
    page_title="Last War Train Picker",
    page_icon="⚔️",
    layout="centered"
)

# ─── STYLES ───
st.markdown("""
<style>
  .css-18e3th9, .main > div { margin: 0 auto !important; max-width:100% !important; padding:0 1rem; }
  body { display:flex; justify-content:center; align-items:center; height:100vh; background:#121212; margin:0; }
  .card { width:100%; max-width:360px; background:#1e1e1e; padding:2rem; border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,0.3); }
  .card h1 { text-align:center; color:#fff; margin-bottom:1.5rem; font-size:1.75rem; }
  .stTextInput>label, .stForm label { color:#ccc; }
  .stTextInput, .stCheckbox, .stButton>button { width:100% !important; }
  .back-button { margin-top:1rem; background:none !important; border:none !important; color:#88f !important; text-decoration:underline; width:auto !important; }
  .hamburger {
      position: fixed;
      top: 1rem;
      left: 1rem;
      cursor: pointer;
      z-index: 1001;
      background: none;
      border: none;
      padding: 0;
  }
  .hamburger div {
      width: 30px;
      height: 4px;
      background-color: white;
      margin: 6px 0;
  }
  .menu {
      background-color: #1e1e1e;
      position: fixed;
      top: 0;
      left: 0;
      width: 250px;
      height: 100%;
      padding: 2rem 1rem;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      box-shadow: 2px 0 10px rgba(0,0,0,0.5);
  }

  /* ─── Force-disable Streamlit default sidebar ─── */
  [data-testid="stSidebar"], 
  [data-testid="stSidebarNav"],
  [data-testid="stSidebarContent"],
  .css-1d391kg,
  .css-hxt7ib,
  header[data-testid="stHeader"] {
      display: none !important;
      visibility: hidden !important;
      width: 0 !important;
      max-width: 0 !important;
      min-width: 0 !important;
  }

  .block-container {
      padding-left: 1rem !important;
      padding-right: 1rem !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ───
DAYS_LIMIT = 7

# ... (rest of the code continues unchanged)
