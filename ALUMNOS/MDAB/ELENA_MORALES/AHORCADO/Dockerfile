# Fase 2: Automatización

FROM python:3.11-slim

WORKDIR /app

COPY palabras.txt  .
COPY ahorcado.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "ahorcado.py"]

