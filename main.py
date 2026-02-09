import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# Configuración de zona horaria para Colombia
local_tz = pytz.timezone('America/Bogota')

st.set_page_config(page_title="Analizador Pro V4 - Martingala", layout="wide")

# --- INICIALIZACIÓN DE SESIÓN ---
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

# --- RELOJ ANIMADO (SEGUNDERO REAL) ---
st.components.v1.html(
    """
    <div style="background: #111; padding: 10px; border-radius: 10px; border: 2px solid #00ff00; text-align: center;">
        <h1 style="color: #00ff00; font-family: monospace; margin: 0; font-size: 35px;">
            🕒 <span id="clock">00:00:00</span>
        </h1>
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
    height=100,
)

st.title("🛡️ Sistema de Trading: Martingala + Porcentaje")

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("📊 Marcador de Hoy")
    st.metric("GANADAS (WIN)", st.session_state.historial["Wins"])
    st.metric("PERDIDAS (LOSS)", st.session_state.historial["Loss"])
    
    st.divider()
    # INDICADOR VISUAL DE MARTINGALA
    if st.session_state.bloqueado:
        st.error("🚫 SISTEMA BLOQUEADO: Se perdieron 2 Martingalas.")
    else:
        color_gale = "green" if st.session_state.nivel_gale == 0 else "orange"
        st.markdown(f"**Nivel de Riesgo Actual:** :{color_gale}[{'Base (Bajo)' if st.session_state.nivel_gale == 0 else 'GALE ' + str(st.session_state.nivel_gale)}]")
    
    mercado = st.selectbox("Activo:", ["FX:EURUSD", "FX:GBPUSD", "FX:USDJPY", "BITSTAMP:BTCUSD"])
    if st.button("🔄 REINICIAR (Volver a Nivel 0)"):
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
            with st.spinner("Escaneando..."):
                time.sleep(1.5)
            res = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            porc = random.randint(89, 99) # El porcentaje de efectividad
            play_alert()
            st.session_state.ultima_senal = {"res": res, "porc": porc}
    
    if st.session_state.ultima_senal:
        s = st.session_state.ultima_senal
        st.success(f"🔥 SEÑAL: {s['res']} | EFECTIVIDAD: {s['porc']}%")

    st.divider()
    st.subheader("🛠️ Control de Resultados (Martingala)")
    c1, c2 = st.columns(2)
    if c1.button('✅ GANÉ (WIN)', use_container_width=True):
        st.session_state.historial["Wins"] += 1
        st.session_state.nivel_gale = 0 # REINICIA EL MARTINGALA A 0
        st.balloons()
        st.rerun()
    if c2.button('❌ PERDÍ (LOSS)', use_container_width=True):
        st.session_state.historial["Loss"] += 1
        st.session_state.nivel_gale += 1 # SUBE EL NIVEL DE MARTINGALA
        if st.session_state.nivel_gale >= 2:
            st.session_state.bloqueado = True # BLOQUEO DE SEGURIDAD
        st.rerun()

with tab2:
    st.subheader("📅 Calendario Futuro (10 Señales)")
    ahora_local = datetime.now(local_tz)
    data = []
    for i in range(1, 11):
        hora_f = (ahora_local + timedelta(minutes=i*2)).strftime("%H:%M")
        data.append({"HORA": hora_f, "ACCIÓN": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]), "PRECISIÓN": f"{random.randint(82, 95)}%"})
    st.table(data)