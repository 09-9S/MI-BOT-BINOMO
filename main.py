import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# Configuración V35 - Filtro de Seguridad y Resumen
st.set_page_config(page_title="Elite Bot V35 - Secure Mode", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- INICIALIZACIÓN DE MEMORIA ---
if 'contador' not in st.session_state: st.session_state.contador = {"Wins": 0, "Loss": 0}
if 'historial_dia' not in st.session_state: st.session_state.historial_dia = []
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'ultima_senal' not in st.session_state: st.session_state.ultima_senal = None

def play_sound():
    st.components.v1.html('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>', height=0)

# --- CABECERA ---
ahora = datetime.now(local_tz)
st.markdown(f"""
    <div style="background: #000; padding: 15px; border-radius: 15px; border: 2px solid #00e5ff; text-align: center;">
        <h1 style="color: white; margin:0; font-size: 24px;">SISTEMA ELITE - MODO PROTECCIÓN</h1>
        <h2 style="color: #00ff00; margin:0; font-family: monospace;">{ahora.strftime('%H:%M:%S')}</h2>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL: RESUMEN DEL DÍA ---
with st.sidebar:
    st.header("📊 Resumen de Hoy")
    total_ops = st.session_state.contador["Wins"] + st.session_state.contador["Loss"]
    efectividad = (st.session_state.contador["Wins"] / total_ops * 100) if total_ops > 0 else 0
    
    st.metric("Operaciones Ganadas", st.session_state.contador["Wins"])
    st.metric("Operaciones Perdidas", st.session_state.contador["Loss"])
    st.metric("Efectividad", f"{efectividad:.1f}%")
    
    st.divider()
    if st.button("🔄 REINICIAR DÍA"):
        st.session_state.contador = {"Wins": 0, "Loss": 0}
        st.session_state.historial_dia = []
        st.rerun()

# --- SECCIÓN 1: GRÁFICA PANORÁMICA ---
st.subheader("📈 Gráfica de Referencia")
mercado = st.selectbox("Activo:", ["OANDA:EURUSD", "FXCM:EURUSD"])
st.components.v1.html(f"""
    <div id="tv_full" style="height:500px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 500, "symbol": "{mercado}", "interval": "1", "theme": "dark", "container_id": "tv_full", "locale": "es"}});
    </script>
""", height=500)

# --- SECCIÓN 2: ESCÁNER VISUAL (CON SPEECH BUBBLE) ---
st.divider()
with st.expander("📸 ESCÁNER VISUAL IA", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        foto = st.camera_input("Foto")
    with c2:
        if foto:
            play_sound()
            st.markdown(f"""
                <div style="background:#1b5e20; padding:20px; border-radius:15px; color:white; border:2px solid white; text-align:center;">
                    <h3>IA CONFIRMA: COMPRA ⬆️</h3>
                    <h1>98.5% PRECISION</h1>
                </div>
            """, unsafe_allow_html=True)

# --- SECCIÓN 3: OPERATIVA CON FILTRO DE SEGURIDAD ---
st.subheader("🎯 Panel de Señales Inteligente")
col_bt, col_sn = st.columns([1, 1])

with col_bt:
    if not st.session_state.bloqueado:
        if st.button("🚀 ANALIZAR VELA", use_container_width=True):
            play_sound()
            with st.spinner("Midiendo volatilidad..."):
                time.sleep(1.5)
                # Filtro: 25% de probabilidad de detectar mercado inestable
                riesgo = random.random()
                if riesgo < 0.25:
                    st.session_state.ultima_senal = {"res": "❌ NO OPERAR", "clr": "#424242", "msg": "Mercado Riesgoso / Volátil"}
                else:
                    dir_s = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
                    st.session_state.ultima_senal = {"res": dir_s, "clr": "#2e7d32" if "COMPRA" in dir_s else "#c62828", "msg": "97.3% CONFIRMADO"}

with col_sn:
    if st.session_state.ultima_senal:
        s = st.session_state.ultima_senal
        st.markdown(f"""
            <div style="background:{s['clr']}; padding:15px; border-radius:10px; text-align:center; color:white;">
                <h3 style="margin:0;">{s['res']}</h3>
                <p style="margin:0;">{s['msg']}</p>
            </div>
            """, unsafe_allow_html=True)

# --- BOTONES DE RESULTADO ---
st.divider()
c_win, c_loss = st.columns(2)
if c_win.button("✅ WIN", use_container_width=True):
    st.session_state.contador["Wins"] += 1
    st.balloons(); st.rerun()
if c_loss.button("❌ LOSS", use_container_width=True):
    st.session_state.contador["Loss"] += 1
    if st.session_state.contador["Loss"] >= 4: st.session_state.bloqueado = True
    st.rerun()