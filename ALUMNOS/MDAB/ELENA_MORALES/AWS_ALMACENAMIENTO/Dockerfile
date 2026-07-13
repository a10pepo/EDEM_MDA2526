# Imagen base ligera de Python
FROM python:3.12-slim

# No generar .pyc y mostrar logs sin buffer (útil en contenedores)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias primero (mejor uso de la caché de capas de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app ./app
COPY scripts ./scripts
COPY data ./data
COPY requirements.txt ./

# La API escucha en el puerto 8000
EXPOSE 8000

# Arrancar el servidor
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
