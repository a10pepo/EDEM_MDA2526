# Usamos Python 3.10 slim con Debian Bookworm
FROM python:3.10-slim

WORKDIR /usr/app

# Actualizamos repositorios e instalamos git y dependencias para PostgreSQL
RUN apt-get update && \
    apt-get install -y git libpq-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalamos dbt con el adaptador de PostgreSQL
RUN pip install --upgrade pip && \
    pip install dbt-postgres

# Comando para mantener el contenedor encendido
CMD ["tail", "-f", "/dev/null"]

