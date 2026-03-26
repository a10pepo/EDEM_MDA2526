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


    if not all([api_key, api_secret, access_token, access_token_secret]):
        logger.error("Faltan llaves en el archivo .env")
        sys.exit(1) 

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    return client

def publicar_mensaje(client, texto):

    if len(texto) == 0:
        print("El mensaje está vacío, no se puede publicar.")
        return
    
    if len(texto) > 280:
        print("El mensaje es demasiado largo para X.")
        return
    
    print(f"Enviando post: {texto}")
    
    try:
        respuesta = client.create_tweet(text=texto)
        
        print(" ¡Publicado correctamente!")
        print("ID del post:", respuesta.data['id'])
    
    except Exception as e:
        error_texto = str(e) 
        
        print(" Ha ocurrido un error al intentar publicar:")
        
        if "401" in error_texto:
            print("- Error 401: Las llaves del .env están mal.")
        elif "402" in error_texto:
            print("- Error 402: No tienes créditos (Payment Required).")
        elif "403" in error_texto:
            print("- Error 403: No tienes permisos de escritura en X.")
        else:
            print("- Detalle:", error_texto)

if __name__ == "__main__":
    bot_cliente = iniciar_bot()
    mensaje_para_x = "¡Hola! Este es mi primer tweet"
    publicar_mensaje(bot_cliente, mensaje_para_x)