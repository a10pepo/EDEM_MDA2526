import tweepy
import os
from dotenv import load_dotenv

# 1. Cargar las claves del archivo .env
def cargar_credenciales():
    load_dotenv()
    credenciales = {
        "consumer_key": os.getenv("X_API_KEY"),
        "consumer_secret": os.getenv("X_API_SECRET"),
        "access_token": os.getenv("X_ACCESS_TOKEN"),
        "access_token_secret": os.getenv("X_ACCESS_TOKEN_SECRET"),
    }
    
    for nombre, valor in credenciales.items():
        if not valor:
            raise ValueError(f"Falta la credencial: {nombre}")
    return credenciales

# 2. Configuracion del cliente
def crear_cliente(credenciales):
    return tweepy.Client(
        consumer_key=credenciales["consumer_key"],
        consumer_secret=credenciales["consumer_secret"],
        access_token=credenciales["access_token"],
        access_token_secret=credenciales["access_token_secret"]
    )

# 3. Funcion de consola
def main():
    print("--- Bot Publicador para X ---")
    try:
        credenciales = cargar_credenciales()
        cliente = crear_cliente(credenciales)
        print("Autenticacion configurada correctamente")
        
        mensaje = input("\nEscribe lo que quieres publicar: ")
        
        if mensaje:
            print(f"\nPublicando: {mensaje}...")
            # Usamos user_auth=True para el plan gratuito
            cliente.create_tweet(text=mensaje, user_auth=True)
            print("Exito: Tweet publicado correctamente")
        else:
            print("Error: El mensaje esta vacio")
            
    except Exception as e:
        print(f"\nError de Twitter API: {e}")

if __name__ == "__main__":
    main()