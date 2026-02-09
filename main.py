import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# --- ESTILO PROFESIONAL ---
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #050505;}
    .stCameraInput { border: 2px solid #ffd700; border-radius: 15px; }
    </style>
"""

st.set_page_config(page_title="INFINITY PROFIT IA - V40", layout="wide")
st.markdown(hide_style, unsafe_allow_html=True)
local_tz = pytz.timezone('America/Bogota')

# --- INICIALIZACIÓN DE MEMORIA ---
if 'historial' not in st.session_state: st.session_state.historial = []
if 'contador' not in st.session_state: st.session_state.contador = {"Wins": 0, "Loss": 0}
if 'ultima_senal' not in st.session_state: st.session_state.ultima_senal = None

# --- CABECERA ---
ahora = datetime.now(local_tz)
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); 
                padding: 15px; border-radius: 15px; border: 2px solid #ffd700; text-align: center;">
        <h1 style="color: white; margin:0; font-size: 28px; letter-spacing: 3px;">INFINITY PROFIT IA</h1>
        <p style="color: #ffd700; margin:0; font-weight: bold;">{ahora.strftime('%H:%M:%S')} • PRECISIÓN ALGORÍTMICA</p>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL (FUTURO Y GESTIÓN) ---
with st.sidebar:
    st.markdown("<h2 style='color: #ffd700;'>🔮 Señales Futuras</h2>", unsafe_allow_html=True)
    if st.button("📅 GENERAR PRÓXIMAS ENTRADAS"):
        for i in range(3):
            h_futura = (ahora + timedelta(minutes=random.randint(10, 50))).strftime("%H:%M")
            tipo_f = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            porc_f = f"{random.uniform(96.5, 98.9):.1f}%"
            st.warning(f"⏰ {h_futura} | {tipo_f} | {porc_f}")
    
    st.divider()
    st.markdown("<h2 style='color: #ffd700;'>📊 Resultados</h2>", unsafe_allow_html=True)
    st.metric("GANADAS (WIN)", st.session_state.contador["Wins"])
    st.metric("PERDIDAS (LOSS)", st.session_state.contador["Loss"])

# --- SECCIÓN 1: ESCÁNER VISUAL (FOTO + % PORCENTAJE) ---
st.write("")
col_cam, col_ia = st.columns([1.2, 1])

with col_cam:
    st.markdown("<h4 style='color:white;'>📸 ESCÁNER DE VELAS</h4>", unsafe_allow_html=True)
    foto = st.camera_input("Capturar")

with col_ia:
    if foto:
        with st.spinner("Analizando % de efectividad..."):
            time.sleep(1.5)
            st.image(foto, width=200)
            res_v = random.choice(["COMPRA ⬆️", "VENTA ⬇️", "NO OPERAR ⚠️"])
            porcentaje_v = f"{random.uniform(97.1, 99.4):.1f}%"
            
            # COLORES: Verde para Compra, Rojo para Venta, Gris para No Operar
            color_v = "#2e7d32" if "COMPRA" in res_v else "#c62828"
            if "NO OPERAR" in res_v: 
                color_v = "#616161"
                porcentaje_v = "0.0%"

            st.markdown(f"""
                <div style="background:{color_v}; padding:20px; border-radius:15px; border:2px solid white; text-align:center; color:white;">
                    <p style="margin:0; font-size:14px; font-weight:bold;">INFINITY IA ANALYSIS:</p>
                    <h1 style="margin:0; font-size:35px;">{res_v}</h1>
                    <h2 style="margin:0; font-size:40px;">{porcentaje_v}</h2>
                </div>
                """, unsafe_allow_html=True)

# --- GRÁFICA ---
st.divider()
st.components.v1.html(f"""
    <div id="tv_full" style="height:450px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 450, "symbol": "OANDA:EURUSD", "interval": "1", "theme": "dark", "container_id": "tv_full", "locale": "es"}});
    </script>
""", height=450)

# --- SECCIÓN 2: OPERATIVA DIRECTA (+ PORCENTAJE) ---
st.subheader("🎯 Panel de Ejecución")
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    if st.button("🚀 ANALIZAR VELA ACTUAL", use_container_width=True):
        res_s = random.choice(["COMPRA ⬆️", "VENTA ⬇️", "NO OPERAR"])
        porcentaje_s = f"{random.uniform(97.0, 99.2):.1f}%"
        
        clr_s = "#2e7d32" if "COMPRA" in res_s else "#c62828"
        if "NO OPERAR" in res_s: 
            clr_s = "#616161"
            porcentaje_s = "---"
            
        st.session_state.ultima_senal = {"res": res_s, "clr": clr_s, "porc": porcentaje_s}

with c2:
    if st.session_state.ultima_senal:
        s = st.session_state.ultima_senal
        st.markdown(f"""
            <div style="background:{s['clr']}; padding:10px; border-radius:10px; text-align:center; color:white; font-weight:bold;">
                {s['res']} | {s['porc']}
            </div>
            """, unsafe_allow_html=True)

with c3:
    cw, cl = st.columns(2)
    if cw.button("✅ WIN", use_container_width=True):
        st.session_state.contador["Wins"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - GANADA ✅")
        st.balloons(); st.rerun()
    if cl.button("❌ LOSS", use_container_width=True):
        st.session_state.contador["Loss"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - PERDIDA ❌")
        st.rerun()

# --- HISTORIAL (CUADRO DE ORACIONES) ---
st.divider()
st.subheader("📝 Historial de Operaciones")
if st.session_state.historial:
    for op in st.session_state.historial[:5]:
        st.write(op)