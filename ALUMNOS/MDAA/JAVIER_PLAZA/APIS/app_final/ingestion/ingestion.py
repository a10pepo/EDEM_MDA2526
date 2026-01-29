import requests
import os
import time

# Tiempo de espera para que tanto la base de datos como la API esten completamente operativas.
time.sleep(60)

url_frutas = "https://fruityvice.com/api/fruit/all"
url_base_api = "http://api:5000"

# Usuario y contraseña para la ingestión de los datos en la base de datos.
usuario = os.getenv("USUARIO_API_INGESTION")
contrasena = os.getenv("CONTRASENA_API_INGESTION")

# Función para registrar al usuario.
def registrar_usuario():
    # POST para crear el usuario con su contraseña.
    respuesta_usuario = requests.post(f"{url_base_api}/registrar_usuarios", json = {
        "usuario": usuario,
        "contrasena": contrasena
    })

    # Para controlar si el usuario se ha creado correctamente o no.
    if respuesta_usuario.status_code == 201:
        print(f"El usuario ha sido creado correctamente")
        return 
    else: 
        print(f"El usuario no se ha creado por el error: {respuesta_usuario.status_code}")

# Función para obtener el token.
def obtener_token():
    # POST para obtener el token para poder hacer la ingestión.
    respuesta_token = requests.post(f"{url_base_api}/iniciar_sesion", auth = (usuario, contrasena))

    # Para controlar si se ha creado el token, si no se crea, devuelve un error. 
    if respuesta_token.status_code == 200:
        print("El token ha sido generado correctamente")

        # Para poder emplear el token se guarda en la variable token.
        respuesta_token = respuesta_token.json()
        token = respuesta_token.get("token_acceso")
        return token
    else:
        print(f"Ha ocurrido un error en la creación del token: {respuesta_token.status_code}")
        return

# Función para poder ingestar los datos en la base de datos.
def ingestar_datos():
    # Activación de la función para registrar al usuario.
    registrar_usuario()

    # Obtener el token para poder ingestar
    token = obtener_token()

    # Obtener los datos de la API donde están los datos de las frutas (SE PUEDEN METER TANTOS DATOS COMO SE QUIERA)
    respuesta_url_frutas = requests.get(url_frutas)
    datos_fruta = respuesta_url_frutas.json()

    # Bucle para ingestar linea a linea los datos de los alimentos, en este caso unicamente frutas. 
    contador = 0
    for fruta in datos_fruta:
        nutrientes = fruta.get("nutritions")
        info_fruta = {
            "nombre": fruta.get("name"),
            "tipo": "fruta",
            "calorias": nutrientes.get("calories"),
            "grasas": nutrientes.get("fat"),
            "azucar": nutrientes.get("sugar"),
            "carbohidratos": nutrientes.get("carbohydrates"),
            "proteina": nutrientes.get("protein")
        }
        try:
            # Realizar el post para introducir los datos en la base de datos. 
            respuesta = requests.post(f"{url_base_api}/insertar_alimentos", json = info_fruta, headers = {
                "Authorization": f"Bearer {token}"
            })
            if respuesta.status_code in [200, 201]:
                print(f"Insertando en la base de datos: {fruta.get("name")}")
                contador += 1
            else:
                print(f"Fallo ingestando la fruta {fruta.get('name')}: {respuesta.status_code}")
        except Exception as e: 
            print(f"Ha ocurrido un error: {e}")

if __name__ == "__main__":
    ingestar_datos()


