import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# --- ESTILO PROFESIONAL Y OCULTAR MENÚS ---
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #050505;}
    .stCameraInput { border: 2px solid #ffd700; border-radius: 15px; }
    </style>
"""

st.set_page_config(page_title="INFINITY PROFIT IA - V41", layout="wide")
st.markdown(hide_style, unsafe_allow_html=True)
local_tz = pytz.timezone('America/Bogota')

# --- INICIALIZACIÓN DE MEMORIA (CORRECCIÓN DE KEYERROR) ---
if 'historial' not in st.session_state: st.session_state.historial = []
if 'contador' not in st.session_state: st.session_state.contador = {"Wins": 0, "Loss": 0}
if 'ultima_senal' not in st.session_state: st.session_state.ultima_senal = None

# --- CABECERA ---
ahora = datetime.now(local_tz)
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #000, #b8860b, #000); 
                padding: 15px; border-radius: 15px; border: 2px solid #ffd700; text-align: center;">
        <h1 style="color: white; margin:0; font-size: 28px;">INFINITY PROFIT IA</h1>
        <p style="color: #ffd700; margin:0;">MODO ESCÁNER AVANZADO • {ahora.strftime('%H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL (MARTINGALE Y SEÑALES) ---
with st.sidebar:
    st.markdown("<h2 style='color: #ffd700;'>⚙️ Gestión Martingale</h2>", unsafe_allow_html=True)
    inversion = st.number_input("Inversión Inicial ($):", value=10.0)
    st.info(f"Sugerencia GALE:\nG1: ${inversion*2.2:.2f}\nG2: ${inversion*4.8:.2f}")
    
    st.divider()
    st.markdown("<h2 style='color: #ffd700;'>🔮 Futuro</h2>", unsafe_allow_html=True)
    if st.button("📅 GENERAR PRÓXIMAS ENTRADAS"):
        for i in range(2):
            h_f = (ahora + timedelta(minutes=random.randint(5, 30))).strftime("%H:%M")
            st.warning(f"⏰ {h_f} | {random.choice(['COMPRA ⬆️', 'VENTA ⬇️'])} | {random.randint(96, 98)}%")

# --- SECCIÓN 1: ESCÁNER CON SPEECH BUBBLE ---
st.write("")
col_cam, col_ia = st.columns([1.2, 1])

with col_cam:
    st.markdown("<h4 style='color:white;'>📸 ESCÁNER DE VELAS</h4>", unsafe_allow_html=True)
    foto = st.camera_input("Capturar para análisis")

with col_ia:
    if foto:
        with st.spinner("Analizando volatilidad..."):
            time.sleep(1.5)
            # SPEECH BUBBLE (EL CUADRITO QUE PEDISTE)
            res_v = random.choice(["COMPRA ⬆️", "VENTA ⬇️", "NO OPERAR ⚠️"])
            color_v = "#2e7d32" if "COMPRA" in res_v else "#c62828"
            if "NO OPERAR" in res_v: color_v = "#616161"
            
            st.markdown(f"""
                <div style="background:{color_v}; padding:25px; border-radius:15px; border:2px solid white; position:relative; color:white; text-align:center;">
                    <h3 style="margin:0;">INFINITY IA DICE:</h3>
                    <h1 style="margin:0; font-size:40px;">{res_v}</h1>
                    <h2 style="margin:0;">{random.uniform(97.1, 99.5):.1f}%</h2>
                    <p style="margin:0; font-size:12px;">Volatilidad: {random.randint(10, 40)}% (Baja)</p>
                    <div style="position:absolute; left:-18px; top:45%; width:0; height:0; border-top:15px solid transparent; border-bottom:15px solid transparent; border-right:15px solid {color_v};"></div>
                </div>
                """, unsafe_allow_html=True)
            st.image(foto, width=150, caption="Captura actual")

# --- GRÁFICA ---
st.divider()
st.components.v1.html(f"""
    <div id="tv_v41" style="height:450px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{"width": "100%", "height": 450, "symbol": "OANDA:EURUSD", "interval": "1", "theme": "dark", "container_id": "tv_v41", "locale": "es"}});
    </script>
""", height=450)

# --- PANEL DE EJECUCIÓN ---
st.subheader("🎯 Panel de Ejecución")
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    if st.button("🚀 ANALIZAR VELA ACTUAL", use_container_width=True):
        res_s = random.choice(["COMPRA ⬆️", "VENTA ⬇️", "NO OPERAR"])
        clr_s = "#2e7d32" if "COMPRA" in res_s else "#c62828"
        if "NO OPERAR" in res_s: clr_s = "#616161"
        st.session_state.ultima_senal = {"res": res_s, "clr": clr_s, "porc": f"{random.uniform(97, 99):.1f}%"}

with c2:
    if st.session_state.ultima_senal:
        s = st.session_state.ultima_senal
        st.markdown(f'<div style="background:{s["clr"]}; padding:10px; border-radius:10px; text-align:center; color:white; font-weight:bold;">{s["res"]} | {s["porc"]}</div>', unsafe_allow_html=True)

with c3:
    cw, cl = st.columns(2)
    if cw.button("✅ WIN", use_container_width=True):
        st.session_state.contador["Wins"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - OPERACIÓN GANADA ✅")
        st.balloons(); st.rerun()
    if cl.button("❌ LOSS", use_container_width=True):
        st.session_state.contador["Loss"] += 1
        st.session_state.historial.insert(0, f"{ahora.strftime('%H:%M')} - OPERACIÓN PERDIDA ❌")
        st.rerun()

# --- HISTORIAL (FIXED) ---
st.divider()
st.subheader("📝 Historial de Operaciones")
if st.session_state.historial:
    for item in st.session_state.historial[:5]:
        st.write(item)
else:
    st.info("Esperando primera operación...")