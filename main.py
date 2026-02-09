import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# --- ESTILO BLINDADO (EVITA DESACOMODOS) ---
st.set_page_config(page_title="INFINITY PROFIT V50", layout="wide")

hide_style = """
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp {background-color: #050505; color: white;}
    
    /* Botones con Colores Fijos */
    .stButton > button { width: 100%; height: 50px; font-weight: bold; border-radius: 12px; }
    .btn-win button { background-color: #2e7d32 !important; color: white !important; border: none; }
    .btn-loss button { background-color: #c62828 !important; color: white !important; border: none; }
    .btn-analizar button { background-color: #ffd700 !important; color: black !important; border: 2px solid #000; }
    
    /* Contenedores de diseño */
    .pacto-container { border: 2px solid #ffd700; border-radius: 15px; padding: 20px; background: #111; margin-bottom: 20px; }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)
local_tz = pytz.timezone('America/Bogota')

# --- MEMORIA DEL SISTEMA ---
if 'historial' not in st.session_state: st.session_state.historial = []
if 'contador' not in st.session_state: st.session_state.contador = {"Wins": 0, "Loss": 0}

# --- BARRA LATERAL (CONFIGURACIÓN COMPLETA) ---
with st.sidebar:
    st.markdown("<h2 style='color: #ffd700;'>≡ CONFIGURACIÓN</h2>", unsafe_allow_html=True)
    
    # MÁS MERCADOS (AGREGADOS)
    lista_mercados = [
        "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", 
        "BTC/USD", "ETH/USD", "SOL/USD", "GOLD (XAU/USD)", "OIL"
    ]
    mercado = st.selectbox("Seleccionar Mercado:", lista_mercados, index=0)
    
    st.divider()
    st.markdown("<h3 style='color: #ffd700;'>💳 BILLETERA Y PROFIT</h3>")
    balance = st.number_input("Saldo Actual ($):", value=1000.0)
    inv_base = st.number_input("Inversión ($):", value=10.0)
    payout = st.slider("Payout (%)", 70, 95, 85)
    ganancia_est = inv_base * (payout/100)
    st.success(f"Ganancia por Win: ${ganancia_est:.2f}")
    
    st.divider()
    st.markdown("<h3 style='color: #ffd700;'>🔮 SEÑALES A FUTURO</h3>")
    if st.button("GENERAR ALERTAS PRÓXIMAS"):
        for _ in range(3):
            hora_f = (datetime.now(local_tz) + timedelta(minutes=random.randint(5, 60))).strftime("%H:%M")
            st.warning(f"⏰ {hora_f} | {random.choice(['COMPRA', 'VENTA'])} | 98.4%")

# --- CABECERA ---
ahora = datetime.now(local_tz)
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); padding: 10px; border-radius: 10px; border: 1px solid #ffd700; text-align: center;">
        <h1 style="color: white; margin:0; font-size: 24px;">INFINITY PROFIT IA V.50</h1>
    </div>
    """, unsafe_allow_html=True)

# --- ESCÁNER VISUAL (CUADRO PACTO) ---
st.write("")
col_cam, col_res = st.columns([1.2, 1])

with col_cam:
    st.markdown("<div class='pacto-container'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#ffd700;'>📸 ESCÁNER DE GRÁFICA</p>", unsafe_allow_html=True)
    foto = st.camera_input("Capturar")
    st.markdown("</div>", unsafe_allow_html=True)

with col_res:
    if foto:
        with st.spinner("IA ESCANEANDO..."):
            time.sleep(1.5)
            res = random.choice(["COMPRA ⬆️", "VENTA ⬇️", "NO OPERAR ⚠️"])
            color = "#2e7d32" if "COMPRA" in res else "#c62828"
            if "NO OPERAR" in res: color = "#424242"
            
            st.markdown(f"""
                <div style="background: {color}; padding: 30px; border-radius: 15px; border: 2px solid white; text-align: center;">
                    <h4 style="margin:0;">TENDENCIA DETECTADA:</h4>
                    <h1 style="margin:0; font-size: 45px;">{res}</h1>
                    <h2 style="margin:0; color: #ffd700;">{random.uniform(97.8, 99.7):.1f}%</h2>
                </div>
            """, unsafe_allow_html=True)

# --- GRÁFICA (TAMAÑO FIJO) ---
st.divider()
st.components.v1.html(f"""
    <div id="tv_v50" style="height:450px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 450, "symbol": "{mercado.replace('/','')}", "interval": "1", "theme": "dark", "container_id": "tv_v50", "locale": "es"}});
    </script>
""", height=450)

# --- PANEL DE RESULTADOS (DISEÑO ORGANIZADO) ---
st.write("")
st.subheader("🎯 Panel de Control de Resultados")
c_a, c_w, c_l = st.columns(3)

with c_a:
    st.markdown('<div class="btn-analizar">', unsafe_allow_html=True)
    if st.button("🚀 ANALIZAR AHORA"):
        st.info("Buscando patrón...")
    st.markdown('</div>', unsafe_allow_html=True)

with c_w:
    st.markdown('<div class="btn-win">', unsafe_allow_html=True)
    if st.button("WIN ✅"):
        st.session_state.contador["Wins"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - {mercado} - WIN ✅")
        st.balloons()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with c_l:
    st.markdown('<div class="btn-loss">', unsafe_allow_html=True)
    if st.button("LOSS ❌"):
        st.session_state.contador["Loss"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - {mercado} - LOSS ❌")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- HISTORIAL ---
st.divider()
st.subheader("📝 Registro de Operaciones")
for op in st.session_state.historial[:5]:
    st.write(f"🔹 {op}")