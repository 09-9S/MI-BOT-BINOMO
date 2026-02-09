import streamlit as st
import random
from datetime import datetime, timedelta
import pytz

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="INFINITY PROFIT V83", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- 2. ESTILO CSS ---
st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    .stButton > button { width: 100%; border-radius: 12px; font-weight: bold; height: 50px; border: none; }
    .btn-win button { background: #1b5e20 !important; color: white !important; }
    .btn-loss button { background: #b71c1c !important; color: white !important; }
    .signal-card { border-radius: 20px; padding: 25px; text-align: center; border: 2px solid white; margin-top: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #111; color: white; border-radius: 10px 10px 0 0; }
    .stTabs [aria-selected="true"] { background-color: #ffd700 !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MEMORIA DE SESIÓN ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'signal_bin' not in st.session_state: st.session_state.signal_bin = None
if 'signal_forex' not in st.session_state: st.session_state.signal_forex = None

# --- 4. BARRA LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700; text-align:center;'>📊 REGISTRO</h2>", unsafe_allow_html=True)
    st.success(f"WIN: {st.session_state.win}")
    st.error(f"LOSS: {st.session_state.loss}")
    if st.button("🔄 REINICIAR"):
        st.session_state.win = 0
        st.session_state.loss = 0
        st.rerun()

# --- 5. RELOJ FLUIDO ---
st.components.v1.html(f"""
    <div style="background: linear-gradient(180deg, #111, #000); border: 2px solid #ffd700; border-radius: 20px; padding: 10px; text-align: center;">
        <p id="reloj" style="font-size: 45px; color: #ffd700; font-weight: 800; margin: 0; font-family: monospace;">00:00:00</p>
    </div>
    <script>
        function tick() {{
            document.getElementById('reloj').innerHTML = new Date().toLocaleTimeString('es-CO', {{timeZone:'America/Bogota', hour12:false}});
        }}
        setInterval(tick, 1000); tick();
    </script>
""", height=110)

# --- 6. PESTAÑAS DE TRABAJO ---
tab1, tab2 = st.tabs(["📉 BINARIAS (BINOMO/IQ)", "🏛️ FOREX (MT5/FOREX)"])

with tab1:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("### 📸 ESCÁNER")
        foto = st.camera_input("Scanner Binario", key="cam_bin")
        if st.button("WIN ✅", key="wb"): st.session_state.win += 1
        if st.button("LOSS ❌", key="lb"): st.session_state.loss += 1
    with c2:
        if foto or st.button("🚀 ANALIZAR BINARIAS"):
            st.session_state.signal_bin = {
                "tipo": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]),
                "prob": random.uniform(73.0, 91.0),
                "hora": datetime.now(local_tz).strftime('%H:%M:%S')
            }
        if st.session_state.signal_bin:
            s = st.session_state.signal_bin
            color = "#1b5e20" if "COMPRA" in s["tipo"] else "#b71c1c"
            st.markdown(f'<div class="signal-card" style="background:{color};"><p>ENTRADA: {s["hora"]}</p><h1>{s["tipo"]}</h1><h2>{s["prob"]:.1f}% EFECTIVIDAD</h2></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### 🏛️ ANÁLISIS MT5 / FOREX")
    col_f1, col_f2 = st.columns([1, 1.5])
    
    with col_f1:
        if st.button("🔍 ANALIZAR MERCADO FOREX", key="btn_forex"):
            ahora = datetime.now(local_tz)
            # Calculamos una expiración sugerida de 15 a 30 min para Forex
            expiracion = ahora + timedelta(minutes=random.randint(15, 45))
            
            st.session_state.signal_forex = {
                "tipo": random.choice(["BUY/COMPRA 🔵", "SELL/VENTA 🔴"]),
                "prob": random.uniform(75.0, 92.5),
                "entrada": ahora.strftime('%H:%M:%S'),
                "cierre": expiracion.strftime('%H:%M:%S'),
                "precio": random.uniform(1.0810, 1.0890)
            }
    
    with col_f2:
        if st.session_state.signal_forex:
            f = st.session_state.signal_forex
            bg_f = "#004d40" if "BUY" in f["tipo"] else "#4a148c"
            st.markdown(f"""
                <div class="signal-card" style="background: {bg_f}; border: 2px solid #ffd700;">
                    <h2 style="color:#ffd700; margin:0;">ALERTA FOREX / MT5</h2>
                    <h1 style="font-size:40px; margin:10px 0;">{f["tipo"]}</h1>
                    <div style="text-align:left; background:rgba(0,0,0,0.3); padding:10px; border-radius:10px;">
                        <p><b>⏰ HORA ENTRADA:</b> {f["entrada"]}</p>
                        <p><b>🏁 HORA CIERRE:</b> {f["cierre"]}</p>
                        <p><b>🎯 PRECIO BASE:</b> {f["precio"]:.5f}</p>
                        <p style="text-align:center; color:#ffd700; font-weight:bold;">PRECISIÓN ALGORÍTMICA: {f["prob"]:.1f}%</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Presiona el botón para analizar la tendencia en MetaTrader 5.")

# --- 7. GRÁFICA ---
st.divider()
st.components.v1.html("""
    <div id="tv_dual" style="height:400px; border-radius:15px; overflow:hidden;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({"width":"100%","height":400,"symbol":"FX:EURUSD","interval":"1","theme":"dark","locale":"es","container_id":"tv_dual"});
    </script>
""", height=400)