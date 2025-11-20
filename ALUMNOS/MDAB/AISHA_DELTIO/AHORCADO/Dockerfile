FROM python:3.14-slim
WORKDIR /app
COPY . .
# Las librerias importadas vienen por defecto en la version de python instalda
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "ahorcado.py"]

# docker build -t ahorcado .
# docker run ahorcado palabras.txt