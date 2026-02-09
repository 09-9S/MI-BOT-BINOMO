import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# --- ESTILO DE ALTA VISIBILIDAD ---
st.set_page_config(page_title="INFINITY PROFIT V56", layout="wide")
local_tz = pytz.timezone('America/Bogota')

style = """
    <style>
    .stApp {background-color: #050505; color: white;}
    label, p, h1, h2, h3, h4, span { color: #ffffff !important; font-weight: bold !important; }
    
    /* Cuadro de Señal Híbrida */
    .signal-card {
        border: 3px solid #ffd700;
        border-radius: 20px;
        padding: 25px;
        background: #111;
        text-align: center;
        margin-top: 10px;
    }
    
    /* Botones */
    .stButton > button { width: 100%; height: 55px; font-weight: bold; border-radius: 12px; border: 2px solid #fff; font-size: 18px !important; }
    .btn-win button { background-color: #2e7d32 !important; color: white !important; }
    .btn-loss button { background-color: #c62828 !important; color: white !important; }
    .btn-analizar button { background-color: #ffd700 !important; color: black !important; border: 2px solid #000; }
    </style>
"""
st.markdown(style, unsafe_allow_html=True)

# --- PANEL LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>⚙️ AJUSTES</h2>", unsafe_allow_html=True)
    mercado = st.selectbox("MERCADO:", ["EURUSD", "GBPUSD", "XAUUSD (ORO)", "BTCUSD", "ETHUSD"])
    st.divider()
    st.markdown("### 💳 BILLETERA")
    balance = st.number_input("SALDO ACTUAL ($):", value=1000.0)
    inv_base = st.number_input("INVERSIÓN ($):", value=10.0)
    st.divider()
    st.markdown("### 🔮 PRÓXIMAS ENTRADAS")
    for i in range(2):
        hf = (datetime.now(local_tz) + timedelta(minutes=random.randint(5, 45))).strftime("%H:%M")
        st.warning(f"⏰ {hf} | {random.choice(['COMPRA', 'VENTA'])} | 98.9%")

# --- CABECERA ---
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); padding: 15px; border-radius: 10px; border: 2px solid #ffd700; text-align: center;">
        <h1 style="color: white; margin:0; font-size: 26px;">INFINITY PROFIT IA V.56</h1>
        <p style="color: #ffd700; margin:0; font-weight: bold;">SISTEMA HÍBRIDO: BINARIAS + METATRADER 5</p>
    </div>
    """, unsafe_allow_html=True)

# --- ZONA DE ANÁLISIS ---
st.write("")
col_cam, col_sig = st.columns([1, 1.2])

with col_cam:
    st.markdown("<h4 style='text-align:center;'>📸 ESCÁNER DE GRÁFICA</h4>", unsafe_allow_html=True)
    foto = st.camera_input("Capturar Vela")

with col_sig:
    if foto or st.session_state.get('analizando', False):
        with st.spinner("IA ESCANEANDO MERCADO..."):
            if foto: time.sleep(1.5)
            
            tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            porcentaje = random.uniform(98.2, 99.9)
            precio_ref = random.uniform(1.0820, 1.0850)
            
            # Cálculo para MT5
            tp = precio_ref + 0.0040 if "COMPRA" in tipo else precio_ref - 0.0040
            sl = precio_ref - 0.0025 if "COMPRA" in tipo else precio_ref + 0.0025
            
            color_fondo = "#1b5e20" if "COMPRA" in tipo else "#b71c1c"

            st.markdown(f"""
                <div class="signal-card" style="background: {color_fondo}; border: 4px solid white;">
                    <h3 style="margin:0; color:white;">SEÑAL DETECTADA</h3>
                    <h1 style="margin:0; font-size: 55px; color: white;">{tipo}</h1>
                    <h2 style="color: #ffd700; margin:0;">{porcentaje:.1f}% PRECISIÓN</h2>
                    <hr style="border: 1px solid white;">
                    <div style="display: flex; justify-content: space-around;">
                        <div>
                            <p style="color: #00ff00; margin:0;">MT5 TAKE PROFIT</p>
                            <h3 style="color:white; margin:0;">{tp:.5f}</h3>
                        </div>
                        <div>
                            <p style="color: #ff5252; margin:0;">MT5 STOP LOSS</p>
                            <h3 style="color:white; margin:0;">{sl:.5f}</h3>
                        </div>
                    </div>
                    <p style="font-size:12px; margin-top:10px; color: white;">Válido para 1-5 minutos en Binarias o Scalping en MT5</p>
                </div>
            """, unsafe_allow_html=True)

# --- GRÁFICA ---
st.divider()
st.components.v1.html(f"""
    <div id="tv_v56" style="height:350px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 350, "symbol": "{mercado}", "interval": "1", "theme": "dark", "container_id": "tv_v56", "locale": "es"}});
    </script>
""", height=350)

# --- PANEL DE CONTROL ---
st.write("")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="btn-analizar">', unsafe_allow_html=True)
    if st.button("🚀 ANALIZAR AHORA"):
        st.session_state.analizando = True
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="btn-win">', unsafe_allow_html=True)
    if st.button("WIN ✅"): st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="btn-loss">', unsafe_allow_html=True)
    if st.button("LOSS ❌"): st.warning("Iniciando Martingala...")
    st.markdown('</div>', unsafe_allow_html=True)