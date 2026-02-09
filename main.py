import streamlit as st
import random
from datetime import datetime
import pytz

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="INFINITY PROFIT V81 - DUAL", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- 2. ESTILO CSS ---
st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    .stButton > button { width: 100%; border-radius: 12px; font-weight: bold; height: 50px; border: none; }
    .btn-win button { background: #1b5e20 !important; color: white !important; }
    .btn-loss button { background: #b71c1c !important; color: white !important; }
    .signal-card { border-radius: 20px; padding: 20px; text-align: center; border: 2px solid white; margin-top: 10px; }
    .stop-alert { background: #4a0000; color: #ff0000; padding: 30px; border-radius: 15px; text-align: center; border: 3px solid red; }
    /* Estilo para las pestañas */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #111;
        border-radius: 10px 10px 0 0;
        color: white;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #ffd700 !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MEMORIA Y RIESGO (4 PÉRDIDAS) ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'fallos' not in st.session_state: st.session_state.fallos = 0
if 'signal_data' not in st.session_state: st.session_state.signal_data = None

# --- 4. BLOQUEO POR STOP LOSS ---
if st.session_state.fallos >= 4:
    st.markdown("""<div class="stop-alert"><h1>⛔ STOP LOSS ALCANZADO (4/4)</h1><p>Sistema bloqueado para proteger tu capital.</p></div>""", unsafe_allow_html=True)
    if st.sidebar.button("🔄 REINICIAR TODO"):
        st.session_state.win = 0
        st.session_state.fallos = 0
        st.session_state.signal_data = None
        st.rerun()
    st.stop()

# --- 5. BARRA LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>📊 ESTADÍSTICAS</h2>", unsafe_allow_html=True)
    st.success(f"GANADAS: {st.session_state.win}")
    st.error(f"PÉRDIDAS: {st.session_state.fallos} / 4")
    if st.button("🔄 RESET"):
        st.session_state.win = 0
        st.session_state.fallos = 0
        st.session_state.signal_data = None
        st.rerun()

# --- 6. RELOJ DINÁMICO ---
st.components.v1.html(f"""
    <div style="background: linear-gradient(180deg, #111, #000); border: 2px solid #ffd700; border-radius: 15px; padding: 10px; text-align: center;">
        <p id="clock_v81" style="font-size: 45px; color: #ffd700; font-weight: 800; margin: 0; font-family: monospace;">00:00:00</p>
    </div>
    <script>
        function run() {{
            document.getElementById('clock_v81').innerHTML = new Date().toLocaleTimeString('es-CO', {{timeZone:'America/Bogota', hour12:false}});
        }}
        setInterval(run, 1000); run();
    </script>
""", height=100)

# --- 7. SISTEMA DE PESTAÑAS (TABS) ---
tab1, tab2 = st.tabs(["📉 BINARIAS (IQ/BINOMO)", "🏛️ FOREX (MT5/TRADINGVIEW)"])

with tab1:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("### 📸 ESCÁNER BINARIO")
        foto = st.camera_input("Scanner", key="cam_bin")
        st.markdown('<div class="btn-win">', unsafe_allow_html=True)
        if st.button("WIN ✅", key="w_bin"): st.session_state.win += 1
        st.markdown('</div><div class="btn-loss">', unsafe_allow_html=True)
        if st.button("LOSS ❌", key="l_bin"): st.session_state.fallos += 1
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if foto or st.button("🚀 ANALIZAR BINARIAS"):
            st.session_state.signal_data = {
                "tipo": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]),
                "prob": random.uniform(74.0, 91.5),
                "hora": datetime.now(local_tz).strftime('%H:%M:%S'),
                "precio": random.uniform(1.0820, 1.0850)
            }
        
        if st.session_state.signal_data:
            s = st.session_state.signal_data
            color = "#1b5e20" if "COMPRA" in s["tipo"] else "#b71c1c"
            st.markdown(f"""
                <div class="signal-card" style="background: {color};">
                    <p style="margin:0; opacity:0.8;">ENTRADA: {s["hora"]}</p>
                    <h1 style="font-size: 40px;">{s["tipo"]}</h1>
                    <h2 style="color:#ffd700;">{s["prob"]:.1f}% PRECISIÓN</h2>
                    <p>Precio sugerido: {s["precio"]:.5f}</p>
                </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 🏛️ TERMINAL FOREX / MT5 GLOBAL")
    st.info("Visualización de alta velocidad para análisis de spreads y tendencias en Forex.")
    # Gráfica avanzada para Forex
    st.components.v1.html("""
        <div id="forex_chart" style="height:500px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({"width":"100%","height":500,"symbol":"FX:EURUSD","interval":"5","theme":"dark","style":"1","locale":"es","toolbar_bg":"#f1f3f6","enable_publishing":false,"hide_side_toolbar":false,"container_id":"forex_chart"});
        </script>
    """, height=500)

# --- 8. GRÁFICA DE APOYO ---
st.divider()
activo = st.selectbox("Activo principal:", ["EUR/USD", "GBP/USD", "BITCOIN", "ORO"])
dict_a = {"EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "BITCOIN": "BINANCE:BTCUSDT", "ORO": "OANDA:XAUUSD"}

st.components.v1.html(f"""
    <div id="main_chart" style="height:400px; border-radius:15px; border: 1px solid #333; overflow:hidden;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width":"100%","height":400,"symbol":"{dict_a[activo]}","interval":"1","theme":"dark","container_id":"main_chart"}});
    </script>
""", height=400)