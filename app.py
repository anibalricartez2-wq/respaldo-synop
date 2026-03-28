import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SAVC SYNOP Auditor", layout="centered")

st.title("📡 Extractor SYNOP 87860")
st.write("### Fuente: NOAA Aviation Weather (SAVC)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Consulta")
    # Para la NOAA, pedimos las últimas horas de datos
    horas = st.slider("Horas hacia atrás:", 1, 48, 24)
    btn_buscar = st.button("🔍 Buscar Registros")
    st.divider()
    st.caption("Esta fuente es la más estable para despachantes.")

# --- MOTOR DE BÚSQUEDA ---
def traer_datos_noaa(hrs):
    # La NOAA nos da los datos crudos (incluyendo el SYNOP si está en el buffer)
    url = f"https://www.aviationweather.gov/cgi-bin/data/metar.php?ids=SAVC&hours={hrs}&format=raw"
    
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200 and len(r.text.strip()) > 10:
            return r.text.strip().split('\n')
    except:
        return None
    return []

# --- LÓGICA DE SALIDA ---
if btn_buscar:
    with st.spinner(f"Consultando servidor de la NOAA..."):
        reportes = traer_datos_noaa(horas)
        
        if reportes:
            st.success(f"✅ Se encontraron {len(reportes)} registros en las últimas {horas} horas.")
            
            # Mostramos los reportes
            for reporte in reportes:
                # Si el reporte es un SYNOP (empieza con 87860 o tiene formato numérico largo)
                # O si es el METAR que contiene información operativa
                st.code(reporte, language="text")
                
            # Botón de descarga
            st.download_button("📥 Descargar Reportes", "\n".join(reportes), "reportes_savc.txt")
        else:
            st.error("❌ No se recibieron datos del servidor central.")
else:
    st.info("Elegí el rango de horas y dale a Buscar. (Sugerido: 24hs)")

st.divider()
st.caption("Repocitorio Limpio v2.0 - Conexión NOAA Directa")
