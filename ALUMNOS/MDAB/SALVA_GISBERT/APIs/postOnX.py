import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import os   

# Carga las variables del archivo .env
load_dotenv()

# Obtiene las claves de las variables de entorno
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

def post_on_x(message):
    url = "https://api.x.com/2/tweets"
    
    # Configuramos la autenticación OAuth 1.0a
    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "text": message
    }
    
    # Realizamos la petición POST incluyendo el objeto 'auth'
    response = requests.post(url, headers=headers, json=data, auth=auth)
    
    return response.json()

if __name__ == "__main__":
    message = "Hola X! Publicando con la URL directa y requests."
    result = post_on_x(message)
    print(result)