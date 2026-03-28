import streamlit as st
import requests

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SAVC Auditor Final", layout="centered")

st.title("📡 Extractor de Fondo SAVC")
st.write("### Estación: 87860 (Comodoro Rivadavia)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Control de Extracción")
    n_reportes = st.slider("Cantidad de reportes a recuperar:", 10, 100, 50)
    btn_forzar = st.button("🔥 Forzar Extracción de Buffer")
    st.divider()
    st.caption("Esta función busca en la memoria profunda del servidor.")

# --- MOTOR DE BÚSQUEDA (BUFFER RECENT) ---
def extraer_buffer_ogimet(cantidad):
    # Esta URL pide los últimos N reportes SYNOP de la estación, sin filtrar por fecha
    url = f"https://www.ogimet.com/display_metars2.php?lang=en&lugar=87860&tipo=synop&fmt=txt&send=send&max={cantidad}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=25)
        if r.status_code == 200:
            # Buscamos las líneas que tengan el ID 87860
            lineas = [l.strip() for l in r.text.split('\n') if "87860" in l and len(l) > 30]
            return lineas
    except:
        return None
    return []

# --- LÓGICA DE SALIDA ---
if btn_forzar:
    with st.spinner("Accediendo al buffer de Ogimet..."):
        reportes = extraer_buffer_ogimet(n_reportes)
        
        if reportes:
            st.success(f"✅ ¡Éxito! Se recuperaron {len(reportes)} registros del historial.")
            
            for i, reporte in enumerate(reportes):
                # Extraer fecha/hora del reporte para el título
                # Ogimet pone AAAAMMDDHHMM al principio
                try:
                    fecha_str = f"{reporte[6:8]}/{reporte[4:6]} {reporte[8:10]}:{reporte[10:12]} UTC"
                except:
                    fecha_str = f"Registro {i+1}"
                
                st.info(f"🕒 **Reporte: {fecha_str}**")
                st.code(reporte, language="text")
                
            st.download_button("📥 Descargar Buffer", "\n".join(reportes), "buffer_savc.txt")
        else:
            st.error("❌ El buffer de Ogimet para la 87860 está vacío.")
            st.warning("Esto confirma que la estación SAVC no está inyectando datos a la red internacional (GTS) en este momento.")
else:
    st.info("Presioná el botón para intentar recuperar los últimos reportes guardados en el servidor.")

st.divider()
st.caption("SAVC 87860 - Auditoría v4.0 (Buffer Mode)")
