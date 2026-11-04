import threading
import uvicorn
import streamlit as st
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# 1. Instanciar FastAPI directamente sin dependencias circulares
app = FastAPI(title="VISUAL STUDIO AI")

@app.get("/")
def read_root():
    return {"message": "FastAPI backend funcionando correctamente"}

# 2. Función para ejecutar uvicorn en segundo plano
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

# Iniciar el hilo de FastAPI una sola vez
if "fastapi_running" not in st.session_state:
    thread = threading.Thread(target=run_fastapi, daemon=True)
    thread.start()
    st.session_state["fastapi_running"] = True

# 3. Interfaz de Streamlit
st.title("VISUAL STUDIO AI - Panel Principal")
st.write("El servidor backend y la interfaz corren de forma unificada.")

if st.button("Probar conexión con Backend"):
    import requests
    try:
        response = requests.get("http://127.0.0.1:8000/")
        st.success(f"Conexión exitosa: {response.json()}")
    except Exception as e:
        st.error(f"Error de conexión: {e}")