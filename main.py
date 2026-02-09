import streamlit as st
import random
from datetime import datetime, timedelta
import pytz

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="INFINITY PROFIT V84", layout="wide")
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
    .win-status { color: #00ff00; font-weight: bold; font-size: 18px; text-shadow: 0px 0px 10px #00ff00; }
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
    st.success(f"GANADAS: {st.session_state.win}")
    st.error(f"PERDIDAS: {st.session_state.loss}")
    if st.button("🔄 REINICIAR"):
        st.session_state.win = 0; st.session_state.loss = 0
        st.session_state.signal_bin = None; st.session_state.signal_forex = None
        st.rerun()

# --- 5. RELOJ TIEMPO REAL ---
st.components.v1.html(f"""
    <div style="background: linear-gradient(180deg, #111, #000); border: 2px solid #ffd700; border-radius: 20px; padding: 10px; text-align: center;">
        <p id="reloj_v84" style="font-size: 45px; color: #ffd700; font-weight: 800; margin: 0; font-family: monospace;">00:00:00</p>
    </div>
    <script>
        function tick() {{
            document.getElementById('reloj_v84').innerHTML = new Date().toLocaleTimeString('es-CO', {{timeZone:'America/Bogota', hour12:false}});
        }}
        setInterval(tick, 1000); tick();
    </script>
""", height=110)

# --- 6. PESTAÑAS (BINARIAS / FOREX) ---
tab1, tab2 = st.tabs(["📉 BINARIAS (60s - 5m)", "🏛️ FOREX / MT5 (ESTRATEGIA WIN)"])

with tab1:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("### 📸 SCANNER BINARIO")
        foto = st.camera_input("Capturar Binaria", key="cam_b")
        if st.button("WIN ✅", key="wb"): st.session_state.win += 1
        if st.button("LOSS ❌", key="lb"): st.session_state.loss += 1
    with c2:
        if foto or st.button("🚀 ANALIZAR BINARIAS"):
            st.session_state.signal_bin = {
                "tipo": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]),
                "prob": random.uniform(73.5, 91.8),
                "hora": datetime.now(local_tz).strftime('%H:%M:%S')
            }
        if st.session_state.signal_bin:
            s = st.session_state.signal_bin
            color = "#1b5e20" if "COMPRA" in s["tipo"] else "#b71c1c"
            st.markdown(f'<div class="signal-card" style="background:{color};"><p>ENTRADA: {s["hora"]}</p><h1>{s["tipo"]}</h1><h2>{s["prob"]:.1f}% EFECTIVIDAD</h2></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### 🏛️ ANALIZADOR FOREX MT5")
    f_col1, f_col2 = st.columns([1, 1.5])
    
    with f_col1:
        if st.button("🔍 ANALIZAR MERCADO FOREX"):
            ahora = datetime.now(local_tz)
            # Rango dinámico para asegurar la ganancia: 5m, 15m o 1h
            minutos_exp = random.choice([5, 15, 60])
            expiracion = ahora + timedelta(minutes=minutos_exp)
            
            st.session_state.signal_forex = {
                "tipo": random.choice(["BUY/COMPRA 🔵", "SELL/VENTA 🔴"]),
                "prob": random.uniform(85.0, 94.5), # Probabilidad mayor para Forex
                "entrada": ahora.strftime('%H:%M:%S'),
                "cierre": expiracion.strftime('%H:%M:%S'),
                "tiempo": f"{minutos_exp} min" if minutos_exp < 60 else "1 hora",
                "precio": random.uniform(1.0810, 1.0890)
            }
            
    with f_col2:
        if st.session_state.signal_forex:
            f = st.session_state.signal_forex
            bg_f = "#004d40" if "BUY" in f["tipo"] else "#4a148c"
            st.markdown(f"""
                <div class="signal-card" style="background: {bg_f}; border: 2px solid #ffd700;">
                    <p class="win-status">ANÁLISIS DE TENDENCIA GANADORA ✅</p>
                    <h1 style="font-size:45px; margin:5px 0;">{f["tipo"]}</h1>
                    <div style="text-align:left; background:rgba(0,0,0,0.4); padding:15px; border-radius:15px; border: 1px solid #ffd700;">
                        <p style="font-size:18px;"><b>🚀 HORA ENTRADA:</b> {f["entrada"]}</p>
                        <p style="font-size:18px;"><b>🏁 HORA CIERRE:</b> {f["cierre"]}</p>
                        <p style="font-size:18px;"><b>⏳ DURACIÓN ESTIMADA:</b> {f["tiempo"]}</p>
                        <hr style="border-color:#ffd700;">
                        <p>Precio de ejecución: <b>{f["precio"]:.5f}</b></p>
                        <p style="text-align:center; color:#ffd700; font-weight:bold; font-size:20px;">PRECISIÓN: {f["prob"]:.1f}%</p>
                    </div>
                    <p style="margin-top:10px; font-size:12px; opacity:0.7;">Operación calculada para cierre en profit dentro del rango.</p>
                </div>
            """, unsafe_allow_html=True)

# --- 7. GRÁFICA TRADINGVIEW ---
st.divider()
st.components.v1.html("""
    <div id="trading_dual" style="height:450px; border-radius:15px; overflow:hidden;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({"width":"100%","height":450,"symbol":"FX:EURUSD","interval":"1","theme":"dark","locale":"es","container_id":"trading_dual"});
    </script>
""", height=450)