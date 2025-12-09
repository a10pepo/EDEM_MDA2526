Clases de DBT

Para seguir las clases será necesario instalar cierto software. El repositorio está pensado para instalar las dependencias con `uv`.
Podeis instalar `uv` con `pip install uv`. Una vez instalado, podeis ejecutar `uv sync` para que os instale los paquetes necesarios (especificados en el `pyproject.toml`).

Además necesitaremos una base de datos. En este caso usaremos duckdb. Podeis ver en su [documentación](https://duckdb.org/install/?platform=macos&environment=cli) las distintas formas de instalarlo.

Si os reconoce en la terminal los comandos `uv` y `duckdb`, significa que está todo bien instalado.