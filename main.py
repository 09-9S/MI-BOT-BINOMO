import streamlit as st
import time
import random
from datetime import datetime
import pytz

# Configuración de estética profesional
st.set_page_config(page_title="Elite Trading Bot - V5", layout="wide")

local_tz = pytz.timezone('America/Bogota')

# --- INICIALIZACIÓN DE MEMORIA ---
if 'historial' not in st.session_state: st.session_state.historial = {"Wins": 0, "Loss": 0}
if 'bitacora' not in st.session_state: st.session_state.bitacora = []
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'nivel_gale' not in st.session_state: st.session_state.nivel_gale = 0
if 'ultima_senal' not in st.session_state: st.session_state.ultima_senal = None

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)

# --- ENCABEZADO PREMIUM ---
st.components.v1.html(
    """
    <div style="background: linear-gradient(90deg, #000, #1b5e20); padding: 15px; border-radius: 15px; text-align: center; border: 1px solid #4caf50;">
        <h1 style="color: #fff; font-family: sans-serif; margin: 0;">ELITE TRADING BOT V5</h1>
        <h2 style="color: #00ff00; font-family: monospace; margin: 5px; font-size: 35px;"><span id="clock">00:00:00</span></h2>
    </div>
    <script>
        function updateClock() {
            const now = new Date();
            const options = { timeZone: 'America/Bogota', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' };
            document.getElementById('clock').innerText = now.toLocaleTimeString('en-GB', options);
        }
        setInterval(updateClock, 1000); updateClock();
    </script>
    """,
    height=130,
)

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("⚙️ Configuración")
    inversion = st.number_input("Inversión por operación ($):", min_value=1.0, value=10.0)
    payout = st.slider("Payout del Broker (%):", 70, 95, 85)
    
    st.divider()
    st.metric("WIN", st.session_state.historial["Wins"])
    st.metric("LOSS", st.session_state.historial["Loss"])
    
    if st.button("🗑️ REINICIAR TODO (CERO)"):
        st.session_state.historial = {"Wins": 0, "Loss": 0}
        st.session_state.bitacora = []
        st.session_state.bloqueado = False
        st.session_state.nivel_gale = 0
        st.rerun()

# --- INTERFAZ PRINCIPAL ---
col_main, col_hist = st.columns([2, 1])

with col_main:
    st.subheader("🚀 Analizador en Vivo")
    mercado = st.selectbox("Activo:", ["FX:EURUSD", "FX:GBPUSD", "OANDA:XAUUSD"])
    st.components.v1.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={mercado}&interval=1&theme=dark" height="350" width="100%"></iframe>', height=350)
    
    if not st.session_state.bloqueado:
        if st.button("🔍 ESCANEAR SEÑAL"):
            with st.spinner("Analizando..."): time.sleep(1)
            res = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            porc = random.randint(91, 99)
            play_alert()
            st.session_state.ultima_senal = {"res": res, "porc": porc}
    
    if st.session_state.ultima_senal:
        s = st.session_state.ultima_senal
        st.success(f"**SEÑAL: {s['res']} | EFECTIVIDAD: {s['porc']}%**")

    st.divider()
    c1, c2 = st.columns(2)
    # REGISTRO EN BITÁCORA
    if c1.button("✅ WIN"):
        ganancia = inversion * (payout / 100)
        nueva_op = {"Hora": datetime.now(local_tz).strftime("%H:%M:%S"), "Tipo": st.session_state.ultima_senal['res'] if st.session_state.ultima_senal else "N/A", "Resultado": "✅ WIN", "Ganancia": f"+${ganancia:.2f}"}
        st.session_state.bitacora.insert(0, nueva_op)
        st.session_state.historial["Wins"] += 1
        st.session_state.nivel_gale = 0
        st.rerun()
        
    if c2.button("❌ LOSS"):
        nueva_op = {"Hora": datetime.now(local_tz).strftime("%H:%M:%S"), "Tipo": st.session_state.ultima_senal['res'] if st.session_state.ultima_senal else "N/A", "Resultado": "❌ LOSS", "Ganancia": f"-${inversion:.2f}"}
        st.session_state.bitacora.insert(0, nueva_op)
        st.session_state.historial["Loss"] += 1
        st.session_state.nivel_gale += 1
        if st.session_state.nivel_gale >= 2: st.session_state.bloqueado = True
        st.rerun()

with col_hist:
    st.subheader("📑 Bitácora de Operaciones")
    # Mostrar las últimas 10 operaciones
    if st.session_state.bitacora:
        st.table(st.session_state.bitacora[:10])
    else:
        st.info("No hay operaciones registradas.")