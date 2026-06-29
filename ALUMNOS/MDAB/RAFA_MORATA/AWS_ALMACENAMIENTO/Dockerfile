FROM python:3.12-slim

# Dependencias del sistema para compilar/conectar psycopg2 y red
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias primero para aprovechar la caché de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del pipeline
COPY initial_info.py main.py ./
COPY pipeline ./pipeline

# Por defecto ejecuta el pipeline completo; se puede sobreescribir:
#   docker run --env-file .env imagen postgres
ENTRYPOINT ["python", "main.py"]
CMD ["all"]
