import tweepy
import os
from dotenv import load_dotenv


# Función para cargar las variables de entorno y verificar que no estén vacías
def cargar_credenciales():

    load_dotenv()

    credenciales = {
        "consumer_key": os.getenv("TWITTER_CONSUMER_KEY"),
        "consumer_secret": os.getenv("TWITTER_CONSUMER_SECRET"),
        "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
        "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    }

    # Verificar que todas las credenciales estén presentes
    for nombre, valor in credenciales.items():
        if not valor:
            raise ValueError(f"Falta la credencial: {nombre}")

    return credenciales

# Función para crear y retornar el cliente autenticado
def crear_cliente(credenciales):

    cliente = tweepy.Client(
        consumer_key=credenciales["consumer_key"],
        consumer_secret=credenciales["consumer_secret"],
        access_token=credenciales["access_token"],
        access_token_secret=credenciales["access_token_secret"],
    )
    return cliente

# Función para publicar un tweet de un texto dado. Devuelve el ID del Tweet
def publicar_tweet(texto):

    if len(texto) > 280:
        raise ValueError(f"El texto supera los 280 caracteres: ({len(texto)} caracteres)")

    credenciales = cargar_credenciales()
    cliente = crear_cliente(credenciales)

    respuesta = cliente.create_tweet(text=texto)

    return respuesta.data["id"]

# Función principal para pedir al usuario que escriba el tweet y publicarlo

def main():

    print("=== Publicador de Tweets ===\n")

    tweet = input("Escribe tu tweet (max. 280 caracteres):\n> ")

    if not tweet.strip():
        print("Error: El tweet no puede estar vacío.")
        return

    print(f"\nCaracteres: {len(tweet)}/280")

    confirmar = input("\n¿Publicar este tweet? (s/n): ")

    if confirmar.lower() != "s":
        print("Publicación cancelada.")
        return

    try:
        tweet_id = publicar_tweet(tweet)
        print(f"\n¡Tweet publicado exitosamente!")
        print(f"ID del tweet: {tweet_id}")
        print(f"URL: https://twitter.com/i/web/status/{tweet_id}")
    except ValueError as e:
        print(f"\nError de validación: {e}")
    except tweepy.TweepyException as e:
        print(f"\nError de Twitter API: {e}")
    except Exception as e:
        print(f"\nError inesperado: {e}")


if __name__ == "__main__":
    main()
