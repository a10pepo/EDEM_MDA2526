# 1. Usamos una imagen ligera de Python
FROM python:3.11-slim

# 2. Evitamos que Python genere archivos .pyc y permitimos logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalamos las dependencias primero (para aprovechar la caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto del código del proyecto
COPY app.py .
COPY scraper.py .

# 6. Exponemos el puerto que usa Flask
EXPOSE 5000

# 7. Ejecutamos la aplicación
CMD ["python", "app.py"]