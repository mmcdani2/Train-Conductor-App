import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def profile_page():
    user = st.session_state.user
    st.title(f"Welcome, {user['username']}!")
    st.markdown(f"**Server:** {user['server']}")
    st.markdown(f"**Alliance:** {user['alliance']}")
    st.markdown(f"**VIP Unlocked:** {'Yes' if user['unlocked'] else 'No'}")

    vip_toggle = st.checkbox("VIP slot unlocked?", value=user["unlocked"])
    if vip_toggle != user["unlocked"]:
        supabase.table("users").update({"unlocked": vip_toggle}).eq("id", user["id"]).execute()
        st.session_state.user["unlocked"] = vip_toggle
        st.success("VIP setting updated. Please refresh or navigate to see changes.")

    how_to_text = """
### 📖 How to Use This App

**Navigation Menu**
- Click the > icon in the top-left to open the menu
- Navigate to: **Profile**, **Eligible Defenders** (if VIP is unlocked), **Random Picker**, or **Log Out**

**Random Picker**
- Paste up to 20 names (one per line) it is common to use top 10 VS daily scores and top 10 weekly tech donators
- The app selects 1 contestant and 1 eligible defender (if VIP is unlocked), otherwise it only selects 1 contestant
- Prevents people from being picked if they were chosen in the last 7 days

**Eligible Defenders**
- Add or remove powerful defenders associated with your alliance
- Recommend only choosing members that are the top 20% power level in your alliance
- Only visible if your account has train VIP slot unlocked

**Log Out**
- Ends your session

💡 Tip: Refresh the app if you encounter a UI issue or stuck state.
"""

    try:
        with st.expander("📖 How to Use This App", expanded=False):
            st.markdown(how_to_text)
    except Exception as e:
        st.error(f"Help section failed: {e}")
