import streamlit as st

translations = {
    "English": {
        "profile": "👤 Profile",
        "eligible_defenders": "🛡️ Eligible Defenders",
        "random_picker": "🎲 Random Picker",
        "logout": "🚪 Log Out",
        "connected": "🔗 Supabase: Connected",
        "disconnected": "🔗 Supabase: Disconnected",
        "language": "🌐 Language",
        "picker_title": "Random Picker",
        "submit_button": "Pick",
        "results_label": "Winner:"
    },
    "Spanish": {
        "profile": "👤 Perfil",
        "eligible_defenders": "🛡️ Defensores Elegibles",
        "random_picker": "🎲 Selector Aleatorio",
        "logout": "🚪 Cerrar Sesión",
        "connected": "🔗 Supabase: Conectado",
        "disconnected": "🔗 Supabase: Desconectado",
        "language": "🌐 Idioma",
        "picker_title": "Selector Aleatorio",
        "submit_button": "Elegir",
        "results_label": "Ganador:"
    },
    "Portuguese": {
        "profile": "👤 Perfil",
        "eligible_defenders": "🛡️ Defensores Elegíveis",
        "random_picker": "🎲 Seletor Aleatório",
        "logout": "🚪 Sair",
        "connected": "🔗 Supabase: Conectado",
        "disconnected": "🔗 Supabase: Desconectado",
        "language": "🌐 Idioma",
        "picker_title": "Seletor Aleatório",
        "submit_button": "Escolher",
        "results_label": "Vencedor:"
    },
    "Korean": {
        "profile": "👤 프로필",
        "eligible_defenders": "🛡️ 선택된 수비수",
        "random_picker": "🎲 무작위 선택기",
        "logout": "🚪 로그아웃",
        "connected": "🔗 Supabase: 연결됨",
        "disconnected": "🔗 Supabase: 연결되지 않음",
        "language": "🌐 언어",
        "picker_title": "무작위 선택기",
        "submit_button": "선택",
        "results_label": "승자:"
    },
    "Indonesian": {
        "profile": "👤 Profil",
        "eligible_defenders": "🛡️ Pembela yang Memenuhi Syarat",
        "random_picker": "🎲 Pemilih Acak",
        "logout": "🚪 Keluar",
        "connected": "🔗 Supabase: Terhubung",
        "disconnected": "🔗 Supabase: Tidak Terhubung",
        "language": "🌐 Bahasa",
        "picker_title": "Pemilih Acak",
        "submit_button": "Pilih",
        "results_label": "Pemenang:"
    }
}

def t(key):
    lang = st.session_state.get("language", "English")
    return translations.get(lang, translations["English"]).get(key, key)

