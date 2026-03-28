import streamlit as st
import requests
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SAVC Auditor Final", layout="centered")

st.title("📡 Extractor de Emergencia SAVC")
st.write("### Estación: 87860 (Comodoro Rivadavia)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Parámetros")
    horas_atras = st.slider("Horas de historial:", 1, 48, 24)
    btn_buscar = st.button("🔍 Forzar Escaneo")
    st.divider()
    st.caption("Fuente: Iowa State University (IEM)")

# --- MOTOR DE BÚSQUEDA ---
def traer_datos_iem(hrs):
    ahora = datetime.utcnow()
    hace_x_horas = ahora - timedelta(hours=hrs)
    
    # URL de acceso directo a los logs de texto plano del IEM
    url = (f"https://mesonet.agron.iastate.edu/cgi-bin/request/asis.py?"
           f"station=SAVC&data=metar&"
           f"year1={hace_x_horas.year}&month1={hace_x_horas.month}&day1={hace_x_horas.day}&hour1={hace_x_horas.hour}&minute1=0&"
           f"year2={ahora.year}&month2={ahora.month}&day2={ahora.day}&hour2={ahora.hour}&minute2=59")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            # Limpiamos líneas vacías o encabezados
            lineas = [l.strip() for l in r.text.split('\n') if len(l) > 20]
            return lineas
    except:
        return None
    return []

# --- LÓGICA DE SALIDA ---
if btn_buscar:
    with st.spinner("Buscando en los logs de Iowa State..."):
        reportes = traer_datos_iem(horas_atras)
        
        if reportes:
            st.success(f"✅ ¡Datos recuperados! {len(reportes)} registros encontrados.")
            
            # Mostramos las tiras
            for i, reporte in enumerate(reportes):
                # Intentamos identificar si es SYNOP o METAR
                tipo = "SYNOP / RAW" if "87860" in reporte else "METAR / SPECI"
                st.info(f"📄 Registro #{i+1} - {tipo}")
                st.code(reporte, language="text")
                
            # Botón de descarga
            st.download_button("📥 Descargar Log Completo", "\n".join(reportes), "auditoria_savc.txt")
        else:
            st.error("⚠️ El servidor de Iowa tampoco tiene registros recientes para SAVC.")
            st.warning("Si esto persiste, es una caída total del nodo de comunicaciones del SMN hacia el exterior.")
else:
    st.info("Elegí el rango de horas y presioná 'Forzar Escaneo'.")

st.divider()
st.caption("SAVC 87860 - Auditoría de Despacho v3.0")
