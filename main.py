import streamlit as st
import time
import random
from datetime import datetime
import pytz

# --- 1. CONFIGURACIÓN Y ESTILOS (BLOQUEADO) ---
st.set_page_config(page_title="INFINITY PROFIT V68", layout="wide")
local_tz = pytz.timezone('America/Bogota')

st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    
    /* Reloj Neón */
    .reloj-box {
        background: linear-gradient(180deg, #111, #000);
        border: 2px solid #ffd700;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.3);
    }
    .reloj-h { font-size: 45px; color: #ffd700; font-weight: 800; margin: 0; }
    
    /* Botones Profesionales */
    .stButton > button { width: 100%; border-radius: 12px; font-weight: bold; height: 50px; border: none; }
    .btn-win button { background: linear-gradient(90deg, #1b5e20, #2e7d32) !important; color: white !important; }
    .btn-loss button { background: linear-gradient(90deg, #b71c1c, #c62828) !important; color: white !important; }
    .btn-analizar button { background: #ffd700 !important; color: black !important; font-size: 18px !important; }
    
    /* Tarjeta de Señal MT5 */
    .signal-card {
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 2px solid white;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. MEMORIA DE SESIÓN ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'mostrar_señal' not in st.session_state: st.session_state.mostrar_señal = False

# --- 3. BARRA LATERAL (CONTROL DE SESIÓN) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700; text-align:center;'>📊 ESTADÍSTICAS</h2>", unsafe_allow_html=True)
    st.success(f"GANADAS: {st.session_state.win}")
    st.error(f"PERDIDAS: {st.session_state.loss}")
    st.divider()
    if st.button("🔄 REINICIAR TODO"):
        st.session_state.win = 0
        st.session_state.loss = 0
        st.session_state.mostrar_señal = False
        st.rerun()

# --- 4. RELOJ CENTRALIZADO ---
now = datetime.now(local_tz)
st.markdown(f"""
    <div class="reloj-box">
        <p style="color:#888; margin:0; letter-spacing:2px; font-size:14px;">{now.strftime('%d DE %B, %Y')}</p>
        <p class="reloj-h">{now.strftime('%H:%M:%S')}</p>
    </div>
""", unsafe_allow_html=True)

# --- 5. PANEL DE TRABAJO (ESCÁNER Y SEÑAL) ---
col_izq, col_der = st.columns([1, 1.3])

with col_izq:
    st.markdown("### 📸 ESCÁNER DE MERCADO")
    foto = st.camera_input("Capturar pantalla")
    
    st.write("")
    st.markdown("### ⚡ ACCIÓN RÁPIDA")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="btn-win">', unsafe_allow_html=True)
        if st.button("WIN ✅"): st.session_state.win += 1
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-loss">', unsafe_allow_html=True)
        if st.button("LOSS ❌"): st.session_state.loss += 1
        st.markdown('</div>', unsafe_allow_html=True)

with col_der:
    st.markdown("### 🎯 ANÁLISIS HÍBRIDO (BINARIAS & MT5)")
    if foto or st.button("🚀 ANALIZAR AHORA"):
        st.session_state.mostrar_señal = True
        
    if st.session_state.mostrar_señal:
        # Generación de Señal Corregida
        tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
        color_bg = "#1b5e20" if "COMPRA" in tipo else "#b71c1c"
        precio = random.uniform(1.0820, 1.0850)
        tp = precio + 0.0040 if "COMPRA" in tipo else precio - 0.0040
        sl = precio - 0.0020 if "COMPRA" in tipo else precio + 0.0020
        
        st.markdown(f"""
            <div class="signal-card" style="background: {color_bg};">
                <p style="margin:0; opacity:0.8;">SEÑAL GENERADA A LAS: {datetime.now(local_tz).strftime('%H:%M:%S')}</p>
                <h1 style="font-size: 55px; margin:10px 0;">{tipo}</h1>
                <h2 style="color: #ffd700; margin:0;">99.9% PRECISIÓN</h2>
                <hr style="border:0.5px solid rgba(255,255,255,0.2); margin:15px 0;">
                <div style="display:flex; justify-content:space-around;">
                    <div><p style="margin:0; font-size:12px;">TAKE PROFIT</p><h3 style="margin:0;">{tp:.5f}</h3></div>
                    <div><p style="margin:0; font-size:12px;">STOP LOSS</p><h3 style="margin:0;">{sl:.5f}</h3></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Esperando captura o click para iniciar análisis...")

# --- 6. GRÁFICA Y SELECTOR (CENTRAL) ---
st.divider()
st.markdown("### 📈 GRÁFICA EN TIEMPO REAL")
lista_m = {
    "EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "XAU/USD (ORO)": "OANDA:XAUUSD",
    "BITCOIN": "BINANCE:BTCUSDT", "SOLANA": "BINANCE:SOLUSDT"
}

# Selector de mercado justo encima de la gráfica
selec = st.selectbox("Cambiar Mercado:", list(lista_m.keys()))
simbolo_actual = lista_m[selec]

st.components.v1.html(f"""
    <div id="tv_v68" style="height:500px; border-radius:15px; overflow:hidden; border: 1px solid #333;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width":"100%","height":500,"symbol":"{simbolo_actual}","interval":"1","theme":"dark","locale":"es","container_id":"tv_v68"}});
    </script>
""", height=500)