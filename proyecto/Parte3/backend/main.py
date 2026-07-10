from fastapi import FastAPI, HTTPException
from generate_prediction import generate_prediction
from models import PredictionRequest, PredictionResponse

# Se crea la instancia de la aplicación FastAPI
app = FastAPI()


# Se define el endpoint para la predicción
@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        # Se genera la predicción utilizando la función generate_prediction
        prediction = generate_prediction(request.asunto, request.contenido)
        return PredictionResponse(prediction=prediction)

    except Exception as e:
        # Se maneja cualquier excepción y se devuelve un error HTTP 500
        raise HTTPException(status_code=500, detail=str(e)) from e
