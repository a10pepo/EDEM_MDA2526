import requests
import os

#Tomamos el token de acceso guardado en la variable de entorno para no filtrarla en git, asegurarse de confirgurarlo correctamente (ver el readme)
if not os.getenv("MASTODON_TOKEN"):
    print("Error: No se ha encontrado el token de acceso. Asegúrate de haberlo configurado en las variables de entorno.")
    exit()    

TOKEN_ACCESO=os.getenv("MASTODON_TOKEN")

URL = "https://mastodon.social"

url = f"{URL}/api/v1/statuses"

#Pedimos al usuario que nos de el mensaje a postear como input
mensaje_usuario = input("Introduce el mensaje que quieres publicar en Mastodon: ")

#Comprobamos que cumple la restricción de 1-280 caracteres
if len(mensaje_usuario) < 1 or len(mensaje_usuario) > 280:
   print("La longitud del mensaje debe ser entre 1 y 280 caracteres. Por favor, inténtalo de nuevo.")
   exit()

#Configuramos la petición
headers = {
    "Authorization": f"Bearer {TOKEN_ACCESO}",
    "Content-Type": "application/json"
}

mensaje = {
    "status": mensaje_usuario,
    "visibility": "public"
}

#Hacemos la petición incluyendo el manejo de errores
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
            print(response.text)

        elif response.status_code == 404:
            print("Endpoint no encontrado")
            print(response.text)

        elif response.status_code == 429:
            print("Demasiadas peticiones, espera un momento antes de volver a intentarlo")
            print(response.text)

        else:
            print("Petición incorrecta")
            print(response.text)

    #Los errores 500 vienen del lado del servidor 
    elif 500 <= response.status_code < 600:
        print(f"Error del servidor ({response.status_code})")
        print("El servidor de Mastodon no pudo procesar la petición")
        print(response.text)

#Este bloque captura errores relacionados con la red, como problemas de conexión, tiempo de espera, etc.
except requests.exceptions.RequestException as e:
    print(f"Error de red o comunicación: {e}")


