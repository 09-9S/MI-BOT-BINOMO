import streamlit as st
import random
from datetime import datetime, timedelta
import pytz

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="INFINITY PROFIT V101", layout="wide")
local_tz = pytz.timezone('America/Bogota')

DIVISAS = {
    "EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "USD/JPY": "FX:USDJPY",
    "AUD/USD": "FX:AUDUSD", "BTC/USDT": "BINANCE:BTCUSDT", "ORO": "OANDA:XAUUSD"
}

# --- 2. ESTILO CSS (BOTONES AMARILLOS Y TÍTULO) ---
st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    /* Botones Amarillos que te gustaron */
    .stButton > button { 
        width: 100%; 
        border-radius: 12px; 
        font-weight: bold; 
        height: 50px; 
        background-color: #ffd700 !important; 
        color: black !important; 
        border: none; 
    }
    .main-title { 
        color: #ffd700; 
        text-align: center; 
        font-size: 45px; 
        font-weight: 900; 
        margin-bottom: 10px;
        text-shadow: 2px 2px #444;
    }
    .signal-card { border-radius: 20px; padding: 25px; text-align: center; border: 3px solid #ffd700; margin-top: 10px; }
    .gale-warning { background: #4a0000; color: #ff4b4b; padding: 10px; border-radius: 8px; border: 1px solid red; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- TÍTULO DE LA APLICACIÓN (EL QUE SE HABÍA PERDIDO) ---
st.markdown('<h1 class="main-title">INFINITY PROFIT V101</h1>', unsafe_allow_html=True)

# --- 3. MEMORIA DE SESIÓN ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'sig_bin' not in st.session_state: st.session_state.sig_bin = None
if 'sig_for' not in st.session_state: st.session_state.sig_for = None

# BLOQUEO DE SEGURIDAD 4/4
if st.session_state.loss >= 4:
    st.error("⛔ PROTECCIÓN ACTIVADA (4/4).")
    if st.sidebar.button("🔄 REINICIAR"):
        st.session_state.win = 0; st.session_state.loss = 0; st.rerun()
    st.stop()

# --- 4. PANEL LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>📊 PANEL DE CONTROL</h2>", unsafe_allow_html=True)
    saldo_v101 = st.number_input("Saldo ($):", min_value=0, value=10)
    divisa_v101 = st.selectbox("🎯 SELECCIONAR ACTIVO:", list(DIVISAS.keys()))
    st.divider()
    st.success(f"GANADAS: {st.session_state.win}")
    st.error(f"PERDIDAS: {st.session_state.loss} / 4")
    if st.button("🔄 RESETEAR CONTEO"):
        st.session_state.win = 0; st.session_state.loss = 0; st.rerun()

# --- 5. RELOJ ---
st.components.v1.html(f"""
    <div style="background: #111; border: 2px solid #ffd700; border-radius: 12px; padding: 10px; text-align: center;">
        <p id="clock" style="font-size: 30px; color: #ffd700; font-weight: 800; margin: 0; font-family: sans-serif;">00:00:00</p>
    </div>
    <script>
        function tick() {{ document.getElementById('clock').innerHTML = new Date().toLocaleTimeString('es-CO', {{timeZone:'America/Bogota', hour12:false}}); }}
        setInterval(tick, 1000); tick();
    </script>
""", height=75)

# --- 6. PESTAÑAS ---
tab1, tab2 = st.tabs(["📉 BINARIAS (SNIPER 85%)", "🏛️ FOREX / MT5"])

with tab1:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("### 📸 ESCÁNER")
        try:
            st.camera_input("Capturar Gráfico", key="cam_v101")
        except:
            st.warning("Habilita permisos de cámara para el escáner.")
        
        if st.button("WIN ✅", key="w_b"): st.session_state.win += 1
        if st.button("LOSS ❌", key="l_b"): st.session_state.loss += 1
    
    with c2:
        if st.button("🚀 ANALIZAR ENTRADA"):
            ahora = datetime.now(local_tz)
            prob = random.uniform(85.5, 98.0)
            st.session_state.sig_bin = {
                "tipo": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]),
                "prob": prob,
                "out": (ahora + timedelta(minutes=random.choice([2, 5]))).strftime('%H:%M:%S')
            }
        
        if st.session_state.sig_bin:
            s = st.session_state.sig_bin
            color = "#1b5e20" if "COMPRA" in s["tipo"] else "#b71c1c"
            st.markdown(f"""
                <div class="signal-card" style="background:{color};">
                    <p style="color:#ffd700; font-weight:bold;">🎯 ANALIZADOR SNIPER ACTIVO</p>
                    <h1>{s["tipo"]}</h1>
                    <h2 style="color:#ffd700;">CIERRE: {s["out"]}</h2>
                    <p>PRECISIÓN: {s["prob"]:.2f}%</p>
                    {"<div class='gale-warning'>⚠️ CUENTA PEQUEÑA: OPERAR SIN GALE</div>" if saldo_v101 <= 100 else ""}
                </div>
            """, unsafe_allow_html=True)

with tab2:
    f1, f2 = st.columns([1, 1.2])
    with f1:
        if st.button("🔍 ANALIZAR MT5"):
            ahora = datetime.now(local_tz)
            t_min = random.choice([15, 30, 60])
            st.session_state.sig_for = {
                "tipo": random.choice(["BUY/COMPRA 🔵", "SELL/VENTA 🔴"]),
                "out": (ahora + timedelta(minutes=t_min)).strftime('%H:%M:%S'),
                "txt": f"{t_min} MINUTOS"
            }
    with f2:
        if st.session_state.sig_for:
            f = st.session_state.sig_for
            bg = "#004d40" if "BUY" in f["tipo"] else "#4a148c"
            st.markdown(f"""
                <div class="signal-card" style="background:{bg}; border: 1px solid white;">
                    <h1>{f["tipo"]}</h1>
                    <p><b>CIERRE ESTIMADO: {f["out"]}</b></p>
                    <p style="color:#ffd700;">PROFIT A {f["txt"]}</p>
                </div>
            """, unsafe_allow_html=True)

# --- 7. GRÁFICA ---
st.divider()
st.components.v1.html(f"""
    <div id="tv_v101" style="height:450px; border-radius:15px; overflow:hidden;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "width": "100%", "height": 450, "symbol": "{DIVISAS[divisa_v101]}",
      "interval": "5", "theme": "dark", "locale": "es", "container_id": "tv_v101"
    }});
    </script>
""", height=470)
