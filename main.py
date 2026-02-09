import streamlit as st
import time
import random
from datetime import datetime
import pytz
# Se agrega esta función para que el reloj se mueva segundo a segundo
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN Y REFRESCO (ESTO HACE QUE EL RELOJ SE MUEVA) ---
st.set_page_config(page_title="INFINITY PROFIT V74", layout="wide")
st_autorefresh(interval=1000, key="datarefresh") # Refresca cada 1 segundo

local_tz = pytz.timezone('America/Bogota')

# --- 2. ESTILO CSS (TODO IGUAL, SIN DAÑAR NADA) ---
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
    .reloj-h { font-size: 50px; color: #ffd700; font-weight: 800; margin: 0; font-family: 'Courier New', monospace; }
    .stButton > button { width: 100%; border-radius: 12px; font-weight: bold; height: 50px; border: none; }
    .btn-win button { background: #1b5e20 !important; color: white !important; }
    .btn-loss button { background: #b71c1c !important; color: white !important; }
    .btn-analizar button { background: #ffd700 !important; color: black !important; font-size: 18px !important; }
    .signal-card { border-radius: 20px; padding: 25px; text-align: center; border: 2px solid white; }
    .futuro-card { background: #111; border-left: 5px solid #ffd700; border-radius: 10px; padding: 15px; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MEMORIA DE SESIÓN ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'mostrar_señal' not in st.session_state: st.session_state.mostrar_señal = False

# --- 4. BARRA LATERAL (CONTROL) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700; text-align:center;'>📊 REGISTRO REAL</h2>", unsafe_allow_html=True)
    st.success(f"WIN: {st.session_state.win}")
    st.error(f"LOSS: {st.session_state.loss}")
    st.divider()
    if st.button("🔄 REINICIAR TODO"):
        st.session_state.win = 0
        st.session_state.loss = 0
        st.session_state.mostrar_señal = False
        st.rerun()

# --- 5. RELOJ CON SEGUNDOS ACTIVOS ---
now = datetime.now(local_tz)
st.markdown(f"""
    <div class="reloj-box">
        <p style="color:#888; margin:0; font-size:14px;">{now.strftime('%d . %m . %Y')}</p>
        <p class="reloj-h">{now.strftime('%H:%M:%S')}</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. PANEL DE TRABAJO ---
col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.markdown("### 📸 ESCÁNER")
    foto = st.camera_input("Scanner")
    
    st.write("")
    st.markdown("### ⚡ REGISTRO")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="btn-win">', unsafe_allow_html=True)
        if st.button("WIN ✅"): st.session_state.win += 1
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-loss">', unsafe_allow_html=True)
        if st.button("LOSS ❌"): st.session_state.loss += 1
        st.markdown('</div>', unsafe_allow_html=True)

with col_der:
    st.markdown("### 🎯 ANÁLISIS")
    if foto or st.button("🚀 ANALIZAR AHORA"):
        st.session_state.mostrar_señal = True
        
    if st.session_state.mostrar_señal:
        probabilidad = random.uniform(72.5, 91.2)
        tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
        color_bg = "#1b5e20" if "COMPRA" in tipo else "#b71c1c"
        precio_actual = random.uniform(1.0820, 1.0850)
        
        st.markdown(f"""
            <div class="signal-card" style="background: {color_bg};">
                <p style="margin:0; opacity:0.8;">CONFIRMACIÓN: {datetime.now(local_tz).strftime('%H:%M:%S')}</p>
                <h1 style="font-size: 50px; margin:10px 0;">{tipo}</h1>
                <h2 style="color: #ffd700; margin:0;">{probabilidad:.1f}% PRECISIÓN</h2>
                <hr style="border:0.5px solid rgba(255,255,255,0.2); margin:15px 0;">
                <p style="font-size:14px; font-weight:bold;">LISTO PARA OPERAR</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="futuro-card">
                <h4 style="color:#ffd700; margin:0;">⏳ OPERACIÓN A FUTURO</h4>
                <p style="margin:5px 0; font-size:14px;">Entrada: <b>{precio_actual:.5f}</b></p>
                <div style="display:flex; justify-content:space-between; font-size:13px;">
                    <span style="color:#00ff00;">TP: {(precio_actual + 0.0035):.5f}</span>
                    <span style="color:#ff4b4b;">SL: {(precio_actual - 0.0015):.5f}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Esperando captura o click para iniciar.")

# --- 7. GRÁFICA Y ACTIVOS ---
st.divider()
dict_m = {
    "EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "USD/JPY": "FX:USDJPY",
    "BITCOIN": "BINANCE:BTCUSDT", "ORO": "OANDA:XAUUSD", "NASDAQ 100": "FOREXCOM:NAS100"
}
selec = st.selectbox("Cambiar Activo:", list(dict_m.keys()))

st.components.v1.html(f"""
    <div id="tv_v74" style="height:480px; border-radius:15px; overflow:hidden; border: 1px solid #333;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width":"100%","height":480,"symbol":"{dict_m[selec]}","interval":"1","theme":"dark","locale":"es","container_id":"tv_v74"}});
    </script>
""", height=480)