import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
      .css-18e3th9, .main > div {
          margin: 0 auto !important;
          max-width:100% !important;
          padding:0 1rem;
      }
      body {
          display:flex;
          justify-content:center;
          align-items:center;
          height:100vh;
          background:#121212;
          margin:0;
      }
      .card {
          width:100%;
          max-width:360px;
          background:#1e1e1e;
          padding:2rem;
          border-radius:16px;
          box-shadow:0 8px 24px rgba(0,0,0,0.3);
      }
      .card h1 {
          text-align:center;
          color:#fff;
          margin-bottom:1.5rem;
          font-size:1.75rem;
      }
      .stTextInput>label, .stForm label {
          color:#ccc;
      }
      .stTextInput, .stCheckbox, .stButton>button {
          width:100% !important;
      }
      .back-button {
          margin-top:1rem;
          background:none !important;
          border:none !important;
          color:#88f !important;
          text-decoration:underline;
          width:auto !important;
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
    </style>
    """, unsafe_allow_html=True)
