
import os
import tweepy
from dotenv import load_dotenv
import time
import requests
load_dotenv()



def request_option():
    option =input("""
      Selecciona una opción: 
      1) Escribir un post en X
      2) Escuchar la API de terremotos
      3) Salir
      Tu elección: """)
    option_list = ['1', '2', '3']

    if option not in option_list:
        print("Opción inválida. Por favor, inténtalo de nuevo")
        return request_option()
    return option

def post_tweet(content):
    try:
    
        print("Posting en X...")
        client = tweepy.Client(
            consumer_key=os.getenv("X_API_KEY"),
            consumer_secret=os.getenv("X_API_SECRET"),
            access_token=os.getenv("X_ACCESS_TOKEN"),
            access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
        )
        response = client.create_tweet(text=content)

        print("✅ Post publicado! Tweet ID:", response.data['id'])
    except Exception as e:
        print(f"⚠️ Error al publicar en X: {e}")



# Funciones de la API de terremotos

def monitor_terremotos():
    """
    Función 1: Escucha la API cada minuto.
    """
    magnitud_minima = float(input("Indica el umbral de magnitud para generar el aviso (0-10): "))
    print(f"Escuchando la API... (Ctrl+C para parar)")

    id_ultimo_terremoto = None

    while True:
        try:
            
            url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
            datos = requests.get(url).json()            

            terremoto = datos['features'][0]
            mag_actual = terremoto['properties']['mag']
            id_actual = terremoto['id']

            if mag_actual >= magnitud_minima and id_actual != id_ultimo_terremoto:
                print(f"Nuevo terremoto detectado de magnitud {mag_actual}")
                id_ultimo_terremoto = id_actual

                menu_alerta(terremoto)


            else:
                print(f"Nada nuevo... (Último: {mag_actual})")


            time.sleep(60)

        except Exception as e:
            print(f"Error conectando con la API: {e}. Reintentando en 1 min...")
            time.sleep(60)

def menu_alerta(terremoto):

    mag = terremoto['properties']['mag']
    lugar = terremoto['properties']['place']
    
    print(f"\n⚠️ ¡TERREMOTO DETECTADO de magnitud {mag} en {lugar}")
    
    opcion = input("""
    1) Publicar Alerta Automática en X
    2) Publicar un mensaje personalizado en X 
    3) Ignorar y seguir escuchando la API
    4) Salir
    Elige: """)

    if opcion == '1':
        mensaje = f"🚨 Terremoto de {mag} en {lugar}. #Earthquake"
        post_tweet(mensaje)
        return True 

    elif opcion == '2':
        mensaje = input("Escribe tu tweet: ")
        post_tweet(mensaje)
        return True 

    elif opcion == '3':
        print("Ignorando...")
        return True 

    elif opcion == '4':
        return False #Salir




if __name__ == "__main__":
    while True:
        user_option = request_option()

        if user_option == '1':
            content = input("Escribe el contenido del post: ")
            if len(content) > 280:
                print("Error: El contenido excede los 280 caracteres. Por favor, inténtalo de nuevo.")
                continue
            if len(content) == 0:
                print("Error: El contenido no puede estar vacío. Por favor, inténtalo de nuevo.")
                continue
            post_tweet(content)

        elif user_option == '2':
            monitor_terremotos()

        elif user_option == '3':
            print("Exiting the app. Bye!")
            break