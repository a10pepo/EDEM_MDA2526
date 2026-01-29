# Mastodon API Challenge — Status Publisher (CLI)

Pequeña aplicación de consola en Python que publica un status (toot) en Mastodon usando la API oficial y un Access Token (Bearer).

## Requisitos
- Python 3.9+ (recomendado)
- Una cuenta en una instancia de Mastodon
- Un Access Token con el scope `write:statuses`

## Crear y activar un entorno virtual
python -m venv .venv
source .venv/bin/activate   # macOS / Linux

## Instalar dependencias
pip install -r requirements.txt


## Configuración
Archivo.env que está en .gitignore con el token y URL 

## Uso
Para publicar en mastodon: 
"Python3 mastodon-post.py "Hola mundo soy Marthaa"

