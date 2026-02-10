import streamlit as st
import random
from datetime import datetime
import pytz

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="INFINITY PROFIT V101", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- 2. SISTEMA DE CLAVE (TAL CUAL PIDIÓ) ---
PASSWORD_MAESTRA = "INFINITY2026" 

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='color:#ffd700; text-align:center;'>🔐 ACCESO EXCLUSIVO</h1>", unsafe_allow_html=True)
    clave = st.text_input("Licencia Mensual:", type="password")
    if st.button("🚀 ACTIVAR"):
        if clave == PASSWORD_MAESTRA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ Clave incorrecta.")
    st.stop()

# --- 3. INTERFAZ ORIGINAL (BOTONES AMARILLOS) ---
st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    .stButton > button { 
        width: 100%; border-radius: 12px; font-weight: bold; height: 50px; 
        background-color: #ffd700 !important; color: black !important;
    }
    .main-title { color: #ffd700; text-align: center; font-size: 35px; font-weight: 900; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">INFINITY PROFIT V101</h1>', unsafe_allow_html=True)

t1, t2 = st.tabs(["📉 BINARIAS", "🏛️ MT5"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        st.camera_input("SCANNER", key="cam_v1")
        
    with col2:
        if st.button("🚀 ANALIZAR ENTRADA"):
            prob = random.uniform(85.5, 98.0)
            tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            st.markdown(f"""
                <div style="border:3px solid #ffd700; border-radius:15px; padding:20px; text-align:center;">
                    <h1 style="color:#ffd700;">{tipo}</h1>
                    <p style="font-size:25px;">EFECTIVIDAD: {prob:.2f}%</p>
                </div>
            """, unsafe_allow_html=True)

st.components.v1.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=FX%3AEURUSD&interval=1&theme=dark" width="100%" height="400"></iframe>', height=400)
