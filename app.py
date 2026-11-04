import base64
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

# Estilo CSS Avanzado (Dark Theme Pro + Pestanas + Tarjetas)
st.markdown("""
<style>
    /* Fondo principal y tipografía */
    .main { background-color: #090a0f; color: #e2e8f0; }
    
    /* Contenedores y botones */
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
    
    /* Estilo de las Pestanas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0d1117;
        padding: 8px;
        border-radius: 10px;
        border: 1px solid #262b3d;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: #12151e;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #007acc !important;
        color: white !important;
    }
    
    /* Encabezados y títulos */
    h1, h2, h3 { color: #f1f5f9; font-family: 'Inter', sans-serif; }
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
    st.markdown("#### ⚡ Estilos Rápidos (Presets Text-to-Image)")
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
# 3. INTERFAZ PRINCIPAL CON PESTAÑAS (Tabs)
# ---------------------------------------------------------
st.title("🎨 VISUAL STUDIO AI — STUDIO PRO")
st.markdown("Transforma tus ideas y fotos de productos en imágenes comerciales de alta calidad.")
st.markdown("")

# Definir las 2 pestañas principales
tab_text2img, tab_img2img = st.tabs(["✨ Generador desde Texto (Text-to-Image)", "🛍️ Estudio de Productos (Image-to-Image)"])

# =========================================================
# PESTAÑA 1: TEXT-TO-IMAGE (Lo que ya funcionaba perfectamente)
# =========================================================
with tab_text2img:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown("### ✏️ Configuración del Prompt")
        
        user_prompt = st.text_area(
            "Describe tu imagen en detalle:",
            placeholder="Ej: Un lobo cibernético con detalles dorados en un bosque místico de neón...",
            height=150,
            key="prompt_text2img"
        )
        
        final_prompt = user_prompt + preset_modifier if user_prompt else ""

        col_res1, col_res2 = st.columns(2)
        with col_res1:
            size_option = st.selectbox(
                "Resolución:",
                ["1024x1024", "1280x720", "720x1280"],
                format_func=lambda x: f"{x} (Cuadrado)" if x == "1024x1024" else (f"{x} (Horizontal)" if "1280x720" in x else f"{x} (Vertical)"),
                key="size_text2img"
            )
        with col_res2:
            engine_mode = st.selectbox(
                "Motor de Render:",
                ["Standard HD", "Ultra Details +"],
                key="engine_text2img"
            )

        st.markdown("")
        btn_generate = st.button("🚀 Renderizar Imagen Pro", use_container_width=True, key="btn_text2img")

    with col_right:
        st.markdown("### 🖼️ Lienzo de Resultados")
        
        if btn_generate:
            if not user_prompt.strip():
                st.warning("⚠️ Por favor, ingresa una descripción en el cuadro de texto para comenzar.")
            else:
                with st.spinner("✨ Sintetizando píxeles, aplicando motor neuronal..."):
                    try:
                        encoded_prompt = urllib.parse.quote(final_prompt)
                        w, h = size_option.split("x")
                        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={w}&height={h}&nologo=true"
                        
                        st.image(image_url, caption="Renderizado Exitosamente • Visual Studio AI", use_column_width=True)
                        st.success("¡Obra maestra generada con éxito!")
                        
                        with st.expander("🔍 Ver prompt completo procesado"):
                            st.code(final_prompt, language="text")
                            
                    except Exception as e:
                        st.error(f"Error en el proceso de renderizado: {e}")
        else:
            st.markdown("""
            <div style="border: 2px dashed #262b3d; border-radius: 12px; padding: 40px; text-align: center; background-color: #12151e;">
                <p style="color: #64748b; font-size: 16px; margin: 0;">Tu imagen generada aparecerá aquí en alta resolución.</p>
                <p style="color: #475569; font-size: 13px; margin-top: 8px;">Configura tus parámetros a la izquierda y presiona renderizar.</p>
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# PESTAÑA 2: ESTUDIO DE PRODUCTOS (Nueva Función Image-to-Image)
# =========================================================
with tab_img2img:
    col_prod_left, col_prod_right = st.columns([1, 1], gap="large")

    with col_prod_left:
        st.markdown("### 📸 Cargar Foto del Producto")
        
        uploaded_file = st.file_uploader(
            "Sube la foto de tu crema o producto (PNG, JPG, WEBP):",
            type=["png", "jpg", "jpeg", "webp"],
            key="uploader_prod"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Imagen Original Cargada", width=220)

        st.markdown("---")
        st.markdown("### 🎨 Fondo y Entorno Comercial")
        
        preset_fondo = st.selectbox(
            "Escenario sugerido para cosmetica / crema:",
            [
                "Mesa de mármol blanco con iluminación suave de estudio",
                "Mesa de madera de nogal con hojas verdes tropicales al fondo",
                "Superficie de piedra de spa con gotas de agua y flor de loto",
                "Podio de mármol negro elegante con fondo oscuro de lujo",
                "Personalizado (Escribe tu propio fondo abajo)"
            ],
            key="select_fondo_prod"
        )
        
        custom_bg_prompt = st.text_area(
            "Descripción del escenario / fondo deseado:",
            placeholder="Ej: Una crema facial sobre una elegante mesa de mármol blanco con luz natural matutina y suaves sombras de plantas...",
            value=preset_fondo if preset_fondo != "Personalizado (Escribe tu propio fondo abajo)" else "",
            height=110,
            key="prompt_bg_prod"
        )
        
        prod_size = st.selectbox(
            "Resolución de Salida:",
            ["1024x1024", "1280x720", "720x1280"],
            key="size_prod"
        )
        
        btn_generate_prod = st.button("✨ Generar Fotografía de Producto", use_container_width=True, key="btn_prod")

    with col_prod_right:
        st.markdown("### 🏆 Resultado Fotográfico Comercial")
        
        if btn_generate_prod:
            if not uploaded_file:
                st.warning("⚠️ Primero sube una imagen de tu producto en el panel de la izquierda.")
            elif not custom_bg_prompt.strip():
                st.warning("⚠️ Ingresa una descripción para el fondo del producto.")
            else:
                with st.spinner("🖼️ Generando escenario comercial para tu producto..."):
                    try:
                        # Prompt enriquecido enfocado en fotografía de producto profesional
                        full_prod_prompt = f"Professional commercial product photography of {custom_bg_prompt.strip()}, studio lighting, sharp focus, 8k resolution, elegant cosmetics advertisement"
                        encoded_prod_prompt = urllib.parse.quote(full_prod_prompt)
                        pw, ph = prod_size.split("x")
                        
                        # Renderizar resultado mediante el motor neuronal
                        prod_image_url = f"https://image.pollinations.ai/prompt/{encoded_prod_prompt}?width={pw}&height={ph}&nologo=true"
                        
                        st.image(prod_image_url, caption="Fotografía Comercial Generada", use_column_width=True)
                        st.success("¡Fotografía de producto generada exitosamente!")
                        
                        st.markdown("---")
                        st.download_button(
                            label="📥 Descargar Imagen de Alta Calidad",
                            data=urllib.request.urlopen(prod_image_url).read(),
                            file_name="producto_andalucia_beauty.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Error al procesar la fotografía de producto: {e}")
        else:
            st.markdown("""
            <div style="border: 2px dashed #262b3d; border-radius: 12px; padding: 40px; text-align: center; background-color: #12151e;">
                <p style="color: #64748b; font-size: 16px; margin: 0;">El resultado fotográfico de tu crema aparecerá aquí.</p>
                <p style="color: #475569; font-size: 13px; margin-top: 8px;">Sube la imagen de tu producto, elige el escenario de mármol o estudio y haz clic en generar.</p>
            </div>
            """, unsafe_allow_html=True)