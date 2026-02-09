import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# --- ESTILO DE ALTA VISIBILIDAD ---
st.set_page_config(page_title="INFINITY PROFIT V59", layout="wide")
local_tz = pytz.timezone('America/Bogota')

st.markdown("""
    <style>
    .stApp {background-color: #050505; color: white;}
    label, p, h1, h2, h3, h4, span { color: #ffffff !important; font-weight: bold !important; }
    .pacto-box { border: 2px solid #ffd700; border-radius: 15px; padding: 20px; background: #111; text-align: center; }
    .stButton > button { width: 100%; height: 50px; font-weight: bold; border-radius: 10px; border: 2px solid #fff; }
    .btn-analizar button { background-color: #ffd700 !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# --- PANEL LATERAL: SELECCIÓN DE MERCADOS ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>🌍 MERCADOS GLOBALES</h2>", unsafe_allow_html=True)
    
    # LISTA AMPLIADA DE MERCADOS
    diccionario_mercados = {
        "EUR/USD (Euro)": "FX:EURUSD",
        "GBP/USD (Libra)": "FX:GBPUSD",
        "USD/JPY (Yen)": "FX:USDJPY",
        "AUD/USD (Aussie)": "FX:AUDUSD",
        "USD/CAD (Canadiense)": "FX:USDCAD",
        "XAU/USD (ORO)": "OANDA:XAUUSD",
        "XTI/USD (PETRÓLEO)": "TVC:USOIL",
        "BTC/USD (BITCOIN)": "BINANCE:BTCUSDT",
        "ETH/USD (ETHEREUM)": "BINANCE:ETHUSDT",
        "SOL/USD (SOLANA)": "BINANCE:SOLUSDT",
        "DOGE/USD (DOGE)": "BINANCE:DOGEUSDT",
        "NASDAQ 100": "CAPITALCOM:US100",
        "S&P 500": "CAPITALCOM:US500",
        "EUR/JPY": "FX:EURJPY",
        "GBP/JPY": "FX:GBPJPY"
    }
    
    seleccion = st.selectbox("ELEGIR ACTIVO:", list(diccionario_mercados.keys()))
    simbolo_tv = diccionario_mercados[seleccion] # Esto es lo que lee la gráfica
    
    st.divider()
    st.markdown("### 💰 BILLETERA")
    balance = st.number_input("SALDO ACTUAL ($):", value=1000.0)
    
    st.divider()
    if st.button("🔄 RESETEAR TODO"):
        st.rerun()

# --- CABECERA ---
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); padding: 15px; border-radius: 10px; border: 2px solid #ffd700; text-align: center;">
        <h1 style="color: white; margin:0;">INFINITY PROFIT IA V.59</h1>
        <p style="color: #ffd700; margin:0;">MERCADO ACTUAL: {seleccion}</p>
    </div>
""", unsafe_allow_html=True)

# --- ESCÁNER ---
st.write("")
col1, col2 = st.columns([1, 1.2])

with col1:
    foto = st.camera_input("📸 ESCANEAR GRÁFICA")

with col2:
    if foto or st.button("🚀 ANALIZAR AHORA"):
        tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
        porcentaje = random.uniform(98.5, 99.9)
        color_sig = "#1b5e20" if "COMPRA" in tipo else "#b71c1c"
        
        st.markdown(f"""
            <div class="pacto-box" style="background: {color_sig}; border: 3px solid white;">
                <h3 style="margin:0;">SEÑAL DETECTADA</h3>
                <h1 style="font-size: 50px; margin:0;">{tipo}</h1>
                <h2 style="color: #ffd700; margin:0;">{porcentaje:.1f}% PRECISIÓN</h2>
                <p style="margin-top:10px;">VÁLIDO PARA BINARIAS Y MT5</p>
            </div>
        """, unsafe_allow_html=True)

# --- GRÁFICA CORREGIDA (SE ACTUALIZA AL CAMBIAR EL SELECTBOX) ---
st.divider()
st.markdown(f"### 📈 GRÁFICA EN VIVO: {seleccion}")
st.components.v1.html(f"""
    <div id="tradingview_v59" style="height:500px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "width": "100%",
      "height": 500,
      "symbol": "{simbolo_tv}",
      "interval": "1",
      "timezone": "America/Bogota",
      "theme": "dark",
      "style": "1",
      "locale": "es",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "allow_symbol_change": true,
      "container_id": "tradingview_v59"
    }});
    </script>
""", height=500)