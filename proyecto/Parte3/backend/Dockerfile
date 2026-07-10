# Imagen base
FROM python:3.12-slim

# Instalar uv copiando el binario desde la imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar SOLO los archivos de definición de dependencias primero
COPY pyproject.toml uv.lock ./

# Instalar dependencias usando el lockfile exacto (reproducible)
RUN uv sync --frozen

# copiar el resto del código de la app
COPY main.py .
COPY models.py .
COPY generate_prediction.py .
COPY modelo_final.pkl .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
