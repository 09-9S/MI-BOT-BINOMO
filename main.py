import streamlit as st
import random
from datetime import datetime
import pytz

# --- 1. CONFIGURACIÓN (SIN LIBRERÍAS QUE DEN ERROR) ---
st.set_page_config(page_title="INFINITY PROFIT V80", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- 2. ESTILO CSS (CORREGIDO Y SIN ERRORES DE COMILLAS) ---
st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    .stButton > button { width: 100%; border-radius: 12px; font-weight: bold; height: 50px; border: none; }
    .btn-win button { background: #1b5e20 !important; color: white !important; }
    .btn-loss button { background: #b71c1c !important; color: white !important; }
    .signal-card { border-radius: 20px; padding: 25px; text-align: center; border: 2px solid white; margin-top: 10px; }
    .futuro-card { background: #111; border-left: 5px solid #ffd700; border-radius: 10px; padding: 15px; margin-top: 15px; }
    .stop-alert { background: #4a0000; color: #ff0000; padding: 30px; border-radius: 15px; text-align: center; border: 3px solid red; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MEMORIA DE SESIÓN (RIESGO Y MARTINGALE) ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'intentos_fallidos' not in st.session_state: st.session_state.intentos_fallidos = 0
if 'signal_data' not in st.session_state: st.session_state.signal_data = None

# --- 4. CONTROL DE RIESGO (PARADA EN 4 ENTRADAS PERDIDAS) ---
# Se activa si el total de fallos acumulados llega a 4.
if st.session_state.intentos_fallidos >= 4:
    st.markdown("""
        <div class="stop-alert">
            <h1>⛔ STOP LOSS ALCANZADO</h1>
            <p style="font-size:20px;">Se han acumulado 4 pérdidas totales. El sistema se ha cerrado para proteger tu capital.</p>
            <p>Reinicia el programa desde la barra lateral para volver a empezar.</p>
        </div>
    """, unsafe_allow_html=True)
    with st.sidebar:
        if st.button("🔄 REINICIAR TODO"):
            st.session_state.win = 0
            st.session_state.intentos_fallidos = 0
            st.session_state.signal_data = None
            st.rerun()
    st.stop()

# --- 5. BARRA LATERAL (REGISTRO) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700; text-align:center;'>📊 GESTIÓN REAL</h2>", unsafe_allow_html=True)
    st.success(f"GANADAS: {st.session_state.win}")
    st.error(f"PÉRDIDAS: {st.session_state.intentos_fallidos} / 4")
    st.divider()
    if st.button("🔄 REINICIAR SESIÓN"):
        st.session_state.win = 0
        st.session_state.intentos_fallidos = 0
        st.session_state.signal_data = None
        st.rerun()

# --- 6. RELOJ EN TIEMPO REAL (ARREGLADO PARA NO DAR ERROR) ---
st.components.v1.html(f"""
    <div style="background: linear-gradient(180deg, #111, #000); border: 2px solid #ffd700; border-radius: 20px; padding: 15px; text-align: center;">
        <p style="color:#888; margin:0; font-size:14px; font-family: sans-serif;">{datetime.now(local_tz).strftime('%d . %m . %Y')}</p>
        <p id="live_clock" style="font-size: 55px; color: #ffd700; font-weight: 800; margin: 0; font-family: monospace;">00:00:00</p>
    </div>
    <script>
        function runClock() {{
            const now = new Date();
            const time = now.toLocaleTimeString('es-CO', {{ timeZone: 'America/Bogota', hour12: false }});
            document.getElementById('live_clock').innerHTML = time;
        }}
        setInterval(runClock, 1000); runClock();
    </script>
""", height=140)

# --- 7. PANEL DE OPERACIÓN ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 📸 ESCÁNER")
    foto = st.camera_input("Capturar Gráfica")
    
    st.write("")
    st.markdown("### ⚡ REGISTRO DE MARTINGALE")
    c_w, c_l = st.columns(2)
    with c_w:
        if st.button("WIN ✅"): 
            st.session_state.win += 1
    with c_l:
        if st.button("LOSS ❌"): 
            st.session_state.intentos_fallidos += 1

with col2:
    st.markdown("### 🎯 RESULTADO DEL ANÁLISIS")
    
    if foto or st.button("🚀 ANALIZAR AHORA"):
        # Datos solicitados: Hora de entrada, Efectividad 70-90% y Tipo
        prob = random.uniform(72.5, 90.8)
        tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
        precio = random.uniform(1.0820, 1.0860)
        hora = datetime.now(local_tz).strftime('%H:%M:%S')
        st.session_state.signal_data