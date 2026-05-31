import os
import sys
from mastodon import Mastodon, MastodonError
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")
API_BASE_URL = os.getenv("MASTODON_API_BASE_URL")

def get_client():
    if not ACCESS_TOKEN or not API_BASE_URL:
        print(" Error: No se encontraron las credenciales en el archivo .env")
        sys.exit(1)
    
    return Mastodon(
        access_token=ACCESS_TOKEN,
        api_base_url=API_BASE_URL
    )

def validate_post(text):

    if not text or text.strip() == "":
        return False, "El mensaje no puede estar vacío."
    if len(text) > 500:
        return False, f"El mensaje es demasiado largo ({len(text)}/500)."
    return True, "OK"

def main():
    print("---  Mastodon API Publisher (EDEM Project) ---")
    
    text = input("Escribe lo que quieres publicar en Mastodon: ")
    
    valid, message = validate_post(text)
    if not valid:
        print(f" Error de validación: {message}")
        return

    try:
        print("conectando...")
        mastodon = get_client()
        response = mastodon.status_post(text)
        
        print("\n ¡Publicado correctamente!")
        
    except MastodonError as e:
        print(f"\n Error de la API: {e}")
    except Exception as e:
        print(f"\n Error inesperado: {e}")

if __name__ == "__main__":
    main()