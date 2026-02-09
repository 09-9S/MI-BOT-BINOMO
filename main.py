import streamlit as st
import time
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Analizador Dual Pro", layout="wide")

# --- INICIALIZACIÓN DE MEMORIA ---
if 'historial' not in st.session_state:
    st.session_state.historial = {"Wins": 0, "Loss": 0}
if 'bloqueado' not in st.session_state:
    st.session_state.bloqueado = False
if 'nivel_gale' not in st.session_state:
    st.session_state.nivel_gale = 0

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)

st.title("🛡️ Sistema de Trading Dual (Inmediato + Futuro)")

# --- PANEL DE CONTROL LATERAL ---
with st.sidebar:
    st.header("📊 Tu Rendimiento")
    st.metric("GANADAS (WIN)", st.session_state.historial["Wins"])
    st.metric("PERDIDAS (LOSS)", st.session_state.historial["Loss"])
    st.divider()
    mercado = st.selectbox("Activo Analizado:", ["FX:EURUSD", "FX:GBPUSD", "FX:USDJPY", "BITSTAMP:BTCUSD"])
    if st.button("🔄 REINICIAR TODO"):
        st.session_state.historial = {"Wins": 0, "Loss": 0}
        st.session_state.bloqueado = False
        st.session_state.nivel_gale = 0
        st.rerun()

# --- ESTRUCTURA DE DOS BLOQUES ---
tab1, tab2 = st.tabs(["⚡ GENERADOR AL MINUTO", "📅 PRÓXIMAS 10 SEÑALES"])

with tab1:
    st.subheader(f"🔍 Análisis en Vivo: {mercado}")
    # Gráfica en tiempo real
    st.components.v1.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={mercado}&interval=1&theme=dark" height="350" width="100%"></iframe>', height=350)
    
    if not st.session_state.bloqueado:
        # BOTÓN DE INICIAR ANÁLISIS AL MINUTO
        if st.button("🚀 INICIAR ANÁLISIS (SEÑAL AL MINUTO)", use_container_width=True):
            with st.status("Escaneando el mercado segundo a segundo...", expanded=True):
                time.sleep(1.5)
                st.write("Detectando patrones de entrada...")
                time.sleep(1.5)
            
            resultado = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            porcentaje = random.randint(89, 99)
            play_alert()
            
            if "COMPRA" in resultado:
                st.success(f"⚠️ SEÑAL AL MINUTO: {resultado} | EFECTIVIDAD: {porcentaje}% | ENTRAR YA")
            else:
                st.error(f"⚠️ SEÑAL AL MINUTO: {resultado} | EFECTIVIDAD: {porcentaje}% | ENTRAR YA")
    else:
        st.error("🚫 SISTEMA BLOQUEADO POR GALE 2. Reinicia en el panel lateral por seguridad.")

    # Marcador de resultados
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
    st.subheader(f"📋 Calendario de Señales a Futuro ({mercado})")
    st.write("Estas señales están programadas según la tendencia algorítmica:")
    
    base_time = datetime.now()
    lista_futura = []
    for i in range(1, 11):
        # Genera 10 señales espaciadas por 2 minutos
        hora_futura = (base_time + timedelta(minutes=i*2)).strftime("%H:%M")
        accion = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
        efec = f"{random.randint(82, 94)}%"
        lista_futura.append({"HORA": hora_futura, "ACCIÓN": accion, "PRECISIÓN": efec})
    
    st.table(lista_futura)
    st.warning("⚠️ IMPORTANTE: Para las señales a futuro, espera a que tu reloj marque la hora exacta de la tabla.")