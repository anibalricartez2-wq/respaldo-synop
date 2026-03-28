import streamlit as st
import requests
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SAVC SYNOP Auditor", layout="centered")

st.title("📡 Extractor SYNOP 87860")
st.write("### Estación: Comodoro Rivadavia (SAVC)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Consulta")
    fecha_consulta = st.date_input("Fecha:", datetime.now())
    btn_buscar = st.button("🔍 Buscar Registros")
    st.divider()
    st.caption("Fuente: Ogimet (Texto Plano)")

# --- MOTOR DE BÚSQUEDA ---
def traer_synop(f):
    # Intentamos traer desde las 00 UTC hasta las 23 UTC
    url = (f"https://www.ogimet.com/display_metars2.php?lang=en&lugar=87860&tipo=synop"
           f"&fmt=txt&ano={f.year}&mes={f.month}&day={f.day}&hora=00"
           f"&anof={f.year}&mesf={f.month}&dayf={f.day}&horaf=23")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            # Buscamos la tira que contenga el ID 87860
            lineas = [l.strip() for l in r.text.split('\n') if "87860" in l and len(l) > 30]
            return lineas
    except:
        return None
    return []

# --- LÓGICA DE SALIDA ---
if btn_buscar:
    with st.spinner("Conectando con el servidor global..."):
        reportes = traer_synop(fecha_consulta)
        
        if reportes:
            st.success(f"✅ Se encontraron {len(reportes)} tiras SYNOP.")
            for reporte in reportes:
                # Extraemos la hora para que sea fácil de leer
                # El formato de Ogimet suele ser AAAAMMDDHHMM al inicio
                hora_utc = f"{reporte[8:10]}:{reporte[10:12]} UTC"
                st.info(f"🕒 **Reporte de las {hora_utc}**")
                st.code(reporte, language="text")
        else:
            st.error("❌ No hay datos para esta fecha todavía.")
            st.warning("💡 **Tip de Despachante:** Si es temprano en la mañana, probá seleccionando el día de AYER. Ogimet a veces tarda 2 o 3 horas en indexar el reporte actual.")
else:
    st.info("Elegí una fecha y dale a Buscar. (Probá con la fecha de ayer si hoy da vacío)")

st.divider()
st.caption("Proyecto Limpio - v1.0")
