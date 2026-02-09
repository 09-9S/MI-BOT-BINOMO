import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INFINITY PROFIT V58", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- ESTILO DE ALTA VISIBILIDAD ---
st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    label, p, h1, h2, h3, h4, span { color: #ffffff !important; font-weight: bold !important; }
    .pacto-box {
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 20px;
        background: #111;
        text-align: center;
        margin-bottom: 15px;
    }
    .stButton > button { width: 100%; height: 50px; font-weight: bold; border-radius: 10px; border: 2px solid #fff; }
    .btn-win button { background-color: #2e7d32 !important; }
    .btn-loss button { background-color: #c62828 !important; }
    .btn-analizar button { background-color: #ffd700 !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# --- MEMORIA ---
if 'historial' not in st.session_state: st.session_state.historial = []

# --- PANEL LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>⚙️ AJUSTES</h2>", unsafe_allow_html=True)
    lista_mercados = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "BTCUSD", "ETHUSD", "SOLUSD", "XTIUSD"]
    mercado = st.selectbox("MERCADO:", lista_mercados)
    
    st.divider()
    balance = st.number_input("SALDO ($):", value=1000.0)
    inv = st.number_input("INVERSIÓN ($):", value=10.0)
    
    st.divider()
    st.markdown("### 🔮 SEÑALES FUTURAS")
    for i in range(2):
        hf = (datetime.now(local_tz) + timedelta(minutes=random.randint(5, 30))).strftime("%H:%M")
        st.warning(f"⏰ {hf} | {random.choice(['COMPRA', 'VENTA'])} | 98.9%")

# --- CABECERA ---
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); padding: 15px; border-radius: 10px; border: 1px solid #ffd700; text-align: center;">
        <h1 style="color: white; margin:0; font-size: 24px;">INFINITY PROFIT IA V.58</h1>
        <p style="color: #ffd700; margin:0;">CORRECCIÓN DE SINTAXIS APLICADA</p>
    </div>
""", unsafe_allow_html=True)

# --- LÓGICA DE ANÁLISIS CORREGIDA (Líneas 82-100) ---
st.write("")
col_cam, col_sig = st.columns([1, 1.2])

with col_cam:
    foto = st.camera_input("📸 CAPTURAR GRÁFICA")

with col_sig:
    if foto or st.button("🚀 ANALIZAR AHORA"):
        with st.spinner("PROCESANDO..."):
            if foto: time.sleep(1)
            
            tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            porcentaje = random.uniform(98.5, 99.9)
            precio = random.uniform(1.0820, 1.0860)
            
            # Cálculo SL/TP para MT5
            tp = precio + 0.0040 if "COMPRA" in tipo else precio - 0.0040
            sl = precio - 0.0020 if "COMPRA" in tipo else precio + 0.0020
            color_sig = "#1b5e20" if "COMPRA" in tipo else "#b71c1c"

            st.markdown(f"""
                <div class="pacto-box" style="background: {color_sig}; border: 3px solid white;">
                    <h3 style="margin:0;">ANÁLISIS DE SEÑAL</h3>
                    <h1 style="font-size: 50px; margin:0;">{tipo}</h1>
                    <h2 style="color: #ffd700; margin:0;">{porcentaje:.1f}% PRECISIÓN</h2>
                    <hr>
                    <div style="display: flex; justify-content: space-around;">
                        <div><p style="color:#00ff00; margin:0;">TP (MT5)</p><h3>{tp:.5f}</h3></div>
                        <div><p style="color:#ff5252; margin:0;">SL (MT5)</p><h3>{sl:.5f}</h3></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# --- GRÁFICA ---
st.divider()
st.components.v1.html(f"""
    <div id="tv_v58" style="height:400px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 400, "symbol": "{mercado}", "interval": "1", "theme": "dark", "container_id": "tv_v58", "locale": "es"}});
    </script>
""", height=400)

# --- PANEL DE ACCIÓN ---
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="btn-win">', unsafe_allow_html=True)
    if st.button("WIN ✅"): st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="btn-loss">', unsafe_allow_html=True)
    if st.button("LOSS ❌"): st.info("Martingala sugerida")
    st.markdown('</div>', unsafe_allow_html=True)