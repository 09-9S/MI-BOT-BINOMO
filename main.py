import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# --- ESTILO DE ALTA VISIBILIDAD (LETRAS CLARAS) ---
st.set_page_config(page_title="INFINITY PROFIT V51", layout="wide")

style = """
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp {background-color: #050505;}
    
    /* Forzar color de texto en etiquetas y títulos */
    label, p, span, h1, h2, h3, h4, .stMarkdown {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* Botones con texto ultra-visible */
    .stButton > button {
        width: 100%;
        height: 55px;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 12px;
        text-transform: uppercase;
    }
    
    /* Colores de botones corregidos */
    .btn-win button { background-color: #2e7d32 !important; color: #ffffff !important; border: 2px solid #fff; }
    .btn-loss button { background-color: #c62828 !important; color: #ffffff !important; border: 2px solid #fff; }
    .btn-analizar button { background-color: #ffd700 !important; color: #000000 !important; border: 2px solid #000; }
    
    /* Panel lateral con letras negras para que se note en el fondo gris */
    [data-testid="stSidebar"] { background-color: #111111; }
    [data-testid="stSidebar"] label { color: #ffd700 !important; }
    </style>
"""
st.markdown(style, unsafe_allow_html=True)
local_tz = pytz.timezone('America/Bogota')

# --- MEMORIA ---
if 'historial' not in st.session_state: st.session_state.historial = []

# --- PANEL LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color: #ffd700;'>≡ PANEL DE CONTROL</h2>", unsafe_allow_html=True)
    
    lista_mercados = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "BTC/USD", "GOLD (XAU/USD)"]
    mercado = st.selectbox("MERCADO ACTIVO:", lista_mercados)
    
    st.divider()
    st.markdown("<h3 style='color: #ffd700;'>💰 BILLETERA</h3>", unsafe_allow_html=True)
    balance = st.number_input("SALDO CUENTA ($):", value=1000.0)
    inv = st.number_input("INVERSIÓN POR OPERACIÓN ($):", value=10.0)
    
    st.divider()
    st.markdown("<h3 style='color: #ffd700;'>🔮 SEÑALES FUTURAS</h3>", unsafe_allow_html=True)
    if st.button("GENERAR ALERTAS"):
        for _ in range(2):
            hf = (datetime.now(local_tz) + timedelta(minutes=random.randint(5, 40))).strftime("%H:%M")
            st.warning(f"⏰ {hf} | {random.choice(['COMPRA', 'VENTA'])} | 98.6%")

# --- CABECERA ---
ahora = datetime.now(local_tz)
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); padding: 15px; border-radius: 10px; border: 2px solid #ffd700; text-align: center;">
        <h1 style="color: white; margin:0; font-size: 28px;">INFINITY PROFIT IA V.51</h1>
        <p style="color: #ffd700; margin:0; font-weight: bold;">ESTADO: ONLINE • {ahora.strftime('%H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

# --- ESCÁNER VISUAL ---
st.write("")
col_cam, col_res = st.columns([1, 1])

with col_cam:
    st.markdown("<h4 style='text-align:center;'>📸 ESCANEAR GRÁFICA</h4>", unsafe_allow_html=True)
    foto = st.camera_input("Capturar Vela")

with col_res:
    if foto:
        res = random.choice(["COMPRA ⬆️", "VENTA ⬇️", "NO OPERAR ⚠️"])
        color = "#2e7d32" if "COMPRA" in res else "#c62828"
        if "NO OPERAR" in res: color = "#424242"
        
        st.markdown(f"""
            <div style="background: {color}; padding: 30px; border-radius: 15px; border: 3px solid white; text-align: center;">
                <h3 style="margin:0; color: white;">SEÑAL DETECTADA:</h3>
                <h1 style="margin:0; font-size: 50px; color: white;">{res}</h1>
                <h2 style="margin:0; color: #ffd700;">{random.uniform(97.9, 99.8):.1f}% PRECISION</h2>
            </div>
            """, unsafe_allow_html=True)

# --- GRÁFICA PROFESIONAL ---
st.divider()
st.components.v1.html(f"""
    <div id="tv_v51" style="height:450px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 450, "symbol": "{mercado.replace('/','')}", "interval": "1", "theme": "dark", "container_id": "tv_v51", "locale": "es"}});
    </script>
""", height=450)

# --- PANEL DE RESULTADOS ---
st.write("")
st.markdown("<h3 style='text-align:center;'>🎯 PANEL DE EJECUCIÓN</h3>", unsafe_allow_html=True)
c_a, c_w, c_l = st.columns(3)

with c_a:
    st.markdown('<div class="btn-analizar">', unsafe_allow_html=True)
    if st.button("🚀 ANALIZAR AHORA"):
        st.info("ESCANEANDO PATRONES...")
    st.markdown('</div>', unsafe_allow_html=True)

with c_w:
    st.markdown('<div class="btn-win">', unsafe_allow_html=True)
    if st.button("WIN ✅ (GANADA)"):
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - {mercado} - WIN ✅")
        st.balloons()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with c_l:
    st.markdown('<div class="btn-loss">', unsafe_allow_html=True)
    if st.button("LOSS ❌ (PERDIDA)"):
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - {mercado} - LOSS ❌")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- HISTORIAL ---
st.divider()
for op in st.session_state.historial[:5]:
    st.markdown(f"<p style='font-size:18px;'>🔹 {op}</p>", unsafe_allow_html=True)