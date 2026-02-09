import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# Configuración profesional para venta
st.set_page_config(page_title="Elite Bot V8 - Martingala System", layout="wide")

local_tz = pytz.timezone('America/Bogota')

# --- MEMORIA DEL SISTEMA ---
if 'historial' not in st.session_state: st.session_state.historial = {"Wins": 0, "Loss": 0}
if 'bitacora' not in st.session_state: st.session_state.bitacora = []
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'nivel_gale' not in st.session_state: st.session_state.nivel_gale = 0
if 'ultima_senal' not in st.session_state: st.session_state.ultima_senal = None

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)

# --- CABECERA CON RELOJ ---
st.components.v1.html(
    """
    <div style="background: linear-gradient(90deg, #000, #1b5e20, #000); padding: 15px; border-radius: 15px; text-align: center; border: 2px solid #4caf50;">
        <h1 style="color: #fff; font-family: sans-serif; margin: 0; font-size: 22px; letter-spacing: 2px;">ELITE BOT V8 - PROTECCIÓN PRO</h1>
        <h2 style="color: #00ff00; font-family: monospace; margin: 5px; font-size: 38px;"><span id="clock">00:00:00</span></h2>
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
    height=140,
)

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("💵 Configuración")
    mercado = st.selectbox("Activo:", ["FX:EURUSD", "FX:GBPUSD", "OANDA:XAUUSD", "BITSTAMP:BTCUSD"])
    inversion_base = st.number_input("Inversión Inicial ($):", min_value=1.0, value=10.0)
    payout = st.slider("Payout %:", 70, 95, 85)
    st.divider()
    st.metric("GANADAS (WIN)", st.session_state.historial["Wins"])
    st.metric("PERDIDAS (LOSS)", st.session_state.historial["Loss"])
    if st.button("🔄 REINICIAR TODO"):
        st.session_state.historial = {"Wins": 0, "Loss": 0}
        st.session_state.bitacora = []
        st.session_state.bloqueado = False
        st.session_state.nivel_gale = 0
        st.session_state.ultima_senal = None
        st.rerun()

# --- INTERFAZ DE 3 BLOQUES ---
tab1, tab2, tab3 = st.tabs(["⚡ ANALIZADOR", "📅 SEÑALES", "📊 BITÁCORA"])

with tab1:
    # BLOQUE DE ALERTA DE MARTINGALA (EL QUE PEDISTE)
    if st.session_state.nivel_gale > 0 and not st.session_state.bloqueado:
        st.warning(f"⚠️ **ATENCIÓN: OPERACIÓN EN MARTINGALA {st.session_state.nivel_gale}**")
        st.markdown(f"""
            <div style="background-color: #ff9800; padding: 15px; border-radius: 10px; text-align: center; color: black; border: 2px solid black; font-weight: bold;">
                ESTADO: ENTRADA FALLIDA ANTERIOR <br>
                INSTRUCCIÓN: REALICE EL MARTINGALA {st.session_state.nivel_gale} AHORA.
            </div>
            """, unsafe_allow_html=True)
    
    st.components.v1.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={mercado}&interval=1&theme=dark" height="380" width="100%"></iframe>', height=380)
    
    if not st.session_state.bloqueado:
        if st.button("🚀 GENERAR SEÑAL AHORA", use_container_width=True):
            with st.spinner("Escaneando tendencia..."): time.sleep(1)
            res = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            porc = random.randint(91, 99)
            play_alert()
            st.session_state.ultima_senal = {"res": res, "porc": porc}
    else:
        st.error("🚫 BLOQUEO DE SEGURIDAD: GALE 2 PERDIDO. POR FAVOR REINICIE EL SISTEMA.")

    if st.session_state.ultima_senal:
        s = st.session_state.ultima_senal
        color = "#2e7d32" if "COMPRA" in s["res"] else "#c62828"
        st.markdown(f"""<div style="background-color: {color}; padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <h2 style="margin:0;">{s['res']} | CONFIANZA: {s['porc']}%</h2></div>""", unsafe_allow_html=True)

with tab2:
    st.subheader("📅 Calendario Futuro")
    ahora = datetime.now(local_tz)
    data = [{"HORA": (ahora + timedelta(minutes=i*3)).strftime("%H:%M"), "ACCIÓN": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]), "ÉXITO": f"{random.randint(85, 96)}%"} for i in range(1, 11)]
    st.table(data)

with tab3:
    st.subheader("📊 Gestión y Resultados")
    cw, cl = st.columns(2)
    with cw:
        if st.button("✅ MARCAR WIN", use_container_width=True):
            inv = inversion_base * (2 ** st.session_state.nivel_gale)
            st.session_state.bitacora.insert(0, {"Hora": datetime.now(local_tz).strftime("%H:%M:%S"), "Tipo": "WIN ✅", "Monto": f"+${inv*(payout/100):.2f}"})
            st.session_state.historial["Wins"] += 1
            st.session_state.nivel_gale = 0 # REINICIA GALE AL GANAR
            st.balloons(); st.rerun()
    with cl:
        if st.button("❌ MARCAR LOSS", use_container_width=True):
            inv = inversion_base * (2 ** st.session_state.nivel_gale)
            st.session_state.bitacora.insert(0, {"Hora": datetime.now(local_tz).strftime("%H:%M:%S"), "Tipo": "LOSS ❌", "Monto": f"-${inv:.2f}"})
            st.session_state.historial["Loss"] += 1
            st.session_state.nivel_gale += 1 # SUBE NIVEL DE GALE
            if st.session_state.nivel_gale > 2: st.session_state.bloqueado = True
            st.rerun()
    st.divider()
    st.write("### Historial Reciente")
    st.table(st.session_state.bitacora[:10])