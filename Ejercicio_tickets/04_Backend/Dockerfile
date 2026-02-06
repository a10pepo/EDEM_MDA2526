# Imagen ligera de Python
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y asegura que los logs se vean en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalar dependencias de sistema para Postgres (psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar requerimientos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Exponer el puerto de la API
EXPOSE 8000

# Ejecutar Uvicorn (el servidor web)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
