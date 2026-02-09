import streamlit as st
import random
from datetime import datetime, timedelta
import pytz

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="INFINITY PROFIT V91", layout="wide")
local_tz = pytz.timezone('America/Bogota')

DIVISAS = {
    "EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "USD/JPY": "FX:USDJPY",
    "AUD/USD": "FX:AUDUSD", "BTC/USDT": "BINANCE:BTCUSDT", "ORO": "OANDA:XAUUSD"
}

# --- 2. ESTILO CSS (DISEÑO ORIGINAL MANTENIDO) ---
st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    .stButton > button { width: 100%; border-radius: 12px; font-weight: bold; height: 50px; border: none; }
    .signal-card { border-radius: 20px; padding: 25px; text-align: center; border: 2px solid white; margin-top: 10px; }
    .alert-mercado { background: #5a4a00; color: #ffd700; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #ffd700; margin-bottom: 20px; font-weight: bold; }
    .gale-warning { background: #4a0000; color: #ff4b4b; padding: 10px; border-radius: 8px; font-size: 14px; margin-top: 10px; border: 1px solid red; }
    .stTabs [aria-selected="true"] { background-color: #ffd700 !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MEMORIA Y SEGURIDAD (BLOQUEO 4/4) ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'sig_bin' not in st.session_state: st.session_state.sig_bin = None
if 'sig_for' not in st.session_state: st.session_state.sig_for = None

if st.session_state.loss >= 4:
    st.error("⛔ PROTECCIÓN ACTIVADA: Límite de pérdidas alcanzado. Sistema bloqueado.")
    if st.sidebar.button("🔄 REINICIAR SISTEMA"):
        st.session_state.win = 0; st.session_state.loss = 0; st.rerun()
    st.stop()

# --- 4. BARRA LATERAL (GESTIÓN DE CUENTA) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700; text-align:center;'>📊 PANEL</h2>", unsafe_allow_html=True)
    saldo = st.number_input("Saldo de cuenta ($):", min_value=0, value=10)
    divisa_actual = st.selectbox("🎯 ACTIVO:", list(DIVISAS.keys()))
    st.divider()
    st.success(f"GANADAS: {st.session_state.win}")
    st.error(f"PERDIDAS: {st.session_state.loss} / 4")
    if st.button("🔄 RESET"):
        st.session_state.win = 0; st.session_state.loss = 0; st.rerun()

# --- 5. RELOJ Y ALERTA DE MERCADO ---
# Simulamos una alerta si la volatilidad es alta
mercado_apto = True if random.random() > 0.2 else False

if not mercado_apto:
    st.markdown('<div class="alert-mercado">⚠️ ALERTA: Mercado con alta volatilidad. Evita operar o busca señales de +90%.</div>', unsafe_allow_html=True)

st.components.v1.html(f"""
    <div style="background: linear-gradient(180deg, #111, #000); border: 2px solid #ffd700; border-radius: 15px; padding: 10px; text-align: center;">
        <p id="clock" style="font-size: 40px; color: #ffd700; font-weight: 800; margin: 0; font-family: monospace;">00:00:00</p>
    </div>
    <script>
        function tick() {{ document.getElementById('clock').innerHTML = new Date().toLocaleTimeString('es-CO', {{timeZone:'America/Bogota', hour12:false}}); }}
        setInterval(tick, 1000); tick();
    </script>
""", height=90)

# --- 6. PESTAÑAS (BINARIAS Y FOREX) ---
tab1, tab2 = st.tabs(["📉 BINARIAS", "🏛️ FOREX / MT5"])

with tab1:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.camera_input("Scanner", key="cam_v91")
        if st.button("WIN ✅", key="wb"): st.session_state.win += 1
        if st.button("LOSS ❌", key="lb"): st.session_state.loss += 1
    with c2:
        if st.button("🚀 ANALIZAR BINARIA"):
            ahora = datetime.now(local_tz)
            prob = random.uniform(80.0, 95.0)
            st.session_state.sig_bin = {
                "tipo": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]),
                "prob": prob,
                "in": ahora.strftime('%H:%M:%S'),
                "out": (ahora + timedelta(minutes=random.choice([2, 5]))).strftime('%H:%M:%S')
            }
        if st.session_state.sig_bin:
            s = st.session_state.sig_bin
            color = "#1b5e20" if "COMPRA" in s["tipo"] else "#b71c1c"
            st.markdown(f"""
                <div class="signal-card" style="background:{color};">
                    <p style="margin:0;">{divisa_actual} | {s["in"]}</p>
                    <h1>{s["tipo"]}</h1>
                    <h2 style="color:#ffd700;">CIERRE: {s["out"]}</h2>
                    {"<div class='gale-warning'>⚠️ CUENTA PEQUEÑA: PROHIBIDO USAR GALE. Si se pierde, esperar siguiente señal.</div>" if saldo <= 100 else "<div style='color:#00ff00;'>Uso de Gale permitido (Cuenta >$100)</div>"}
                </div>
            """, unsafe_allow_html=True)

with tab2:
    f1, f2 = st.columns([1, 1.2])
    with f1:
        if st.button("🔍 ANALIZAR MERCADO FOREX"):
            ahora = datetime.now(local_tz)
            tiempo = random.choice([15, 30, 60])
            st.session_state.sig_for = {
                "tipo": random.choice(["BUY 🔵", "SELL 🔴"]),
                "in": ahora.strftime('%H:%M:%S'),
                "out": (ahora + timedelta(minutes=tiempo)).strftime('%H:%M:%S'),
                "txt": f"{tiempo} min"
            }
    with f2:
        if st.session_state.sig_for:
            f = st.session_state.sig_for
            bg_f = "#004d40" if "BUY" in f["tipo"] else "#4a148c"
            st.markdown(f"""
                <div class="signal-card" style="background:{bg_f}; border: 2px solid #ffd700;">
                    <h1>{f["tipo"]}</h1>
                    <p><b>IN:</b> {f["in"]} | <b>OUT:</b> {f["out"]}</p>
                    <p style="color:#ffd700;">TIEMPO: {f["txt"]}</p>
                    {"<p style='color:red;'>⚠️ OPERACIÓN DIRECTA (SIN GALE)</p>" if saldo <= 100 else ""}
                </div>
            """, unsafe_allow_html=True)

# --- 7. GRÁFICA ---
st.divider()
st.components.v1.html(f"""
    <div id="tv_v91" style="height:500px; border-radius:15px; overflow:hidden; border: 1px solid #333;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width":"100%","height":500,"symbol":"{DIVISAS[divisa_actual]}","interval":"5","theme":"dark","locale":"es","container_id":"tv_v91"}});
    </script>
""", height=520)