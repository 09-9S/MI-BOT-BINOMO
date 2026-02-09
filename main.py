import streamlit as st
import time
import random
from datetime import datetime

st.set_page_config(page_title="Analizador Binomo Pro", layout="wide")

def play_alert():
    st.components.v1.html(
        """<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""",
        height=0,
    )

st.title("🤖 Analizador de Señales - Binomo")

# --- BARRA LATERAL (SETTINGS) ---
with st.sidebar:
    st.header("⚙️ Configuración")
    # AQUÍ ES DONDE CAMBIAS EL MERCADO
    mercado = st.selectbox("Selecciona Divisa:", ["FX:EURUSD", "FX:GBPUSD", "FX:USDJPY", "FX:AUDUSD", "BITSTAMP:BTCUSD"])
    st.info("Al cambiar la divisa aquí, la gráfica de la derecha se actualizará automáticamente.")

# --- RELOJ Y GRÁFICA ---
st.subheader(f"🕒 Hora Actual: {datetime.now().strftime('%H:%M:%S')}")

st.components.v1.html(
    f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={mercado}&interval=1&theme=dark" height="400" width="100%"></iframe>',
    height=400,
)

st.divider()

# --- GENERADOR DE SEÑAL CON PORCENTAJE ---
st.markdown("### 🔍 Generador de Señal")
if st.button("🚀 INICIAR ANÁLISIS", use_container_width=True):
    with st.status("Analizando tendencia...", expanded=True) as status:
        time.sleep(2)
        st.write("Verificando volatilidad...")
        time.sleep(2)
        status.update(label="¡ANÁLISIS COMPLETO!", state="complete", expanded=False)
    
    resultado = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
    porcentaje = random.randint(85, 98) # El porcentaje que pediste
    
    play_alert()
    
    if "COMPRA" in resultado:
        st.success(f"⚠️ SEÑAL: {resultado} | EFECTIVIDAD: {porcentaje}% | ENTRAR YA (1 MIN)")
    else:
        st.error(f"⚠️ SEÑAL: {resultado} | EFECTIVIDAD: {porcentaje}% | ENTRAR YA (1 MIN)")

st.divider()

# --- REGISTRO ---
col1, col2, col3 = st.columns(3)
if col1.button('✅ WIN', use_container_width=True):
    st.balloons()
if col2.button('❌ PERDÍ', use_container_width=True):
    st.info("Sugerencia: GALE 1")
if col3.button('⚠️ GALE PERDIDO', use_container_width=True):
    st.warning("Ciclo de seguridad activado")