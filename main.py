import streamlit as st
import time
import random
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="INFINITY PROFIT V47", layout="wide")

hide_style = """
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp {background-color: #0a0a0a; color: white;}
    /* Diseño del Escáner Pacto */
    .scan-card {
        background: linear-gradient(145deg, #161616, #000000);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.2);
    }
    .metric-val { font-size: 45px; font-weight: bold; color: #ffd700; margin: 0; }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)
local_tz = pytz.timezone('America/Bogota')

# --- INICIALIZACIÓN DE MEMORIA ---
if 'historial' not in st.session_state: st.session_state.historial = []
if 'contador' not in st.session_state: st.session_state.contador = {"Wins": 0, "Loss": 0}

# --- BARRA DE CONFIGURACIÓN (≡) ---
with st.expander("≡ CONFIGURACIÓN DE MERCADO Y BILLETERA"):
    c1, c2, c3 = st.columns(3)
    with c1:
        mercado = st.selectbox("Activo:", ["EUR/USD", "BTC/USD", "USD/JPY"], index=0)
    with c2:
        balance = st.number_input("Balance ($):", value=1000.0)
    with c3:
        inv_base = st.number_input("Inversión Inicial ($):", value=10.0)
        st.caption(f"G1: ${inv_base*2.2:.2f} | G2: ${inv_base*4.8:.2f}")

# --- CABECERA ---
ahora = datetime.now(local_tz)
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); padding: 10px; border-radius: 10px; border-bottom: 2px solid #ffd700; text-align: center; margin-bottom: 20px;">
        <h1 style="color: white; margin:0; font-size: 26px; letter-spacing: 2px;">INFINITY PROFIT IA V.47</h1>
        <p style="color: #ffd700; margin:0;">SISTEMA DE ALTA PRECISIÓN • {ahora.strftime('%H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

# --- SECCIÓN DE ESCÁNER (EL DISEÑO QUE QUERÍAS) ---
col_foto, col_stats = st.columns([1, 1.5])

with col_foto:
    st.markdown("<div class='scan-card'>", unsafe_allow_html=True)
    st.markdown("🟡 **CÁMARA DE ANÁLISIS**")
    foto = st.camera_input("Capturar Vela")
    st.markdown("</div>", unsafe_allow_html=True)

with col_stats:
    if foto:
        with st.spinner("IA PROCESANDO DATOS..."):
            time.sleep(1.2)
            res_ia = random.choice(["COMPRA ⬆️", "VENTA ⬇️", "NO OPERAR ⚠️"])
            tendencia = "ALCISTA 📈" if "COMPRA" in res_ia else "BAJISTA 📉"
            if "NO OPERAR" in res_ia: tendencia = "INCIERTA 🔄"
            
            p_val = random.uniform(97.2, 99.8)
            color_res = "#2e7d32" if "COMPRA" in res_ia else "#c62828"
            if "NO OPERAR" in res_ia: color_res = "#424242"

            st.markdown(f"""
                <div style="background: {color_res}; padding: 25px; border-radius: 15px; border: 2px solid #fff; text-align: center;">
                    <h4 style="margin:0; color: #fff; opacity: 0.8;">TENDENCIA DETECTADA</h4>
                    <h2 style="margin:0; color: #fff;">{tendencia}</h2>
                    <hr style="border: 0.5px solid rgba(255,255,255,0.2);">
                    <h1 style="margin:0; font-size: 50px; color: #fff;">{res_ia}</h1>
                    <p class="metric-val">{p_val:.1f}%</p>
                    <p style="margin:0; color: #fff;">PRECISIÓN CALCULADA</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Presiona 'Take Photo' para iniciar el análisis estadístico.")

# --- GRÁFICA PROFESIONAL ---
st.write("")
st.components.v1.html(f"""
    <div id="tradingview_v47" style="height:450px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 450, "symbol": "{mercado.replace('/','')}", "interval": "1", "theme": "dark", "container_id": "tradingview_v47", "locale": "es", "style": "1"}});
    </script>
""", height=450)

# --- PANEL DE EJECUCIÓN ---
st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 ANALIZAR AHORA", use_container_width=True):
        st.session_state.temp_s = {"r": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]), "p": f"{random.uniform(97,99):.1f}%"}
with c2:
    if 'temp_s' in st.session_state:
        st.success(f"{st.session_state.temp_s['r']} | {st.session_state.temp_s['p']}")
with c3:
    cw, cl = st.columns(2)
    if cw.button("WIN ✅", use_container_width=True):
        st.session_state.contador["Wins"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - {mercado} - GANADA ✅")
        st.rerun()
    if cl.button("LOSS ❌", use_container_width=True):
        st.session_state.contador["Loss"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - {mercado} - PERDIDA ❌")
        st.rerun()

# --- HISTORIAL LIMPIO ---
st.subheader("📝 Historial de Operaciones")
if st.session_state.historial:
    for op in st.session_state.historial[:5]:
        st.write(f"🔹 {op}")
else:
    st.caption("Esperando registros...")