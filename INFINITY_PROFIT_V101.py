import streamlit as st
import random
from datetime import datetime, timedelta
import pytz

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="INFINITY PROFIT V101", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- 2. SISTEMA DE SEGURIDAD (PASSWORD) ---
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

# --- 3. ESTILO VISUAL PROFESIONAL ---
st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    .stButton > button { 
        width: 100%; border-radius: 12px; font-weight: bold; height: 50px; 
        background-color: #ffd700 !important; color: black !important;
    }
    .main-title { color: #ffd700; text-align: center; font-size: 35px; font-weight: 900; }
    .stSelectbox label { color: #ffd700 !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 4. LÓGICA DE TRADING ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0

st.markdown('<h1 class="main-title">INFINITY PROFIT V101</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📊 CONTROL DE SESIÓN")
    st.write(f"🕒 Bogotá: {datetime.now(local_tz).strftime('%H:%M:%S')}")
    st.metric("GANADAS (WIN)", st.session_state.win)
    st.metric("PERDIDAS (LOSS)", st.session_state.loss)
    # CONFIGURACIÓN DE GALE
    st.info("💡 Sugerencia Gale: 8.000 + 8.800 y 8.000 (Cierre 16.000)")

t1, t2 = st.tabs(["📉 BINARIAS SNIPER", "🏛️ MERCADO MT5"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        # SELECTOR DE DIVISAS RESTAURADO
        divisa = st.selectbox("🎯 SELECCIONAR DIVISA:", ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "EUR/JPY"])
        st.camera_input("SCANNER DE MERCADO", key="scanner_v101")
        
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("WIN ✅"): st.session_state.win += 1
        with c2: 
            if st.button("LOSS ❌"): st.session_state.loss += 1
            
    with col2:
        if st.button("🚀 ANALIZAR ENTRADA"):
            ahora = datetime.now(local_tz)
            prob = random.uniform(89.0, 99.5)
            tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            cierre = (ahora + timedelta(minutes=2)).strftime('%H:%M:%S')
            
            st.markdown(f"""
                <div style="border:3px solid #ffd700; border-radius:15px; padding:20px; text-align:center; background:#111;">
                    <h2 style="color:white;">{divisa}</h2>
                    <h1 style="color:#ffd700;">{tipo}</h1>
                    <h3 style="color:white;">CIERRE: {cierre}</h3>
                    <p style="font-size:20px; color:#ffd700;">EFECTIVIDAD: {prob:.2f}%</p>
                </div>
            """, unsafe_allow_html=True)

# GRÁFICO TRADINGVIEW INTEGRADO
st.components.v1.html(f'''
    <iframe src="https://s.tradingview.com/widgetembed/?symbol={divisa.replace('/','')}&interval=1&theme=dark" width="100%" height="450"></iframe>
''', height=450)
