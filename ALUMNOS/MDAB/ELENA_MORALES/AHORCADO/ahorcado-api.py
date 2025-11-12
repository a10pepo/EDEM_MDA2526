import os   
import time
import requests
import psycopg

listapalabras = []
letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

url_api = f"https://rae-api.com/api/words/random"
database_url = os.getenv("DATABASE_URL")

def obtener_palabra_api():
    try:
        response = requests.get(url_api)
        response.raise_for_status()
        data = response.json()
        palabra = data.get("word", "").upper()
        return palabra
    except requests.RequestException as e:
        print(f"Error al obtener la palabra de la API: {e}")
        return None