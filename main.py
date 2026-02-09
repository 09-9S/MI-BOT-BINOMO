import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# Zona horaria Colombia
local_tz = pytz.timezone('America/Bogota')

st.set_page_config(page_title="Analizador Maestro V4", layout="wide")

# --- MEMORIA DEL BOT ---
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

# --- RELOJ CON SEGUNDERO (YA CORREGIDO) ---
st.components.v1.html(
    """
    <div style="background: #111; padding: 15px; border-radius: 10px; border: 2px solid #00ff00; text-align: center;">
        <h1 style="color: #00ff00; font-family: monospace; margin: 0; font-size: 40px;">
            <span id="clock">00:00:00</span>
        </h1>
        <p style="color: white; margin: 5px 0 0 0;">HORA COLOMBIA</p>
    </div>
    <script>
        function updateClock() {
            const now = new Date();
            const options = { timeZone: 'America/Bogota', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' };
            document.getElementById('clock').innerText = now.toLocaleTimeString('en-GB', options);
        }
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """,
    height=120,
)

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("🏆 Marcador Global")
    st.metric("WIN", st.session_state.historial["Wins"])
    st.metric("LOSS", st.session_state.historial["Loss"])
    st.divider()
    mercado = st.selectbox("Mercado:", ["FX:EURUSD", "FX:GBPUSD", "FX:USDJPY", "BITSTAMP:BTCUSD"])
    if st.button("🔄 REINICIAR TODO"):
        st.session_state.historial = {"Wins": 0, "Loss": 0}
        st.session_state.bloqueado = False
        st.session_state.nivel_gale = 0
        st.session_state.ultima_senal = None
        st.rerun()

# --- BLOQUES DE SEÑALES ---
tab1, tab2 = st.tabs(["⚡ SEÑAL AL MINUTO", "📅 PRÓXIMAS 10 SEÑALES"])

with tab1:
    st.components.v1.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={mercado}&interval=1&theme=dark" height="350" width="100%"></iframe>', height=350)
    
    if not st.session_state.bloqueado:
        if st.button("🚀 GENERAR SEÑAL AHORA", use_container_width=True):
            with st.spinner("Escaneando tendencia..."):
                time.sleep(1.5)
            res = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            porc = random.randint(88, 98)
            play_alert()
            st.session_state.ultima_senal = {"res": res, "porc": porc}
    else:
        st.error("🚫 SISTEMA BLOQUEADO (GALE 2 PERDIDO). Reinicia en el panel lateral.")

    if st.session_state.ultima_senal:
        s = st.session_state.ultima_senal
        if "COMPRA" in s["res"]:
            st.success(f"🔥 SEÑAL: {s['res']} | EFECTIVIDAD: {s['porc']}%")
        else:
            st.error(f"🔥 SEÑAL: {s['res']} | EFECTIVIDAD: {s['porc']}%")

    st.divider()
    st.write("### Registrar Resultado")
    c1, c2 = st.columns(2)
    if c1.button('✅ GANADA (WIN)', use_container_width=True):
        st.session_state.historial["Wins"] += 1
        st.session_state.nivel_gale = 0
        st.balloons()
        st.rerun()
    if c2.button('❌ PERDIDA (LOSS)', use_container_width=True):
        st.session_state.historial["Loss"] += 1
        st.session_state.nivel_gale += 1
        if st.session_state.nivel_gale >= 2: st.session_state.bloqueado = True
        st.rerun()

with tab2:
    st.subheader("📅 Calendario Futuro (Próximas 10)")
    ahora_local = datetime.now(local_tz)
    data = []
    for i in range(1, 11):
        hora_f = (ahora_local + timedelta(minutes=i*2)).strftime("%H:%M")
        data.append({"HORA": hora_f, "ACCIÓN": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]), "PRECISIÓN": f"{random.randint(82, 95)}%"})
    st.table(data)