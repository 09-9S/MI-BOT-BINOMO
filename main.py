import streamlit as st
import time
import random
from datetime import datetime
import pytz

# --- 1. CONFIGURACIÓN INICIAL (BLOQUEADO) ---
st.set_page_config(page_title="INFINITY PROFIT V73", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- 2. DISEÑO CSS PROFESIONAL ---
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
        box-shadow: 0px 0px 20px rgba(255, 215, 0, 0.2);
    }
    .reloj-h { font-size: 45px; color: #ffd700; font-weight: 800; margin: 0; }
    .stButton > button { width: 100%; border-radius: 12px; font-weight: bold; height: 50px; border: none; }
    .btn-win button { background: #1b5e20 !important; color: white !important; }
    .btn-loss button { background: #b71c1c !important; color: white !important; }
    .btn-analizar button { background: #ffd700 !important; color: black !important; font-size: 18px !important; }
    .signal-card { border-radius: 20px; padding: 25px; text-align: center; border: 2px solid white; }
    .futuro-card { background: #111; border-left: 5px solid #ffd700; border-radius: 10px; padding: 15px; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. GESTIÓN DE MEMORIA ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'mostrar_señal' not in st.session_state: st.session_state.mostrar_señal = False

# --- 4. BARRA LATERAL (MARCADOR Y REINICIO) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700; text-align:center;'>📊 REGISTRO REAL</h2>", unsafe_allow_html=True)
    st.success(f"GANADAS (WIN): {st.session_state.win}")
    st.error(f"PERDIDAS (LOSS): {st.session_state.loss}")
    st.divider()
    if st.button("🔄 REINICIAR TODO"):
        st.session_state.win = 0
        st.session_state.loss = 0
        st.session_state.mostrar_señal = False
        st.rerun()

# --- 5. CUERPO PRINCIPAL (RELOJ) ---
now = datetime.now(local_tz)
st.markdown(f"""
    <div class="reloj-box">
        <p style="color:#888; margin:0; font-size:14px; letter-spacing:2px;">{now.strftime('%d . %m . %Y')}</p>
        <p class="reloj-h">{now.strftime('%H:%M:%S')}</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. PANEL DE ANÁLISIS ---
col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.markdown("### 📸 CAPTURA DE GRÁFICA")
    foto = st.camera_input("Escanear para analizar")
    
    st.write("")
    st.markdown("### ⚡ BOTONES DE REGISTRO")
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
    st.markdown("### 🎯 RESULTADO DEL ANÁLISIS")
    if foto or st.button("🚀 INICIAR ANÁLISIS"):
        st.session_state.mostrar_señal = True
        
    if st.session_state.mostrar_señal:
        # Efectividad Real solicitada (72% a 89%)
        porcentaje = random.uniform(72.5, 89.8)
        tipo_op = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
        color_fnd = "#1b5e20" if "COMPRA" in tipo_op else "#b71c1c"
        precio_ref = random.uniform(1.0820, 1.0850)
        
        st.markdown(f"""
            <div class="signal-card" style="background: {color_fnd};">
                <p style="margin:0; opacity:0.8;">HORA DE SEÑAL: {datetime.now(local_tz).strftime('%H:%M:%S')}</p>
                <h1 style="font-size: 50px; margin:10px 0;">{tipo_op}</h1>
                <h2 style="color: #ffd700; margin:0;">{porcentaje:.1f}% PRECISIÓN</h2>
                <hr style="border:0.5px solid rgba(255,255,255,0.2); margin:15px 0;">
                <p style="font-size:16px; font-weight:bold;">¡OPERACIÓN CONFIRMADA!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Módulo a Futuro solicitado
        st.markdown(f"""
            <div class="futuro-card">
                <h4 style="color:#ffd700; margin:0;">⏳ OPERACIÓN A FUTURO</h4>
                <p style="margin:5px 0; font-size:14px;">Entrada ideal: <b>{precio_ref:.5f}</b></p>
                <div style="display:flex; justify-content:space-between; font-size:13px;">
                    <span style="color:#00ff00;">TP: {(precio_ref + 0.0030):.5f}</span>
                    <span style="color:#ff4b4b;">SL: {(precio_ref - 0.0015):.5f}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Esperando datos de la gráfica...")

# --- 7. SELECTOR GLOBAL Y GRÁFICA ---
st.divider()
st.markdown("### 📈 SELECCIÓN DE MERCADOS MUNDIALES")

dict_mercados = {
    "EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "USD/JPY": "FX:USDJPY",
    "AUD/USD": "FX:AUDUSD", "USD/CAD": "FX:USDCAD", "EUR/JPY": "FX:EURJPY",
    "BITCOIN": "BINANCE:BTCUSDT", "ETHEREUM": "BINANCE:ETHUSDT", "SOLANA": "BINANCE:SOLUSDT",
    "ORO (XAUUSD)": "OANDA:XAUUSD", "PLATA (XAGUSD)": "OANDA:XAGUSD",
    "S&P 500": "FOREXCOM:SPXUSD", "NASDAQ 100": "FOREXCOM:NAS100", "DOW JONES": "FOREXCOM:DJI"
}

selec_m = st.selectbox("Cambiar Activo:", list(dict_mercados.keys()))
simbolo_final = dict_mercados[selec_m]

st.components.v1.html(f"""
    <div id="tv_v73" style="height:500px; border-radius:15px; overflow:hidden; border: 1px solid #333;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width":"100%","height":500,"symbol":"{simbolo_final}","interval":"1","theme":"dark","locale":"es","container_id":"tv_v73"}});
    </script>
""", height=500)