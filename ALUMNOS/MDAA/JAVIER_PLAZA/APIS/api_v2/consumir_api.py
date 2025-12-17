import requests
import random

# URL de base para todas las peticiones de la API creada.
url_base = "http://127.0.0.1:5000"

# Función para obtener la información de la fruta. 
def obtener_fruta():

    # Usuario y contraseña para la creación de un usuarion en la dirección "/usuarios".
    usuario_py = random.choice
    contraseña_py = usuario_py

    # POST para poder crear un usuario con su contraseña.
    respuesta_usuarios = requests.post(f"{url_base}/usuarios", json = {
        "usuario": usuario_py,
        "contraseña": contraseña_py
    })

    # Para controlar si el usuario se ha creado o no. Si no se crea, devuelve el error.
    if respuesta_usuarios.status_code == 201:
        print(f"El usuario {usuario_py}, ha sido creado correctamente")
    else: 
        print(f"El usuario {usuario_py}, no se ha creado por el error: {respuesta_usuarios.status_code}")
        return 

    # POST para poder obtener un token para poder obtener la información nutricional de una fruta.
    respuesta_login = requests.post(f"{url_base}/usuarios", json = {
        "usuario": usuario_py,
        "contraseña": contraseña_py
    })

    # Para controlar si el token se ha creado o no. Si no se crea. devuelve el error. 
    if respuesta_login.status_code == 200:
        print("El token ha sido creado correctamente")
    else: 
        print(f"Ha ocurrido un error al generar el token. Error: {respuesta_login.status_code}")
        return

    

