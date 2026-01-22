import os
import sys
import logging
import tweepy
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def iniciar_bot():
    
    load_dotenv()
    
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    # 2. Verificamos que tengamos todas las llaves
    if not all([api_key, api_secret, access_token, access_token_secret]):
        logger.error("Faltan llaves en el archivo .env")
        sys.exit(1) # Detenemos el programa si hay un error grave

    # 3. Conectamos con la API de X
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    return client

def publicar_mensaje(client, texto):
    try:
        # Intentamos publicar el post
        response = client.create_tweet(text=texto)
        logger.info(f"✅ Se ha publicado tu post con éxito! ID: {response.data['id']}")
    except Exception as e:
        logger.error(f"❌ Error al publicar: {e}")


if __name__ == "__main__":
    bot_cliente = iniciar_bot()
    mensaje_para_x = "¡Hola! Este es mi primer tweet"
    publicar_mensaje(bot_cliente, mensaje_para_x)