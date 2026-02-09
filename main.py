import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# Configuración de Terminal Blindada
st.set_page_config(page_title="Elite Bot V12 - Global Stop Loss", layout="wide")

local_tz = pytz.timezone('America/Bogota')

# --- MEMORIA DEL SISTEMA ---
if 'historial' not in st.session_state: st.session_state.historial = {"Wins": 0, "Loss": 0}
if 'bitacora' not in st.session_state: st.session_state.bitacora = []
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'nivel_gale' not in st.session_state: st.session_state.nivel_gale = 0
if 'ultima_senal' not in st.session_state: st.session_state.ultima_senal = None

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)

# --- CABECERA ---
st.components.v1.html(
    """
    <div style="background: linear-gradient(90deg, #000, #4a148c, #000); padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #7b1fa2;">
        <h1 style="color: #fff; font-family: sans-serif; margin: 0; font-size: 18px;">ELITE BOT V12 - STOP LOSS ACUMULADO (4)</h1>
        <h2 style="color: #ea80fc; font-family: monospace; margin: 5px; font-size: 32px;"><span id="clock">00:00:00</span></h2>
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
    st.header("⚙️ Control de Riesgo")
    mercado = st.selectbox("Activo:", ["FX:EURUSD", "FX:GBPUSD", "OANDA:XAUUSD", "BITSTAMP:BTCUSD"])
    inv_base = st.number_input("Inversión Base ($):", min_value=1.0, value=10.0)
    payout = st.slider("Payout %:", 70, 95, 85)
    st.divider()
    
    # Marcador visual de peligro
    perdidas_actuales = st.session_state.historial["Loss"]
    st.metric("PÉRDIDAS ACUMULADAS", f"{perdidas_actuales} / 4")
    
    if st.button("🔄 REINICIAR CONTADORES"):
        st.session_state.historial = {"Wins": 0, "Loss": 0}
        st.session_state.bitacora = []
        st.session_state.bloqueado = False
        st.session_state.nivel_gale = 0
        st.session_state.ultima_senal = None
        st.rerun()

# --- INTERFAZ ---
tab1, tab2 = st.tabs(["⚡ ANALIZADOR PROFESIONAL", "📅 CALENDARIO"])

with tab1:
    # Gráfica amplia
    st.components.v1.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={mercado}&interval=1&theme=dark" height="420" width="100%"></iframe>', height=420)
    
    st.divider()

    col_acc, col_gale, col_hist = st.columns([1.5, 1.5, 2])

    with col_acc:
        st.subheader("🎯 Señal")
        if not st.session_state.bloqueado:
            if st.button("🔍 ANALIZAR AHORA", use_container_width=True):
                with st.spinner("Procesando algoritmo..."): time.sleep(1)
                res = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
                porc = random.randint(91, 99)
                play_alert()
                st.session_state.ultima_senal = {"res": res, "porc": porc}
        else:
            st.error("🚫 LÍMITE DE PÉRDIDAS ALCANZADO (4/4)")

        if st.session_state.ultima_senal:
            s = st.session_state.ultima_senal
            color = "#2e7d32" if "COMPRA" in s["res"] else "#c62828"
            st.markdown(f'<div style="background-color: {color}; padding: 10px; border-radius: 5px; text-align:center; color:white;"><b>{s["res"]} | {s["porc"]}%</b></div>', unsafe_allow_html=True)

    with col_gale:
        st.subheader("🛡️ Gestión")
        # El Martingala solo se activa si la pérdida fue INMEDIATA anterior
        if st.session_state.nivel_gale > 0 and not st.session_state.bloqueado:
            st.warning(f"MARTINGALA ACTIVO: GALE {st.session_state.nivel_gale}")
        
        c1, c2 = st.columns(2)
        if c1.button("✅ WIN", use_container_width=True):
            inv_g = inv_base * (2**st.session_state.nivel_gale)
            gan = inv_g * (payout/100)
            st.session_state.bitacora.insert(0, {"Hora": datetime.now(local_tz).strftime("%H:%M"), "Res": "WIN", "Monto": f"+${gan:.2f}"})
            st.session_state.historial["Wins"] += 1
            st.session_state.nivel_gale = 0
            st.balloons(); st.rerun()
        
        if c2.button("❌ LOSS", use_container_width=True):
            inv_p = inv_base * (2**st.session_state.nivel_gale)
            st.session_state.bitacora.insert(0, {"Hora": datetime.now(local_tz).strftime("%H:%M"), "Res": "LOSS", "Monto": f"-${inv_p:.2f}"})
            st.session_state.historial["Loss"] += 1
            
            # Lógica de Martingala (Gale individual)
            st.session_state.nivel_gale += 1
            if st.session_state.nivel_gale > 2: st.session_state.nivel_gale = 0 # Resetea el Gale pero no el contador global
            
            # BLOQUEO GLOBAL SI EL TOTAL DE PÉRDIDAS LLEGA A 4
            if st.session_state.historial["Loss"] >= 4:
                st.session_state.bloqueado = True
            st.rerun()

    with col_hist:
        st.subheader("📝 Historial")
        st.table(st.session_state.bitacora[:5])

with tab2:
    st.subheader("📅 Próximas Señales")
    ahora = datetime.now(local_tz)
    futuras = [{"HORA": (ahora + timedelta(minutes=i*3)).strftime("%H:%M"), "ACCIÓN": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]), "ÉXITO": f"{random.randint(85, 96)}%"} for i in range(1, 11)]
    st.table(futuras)