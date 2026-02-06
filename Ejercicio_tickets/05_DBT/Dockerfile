# Usamos una imagen base de Python oficial y ligera
FROM python:3.10-slim

# Evita archivos temporales y buffer en logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /usr/app/dbt

# 1. Instalamos dependencias del sistema
# git es necesario si usas paquetes externos en packages.yml
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Instalamos dbt con el adaptador de Postgres
# Puedes fijar la versión si quieres estabilidad (ej: dbt-postgres==1.8.0)
RUN pip install --no-cache-dir dbt-postgres

# 3. Copiamos los archivos de tu proyecto al contenedor
COPY . .

# 4. Configuración vital:
# Le decimos a dbt que busque el archivo profiles.yml en la carpeta actual
ENV DBT_PROFILES_DIR=/usr/app/dbt

# 5. Instalamos dependencias de dbt (si tienes packages.yml)
# Si no tienes packages.yml, este paso no hará daño, pero asegurará que dbt funcione.
RUN dbt deps || echo "No packages.yml found, skipping dependencies"

# 6. Comando de inicio
# Usamos 'tail -f /dev/null' para mantener el contenedor encendido indefinidamente.
# Esto te permite hacer "docker exec" para lanzar dbt run cuando tú quieras.
CMD ["tail", "-f", "/dev/null"]