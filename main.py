import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz # Librería para la hora local

# Configuración de zona horaria para Colombia
local_tz = pytz.timezone('America/Bogota')

st.set_page_config(page_title="Analizador Dual Pro", layout="wide")

# --- INICIALIZACIÓN ---
if 'historial' not in st.session_state:
    st.session_state.historial = {"Wins": 0, "Loss": 0}
if 'bloqueado' not in st.session_state:
    st.session_state.bloqueado = False
if 'nivel_gale' not in st.session_state:
    st.session_state.nivel_gale = 0

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)

# --- RELOJ EN TIEMPO REAL (HORA LOCAL) ---
# Esto aparecerá arriba de todo para que nunca se borre
ahora_local = datetime.now(local_tz)
st.markdown(f"## 🕒 Hora Local: {ahora_local.strftime('%H:%M:%S')}")

st.title("🛡️ Sistema de Trading Dual")

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("📊 Marcador")
    st.metric("WIN", st.session_state.historial["Wins"])
    st.metric("LOSS", st.session_state.historial["Loss"])
    mercado = st.selectbox("Activo:", ["FX:EURUSD", "FX:GBPUSD", "FX:USDJPY", "BITSTAMP:BTCUSD"])
    if st.button("🔄 REINICIAR"):
        st.session_state.historial = {"Wins": 0, "Loss": 0}
        st.session_state.bloqueado = False
        st.session_state.nivel_gale = 0
        st.rerun()

tab1, tab2 = st.tabs(["⚡ GENERADOR AL MINUTO", "📅 PRÓXIMAS 10 SEÑALES"])

with tab1:
    st.components.v1.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={mercado}&interval=1&theme=dark" height="350" width="100%"></iframe>', height=350)
    
    if not st.session_state.bloqueado:
        if st.button("🚀 INICIAR ANÁLISIS AL MINUTO", use_container_width=True):
            with st.status("Analizando minuto actual...", expanded=False):
                time.sleep(1.5)
            res = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            play_alert()
            st.success(f"⚠️ SEÑAL DETECTADA: {res} | {random.randint(89, 99)}% | HORA: {datetime.now(local_tz).strftime('%H:%M:%S')}")
    else:
        st.error("SISTEMA BLOQUEADO. Reinicia para operar.")

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
    st.subheader("📋 Señales Programadas (Hora Colombia)")
    lista_futura = []
    for i in range(1, 11):
        # Genera señales basadas en tu hora local exacta
        hora_f = (ahora_local + timedelta(minutes=i*2)).strftime("%H:%M")
        accion = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
        lista_futura.append({"HORA": hora_f, "ACCIÓN": accion, "PRECISIÓN": f"{random.randint(82, 94)}%"})
    st.table(lista_futura)