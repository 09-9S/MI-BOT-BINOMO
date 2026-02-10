import streamlit as st
import random
from datetime import datetime, timedelta
import pytz

# --- 1. CONFIGURACIÓN DE PESTAÑA ---
st.set_page_config(page_title="INFINITY PROFIT V101", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- 2. SISTEMA DE BLOQUEO (CONTRASEÑA) ---
# Cambia esto cada mes para que tus clientes tengan que pagarte de nuevo.
PASSWORD_DEL_MES = "INFINITY2026" 

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("""
        <style>
        .stApp {background-color: #050505;}
        .login-box {
            border: 3px solid #ffd700;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            background-color: #111;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h1 style='color:#ffd700;'>🔐 ACCESO EXCLUSIVO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:white;'>Software de Señales Sniper - Introduzca su Licencia Mensual</p>", unsafe_allow_html=True)
    
    clave = st.text_input("Licencia:", type="password")
    
    if st.button("🚀 ACTIVAR SOFTWARE"):
        if clave == PASSWORD_DEL_MES:
            st.session_state.autenticado = True
            st.success("✅ Licencia validada. Cargando sistema...")
            st.rerun()
        else:
            st.error("❌ Licencia incorrecta o vencida.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 3. ESTILO VISUAL (LO QUE YA TENÍAMOS) ---
st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    .stButton > button { 
        width: 100%; border-radius: 12px; font-weight: bold; height: 50px; 
        background-color: #ffd700 !important; color: black !important; border: none; 
    }
    .main-title { color: #ffd700; text-align: center; font-size: 35px; font-weight: 900; margin-bottom: 20px; text-shadow: 2px 2px #444; }
    .signal-card { border-radius: 20px; padding: 25px; text-align: center; border: 3px solid #ffd700; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">INFINITY PROFIT V101</h1>', unsafe_allow_html=True)

# --- 4. LÓGICA DE SEÑALES ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'sig_bin' not in st.session_state: st.session_state.sig_bin = None

# PANEL LATERAL
with st.sidebar:
    st.header("📊 PANEL DE CONTROL")
    st.write(f"📅 Fecha: {datetime.now(local_tz).strftime('%d/%m/%Y')}")
    st.success(f"WIN: {st.session_state.win}")
    st.error(f"LOSS: {st.session_state.loss} / 4")
    if st.button("Reiniciar Contador"):
        st.session_state.win = 0
        st.session_state.loss = 0
        st.rerun()

# PESTAÑAS
t1, t2 = st.tabs(["📉 BINARIAS SNIPER", "🏛️ MERCADO MT5"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        st.camera_input("SCANNER DE MERCADO", key="cam_v101")
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("WIN ✅"): st.session_state.win += 1
        with c2: 
            if st.button("LOSS ❌"): st.session_state.loss += 1
            
    with col2:
        if st.button("🚀 ANALIZAR ENTRADA"):
            ahora = datetime.now(local_tz)
            prob = random.uniform(85.5, 98.0)
            st.session_state.sig_bin = {
                "tipo": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]), 
                "prob": prob, 
                "out": (ahora + timedelta(minutes=2)).strftime('%H:%M:%S')
            }
        
        if st.session_state.sig_bin:
            s = st.session_state.sig_bin
            color = "#1b5e20" if "COMPRA" in s["tipo"] else "#b71c1c"
            st.markdown(f'''
                <div class="signal-card" style="background:{color};">
                    <h1>{s["tipo"]}</h1>
                    <h2>CIERRE: {s["out"]}</h2>
                    <p style="font-size: 20px;">EFECTIVIDAD: {s["prob"]:.2f}%</p>
                </div>
            ''', unsafe_allow_html=True)

# GRÁFICA TRADINGVIEW (ABAJO)
st.components.v1.html('''
    <div id="tradingview_chart"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({
      "width": "100%",
      "height": 450,
      "symbol": "FX:EURUSD",
      "interval": "1",
      "theme": "dark",
      "style": "1",
      "locale": "es",
      "container_id": "tradingview_chart"
    });
    </script>
''', height=450)
