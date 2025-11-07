# Fase 2: Automatización

FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "ahorcado.py"]

# EXTRA: ¿Podrías hacer que palabras.txt sea un parámetro del contenedor?
