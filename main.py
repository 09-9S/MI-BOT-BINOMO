import streamlit as st

st.set_page_config(page_title="Bot Binomo VIP", layout="wide")
st.title("📊 Panel de Control - Bot Binomo")

# Gráfica
st.components.v1.html(
    '<iframe src="https://s.tradingview.com/widgetembed/?symbol=FX%3AEURUSD&theme=dark" width="100%" height="400"></iframe>',
    height=400,
)

# Botones
col1, col2, col3 = st.columns(3)
if col1.button('✅ WIN', use_container_width=True):
    st.success("¡Operación Ganada!")
if col2.button('❌ PERDÍ', use_container_width=True):
    st.error("Operación Perdida.")
if col3.button('⚠️ GALE PERDIDO', use_container_width=True):
    st.warning("Bloqueando por seguridad (8,000 + 8,800).")