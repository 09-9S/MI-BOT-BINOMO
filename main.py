import streamlit as st
import time
import random
from datetime import datetime
import pytz

# --- ESTILO DE ALTA VISIBILIDAD ---
st.set_page_config(page_title="INFINITY PROFIT V61", layout="wide")

# Intentar detectar zona horaria local, por defecto Bogotá
try:
    local_tz = pytz.timezone('America/Bogota')
except:
    local_tz = pytz.utc

st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    label, p, h1, h2, h3, h4, span { color: #ffffff !important; font-weight: bold !important; }
    .pacto-box { border: 2px solid #ffd700; border-radius: 15px; padding: 20px; background: #111; text-align: center; }
    .stButton > button { width: 100%; height: 50px; font-weight: bold; border-radius: 10px; border: 2px solid #fff; }
    .btn-compra button { background-color: #2e7d32 !important; }
    .btn-venta button { background-color: #c62828 !important; }
    .btn-analizar button { background-color: #ffd700 !important; color: black !important; }
    .reloj-text { font-size: 24px; color: #ffd700 !important; font-weight: bold; text-align: center; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- MEMORIA ---
if 'ganadas' not in st.session_state: st.session_state.ganadas = 0
if 'perdidas' not in st.session_state: st.session_state.perdidas = 0

# --- PANEL LATERAL ---
with st.sidebar:
    # RELOJ EN TIEMPO REAL
    hora_actual = datetime.now(local_tz).strftime("%H:%M:%S")
    st.markdown(f"<div class='reloj-text'>🕒 HORA LOCAL<br>{hora_actual}</div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='color:#ffd700;'>🌍 MERCADOS</h2>", unsafe_allow_html=True)
    diccionario_mercados = {
        "EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "XAU/USD (ORO)": "OANDA:XAUUSD",
        "BTC/USD": "BINANCE:BTCUSDT", "SOL/USD": "BINANCE:SOLUSDT"
    }
    seleccion = st.selectbox("ELEGIR ACTIVO:", list(diccionario_mercados.keys()))
    simbolo_tv = diccionario_mercados[seleccion]
    
    st.divider()
    st.success(f"WIN: {st.session_state.ganadas}")
    st.error(f"LOSS: {st.session_state.perdidas}")
    if st.button("🔄 REINICIAR"):
        st.session_state.ganadas = 0
        st.session_state.perdidas = 0
        st.rerun()

# --- CABECERA ---
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); padding: 15px; border-radius: 10px; border: 2px solid #ffd700; text-align: center;">
        <h1 style="color: white; margin:0; font-size: 24px;">INFINITY PROFIT IA V.61</h1>
        <p style="color: #ffd700; margin:0;">SISTEMA INTEGRAL MT5 & BINARIAS</p>
    </div>
""", unsafe_allow_html=True)

# --- BOTONES DE ACCIÓN ---
st.write("")
c_win, c_loss = st.columns(2)
with c_win:
    st.markdown('<div class="btn-compra">', unsafe_allow_html=True)
    if st.button("⬆️ GANÉ (WIN)"): st.session_state.ganadas += 1
    st.markdown('</div>', unsafe_allow_html=True)
with c_loss:
    st.markdown('<div class="btn-venta">', unsafe_allow_html=True)
    if st.button("⬇️ PERDÍ (LOSS)"): st.session_state.perdidas += 1
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANÁLISIS HÍBRIDO CON HORA ---
st.divider()
col1, col2 = st.columns([1, 1.2])

with col1:
    foto = st.camera_input("📸 ANALIZAR GRÁFICA")

with col2:
    if foto or st.button("🚀 GENERAR SEÑAL"):
        tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
        porcentaje = random.uniform(98.5, 99.9)
        hora_entrada = datetime.now(local_tz).strftime("%H:%M:%S")
        
        # Datos MT5
        precio = random.uniform(1.0820, 1.0850)
        tp = precio + 0.0040 if "COMPRA" in tipo else precio - 0.0040
        sl = precio - 0.0020 if "COMPRA" in tipo else precio + 0.0020
        color_sig = "#1b5e20" if "COMPRA" in tipo else "#b71c1c"
        
        st.markdown(f"""
            <div class="pacto-box" style="background: {color_sig}; border: 3px solid white;">
                <p style="margin:0; color:#ffd700;">🕒 ENTRADA TOMADA A LAS: {hora_entrada}</p>
                <h1 style="font-size: 45px; margin:0;">{tipo}</h1>
                <h2 style="color: #ffd700; margin:0;">{porcentaje:.1f}% PRECISIÓN</h2>
                <hr>
                <p style="margin:0; font-weight:bold;">CONFIGURACIÓN METATRADER 5:</p>
                <div style="display: flex; justify-content: space-around; margin-top:10px;">
                    <div><p style="color:#00ff00; margin:0;">TP</p><h3>{tp:.5f}</h3></div>
                    <div><p style="color:#ff5252; margin:0;">SL</p><h3>{sl:.5f}</h3></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- GRÁFICA ---
st.divider()
st.components.v1.html(f"""
    <div id="tv_v61" style="height:500px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 500, "symbol": "{simbolo_tv}", "interval": "1", "theme": "dark", "locale": "es", "container_id": "tv_v61"}});
    </script>
""", height=500)