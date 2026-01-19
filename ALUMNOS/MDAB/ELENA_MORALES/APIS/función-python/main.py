import os
import tweepy
from dotenv import load_dotenv
from datetime import datetime

# 1. Cargar variables de entorno
load_dotenv()

# Clase para manejar la conexión con X
class XPublisher:
    def __init__(self):
        # Recuperamos las credenciales del archivo .env
        self.consumer_key = os.getenv("X_API_KEY")
        self.consumer_secret = os.getenv("X_API_SECRET")
        self.access_token = os.getenv("X_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
        self.client = None

    def authenticate(self):
        """Realiza la autenticación con la API v2 de X"""
        try:
            # Usamos 'Client' porque es el método para la API v2 
            self.client = tweepy.Client(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
            print("Autenticación configurada correctamente")
            return True
        except Exception as e:
            print(f"Error configurando el cliente: {e}")
            return False

    def post_tweet(self, text):
        """Publica el tweet en X"""
        if not self.client:
            print("Error: No estás autenticado")
            return

        try:
            # Agregamos la hora actual para evitar error de "Tweet duplicado" al hacer pruebas
            now = datetime.now().strftime("%H:%M:%S")
            final_text = f"{text}\n\n[Publicado via API murciana a las {now}]"

            # Llamada a la API para crear el tweet
            response = self.client.create_tweet(text=final_text)
            
            # Si todo va bien, obtenemos el ID del tweet
            tweet_id = response.data['id']
            print(f"\n¡Éxitooooo! Mi primer tweet publicado desde Murcia usando la API de X")
            print(f"ID del Tweet: {tweet_id}")
            print(f"https://twitter.com/user/status/{tweet_id}")
            
        except tweepy.TweepyException as e:
            print(f"\n Error de la API de X, no pasa nada, keep on it: {e}")
            # Pista: Si sale error 403, suele ser problema de permisos Read/Write en el portal
        except Exception as e:
            print(f"\n Vaya, un error inesperado: {e}")

# --- Ejecución del programa (CLI) ---
if __name__ == "__main__":
    print("--- Bot Publicador para X ---")
    
    bot = XPublisher()
    
    if bot.authenticate():
        user_text = input("\n Escribe lo que quieres publicar: ")
        
        if user_text.strip():
            bot.post_tweet(user_text)
        else:
            print("No has escrito nada, me voy, sorry")