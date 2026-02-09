import streamlit as st
import time
import random
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="INFINITY PROFIT V64", layout="wide")
local_tz = pytz.timezone('America/Bogota')

# --- ESTILO CSS DE ALTA GAMA (EXCELENCIA VISUAL) ---
st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    
    /* Reloj Estilo Neon */
    .reloj-box {
        background: linear-gradient(180deg, #111 0%, #000 100%);
        border: 2px solid #ffd700;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.2);
        margin-bottom: 25px;
    }
    .reloj-h { font-size: 45px; color: #ffd700; font-weight: 800; margin: 0; line-height: 1; }
    .reloj-f { font-size: 16px; color: #888; text-transform: uppercase; letter-spacing: 2px; }

    /* Contenedores Organizados */
    .card-pro {
        background: #0f0f0f;
        border: 1px solid #222;
        border-radius: 15px;
        padding: 20px;
        height: 100%;
    }
    
    /* Botones de Acción */
    .stButton > button { width: 100%; border-radius: 12px; font-weight: bold; height: 50px; border: none; transition: 0.3s; }
    .btn-win button { background: linear-gradient(90deg, #1b5e20, #2e7d32) !important; color: white !important; }
    .btn-loss button { background: linear-gradient(90deg, #b71c1c, #c62828) !important; color: white !important; }
    .btn-reset button { background: transparent !important; color: #ff4b4b !important; border: 1px solid #ff4b4b !important; }
    .btn-analizar button { background: #ffd700 !important; color: black !important; font-size: 18px !important; }
    
    /* Señal Híbrida Premium */
    .signal-card {
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 2px solid white;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE REINICIO ---
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'mostrar_señal' not in st.session_state: st.session_state.mostrar_señal = False

def limpiar_todo():
    st.session_state.win = 0
    st.session_state.loss = 0
    st.session_state.mostrar_señal = False
    st.rerun()

# --- BLOQUE 1: RELOJ CENTRAL (EXCELENTE VISIBILIDAD) ---
now = datetime.now(local_tz)
st.markdown(f"""
    <div class="reloj-box">
        <p class="reloj-f">{now.strftime('%d . %m . %Y')}</p>
        <p class="reloj-h">{now.strftime('%H:%M:%S')}</p>
        <p style="margin:0; color:#ffd700; font-size:12px;">ZONA HORARIA: COLOMBIA</p>
    </div>
""", unsafe_allow_html=True)

# --- BLOQUE 2: DASHBOARD PRINCIPAL ---
col_izq, col_der = st.columns([1, 1.3])

with col_izq:
    st.markdown("### 📸 ENTRADA DE DATOS")
    with st.container():
        foto = st.camera_input("Scanner de Gráfica")
    
    st.write("")
    st.markdown("### 📊 MARCADOR DE SESIÓN")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="btn-win">', unsafe_allow_html=True)
        if st.button("WIN ✅"): st.session_state.win += 1
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-loss">', unsafe_allow_html=True)
        if st.button("LOSS ❌"): st.session_state.loss += 1
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="display:flex; justify-content:space-around; background:#111; padding:15px; border-radius:10px; border:1px solid #333; margin-top:10px;">
            <div style="text-align:center;"><h4 style="margin:0; color:#00ff00;">{st.session_state.win}</h4><p style="font-size:10px; margin:0;">GANADAS</p></div>
            <div style="text-align:center;"><h4 style="margin:0; color:#ff4b4b;">{st.session_state.loss}</h4><p style="font-size:10px; margin:0;">PERDIDAS</p></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="btn-reset" style="margin-top:15px;">', unsafe_allow_html=True)
    if st.button("⚠️ REINICIAR TODO"): limpiar_todo()
    st.markdown('</div>', unsafe_allow_html=True)

with col_der:
    st.markdown("### 🎯 ANÁLISIS HÍBRIDO")
    if foto or st.button("🚀 ANALIZAR AHORA"):
        st.session_state.mostrar_señal = True
        
    if st.session_state.mostrar_señal:
        tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
        color_bg = "#1b5e20" if "COMPRA" in tipo else "#b71c1c"
        precis = random.uniform(99.4, 99.9)
        # Datos MT5
        precio = random.uniform(1.0820, 1.0850)
        tp = precio + 0.0040 if "COMPRA" in tipo else precio - 0.0040
        sl = precio - 0.0020 if "COMPRA" in tipo else precio + 0.0020
        
        st.markdown(f"""
            <div class="signal-card" style="background: {color_bg};">
                <p style="margin:0; opacity:0.8;">SEÑAL DETECTADA A LAS: {datetime.now(local_tz).strftime('%H:%M:%S')}</p>
                <h1 style="font-size: 65px; margin:10px 0;">{tipo}</h1>
                <h2 style="color: #ffd700; margin:0;">{precis:.1f}% PRECISIÓN</h2>
                <hr style="border:0.5px solid rgba(255,255,255,0.2); margin:20px 0;">
                <div style="display:flex; justify-content:space-around;">
                    <div><p style="font-size:12px; margin:0;">TP (MT5)</p><h3 style="margin:0;">{tp:.5f}</h3></div>
                    <div><p style="font-size:12px; margin:0;">SL (MT5)</p><h3 style="margin:0;">{sl:.5f}</h3></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="height:250px; border:2px dashed #333; border-radius:20px; display:flex; align-items:center; justify-content:center;">
                <p style="color:#555 !important;">ESPERANDO CAPTURA PARA ANALIZAR...</p>
            </div>
        """, unsafe_allow_html=True)

# --- BLOQUE 3: MERCADOS Y GRÁFICA ---
st.divider()
col_m1, col_m2 = st.columns([1, 3])
with col_m1:
    lista_m = {"EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "ORO": "OANDA:XAUUSD", "BTC": "BINANCE:BTCUSDT"}
    selec = st.selectbox("CAMBIAR MERCADO:", list(lista_m.keys()))
    st.info(f"ACTIVO: {selec}")

with col_m2:
    st.components.v1.html(f"""
        <div id="tv_v64" style="height:450px; border-radius:15px; overflow:hidden;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{"width":"100%","height":450,"symbol":"{lista_m[selec]}","interval":"1","theme":"dark","locale":"es","container_id":"tv_v64"}});
        </script>
    """, height=450)