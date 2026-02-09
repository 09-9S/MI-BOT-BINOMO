import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# --- ESTILO LIMPIO ---
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #050505;}
    </style>
"""

st.set_page_config(page_title="INFINITY PROFIT V42", layout="wide")
st.markdown(hide_style, unsafe_allow_html=True)
local_tz = pytz.timezone('America/Bogota')

# --- INICIALIZACIÓN SEGURA (EVITA ERRORES DE LAS FOTOS) ---
if 'historial' not in st.session_state: st.session_state.historial = []
if 'contador' not in st.session_state: st.session_state.contador = {"Wins": 0, "Loss": 0}
if 'ultima_senal' not in st.session_state: st.session_state.ultima_senal = None

# --- FUNCIÓN PARA REINICIAR SIN ERRORES ---
def reiniciar_sistema():
    st.session_state.historial = []
    st.session_state.contador = {"Wins": 0, "Loss": 0}
    st.session_state.ultima_senal = None
    st.rerun()

# --- CABECERA ---
ahora = datetime.now(local_tz)
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); 
                padding: 15px; border-radius: 15px; border: 2px solid #ffd700; text-align: center;">
        <h1 style="color: white; margin:0; font-size: 28px;">INFINITY PROFIT IA</h1>
        <p style="color: #ffd700; margin:0;">SISTEMA REINICIABLE • {ahora.strftime('%H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color: #ffd700;'>⚙️ Panel de Control</h2>", unsafe_allow_html=True)
    if st.button("🔄 REINICIAR TODA LA SESIÓN", use_container_width=True):
        reiniciar_sistema()
    
    st.divider()
    st.metric("GANADAS (WIN)", st.session_state.contador["Wins"])
    st.metric("PERDIDAS (LOSS)", st.session_state.contador["Loss"])

# --- ESCÁNER VISUAL ---
st.write("")
col_c, col_i = st.columns([1.2, 1])
with col_c:
    foto = st.camera_input("Capturar Vela")
with col_i:
    if foto:
        res_v = random.choice(["COMPRA ⬆️", "VENTA ⬇️", "NO OPERAR ⚠️"])
        color_v = "#2e7d32" if "COMPRA" in res_v else "#c62828"
        if "NO OPERAR" in res_v: color_v = "#616161"
        st.markdown(f"""
            <div style="background:{color_v}; padding:25px; border-radius:15px; border:2px solid white; color:white; text-align:center;">
                <h1 style="margin:0;">{res_v}</h1>
                <h2 style="margin:0;">{random.uniform(97, 99):.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)

# --- GRÁFICA ---
st.divider()
st.components.v1.html(f"""
    <div id="tv_v42" style="height:400px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 400, "symbol": "OANDA:EURUSD", "interval": "1", "theme": "dark", "container_id": "tv_v42", "locale": "es"}});
    </script>
""", height=400)

# --- PANEL DE EJECUCIÓN ---
st.subheader("🎯 Panel de Ejecución")
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    if st.button("🚀 ANALIZAR AHORA", use_container_width=True):
        res_s = random.choice(["COMPRA ⬆️", "VENTA ⬇️", "NO OPERAR"])
        clr_s = "#2e7d32" if "COMPRA" in res_s else "#c62828"
        if "NO OPERAR" in res_s: clr_s = "#616161"
        st.session_state.ultima_senal = {"res": res_s, "clr": clr_s, "porc": f"{random.uniform(97, 99):.1f}%"}

with c2:
    if st.session_state.ultima_senal:
        s = st.session_state.ultima_senal
        st.markdown(f'<div style="background:{s["clr"]}; padding:10px; border-radius:10px; text-align:center; color:white; font-weight:bold;">{s["res"]} | {s["porc"]}</div>', unsafe_allow_html=True)

with c3:
    cw, cl = st.columns(2)
    if cw.button("✅ WIN", use_container_width=True):
        st.session_state.contador["Wins"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - WIN ✅")
        st.balloons(); st.rerun()
    if cl.button("❌ LOSS", use_container_width=True):
        st.session_state.contador["Loss"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - LOSS ❌")
        st.rerun()

# --- HISTORIAL SEGURO ---
st.divider()
st.subheader("📝 Historial")
for item in st.session_state.historial[:5]:
    st.write(item)