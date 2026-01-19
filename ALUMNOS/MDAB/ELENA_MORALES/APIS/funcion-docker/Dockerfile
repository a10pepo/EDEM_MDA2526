FROM python:3.9-slim
WORKDIR /app

# Evita que Python genere archivos .pyc y active el buffer de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY main.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "main.py"]