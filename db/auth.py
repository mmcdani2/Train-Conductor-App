import bcrypt
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def health_check():
    try:
        supabase.table("users").select("id").limit(1).execute()
        return True
    except:
        return False

def signup(user, pwd, server, alliance, unlocked):
    pw_hash = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
    payload = {
        "username": user,
        "password_hash": pw_hash,
        "server": server,
        "alliance": alliance,
        "unlocked": unlocked,
        "defenders": []
    }
    supabase.table("users").insert(payload).execute()

def login(user, pwd):
    resp = supabase.table("users").select("*").eq("username", user).limit(1).execute()
    if resp.data and bcrypt.checkpw(pwd.encode(), resp.data[0]["password_hash"].encode()):
        return resp.data[0]
    return None

