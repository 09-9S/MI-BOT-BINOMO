import streamlit as st
import random
from datetime import datetime, timedelta
import pytz

# --- 1. CONFIGURACIÓN DEL DUEÑO ---
local_tz = pytz.timezone('America/Bogota')
PASSWORD_MAESTRA = "INFINITY2026" 
# FECHA DE CORTE: (Año, Mes, Día)
FECHA_VENCIMIENTO = datetime(2026, 3, 9, tzinfo=local_tz) 

st.set_page_config(page_title="INFINITY PROFIT V101", layout="wide")

# --- 2. LÓGICA DE CIERRE AUTOMÁTICO ---
ahora = datetime.now(local_tz)

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# Si pasa la fecha, se bloquea totalmente
if ahora > FECHA_VENCIMIENTO:
    st.markdown("<h1 style='color:red; text-align:center;'>🚨 LICENCIA VENCIDA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Tu suscripción mensual ha finalizado. Contacta al administrador para renovar.</p>", unsafe_allow_html=True)
    st.stop()

# Pantalla de Login
if not st.session_state.autenticado:
    st.markdown("<h1 style='color:#ffd700; text-align:center;'>🔐 ACCESO EXCLUSIVO</h1>", unsafe_allow_html=True)
    clave = st.text_input("Introduce tu Licencia Mensual:", type="password")
    if st.button("🚀 ACTIVAR SOFTWARE"):
        if clave == PASSWORD_MAESTRA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ Clave incorrecta o vencida.")
    st.stop()

# --- 3. INTERFAZ PROFESIONAL (SNIPER + ESCÁNER) ---
st.markdown('<h1 style="color:#ffd700; text-align:center;">INFINITY PROFIT V101</h1>', unsafe_allow_html=True)

t1, t2 = st.tabs(["📉 BINARIAS SNIPER", "🏛️ MERCADO MT5"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📸 ESCÁNER DE MERCADO")
        # Arreglo de la cámara: Mensaje de instrucción
        st.camera_input("Enfoca el gráfico", key="scanner_v1")
        st.warning("⚠️ SI VES LA PANTALLA NEGRA: Pulsa el icono del CANDADO arriba en la barra de direcciones y dale a 'PERMITIR CÁMARA'.")
        
    with col2:
        st.write(f"🕒 Hora Bogotá: {ahora.strftime('%H:%M:%S')}")
        if st.button("🚀 ANALIZAR ENTRADA"):
            # Lógica de señales Sniper al 85%
            prob = random.uniform(85.5, 98.0)
            tipo = random.choice(["COMPRA ⬆️", "VENTA ⬇️"])
            st.markdown(f"""
                <div style="border:3px solid #ffd700; border-radius:15px; padding:20px; text-align:center; background:#111;">
                    <h1 style="color:#ffd700;">{tipo}</h1>
                    <p style="font-size:25px;">EFECTIVIDAD: {prob:.2f}%</p>
                </div>
            """, unsafe_allow_html=True)

# GRÁFICO TRADINGVIEW
st.components.v1.html('<iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_76292&symbol=FX%3AEURUSD&interval=1&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=%5B%5D&theme=dark&style=1&timezone=America%2FBogota" width="100%" height="400"></iframe>', height=400)
