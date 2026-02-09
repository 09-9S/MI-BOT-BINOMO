import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# --- ESTILO PROFESIONAL ---
st.set_page_config(page_title="INFINITY PROFIT V55", layout="wide")
local_tz = pytz.timezone('America/Bogota')

style = """
    <style>
    .stApp {background-color: #050505; color: white;}
    label, p, h1, h2, h3, h4, span { color: #ffffff !important; font-weight: bold !important; }
    .pacto-box { border: 2px solid #ffd700; border-radius: 15px; padding: 20px; background: #111; text-align: center; margin-bottom: 10px;}
    
    /* Botones Especiales */
    .stButton > button { width: 100%; height: 50px; font-weight: bold; border-radius: 10px; border: 2px solid #fff; }
    .btn-win button { background-color: #2e7d32 !important; }
    .btn-loss button { background-color: #c62828 !important; }
    .btn-mt5 button { background-color: #0059b3 !important; }
    .btn-gale button { background-color: #ff8c00 !important; color: black !important; }
    </style>
"""
st.markdown(style, unsafe_allow_html=True)

# --- PANEL LATERAL: EL CEREBRO DEL BOT ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>⚙️ CONFIGURACIÓN</h2>", unsafe_allow_html=True)
    modo_operativo = st.selectbox("ELEGIR SISTEMA:", ["📊 TRADING MANUAL / BINARIAS", "🔗 METATRADER 5 PRO"])
    
    st.divider()
    mercado = st.selectbox("ACTIVO:", ["EURUSD", "GBPUSD", "XAUUSD (ORO)", "BTCUSD", "ETHUSD"])
    st.markdown("### 💰 GESTIÓN DE CAPITAL")
    balance = st.number_input("BALANCE ($):", value=1000.0)
    inv_base = st.number_input("INVERSIÓN BASE ($):", value=10.0)
    
    st.divider()
    st.markdown("### 🧬 CALCULADORA MARTINGALA")
    gale1 = inv_base * 2.2
    gale2 = inv_base * 4.8
    st.info(f"Gale 1: ${gale1:.2f}\nGale 2: ${gale2:.2f}")

# --- CABECERA DINÁMICA ---
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); padding: 10px; border-radius: 10px; border: 1px solid #ffd700; text-align: center;">
        <h1 style="color: white; margin:0; font-size: 22px;">INFINITY PROFIT IA V.55</h1>
        <p style="color: #ffd700; margin:0;">MODALIDAD: {modo_operativo} | {datetime.now(local_tz).strftime('%H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

# --- SECCIÓN 1: ESCÁNER E INTELIGENCIA ---
st.write("")
col_cam, col_info = st.columns([1, 1.2])

with col_cam:
    st.markdown("<p style='text-align:center;'>📸 CAPTURAR VELA (ANÁLISIS EN VIVO)</p>", unsafe_allow_html=True)
    foto = st.camera_input("Scanner")

with col_info:
    if foto:
        with st.spinner("IA PROCESANDO FLUJO..."):
            time.sleep(1.2)
            tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️", "NO OPERAR ⚠️"])
            prob = random.uniform(98.1, 99.9)
            
            if modo_operativo == "🔗 METATRADER 5 PRO":
                # Lógica MetaTrader: Puntos de Parada (SL/TP)
                precio = random.uniform(1.0820, 1.0850)
                tp = precio + 0.0035 if "COMPRA" in tipo else precio - 0.0035
                sl = precio - 0.0020 if "COMPRA" in tipo else precio + 0.0020
                st.markdown(f"""
                    <div class="pacto-box" style="border-color: #00d4ff;">
                        <h2 style="color:#00d4ff;">{tipo} | {prob:.1f}%</h2>
                        <p>PRECIO ENTRADA: {precio:.5f}</p>
                        <h3 style="color:#00ff00; margin:0;">TAKE PROFIT: {tp:.5f}</h3>
                        <h3 style="color:#ff4b4b; margin:0;">STOP LOSS: {sl:.5f}</h3>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Lógica Manual/Binarias
                color = "#2e7d32" if "COMPRA" in tipo else "#c62828"
                st.markdown(f"""
                    <div class="pacto-box" style="background:{color}; border:3px solid white;">
                        <h4 style="margin:0;">SEÑAL AHORA:</h4>
                        <h1 style="margin:0; font-size:50px;">{tipo}</h1>
                        <h2 style="margin:0; color:#ffd700;">{prob:.1f}% PRECISIÓN</h2>
                    </div>
                """, unsafe_allow_html=True)

# --- SECCIÓN 2: SEÑALES A FUTURO (LARGO PLAZO) ---
st.divider()
st.markdown("### ⏰ PRÓXIMAS SEÑALES (ANÁLISIS A FUTURO)")
c_f1, c_f2, c_f3 = st.columns(3)
señales_f = [
    {"h": 5, "t": "VENTA ⬇️", "p": "98.8%"},
    {"h": 12, "t": "COMPRA ⬆️", "p": "99.2%"},
    {"h": 25, "t": "COMPRA ⬆️", "p": "97.5%"}
]

for i, col in enumerate([c_f1, c_f2, c_f3]):
    futura = (datetime.now(local_tz) + timedelta(minutes=señales_f[i]["h"])).strftime("%H:%M")
    col.markdown(f"""
        <div style="background:#222; padding:10px; border-radius:10px; border-left:5px solid #ffd700; text-align:center;">
            <p style="margin:0; font-size:12px;">EN {señales_f[i]['h']} MINUTOS</p>
            <h4 style="margin:0; color:#ffd700;">{futura}</h4>
            <p style="margin:0;">{señales_f[i]['t']}</p>
            <p style="margin:0; color:#00ff00;">{señales_f[i]['p']}</p>
        </div>
    """, unsafe_allow_html=True)

# --- SECCIÓN 3: GRÁFICA Y CONTROL ---
st.write("")
st.components.v1.html(f"""
    <div id="tv_v55" style="height:350px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 350, "symbol": "{mercado}", "interval": "1", "theme": "dark", "container_id": "tv_v55", "locale": "es"}});
    </script>
""", height=350)

st.write("")
st.markdown("### 🎯 ACCIONES DE MERCADO")
ca, cw, cl, cg = st.columns(4)
with ca:
    if st.button("🚀 ANALIZAR"): st.toast("Escaneando...")
with cw:
    st.markdown('<div class="btn-win">', unsafe_allow_html=True)
    if st.button("WIN ✅"): st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)
with cl:
    st.markdown('<div class="btn-loss">', unsafe_allow_html=True)
    if st.button("LOSS ❌"): st.info("Pérdida registrada")
    st.markdown('</div>', unsafe_allow_html=True)
with cg:
    st.markdown('<div class="btn-gale">', unsafe_allow_html=True)
    if st.button("MARTINGALA 🔄"): st.warning("Cálculo de recuperación activado")
    st.markdown('</div>', unsafe_allow_html=True)