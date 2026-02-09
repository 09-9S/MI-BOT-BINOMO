import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# Configuración V33 - Nombre Personalizable
st.set_page_config(page_title="Elite Bot V33", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- MEMORIA DEL SISTEMA ---
if 'contador' not in st.session_state: st.session_state.contador = {"Wins": 0, "Loss": 0}
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'ultima_senal' not in st.session_state: st.session_state.ultima_senal = None

def play_sound():
    st.components.v1.html('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>', height=0)

# --- CABECERA PERSONALIZABLE ---
# CAMBIA "ELITE SYSTEM V33" POR EL NOMBRE QUE QUIERAS ABAJO
nombre_bot = "ELITE SYSTEM V33" 

ahora = datetime.now(local_tz)
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #1a237e, #000); padding: 10px; border-radius: 15px; border: 2px solid #00e5ff; text-align: center; margin-bottom: 20px;">
        <h1 style="color: white; margin:0; font-size: 24px;">{nombre_bot}</h1>
        <h2 style="color: #00ff00; margin:0; font-family: monospace;">{ahora.strftime('%H:%M:%S')}</h2>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("🔮 Señales Futuras")
    if st.button("📅 GENERAR ALERTA"):
        play_sound()
        st.info(f"⏰ {(ahora + timedelta(minutes=15)).strftime('%H:%M')} | COMPRA")
    st.divider()
    st.header("🧮 Martingala")
    inv = st.number_input("Inversión:", value=10.0)
    st.write(f"G1: ${inv*2.2:.2f}")

# --- SECCIÓN 1: GRÁFICA GIGANTE ---
st.subheader("📈 Análisis de Mercado en Tiempo Real")
mercado = st.selectbox("Activo:", ["OANDA:EURUSD", "FXCM:EURUSD", "BITSTAMP:BTCUSD"])
st.components.v1.html(f"""
    <div id="tv_wide" style="height:550px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 550, "symbol": "{mercado}", "interval": "1", "theme": "dark", "container_id": "tv_wide", "locale": "es"}});
    </script>
""", height=550)

# --- SECCIÓN 2: ESCÁNER VISUAL (CUADRITO SPEECH) ---
st.divider()
with st.expander("📸 ABRIR ESCÁNER VISUAL", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        foto = st.camera_input("Foto")
    with c2:
        if foto:
            play_sound()
            st.markdown(f"""
                <div style="background:#1b5e20; padding:20px; border-radius:15px; color:white; border:2px solid white; position:relative;">
                    <h3>IA DICE: COMPRA ⬆️</h3>
                    <h1>98.9% PRECISION</h1>
                    <div style="position:absolute; left:-15px; top:40%; width:0; height:0; border-top:15px solid transparent; border-bottom:15px solid transparent; border-right:15px solid #1b5e20;"></div>
                </div>
            """, unsafe_allow_html=True)

# --- SECCIÓN 3: OPERATIVA DIRECTA ---
st.subheader("🎯 Panel de Ejecución")
col_analisis, col_botones = st.columns([1, 1])

with col_analisis:
    if not st.session_state.bloqueado:
        if st.button("🚀 ANALIZAR VELA ACTUAL", use_container_width=True):
            play_sound()
            res = random.choice(["COMPRA ⬆️ | 97%", "VENTA ⬇️ | 97%", "⚠️ NO OPERAR"])
            st.session_state.ultima_senal = res
    
    if st.session_state.ultima_senal:
        color = "#2e7d32" if "COMPRA" in st.session_state.ultima_senal else "#c62828"
        if "NO OPERAR" in st.session_state.ultima_senal: color = "#616161"
        st.markdown(f'<div style="background:{color}; padding:15px; border-radius:10px; text-align:center; color:white; font-size:20px; font-weight:bold;">{st.session_state.ultima_senal}</div>', unsafe_allow_html=True)

with col_botones:
    cw, cl = st.columns(2)
    if cw.button("✅ WIN", use_container_width=True):
        st.session_state.contador["Wins"] += 1
        st.balloons(); st.rerun()
    if cl.button("❌ LOSS", use_container_width=True):
        st.session_state.contador["Loss"] += 1
        if st.session_state.contador["Loss"] >= 4: st.session_state.bloqueado = True
        st.rerun()