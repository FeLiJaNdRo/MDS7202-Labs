from typing import Literal

from pydantic import BaseModel


# Se definen la clase PredictionRequest para la solicitud
class PredictionRequest(BaseModel):
    asunto: str
    contenido: str


# Se define la clase PredictionResponse para la respuesta de predicción
class PredictionResponse(BaseModel):
    prediction: Literal["Baja", "Media", "Alta", "Critica"]
