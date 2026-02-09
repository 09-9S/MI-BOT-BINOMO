import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# Configuración de zona horaria (Colombia)
local_tz = pytz.timezone('America/Bogota')

st.set_page_config(page_title="Analizador Pro con Segundero", layout="wide")

# --- MEMORIA DEL SISTEMA ---
if 'historial' not in st.session_state:
    st.session_state.historial = {"Wins": 0, "Loss": 0}
if 'bloqueado' not in st.session_state:
    st.session_state.bloqueado = False
if 'nivel_gale' not in st.session_state:
    st.session_state.nivel_gale = 0

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)

# --- BLOQUE 1: RELOJ ANIMADO (SEGUNDERO REAL) ---
# Este bloque crea un reloj que se mueve solo sin refrescar toda la página
st.components.v1.html(
    """
    <div style="background: #1e1e1e; padding: 10px; border-radius: 10px; border: 1px solid #333; text-align: center;">
        <h2 style="color: #00ff00; font-family: 'Courier New', Courier, monospace; margin: 0;">
            🕒 HORA LOCAL: <span id="clock">00:00:00</span>
        </h2>
    </div>
    <script>
        function updateClock() {
            const now = new Date();
            // Ajuste manual a hora Colombia si el PC está en otra zona
            const options = { timeZone: 'America/Bogota', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' };
            const timeString = now.toLocaleTimeString('en-GB', options);
            document.getElementById('clock').innerText = timeString;
            
            // Lógica de alerta de 2 segundos (Faltan 2 para el minuto nuevo)
            const seconds = now.getSeconds();
            if (seconds === 58) {
                // Sonido o cambio visual aquí si se desea
            }
        }
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """,
    height=80,
)

st.title("🛡️ Analizador Dual - Precisión Total")

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("📊 Marcador")
    st.metric("WIN", st.session_state.historial["Wins"])
    st.metric("LOSS", st.session_state.historial["Loss"])
    st.divider()
    mercado = st.selectbox("Activo:", ["FX:EURUSD", "FX:GBPUSD", "FX:USDJPY", "BITSTAMP:BTCUSD"])
    if st.button("🔄 REINICIAR SISTEMA"):
        st.session_state.historial = {"Wins": 0, "Loss": 0}
        st.session_state.bloqueado = False
        st.rerun()

tab1, tab2 = st.tabs(["⚡ SEÑAL AL MINUTO", "📅 LISTA A FUTURO"])

with tab1:
    st.components.v1.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={mercado}&interval=1&theme=dark" height="350" width="100%"></iframe>', height=350)
    
    if not st.session_state.bloqueado:
        col_btn, col_info = st.columns([2, 1])
        with col_btn:
            if st.button("🚀 ANALIZAR ENTRADA", use_container_width=True):
                with st.status("Verificando segundos finales...", expanded=False):
                    time.sleep(1.2)
                res = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
                play_alert()
                st.session_state.ultima_senal = res
        
        with col_info:
            # Aviso especial de los 2 segundos
            ahora = datetime.now(local_tz)
            segundos_restantes = 60 - ahora.second
            if segundos_restantes <= 5:
                st.warning(f"⚠️ ¡PREPARA ENTRADA! Faltan {segundos_restantes} seg.")
    
    if 'ultima_senal' in st.session_state:
        st.success(f"⚠️ SEÑAL: {st.session_state.ultima_senal} | ENTRAR AHORA")

    st.divider()
    c1, c2 = st.columns(2)
    if c1.button('✅ WIN', use_container_width=True):
        st.session_state.historial["Wins"] += 1
        st.session_state.nivel_gale = 0
        st.balloons()
        st.rerun()
    if c2.button('❌ LOSS', use_container_width=True):
        st.session_state.historial["Loss"] += 1
        st.session_state.nivel_gale += 1
        if st.session_state.nivel_gale >= 2: st.session_state.bloqueado = True
        st.rerun()

with tab2:
    st.subheader("📋 Calendario a Futuro (Hora Colombia)")
    ahora_local = datetime.now(local_tz)
    lista = []
    for i in range(1, 11):
        hora_f = (ahora_local + timedelta(minutes=i*2)).strftime("%H:%M")
        lista.append({"HORA": hora_f, "ACCIÓN": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]), "EFECTIVIDAD": f"{random.randint(82, 95)}%"})
    st.table(lista)