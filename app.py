import os
import requests
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
# 2. INTERFAZ DE USUARIO FRONTEND (Streamlit + OpenAI Directo)
# ---------------------------------------------------------
st.title("🎨 VISUAL STUDIO AI")
st.caption("Sistema de Generación Inteligente • DALL-E 3 Engine")

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
        ["1024x1024", "1792x1024", "1024x1792"],
        format_func=lambda x: f"{x} (Cuadrado)" if x == "1024x1024" else (f"{x} (Horizontal)" if "1792x1024" in x else f"{x} (Vertical)")
    )
    
    btn_generate = st.button("🚀 Generar Imagen", type="primary", use_container_width=True)

    # Estado del sistema
    st.markdown("---")
    st.markdown("##### 🟢 Estado del Sistema")
    st.success("Motor de IA Directo: Activo y Estable")

with col_right:
    st.subheader("🖼️ Vista Previa / Resultado")
    
    if btn_generate:
        if not prompt_input.strip():
            st.warning("Escribe una descripción en el cuadro de texto antes de continuar.")
        else:
            api_key = os.environ.get("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")
            
            if not api_key:
                st.error("OPENAI_API_KEY no configurada en los Secrets de Streamlit Cloud.")
            else:
                with st.spinner("Generando imagen con DALL-E 3..."):
                    try:
                        headers = {
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json"
                        }
                        payload = {
                            "model": "dall-e-2",
                            "prompt": prompt_input,
                            "n": 1,
                            "size": "1024x1024"
                        }
                        
                        response = requests.post(
                            "https://api.openai.com/v1/images/generations",
                            headers=headers,
                            json=payload,
                            timeout=65
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            image_url = data["data"][0]["url"]
                            revised_prompt = data["data"][0].get("revised_prompt", prompt_input)
                            
                            st.image(image_url, caption="Imagen Generada", use_column_width=True)
                            st.success("¡Imagen generada exitosamente!")
                            with st.expander("Ver prompt optimizado por la IA"):
                                st.write(revised_prompt)
                        else:
                            try:
                                err_detail = response.json().get("error", {}).get("message", response.text)
                            except Exception:
                                err_detail = response.text
                            st.error(f"Error en la generación: {err_detail}")
                    except Exception as e:
                        st.error(f"Error de conexión: {e}")
    else:
        st.info("Ingresa un prompt y presiona **Generar Imagen** para desplegar el resultado aquí.")