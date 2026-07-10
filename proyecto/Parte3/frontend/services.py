import os

import requests


def enviar_prediccion(asunto: str, contenido: str) -> str:
    """Realiza la llamada API hacia el endpoint de predicción y retorna el Nivel_Prioridad."""

    # Leer backend url desde variables de entorno
    backend_url = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

    # Construir la URL completa del endpoint de predicción
    url = f"{backend_url}/predict"

    try:
        # Realizar la llamada API real al backend de FastAPI
        response = requests.post(
            url,
            json={"asunto": asunto, "contenido": contenido},
            timeout=30,
        )
    except requests.exceptions.RequestException as e:
        # Cubre errores de conexión
        return f"Error de conexión con el backend: {e}"

    # Manejar caso específico de error de validación (422)
    if response.status_code == 422:
        return f"Error de validación: {response.text}"

    # Manejar cualquier otro error HTTP
    if response.status_code != 200:
        return f"Error en la llamada API ({response.status_code}): {response.text}"

    # Extraer el campo 'prediction' del JSON de respuesta
    return response.json()["prediction"]
