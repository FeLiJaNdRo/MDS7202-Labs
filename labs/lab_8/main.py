from fastapi import FastAPI
import uvicorn

# inicializamos una instancia
app = FastAPI()

# definimos un `GET` con ruta tipo home que describa brevemente el modelo, el problema que intenta resolver, su entrada y salida.
@app.get('/') # ruta
async def home():
    return {
        'Modelo': 'XGBoost optimizado',
        'Problema que intenta resolver': 'elaborar un sistema para estimar si el agua es potable o no dado un set de mediciones',
        'Entrada': {
            "Descripción": "JSON con las mediciones físico-químicas del agua utilizando los siguientes campos:",
            "Ejemplo_Body": {
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
        },
        'Salida': '1 si es potable, 0 no lo es'
    }

# despliegue del modelo usando 'POST'
@app.post('/potabilidad/') # ruta
async def funcion_para_predecir_el_XGBOOST():
#    label = 'llamar la funcion que haga predict'+
    # placeholder
    label = 1
    return {"potabilidad": label}

# levantamiento de la app
if __name__ == '__main__':
    uvicorn.run('main:app', port = 8000)