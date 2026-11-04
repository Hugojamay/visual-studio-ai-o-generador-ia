import urllib.parse
import streamlit as st

# ---------------------------------------------------------
# 1. CONFIGURACIÓN Y ESTILOS DE LA INTERFAZ (Visual Studio AI Pro)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Visual Studio AI Pro",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS Avanzado (Dark Theme Pro + Tarjetas Estilizadas)
st.markdown("""
<style>
    /* Fondo principal y tipografía */
    .main { background-color: #090a0f; color: #e2e8f0; }
    
    /* Contenedores y tarjetas */
    div.stButton > button {
        background: linear-gradient(135deg, #007acc 0%, #005999 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1rem;
        box-shadow: 0 4px 12px rgba(0, 122, 204, 0.3);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #0099ff 0%, #007acc 100%);
        box-shadow: 0 6px 16px rgba(0, 153, 255, 0.5);
        transform: translateY(-1px);
    }
    
    /* Cajas de texto y selectores */
    .stTextArea textarea {
        background-color: #12151e;
        color: #f8fafc;
        border-radius: 10px;
        border: 1px solid #262b3d;
        padding: 12px;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: #12151e;
        border-radius: 8px;
        border: 1px solid #262b3d;
    }
    
    /* Tarjetas de estado y contenedores laterales */
    .css-1d391kg { background-color: #0d1117; }
    
    /* Encabezados y títulos */
    h1, h2, h3 {
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. BARRA LATERAL (Presets y Configuración Pro)
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.markdown("### **Visual Studio AI**")
    st.caption("Suite de Generación Visual Profesional")
    
    st.markdown("---")
    st.markdown("#### ⚡ Estilos Rápidos (Presets)")
    preset_choice = st.selectbox(
        "Elige un estilo base:",
        [
            "Ninguno (Personalizado)",
            "Cyberpunk Neon 8k",
            "Fotografía Cinematográfica Realista",
            "Arte Digital Minimalista",
            "Fantasía Épica / Concept Art",
            "Anime / Manga High Quality"
        ]
    )
    
    # Asignar sufijos según el preset elegido
    preset_modifier = ""
    if "Cyberpunk" in preset_choice:
        preset_modifier = ", cyberpunk neon lighting, futuristic city, 8k resolution, highly detailed"
    elif "Cinematográfica" in preset_choice:
        preset_modifier = ", cinematic lighting, photorealistic, dramatic shadows, 35mm lens, 8k"
    elif "Minimalista" in preset_choice:
        preset_modifier = ", minimalist design, clean vector aesthetics, elegant composition, modern art"
    elif "Fantasía" in preset_choice:
        preset_modifier = ", epic fantasy concept art, intricate details, magical glow, masterpiece"
    elif "Anime" in preset_choice:
        preset_modifier = ", high quality anime style, vibrant colors, studio ghibli aesthetic, sharp lines"

    st.markdown("---")
    st.markdown("#### 🛠️ Estado de Conexión")
    st.success("🟢 Motor Neural: En Línea")
    st.info("💎 Licencia: 100% Gratuita / Ilimitada")

# ---------------------------------------------------------
# 3. INTERFAZ PRINCIPAL (Layout de Dos Columnas Profesional)
# ---------------------------------------------------------
st.title("🎨 VISUAL STUDIO AI — STUDIO PRO")
st.markdown("Transforma tus ideas en obras maestras visuales de calidad comercial al instante.")
st.markdown("")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("### ✏️ Configuración del Prompt")
    
    user_prompt = st.text_area(
        "Describe tu imagen en detalle:",
        placeholder="Ej: Un lobo cibernético con detalles dorados en un bosque místico de neón...",
        height=150
    )
    
    # Combinar prompt con el preset si se seleccionó uno
    final_prompt = user_prompt + preset_modifier if user_prompt else ""

    col_res1, col_res2 = st.columns(2)
    with col_res1:
        size_option = st.selectbox(
            "Resolución:",
            ["1024x1024", "1280x720", "720x1280"],
            format_func=lambda x: f"{x} (Cuadrado)" if x == "1024x1024" else (f"{x} (Horizontal)" if "1280x720" in x else f"{x} (Vertical)")
        )
    with col_res2:
        engine_mode = st.selectbox(
            "Motor de Render:",
            ["Standard HD", "Ultra Details +"]
        )

    st.markdown("")
    btn_generate = st.button("🚀 Renderizar Imagen Pro", use_container_width=True)

with col_right:
    st.markdown("### 🖼️ Lienzo de Resultados")
    
    if btn_generate:
        if not user_prompt.strip():
            st.warning("⚠️ Por favor, ingresa una descripción en el cuadro de texto para comenzar.")
        else:
            with st.spinner("✨ Sintetizando píxeles, aplicando motor neuronal..."):
                try:
                    # Codificar prompt de forma segura para la URL
                    encoded_prompt = urllib.parse.quote(final_prompt)
                    w, h = size_option.split("x")
                    
                    # Generar URL de renderizado optimizado
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={w}&height={h}&nologo=true"
                    
                    st.image(image_url, caption="Renderizado Exitosamente • Visual Studio AI", use_column_width=True)
                    st.success("¡Obra maestra generada con éxito!")
                    
                    with st.expander("🔍 Ver prompt completo procesado"):
                        st.code(final_prompt, language="text")
                        
                except Exception as e:
                    st.error(f"Error en el proceso de renderizado: {e}")
    else:
        # Contenedor visual elegante cuando aún no hay imagen
        st.markdown("""
        <div style="border: 2px dashed #262b3d; border-radius: 12px; padding: 40px; text-align: center; background-color: #12151e;">
            <p style="color: #64748b; font-size: 16px; margin: 0;">Tu imagen generada aparecerá aquí en alta resolución.</p>
            <p style="color: #475569; font-size: 13px; margin-top: 8px;">Configura tus parámetros a la izquierda y presiona renderizar.</p>
        </div>
        """, unsafe_allow_html=True)