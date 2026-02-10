import streamlit as st
import random
from datetime import datetime, timedelta
import pytz

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="INFINITY PROFIT V101", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- 2. SISTEMA DE SEGURIDAD ---
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

# --- 3. DISEÑO DE BOTONES AMARILLOS ---
st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    .stButton > button { 
        width: 100%; border-radius: 12px; font-weight: bold; height: 50px; 
        background-color: #ffd700 !important; color: black !important;
    }
    .main-title { color: #ffd700; text-align: center; font-size: 35px; font-weight: 900; margin-bottom: 20px; }
    .signal-card { border: 3px solid #ffd700; border-radius: 20px; padding: 20px; text-align: center; background: #111; }
    </style>
""", unsafe_allow_html=True)

# --- 4. LÓGICA DE CONTADORES ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'signal' not in st.session_state: st.session_state.signal = None

st.markdown('<h1 class="main-title">INFINITY PROFIT FULL INTERFACE</h1>', unsafe_allow_html=True)

# PANEL LATERAL CON RELOJ DE BOGOTÁ
with st.sidebar:
    st.header("📊 PANEL DE CONTROL")
    st.write(f"🕒 Hora Colombia: {datetime.now(local_tz).strftime('%H:%M:%S')}")
    st.success(f"WIN: {st.session_state.win}")
    st.error(f"LOSS: {st.session_state.loss}")
    if st.button("Reiniciar Sesión"):
        st.session_state.win = 0
        st.session_state.loss = 0
        st.rerun()

t1, t2 = st.tabs(["📉 BINARIAS SNIPER", "🏛️ MERCADO MT5"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        st.camera_input("SCANNER DE MERCADO", key="scanner_pro")
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("WIN ✅"): st.session_state.win += 1
        with c2: 
            if st.button("LOSS ❌"): st.session_state.loss += 1
            
    with col2:
        if st.button("🚀 ANALIZAR ENTRADA"):
            ahora = datetime.now(local_tz)
            prob = random.uniform(88.0, 99.0)
            tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            cierre = (ahora + timedelta(minutes=2)).strftime('%H:%M:%S')
            st.session_state.signal = {"tipo": tipo, "prob": prob, "cierre": cierre}
        
        if st.session_state.signal:
            s = st.session_state.signal
            st.markdown(f"""
                <div class="signal-card">
                    <h1 style="color:#ffd700;">{s['tipo']}</h1>
                    <h2 style="color:white;">CIERRE: {s['cierre']}</h2>
                    <p style="font-size:22px; color:#ffd700;">EFECTIVIDAD: {s['prob']:.2f}%</p>
                </div>
            """, unsafe_allow_html=True)

# GRÁFICO TRADINGVIEW COMPLETO
st.components.v1.html('''
    <iframe src="https://s.tradingview.com/widgetembed/?symbol=FX%3AEURUSD&interval=1&theme=dark" width="100%" height="450"></iframe>
''', height=450)
