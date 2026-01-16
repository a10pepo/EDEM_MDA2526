FROM python:3.11-slim
WORKDIR /app

#Primero copiamos el archivo requirements así docker guarda el paso en memoria y si editamos el .py en un futuro no volverá a descargar las librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python","valenbisi_collector.py"]