import os
import tweepy
from dotenv import load_dotenv
from datetime import datetime

# Cargamos las llaves desde el archivo .env extraídas del developer de X 
# con permisos de lectura y escritura

load_dotenv()

# Clase para manejar la conexión con X
class XPublisher:
    def __init__(self):
        # Con getenv leemos la api key y la api key secret del .env
        self.consumer_key = os.getenv("API_KEY")
        self.consumer_secret = os.getenv("API_KEY_SECRET")
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
        self.client = None

    def authenticate(self):
        """Realiza la autenticación con la API v2"""
        try:
            # Para API V2 utilizamos "client" 
            self.client = tweepy.Client(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
            print("Autenticación exitosa")
            return True
        except Exception as e:
            print(f"Error en la configuración: {e}")
            return False

    def post_tweet(self, text):
        """Publica el tweet"""
        if not self.client:
            print("Error: Falta autenticación")
            return

        try:
# Agregamos la hora actual
            now = datetime.now().strftime("%H:%M:%S")
            final_text = f"{text}\n\n[Publicando a las... {now}]"

# Llamada a la API para crear el tweet
            response = self.client.create_tweet(text=final_text)

 # Deberíamos obtener el ID del tweet
            tweet_id = response.data['id']
            print(f"El ID del Tweet es: {tweet_id}")

        except tweepy.TweepyException as e:
            print(f"\n ❌ Error al publicar: {e}")
        except Exception as e:
            print(f"\n ❌ Error al publicar: {e}")

# --- Ejecución del programa ---
if __name__ == "__main__":
    print("--- Bot publica tweets ---")

    bot = XPublisher()

    if bot.authenticate():
        user_text = input("\n ¿Qué estás pensando?: ")

        if user_text.strip():
            bot.post_tweet(user_text)
        else:
            print("Gracias por nada")