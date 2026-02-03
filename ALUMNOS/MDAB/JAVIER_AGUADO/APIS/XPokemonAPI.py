import os
import time
import tweepy
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Credenciales de la API de Twitter desde variables de entorno
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Optional: Check if running in development mode
APP_MODE = os.getenv('APP_MODE', 'production')  # default to 'production'

# Tiempo en segundos entre cada publicación
TIEMPO_ESPERA = 90 * 60  # 90 minutos = 17 tweets al dia (máx permitido por Twitter)

def publicar_tweet(msg, imagen_url):
    # Autenticación con la API de Twitter
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)     
    api = tweepy.API(auth)

    # Autenticación con la API de Twitter
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET_KEY,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

    # Publicar el tweet
    if APP_MODE == 'production':
        try:
            # Descargar la imagen en local
            with open("temp.jpg", "wb") as f:
                f.write(requests.get(imagen_url, timeout=10).content)
            # Subir la imagen a Twitter
            media = api.media_upload("temp.jpg")
            # Publicar el tweet 
            response = client.create_tweet(text=msg, media_ids=[media.media_id])
            # Guarda local del tweet publicado
            with open("mis_tweets.json", "a", encoding="utf-8") as f:
                f.write(str(response.data))
            print(f"Tweet publicado con éxito. ID: {response.data['id']}")
        except Exception as e:
            print(f"Error en la publicación: {e}")
    else:
        print(f"[DEV MODE] Tweet a publicar: {msg}\nImagen URL: {imagen_url}")

def publicar_tweet_pokemon(pokemon_id):
    # Obtener datos del Pokémon desde la API de PokéAPI
    respuesta = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}', timeout=10)
    if respuesta.status_code != 200:
        print(f"No se pudo obtener el Pokémon con ID {pokemon_id}")
        return
    datos_pokemon = respuesta.json()

    # Procesar los datos del Pokémon
    # Nombre
    nombre = datos_pokemon['name'].capitalize()

    # Tipos
    tipos = []
    for tipo in datos_pokemon['types']:
        tipos.append(tipo['type']['name'].capitalize())

    # Imagen
    # imagen_url = datos_pokemon['sprites']['front_default']
    # Mejor imagen extraída desde la web oficial de Pokémon
    pokemon_id_text = ''
    if pokemon_id < 10:
        pokemon_id_text = '00'
    elif pokemon_id < 100:
        pokemon_id_text = '0'
    imagen_url = f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{pokemon_id_text}{pokemon_id}.png"

    # Debilidades
    debilidades = []
    for tipo in tipos:
        try:
            respuesta_tipo = requests.get(f'https://pokeapi.co/api/v2/type/{tipo.lower()}', timeout=10)
            if respuesta_tipo.status_code == 200:
                datos_respuesta_tipo = respuesta_tipo.json()
                for daño in datos_respuesta_tipo['damage_relations']['double_damage_from']:
                    debilidades.append(daño['name'].capitalize())
        except Exception as e:
            print(f"Error al obtener debilidades para el tipo {tipo}: {e}")
    
    # Pokemon ejemplos de debilidades
    ejemplos_debilidades = []
    for debilidad in debilidades:
        try:
            respuesta_tipo = requests.get(f'https://pokeapi.co/api/v2/type/{debilidad.lower()}', timeout=10)
            if respuesta_tipo.status_code == 200:
                datos_respuesta_tipo = respuesta_tipo.json()
                pokemon = datos_respuesta_tipo['pokemon'][0]
                nombre_pokemon = pokemon['pokemon']['name'].capitalize()
                pokemon_data = requests.get(pokemon['pokemon']['url']).json()
                pokemon_id_aux = pokemon_data['id']
                ejemplos_debilidades.append(f"{nombre_pokemon} [{pokemon_id_aux}]")
        except Exception as e:
            print(f"Error al obtener ejemplos de debilidades para {debilidad}: {e}")

    # Fortalezas
    fortalezas = []
    for tipo in tipos:
        try:
            respuesta_tipo = requests.get(f'https://pokeapi.co/api/v2/type/{tipo.lower()}', timeout=10)
            if respuesta_tipo.status_code == 200:
                datos_respuesta_tipo = respuesta_tipo.json()
                for daño in datos_respuesta_tipo['damage_relations']['half_damage_from']:
                    fortalezas.append(daño['name'].capitalize())
        except Exception as e:
            print(f"Error al obtener fortalezas para el tipo {tipo}: {e}")

    # Pokemon ejemplos de fortalezas
    ejemplos_fortalezas = []
    for fortaleza in fortalezas:
        try:
            respuesta_tipo = requests.get(f'https://pokeapi.co/api/v2/type/{fortaleza.lower()}', timeout=10)
            if respuesta_tipo.status_code == 200:
                datos_respuesta_tipo = respuesta_tipo.json()
                pokemon = datos_respuesta_tipo['pokemon'][0]
                nombre_pokemon = pokemon['pokemon']['name'].capitalize()
                pokemon_data = requests.get(pokemon['pokemon']['url']).json()
                pokemon_id_aux = pokemon_data['id']
                ejemplos_fortalezas.append(f"{nombre_pokemon} [{pokemon_id_aux}]")
        except Exception as e:
            print(f"Error al obtener ejemplos de fortalezas para {fortaleza}: {e}")

    # Construir el mensaje del tweet
    msg = f"¡Conoce a {nombre} [{pokemon_id}]!\nTipo: {', '.join(tipos)}\n\nDebilidades: {', '.join(debilidades)}\nEjemplos: {', '.join(ejemplos_debilidades) if ejemplos_debilidades else 'Ninguno'}\n\nFortalezas: {', '.join(fortalezas)}\nEjemplos: {', '.join(ejemplos_fortalezas) if ejemplos_fortalezas else 'Ninguno'}"

    # Asegurarse de que el mensaje no exceda el límite de caracteres de Twitter
    if len(msg) > 280:
        msg = msg[:277] + "..."
        
    # Publicar el tweet
    publicar_tweet(msg, imagen_url)

# función que accede a la API de Twitter y obtiene el último tweet publicado en la cuenta de las credenciales de acceso
def obtener_siguiente_pokemon_id():
    archivo = "last_pokemon_id.txt"
    
    try:
        # Leer el último ID guardado
        with open(archivo, "r") as f:
            contenido = f.read().strip()
            if not contenido:
                last_pokemon_id = 0
            else:
                last_pokemon_id = int(contenido)
        
        # Calcular el siguiente ID
        siguiente_id = last_pokemon_id + 1
        
        # Guardar el siguiente ID para la próxima ejecución
        with open(archivo, "w") as f:
            f.write(str(siguiente_id))
        
        return siguiente_id
        
    except FileNotFoundError:
        print(f"Archivo {archivo} no encontrado. Iniciando desde Pokémon ID 1")
        with open(archivo, "w") as f:
            f.write("1")
        return 1
    except ValueError:
        print(f"Contenido inválido en {archivo}. Reiniciando desde Pokémon ID 1")
        with open(archivo, "w") as f:
            f.write("1")
        return 1

def main():
    try:
        if not all([API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
            raise ValueError("Faltan variables de entorno requeridas. Verifica tu archivo .env.")
        num_pokemon = obtener_siguiente_pokemon_id()
        while True:
            publicar_tweet_pokemon(num_pokemon)
            num_pokemon += 1
            time.sleep(TIEMPO_ESPERA)
    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario (Ctrl+C)")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()