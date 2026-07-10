import logging
from pathlib import Path

import cloudpickle
import pandas as pd
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

log = logging.getLogger(__name__)

# Se carga Google API Key desde el archivo .env local (no se sube a GitHub)
load_dotenv(Path(__file__).resolve().parent / ".env")

# Constantes que reflejan EXACTAMENTE el entrenamiento (Parte 2)
MODEL_PATH = Path(__file__).resolve().parent / "modelo_final.pkl"
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIM = 1024

# nombres 1-indexados
EMBEDDING_COLS = [f"embedding_dim_{i}" for i in range(1, EMBEDDING_DIM + 1)]


# Se carga el pipeline entrenado desde el .pickle (cloudpickle, no pickle estándar)
def _cargar_pipeline():
    """Carga el pipeline entrenado desde el .pickle"""
    with open(MODEL_PATH, "rb") as f:
        return cloudpickle.load(f)


def generate_prediction(asunto: str, contenido: str) -> str:
    """Genera la predicción de Nivel_Prioridad para un ticket nuevo"""

    # Se construye el texto exactamente igual a como se generaron los embeddings originales
    texto = f"Asunto_Ticket: {asunto}\nContenido_Ticket: {contenido}\n"
    log.info("Texto construido para embedding (%d caracteres)", len(texto))

    # Se vectoriza con el mismo modelo y dimensión usados en entrenamiento
    embedding_client = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        output_dimensionality=EMBEDDING_DIM,
    )
    vector = embedding_client.embed_query(texto)
    log.info("Embedding generado: dimensión %d", len(vector))

    # Se arma el input tal como lo espera el ColumnTransformer del pipeline
    X_nuevo = pd.DataFrame([vector], columns=EMBEDDING_COLS)

    # Se carga el pipeline y se predice
    pipeline = _cargar_pipeline()
    prediccion = pipeline.predict(X_nuevo)[0]
    log.info("Predicción generada: %s", prediccion)

    # Se retorna la predicción
    return prediccion


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Ejemplo de ejecución directa
    ejemplo_asunto = "Cargo desconocido en mi tarjeta"
    ejemplo_contenido = "Hola, buenas, escribo porque me apareció un cargo en mi tarjeta de $1.500.000 que no reconozco. Necesito que revisen esto urgente porque no fui yo, y necesto ese dinero para pagar mis cuentas."

    resultado = generate_prediction(asunto=ejemplo_asunto, contenido=ejemplo_contenido)
    print(f"Predicción de Nivel_Prioridad: {resultado}")
