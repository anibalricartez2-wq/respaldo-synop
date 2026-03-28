import streamlit as st
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Auditoría SYNOP 87860", layout="centered")

st.title("📡 Extractor de SYNOP (SAVC)")
st.write("Consulta de tiras crudas para la estación **87860 - Comodoro Rivadavia**.")

# --- BARRA LATERAL (CONTROLES) ---
with st.sidebar:
    st.header("Configuración")
    # Selector de fecha: por defecto hoy
    fecha_consulta = st.date_input("Seleccionar Fecha", datetime.now())
    # Botón de ejecución
    btn_buscar = st.button("🚀 Buscar en Base de Datos")
    
    st.divider()
    st.info("Esta herramienta extrae los registros directamente desde Ogimet en formato de texto plano.")

# --- MOTOR DE BÚSQUEDA ---
def obtener_data(f):
    # URL técnica: pide el día completo (00 a 23 UTC) de la 87860
    url = (f"https://www.ogimet.com/display_metars2.php?lang=en&lugar=87860&tipo=synop"
           f"&fmt=txt&ano={f.year}&mes={f.month}&day={f.day}&hora=00"
           f"&anof={f.year}&mesf={f.month}&dayf={f.day}&horaf=23")
    
    headers = {'User-Agent': 'Mozilla/5.0'} # Engaña al servidor para que no bloquee al script
    
    try:
        r = requests.get(url, headers=headers, timeout=25)
        if r.status_code == 200:
            # Filtramos: solo líneas que tengan el ID 87860 y longitud de un SYNOP real
            lineas = [l.strip() for l in r.text.split('\n') if "87860" in l and len(l) > 30]
            return lineas
    except Exception as e:
        st.error(f"Error de conexión: {e}")
    return []

# --- RESULTADOS ---
if btn_buscar:
    with st.spinner(f"Escaneando registros del {fecha_consulta}..."):
        reportes = obtener_data(fecha_consulta)
        
        if reportes:
            st.success(f"Se encontraron {len(reportes)} reportes SYNOP.")
            
            # Mostramos cada tira en un bloque de código limpio
            for reporte in reportes:
                # Extraemos la hora (formato Ogimet: AAAAMMDDHHMM)
                hora_utc = f"{reporte[8:10]}:{reporte[10:12]} UTC"
                
                st.subheader(f"🕒 Reporte de las {hora_utc}")
                st.code(reporte, language="text")
            
            # Botón de descarga
            datos_txt = "\n".join(reportes)
            st.download_button(
                label="📥 Descargar tiras (.txt)",
                data=datos_txt,
                file_name=f"SYNOP_87860_{fecha_consulta}.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ No hay datos para esa fecha. Verifique si la estación reportó o intente con el día de ayer.")
else:
    st.info("Elegí una fecha a la izquierda y dale a 'Buscar'.")

st.divider()
st.caption("Uso técnico - Despacho de Aeronaves | Comodoro Rivadavia")
