import urllib.parse
import streamlit as st

# ---------------------------------------------------------
# 1. CONFIGURACIÓN Y ESTILOS DE LA INTERFAZ (Estilo VS AI)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Visual Studio AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado CSS (Dark Theme + Cards)
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { background-color: #1e1e2e; color: #ffffff; border-radius: 8px; border: 1px solid #313244; }
    .stButton>button { background-color: #007acc; color: white; border-radius: 6px; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #005999; color: white; }
    .status-card { padding: 15px; border-radius: 8px; background-color: #181825; border: 1px solid #313244; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. INTERFAZ DE USUARIO FRONTEND (Streamlit + Motor Gratuito)
# ---------------------------------------------------------
st.title("🎨 VISUAL STUDIO AI")
st.caption("Sistema de Generación Inteligente • 100% Gratuito y Sin Límites")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("⚡ Parámetros de Generación")
    
    prompt_input = st.text_area(
        "Prompt de la imagen:",
        placeholder="Ej: Un león cibernético rodeado de luces de neón en estilo arte digital 8k...",
        height=140
    )
    
    size_option = st.selectbox(
        "Resolución / Tamaño:",
        ["1024x1024", "1280x720", "720x1280"],
        format_func=lambda x: f"{x} (Cuadrado)" if x == "1024x1024" else (f"{x} (Horizontal)" if "1280x720" in x else f"{x} (Vertical)")
    )
    
    btn_generate = st.button("🚀 Generar Imagen Gratis", type="primary", use_container_width=True)

    # Estado del sistema
    st.markdown("---")
    st.markdown("##### 🟢 Estado del Sistema")
    st.success("Motor Gratuito: Activo y Sin Restricciones")

with col_right:
    st.subheader("🖼️ Vista Previa / Resultado")
    
    if btn_generate:
        if not prompt_input.strip():
            st.warning("Escribe una descripción en el cuadro de texto antes de continuar.")
        else:
            with st.spinner("Generando imagen de alta calidad gratis..."):
                try:
                    # Codificar el prompt para la URL de forma segura
                    encoded_prompt = urllib.parse.quote(prompt_input)
                    
                    # Separar ancho y alto de la resolución seleccionada
                    w, h = size_option.split("x")
                    
                    # URL del motor de generación gratuito de alta calidad
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={w}&height={h}&nologo=true"
                    
                    st.image(image_url, caption="Imagen Generada Exitosamente", use_column_width=True)
                    st.success("¡Imagen generada 100% gratis y sin recargas!")
                except Exception as e:
                    st.error(f"Error de generación: {e}")
    else:
        st.info("Ingresa un prompt y presiona **Generar Imagen Gratis** para desplegar el resultado aquí.")