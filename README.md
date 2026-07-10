# MDS7202 - Laboratorio de Programación Científica para Ciencia de Datos

Repositorio del curso MDS7202 (Otoño 2026), Facultad de Ciencias Físicas y Matemáticas, Universidad de Chile.

Este repositorio contiene los laboratorios (`labs/`) y el proyecto de curso (`proyecto/`), organizados por carpetas según cada entrega.

## Integrantes

| Nombre | GitHub |
|--------|--------|
| Felipe Muñoz M. | [@FeLiJaNdRo](https://github.com/FeLiJaNdRo/FelipeMunozM) |
| Nombre Apellido 2 | [@aplandaeta](https://github.com/aplandaeta/aplandaeta) |

## Estructura del repositorio

```
.
├── labs/                               # Laboratorios semanales
│   ├── lab_1/                          # Introducción a Python científico
│   │   └── Laboratorio_1.ipynb
│   ├── lab_2/                          # Procesamiento de imágenes
│   │   ├── images_lab/
│   │   └── Laboratorio_2.ipynb
│   ├── lab_3/
│   │   └── Lab3_Enunciado.ipynb
│   ├── lab_4/                          # Clustering (Online Retail)
│   │   ├── Lab4_Enunciado.ipynb
│   │   └── online_retail_I.pickle, online_retail_II.pickle
│   ├── lab_5/
│   │   └── Lab5_enunciado.ipynb
│   ├── lab_6/                          # Regresión (Precios Casas RM)
│   │   ├── Lab6_Enunciado.ipynb
│   │   ├── Precios Casas RM.csv
│   │   ├── documentacion_dataset.md
│   │   └── ingresos_por_comuna_2024.xlsx
│   ├── lab_7/                          # Optimización de hiperparámetros (Optuna)
│   │   ├── Lab7_final.ipynb
│   │   ├── comics_no_label.csv, df_comics.csv
│   │   ├── optuna_lab7.db
│   │   └── Importanciahiperparametros.png, Optimizacionhistorial.png, PFI.png, Paralelas.png
│   ├── lab_8/                          # Despliegue con FastAPI + Docker
│   │   ├── Lab8.ipynb
│   │   ├── main.py, optimize.py
│   │   ├── models/, plots/
│   │   ├── Dockerfile, .dockerignore
│   │   ├── requirements.txt
│   │   ├── water_potability.csv
│   │   └── optuna_lab8.db
│   ├── lab_9/                          # Orquestación de pipelines (Airflow)
│   │   ├── Lab9.ipynb
│   │   ├── dags/
│   │   ├── data/, logs/dag_processor/
│   │   ├── airflow.cfg, airflow.db
│   │   └── lab_8.zip
│   └── lab_10/                         # RAG con FAISS
│       ├── Lab10_enunciado.ipynb
│       ├── faiss_index_edo/, faiss_index_organiza/
│       └── Apunte_EDO.pdf, Apuntes_Organizacion_Industrial.pdf
│
├── proyecto/                           # Proyecto del curso
│   ├── Parte1/                         # Análisis exploratorio
│   │   ├── Enunciado_Parte1_Analisis.ipynb
│   │   └── img/
│   ├── Parte2/                         # Modelamiento
│   │   ├── Enunciado_Parte2_Modelo.ipynb
│   │   ├── modelo_final.pkl
│   │   └── mlflow.db
│   └── Parte3/                         # Despliegue (backend + frontend)
│       ├── Enunciado_Parte3_Despliegue.ipynb
│       ├── docker-compose.yaml
│       ├── chaucherapp.jpg
│       ├── data/
│       ├── backend/                    # API FastAPI de predicción
│       │   ├── main.py, models.py, generate_prediction.py
│       │   ├── modelo_final.pkl
│       │   ├── Dockerfile, .dockerignore
│       │   └── pyproject.toml, uv.lock
│       └── frontend/                   # Interfaz de usuario
│           ├── app.py, main.py, services.py
│           ├── img/
│           ├── Dockerfile, .dockerignore
│           └── pyproject.toml, uv.lock
│
├── .github/
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── mlflow.db
├── pyproject.toml
├── requirements.txt
└── uv.lock
```
