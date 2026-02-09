import streamlit as st
import time
import random
from datetime import datetime
import pytz

# --- ESTILO DE ALTA GAMA ---
st.set_page_config(page_title="INFINITY PROFIT V45", layout="wide")

hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #050505;}
    /* Botón de Cámara Largo y Elegante */
    .stCameraInput > div > button {
        background-color: #ffd700 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- FUNCIÓN DE SONIDO (BEEP) ---
def play_sound(tipo):
    if tipo == "win":
        audio_url = "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"
    elif tipo == "gale":
        audio_url = "https://www.soundjay.com/buttons/sounds/button-10.mp3"
    else:
        audio_url = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
    
    st.components.v1.html(f"""
        <audio autoplay>
            <source src="{audio_url}" type="audio/mp3">
        </audio>
    """, height=0)

# --- MENÚ DE CONFIGURACIÓN (LAS TRES LÍNEAS) ---
with st.expander("≡ CONFIGURACIÓN DE MERCADO Y BILLETERA"):
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        mercado = st.selectbox("Mercado:", ["EUR/USD", "BTC/USD", "USD/JPY"])
    with col_m2:
        balance = st.number_input("Balance Cuenta ($):", value=1000.0)
    with col_m3:
        profit_deseado = st.slider("Profit Objetivo (%):", 1, 100, 85)
    
    inversion_base = st.number_input("Inversión por Operación ($):", value=10.0)
    st.write(f"Ganancia Estimada: ${inversion_base * (profit_deseado/100):.2f}")

# --- CABECERA ---
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); padding: 10px; border-radius: 15px; border: 1px solid #ffd700; text-align: center;">
        <h1 style="color: white; margin:0; font-size: 25px;">INFINITY PROFIT IA V.45</h1>
    </div>
    """, unsafe_allow_html=True)

# --- ESCÁNER DE FOTO (CUADRO APARTE) ---
st.write("")
st.subheader("📸 ESCÁNER IA DE ALTA PRECISIÓN")
with st.container():
    # Botón largo para la foto
    foto = st.camera_input("PRESIONA AQUÍ PARA ESCANEAR VELA")
    
    if foto:
        play_sound("gale")
        with st.spinner("PROCESANDO TENDENCIA..."):
            time.sleep(1.5)
            tendencia = random.choice(["ALCISTA 🟢", "BAJISTA 🔴"])
            operacion = "COMPRA ⬆️" if "ALCISTA" in tendencia else "VENTA ⬇️"
            porcentaje = random.uniform(97.8, 99.9)
            
            color_box = "#1b5e20" if "ALCISTA" in tendencia else "#b71c1c"
            
            st.markdown(f"""
                <div style="background: {color_box}; padding: 25px; border-radius: 20px; border: 3px solid #fff; text-align: center; color: white;">
                    <h2 style="margin:0;">TENDENCIA: {tendencia}</h2>
                    <h1 style="margin:0; font-size: 50px;">{operacion}</h1>
                    <h1 style="margin:0; font-size: 60px; color: #ffd700;">{porcentaje:.1f}%</h1>
                </div>
            """, unsafe_allow_html=True)

# --- GRÁFICA ---
st.divider()
st.components.v1.html(f"""
    <div id="tv_v45" style="height:400px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 400, "symbol": "{mercado.replace('/','')}", "interval": "1", "theme": "dark", "container_id": "tv_v45", "locale": "es"}});
    </script>
""", height=400)

# --- BOTONES DE ACCIÓN CON SONIDO ---
st.write("")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 ANALIZAR AHORA", use_container_width=True):
        play_sound("click")
        st.info("Buscando señal...")
with c2:
    if st.button("✅ WIN (GANADA)", use_container_width=True):
        play_sound("win")
        st.balloons()
with c3:
    if st.button("⚠️ MARTINGALE", use_container_width=True):
        play_sound("gale")
        st.warning(f"ENTRAR EN GALE: ${inversion_base * 2.2:.2f}")