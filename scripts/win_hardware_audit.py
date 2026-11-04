"""
VISUAL STUDIO AI - Script de Auditoría de Hardware en Entorno Windows
---------------------------------------------------------------------
Este script evalúa las capacidades del sistema local para determinar
el perfil de ejecución de modelos de difusión (FLUX.1-schnell / SD1.5 / SDXL).
"""

import sys
import subprocess
import json
import platform
import psutil

def run_command(command: str) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error al ejecutar comando '{command}': {str(e)}"

def check_nvidia_gpus():
    cmd = "nvidia-smi --query-gpu=index,name,memory.total,driver_version --format=csv,noheader,nounits"
    output = run_command(cmd)
    
    if "Error" in output or not output:
        return []
    
    gpus = []
    lines = output.split('\n')
    for line in lines:
        if line.strip():
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 4:
                gpus.append({
                    "index": int(parts[0]),
                    "name": parts[1],
                    "vram_mb": int(parts[2]),
                    "driver_version": parts[3]
                })
    return gpus

def evaluate_hardware_profile():
    cpu_name = platform.processor()
    ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    disk_free_gb = round(psutil.disk_usage('.').free / (1024 ** 3), 2)
    gpus = check_nvidia_gpus()

    print("=" * 65)
    print("      VISUAL STUDIO AI - INFORME DE AUDITORÍA DE HARDWARE")
    print("=" * 65)
    print(f"Sistema Operativo: {platform.system()} {platform.release()} ({platform.architecture()[0]})")
    print(f"Procesador:        {cpu_name}")
    print(f"Memoria RAM:       {ram_gb} GB")
    print(f"Espacio en Disco:  {disk_free_gb} GB Libres")
    print("-" * 65)
    print("DISPOSITIVOS GPU DETECTADOS:")

    profile = "INSUFFICIENT"

    if not gpus:
        print("  ❌ No se detectó ninguna GPU NVIDIA accesible vía nvidia-smi.")
        print("  ⚠️ El sistema deberá ejecutarse en modo REMOTO / CLOUD.")
    else:
        for gpu in gpus:
            vram = gpu["vram_mb"]
            print(f"  • [{gpu['index']}] {gpu['name']}")
            print(f"    - VRAM Totales:   {vram} MB ({round(vram/1024, 2)} GB)")
            print(f"    - Versión Driver: {gpu['driver_version']}")

            if vram >= 16384:
                profile = "HIGH_END_FLUX"
            elif vram >= 11264:
                profile = "MID_RANGE_FLUX_FP8"
            elif vram >= 8192:
                profile = "ENTRY_LEVEL_SDXL"
            else:
                profile = "LEGACY_SD15"

    print("-" * 65)
    print("EVALUACIÓN Y RECOMENDACIÓN DE ARQUITECTURA DE MODELOS:")
    
    if profile == "HIGH_END_FLUX":
        print("  ✅ EXCELENTE: Capacidad total para ejecutar FLUX.1 [dev] / [schnell] en FP16 localmente.")
    elif profile == "MID_RANGE_FLUX_FP8":
        print("  ✅ BUENO: Capacidad para ejecutar FLUX.1 [schnell] / [dev] cuantizado a FP8 localmente.")
    elif profile == "ENTRY_LEVEL_SDXL":
        print("  ⚠️ MODERADO: Recomendado ejecutar SDXL Turbomodel / SD 1.5 con Lora / FLUX vía API remota.")
    elif profile == "LEGACY_SD15":
        print("  ⚠️ BÁSICO: Soporte local para Stable Diffusion 1.5 en baja resolución. Se recomienda API remota.")
    else:
        print("  🔴 SIN GPU LOCAL COMPATIBLE: El backend debe configurarse exclusivamente para ComfyUI Remoto o Replicate API.")

    print("=" * 65)

if __name__ == "__main__":
    evaluate_hardware_profile()