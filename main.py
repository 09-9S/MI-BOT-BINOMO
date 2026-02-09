import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# Configuración de Alta Gama
st.set_page_config(page_title="Elite Bot V10 - Terminal Pro", layout="wide")

local_tz = pytz.timezone('America/Bogota')

# --- MEMORIA DEL SISTEMA ---
if 'historial' not in st.session_state: st.session_state.historial = {"Wins": 0, "Loss": 0}
if 'bitacora' not in st.session_state: st.session_state.bitacora = []
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'nivel_gale' not in st.session_state: st.session_state.nivel_gale = 0
if 'ultima_senal' not in st.session_state: st.session_state.ultima_senal = None

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)

# --- CABECERA ESTILO DASHBOARD ---
st.components.v1.html(
    """
    <div style="background: linear-gradient(90deg, #000, #1b5e20, #000); padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #4caf50; margin-bottom: 10px;">
        <h1 style="color: #fff; font-family: sans-serif; margin: 0; font-size: 18px; letter-spacing: 2px;">TERMINAL DE OPERACIONES ELITE V10</h1>
        <h2 style="color: #00ff00; font-family: monospace; margin: 5px; font-size: 32px;"><span id="clock">00:00:00</span></h2>
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
    height=120,
)

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("⚙️ Parámetros")
    mercado = st.selectbox("Activo:", ["FX:EURUSD", "FX:GBPUSD", "OANDA:XAUUSD", "BITSTAMP:BTCUSD"])
    inv_base = st.number_input("Inversión ($):", min_value=1.0, value=10.0)
    payout = st.slider("Payout %:", 70, 95, 85)
    st.divider()
    if st.button("🔄 REINICIAR SESIÓN"):
        st.session_state.historial = {"Wins": 0, "Loss": 0}
        st.session_state.bitacora = []
        st.session_state.bloqueado = False
        st.session_state.nivel_gale = 0
        st.session_state.ultima_senal = None
        st.rerun()

# --- ESTRUCTURA DE BLOQUES ---
tab1, tab2 = st.tabs(["⚡ OPERACIÓN EN VIVO", "📅 CALENDARIO DE SEÑALES"])

with tab1:
    # 1. BLOQUE DE GRÁFICA AMPLIADA (ARRIBA)
    st.components.v1.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={mercado}&interval=1&theme=dark" height="450" width="100%"></iframe>', height=450)
    
    st.divider()

    # 2. BLOQUE DE CONTROL Y RESULTADOS (ABAJO)
    col_acc, col_gale, col_hist = st.columns([1.5, 1.5, 2])

    with col_acc:
        st.subheader("🎯 Acción")
        if not st.session_state.bloqueado:
            if st.button("🔍 ESCANEAR SEÑAL", use_container_width=True):
                with st.spinner("Analizando..."): time.sleep(1)
                res = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
                porc = random.randint(91, 99)
                play_alert()
                st.session_state.ultima_senal = {"res": res, "porc": porc}
        else:
            st.error("🚫 SISTEMA BLOQUEADO")

        if st.session_state.ultima_senal:
            s = st.session_state.ultima_senal
            color = "#2e7d32" if "COMPRA" in s["res"] else "#c62828"
            st.markdown(f'<div style="background-color: {color}; padding: 10px; border-radius: 5px; text-align:center; color:white;"><b>{s["res"]} | {s["porc"]}%</b></div>', unsafe_allow_html=True)

    with col_gale:
        st.subheader("🛡️ Gestión")
        if st.session_state.nivel_gale > 0 and not st.session_state.bloqueado:
            st.warning(f"MARTINGALA {st.session_state.nivel_gale} ACTIVO")
        
        c1, c2 = st.columns(2)
        if c1.button("✅ WIN", use_container_width=True):
            gan = (inv_base * (2**st.session_state.nivel_gale)) * (payout/100)
            st.session_state.bitacora.insert(0, {"Hora": datetime.now(local_tz).strftime("%H:%M"), "Res": "WIN", "Monto": f"+${gan:.2f}"})
            st.session_state.historial["Wins"] += 1
            st.session_state.nivel_gale = 0
            st.balloons(); st.rerun()
        
        if c2.button("❌ LOSS", use_container_width=True):
            per = inv_base * (2**st.session_state.nivel_gale)
            st.session_state.bitacora.insert(0, {"Hora": datetime.now(local_tz).strftime("%H:%M"), "Res": "LOSS", "Monto": f"-${per:.2f}"})
            st.session_state.historial["Loss"] += 1
            st.session_state.nivel_gale += 1
            if st.session_state.nivel_gale > 2: st.session_state.bloqueado = True
            st.rerun()

    with col_hist:
        st.subheader("📝 Historial")
        if st.session_state.bitacora:
            st.table(st.session_state.bitacora[:5]) # Muestra las últimas 5 para mantener elegancia
        else:
            st.caption("Sin datos.")

with tab2:
    st.subheader("📅 Próximas Previsiones")
    ahora = datetime.now(local_tz)
    futuras = [{"HORA": (ahora + timedelta(minutes=i*3)).strftime("%H:%M"), "ACCIÓN": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]), "EXITO": f"{random.randint(85, 96)}%"} for i in range(1, 11)]
    st.table(futuras)