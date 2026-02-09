import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Bot Binomo Pro", layout="wide")

# --- FUNCIÓN PARA EL SONIDO ---
def play_alert():
    st.components.v1.html(
        """
        <audio autoplay>
            <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg">
        </audio>
        """,
        height=0,
    )

st.title("🚀 Panel Pro - Binomo Global")

# --- SELECTOR DE MERCADO Y CAPITAL ---
with st.sidebar:
    st.header("⚙️ Configuración")
    mercado = st.selectbox(
        "Selecciona el Mercado:",
        ["FX:EURUSD", "FX:GBPUSD", "FX:USDJPY", "FX:AUDUSD", "BITSTAMP:BTCUSD"]
    )
    capital = st.number_input("Monto de Inversión (USD):", min_value=1, value=10)
    st.info(f"Capital a usar: ${capital}")

# --- SECCIÓN DE RELOJ Y ALERTAS ---
col_t1, col_t2 = st.columns(2)
with col_t1:
    st.subheader(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
with col_t2:
    if st.button("🔔 Probar Sonido de Alerta"):
        play_alert()
        st.toast("Sonido funcionando")

# --- GRÁFICA DINÁMICA ---
st.components.v1.html(
    f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={mercado}&interval=1&theme=dark" height="450" width="100%"></iframe>',
    height=450,
)

# --- BOTONES DE OPERACIÓN ---
st.markdown("### ⚡ EJECUCIÓN")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("⬆️ COMPRA", use_container_width=True):
        play_alert()
        st.success(f"Compra ejecutada: ${capital}")
with c2:
    st.button("⏱️ 1 MIN", use_container_width=True)
with c3:
    if st.button("⬇️ VENTA", use_container_width=True):
        play_alert()
        st.error(f"Venta ejecutada: ${capital}")

st.divider()

# --- RESULTADOS ---
res1, res2, res3 = st.columns(3)
if res1.button('✅ WIN', use_container_width=True):
    st.balloons()
if res2.button('❌ PERDÍ', use_container_width=True):
    st.warning("Martingala sugerida: " + str(capital * 2.2))
if res3.button('⚠️ GALE PERDIDO', use_container_width=True):
    st.error("Ciclo cerrado. Reiniciar.")