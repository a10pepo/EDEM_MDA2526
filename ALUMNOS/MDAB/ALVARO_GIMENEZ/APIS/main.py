import requests
import os

#Guardamos el token de acceso en una variable de entorno para no filtrarla en git
TOKEN_ACCESO = os.getenv("MASTODON_TOKEN")
URL = "https://mastodon.social"

url = f"{URL}/api/v1/statuses"

#Pedimos al usuario que nos de el mensaje a postear como input
mensaje_usuario = input("Introduce el mensaje que quieres publicar en Mastodon: ")

#Configuramos la petición
headers = {
    "Authorization": f"Bearer {TOKEN_ACCESO}",
    "Content-Type": "application/json"
}

mensaje = {
    "status": mensaje_usuario,
    "visibility": "public"
}

#Hacemos pa petición incluyendo el manejo de errores
try:
    response = requests.post(url, json=mensaje, headers=headers, timeout=10)

    #Si recibimos un 200, el post se ha publicado OK
    if response.status_code == 200:
        print("Post publicado correctamente")
        print(response.json())

    #Los errores 400 están relacionados con problemas en la petición
    elif 400 <= response.status_code < 500:
        print(f"Error del cliente ({response.status_code})")

        if response.status_code == 401:
            print("No autorizado. Revisar token")
        elif response.status_code == 404:
            print("Endpoint no encontrado")
        elif response.status_code == 429:
            print("Demasiadas peticiones, epera un momento antes de volver a intentarlo")
        else:
            print("Petición incorrecta")

        print(response.text)

    #Los errores 500 vienen del lado del servidor 
    elif 500 <= response.status_code < 600:
        print(f"Error del servidor ({response.status_code})")
        print("El servidor de Mastodon no pudo procesar la petición")
        print(response.text)

#En caso de que no se cumpla nada de lo de arriba, mostramos una "respuesta inesperada"
except:
    print("Respuesta inesperada o error en la red")
