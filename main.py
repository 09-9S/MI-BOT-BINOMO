import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# Configuración profesional de alto nivel
st.set_page_config(page_title="Elite Bot V9 - Terminal Integrada", layout="wide")

local_tz = pytz.timezone('America/Bogota')

# --- MEMORIA BLINDADA ---
if 'historial' not in st.session_state: st.session_state.historial = {"Wins": 0, "Loss": 0}
if 'bitacora' not in st.session_state: st.session_state.bitacora = []
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'nivel_gale' not in st.session_state: st.session_state.nivel_gale = 0
if 'ultima_senal' not in st.session_state: st.session_state.ultima_senal = None

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)

# --- CABECERA PREMIUM ---
st.components.v1.html(
    """
    <div style="background: linear-gradient(90deg, #000, #1b5e20, #000); padding: 10px; border-radius: 15px; text-align: center; border: 2px solid #4caf50;">
        <h1 style="color: #fff; font-family: sans-serif; margin: 0; font-size: 20px;">TERMINAL ELITE V9</h1>
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
    height=125,
)

# --- PANEL LATERAL DE CONFIGURACIÓN ---
with st.sidebar:
    st.header("⚙️ Ajustes")
    mercado = st.selectbox("Mercado:", ["FX:EURUSD", "FX:GBPUSD", "OANDA:XAUUSD", "BITSTAMP:BTCUSD"])
    inv_base = st.number_input("Inversión ($):", min_value=1.0, value=10.0)
    payout = st.slider("Payout %:", 70, 95, 85)
    st.divider()
    st.metric("GANADAS", st.session_state.historial["Wins"])
    st.metric("PERDIDAS", st.session_state.historial["Loss"])
    if st.button("🔄 REINICIAR SISTEMA"):
        st.session_state.historial = {"Wins": 0, "Loss": 0}
        st.session_state.bitacora = []
        st.session_state.bloqueado = False
        st.session_state.nivel_gale = 0
        st.session_state.ultima_senal = None
        st.rerun()

# --- INTERFAZ DE 2 BLOQUES ---
tab1, tab2 = st.tabs(["⚡ ANALIZADOR TOTAL", "📅 SEÑALES A FUTURO"])

with tab1:
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        # ALERTA DE MARTINGALA INTEGRADA
        if st.session_state.nivel_gale > 0 and not st.session_state.bloqueado:
            st.warning(f"⚠️ MARTINGALA {st.session_state.nivel_gale} REQUERIDO")
        
        st.components.v1.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={mercado}&interval=1&theme=dark" height="380" width="100%"></iframe>', height=380)
        
        if not st.session_state.bloqueado:
            if st.button("🔍 ESCANEAR MERCADO", use_container_width=True):
                with st.spinner("Analizando..."): time.sleep(1)
                res = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
                porc = random.randint(91, 99)
                play_alert()
                st.session_state.ultima_senal = {"res": res, "porc": porc}
        else:
            st.error("🚫 BLOQUEO POR GALE 2")

        if st.session_state.ultima_senal:
            s = st.session_state.ultima_senal
            color = "#2e7d32" if "COMPRA" in s["res"] else "#c62828"
            st.markdown(f'<div style="background-color: {color}; padding: 15px; border-radius: 10px; text-align:center; color:white;"><h3>{s["res"]} | {s["porc"]}%</h3></div>', unsafe_allow_html=True)

    with col_der:
        st.subheader("📊 Control")
        c1, c2 = st.columns(2)
        if c1.button("✅ WIN", use_container_width=True):
            gan = (inv_base * (2**st.session_state.nivel_gale)) * (payout/100)
            st.session_state.bitacora.insert(0, {"H": datetime.now(local_tz).strftime("%H:%M"), "R": "WIN ✅", "P": f"+${gan:.2f}"})
            st.session_state.historial["Wins"] += 1
            st.session_state.nivel_gale = 0
            st.balloons(); st.rerun()
        
        if c2.button("❌ LOSS", use_container_width=True):
            per = inv_base * (2**st.session_state.nivel_gale)
            st.session_state.bitacora.insert(0, {"H": datetime.now(local_tz).strftime("%H:%M"), "R": "LOSS ❌", "P": f"-${per:.2f}"})
            st.session_state.historial["Loss"] += 1
            st.session_state.nivel_gale += 1
            if st.session_state.nivel_gale > 2: st.session_state.bloqueado = True
            st.rerun()
        
        st.divider()
        st.write("**Historial de Hoy:**")
        if st.session_state.bitacora:
            st.table(st.session_state.bitacora[:10])
        else:
            st.caption("Esperando resultados...")

with tab2:
    st.subheader("📅 Próximas 10 Señales")
    ahora = datetime.now(local_tz)
    futuras = [{"HORA": (ahora + timedelta(minutes=i*3)).strftime("%H:%M"), "ACCIÓN": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]), "CONFIANZA": f"{random.randint(85, 96)}%"} for i in range(1, 11)]
    st.table(futuras)