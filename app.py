import os
import socket
import threading
import uvicorn
import requests
import streamlit as st
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

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
# 2. BACKEND SERVIDOR (FastAPI)
# ---------------------------------------------------------
app = FastAPI(title="Visual Studio AI Engine", version="1.0.0")

class PromptRequest(BaseModel):
    prompt: str
    size: str = "1024x1024"

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "FastAPI Engine 24/7"}

@app.post("/api/generate")
def generate_image_endpoint(data: PromptRequest):
    if not data.prompt.strip():
        return JSONResponse(status_code=400, content={"error": "El prompt no puede estar vacío."})

    # Obtener API Key de las variables de entorno o Secrets de Streamlit
    api_key = os.environ.get("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

    if not api_key:
        return JSONResponse(
            status_code=500, 
            content={"error": "OPENAI_API_KEY no configurada en los Secrets del servidor."}
        )

    try:
        # Petición a la API de OpenAI DALL-E 3
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "dall-e-3",
            "prompt": data.prompt,
            "n": 1,
            "size": data.size,
            "quality": "standard"
        }
        
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            res_data = response.json()
            image_url = res_data["data"][0]["url"]
            revised_prompt = res_data["data"][0].get("revised_prompt", data.prompt)
            return {
                "status": "success",
                "image_url": image_url,
                "revised_prompt": revised_prompt
            }
        else:
            # Capturar el mensaje de error explícito devuelto por OpenAI
            try:
                err_body = response.json()
                err_msg = err_body.get("error", {}).get("message", response.text)
            except Exception:
                err_msg = response.text
            return JSONResponse(status_code=response.status_code, content={"error": err_msg})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error interno: {str(e)}"})

def is_port_in_use(port: int) -> bool:
    """Verifica si el puerto del backend ya está ocupado para evitar conflictos."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_fastapi():
    if not is_port_in_use(8000):
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

# Iniciar servidor backend en segundo plano de forma segura
if "fastapi_started" not in st.session_state:
    if not is_port_in_use(8000):
        thread = threading.Thread(target=run_fastapi, daemon=True)
        thread.start()
    st.session_state["fastapi_started"] = True

# ---------------------------------------------------------
# 3. INTERFAZ DE USUARIO FRONTEND (Streamlit)
# ---------------------------------------------------------
st.title("🎨 VISUAL STUDIO AI")
st.caption("Sistema unificado 24/7 • FastAPI Engine + Streamlit UI")

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

    # Estado del servidor
    st.markdown("---")
    st.markdown("##### 🟢 Estado del Backend")
    try:
        h_res = requests.get("http://127.0.0.1:8000/health", timeout=2)
        if h_res.status_code == 200:
            st.success("FastAPI Activo en `127.0.0.1:8000`")
        else:
            st.warning("Backend respondiendo con demoras")
    except Exception:
        st.error("Iniciando servicio backend...")

with col_right:
    st.subheader("🖼️ Vista Previa / Resultado")
    
    if btn_generate:
        if not prompt_input.strip():
            st.warning("Escribe una descripción en el cuadro de texto antes de continuar.")
        else:
            with st.spinner("Conectando con FastAPI y procesando con la IA..."):
                try:
                    payload = {"prompt": prompt_input, "size": size_option}
                    response = requests.post("http://127.0.0.1:8000/api/generate", json=payload, timeout=65)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.image(data["image_url"], caption="Imagen Generada", use_container_width=True)
                        st.success("¡Imagen generada exitosamente!")
                        with st.expander("Ver prompt optimizado por la IA"):
                            st.write(data.get("revised_prompt", prompt_input))
                    else:
                        try:
                            err_detail = response.json().get("error", response.text)
                        except Exception:
                            err_detail = response.text
                        st.error(f"Error en la generación: {err_detail}")
                except Exception as e:
                    st.error(f"Error de conexión interna: {e}")
    else:
        st.info("Ingresa un prompt y presiona **Generar Imagen** para desplegar el resultado aquí.")