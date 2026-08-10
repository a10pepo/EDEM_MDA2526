FROM python:3.11-slim

WORKDIR /app

COPY ahorcado.py .
COPY palabras.txt .

ENTRYPOINT ["python", "ahorcado.py", "palabras.txt"]

# Para ejecutarlo, usar:
# docker run ahorcado