# Cargar las librerías necesarias para la app_inicial

# Librería de python, de código abierto, para usar la API de X. https://github.com/tweepy/tweepy
import tweepy 

# Librería de python, que se empleará para obtener las credenciales, se manera segura desde el archivo .env
import os 

# Credenciales de la API de X
consumer_key = os.getenv("X_API_KEY")
consumer_secret = os.getenv("X_API_SECRET")
access_token = os.getenv("X_ACCESS_TOKEN")
access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

# Bloque para crear la publicación.
try:
    # Creación del cliente, que pueda crear las publicaciones.
    client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
    )

    # Publicación. 
    response = client.create_tweet(
    text="Este es mi primera publicación, y ha sido generada a partir de un archivo python empleando la librería tweepy y la API de X. Todo esto en un entorno de Docker. La finalidad de esta primera publicación es aprender como funciona la API de X."
    )

    # Para conocer cual es el id de la publicación, se realiza el siguiente print.
    print(response.data["id"])

# Por si aparece algún error al realizar la publicación, se sabrá porque
except Exception as e:
    print(f"Erro al crear la publicación: {e}")