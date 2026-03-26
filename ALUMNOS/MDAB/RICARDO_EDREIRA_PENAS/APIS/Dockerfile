# Imagen base de Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear carpeta de datos
RUN mkdir -p data

# Puerto de la aplicación
EXPOSE 5000

# Comando para ejecutar la app
CMD ["python", "run.py"]
