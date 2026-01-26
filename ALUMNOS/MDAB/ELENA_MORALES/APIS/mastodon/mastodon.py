import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# 1. Cargar variables de entorno
load_dotenv()

# Clase para manejar la conexión con Mastodon
class MastodonPublisher:
    def __init__(self):
        # Recuperamos las credenciales del archivo .env
        self.instance_url = os.getenv("MASTODON_INSTANCE")
        self.app_id = os.getenv("Id-aplicación")
        self.secret = os.getenv("Secreto")
        self.access_token = os.getenv("Token-acceso")
        self.client = None

    def authenticate(self):
        """Realiza la autenticación con la API de Mastodon"""
        try:
            # Verificamos las credenciales haciendo una petición de prueba
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = requests.get(
                f"{self.instance_url}/api/v1/accounts/verify_credentials",
                headers=headers
            )
            
            if response.status_code == 200:
                self.client = True
                user_data = response.json()
                print(f"Autenticación configurada correctamente")
                print(f"Usuario: @{user_data['username']}")
                return True
            else:
                print(f"Error en la autenticación: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error configurando el cliente: {e}")
            return False

    def post_toot(self, text):
        """Publica el toot en Mastodon"""
        if not self.client:
            print("Error: No estás autenticado")
            return

        try:
            # Agregamos la hora actual para evitar error de "Toot duplicado" al hacer pruebas
            now = datetime.now().strftime("%H:%M:%S")
            final_text = f"{text}\n\n[Publicado via API murciana a las {now}]"

            # Headers para la autenticación
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Datos del toot
            data = {
                "status": final_text,
                "visibility": "public"  # Opciones: public, unlisted, private, direct
            }

            # Llamada a la API para crear el toot
            response = requests.post(
                f"{self.instance_url}/api/v1/statuses",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                # Si todo va bien, obtenemos los datos del toot
                toot_data = response.json()
                toot_id = toot_data['id']
                toot_url = toot_data['url']
                
                print(f"\n¡Éxitooooo! Mi primer toot publicado desde Murcia usando la API de Mastodon 🐘")
                print(f"ID del Toot: {toot_id}")
                print(f"{toot_url}")
            else:
                print(f"\n Error de la API de Mastodon: {response.status_code}")
                print(f"Detalles: {response.text}")
            
        except requests.exceptions.RequestException as e:
            print(f"\n Error de la API de Mastodon, no pasa nada, keep on it: {e}")
            # Pista: Si sale error 401, suele ser problema con el token de acceso
        except Exception as e:
            print(f"\n Vaya, un error inesperado: {e}")

# --- Ejecución del programa (CLI) ---
if __name__ == "__main__":
    print("--- Bot Publicador para Mastodon ---")
    
    bot = MastodonPublisher()
    
    if bot.authenticate():
        user_text = input("\n Escribe lo que quieres publicar: ")
        
        if user_text.strip():
            bot.post_toot(user_text)
        else:
            print("No has escrito nada, me voy, sorry")