import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pytz

# Configuración de zona horaria para Colombia
local_tz = pytz.timezone('America/Bogota')

st.set_page_config(page_title="Analizador Dual Pro V3", layout="wide")

# --- INICIALIZACIÓN DE MEMORIA Y SISTEMA ---
if 'historial' not in st.session_state:
    st.session_state.historial = {"Wins": 0, "Loss": 0}
if 'bloqueado' not in st.session_state:
    st.session_state.bloqueado = False
if 'nivel_gale' not in st.session_state:
    st.session_state.nivel_gale = 0
if 'ultima_senal' not in st.session_state:
    st.session_state.ultima_senal = None

def play_alert():
    st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)

# --- BLOQUE 1: RELOJ ANIMADO (SEGUNDERO REAL) ---
st.components.v1.html(
    """
    <div style="background: #1e1e1e; padding: 10px; border-radius: 10px; border: 1px solid #333; text-align: center;">
        <h2 style="color: #00ff00; font-