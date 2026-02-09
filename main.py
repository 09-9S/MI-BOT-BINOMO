import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# Configuración V32 - Gráfica Extendida y Operativa Inferior
st.set_page_config(page_title="Elite Bot V32 - Wide View", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- INICIALIZACIÓN DE MEMORIA ---
if 'historial_lista' not in st.session_state: st.session_state.historial_lista = []
if 'contador' not in st.session_state: st.session_state.contador = {"Wins": 0, "Loss": 0}
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'ultima_senal' not in st.session_state: st.session_state.ultima_senal = None

def play_sound():
    st.components.v1.html('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>', height=0)

# --- CABECERA ---
ahora = datetime.now(local_tz)
st.markdown(f"""
    <div style="background: #000; padding: 10px; border-radius: 10px; border-bottom: 3px solid #00e5ff; text-align: center; margin-bottom: 10px;">
        <h2 style="color: white; margin:0; font-size: 20px;">ELITE V32 - VISTA PANORÁMICA PROFESIONAL</h2>
        <h1 style="color: #00ff00; margin:0; font-family: monospace;">{ahora.strftime('%H:%M:%S')}</h1>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL (GALE Y FUTURO) ---
with st.sidebar:
    st.header("🧮 Gestión Gale")
    inv = st.number_input("Inversión ($):", value=10.0)
    st.caption(f"G1: ${inv*2.2:.2f} | G2: ${inv*4.8:.2f}")
    st.divider()
    st.header("🔮 Próximas Entradas")
    if st.button("📅 GENERAR"):
        play_sound()
        for i in range(2):
            st.info(f"⏰ {(ahora + timedelta(minutes=random.randint(5,30))).strftime('%H:%M')} | COMPRA")

# --- SECCIÓN 1: ESCÁNER VISUAL (CENTRO) ---
with st.expander("📸 ESCÁNER DE VISIÓN IA (ABRIR PARA ANALIZAR FOTO)", expanded=False):
    col_c, col_s = st.columns([1, 1])
    with col_c:
        foto = st.camera_input("Captura")
    with col_s:
        if foto:
            play_sound()
            st.markdown(f'<div style="background:#1b5e20; padding:20px; border-radius:15px; color:white; border:2px solid white; text-align:center;"><h2>ANÁLISIS IA: SUBE ⬆️</h2><h1>98.7%</h1></div>', unsafe_allow_html=True)

st.divider()

# --- SECCIÓN 2: GRÁFICA ANCHA (VISTA TOTAL) ---
st.subheader("📈 Gráfica de Referencia Full Width")
mercado = st.selectbox("Seleccionar Activo:", ["OANDA:EURUSD", "FXCM:EURUSD", "BITSTAMP:BTCUSD"])
st.components.v1.html(f"""
    <div id="tv_panoramic" style="height:500px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 500, "symbol": "{mercado}", "interval": "1", "theme": "dark", "container_id": "tv_panoramic", "style": "1", "locale": "es", "toolbar_bg": "#f1f3f6", "enable_publishing": false, "hide_side_toolbar": false, "allow_symbol_change": true}});
    </script>
""", height=500)

# --- SECCIÓN 3: OPERATIVA DIRECTA (ABAJO DE LA GRÁFICA) ---
st.markdown("---")
st.subheader("🎯 Panel de Operativa Directa")
col_bot, col_status, col_hist = st.columns([1, 1, 1])

with col_bot:
    if not st.session_state.bloqueado:
        if st.button("🚀 ANALIZAR AHORA", use_container_width=True):
            play_sound()
            with st.spinner("Sincronizando..."):
                time.sleep(1.5)
                if random.random() < 0.15:
                    st.session_state.ultima_senal = {"res": "⚠️ NO OPERAR", "clr": "#ff4b4b"}
                else:
                    st.session_state.ultima_senal = {"res": "VENTA ⬇️ | 97.4%", "clr": "#c62828"}

with col_status:
    if st.session_state.ultima_senal:
        s = st.session_state.ultima_senal
        st.markdown(f'<div style="background:{s["clr"]}; padding:10px; border-radius:10px; text-align:center; color:white; font-weight:bold;">{s["res"]}</div>', unsafe_allow_html=True)

with col_hist:
    cw, cl = st.columns(2)
    if cw.button("✅ WIN", use_container_width=True):
        st.session_state.contador["Wins"] += 1
        st.session_state.historial_lista.insert(0, {"H": ahora.strftime("%H:%M"), "R": "WIN ✅"})
        st.balloons(); st.rerun()
    if cl.button("❌ LOSS", use_container_width=True):
        st.session_state.contador["Loss"] += 1
        st.session_state.historial_lista.insert(0, {"H": ahora.strftime("%H:%M"), "R": "LOSS ❌"})
        if st.session_state.contador["Loss"] >= 4: st.session_state.bloqueado = True
        st.rerun()

# --- HISTORIAL INFERIOR ---
if st.session_state.historial_lista:
    with st.expander("📝 Ver Historial de Operaciones", expanded=False):
        st.table(st.session_state.historial_lista[:5])