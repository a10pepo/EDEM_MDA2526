FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
# (libpq-dev y gcc son a menudo necesarios para compilar el driver si no se usa el binario)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY valenbisi_collector.py ./

CMD ["python", "valenbisi_collector.py"]