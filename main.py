import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# Zona horaria Colombia
local_tz = pytz.timezone('America/Bogota')

st.set_page_config(page_title="Analizador Maestro V3", layout="wide")

# --- INICIALIZACIÓN ---
if 'historial' not in st.session_state:
    st.session_state.historial = {"Wins": 0, "Loss": 0}
if 'bloqueado' not in st.session_state:
    st.session_state.bloqueado = False
if 'nivel_gale' not in st.session_state:
    st.session_state.nivel_gale = 0
if 'ultima_senal' not in st.session_state:
    st.session_state.ultima_senal = None

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)

# --- RELOJ ANIMADO CORREGIDO ---
st.components.v1.html(
    """
    <div style="background: #1e1e1e; padding: 10px; border-radius: 10px; border: 1px solid #333; text-align: center;">
        <h2 style="color: #00ff00; font-family: 'Courier New', Courier, monospace; margin: 0;">
            🕒 HORA COLOMBIA: <span id="clock">00:00:00</span>
        </h2>
    </div>
    <script>
        function updateClock() {
            const now = new Date();
            const options = { timeZone: 'America/Bogota', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' };
            const timeString = now.toLocaleTimeString('en-GB', options);
            document.getElementById('clock').innerText = timeString;
        }
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """,
    height=80,
)

st.title("🛡️ Estación de Análisis Dual")

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("📊 Gestión de Riesgo")
    st.metric("GANADAS", st.session_state.historial["Wins"])
    st.metric("PERDIDAS", st.session_state.historial["Loss"])
    st.divider()
    if st.session_state.bloqueado:
        st.error("🚫 SISTEMA BLOQUEADO (GALE 2)")
    else:
        st.info(f"Nivel: {'Base' if st.session_state.nivel_gale == 0 else 'Martingala ' + str(st.session_state.nivel_gale)}")
    
    mercado = st.selectbox("Mercado:", ["FX:EURUSD", "FX:GBPUSD", "FX:USDJPY", "BITSTAMP:BTCUSD"])
    if st.button("🔄 REINICIAR TODO"):
        st.session_state.historial = {"Wins":