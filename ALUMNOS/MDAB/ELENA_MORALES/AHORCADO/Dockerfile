# Fase 2: Automatización

FROM python:3.11-slim

WORKDIR /app

COPY palabras.txt  palabras.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "ahorcado.py"]

