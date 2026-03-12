from mastodon import Mastodon
import os
import sys
from dotenv import load_dotenv

# 1. Cargar variables
load_dotenv()

def get_mastodon_client():
    token = os.getenv("MASTODON_ACCESS_TOKEN")
    base_url = os.getenv("MASTODON_BASE_URL")

    if not token or not base_url:
        print(" Error: Faltan variables en el .env")
        sys.exit(1)

    # Conexión a Mastodon (¡Es así de simple!)
    client = Mastodon(
        access_token=token,
        api_base_url=base_url
    )
    return client

def post_toot(text):
    mastodon = get_mastodon_client()

    try:
        print(f" Intentando publicar en Mastodon: '{text}'...")
        
        # En Mastodon los posts se llaman "toots"
        response = mastodon.toot(text)
        
        # Si funciona, nos devuelve info del post
        post_url = response['url']
        print(f" ¡Éxito! Toot publicado.")
        print(f" Ver aquí: {post_url}")

    except Exception as e:
        print(f" Error al publicar: {e}")

if __name__ == "__main__":
    print("--- PUBLICADOR DE MASTODON ---")
    texto = input("Escribe tu toot: ")
    
    # Mastodon permite hasta 500 caracteres
    if 1 <= len(texto) <= 500:
        post_toot(texto)
    else:
        print(" El texto está vacío o es demasiado largo (>500).")
        
