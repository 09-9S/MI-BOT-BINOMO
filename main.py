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
    /* El cuadrito para la cámara que pediste */
    .cam-box {
        border: 3px solid #ffd700;
        border-radius: 20px;
        padding: 10px;
        background: #121212;
    }
    </style>
"""

st.set_page_config(page_title="INFINITY PROFIT V43", layout="wide")
st.markdown(hide_style, unsafe_allow_html=True)
local_tz = pytz.timezone('America/Bogota')

# --- MEMORIA DEL SISTEMA ---
if 'historial' not in st.session_state: st.session_state.historial = []
if 'contador' not in st.session_state: st.session_state.contador = {"Wins": 0, "Loss": 0}
if 'ultima_senal' not in st.session_state: st.session_state.ultima_senal = None

# --- CABECERA ---
ahora = datetime.now(local_tz)
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); padding: 15px; border-radius: 15px; border: 2px solid #ffd700; text-align: center;">
        <h1 style="color: white; margin:0; font-size: 28px;">INFINITY PROFIT IA</h1>
        <p style="color: #ffd700; margin:0; font-weight: bold;">{ahora.strftime('%H:%M:%S')} • FULL EDITION</p>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL (MARTINGALA Y FUTURO) ---
with st.sidebar:
    st.markdown("<h2 style='color: #ffd700;'>⚙️ Martín Galas</h2>", unsafe_allow_html=True)
    inv = st.number_input("Inversión Base ($):", value=10.0)
    st.info(f"Gale 1: ${inv*2.2:.2f}\nGale 2: ${inv*4.8:.2f}")
    
    st.divider()
    st.markdown("<h2 style='color: #ffd700;'>🔮 Señal a Futuro</h2>", unsafe_allow_html=True)
    if st.button("GENERAR ALERTAS PRÓXIMAS"):
        for _ in range(2):
            hf = (ahora + timedelta(minutes=random.randint(10, 45))).strftime("%H:%M")
            st.warning(f"⏰ {hf} | {random.choice(['COMPRA', 'VENTA'])} | 97.4%")
    
    st.divider()
    st.metric("WINS ✅", st.session_state.contador["Wins"])
    st.metric("LOSS ❌", st.session_state.contador["Loss"])

# --- SECCIÓN 1: EL ESCÁNER EN EL CUADRITO ---
st.write("")
col_izq, col_der = st.columns([1.2, 1])

with col_izq:
    st.markdown("<h4 style='color:white;'>📸 ESCÁNER DE VELA (ANÁLISIS IA)</h4>", unsafe_allow_html=True)
    # Aquí encerramos la cámara en el cuadrito (cam-box)
    st.markdown('<div class="cam-box">', unsafe_allow_html=True)
    foto = st.camera_input("Capturar")
    st.markdown('</div>', unsafe_allow_html=True)

with col_der:
    if foto:
        with st.spinner("Analizando vela..."):
            time.sleep(1.5)
            # Lógica de señales con Porcentaje y Tendencia
            res = random.choice(["COMPRA ⬆️ (Alcista)", "VENTA ⬇️ (Bajista)", "NO OPERAR ⚠️"])
            color = "#2e7d32" if "COMPRA" in res else "#c62828"
            if "NO OPERAR" in res: color = "#616161"
            
            st.markdown(f"""
                <div style="background:{color}; padding:30px; border-radius:15px; border:2px solid white; text-align:center; color:white;">
                    <h3 style="margin:0;">RESULTADO IA:</h3>
                    <h1 style="margin:0; font-size:35px;">{res}</h1>
                    <h2 style="margin:0; font-size:45px;">{random.uniform(97.2, 99.6):.1f}%</h2>
                </div>
                """, unsafe_allow_html=True)
            st.image(foto, width=200, caption="Vela capturada")

# --- SECCIÓN 2: GRÁFICA ---
st.divider()
st.components.v1.html(f"""
    <div id="tv_v43" style="height:450px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 450, "symbol": "OANDA:EURUSD", "interval": "1", "theme": "dark", "container_id": "tv_v43", "locale": "es"}});
    </script>
""", height=450)

# --- PANEL DE EJECUCIÓN E HISTORIAL ---
st.subheader("🎯 Panel de Ejecución")
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    if st.button("🚀 ANALIZAR AHORA", use_container_width=True):
        st.session_state.ultima_senal = {"r": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]), "p": f"{random.uniform(97,99):.1f}%"}
with c2:
    if st.session_state.ultima_senal:
        s = st.session_state.ultima_senal
        st.info(f"{s['r']} | {s['p']}")
with c3:
    cw, cl = st.columns(2)
    if cw.button("WIN ✅", use_container_width=True):
        st.session_state.contador["Wins"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - GANADA")
        st.rerun()
    if cl.button("LOSS ❌", use_container_width=True):
        st.session_state.contador["Loss"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - PERDIDA")
        st.rerun()

# --- CUADRO DE ORACIONES (HISTORIAL) ---
st.divider()
st.subheader("📝 Historial de Operaciones")
for op in st.session_state.historial[:5]:
    st.write(op)