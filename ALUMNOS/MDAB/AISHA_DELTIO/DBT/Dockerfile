FROM python:3.12-slim

# 1. Instalamos utilidades del sistema
# Añadimos 'curl' y 'unzip' que son necesarios para bajar DuckDB
RUN apt-get update && apt-get install -y \
    git \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalamos 'uv' (Gestor de paquetes de Python)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 3. Instalamos DuckDB CLI (La herramienta de terminal)
# Esto descarga el ejecutable oficial y lo pone en la carpeta de programas
RUN curl -L https://github.com/duckdb/duckdb/releases/download/v1.1.3/duckdb_cli-linux-amd64.zip -o duckdb_cli.zip \
    && unzip duckdb_cli.zip \
    && mv duckdb /usr/local/bin/ \
    && chmod +x /usr/local/bin/duckdb \
    && rm duckdb_cli.zip

# 4. Configuración del proyecto
WORKDIR /usr/app

# Copiamos los archivos de dependencias
COPY pyproject.toml uv.lock ./

# Creamos el entorno virtual e instalamos las dependencias de Python
RUN uv sync --frozen

# Aseguramos que el entorno virtual esté en el PATH
ENV PATH="/usr/app/.venv/bin:$PATH"

# Mantenemos el contenedor encendido
CMD ["tail", "-f", "/dev/null"]