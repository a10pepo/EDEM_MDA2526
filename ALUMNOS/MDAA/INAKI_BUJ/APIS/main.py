import os
import tweepy
from dotenv import load_dotenv

##Cargamos las variables desde el archivo .env
load_dotenv()

def publicar_tweet():
    #Recuperamos las credenciales de forma segura
    api_key = os.getenv('X_API_KEY')
    api_secret = os.getenv('X_API_SECRET')
    access_token = os.getenv('X_ACCESS_TOKEN')
    access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')
    
    ##Configuramos el cliente de X (API v2)
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    contenido = "¡Lo logré! ⚡️ Si estás leyendo esto, mi script ha cobrado vida propia. 🤖🚀 #Python #XAPI #BuildInPublic"
    
    if len(contenido) > 280:
        print(f"❌ Error: El post supera los 280 caracteres (Total: {len(contenido)})")
        return # Detiene la ejecución antes de llamar a la API
    
    try:
        
        # Publicar
        print("Enviando post a X...")
        response = client.create_tweet(text=contenido)
        
        print(f"✅ Éxito. Post publicado. ID: {response.data['id']}")

    except tweepy.TweepyException as e:
        print(f"❌ Error de autenticación o límites: {e}")
    except Exception as e:
        print(f"⚠️ Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    publicar_tweet()
        