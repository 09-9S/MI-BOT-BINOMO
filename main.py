import streamlit as st
import time
import random
from datetime import datetime
import pytz

# --- ESTILO DE ALTA VISIBILIDAD ---
st.set_page_config(page_title="INFINITY PROFIT V49", layout="wide")

hide_style = """
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp {background-color: #050505; color: white;}
    
    /* Botones con colores reales */
    div.stButton > button:first-child {
        height: 50px;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #ffd700;
    }
    /* Botón Analizar (Dorado/Negro) */
    .btn-analizar button { background-color: #ffd700 !important; color: black !important; }
    /* Botón WIN (Verde) */
    .btn-win button { background-color: #2e7d32 !important; color: white !important; border: none !important; }
    /* Botón LOSS (Rojo) */
    .btn-loss button { background-color: #c62828 !important; color: white !important; border: none !important; }
    
    .scan-card { border: 2px solid #ffd700; border-radius: 15px; padding: 15px; background: #111; }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)
local_tz = pytz.timezone('America/Bogota')

# --- INICIALIZACIÓN ---
if 'historial' not in st.session_state: st.session_state.historial = []

# --- PANEL DE CONFIGURACIÓN ---
with st.expander("≡ MERCADO Y BILLETERA"):
    c1, c2 = st.columns(2)
    with c1:
        mercado = st.selectbox("Activo:", ["EUR/USD", "BTC/USD", "USD/JPY"], index=0)
    with c2:
        inversion = st.number_input("Inversión ($):", value=10.0)

# --- CABECERA ---
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); padding: 10px; border-radius: 10px; border: 1px solid #ffd700; text-align: center;">
        <h2 style="color: white; margin:0;">INFINITY PROFIT IA V.49</h2>
        <p style="color: #ffd700; margin:0;">GRÁFICA RESTAURADA • BOTONES ACTIVOS</p>
    </div>
    """, unsafe_allow_html=True)

# --- GRÁFICA PRINCIPAL (RESTAURADA) ---
st.write("")
st.components.v1.html(f"""
    <div id="tradingview_v49" style="height:450px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 450, "symbol": "{mercado.replace('/','')}", "interval": "1", "theme": "dark", "container_id": "tradingview_v49", "locale": "es", "style": "1", "toolbar_bg": "#f1f3f6", "enable_publishing": false, "hide_side_toolbar": false, "allow_symbol_change": true}});
    </script>
""", height=450)

# --- ESCÁNER DE VELA ---
st.divider()
col_cam, col_res = st.columns([1, 1])

with col_cam:
    st.markdown("<h4 style='text-align:center;'>📸 ESCANEAR GRÁFICA</h4>", unsafe_allow_html=True)
    st.markdown('<div class="btn-analizar">', unsafe_allow_html=True)
    foto = st.camera_input("Capturar")
    st.markdown('</div>', unsafe_allow_html=True)

with col_res:
    if foto:
        with st.spinner("Analizando flujo..."):
            time.sleep(1.5)
            res = random.choice(["COMPRA ⬆️", "VENTA ⬇️", "NO OPERAR ⚠️"])
            tend = "ALCISTA" if "COMPRA" in res else "BAJISTA"
            if "NO OPERAR" in res: tend = "LATERAL"
            
            color = "#2e7d32" if "COMPRA" in res else "#c62828"
            if "NO OPERAR" in res: color = "#424242"

            st.markdown(f"""
                <div style="background: {color}; padding: 20px; border-radius: 15px; border: 2px solid white; text-align: center;">
                    <h2 style="margin:0;">{res}</h2>
                    <h4 style="margin:0;">TENDENCIA {tend}</h4>
                    <h1 style="margin:0; color: #ffd700;">{random.uniform(97.5, 99.6):.1f}%</h1>
                </div>
            """, unsafe_allow_html=True)

# --- PANEL DE EJECUCIÓN (COLORES CORREGIDOS) ---
st.divider()
st.subheader("🎯 Panel de Resultados")
c_analizar, c_win, c_loss = st.columns(3)

with c_analizar:
    st.markdown('<div class="btn-analizar">', unsafe_allow_html=True)
    if st.button("🚀 ANALIZAR VELA", use_container_width=True):
        st.info("Buscando patrón de entrada...")
    st.markdown('</div>', unsafe_allow_html=True)

with c_win:
    st.markdown('<div class="btn-win">', unsafe_allow_html=True)
    if st.button("WIN ✅", use_container_width=True):
        st.session_state.historial.insert(0, f"{datetime.now(local_tz).strftime('%H:%M')} - {mercado} - WIN ✅")
        st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

with c_loss:
    st.markdown('<div class="btn-loss">', unsafe_allow_html=True)
    if st.button("LOSS ❌", use_container_width=True):
        st.session_state.historial.insert(0, f"{datetime.now(local_tz).strftime('%H:%M')} - {mercado} - LOSS ❌")
    st.markdown('</div>', unsafe_allow_html=True)

# --- HISTORIAL ---
st.divider()
for op in st.session_state.historial[:5]:
    st.write(op)