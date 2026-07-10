# Imagen base
FROM python:3.12-slim

# Instalar uv copiando el binario desde la imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar SOLO los archivos de definición de dependencias primero
COPY pyproject.toml uv.lock ./

# Instalar dependencias
RUN uv sync --frozen

# Copiar el resto del código de la app 
COPY app.py .
COPY services.py .

EXPOSE 7860

CMD ["uv", "run", "python", "app.py"]