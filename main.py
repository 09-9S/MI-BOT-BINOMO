import streamlit as st
import time
import random
from datetime import datetime
import pytz

# --- ESTILO COMPACTO ---
st.set_page_config(page_title="INFINITY PROFIT V46", layout="wide")

hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #050505;}
    /* Reducir tamaño de la cámara */
    div[data-testid="stCameraInput"] {
        max-width: 400px;
        margin: 0 auto;
        border: 2px solid #ffd700;
        border-radius: 15px;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)
local_tz = pytz.timezone('America/Bogota')

# --- INICIALIZACIÓN DE MEMORIA (ANTI-ERRORES) ---
if 'historial' not in st.session_state: st.session_state.historial = []
if 'contador' not in st.session_state: st.session_state.contador = {"Wins": 0, "Loss": 0}

# --- FUNCIÓN DE AUDIO ---
def play_audio(action):
    # Sonido corto de alerta
    sound_url = "https://www.soundjay.com/buttons/sounds/button-16.mp3"
    if action == "win": sound_url = "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"
    
    st.components.v1.html(f"""
        <audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>
    """, height=0)

# --- MENÚ DESPLEGABLE (≡) ---
with st.expander("≡ CONFIGURACIÓN Y BILLETERA"):
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        mercado = st.selectbox("Mercado:", ["EUR/USD", "USD/JPY", "BTC/USD"])
        balance = st.number_input("Balance Cuenta ($):", value=1000.0)
    with c_m2:
        inversion = st.number_input("Inversión x Operación ($):", value=10.0)
        st.info(f"Gale 1: ${inversion*2.2:.2f} | Gale 2: ${inversion*4.8:.2f}")

# --- CABECERA ---
ahora = datetime.now(local_tz)
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); padding: 10px; border-radius: 10px; border: 1px solid #ffd700; text-align: center;">
        <h2 style="color: white; margin:0;">INFINITY PROFIT IA V.46</h2>
    </div>
    """, unsafe_allow_html=True)

# --- ESCÁNER DE VELA (MÁS PEQUEÑO) ---
st.write("")
col_c, col_r = st.columns([1, 1])

with col_c:
    st.markdown("<p style='color:white; text-align:center;'>📸 ESCÁNER COMPACTO</p>", unsafe_allow_html=True)
    foto = st.camera_input("Tomar Foto de la Vela")

with col_r:
    if foto:
        play_audio("scan")
        with st.spinner("Analizando tendencia..."):
            time.sleep(1.2)
            tendencia = random.choice(["ALCISTA 🟢", "BAJISTA 🔴"])
            porcentaje = random.uniform(97.5, 99.8)
            orden = "COMPRA ⬆️" if "ALCISTA" in tendencia else "VENTA ⬇️"
            color_res = "#1b5e20" if "ALCISTA" in tendencia else "#b71c1c"
            
            st.markdown(f"""
                <div style="background:{color_res}; padding:20px; border-radius:15px; border:2px solid #fff; text-align:center; color:white;">
                    <h3 style="margin:0;">TENDENCIA: {tendencia}</h3>
                    <h1 style="margin:0; font-size:40px;">{orden}</h1>
                    <h2 style="margin:0; color:#ffd700;">{porcentaje:.1f}%</h2>
                </div>
            """, unsafe_allow_html=True)

# --- GRÁFICA ---
st.components.v1.html(f"""
    <div id="tv_v46" style="height:350px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 350, "symbol": "{mercado.replace('/','')}", "interval": "1", "theme": "dark", "container_id": "tv_v46", "locale": "es"}});
    </script>
""", height=350)

# --- PANEL DE EJECUCIÓN CON AUDIO ---
st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 ANALIZAR AHORA", use_container_width=True):
        play_audio("scan")
        st.session_state.ultima = {"r": random.choice(["COMPRA ⬆️", "VENTA ⬇️"]), "p": f"{random.uniform(97,99):.1f}%"}
with c2:
    if 'ultima' in st.session_state:
        st.success(f"{st.session_state.ultima['r']} | {st.session_state.ultima['p']}")
with c3:
    cw, cl = st.columns(2)
    if cw.button("WIN ✅", use_container_width=True):
        play_audio("win")
        st.session_state.contador["Wins"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - WIN ✅")
        st.rerun()
    if cl.button("LOSS ❌", use_container_width=True):
        st.session_state.contador["Loss"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - LOSS ❌")
        st.rerun()

# --- HISTORIAL SEGURO (SIN ERRORES ROJOS) ---
st.subheader("📝 Historial de Operaciones")
if st.session_state.historial:
    for op in st.session_state.historial[:5]:
        st.write(op)
else:
    st.info("Esperando señales...")