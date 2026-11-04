import threading
import uvicorn
import streamlit as st
from backend.main import app as fastapi_app

def run_fastapi():
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000, log_level="warning")

@st.cache_resource
def start_backend():
    server_thread = threading.Thread(target=run_fastapi, daemon=True)
    server_thread.start()

start_backend()

st.title("Generador de Imágenes Profesionales con IA")
st.write("¡Backend de FastAPI y Frontend de Streamlit operando en sintonía 24/7!")

prompt = st.text_input("Describe tu imagen profesional:")
if st.button("Generar Imagen"):
    if prompt.strip():
        st.success(f"Generando imagen para: {prompt}")
        # Aquí puedes agregar la petición requests.post('http://127.0.0.1:8000/tu-ruta', json={"prompt": prompt})
    else:
        st.warning("Por favor ingresa una descripción válida.")