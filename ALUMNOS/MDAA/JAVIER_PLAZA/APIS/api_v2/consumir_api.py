import requests
import random

# URL de base para todas las peticiones de la API creada.
url_base = "http://api:5000"

# Función para obtener la información de la fruta. 
def obtener_fruta():

    # Usuario y contraseña para la creación de un usuarion en la dirección "/usuarios".
    usuario_py = "admin_python"
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
    respuesta_login = requests.post(f"{url_base}/login", auth = (usuario_py, contraseña_py))

    # Para controlar si el token se ha creado o no. Si no se crea. devuelve el error. 
    if respuesta_login.status_code == 200:
        print("El token ha sido creado correctamente")

        # Para poder emplear el token para obtener la fruta, se guarda en al variable token.
        respuesta_login = respuesta_login.json()
        token = respuesta_login.get("token_acceso")
    else: 
        print(f"Ha ocurrido un error al generar el token. Error: {respuesta_login.status_code}")
        return

    # Como la API para obtener la información nutricional de la fruta aleatoria puede dar error en las primeras peticiones, se mete un bucle infinito que parará cuando obtenga la información de una fruta. 
    while True: 

        # GET para obtener la información nutricional de una fruta aleatoria.
        respuesta_fruta = requests.get(f"{url_base}/fruta", headers = {
            "Authorization": f"Bearer {token}"
            })

        # Para controlar si la API nos trae la información y además si trae la información nutricional de la fruta, muestra dicha información por consola. 
        if respuesta_fruta.status_code == 200:
            respuesta_fruta = respuesta_fruta.json()
            nombre = respuesta_fruta.get("nombre")
            calorias = respuesta_fruta.get("calorias")
            grasa = respuesta_fruta.get("grasa")
            azucar = respuesta_fruta.get("azucar")
            carbohidratos = respuesta_fruta.get("carbohidratos")
            proteina = respuesta_fruta.get("proteina")
            print(f"La fruta obtenida aleatoriamente es {nombre}, y su información nutricional es la siguiente:")
            print(f"    - Calorias: {calorias}")
            print(f"    - Grasa: {grasa}")
            print(f"    - Azucar: {azucar}")
            print(f"    - Carbohidratos: {carbohidratos}")
            print(f"    - Proteina: {proteina}")
            break
        else: 
            print(f"Ha ocurrido un error al mostrar la información nutricional de una fruta. Error: {respuesta_fruta.status_code}")

if __name__ == '__main__':
    obtener_fruta()

