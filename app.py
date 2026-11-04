import os
import threading
import uvicorn
import requests
import streamlit as st
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ---------------------------------------------------------
# 1. SERVIDOR BACKEND (FastAPI)
# ---------------------------------------------------------
app = FastAPI(title="VISUAL STUDIO AI", version="1.0.0")

class PromptRequest(BaseModel):
    prompt: str
    aspect_ratio: str = "1:1"

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend FastAPI 24/7 activo"}

@app.post("/api/generate")
def generate_image_endpoint(data: PromptRequest):
    # Aquí se procesa el prompt de generación
    if not data.prompt.strip():
        return JSONResponse(status_code=400, content={"error": "El prompt no puede estar vacío"})
    
    # Respuesta simulada o integración de API
    return {
        "status": "success",
        "prompt": data.prompt,
        "aspect_ratio": data.aspect_ratio,
        "message": "Imagen procesada correctamente"
    }

def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

# Iniciar backend en segundo plano
if "fastapi_started" not in st.session_state:
    thread = threading.Thread(target=run_fastapi, daemon=True)
    thread.start()
    st.session_state["fastapi_started"] = True

# ---------------------------------------------------------
# 2. INTERFAZ DE USUARIO (Streamlit)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Visual Studio AI - Generador",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 VISUAL STUDIO AI")
st.subheader("Generador de Imágenes 24/7 (FastAPI + Streamlit)")

col1, col2 = st.columns([2, 1])

with col1:
    prompt_input = st.text_area(
        "Describe la imagen que deseas generar:",
        placeholder="Ej. Un paisaje futurista de Guadalajara al atardecer, estilo cyberpunk...",
        height=120
    )
    
    aspect_ratio = st.selectbox(
        "Formato de imagen:",
        ["1:1 (Cuadrado)", "16:9 (Horizontal)", "9:16 (Vertical / Stories)"]
    )
    
    btn_generate = st.button("🚀 Generar Imagen", type="primary", use_container_width=True)

with col2:
    st.markdown("### Estado del Sistema")
    try:
        res = requests.get("http://127.0.0.1:8000/health", timeout=2)
        if res.status_code == 200:
            st.success("🟢 Backend FastAPI: Conectado (127.0.0.1:8000)")
        else:
            st.warning("🟡 Backend respondiendo con estado distinto")
    except Exception:
        st.error("🔴 Backend desorganizado o iniciando...")

if btn_generate:
    if not prompt_input.strip():
        st.warning("Por favor escribe una descripción antes de generar.")
    else:
        with st.spinner("Procesando solicitud en el backend..."):
            try:
                payload = {
                    "prompt": prompt_input,
                    "aspect_ratio": aspect_ratio.split()[0]
                }
                response = requests.post("http://127.0.0.1:8000/api/generate", json=payload)
                if response.status_code == 200:
                    st.balloons()
                    st.success("¡Solicitud procesada con éxito!")
                    st.json(response.json())
                else:
                    st.error(f"Error en el servidor: {response.text}")
            except Exception as e:
                st.error(f"Error de comunicación con el Backend: {e}")