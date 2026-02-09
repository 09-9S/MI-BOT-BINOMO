import streamlit as st
import time
import random
from datetime import datetime
import pytz

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INFINITY PROFIT V72", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- 2. ESTILO VISUAL (ORGANIZACIÓN IMPECABLE) ---
st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    .reloj-box {
        background: linear-gradient(180deg, #111, #000);
        border: 2px solid #ffd700;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        margin-bottom: 25px;
    }
    .reloj-h { font-size: 45px; color: #ffd700; font-weight: 800; margin: 0; }
    .stButton > button { width: 100%; border-radius: 12px; font-weight: bold; height: 50px; border: none; }
    .btn-win button { background: #1b5e20 !important; color: white !important; }
    .btn-loss button { background: #b71c1c !important; color: white !important; }
    .btn-analizar button { background: #ffd700 !important; color: black !important; font-size: 18px !important; }
    .signal-card { border-radius: 20px; padding: 25px; text-align: center; border: 2px solid white; }
    .futuro-card { background: #1a1a1a; border-left: 5px solid #ffd700; border-radius: 10px; padding: 15px; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MEMORIA DE SESIÓN ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'mostrar_señal' not in st.session_state: st.session_state.mostrar_señal = False

# --- 4. BARRA LATERAL (REGISTRO Y REINICIO) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700; text-align:center;'>📊 SESIÓN REAL</h2>", unsafe_allow_html=True)