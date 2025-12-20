# CAMBIO IMPORTANTE: Usamos 'slim' a secas, que usa la versión más moderna de Debian (Bookworm)
FROM python:3.10-slim

WORKDIR /usr/app

# Actualizamos repositorios e instalamos git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

# Instalamos dbt con el adaptador de DuckDB
RUN pip install --upgrade pip && \
    pip install dbt-duckdb

# Comando para mantener el contenedor encendido
CMD ["tail", "-f", "/dev/null"]