import pickle
import os
from fastapi import FastAPI, Body
import pandas as pd
import uvicorn
import mlflow


# Configuración de rutas relativas al archivo main.py (Búsqueda local en labs/lab_8)
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
# Buscamos la carpeta 'models' que está justo al lado de este archivo main.py
MODEL_PATH = os.path.normpath(os.path.join(DIRECTORIO_ACTUAL, "models", "best_model.pkl"))

# Cargamos el modelo 
try:
    with open(MODEL_PATH, "rb") as file:
        modelo = pickle.load(file)
    print("-> Mejor modelo XGBoost cargado con éxito")
except Exception as e:
    modelo = None
    print(f"-> ALERTA: No se pudo cargar el archivo pickle. Error: {e}")

# Inicializamos la instancia
app = FastAPI()

# Definimos un GET 
@app.get('/') # ruta
async def home():
    return {
        'Modelo': 'XGBoost optimizado',
        'Problema que intenta resolver': 'elaborar un sistema para estimar si el agua es potable o no dado un set de mediciones',
        'Entrada': {
            "Descripción": "JSON con las mediciones físico-químicas del agua utilizando los siguientes campos:",
            "Variables": ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
        },
        'Salida': '1 si es potable, 0 no lo es'
    }


@app.post('/potabilidad/')
async def prediccion_XGBOOST(
    medicion: dict = Body(
        ...,
        openapi_examples={
            "Ejemplo Valido": {
                "summary": "Datos de prueba del laboratorio",
                "value": {
                    "ph": 10.316400384553162,
                    "Hardness": 217.2668424334475,
                    "Solids": 10676.508475429378,
                    "Chloramines": 3.445514571005745,
                    "Sulfate": 397.7549459751925,
                    "Conductivity": 492.20647361771086,
                    "Organic_carbon": 12.812732207582542,
                    "Trihalomethanes": 72.28192021570328,
                    "Turbidity": 3.4073494284238364
                }
            }
        }
    )
):
    if modelo is None:
        return {"error": "El modelo predictivo no está cargado."}

    # creamos DataFrame directo
    df_entrada = pd.DataFrame([medicion])
    
    # Alineamiento exacto de columnas según el entrenamiento de optimize.py
    columnas_entrenamiento = [
        'ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 
        'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity'
    ]
    df_entrada = df_entrada[columnas_entrenamiento]
    
    # pasar a float por si acaso
    df_entrada = df_entrada.astype(float)
    
    # Predicción
    prediccion = modelo.predict(df_entrada)[0]
    
    return {"potabilidad": int(prediccion)}

# Levantamiento de la app 
if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000)